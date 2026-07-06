# 意图：展示二维平面如何被一个 2x2 矩阵进行线性变换（如剪切、缩放、旋转），并观察网格线和基向量的动态扭曲过程。
# 关键词：线性代数, 矩阵变换, 空间扭曲, 基向量, NumberPlane, apply_matrix, Vector

下面是完整的 Manim 代码示例：
```python
from manim import *

class MatrixTransformation(Scene):
    def construct(self):
        # 1. 创建带有背景色的数字网格平面
        plane = NumberPlane(
            background_line_style={"stroke_opacity": 0.5}
        )
        
        # 2. 创建基向量 i_hat (绿色) 和 j_hat (红色)
        i_hat = Vector([1, 0], color=GREEN)
        j_hat = Vector([0, 1], color=RED)
        
        # 添加标签
        i_label = MathTex(r"\hat{i}", color=GREEN).next_to(i_hat.get_end(), DOWN)
        j_label = MathTex(r"\hat{j}", color=RED).next_to(j_hat.get_end(), LEFT)
        
        # 编组以便后续一起变换
        moving_mobjects = VGroup(plane, i_hat, j_hat, i_label, j_label)

        self.play(Create(plane), GrowArrow(i_hat), GrowArrow(j_hat), Write(i_label), Write(j_label))
        self.wait(1)

        # 3. 定义 2x2 变换矩阵 (这里是一个剪切变换)
        matrix = [[1, 1], 
                  [0, 1]]
        
        # 4. 核心：使用 apply_matrix 将整个空间平滑扭曲
        self.play(
            moving_mobjects.animate.apply_matrix(matrix),
            run_time=3,
            rate_func=smooth
        )
        self.wait(2)