from manim import *

class TaylorExpansionAnimation(Scene):
    def construct(self):
        # 定义函数及其泰勒展开式
        f = lambda x: np.exp(x)
        taylor_expansion = lambda x, n_terms: sum([x**i / sp.factorial(i) for i in range(n_terms)])

        # 创建坐标轴
        ax = Axes(
            x_range=[-2, 2, 1],
            y_range=[0, 5, 1],
            axis_config={"include_numbers": True}
        ).shift(DOWN * 0.5)

        # 绘制原始函数和泰勒展开近似
        f_graph = ax.plot(f)
        taylor_graph = ax.plot(lambda x: taylor_expansion(x, 10))

        # 创建标签
        f_label = MathTex(r"f(x) = e^x").next_to(f_graph, UP, buff=0.2)
        taylor_label = MathTex(r"T_{10}(x)").next_to(taylor_graph, UP, buff=0.2)

        # 绘制点和箭头
        points = VGroup(*[Dot(ax.c2p(i, f(i)), color=RED) for i in np.linspace(-2, 2, 5)])
        arrows = VGroup()
        for point in points:
            arrow = Arrow(start=point.get_center(), end=ax.p2c((point.get_center()[0], taylor_expansion(point.get_center()[0], 10))), color=BLUE)
            arrows.add(arrow)

        # 动画
        self.play(Create(ax), Write(f_label))
        self.wait(1)
        self.play(Create(f_graph))
        self.wait(1)
        self.play(FadeIn(points))
        for arrow in arrows:
            self.play(Create(arrow))
        self.wait(1)
        self.play(Create(taylor_graph), Write(taylor_label))
        self.wait(2)