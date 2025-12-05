import argparse
import mini_toolkit.core.csv2json as csv2json
import mini_toolkit.core.json2csv as json2csv
import mini_toolkit.core.concate_csv as concat_csv
import mini_toolkit.core.HeadConfigChecker as HeadConfigChecker


def main_json2csv():
    parser = argparse.ArgumentParser(description="Convert JSON to CSV")
    parser.add_argument("-i", "--input", required=True, help="Input JSON file path")
    parser.add_argument("-o", "--output", help="Output CSV file path")
    parser.add_argument("-k", "--key", default="key", help="Key to extract from JSON")
    args = parser.parse_args()
    out_file = json2csv.json_to_csv(args.input, args.output, data_key=args.key)
    print(f"[INFO] Converted JSON to CSV: {out_file}")


def main_csv2json():
    parser = argparse.ArgumentParser(description="Convert CSV to JSON")
    parser.add_argument("-i", "--input", required=True, help="Input CSV file path")
    parser.add_argument("-o", "--output", help="Output JSON file path")
    args = parser.parse_args()
    out_file = csv2json.csv_to_json(args.input, args.output)
    print(f"[INFO] Converted CSV to JSON: {out_file}")


def main_concat_csv():
    parser = argparse.ArgumentParser(description="Concatenate multiple CSV files in a folder")
    parser.add_argument("-d", "--dir", required=True, help="Directory containing CSV files")
    parser.add_argument("-o", "--output", required=True, help="Output CSV file path")
    parser.add_argument("-m", "--mode", default="vertical", choices=["vertical", "horizontal"], help="Concatenation mode: vertical or horizontal")
    args = parser.parse_args()
    out_file = concat_csv.concatenate_csv_files(args.dir, args.output, mode=args.mode)
    if out_file:
        print(f"[INFO] Concatenated CSV files into: {out_file}")
    else:
        print("[WARNING] No CSV files were concatenated.")

def main_check_head_config():
    parser = argparse.ArgumentParser(description="检查头模组配置文件中的舵机对称性和默认值")
    # parser.add_argument("-f", "--file", default="/home/myf/myf/work_space/em/config/head.json", help="头模组配置文件路径")
    # parser.add_argument("-n", "--name", default="xishiG2_F02_ID05", help="要检查的头模组名称")
    parser.add_argument("-f", "--file", required=True, help="头模组配置文件路径")
    parser.add_argument("-n", "--name", required=True, help="要检查的头模组名称")
    args = parser.parse_args()
    
    # 使用HeadConfigChecker类
    checker = HeadConfigChecker.HeadConfigChecker(args.file, args.name)
    result = checker.run_checks()
    
    if result:
        print(f"[INFO] 头模组配置检查完成: {args.file} - {args.name}")
    else:
        print(f"[WARNING] 头模组配置检查失败或发现异常: {args.file} - {args.name}")

