# 意图：展示物体（如等边三角形）绕着中心点做标准的圆周运动，利用 ValueTracker 优雅控制极坐标参数，规避 Updater 内部的 animate 冲突。
# 关键词：圆周运动, 旋转, 极坐标, ValueTracker, always_redraw, Triangle, np.cos, np.sin

下面是完整的 Manim 代码示例：
```python
from manim import *
import numpy as np

class CircularMotionTracker(Scene):
    def construct(self):
        # 1. 绘制辅助圆形轨道
        orbit = Circle(radius=2.5, color=GRAY, stroke_width=2).set_opacity(0.4)
        self.add(orbit)

        # 2. 创建角度追踪器（弧度制，从 0 开始）
        angle_tracker = ValueTracker(0)

        # 3. 使用 always_redraw 让三角形的中心坐标紧紧绑定极坐标方程
        # x = r * cos(theta), y = r * sin(theta)
        triangle = always_redraw(lambda: Triangle(
            color=BLUE, fill_opacity=0.6
        ).scale(0.5).move_to(
            np.array([
                2.5 * np.cos(angle_tracker.get_value()),
                2.5 * np.sin(angle_tracker.get_value()),
                0
            ])
        ))

        self.add(triangle)

        # 4. 动画：让角度追踪器在 5 秒内平滑增加到 2 个 TAU（转两圈）
        # 如果需要匀加速圆周运动，只需要把 rate_func 改为 ease_in_quad 即可！
        self.play(
            angle_tracker.animate.set_value(2 * TAU),
            run_time=5,
            rate_func=linear
        )
        self.wait(1)