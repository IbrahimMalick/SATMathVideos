"""Worked problem: the art of the shortcut (Algebra Q2).

Narration script: scripts/Q02-art-of-shortcut.md
The problem stays on screen from its reveal; the shortcut path builds on
the left, the standard three-step recipe appears on the right for
comparison.
"""

import numpy as np

from manim import (
    Create,
    FadeOut,
    Line,
    MathTex,
    TransformMatchingTex,
    VGroup,
    Write,
    DOWN,
    LEFT,
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
    TERRACOTTA,
    TITLE_SIZE,
    mono,
    serif,
)
from scenes.base import SATScene


def underline(mobject, color=SAGE):
    return Line(
        mobject.get_corner(DOWN + LEFT) + DOWN * GAP_SM,
        mobject.get_corner(DOWN + RIGHT) + DOWN * GAP_SM,
        color=color,
        stroke_width=3,
    )


class AlgebraQ2(SATScene):
    scene_id = "worked.algebra_q2"

    def construct(self):
        self.margin_note = mono("Q02 · the shortcut", MARGIN_SIZE)
        self.margin_note.to_corner(UP + LEFT, buff=GAP_SM)
        self.add(self.margin_note)

        self.intro()
        self.problem_and_structure()
        self.shortcut()
        self.comparison()
        self.recap()

    # ------------------------------------------------------------ sections

    def intro(self):
        title = serif("The Art of the Shortcut", TITLE_SIZE * 1.15)
        subtitle = serif("Q2 · structure and equivalence", BODY_SIZE, GREY)
        subtitle.next_to(title, DOWN, buff=GAP_MD)
        VGroup(title, subtitle).move_to(UP * 1.2)

        with self.beat("title") as t:
            self.play(Write(title), run_time=t.fill(0.4))
            self.play(Write(subtitle), run_time=t.fill(0.25))
            t.hold()

        big1 = serif("the SAT asks for expressions, not just x", BODY_SIZE)
        big1.next_to(subtitle, DOWN, buff=GAP_MD * 1.6)
        big2 = serif("procedural flexibility — choose the efficient path",
                     LABEL_SIZE, GREY)
        big2.next_to(big1, DOWN, buff=GAP_MD)

        with self.beat("big_picture") as t:
            self.play(Write(big1), run_time=t.fill(0.3))
            self.play(Create(underline(big1)), run_time=t.fill(0.12))
            self.play(Write(big2), run_time=t.fill(0.2))
            t.hold()

        self._intro_group = VGroup(title, subtitle, big1, big2)

    def problem_and_structure(self):
        problem = MathTex(
            "3x + 12 = 30", font_size=DISPLAY_SIZE, color=CHARCOAL
        )
        question = serif("what is the value of x + 4 ?", BODY_SIZE)
        question.next_to(problem, DOWN, buff=GAP_MD)
        card = VGroup(problem, question)
        card.to_edge(UP, buff=GAP_MD * 1.9)
        self.card = card

        with self.beat("problem") as t:
            self.play(*[FadeOut(m) for m in self._intro_group],
                      run_time=t.fill(0.12))
            self.play(Write(problem), run_time=t.fill(0.3))
            self.play(Write(question), run_time=t.fill(0.25))
            t.hold()

        have_label = serif("have", LABEL_SIZE, GREY)
        have = MathTex("3x + 12", font_size=DISPLAY_SIZE, color=CHARCOAL)
        have.next_to(have_label, DOWN, buff=GAP_SM * 1.4)
        have_col = VGroup(have_label, have)
        have_col.move_to(np.array([-3.4, 0.1, 0]))

        want_label = serif("want", LABEL_SIZE, GREY)
        want = MathTex("x + 4", font_size=DISPLAY_SIZE, color=CHARCOAL)
        want.next_to(want_label, DOWN, buff=GAP_SM * 1.4)
        want_col = VGroup(want_label, want)
        want_col.move_to(np.array([3.4, 0.1, 0]))

        with self.beat("compare") as t:
            self.play(Write(have_col), run_time=t.fill(0.25))
            self.play(Write(want_col), run_time=t.fill(0.25))
            t.hold()

        times3 = MathTex(
            "3x = 3 \\cdot x \\qquad 12 = 3 \\cdot 4",
            font_size=EQUATION_SIZE, color=TERRACOTTA,
        )
        times3.move_to(DOWN * 1.5)
        magnified = serif("the same expression, magnified by 3", LABEL_SIZE, GREY)
        magnified.next_to(times3, DOWN, buff=GAP_MD)

        with self.beat("structure") as t:
            self.play(Write(times3), run_time=t.fill(0.3))
            self.play(Write(magnified), run_time=t.fill(0.2))
            t.hold()

        self._compare_group = VGroup(have_col, want_col, times3, magnified)

    def shortcut(self):
        scale_note = serif("a balanced scale — equal signs mean equal value",
                           BODY_SIZE)
        scale_note.move_to(DOWN * 2.9)

        with self.beat("equivalence") as t:
            self.play(
                self._compare_group.animate.shift(UP * 0.4),
                run_time=t.fill(0.1),
            )
            self.play(Write(scale_note), run_time=t.fill(0.3))
            t.hold()

        divide_note = serif("divide both sides by 3 — one step", BODY_SIZE)
        divide_note.move_to(DOWN * 2.9)

        with self.beat("divide") as t:
            self.play(FadeOut(scale_note), run_time=t.fill(0.08))
            self.play(*[FadeOut(m) for m in self._compare_group[2:]],
                      run_time=t.fill(0.08))
            self.play(Write(divide_note), run_time=t.fill(0.25))
            self.play(Create(underline(divide_note)), run_time=t.fill(0.12))
            t.hold()

        left = MathTex(
            "\\frac{3x + 12}{3}", "=", "x + 4",
            font_size=DISPLAY_SIZE, color=CHARCOAL,
        )
        left.move_to(np.array([-3.4, -1.2, 0]))

        with self.beat("divide_left") as t:
            self.play(Write(left), run_time=t.fill(0.4))
            t.hold()

        right = MathTex(
            "\\frac{30}{3}", "=", "10",
            font_size=DISPLAY_SIZE, color=CHARCOAL,
        )
        right.move_to(np.array([3.4, -1.2, 0]))

        with self.beat("divide_right") as t:
            self.play(Write(right), run_time=t.fill(0.4))
            t.hold()

        result = MathTex("x + 4 = 10", font_size=DISPLAY_SIZE, color=CHARCOAL)
        result.set_color(SAGE)
        result.move_to(DOWN * 2.9)

        with self.beat("result") as t:
            self.play(FadeOut(divide_note), run_time=t.fill(0.08))
            self.play(Write(result), run_time=t.fill(0.3))
            self.play(Create(underline(result)), run_time=t.fill(0.12))
            t.hold()

        self._shortcut_group = VGroup(
            self._compare_group[0], self._compare_group[1], left, right, result
        )

    def comparison(self):
        steps = VGroup(
            MathTex("3x = 18", font_size=EQUATION_SIZE, color=GREY),
            MathTex("x = 6", font_size=EQUATION_SIZE, color=GREY),
            MathTex("6 + 4 = 10", font_size=EQUATION_SIZE, color=GREY),
        ).arrange(DOWN, buff=GAP_SM * 1.5)
        steps_label = serif("the standard recipe", LABEL_SIZE, GREY)
        standard = VGroup(steps_label, steps).arrange(DOWN, buff=GAP_MD)
        standard.move_to(np.array([-3.4, -0.9, 0]))

        with self.beat("standard") as t:
            self.play(
                *[FadeOut(m) for m in self._shortcut_group[:4]],
                self._shortcut_group[4].animate.move_to(
                    np.array([3.4, -0.9, 0])
                ),
                run_time=t.fill(0.12),
            )
            self.play(Write(standard), run_time=t.fill(0.45))
            t.hold()

        three = serif("three calculations", LABEL_SIZE, GREY)
        three.next_to(standard, DOWN, buff=GAP_MD)
        one = serif("one step", LABEL_SIZE, SAGE)
        one.next_to(self._shortcut_group[4], DOWN, buff=GAP_MD * 2.2)

        with self.beat("compare_ways") as t:
            self.play(Write(three), run_time=t.fill(0.2))
            self.play(Write(one), run_time=t.fill(0.2))
            t.hold()

        self._comparison_group = VGroup(
            standard, three, one, self._shortcut_group[4]
        )

    def recap(self):
        head = serif("Investigate, don't just calculate", TITLE_SIZE * 0.95)
        head.to_edge(UP, buff=GAP_MD * 1.6)

        with self.beat("recap") as t:
            self.play(
                FadeOut(self.card),
                *[FadeOut(m) for m in self._comparison_group],
                run_time=t.fill(0.12),
            )
            self.play(Write(head), run_time=t.fill(0.3))
            t.hold()

        items = VGroup(
            serif("compare — what do I have, what do I want?", BODY_SIZE),
            serif("find the factor — multiply or divide to get there", BODY_SIZE),
            serif("balance the scale — same operation on both sides", BODY_SIZE),
        ).arrange(DOWN, buff=GAP_MD, aligned_edge=LEFT)
        items.next_to(head, DOWN, buff=GAP_MD * 1.6)

        with self.beat("recap_list") as t:
            self.play(Write(items), run_time=t.fill(0.5))
            t.hold()

        closing = serif("the bridge from beginner to expert", LABEL_SIZE, GREY)
        closing.next_to(items, DOWN, buff=GAP_MD * 1.6)

        with self.beat("outro") as t:
            self.play(Write(closing), run_time=t.fill(0.3))
            t.hold()
