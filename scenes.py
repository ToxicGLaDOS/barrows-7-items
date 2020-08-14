#!/usr/bin/env python

from manim import *

class Definitions(Scene):
    def construct(self):
        # Set up the text for the definitions of I and N
        i_def = TexMobject("I", r" = \textrm{getting a barrows item}")
        n_def = TexMobject("N", r" = \textrm{the number of barrows brothers killed}")
        i_def.set_color(RED_A)
        n_def.set_color(BLUE_A)

        # Create equals text
        equals = TexMobject(r"=")

        # Create probability_function P(I|N)
        probability_function = TexMobject("P", "(", "I", "|", "N", ")")
        probability_function[0].set_color(YELLOW_A)
        probability_function[2].set_color(i_def.get_color())
        probability_function[4].set_color(n_def.get_color())

        # Create worded version of probability_function
        probability_function_worded_p1 = TextMobject(r"The probability of ", "getting a barrows item ", "given ")
        probability_function_worded_p2 = TextMobject(r"the number of barrows brothers killed")
        probability_function_worded_p2.next_to(probability_function_worded_p1, DOWN)
        probability_function_worded_p1[0].set_color(probability_function[0].get_color())
        probability_function_worded_p1[1].set_color(i_def.get_color())
        probability_function_worded_p2.set_color(n_def.get_color())

        # Create group of worded version 1 and 2
        probability_function_worded = VGroup(probability_function_worded_p1, probability_function_worded_p2)

        # Create target for probability_function_worded to move to
        probability_function_worded_target = probability_function_worded.generate_target()

        # Position inital text
        probability_function_worded_target.shift(UP * 3)
        i_def.shift(UP)
        n_def.shift(DOWN)
        equals.next_to(probability_function, RIGHT)

        # Draw the initial text
        self.play(Write(probability_function_worded))
        self.wait()

        # Move probability_function_worded up and create i_def and n_def out of the worded version
        self.play(MoveToTarget(probability_function_worded))
        p1_copy = probability_function_worded_p1[1].copy()
        p2_copy = probability_function_worded_p2[0].copy()
        self.play(Transform(p1_copy, i_def))
        self.play(Transform(p2_copy, n_def))
        self.wait()

        # Fade out worded function and move i_def and n_def up
        self.add(i_def, n_def)
        self.remove(p1_copy, p2_copy)
        self.play(FadeOut(probability_function_worded))
        i_def.generate_target().shift(UP * 2)
        n_def.generate_target().shift(UP * 3)
        self.play(MoveToTarget(i_def), MoveToTarget(n_def))
        self.wait()

        # Create probability_function from definitions
        # and show it equal to worded version
        probability_function_worded.next_to(equals, RIGHT)
        probability_function_group = VGroup(probability_function, equals, probability_function_worded)
        probability_function_group.move_to([0, 0, 0])
        i_copy = i_def[0].copy()
        i_copy.generate_target().move_to(probability_function[2])
        n_copy = n_def[0].copy()
        n_copy.generate_target().move_to(probability_function[4])
        self.play(FadeIn(probability_function[0]),
                  FadeIn(probability_function[1]),
                  FadeIn(probability_function[3]),
                  FadeIn(probability_function[5]),
                  MoveToTarget(i_copy),
                  MoveToTarget(n_copy))
        self.play(Write(equals), Write(probability_function_worded))
        self.wait()
        # Cut in wiki page for barrows here

class Equation(Scene):
    def construct(self):
        # Create the probability_function P(I|N)
        probability_function = TexMobject("P", "(", "I", "|", "N", ")")
        probability_function[0].set_color(YELLOW_A)
        probability_function[2].set_color(RED_A)
        probability_function[4].set_color(BLUE_A)

        # Create the equals sign
        equals = TexMobject(r"=")
        equals.next_to(probability_function, RIGHT)

        # Create the worded version of the probability_function
        probability_function_worded_p1 = TextMobject(r"The probability of ", "getting a barrows item ", "given ")
        probability_function_worded_p2 = TextMobject(r"the number of barrows brothers killed")
        probability_function_worded_p1[0].set_color(probability_function[0].get_color())
        probability_function_worded_p1[1].set_color(probability_function[2].get_color())
        probability_function_worded_p2.set_color(probability_function[4].get_color())
        probability_function_worded_p2.next_to(probability_function_worded_p1, DOWN)
        probability_function_worded = VGroup(probability_function_worded_p1, probability_function_worded_p2)
        probability_function_worded.next_to(equals, RIGHT)
        probability_function_group = VGroup(probability_function, equals, probability_function_worded)
        probability_function_group.move_to(ORIGIN)

        # Start with P(I|N) = probability_function_worded on the screen
        self.add(probability_function_group)
        self.wait()

        #self.add(equation)
        probability_equation = TexMobject(r"\frac{1}{450-58\times", "N", "}")
        probability_equation.next_to(equals, RIGHT)

        # Create a target to center the equation
        probability_equation_group = VGroup(probability_function, equals, probability_equation)

        # Copy the equation group for positioning
        probability_equation_group_2 = probability_equation_group.copy()
        probability_equation_group_2.move_to(ORIGIN)
        # Generate targets for the probability_function, equals and probability_equation and move the targets
        # to where they will be when the whole equation is centered
        probability_function.generate_target().move_to(probability_equation_group_2[0])
        equals.generate_target().move_to(probability_equation_group_2[1])
        prob_worded_transform_target = probability_equation_group_2[2]

        # Move the probability equation to where it's supposed to be when centered
        probability_equation.move_to(prob_worded_transform_target)

        # Turn the probability_function_worded into the real function from the wiki
        # and slide stuff around to be centered
        self.play(Transform(probability_function_worded, prob_worded_transform_target), MoveToTarget(probability_function), MoveToTarget(equals))
        self.remove(probability_function_worded)
        self.add(probability_equation)
        self.wait()

        # Define the equation for item drops per roll
        equation = TexMobject(r"\left(", r"{\frac{1}{450-58\times", "N", r"}}\right)^x")
        equation.next_to(equals, RIGHT)

        # Generate a target for where probability_equation needs to move to
        # so it can be in place for when we add the brackets
        probability_equation.generate_target().move_to(VGroup(equation[1], equation[2]))

        # Move the probability_equation over to make room for the brackets
        # and fade in the brackets and exponent
        self.play(MoveToTarget(probability_equation))
        self.play(FadeIn(equation[0]), FadeIn(equation[3]))
        self.remove(probability_equation)
        self.add(equation)
        self.wait()

        # Create function f(x,N) and position it to where probability_function, P(I|N), is now
        function = TexMobject(r"f(x,N)")
        function.move_to(probability_function)

        # Turn probability_function into function
        self.play(Transform(probability_function, function))
        self.wait()

