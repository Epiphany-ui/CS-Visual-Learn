from manim import *
import math
import numpy as np

class TaylorApproximation(Scene):
    def construct(self):
        # 建立坐标轴，强制关闭数字标签以避免 LaTeX
        axes = Axes(
            x_range=[-PI - 0.5, PI + 0.5, 1],
            y_range=[-2, 2, 0.5],
            x_length=10,
            y_length=5,
            axis_config={"color": WHITE, "include_numbers": False}
        )
        # 不创建轴标签（get_axis_labels 会生成 MathTex）

        # 绘制 sin(x) 曲线（蓝色）
        sin_curve = axes.plot(
            lambda x: np.sin(x),
            color=BLUE,
            x_range=[-PI, PI],
            stroke_width=3
        )

        # 计算泰勒系数（sin 在 0 处展开）
        max_order = 15
        coeffs = []
        for k in range(max_order + 1):
            coeffs.append(((-1)**k) / math.factorial(2 * k + 1))

        # 生成 0 到 max_order 阶的泰勒多项式曲线（黄色，半透明）
        poly_curves = []
        for n in range(max_order + 1):
            # 闭包捕获当前 n，保证每条曲线对应正确的阶数
            def poly_func(x, n=n):
                total = 0.0
                for k in range(n + 1):
                    total += coeffs[k] * x**(2 * k + 1)
                return total
            curve = axes.plot(
                poly_func,
                color=YELLOW,
                x_range=[-PI, PI],
                stroke_width=2,
                stroke_opacity=0.8
            )
            poly_curves.append(curve)

        # 阶数追踪器和实时标签（使用 Text 替代 MathTex）
        n_tracker = ValueTracker(0)
        n_label = always_redraw(
            lambda: Text(f"n = {int(n_tracker.get_value())}").to_corner(UR)
        )

        # 先添加坐标轴、sin 曲线和初始标签
        self.play(Create(axes))
        self.wait(0.3)
        self.play(Create(sin_curve), run_time=1.5)
        self.wait(0.3)
        self.add(n_label)
        self.wait(0.2)

        # 构建动画组：每个组同时创建一条多项式曲线和更新追踪器
        anim_groups = []
        for i in range(max_order + 1):
            group = AnimationGroup(
                Create(poly_curves[i], run_time=0.8),
                n_tracker.animate.set_value(i),
                run_time=0.8
            )
            anim_groups.append(group)

        # 使用 LaggedStart 按顺序播放每个动画组，实现阶数递增效果
        self.play(
            LaggedStart(*anim_groups, lag_ratio=0.4),
            run_time=len(anim_groups) * 0.8 + 0.4 * (len(anim_groups) - 1)
        )
        self.wait(2)