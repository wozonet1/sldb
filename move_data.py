import os
import csv
import mysql.connector
from mysql.connector import Error

def create_connection(host, user, password, database=None):
    """创建与MySQL数据库的连接"""
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        print("数据库连接成功")
        return connection
    except Error as e:
        print(f"错误: {e}")
        return None

def create_database(connection, db_name):
    """创建数据库"""
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4")
        print(f"数据库 {db_name} 创建成功")
    except Error as e:
        print(f"错误: {e}")

def create_table(connection, table_name, columns):
    """创建数据表"""
    cursor = connection.cursor()
    try:
        # 构建CREATE TABLE语句
        column_definitions = []
        for col in columns:
            # 将列名中的特殊字符替换为下划线
            clean_col = col.strip().replace(' ', '_').replace('-', '_').replace('/', '_')
            # 假设所有字段为TEXT类型，可根据实际需求调整
            column_definitions.append(f"`{clean_col}` TEXT")
        
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS `{table_name}` (
            `id` INT AUTO_INCREMENT PRIMARY KEY,
            {', '.join(column_definitions)}
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """
        
        cursor.execute(create_table_query)
        print(f"数据表 {table_name} 创建成功")
    except Error as e:
        print(f"错误: {e}")

def import_csv_to_mysql(connection, csv_file_path, table_name):
    """将CSV文件导入到MySQL表中"""
    cursor = connection.cursor()
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)  # 获取表头
            
            # 清理列名，移除特殊字符
            clean_headers = [h.strip().replace(' ', '_').replace('-', '_').replace('/', '_') for h in headers]
            
            # 构建INSERT语句
            placeholders = ', '.join(['%s'] * len(clean_headers))
            insert_query = f"""
            INSERT INTO `{table_name}` ({', '.join([f'`{h}`' for h in clean_headers])})
            VALUES ({placeholders})
            """
            
            # 批量插入数据
            total_rows = 0
            for row in csv_reader:
                # 处理每行数据，确保数据长度与列数匹配
                if len(row) < len(clean_headers):
                    row.extend([None] * (len(clean_headers) - len(row)))
                elif len(row) > len(clean_headers):
                    row = row[:len(clean_headers)]
                
                cursor.execute(insert_query, row)
                total_rows += 1
            
            connection.commit()
            print(f"成功导入 {total_rows} 行数据到表 {table_name}")
    
    except Error as e:
        print(f"错误: {e}")
        connection.rollback()

def main():
    # 数据库配置
    db_config = {
        'host': 'localhost',
        'user': 'your_username',      # 替换为你的MySQL用户名
        'password': 'your_password',  # 替换为你的MySQL密码
        'database': 'gene_prediction' # 数据库名
    }
    
    # CSV文件所在文件夹路径
    csv_folder = 'path/to/your/csv/files'  # 替换为实际文件夹路径
    
    # 创建数据库连接
    connection = create_connection(**db_config)
    if not connection:
        return
    
    # 创建数据库（如果不存在）
    create_database(connection, db_config['database'])
    
    # 重新连接到指定数据库
    connection = create_connection(**db_config)
    if not connection:
        return
    
    # 获取所有CSV文件
    csv_files = [f for f in os.listdir(csv_folder) if f.endswith('.csv')]
    
    if not csv_files:
        print("未找到CSV文件")
        return
    
    # 处理每个CSV文件
    for csv_file in csv_files:
        csv_path = os.path.join(csv_folder, csv_file)
        # 使用文件名（不含扩展名）作为表名
        table_name = os.path.splitext(csv_file)[0].replace(' ', '_').replace('-', '_')
        
        # 读取CSV文件的第一行（表头）
        with open(csv_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)
        
        # 创建表
        create_table(connection, table_name, headers)
        
        # 导入数据
        import_csv_to_mysql(connection, csv_path, table_name)
    
    # 关闭数据库连接
    if connection.is_connected():
        connection.close()
        print("数据库连接已关闭")

if __name__ == "__main__":
    main()    