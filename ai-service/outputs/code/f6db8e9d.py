from manim import *

class CircularMotion(Scene):
    def construct(self):
        circle = Circle(radius=1, color=BLUE).shift(LEFT)
        dot = Dot(color=RED).scale(2)

        # 创建一个更新器函数，使小球在圆周上运动
        def update_dot(mob, dt):
            angle = mob.time * 2 * PI / 5  # 每5秒完成一次完整圆周运动
            x = circle.get_center()[0] + circle.radius * np.cos(angle)
            y = circle.get_center()[1] + circle.radius * np.sin(angle)
            mob.move_to(RIGHT * x + UP * y)

        dot.add_updater(update_dot)  # 将更新器添加到小球上

        self.play(Create(circle), Create(dot))  # 创建圆和小球
        self.wait(5)  # 等待5秒，让小球完成一次完整圆周运动