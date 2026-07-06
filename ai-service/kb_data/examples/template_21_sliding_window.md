---

### 📦 21. 数据结构：数组与滑动窗口算法 (Sliding Window)
**文件建议命名：** `template_21_sliding_window.md`

```markdown
# 意图：可视化经典算法“滑动窗口”。在一个数组上，用一个矩形框框住特定长度的子数组，并将矩形框逐步向右滑动。
# 关键词：算法, 滑动窗口, 数组, SurroundingRectangle, VGroup, 遍历

下面是完整的 Manim 代码示例：
```python
from manim import *

class SlidingWindowAlgorithm(Scene):
    def construct(self):
        # 1. 构建数组元素
        array_data = [4, 2, 8, 3, 1, 5, 9]
        array_group = VGroup()
        
        for num in array_data:
            # 使用正方形和普通文本组合成数组格子
            box = Square(side_length=1.0, color=WHITE)
            text = Text(str(num), font_size=36)
            cell = VGroup(box, text)
            array_group.add(cell)
            
        # 横向排列并居中
        array_group.arrange(RIGHT, buff=0)
        self.play(FadeIn(array_group, shift=UP))
        self.wait(1)

        # 2. 创建滑动窗口（框住前 3 个元素）
        window_size = 3
        window_rect = SurroundingRectangle(
            array_group[0:window_size], 
            color=YELLOW, 
            stroke_width=4, 
            buff=0.1
        )
        
        # 窗口上方的标签
        label = Text("窗口大小 = 3", font_size=24, color=YELLOW)
        label.add_updater(lambda m: m.next_to(window_rect, UP))
        
        self.play(Create(window_rect), Write(label))
        self.wait(1)

        # 3. 动画：向右滑动窗口
        # 遍历剩余的元素索引
        for i in range(1, len(array_data) - window_size + 1):
            # 将矩形平滑移动到新的子数组目标上
            target_rect = SurroundingRectangle(array_group[i:i+window_size], buff=0.1)
            self.play(
                window_rect.animate.move_to(target_rect.get_center()),
                run_time=1
            )
            self.wait(0.5)
            
        label.clear_updaters()