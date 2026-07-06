from manim import *
import numpy as np
import math

def taylor_sin(x, order):
    """计算 sin(x) 在 x=0 处的泰勒展开，最高阶为 order（仅奇数阶）"""
    result = 0.0
    for n in range(1, order + 1, 2):
        sign = 1 if ((n - 1) // 2) % 2 == 0 else -1
        result += sign * (x ** n) / math.factorial(n)
    return result

class TaylorVisualization(Scene):
    def construct(self):
        # 标题
        title = Tex("Taylor Expansion of $\\sin(x)$", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # 创建坐标轴
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-2, 2, 0.5],
            x_length=8,
            y_length=4,
            axis_config={"color": GREY}
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")
        self.play(Create(axes), Write(axes_labels))
        self.wait(0.5)

        # 绘制 sin(x) 曲线
        sin_curve = axes.plot(lambda x: np.sin(x), color=BLUE, stroke_width=2)
        sin_label = MathTex("\\sin(x)", color=BLUE).next_to(sin_curve, UP, buff=0.1)
        self.play(Create(sin_curve), Write(sin_label))
        self.wait(0.5)

        # 准备各阶泰勒曲线和标签
        orders = [1, 3, 5, 7]
        colors = [YELLOW, ORANGE, RED, PURPLE]
        curves = []
        labels = []

        for i, order in enumerate(orders):
            # 使用默认参数捕获循环变量，避免闭包问题
            curve = axes.plot(
                lambda x, o=order: taylor_sin(x, o),
                color=colors[i],
                stroke_width=2,
                stroke_opacity=0.8
            )
            label = MathTex(
                f"T_{{{order}}}(x)",
                color=colors[i]
            ).next_to(curve, UP if i % 2 == 0 else DOWN, buff=0.2)
            curves.append(curve)
            labels.append(label)

        # 依次展示每条泰勒曲线和标签（使用 LaggedStart 避免循环内多次 self.play）
        all_animations = []
        for curve, label in zip(curves, labels):
            all_animations.append(Create(curve))
            all_animations.append(Write(label))
        self.play(LaggedStart(*all_animations, lag_ratio=0.6))
        self.wait(1)