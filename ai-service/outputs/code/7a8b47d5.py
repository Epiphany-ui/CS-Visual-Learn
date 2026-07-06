from manim import *
import numpy as np

class FourierTransform(Scene):
    def construct(self):
        # 创建复平面，适当缩放以容纳轨迹
        plane = ComplexPlane(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
        ).add_coordinates()
        self.add(plane)

        # 傅里叶系数：前5项，幅度 1/n，相位 -45°
        coeffs = [(1.0 / n) * (1 - 1j) for n in range(1, 6)]
        freqs = list(range(1, len(coeffs) + 1))    # 对应频率 1,2,3,4,5

        # 使用 ValueTracker 控制时间
        t = ValueTracker(0)

        # 原点标记
        origin_dot = Dot(plane.n2p(0), radius=0.05, color=WHITE)
        self.add(origin_dot)

        # 创建每一条向量线段（初始为退化线段）
        lines = VGroup()
        for _ in range(len(coeffs)):
            lines.add(Line(ORIGIN, ORIGIN, color=BLUE))

        # 笔尖和尾迹
        pen = Dot(color=YELLOW, radius=0.1)
        trace = TracedPath(pen.get_center, stroke_color=YELLOW, stroke_width=2)
        self.add(trace, pen)

        # 定义更新器，用于所有向量和笔尖
        def update_lines(mob):
            current = 0 + 0j          # 复数形式的当前位置
            t_val = t.get_value()

            for i, (coeff, freq) in enumerate(zip(coeffs, freqs)):
                # 当前向量旋转后的复数（方向和长度）
                rotated = coeff * np.exp(1j * freq * t_val)
                start = current
                end = current + rotated

                # 更新对应线段
                line = mob[i]
                line.put_start_and_end_on(
                    plane.n2p(start),
                    plane.n2p(end)
                )
                current = end

            # 笔尖移动到向量末端的最终位置
            pen.move_to(plane.n2p(current))

        lines.add_updater(update_lines)
        self.add(lines)

        # 标题
        title = Text("傅里叶级数可视化", font_size=36).to_corner(UL)
        self.add(title)

        # 播放动画：时间从0到10个周期，时长20秒
        self.play(t.animate.set_value(10 * PI), run_time=20, rate_func=linear)
        self.wait(5)