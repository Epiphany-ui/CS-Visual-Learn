from manim import *

class TaylorExpansion(Scene):
    def construct(self):
        # 定义函数和其泰勒展开式
        f = lambda x: math.exp(x)
        taylor_series = [f(0), f(1)*x, f(2)*(x**2)/math.factorial(2), f(3)*(x**3)/math.factorial(3)]

        # 创建函数图像和泰勒展开式图像
        graph_f = FunctionGraph(f, x_range=[-2, 2], color=BLUE)
        graphs_taylor = [FunctionGraph(lambda x: sum(ts[:i+1].subs(x=x) for i in range(len(ts))), x_range=[-2, 2], color=RED) for ts in taylor_series]

        # 创建标签
        label_f = Text("f(x) = e^x").to_edge(UP)
        labels_taylor = [Text(f"Taylor Series (n={i})").next_to(graphs_taylor[i], DOWN) for i in range(len(graphs_taylor))]

        # 添加到场景
        self.play(Create(graph_f), Write(label_f))
        self.wait(1)

        for i, graph_taylor in enumerate(graphs_taylor):
            self.play(Transform(graph_f, graph_taylor), Transform(label_f, labels_taylor[i]))
            self.wait(0.5)

        self.wait(2)