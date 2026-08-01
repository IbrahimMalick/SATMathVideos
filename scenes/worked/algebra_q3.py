"""Worked problem: systems of equations by substitution (Algebra Q3).

Narration script: scripts/Q03-systems-substitution.md
The system card stays on screen from its reveal; the work area rotates
through tool choice, the disguise, the three solving steps, the graph of
both lines with their intersection, and the recap.
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


class AlgebraQ3(SATScene):
    scene_id = "worked.algebra_q3"

    WORK_X = 3.4

    def construct(self):
        self.margin_note = mono("Q03 · substitution", MARGIN_SIZE)
        self.margin_note.to_corner(UP + LEFT, buff=GAP_SM)
        self.add(self.margin_note)
        self.work = VGroup()

        self.intro()
        self.clues_and_system()
        self.choose_tool()
        self.solve()
        self.cartesian()
        self.recap()

    def swap_work(self, t, fraction=0.1):
        if len(self.work) > 0:
            self.play(*[FadeOut(m) for m in self.work], run_time=t.fill(fraction))
            self.work = VGroup()

    # ------------------------------------------------------------ sections

    def intro(self):
        title = serif("Systems of Equations", TITLE_SIZE * 1.15)
        subtitle = serif("Q3 · the substitution method", BODY_SIZE, GREY)
        subtitle.next_to(title, DOWN, buff=GAP_MD)
        VGroup(title, subtitle).move_to(UP * 1.2)

        with self.beat("title") as t:
            self.play(Write(title), run_time=t.fill(0.4))
            self.play(Write(subtitle), run_time=t.fill(0.25))
            t.hold()

        why = serif("several rules, interacting at the same time", LABEL_SIZE, GREY)
        why.next_to(subtitle, DOWN, buff=GAP_MD * 1.5)

        with self.beat("why") as t:
            self.play(Write(why), run_time=t.fill(0.3))
            t.hold()

        method = serif("today: substitution", BODY_SIZE)
        method.next_to(why, DOWN, buff=GAP_MD * 1.2)
        method_line = underline(method)

        with self.beat("method_intro") as t:
            self.play(Write(method), run_time=t.fill(0.3))
            self.play(Create(method_line), run_time=t.fill(0.12))
            t.hold()

        self._intro_group = VGroup(title, subtitle, why, method, method_line)

    def clues_and_system(self):
        clue1 = serif("clue 1 — two numbers add up to 25", BODY_SIZE)
        clue2 = serif("clue 2 — x is four times as large as y", BODY_SIZE)
        clues = VGroup(clue1, clue2).arrange(DOWN, buff=GAP_MD, aligned_edge=LEFT)
        clues.move_to(UP * 0.3)

        with self.beat("clues") as t:
            self.play(*[FadeOut(m) for m in self._intro_group],
                      run_time=t.fill(0.12))
            self.play(Write(clue1), run_time=t.fill(0.3))
            self.play(Write(clue2), run_time=t.fill(0.3))
            t.hold()

        eq1 = MathTex("1.\\quad x + y = 25", font_size=EQUATION_SIZE, color=CHARCOAL)
        eq2 = MathTex("2.\\quad x = 4y", font_size=EQUATION_SIZE, color=CHARCOAL)
        system = VGroup(eq1, eq2).arrange(DOWN, buff=GAP_SM * 1.4, aligned_edge=LEFT)
        system.to_edge(UP, buff=GAP_MD * 1.8)
        goal = serif("find the one pair (x, y) that fits both", LABEL_SIZE, GREY)
        goal.next_to(system, DOWN, buff=GAP_MD)
        self.system = system
        self.eq1, self.eq2 = eq1, eq2

        with self.beat("system") as t:
            self.play(FadeOut(clue1), FadeOut(clue2), run_time=t.fill(0.1))
            self.play(Write(system), run_time=t.fill(0.35))
            self.play(Write(goal), run_time=t.fill(0.2))
            self.work.add(goal)
            t.hold()

    def choose_tool(self):
        tools = VGroup(
            serif("graphing", LABEL_SIZE),
            serif("elimination", LABEL_SIZE),
            serif("substitution", LABEL_SIZE),
        ).arrange(DOWN, buff=GAP_SM * 1.3, aligned_edge=LEFT)
        tools.move_to(np.array([-3.8, -0.6, 0]))
        expert = serif("the expert reads the structure first", LABEL_SIZE, GREY)
        expert.next_to(tools, DOWN, buff=GAP_MD)
        expert.move_to(np.array([-3.4, expert.get_center()[1], 0]))

        with self.beat("tool") as t:
            self.swap_work(t)
            self.play(Write(tools), run_time=t.fill(0.35))
            self.play(Write(expert), run_time=t.fill(0.2))
            self.work.add(tools, expert)
            t.hold()

        cue_note = VGroup(
            serif("x is already isolated —", LABEL_SIZE),
            serif("a massive math cue", LABEL_SIZE, TERRACOTTA),
        ).arrange(DOWN, buff=GAP_SM, aligned_edge=LEFT)
        cue_note.move_to(np.array([self.WORK_X, -0.7, 0]))

        sub_line = underline(tools[2])

        with self.beat("cue") as t:
            self.play(self.eq2.animate.set_color(TERRACOTTA), run_time=t.fill(0.1))
            self.play(Create(sub_line), run_time=t.fill(0.1))
            self.play(Write(cue_note), run_time=t.fill(0.25))
            self.work.add(cue_note, sub_line)
            t.hold()

        disguise = MathTex(
            "x \\;\\longrightarrow\\; 4y",
            font_size=DISPLAY_SIZE, color=CHARCOAL,
        )
        disguise.move_to(np.array([self.WORK_X, -2.4, 0]))
        disguise_note = serif("same value, different form", LABEL_SIZE, GREY)
        disguise_note.next_to(disguise, DOWN, buff=GAP_SM * 1.4)

        with self.beat("disguise") as t:
            self.play(self.eq2.animate.set_color(CHARCOAL), run_time=t.fill(0.08))
            self.play(Write(disguise), run_time=t.fill(0.3))
            self.play(Write(disguise_note), run_time=t.fill(0.15))
            self.work.add(disguise, disguise_note)
            t.hold()

    def solve(self):
        step1a = MathTex("x + y = 25", font_size=DISPLAY_SIZE, color=CHARCOAL)
        step1b = MathTex("4y + y = 25", font_size=DISPLAY_SIZE, color=CHARCOAL)
        step2 = MathTex("5y = 25", font_size=DISPLAY_SIZE, color=CHARCOAL)
        step3 = MathTex("y = 5", font_size=DISPLAY_SIZE, color=CHARCOAL)
        for s in (step1a, step1b, step2, step3):
            s.move_to(DOWN * 0.9)

        label1 = serif("step 1 — perform the swap", LABEL_SIZE, GREY)
        label1.move_to(UP * 0.3)

        with self.beat("step1") as t:
            self.swap_work(t)
            self.play(Write(label1), run_time=t.fill(0.15))
            self.play(Write(step1a), run_time=t.fill(0.2))
            self.play(TransformMatchingTex(step1a, step1b), run_time=t.fill(0.25))
            self.work.add(label1)
            t.hold()

        label2 = serif("step 2 — combine like terms", LABEL_SIZE, GREY)
        label2.move_to(UP * 0.3)

        with self.beat("step2") as t:
            self.play(FadeOut(label1), run_time=t.fill(0.06))
            self.work.remove(label1)
            self.play(Write(label2), run_time=t.fill(0.12))
            self.play(TransformMatchingTex(step1b, step2), run_time=t.fill(0.3))
            self.work.add(label2)
            t.hold()

        label3 = serif("step 3 — divide both sides by 5", LABEL_SIZE, GREY)
        label3.move_to(UP * 0.3)

        with self.beat("step3") as t:
            self.play(FadeOut(label2), run_time=t.fill(0.06))
            self.work.remove(label2)
            self.play(Write(label3), run_time=t.fill(0.12))
            self.play(TransformMatchingTex(step2, step3), run_time=t.fill(0.3))
            self.work.add(label3)
            t.hold()

        conclusion_line = underline(step3)

        with self.beat("conclusion") as t:
            self.play(step3.animate.set_color(SAGE), run_time=t.fill(0.12))
            self.play(Create(conclusion_line), run_time=t.fill(0.12))
            t.hold()

        self.work.add(step3, conclusion_line)

    def cartesian(self):
        axes = Axes(
            x_range=[0, 30, 5],
            y_range=[0, 30, 5],
            x_length=5.2,
            y_length=4.2,
            axis_config={"color": CHARCOAL, "include_ticks": False,
                         "tip_length": 0.15},
        )
        axes.move_to(np.array([-3.2, -1.1, 0]))
        line1 = axes.plot(lambda x: 25 - x, x_range=[0, 28], color=SLATE)
        line2 = axes.plot(lambda x: x / 4, x_range=[0, 28], color=CHARCOAL)
        l1_label = MathTex("x + y = 25", font_size=MARGIN_SIZE, color=SLATE)
        l1_label.next_to(axes.c2p(4, 21), RIGHT, buff=GAP_SM)
        l2_label = MathTex("x = 4y", font_size=MARGIN_SIZE, color=CHARCOAL)
        l2_label.next_to(axes.c2p(24, 6), UP, buff=GAP_SM)

        with self.beat("cartesian") as t:
            self.swap_work(t)
            self.play(Create(axes), run_time=t.fill(0.2))
            self.play(Create(line1), Write(l1_label), run_time=t.fill(0.25))
            self.play(Create(line2), Write(l2_label), run_time=t.fill(0.25))
            self.work.add(axes, line1, line2, l1_label, l2_label)
            t.hold()

        meet = serif("the point where the lines cross", LABEL_SIZE, GREY)
        meet.move_to(np.array([self.WORK_X, 0.2, 0]))

        with self.beat("intersection") as t:
            self.play(Write(meet), run_time=t.fill(0.3))
            self.work.add(meet)
            t.hold()

        plug = MathTex(
            "x = 4(5) = 20", font_size=EQUATION_SIZE, color=CHARCOAL
        )
        plug.next_to(meet, DOWN, buff=GAP_MD)
        point = Dot(axes.c2p(20, 5), color=TERRACOTTA, radius=0.09)
        point_label = MathTex("(20, 5)", font_size=EQUATION_SIZE, color=TERRACOTTA)
        point_label.next_to(point, UP + RIGHT, buff=GAP_SM * 0.8)

        with self.beat("plug") as t:
            self.play(Write(plug), run_time=t.fill(0.25))
            self.play(Create(VGroup(point, point_label)), run_time=t.fill(0.2))
            self.work.add(plug, point, point_label)
            t.hold()

    def recap(self):
        head = serif("Wrap it up", TITLE_SIZE)
        head.to_edge(UP, buff=GAP_MD * 1.6)

        line1 = serif("is one variable already solved for?  substitution",
                      BODY_SIZE)

        with self.beat("recap") as t:
            self.play(FadeOut(self.system), run_time=t.fill(0.06))
            self.swap_work(t, fraction=0.06)
            self.play(Write(head), run_time=t.fill(0.2))
            line1.next_to(head, DOWN, buff=GAP_MD * 1.6)
            self.play(Write(line1), run_time=t.fill(0.3))
            t.hold()

        rest = VGroup(
            serif("use the disguise — swap for the equivalent", BODY_SIZE),
            serif("preserve the balance — same operation, both sides", BODY_SIZE),
        ).arrange(DOWN, buff=GAP_MD, aligned_edge=LEFT)
        rest.next_to(line1, DOWN, buff=GAP_MD, aligned_edge=LEFT)

        with self.beat("recap2") as t:
            self.play(Write(rest), run_time=t.fill(0.4))
            t.hold()

        closing = serif("next: the elimination method", LABEL_SIZE, GREY)
        closing.next_to(rest, DOWN, buff=GAP_MD * 1.6)

        with self.beat("outro") as t:
            self.play(Write(closing), run_time=t.fill(0.3))
            t.hold()
