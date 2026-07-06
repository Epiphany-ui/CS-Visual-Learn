---

#### 📦 30. 傅里叶级数基础：圆周本轮与均轮变换 (Epicycle)
**文件建议命名：** `template_30_fourier_epicycle.md`

```markdown
# 意图：展示傅里叶变换的几何核心——大圆套小圆（旋转圆叠加）。大圆在旋转的同时，小圆的中心挂在大圆的边缘上也在旋转。
# 关键词：傅里叶级数, 周转圆, 向量叠加, 复合旋转, always_redraw, Circle, Line

下面是完整的 Manim 代码示例：
```python
from manim import *
import numpy as np

class FourierEpicycle(Scene):
    def construct(self):
        # 1. 建立时间变量
        time_tracker = ValueTracker(0)

        # 2. 动态构建双层嵌套旋转圆系统
        system = always_redraw(lambda: create_epicycles(time_tracker.get_value()))
        
        def create_epicycles(t):
            # 第一层：大圆（半径 2，速度慢）
            r1 = 2.0
            omega1 = 1.0
            center1 = ORIGIN
            circle1 = Circle(radius=r1, color=BLUE).move_to(center1).set_opacity(0.3)
            pointer1 = Line(center1, center1 + np.array([r1*np.cos(omega1*t), r1*np.sin(omega1*t), 0]), color=BLUE)

            # 第二层：小圆（半径 0.8，挂在大圆指针的末端，速度快）
            center2 = pointer1.get_end()
            r2 = 0.8
            omega2 = 4.0  # 4倍频自转
            circle2 = Circle(radius=r2, color=YELLOW).move_to(center2).set_opacity(0.5)
            pointer2 = Line(center2, center2 + np.array([r2*np.cos(omega2*t), r2*np.sin(omega2*t), 0]), color=YELLOW)

            # 最终的绘图质点
            tip_dot = Dot(pointer2.get_end(), color=RED, radius=0.1)

            return VGroup(circle1, pointer1, circle2, pointer2, tip_dot)

        # 3. 追踪最终红点的运动轨迹
        # 注意：由于我们要追踪嵌套组内部的特定位置，可以通过动态函数实时捕获末端坐标
        trace = TracedPath(lambda: system[-1].get_center(), stroke_color=RED, stroke_width=3)

        self.add(system, trace)
        
        # 4. 转动 2 个完整的周期
        self.play(time_tracker.animate.set_value(2 * PI), run_time=6, rate_func=linear)
        self.wait(1)