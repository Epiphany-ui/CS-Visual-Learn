from manim import *
import numpy as np

class FourierVisualization(Scene):
    def construct(self):
        # 方波的傅里叶级数系数（前8个奇次谐波）
        coeffs = []
        for k in range(1, 16, 2):
            amp = 4 / (np.pi * k)
            phase = -PI / 2  # 因为 sin(k t) = cos(k t - pi/2)
            coeffs.append((k, amp, phase))

        # 追踪末端点的圆点
        drawing_dot = Dot(color=YELLOW, radius=0.08)
        self.add(drawing_dot)

        # 轨迹线，追踪drawing_dot的位置
        traced_path = TracedPath(drawing_dot.get_center, stroke_color=BLUE, stroke_width=2)
        self.add(traced_path)

        # 创建用于表示每个旋转向量的线段组
        vectors = VGroup()
        for _ in coeffs:
            line = Line(ORIGIN, ORIGIN, stroke_width=1.5, color=WHITE)
            vectors.add(line)
        self.add(vectors)

        # 角度时间追踪器
        angle_tracker = ValueTracker(0)

        # 更新函数：根据当前角度更新所有线段和末端点
        def update_vectors(mob, dt):
            current_angle = angle_tracker.get_value()
            pos = np.array([0.0, 0.0, 0.0])
            for idx, (freq, amp, phase) in enumerate(coeffs):
                # 计算当前向量在复平面上的投影
                real = amp * np.cos(freq * current_angle + phase)
                imag = amp * np.sin(freq * current_angle + phase)
                end = pos + np.array([real, imag, 0])
                vectors[idx].put_start_and_end_on(pos, end)
                pos = end
            drawing_dot.move_to(pos)

        vectors.add_updater(update_vectors)

        # 播放动画：角度从0到2π
        self.play(angle_tracker.animate.set_value(2 * PI), run_time=10, rate_func=linear)
        self.wait(2)