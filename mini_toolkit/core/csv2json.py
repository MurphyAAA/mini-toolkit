import csv
import json
import os
from typing import List

def csv_to_json(csv_file: str, output_file: str = None) -> str:
    """
    将 CSV 文件转换为 JSON 文件，并打印执行状态。

    Args:
        csv_file (str): 输入 CSV 文件路径
        output_file (str, optional): 输出 JSON 文件路径。如果为 None，则使用 csv_file 同名 JSON 文件

    Returns:
        str: 输出 JSON 文件路径

    Raises:
        FileNotFoundError: 当输入 CSV 文件不存在
    """
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"Input file '{csv_file}' not found.")

    # 自动生成输出文件名
    if output_file is None:
        output_file = os.path.splitext(csv_file)[0] + '.json'

    # 读取 CSV 并转换为二维列表
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        data: List[List[float]] = [[float(x) for x in row] for row in reader]

    # 写入 JSON 文件
    key = os.path.splitext(os.path.basename(output_file))[0] # key
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('{\n')
        f.write(f'  "{key}": [\n')
        for i, row in enumerate(data):
            row_json = json.dumps(row, ensure_ascii=False, separators=(',', ':'))
            if i < len(data) - 1:
                f.write(f'    {row_json},\n')
            else:
                f.write(f'    {row_json}\n')
        f.write('  ]\n')
        f.write('}\n')

    # 打印执行状态
    print(f"Converted '{csv_file}' to '{output_file}' successfully.")
    return output_file
