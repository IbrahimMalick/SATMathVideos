"""Worked problem: translating a word problem into an equation (Algebra Q1).

Narration script: scripts/Q01-algebra-translating.md
The problem and choices stay on screen from the reveal onward; the work
area below and beside them rotates through cues, the equation build, other
representations, and verification.
"""

import textwrap

import numpy as np

from manim import (
    Axes,
    Create,
    FadeOut,
    Line,
    MathTex,
    Text,
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
    EQUATION_SIZE,
    DISPLAY_SIZE,
    GAP_MD,
    GAP_SM,
    GREY,
    LABEL_SIZE,
    MARGIN_SIZE,
    SAGE,
    SERIF_FONT,
    SLATE,
    TERRACOTTA,
    TITLE_SIZE,
    mono,
    serif,
)
from components.answer_choices import AnswerChoices
from components.table import make_table
from scenes.base import SATScene

PROBLEM = (
    "A delivery service charges a flat processing fee of $12 plus an "
    "additional $0.75 per pound for shipping. If the total charge for a "
    "shipment was $21, which equation represents the weight of the "
    "shipment, w, in pounds?"
)


def underline(mobject, color=SAGE):
    return Line(
        mobject.get_corner(DOWN + LEFT) + DOWN * GAP_SM,
        mobject.get_corner(DOWN + RIGHT) + DOWN * GAP_SM,
        color=color,
        stroke_width=3,
    )


class AlgebraQ1(SATScene):
    scene_id = "worked.algebra_q1"

    WORK_X = 3.3   # centre of the right-hand work column

    def construct(self):
        self.margin_note = mono("Q01 · translating words", MARGIN_SIZE)
        self.margin_note.to_corner(UP + LEFT, buff=GAP_SM)
        self.add(self.margin_note)
        self.work = VGroup()   # rotating work-area content

        self.intro()
        self.show_problem()
        self.three_cues()
        self.build_equation()
        self.other_languages()
        self.verification()
        self.wrap_up()

    def swap_work(self, t, fraction=0.1):
        """Fade out the current work-area content."""
        if len(self.work) > 0:
            self.play(*[FadeOut(m) for m in self.work], run_time=t.fill(fraction))
            self.work = VGroup()

    # ------------------------------------------------------------ sections

    def intro(self):
        title = serif("SAT Algebra · Practice", TITLE_SIZE * 1.15)
        subtitle = serif("Q1 · translating word problems", BODY_SIZE, GREY)
        subtitle.next_to(title, DOWN, buff=GAP_MD)
        VGroup(title, subtitle).to_edge(UP, buff=GAP_MD * 1.6)

        with self.beat("title") as t:
            self.play(Write(title), run_time=t.fill(0.4))
            self.play(Write(subtitle), run_time=t.fill(0.25))
            t.hold()

        topics = VGroup(
            *[
                serif(line, LABEL_SIZE)
                for line in [
                    "translating word problems",
                    "recognizing equivalent expressions",
                    "solving systems of equations",
                    "interpreting linear coefficients",
                    "constructing the equation of a line",
                ]
            ]
        ).arrange(DOWN, buff=GAP_SM * 1.2, aligned_edge=LEFT)
        topics.next_to(subtitle, DOWN, buff=GAP_MD * 1.3)

        with self.beat("topics") as t:
            self.play(Write(topics), run_time=t.fill(0.5))
            t.hold()

        fmt = serif("read · pause and attempt · solve step by step",
                    LABEL_SIZE, GREY)
        fmt.next_to(topics, DOWN, buff=GAP_MD * 1.2)

        with self.beat("format") as t:
            self.play(Write(fmt), run_time=t.fill(0.3))
            t.hold()

        goal = serif("from English into the language of algebra", LABEL_SIZE, GREY)
        goal.next_to(fmt, DOWN, buff=GAP_MD)

        with self.beat("lesson_goal") as t:
            self.play(Write(goal), run_time=t.fill(0.3))
            t.hold()

        model = serif("linear — it changes at a constant rate", BODY_SIZE)
        model.next_to(goal, DOWN, buff=GAP_MD)

        with self.beat("model") as t:
            self.play(Write(model), run_time=t.fill(0.3))
            self.play(Create(underline(model)), run_time=t.fill(0.15))
            t.hold()

        self._intro_group = VGroup(title, subtitle, topics, fmt, goal, model)

    def show_problem(self):
        problem = Text(
            textwrap.fill(PROBLEM, 62),
            font=SERIF_FONT,
            font_size=MARGIN_SIZE,
            color=CHARCOAL,
            line_spacing=1.1,
        )
        problem.to_edge(UP, buff=GAP_MD * 1.9)

        choices = AnswerChoices(
            [
                MathTex("12w + 0.75 = 21", font_size=EQUATION_SIZE, color=CHARCOAL),
                MathTex("0.75w + 12 = 21", font_size=EQUATION_SIZE, color=CHARCOAL),
                MathTex("12.75w = 21", font_size=EQUATION_SIZE, color=CHARCOAL),
                MathTex("0.75w - 12 = 21", font_size=EQUATION_SIZE, color=CHARCOAL),
            ]
        )
        choices.next_to(problem, DOWN, buff=GAP_MD * 1.3)
        choices.move_to(np.array([-3.8, choices.get_center()[1], 0]))
        self.problem = problem
        self.choices = choices

        with self.beat("problem") as t:
            self.play(*[FadeOut(m) for m in self._intro_group], run_time=t.fill(0.15))
            self.play(Write(problem), run_time=t.fill(0.35))
            self.play(Write(choices), run_time=t.fill(0.3))
            t.hold()

        pause_note = mono("pause — try it yourself", MARGIN_SIZE)
        pause_note.to_edge(DOWN, buff=GAP_MD)

        with self.beat("pause") as t:
            self.play(Write(pause_note), run_time=t.fill(0.15))
            t.hold()

        with self.beat("answer") as t:
            self.play(FadeOut(pause_note), run_time=t.fill(0.08))
            self.play(*self.choices.confirm("B"), run_time=t.fill(0.3))
            t.hold()

    def three_cues(self):
        mxb = MathTex(
            "y", "=", "m", "x", "+", "b",
            font_size=DISPLAY_SIZE, color=GREY,
        )
        mxb.move_to(np.array([self.WORK_X, 0.65, 0]))

        cue1 = VGroup(
            serif("the anchor — happens once", LABEL_SIZE),
            serif("flat fee: 12", LABEL_SIZE, TERRACOTTA),
        ).arrange(DOWN, buff=GAP_SM, aligned_edge=LEFT)
        cue1.next_to(mxb, DOWN, buff=GAP_SM * 1.5)
        cue1.move_to(np.array([self.WORK_X, cue1.get_center()[1], 0]))

        with self.beat("cue_constant") as t:
            self.play(Write(mxb), run_time=t.fill(0.2))
            self.play(mxb[5].animate.set_color(TERRACOTTA), run_time=t.fill(0.08))
            self.play(Write(cue1), run_time=t.fill(0.25))
            t.hold()

        cue2 = VGroup(
            serif("the jumper — per, each, every", LABEL_SIZE),
            serif("rate: 0.75 per pound", LABEL_SIZE, TERRACOTTA),
        ).arrange(DOWN, buff=GAP_SM, aligned_edge=LEFT)
        cue2.next_to(cue1, DOWN, buff=GAP_SM * 1.5, aligned_edge=LEFT)

        with self.beat("cue_rate") as t:
            self.play(
                mxb[5].animate.set_color(GREY),
                cue1[1].animate.set_color(CHARCOAL),
                run_time=t.fill(0.08),
            )
            self.play(mxb[2].animate.set_color(TERRACOTTA), run_time=t.fill(0.08))
            self.play(Write(cue2), run_time=t.fill(0.25))
            t.hold()

        cue3 = VGroup(
            serif("the result of the story", LABEL_SIZE),
            serif("total: 21", LABEL_SIZE, TERRACOTTA),
        ).arrange(DOWN, buff=GAP_SM, aligned_edge=LEFT)
        cue3.next_to(cue2, DOWN, buff=GAP_SM * 1.5, aligned_edge=LEFT)

        with self.beat("cue_total") as t:
            self.play(
                mxb[2].animate.set_color(GREY),
                cue2[1].animate.set_color(CHARCOAL),
                run_time=t.fill(0.08),
            )
            self.play(Write(cue3), run_time=t.fill(0.25))
            t.hold()

        self.work = VGroup(mxb, cue1, cue2, cue3)

    def build_equation(self):
        step1 = MathTex("0.75w", font_size=DISPLAY_SIZE, color=CHARCOAL)
        step2 = MathTex("0.75w", "+", "12", font_size=DISPLAY_SIZE, color=CHARCOAL)
        step3 = MathTex(
            "0.75w", "+", "12", "=", "21",
            font_size=DISPLAY_SIZE, color=CHARCOAL,
        )
        for step in (step1, step2, step3):
            step.move_to(np.array([self.WORK_X, -0.5, 0]))

        with self.beat("build_var") as t:
            self.swap_work(t)
            label = serif("rate × variable", LABEL_SIZE, GREY)
            label.move_to(np.array([self.WORK_X, 0.55, 0]))
            self.play(Write(label), run_time=t.fill(0.15))
            self.play(Write(step1), run_time=t.fill(0.3))
            self.work.add(label)
            t.hold()

        with self.beat("build_fix") as t:
            self.play(TransformMatchingTex(step1, step2), run_time=t.fill(0.4))
            t.hold()

        with self.beat("build_total") as t:
            self.play(TransformMatchingTex(step2, step3), run_time=t.fill(0.35))
            self.play(Create(underline(self.choices.rows["B"])), run_time=t.fill(0.2))
            t.hold()

        self.work.add(step3)

    def other_languages(self):
        table, _cells = make_table(
            ["pounds", "cost"],
            [[0, "$12.00"], [1, "$12.75"], [2, "$13.50"]],
            col_widths=[1.9, 1.9],
        )
        table.scale(0.9)
        table.move_to(np.array([1.5, -2.2, 0]))

        with self.beat("table_lang") as t:
            self.swap_work(t)
            self.play(Write(table), run_time=t.fill(0.35))
            self.work.add(table)
            t.hold()

        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 24, 6],
            x_length=2.6,
            y_length=2.4,
            axis_config={"color": CHARCOAL, "include_ticks": False,
                         "tip_length": 0.12},
        )
        axes.move_to(np.array([5.5, -2.2, 0]))
        line = axes.plot(lambda x: 12 + 0.75 * x * 4, x_range=[0, 3.8], color=SLATE)
        intercept = MathTex("12", font_size=MARGIN_SIZE, color=CHARCOAL)
        intercept.next_to(axes.c2p(0, 12), LEFT, buff=GAP_SM * 0.8)

        with self.beat("graph_lang") as t:
            self.play(Create(axes), run_time=t.fill(0.15))
            self.play(Create(line), run_time=t.fill(0.25))
            self.play(Write(intercept), run_time=t.fill(0.1))
            self.work.add(axes, line, intercept)
            t.hold()

    def verification(self):
        head = serif("test a value: w = 10", BODY_SIZE)
        head.move_to(np.array([self.WORK_X, 0.6, 0]))

        with self.beat("verify") as t:
            self.swap_work(t)
            self.play(Write(head), run_time=t.fill(0.25))
            self.play(Create(underline(head)), run_time=t.fill(0.12))
            self.work.add(head)
            t.hold()

        check_b = MathTex(
            "0.75(10) + 12", "=", "19.50",
            font_size=EQUATION_SIZE, color=CHARCOAL,
        )
        check_b[2].set_color(SAGE)
        check_b.next_to(head, DOWN, buff=GAP_MD * 1.3)
        check_b.move_to(np.array([self.WORK_X, check_b.get_center()[1], 0]))

        with self.beat("verify_b") as t:
            self.play(Write(check_b), run_time=t.fill(0.35))
            self.work.add(check_b)
            t.hold()

        check_a = MathTex(
            "12(10) + 0.75", "=", "120.75",
            font_size=EQUATION_SIZE, color=CHARCOAL,
        )
        check_a[2].set_color(TERRACOTTA)
        check_a.next_to(check_b, DOWN, buff=GAP_MD)
        check_a.move_to(np.array([self.WORK_X, check_a.get_center()[1], 0]))

        with self.beat("verify_a") as t:
            self.play(Write(check_a), run_time=t.fill(0.3))
            self.play(*self.choices.eliminate("A"), run_time=t.fill(0.2))
            self.work.add(check_a)
            t.hold()

    def wrap_up(self):
        lines = VGroup(
            serif("starting amount → the constant b", LABEL_SIZE),
            serif("jump per unit → the rate m", LABEL_SIZE),
            serif("final result → what it equals", LABEL_SIZE),
        ).arrange(DOWN, buff=GAP_SM * 1.5, aligned_edge=LEFT)
        lines.move_to(np.array([self.WORK_X, -0.2, 0]))

        with self.beat("wrap") as t:
            self.swap_work(t)
            self.play(Write(lines), run_time=t.fill(0.45))
            self.work.add(lines)
            t.hold()

        closing = serif("you're building a model of the real world", BODY_SIZE)
        closing.to_edge(DOWN, buff=GAP_MD * 1.2)

        with self.beat("outro") as t:
            self.play(Write(closing), run_time=t.fill(0.3))
            self.play(Create(underline(closing)), run_time=t.fill(0.15))
            t.hold()
