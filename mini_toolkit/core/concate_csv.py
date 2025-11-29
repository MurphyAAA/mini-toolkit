import pandas as pd
import os
import glob
from typing import Optional

def concatenate_csv_files(data_path: str, output_file: str) -> Optional[str]:
    """
    合并指定目录下的所有 CSV 文件并保存为一个 CSV 文件。

    Args:
        data_path (str): 包含 CSV 文件的目录路径
        output_file (str): 输出 CSV 文件路径

    Returns:
        str: 输出文件路径，如果没有找到文件返回 None
    """
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data path '{data_path}' does not exist.")

    if not data_path.endswith(os.sep):
        data_path += os.sep

    csv_files = glob.glob(os.path.join(data_path, '*.csv'))

    if not csv_files:
        print("[WARNING] No CSV files found in the specified directory.")
        return None

    dataframes = []
    for file in csv_files:
        try:
            df = pd.read_csv(file)
            dataframes.append(df)
            print(f"[INFO] Loaded '{file}' with shape {df.shape}")
        except Exception as e:
            print(f"[ERROR] Error reading '{file}': {e}")

    if dataframes:
        merged_df = pd.concat(dataframes, ignore_index=True)
        merged_df.to_csv(output_file, index=False)
        print(f"[INFO] Successfully merged {len(dataframes)} CSV files into '{output_file}'")
        return output_file
    else:
        print("[WARNING] No dataframes to concatenate.")
        return None
    
# if __name__ == "__main__": 
#     data_path = '/home/myf/myf/work_space/ARServo/data/raw/recorded/filtered_dataset' 
#     output_file = '/home/myf/myf/work_space/ARServo/data/raw/recorded/filtered_dataset/filtered_dataset31k.csv' 
#     concatenate_csv_files(data_path, output_file)