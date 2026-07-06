---

### 📦 11. 向量投影与点积几何意义 (Dot Product Projection)
**文件建议命名：** `template_11_dot_product_projection.md`

```markdown
# 意图：动态展示一个向量在另一个向量上的正交投影，并画出垂直辅助线。这是点积的几何核心。
# 关键词：点积, 投影, 垂直辅助线, 正交, project_along_vector, DashedLine, RightAngle

下面是完整的 Manim 代码示例：
```python
from manim import *

class DotProductProjection(Scene):
    def construct(self):
        # 1. 创建底座向量 v 和被投影向量 w
        vec_v = Vector(RIGHT * 4, color=BLUE)
        vec_w = Vector(RIGHT * 2 + UP * 3, color=YELLOW)
        
        label_v = MathTex(r"\vec{v}").next_to(vec_v, DOWN)
        label_w = MathTex(r"\vec{w}").next_to(vec_w, UP)

        self.play(GrowArrow(vec_v), GrowArrow(vec_w), Write(label_v), Write(label_w))

        # 2. 计算 w 在 v 上的投影向量
        # 投影公式: p = (w·v / v·v) * v
        proj_coord = (np.dot(vec_w.get_end(), vec_v.get_end()) / np.dot(vec_v.get_end(), vec_v.get_end())) * vec_v.get_end()
        vec_proj = Vector(proj_coord, color=GREEN)
        
        # 3. 绘制从 w 终点垂直落到 v 上的虚线
        dashed_line = DashedLine(vec_w.get_end(), proj_coord, color=GRAY)
        
        # 4. 绘制直角符号
        right_angle = RightAngle(dashed_line, vec_v, length=0.3, quadrant=(1, -1))

        # 播放投影动画
        self.play(Create(dashed_line))
        self.play(GrowArrow(vec_proj))
        self.play(Create(right_angle))
        
        # 标记投影
        proj_label = MathTex(r"proj_{\vec{v}}(\vec{w})", color=GREEN).next_to(vec_proj, UP*0.1+LEFT*0.5)
        self.play(Write(proj_label))
        self.wait(2)