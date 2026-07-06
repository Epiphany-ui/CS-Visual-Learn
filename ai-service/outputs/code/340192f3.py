from manim import *

class UniformAccelerationMotion(Scene):
    def construct(self):
        # 创建坐标轴
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-2, 8, 1],
            axis_config={"color": BLUE},
        )
        axes.shift(LEFT * 3)

        # 添加坐标轴到场景
        self.add(axes)

        # 创建运动点和轨迹
        point = Dot()
        trajectory = VGroup()

        # 定义匀加速直线运动的参数
        initial_position = axes.c2p(0, 1)
        initial_velocity = RIGHT * 1.5
        acceleration = DOWN * 0.5

        # 更新点的位置
        def update_point(mob):
            mob.shift(initial_velocity * dt + 0.5 * acceleration * dt**2)

        point.add_updater(update_point)

        # 将点添加到轨迹中
        trajectory.add(point)

        # 播放动画
        self.play(Create(trajectory), run_time=8)
        self.wait(1)