from manim import *

class BasicAnimation(Scene):
    def construct(self):
        circle = Circle(radius=1)
        self.add(circle)
        self.play(Create(circle))