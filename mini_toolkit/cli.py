import argparse
import mini_toolkit.core.csv2json as csv2json
import mini_toolkit.core.json2csv as json2csv
import mini_toolkit.core.concate_csv as concat_csv


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
    args = parser.parse_args()
    out_file = concat_csv.concatenate_csv_files(args.dir, args.output)
    if out_file:
        print(f"[INFO] Concatenated CSV files into: {out_file}")
    else:
        print("[WARNING] No CSV files were concatenated.")