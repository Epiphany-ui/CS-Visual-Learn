from manim import *

class FourierTransform(Scene):
    def construct(self):
        # 设置坐标系
        plane = NumberPlane(x_range=(-2, 4), y_range=(-1.5, 1.5), axis_config={"color": BLUE})
        self.add(plane)

        # 创建傅里叶变换的表达式
        fourier_expr = MathTex(r"e^{ix} = \cos(x) + i\sin(x)")
        fourier_expr.to_edge(UP)
        self.play(Write(fourier_expr))

        # 创建复数点
        complex_points = VGroup()
        for x in np.linspace(-2, 4, 10):
            y = np.cos(x)
            point = Dot([x, y, 0], color=RED).scale(0.5)
            complex_points.add(point)

        # 显示复数点
        self.play(FadeIn(complex_points), run_time=2)

        # 创建傅里叶级数的表达式
        fourier_series = MathTex(r"e^{ix} \approx 1 + x - \frac{x^2}{2} + \frac{x^3}{6} - \cdots")
        fourier_series.next_to(fourier_expr, DOWN)
        self.play(Write(fourier_series), run_time=2)

        # 创建傅里叶级数的近似
        approx = VGroup()
        for n in range(1, 5):
            coeff = (-1)**n / factorial(n)
            x_val = np.linspace(-2, 4, 100)
            y_val = np.cos(x_val) * coeff
            line = Line([x_val[0], y_val[0], 0], [x_val[-1], y_val[-1], 0], color=BLUE).scale(0.5)
            approx.add(line)

        # 显示傅里叶级数的近似
        self.play(FadeIn(approx), run_time=2)

        # 清除屏幕
        self.wait(2)
        self.clear()