import numpy as np
from manim import *

class LawOfLargeNumbers(Scene):
    def construct(self):
        # --------------------------
        # 1. 预计算不同样本量下的标准化样本均值（减少样本量以提升性能）
        # --------------------------
        np.random.seed(42)
        sample_counts = 1000                # 从2000减至1000
        n_min, n_max = 1, 100
        n_values = list(range(n_min, n_max + 1))
        self.standardized_means = []
        for n in n_values:
            samples = np.random.binomial(n, 0.5, size=sample_counts) / n
            means_std = (samples - 0.5) * 2 * np.sqrt(n)
            self.standardized_means.append(means_std)

        # 减少直方图 bin 数量（81 → 61），降低更新开销
        self.bin_edges = np.linspace(-4, 4, 61)
        bin_width = self.bin_edges[1] - self.bin_edges[0]

        # 预计算每个 n 对应的直方图密度，避免每帧重复计算
        self.hist_densities = []
        for data in self.standardized_means:
            counts, _ = np.histogram(data, bins=self.bin_edges, density=False)
            density = counts / (sample_counts * bin_width)
            self.hist_densities.append(density)

        # 预计算每个 bin 中心对应的坐标系底部点（x坐标固定，y=0）
        self.bin_bottom_points = []
        for i in range(len(self.bin_edges) - 1):
            center = (self.bin_edges[i] + self.bin_edges[i+1]) / 2
            self.bin_bottom_points.append(center)  # 只保存 x 值，后续用 axes.c2p

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

        # 创建直方图矩形容器（固定数量，后续只更新高度和位置）
        n_bins = len(self.bin_edges) - 1
        hist_bars = VGroup()
        for _ in range(n_bins):
            rect = Rectangle(
                width=0.01, height=0.01,
                color=BLUE, fill_opacity=0.6,
                stroke_width=1,
            )
            rect.set_stroke(GREY, opacity=0.3)
            hist_bars.add(rect)
        self.add(hist_bars)

        # 标签（使用固定 Text 对象，避免每帧创建新对象）
        n_label = Text("n = 1", font_size=28).to_corner(UR)
        self.add(n_label)

        # 控制样本量变化的 ValueTracker
        n_tracker = ValueTracker(0)

        # --------------------------
        # 3. 定义 updater（优化：使用预计算密度、预计算坐标、更新文本而非重建）
        # --------------------------
        def update_histogram(mob, dt):
            t = n_tracker.get_value()
            n_float = n_min + (n_max - n_min) * t
            n_int = int(np.clip(n_float, n_min, n_max))
            n_idx = n_int - n_min

            density = self.hist_densities[n_idx]

            # 更新每个矩形
            for i, rect in enumerate(hist_bars):
                left = self.bin_edges[i]
                right = self.bin_edges[i+1]
                center = (left + right) / 2.0
                height = density[i]

                if height <= 0:
                    rect.set_height(0.001)
                    rect.set_opacity(0)
                else:
                    rect.set_height(height, stretch=True)
                    rect.set_opacity(0.6)

                rect.set_width(bin_width * 0.95, stretch=True)

                # 使用预计算的 x 坐标 + 固定 y=0 底部点
                bottom_point = axes.c2p(center, 0)
                rect.move_to(bottom_point, aligned_edge=DOWN)

            # 更新标签文本（只改变内容，不重建对象）
            n_label.set_text(f"n = {n_int}")
            n_label.to_corner(UR)

        hist_bars.add_updater(update_histogram)

        # --------------------------
        # 4. 启动动画（缩短运行时间，保证总渲染在 30 秒内）
        # --------------------------
        self.play(
            n_tracker.animate.set_value(1),
            run_time=15,           # 从28秒减至15秒
            rate_func=linear,
        )
        self.wait(2)