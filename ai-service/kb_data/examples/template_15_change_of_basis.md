---

### 📦 15. 基底变换的坐标网格相对运动 (Change of Basis)
**文件建议命名：** `template_15_change_of_basis.md`

```markdown
# 意图：展示当我们改变观察视角（基底）时，同一个向量在全局空间（标准基底）和局部空间（新基底）下的坐标表现形式。绘制两套不同颜色的网格叠加。
# 关键词：基底变换, 新基底, 两套网格, NumberPlane, apply_matrix, set_opacity

下面是完整的 Manim 代码示例：
```python
from manim import *

class ChangeOfBasis(Scene):
    def construct(self):
        # 1. 建立标准的全局网格 (浅灰色，不移动)
        standard_plane = NumberPlane(
            axis_config={"color": GRAY},
            background_line_style={"stroke_color": GRAY, "stroke_opacity": 0.3}
        )
        self.add(standard_plane)

        # 2. 建立新基底网格 (青色，将随基底变换)
        new_basis_plane = NumberPlane(
            axis_config={"color": TEAL},
            background_line_style={"stroke_color": TEAL, "stroke_opacity": 0.8}
        )
        
        # 3. 在新基底上定义一个向量 (在新视角下它的坐标是 [1, 1])
        # 但是在屏幕上初始时它和标准基底重合
        vec = Vector([1, 1], color=YELLOW)
        
        # 把向量绑定到新基底网格上
        new_basis_group = VGroup(new_basis_plane, vec)
        
        self.play(Create(new_basis_plane), GrowArrow(vec))
        self.wait(1)

        # 4. 定义新基底在标准基底下的坐标变换矩阵
        # 比如新基底的 i_hat 变成了 [2, 1], j_hat 变成了 [-1, 1]
        transform_matrix = [[2, -1],
                            [1,  1]]

        # 5. 动画：新基底发生扭曲变形，由于向量绑定在新基底上，它会跟着移动到全局的真实位置
        text = Text("对新基底网格施加变换矩阵\n黄色向量的局部坐标仍是(1,1)", font_size=24).to_corner(UL)
        self.play(Write(text))
        
        self.play(
            new_basis_group.animate.apply_matrix(transform_matrix),
            run_time=3
        )
        self.wait(2)