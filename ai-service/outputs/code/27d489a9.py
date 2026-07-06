from manim import *

class UniformAccelerationMotion(Scene):
    def construct(self):
        # 创建一个坐标轴
        axes = Axes(x_range=[-5, 10], y_range=[-5, 20], axis_config={"color": BLUE})
        
        # 创建物体和运动路径
        object = Circle(radius=0.5, color=RED).shift(RIGHT * 2)
        path = DashedVMobject(Line(start=LEFT * 4, end=RIGHT * 8), color=GREEN)
        
        # 添加坐标轴和物体到场景
        self.add(axes, path, object)
        
        # 定义匀加速直线运动的参数
        initial_position = object.get_center()
        acceleration = 1
        time = 5
        
        # 计算最终位置
        final_position = initial_position + acceleration * (time ** 2) / 2 * RIGHT
        
        # 使用 MoveTo 动画将物体移动到最终位置
        self.play(MobjectMoveAlongPath(object, path), run_time=time)