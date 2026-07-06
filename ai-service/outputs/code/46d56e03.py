from manim import *

class RotatingTriangle(Scene):
    def construct(self):
        triangle = RegularPolygon(n=3, fill_color=BLUE, fill_opacity=0.7)
        
        # 使用 updater 来实现匀加速运动
        center = ORIGIN
        radius = 2
        velocity = 1
        acceleration = 0.5
        
        def move_triangle(mob):
            nonlocal velocity
            position = mob.get_center()
            distance_from_center = np.linalg.norm(position - center)
            if distance_from_center < radius:
                velocity += acceleration * dt
                angle_change = velocity * dt
                mob.animate.shift(angle_to_vector(TAU / 3) * angle_change).set_fill(opacity=1).shift(center - position)
        
        triangle.add_updater(move_triangle)
        
        self.play(Create(triangle))
        self.wait(5)
        triangle.clear_updaters()
        self.play(FadeOut(triangle))