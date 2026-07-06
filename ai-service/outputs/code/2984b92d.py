from manim import *

class UniformAccelerationMotion(Scene):
    def construct(self):
        # 定义物体和初始状态
        ball = Sphere(radius=0.5, color=BLUE)
        ball.shift(LEFT * 3)

        # 初始速度和加速度
        initial_velocity = RIGHT * 1
        acceleration = RIGHT * 0.2

        # 时间步长
        dt = 0.1

        # 动画总时长
        total_time = 5

        for t in np.arange(0, total_time, dt):
            # 计算当前速度
            current_velocity = initial_velocity + acceleration * t
            # 更新物体位置
            ball.animate.shift(current_velocity * dt)
            # 播放动画
            self.play(ball.animate)

        # 保持画面最后一秒
        self.wait(1)