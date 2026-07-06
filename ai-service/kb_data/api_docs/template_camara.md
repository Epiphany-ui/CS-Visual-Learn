---

### 📦 模板 6：3D 场景与摄像机旋转
如果你的 AI 系统被要求生成 3D 图像，没这个模板模型绝对会写错配置。

```markdown
# 意图：创建三维坐标系，绘制3D曲面，并设置摄像机视角的自动旋转
# 关键词：3D, 三维, 曲面, 视角, 摄像机, ThreeDScene, ThreeDAxes, Surface, set_camera_orientation

下面是完整的 Manim 代码示例：
```python
from manim import *

# 注意：3D 动画必须继承 ThreeDScene 而不是 Scene
class Rotation3DScene(ThreeDScene):
    def construct(self):
        # 1. 设置 3D 坐标系
        axes = ThreeDAxes()

        # 2. 定义 3D 参数曲面 (例如抛物面 z = x^2 + y^2)
        surface = Surface(
            lambda u, v: axes.c2p(u, v, u**2 + v**2),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(16, 16)
        )
        surface.set_style(fill_opacity=0.7, stroke_color=BLUE, stroke_width=0.5)

        # 3. 初始化摄像机视角：设置俯仰角(phi)和方位角(theta)
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        self.play(Create(axes))
        self.play(Create(surface))
        
        # 4. 开始摄像机旋转动画
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(4)
        self.stop_ambient_camera_rotation()