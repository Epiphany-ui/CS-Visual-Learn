---

### 📦 34. 拓扑学：三维莫比乌斯环参数曲面 (Möbius Strip)
**文件建议命名：** `template_34_mobius_strip.md`

```markdown
# 意图：利用三维参数方程绘制拓扑学中最著名的“莫比乌斯环”（单面几何体），并启动摄像机环绕其进行多角度渲染。
# 关键词：拓扑, 莫比乌斯环, 3D曲面, 参数方程, ThreeDScene, Surface, camera

下面是完整的 Manim 代码示例：
```python
from manim import *
import numpy as np

# 必须继承 ThreeDScene 才能渲染 3D
class MobiusStrip(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(x_range=[-3,3], y_range=[-3,3], z_range=[-2,2])
        self.set_camera_orientation(phi=65 * DEGREES, theta=30 * DEGREES)
        self.play(Create(axes))

        # 1. 莫比乌斯环的核心参数方程
        def mobius_func(u, v):
            # u 控制环绕主圆的圈数 (0 到 2PI)
            # v 控制纸带的宽度 (-1 到 1)
            x = (2 + v * np.cos(u / 2)) * np.cos(u)
            y = (2 + v * np.cos(u / 2)) * np.sin(u)
            z = v * np.sin(u / 2)
            return np.array([x, y, z])

        # 2. 生成 Surface 3D 曲面
        mobius_surface = Surface(
            mobius_func,
            u_range=[0, TAU],
            v_range=[-0.8, 0.8],
            resolution=(64, 16) # 网格精细度
        )
        
        # 涂上双色材质以便观察翻转
        mobius_surface.set_style(fill_opacity=0.8, stroke_width=0.5, stroke_color=WHITE)
        mobius_surface.set_fill_by_checkerboard(ORANGE, BLUE)

        # 3. 渲染出场
        self.play(Create(mobius_surface), run_time=3)

        # 4. 摄像机自动环绕，展示其“单面”的拓扑奇观
        self.begin_ambient_camera_rotation(rate=0.4)
        
        # 顺便给摄像机俯仰角来个动态变化
        self.move_camera(phi=45 * DEGREES, run_time=4)
        self.wait(1)
        
        self.stop_ambient_camera_rotation()