from manimlib.imports import *


class Highlight(Transform):
    CONFIG = {
        "rate_func": there_and_back
    }
    def __init__(self, mobject: Mobject, color, scale_factor=1.5, **kwargs):
        self.mobject = mobject
        self.color = color
        self.scale_factor = scale_factor
        super().__init__(mobject, **kwargs)

    def create_target(self):
        copy = self.mobject.copy()
        copy.set_color(self.color)
        copy.scale(self.scale_factor)
        return copy

class HighlightToColor(Succession):
    def __init__(self, mobject: Mobject, color, scale_factor=1.5, **kwargs):
        self.mobject = mobject
        self.color = color
        self.scale_factor = scale_factor
        super().__init__(ApplyFunction(self.animate, mobject), ScaleInPlace(mobject, 1/scale_factor), **kwargs)

    def animate(self, mobject):
        copy = mobject.copy()
        copy.set_color(self.color)
        copy.scale(self.scale_factor)
        return copy

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

    def replace_n_arg(self, n_arg_replacement, color):
        self.n_arg = n_arg_replacement
        replacement = CumulativeDistributionFunction(n_arg_replacement, self.p, self.n)
        replacement.rescale_to_fit(13, 0)
        replacement.match_style(self)
        replacement[1].set_color(color)
        return replacement, ReplacementTransform(self, replacement)

    def add_bounds(self, N_color, k_color):
        # Create objects for next animation
        lhs = self[0:3]
        rhs = self[3:]
        zero = TexMobject("0")
        top_ineq = TexMobject("N", "<", "k")
        bottom_ineq = TexMobject("N", r"\geq", "k")
        top_ineq[0].set_color(N_color)
        top_ineq[2].set_color(k_color)
        bottom_ineq[0].set_color(N_color)
        bottom_ineq[2].set_color(k_color)

        # Align 0 and brace
        zero.next_to(rhs, DOWN)
        zero.shift(DOWN)
        rhs = VGroup(rhs, zero)
        brace = Brace(rhs, LEFT)

        # Align ineqs
        top_ineq.next_to(self[3:], RIGHT)
        bottom_ineq.next_to(zero, RIGHT)
        bottom_ineq.align_to(top_ineq, LEFT)
        ineqs = VGroup(top_ineq, bottom_ineq)

        top_group = VGroup(self[3:], top_ineq)
        bottom_group = VGroup(zero, bottom_ineq)
        rhs = VGroup(top_group, bottom_group)
        whole_thing = VGroup(lhs, brace, rhs)

        return self, (Write(top_ineq),
                      Write(bottom_ineq),
                      Write(brace),
                      Write(zero),
                      whole_thing.arrange,
                      whole_thing.rescale_to_fit, 13, 0)

class CumulativeFunctionScene(Scene):
    cdf: CumulativeDistributionFunction

    def __init__(self, **kwargs):
        self.cdf = CumulativeDistributionFunction("n", "p", "n")
        self.definitions = {
            'k': TexMobject("k", r" = \textrm{number of successes}"),
            'n': TexMobject("n", r" = \textrm{number of trials}"),
            'p': TexMobject("p", r" = \textrm{probability of success}"),
            'i': TexMobject("i", r" = \textrm{iterator}"),
            'N': TexMobject("N", r" = \textrm{the number of barrows brothers killed}"),
            'I': TexMobject("I", r" = \textrm{getting a barrows item}"),
        }
        self.definition_colors = {
            'k': RED,
            'n': BLUE,
            'p': PURPLE,
            'i': GREEN,
            'N': YELLOW,
            'I': MAROON
        }
        self.cdf_definition_parts = {
            'k': [self.cdf[0][2], self.cdf[3][1]],
            'n': [self.cdf[1][0], self.cdf[4][1], self.cdf[10][0]],
            'p': [self.cdf[2][1], self.cdf[5][0], self.cdf[8][0]],
            'i': [self.cdf[3][4], self.cdf[4][2], self.cdf[6][0], self.cdf[11][1]],
            'N': [],
            'I': []
        }
        Scene.__init__(self, **kwargs)

    def introduce_cdf(self):
        self.add(self.cdf)
        self.wait()

        self.play(ApplyMethod(self.cdf.shift, UP*3))
        self.wait()

        definition_padding = 0.5
        for index, letter in enumerate(self.definitions):
            definition = self.definitions[letter]
            definition.set_color(self.definition_colors[letter])
            half_definition_size = len(self.definitions) / 2
            align_side = LEFT_SIDE if index < half_definition_size else RIGHT_SIDE
            align_vector = LEFT if index < half_definition_size else RIGHT
            self.play(Write(definition))
            self.wait()

            cdf_part_animations = []
            for part in self.cdf_definition_parts[letter]:
                cdf_part_animations.append(ApplyMethod(part.set_color, self.definition_colors[letter]))

            # Prevents errors when calling play with no animations
            if cdf_part_animations:
                self.play(*cdf_part_animations)

            self.play(definition.scale, .5,
                      definition.align_to, align_side, align_vector,
                      definition.align_to, BOTTOM, DOWN,
                      definition.shift, UP * definition_padding * (index % half_definition_size))
            self.wait()

        self.play(ApplyMethod(self.cdf.move_to, ORIGIN))

    def replace_p_with_definition(self):
        p_def = self.definitions['p']
        p_def.save_state()
        self.play(p_def.move_to, self.cdf,
                  p_def.shift, DOWN * 1.5)
        self.play(ScaleInPlace(p_def, 1.5, rate_func=there_and_back))
        self.play(Restore(p_def))
        self.wait()

        self.cdf, anim = self.cdf.replace_p(r"\left(1 \over 450-58\times N\right)")
        self.play(anim)
        self.wait()

        N_parts = self.cdf.get_parts_by_tex('N')
        # These indexes had to be found manually because if I used the substring_to_isolate
        # CONFIG option and found the Ns with get_part_by_tex than the N in the \binom{}{}
        # would never get found properly. Instead, when I tired to color it it would color the parentheses
        # before the N instead. N_1 and N_2 worked properly, but now that I can't use the substring_to_isolate
        # thing, they have to get done like this too :(
        N_0 = N_parts[0][10]
        N_1 = N_parts[1][10]

        self.play(HighlightToColor(N_0, self.definition_colors['N']), HighlightToColor(N_1, self.definition_colors['N']))
        self.wait()

    def replace_n_with_definition(self):
        N_def = self.definitions['N']
        n_def = self.definitions['n']
        n_equals_N_plus_one = TexMobject("n", "=", "N", "+", "1")
        n_equals_N_plus_one[0].set_color(self.definition_colors['n'])
        n_equals_N_plus_one[2].set_color(self.definition_colors['N'])


        N_def.save_state()
        n_def.save_state()

        n_N_group = VGroup(n_def, N_def)

        self.play(n_N_group.scale, 2,
                  n_N_group.arrange, DOWN,
                  n_N_group.next_to, self.cdf, DOWN)

        n_equals_N_plus_one.next_to(n_N_group, DOWN)

        self.play(Write(n_equals_N_plus_one))
        self.wait()

        self.play(Restore(N_def), Restore(n_def))
        self.wait()

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

        self.play(HighlightToColor(N_0, self.definition_colors['N']))

        self.cdf, anim = self.cdf.replace_n_arg("N", self.definition_colors['N'])
        self.play(anim)
        self.play(FadeOut(n_equals_N_plus_one))
        self.wait()

    def add_bounds(self):
        self.cdf, anim = self.cdf.add_bounds(self.definition_colors['N'], self.definition_colors['k'])
        self.play(*anim)
        self.wait()

    def construct(self):
        self.introduce_cdf()
        self.replace_p_with_definition()
        self.replace_n_with_definition()
        self.add_bounds()