#!/bin/bash

# =============================================================================
# Docker容器创建和配置脚本
# 功能：创建packj-test容器，挂载本地目录，设置权限，升级Node.js
# 作者：基于用户的packj分析代码逻辑
# =============================================================================

# 配置变量
CONTAINER_PREFIX="packj-dev"
LOCAL_PATH_PREFIX="/tmp/domain_package"
CONTAINER_PATH="/tmp/packj/domain_package"
DOCKER_IMAGE="ossillate/packj:latest"

# 需要挂载的子目录配置
declare -A MOUNT_DIRS=(
    ["unzip_benign"]="/tmp/domain_package/unzip_benign:/tmp/packj/domain_package/unzip_benign"
    ["unzip_malware"]="/tmp/domain_package/unzip_malware:/tmp/packj/domain_package/unzip_malware"
)

# 默认容器数量（可通过命令行参数修改）
DEFAULT_CONTAINER_COUNT=20

# 解析命令行参数
parse_arguments() {
    CONTAINER_COUNT=$DEFAULT_CONTAINER_COUNT
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            -n|--count)
                CONTAINER_COUNT="$2"
                if ! [[ "$CONTAINER_COUNT" =~ ^[1-9][0-9]*$ ]]; then
                    print_error "容器数量必须是正整数"
                    exit 1
                fi
                shift 2
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                print_error "未知参数: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

# 显示帮助信息
show_help() {
    echo "Docker容器批量创建脚本"
    echo ""
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -n, --count NUMBER    创建容器的数量 (默认: $DEFAULT_CONTAINER_COUNT)"
    echo "  -h, --help           显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0                   # 创建 $DEFAULT_CONTAINER_COUNT 个容器"
    echo "  $0 -n 5              # 创建 5 个容器"
    echo "  $0 --count 10        # 创建 10 个容器"
    echo ""
    echo "容器将被命名为: ${CONTAINER_PREFIX}-1, ${CONTAINER_PREFIX}-2, ..."
}

# 颜色输出函数
print_step() {
    echo -e "\033[1;32m=== $1 ===\033[0m"
}

print_info() {
    echo -e "\033[1;34m[INFO] $1\033[0m"
}

print_error() {
    echo -e "\033[1;31m[ERROR] $1\033[0m"
}

print_success() {
    echo -e "\033[1;32m[SUCCESS] $1\033[0m"
}

# 检查本地目录是否存在
check_local_directories() {
    print_step "检查本地目录"
    
    # 检查要挂载的源目录
    for mount_name in "${!MOUNT_DIRS[@]}"; do
        local_path=$(echo "${MOUNT_DIRS[$mount_name]}" | cut -d':' -f1)
        
        if [ ! -d "$local_path" ]; then
            print_error "挂载源目录不存在: $local_path"
            print_info "请确保以下目录存在："
            for name in "${!MOUNT_DIRS[@]}"; do
                src_path=$(echo "${MOUNT_DIRS[$name]}" | cut -d':' -f1)
                echo "  - $src_path"
            done
            exit 1
        else
            print_success "挂载源目录已存在: $local_path"
        fi
    done
    
    # 为每个容器检查/创建对应的编号目录（如果需要）
    for ((i=1; i<=CONTAINER_COUNT; i++)); do
        LOCAL_PATH="${LOCAL_PATH_PREFIX}-${i}"
        
        if [ ! -d "$LOCAL_PATH" ]; then
            print_info "本地容器专用目录不存在，正在创建: $LOCAL_PATH"
            mkdir -p "$LOCAL_PATH"
            if [ $? -eq 0 ]; then
                print_success "本地容器专用目录创建成功: $LOCAL_PATH"
            else
                print_error "本地容器专用目录创建失败: $LOCAL_PATH"
                exit 1
            fi
        else
            print_success "本地容器专用目录已存在: $LOCAL_PATH"
        fi
    done
}

# 清理现有容器
cleanup_existing_containers() {
    print_step "清理现有容器"
    
    local containers_found=false
    
    for ((i=1; i<=CONTAINER_COUNT; i++)); do
        CONTAINER_NAME="${CONTAINER_PREFIX}-${i}"
        
        # 检查容器是否存在
        if docker ps -a --filter "name=$CONTAINER_NAME" --format "{{.Names}}" | grep -q "^$CONTAINER_NAME$"; then
            print_info "发现现有容器 $CONTAINER_NAME，正在清理..."
            containers_found=true
            
            # 停止容器
            print_info "停止容器 $CONTAINER_NAME..."
            docker stop "$CONTAINER_NAME" >/dev/null 2>&1
            
            # 删除容器
            print_info "删除容器 $CONTAINER_NAME..."
            docker rm "$CONTAINER_NAME" >/dev/null 2>&1
            
            print_success "容器 $CONTAINER_NAME 清理完成"
        fi
    done
    
    if [ "$containers_found" = false ]; then
        print_info "没有发现现有容器，跳过清理步骤"
    fi
}

# 创建新容器
create_containers() {
    print_step "创建新容器"
    
    for ((i=1; i<=CONTAINER_COUNT; i++)); do
        CONTAINER_NAME="${CONTAINER_PREFIX}-${i}"
        LOCAL_PATH="${LOCAL_PATH_PREFIX}-${i}"
        
        print_info "创建容器: $CONTAINER_NAME"
        print_info "容器专用目录挂载: $LOCAL_PATH -> $CONTAINER_PATH"
        
        # 构建挂载参数
        MOUNT_ARGS="-v $LOCAL_PATH:$CONTAINER_PATH"
        
        # 添加子目录挂载
        for mount_name in "${!MOUNT_DIRS[@]}"; do
            mount_spec="${MOUNT_DIRS[$mount_name]}"
            src_path=$(echo "$mount_spec" | cut -d':' -f1)
            dst_path=$(echo "$mount_spec" | cut -d':' -f2)
            
            print_info "数据目录挂载: $src_path -> $dst_path"
            MOUNT_ARGS="$MOUNT_ARGS -v $mount_spec"
        done
        
        print_info "使用镜像: $DOCKER_IMAGE"
        
        docker run -d \
            --name "$CONTAINER_NAME" \
            --entrypoint '/bin/bash' \
            $MOUNT_ARGS \
            "$DOCKER_IMAGE" \
            -c 'tail -f /dev/null'
        
        # 检查容器是否成功启动
        if docker ps -q -f name="$CONTAINER_NAME" | grep -q .; then
            print_success "容器 $CONTAINER_NAME 成功启动"
        else
            print_error "容器 $CONTAINER_NAME 启动失败"
            exit 1
        fi
        
        echo ""  # 添加空行以便区分不同容器
    done
}

# 设置容器权限
setup_permissions() {
    print_step "设置容器权限"
    
    for ((i=1; i<=CONTAINER_COUNT; i++)); do
        CONTAINER_NAME="${CONTAINER_PREFIX}-${i}"
        
        print_info "设置容器 $CONTAINER_NAME 权限..."
        
        # 第一条命令：设置 /tmp/packj 权限
        print_info "  设置 $CONTAINER_PATH 目录权限..."
        docker exec -u 0 "$CONTAINER_NAME" chmod -R 777 "$CONTAINER_PATH" 2>/dev/null
        if [ $? -eq 0 ]; then
            print_success "  $CONTAINER_PATH 权限设置成功"
        else
            print_error "  $CONTAINER_PATH 权限设置失败"
        fi
        
        # 第二条命令：设置 /tmp 目录权限
        print_info "  设置 /tmp 目录权限..."
        docker exec -u 0 "$CONTAINER_NAME" chmod -R 777 /tmp 2>/dev/null
        if [ $? -eq 0 ]; then
            print_success "  /tmp 目录权限设置成功"
        else
            print_error "  /tmp 目录权限设置失败"
        fi
        
        # 第三条命令：设置根目录权限（忽略系统文件错误）
        print_info "  设置根目录权限（忽略系统文件错误）..."
        docker exec -u 0 "$CONTAINER_NAME" bash -c "chmod -R 777 / 2>/dev/null || true"
        print_success "  根目录权限设置完成（已忽略系统文件权限错误）"
        
        # 设置目录所有权
        print_info "  设置目录所有权为 ubuntu:ubuntu..."
        docker exec -u 0 "$CONTAINER_NAME" chown -R ubuntu:ubuntu "$CONTAINER_PATH"
        if [ $? -eq 0 ]; then
            print_success "  目录所有权设置成功"
        else
            print_error "  目录所有权设置失败"
        fi
        
        echo ""  # 添加空行以便区分不同容器
    done
}

# 升级Node.js
upgrade_nodejs() {
    print_step "升级Node.js到最新版本"
    
    for ((i=1; i<=CONTAINER_COUNT; i++)); do
        CONTAINER_NAME="${CONTAINER_PREFIX}-${i}"
        
        print_info "升级容器 $CONTAINER_NAME 的Node.js..."
        
        print_info "  更新包管理器..."
        docker exec -u 0 "$CONTAINER_NAME" apt-get update -y >/dev/null 2>&1
        
        print_info "  安装必要依赖..."
        docker exec -u 0 "$CONTAINER_NAME" apt-get install -y curl software-properties-common >/dev/null 2>&1
        
        print_info "  添加NodeSource官方仓库..."
        docker exec -u 0 "$CONTAINER_NAME" bash -c "curl -fsSL https://deb.nodesource.com/setup_20.x | bash -" >/dev/null 2>&1
        
        print_info "  安装Node.js 20.x LTS..."
        docker exec -u 0 "$CONTAINER_NAME" apt-get install -y nodejs >/dev/null 2>&1
        
        if [ $? -eq 0 ]; then
            print_success "  容器 $CONTAINER_NAME Node.js升级完成"
        else
            print_error "  容器 $CONTAINER_NAME Node.js升级失败"
        fi
        
        echo ""  # 添加空行以便区分不同容器
    done
}

# 复制本地pm_util.py到容器
copy_local_pm_util() {
    print_step "复制本地pm_util.py到容器"
    
    # 定义路径
    HOST_PM_UTIL_PATH="/home2/wenbo/Documents/NPMAnalysis/Tools/packj/packj/audit/pm_util.py"
    CONTAINER_PM_UTIL_PATH="/home/ubuntu/packj/packj/audit/pm_util.py"
    
    for ((i=1; i<=CONTAINER_COUNT; i++)); do
        CONTAINER_NAME="${CONTAINER_PREFIX}-${i}"
        
        print_info "复制 pm_util.py 到容器 $CONTAINER_NAME..."
        docker cp "$HOST_PM_UTIL_PATH" "$CONTAINER_NAME:$CONTAINER_PM_UTIL_PATH"
        
        if [ $? -eq 0 ]; then
            print_success "  容器 $CONTAINER_NAME pm_util.py文件复制完成"
        else
            print_error "  容器 $CONTAINER_NAME pm_util.py文件复制失败"
        fi
    done
}

# 验证配置
verify_setup() {
    print_step "验证容器配置"
    
    print_info "所有容器状态:"
    docker ps --filter name="${CONTAINER_PREFIX}-" --format "table {{.Names}}\t{{.Status}}\t{{.CreatedAt}}"
    echo ""
    
    for ((i=1; i<=CONTAINER_COUNT; i++)); do
        CONTAINER_NAME="${CONTAINER_PREFIX}-${i}"
        LOCAL_PATH="${LOCAL_PATH_PREFIX}-${i}"
        
        print_info "验证容器 $CONTAINER_NAME:"
        
        print_info "  容器专用目录内容 ($LOCAL_PATH -> $CONTAINER_PATH):"
        docker exec -u ubuntu "$CONTAINER_NAME" ls -la "$CONTAINER_PATH" 2>/dev/null || print_info "  容器专用目录为空或无法访问"
        
        # 验证数据目录挂载
        for mount_name in "${!MOUNT_DIRS[@]}"; do
            mount_spec="${MOUNT_DIRS[$mount_name]}"
            src_path=$(echo "$mount_spec" | cut -d':' -f1)
            dst_path=$(echo "$mount_spec" | cut -d':' -f2)
            
            print_info "  数据目录 $mount_name ($src_path -> $dst_path):"
            file_count=$(docker exec -u ubuntu "$CONTAINER_NAME" find "$dst_path" -type f 2>/dev/null | wc -l)
            if [ $? -eq 0 ] && [ "$file_count" -gt 0 ]; then
                print_success "    包含 $file_count 个文件"
                # 显示前几个目录作为示例
                docker exec -u ubuntu "$CONTAINER_NAME" ls "$dst_path" 2>/dev/null | head -3 | while read dir; do
                    echo "    示例目录: $dir"
                done
            else
                print_error "    目录为空或无法访问"
            fi
        done
        
        print_info "  Node.js版本:"
        NODE_VERSION=$(docker exec -u ubuntu "$CONTAINER_NAME" node --version 2>/dev/null)
        if [ $? -eq 0 ]; then
            echo "    $NODE_VERSION"
        else
            print_error "    无法获取Node.js版本"
        fi
        
        print_info "  npm版本:"
        NPM_VERSION=$(docker exec -u ubuntu "$CONTAINER_NAME" npm --version 2>/dev/null)
        if [ $? -eq 0 ]; then
            echo "    $NPM_VERSION"
        else
            print_error "    无法获取npm版本"
        fi
        
        echo ""  # 添加空行以便区分不同容器
    done
}

# 显示使用说明
show_usage_info() {
    print_step "使用说明"
    echo "容器配置完成！"
    echo ""
    echo "容器信息:"
    echo "  容器数量: $CONTAINER_COUNT"
    echo "  容器前缀: $CONTAINER_PREFIX"
    echo "  本地路径前缀: $LOCAL_PATH_PREFIX"
    echo "  容器内路径: $CONTAINER_PATH"
    echo "  Docker镜像: $DOCKER_IMAGE"
    echo ""
    echo "数据目录挂载:"
    for mount_name in "${!MOUNT_DIRS[@]}"; do
        mount_spec="${MOUNT_DIRS[$mount_name]}"
        src_path=$(echo "$mount_spec" | cut -d':' -f1)
        dst_path=$(echo "$mount_spec" | cut -d':' -f2)
        echo "  $mount_name: $src_path -> $dst_path"
    done
    echo ""
    echo "创建的容器列表:"
    for ((i=1; i<=CONTAINER_COUNT; i++)); do
        echo "  ${CONTAINER_PREFIX}-${i} -> ${LOCAL_PATH_PREFIX}-${i}"
    done
    echo ""
    echo "常用命令:"
    echo "  进入容器: docker exec -u ubuntu -it <容器名> bash"
    echo "    示例: docker exec -u ubuntu -it ${CONTAINER_PREFIX}-1 bash"
    echo "  停止所有容器: docker stop \$(docker ps -q --filter name=${CONTAINER_PREFIX}-)"
    echo "  删除所有容器: docker rm \$(docker ps -aq --filter name=${CONTAINER_PREFIX}-)"
    echo "  查看所有容器: docker ps --filter name=${CONTAINER_PREFIX}-"
    echo ""
    echo "packj分析命令示例:"
    echo "  # 分析benign包："
    echo "  docker exec -u ubuntu -it ${CONTAINER_PREFIX}-1 python3 /home/ubuntu/packj/main.py audit -t -p local_nodejs:/tmp/packj/domain_package/unzip_benign/package_name/version/package"
    echo ""
    echo "  # 分析malware包："
    echo "  docker exec -u ubuntu -it ${CONTAINER_PREFIX}-1 python3 /home/ubuntu/packj/main.py audit -t -p local_nodejs:/tmp/packj/domain_package/unzip_malware/package_name/version/package"
    echo ""
    echo "并行分析示例："
    echo "  # 在不同容器中同时分析不同包"
    local max_examples=$((CONTAINER_COUNT < 3 ? CONTAINER_COUNT : 3))
    for ((i=1; i<=max_examples; i++)); do
        echo "  docker exec -u ubuntu -d ${CONTAINER_PREFIX}-${i} python3 /home/ubuntu/packj/main.py audit -t -p local_nodejs:/tmp/packj/domain_package/unzip_benign/some_package${i}/version/package &"
    done
    if [ $CONTAINER_COUNT -gt 3 ]; then
        echo "  # ... 更多容器"
    fi
    echo "  wait  # 等待所有后台任务完成"
}

# 主函数
main() {
    # 解析命令行参数
    parse_arguments "$@"
    
    echo "Docker容器批量自动化配置脚本"
    echo "目标：创建 $CONTAINER_COUNT 个 ${CONTAINER_PREFIX}-X 容器"
    echo ""
    
    # 执行各个步骤
    check_local_directories
    cleanup_existing_containers
    create_containers
    setup_permissions
    upgrade_nodejs
    copy_local_pm_util
    verify_setup
    show_usage_info
    
    print_success "所有 $CONTAINER_COUNT 个容器配置步骤完成！"
}

# 错误处理
set -e
trap 'print_error "脚本执行失败，请检查错误信息"' ERR

# 执行主函数
main "$@"