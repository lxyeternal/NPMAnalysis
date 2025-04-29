import os
import json
import requests
import time
import multiprocessing
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor

# 创建基础目录用于存储所有包
BASE_DIR = Path("../../Dataset/benign")
BASE_DIR.mkdir(exist_ok=True)

TOTAL_PACKAGES = 15000
# 进程数，可以根据您的CPU核心数调整
NUM_PROCESSES = 20
# 存储下载结果的队列
results_queue = multiprocessing.Manager().Queue()

def normalize_package_name(package_name):
    """将包名中的 @ 和 / 处理成合法的文件名"""
    if package_name.startswith('@'):
        # 将 @XXX/AAA 转换成 @XXX##AAA
        return package_name.replace('/', '##')
    return package_name

def fetch_popular_packages():
    """从 NPM 注册表获取流行的 NPM 包"""
    url = "https://registry.npmjs.org/-/v1/search?text=popularity:>0.3&size=10000"
    
    try:
        packages = set()  # 使用集合来去重
        offset = 0
        
        # NPM API 每次最多返回 1000 个结果，所以需要多次请求
        while len(packages) < TOTAL_PACKAGES:
            print(f"正在获取包列表，已获取 {len(packages)} 个...")
            response = requests.get(f"{url}&from={offset}", timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if "objects" not in data or not data["objects"]:
                break
                
            # 提取包名
            batch_packages = [obj["package"]["name"] for obj in data["objects"]]
            packages.update(batch_packages)  # 使用update而不是extend
            
            offset += len(batch_packages)
            
            # 防止超过请求限制
            time.sleep(1)
            
        return list(packages)[:TOTAL_PACKAGES]  # 转换为列表并截取
    except requests.exceptions.RequestException as e:
        print(f"获取包列表时出错: {e}")
        return []

def download_package_tarball(package_info):
    """直接从 NPM 注册表下载包的 tarball 并保存为压缩包"""
    package_name, index = package_info
    normalized_name = normalize_package_name(package_name)
    package_dir = BASE_DIR / normalized_name
    
    # 检查是否已经下载过
    tarball_files = list(package_dir.glob("*.tgz"))
    if package_dir.exists() and tarball_files:
        print(f"[{index}/{TOTAL_PACKAGES}] 包 {package_name} 已经下载过，跳过")
        results_queue.put((package_name, True, "已跳过"))
        return True
    
    try:
        # 获取包信息
        registry_url = f"https://registry.npmjs.org/{package_name}"
        response = requests.get(registry_url, timeout=30)
        response.raise_for_status()
        
        package_data = response.json()
        
        # 获取最新版本
        latest_version = package_data.get('dist-tags', {}).get('latest')
        if not latest_version and 'versions' in package_data:
            # 如果没有 latest 标签，取最后一个版本
            latest_version = list(package_data['versions'].keys())[-1]
        
        if not latest_version:
            print(f"[{index}/{TOTAL_PACKAGES}] 无法确定 {package_name} 的最新版本")
            results_queue.put((package_name, False, "版本获取失败"))
            return False
        
        # 获取 tarball URL
        tarball_url = package_data.get('versions', {}).get(latest_version, {}).get('dist', {}).get('tarball')
        
        if not tarball_url:
            print(f"[{index}/{TOTAL_PACKAGES}] 无法获取 {package_name} 的 tarball URL")
            results_queue.put((package_name, False, "tarball URL获取失败"))
            return False
        
        # 下载 tarball
        print(f"[{index}/{TOTAL_PACKAGES}] 正在下载: {package_name}@{latest_version}")
        
        tarball_response = requests.get(tarball_url, timeout=60)
        tarball_response.raise_for_status()
        
        # 创建包目录
        package_dir.mkdir(exist_ok=True, parents=True)
        
        # 保存为压缩包
        tarball_path = package_dir / f"{normalized_name}-{latest_version}.tgz"
        with open(tarball_path, 'wb') as f:
            f.write(tarball_response.content)
        
        print(f"[{index}/{TOTAL_PACKAGES}] 成功下载: {package_name}")
        results_queue.put((package_name, True, "成功"))
        return True
    except requests.exceptions.RequestException as e:
        print(f"[{index}/{TOTAL_PACKAGES}] 下载 {package_name} 时网络错误: {e}")
        results_queue.put((package_name, False, f"网络错误: {str(e)[:100]}"))
        return False
    except Exception as e:
        print(f"[{index}/{TOTAL_PACKAGES}] 下载 {package_name} 时出错: {e}")
        results_queue.put((package_name, False, f"其他错误: {str(e)[:100]}"))
        return False

def process_batch(batch_packages):
    """处理一批包"""
    for package_info in batch_packages:
        download_package_tarball(package_info)

def main():
    print("获取 NPM 流行包列表...")
    packages = fetch_popular_packages()
    
    if not packages:
        print("无法获取包列表。退出。")
        return
    
    print(f"找到 {len(packages)} 个包。开始下载...")
    
    # 准备多进程下载
    package_infos = [(pkg, i+1) for i, pkg in enumerate(packages)]
    
    # 分批处理，以避免创建过多进程
    batch_size = max(1, len(package_infos) // NUM_PROCESSES)
    batches = [package_infos[i:i+batch_size] for i in range(0, len(package_infos), batch_size)]
    
    # 使用进程池下载
    with ProcessPoolExecutor(max_workers=NUM_PROCESSES) as executor:
        executor.map(process_batch, batches)
    
    # 统计下载结果
    successful = 0
    failed = 0
    skipped = 0
    failed_packages = []
    
    while not results_queue.empty():
        package_name, success, reason = results_queue.get()
        if success:
            if reason == "已跳过":
                skipped += 1
            else:
                successful += 1
        else:
            failed += 1
            failed_packages.append((package_name, reason))
    
    print(f"\n下载完成！成功: {successful}, 跳过: {skipped}, 失败: {failed}")
    
    if failed > 0:
        print("失败的包:")
        for pkg, reason in failed_packages:
            print(f"  - {pkg}: {reason}")
        
        # 将失败的包列表保存到文件
        with open("failed_packages.txt", "w") as f:
            for pkg, reason in failed_packages:
                f.write(f"{pkg}: {reason}\n")

if __name__ == "__main__":
    main()