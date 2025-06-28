from flask import Flask, request, jsonify
import os
import random
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Emakingir5',
    'database': 'your_database',
    'port': 3306
}

def create_db_connection():
    """创建数据库连接"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"数据库连接错误: {e}")
        return None

@app.route('/predict', methods=['GET'])
def predict():
    geneA = request.args.get('geneA')
    geneB = request.args.get('geneB')

    if not geneA:
        return jsonify({"error": "Gene A is required"}), 400

    connection = create_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        
        if geneB:
            # 查询特定GeneA和GeneB的记录
            query = """
            SELECT GeneA AS `Gene A`, GeneB AS `Gene B`, 
                   Prediction AS `Prediction score`, label AS `Predicting relation`
            FROM gene_predictions 
            WHERE GeneA = %s AND GeneB = %s
            """
            cursor.execute(query, (geneA, geneB))
            result = cursor.fetchone()
            
            if not result:
                return jsonify({"error": f"No data found for Gene A: {geneA} and Gene B: {geneB}"}), 404
            return jsonify(result)
        else:
            # 查询GeneA的所有记录，按优先级排序
            query = """
            SELECT GeneA AS `Gene A`, GeneB AS `Gene B`, 
                   Prediction AS `Prediction score`, label AS `Predicting relation`,
                   BinaryPrediction, label
            FROM gene_predictions 
            WHERE GeneA = %s
            """
            cursor.execute(query, (geneA,))
            all_records = cursor.fetchall()
            
            if not all_records:
                return jsonify({"error": f"No data found for Gene A: {geneA}"}), 404
            
            # 内存中筛选和排序逻辑（与原代码保持一致）
            priority_records = [r for r in all_records if r['BinaryPrediction'] == 1 and r['label'] == 'old_SL']
            remaining_records = [r for r in all_records if r['BinaryPrediction'] == 1 and r['label'] != 'old_SL']
            
            # 移除临时字段
            for record in all_records:
                record.pop('BinaryPrediction', None)
                record.pop('label', None)
            
            # 如果优先数据不足20条，从剩余数据中随机选择
            num_priority = len(priority_records)
            if num_priority < 20 and remaining_records:
                remaining_sample = random.sample(remaining_records, min(20 - num_priority, len(remaining_records)))
                combined_records = priority_records + remaining_sample
            else:
                combined_records = priority_records[:20]
            
            # 按预测分数降序排列
            sorted_records = sorted(combined_records, key=lambda x: x['Prediction score'], reverse=True)
            
            return jsonify(sorted_records)
            
    except Error as e:
        print(f"数据库查询错误: {e}")
        return jsonify({"error": "Database query error"}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.errorhandler(500)
def handle_500_error(e):
    return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5555
    )