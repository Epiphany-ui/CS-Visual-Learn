---

### 📦 20. 优化算法：梯度下降动态可视化 (Gradient Descent)
**文件建议命名：** `template_20_gradient_descent.md`

```markdown
# 意图：展示机器学习中梯度下降算法寻找局部最优解的过程。一个小球在抛物线函数上滑动，并实时显示经过该点的切线（梯度）。
# 关键词：梯度下降, 优化, 抛物线, 导数, 切线, ValueTracker, always_redraw

下面是完整的 Manim 代码示例：
```python
from manim import *

class GradientDescent(Scene):
    def construct(self):
        # 1. 构建损失函数图像（抛物线）
        axes = Axes(x_range=[-4, 4], y_range=[-1, 10], axis_config={"color": WHITE})
        # 损失函数 y = x^2
        loss_func = axes.plot(lambda x: x**2, color=YELLOW)
        
        self.add(axes, loss_func)

        # 2. 初始化自变量 x 的追踪器（相当于权重参数）
        # 初始权重设在 x = 3 处
        x_tracker = ValueTracker(3.0)

        # 3. 动态质点（当前参数位置）
        dot = always_redraw(lambda: Dot(
            axes.c2p(x_tracker.get_value(), x_tracker.get_value()**2),
            color=RED, radius=0.15
        ))

        # 4. 动态切线（表示当前梯度）
        # 导数 f'(x) = 2x
        tangent_line = always_redraw(lambda: axes.get_secant_slope_group(
            x=x_tracker.get_value(),
            graph=loss_func,
            dx=0.01,
            secant_line_length=3,
            secant_line_color=GREEN
        ))

        self.play(FadeIn(dot), Create(tangent_line))
        self.wait(1)

        # 5. 模拟梯度下降过程：让 x 的值平滑地移动到 0（局部极小值）
        # 使用 smooth 速率函数模拟学习率随梯度减小而步长变短的效果
        self.play(x_tracker.animate.set_value(0), run_time=4, rate_func=smooth)
        self.wait(2)