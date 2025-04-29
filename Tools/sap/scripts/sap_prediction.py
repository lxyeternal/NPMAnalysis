# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# @File     : sap_prediction.py
# @Project  : PyGuardX
# Time      : 23/9/24 10:36 am
# Author    : honywen
# version   : python 3.8
# Description：
"""

import joblib
import pandas as pd


def load_model(model_path):
    """加载模型"""
    return joblib.load(model_path)


def load_and_prepare_data(csv_path):
    """加载并预处理CSV文件，移除不需要的列"""
    df = pd.read_csv(csv_path)
    # 移除 'Package Name' 和 'repository' 列
    package_names = df['Package Name']  # 保留包名
    df = df.drop(columns=['Package Name', 'repository'])
    return df, package_names


def predict_and_store_results(model, X, package_names):
    """对数据进行预测并将结果与包名对齐"""
    predictions = model.predict(X)
    return pd.DataFrame({'Package Name': package_names, 'Prediction': predictions})


def main():
    # 模型路径
    models = {
        'DT': '/home/wenbo/NPMAnalysis/Tools/sap/scripts/JS_monolanguage_DT.pkl',
        'RF': '/home/wenbo/NPMAnalysis/Tools/sap/scripts/JS_monolanguage_RF.pkl',
        'XGB': '/home/wenbo/NPMAnalysis/Tools/sap/scripts/JS_monolanguage_XGB.pkl'
    }

    # 数据文件路径
    data_files = [
        ('malware',
         '/home/wenbo/NPMAnalysis/Tools/sap/scripts/feature_extraction/malware_npm_feature_extracted.csv'),
        ('benign',
         '/home/wenbo/NPMAnalysis/Tools/sap/scripts/feature_extraction/benign_npm_feature_extracted.csv')
    ]

    # 加载模型
    loaded_models = {name: load_model(path) for name, path in models.items()}
    # 用于存储最终结果的 DataFrame
    final_results = pd.DataFrame()
    # 遍历每个数据文件进行预测
    for data_type, file_path in data_files:
        # 读取和预处理数据
        data, package_names = load_and_prepare_data(file_path)
        # 初始化 DataFrame，用于存储当前数据文件的结果
        result_df = pd.DataFrame()
        result_df['Package Name'] = package_names
        result_df['type'] = data_type
        # 针对每个模型进行预测并将结果存储
        for model_name, model in loaded_models.items():
            predictions = model.predict(data)
            result_df[model_name] = predictions
        # 合并结果到最终 DataFrame
        final_results = pd.concat([final_results, result_df], ignore_index=True)
    # 保存最终结果为 CSV 文件
    final_results.to_csv('/home/wenbo/NPMAnalysis/Tools/sap/scripts/sap_detection_results.csv', index=False)


if __name__ == '__main__':
    main()
