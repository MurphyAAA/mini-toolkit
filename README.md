一些常用工具
## 安装
```shell
    pip install dist/mini_toolkit-0.1.0-py3-none-any.whl
```


## 目录

### 1. concate_csv.py
**文件夹下多个csv拼接为一个csv文件，用于合并数据集**

#### 使用

##### CLI
```shell
    concat_csv -d ./data_folder -o merged.csv
```
- -d / --data-path: folder containing CSV files
- -o / --output: output CSV file

##### 导入
```python
    from mini_toolkit.core.concat_csv import concatenate_csv_files
    
    concatenate_csv_files("./dataset", "merged.csv")
```

### 2. json2csv.py
**json文件转为csv**

#### 使用

##### CLI
```shell
    json2csv -i data.json -o data.csv -k key
```
- -i / --input: input JSON file
- -o / --output: output CSV file (optional, default: same name as input)
- -k / --key: key in JSON to convert (default: "key")

##### 导入
```python
    from mini_toolkit.core.json2csv import json_to_csv
    output_file = json_to_csv("data.json", output_file="data.csv", data_key="key")
```


### 3. csv2json.py
**csv文件转为json**

#### 使用

##### CLI
```shell
    csv2json -i input.csv -o output.json
```
- -i / --input: input CSV file
- -o / --output: output JSON file (optional, default: same name as input)

##### 导入
```python
    from mini_toolkit.core.csv2json import csv_to_json
    
    csv_to_json("data.csv", output_file="data.json")
```



### 4. interpolation.py
**直接对list计算插值**

#### 使用
##### 1. 
```python
    from mini_toolkit.core.interpolation import 
    global_bezier_interpolation, bezier_interpolation_with_easing,
    cubic_spline_interpolation, interpolate_with_easing,
    gaussian_process_interpolation, gaussian_process_interpolation_with_easing
    

    frames = [[0, 1], [1, 2], [2, 3]]  # example frames
    extended = cubic_spline_interpolation(frames, target_frame_count=10)

    # With easing function
    def ease_in_out_cubic(alpha):
        """三次缓动"""
        return 4 * alpha * alpha * alpha if alpha < 0.5 else 1 - math.pow(-2 * alpha + 2, 3) / 2

    extended_eased = interpolate_with_easing(frames, target_frame_count=10, easing_func=ease_in_out_cubic)

```
##### 2. 
```python
    import json
    from custom_json_format import format_dict
    
    file_name = "xxx.json"
    output_file = 'pxxx.json'
    with open(file_name, 'r', encoding='UTF-8') as f:
        expression = json.load(f)

    res_frames = {}
    exp_list = ['微笑', '跳舞', '开心', '点头同意', '调皮', '享受', '生气', '惊讶', '震惊', '惊喜', '难过']
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
        # 插值结果保存回字典
        res_frames[exp_name] = frame.copy()
        # res_frames 写回json文件

    with open(output_file, 'w', encoding='utf-8') as f:
        # json.dump(res_frames, f, ensure_ascii=False, indent=4)
        f.write(format_dict(res_frames))

    print(f'已写入文件{output_file}')
```

### 5. filter.py
**滤波方法**

```python
    from mini_toolkit.core.filter import SmartEWMA
    import torch

    ewma = SmartEWMA(alpha=0.3, speed_limit=0.1,alpha_min=0.05, alpha_max=0.9, k=8.0)
    x = torch.randn(10, 55)  # example tensor
    filtered = ewma.update_list(x)
```


### 6. custom_json_format.py 
**自定义json输出的格式**

```python
    from mini_toolkit.core.custom_json_format import format_dict

    with open(output_file, 'w', encoding='utf-8') as f:
        # json.dump(res_frames, f, ensure_ascii=False, indent=4)
        f.write(format_dict(res_frames))
```


