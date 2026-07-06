from manim import *

class BrownCircle(Scene):
    def construct(self):
        # 创建一个棕色的圆，并设置其颜色、半径和位置
        brown_circle = Circle(color=ORANGE, radius=2)
        brown_circle.shift(LEFT)

        # 播放动画，先创建圆，再淡入
        self.play(Create(brown_circle), FadeIn(brown_circle))