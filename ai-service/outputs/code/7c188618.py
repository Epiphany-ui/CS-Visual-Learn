import numpy as np
from manim import *

class LawOfLargeNumbers(Scene):
    def construct(self):
        # --------------------------
        # 1. 预计算不同样本量下的标准化样本均值
        # --------------------------
        np.random.seed(42)
        sample_counts = 2000
        n_min, n_max = 1, 100
        n_values = list(range(n_min, n_max + 1))
        self.standardized_means = []
        for n in n_values:
            samples = np.random.binomial(n, 0.5, size=sample_counts) / n
            means_std = (samples - 0.5) * 2 * np.sqrt(n)
            self.standardized_means.append(means_std)

        self.bin_edges = np.linspace(-4, 4, 81)

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
        # 使用 Text 替代 Tex 以支持中文
        x_label = Text("标准化样本均值", font_size=28).next_to(axes.x_axis, DOWN)
        y_label = Text("概率密度", font_size=28).next_to(axes.y_axis, LEFT)
        axes_labels = VGroup(x_label, y_label)
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

        # 显示当前样本量的标签（使用 Text）
        n_label = Text("n = 1", font_size=28).to_corner(UR)
        self.add(n_label)

        # 控制样本量变化的 ValueTracker (从0到1)
        n_tracker = ValueTracker(0)

        # --------------------------
        # 3. 定义 updater，负责更新直方图和标签
        # --------------------------
        def update_histogram(mob, dt):
            t = n_tracker.get_value()
            n_float = n_min + (n_max - n_min) * t
            n_int = int(np.clip(n_float, n_min, n_max))
            n_idx = n_int - n_min

            data = self.standardized_means[n_idx]

            counts, _ = np.histogram(data, bins=self.bin_edges, density=False)
            bin_width = self.bin_edges[1] - self.bin_edges[0]
            density = counts / (sample_counts * bin_width)

            for i, rect in enumerate(hist_bars):
                left = self.bin_edges[i]
                right = self.bin_edges[i+1]
                center = (left + right) / 2
                height = density[i]

                if height <= 0:
                    rect.set_height(0.001)
                else:
                    rect.set_height(height, stretch=True)
                rect.set_width(bin_width * 0.95, stretch=True)
                bottom_point = axes.c2p(center, 0)
                rect.move_to(bottom_point, aligned_edge=DOWN)
                if height < 0.001:
                    rect.set_opacity(0)
                else:
                    rect.set_opacity(0.6)

            new_label = Text(f"n = {n_int}", font_size=28).to_corner(UR)
            n_label.become(new_label)

        hist_bars.add_updater(update_histogram)

        # --------------------------
        # 4. 启动动画
        # --------------------------
        self.play(
            n_tracker.animate.set_value(1),
            run_time=28,
            rate_func=linear,
        )
        self.wait(2)