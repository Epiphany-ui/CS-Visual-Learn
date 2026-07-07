import numpy as np
from manim import *

class FractalCurve(Scene):
    def construct(self):
        # 参数设置
        max_iter = 4          # 最大迭代次数
        start = np.array([-4.0, 0.0, 0.0])
        end = np.array([4.0, 0.0, 0.0])

        # 坐标轴
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-1, 1, 0.5],
            x_length=10,
            y_length=4,
            axis_config={"color": BLUE, "include_numbers": True}
        )
        axes.shift(DOWN * 0.5)   # 向下移动一点，给文字留空间
        self.add(axes)

        # 坐标轴标签
        x_label = axes.get_x_axis_label(Text("x"))
        y_label = axes.get_y_axis_label(Text("y"))
        self.add(x_label, y_label)

        # 预计算所有迭代的点列表
        points_by_iter = []
        for n in range(max_iter + 1):
            pts = self._koch_points(start, end, n)
            points_by_iter.append(pts)

        # 当前迭代次数跟踪器
        iter_tracker = ValueTracker(0)

        # 分形曲线对象
        curve = VMobject(stroke_color=YELLOW, stroke_width=3)
        curve.add_updater(lambda mob, dt: self._update_curve(mob, iter_tracker, points_by_iter))
        self.add(curve)

        # 迭代次数文字标注
        iter_text = Text("Iteration: 0", font_size=36, color=WHITE)
        iter_text.next_to(axes, UP, buff=0.5)
        iter_text.add_updater(lambda mob, dt: mob.set_text(f"Iteration: {int(iter_tracker.get_value())}"))
        self.add(iter_text)

        # 动画：逐步增加迭代次数
        self.wait(1)
        for i in range(1, max_iter + 1):
            self.play(iter_tracker.animate.set_value(i), run_time=1.5)
        self.wait(2)

    def _koch_points(self, p1, p2, n):
        """递归生成科赫曲线点列表（迭代n次，返回顺序点集）"""
        if n == 0:
            return [p1, p2]

        # 计算五个控制点
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        length = np.sqrt(dx**2 + dy**2) / 3.0
        angle = np.arctan2(dy, dx)

        # 第一个三等分点
        a = np.array([p1[0] + dx/3, p1[1] + dy/3, 0])
        # 第二个三等分点
        b = np.array([p1[0] + 2*dx/3, p1[1] + 2*dy/3, 0])
        # 凸起点（旋转60度）
        cx = a[0] + length * np.cos(angle + np.pi/3)
        cy = a[1] + length * np.sin(angle + np.pi/3)
        c = np.array([cx, cy, 0])

        # 递归拼接四段
        pts1 = self._koch_points(p1, a, n-1)
        pts2 = self._koch_points(a, c, n-1)
        pts3 = self._koch_points(c, b, n-1)
        pts4 = self._koch_points(b, p2, n-1)
        # 去除重复端点（除第一个点外，每段的第一个点与前一段最后一个点重复）
        return pts1[:-1] + pts2[:-1] + pts3[:-1] + pts4

    def _update_curve(self, mob, tracker, points_by_iter):
        """更新折线点集"""
        n = int(tracker.get_value())
        pts = points_by_iter[n]
        # 转换为二维点（Manim点集要求每个点是三维数组，但可以用二维数组）
        points_array = np.array(pts)
        mob.set_points_as_corners(points_array)