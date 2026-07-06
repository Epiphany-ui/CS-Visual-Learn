from manim import *

class MomentumConservation(Scene):
    def construct(self):
        # 标题
        title = Text("动量守恒", color=WHITE, font_size=48).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # 定义参数
        r = 0.3                      # 小球半径
        v_scale = 1.5               # 箭头速度标度

        # 创建两个小球
        ball1 = Circle(radius=r, color=RED, fill_opacity=1).move_to(LEFT * 3)
        ball2 = Circle(radius=r, color=BLUE, fill_opacity=1).move_to(ORIGIN)

        # 质量标签
        m1_label = MathTex("m_1", color=RED).next_to(ball1, DOWN)
        m2_label = MathTex("m_2", color=BLUE).next_to(ball2, DOWN)

        # 初始动量箭头（ball1运动，ball2静止）
        arrow1_init = Arrow(
            ball1.get_center(),
            ball1.get_center() + RIGHT * v_scale,
            color=YELLOW, buff=0
        )
        arrow2_init = Arrow(
            ball2.get_center(),
            ball2.get_center() + RIGHT * 0.01,   # 几乎为零长度，视觉上看不见
            color=YELLOW, buff=0
        )
        # 为后续变换保留引用
        arrow1 = arrow1_init
        arrow2 = arrow2_init

        # 组合初始画面
        initial_group = VGroup(ball1, ball2, m1_label, m2_label, arrow1, arrow2)
        self.play(Create(initial_group))
        self.wait(0.5)

        # 显示动量公式（将中文“初”、“末”改为英文以避免LaTeX编译错误）
        formula = MathTex(r"\vec{p}_{\text{initial}} = m_1 \vec{v} = \vec{p}_{\text{final}} = m_2 \vec{v}'",
                          color=WHITE).next_to(initial_group, DOWN, buff=0.8)
        self.play(Write(formula))
        self.wait(1)

        # ---------- 碰撞前 ----------
        # ball1 向右移动至刚好接触 ball2（球心距 = 2r）
        contact_x = -2 * r   # ball2中心在0，接触时ball1中心在 -0.6
        delta1 = contact_x - ball1.get_center()[0]
        self.play(
            ball1.animate.shift(RIGHT * delta1),
            arrow1.animate.shift(RIGHT * delta1),       # 箭头随球移动
            m1_label.animate.next_to(ball1, DOWN),
            run_time=1.5,
            rate_func=linear
        )
        self.wait(0.3)

        # ---------- 碰撞后 ----------
        # ball1 停止在接触点，ball2 获得速度向右移动
        # 同时箭头变换：ball1箭头缩至零，ball2箭头伸长
        target_x_ball2 = RIGHT * 3
        target_arrow1 = Arrow(
            ball1.get_center(),
            ball1.get_center() + RIGHT * 0.01,
            color=YELLOW, buff=0
        )
        target_arrow2 = Arrow(
            ball2.get_center(),
            ball2.get_center() + RIGHT * v_scale,
            color=YELLOW, buff=0
        )
        # 更新标签位置
        new_m2_label = m2_label.copy().next_to(target_x_ball2, DOWN)

        self.play(
            ball2.animate.move_to(target_x_ball2),
            Transform(arrow1, target_arrow1),          # ball1箭头消失
            Transform(arrow2, target_arrow2),          # ball2箭头出现
            Transform(m2_label, new_m2_label),
            run_time=1.5,
            rate_func=linear
        )
        self.wait(0.5)

        # 显示动量守恒结论
        conclusion = Text("总动量保持不变", color=GREEN, font_size=36).next_to(formula, DOWN, buff=0.5)
        self.play(Write(conclusion))
        self.wait(2)