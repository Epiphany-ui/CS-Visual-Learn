from manim import *

class ComplexMapping(Scene):
    def construct(self):
        # 创建两个复平面，并排摆放
        left_plane = ComplexPlane(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            background_line_style={
                "stroke_color": BLUE_D,
                "stroke_width": 1,
                "stroke_opacity": 0.5
            }
        ).scale(0.8).shift(LEFT * 3.5)
        left_plane.add_coordinates()
        left_label = Text("z-plane").next_to(left_plane, UP)

        right_plane = ComplexPlane(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            background_line_style={
                "stroke_color": BLUE_D,
                "stroke_width": 1,
                "stroke_opacity": 0.5
            }
        ).scale(0.8).shift(RIGHT * 3.5)
        right_plane.add_coordinates()
        right_label = Text("w-plane").next_to(right_plane, UP)

        # 显示函数表达式
        func_text = MathTex("w = z^2").scale(0.8).to_edge(UP)

        # 控制角度
        angle = ValueTracker(0)

        # 左平面的点 (z = e^{iθ})
        z_dot = Dot(
            left_plane.n2p(complex(1, 0)),
            color=YELLOW
        )
        z_label = MathTex("z", color=YELLOW).scale(0.7).next_to(z_dot, UR, 0.1)

        # 右平面的对应点 (w = z^2)
        w_dot = Dot(
            right_plane.n2p(complex(1, 0)),
            color=ORANGE
        )
        w_label = MathTex("w", color=ORANGE).scale(0.7).next_to(w_dot, UR, 0.1)

        # 轨迹线追踪w点的路径
        trace = TracedPath(w_dot.get_center, stroke_color=ORANGE, stroke_width=2)

        # 更新函数
        def update_z_dot(mob, dt):
            theta = angle.get_value()
            z = complex(np.cos(theta), np.sin(theta))
            mob.move_to(left_plane.n2p(z))

        def update_w_dot(mob, dt):
            theta = angle.get_value()
            z = complex(np.cos(theta), np.sin(theta))
            w = z ** 2
            mob.move_to(right_plane.n2p(w))

        def update_labels(mob, dt):
            z_dot_center = z_dot.get_center()
            z_label.next_to(z_dot_center, UR, 0.1)
            w_dot_center = w_dot.get_center()
            w_label.next_to(w_dot_center, UR, 0.1)

        z_dot.add_updater(update_z_dot)
        w_dot.add_updater(update_w_dot)
        z_label.add_updater(update_labels)
        w_label.add_updater(update_labels)

        # 构建场景
        self.add(left_plane, left_label, right_plane, right_label, func_text)
        self.add(z_dot, w_dot, z_label, w_label, trace)

        # 播放动画：角度从0到2π
        self.play(
            angle.animate.set_value(2 * PI),
            rate_func=smooth,
            run_time=12
        )
        self.wait(2)