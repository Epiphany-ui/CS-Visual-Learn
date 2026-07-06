from manim import *
import numpy as np

class MatrixTransformation(Scene):
    def construct(self):
        # 背景坐标平面
        plane = NumberPlane()
        self.add(plane)

        # 原始正方形顶点（逆时针，z=0）
        orig_points = np.array([
            [-1, -1, 0],
            [1, -1, 0],
            [1, 1, 0],
            [-1, 1, 0]
        ])

        # 创建多边形
        polygon = Polygon(
            orig_points[0], orig_points[1], orig_points[2], orig_points[3],
            color=BLUE, fill_opacity=0.3
        )
        # 顶点标记（使用三维坐标）
        dots = VGroup(*[Dot(orig_points[i], color=RED) for i in range(4)])
        # 矩阵显示（初始为单位矩阵）
        matrix_tex = MathTex(r"\begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}").to_corner(UL)

        # 控制参数：插值因子 0~1
        t = ValueTracker(0.0)
        I = np.eye(2)
        A = np.array([[2, 0], [0, 1]])  # 目标矩阵（横向拉伸）

        # ---- 更新多边形 ----
        def update_polygon(mob, dt):
            val = t.get_value()
            M = (1 - val) * I + val * A
            # 变换顶点：p_new = p_orig @ M.T
            new_points = orig_points.copy()
            new_points[:, :2] = orig_points[:, :2] @ M.T
            mob.set_points_as_corners([new_points[0], new_points[1], new_points[2], new_points[3]])

        # ---- 更新顶点标记 ----
        def update_dots(mob, dt):
            val = t.get_value()
            M = (1 - val) * I + val * A
            for i, dot in enumerate(mob):
                new_pos = M @ orig_points[i, :2]
                dot.move_to([new_pos[0], new_pos[1], 0])

        # ---- 更新矩阵显示 ----
        def update_matrix(mob, dt):
            val = t.get_value()
            M = (1 - val) * I + val * A
            a, b = M[0, 0], M[0, 1]
            c, d = M[1, 0], M[1, 1]
            new_tex = MathTex(
                r"\begin{pmatrix} {:.2f} & {:.2f} \\ {:.2f} & {:.2f} \end{pmatrix}".format(a, b, c, d)
            ).to_corner(UL)
            mob.become(new_tex)

        # 添加更新器
        polygon.add_updater(update_polygon)
        dots.add_updater(update_dots)
        matrix_tex.add_updater(update_matrix)

        # 添加到场景
        self.add(polygon, dots, matrix_tex)

        # 动画：从单位矩阵变换到目标矩阵（3秒）
        self.play(t.animate.set_value(1), run_time=3)
        self.wait(1)

        # 再变换回来（展示可逆性）
        self.play(t.animate.set_value(0), run_time=3)
        self.wait(1)