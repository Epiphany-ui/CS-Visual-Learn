---

### 📦 33. 信号处理：动态卷积积分 (Continuous Convolution)
**文件建议命名：** `template_33_convolution_integral.md`

```markdown
# 意图：可视化两个函数的卷积操作（Convolution）。展示一个方波反转后，如何在另一个方波上滑动，并实时填充和计算它们重叠面积的积分结果。
# 关键词：卷积, 信号处理, 积分, 滑动窗口, 面积, get_area, Intersection

下面是完整的 Manim 代码示例：
```python
from manim import *

class ConvolutionVisualization(Scene):
    def construct(self):
        axes = Axes(x_range=[-4, 6, 1], y_range=[0, 3, 1], axis_config={"color": GRAY})
        self.play(Create(axes))

        # 1. 定义固定的信号 f(t) [用一个宽度为 2 的方波表示]
        f_rect = Rectangle(width=2, height=2, color=BLUE, fill_opacity=0.5)
        f_rect.move_to(axes.c2p(1, 1)) # 中心在 x=1
        f_label = Text("函数 f", font_size=24, color=BLUE).next_to(f_rect, UP)
        self.play(FadeIn(f_rect), Write(f_label))

        # 2. 定义滑动的滤波器 g(t-tau) [用另一个方波表示]
        slide_tracker = ValueTracker(-3.0)
        
        g_rect = always_redraw(lambda: Rectangle(
            width=2, height=1.5, color=RED, fill_opacity=0.5
        ).move_to(axes.c2p(slide_tracker.get_value(), 0.75)))
        
        g_label = always_redraw(lambda: Text(
            "滤波器 g 滑动", font_size=20, color=RED
        ).next_to(g_rect, DOWN))

        self.add(g_rect, g_label)

        # 3. 核心机制：计算重叠部分的动态面积（交集）
        # 利用 Intersection 布尔运算实时求交集图形
        overlap = always_redraw(lambda: Intersection(
            f_rect, g_rect, color=YELLOW, fill_opacity=0.8
        ))
        self.add(overlap)

        # 4. 卷积滑动动画，让滤波器穿过固定信号
        self.play(slide_tracker.animate.set_value(5.0), run_time=6, rate_func=linear)
        self.wait(1)