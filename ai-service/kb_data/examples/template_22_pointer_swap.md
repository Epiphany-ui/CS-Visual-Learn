---

### 📦 22. 数据结构：指针交换与数组排序 (Pointer Swap)
**文件建议命名：** `template_22_pointer_swap.md`

```markdown
# 意图：可视化排序算法（如快排或冒泡）中的两个指针互换数组元素的过程。包括指针箭头的移动和两个数值框的三维翻转交换。
# 关键词：数组, 排序, 指针, 交换, Swap, Arrow, CyclicReplace

下面是完整的 Manim 代码示例：
```python
from manim import *

class ArraySwap(Scene):
    def construct(self):
        # 1. 构建数组
        elements = [7, 3, 5, 2]
        cells = VGroup(*[
            VGroup(Square(side_length=1.2), Text(str(val), font_size=40)) 
            for val in elements
        ]).arrange(RIGHT, buff=0.2)
        
        self.play(Create(cells))

        # 2. 定义两个指针（箭头）
        idx_i, idx_j = 0, 3  # 准备交换第 0 个和第 3 个元素
        
        ptr_i = Arrow(DOWN, UP, color=RED).next_to(cells[idx_i], DOWN)
        label_i = Text("i", font_size=24, color=RED).next_to(ptr_i, DOWN)
        
        ptr_j = Arrow(DOWN, UP, color=GREEN).next_to(cells[idx_j], DOWN)
        label_j = Text("j", font_size=24, color=GREEN).next_to(ptr_j, DOWN)

        self.play(GrowArrow(ptr_i), Write(label_i), GrowArrow(ptr_j), Write(label_j))
        self.wait(1)

        # 3. 高亮需要交换的单元格
        self.play(
            cells[idx_i][0].animate.set_color(RED),
            cells[idx_j][0].animate.set_color(GREEN)
        )

        # 4. 执行交换动画
        # CyclicReplace 能够让两个物体沿着弧线轨迹优美地互换位置
        self.play(CyclicReplace(cells[idx_i], cells[idx_j]), path_arc=90*DEGREES, run_time=1.5)
        
        # 在列表中同步更新数据（重要！保持代码逻辑与动画一致）
        cells.submobjects[idx_i], cells.submobjects[idx_j] = cells.submobjects[idx_j], cells.submobjects[idx_i]
        self.wait(2)