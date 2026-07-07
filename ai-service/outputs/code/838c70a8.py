from manim import *
import numpy as np
import random
import math

class CenterLimitTheorem(Scene):
    def construct(self):
        # 参数设置
        n = 10                               # 每个样本的大小
        total_samples = 2000                 # 模拟的总样本数
        bins = 20                           # 直方图的组数
        x_min, x_max = 0.2, 0.8            # 横轴范围
        mu = 0.5                            # 总体均值
        sigma_pop = math.sqrt(1/12)         # 总体标准差（均匀分布U(0,1)）
        sigma_mean = sigma_pop / math.sqrt(n)  # 样本均值的标准差

        bin_width = (x_max - x_min) / bins

        # 生成所有样本均值
        means = []
        for _ in range(total_samples):
            s = sum(random.random() for _ in range(n)) / n
            means.append(s)

        # 创建坐标轴
        ax = Axes(
            x_range=[x_min, x_max, 0.1],
            y_range=[0, 8, 1],
            x_length=10,
            y_length=5,
            axis_config={"include_numbers": True}
        ).shift(2 * LEFT)
        x_label = ax.get_x_axis_label(Tex("样本均值"))
        y_label = ax.get_y_axis_label(Tex("频率密度"))

        # 理论正态曲线
        def norm_func(x):
            return np.exp(-(x - mu)**2 / (2 * sigma_mean**2)) / (sigma_mean * np.sqrt(2 * np.pi))

        curve = ax.plot(norm_func, x_range=[x_min, x_max], color=YELLOW, stroke_width=2)
        curve_label = MathTex(r"\mathcal{N}(\mu, \sigma/\sqrt{n})", color=YELLOW).scale(0.6).next_to(curve, UR)

        # 创建直方图的矩形条
        rects = VGroup()
        for i in range(bins):
            x_center = x_min + i * bin_width + bin_width / 2
            bottom_point = ax.c2p(x_center, 0)
            # 计算像素宽度
            left_x = ax.c2p(x_min + i * bin_width, 0)[0]
            right_x = ax.c2p(x_min + (i + 1) * bin_width, 0)[0]
            width_px = right_x - left_x
            rect = Rectangle(
                width=width_px,
                height=0,
                fill_opacity=0.6,
                fill_color=BLUE,
                stroke_color=BLUE,
                stroke_width=1
            )
            rect.move_to(bottom_point, aligned_edge=DOWN)
            rects.add(rect)

        # 样本数计数器
        count_text = Tex("样本数: 0").to_corner(UR)

        # 将静态元素添加到场景
        self.add(ax, x_label, y_label, curve, curve_label, rects, count_text)

        # 初始化计数和已处理数量
        self.counts = [0] * bins
        self.processed = 0
        tracker = ValueTracker(0)

        # 更新函数（每帧调用）
        def update_histogram(mob, dt):
            target = int(tracker.get_value())
            # 处理新增的样本均值
            while self.processed < target and self.processed < len(means):
                val = means[self.processed]
                idx = int((val - x_min) // bin_width)
                if 0 <= idx < bins:
                    self.counts[idx] += 1
                self.processed += 1
            total_now = self.processed
            # 更新每个矩形的高度（频率密度）
            for i, rect in enumerate(rects):
                density = self.counts[i] / (total_now * bin_width) if total_now > 0 else 0
                # 限制密度不超过坐标轴上限
                density = min(density, ax.y_range[1])
                # 将密度值转换为像素高度
                top = ax.c2p(0, density)
                bottom = ax.c2p(0, 0)
                height = top[1] - bottom[1]  # c2p返回二维数组？实际是三维，取第1维
                rect.set_height(max(height, 0))
            # 更新计数器文本
            new_text = Tex(f"样本数: {total_now}").to_corner(UR)
            count_text.become(new_text)

        rects.add_updater(update_histogram)

        # 播放动画：tracker从0增加到total_samples
        self.play(tracker.animate.set_value(total_samples), run_time=15, rate_func=linear)
        self.wait(2)

        # 清除更新器
        rects.clear_updaters()