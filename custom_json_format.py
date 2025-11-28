import json
"""
仿生头表情的json格式
{
    exp_name:[
        [xxxx],
        [xxxx],
    ]
}
"""
# 手动构建JSON格式，支持多级列表
def format_value(value, indent_level):
    """递归格式化值"""
    indent = '    ' * indent_level
    
    if isinstance(value, list):
        # 检查是否是二维数组
        if value and all(isinstance(item, list) for item in value):
            # 二维数组：外层竖排，内层横排
            result = '[\n'
            for i, sublist in enumerate(value):
                result += f'{indent}    {json.dumps(sublist, ensure_ascii=False)}'
                if i < len(value) - 1:
                    result += ','
                result += '\n'
            result += f'{indent}]'
            return result
        else:
            # 一维数组：横排
            return json.dumps(value, ensure_ascii=False)
    elif isinstance(value, dict):
        # 字典：正常缩进
        return format_dict(value, indent_level)
    else:
        return json.dumps(value, ensure_ascii=False)

def format_dict(obj, indent_level=0):
    """格式化字典"""
    indent = '    ' * indent_level
    result = '{\n'
    
    items = list(obj.items())
    for i, (key, value) in enumerate(items):
        result += f'{indent}    "{key}": {format_value(value, indent_level + 1)}'
        if i < len(items) - 1:
            result += ','
        result += '\n'
    
    result += f'{indent}}}'
    return result