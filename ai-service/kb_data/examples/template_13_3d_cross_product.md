---

### 📦 13. 三维空间：叉乘与右手定则 (3D Cross Product)
**文件建议命名：** `template_13_3d_cross_product.md`

```markdown
# 意图：在三维坐标系中，给定 XY 平面上的两个向量，通过叉积计算生成一个垂直于这两个向量的新向量，展示右手定则。
# 关键词：叉积, 三维向量, 右手定则, 垂直向量, np.cross, ThreeDAxes, ThreeDScene

下面是完整的 Manim 代码示例：
```python
from manim import *

class CrossProduct3D(ThreeDScene):
    def construct(self):
        # 1. 初始化 3D 坐标轴和视角
        axes = ThreeDAxes()
        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES)
        self.play(Create(axes))

        # 2. 在 XY 平面定义两个向量 v 和 w
        coord_v = np.array([2, 0, 0])
        coord_w = np.array([1, 2, 0])
        
        # np.cross 自动计算三维叉积坐标
        coord_cross = np.cross(coord_v, coord_w)

        vec_v = Arrow3D(ORIGIN, coord_v, color=BLUE)
        vec_w = Arrow3D(ORIGIN, coord_w, color=YELLOW)
        vec_cross = Arrow3D(ORIGIN, coord_cross, color=RED)

        # 3. 添加文字标签 (使用 3D 锚点)
        label_v = MathTex(r"\vec{v}").move_to(coord_v + RIGHT*0.5)
        label_w = MathTex(r"\vec{w}").move_to(coord_w + UP*0.5)
        label_cross = MathTex(r"\vec{v} \times \vec{w}", color=RED).move_to(coord_cross + UP*0.5)
        
        # 固定标签方向使其始终面向摄像机
        self.add_fixed_orientation_mobjects(label_v, label_w, label_cross)

        # 4. 动画展示
        self.play(Create(vec_v), Write(label_v))
        self.play(Create(vec_w), Write(label_w))
        self.wait(1)
        
        # 叉积向量破空而出
        self.play(Create(vec_cross), Write(label_cross))
        
        # 旋转摄像机全方位观察垂直关系
        self.begin_ambient_camera_rotation(rate=0.4)
        self.wait(4)
        self.stop_ambient_camera_rotation()