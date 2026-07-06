# 意图：绘制基本几何图形（圆和正方形），并展示平滑的形状变形变换过程
# 关键词：几何, 形状, 变换, 排版, Circle, Square, Transform, Create, next_to

下面是完整的 Manim 代码示例：
```python
from manim import *

class ShapeTransformation(Scene):
    def construct(self):
        # 1. 规范设置：明确颜色和透明度，建立高质感图形
        circle = Circle(radius=1.5, color=BLUE, fill_opacity=0.5)
        square = Square(side_length=3, color=GREEN, fill_opacity=0.5)

        # 将正方形放在圆形的右侧，设置间距
        square.next_to(circle, RIGHT, buff=1.0)

        # 组合起来居中
        group = VGroup(circle, square).move_to(ORIGIN)

        # 2. 动画展示：先同时画出轮廓
        self.play(
            Create(circle),
            Create(square),
            run_time=2
        )
        self.wait(0.5)

        # 3. 形变动画：将圆形平滑变换为正方形（注意此时不能再用Create）
        self.play(Transform(circle, square), run_time=1.5)
        self.wait(1)