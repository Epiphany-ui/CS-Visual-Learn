from manim import *

class TaylorSeriesAnimation(Scene):
    def construct(self):
        # 定义函数和其泰勒级数展开
        f = lambda x: np.sin(x)
        taylor_series = [lambda x, n=0: 0]
        for i in range(1, 6):
            taylor_series.append(lambda x, n=i: taylor_series[-1](x) + (-1)**i * (x**(2*i+1)) / np.math.factorial(2*i+1))

        # 创建坐标轴
        axes = Axes(
            x_range=[-2*np.pi, 2*np.pi],
            y_range=[-1.5, 1.5],
            axis_config={"color": BLUE},
            tips=False,
        ).scale(0.7).shift(DOWN)

        # 绘制原函数和泰勒级数展开
        graph = axes.plot(f, color=RED)
        taylor_graphs = [axes.plot(taylor_series[i], color=GREEN) for i in range(1, 6)]

        # 创建标签
        f_label = axes.get_graph_label(graph, label="sin(x)")
        taylor_labels = [axes.get_graph_label(taylor_graphs[i], label=f"Taylor Series (n={i})") for i in range(1, 6)]

        # 绘制坐标轴和函数图
        self.play(Create(axes), Create(f_label))
        self.wait(1)

        # 动态逼近泰勒级数
        for i in range(1, 6):
            self.play(Transform(taylor_graphs[i-1], taylor_graphs[i]), Transform(taylor_labels[i-1], taylor_labels[i]))
            self.wait(0.5)

        self.wait(2)