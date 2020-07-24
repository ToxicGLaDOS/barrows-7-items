#!/usr/bin/env python

from manimlib.imports import *

class Definitions(Scene):
    def construct(self):
        # Set up the text
        i_def = TexMobject("I", r" = \textrm{getting a barrows item}")
        n_def = TexMobject("N", r" = \textrm{the number of barrows brothers killed}")
        i_def.set_color(RED_A)
        n_def.set_color(BLUE_A)
        n = n_def[0]
        equation = TexMobject(r"f(x,N) = {(\frac{1}{450-58\times", "N", "}})^x")
        equals = TexMobject(r"=")
        probabilty_function = TexMobject("P", "(", "I", "|", "N", ")")
        probabilty_function[0].set_color(YELLOW_A)
        probabilty_function[2].set_color(i_def.get_color())
        probabilty_function[4].set_color(n_def.get_color())

        probabilty_function_worded_p1 = TextMobject(r"The probability of ", "getting a barrows item ", "given ")
        probabilty_function_worded_p2 = TextMobject(r"the number of barrows brothers killed")

        probabilty_function_worded_p2.next_to(probabilty_function_worded_p1, DOWN)

        probabilty_function_worded = VGroup(probabilty_function_worded_p1, probabilty_function_worded_p2)
        probabilty_function_worded_p1[0].set_color(probabilty_function[0].get_color())
        probabilty_function_worded_p1[1].set_color(i_def.get_color())
        probabilty_function_worded_p2.set_color(n_def.get_color())

        probabilty_function_worded_target = probabilty_function_worded.generate_target()

        # Position text
        probabilty_function_worded_target.shift(UP * 3)
        i_def.shift(UP)
        n_def.shift(DOWN)
        probabilty_function.move_to([-5, 0, 0])
        equals.next_to(probabilty_function, RIGHT)

        # Copy n and set a target for it
        n_copy = n.deepcopy()
        target_n = n_copy.generate_target()
        target_n.move_to(equation[1])

        self.play(Write(probabilty_function_worded))
        self.wait()

        self.play(MoveToTarget(probabilty_function_worded))
        p1_copy = probabilty_function_worded_p1[1].copy()
        p2_copy = probabilty_function_worded_p2[0].copy()
        self.play(Transform(p1_copy, i_def))
        self.play(Transform(p2_copy, n_def))
        self.wait()

        self.add(i_def, n_def)
        self.remove(p1_copy, p2_copy)
        self.play(FadeOut(probabilty_function_worded))
        i_def.generate_target().shift(UP * 2)
        n_def.generate_target().shift(UP * 3)
        self.play(MoveToTarget(i_def), MoveToTarget(n_def))
        self.wait()

        i_copy = i_def[0].copy()
        i_copy.generate_target().move_to(probabilty_function[2])
        n_copy = n_def[0].copy()
        n_copy.generate_target().move_to(probabilty_function[4])
        probabilty_function_worded.next_to(equals, RIGHT)
        self.play(FadeIn(probabilty_function[0]),
                  FadeIn(probabilty_function[1]),
                  FadeIn(probabilty_function[3]),
                  FadeIn(probabilty_function[5]),
                  MoveToTarget(i_copy),
                  MoveToTarget(n_copy))
        self.play(Write(equals), Write(probabilty_function_worded))
        self.wait()

        #self.play(Write(i_def))
        #self.play(Write(n_def))
        #self.add(n_copy)
        #self.wait()

        #self.play(MoveToTarget(n_copy))
        #self.play(Write(equation))
        #self.wait()

