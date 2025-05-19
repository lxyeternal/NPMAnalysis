import os
import re
import pandas as pd

# 定义基本目录路径
base_path = "/Users/kzyinglili/Documents/Empirical_study_NPM/NPM_new/NPM/zip_malware"

def collect_package_info():
    """
    收集所有包的名称和版本信息
    
    返回:
    包含所有包信息的列表，每个元素为 (package_name, version) 元组
    """

    results =[]

    for package_dir in os.listdir(base_path):
        package_path= os.path.join(base_path,package_dir)

        if not os.path.isdir(package_path):
            continue

        package_name = package_dir.replace('##','/')

        try:
            for version_dir in os.listdir(package_path):
                version_path=os.path.join(package_path,version_dir)

                if not os.path.isdir(version_path):
                    continue

                
                version = version_dir

                results.append((package_name, version))
        except Exception as e:
            print(f"Error processing package {package_name}: {e}")

    unique_packages = set([r[0] for r in results])
    print(f"共找到 {len(results)} 个包版本组合")
    print(f"共找到 {len(unique_packages)} 个唯一的包名")
    return results

def main():

    package_info =collect_package_info()

    df =pd.DataFrame(package_info, columns=['package_name', 'version'])

    output_file='npm_packages.csv'
    df.to_csv(output_file, index=False)
    print(f"已收集到 {len(df)} 个包的信息")
    print(f"结果已保存至 {output_file}")

if __name__ == "__main__":
    main()