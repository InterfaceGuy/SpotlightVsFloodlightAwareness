from manim import *
import numpy as np
import math

RED = "#FF644E"
BLUE = "#00a2ff"

class SineCurveOnCircle(Scene):
    def construct(self):
        
        circle_radius = 3
        
        def sine_curve(theta):
            radius = circle_radius+np.sin(24*theta)/3  # Radius as a function of theta
            return np.array([
                radius * np.sin(theta),
                radius * np.cos(theta),
                0
            ])

        circle = Circle(radius=circle_radius)
        sine_curve_obj = ParametricFunction(
            sine_curve,
            t_range=[-PI, PI, 0.01],
            stroke_width=4,
            color=RED
        )

        self.play(Create(sine_curve_obj, rate_func=linear), run_time=3)
        self.wait()


class TaylorSeriesRadial(Scene):
    def construct(self):
        # Set the range for the x-axis
        x_range = (-48, 48)

        # Set the circle radius
        circle_radius = 2

        # Define the function for the sine curve
        def sine(x):
            return np.sin(x)/4

        # Define the function for the Taylor expansion
        def taylor_expansion(x, n):
            summation = 0
            for i in range(n + 1):
                term = (-1) ** i * x ** (2 * i + 1) / math.factorial(2 * i + 1)
                summation += term
            return summation/4

        # Create axes
        axes = Axes(
            x_range=x_range,
            y_range=(-2, 2),
            x_length=12,
            y_length=6,
            tips=False,
            axis_config={"include_ticks": False},
        )

        # Define the function to wrap the coordinate space around a circle
        def wrap_around_circle(point):
            x, y = point[:2]
            radius = y + circle_radius/2
            angle = x*12
            new_x = radius * np.sin(angle)
            new_y = radius * np.cos(angle)
            return np.array([new_x, new_y, 0])

        # Apply the wrapping transformation to the axes
        wrapped_axes = axes.apply_function(wrap_around_circle)

        # Plot the sine curve
        sine_curve = wrapped_axes.plot(sine, color=RED)

        # Apply the wrapping transformation to the sine curve
        sine_curve = sine_curve.apply_function(wrap_around_circle)

        # Plot the Taylor expansion
        taylor_curve0 = wrapped_axes.plot(lambda x: taylor_expansion(x, 0), color=BLUE).apply_function(wrap_around_circle)
        taylor_curve1 = wrapped_axes.plot(lambda x: taylor_expansion(x, 1), color=BLUE).apply_function(wrap_around_circle)
        taylor_curve2 = wrapped_axes.plot(lambda x: taylor_expansion(x, 2), color=BLUE).apply_function(wrap_around_circle)
        taylor_curve3 = wrapped_axes.plot(lambda x: taylor_expansion(x, 3), color=BLUE).apply_function(wrap_around_circle)
        taylor_curve4 = wrapped_axes.plot(lambda x: taylor_expansion(x, 4), color=BLUE).apply_function(wrap_around_circle)
        taylor_curve5 = wrapped_axes.plot(lambda x: taylor_expansion(x, 5), color=BLUE).apply_function(wrap_around_circle)

        # Remove points outside radius range from taylor curves
        outer_circle = Circle(radius=3/2*circle_radius)
        inner_circle = Circle(radius=circle_radius/2)
        for curve in taylor_curve0, taylor_curve1, taylor_curve2, taylor_curve3, taylor_curve4, taylor_curve5:
            curve.points = [point for point in curve.points if circle_radius/2 <= np.linalg.norm(point[:2]) <= 3/2*circle_radius and point[1]>=0]

        # Animate the plots
        self.add(sine_curve)
        self.play(Create(taylor_curve0), run_time=3)
        self.play(ReplacementTransform(taylor_curve0, taylor_curve1, clone=False), run_time=3/2)
        self.play(ReplacementTransform(taylor_curve1, taylor_curve2, clone=False), run_time=3/2)
        self.play(ReplacementTransform(taylor_curve2, taylor_curve3, clone=False), run_time=3/2)
        self.play(ReplacementTransform(taylor_curve3, taylor_curve4, clone=False), run_time=3/2)
        self.play(ReplacementTransform(taylor_curve4, taylor_curve5, clone=False), run_time=3/2)
        self.wait(2)
