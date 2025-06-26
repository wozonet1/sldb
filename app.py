from flask import Flask, request, jsonify
import pandas as pd
import os
import random
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 预测文件夹路径
PREDICTION_FOLDER = "./predict_label"

@app.route('/predict', methods=['GET'])
def predict():
    geneA = request.args.get('geneA')
    geneB = request.args.get('geneB')

    if not geneA:
        return jsonify({"error": "Gene A is required"}), 400

    # 构造文件路径
    file_path = os.path.join(PREDICTION_FOLDER, f"{geneA}.csv")

    if not os.path.exists(file_path):
        return jsonify({"error": f"No data found for Gene A: {geneA}"}), 404

    # 读取CSV文件
    df = pd.read_csv(file_path)

    if geneB:
        # 如果提供了Gene B，直接查找对应的行
        result = df[(df['GeneA'] == geneA) & (df['GeneB'] == geneB)].to_dict(orient='records')
        if not result:
            return jsonify({"error": f"No data found for Gene A: {geneA} and Gene B: {geneB}"}), 404
        return jsonify(result[0])

    else:
        # 如果只提供了Gene A，筛选并返回数据
        # 优先选择BinaryPrediction为1且label为old_SL的数据
        priority_df = df[(df['BinaryPrediction'] == 1) & (df['label'] == 'old_SL')]
        # priority_df = df[df['label'] == 'old_SL']
        remaining_df = df[(df['BinaryPrediction'] == 1) & (df['label'] != 'old_SL')]

        # 如果优先数据不足20条，从剩余数据中随机选择
        num_priority = len(priority_df)
        if num_priority < 20 and len(remaining_df) > 0:
            remaining_sample = remaining_df.sample(min(20 - num_priority, len(remaining_df)))
            combined_df = pd.concat([priority_df, remaining_sample])
        else:
            combined_df = priority_df.head(20)

        # 按Prediction列降序排列
        sorted_df = combined_df.sort_values(by='Prediction', ascending=False)

        # 转换列为所需名称
        sorted_df.rename(columns={'GeneA': 'Gene A', 'GeneB': 'Gene B', 'Prediction': 'Prediction score', 'label': 'Predicting relation'}, inplace=True)

        return jsonify(sorted_df.to_dict(orient='records'))

@app.errorhandler(500)
def handle_500_error(e):
    return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5555
    )