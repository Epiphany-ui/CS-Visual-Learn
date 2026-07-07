from manim import *
import numpy as np

class FourierEighthNote(Scene):
    def construct(self):
        # ------------------------ 参数设置 -------------------------
        NUM_POINTS = 300          # 采样点数
        NUM_COMPONENTS = 30       # 使用的傅里叶分量数
        CYCLE_TIME = 4.0          # 画完一个完整周期的时间（秒）
        # 音符形状参数
        R_BASE = 1.5              # 音符基本半径
        EXTRA_AMP = 1.2           # 尾巴处突出幅度
        # ----------------------------------------------------------

        # 1. 生成闭合路径（极坐标方式，模拟八分音符轮廓）
        angles = np.linspace(0, 2 * PI, NUM_POINTS, endpoint=False)
        points = []
        for i, theta in enumerate(angles):
            r = R_BASE
            shift_angle = 0.0
            # 尾巴位于右上方区域 (π/4 ~ 3π/4)
            if PI / 4 <= theta <= 3 * PI / 4:
                t = (theta - PI / 4) / (PI / 2)   # 归一化到 [0,1]
                extra = EXTRA_AMP * np.sin(PI * t)  # 径向突出
                r += extra
                # 角度向左偏移，使尾巴弯曲
                shift_angle = -0.3 * (1 - np.cos(2 * PI * t))
            x = r * np.cos(theta + shift_angle)
            y = r * np.sin(theta + shift_angle)
            points.append(np.array([x, y, 0]))

        # 转换为复数数组
        complex_points = [p[0] + 1j * p[1] for p in points]
        # 计算傅里叶系数
        coeffs = np.fft.fft(complex_points) / NUM_POINTS
        # 选择幅度最大的前 NUM_COMPONENTS 个（排除直流？但包含直流）
        amps = np.abs(coeffs)
        order = np.argsort(amps)[::-1]   # 按幅度降序
        # 取前N个，但保证包含所有频率
        selected_indices = order[:NUM_COMPONENTS] if len(order) > NUM_COMPONENTS else order
        # 确保包含0频率（直流分量）
        if 0 not in selected_indices:
            selected_indices = np.append(selected_indices, 0)

        # 提取分量信息，频率使用索引（0~N/2为正，N/2+1~N-1为负）
        N = NUM_POINTS
        components = []  # 每个元素: (freq, amp, phase)
        for idx in selected_indices:
            c = coeffs[idx]
            amp = abs(c)
            if amp < 1e-5:
                continue
            phase = np.angle(c)
            if idx <= N // 2:
                freq = idx
            else:
                freq = idx - N
            components.append((freq, amp, phase))

        # 按频率升序排列，使得圆从慢到快
        components.sort(key=lambda x: x[0])

        # 2. 创建坐标轴（适当缩放）
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            axis_config={"color": BLUE_D, "include_numbers": False}
        )
        axes_labels = axes.get_axis_labels(
            Text("x").scale(0.6), Text("y").scale(0.6)
        )
        self.add(axes, axes_labels)

        # 3. 创建旋转向量（圆圈+箭头）
        circles = VGroup()
        arrows = VGroup()
        # 初始位置为原点
        pos_tracker = ValueTracker(0.0)   # 时间参数 t

        def get_vector_end(freq, amp, phase, t):
            """返回该分量对应的向量 (作为复数)"""
            return amp * np.exp(1j * (2 * PI * freq * t / CYCLE_TIME + phase))

        # 从底层开始叠加
        current_pos = np.array([0.0, 0.0, 0.0])
        for i, (freq, amp, phase) in enumerate(components):
            # 圆圈半径 = 振幅
            circle = Circle(
                radius=amp,
                color=YELLOW,
                stroke_width=1.5,
                stroke_opacity=0.7
            )
            # 箭头从圆心指向终点
            arrow = Arrow(
                start=ORIGIN,
                end=RIGHT * amp,
                color=WHITE,
                stroke_width=2,
                buff=0
            )
            # 初始位置放在累积位置
            circle.shift(current_pos)
            arrow.shift(current_pos)
            circles.add(circle)
            arrows.add(arrow)
            # 更新当前累积位置（初始相位）
            vec = get_vector_end(freq, amp, phase, 0)
            current_pos += np.array([vec.real, vec.imag, 0])

        # 末端追踪点（初始在最后位置）
        trace_point = Dot(current_pos, color=GREEN, radius=0.08)
        # 轨迹
        traced_path = TracedPath(trace_point.get_center, stroke_color=GREEN_B, stroke_width=2.5, stroke_opacity=0.9)

        # 4. 创建更新器
        def update_circles(mob, dt):
            t = pos_tracker.get_value()
            # 更新所有圆和箭头
            acc_pos = np.array([0.0, 0.0, 0.0])
            for i in range(len(components)):
                freq, amp, phase = components[i]
                # 该分量的向量
                vec = get_vector_end(freq, amp, phase, t)
                vec_3d = np.array([vec.real, vec.imag, 0])
                # 圆心位置 = 累积位置
                circle = circles[i]
                arrow = arrows[i]
                circle.move_to(acc_pos)
                # 箭头：从圆心指向圆心+vec
                arrow.put_start_and_end_on(acc_pos, acc_pos + vec_3d)
                # 累加位置
                acc_pos += vec_3d
            # 更新末端追踪点
            trace_point.move_to(acc_pos)

        # 将更新器添加到场景的一个虚拟机对象（或直接添加到 mob 的 updater）
        dummy_clock = Mobject()
        # 时间递增更新器
        dummy_clock.add_updater(lambda m, dt: pos_tracker.increment_value(dt))
        # 同时添加更新器到 circles 组（用于更新位置）
        circles.add_updater(update_circles)
        self.add(dummy_clock, circles, arrows, trace_point, traced_path)

        # 5. 文字标注
        title = Text("傅里叶级数绘制八分音符", font_size=36, color=PURPLE)
        title.to_edge(UP)
        self.add(title)

        info = Text(f"使用 {len(components)} 个分量", font_size=24, color=GRAY_A)
        info.next_to(title, DOWN, buff=0.3)
        self.add(info)

        # 6. 播放动画（固定时间，让系统自动运行）
        # 运行一个周期
        self.wait(CYCLE_TIME)
        # 再保持一小段时间
        self.wait(0.5)
        # 清除所有更新器
        circles.clear_updaters()
        dummy_clock.clear_updaters()
        self.wait(1)