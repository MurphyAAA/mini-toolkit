import numpy as np
import torch
import pandas as pd
from scipy.signal import savgol_filter


class SmartEWMA:
    def __init__(self, alpha=0.5, speed_limit=None,
                 alpha_min=0.05, alpha_max=0.9, k=8.0):
        self.alpha = alpha              # 基础 EWMA
        self.speed_limit = speed_limit  # 最大速度限制
        self.alpha_min = alpha_min      # 动态 alpha 下限
        self.alpha_max = alpha_max      # 动态 alpha 上限
        self.k = k                      # 动态 alpha 放大系数

        self.value = None               # 上一帧值
        self.values = None          # 55维输入的上一帧值
        self.initilaized = False

    def update(self, new):
        new = float(new)

        # 第一次
        if self.value is None:
            self.value = new
            return new

        # 动态 alpha
        delta = abs(new - self.value)
        alpha_dynamic = np.clip(delta * self.k,
                                self.alpha_min,
                                self.alpha_max)

        # EWMA
        filtered = alpha_dynamic * new + (1 - alpha_dynamic) * self.value

        # 限速
        if self.speed_limit is not None:
            diff = filtered - self.value
            if abs(diff) > self.speed_limit:
                filtered = self.value + self.speed_limit * (1 if diff > 0 else -1)

        self.value = filtered
        return filtered
    
    def update_list(self, new_list: torch.Tensor):
        assert isinstance(new_list, torch.Tensor), f"输入必须是 torch.Tensor，但得到 {type(new_list)}"
        assert new_list.shape[-1] == 55, f"输入的最后维度必须是55，但得到 {new_list.shape[-1]}"

        if new_list.dtype != torch.float32:
            new_list = new_list.to(torch.float32)

        # 第一次
        if not self.initilaized:
            self.values = new_list.clone()
            self.initilaized = True
            return new_list.clone()

        if self.values.device != new_list.device:
            self.values = self.values.to(new_list.device)

        # 动态 alpha
        delta = torch.abs(new_list - self.values)
        alpha_dynamic = torch.clamp(delta * self.k, self.alpha_min, self.alpha_max)

        # EWMA
        filtered = alpha_dynamic * new_list + (1 - alpha_dynamic) * self.values

        # 限速
        if self.speed_limit is not None:
            diff = filtered - self.values
            speed_mask = torch.abs(diff) > self.speed_limit

            direction = torch.where(diff>0, 1.0, -1.0)
            correction = self.values + self.speed_limit * direction

            filtered = torch.where(speed_mask, correction, filtered)

        self.values = filtered.clone()
        return filtered.clone()
    

def non_causal_filter():
    """
    它不直接对窗口内的数据进行平均，而是用一个多项式来拟合这些数据点，然后用这个拟合出的多项式在中心点的值，作为平滑后的新值。
    对于每个窗口位置，用一个指定阶数（例如，二次或三次）的多项式，对窗口内的所有数据点进行最小二乘拟合
    取这个拟合出的多项式在窗口中心点的值，作为该点平滑后的输出值。
    整个“局部多项式最小二乘拟合”的过程，等价于一维离散卷积。
    """
    # 读取文件
    df = pd.read_csv("recorded_arkit_servo_11k_o.csv")

    filtered_df = df.copy()

    # SG 滤波参数
    window = 7   # 必须为奇数
    poly = 3

    # 对前 55 列进行非因果平滑
    for col in df.columns[:55]:
        filtered_df[col] = savgol_filter(
            df[col],
            window_length=window,
            polyorder=poly,
            mode='interp'
        )

    # 保存
    filtered_df.to_csv("filtered_data.csv", index=False)

    print("done!")



inputs = [[0.28798854, 0.42190576, 0.02740046, 0.24077058, 0.02524265, 0.42497808, 0.00254169, 0.30828366, 0.38270852, 0.23165941, 0.00878475, 0.01652773, 0.38568485, 0.00100611, 3.923e-05, 5.277e-05, 0.00129827, 0.00847114, 0.00308516, 0.00104271, 0.07539622, 0.00359017, 0.00032477, 6.645e-05, 0.00010321, 0.00126185, 0.00095213, 0.00038232, 0.00975903, 0.00153509, 0.00116839, 0.01055456, 0.0045683, 0.00978505, 0.00386939, 0.00526815, 0.03229946, 0.0007037, 0.00035895, 3.968e-05, 0.00010344, 0.00302992, 0.00273124, 0.12467154, 0.33761945, 0.12479063, 8.28e-06, 1.4e-07, 5e-08, 1.28e-06, 1.6e-07, 0, -0.011540991, 0.05043092244881334, -0.014294233],
[0.28798854, 0.42190576, 0.02740046, 0.24077058, 0.02524265, 0.42497808, 0.00254169, 0.30828366, 0.38270852, 0.23165941, 0.00878475, 0.01652773, 0.38568485, 0.00100611, 3.923e-05, 5.277e-05, 0.00129827, 0.00847114, 0.00308516, 0.00104271, 0.07539622, 0.00359017, 0.00032477, 6.645e-05, 0.00010321, 0.00126185, 0.00095213, 0.00038232, 0.00975903, 0.00153509, 0.00116839, 0.01055456, 0.0045683, 0.00978505, 0.00386939, 0.00526815, 0.03229946, 0.0007037, 0.00035895, 3.968e-05, 0.00010344, 0.00302992, 0.00273124, 0.12467154, 0.33761945, 0.12479063, 8.28e-06, 1.4e-07, 5e-08, 1.28e-06, 1.6e-07, 0, -0.011540991, 0.05043092244881334, -0.014294233]]
inputs = torch.tensor(inputs)
if __name__ == "__main__":
    filter = SmartEWMA(alpha=0.4, speed_limit=0.2, alpha_max=0.85, alpha_min=0.15, k=18)


    # 一维输入 (55,)
    input_1d = torch.randn(55)
    output_1d = filter.update_list(input_1d)
    print(f"一维输入: {input_1d.shape} -> {output_1d.shape}")

    # 二维输入 (batch_size, 55)
    input_2d = torch.randn(3, 55)
    filter = SmartEWMA(alpha=0.4, speed_limit=0.2, alpha_max=0.85, alpha_min=0.15, k=18)
    output_2d = filter.update_list(input_2d)
    print(f"二维输入: {input_2d.shape} -> {output_2d.shape}")

    # 三维输入 (batch_size, seq_len, 55)
    input_3d = torch.randn(2, 5, 55)
    filter = SmartEWMA(alpha=0.4, speed_limit=0.2, alpha_max=0.85, alpha_min=0.15, k=18)
    output_3d = filter.update_list(input_3d)
    print(f"三维输入: {input_3d.shape} -> {output_3d.shape}")

    # 错误输入测试
    try:
        wrong_input = torch.randn(54)
        filter = SmartEWMA(alpha=0.4, speed_limit=0.2, alpha_max=0.85, alpha_min=0.15, k=18)
        filter.update_list(wrong_input)
    except AssertionError as e:
        print(f"错误输入捕获: {e}")







