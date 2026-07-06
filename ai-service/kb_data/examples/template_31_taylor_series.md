# 意图：展示泰勒级数如何随着阶数的增加，像“蛇”一样逐渐缠绕并完美贴合原函数（如正弦函数）。这是微积分中最直观的逼近动画。
# 关键词：泰勒级数, 微积分, 函数逼近, 多项式, Axes, Transform, 阶数

下面是完整的 Manim 代码示例：
```python
from manim import *
import math

class TaylorSeriesApproximation(Scene):
    def construct(self):
        # 1. 创建坐标轴和目标函数 (sin(x))
        axes = Axes(x_range=[-6, 6, 1], y_range=[-3, 3, 1], axis_config={"color": GRAY})
        sin_graph = axes.plot(lambda x: math.sin(x), color=BLUE, stroke_width=4)
        
        label_sin = Text("目标函数: sin(x)", font_size=24, color=BLUE).to_corner(UL)
        self.play(Create(axes), Create(sin_graph), Write(label_sin))
        self.wait(1)

        # 2. 定义泰勒展开计算公式 (sin(x) 在 x=0 处的展开)
        def get_taylor_polynomial(n_terms):
            def func(x):
                result = 0
                for i in range(n_terms):
                    # 泰勒级数项： (-1)^i * x^(2i+1) / (2i+1)!
                    sign = (-1)**i
                    power = 2 * i + 1
                    result += sign * (x**power) / math.factorial(power)
                return result
            return axes.plot(func, color=YELLOW, stroke_width=4)

        # 3. 初始第一项 (一条直线 y=x)
        current_taylor = get_taylor_polynomial(1)
        label_term = Text("泰勒展开阶数: 1", font_size=24, color=YELLOW).next_to(label_sin, DOWN, aligned_edge=LEFT)
        
        self.play(Create(current_taylor), Write(label_term))
        self.wait(1)

        # 4. 动态增加阶数，演示逐渐逼近
        for terms in [2, 3, 5, 8]:
            new_taylor = get_taylor_polynomial(terms)
            new_label = Text(f"泰勒展开阶数: {2*terms-1}", font_size=24, color=YELLOW).move_to(label_term.get_center())
            
            # 使用 Transform 平滑过渡到更高阶的多项式曲线
            self.play(
                Transform(current_taylor, new_taylor),
                Transform(label_term, new_label),
                run_time=1.5
            )
            self.wait(0.5)