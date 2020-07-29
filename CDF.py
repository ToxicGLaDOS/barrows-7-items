from manimlib.imports import *


class CumulativeDistributionFunction(TexMobject):
    def __init__(self, p, n, *tex_strings, **kwargs):
        TexMobject.__init__(self,
                            r"\sum\limits_{i=0}^{\lfloor{k}\rfloor}", rf"{{", fr"\binom{{{n}}}{{i}}", p, "^i", r"\left(1-", p, rf"\right)^{{", n, "-i}}",
                            *tex_strings,
                            **kwargs)


class CumulativeFunctionScene(Scene):
    def construct(self):
        function_notation = TexMobject(r"F\left(k;n,p\right) =")
        cdf   = VGroup(function_notation.copy(), CumulativeDistributionFunction("p", "n"))
        cdf.arrange()
        cdf_2 = VGroup(function_notation.copy(), CumulativeDistributionFunction(r"\left(\frac{1}{450-58\times N}\right)", "n"))
        cdf_2.arrange()
        cdf_2.rescale_to_fit(13, 0)
        cdf_3 = VGroup(function_notation.copy(), CumulativeDistributionFunction(r"\left(\frac{1}{450-58\times N}\right)", "N+1"))
        cdf_3.arrange()
        cdf_3.rescale_to_fit(13, 0)
        self.add(cdf)
        self.wait()

        # ReplacementTransform is like a short cut for "turn x into y and then remove x from the scene and add y"
        # So in this case it turns cdf into cdf_2 and then cdf is removed from the scene while cdf_2 is put into the scene
        # which means that we can interact with cdf_2 later
        self.play(ReplacementTransform(cdf, cdf_2))
        self.wait()

        self.play(ReplacementTransform(cdf_2, cdf_3))
        self.wait()

        # Create objects for next animation
        lhs = cdf_3[0]
        rhs = cdf_3[1]
        zero = TexMobject("0")
        top_ineq = TexMobject("N < k")
        bottom_ineq = TexMobject(r"N \geq k")

        # Align 0 and brace
        zero.align_to(rhs, ORIGIN)
        zero.shift(DOWN  * 2)
        rhs = VGroup(rhs, zero)
        brace = Brace(rhs, LEFT)
        whole_thing = VGroup(lhs, brace, rhs)

        # Align ineqs
        top_ineq.next_to(cdf_3, RIGHT)
        bottom_ineq.next_to(zero, RIGHT)
        bottom_ineq.align_to(top_ineq, LEFT)
        ineqs = VGroup(top_ineq, bottom_ineq)

        whole_thing.add(ineqs)
        self.play(Write(top_ineq),
                  Write(bottom_ineq),
                  Write(brace),
                  Write(zero),
                  whole_thing.arrange,
                  whole_thing.rescale_to_fit, 13, 0)
        self.wait()