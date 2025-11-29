if __name__ == '__main__':
    import json
    from custom_json_format import format_dict
    
    file_name = "/home/myf/myf/work_space/em/config/xishi_F03_expression.json/xishiG2_F03_expression.json"
    output_file = 'processed_xishiG2_F03_expression.json'
    with open(file_name, 'r', encoding='UTF-8') as f:
        expression = json.load(f)
        expression = expression['xishiG2_F03']

    res_frames = {}
    exp_list = ["重置", "空表情", "点头", "高兴", "害怕", "害羞", "紧张", "怀疑", "惊讶", "生气", "微笑", "厌恶", "伤心"]
    # exp_list = ["重置"]

    for exp_name in exp_list:
        res_rows = [] # 同一个表情的所有行
        rows = expression[exp_name]
        for row in rows:
            # print(len(row))
            tmp = row[:7] + [0] + row[7:] + [0, 0, 0, 0]
            res_rows.append(tmp)
        # print(len(rows))
        # 插值结果保存回字典，之后写入json文件
        res_frames[exp_name] = res_rows.copy()
    # print(res_frames, len(res_frames["重置"][0]))
    # res_frames 写回json文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(format_dict(res_frames))

        
    print(f'已写入文件{output_file}')