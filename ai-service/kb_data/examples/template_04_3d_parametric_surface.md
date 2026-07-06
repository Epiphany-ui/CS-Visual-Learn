---

### 📦 4. 复杂 3D 参数曲面与动态光影视角 (3D Surface & Camera)
**文件建议命名：** `template_04_3d_parametric_surface.md`

```markdown
# 意图：在三维空间中绘制复杂的参数方程曲面（波浪涟漪面），设置自定义灯光角度，并围绕坐标轴进行连续的摄像机环绕旋转动画。
# 关键词：3D, 曲面, 三维坐标系, 摄像机旋转, 参数方程, ThreeDScene, ParametricSurface

下面是完整的 Manim 代码示例：
```python
from manim import *

# 必须继承 ThreeDScene
class Dynamic3DSurface(ThreeDScene):
    def construct(self):
        # 1. 初始化 3D 坐标系
        axes = ThreeDAxes()
        self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES)

        # 2. 定义复杂的参数曲面：z = sin(x^2 + y^2) 产生的涟漪效果
        def ripple_surface_func(u, v):
            r = np.sqrt(u**2 + v**2)
            z = np.sin(r) * 0.5
            return axes.c2p(u, v, z)

        surface = Surface(
            ripple_surface_func,
            u_range=[-4, 4],
            v_range=[-4, 4],
            resolution=(32, 32)
        )
        
        # 设置曲面的材质和颜色
        surface.set_style(fill_opacity=0.8, fill_color=BLUE_D, stroke_color=TEAL, stroke_width=0.2)

        # 3. 渲染出场动画
        self.play(Create(axes))
        self.play(DrawBorderThenFill(surface), run_time=2)

        # 4. 动态视角动画：摄像机围绕 Z 轴自动旋转
        self.begin_ambient_camera_rotation(rate=0.5)
        
        # 旋转的同时，改变俯仰角 phi 形成俯冲效果
        self.move_camera(phi=45 * DEGREES, theta=120 * DEGREES, run_time=3)
        self.wait(2)
        
        self.stop_ambient_camera_rotation()