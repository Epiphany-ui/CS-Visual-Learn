---

### 📦 14. 线性方程组与克莱姆法则几何意义 (Linear Equations Intersection)
**文件建议命名：** `template_14_linear_equations.md`

```markdown
# 意图：将二元一次方程组转化为直线的交点问题，展示点坐标就是方程解的几何直观表示，并画出交点高亮。
# 关键词：线性方程组, 直线方程, 交点, 几何解, Axes, plot_line, Dot

下面是完整的 Manim 代码示例：
```python
from manim import *

class SystemOfEquations(Scene):
    def construct(self):
        # 1. 构建坐标轴
        axes = Axes(x_range=[-2, 5], y_range=[-2, 5], axis_config={"include_numbers": True})
        self.play(Create(axes))

        # 2. 绘制方程1：2x + y = 4 -> y = -2x + 4
        line1 = axes.plot(lambda x: -2 * x + 4, color=BLUE)
        eq1_label = MathTex("2x + y = 4", color=BLUE).next_to(line1, UP+RIGHT, buff=-2)

        # 3. 绘制方程2：x - y = -1 -> y = x + 1
        line2 = axes.plot(lambda x: x + 1, color=YELLOW)
        eq2_label = MathTex("x - y = -1", color=YELLOW).next_to(line2, DOWN+RIGHT, buff=-2)

        self.play(Create(line1), Write(eq1_label))
        self.play(Create(line2), Write(eq2_label))

        # 4. 求解交点（代数计算交点坐标 x=1, y=2）
        intersection_x, intersection_y = 1, 2
        intersect_dot = Dot(axes.c2p(intersection_x, intersection_y), color=RED, radius=0.1)
        
        # 绘制交点坐标文字和虚线辅助线
        coords = MathTex("(1, 2)", color=RED).next_to(intersect_dot, UP+RIGHT)
        h_line = axes.get_horizontal_line(intersect_dot.get_center(), color=GRAY, line_func=DashedLine)
        v_line = axes.get_vertical_line(intersect_dot.get_center(), color=GRAY, line_func=DashedLine)

        # 5. 高亮交点表示唯一解
        self.play(FadeIn(intersect_dot, scale=0.5))
        self.play(Create(h_line), Create(v_line), Write(coords))
        self.wait(2)