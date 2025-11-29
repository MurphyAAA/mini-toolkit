import json
import math
from custom_json_format import format_dict
from interpolation import global_bezier_interpolation

if __name__ == '__main__':
    # 表情插值扩展
    file_name = "/home/myf/myf/work_space/tools/exp3.json"
    output_file = 'processed_expression_xishiG2_F03.json'
    with open(file_name, 'r', encoding='UTF-8') as f:
        expression = json.load(f)

    res_frames = {}
    # exp_list = ['微笑', '跳舞', '开心', '点头同意', '调皮', '享受', '生气', '惊讶', '震惊', '惊喜', '难过']
    exp_list = ['点头', '高兴', '害怕', '害羞', '紧张', '怀疑', '惊讶', '生气', '微笑', '厌恶', '伤心']
    # 遍历json所有表情，分别进行插值
    for exp_name in exp_list:
        target_time = 5000 # ms
        flash_time = 30 # ms
        # 根据时间计算要插值多少个
        target_frame_count = target_time // flash_time 
        # 如果当前的帧数已经大于默认总时间5s，则时间*2
        while len(expression[exp_name]) > target_frame_count:
            target_frame_count *= 2
        # 进行插值
        frame = global_bezier_interpolation(expression[exp_name], target_frame_count)
        # 插值结果保存回字典，之后写入json文件
        res_frames[exp_name] = frame.copy()

    # res_frames 写回json文件
    with open(output_file, 'w', encoding='utf-8') as f:
        # json.dump(res_frames, f, ensure_ascii=False, indent=4)
        f.write(format_dict(res_frames))

        
    print(f'已写入文件{output_file}')
