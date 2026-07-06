from manim import *

class FourierTransform(Scene):
    def construct(self):
        # 创建坐标轴
        axes = Axes(
            x_range=[0, 2*PI],
            y_range=[-1.5, 1.5],
            axis_config={"color": BLUE},
            tips=False,
        ).shift(DOWN)

        # 创建函数图像
        function = FunctionGraph(lambda x: np.sin(x), color=BLUE)
        self.play(Create(axes), Create(function))
        self.wait()

        # 创建傅里叶级数的近似
        def fourier_series(x, n_terms):
            return sum(np.sin((2*k + 1) * x / (2 * n_terms)) for k in range(n_terms))

        # 动画展示傅里叶级数的近似
        fourier_approx = FunctionGraph(lambda x: fourier_series(x, 1), color=RED)
        self.play(Create(fourier_approx))
        self.wait()

        for i in range(2, 10):
            new_approx = FunctionGraph(lambda x: fourier_series(x, i), color=RED)
            self.play(Transform(fourier_approx, new_approx))
            self.wait(0.5)

        self.wait(2)