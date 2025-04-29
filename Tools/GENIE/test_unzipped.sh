#!/bin/bash

# 测试脚本，用于验证对已解压包的分析功能

# 设置测试包版本路径 - 这里的路径是到版本目录的
TEST_VERSION_DIR="/home/wenbo/NPMAnalysis/Dataset/unzip_benign/envoy-toolkit-javascript/0.0.95"

# 首先设置项目
echo "设置GENIE项目..."
./scripts/main.sh 3  # 选择初始化选项

# 分析单个包版本
echo "测试单个包版本分析..."
./scripts/main.sh -u "$TEST_VERSION_DIR"

# 测试批量分析
# echo "测试批量分析..."
# TEST_BATCH_DIR="/home/wenbo/NPMAnalysis/Dataset/unzip_benign"
# ./scripts/main.sh -b "$TEST_BATCH_DIR"

echo "测试完成。" 