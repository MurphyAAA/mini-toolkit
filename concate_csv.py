import pandas as pd
import os
import glob

def concatenate_csv_files(data_path, output_file):
    if not data_path.endswith('/'):
        data_path += '/'
    csv_files = glob.glob(os.path.join(data_path, '*.csv'))

    if not csv_files:
        print("No CSV files found in the specified directory.")
        return
    dataframes = []
    for file in csv_files:
        try:
            df = pd.read_csv(file)
            dataframes.append(df)
            print(f"Loaded {file} with shape {df.shape}")
        except Exception as e:
            print(f"Error reading {file}: {e}")
    
    if dataframes:
        merged_df = pd.concat(dataframes, ignore_index=True)
        merged_df.to_csv(output_file, index=False)
        print(f"Successfully merged CSV files into {output_file}")
    else:
        print("No dataframes to concatenate.")

if __name__ == "__main__":

    data_path = '/home/myf/myf/work_space/ARServo/data/raw/recorded/filtered_dataset'
    output_file = '/home/myf/myf/work_space/ARServo/data/raw/recorded/filtered_dataset/filtered_dataset31k.csv'
    concatenate_csv_files(data_path, output_file)
