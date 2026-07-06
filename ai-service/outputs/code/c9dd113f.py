from manim import *
import numpy as np

class FourierTransformVisualization(Scene):
    def construct(self):
        self.camera.background_color = "#0D1117"
        
        # 标题
        title = Text("傅里叶变换: 矩形脉冲", font_size=36, color=WHITE).to_edge(UP)
        
        # 时域坐标系
        axes_time = Axes(
            x_range=[-4, 4, 1],
            y_range=[-0.5, 2, 0.5],
            x_length=6,
            y_length=3,
            axis_config={"include_numbers": True, "color": BLUE},
        ).shift(LEFT * 3.5 + DOWN * 0.5)
        time_label = axes_time.get_axis_labels(x_label="t", y_label="f(t)")
        
        # 频域坐标系
        axes_freq = Axes(
            x_range=[-6, 6, 1],
            y_range=[-0.5, 2, 0.5],
            x_length=6,
            y_length=3,
            axis_config={"include_numbers": True, "color": YELLOW},
        ).shift(RIGHT * 3.5 + DOWN * 0.5)
        freq_label = axes_freq.get_axis_labels(x_label="ω", y_label="|F(ω)|")
        
        # 中间的变换符号
        transform_arrow = MathTex(r"\Rightarrow", color=WHITE).scale(2).shift(DOWN * 0.5)
        
        # 函数表达式标签
        formula_time = MathTex(r"f(t)=\mathrm{rect}(t/T)", color=BLUE).next_to(axes_time, DOWN)
        formula_freq = MathTex(r"|F(\omega)|=T\cdot\mathrm{sinc}(T\omega/2)", color=YELLOW).next_to(axes_freq, DOWN)
        
        # 用于控制脉冲宽度的数值追踪器
        pulse_width = ValueTracker(1.0)
        
        # 时域矩形脉冲（自动更新）
        rect_pulse = always_redraw(lambda: self.get_rect_pulse(axes_time, pulse_width.get_value()))
        
        # 频域 Sinc 函数图像（自动更新）
        sinc_graph = always_redraw(lambda: self.get_sinc_graph(axes_freq, pulse_width.get_value()))
        
        # 显示当前 T 值的标签
        T_label = always_redraw(lambda: MathTex(f"T = {pulse_width.get_value():.1f}", color=WHITE).to_corner(UL))
        
        # 添加到场景
        self.add(title, axes_time, time_label, rect_pulse, formula_time, transform_arrow, 
                 axes_freq, freq_label, sinc_graph, formula_freq, T_label)
        
        # 播放动画，展示脉冲宽度变化对频域的影响（傅里叶变换的尺度变换性质）
        self.wait(1)
        self.play(pulse_width.animate.set_value(2.0), run_time=5, rate_func=there_and_back)
        self.play(pulse_width.animate.set_value(0.5), run_time=5, rate_func=there_and_back)
        self.play(pulse_width.animate.set_value(1.5), run_time=4, rate_func=there_and_back)
        self.wait(2)
    
    def get_rect_pulse(self, axes, T):
        """生成时域矩形脉冲"""
        left = -T / 2
        right = T / 2
        # 构建矩形四个顶点
        points = [
            axes.coords_to_point(left, 0),
            axes.coords_to_point(right, 0),
            axes.coords_to_point(right, 1),
            axes.coords_to_point(left, 1),
        ]
        return Polygon(*points, color=BLUE, fill_opacity=0.5, stroke_width=2)
    
    def get_sinc_graph(self, axes, T):
        """生成频域 Sinc 函数图像"""
        graph = axes.plot(
            lambda w: T * np.sinc(T * w / (2 * np.pi)),
            x_range=[-6, 6],
            color=YELLOW,
            stroke_width=2,
        )
        return graph