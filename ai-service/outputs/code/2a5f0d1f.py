from manim import *

class DrawEquilateralTriangle(Scene):
    def construct(self):
        # 创建一个等边三角形
        triangle = Polygon(
            np.array([0, 1.732/3, 0]), 
            np.array([-1, -1.732/6, 0]), 
            np.array([1, -1.732/6, 0]),
            color=BLUE,
            fill_opacity=0.5
        )
        
        # 将三角形添加到场景中并播放动画
        self.play(Create(triangle), run_time=2)
        self.wait(1)