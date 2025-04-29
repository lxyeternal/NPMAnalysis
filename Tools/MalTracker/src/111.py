import os
import subprocess
import json
import logging
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from utils import FeatureExtractor  # 从 utils.py 引入特征提取器
from pkg2spt import Extractor  # 从 pkg2spt.py 引入特征提取类
from iggraph import IGGraph  # 从 iggraph.py 引入图构建类
from spt2pdg import PDG  # 从 spt2pdg.py 引入 PDG 类
from trainer import clf_chooser, train_and_evaluate  # 从 trainer.py 引入分类器选择和训练评估方法

# 设置日志
logging.basicConfig(filename='./log/malware_detection.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 配置路径
NEW_MALWARE_DIR = r"F:\z_my_cources_scripts\ntu\Empirical_study_in_NPM\NPM\our_npm\akgularjs\1.1.2\akgularjs-1.1.2.tgz"
CALLGRAPH_DIR = './callgraphs'
PDG_DIR = './pdgs'
FEATURES_DIR = './features'
MODEL_DIR = './models'

# 工具路径配置
CALLGRAPH_TOOL = 'ts-node ../res/jelly/src/main.ts'
PDG_TOOL = 'python ../../tools/fast/generate_graph.py'

# 执行外部命令
def execute_command(command):
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        logger.error(f"命令执行失败: {command}")
        logger.error(result.stderr)
        raise Exception(f"命令执行失败: {command}")
    logger.info(f"命令执行成功: {command}")
    return result.stdout

# 生成调用图
def generate_call_graph():
    command = f"{CALLGRAPH_TOOL} --timeout 15 --callgraph-json {CALLGRAPH_DIR}/callgraph.json {NEW_MALWARE_DIR}"
    execute_command(command)

# 生成程序依赖图
def generate_pdg():
    command = f"{PDG_TOOL} -a -no {PDG_DIR}/nodes.tsv -eo {PDG_DIR}/edges.tsv {CALLGRAPH_DIR}/callgraph.json"
    execute_command(command)

# 提取特征
def extract_features(pdg_file):
    extractor = FeatureExtractor(pdg_file)  # 使用 FeatureExtractor 提取特征
    features = extractor.extract_features()  # 提取的特征
    return features

# 训练和评估模型
def train_and_evaluate_model(features, labels):
    clf = clf_chooser()  # 选择分类器
    model, report = train_and_evaluate(features, labels, clf)  # 训练和评估模型
    return model, report

# 保存模型
def save_model(model):
    import joblib
    model_filename = f"{MODEL_DIR}/malware_detection_model.pkl"
    joblib.dump(model, model_filename)
    logger.info(f"模型已保存: {model_filename}")

# 检测恶意包
def detect_malware():
    # 1. 生成调用图
    generate_call_graph()

    # 2. 生成程序依赖图（PDG）
    generate_pdg()

    # 3. 从 PDG 提取特征
    pdg_file = f"{PDG_DIR}/nodes.tsv"  # 这里使用 nodes.tsv 文件作为输入
    features = extract_features(pdg_file)

    # 4. 假设已加载标签数据（如恶意或正常标签）
    labels = []  # 在这里填入实际的标签数据

    # 5. 训练和评估模型
    model, report = train_and_evaluate_model(features, labels)

    # 6. 保存模型
    save_model(model)

    # 返回评估报告
    return report

# 主程序入口
if __name__ == "__main__":
    try:
        report = detect_malware()  # 执行恶意包检测
        logger.info(f"检测报告:\n{report}")  # 输出检测报告
    except Exception as e:
        logger.error(f"检测过程中发生错误: {e}")  # 记录错误
        print(f"检测过程中发生错误: {e}")  # 控制台输出错误
