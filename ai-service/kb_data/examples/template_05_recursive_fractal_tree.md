---

### 📦 5. 算法可视化：递归分形树 (Algorithms & Fractals)
**文件建议命名：** `template_05_recursive_fractal_tree.md`

```markdown
# 意图：利用递归算法在 Manim 中生成具有数学美感的分形树（Fractal Tree），演示如何通过循环和数学变换批量构建 VGroup 并统一渲染。
# 关键词：算法, 分形树, 递归, 树状图, VGroup, Line, 角度旋转

下面是完整的 Manim 代码示例：
```python
from manim import *

class FractalTree(Scene):
    def construct(self):
        # 1. 声明一个 VGroup 用于存储所有生成的树枝
        tree_group = VGroup()

        # 2. 定义递归生成树枝的算法函数
        def draw_tree(start_point, angle, length, depth):
            if depth == 0:
                return
            
            # 计算当前树枝的终点坐标
            dx = length * np.cos(angle)
            dy = length * np.sin(angle)
            end_point = start_point + np.array([dx, dy, 0])
            
            # 根据深度设置颜色渐变（越接近末端越绿）
            color = interpolate_color(MAROON, GREEN, 1 - depth / 6)
            branch = Line(start_point, end_point, color=color, stroke_width=depth)
            tree_group.add(branch)
            
            # 递归调用：向左偏和向右偏生成子树枝，长度按比例缩小
            draw_tree(end_point, angle + 30 * DEGREES, length * 0.75, depth - 1)
            draw_tree(end_point, angle - 25 * DEGREES, length * 0.75, depth - 1)

        # 3. 触发递归生成，初始树干朝上（90度），深度为 6
        root_point = DOWN * 3
        draw_tree(root_point, 90 * DEGREES, 1.5, 6)

        # 4. 优雅的入场动画：使用 LaggedStart 使数千条线段带有流线感地依次生长出来
        self.play(LaggedStartMap(Create, tree_group, lag_ratio=0.01), run_time=4)
        self.wait(1)