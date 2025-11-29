"""
插值函数
"""

import numpy as np
from scipy.interpolate import CubicSpline
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
import math


# ==================================================================================================


def global_bezier_interpolation(original_frames, target_frame_count):
    """将原始帧通过全局贝塞尔曲线拟合进行扩展"""
    # n = len(original_frames)
    # t_original = np.linspace(0, 1, n)
    t_target = np.linspace(0, 1, target_frame_count)
    
    # 计算贝塞尔曲线控制点（使用所有原始帧作为控制点）
    def bezier_point(t, control_points):
        n = len(control_points) - 1
        point = [0] * len(control_points[0])
        for i, control_point in enumerate(control_points):
            # 伯恩斯坦多项式
            bernstein = math.comb(n, i) * (t ** i) * ((1 - t) ** (n - i))
            for j in range(len(point)):
                point[j] += control_point[j] * bernstein
        return point
    
    extended_frames = [bezier_point(t, original_frames) for t in t_target]
    return extended_frames


def bezier_interpolation_with_easing(original_frames, target_frame_count, easing_func=None):
    """贝塞尔曲线 + 缓动函数控制节奏"""
    if easing_func is None:
        easing_func = lambda x: x
    
    # n = len(original_frames)
    
    # 目标时间轴（应用缓动函数）
    t_target_linear = np.linspace(0, 1, target_frame_count)
    t_target_eased = [easing_func(t) for t in t_target_linear]
    
    def bezier_point(t, control_points):
        """计算贝塞尔曲线上的点"""
        n_ctrl = len(control_points) - 1
        point = [0] * len(control_points[0])
        for i, control_point in enumerate(control_points):
            bernstein = math.comb(n_ctrl, i) * (t ** i) * ((1 - t) ** (n_ctrl - i))
            for j in range(len(point)):
                point[j] += control_point[j] * bernstein
        return point
    
    # 在缓动后的时间轴上采样贝塞尔曲线
    extended_frames = [bezier_point(t, original_frames) for t in t_target_eased]
    return extended_frames


# ==================================================================================================



def cubic_spline_interpolation(original_frames, target_frame_count):
    """使用三次样条插值进行平滑扩展"""
    if len(original_frames) == 1:
        original_frames.append(original_frames[0].copy())

    n_original = len(original_frames)
    dim = len(original_frames[0])
    
    # 时间轴
    t_original = np.linspace(0, 1, n_original)
    t_target = np.linspace(0, 1, target_frame_count)
    
    extended_frames = []
    
    # 对每个维度分别进行样条插值
    for d in range(dim):
        # 提取该维度的数据
        y_data = [frame[d] for frame in original_frames]
        
        # 创建三次样条
        cs = CubicSpline(t_original, y_data)
        
        # 插值
        y_interpolated = cs(t_target)
        
        if d == 0:
            # 初始化结果列表
            extended_frames = [[y] for y in y_interpolated]
        else:
            # 添加其他维度
            for i, y in enumerate(y_interpolated):
                extended_frames[i].append(y)
    
    return extended_frames


def interpolate_with_easing(original_frames, target_frame_count, easing_func=None):
    """使用缓动函数控制插值节奏"""
    if len(original_frames) == 1:
        original_frames.append(original_frames[0].copy())

    n_original = len(original_frames)
    dim = len(original_frames[0])
    
    # 原始均匀时间轴
    t_original = np.linspace(0, 1, n_original)
    
    # 目标时间轴（应用缓动函数）
    if easing_func is None:
        easing_func = lambda x: x  # 线性
    
    t_target_linear = np.linspace(0, 1, target_frame_count)
    t_target_eased = [easing_func(t) for t in t_target_linear]
    
    extended_frames = []
    
    for d in range(dim):
        y_data = [frame[d] for frame in original_frames]
        
        # 在原始时间轴上创建样条
        cs = CubicSpline(t_original, y_data)
        
        # 在缓动后的时间轴上采样
        y_interpolated = cs(t_target_eased)
        
        if d == 0:
            extended_frames = [[y] for y in y_interpolated]
        else:
            for i, y in enumerate(y_interpolated):
                extended_frames[i].append(y)
    
    return extended_frames



# ==================================================================================================

def gaussian_process_interpolation(original_frames, target_frame_count):
    """使用高斯过程回归进行概率性插值"""
    n_original = len(original_frames)
    dim = len(original_frames[0])
    
    X_original = np.linspace(0, 1, n_original).reshape(-1, 1)
    X_target = np.linspace(0, 1, target_frame_count).reshape(-1, 1)
    
    extended_frames = []
    
    for d in range(dim):
        y_data = [frame[d] for frame in original_frames]
        
        # 定义高斯过程
        kernel = C(1.0, (1e-3, 1e3)) * RBF(1.0, (1e-2, 1e2))
        gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10)
        
        # 训练
        gp.fit(X_original, y_data)
        
        # 预测
        y_interpolated, sigma = gp.predict(X_target, return_std=True)
        
        if d == 0:
            extended_frames = [[y] for y in y_interpolated]
        else:
            for i, y in enumerate(y_interpolated):
                extended_frames[i].append(y)
    
    return extended_frames


def gaussian_process_interpolation_with_easing(original_frames, target_frame_count, easing_func=None):
    """高斯过程回归 + 缓动函数控制节奏"""
    if easing_func is None:
        easing_func = lambda x: x  # 线性
    
    n_original = len(original_frames)
    dim = len(original_frames[0])
    
    # 原始时间轴
    X_original = np.linspace(0, 1, n_original).reshape(-1, 1)
    
    # 目标时间轴（应用缓动函数）
    t_target_linear = np.linspace(0, 1, target_frame_count)
    t_target_eased = [easing_func(t) for t in t_target_linear]
    X_target = np.array(t_target_eased).reshape(-1, 1)
    
    extended_frames = []
    
    for d in range(dim):
        y_data = [frame[d] for frame in original_frames]
        
        # 高斯过程回归
        kernel = C(1.0, (1e-3, 1e3)) * RBF(1.0, (1e-2, 1e2))
        gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10)
        gp.fit(X_original, y_data)
        
        # 在缓动后的时间轴上预测
        y_interpolated = gp.predict(X_target)
        
        if d == 0:
            extended_frames = [[y] for y in y_interpolated]
        else:
            for i, y in enumerate(y_interpolated):
                extended_frames[i].append(y)
    
    return extended_frames



# ==================================================================================================

def ease_in_out_cubic(alpha):
    """三次缓动"""
    return 4 * alpha * alpha * alpha if alpha < 0.5 else 1 - math.pow(-2 * alpha + 2, 3) / 2


# if __name__ == '__main__':
#     import json
#     from custom_json_format import format_dict
#     '''
#     # 表情插值扩展
#     file_name = "/home/myf/myf/work_space/tools/exp3.json"
#     output_file = 'processed_expression_xishiG2_F03.json'
#     with open(file_name, 'r', encoding='UTF-8') as f:
#         expression = json.load(f)

#     res_frames = {}
#     # exp_list = ['微笑', '跳舞', '开心', '点头同意', '调皮', '享受', '生气', '惊讶', '震惊', '惊喜', '难过']
#     exp_list = ['点头', '高兴', '害怕', '害羞', '紧张', '怀疑', '惊讶', '生气', '微笑', '厌恶', '伤心']
#     # 遍历json所有表情，分别进行插值
#     for exp_name in exp_list:
#         target_time = 5000 # ms
#         flash_time = 30 # ms
#         # 根据时间计算要插值多少个
#         target_frame_count = target_time // flash_time 
#         # 如果当前的帧数已经大于默认总时间5s，则时间*2
#         while len(expression[exp_name]) > target_frame_count:
#             target_frame_count *= 2
#         # 进行插值
#         frame = global_bezier_interpolation(expression[exp_name], target_frame_count)
#         # 插值结果保存回字典，之后写入json文件
#         res_frames[exp_name] = frame.copy()

#     # res_frames 写回json文件
#     with open(output_file, 'w', encoding='utf-8') as f:
#         # json.dump(res_frames, f, ensure_ascii=False, indent=4)
#         f.write(format_dict(res_frames))

        
#     print(f'已写入文件{output_file}')

#     '''

#     # result = global_bezier_interpolation([[1]],10)
#     # print(result)