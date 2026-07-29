"""Concept lecture: Advanced Math (Math domain 3 — nonlinear functions).

Narration script: scripts/L03-advanced-math.md
Ten sections; content clears between them, the margin note persists.
"""

import numpy as np

from manim import (
    Axes,
    Create,
    Dot,
    FadeOut,
    Line,
    MathTex,
    TransformMatchingTex,
    VGroup,
    Write,
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
)

from brand import (
    BODY_SIZE,
    CHARCOAL,
    DISPLAY_SIZE,
    EQUATION_SIZE,
    GAP_MD,
    GAP_SM,
    GREY,
    LABEL_SIZE,
    MARGIN_SIZE,
    SAGE,
    SLATE,
    TERRACOTTA,
    TITLE_SIZE,
    mono,
    serif,
)
from components.table import make_table
from scenes.base import SATScene


def underline(mobject, color=SAGE):
    return Line(
        mobject.get_corner(DOWN + LEFT) + DOWN * GAP_SM,
        mobject.get_corner(DOWN + RIGHT) + DOWN * GAP_SM,
        color=color,
        stroke_width=3,
    )


class AdvancedMath(SATScene):
    scene_id = "concept.advanced_math"

    def clear_section(self, t, fraction=0.12):
        old = [m for m in self.mobjects if m is not self.margin_note]
        if old:
            self.play(*[FadeOut(m) for m in old], run_time=t.fill(fraction))

    def construct(self):
        self.margin_note = mono("L03 · advanced math", MARGIN_SIZE)
        self.margin_note.to_corner(UP + LEFT, buff=GAP_SM)
        self.add(self.margin_note)

        self.intro()
        self.correspondence()
        self.covariation()
        self.real_world()
        self.cartesian()
        self.quadratic_forms()
        self.transformations()
        self.reverse_thinking()
        self.question_list()
        self.closing()

    # ------------------------------------------------------------ sections

    def intro(self):
        title = serif("Advanced Math", TITLE_SIZE * 1.3)
        subtitle = serif("Digital SAT · Math domain 3", BODY_SIZE, GREY)
        subtitle.next_to(title, DOWN, buff=GAP_MD)
        VGroup(title, subtitle).move_to(UP * 1.4)

        with self.beat("title") as t:
            self.play(Write(title), run_time=t.fill(0.4))
            self.play(Write(subtitle), run_time=t.fill(0.2))
            t.hold()

        recap = serif("from linear relationships to nonlinear functions",
                      LABEL_SIZE, GREY)
        recap.next_to(subtitle, DOWN, buff=GAP_MD * 1.5)

        with self.beat("recap") as t:
            self.play(Write(recap), run_time=t.fill(0.35))
            t.hold()

        third = serif("about one third of SAT Math", BODY_SIZE)
        third.next_to(recap, DOWN, buff=GAP_MD * 1.3)

        with self.beat("third") as t:
            self.play(Write(third), run_time=t.fill(0.3))
            self.play(Create(underline(third)), run_time=t.fill(0.15))
            t.hold()

        bridge = serif("the bridge to calculus and STEM", LABEL_SIZE, GREY)
        bridge.next_to(third, DOWN, buff=GAP_MD * 1.3)

        with self.beat("bridge") as t:
            self.play(Write(bridge), run_time=t.fill(0.3))
            t.hold()

    def correspondence(self):
        head = serif("A function is a machine", TITLE_SIZE)
        head.to_edge(UP, buff=GAP_MD * 1.6)
        flow = serif("input  →  rule  →  exactly one output", LABEL_SIZE, GREY)
        flow.next_to(head, DOWN, buff=GAP_MD)

        with self.beat("corr") as t:
            self.clear_section(t)
            self.play(Write(head), run_time=t.fill(0.3))
            self.play(Write(flow), run_time=t.fill(0.2))
            t.hold()

        fdef = MathTex("f(x)", "=", "2x + 3", font_size=DISPLAY_SIZE, color=CHARCOAL)
        fdef.next_to(flow, DOWN, buff=GAP_MD * 1.4)

        with self.beat("feval") as t:
            self.play(Write(fdef), run_time=t.fill(0.35))
            t.hold()

        chain = MathTex(
            "f(4)", "=", "2 \\cdot 4 + 3", "=", "11",
            font_size=DISPLAY_SIZE, color=CHARCOAL,
        )
        chain.next_to(fdef, DOWN, buff=GAP_MD * 1.2)
        chain[4].set_color(SAGE)

        with self.beat("feval2") as t:
            self.play(Write(chain), run_time=t.fill(0.4))
            t.hold()

        note = serif("the input can also be an expression", LABEL_SIZE, GREY)
        note.next_to(chain, DOWN, buff=GAP_MD * 1.2)

        with self.beat("fnotation") as t:
            self.play(Write(note), run_time=t.fill(0.3))
            t.hold()

        fxa = MathTex(
            "f(x + a)", "=", "2(x + a) + 3",
            font_size=DISPLAY_SIZE, color=CHARCOAL,
        )
        fxa.next_to(note, DOWN, buff=GAP_MD * 1.2)

        with self.beat("fxa") as t:
            self.play(Write(fxa), run_time=t.fill(0.4))
            t.hold()

        fxa2 = MathTex(
            "f(x + a)", "=", "2x + 2a + 3",
            font_size=DISPLAY_SIZE, color=CHARCOAL,
        )
        fxa2.move_to(fxa)

        with self.beat("fxa2") as t:
            self.play(TransformMatchingTex(fxa, fxa2), run_time=t.fill(0.4))
            t.hold()

        warning = serif("substitute the whole input, everywhere x appears",
                        LABEL_SIZE, TERRACOTTA)
        warning.to_edge(DOWN, buff=GAP_MD)

        with self.beat("mistake") as t:
            self.play(Write(warning), run_time=t.fill(0.3))
            t.hold()

    def covariation(self):
        head = serif("How do the quantities change together?", TITLE_SIZE)
        head.to_edge(UP, buff=GAP_MD * 1.6)

        with self.beat("cov") as t:
            self.clear_section(t)
            self.play(Write(head), run_time=t.fill(0.35))
            t.hold()

        linear = serif("linear — the output rises by 3 every step", LABEL_SIZE)
        linear.next_to(head, DOWN, buff=GAP_MD * 1.3)
        linear.move_to(np.array([-2.6, linear.get_center()[1], 0]))

        with self.beat("linear_rate") as t:
            self.play(Write(linear), run_time=t.fill(0.35))
            t.hold()

        quad = serif("quadratic — second differences are constant", LABEL_SIZE)
        quad.next_to(linear, DOWN, buff=GAP_SM * 1.5, aligned_edge=LEFT)

        with self.beat("quad_rate") as t:
            self.play(Write(quad), run_time=t.fill(0.35))
            t.hold()

        expo = serif("exponential — multiplied by a constant factor", LABEL_SIZE)
        expo.next_to(quad, DOWN, buff=GAP_SM * 1.5, aligned_edge=LEFT)
        seq = MathTex(
            "2", "\\;\\xrightarrow{\\times 3}\\;", "6",
            "\\;\\xrightarrow{\\times 3}\\;", "18",
            "\\;\\xrightarrow{\\times 3}\\;", "54",
            font_size=EQUATION_SIZE, color=CHARCOAL,
        )
        seq.next_to(expo, DOWN, buff=GAP_MD * 1.2)
        seq.move_to(np.array([0, seq.get_center()[1], 0]))
        for i in (1, 3, 5):
            seq[i].set_color(TERRACOTTA)

        with self.beat("expo") as t:
            self.play(Write(expo), run_time=t.fill(0.25))
            self.play(Write(seq), run_time=t.fill(0.35))
            t.hold()

        families = serif("the pattern tells you the family", BODY_SIZE)
        families.to_edge(DOWN, buff=GAP_MD * 1.4)

        with self.beat("families") as t:
            self.play(Write(families), run_time=t.fill(0.3))
            self.play(Create(underline(families)), run_time=t.fill(0.15))
            t.hold()

    def real_world(self):
        head = serif("Nonlinear models in the real world", TITLE_SIZE)
        head.to_edge(UP, buff=GAP_MD * 1.6)

        with self.beat("real") as t:
            self.clear_section(t)
            self.play(Write(head), run_time=t.fill(0.35))
            t.hold()

        # A thrown ball: rise, peak, fall.
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 4.5, 1],
            x_length=4.2,
            y_length=2.8,
            axis_config={"color": CHARCOAL, "include_ticks": False,
                         "tip_length": 0.15},
        )
        axes.move_to(LEFT * 3.6 + DOWN * 0.4)
        path = axes.plot(lambda x: 4 - (x - 2) ** 2, x_range=[0.1, 3.9], color=SLATE)
        ball_label = serif("a thrown ball — quadratic", LABEL_SIZE, GREY)
        ball_label.next_to(axes, DOWN, buff=GAP_SM * 1.4)

        with self.beat("ball") as t:
            self.play(Create(axes), run_time=t.fill(0.2))
            self.play(Create(path), run_time=t.fill(0.35))
            self.play(Write(ball_label), run_time=t.fill(0.15))
            t.hold()

        profit = serif("profit rises, then falls", LABEL_SIZE)
        profit.move_to(RIGHT * 3.4 + UP * 1.0)

        with self.beat("profit") as t:
            self.play(Write(profit), run_time=t.fill(0.3))
            t.hold()

        expo_real = VGroup(
            serif("exponential:", LABEL_SIZE),
            serif("interest · population · decay", LABEL_SIZE, GREY),
        ).arrange(DOWN, buff=GAP_SM, aligned_edge=LEFT)
        expo_real.next_to(profit, DOWN, buff=GAP_MD, aligned_edge=LEFT)

        with self.beat("expo_real") as t:
            self.play(Write(expo_real), run_time=t.fill(0.35))
            t.hold()

        poly = VGroup(
            serif("polynomial and rational:", LABEL_SIZE),
            serif("structures · speeds · volume", LABEL_SIZE, GREY),
        ).arrange(DOWN, buff=GAP_SM, aligned_edge=LEFT)
        poly.next_to(expo_real, DOWN, buff=GAP_MD, aligned_edge=LEFT)

        with self.beat("poly") as t:
            self.play(Write(poly), run_time=t.fill(0.35))
            t.hold()

        with self.beat("interpret") as t:
            self.clear_section(t)
            head2 = serif("Interpret before you calculate", TITLE_SIZE)
            head2.to_edge(UP, buff=GAP_MD * 1.6)
            self.play(Write(head2), run_time=t.fill(0.35))
            t.hold()

        asks = VGroup(
            serif("same amount each step?  linear", BODY_SIZE),
            serif("same factor each step?  exponential", BODY_SIZE),
            serif("rises then falls?  quadratic", BODY_SIZE),
        ).arrange(DOWN, buff=GAP_MD, aligned_edge=LEFT)
        asks.move_to(UP * 0.2)

        with self.beat("ask_list") as t:
            self.play(Write(asks), run_time=t.fill(0.5))
            t.hold()

        pattern = serif("the pattern matters more than the formula", LABEL_SIZE)
        pattern.next_to(asks, DOWN, buff=GAP_MD * 1.6)

        with self.beat("pattern_note") as t:
            self.play(Write(pattern), run_time=t.fill(0.3))
            self.play(Create(underline(pattern)), run_time=t.fill(0.15))
            t.hold()

    def cartesian(self):
        head = serif("A point on a graph makes the equation true", TITLE_SIZE * 0.9)
        head.to_edge(UP, buff=GAP_MD * 1.6)

        with self.beat("cart") as t:
            self.clear_section(t)
            self.play(Write(head), run_time=t.fill(0.35))
            t.hold()

        eq = MathTex("y = x^2 + 1", font_size=DISPLAY_SIZE, color=CHARCOAL)
        eq.next_to(head, DOWN, buff=GAP_MD * 1.4)
        point = MathTex("(2, 5)\\ \\text{?}", font_size=DISPLAY_SIZE, color=CHARCOAL)
        point.next_to(eq, DOWN, buff=GAP_MD)

        with self.beat("cart_ex") as t:
            self.play(Write(eq), run_time=t.fill(0.3))
            self.play(Write(point), run_time=t.fill(0.2))
            t.hold()

        check = MathTex(
            "2^2 + 1", "=", "5", "\\quad\\checkmark",
            font_size=DISPLAY_SIZE, color=CHARCOAL,
        )
        check.next_to(point, DOWN, buff=GAP_MD * 1.2)
        check[2].set_color(SAGE)
        check[3].set_color(SAGE)

        with self.beat("cart_on") as t:
            self.play(Write(check), run_time=t.fill(0.4))
            t.hold()

        off = MathTex(
            "(2, 6):", "\\quad 5 \\ne 6",
            font_size=DISPLAY_SIZE, color=CHARCOAL,
        )
        off.next_to(check, DOWN, buff=GAP_MD * 1.2)
        off[1].set_color(TERRACOTTA)

        with self.beat("cart_off") as t:
            self.play(Write(off), run_time=t.fill(0.4))
            t.hold()

        note = serif("test points · read intercepts · connect algebra to graphs",
                     LABEL_SIZE, GREY)
        note.to_edge(DOWN, buff=GAP_MD)

        with self.beat("cart_note") as t:
            self.play(Write(note), run_time=t.fill(0.3))
            t.hold()

    def quadratic_forms(self):
        head = serif("Three forms, three reveals", TITLE_SIZE)
        head.to_edge(UP, buff=GAP_MD * 1.6)

        with self.beat("forms") as t:
            self.clear_section(t)
            self.play(Write(head), run_time=t.fill(0.35))
            t.hold()

        col_x = [-4.4, 0.0, 4.4]
        std_head = serif("standard", BODY_SIZE)
        std_head.move_to(np.array([col_x[0], 2.2, 0]))
        std_form = MathTex("ax^2 + bx + c", font_size=EQUATION_SIZE, color=CHARCOAL)
        std_form.next_to(std_head, DOWN, buff=GAP_MD)
        std_reveal = serif("c is the y-intercept", LABEL_SIZE, GREY)
        std_reveal.next_to(std_form, DOWN, buff=GAP_SM * 1.4)

        with self.beat("standard") as t:
            self.play(Write(std_head), run_time=t.fill(0.15))
            self.play(Write(std_form), run_time=t.fill(0.25))
            self.play(Write(std_reveal), run_time=t.fill(0.15))
            t.hold()

        std_ex = MathTex(
            "2x^2 - 5x + ", "7", font_size=EQUATION_SIZE, color=CHARCOAL
        )
        std_ex.next_to(std_reveal, DOWN, buff=GAP_MD)
        std_ex[1].set_color(TERRACOTTA)

        with self.beat("standard_ex") as t:
            self.play(Write(std_ex), run_time=t.fill(0.3))
            t.hold()

        fac_head = serif("factored", BODY_SIZE)
        fac_head.move_to(np.array([col_x[1], 2.2, 0]))
        fac_form = MathTex("a(x - r)(x - s)", font_size=EQUATION_SIZE, color=CHARCOAL)
        fac_form.next_to(fac_head, DOWN, buff=GAP_MD)
        fac_reveal = serif("r and s are the roots", LABEL_SIZE, GREY)
        fac_reveal.next_to(fac_form, DOWN, buff=GAP_SM * 1.4)

        with self.beat("factored") as t:
            self.play(std_ex[1].animate.set_color(CHARCOAL), run_time=t.fill(0.05))
            self.play(Write(fac_head), run_time=t.fill(0.15))
            self.play(Write(fac_form), run_time=t.fill(0.25))
            self.play(Write(fac_reveal), run_time=t.fill(0.15))
            t.hold()

        fac_ex = MathTex(
            "(x - 3)(x + 2)", font_size=EQUATION_SIZE, color=CHARCOAL
        )
        fac_ex.next_to(fac_reveal, DOWN, buff=GAP_MD)
        fac_roots = MathTex(
            "x = 3,\\ x = -2", font_size=EQUATION_SIZE, color=TERRACOTTA
        )
        fac_roots.next_to(fac_ex, DOWN, buff=GAP_SM * 1.4)

        with self.beat("factored_ex") as t:
            self.play(Write(fac_ex), run_time=t.fill(0.25))
            self.play(Write(fac_roots), run_time=t.fill(0.2))
            t.hold()

        ver_head = serif("vertex", BODY_SIZE)
        ver_head.move_to(np.array([col_x[2], 2.2, 0]))
        ver_form = MathTex("a(x - h)^2 + k", font_size=EQUATION_SIZE, color=CHARCOAL)
        ver_form.next_to(ver_head, DOWN, buff=GAP_MD)
        ver_reveal = serif("vertex at (h, k)", LABEL_SIZE, GREY)
        ver_reveal.next_to(ver_form, DOWN, buff=GAP_SM * 1.4)

        with self.beat("vertexform") as t:
            self.play(fac_roots.animate.set_color(CHARCOAL), run_time=t.fill(0.05))
            self.play(Write(ver_head), run_time=t.fill(0.15))
            self.play(Write(ver_form), run_time=t.fill(0.25))
            self.play(Write(ver_reveal), run_time=t.fill(0.15))
            t.hold()

        ver_ex = MathTex(
            "2(x - 4)^2 + 1", font_size=EQUATION_SIZE, color=CHARCOAL
        )
        ver_ex.next_to(ver_reveal, DOWN, buff=GAP_MD)
        ver_vertex = MathTex(
            "(4, 1)\\ \\text{minimum}", font_size=EQUATION_SIZE, color=TERRACOTTA
        )
        ver_vertex.next_to(ver_ex, DOWN, buff=GAP_SM * 1.4)

        with self.beat("vertex_ex") as t:
            self.play(Write(ver_ex), run_time=t.fill(0.25))
            self.play(Write(ver_vertex), run_time=t.fill(0.2))
            t.hold()

        with self.beat("which") as t:
            self.play(ver_vertex.animate.set_color(CHARCOAL), run_time=t.fill(0.05))
            self.play(
                Create(underline(std_head)),
                Create(underline(fac_head)),
                Create(underline(ver_head)),
                run_time=t.fill(0.25),
            )
            t.hold()

        rewrite = serif("rewriting a form reveals hidden information",
                        LABEL_SIZE, GREY)
        rewrite.to_edge(DOWN, buff=GAP_MD)

        with self.beat("rewrite") as t:
            self.play(Write(rewrite), run_time=t.fill(0.3))
            t.hold()

    def transformations(self):
        head = serif("Transformations of the parent function", TITLE_SIZE * 0.9)
        head.to_edge(UP, buff=GAP_MD * 1.6)

        axes = Axes(
            x_range=[-5, 7, 1],
            y_range=[-4, 5, 1],
            x_length=6.6,
            y_length=4.6,
            axis_config={"color": CHARCOAL, "include_ticks": False,
                         "tip_length": 0.15},
        )
        axes.move_to(LEFT * 3.2 + DOWN * 0.9)
        parent = axes.plot(lambda x: 0.4 * x ** 2, x_range=[-3.3, 3.3], color=SLATE)
        parent_eq = MathTex("y = x^2", font_size=EQUATION_SIZE, color=SLATE)
        parent_eq.move_to(RIGHT * 3.4 + UP * 1.6)

        with self.beat("parent") as t:
            self.clear_section(t)
            self.play(Write(head), run_time=t.fill(0.2))
            self.play(Create(axes), run_time=t.fill(0.2))
            self.play(Create(parent), run_time=t.fill(0.25))
            self.play(Write(parent_eq), run_time=t.fill(0.15))
            t.hold()

        up3 = axes.plot(lambda x: 0.4 * x ** 2 + 1.6, x_range=[-2.8, 2.8],
                        color=CHARCOAL)
        up3_eq = MathTex("y = x^2 + 3", font_size=EQUATION_SIZE, color=CHARCOAL)
        up3_eq.next_to(parent_eq, DOWN, buff=GAP_MD, aligned_edge=LEFT)

        with self.beat("vshift") as t:
            self.play(Create(up3), run_time=t.fill(0.3))
            self.play(Write(up3_eq), run_time=t.fill(0.2))
            t.hold()

        right4 = axes.plot(lambda x: 0.4 * (x - 4) ** 2, x_range=[0.7, 6.9],
                           color=TERRACOTTA)
        right4_eq = MathTex("y = (x - 4)^2", font_size=EQUATION_SIZE,
                            color=TERRACOTTA)
        right4_eq.next_to(up3_eq, DOWN, buff=GAP_MD, aligned_edge=LEFT)
        zero_note = serif("x − 4 = 0 at x = 4", LABEL_SIZE, GREY)
        zero_note.next_to(right4_eq, DOWN, buff=GAP_SM * 1.4, aligned_edge=LEFT)

        with self.beat("hshift") as t:
            self.play(Create(right4), run_time=t.fill(0.3))
            self.play(Write(right4_eq), run_time=t.fill(0.15))
            self.play(Write(zero_note), run_time=t.fill(0.15))
            t.hold()

        left4_eq = MathTex("y = (x + 4)^2 \\to \\text{left}",
                           font_size=EQUATION_SIZE, color=CHARCOAL)
        left4_eq.next_to(zero_note, DOWN, buff=GAP_MD, aligned_edge=LEFT)

        with self.beat("hshift2") as t:
            self.play(right4.animate.set_color(GREY),
                      right4_eq.animate.set_color(GREY), run_time=t.fill(0.1))
            self.play(Write(left4_eq), run_time=t.fill(0.3))
            t.hold()

        rule = serif("outside: vertical · inside: horizontal, opposite the sign",
                     LABEL_SIZE)
        rule.to_edge(DOWN, buff=GAP_MD * 0.8)

        with self.beat("shift_rule") as t:
            self.play(Write(rule), run_time=t.fill(0.3))
            self.play(Create(underline(rule)), run_time=t.fill(0.15))
            t.hold()

        with self.beat("stretch") as t:
            self.clear_section(t)
            head2 = serif("Stretch, compress, reflect", TITLE_SIZE)
            head2.to_edge(UP, buff=GAP_MD * 1.6)
            narrow = serif("3x² — narrower", BODY_SIZE)
            narrow.move_to(UP * 0.8)
            self.play(Write(head2), run_time=t.fill(0.25))
            self.play(Write(narrow), run_time=t.fill(0.25))
            t.hold()

        wider = serif("½x² — wider", BODY_SIZE)
        wider.move_to(ORIGIN + DOWN * 0.2)

        with self.beat("compress") as t:
            self.play(Write(wider), run_time=t.fill(0.35))
            t.hold()

        reflect = serif("−x² — reflected, opens downward", BODY_SIZE)
        reflect.move_to(DOWN * 1.2)

        with self.beat("reflect") as t:
            self.play(Write(reflect), run_time=t.fill(0.35))
            t.hold()

    def reverse_thinking(self):
        head = serif("Reverse thinking", TITLE_SIZE)
        head.to_edge(UP, buff=GAP_MD * 1.6)
        note = serif("from the output back to the input", LABEL_SIZE, GREY)
        note.next_to(head, DOWN, buff=GAP_MD)

        with self.beat("reverse") as t:
            self.clear_section(t)
            self.play(Write(head), run_time=t.fill(0.3))
            self.play(Write(note), run_time=t.fill(0.2))
            t.hold()

        step1 = MathTex("3x + 2", "=", "17", font_size=DISPLAY_SIZE, color=CHARCOAL)
        step2 = MathTex("3x", "=", "15", font_size=DISPLAY_SIZE, color=CHARCOAL)
        step3 = MathTex("x", "=", "5", font_size=DISPLAY_SIZE, color=CHARCOAL)
        for step in (step1, step2, step3):
            step.move_to(DOWN * 0.4)

        with self.beat("rev_eq") as t:
            self.play(Write(step1), run_time=t.fill(0.4))
            t.hold()

        with self.beat("rev_solve") as t:
            self.play(TransformMatchingTex(step1, step2), run_time=t.fill(0.45))
            t.hold()

        with self.beat("rev_answer") as t:
            self.play(TransformMatchingTex(step2, step3), run_time=t.fill(0.4))
            t.hold()

        meaning = serif("solve for meaning, not just symbols", LABEL_SIZE, GREY)
        meaning.next_to(step3, DOWN, buff=GAP_MD * 1.6)

        with self.beat("rev_note") as t:
            self.play(Write(meaning), run_time=t.fill(0.3))
            t.hold()

    def question_list(self):
        head = serif("Ask yourself", TITLE_SIZE)
        head.to_edge(UP, buff=GAP_MD * 1.6)
        left = VGroup(
            serif("what is given?", LABEL_SIZE),
            serif("what is hidden?", LABEL_SIZE),
            serif("which form reveals it?", LABEL_SIZE),
            serif("what input gives this output?", LABEL_SIZE),
        ).arrange(DOWN, buff=GAP_SM * 1.4, aligned_edge=LEFT)
        right = VGroup(
            serif("what does the coefficient mean?", LABEL_SIZE),
            serif("what does the point mean?", LABEL_SIZE),
            serif("which family is the pattern?", LABEL_SIZE),
        ).arrange(DOWN, buff=GAP_SM * 1.4, aligned_edge=LEFT)
        left.next_to(head, DOWN, buff=GAP_MD * 1.5)
        left.move_to(np.array([-3.6, left.get_center()[1], 0]))
        right.next_to(head, DOWN, buff=GAP_MD * 1.5)
        right.move_to(np.array([3.2, right.get_center()[1], 0]))

        with self.beat("questions") as t:
            self.clear_section(t)
            self.play(Write(head), run_time=t.fill(0.2))
            self.play(Write(left), run_time=t.fill(0.3))
            self.play(Write(right), run_time=t.fill(0.3))
            t.hold()

    def closing(self):
        head = serif("Review", TITLE_SIZE)
        head.to_edge(UP, buff=GAP_MD * 1.6)

        with self.beat("review") as t:
            self.clear_section(t)
            self.play(Write(head), run_time=t.fill(0.35))
            t.hold()

        lines = [
            "1  a function: one input, one output — and a relationship",
            "2  linear +amount · quadratic 2nd differences · exponential ×factor",
            "3  a point on the graph makes the equation true",
            "4  standard → y-intercept · factored → roots · vertex → extremum",
            "5  outside shifts vertically, inside shifts horizontally",
            "6  reverse thinking: output back to input",
        ]
        review_lines = VGroup(
            *[serif(line, MARGIN_SIZE) for line in lines]
        ).arrange(DOWN, buff=GAP_SM * 1.5, aligned_edge=LEFT)
        review_lines.next_to(head, DOWN, buff=GAP_MD * 1.3)

        for name, line in zip(
            ["rev1", "rev2", "rev3", "rev4", "rev5", "rev6"], review_lines
        ):
            with self.beat(name) as t:
                self.play(Write(line), run_time=t.fill(0.35))
                t.hold()

        key = serif("Structure over formulas.", TITLE_SIZE)
        key.move_to(ORIGIN)

        with self.beat("key") as t:
            self.clear_section(t)
            self.play(Write(key), run_time=t.fill(0.35))
            self.play(Create(underline(key)), run_time=t.fill(0.15))
            t.hold()

        upcoming = serif("next: Geometry and Trigonometry", LABEL_SIZE, GREY)
        upcoming.next_to(key, DOWN, buff=GAP_MD * 1.6)

        with self.beat("next_lecture") as t:
            self.play(Write(upcoming), run_time=t.fill(0.35))
            t.hold()

        end = mono("end of lecture", MARGIN_SIZE)
        end.to_edge(DOWN, buff=GAP_MD)

        with self.beat("end") as t:
            self.play(Write(end), run_time=t.fill(0.4))
            t.hold()
