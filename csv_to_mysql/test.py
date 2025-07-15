import argparse
import logging
import math
import os
import random
import sys
from move_data import parse_go_annotations

import mysql.connector
import pandas as pd
from mysql.connector import Error

# --- 与主脚本相同的配置和辅助函数 ---

def setup_logger():
    """配置一个简单的日志记录器，仅输出到控制台"""
    logger = logging.getLogger('gene_tester')
    logger.setLevel(logging.INFO)
    
    # 防止重复添加处理器
    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger

logger = setup_logger()

def find_csv_files(folder_paths: list[str]) -> list[str]:
    """查找给定文件夹中的所有CSV文件，返回文件路径列表"""
    csv_files = []
    for folder_path in folder_paths:
        if not os.path.exists(folder_path):
            logger.warning(f"路径不存在: {folder_path}")
            continue
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith('.csv'):
                    full_path = os.path.join(root, file)
                    csv_files.append(full_path)
    logger.info(f"在指定路径下共找到 {len(csv_files)} 个CSV文件")
    return csv_files

def create_db_connection(host: str, user: str, password: str, database: str) -> mysql.connector.MySQLConnection | None:
    """创建数据库连接（测试脚本只连接，不创建）"""
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if connection.is_connected():
            logger.info(f"成功连接到数据库: {database}")
            return connection
    except Error as e:
        logger.error(f"数据库连接失败: {e}")
        return None

# --- 测试核心逻辑 ---

def get_gene_id(cursor: mysql.connector.cursor.MySQLCursor, gene_symbol: str) -> int | None:
    """从数据库中查询基因的ID"""
    cursor.execute("SELECT gene_id FROM genes WHERE symbol = %s", (gene_symbol,))
    result = cursor.fetchone()
    return result[0] if result else None

def test_random_records(connection: mysql.connector.MySQLConnection, csv_files: list[str], 
                        num_files_to_test: int, num_records_per_file: int, verbose: bool):
    """
    随机抽查记录进行验证的核心函数。
    此版本已包含对GSE数据存储正确性的验证。
    """
    if verbose:
        logger.info(f"测试开始：将从 {num_files_to_test} 个文件中，每个文件抽查 {num_records_per_file} 条记录。")
    
    files_to_sample = min(num_files_to_test, len(csv_files))
    if files_to_sample == 0:
        logger.warning("没有找到任何CSV文件可供测试。")
        return

    selected_files = random.sample(csv_files, files_to_sample)
    
    cursor = connection.cursor()
    total_checked = 0
    success_count = 0
    failures = []

    FLOAT_PRECISION = 4

    for csv_file in selected_files:
        try:
            if verbose:
                logger.info(f"--- 正在测试文件: {os.path.basename(csv_file)} ---")
            df = pd.read_csv(csv_file)
            
            # 预先找到文件中的GSE列
            gse_columns = [col for col in df.columns if col.startswith('GSE')]

            records_to_sample = min(num_records_per_file, len(df))
            if records_to_sample == 0:
                if verbose:
                    logger.warning(f"文件 {os.path.basename(csv_file)} 为空，已跳过。")
                continue

            sampled_rows = df.sample(n=records_to_sample)
            
            for _, row in sampled_rows.iterrows():
                total_checked += 1
                gene_a_sym, gene_b_sym = row['GeneA'], row['GeneB']
                
                gene_a_id = get_gene_id(cursor, gene_a_sym)
                gene_b_id = get_gene_id(cursor, gene_b_sym)
                
                if not gene_a_id or not gene_b_id:
                    failure_msg = f"验证失败: 基因 '{gene_a_sym}' 或 '{gene_b_sym}' 在数据库中未找到。"
                    logger.error(failure_msg)
                    failures.append(f"文件'{os.path.basename(csv_file)}'中的记录 ({gene_a_sym}, {gene_b_sym}): {failure_msg}")
                    continue
                
                norm_a_id, norm_b_id = min(gene_a_id, gene_b_id), max(gene_a_id, gene_b_id)
                
                # --- [核心修改 1] ---
                # 查询时一并获取 gse_source 和 gse_data
                cursor.execute(
                    "SELECT prediction_score, binary_prediction, label, gse_source, gse_data FROM predictions WHERE gene_a_id = %s AND gene_b_id = %s",
                    (norm_a_id, norm_b_id)
                )
                db_result = cursor.fetchone()
                
                if not db_result:
                    failure_msg = f"验证失败: 基因对 ({gene_a_sym}, {gene_b_sym}) 在 predictions 表中未找到。"
                    logger.error(failure_msg)
                    failures.append(f"文件'{os.path.basename(csv_file)}'中的记录 ({gene_a_sym}, {gene_b_sym}): {failure_msg}")
                    continue

                db_score, db_binary, db_label, db_gse_source, db_gse_data = db_result
                
                # --- [核心修改 2] ---
                # 在测试端，模拟主脚本的GSE数据处理逻辑，生成期望值
                gse_sources_found = [col for col in gse_columns if pd.notna(row.get(col)) and str(row.get(col)).strip()]
                gse_data_found = [str(row.get(col)) for col in gse_sources_found]
                
                expected_gse_source = ",".join(gse_sources_found) if gse_sources_found else None
                expected_gse_data = "|".join(gse_data_found) if gse_data_found else None

                # 验证其他字段
                csv_score = float(row['Prediction'])
                csv_binary = int(row['BinaryPrediction'])
                csv_label = row['label'] if pd.notna(row['label']) else None

                errors = []
                if round(csv_score, FLOAT_PRECISION) != round(db_score, FLOAT_PRECISION):
                    errors.append(f"Prediction分数不匹配 (CSV: {csv_score}, DB: {db_score})")
                if csv_binary != db_binary:
                    errors.append(f"BinaryPrediction不匹配 (CSV: {csv_binary}, DB: {db_binary})")
                if csv_label != db_label:
                    errors.append(f"label不匹配 (CSV: '{csv_label}', DB: '{db_label}')")
                
                # --- [核心修改 3] ---
                # 添加对GSE字段的验证
                if expected_gse_source != db_gse_source:
                    errors.append(f"gse_source不匹配 (CSV: '{expected_gse_source}', DB: '{db_gse_source}')")
                if expected_gse_data != db_gse_data:
                    errors.append(f"gse_data不匹配 (CSV: '{expected_gse_data}', DB: '{db_gse_data}')")

                if errors:
                    failure_msg = "验证失败: " + " | ".join(errors)
                    logger.error(f"记录 ({gene_a_sym}, {gene_b_sym}) {failure_msg}")
                    failures.append(f"文件'{os.path.basename(csv_file)}'中的记录 ({gene_a_sym}, {gene_b_sym}): {failure_msg}")
                else:
                    if verbose:
                        logger.info(f"记录 ({gene_a_sym}, {gene_b_sym}) 验证成功。")
                    success_count += 1
        
        except FileNotFoundError:
            logger.error(f"测试失败: 文件未找到 {csv_file}")
        except Exception as e:
            logger.error(f"测试文件 {os.path.basename(csv_file)} 时发生意外错误: {e}", exc_info=True)

    # --- 最终报告 (代码不变) ---
    print("\n" + "="*50)
    print(" " * 18 + "预测记录测试报告")
    print("="*50)
    print(f"总共检查记录数: {total_checked}")
    print(f"  - \033[92m验证成功\033[0m: {success_count}")
    print(f"  - \033[91m验证失败\033[0m: {len(failures)}")
    print("="*50)

    if failures:
        print("\n\033[91m失败记录详情:\033[0m")
        for i, f in enumerate(failures, 1):
            print(f"{i}. {f}")
    
    if total_checked > 0 and len(failures) == 0:
        print("\n\033[92m所有抽样的预测记录测试均已通过！\033[0m")

def test_go_annotations(connection: mysql.connector.MySQLConnection, csv_files: list[str], 
                        num_genes_to_test: int, verbose: bool):
    """
    随机抽查基因，验证其GO注释是否正确导入。
    此版本已添加 verbose 开关来控制日志输出的详细程度。
    """
    if verbose:
        logger.info("\n" + "="*20 + " GO注释验证开始 " + "="*20)
    
    if verbose:
        logger.info("正在从所有CSV文件中构建可供测试的基因池...")
    gene_pool = {}
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file)
            df_annotated = df[df['GeneB_Annotation'].notna() & (df['GeneB_Annotation'] != '')]
            for _, row in df_annotated.iterrows():
                gene_sym = row['GeneB']
                if gene_sym not in gene_pool:
                    gene_pool[gene_sym] = {
                        'annotation': row['GeneB_Annotation'],
                        'source_file': os.path.basename(csv_file)
                    }
        except Exception as e:
            if verbose:
                logger.warning(f"读取或处理文件 {os.path.basename(csv_file)} 时未读取到Annotation，已跳过")

    if not gene_pool:
        logger.warning("在所有文件中均未找到任何带有GO注释的基因，GO注释测试终止。")
        return

    actual_num_genes_to_test = min(num_genes_to_test, len(gene_pool))
    if verbose:
        logger.info(f"基因池构建完成，共发现 {len(gene_pool)} 个独立基因。将随机抽查 {actual_num_genes_to_test} 个进行验证。")
    
    genes_to_test = random.sample(list(gene_pool.keys()), actual_num_genes_to_test)
    
    cursor = connection.cursor(dictionary=True)
    success_genes_count = 0
    go_failures = []

    for gene_sym in genes_to_test:
        gene_info = gene_pool[gene_sym]
        if verbose:
            logger.info(f"--- 正在验证基因: '{gene_sym}' (来自文件: {gene_info['source_file']}) ---")

        try:
            expected_go_raw = parse_go_annotations(gene_info['annotation'])
            expected_go_ids = {go_id for go_id, desc in expected_go_raw}

            cursor.execute("SELECT gene_id FROM genes WHERE symbol = %s", (gene_sym,))
            gene_result = cursor.fetchone()
            if not gene_result:
                msg = f"验证失败: 基因 '{gene_sym}' 在 'genes' 表中未找到。"
                logger.error(msg)
                go_failures.append(f"基因 '{gene_sym}': {msg}")
                continue

            gene_id = gene_result['gene_id']
            cursor.execute("SELECT go_id FROM gene_go_mapping WHERE gene_id = %s", (gene_id,))
            db_results = cursor.fetchall()
            actual_go_ids = {row['go_id'] for row in db_results}

            if expected_go_ids == actual_go_ids:
                if verbose:
                    logger.info(f"基因 '{gene_sym}' 的GO注释验证成功 ({len(expected_go_ids)}条)。")
                success_genes_count += 1
            else:
                missing_in_db = expected_go_ids - actual_go_ids
                extra_in_db = actual_go_ids - expected_go_ids
                errors = []
                if missing_in_db:
                    errors.append(f"数据库中缺失以下GO ID: {missing_in_db}")
                if extra_in_db:
                    errors.append(f"数据库中多出以下GO ID: {extra_in_db}")
                
                msg = "验证失败: " + " | ".join(errors)
                logger.error(f"基因 '{gene_sym}' {msg}")
                go_failures.append(f"基因 '{gene_sym}': {msg}")

        except Exception as e:
            logger.error(f"验证基因 '{gene_sym}' 时发生意外错误: {e}", exc_info=True)
            go_failures.append(f"基因 '{gene_sym}': 发生意外错误，详见日志。")
    
    # --- 最终报告 (始终显示) ---
    print("\n" + "="*50)
    print(" " * 16 + "GO注释测试结果报告")
    print("="*50)
    print(f"总共检查独立基因数: {len(genes_to_test)}")
    print(f"  - \033[92m验证成功\033[0m: {success_genes_count}")
    print(f"  - \033[91m验证失败\033[0m: {len(go_failures)}")
    print("="*50)

    if go_failures:
        print("\n\033[91mGO测试失败详情:\033[0m")
        for i, f in enumerate(go_failures, 1):
            print(f"{i}. {f}")

def main():
    # 与主脚本相同的数据库配置
    db_config = {
        'host': 'localhost',
        'user': 'zhucj',
        'password': 'Emakingir5!',
        'database': 'gene_prediction'
    }
    
    # 1. 配置命令行参数解析
    parser = argparse.ArgumentParser(
        description='验证基因预测数据是否已正确导入数据库。',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('folders', nargs='+', 
                        help='包含CSV文件的文件夹路径。')
    parser.add_argument('-f', '--num-files', type=int, default=5,
                        help='要抽查预测记录的CSV文件数量。')
    parser.add_argument('-n', '--num-records', type=int, default=10,
                        help='每个文件中要抽查的预测记录数量。')
    parser.add_argument('--test-go', action='store_true',
                        help='执行GO注释的验证测试。')
    parser.add_argument('--num-genes', type=int, default=5,
                        help='执行GO测试时，要抽查的独立基因数量。')
    
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='显示详细的逐条测试日志。')
    
    args = parser.parse_args()
    
    # 2. 查找所有CSV文件
    all_csv_files = find_csv_files(args.folders)
    if not all_csv_files:
        logger.error("未找到任何CSV文件，测试终止。")
        return
        
    # 3. 连接数据库
    connection = create_db_connection(**db_config)
    if not connection:
        logger.critical("无法建立数据库连接，测试终止。")
        return
    
    try:
        # 4. 执行预测记录的测试
        print("\n" + "#"*20 + " 预测记录验证开始 " + "#"*20)
        actual_num_files_to_test = min(args.num_files, len(all_csv_files))
        test_random_records(
            connection=connection,
            csv_files=all_csv_files,
            num_files_to_test=actual_num_files_to_test,
            num_records_per_file=args.num_records,
            verbose=args.verbose  # 传递 verbose 参数
        )

        # 5. 如果用户指定，则执行GO注释的测试
        if args.test_go:
            test_go_annotations(
                connection=connection, 
                csv_files=all_csv_files.copy(), 
                num_genes_to_test=args.num_genes,
                verbose=args.verbose  # 传递 verbose 参数
            )

    finally:
        # 6. 关闭连接
        if connection and connection.is_connected():
            connection.close()
            if args.verbose:
                logger.info("\n数据库连接已关闭。")


if __name__ == "__main__":
    main()