import json
import csv
import os

def json_to_csv(json_file: str, output_file:str=None, data_key:str='key') -> str:
    """
    将JSON文件转换为CSV
    
    Args:
        json_file (str): 输入的JSON文件路径
        output_file (str, optional): 输出的CSV文件路径
        data_key (str): 要提取的JSON键名
    
    Returns:
        str: 输出文件的路径
    
    Raises:
        FileNotFoundError: 当输入文件不存在时
        ValueError: 当指定的键不存在时
    """

    if not os.path.exists(json_file):
        raise FileNotFoundError(f"Input file '{json_file}' not found.")
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if data_key not in data:
        raise ValueError(f"Key '{data_key}' not found in JSON data")
    
    if output_file is None:
        output_file = os.path.splitext(json_file)[0] + '.csv'
    
    list_data = data[data_key]
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(list_data)
    
    print(f"Converted {json_file} to {output_file} successfully.")
    return output_file