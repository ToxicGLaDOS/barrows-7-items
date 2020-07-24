#!/usr/bin/env python

from manimlib.imports import *


class Definitions(Scene):
    def construct(self):
        # Set up the text
        i_def = TexMobject(r"I = \textrm{getting a barrows item}")
        n_def = TexMobject("N", r" = \textrm{the number of barrows brothers killed}")
        n = n_def[0]
        equation = TexMobject(r"f(x,N) = {(\frac{1}{450-58\times", "N", "}})^x")

        # Position text
        i_def.shift(UP)
        n_def.shift(DOWN)

        # Copy n and set a target for it
        n_copy = n.deepcopy()
        target_n = n_copy.generate_target()
        target_n.move_to(equation[1])

        self.play(Write(i_def))
        self.play(Write(n_def))
        self.add(n_copy)
        self.wait()

        self.play(MoveToTarget(n_copy))
        self.play(Write(equation))
        self.wait()

