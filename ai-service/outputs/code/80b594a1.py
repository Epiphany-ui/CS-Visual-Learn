from manim import *

class FourierTransform(Scene):
    def construct(self):
        # 创建一个圆和它的轨迹
        circle = Circle(radius=1, color=BLUE)
        dot = Dot(color=RED).next_to(circle, UP)

        # 创建轨迹路径
        trajectory = TracedPath(dot.get_center, stroke_width=2)

        # 将轨迹添加到点上
        dot.add(trajectory)

        # 旋转圆和点
        self.play(Rotate(circle, angle=TAU, about_point=[0, -1.5, 0]), 
                  Rotate(dot, angle=TAU, about_origin=[0, -1.5, 0]),
                  run_time=3)

        # 创建频谱
        spectrum = VGroup()
        for i in range(8):
            freq_circle = Circle(radius=0.2, color=GREEN).shift(RIGHT * (i + 1) * 0.5)
            self.play(Create(freq_circle), run_time=0.5)

        # 动画结束
        self.wait(2)