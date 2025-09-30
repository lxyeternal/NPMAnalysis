from npm_feature_extractor import NPM_Feature_Extractor
import time


start_time = time.time()
print(f"开始执行时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")

npm_fe = NPM_Feature_Extractor()
input_data = npm_fe.extract_features("/home/wenbo/NPMAnalysis/Dataset/unzip_benign_new")
# input_data = npm_fe.extract_features("/home/wenbo/NPMAnalysis/Dataset/unzip_malware_new")

end_time = time.time()
print(f"结束执行时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")
print(f"执行总时间: {end_time - start_time:.2f} 秒")
