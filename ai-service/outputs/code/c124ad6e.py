import numpy as np
from manim import *

class LawOfLargeNumbers(Scene):
    def construct(self):
        # --------------------------
        # 1. 预计算不同样本量下的标准化样本均值
        # --------------------------
        np.random.seed(42)                 # 固定随机种子，结果可复现
        sample_counts = 2000               # 每个n下生成多少个样本均值
        n_min, n_max = 1, 100              # 样本量范围
        n_values = list(range(n_min, n_max + 1))
        # 数据存储为列表，每个元素是长度为 sample_counts 的数组
        self.standardized_means = []
        for n in n_values:
            # 从伯努利分布 (p=0.5) 采样
            samples = np.random.binomial(n, 0.5, size=sample_counts) / n
            # 标准化：均值 = 0.5，方差 = 0.25/n  →  (mean - 0.5) * 2 * sqrt(n)
            means_std = (samples - 0.5) * 2 * np.sqrt(n)
            self.standardized_means.append(means_std)

        self.bin_edges = np.linspace(-4, 4, 81)  # 80个等宽区间

        # --------------------------
        # 2. 创建坐标轴、正态曲线、直方图初始矩形、标签
        # --------------------------
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 0.5, 0.1],
            x_length=10,
            y_length=5,
            axis_config={"include_numbers": True},
        ).shift(DOWN * 0.5)
        self.add(axes)
        axes_labels = axes.get_axis_labels(
            x_label="标准化样本均值",
            y_label="概率密度"
        )
        self.add(axes_labels)

        # 理论标准正态曲线
        normal_curve = axes.plot(
            lambda x: np.exp(-x**2 / 2) / np.sqrt(2 * np.pi),
            x_range=[-4, 4],
            color=YELLOW,
        )
        self.add(normal_curve)

        # 直方图的矩形容器
        hist_bars = VGroup()
        n_bins = len(self.bin_edges) - 1
        for _ in range(n_bins):
            rect = Rectangle(
                width=0.01, height=0.01,
                color=BLUE, fill_opacity=0.6,
                stroke_width=1,
            )
            rect.set_stroke(GREY, opacity=0.3)
            hist_bars.add(rect)
        self.add(hist_bars)

        # 显示当前样本量的标签
        n_label = Tex("n = 1", font_size=28).to_corner(UR)
        self.add(n_label)

        # 控制样本量变化的 ValueTracker (从0到1)
        n_tracker = ValueTracker(0)

        # --------------------------
        # 3. 定义 updater，负责更新直方图和标签
        # --------------------------
        def update_histogram(mobs, dt):
            # 根据 n_tracker 的值计算当前整数样本量
            t = n_tracker.get_value()
            n_float = n_min + (n_max - n_min) * t
            n_int = int(np.clip(n_float, n_min, n_max))
            n_idx = n_int - n_min  # 对应预计算数组的索引

            # 获取当前样本均值数据
            data = self.standardized_means[n_idx]

            # 计算频数
            counts, _ = np.histogram(data, bins=self.bin_edges, density=False)
            bin_width = self.bin_edges[1] - self.bin_edges[0]
            # 概率密度 = 频数 / (总样本数 * 区间宽度)
            density = counts / (sample_counts * bin_width)

            # 更新每个矩形
            for i, rect in enumerate(hist_bars):
                left = self.bin_edges[i]
                right = self.bin_edges[i+1]
                center = (left + right) / 2
                height = density[i]

                # 如果高度为0，设置一个极小的值以避免宽度消失
                if height <= 0:
                    rect.set_height(0.001)
                else:
                    rect.set_height(height, stretch=True)
                # 设置宽度（固定）
                rect.set_width(bin_width * 0.95, stretch=True)
                # 移动矩形的底部到 y=0（数据坐标）
                bottom_point = axes.c2p(center, 0)
                rect.move_to(bottom_point, aligned_edge=DOWN)
                # 如果高度极低，直接隐藏
                if height < 0.001:
                    rect.set_opacity(0)
                else:
                    rect.set_opacity(0.6)

            # 更新标签
            new_label = Tex(f"n = {n_int}", font_size=28).to_corner(UR)
            n_label.become(new_label)

        hist_bars.add_updater(update_histogram)

        # --------------------------
        # 4. 启动动画
        # --------------------------
        # 让 n_tracker 在 28 秒内从 0 线性增长到 1
        self.play(
            n_tracker.animate.set_value(1),
            run_time=28,
            rate_func=linear,
        )
        self.wait(2)   # 停留，总时长 ≈ 30 秒