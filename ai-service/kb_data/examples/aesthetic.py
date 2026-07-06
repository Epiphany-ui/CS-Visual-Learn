from manim import *

class AestheticCircle(Scene):
    def construct(self):
        # 带有填充和边缘的质感圆
        circle = Circle(
            radius=2.0,
            color=BLUE,
            fill_opacity=0.3,
            stroke_width=6
        )
        # 标签
        label = Text("Beautiful Circle", font_size=36)
        label.next_to(circle, UP)

        self.play(Create(circle), Write(label))
        self.wait(2)