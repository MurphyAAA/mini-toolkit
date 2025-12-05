import json

class HeadConfigChecker:
    def __init__(self, config_path, head_name):
        """
        头模组配置检查器
        
        Args:
            config_path: 配置文件路径
            head_name: 头模组名称
        """
        self.config_path = config_path
        self.head_name = head_name
        
        # 默认角度比例（固定值）
        self.default_angles = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 
                            0.2, 0.2, 0.5, 0.5, 0.2, 0.5, 0, 0.2, 
                            0.2, 0.5, 0, 0.2, 0.5, 0.2, 0.5, 0.2, 
                            0, 0, 0.5, 0.5]
        
        # 对称检查的舵机对（索引）
        self.checking_pair_ids = [
            (0, 1), (2, 3), (4, 5), (7, 8), (9, 10), 
            (11, 14), (15, 18), (19, 21), (20, 22), 
            (23, 24), (25, 26)
        ]
        
        self.motor_names = []
        self.angles = []
        self.ranges = []
        
    def load_config(self):
        """加载配置文件并解析数据"""
        try:
            with open(self.config_path, "r", encoding="utf-8") as file:
                config_file = json.load(file)
            
            if self.head_name not in config_file:
                raise ValueError(f"在配置文件中找不到头模组 '{self.head_name}'")
                
            head_config = config_file[self.head_name]
            
            # 解析配置数据
            self.motor_names = list(head_config.keys())
            self.angles = []
            self.ranges = []
            
            for motor_name in self.motor_names:
                motor_config = head_config[motor_name]
                angle_config = motor_config["angle"]
                self.angles.append(angle_config)
                self.ranges.append(angle_config[-1] - angle_config[0])
                
            return True
            
        except Exception as e:
            print(f"加载配置失败: {e}")
            return False
    
    def check_symmetry(self):
        """执行对称性检查"""
        asymmetry_list = []
        
        for i, j in self.checking_pair_ids:
            if i < len(self.ranges) and j < len(self.ranges):
                if self.ranges[i] != self.ranges[j]:
                    asymmetry_list.append((i, j))
        
        return asymmetry_list
    
    def check_defaults(self):
        """执行默认值检查"""
        correct_defaults = []
        
        for i, default_ratio in enumerate(self.default_angles):
            if i < len(self.angles) and i < len(self.ranges):
                corr_default = round(self.angles[i][0] + self.ranges[i] * default_ratio)
                if self.angles[i][1] != corr_default:
                    correct_defaults.append(
                        (self.motor_names[i], corr_default, self.angles[i][1])
                    )
        
        return correct_defaults
    
    def run_checks(self):
        """
        运行所有检查
        
        Returns:
            bool: 是否全部检查通过
        """
        if not self.load_config():
            return False
        
        # 对称性检查
        asymmetry_list = self.check_symmetry()
        
        # 默认值检查
        correct_defaults = self.check_defaults()
        
        # 打印结果
        self._print_results(asymmetry_list, correct_defaults)
        
        # 返回是否全部通过
        return len(asymmetry_list) == 0 and len(correct_defaults) == 0


    def _print_results(self, asymmetry_list, correct_defaults):
        """打印检查结果"""
        # 对称性检查输出
        print("="*20, " 对称性检查 ", "="*20)
        if asymmetry_list:
            print(" 活动范围不对称舵机如下：")
            for i, j in asymmetry_list:
                print(f"  >> {self.motor_names[i]} - {self.ranges[i]}度 // "
                      f"{self.motor_names[j]} - {self.ranges[j]}度")
        else:
            print("对称性检查通过。")
        print("="*54, "\n")
        
        # 默认值检查输出
        print("="*20, " 默认值检查 ", "="*20)
        if correct_defaults:
            print(" 默认值错误舵机如下：")
            for motor_name, correct_val, current_val in correct_defaults:
                print(f"  >> {motor_name} 正确默认值:{correct_val}. 当前值为:{current_val}.")
        else:
            print("默认值检查通过。")
        print("="*54)




if __name__ == "__main__":
    checker = HeadConfigChecker("/home/myf/myf/work_space/em/config/head.json", "xishiG2_F02_ID05")
    result = checker.run_checks()
    