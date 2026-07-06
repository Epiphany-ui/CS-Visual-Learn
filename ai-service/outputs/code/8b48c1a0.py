from manim import *

class CircleAnimation(Scene):
    def construct(self):
        # 创建一个棕色的圆，半径为2，位置在原点
        circle = Circle(radius=2, color=YELLOW_B)

        # 使用self.play动画播放创建圆的动作
        self.play(Create(circle))