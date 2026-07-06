---

#### 📦 28. 高等数学：三角函数与简谐运动单摆 (Oscillation)
**文件建议命名：** `template_28_pendulum_oscillation.md`

```markdown
# 意图：绘制一个单摆模型，利用正弦函数规律动态更新单摆绳子的角度和摆球位置，完美还原阻尼简谐震荡的物理过程。
# 关键词：单摆, 简谐运动, 震荡, 三角函数, Line, always_redraw, ValueTracker

下面是完整的 Manim 代码示例：
```python
from manim import *
import numpy as np

class PendulumOscillation(Scene):
    def construct(self):
        # 1. 设置天花板悬挂点
        pivot = UP * 2.5
        self.add(Dot(pivot, color=WHITE))

        # 2. 创建时间变量追踪器
        time_tracker = ValueTracker(0)

        # 3. 动态重绘单摆组件（绳子 + 摆球）
        # 摆角公式：theta = theta_max * cos(w * t)
        pendulum = always_redraw(lambda: Skinner())
        
        def Skinner():
            t = time_tracker.get_value()
            length = 4.0  # 绳长
            # 简谐震荡公式，带有一点点衰减系数 e^(-0.1t)
            angle = (45 * DEGREES) * np.cos(3 * t) * np.exp(-0.05 * t)
            
            # 计算摆球的真实 X, Y 坐标
            bob_pos = pivot + np.array([
                length * np.sin(angle),
                -length * np.cos(angle),
                0
            ])
            
            # 组装绳子和球
            rod = Line(pivot, bob_pos, color=GRAY, stroke_width=3)
            bob = Dot(bob_pos, radius=0.3, color=RED, fill_opacity=1)
            return VGroup(rod, bob)

        self.add(pendulum)
        self.wait(0.5)

        # 4. 激活时间线，让单摆震荡 8 秒
        self.play(time_tracker.animate.set_value(8), run_time=8, rate_func=linear)
        self.wait(1)