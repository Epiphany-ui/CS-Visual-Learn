from manim import *

class CircularMotion(Scene):
    def construct(self):
        circle = Circle(radius=1, color=BLUE)
        dot = Dot(radius=0.05, color=RED).shift(RIGHT)

        # Create the circle and dot
        self.play(Create(circle), FadeIn(dot))

        # Define the updater function for the dot to move in a circular path
        def update_dot(mob, dt):
            angle = mob.time * 2 * PI
            x = np.cos(angle)
            y = np.sin(angle)
            mob.shift(RIGHT - mob.get_center()).shift(x * RIGHT + y * UP)
            mob.time += dt

        dot.add_updater(update_dot)
        dot.time = 0

        # Wait for the animation to complete
        self.wait(5)