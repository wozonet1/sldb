import csv
import mysql.connector
from mysql.connector import Error

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Emakingir5',
    'database': 'your_database',
    'port': 3306
}

# CSV文件夹路径
CSV_FOLDER = "./predict_label"

def migrate_data():
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()
    
    # 清空表（可选）
    cursor.execute("TRUNCATE TABLE gene_predictions")
    
    # 遍历CSV文件
    for filename in os.listdir(CSV_FOLDER):
        if filename.endswith('.csv'):
            geneA = os.path.splitext(filename)[0]
            csv_path = os.path.join(CSV_FOLDER, filename)
            
            with open(csv_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    # 确保数据格式正确
                    prediction = float(row.get('Prediction', 0))
                    binary_prediction = int(row.get('BinaryPrediction', 0))
                    label = row.get('label', '')
                    
                    # 插入数据
                    query = """
                    INSERT INTO gene_predictions (GeneA, GeneB, Prediction, BinaryPrediction, label)
                    VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(query, (geneA, row['GeneB'], prediction, binary_prediction, label))
    
    connection.commit()
    connection.close()
    print("数据迁移完成")

if __name__ == "__main__":
    migrate_data()