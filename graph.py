from manim import *
from manim.constants import *
from manim import config
import math
from decimal import *
from axis_graph_scene import AxisConfigurableGraphScene
from sci_formatter import formatter
from shared_functions import *

def align_label(label, dot):
    label.move_to(dot)
    label.shift(RIGHT * .5)


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
        "y_labeled_nums": [x * 1/10 for x in range(0, 10 + 1)],
        "x_axis_config": {

        },
        "y_axis_config": {
            "decimal_number_config": {
                "num_decimal_places": 1,
            }
        }
    }

    def initialize(self):
        # Set Decimal precision
        getcontext().prec = 15
        self.setup_axes(animate=True)

    def create_dots(self):
        self.dots = []
        self.dot_labels = []
        self.dot_coords = []
        for k in range(0, 7 + 1):
            coord = [k, cdf(k)]
            self.dot_coords.append(coord)
            dot = Dot(self.coords_to_point(*coord))
            self.dots.append(dot)

            dot_label = TexMobject(str(cdf(k, super_precise=True)))
            dot_label.scale(.5)
            dot_label.rotate(-np.pi / 4, [0, 0, 1])
            align_label(dot_label, dot)
            self.dot_labels.append(dot_label)

        self.play(ShowCreation(VGroup(*self.dots)))
        self.wait()

        self.play(Write(VGroup(*self.dot_labels)))
        self.wait()

    def become_inverse_graph(self):
        # List of the (x, y) coords where the dot belongs on the graph
        self.dot_coords = []
        animations = []
        for index, (dot, label) in enumerate(zip(self.dots, self.dot_labels)):
            coord = [index, inverse_cdf(index)]
            self.dot_coords.append(coord)
            dot_target = dot.generate_target()
            dot_target.move_to(self.coords_to_point_with_axes(coord[0], coord[1], self.x_axis, self.y_axis))
            # If this is in scientific notation then we expand it to decimal
            value = str(inverse_cdf(index, super_precise=True))
            if formatter.is_sci_form(value):
                value = formatter.build_number_string_from_sci_form(value)
            label_target = TexMobject(value)
            label_target.scale(.5)
            label_target.rotate(-np.pi / 4, [0, 0, 1])
            align_label(label_target, dot_target)
            animations.extend((MoveToTarget(dot), Transform(label, label_target)))
        self.play(*animations)
        self.wait()

    def round_labels(self):
        animations = []
        for index, (dot, label) in enumerate(zip(self.dots, self.dot_labels)):
            full_prec = cdf(index, super_precise=True)
            value = self.round_to_nines(full_prec)
            label_target = TexMobject(value)
            label_target.scale(.5)
            label_target.rotate(-np.pi / 4, [0, 0, 1])
            align_label(label_target, dot)
            animations.append(Transform(label, label_target))
        self.play(*animations)
        self.wait()

    def repeated_zoom(self):
        x_min = 0.9
        zoom_factor = 1
        zoom_label = TextMobject(str(zoom_factor), r"$\times$ zoom")
        zoom_label.move_to(self.x_axis.number_to_point(3.5))
        zoom_label.shift(UP * 3)
        self.play(Write(zoom_label))

        for x in range(1, 15):
            zoom_factor *= 10
            zoom_label_target = TextMobject(str(zoom_factor), r'$\times$ zoom')
            zoom_label_target.move_to(zoom_label)
            y_axis_copy = self.scale_y_axis(x_min, 1, len(str(zoom_factor)))
            animations = self.move_dots_to_new_y_axis(y_axis_copy)
            x_min += (0.9 / zoom_factor)
            self.play(Transform(zoom_label, zoom_label_target), *animations)
            self.y_axis = y_axis_copy
        self.wait()

        zoom_label_target = TextMobject('one hundred trillion', r'$\times$ zoom')
        zoom_label_target.move_to(zoom_label)
        self.play(Transform(zoom_label, zoom_label_target))
        self.wait()

        self.play(FadeOut(zoom_label))
        self.wait()

    def scale_back_down(self):
        y_axis_copy = self.scale_y_axis(0, 1, 1)

        animations = []
        # Just move the offscreen ones
        for (dot, label) in zip(self.dots[:6], self.dot_labels[:6]):
            # Move dots to just above the screen because they're all so high up at this point
            # that if we interpolated them to the correct spot then they would just appear to teleport here
            dot.move_to([0, -8, 0])
            align_label(label, dot)

        for dot, label, coord in zip(self.dots, self.dot_labels, self.dot_coords):
            dot_target = dot.generate_target()
            label_target = label.generate_target()
            point = self.coords_to_point_with_axes(coord[0], coord[1], self.x_axis, y_axis_copy)

            dot_target.move_to(point)
            align_label(label_target, dot_target)

            animations.extend((MoveToTarget(dot), MoveToTarget(label)))

        self.play(ReplacementTransform(self.y_axis, y_axis_copy), *animations)
        self.y_axis = y_axis_copy
        self.wait()

    def example_usage(self):
        shift_graph_animations = self.shift_graph((-3.3, 0, 0))
        self.play(*shift_graph_animations)
        self.wait()

        how_does_this_work = TextMobject("But how does this graph help us?")
        self.play(Write(how_does_this_work))
        self.wait()

        self.play(FadeOut(how_does_this_work))
        self.wait()

        cdf_x = TextMobject("$cdf($", "$x$", "$) = $ The odds of getting ", "x", " or less successes (drops)")
        self.play(Write(cdf_x))
        self.wait()

        cdf_function   = TextMobject("$cdf($", "$0$", "$) = $ The odds of getting ", "0", " or less drops")
        self.play(ReplacementTransform(cdf_x, cdf_function))

        for x in range(4):
            new_cdf = TextMobject("$cdf($", f"${str(x)}$", "$) = $ The odds of getting ", str(x), " or less drops")
            self.play(Transform(cdf_function, new_cdf))

        and_so_on = TextMobject("and so on...")
        and_so_on.shift(DOWN)
        self.play(FadeIn(and_so_on))
        self.wait()

        self.play(FadeOut(cdf_function), FadeOut(and_so_on))
        self.wait()

        with_that_we_can = TextMobject("We can calculate more complex probabilities as well!")
        self.play(Write(with_that_we_can))
        self.wait()

        self.play(FadeOut(with_that_we_can))
        self.wait()

        subtraction_1 = TextMobject("$cdf(5) - cdf(3) = $")
        subtraction_2 = TextMobject("The chance of getting 5 or less drops")
        subtraction_3 = TextMobject("minus")
        subtraction_4 = TextMobject("the chance of getting 3 or less drops")
        which_means = TextMobject("which is the chance of getting 4-5 drops.")
        subtraction_1.shift(UP*2)
        subtraction_2.shift(UP*1)
        #subtraction_3.shift()
        subtraction_4.shift(DOWN*1)
        which_means.shift(DOWN*2)

        subtraction_group = VGroup(subtraction_1, subtraction_2, subtraction_3, subtraction_4, which_means)

        self.play(Write(subtraction_1))
        self.play(Write(subtraction_2))
        self.play(Write(subtraction_3))
        self.play(Write(subtraction_4))
        self.wait()

        self.play(Write(which_means))
        self.wait()

        self.play(FadeOut(subtraction_group))
        self.wait()

        cdf_5 = TexMobject(str(self.round_to_nines(cdf(5))))
        minus = TexMobject('-')
        cdf_3 = TexMobject(str(self.round_to_nines(cdf(3))))
        equals = TexMobject('=')
        five_minus_three = cdf(5) - cdf(3)
        five_minus_three_string = f'{five_minus_three:.8g}'
        if formatter.is_sci_form(five_minus_three_string):
            five_minus_three_string = formatter.build_number_string_from_sci_form(five_minus_three_string)


        result = TexMobject(five_minus_three_string)
        concrete_example_group = VGroup(cdf_5, minus, cdf_3, equals, result)
        concrete_example_group.arrange()

        self.play(Write(concrete_example_group))
        self.wait()

        percentage = five_minus_three * 100
        percentage_string = f'{percentage:.6g}'
        if formatter.is_sci_form(percentage_string):
            percentage_string = formatter.build_number_string_from_sci_form(percentage_string)

        result_target = TexMobject(f'{percentage_string}', "\%")
        target_group = VGroup(cdf_5, minus, cdf_3, equals, result_target)
        result_target.next_to(equals)

        self.play(Transform(concrete_example_group, target_group))
        self.wait()

        self.play(FadeOut(concrete_example_group))
        self.wait()

        but_why = TextMobject("But why?")
        self.play(Write(but_why))
        self.wait()
        self.play(FadeOut(but_why))
        self.wait()
        number_colors = {'5': BLUE,
                         '4': BLUE,
                         '3': RED,
                         '2': RED,
                         '1': RED,
                         '0': RED}
        cdf_5_expanded = VGroup(TexMobject("cdf(5)="),
                                TextMobject(r"The odds of getting 5, 4, 3, 2, 1, or 0 drops", tex_to_color_map=number_colors))
        cdf_5_expanded.arrange(center=False)
        cdf_3_expanded = VGroup(TexMobject("cdf(3)="),
                                TextMobject("The odds of getting 3, 2, 1, or 0 drops", tex_to_color_map=number_colors))
        cdf_3_expanded.arrange(center=False)
        cdf_5_minus_cdf_3_expanded = VGroup(TexMobject("cdf(5) - cdf(3)="),
                                            TextMobject("The odds of getting 5 or 4 drops", tex_to_color_map=number_colors))
        cdf_5_minus_cdf_3_expanded.arrange(center=False)

        expanded_group = VGroup(cdf_5_expanded, cdf_3_expanded, cdf_5_minus_cdf_3_expanded)
        expanded_group.arrange(DOWN)

        self.play(Write(cdf_5_expanded))
        self.play(Write(cdf_3_expanded))
        self.play(Write(cdf_5_minus_cdf_3_expanded))
        self.wait()

        self.play(FadeOut(expanded_group))
        self.wait()

        cdf_7 = TexMobject("cdf(7)")
        cdf_6 = TexMobject("cdf(6)")
        minus = TexMobject("-")
        equals = TexMobject("=")
        left_minus = minus.copy()
        cdf_7_value = TexMobject(str(cdf(7)))
        cdf_6_value = TexMobject(str(cdf(6)))
        value = str(round(cdf(7) - cdf(6), 15))
        if formatter.is_sci_form(value):
            value = formatter.build_number_string_from_sci_form(value)
        cdf_7_minus_cdf_6_value = TexMobject(value)
        rhs = VGroup(cdf_7_value, minus, cdf_6_value)
        rhs.arrange()
        drop_chance_7 = VGroup(cdf_7, left_minus, cdf_6, equals, rhs)
        drop_chance_7.arrange()

        self.play(Write(drop_chance_7))
        self.wait()

        drop_chance_7_target = VGroup(*[tex.copy() for tex in drop_chance_7[:-1]], cdf_7_minus_cdf_6_value)
        drop_chance_7_target.arrange()
        self.play(Transform(drop_chance_7, drop_chance_7_target))
        self.wait()


        shift_graph_animations = self.shift_graph((3.3, 0, 0))
        self.play(*shift_graph_animations)
        self.wait()

    def construct(self):
        self.initialize()
        self.create_dots()
        #self.become_inverse_graph()
        self.round_labels()
        self.repeated_zoom()
        self.scale_back_down()
        self.example_usage()

    def shift_graph(self, by):
        x_target = self.x_axis.generate_target()
        y_target = self.y_axis.generate_target()
        x_target.shift(by)
        y_target.shift(by)
        animations = []
        animations.extend((MoveToTarget(self.x_axis), MoveToTarget(self.y_axis)))

        for dot, label in zip(self.dots, self.dot_labels):
            dot_target = dot.generate_target()
            dot_target.shift(by)
            label_target = label.generate_target()
            align_label(label_target, dot_target)
            animations.extend((MoveToTarget(dot), MoveToTarget(label)))

        return animations

    def move_dots_to_new_y_axis(self, y_axis):
        # Create the animations that move the dots and labels
        # to the proper point on the scale graph
        animations = []
        for dot, label, coord in zip(self.dots, self.dot_labels, self.dot_coords):
            dot_target = dot.generate_target()
            dot_target.move_to(self.coords_to_point_with_axes(coord[0], coord[1], self.x_axis, y_axis))
            label_target = label.generate_target()
            align_label(label_target, dot_target)
            animations.extend(
                (MoveToTarget(dot),
                 MoveToTarget(label))
            )

        return (ReplacementTransform(self.y_axis, y_axis), *animations)

    def scale_y_axis(self, new_min, new_max, num_decimal_places):
        # Construct a copy of self.y_axis with the labeled numbers scaled to scale_factor
        new_x_min = new_min
        new_x_max = new_max
        y_num_range = float(new_x_max - new_x_min)
        space_unit_to_y = self.y_axis_height / y_num_range
        labeled_numbers = [new_x_min + y_num_range / 10 * x for x in range(0, 11)]
        y_axis_copy = NumberLine(x_max=new_x_max,
                                 x_min=new_x_min,
                                 unit_size=space_unit_to_y,
                                 tick_frequency=y_num_range/10,
                                 numbers_with_elongated_ticks=labeled_numbers,
                                 line_to_number_vect=LEFT,
                                 label_direction=LEFT,
                                 leftmost_tick=new_x_min,
                                 decimal_number_config={
                                     "num_decimal_places": num_decimal_places,
                                 }
                                 )
        y_axis_copy.rotate(np.pi / 2)
        y_axis_copy.shift(self.graph_origin - y_axis_copy.number_to_point(new_x_min))
        y_axis_copy.match_style(self.y_axis)
        y_axis_copy.add_numbers(*labeled_numbers)
        y_axis_copy.add(self.y_axis_label_mob)

        return y_axis_copy

    def round_to_nines(self, number):
        if number >= 1 or number <= -1:
            return number
            #raise ValueError(f"round_to_nines only accepts numbers between -1-1 ya ding dong. Got {number}")

        s = str(number)
        dot_at = s.index('.')
        num_nines = 0
        for char in s[dot_at+1:]:
            if char == '9':
                num_nines += 1
            else:
                break

        s = s[:dot_at + num_nines + 3]

        return s

    def coords_to_point_with_axes(self, x, y, x_axis, y_axis):
        result = x_axis.number_to_point(x)[0] * RIGHT
        result += y_axis.number_to_point(y)[1] * UP
        return result


