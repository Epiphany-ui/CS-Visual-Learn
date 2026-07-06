一、RAG 向量库 Markdown 文档
markdown
# 矩形脉冲信号的傅里叶变换（Rectangular Pulse → sinc Spectrum）

## 概述

矩形脉冲（Rectangular Pulse）是信号与系统中最基本的信号之一，其连续傅里叶变换（Continuous-Time Fourier Transform, CTFT）结果是一个 **sinc 函数**。这是理解傅里叶变换时域-频域对偶性的经典范例。

## 数学定义

### 时域：矩形脉冲

中心对称的单位矩形脉冲定义为[reference:0]：

$$p_\tau(t) = \begin{cases} 1, & |t| \leq \tau/2 \\ 0, & |t| > \tau/2 \end{cases}$$

其中 $\tau$ 为脉冲宽度。

更一般的形式：高度为 $A$、宽度为 $T$、中心在 $t_0$ 的矩形脉冲[reference:1]。

### 频域：sinc 函数

矩形脉冲的傅里叶变换为[reference:2][reference:3]：

$$P(f) = \tau \cdot \text{sinc}(\tau f) = \tau \cdot \frac{\sin(\pi \tau f)}{\pi \tau f}$$

其中 $\text{sinc}(x) = \frac{\sin(\pi x)}{\pi x}$[reference:4]。

等价地，用角频率 $\omega$ 表示[reference:5]：

$$P(\omega) = \tau \cdot \text{sinc}\left(\frac{\tau \omega}{2\pi}\right) = \frac{2\sin(\omega \tau/2)}{\omega}$$

## 傅里叶变换对

$$\boxed{p_\tau(t) = \text{rect}\left(\frac{t}{\tau}\right) \;\; \stackrel{\mathcal{F}}{\longleftrightarrow} \;\; \tau \cdot \text{sinc}(\tau f)}$$

## 关键性质

1. **时域越窄，频域越宽**：脉冲宽度 $\tau$ 减小时，sinc 主瓣变宽；反之脉冲变宽时，频谱主瓣变窄[reference:6]。
2. **能量守恒**：Parseval 定理表明，时域能量等于频域能量。
3. **sinc 函数的零点**：出现在 $f = n/\tau$（$n = \pm1, \pm2, \dots$）处。

## 应用场景

- 信号与系统课程教学可视化
- 数字信号处理中的理想低通滤波器设计
- 通信系统中的脉冲成型与带宽分析
- 雷达信号分析[reference:8]
二、Manim 动画代码
以下代码展示矩形脉冲时域波形及其傅里叶变换得到的 sinc 频谱，包含从时域到频域的变换动画效果。

python
from manim import *
import numpy as np

class RectangularPulseToSinc(Scene):
    """
    矩形脉冲 → sinc 连续频谱 傅里叶变换可视化
    展示时域矩形脉冲及其频域 sinc 函数频谱
    """
    def construct(self):
        # ========== 参数设置 ==========
        pulse_width = 2.0      # 脉冲宽度 tau
        pulse_height = 1.0     # 脉冲幅度 A
        
        # ========== 标题 ==========
        title = Text(
            "矩形脉冲的傅里叶变换",
            font_size=36,
            color=WHITE
        ).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)
        
        # ========== 时域坐标轴 ==========
        time_axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-0.5, 1.5, 0.5],
            x_length=6,
            y_length=3,
            axis_config={"color": BLUE},
            x_axis_config={"numbers_to_include": range(-4, 5)},
            y_axis_config={"numbers_to_include": [0, 0.5, 1.0]},
        ).shift(UP * 1.8 + LEFT * 3.2)
        
        time_label = time_axes.get_axis_labels(
            x_label=Tex("t"), 
            y_label=Tex("p(t)")
        )
        time_label.set_color(WHITE)
        
        time_title = Text("时域", font_size=24, color=BLUE).next_to(
            time_axes, UP, buff=0.1
        )
        
        self.play(Create(time_axes), Write(time_label), Write(time_title))
        self.wait(0.5)
        
        # ========== 绘制矩形脉冲 ==========
        # 矩形脉冲：宽度 pulse_width，高度 pulse_height，中心在 0
        rect = Rectangle(
            width=pulse_width,
            height=pulse_height,
            color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=0.3
        )
        # 将矩形放置到坐标轴对应位置
        rect.move_to(time_axes.coords_to_point(0, pulse_height/2))
        
        # 脉冲顶部水平线（视觉增强）
        top_line = Line(
            time_axes.coords_to_point(-pulse_width/2, pulse_height),
            time_axes.coords_to_point(pulse_width/2, pulse_height),
            color=YELLOW,
            stroke_width=3
        )
        
        # 脉冲底部水平线（在 x 轴上）
        bottom_line = Line(
            time_axes.coords_to_point(-pulse_width/2, 0),
            time_axes.coords_to_point(pulse_width/2, 0),
            color=YELLOW,
            stroke_width=3
        )
        
        # 左侧垂直线
        left_line = Line(
            time_axes.coords_to_point(-pulse_width/2, 0),
            time_axes.coords_to_point(-pulse_width/2, pulse_height),
            color=YELLOW,
            stroke_width=3
        )
        
        # 右侧垂直线
        right_line = Line(
            time_axes.coords_to_point(pulse_width/2, 0),
            time_axes.coords_to_point(pulse_width/2, pulse_height),
            color=YELLOW,
            stroke_width=3
        )
        
        pulse = VGroup(rect, top_line, bottom_line, left_line, right_line)
        
        self.play(Create(pulse), run_time=1.5)
        self.wait(0.5)
        
        # ========== 添加脉冲标注 ==========
        pulse_label = MathTex(
            f"p(t) = \\text{{rect}}\\left(\\frac{{t}}{{{pulse_width:.1f}}}\\right)",
            color=YELLOW,
            font_size=28
        ).next_to(time_axes, DOWN, buff=0.3)
        self.play(Write(pulse_label))
        self.wait(1)
        
        # ========== 频域坐标轴 ==========
        freq_axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-0.5, 2.5, 0.5],
            x_length=6,
            y_length=3,
            axis_config={"color": RED},
            x_axis_config={"numbers_to_include": range(-5, 6)},
            y_axis_config={"numbers_to_include": [0, 0.5, 1.0, 1.5, 2.0]},
        ).shift(UP * 1.8 + RIGHT * 3.2)
        
        freq_label = freq_axes.get_axis_labels(
            x_label=Tex("f"), 
            y_label=Tex("|P(f)|")
        )
        freq_label.set_color(WHITE)
        
        freq_title = Text("频域", font_size=24, color=RED).next_to(
            freq_axes, UP, buff=0.1
        )
        
        self.play(
            Create(freq_axes), 
            Write(freq_label), 
            Write(freq_title)
        )
        self.wait(0.5)
        
        # ========== 绘制 sinc 频谱 ==========
        # 定义 sinc 函数：P(f) = tau * sinc(tau * f)
        def sinc_spectrum(f):
            x = pulse_width * f
            if abs(x) < 1e-10:
                return pulse_width
            return pulse_width * np.sin(np.pi * x) / (np.pi * x)
        
        # 生成频谱曲线
        spectrum = freq_axes.plot(
            sinc_spectrum,
            x_range=[-4.8, 4.8],
            color=RED,
            stroke_width=3
        )
        
        # 添加频谱下方的填充区域
        filled_spectrum = freq_axes.get_area(
            sinc_spectrum,
            x_range=[-4.8, 4.8],
            color=RED,
            opacity=0.2
        )
        
        self.play(
            Create(filled_spectrum),
            Create(spectrum),
            run_time=2
        )
        self.wait(0.5)
        
        # ========== 添加频谱标注 ==========
        spectrum_label = MathTex(
            f"P(f) = {pulse_width:.1f} \\cdot \\text{{sinc}}({pulse_width:.1f}f)",
            color=RED,
            font_size=28
        ).next_to(freq_axes, DOWN, buff=0.3)
        self.play(Write(spectrum_label))
        self.wait(1)
        
        # ========== 添加傅里叶变换箭头 ==========
        arrow = DoubleArrow(
            start=time_axes.get_center() + RIGHT * 1.5,
            end=freq_axes.get_center() + LEFT * 1.5,
            color=WHITE,
            stroke_width=3,
            buff=0.3
        )
        arrow_label = MathTex(
            "\\mathcal{F}",
            color=WHITE,
            font_size=32
        ).move_to(arrow.get_center())
        
        self.play(
            Create(arrow),
            Write(arrow_label)
        )
        self.wait(0.5)
        
        # ========== 添加傅里叶变换对公式 ==========
        transform_pair = MathTex(
            r"p_\tau(t) = \text{rect}\left(\frac{t}{\tau}\right)",
            r"\quad \stackrel{\mathcal{F}}{\longleftrightarrow} \quad",
            r"P(f) = \tau \cdot \text{sinc}(\tau f)",
            font_size=30,
            color=WHITE
        ).to_edge(DOWN, buff=0.5)
        transform_pair[0].set_color(YELLOW)
        transform_pair[2].set_color(RED)
        
        self.play(Write(transform_pair))
        self.wait(0.5)
        
        # ========== 高亮脉冲宽度对频谱的影响 ==========
        self.wait(1)
        
        # 显示脉冲宽度标注
        width_brace = Brace(
            Line(
                time_axes.coords_to_point(-pulse_width/2, -0.15),
                time_axes.coords_to_point(pulse_width/2, -0.15),
            ),
            direction=DOWN,
            color=WHITE
        )
        width_label = MathTex(
            f"\\tau = {pulse_width:.1f}",
            color=WHITE,
            font_size=24
        ).next_to(width_brace, DOWN, buff=0.1)
        
        self.play(
            Create(width_brace),
            Write(width_label)
        )
        self.wait(0.5)
        
        # ========== 标注 sinc 主瓣 ==========
        # 第一个零点位置：f = 1/tau
        first_zero = 1.0 / pulse_width
        if abs(first_zero) < 4.8:
            zero_line = DashedLine(
                freq_axes.coords_to_point(first_zero, 0),
                freq_axes.coords_to_point(first_zero, sinc_spectrum(first_zero) + 0.1),
                color=WHITE,
                stroke_width=1.5,
                dash_length=0.05
            )
            zero_label = MathTex(
                f"f = 1/\\tau",
                color=WHITE,
                font_size=20
            ).next_to(zero_line, UP, buff=0.05)
            self.play(Create(zero_line), Write(zero_label))
        
        # ========== 收尾 ==========
        self.wait(2)
        
        # 淡出所有元素
        self.play(
            *[FadeOut(mob) for mob in self.mobjects if mob != title]
        )
        self.wait(0.5)
        self.play(FadeOut(title))
        self.wait(0.5)


class RectangularPulseWidthVariation(Scene):
    """
    矩形脉冲宽度变化对 sinc 频谱的影响
    展示时域脉冲越窄，频域 sinc 主瓣越宽
    """
    def construct(self):
        title = Text(
            "脉冲宽度变化对频谱的影响",
            font_size=36,
            color=WHITE
        ).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)
        
        # 创建时域和频域的坐标轴
        time_axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-0.5, 1.5, 0.5],
            x_length=5,
            y_length=2.5,
            axis_config={"color": BLUE},
        ).shift(UP * 1.5 + LEFT * 3.5)
        
        freq_axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-0.5, 3.5, 0.5],
            x_length=5,
            y_length=2.5,
            axis_config={"color": RED},
        ).shift(UP * 1.5 + RIGHT * 3.5)
        
        time_label = time_axes.get_axis_labels("t", "p(t)")
        freq_label = freq_axes.get_axis_labels("f", "|P(f)|")
        
        self.play(
            Create(time_axes), Write(time_label),
            Create(freq_axes), Write(freq_label)
        )
        self.wait(0.5)
        
        # 不同脉冲宽度
        widths = [3.0, 2.0, 1.0, 0.6]
        colors = [BLUE_D, BLUE, GREEN, YELLOW]
        freq_colors = [RED_D, RED, ORANGE, PINK]
        
        pulses = VGroup()
        spectra = VGroup()
        
        for i, (w, c, fc) in enumerate(zip(widths, colors, freq_colors)):
            # 绘制矩形脉冲
            rect = Rectangle(
                width=w,
                height=1.0,
                color=c,
                fill_color=c,
                fill_opacity=0.2
            )
            rect.move_to(time_axes.coords_to_point(0, 0.5))
            
            # 脉冲边框
            pulse_lines = VGroup()
            pulse_lines.add(
                Line(time_axes.coords_to_point(-w/2, 0), time_axes.coords_to_point(-w/2, 1), color=c),
                Line(time_axes.coords_to_point(w/2, 0), time_axes.coords_to_point(w/2, 1), color=c),
                Line(time_axes.coords_to_point(-w/2, 1), time_axes.coords_to_point(w/2, 1), color=c),
            )
            
            pulse = VGroup(rect, pulse_lines)
            pulse.shift(DOWN * i * 0.7)
            pulses.add(pulse)
            
            # 计算并绘制对应的 sinc 频谱
            def make_sinc(w):
                def func(f):
                    x = w * f
                    if abs(x) < 1e-10:
                        return w
                    return w * np.sin(np.pi * x) / (np.pi * x)
                return func
            
            spectrum = freq_axes.plot(
                make_sinc(w),
                x_range=[-4.8, 4.8],
                color=fc,
                stroke_width=2.5
            )
            spectrum.shift(DOWN * i * 0.7)
            spectra.add(spectrum)
        
        # 逐个显示
        for i in range(len(widths)):
            self.play(
                Create(pulses[i]),
                Create(spectra[i]),
                run_time=0.8
            )
            self.wait(0.3)
        
        # 添加说明
        note = Text(
            "脉冲越窄 → 频谱越宽",
            font_size=28,
            color=WHITE
        ).to_edge(DOWN)
        self.play(Write(note))
        
        self.wait(2)
三、使用说明
环境要求
Python 3.7+

Manim Community Edition (pip install manim)

NumPy (pip install numpy)

运行命令
bash
# 运行主场景
manim -pql your_file.py RectangularPulseToSinc

# 运行脉冲宽度变化演示
manim -pql your_file.py RectangularPulseWidthVariation
代码结构说明
类名	功能
RectangularPulseToSinc	主场景：并排显示时域矩形脉冲和频域 sinc 频谱，包含完整的傅里叶变换对公式
RectangularPulseWidthVariation	扩展场景：展示不同脉冲宽度对应的频谱变化，直观体现"时域越窄，频域越宽"
