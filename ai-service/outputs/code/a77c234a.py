from manim import *

class CircleAnimation(Scene):
    def construct(self):
        circle = Circle(radius=3, color=BLUE)
        self.play(Create(circle))