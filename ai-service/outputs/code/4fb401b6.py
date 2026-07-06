from manim import *

class ParabolicMotion(Scene):
    def construct(self):
        # 设置场景背景
        self.background = Rectangle(width=10, height=6, color=WHITE)
        self.add(self.background)

        # 创建小球
        ball = Circle(radius=0.5, color=BLUE, fill_color=BLUE, fill_opacity=0.7)
        ball.shift(LEFT * 3 + DOWN * 2)

        # 设置重力加速度
        g = 9.81

        # 定义小球的位置更新器
        def update_ball(ball, dt):
            ball.velocity_y -= g * dt
            ball.shift(RIGHT * ball.velocity_x * dt + UP * ball.velocity_y * dt)
            ball.time += dt

        # 设置初始速度
        ball.velocity_x = 5
        ball.velocity_y = 10
        ball.time = 0

        # 应用位置更新器
        ball.add_updater(update_ball)

        # 播放动画，持续时间为2秒
        self.play(self.background.animate.set_fill(color=GRAY, opacity=0.3), run_time=2)
        self.wait(1)  # 等待初始状态
        self.play(run_time=4)  # 让小球运动一段时间

        # 去除更新器，停止动画
        ball.remove_updater(update_ball)

        # 播放最后的静态小球
        self.play(FadeOut(self.background), Transform(ball, ball))