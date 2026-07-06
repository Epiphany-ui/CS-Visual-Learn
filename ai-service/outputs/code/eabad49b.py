from manim import *

class MomentumConservation(Scene):
    def construct(self):
        # 创建两个小球，分别代表不同质量的小球
        ball1 = Circle(radius=0.5, color=BLUE).shift(LEFT * 2)
        ball2 = Circle(radius=0.3, color=RED).shift(RIGHT * 2)

        # 设置初始速度
        ball1.velocity = LEFT * 4
        ball2.velocity = RIGHT * 2

        # 创建轨迹路径
        path1 = TracedPath(ball1.get_center)
        path2 = TracedPath(ball2.get_center)

        # 将轨迹挂载到小球上
        ball1.add_updater(lambda m, dt: m.shift(m.velocity * dt))
        ball2.add_updater(lambda m, dt: m.shift(m.velocity * dt))

        # 添加轨迹路径到场景中
        self.add(path1, path2)

        # 创建初始状态的动画
        self.play(FadeIn(ball1), FadeIn(ball2), run_time=1)

        # 让小球碰撞并交换速度
        ball1.velocity = RIGHT * 4
        ball2.velocity = LEFT * 2

        # 播放碰撞动画
        self.play(self.wait(1))

        # 更新小球的轨迹路径
        path1.clear_points()
        path2.clear_points()

        # 继续播放动画直到运动结束
        self.play(self.wait(3))