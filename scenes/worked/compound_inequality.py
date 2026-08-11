"""Worked problem: compound inequality (cricket rating, Q04).

Narration script: scripts/Q04-compound-inequality.md
The rating formula stays up top; the inequality transforms step by step,
then a number line shows the capped range.
"""

import numpy as np

from manim import (
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
from scenes.base import SATScene


def underline(mobject, color=SAGE):
    return Line(
        mobject.get_corner(DOWN + LEFT) + DOWN * GAP_SM,
        mobject.get_corner(DOWN + RIGHT) + DOWN * GAP_SM,
        color=color,
        stroke_width=3,
    )


class CompoundInequality(SATScene):
    scene_id = "worked.compound_inequality"

    def construct(self):
        self.margin_note = mono("Q04 · compound inequality", MARGIN_SIZE)
        self.margin_note.to_corner(UP + LEFT, buff=GAP_SM)
        self.add(self.margin_note)

        hook = serif("84 in practice — can Ali still reach a 90 rating?",
                     BODY_SIZE)
        hook.move_to(UP * 0.8)
        hook_line = underline(hook, TERRACOTTA)

        with self.beat("hook") as t:
            self.play(Write(hook), run_time=t.fill(0.35))
            self.play(Create(hook_line), run_time=t.fill(0.12))
            t.hold()

        weights = VGroup(
            serif("40% — practice performance", LABEL_SIZE),
            serif("60% — final batting trial", LABEL_SIZE),
        ).arrange(DOWN, buff=GAP_SM * 1.4, aligned_edge=LEFT)
        weights.next_to(hook, DOWN, buff=GAP_MD * 1.4)

        with self.beat("setup") as t:
            self.play(Write(weights), run_time=t.fill(0.4))
            t.hold()

        rating = MathTex(
            "\\text{rating}", "=", "0.4(84)", "+", "0.6x",
            font_size=EQUATION_SIZE, color=CHARCOAL,
        )
        rating.to_edge(UP, buff=GAP_MD * 1.8)

        with self.beat("ali") as t:
            self.play(FadeOut(hook), FadeOut(hook_line),
                      FadeOut(weights), run_time=t.fill(0.1))
            self.play(Write(rating), run_time=t.fill(0.35))
            t.hold()

        ineq1 = MathTex(
            "90", "\\le", "0.4(84) + 0.6x", "\\le", "100",
            font_size=DISPLAY_SIZE, color=CHARCOAL,
        )
        ineq2 = MathTex(
            "90", "\\le", "33.6 + 0.6x", "\\le", "100",
            font_size=DISPLAY_SIZE, color=CHARCOAL,
        )
        ineq3 = MathTex(
            "56.4", "\\le", "0.6x", "\\le", "66.4",
            font_size=DISPLAY_SIZE, color=CHARCOAL,
        )
        ineq4 = MathTex(
            "94", "\\le", "x", "\\le", "110.7",
            font_size=DISPLAY_SIZE, color=CHARCOAL,
        )
        for ineq in (ineq1, ineq2, ineq3, ineq4):
            ineq.move_to(UP * 0.4)

        with self.beat("target") as t:
            self.play(Write(ineq1), run_time=t.fill(0.4))
            t.hold()

        label = serif("a compound inequality — a minimum and a maximum",
                      LABEL_SIZE)
        label.next_to(ineq1, DOWN, buff=GAP_MD * 1.3)
        label_line = underline(label)

        with self.beat("compound") as t:
            self.play(Write(label), run_time=t.fill(0.3))
            self.play(Create(label_line), run_time=t.fill(0.12))
            t.hold()

        step_note = serif("0.4 × 84 = 33.6", LABEL_SIZE, GREY)
        step_note.next_to(label, DOWN, buff=GAP_MD * 1.2)

        with self.beat("step1") as t:
            self.play(Write(step_note), run_time=t.fill(0.15))
            self.play(TransformMatchingTex(ineq1, ineq2), run_time=t.fill(0.35))
            t.hold()

        step2_note = serif("subtract 33.6 from all three parts", LABEL_SIZE, GREY)
        step2_note.move_to(step_note)

        with self.beat("step2") as t:
            self.play(FadeOut(step_note), run_time=t.fill(0.06))
            self.play(Write(step2_note), run_time=t.fill(0.12))
            self.play(TransformMatchingTex(ineq2, ineq3), run_time=t.fill(0.35))
            t.hold()

        step3_note = serif("divide everything by 0.6", LABEL_SIZE, GREY)
        step3_note.move_to(step2_note)

        with self.beat("step3") as t:
            self.play(FadeOut(step2_note), run_time=t.fill(0.06))
            self.play(Write(step3_note), run_time=t.fill(0.12))
            self.play(TransformMatchingTex(ineq3, ineq4), run_time=t.fill(0.35))
            t.hold()

        catch = serif("the trial is scored out of 100", LABEL_SIZE, TERRACOTTA)
        catch.move_to(step3_note)
        capped = MathTex(
            "94", "\\le", "x", "\\le", "100",
            font_size=DISPLAY_SIZE, color=CHARCOAL,
        )
        capped.move_to(ineq4)

        # Number line: 90 to 112, sage segment 94-100.
        def nl_x(v):
            return -4.0 + (v - 88) * 0.32

        base = -2.4
        nline = Line(np.array([nl_x(88), base, 0]), np.array([nl_x(112), base, 0]),
                     color=CHARCOAL, stroke_width=2)
        seg = Line(np.array([nl_x(94), base, 0]), np.array([nl_x(100), base, 0]),
                   color=SAGE, stroke_width=7)
        d94 = Dot(np.array([nl_x(94), base, 0]), color=SAGE, radius=0.09)
        d100 = Dot(np.array([nl_x(100), base, 0]), color=SAGE, radius=0.09)
        l94 = MathTex("94", font_size=MARGIN_SIZE, color=CHARCOAL)
        l94.next_to(d94, DOWN, buff=GAP_SM)
        l100 = MathTex("100", font_size=MARGIN_SIZE, color=CHARCOAL)
        l100.next_to(d100, DOWN, buff=GAP_SM)
        l110 = MathTex("110.7", font_size=MARGIN_SIZE, color=GREY)
        l110.next_to(np.array([nl_x(110.7), base, 0]), DOWN, buff=GAP_SM)

        with self.beat("catch") as t:
            self.play(FadeOut(step3_note), run_time=t.fill(0.06))
            self.play(Write(catch), run_time=t.fill(0.15))
            self.play(TransformMatchingTex(ineq4, capped), run_time=t.fill(0.25))
            self.play(Create(nline), run_time=t.fill(0.12))
            self.play(Create(seg), Create(d94), Create(d100), run_time=t.fill(0.15))
            self.play(Write(l94), Write(l100), Write(l110), run_time=t.fill(0.12))
            t.hold()

        answer = serif("Ali needs at least 94 on the batting trial", BODY_SIZE)
        answer.to_edge(DOWN, buff=GAP_MD)
        answer_line = underline(answer)

        with self.beat("answer") as t:
            self.play(Write(answer), run_time=t.fill(0.3))
            self.play(Create(answer_line), run_time=t.fill(0.12))
            t.hold()

        key = serif("a minimum and a maximum?  think compound inequality",
                    BODY_SIZE)
        key.move_to(UP * 1.4)

        with self.beat("key") as t:
            old = [m for m in self.mobjects if m is not self.margin_note]
            self.play(*[FadeOut(m) for m in old], run_time=t.fill(0.1))
            self.play(Write(key), run_time=t.fill(0.3))
            self.play(Create(underline(key)), run_time=t.fill(0.12))
            t.hold()

        boundaries = serif("like cricket boundaries — stay inside the limits",
                           LABEL_SIZE, GREY)
        boundaries.next_to(key, DOWN, buff=GAP_MD * 1.5)

        with self.beat("boundaries") as t:
            self.play(Write(boundaries), run_time=t.fill(0.35))
            t.hold()
