import numpy as np
from manim import *

class CLTAnimation(Scene):
    def construct(self):
        np.random.seed(42)

        # 参数
        n_values = [1, 2, 3, 5, 10, 20, 30]
        num_samples = 10000          # 每个 n 的样本个数
        num_bins = 50                # 直方图 bin 数量
        lower, upper = -0.5, 0.5     # 均匀分布范围
        mu = 0.0
        sigma_pop = np.sqrt(1.0/12.0)

        # ---------- 预计算所有 n 对应的样本均值 ----------
        all_means = []
        for n in n_values:
            samples = np.random.uniform(lower, upper, (num_samples, n))
            means = np.mean(samples, axis=1)
            all_means.append(means)

        # 全局数据范围
        global_min = min(np.min(m) for m in all_means)
        global_max = max(np.max(m) for m in all_means)

        # 固定 bin 划分
        bin_edges = np.linspace(global_min, global_max, num_bins+1)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2.0
        bin_width = bin_edges[1] - bin_edges[0]

        # 计算每个 n 的密度直方图（density=True 使得积分=1）
        densities_list = []
        for means in all_means:
            counts, _ = np.histogram(means, bins=bin_edges, density=True)
            densities_list.append(counts)

        # 理论正态曲线的最高点（用于设定 y 轴上限）
        max_theory = max(
            1.0 / (sigma_pop / np.sqrt(n) * np.sqrt(2*np.pi))
            for n in n_values
        )
        y_max = max(np.max(d) for d in densities_list) * 1.2
        y_max = max(y_max, max_theory * 1.2)

        # ---------- 创建坐标轴 ----------
        axes = Axes(
            x_range=[global_min, global_max, (global_max - global_min)/10],
            y_range=[0, y_max, y_max/6],
            x_length=10,
            y_length=6,
            axis_config={"include_numbers": True, "decimal_number_config": {"num_decimal_places": 2}},
        )
        axes_labels = axes.get_axis_labels(
            Text("样本均值"), Text("概率密度")
        )
        title = Text("中心极限定理：样本均值分布渐近正态", font_size=32).to_edge(UP)
        self.play(Write(title), Create(axes), Write(axes_labels))

        # ---------- 创建直方图的矩形条 ----------
        # 计算场景中每个 bin 的宽度
        bar_width = axes.c2p(bin_edges[1], 0)[0] - axes.c2p(bin_edges[0], 0)[0]
        bars = VGroup()
        for center in bin_centers:
            rect = Rectangle(
                width=bar_width,
                height=0,
                fill_opacity=0.7,
                fill_color=BLUE,
                stroke_width=1,
                stroke_color=WHITE,
            )
            rect.move_to(axes.c2p(center, 0), aligned_edge=DOWN)
            bars.add(rect)
        self.add(bars)

        # 显示当前 n 的文本
        n_text = Text(f"n = {n_values[0]}", font_size=28).to_corner(UR)
        self.add(n_text)

        # ---------- 辅助函数 ----------
        def get_bar_height(density_value):
            """将概率密度值映射为场景中的矩形高度"""
            return axes.c2p(0, density_value)[1] - axes.c2p(0, 0)[1]

        def set_histogram(densities, animate=False):
            """批量设置所有矩形的高度，animate 决定是否使用动画，返回动画列表"""
            animations = []
            for bar, dens in zip(bars, densities):
                h = get_bar_height(dens)
                if animate:
                    animations.append(bar.animate.stretch_to_fit_height(h, about_edge=DOWN))
                else:
                    bar.stretch_to_fit_height(h, about_edge=DOWN)
            return animations

        def get_theory_curve(n):
            """返回 n 对应的理论正态分布曲线 VMobject"""
            sigma = sigma_pop / np.sqrt(n)
            x_min, x_max = axes.x_range[:2]
            num_pts = 200
            pts = []
            for i in range(num_pts + 1):
                x = x_min + (x_max - x_min) * i / num_pts
                y = 1.0 / (sigma * np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)
                if np.isfinite(y):
                    pts.append(axes.c2p(x, y))
                else:
                    pts.append(axes.c2p(x, 0))
            curve = VMobject()
            curve.set_points_smoothly(pts)
            curve.set_stroke(YELLOW, width=3)
            return curve

        # ---------- 初始显示第一个 n ----------
        set_histogram(densities_list[0], animate=False)
        curve = get_theory_curve(n_values[0])
        self.add(curve)

        # ---------- 依次展示后续 n ----------
        for i in range(1, len(n_values)):
            n = n_values[i]
            new_dens = densities_list[i]

            # 获取直方图动画列表
            hist_animations = set_histogram(new_dens, animate=True)

            # 更新 n 文本
            new_n_text = Text(f"n = {n}", font_size=28).to_corner(UR)

            # 更新理论曲线
            new_curve = get_theory_curve(n)

            # 同时播放所有动画
            self.play(
                *hist_animations,
                ReplacementTransform(n_text, new_n_text),
                ReplacementTransform(curve, new_curve),
                run_time=1.5
            )
            n_text = new_n_text
            curve = new_curve

            self.wait(0.5)

        self.wait(2)