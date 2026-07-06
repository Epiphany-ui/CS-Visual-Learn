
---

### 📦 35. 傅里叶连续变换：缠绕机器频率频谱 (Fourier Transform Winding)
**文件建议命名：** `template_35_fourier_transform_winding.md`

```markdown
# 意图：完美复刻 3Blue1Brown 最著名的傅里叶变换原理（缠绕机器）。将一个随时间波动的复合信号，按照不同的缠绕频率，缠绕在复平面的原点上。
# 关键词：傅里叶变换, 频谱, 信号缠绕, 质心, 连续变换, ParametricFunction, ValueTracker

下面是完整的 Manim 代码示例：
```python
from manim import *
import numpy as np

class FourierWindingMachine(Scene):
    def construct(self):
        # 1. 复平面环境
        plane = ComplexPlane(x_range=[-2, 2, 1], y_range=[-2, 2, 1]).set_opacity(0.5)
        self.add(plane)

        # 2. 纯文本标签
        freq_label_text = Text("当前缠绕频率 (Hz):", font_size=24).to_corner(UL)
        self.add(freq_label_text)

        # 3. 缠绕频率追踪器
        freq_tracker = ValueTracker(0.1)
        
        freq_val_label = always_redraw(lambda: Text(
            f"{freq_tracker.get_value():.2f}", 
            font_size=24, color=YELLOW
        ).next_to(freq_label_text, RIGHT))
        self.add(freq_val_label)

        # 4. 核心逻辑：定义复合信号并执行指数缠绕 (Fourier 核心公式 f(t) * e^(-i * 2pi * f * t))
        def get_wound_curve():
            winding_freq = freq_tracker.get_value()
            
            # ParametricFunction 能将一维信号变成复平面上的二维曲线
            return ParametricFunction(
                lambda t: plane.n2p(
                    # 原始信号: 包含 2Hz 和 3Hz 的复合波
                    (np.cos(2 * PI * 2 * t) + 0.5 * np.cos(2 * PI * 3 * t)) 
                    # 缠绕算子
                    * np.exp(-1j * 2 * PI * winding_freq * t)
                ),
                t_range=[0, 3, 0.01], # 对信号采样 3 秒
                color=YELLOW,
                stroke_width=2
            )

        # 使用 always_redraw 保证当频率改变时，整个缠绕图案会动态重绘
        wound_signal = always_redraw(get_wound_curve)
        self.add(wound_signal)

        # 5. 扫描频率动画：从 0.1Hz 扫到 4Hz。
        # 当频率经过 2Hz 和 3Hz 时，图案会严重偏向一侧（这就是频域尖峰的几何本质）
        self.play(freq_tracker.animate.set_value(4.0), run_time=10, rate_func=linear)
        self.wait(1)