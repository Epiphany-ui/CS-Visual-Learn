from manim import *

class SnowflakeScene(Scene):
    def construct(self):
        # 定义雪花的单个分支
        single_branch = VGroup()

        # 主骨架线
        main_bone = Line(ORIGIN, UP * 3, stroke_width=4, color=WHITE)
        single_branch.add(main_bone)

        # 批量添加侧边的小冰晶分叉（利用循环和镜像坐标）
        for h in [1.0, 1.8, 2.4]:  # 分叉在主干上的不同高度
            scale_factor = (3.0 - h) / 3.0  # 越靠近顶端，分叉越短
            left_sub = Line(
                UP * h, 
                UP * h + LEFT * 0.7 * scale_factor + UP * 0.4 * scale_factor, 
                stroke_width=3, 
                color=WHITE
            )
            right_sub = Line(
                UP * h, 
                UP * h + RIGHT * 0.7 * scale_factor + UP * 0.4 * scale_factor, 
                stroke_width=3, 
                color=WHITE
            )
            single_branch.add(left_sub, right_sub)

        # 创建雪花的六角对称结构
        snowflake_group = VGroup()
        for i in range(6):
            rotated_branch = single_branch.copy()
            rotated_branch.rotate(i * 60 * DEGREES, about_point=ORIGIN)
            snowflake_group.add(rotated_branch)

        # 添加中心冰核
        center_core = RegularPolygon(n=6, radius=0.3, color=BLUE_A, fill_opacity=0.3)
        snowflake_group.add(center_core)

        snowflake_group.move_to(ORIGIN).scale(1.2)

        # 动画：逐层生长入场
        self.play(
            LaggedStart(
                *[Create(branch) for branch in snowflake_group], 
                lag_ratio=0.15
            ), 
            run_time=3
        )

        # 让雪花平滑自转两圈，充满动态呼吸感
        self.play(snowflake_group.animate.rotate(120 * DEGREES), run_time=3, rate_func=linear)
        self.wait(1)