import csv
import json

file_path = '/home/myf/myf/work_space/ARServo/data/raw/recorded/trans_3.json'  # 替换为你的JSON文件路径

def list_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(data)

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
    exp = data['trans_3']  # 替换为你的表情名称

print(exp)
list_to_csv(exp, '/home/myf/myf/work_space/ARServo/data/raw/recorded/trans_3.csv')  # 替换为你想要保存的CSV文件名


