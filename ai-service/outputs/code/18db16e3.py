from manim import *
import math

class FourierTransform(Scene):
    def construct(self):
        n_harmonics = 3
        amplitudes = [1, 1/3, 1/5]
        frequencies = [1, 3, 5]
        T = 2 * PI

        # ---------- 坐标轴 ----------
        # 左侧：复平面，显示旋转向量（实轴向右，虚轴向上）
        left_axes = Axes(
            x_range=[-2, 2], y_range=[-2, 2],
            x_length=4, y_length=4,
            axis_config={"color": BLUE_D, "include_numbers": False}
        ).shift(LEFT * 3)
        # 使用 Text 替代 MathTex 标签
        re_label = Text("Re", color=BLUE_D).next_to(left_axes.get_x_axis(), DOWN)
        im_label = Text("Im", color=BLUE_D).next_to(left_axes.get_y_axis(), LEFT)
        left_labels = VGroup(re_label, im_label)

        # 右侧：频域幅度条（频率 vs 幅度）
        right_axes = Axes(
            x_range=[0, 4], y_range=[0, 1.5],
            x_length=3, y_length=3,
            axis_config={"color": GREEN_D, "include_numbers": False}
        ).shift(RIGHT * 3)
        f_label = Text("f", color=GREEN_D).next_to(right_axes.get_x_axis(), DOWN)
        a_label = Text("A", color=GREEN_D).next_to(right_axes.get_y_axis(), LEFT)
        freq_labels = VGroup(f_label, a_label)

        # ---------- 频域条形图 ----------
        bars = VGroup()
        bar_colors = [YELLOW, ORANGE, RED]
        for i in range(n_harmonics):
            bar = Rectangle(
                width=0.5, height=amplitudes[i],
                fill_opacity=0.8,
                color=bar_colors[i]
            )
            bar.move_to(
                right_axes.c2p(frequencies[i], 0) + UP * (amplitudes[i] / 2),
                aligned_edge=DOWN
            )
            bars.add(bar)

        # 使用 Text 代替 MathTex
        freq_labels_text = VGroup(
            Text("1", color=YELLOW).next_to(bars[0], DOWN),
            Text("3", color=ORANGE).next_to(bars[1], DOWN),
            Text("5", color=RED).next_to(bars[2], DOWN)
        )

        # ---------- 旋转向量（复平面） ----------
        circles = VGroup()
        circle_colors = [BLUE_C, TEAL_C, PURPLE_C]
        for i in range(n_harmonics):
            c = Circle(
                radius=amplitudes[i],
                color=circle_colors[i],
                stroke_opacity=0.3
            ).move_to(left_axes.c2p(0, 0))
            circles.add(c)

        vectors = VGroup()
        vector_colors = [BLUE, TEAL, PURPLE]
        for i in range(n_harmonics):
            vec = Line(
                left_axes.c2p(0, 0),
                left_axes.c2p(0, 0),
                color=vector_colors[i]
            )
            vectors.add(vec)

        dots = VGroup()
        for i in range(n_harmonics):
            dot = Dot(color=circle_colors[i], radius=0.05)
            dots.add(dot)

        # ---------- 时域信号合成 ----------
        time_axes = Axes(
            x_range=[0, T], y_range=[-2, 2],
            x_length=6, y_length=2,
            axis_config={"color": GREY_C, "include_numbers": False}
        ).shift(DOWN * 2.5)
        t_label = Text("t", color=GREY_C).next_to(time_axes.get_x_axis(), DOWN)
        xt_label = Text("x(t)", color=GREY_C).next_to(time_axes.get_y_axis(), LEFT)
        time_labels = VGroup(t_label, xt_label)

        time_dot = Dot(color=YELLOW, radius=0.08)
        trace = TracedPath(time_dot.get_center, stroke_opacity=0.8, stroke_width=3)
        self.add(trace)

        t_tracker = ValueTracker(0)

        # ---------- 更新函数 ----------
        def update_vectors(mob, dt):
            t = t_tracker.get_value()
            start = left_axes.c2p(0, 0)
            cum_x = 0
            cum_y = 0
            for i in range(n_harmonics):
                angle = frequencies[i] * t
                vec_x = amplitudes[i] * math.cos(angle)
                vec_y = amplitudes[i] * math.sin(angle)
                # 将当前起点转为数值坐标
                start_num = left_axes.p2c(start)
                end_num = (start_num[0] + vec_x, start_num[1] + vec_y)
                end_point = left_axes.c2p(end_num[0], end_num[1])
                vectors[i].put_start_and_end_on(start, end_point)
                dots[i].move_to(end_point)
                start = end_point
                cum_x += vec_x
                cum_y += vec_y

            signal_x = cum_x
            t_coord = time_axes.c2p(t, signal_x)
            time_dot.move_to(t_coord)

        vectors.add_updater(update_vectors)

        # ---------- 创建动画 ----------
        self.play(
            Create(left_axes), Write(left_labels),
            Create(right_axes), Write(freq_labels),
            Create(time_axes), Write(time_labels),
            Create(circles),
            Create(bars), Write(freq_labels_text),
            run_time=4
        )
        self.play(
            LaggedStart(
                *[Create(vec) for vec in vectors],
                *[Create(dot) for dot in dots],
                lag_ratio=0.3
            ),
            run_time=3
        )
        self.play(Create(time_dot), run_time=1)

        self.play(
            t_tracker.animate.set_value(T),
            run_time=15,
            rate_func=linear
        )
        self.wait(2)
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=3
        )