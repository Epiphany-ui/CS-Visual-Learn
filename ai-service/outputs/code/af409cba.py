from manim import *
import math

class FourierTransformScene(Scene):
    def construct(self):
        # ========== 1. 配置坐标轴 ==========
        # 时域坐标轴：x轴范围 0~2π，y轴范围 -2~2
        axes_time = Axes(
            x_range=[0, 2 * PI, PI / 2],
            y_range=[-2, 2, 1],
            x_length=5,
            y_length=3.5,
            axis_config={"include_numbers": False, "color": BLUE_C},
        ).shift(LEFT * 3 + DOWN * 0.5)
        axes_time_labels = axes_time.get_axis_labels(x_label="t", y_label="Amp")

        # 频域坐标轴：x轴范围 0~8，y轴范围 0~1.5
        axes_freq = Axes(
            x_range=[0, 8, 1],
            y_range=[0, 1.5, 0.5],
            x_length=5,
            y_length=3.5,
            axis_config={"include_numbers": False, "color": ORANGE},
        ).shift(RIGHT * 3 + DOWN * 0.5)
        axes_freq_labels = axes_freq.get_axis_labels(x_label="f", y_label="Mag")

        # ========== 2. 时域信号（复合正弦波） ==========
        # f(t) = sin(2*pi*2*t) + 0.5*sin(2*pi*5*t)
        def f(t):
            return math.sin(2 * PI * 2 * t) + 0.5 * math.sin(2 * PI * 5 * t)

        time_curve = axes_time.plot(
            f,
            x_range=[0, 2 * PI],
            color=BLUE,
            stroke_width=3,
            use_smoothing=False,
        )

        # ========== 3. 频域幅度谱（离散条形） ==========
        freq_peaks = [(2, 1.0), (5, 0.5)]  # (频率, 幅度)
        bar_width = 0.5
        bars = VGroup()
        for f_val, amp in freq_peaks:
            # 在频域坐标上生成条形矩形
            bottom_left = axes_freq.c2p(f_val - bar_width / 2, 0)
            top_right = axes_freq.c2p(f_val + bar_width / 2, amp)
            rect = Rectangle(
                width=top_right[0] - bottom_left[0],
                height=top_right[1] - bottom_left[1],
                fill_color=ORANGE,
                fill_opacity=0.8,
                stroke_color=YELLOW,
                stroke_width=2,
            ).move_to(
                np.array([(bottom_left[0] + top_right[0]) / 2,
                          (bottom_left[1] + top_right[1]) / 2, 0])
            )
            bars.add(rect)

        # 添加频率数值标签
        freq_labels = VGroup()
        for f_val, amp in freq_peaks:
            label = MathTex(str(f_val), color=ORANGE, font_size=24)
            label.next_to(axes_freq.c2p(f_val, 0), DOWN, buff=0.15)
            freq_labels.add(label)

        # ========== 4. 标题 ==========
        title = Text("傅里叶变换：时域 → 频域", font_size=30, color=WHITE)
        title.to_edge(UP, buff=0.3)

        # ========== 5. 动画序列 ==========
        # 第一步：显示标题和坐标轴
        self.play(
            Write(title, run_time=1.5),
            Create(axes_time, run_time=1.2),
            Write(axes_time_labels, run_time=0.5),
            Create(axes_freq, run_time=1.2),
            Write(axes_freq_labels, run_time=0.5),
        )
        self.wait(0.5)

        # 第二步：绘制时域信号曲线
        self.play(
            Create(time_curve, run_time=3, rate_func=smooth),
        )
        self.wait(0.3)

        # 第三步：绘制频域幅度谱
        self.play(
            Create(bars, run_time=2, rate_func=linear),
            Write(freq_labels, run_time=1),
        )
        self.wait(1)

        # 第四步：强调对应关系（添加连接箭头）
        arrow1 = Arrow(
            start=axes_time.c2p(0.25, f(0.25)),
            end=axes_freq.c2p(2, 1.0),
            color=YELLOW,
            stroke_width=3,
            buff=0.1,
        )
        arrow2 = Arrow(
            start=axes_time.c2p(0.4, f(0.4)),
            end=axes_freq.c2p(5, 0.5),
            color=YELLOW,
            stroke_width=3,
            buff=0.1,
        )
        self.play(
            Create(arrow1, run_time=1),
            Create(arrow2, run_time=1),
        )
        self.wait(1.5)

        # 结束前短暂定格
        self.wait(1)