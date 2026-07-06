from manim import *

class MomentumConservation(Scene):
    def construct(self):
        # 创建场景元素
        ball1 = Circle(radius=0.5, color=BLUE, fill_opacity=0.8).shift(LEFT * 2)
        ball2 = Circle(radius=0.5, color=RED, fill_opacity=0.8).shift(RIGHT * 2)

        # 将球组合在一起
        balls = VGroup(ball1, ball2)

        # 动画：球从两侧移动并向中间碰撞
        self.play(MoveToTarget(ball1), MoveToTarget(ball2))
        self.wait(1)
        self.play(ball1.animate.shift(RIGHT * 4).set_color(GREEN), 
                  ball2.animate.shift(LEFT * 4).set_color(YELLOW))
        self.wait(1)

        # 动画：球反弹
        self.play(ball1.animate.shift(LEFT * 8).set_color(BLUE), 
                  ball2.animate.shift(RIGHT * 8).set_color(RED))
        self.wait(1)