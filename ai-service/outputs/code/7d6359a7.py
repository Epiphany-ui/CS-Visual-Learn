from manim import *

class TaylorSeriesAnimation(Scene):
    def construct(self):
        # 定义函数和其泰勒级数展开
        f = lambda x: np.sin(x)
        taylor_series = [
            lambda x: 0,
            lambda x: x,
            lambda x: x - (x**3) / 6,
            lambda x: x - (x**3) / 6 + (x**5) / 120
        ]

        # 创建坐标轴
        axes = Axes(
            x_range=[-2 * PI, 2 * PI],
            y_range=[-1.5, 1.5],
            axis_config={"color": BLUE},
            tips=False,
        )

        # 绘制原函数和泰勒级数展开
        function_graph = axes.plot(f, color=RED)
        taylor_graphs = [axes.plot(ts, color=GREEN) for ts in taylor_series]

        # 创建标签
        function_label = MathTex(r"f(x) = \sin(x)").next_to(axes, UP)
        taylor_labels = [
            MathTex(r"T_n(x)").next_to(taylor_graphs[i], RIGHT).shift(RIGHT * 0.5)
            for i in range(len(taylor_series))
        ]

        # 绘制坐标轴和标签
        self.play(Create(axes), Write(function_label))
        self.wait(1)

        # 动态展示泰勒级数逼近过程
        for i, taylor_graph in enumerate(taylor_graphs):
            if i > 0:
                self.play(Transform(taylor_graphs[i - 1], taylor_graphs[i]), Transform(taylor_labels[i - 1], taylor_labels[i]))
            else:
                self.play(Create(taylor_graph), Write(taylor_label[i]))

        # 添加尾迹
        dot = Dot().move_to(axes.c2p(0, f(0)))
        dot.add_updater(lambda m, dt: m.move_to(axes.c2p(dt * 2 * PI, f(dt * 2 * PI))))
        self.play(Create(dot))
        self.wait(3)