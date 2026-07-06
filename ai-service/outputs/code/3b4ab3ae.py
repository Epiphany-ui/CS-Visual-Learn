from manim import *

class AcceleratingMotion(Scene):
    def construct(self):
        # 创建一个圆
        circle = Circle(radius=1, color=BLUE, fill_opacity=0.5)
        
        # 设置初始位置和速度
        circle.shift(LEFT * 3)
        velocity = 0
        acceleration = RIGHT * 0.1
        
        # 定义更新器函数
        def update_circle(mob, dt):
            nonlocal velocity
            # 匀加速运动公式：v = v0 + a*t
            velocity += acceleration[0] * dt
            # 更新圆的位置
            mob.shift(velocity * dt)
        
        # 将更新器应用到圆上
        circle.add_updater(update_circle)
        
        # 添加圆到场景中并播放动画
        self.add(circle)
        self.wait(10)  # 播放时间为10秒，以展示匀加速运动