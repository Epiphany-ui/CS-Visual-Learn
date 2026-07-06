from manim import *

class CircleExample(Scene):
    def construct(self):
        # 创建一个棕色的圆，颜色为棕色，填充透明度为0.5，半径为2，位置在原点
        brown_circle = Circle(radius=2, color=PURPLE_B, fill_opacity=0.5)
        
        # 平滑地将圆从当前位置移动到新位置（位于原点）
        self.play(Create(brown_circle), run_time=2)