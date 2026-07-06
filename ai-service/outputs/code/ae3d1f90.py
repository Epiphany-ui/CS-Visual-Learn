from manim import *

class CircleScene(Scene):
    def construct(self):
        # 创建一个圆：蓝色、半透明填充、半径1.5，并略微向左上方偏移
        circle = Circle(
            color=BLUE,
            fill_opacity=0.5,
            radius=1.5,
        ).shift(LEFT * 0.5 + UP * 0.3)

        # 使用 Create 动画显示圆，时长2秒
        self.play(Create(circle), run_time=2)
        self.wait(1)