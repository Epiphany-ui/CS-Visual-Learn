---

### 📦 32. 复变函数：欧拉公式与复平面螺旋 (Euler's Formula)
**文件建议命名：** `template_32_euler_formula.md`

```markdown
# 意图：在复平面中可视化最美数学公式 Euler's formula。展示实数轴上的线性时间 $t$ 如何通过 $e^{it}$ 映射为复平面上的完美单位圆轨迹。
# 关键词：复平面, 欧拉公式, 虚数, 螺旋, 极坐标, ComplexPlane, np.exp, TracedPath

下面是完整的 Manim 代码示例：
```python
from manim import *
import numpy as np

class EulerFormulaPlane(Scene):
    def construct(self):
        # 1. 创建复平面 (带实轴和虚轴)
        plane = ComplexPlane(
            x_range=[-3, 3, 1], 
            y_range=[-3, 3, 1],
            background_line_style={"stroke_opacity": 0.5}
        )
        self.play(Create(plane))

        # 添加坐标轴纯文本说明
        real_label = Text("实轴 (Real)", font_size=24).next_to(plane.c2p(3, 0), DOWN)
        imag_label = Text("虚轴 (Imaginary)", font_size=24).next_to(plane.c2p(0, 3), LEFT)
        self.play(Write(real_label), Write(imag_label))

        # 2. 创建追踪器代表时间 t
        t_tracker = ValueTracker(0)

        # 3. 定义复数质点，计算欧拉公式 e^(i*t)
        euler_dot = always_redraw(lambda: Dot(
            # np.exp(1j * t) 是核心数学魔法
            plane.n2p(np.exp(1j * t_tracker.get_value())), 
            color=YELLOW, 
            radius=0.1
        ))

        # 4. 挂载拖尾，绘制单位圆
        trail = TracedPath(euler_dot.get_center, stroke_color=YELLOW, stroke_width=4)
        
        # 动态文本显示当前的 t 值
        t_label = always_redraw(lambda: Text(
            f"t = {t_tracker.get_value():.2f} 弧度", 
            font_size=28, color=YELLOW
        ).to_corner(UR))

        self.add(trail, euler_dot, t_label)

        # 5. 动画：让 t 从 0 跑到 2*PI (即一整圈)
        self.play(t_tracker.animate.set_value(2 * PI), run_time=5, rate_func=linear)
        self.wait(1)