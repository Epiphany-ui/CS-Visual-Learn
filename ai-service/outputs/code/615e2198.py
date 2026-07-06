from manim import *

class UniformAccelerationMotion(Scene):
    def construct(self):
        # 定义初始位置和速度
        initial_position = LEFT * 3
        velocity = RIGHT

        # 创建一个圆作为小球，并设置其颜色和填充
        ball = Circle(radius=0.5, color=BLUE, fill_opacity=1).move_to(initial_position)
        
        # 创建一个坐标系并添加到场景中
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-2, 2, 1],
            axis_config={"color": WHITE},
            tips=False,
        )
        self.add(axes)

        # 将小球添加到场景中
        self.play(Create(ball))
        
        # 定义加速度向量
        acceleration = RIGHT * 0.5
        
        # 使用 add_updater 更新小球的位置
        ball.add_updater(lambda m, dt: m.move_to(m.get_center() + velocity * dt + 0.5 * acceleration * dt**2))
        
        # 等待一段时间，让动画持续
        self.wait(6)
        
        # 停止更新器
        ball.clear_updaters()