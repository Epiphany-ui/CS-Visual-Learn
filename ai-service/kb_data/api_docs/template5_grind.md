---

### 📦 模板 5：复杂元素的网格排版 (VGroup 进阶)
教会大模型不要硬算坐标（比如 `.shift(UP*2 + RIGHT*3)`），而是用现代化的网格排版。

```markdown
# 意图：生成多个相似物体，并使用组将其按照行列（网格）进行自动整齐排版布局
# 关键词：网格, 排版, 布局, 阵列, VGroup, arrange_in_grid, Dot

下面是完整的 Manim 代码示例：
```python
from manim import *

class GridLayoutExample(Scene):
    def construct(self):
        # 1. 批量创建多个元素（例如 12 个点）放入列表中
        dots = [Dot(radius=0.2, color=color) for color in [RED, BLUE, GREEN, YELLOW] * 3]
        
        # 2. 使用 VGroup 将列表转换为组
        dot_group = VGroup(*dots)
        
        # 3. 自动网格排版：3行4列，设置元素间距
        dot_group.arrange_in_grid(rows=3, cols=4, buff=0.5)
        
        # 居中对齐
        dot_group.move_to(ORIGIN)

        # 4. 延迟动画：让这些点依次出现，而不是瞬间出现
        self.play(LaggedStart(*[FadeIn(dot, shift=UP) for dot in dot_group], lag_ratio=0.1))
        self.wait(1)