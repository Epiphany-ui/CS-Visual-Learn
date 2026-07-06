---

### 📦 24. 物理与信号：正弦波相位移动 (Signal Processing)
**文件建议命名：** `template_24_sine_wave_phase.md`

```markdown
# 意图：展示信号处理中的正弦波。利用 ValueTracker 动态修改正弦函数的相位（Phase），使得波形在坐标轴上产生平滑滚动的效果。
# 关键词：正弦波, 信号, 相位, 波形滚动, 函数图像, np.sin, always_redraw

下面是完整的 Manim 代码示例：
```python
from manim import *

class SineWavePhaseShift(Scene):
    def construct(self):
        # 1. 建立长条形坐标系
        axes = Axes(
            x_range=[0, 4 * PI, PI / 2],
            y_range=[-2, 2, 1],
            x_length=10,
            y_length=4,
            axis_config={"color": GRAY}
        )
        self.add(axes)

        # 2. 定义相位追踪器
        phase_tracker = ValueTracker(0)

        # 3. 使用 always_redraw 动态重绘函数图像
        # 公式: y = sin(x - phase)
        wave = always_redraw(lambda: axes.plot(
            lambda x: np.sin(x - phase_tracker.get_value()),
            color=YELLOW,
            stroke_width=4
        ))

        self.play(Create(wave))
        self.wait(1)

        # 4. 动画：让相位从 0 变到 4π，由于 wave 被 always_redraw 绑定，会产生向右滚动的视觉效果
        self.play(
            phase_tracker.animate.set_value(4 * PI),
            run_time=4,
            rate_func=linear # 线性匀速滚动
        )
        self.wait(1)