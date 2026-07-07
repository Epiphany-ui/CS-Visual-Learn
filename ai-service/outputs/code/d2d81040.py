import numpy as np
import math
from manim import *

class RiemannZetaAnalyticContinuation(Scene):
    def construct(self):
        # 坐标轴配置
        axes = Axes(
            x_range=[0.3, 2.7, 0.5],
            y_range=[-5, 5, 1],
            x_length=10,
            y_length=6,
            axis_config={"include_numbers": True}
        )
        x_label = axes.get_x_axis_label(Text("s"))
        y_label = axes.get_y_axis_label(Text("ζ(s)"))
        self.add(axes, x_label, y_label)

        # 标题和公式
        title = Text("Riemann Zeta Function ζ(s)", font_size=36).to_edge(UP)
        formula = MathTex(r"\zeta(s) = \sum_{n=1}^{\infty} \frac{1}{n^s} \quad (\Re(s)>1)")
        formula.next_to(title, DOWN, buff=0.3)
        self.add(title, formula)

        # 预计算数据点 (实轴上的 ζ(s) 值)
        xs = np.arange(0.5, 2.5, 0.04)          # 跳过 s=1
        def zeta_real(s):
            if abs(s - 1.0) < 1e-6:
                return None
            if s > 1:
                # 级数定义
                total = 0.0
                for n in range(1, 2000):
                    term = 1.0 / (n ** s)
                    total += term
                    if abs(term) < 1e-10:
                        break
                return total
            else:  # s < 1  用反射公式
                t = 1 - s                     # t > 1
                total = 0.0
                for n in range(1, 2000):
                    term = 1.0 / (n ** t)
                    total += term
                    if abs(term) < 1e-10:
                        break
                zeta_t = total
                factor = (2.0 ** s) * (math.pi ** (s - 1.0)) * math.sin(math.pi * s / 2.0) * math.gamma(1.0 - s)
                return factor * zeta_t

        points = [axes.c2p(s, zeta_real(s)) for s in xs if zeta_real(s) is not None]

        # 追踪点和轨迹
        dot = Dot(points[0], color=YELLOW)
        dot.set_z_index(10)
        path = TracedPath(dot.get_center, stroke_color=BLUE, stroke_width=3)
        self.add(dot, path)

        # 动画进度控制器
        t = ValueTracker(0)

        def update_dot(mob, dt):
            idx = int(t.get_value() * (len(points) - 1))
            if idx < len(points):
                mob.move_to(points[idx])

        dot.add_updater(update_dot)

        # 标注文字
        pole_label = Text("Pole at s=1", color=RED, font_size=28)
        pole_label.move_to(axes.c2p(1, -4.5))
        series_label = Text("Series definition", font_size=24, color=GREEN)
        series_label.move_to(axes.c2p(2.2, 2.5))
        extension_label = Text("Analytic continuation", font_size=24, color=BLUE)
        extension_label.move_to(axes.c2p(0.7, -2.5))

        # 动画流程
        self.play(FadeIn(title), FadeIn(formula), run_time=1)
        self.wait(0.5)

        # 移动点并画出曲线
        self.play(
            t.animate.set_value(1),
            run_time=18,
            rate_func=linear
        )
        dot.clear_updaters()

        # 显示标注
        self.play(
            Write(pole_label),
            Write(series_label),
            Write(extension_label),
            run_time=1
        )
        self.wait(1)