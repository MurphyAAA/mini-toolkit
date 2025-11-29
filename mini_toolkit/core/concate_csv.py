import pandas as pd
import os
import glob
from typing import Optional

def concatenate_csv_files(data_path: str, output_file: str, mode: str="vertical") -> Optional[str]:
    """
    合并指定目录下的所有 CSV 文件并保存为一个 CSV 文件。

    Args:
        data_path (str): 包含 CSV 文件的目录路径
        output_file (str): 输出 CSV 文件路径
        mode (str): 合并模式，默认为"vertical" 垂直拼接，可选值有 "vertical" 和 "horizontal"

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
    
    if not dataframes:
        print("[WARNING] No dataframes to concatenate.")
        return None
    
    mode = mode.lower()
    if mode == "vertical":
        merged_df = pd.concat(dataframes, axis=0, ignore_index=True)
    elif mode == "horizontal":
        max_len = max(len(df) for df in dataframes)
        padding_dfs = []
        for i, df in enumerate(dataframes):
            if len(df) < max_len:
                print(f"[INFO] Padding '{csv_files[i]}' from length {len(df)} to {max_len} with 0")
                df = df.reindex(range(max_len)) # 补行(NaN)
                df = df.fillna(0)
            padding_dfs.append(df)
        merged_df = pd.concat(padding_dfs, axis=1)
    else:
        raise ValueError("Invalid mode. Choose 'vertical' or 'horizontal'.")

    merged_df.to_csv(output_file, index=False)
    print(f"[INFO] Successfully merged {len(dataframes)} CSV files into '{output_file}'")
    return output_file

    
# if __name__ == "__main__": 
#     data_path = '/home/myf/myf/work_space/ARServo/data/raw/recorded/filtered_dataset' 
#     output_file = '/home/myf/myf/work_space/ARServo/data/raw/recorded/filtered_dataset/filtered_dataset31k.csv' 
#     concatenate_csv_files(data_path, output_file)