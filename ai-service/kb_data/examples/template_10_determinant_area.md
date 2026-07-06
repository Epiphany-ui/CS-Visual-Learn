---

### 📦 10. 行列式的几何意义：面积变化 (Determinant as Area)
**文件建议命名：** `template_10_determinant_area.md`

```markdown
# 意图：展示矩阵行列式的本质——它是空间变换后，基向量所围成的单位正方形面积的缩放比例。
# 关键词：行列式, 面积缩放, 基底正方形, 线性变换, Polygon, apply_matrix, MathTex

下面是完整的 Manim 代码示例：
```python
from manim import *

class DeterminantArea(Scene):
    def construct(self):
        plane = NumberPlane()
        
        # 1. 构建初始单位正方形 (由 i_hat 和 j_hat 组成)
        square = Polygon(
            ORIGIN, RIGHT, RIGHT + UP, UP,
            color=YELLOW, fill_color=YELLOW, fill_opacity=0.4
        )
        
        area_text = MathTex("Area = 1").move_to(square.get_center())
        
        group = VGroup(plane, square)

        self.play(Create(plane), FadeIn(square), Write(area_text))
        self.wait(1)

        # 2. 定义变换矩阵，行列式 det = (2*1.5) - (1*0) = 3.0
        matrix = [[2, 1],
                  [0, 1.5]]

        # 3. 应用空间变换
        self.play(FadeOut(area_text))
        self.play(group.animate.apply_matrix(matrix), run_time=3)
        
        # 4. 显示变换后的面积
        new_area_text = MathTex("Area = \\det(A) = 3.0", color=YELLOW)
        # 将文本移动到新平行四边形的中心
        new_area_text.move_to(square.get_center())
        
        self.play(Write(new_area_text))
        self.wait(2)