from manim import *

class FreeFallingObject(Scene):
    def construct(self):
        # 创建地球和小球
        earth = Rectangle(width=10, height=2, color=YELLOW).shift(DOWN * 5)
        ball = Circle(radius=0.5, color=BLUE).shift(UP * 10)

        # 将地球和小球组合到一个 VGroup 中
        scene_objects = VGroup(earth, ball)

        # 小球的初始速度
        v = 0
        # 重力加速度
        g = 9.8

        # 定义小球的位置更新器
        def update_ball(ball, dt):
            nonlocal v
            # 更新小球的速度
            v += g * dt
            # 更新小球的位置
            ball.shift(DOWN * v * dt)

        # 将更新器添加到小球上
        ball.add_updater(update_ball)

        # 将地球和小球添加到场景中
        self.add(scene_objects)

        # 等待一段时间以显示动画
        self.wait(3)