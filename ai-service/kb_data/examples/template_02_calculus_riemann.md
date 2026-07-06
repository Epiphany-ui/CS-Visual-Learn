---

### 📦 2. 高阶微积分：黎曼和逼近积分 (Advanced Calculus)
**文件建议命名：** `template_02_calculus_riemann.md`

```markdown
# 意图：绘制坐标系及复杂函数曲线，动态展示黎曼和矩形数量(dx)逐渐变小，最终平滑演变为函数积分面积的过程。
# 关键词：微积分, 黎曼和, 积分, 面积, 极限, Axes, get_riemann_rectangles, Transform, 动态更新

下面是完整的 Manim 代码示例：
```python
from manim import *

class RiemannSumToIntegral(Scene):
    def construct(self):
        # 1. 初始化坐标系与函数
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 5, 1],
            axis_config={"include_numbers": True}
        )
        # 函数表达式：f(x) = 0.1 * x^2 + 1
        func = axes.plot(lambda x: 0.1 * x**2 + 1, color=YELLOW)
        
        # 2. 创建初始的黎曼矩形（dx 较大，矩形较少）
        initial_dx = 1.0
        rects = axes.get_riemann_rectangles(
            func, x_range=[2, 8], dx=initial_dx, color=BLUE, fill_opacity=0.5
        )
        
        self.play(Create(axes), Create(func))
        self.play(Write(rects))
        self.wait(1)

        # 3. 动态展示 dx 逼近于 0 的极限过程
        # 定义我们需要展示的几个 dx 阶段
        dx_values = [0.5, 0.25, 0.1, 0.05]
        
        for dx in dx_values:
            new_rects = axes.get_riemann_rectangles(
                func, x_range=[2, 8], dx=dx, color=BLUE, fill_opacity=0.5
            )
            # 使用 Transform 实现矩形的平滑分裂与演变
            self.play(Transform(rects, new_rects), run_time=1)
        
        # 4. 最终演变为真正的积分平滑面积
        integral_area = axes.get_area(func, x_range=[2, 8], color=BLUE, opacity=0.5)
        self.play(Transform(rects, integral_area), run_time=1.5)
        self.wait(1)