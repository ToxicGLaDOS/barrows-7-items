from manim import *
from manim.constants import *
from manim import config
import math
from decimal import *
from axis_graph_scene import AxisConfigurableGraphScene

class CDFGraph(AxisConfigurableGraphScene):
    CONFIG = {
        "x_min": 0,
        "x_max": 7,
        "y_min": 0,
        "y_max": 1.0,
        "y_tick_frequency": 0.1,
        "graph_origin": config['bottom'] + config['left_side'] + UP + RIGHT,
        "function_color": RED,
        "axes_color": GREEN,
        "x_labeled_nums": range(0, 7 + 1),
        "y_labeled_nums": [x * 1/10 for x in range(0,10 + 1)],
        "x_axis_config": {

        },
        "y_axis_config": {
            "decimal_number_config": {
                "num_decimal_places": 1,
            }
        }
    }
    def construct(self):
        # Set Decimal precision
        getcontext().prec = 15
        self.setup_axes(animate=True)

        dots = []
        dot_labels = []
        for k in range(0, 7 + 1):
            dot = Dot(self.coords_to_point(k, self.cdf(k)))
            # list() applied to a string turns it into a list of all the characters
            # so this creates the super_precise version of the number where each character is it's own submobject
            dot_label = TexMobject(*list(str(self.cdf(k, super_precise=True))))
            dot_label.scale(.5)
            dot_label.rotate(-np.pi/4, [0, 0, 1])
            dot_label.move_to(dot)
            dot_label.shift(RIGHT * .5)
            dot_labels.append(dot_label)
            dots.append(dot)

        self.play(ShowCreation(VGroup(*dots)))
        self.wait()
        self.play(Write(VGroup(*dot_labels)))
        self.wait()

    def cdf(self, k, N=6, super_precise=False):
        value = sum([choose(N + 1, i) * self.p(N) ** i * (1 - self.p(N)) ** (N + 1 - i) for i in range(math.floor(k + 1))])
        if super_precise:
            return value
        else:
            return float(value)

    def choose(self, n, r):
        f = math.factorial
        return f(n) // f(r) // f(n - r)

    def p(self, N):
        return 1/Decimal(450 - 58 * N)


class InverseCDFGraph(AxisConfigurableGraphScene):
    CONFIG = {
        "x_min": 0,
        "x_max": 7,
        "y_min": 0,
        "y_max": 1.0,
        "y_tick_frequency": 0.1,
        "graph_origin": config['bottom'] + config['left_side'] + UP + RIGHT * 4,
        "axes_color": GREEN,
        "x_labeled_nums": range(0, 7 + 1),
        "y_labeled_nums": [x * 1/10 for x in range(0,10 + 1)],
        "x_axis_config": {

        },
        "y_axis_config": {
            "decimal_number_config": {
                "num_decimal_places": 1,
            }
        }
    }
    def construct(self):
        # Set Decimal precision
        getcontext().prec = 15
        self.setup_axes(animate=True)

        self.dots = []
        self.dot_labels = []
        # List of the (x, y) coords where the dot belongs on the graph
        self.dot_coords = []
        for k in range(0, 7 + 1):
            coord = [k, 1 - self.cdf(k)]
            self.dot_coords.append(coord)
            dot = Dot(self.coords_to_point(*coord))
            # list() applied to a string turns it into a list of all the characters
            # so this creates the super_precise version of the number where each character is it's own submobject
            dot_label = TexMobject(*list(str(Decimal(1) - self.cdf(k, super_precise=True))))
            dot_label.scale(.5)
            dot_label.rotate(-np.pi/4, [0, 0, 1])
            dot_label.move_to(dot)
            dot_label.shift(RIGHT * .5)
            self.dot_labels.append(dot_label)
            self.dots.append(dot)


        self.play(ShowCreation(VGroup(*self.dots)))
        self.wait()
        self.play(Write(VGroup(*self.dot_labels)))
        self.wait()

        zoom_factor = 1
        zoom_label = TextMobject(str(zoom_factor), r"$\times$ zoom")
        zoom_label.move_to(self.x_axis.number_to_point(3.5))
        zoom_label.shift(UP * 3)
        self.play(Write(zoom_label))

        for x in range(14):
            zoom_factor *= 10
            zoom_label_target = TextMobject(str(zoom_factor), r'$\times$ zoom')
            zoom_label_target.move_to(zoom_label)
            y_axis_copy, animations = self.scale_y_axis(0.1, len(str(zoom_factor)))
            self.play(Transform(zoom_label, zoom_label_target), *animations)
            self.y_axis = y_axis_copy
        self.wait()

        zoom_label_target = TextMobject('one hundred trillion', r'$\times$ zoom')
        zoom_label_target.move_to(zoom_label)
        self.play(Transform(zoom_label, zoom_label_target))
        self.wait()

    def scale_y_axis(self, scale_factor, num_decimal_places):
        # Construct a copy of self.y_axis with the labeled numbers scaled to scale_factor
        new_x_min = 0
        new_x_max = self.y_axis.x_max * scale_factor
        y_num_range = float(new_x_max - new_x_min)
        space_unit_to_y = self.y_axis_height / y_num_range
        labeled_numbers = [x * new_x_max / 10 for x in range(0, 11)]
        y_axis_copy = NumberLine(x_max=new_x_max,
                                 x_min=new_x_min,
                                 unit_size=space_unit_to_y,
                                 tick_frequency=new_x_max/10,
                                 numbers_with_elongated_ticks=labeled_numbers,
                                 line_to_number_vect=LEFT,
                                 label_direction=LEFT,
                                 leftmost_tick=new_x_min,
                                 decimal_number_config={
                                     "num_decimal_places": num_decimal_places,
                                 }
                                 )
        y_axis_copy.rotate(np.pi / 2)
        y_axis_copy.shift(self.graph_origin - y_axis_copy.number_to_point(0))
        y_axis_copy.match_style(self.y_axis)
        y_axis_copy.add_numbers(*labeled_numbers)
        y_axis_copy.add(self.y_axis_label_mob)

        # Create the animations that move the dots and labels
        # to the proper point on the scale graph
        animations = []
        for dot, label, coord in zip(self.dots, self.dot_labels, self.dot_coords):
            dot_target = dot.generate_target()
            dot_target.move_to(self.coords_to_point_with_axes(coord[0], coord[1], self.x_axis, y_axis_copy))
            label_target = label.generate_target()
            label_target.move_to(dot_target)
            label_target.shift(RIGHT * .5)
            animations.extend((MoveToTarget(dot), MoveToTarget(label)))

        return y_axis_copy, (ReplacementTransform(self.y_axis, y_axis_copy), *animations)

    def coords_to_point_with_axes(self, x, y, x_axis, y_axis):
        result = x_axis.number_to_point(x)[0] * RIGHT
        result += y_axis.number_to_point(y)[1] * UP
        return result

    def cdf(self, k, N=6, super_precise=False):
        value = sum([choose(N + 1, i) * self.p(N) ** i * (1 - self.p(N)) ** (N + 1 - i) for i in range(math.floor(k + 1))])
        if super_precise:
            return value
        else:
            return float(value)

    def choose(self, n, r):
        f = math.factorial
        return f(n) // f(r) // f(n - r)

    def p(self, N):
        return 1/Decimal(450 - 58 * N)