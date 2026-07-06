from manim import *

class CircleMotion(Scene):
    def construct(self):
        circle = Circle(radius=1, color=BLUE).shift(LEFT)
        dot = Dot(color=RED).scale(2)

        # 创建一个更新器函数，用于移动小圆点
        def move_dot(mob, dt):
            angle = mob.time * 2 * PI
            mob.move_to(circle.point_from_proportion(angle))

        # 将更新器添加到小圆点上，并设置初始时间
        dot.add_updater(move_dot)
        dot.time = 0

        self.play(Create(circle), Create(dot))
        self.wait(5)  # 等待5秒，让动画持续