from manimlib.imports import *



class CumulativeDistributionFunction(TexMobject):
    def __init__(self, n_arg, p, n, *tex_strings, **kwargs):
        TexMobject.__init__(self,
                            r"F\left(k;", n_arg, r",p\right) =", r"\sum\limits_{i=0}^{\lfloor{k}\rfloor}{{", fr"\binom{{ {n} }}{{ i }}", p, "^i", r"\left(1-", p, rf"\right)^{{", n, "-i}}",
                            *tex_strings,
                            **kwargs)
        self.p = p
        self.n = n
        self.n_arg = n_arg

    def replace_p(self, p_replacement):
        self.p = p_replacement
        replacement = CumulativeDistributionFunction(self.n_arg, p_replacement, self.n)
        replacement.rescale_to_fit(13, 0)
        replacement.match_style(self)
        return replacement, ReplacementTransform(self, replacement)

    def replace_n(self, n_replacement, **kwargs):
        self.n = n_replacement
        replacement = CumulativeDistributionFunction(self.n_arg, self.p, n_replacement, **kwargs)
        replacement.rescale_to_fit(13, 0)
        replacement.match_style(self)
        return replacement, ReplacementTransform(self, replacement)

    def replace_n_arg(self, n_arg_replacement):
        self.n_arg = n_arg_replacement
        replacement = CumulativeDistributionFunction(n_arg_replacement, self.p, self.n)
        replacement.rescale_to_fit(13, 0)
        replacement.match_style(self)
        return replacement, ReplacementTransform(self, replacement)

    def add_bounds(self):
        # Create objects for next animation
        lhs = self[0:3]
        rhs = self[3:]
        zero = TexMobject("0")
        top_ineq = TexMobject("N < k")
        bottom_ineq = TexMobject(r"N \geq k")

        # Align 0 and brace
        zero.align_to(rhs, ORIGIN)
        zero.shift(DOWN * 2)
        rhs = VGroup(rhs, zero)
        brace = Brace(rhs, LEFT)
        whole_thing = VGroup(lhs, brace, rhs)

        # Align ineqs
        top_ineq.next_to(self, RIGHT)
        bottom_ineq.next_to(zero, RIGHT)
        bottom_ineq.align_to(top_ineq, LEFT)
        ineqs = VGroup(top_ineq, bottom_ineq)

        whole_thing.add(ineqs)
        return self, (Write(top_ineq),
                      Write(bottom_ineq),
                      Write(brace),
                      Write(zero),
                      whole_thing.arrange,
                      whole_thing.rescale_to_fit, 13, 0)

class CumulativeFunctionScene(Scene):
    cdf: CumulativeDistributionFunction

    def __init__(self, **kwargs):
        self.definitions = {
            'I': ("I", r" = \textrm{getting a barrows item}"),
            'N': ("N", r" = \textrm{the number of barrows brothers killed}"),
            'n': ("n", r" = \textrm{number of trials}"),
            'k': ("k", r" = \textrm{number of successes}"),
            'i': ("i", r" = \textrm{iterator}"),
            'p': ("p", r" = \textrm{probability of success}")
        }

        self.cdf = CumulativeDistributionFunction("n", "p", "n")
        Scene.__init__(self, **kwargs)

    def introduce_cdf(self):
        self.add(self.cdf)
        self.wait()

    def replace_p_with_definition(self):
        p_def = TexMobject(*self.definitions['p'])
        p_def.shift(UP * 3)
        self.play(Write(p_def))
        self.wait()

        self.cdf, anim = self.cdf.replace_p(r"\left(1 \over 450-58\times N\right)")
        self.play(anim)
        self.wait()

        self.play(FadeOut(p_def))
        self.wait()

    def replace_n_with_definition(self):
        N_def = TexMobject(*self.definitions['N'])
        n_def = TexMobject(*self.definitions['n'])
        n_equals_N_plus_one = TexMobject("n", "=", "N", "+", "1")

        N_def.shift(UP * 3)
        n_def.shift(UP * 2)
        n_equals_N_plus_one.shift(UP)

        self.play(Write(N_def), Write(n_def))
        self.wait()

        self.play(Write(n_equals_N_plus_one))
        self.wait()

        self.play(FadeOut(N_def), FadeOut(n_def))
        self.play(n_equals_N_plus_one.shift, UP * 2)
        self.cdf, anim = self.cdf.replace_n(("N+1"))
        self.play(anim)
        self.wait()

        n_part = self.cdf.get_part_by_tex('n')
        N_parts = self.cdf.get_parts_by_tex('N')

        # These indexes had to be found manually because if I used the substring_to_isolate
        # CONFIG option and found the Ns with get_part_by_tex than the N in the \binom{}{}
        # would never get found properly. Instead, when I tired to color it it would color the parentheses
        # before the N instead. N_1 and N_2 worked properly, but now that I can't use the substring_to_isolate
        # thing, they have to get done like this too :(
        N_0 = N_parts[0][1]
        N_1 = N_parts[1][10]
        N_2 = N_parts[2][10]

        self.play(FadeToColor(n_part, RED))
        self.play(FadeToColor(N_0, PURPLE), FadeToColor(N_1, PURPLE), FadeToColor(N_2, PURPLE))
        self.wait()
        self.play(FadeToColor(N_0, WHITE), FadeToColor(N_1, WHITE), FadeToColor(N_2, WHITE), FadeToColor(n_part, WHITE))
        self.wait()

        self.cdf, anim = self.cdf.replace_n_arg("N")
        self.play(anim)
        self.play(FadeOut(n_equals_N_plus_one))
        self.wait()

    def add_bounds(self):
        self.cdf, anim = self.cdf.add_bounds()
        self.play(*anim)
        self.wait()

    def construct(self):
        self.introduce_cdf()
        self.replace_p_with_definition()
        self.replace_n_with_definition()
        self.add_bounds()