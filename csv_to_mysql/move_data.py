import csv
import re
import os
import logging
from logging.handlers import RotatingFileHandler
import mysql.connector
from mysql.connector import Error
from typing import Dict, List, Tuple
import argparse  # 添加参数解析模块


# -------------------------- 日志配置 --------------------------
def setup_logger():
    """配置日志：同时输出到控制台和文件，自动切割日志文件"""
    logger = logging.getLogger('gene_importer')
    logger.setLevel(logging.INFO)  # 日志级别：INFO及以上
    
    # 日志格式：时间-日志级别-模块-消息
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # 文件处理器（自动切割，保留5个备份，每个最大5MB）
    file_handler = RotatingFileHandler(
        'gene_import.log',
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    
    # 添加处理器
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

# 初始化日志
logger = setup_logger()

# -------------------------- 数据库操作 --------------------------
def create_db_connection(host: str, user: str, password: str, database: str) -> mysql.connector.MySQLConnection:
    """创建数据库连接，自动创建数据库（若不存在）"""
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            autocommit=False  # 关闭自动提交，手动管理事务
        )
        logger.info(f"成功连接到数据库: {database}")
        return connection
    except Error as e:
        if "Unknown database" in str(e):
            try:
                # 先连接到MySQL服务器，创建数据库
                connection = mysql.connector.connect(
                    host=host,
                    user=user,
                    password=password,
                    autocommit=False
                )
                cursor = connection.cursor()
                cursor.execute(f"CREATE DATABASE {database} CHARACTER SET utf8mb4")
                connection.database = database
                logger.info(f"数据库 {database} 不存在，已自动创建")
                return connection
            except Error as e2:
                logger.error(f"创建数据库失败: {str(e2)}", exc_info=True)
                return None
        else:
            logger.error(f"数据库连接失败: {str(e)}", exc_info=True)
            return None


def create_tables(connection: mysql.connector.MySQLConnection) -> None:
    """创建表结构（强化无方向性基因对约束）"""
    cursor = connection.cursor()
    
    try:
        # 基因表（唯一基因符号）
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS genes (
            gene_id INT AUTO_INCREMENT PRIMARY KEY,
            symbol VARCHAR(20) UNIQUE NOT NULL COMMENT '基因符号'
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        
        # GO注释表（唯一GO编号）
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS go_annotations (
            go_id VARCHAR(20) PRIMARY KEY COMMENT 'GO编号',
            description VARCHAR(150) NOT NULL COMMENT 'GO描述'
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        
        # 基因-GO映射表（去重）
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS gene_go_mapping (
            gene_id INT NOT NULL COMMENT '基因ID',
            go_id VARCHAR(20) NOT NULL COMMENT 'GO编号',
            PRIMARY KEY (gene_id, go_id),
            FOREIGN KEY (gene_id) REFERENCES genes(gene_id) ON DELETE CASCADE,
            FOREIGN KEY (go_id) REFERENCES go_annotations(go_id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        
        # 预测结果表（无方向性基因对，唯一约束）
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            gene_a_id INT NOT NULL COMMENT '基因A ID（较小ID）',
            gene_b_id INT NOT NULL COMMENT '基因B ID（较大ID）',
            prediction_score FLOAT NOT NULL COMMENT '预测分数',
            binary_prediction TINYINT NOT NULL COMMENT '二分类结果',
            label ENUM('new_SL', 'new_nonSL', 'old_SL','old_nonSL') COMMENT '预测来源',
            gse_source VARCHAR(50) COMMENT 'GSE来源',
            gse_data VARCHAR(500) COMMENT 'GSE数据',
            FOREIGN KEY (gene_a_id) REFERENCES genes(gene_id) ON DELETE CASCADE,
            FOREIGN KEY (gene_b_id) REFERENCES genes(gene_id) ON DELETE CASCADE,
            UNIQUE KEY unique_gene_pair (gene_a_id, gene_b_id) COMMENT '确保基因对无重复（A,B与B,A视为同一对）'
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        
        connection.commit()
        logger.info("表结构创建/验证成功")
    except Error as e:
        logger.error(f"创建表时出错: {str(e)}", exc_info=True)
        connection.rollback()
        raise e  


# -------------------------- 数据解析与处理 --------------------------
def parse_go_annotations(annotation_text: str) -> List[Tuple[str, str]]:
    """解析GO注释，返回(go_id, description)列表"""
    annotations = []
    if not annotation_text:
        return annotations
    
    go_pattern = re.compile(r'([^\[]+)\s+\[([A-Z]+:\d+)\]')
    for line in annotation_text.strip().split('\n'):
        match = go_pattern.search(line)
        if match:
            description = match.group(1).strip()
            go_id = match.group(2)
            annotations.append((go_id, description))
    
    return annotations

def normalize_gene_pair(gene_a_id: int, gene_b_id: int) -> Tuple[int, int]:
    """标准化基因对：确保gene_a_id < gene_b_id，消除方向性"""
    if gene_a_id < gene_b_id:
        return (gene_a_id, gene_b_id)
    else:
        return (gene_b_id, gene_a_id)

def get_or_create_gene_id(gene_symbol: str, cursor: mysql.connector.cursor.MySQLCursor, gene_cache: Dict[str, int]) -> Tuple[int, bool]:
    """
    获取或创建基因ID，并更新缓存。

    Args:
        gene_symbol: 基因符号 (例如, 'ACSS2')。
        cursor: 用于执行查询的数据库游标。
        gene_cache: 内存中的基因符号到ID的映射缓存。

    Returns:
        一个元组，包含:
        - 基因ID (int)
        - 一个布尔值 (如果基因已存在则为 True，如果是新创建的则为 False)。
    """
    # 1. 优先检查缓存 (速度最快)
    if gene_symbol in gene_cache:
        return gene_cache[gene_symbol], True

    # 2. 缓存未命中，查询数据库
    cursor.execute("SELECT gene_id FROM genes WHERE symbol = %s", (gene_symbol,))
    result = cursor.fetchone()
    
    if result:
        # 在数据库中找到
        gene_id = result[0]
        gene_cache[gene_symbol] = gene_id  # 更新缓存
        return gene_id, True
    else:
        # 3. 数据库中也不存在，插入新基因
        cursor.execute("INSERT INTO genes (symbol) VALUES (%s)", (gene_symbol,))
        gene_id = cursor.lastrowid
        if gene_id:
            gene_cache[gene_symbol] = gene_id  # 用新ID更新缓存
            logger.debug(f"新增基因: {gene_symbol} (ID: {gene_id})")
            return gene_id, False
        else:
            # 针对 lastrowid 不可靠的罕见情况进行回退检查
            logger.warning(f"无法获取新插入基因 {gene_symbol} 的 lastrowid，将重新查询。")
            cursor.execute("SELECT gene_id FROM genes WHERE symbol = %s", (gene_symbol,))
            result = cursor.fetchone()
            if result:
                gene_id = result[0]
                gene_cache[gene_symbol] = gene_id
                return gene_id, False  # 本次运行中仍视为“新”基因
            else:
                raise Exception(f"严重错误：插入基因 {gene_symbol} 后无法在数据库中找到它！")

def process_gene_annotations(gene_id: int, annotation_text: str, cursor: mysql.connector.cursor.MySQLCursor, go_cache: Dict[str, bool]):
    """
    解析给定基因的GO注释文本，并使用INSERT IGNORE高效地更新数据库。
    """
    annotations = parse_go_annotations(annotation_text)
    for go_id, description in annotations:
        # 确保GO术语实体存在
        if go_id not in go_cache:
            cursor.execute("INSERT IGNORE INTO go_annotations (go_id, description) VALUES (%s, %s)", (go_id, description))
            go_cache[go_id] = True
        
        # 确保基因与GO术语的映射关系存在
        cursor.execute("INSERT IGNORE INTO gene_go_mapping (gene_id, go_id) VALUES (%s, %s)", (gene_id, go_id))
def import_single_csv(connection: mysql.connector.MySQLConnection, csv_file_path: str,
                     gene_cache: Dict[str, int], go_cache: Dict[str, bool],
                     batch_size: int = 1000) -> int:
    """
    导入单个CSV文件。：
    - 使用辅助函数处理基因和GO注释，代码简洁。
    - 优化以跳过已存在基因的GO注释处理，提高效率。
    - 包含完整的健壮性检查。
    """
    cursor = connection.cursor()
    file_name = os.path.basename(csv_file_path)
    logger.info(f"开始处理文件: {file_name}")
    
    prediction_batch: List[Tuple] = []
    success_count = 0
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            required_cols = ['GeneA', 'GeneB', 'Prediction', 'BinaryPrediction', 'label']
            if not all(col in csv_reader.fieldnames for col in required_cols):
                logger.error(f"文件 {file_name} 缺少必要的列，已跳过。")
                return 0
            
            gse_columns = [col for col in csv_reader.fieldnames if col.startswith('GSE')]
            if gse_columns:
                logger.info(f"在文件 {file_name} 中找到GSE列: {gse_columns}")
            
            total_rows = 0
            for row in csv_reader:
                total_rows += 1
                
                gene_a_sym = row.get('GeneA')
                gene_b_sym = row.get('GeneB')

                if not gene_a_sym or not gene_b_sym:
                    logger.warning(f"文件 {file_name} 第 {total_rows+1} 行缺少GeneA或GeneB，已跳过。")
                    continue
                
                # --- [核心优化 1] ---
                # 获取基因ID，并得知其是否已存在
                gene_a_id, gene_a_existed = get_or_create_gene_id(gene_a_sym, cursor, gene_cache)
                gene_b_id, gene_b_existed = get_or_create_gene_id(gene_b_sym, cursor, gene_cache)
                
                # --- [核心优化 2] ---
                # 只有当基因是新创建的时，才处理其GO注释
                if not gene_a_existed:
                    process_gene_annotations(gene_a_id, row.get('GeneA_Annotation', ''), cursor, go_cache)
                if not gene_b_existed:
                    process_gene_annotations(gene_b_id, row.get('GeneB_Annotation', ''), cursor, go_cache)
                
                # --- 预测结果处理 ---
                norm_a_id, norm_b_id = normalize_gene_pair(gene_a_id, gene_b_id)
                
                gse_sources_found = [col for col in gse_columns if row.get(col, '').strip()]
                gse_data_found = [row.get(col) for col in gse_sources_found]
                
                gse_source_str = ",".join(gse_sources_found) if gse_sources_found else None
                gse_data_str = "|".join(gse_data_found) if gse_data_found else None

                # (此处可以按需添加长度校验)
                
                try:
                    prediction_score = float(row.get('Prediction', 0.0))
                    binary_prediction = int(row.get('BinaryPrediction', 0))
                except (ValueError, TypeError):
                    logger.warning(f"文件 {file_name} 第 {total_rows+1} 行预测值格式错误，已跳过。")
                    continue
                
                prediction_record = (
                    norm_a_id, norm_b_id, prediction_score, binary_prediction,
                    row.get('label') or None, gse_source_str, gse_data_str
                )
                prediction_batch.append(prediction_record)
                
                if len(prediction_batch) >= batch_size:
                    cursor.executemany("""
                        INSERT IGNORE INTO predictions (gene_a_id, gene_b_id, prediction_score, 
                        binary_prediction, label, gse_source, gse_data) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, prediction_batch)
                    success_count += cursor.rowcount
                    connection.commit()
                    logger.info(f"文件 {file_name} 已批量插入 {len(prediction_batch)} 条记录（新增 {cursor.rowcount} 条）")
                    prediction_batch = []
            
            if prediction_batch:
                cursor.executemany("""
                    INSERT IGNORE INTO predictions (gene_a_id, gene_b_id, prediction_score, 
                    binary_prediction, label, gse_source, gse_data) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, prediction_batch)
                success_count += cursor.rowcount
                connection.commit()
                logger.info(f"文件 {file_name} 剩余记录插入完成（新增 {cursor.rowcount} 条）")
        
        logger.info(f"文件 {file_name} 处理完成，总记录数: {total_rows}，新增预测记录: {success_count}")
        return success_count
    
    except Exception as e:
        logger.error(f"文件 {file_name} 处理时发生意外错误: {str(e)}", exc_info=True)
        connection.rollback()
        return 0
def find_csv_files(folder_paths: List[str]) -> List[str]:
    """查找给定文件夹中的所有CSV文件，返回文件路径列表"""
    csv_files = []
    
    for folder_path in folder_paths:
        # 确保路径存在
        if not os.path.exists(folder_path):
            logger.warning(f"路径不存在: {folder_path}")
            continue
            
        # 遍历文件夹中的所有文件
        for root, _, files in os.walk(folder_path):
            for file in files:
                # 检查文件扩展名是否为.csv（不区分大小写）
                if file.lower().endswith('.csv'):
                    full_path = os.path.join(root, file)
                    csv_files.append(full_path)
                    logger.debug(f"找到CSV文件: {full_path}")
    
    logger.info(f"共找到 {len(csv_files)} 个CSV文件")
    return csv_files


def import_multiple_csvs(connection: mysql.connector.MySQLConnection, csv_file_paths: List[str],
                         batch_size: int = 1000) -> int:
    """导入多个CSV文件，返回总新增记录数"""
    # 预加载缓存（减少数据库查询）
    gene_cache: Dict[str, int] = {}
    go_cache: Dict[str, bool] = {}
    cursor = connection.cursor()

    # 加载已有基因
    cursor.execute("SELECT symbol, gene_id FROM genes")
    for sym, gene_id in cursor.fetchall():
        gene_cache[sym] = gene_id
    logger.info(f"已加载 {len(gene_cache)} 个已有基因到缓存")

    # 加载已有GO注释
    cursor.execute("SELECT go_id FROM go_annotations")
    for (go_id,) in cursor.fetchall():
        go_cache[go_id] = True
    logger.info(f"已加载 {len(go_cache)} 个已有GO注释到缓存")

    if not csv_file_paths:
        logger.warning("未提供任何CSV文件路径")
        return 0

    total_new = 0
    logger.info(f"共发现 {len(csv_file_paths)} 个CSV文件，开始批量导入...")

    for i, csv_path in enumerate(csv_file_paths, 1):
        # 确保文件存在且是CSV
        if not os.path.exists(csv_path):
            logger.warning(f"文件不存在: {csv_path}，已跳过")
            continue
            
        if not csv_path.lower().endswith('.csv'):
            logger.warning(f"路径不是CSV文件: {csv_path}，已跳过")
            continue
        
        logger.info(f"处理文件 {i}/{len(csv_file_paths)}: {os.path.basename(csv_path)}")
        total_new += import_single_csv(connection, csv_path, gene_cache, go_cache, batch_size)

    logger.info(f"所有文件处理完成，本次累计新增预测记录: {total_new}")
    return total_new


# -------------------------- 主函数 --------------------------
def main():
    # 配置数据库参数（可改为命令行参数）
    db_config = {
        'host': 'localhost',
        'user': 'zhucj',
        'password': 'Emakingir5!',
        'database': 'gene_prediction'
    }
    
    # 配置命令行参数解析
    parser = argparse.ArgumentParser(description='导入基因预测数据到数据库')
    parser.add_argument('folders', nargs='+', 
                        help='输入多个包含CSV文件的文件夹路径')
    args = parser.parse_args()
    
    # 1. 查找指定文件夹中的所有CSV文件
    all_csv_files = find_csv_files(args.folders)
    
    if not all_csv_files:
        logger.error("未找到任何CSV文件，程序退出")
        return
        
    # 2. 连接数据库
    connection = create_db_connection(**db_config)
    if not connection:
        logger.critical("无法建立数据库连接，程序退出")
        return
    
    # 3. 创建表结构
    create_tables(connection)
    
    # 4. 批量导入所有CSV文件
    import_multiple_csvs(connection, all_csv_files)
    
    # 5. 关闭连接
    if connection.is_connected():
        connection.close()
        logger.info("数据库连接已关闭")
        logger.info("程序执行完毕")


if __name__ == "__main__":
    main()