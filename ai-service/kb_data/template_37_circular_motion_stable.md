from manim import *

class CircularMotion(Scene):
    def construct(self):
        circle = Circle(radius=2, color=BLUE)
        dot = Dot(color=RED, radius=0.2)
        
        # 🌟 关键点：使用 ValueTracker 来替代 mob.time，这是绝对安全的
        angle_tracker = ValueTracker(0)

        # 挂载更新器：只读取追踪器的值，不修改任何 mob 的动态属性
        dot.add_updater(lambda m: m.move_to(
            circle.get_center() + 2 * np.array([
                np.cos(angle_tracker.get_value()), 
                np.sin(angle_tracker.get_value()), 
                0
            ])
        ))

        self.play(Create(circle), Create(dot))
        
        # 🌟 通过控制追踪器来实现动画，这里极其稳定
        # 从 0 旋转到 2*PI（一圈），速度匀速
        self.play(angle_tracker.animate.set_value(2 * PI), run_time=5, rate_func=linear)
        
        dot.clear_updaters()
        self.wait(1)