from manim import *

class AcceleratingMotion(Scene):
    def construct(self):
        axes = Axes(
            x_range=[0, 10],
            y_range=[-5, 5],
            axis_config={"color": WHITE},
        ).shift(UP * 2)

        graph = axes.plot(lambda t: -t**2 + 4*t - 3, color=BLUE)

        label_graph = axes.get_graph_label(
            graph,
            label="s(t) = -t^2 + 4t - 3",
            direction=UL,
            buff=0.5
        )

        origin = Dot().shift(DOWN * 2)
        velocity_vector = Vector(RIGHT, color=RED).next_to(origin, RIGHT)

        self.play(Create(axes), Create(label_graph))
        self.wait(1)
        self.play(Create(graph))
        self.wait(1)
        self.play(FadeIn(origin))
        self.wait(1)
        self.play(Create(velocity_vector))
        self.wait(2)

        # Animation of the particle moving along the curve
        def particle_updater(particle, dt):
            t = axes.x_axis.number_to_point(particle.get_center())[0]
            new_y = -t**2 + 4*t - 3
            particle.move_to(axes.c2p(t, new_y))

        particle = Dot().set_color(GREEN)
        self.add(particle)

        particle.add_updater(particle_updater)
        self.play(self.camera.animate.set_center_of_mass(ORIGIN), run_time=10, rate_func=linear)
        self.remove(particle)