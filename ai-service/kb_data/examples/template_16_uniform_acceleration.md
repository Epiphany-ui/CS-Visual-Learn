# 意图：展示物体在一条直线上进行匀加速运动的过程。利用 rate_func 来控制动画的速率曲线，使其符合物理学的匀加速定律。
# 关键词：匀加速, 直线运动, 物理, 运动学, 加速度, 速度, rate_func, ease_in_quad, NumberLine

下面是完整的 Manim 代码示例：
```python
from manim import *

class UniformAccelerationMotion(Scene):
    def construct(self):
        # 1. 绘制物理轨道 (数轴)
        track = NumberLine(
            x_range=[0, 10, 1], 
            length=10, 
            color=BLUE,
            include_numbers=True
        )
        track.move_to(DOWN)
        self.play(Create(track))

        # 2. 创建运动物体（红色小球）
        ball = Dot(color=RED, radius=0.2)
        # 将小球初始位置设定在坐标轴的 0 刻度处
        ball.move_to(track.n2p(0))
        
        # 创建一个跟随小球的标签
        label = MathTex("v = at", color=YELLOW).next_to(ball, UP)
        
        # 将标签与小球编组，或者使用 updater 使其跟随
        label.add_updater(lambda m: m.next_to(ball, UP))
        
        self.play(FadeIn(ball), Write(label))
        self.wait(0.5)

        # 3. 核心机制：使用 rate_func=rate_functions.ease_in_quad 模拟匀加速运动
        # ease_in_quad 函数的图像是抛物线，意味着位移随时间的平方增长，完美契合匀加速直线运动 x = 1/2 * a * t^2
        self.play(
            ball.animate.move_to(track.n2p(10)),
            run_time=3,
            rate_func=rate_functions.ease_in_quad
        )
        self.wait(1)
        
        # 记得移除 updater 释放资源
        label.clear_updaters()