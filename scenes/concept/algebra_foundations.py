"""Concept lecture: Algebra — the foundation of SAT math.

Narration script: scripts/L01-algebra-foundations.md
Eight sections; content clears between them, the margin note persists.
"""

import numpy as np

from manim import (
    Create,
    Dot,
    FadeOut,
    Line,
    MathTex,
    Text,
    TransformMatchingTex,
    VGroup,
    Write,
    Axes,
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
    MONO_FONT,
    SAGE,
    SERIF_FONT,
    SLATE,
    TERRACOTTA,
    TITLE_SIZE,
)
from scenes.base import SATScene


def serif(text, size=BODY_SIZE, color=CHARCOAL):
    return Text(text, font=SERIF_FONT, font_size=size, color=color)


def make_table(headers, rows, row_height=0.6, col_widths=None):
    """A minimal editorial table: header row, one grey rule, right-aligned cells.

    Returns (group, cells) where cells[(row, col)] is the cell mobject and
    row 0 is the header.
    """
    n_cols = len(headers)
    col_widths = col_widths or [2.4] * n_cols
    x_right = np.cumsum(col_widths)
    cells = {}
    group = VGroup()
    for i, row in enumerate([headers] + [list(r) for r in rows]):
        for j, cell_text in enumerate(row):
            color = GREY if i == 0 else CHARCOAL
            cell = serif(str(cell_text), LABEL_SIZE, color)
            cell.move_to(np.array([x_right[j], -i * row_height, 0]), aligned_edge=RIGHT)
            cells[(i, j)] = cell
            group.add(cell)
    rule = Line(
        np.array([0, -row_height / 2, 0]),
        np.array([x_right[-1] + GAP_SM, -row_height / 2, 0]),
        color=GREY,
        stroke_width=1.5,
    )
    group.add(rule)
    group.move_to(ORIGIN)
    return group, cells


def underline(mobject, color=SAGE):
    return Line(
        mobject.get_corner(DOWN + LEFT) + DOWN * GAP_SM,
        mobject.get_corner(DOWN + RIGHT) + DOWN * GAP_SM,
        color=color,
        stroke_width=3,
    )


class AlgebraFoundations(SATScene):
    scene_id = "concept.algebra_foundations"

    def clear_section(self, t, fraction=0.15):
        """Fade out everything except the margin note."""
        old = [m for m in self.mobjects if m is not self.margin_note]
        if old:
            self.play(*[FadeOut(m) for m in old], run_time=t.fill(fraction))

    def construct(self):
        self.margin_note = Text(
            "L01 · algebra", font=MONO_FONT, font_size=MARGIN_SIZE, color=GREY
        )
        self.margin_note.to_corner(UP + LEFT, buff=GAP_SM)
        self.add(self.margin_note)

        self.intro()
        self.two_perspectives()
        self.equivalence()
        self.three_representations()
        self.constant_change()
        self.word_problems()
        self.strategy_section()
        self.review()

    # ------------------------------------------------------------ sections

    def intro(self):
        title = serif("Algebra", TITLE_SIZE * 1.4)
        subtitle = serif("The Foundation of SAT Math", BODY_SIZE, GREY)
        subtitle.next_to(title, DOWN, buff=GAP_MD)
        VGroup(title, subtitle).move_to(UP * 0.5)

        with self.beat("title") as t:
            self.play(Write(title), run_time=t.fill(0.5))
            self.play(Write(subtitle), run_time=t.fill(0.25))
            t.hold()

        topics = VGroup(
            *[
                serif(line, LABEL_SIZE)
                for line in [
                    "linear expressions",
                    "linear equations",
                    "linear inequalities",
                    "systems of equations",
                    "linear functions",
                ]
            ]
        ).arrange(DOWN, buff=GAP_SM, aligned_edge=LEFT)
        topics.next_to(subtitle, DOWN, buff=GAP_MD * 1.5)

        with self.beat("scope") as t:
            self.play(
                VGroup(title, subtitle).animate.shift(UP * 1.5),
                run_time=t.fill(0.15),
            )
            topics.shift(UP * 1.5)
            self.play(Write(topics), run_time=t.fill(0.45))
            t.hold()

        why = serif("relationships · patterns · real-world problems", LABEL_SIZE, GREY)
        why.next_to(topics, DOWN, buff=GAP_MD * 1.5)

        with self.beat("why") as t:
            self.play(Write(why), run_time=t.fill(0.3))
            t.hold()

    def two_perspectives(self):
        eq_head = serif("Equations", BODY_SIZE)
        fn_head = serif("Functions", BODY_SIZE)
        eq_head.move_to(LEFT * 3.4 + UP * 2.2)
        fn_head.move_to(RIGHT * 3.4 + UP * 2.2)

        with self.beat("two_ways") as t:
            self.clear_section(t)
            self.play(Write(eq_head), Write(fn_head), run_time=t.fill(0.35))
            t.hold()

        eq = MathTex("3x + 5 = 20", font_size=DISPLAY_SIZE, color=CHARCOAL)
        eq.next_to(eq_head, DOWN, buff=GAP_MD * 2)
        eq_note = serif("find the value of x", LABEL_SIZE, GREY)
        eq_note.next_to(eq, DOWN, buff=GAP_MD)

        with self.beat("eq_example") as t:
            self.play(Write(eq), run_time=t.fill(0.3))
            self.play(Write(eq_note), run_time=t.fill(0.2))
            t.hold()

        fn = MathTex("y = 3x + 5", font_size=DISPLAY_SIZE, color=SLATE)
        fn.next_to(fn_head, DOWN, buff=GAP_MD * 2)
        fn_note = serif("a whole relationship", LABEL_SIZE, GREY)
        fn_note.next_to(fn, DOWN, buff=GAP_MD)

        with self.beat("fn_example") as t:
            self.play(Write(fn), run_time=t.fill(0.3))
            self.play(Write(fn_note), run_time=t.fill(0.2))
            t.hold()

        with self.beat("both") as t:
            self.play(
                Create(underline(eq_head)), Create(underline(fn_head)),
                run_time=t.fill(0.3),
            )
            t.hold()

    def equivalence(self):
        head = serif("Equivalence", TITLE_SIZE)
        head.to_edge(UP, buff=GAP_MD * 1.6)
        note = serif("whatever you do to one side, do to the other", LABEL_SIZE, GREY)
        note.next_to(head, DOWN, buff=GAP_MD)

        with self.beat("equivalence") as t:
            self.clear_section(t)
            self.play(Write(head), run_time=t.fill(0.25))
            self.play(Write(note), run_time=t.fill(0.2))
            t.hold()

        step1 = MathTex("x", "+", "7", "=", "15", font_size=DISPLAY_SIZE, color=CHARCOAL)
        step2 = MathTex(
            "x", "+", "7", "-", "7", "=", "15", "-", "7",
            font_size=DISPLAY_SIZE, color=CHARCOAL,
        )
        step3 = MathTex("x", "=", "8", font_size=DISPLAY_SIZE, color=CHARCOAL)
        for step in (step1, step2, step3):
            step.move_to(DOWN * 0.4)

        with self.beat("solve_setup") as t:
            self.play(Write(step1), run_time=t.fill(0.4))
            t.hold()

        with self.beat("solve_sub") as t:
            self.play(TransformMatchingTex(step1, step2), run_time=t.fill(0.5))
            t.hold()

        with self.beat("solve_result") as t:
            self.play(TransformMatchingTex(step2, step3), run_time=t.fill(0.35))
            t.hold()

        check = MathTex("8 + 7 = 15", font_size=EQUATION_SIZE, color=SAGE)
        check.next_to(step3, DOWN, buff=GAP_MD * 1.6)
        check_note = serif("always check", LABEL_SIZE, GREY)
        check_note.next_to(check, DOWN, buff=GAP_SM)

        with self.beat("check") as t:
            self.play(Write(check), run_time=t.fill(0.25))
            self.play(Write(check_note), run_time=t.fill(0.15))
            t.hold()

    def three_representations(self):
        heads = VGroup(
            serif("equation", BODY_SIZE),
            serif("table", BODY_SIZE),
            serif("graph", BODY_SIZE),
        )
        xs = [-4.6, 0.0, 4.4]
        for head, x in zip(heads, xs):
            head.move_to(np.array([x, 3.0, 0]))

        with self.beat("three_reps") as t:
            self.clear_section(t)
            self.play(*[Write(h) for h in heads], run_time=t.fill(0.35))
            t.hold()

        gym_eq = MathTex(
            "c", "=", "10", "+", "15", "m", font_size=EQUATION_SIZE, color=CHARCOAL
        )
        gym_eq.move_to(np.array([xs[0], 1.2, 0]))
        gym_note = VGroup(
            serif("$10 joining fee", LABEL_SIZE, GREY),
            serif("$15 per month", LABEL_SIZE, GREY),
        ).arrange(DOWN, buff=GAP_SM, aligned_edge=LEFT)
        gym_note.next_to(gym_eq, DOWN, buff=GAP_MD)

        with self.beat("gym_eq") as t:
            self.play(Write(gym_eq), run_time=t.fill(0.25))
            self.play(Write(gym_note), run_time=t.fill(0.2))
            t.hold()

        table, cells = make_table(
            ["months", "cost"],
            [[0, "$10"], [1, "$25"], [2, "$40"], [3, "$55"]],
            col_widths=[1.8, 1.6],
        )
        table.move_to(np.array([xs[1], 0.6, 0]))

        with self.beat("gym_table") as t:
            self.play(Write(table), run_time=t.fill(0.45))
            t.hold()

        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 70, 10],
            x_length=3.4,
            y_length=3.4,
            axis_config={"color": CHARCOAL, "include_ticks": False, "tip_length": 0.15},
        )
        axes.move_to(np.array([xs[2], 0.6, 0]))
        line = axes.plot(lambda x: 10 + 15 * x, x_range=[0, 3.6], color=SLATE)
        intercept = Dot(axes.c2p(0, 10), color=TERRACOTTA)
        intercept_label = MathTex("(0, 10)", font_size=EQUATION_SIZE, color=TERRACOTTA)
        intercept_label.next_to(intercept, RIGHT, buff=GAP_SM).shift(DOWN * 0.15)

        with self.beat("gym_graph") as t:
            self.play(Create(axes), run_time=t.fill(0.25))
            self.play(Create(line), run_time=t.fill(0.25))
            self.play(Create(VGroup(intercept, intercept_label)), run_time=t.fill(0.15))
            t.hold()

        run = Line(axes.c2p(1, 25), axes.c2p(2, 25), color=GREY, stroke_width=2.5)
        rise = Line(axes.c2p(2, 25), axes.c2p(2, 40), color=GREY, stroke_width=2.5)
        run_label = MathTex("+1", font_size=EQUATION_SIZE, color=GREY)
        run_label.next_to(run, DOWN, buff=GAP_SM * 0.6)
        rise_label = MathTex("+15", font_size=EQUATION_SIZE, color=GREY)
        rise_label.next_to(rise, RIGHT, buff=GAP_SM * 0.6)
        slope_marks = VGroup(run, rise, run_label, rise_label)

        with self.beat("gym_slope") as t:
            self.play(
                VGroup(intercept, intercept_label).animate.set_color(SLATE),
                run_time=t.fill(0.1),
            )
            self.play(Create(slope_marks), run_time=t.fill(0.3))
            t.hold()

        # The same 15, three ways — one terracotta highlight at a time.
        with self.beat("same_15_eq") as t:
            self.play(gym_eq[4].animate.set_color(TERRACOTTA), run_time=t.fill(0.2))
            t.hold()

        diffs = VGroup()
        for i in range(1, 4):
            mark = serif("+15", MARGIN_SIZE, TERRACOTTA)
            upper, lower = cells[(i, 1)], cells[(i + 1, 1)]
            mark.move_to(
                np.array(
                    [
                        table.get_right()[0] + GAP_MD * 1.2,
                        (upper.get_center()[1] + lower.get_center()[1]) / 2,
                        0,
                    ]
                )
            )
            diffs.add(mark)

        with self.beat("same_15_table") as t:
            self.play(gym_eq[4].animate.set_color(CHARCOAL), run_time=t.fill(0.08))
            self.play(Write(diffs), run_time=t.fill(0.25))
            t.hold()

        with self.beat("same_15_graph") as t:
            self.play(diffs.animate.set_color(GREY), run_time=t.fill(0.08))
            self.play(rise_label.animate.set_color(TERRACOTTA), run_time=t.fill(0.15))
            t.hold()

        with self.beat("connect") as t:
            self.play(rise_label.animate.set_color(GREY), run_time=t.fill(0.08))
            self.play(*[Create(underline(h)) for h in heads], run_time=t.fill(0.25))
            t.hold()

    def constant_change(self):
        eq = MathTex(
            "c", "=", "20", "+", "4", "m", font_size=DISPLAY_SIZE, color=CHARCOAL
        )
        eq.move_to(UP * 2.2)
        eq_note = serif("$20 fee, then $4 per mile — a constant rate", LABEL_SIZE, GREY)
        eq_note.next_to(eq, DOWN, buff=GAP_MD)

        with self.beat("linear") as t:
            self.clear_section(t)
            self.play(Write(eq), run_time=t.fill(0.3))
            self.play(Write(eq_note), run_time=t.fill(0.2))
            t.hold()

        table, cells = make_table(
            ["x", "y"],
            [[1, 7], [2, 10], [3, 13], [4, 16]],
            col_widths=[1.4, 1.4],
        )
        table.move_to(DOWN * 1.3 + LEFT * 0.6)

        with self.beat("diff_table") as t:
            self.play(Write(table), run_time=t.fill(0.4))
            t.hold()

        diffs = VGroup()
        for i in range(1, 4):
            mark = serif("+3", MARGIN_SIZE, TERRACOTTA)
            upper, lower = cells[(i, 1)], cells[(i + 1, 1)]
            mark.move_to(
                np.array(
                    [
                        table.get_right()[0] + GAP_MD * 1.2,
                        (upper.get_center()[1] + lower.get_center()[1]) / 2,
                        0,
                    ]
                )
            )
            diffs.add(mark)

        with self.beat("diff_mark") as t:
            self.play(Write(diffs), run_time=t.fill(0.3))
            t.hold()

        nonlinear = serif("quadratic and exponential change comes later", LABEL_SIZE, GREY)
        nonlinear.next_to(table, RIGHT, buff=GAP_MD * 3).shift(UP * 0.3)

        with self.beat("nonlinear") as t:
            self.play(diffs.animate.set_color(GREY), run_time=t.fill(0.08))
            self.play(Write(nonlinear), run_time=t.fill(0.2))
            t.hold()

        key = serif("A straight line has a constant rate of change.", BODY_SIZE)
        key.next_to(nonlinear, DOWN, buff=GAP_MD * 1.4)

        with self.beat("key_idea") as t:
            self.play(Write(key), run_time=t.fill(0.3))
            self.play(Create(underline(key)), run_time=t.fill(0.2))
            t.hold()

    def word_problems(self):
        head = serif("Word problems", TITLE_SIZE)
        head.to_edge(UP, buff=GAP_MD * 1.6)
        keys = VGroup(
            serif("the starting value", BODY_SIZE),
            serif("the rate of change", BODY_SIZE),
        ).arrange(DOWN, buff=GAP_SM * 1.5, aligned_edge=LEFT)
        keys.next_to(head, DOWN, buff=GAP_MD * 1.5)

        with self.beat("word") as t:
            self.clear_section(t)
            self.play(Write(head), run_time=t.fill(0.2))
            self.play(Write(keys), run_time=t.fill(0.3))
            t.hold()

        stream = serif("$12 activation fee  ·  $8 per month", LABEL_SIZE, GREY)
        stream.next_to(keys, DOWN, buff=GAP_MD * 1.5)

        with self.beat("stream") as t:
            self.play(Write(stream), run_time=t.fill(0.25))
            t.hold()

        stream_eq = MathTex(
            "c", "=", "12", "+", "8", "m", font_size=DISPLAY_SIZE, color=CHARCOAL
        )
        stream_eq.next_to(stream, DOWN, buff=GAP_MD * 1.4)

        with self.beat("stream_eq") as t:
            self.play(Write(stream_eq), run_time=t.fill(0.35))
            t.hold()

        mxb = MathTex("y", "=", "m", "x", "+", "b", font_size=DISPLAY_SIZE, color=CHARCOAL)
        mxb.next_to(stream_eq, DOWN, buff=GAP_MD * 1.6)
        slope_note = serif("slope", LABEL_SIZE, GREY)
        slope_note.next_to(mxb[2], DOWN, buff=GAP_MD)
        intercept_note = serif("intercept", LABEL_SIZE, GREY)
        intercept_note.next_to(mxb[5], DOWN, buff=GAP_MD).shift(RIGHT * 0.6)

        with self.beat("mxb") as t:
            self.play(Write(mxb), run_time=t.fill(0.3))
            self.play(Write(slope_note), Write(intercept_note), run_time=t.fill(0.2))
            t.hold()

        with self.beat("m_warning") as t:
            self.play(mxb[2].animate.set_color(TERRACOTTA), run_time=t.fill(0.15))
            t.hold()

    def strategy_section(self):
        head = serif("One problem, many routes", TITLE_SIZE)
        head.to_edge(UP, buff=GAP_MD * 1.6)

        with self.beat("strategy") as t:
            self.clear_section(t)
            self.play(Write(head), run_time=t.fill(0.3))
            t.hold()

        routes = VGroup(
            *[
                serif(line, LABEL_SIZE)
                for line in [
                    "solve symbolically",
                    "sketch a graph",
                    "make a small table",
                    "substitute the answer choices",
                    "test convenient values",
                    "use Desmos",
                ]
            ]
        ).arrange(DOWN, buff=GAP_SM * 1.3, aligned_edge=LEFT)
        routes.next_to(head, DOWN, buff=GAP_MD * 1.5)

        with self.beat("strat_list") as t:
            self.play(Write(routes), run_time=t.fill(0.5))
            t.hold()

        goal = serif("fast · accurate · appropriate", BODY_SIZE)
        goal.next_to(routes, DOWN, buff=GAP_MD * 1.5)

        with self.beat("efficient") as t:
            self.play(Write(goal), run_time=t.fill(0.25))
            self.play(Create(underline(goal)), run_time=t.fill(0.2))
            t.hold()

    def review(self):
        head = serif("Final review", TITLE_SIZE)
        head.to_edge(UP, buff=GAP_MD * 1.6)

        with self.beat("review") as t:
            self.clear_section(t)
            self.play(Write(head), run_time=t.fill(0.35))
            t.hold()

        lines = [
            "1  equations find unknowns; functions describe relationships",
            "2  equivalence: do the same to both sides",
            "3  one function — equation, table, graph",
            "4  linear means a constant rate of change",
            "5  choose the efficient strategy, not the familiar one",
        ]
        review_lines = VGroup(
            *[serif(line, LABEL_SIZE) for line in lines]
        ).arrange(DOWN, buff=GAP_SM * 1.6, aligned_edge=LEFT)
        review_lines.next_to(head, DOWN, buff=GAP_MD * 1.5)

        for name, line in zip(["rev1", "rev2", "rev3", "rev4", "rev5"], review_lines):
            with self.beat(name) as t:
                self.play(Write(line), run_time=t.fill(0.35))
                t.hold()

        upcoming = serif(
            "next: linear equations · inequalities · slope · systems",
            LABEL_SIZE,
            GREY,
        )
        upcoming.next_to(review_lines, DOWN, buff=GAP_MD * 1.4)

        with self.beat("next") as t:
            self.play(Write(upcoming), run_time=t.fill(0.3))
            t.hold()

        pillars = VGroup(
            serif("equivalence", BODY_SIZE),
            serif("multiple representations", BODY_SIZE),
            serif("constant change", BODY_SIZE),
        ).arrange(RIGHT, buff=GAP_MD * 2.4)
        pillars.move_to(ORIGIN)

        with self.beat("pillars") as t:
            self.clear_section(t)
            self.play(Write(pillars), run_time=t.fill(0.3))
            self.play(Create(underline(pillars)), run_time=t.fill(0.2))
            t.hold()
