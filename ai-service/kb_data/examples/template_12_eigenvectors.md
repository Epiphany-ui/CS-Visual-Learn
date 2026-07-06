
---

### 📦 12. 特征值与特征向量的本质 (Eigenvectors & Span)
**文件建议命名：** `template_12_eigenvectors.md`

```markdown
# 意图：展示在矩阵变换下，普通向量会偏离原来的方向（跨度），而特征向量始终保持在其原有的直线上，仅仅发生了缩放（特征值）。
# 关键词：特征值, 特征向量, 跨度线, 不变直线, Line, apply_matrix, 变换

下面是完整的 Manim 代码示例：
```python
from manim import *

class EigenvectorVisualization(Scene):
    def construct(self):
        plane = NumberPlane()
        
        # 1. 定义特征向量及其跨度所在的直线
        eigen_vec = Vector([2, 1], color=YELLOW)
        # 绘制一根贯穿全屏的直线表示张成的空间(Span)
        span_line = Line(start=[-6, -3, 0], end=[6, 3, 0], color=YELLOW_A, stroke_width=2)
        
        # 2. 定义一个普通向量作为对比
        normal_vec = Vector([-1, 1], color=RED)
        
        self.add(plane, span_line, eigen_vec, normal_vec)

        # 3. 定义具有特征向量 [2, 1] 的变换矩阵
        # 该矩阵使 [2, 1] 放大 2 倍 (特征值为 2)
        matrix = [[1.5, 1],
                  [0.5, 1]]

        # 4. 连同整个空间一起变换
        group = VGroup(plane, span_line, eigen_vec, normal_vec)
        
        text = Text("特征向量始终保持在黄色跨度线上\n普通红色向量被偏转", font_size=24)
        text.to_corner(UL).add_background_rectangle()
        
        self.play(Write(text))
        self.play(group.animate.apply_matrix(matrix), run_time=4)
        self.wait(2)