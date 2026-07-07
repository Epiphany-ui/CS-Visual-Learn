import numpy as np
from manim import *

class LawOfLargeNumbers(Scene):
    def construct(self):
        # --------------------------
        # 1. 预计算不同样本量下的标准化样本均值（减少样本量和样本数）
        # --------------------------
        np.random.seed(42)
        sample_counts = 500                 # 从1000减至500
        n_min, n_max = 1, 50                # 从100减至50
        n_values = list(range(n_min, n_max + 1))
        self.standardized_means = []
        for n in n_values:
            samples = np.random.binomial(n, 0.5, size=sample_counts) / n
            means_std = (samples - 0.5) * 2 * np.sqrt(n)
            self.standardized_means.append(means_std)

        # 减少直方图 bin 数量（61 → 41），降低更新开销
        self.bin_edges = np.linspace(-4, 4, 41)
        bin_width = self.bin_edges[1] - self.bin_edges[0]

        # 预计算每个 n 对应的直方图密度
        self.hist_densities = []
        for data in self.standardized_means:
            counts, _ = np.histogram(data, bins=self.bin_edges, density=False)
            density = counts / (sample_counts * bin_width)
            self.hist_densities.append(density)

        # 预计算每个 bin 中心对应的坐标系底部点
        n_bins = len(self.bin_edges) - 1
        self.bin_bottom_points = []

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

        # 预计算底部点（在 axes 创建之后）
        for i in range(n_bins):
            center = (self.bin_edges[i] + self.bin_edges[i+1]) / 2
            bottom_point = axes.c2p(center, 0)
            self.bin_bottom_points.append(bottom_point)

        # 创建直方图矩形容器（固定宽度，只更新高度和位置）
        hist_bars = VGroup()
        for i in range(n_bins):
            rect = Rectangle(
                width=bin_width * 0.95,       # 宽度固定
                height=0.01,
                color=BLUE, fill_opacity=0.6,
                stroke_width=1,
            )
            rect.set_stroke(GREY, opacity=0.3)
            # 放置在预计算底部点处（底部对齐）
            rect.move_to(self.bin_bottom_points[i], aligned_edge=DOWN)
            hist_bars.add(rect)
        self.add(hist_bars)

        # 标签
        n_label = Text("n = 1", font_size=28).to_corner(UR)
        self.add(n_label)

        # 控制样本量变化的 ValueTracker
        n_tracker = ValueTracker(0)

        # --------------------------
        # 3. 定义 updater（使用预计算密度、底部点，避免重复 c2p）
        # --------------------------
        def update_histogram(mob, dt):
            t = n_tracker.get_value()
            n_float = n_min + (n_max - n_min) * t
            n_int = int(np.clip(n_float, n_min, n_max))
            n_idx = n_int - n_min

            density = self.hist_densities[n_idx]

            # 更新每个矩形
            for i, rect in enumerate(hist_bars):
                height = density[i]

                if height <= 0:
                    rect.set_height(0.001)
                    rect.set_opacity(0)
                else:
                    rect.set_height(height, stretch=True)
                    rect.set_opacity(0.6)

                # 位置用预计算底部点，不需要每帧计算
                rect.move_to(self.bin_bottom_points[i], aligned_edge=DOWN)

            # 更新标签文本
            n_label.set_text(f"n = {n_int}")
            n_label.to_corner(UR)

        hist_bars.add_updater(update_histogram)

        # --------------------------
        # 4. 启动动画（缩短运行时间，保证总渲染在 30 秒内）
        # --------------------------
        self.play(
            n_tracker.animate.set_value(1),
            run_time=8,            # 从15秒减至8秒
            rate_func=linear,
        )
        self.wait(2)