from manim import *

class TaylorExpansionAnimation(Scene):
    def construct(self):
        # 定义函数和其泰勒展开近似
        function = MathTex(r"f(x) = e^x")
        taylor_approximation = MathTex(r"e^x \approx 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!}")
        
        # 创建函数和近似值的组合
        function_group = VGroup(function, taylor_approximation).arrange(DOWN)
        
        # 显示函数和近似值
        self.play(Write(function_group))
        self.wait(2)
        
        # 定义泰勒展开的每一项
        terms = [
            MathTex(r"1"),
            MathTex(r"x"),
            MathTex(r"\frac{x^2}{2!}"),
            MathTex(r"\frac{x^3}{3!}")
        ]
        
        # 创建一个点来表示x的值
        x_point = Dot().shift(RIGHT * 2)
        
        # 定义泰勒展开近似曲线
        taylor_curve = FunctionGraph(lambda x: np.exp(x), x_min=-1, x_max=3)
        
        # 显示泰勒展开近似曲线
        self.play(Create(taylor_curve))
        self.wait(1)
        
        # 动态逼近每一项
        for term in terms:
            taylor_approximation += term
            self.play(Transform(taylor_approximation[-1], term), run_time=0.5)
            self.wait(0.5)
            
        # 显示最终的泰勒展开近似
        self.wait(2)
        
        # 添加尾迹效果
        trace = TracedPath(x_point.get_center, stroke_width=3, color=BLUE)
        x_point.add_updater(lambda m, dt: m.shift(RIGHT * 0.1 * dt))
        self.play(Create(trace), run_time=5)