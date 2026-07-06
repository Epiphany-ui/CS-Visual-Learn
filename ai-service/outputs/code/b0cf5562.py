from manim import *

class CircleExample(Scene):
    def construct(self):
        # 创建一个蓝色的圆
        circle = Circle(color=BLUE)
        
        # 添加圆到场景中
        self.play(Create(circle))