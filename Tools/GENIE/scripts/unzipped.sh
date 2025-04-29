#!/bin/bash

echo "直接分析已解压的NPM包..."

SCRIPT_FS=$SCRIPTS'utils_FS.sh'
SCRIPT_QL=$SCRIPTS'utils_QL.sh'
SCRIPT_NPM=$SCRIPTS'utils_NPM.sh'

source $SCRIPT_FS
source $SCRIPT_QL
source $SCRIPT_NPM

# ---------- #

<<doc
直接处理已解压的NPM包版本目录
输入: 已解压包版本目录的路径，形如：/path/to/packagename/version/package/
doc
process_Unzipped_Package()
{
    # 包版本目录路径
    VERSION_DIR=$1
    
    # 检查是否存在package子目录
    if [ ! -d "$VERSION_DIR/package" ]; then
        echo "错误: 在 $VERSION_DIR 中未找到package目录"
        return $FAILURE_CODE_UNTAR
    fi
    
    # 提取包名和版本
    PKG_Dir=$(basename "$(dirname "$VERSION_DIR")")
    VERSION=$(basename "$VERSION_DIR")
    PKG_Name="${PKG_Dir//@/at-}" # 替换@符号，防止路径问题
    PKG_Name="${PKG_Name//##/--}" # 替换##符号
    
    # 构建输出目录，包含版本信息
    CB_Path=$GENIE_CB_NPM$PKG_Name"_"$VERSION
    DB_Path=$GENIE_DB_NPM$PKG_Name"_"$VERSION
    
    # 日志路径
    LOG_BUILD=$GENIE_LOG_Build$PKG_Name"_"$VERSION$LOG_EXTENSION
    LOG_QUERY=$GENIE_LOG_Query$PKG_Name"_"$VERSION$LOG_EXTENSION
    
    echo "处理包: $PKG_Name 版本: $VERSION"
    
    # 如果代码库目录不存在，创建它
    if [ ! -d "$CB_Path" ]; then
        mkdir -p "$CB_Path"
        # 复制package目录内容到代码库
        cp -r "$VERSION_DIR/package/"* "$CB_Path/"
        # 生成dummy文件
        UTILS_Dummy_JS "$CB_Path"
        echo "创建代码库于 $CB_Path"
    else
        echo "代码库已存在于 $CB_Path"
    fi
    
    # 如果数据库不存在，创建它
    if [ ! -d "$DB_Path" ]; then
        # 创建数据库
        UTILS_Create_DB "$CB_Path" "$DB_Path" "$LOG_BUILD"
        if [ $? -ne 0 ]; then
            echo "为 $PKG_Name 版本 $VERSION 构建数据库失败"
            return $FAILURE_CODE_BUILD
        fi
        echo "创建数据库于 $DB_Path"
    else
        echo "数据库已存在于 $DB_Path"
    fi
    
    # 返回成功
    return $SUCCESS_CODE
}

<<doc
对单个已解压的包版本执行所有CodeQL查询
doc
query_Unzipped_Package()
{
    # 包版本目录路径
    VERSION_DIR=$1
    
    # 提取包名和版本
    PKG_Dir=$(basename "$(dirname "$VERSION_DIR")")
    VERSION=$(basename "$VERSION_DIR")
    PKG_Name="${PKG_Dir//@/at-}" # 替换@符号，防止路径问题
    PKG_Name="${PKG_Name//##/--}" # 替换##符号
    
    # 构建数据库路径
    DB_Path=$GENIE_DB_NPM$PKG_Name"_"$VERSION
    
    # 检查数据库是否存在
    if [ ! -d "$DB_Path" ]; then
        echo "数据库不存在: $PKG_Name 版本 $VERSION。请先处理包。"
        return $FAILURE_CODE_QUERY
    fi
    
    # 查询所有恶意软件查询
    echo "在 $PKG_Name 版本 $VERSION 上运行恶意软件查询..."
    
    # 对每个malware查询执行查询
    for QUERY_Path in $GENIE_QUERIES/malware/*.ql; do
        QUERY_Name=$(basename "$QUERY_Path" .ql)
        OUT_Path=$GENIE_QUERY_Output$PKG_Name"_"$VERSION"_"$QUERY_Name$OUT_EXTENSION
        LOG_QUERY=$GENIE_LOG_Query$PKG_Name"_"$VERSION"_"$QUERY_Name$LOG_EXTENSION
        
        echo "运行查询: $QUERY_Name"
        UTILS_Query_DB "$QUERY_Path" "$DB_Path" "$OUT_Path" "$LOG_QUERY"
        
        # 检查结果
        if [ -f "$OUT_Path" ] && [ -s "$OUT_Path" ]; then
            echo "警告: 查询 $QUERY_Name 在 $PKG_Name 版本 $VERSION 中发现问题"
            # 打印CSV内容的第一行和最后一行
            head -n 1 "$OUT_Path"
            tail -n 1 "$OUT_Path"
        fi
    done
    
    # 对每个obfuscator查询执行查询
    echo "在 $PKG_Name 版本 $VERSION 上运行混淆检测查询..."
    for QUERY_Path in $GENIE_QUERIES/obfuscator/*.ql; do
        QUERY_Name=$(basename "$QUERY_Path" .ql)
        OUT_Path=$GENIE_QUERY_Output$PKG_Name"_"$VERSION"_"$QUERY_Name$OUT_EXTENSION
        LOG_QUERY=$GENIE_LOG_Query$PKG_Name"_"$VERSION"_"$QUERY_Name$LOG_EXTENSION
        
        echo "运行查询: $QUERY_Name"
        UTILS_Query_DB "$QUERY_Path" "$DB_Path" "$OUT_Path" "$LOG_QUERY"
        
        # 检查结果
        if [ -f "$OUT_Path" ] && [ -s "$OUT_Path" ]; then
            echo "警告: 查询 $QUERY_Name 在 $PKG_Name 版本 $VERSION 中发现问题"
            # 打印CSV内容的第一行和最后一行
            head -n 1 "$OUT_Path"
            tail -n 1 "$OUT_Path"
        fi
    done
    
    return $SUCCESS_CODE
}

# ---------- #

<<doc
主函数，用于分析单个已解压的包版本
doc
analyze_Unzipped_Package()
{
    # 从命令行获取包版本路径或请求用户输入
    if [ -z "$1" ]; then
        read -p "输入已解压包版本目录的路径: " VERSION_PATH
    else
        VERSION_PATH=$1
    fi
    
    # 检查路径是否存在
    if [ ! -d "$VERSION_PATH" ]; then
        echo "错误: 目录不存在: $VERSION_PATH"
        return 1
    fi
    
    echo "开始分析包版本: $VERSION_PATH"
    
    # 处理包
    process_Unzipped_Package "$VERSION_PATH"
    if [ $? -ne 0 ]; then
        echo "处理包时出错，中止。"
        return 1
    fi
    
    # 查询包
    query_Unzipped_Package "$VERSION_PATH"
    
    echo "完成分析包版本: $VERSION_PATH"
    return 0
}

# ---------- #

<<doc
批量处理多个已解压的包
doc
analyze_Unzipped_Packages_Batch()
{
    BASE_DIR=$1
    
    if [ -z "$BASE_DIR" ]; then
        read -p "输入包含已解压包的基础目录: " BASE_DIR
    fi
    
    # 检查目录是否存在
    if [ ! -d "$BASE_DIR" ]; then
        echo "错误: 目录不存在: $BASE_DIR"
        return 1
    fi
    
    echo "开始批量分析 $BASE_DIR 中的包"
    
    # 遍历基目录中的所有包
    for PKG_DIR in "$BASE_DIR"/*; do
        if [ -d "$PKG_DIR" ]; then
            # 获取包名
            PKG_NAME=$(basename "$PKG_DIR")
            echo "处理包: $PKG_NAME"
            
            # 遍历所有版本
            for VERSION_DIR in "$PKG_DIR"/*; do
                if [ -d "$VERSION_DIR" ]; then
                    VERSION=$(basename "$VERSION_DIR")
                    echo "处理版本: $VERSION"
                    
                    # 分析此版本
                    analyze_Unzipped_Package "$VERSION_DIR"
                fi
            done
        fi
    done
    
    echo "批量分析完成"
    return 0
}

# ---------- #

# 主交互菜单
if [[ "$1" == "" ]]; then  # 没有命令行参数时显示交互菜单
    PS3="已解压包分析 > "
    select option in "分析单个包版本" "批量分析包" "返回"; do
        case $option in
            "分析单个包版本")
                read -p "输入已解压包版本目录的路径: " VERSION_PATH
                analyze_Unzipped_Package "$VERSION_PATH"
                ;;
            "批量分析包")
                read -p "输入包含已解压包的基础目录: " BASE_DIR
                analyze_Unzipped_Packages_Batch "$BASE_DIR"
                ;;
            "返回")
                break
                ;;
            *) 
                echo "无效选项"
                ;;
        esac
    done
else  # 有命令行参数时处理命令行选项
    while getopts 'u:b:' OPERATION; do
        case $OPERATION in
            u)  # 分析单个包版本
                echo "分析单个包版本!"
                analyze_Unzipped_Package "$OPTARG"
                ;;
            b)  # 批量分析包
                echo "批量分析包!"
                analyze_Unzipped_Packages_Batch "$OPTARG"
                ;;
        esac
    done
fi 