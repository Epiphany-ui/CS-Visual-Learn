from manim import *

class Snowflake(Scene):
    def construct(self):
        # 创建雪花的各个部分
        points = [
            RIGHT * 2,
            LEFT * 2,
            UP * 3,
            DOWN * 3,
            RIGHT * 1.5 + UP * 1,
            RIGHT * 1.5 + DOWN * 1,
            LEFT * 1.5 + UP * 1,
            LEFT * 1.5 + DOWN * 1,
        ]
        
        # 绘制雪花的主体
        snowflake = VGroup(*[Dot(point, radius=0.1) for point in points]).set_color(WHITE)
        
        # 添加动画效果
        self.play(Create(snowflake), run_time=2)