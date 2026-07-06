from manim import *

class DrawEquilateralTriangle(Scene):
    def construct(self):
        # 定义等边三角形的顶点
        triangle_points = [
            np.array([-1, 0, 0]),
            np.array([1, 0, 0]),
            np.array([0, np.sqrt(3), 0])
        ]
        
        # 创建等边三角形
        equilateral_triangle = Polygon(*triangle_points, color=BLUE).scale(2)
        
        # 添加动画效果
        self.play(Create(equilateral_triangle))
        self.wait(1)