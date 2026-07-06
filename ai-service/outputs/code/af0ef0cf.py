import numpy as np
from manim import *

class FourierTransformVisualization(Scene):
    def construct(self):
        # 创建时域坐标系 (左半部分)
        time_axes = Axes(
            x_range=[0, 4, 1],
            y_range=[-2, 2, 1],
            x_length=5,
            y_length=3.5,
            axis_config={"include_numbers": True, "font_size": 24},
            x_axis_config={"numbers_to_include": range(5)},
            y_axis_config={"numbers_to_include": range(-2, 3)},
        ).to_edge(LEFT, buff=1)
        time_label = Text("时域波形", font_size=24).next_to(time_axes, UP)

        # 创建频域坐标系 (右半部分)
        freq_axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 1.5, 0.5],
            x_length=5,
            y_length=3.5,
            axis_config={"include_numbers": True, "font_size": 24},
            x_axis_config={"numbers_to_include": range(6)},
            y_axis_config={"numbers_to_include": [0, 0.5, 1.0, 1.5]},
        ).to_edge(RIGHT, buff=1)
        freq_label = Text("频域幅度谱", font_size=24).next_to(freq_axes, UP)

        # 合成信号: 两个正弦波叠加，展示时域波形
        signal = time_axes.plot(
            lambda x: np.sin(2 * PI * 1 * x) + 0.5 * np.sin(2 * PI * 3 * x),
            x_range=[0, 4, 0.01],
            color=BLUE,
            stroke_width=2.5,
        )

        # 频域中的两个主峰 (频率 1 Hz 和 3 Hz)
        stem1 = Line(
            freq_axes.c2p(1, 0),
            freq_axes.c2p(1, 1),
            color=YELLOW,
            stroke_width=4,
        )
        tip1 = Dot(freq_axes.c2p(1, 1), color=YELLOW, radius=0.1)
        stem2 = Line(
            freq_axes.c2p(3, 0),
            freq_axes.c2p(3, 0.5),
            color=YELLOW,
            stroke_width=4,
        )
        tip2 = Dot(freq_axes.c2p(3, 0.5), color=YELLOW, radius=0.1)
        freq_stems = VGroup(stem1, tip1, stem2, tip2)

        # 动画步骤
        # 1. 绘制时域坐标系和信号波形
        self.play(Create(time_axes), Write(time_label))
        self.play(Create(signal), run_time=3)
        self.wait(0.5)

        # 2. 绘制频域坐标系
        self.play(Create(freq_axes), Write(freq_label))

        # 3. 依次出现频域中的峰值，体现时频对应
        self.play(GrowFromEdge(stem1, DOWN), GrowFromCenter(tip1))
        self.wait(0.3)
        self.play(GrowFromEdge(stem2, DOWN), GrowFromCenter(tip2))
        self.wait(0.5)

        # 4. 最后整体保持片刻，总时长控制在30秒内
        self.wait(2)