---

### 📦 模板 4：动态追踪与实时数值更新 (Updater)
大模型极难写对 `updater`（更新器）。这个模板教会大模型如何使用 `ValueTracker` 让数字跟着图形一起变。

```markdown
# 意图：使用变量追踪器，让屏幕上的数字或图形属性（如小数点数值）进行动态实时变化
# 关键词：动态, 实时更新, 数值, 追踪, ValueTracker, always_redraw, DecimalNumber

下面是完整的 Manim 代码示例：
```python
from manim import *

class DynamicValueTracker(Scene):
    def construct(self):
        # 1. 创建核心追踪器，初始值为 0
        tracker = ValueTracker(0)

        # 2. 创建动态数字，并绑定到追踪器的值上
        number = always_redraw(
            lambda: DecimalNumber(
                tracker.get_value(),
                num_decimal_places=2,
                color=GREEN,
                font_size=72
            )
        )
        
        # 添加一些固定说明文字
        label = Text("当前数值：", font_size=40).next_to(number, LEFT)
        group = VGroup(label, number).move_to(ORIGIN)

        self.play(Write(label), FadeIn(number))
        
        # 3. 动画：通过改变 tracker 的值，数字会自动更新
        self.play(tracker.animate.set_value(100), run_time=3, rate_func=smooth)
        self.wait(1)