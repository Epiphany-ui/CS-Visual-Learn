from manim import *

class RedCircle(Scene):
    def construct(self):
        circle = Circle(color=RED)
        self.add(circle)

        # 添加一些文字说明
        text = Text("这是一个红色圆")
        text.next_to(circle, RIGHT, buff=0.5)
        self.add(text)