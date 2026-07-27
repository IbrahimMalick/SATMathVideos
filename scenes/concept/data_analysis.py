"""Concept lecture: Problem Solving and Data Analysis (Math domain 2).

Narration script: scripts/L02-data-analysis.md
Nine sections; content clears between them, the margin note persists.
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
from components.table import make_table
from scenes.base import SATScene


def underline(mobject, color=SAGE):
    return Line(
        mobject.get_corner(DOWN + LEFT) + DOWN * GAP_SM,
        mobject.get_corner(DOWN + RIGHT) + DOWN * GAP_SM,
        color=color,
        stroke_width=3,
    )


class DataAnalysis(SATScene):
    scene_id = "concept.data_analysis"

    def clear_section(self, t, fraction=0.12):
        old = [m for m in self.mobjects if m is not self.margin_note]
        if old:
            self.play(*[FadeOut(m) for m in old], run_time=t.fill(fraction))

    def construct(self):
        self.margin_note = mono("L02 · data analysis", MARGIN_SIZE)
        self.margin_note.to_corner(UP + LEFT, buff=GAP_SM)
        self.add(self.margin_note)

        self.intro()
        self.proportional()
        self.percentages()
        self.multivariable()
        self.centre_and_spread()
        self.probability()
        self.inference()
        self.investigator()
        self.closing()

    # ------------------------------------------------------------ sections

    def intro(self):
        title = serif("Problem Solving", TITLE_SIZE * 1.2)
        title2 = serif("and Data Analysis", TITLE_SIZE * 1.2)
        title2.next_to(title, DOWN, buff=GAP_SM * 1.4)
        subtitle = serif("Digital SAT · Math domain 2", BODY_SIZE, GREY)
        subtitle.next_to(title2, DOWN, buff=GAP_MD)
        VGroup(title, title2, subtitle).move_to(UP * 1.2)

        with self.beat("title") as t:
            self.play(Write(title), Write(title2), run_time=t.fill(0.4))
            self.play(Write(subtitle), run_time=t.fill(0.2))
            t.hold()

        recap = serif("from equations and variables to real situations",
                      LABEL_SIZE, GREY)
        recap.next_to(subtitle, DOWN, buff=GAP_MD * 1.6)

        with self.beat("recap") as t:
            self.play(Write(recap), run_time=t.fill(0.35))
            t.hold()

        topics = serif(
            "data · ratios · rates · percentages · probability · statistics",
            LABEL_SIZE,
        )
        topics.next_to(recap, DOWN, buff=GAP_MD * 1.4)

        with self.beat("topics") as t:
            self.play(Write(topics), run_time=t.fill(0.35))
            self.play(Create(underline(topics)), run_time=t.fill(0.15))
            t.hold()

    def proportional(self):
        head = serif("Proportional relationships", TITLE_SIZE)
        head.to_edge(UP, buff=GAP_MD * 1.6)

        with self.beat("prop") as t:
            self.clear_section(t)
            self.play(Write(head), run_time=t.fill(0.35))
            t.hold()

        definition = serif("two quantities change at a constant rate", BODY_SIZE)
        definition.next_to(head, DOWN, buff=GAP_MD * 1.2)

        with self.beat("prop_def") as t:
            self.play(Write(definition), run_time=t.fill(0.3))
            self.play(Create(underline(definition)), run_time=t.fill(0.15))
            t.hold()

        eq = MathTex("c", "=", "20", "\\, p", font_size=DISPLAY_SIZE, color=CHARCOAL)
        eq.move_to(LEFT * 3.8 + DOWN * 0.6)
        eq_note = serif("£20 per person", LABEL_SIZE, GREY)
        eq_note.next_to(eq, DOWN, buff=GAP_MD)

        with self.beat("event") as t:
            self.play(Write(eq), run_time=t.fill(0.3))
            self.play(Write(eq_note), run_time=t.fill(0.2))
            t.hold()

        const_label = serif("the constant of proportionality", LABEL_SIZE, TERRACOTTA)
        const_label.next_to(eq_note, DOWN, buff=GAP_MD)
        const_label.move_to(np.array([-3.4, const_label.get_center()[1], 0]))

        with self.beat("constant") as t:
            self.play(eq[2].animate.set_color(TERRACOTTA), run_time=t.fill(0.15))
            self.play(Write(const_label), run_time=t.fill(0.2))
            t.hold()

        table, _cells = make_table(
            ["people", "cost"],
            [[10, "£200"], [50, "£1,000"]],
            col_widths=[2.0, 2.0],
        )
        table.move_to(RIGHT * 3.2 + DOWN * 0.9)

        with self.beat("event_values") as t:
            self.play(eq[2].animate.set_color(CHARCOAL),
                      const_label.animate.set_color(GREY), run_time=t.fill(0.1))
            self.play(Write(table), run_time=t.fill(0.35))
            t.hold()

        rate_note = serif("ratios · rates · conversions · density", LABEL_SIZE, GREY)
        rate_note.to_edge(DOWN, buff=GAP_MD * 1.2)

        with self.beat("rates") as t:
            self.play(Write(rate_note), run_time=t.fill(0.3))
            t.hold()

        with self.beat("units") as t:
            self.clear_section(t)
            unit_head = serif("Units are part of the calculation", TITLE_SIZE)
            unit_head.to_edge(UP, buff=GAP_MD * 1.6)
            unit_note = serif("they multiply, divide, and cancel like numbers",
                              LABEL_SIZE, GREY)
            unit_note.next_to(unit_head, DOWN, buff=GAP_MD)
            self.play(Write(unit_head), run_time=t.fill(0.3))
            self.play(Write(unit_note), run_time=t.fill(0.2))
            t.hold()

        speed = MathTex(
            "\\frac{60\\ \\text{miles}}{2\\ \\text{hours}}",
            font_size=DISPLAY_SIZE,
            color=CHARCOAL,
        )
        speed.move_to(DOWN * 0.9 + LEFT * 2.2)

        with self.beat("speed") as t:
            self.play(Write(speed), run_time=t.fill(0.4))
            t.hold()

        result = MathTex(
            "=", "30", "\\ \\text{miles per hour}",
            font_size=DISPLAY_SIZE, color=CHARCOAL,
        )
        result.next_to(speed, RIGHT, buff=GAP_MD)
        result[2].set_color(SLATE)

        with self.beat("speed_result") as t:
            self.play(Write(result), run_time=t.fill(0.35))
            t.hold()

    def percentages(self):
        head = serif("Percentages", TITLE_SIZE)
        head.to_edge(UP, buff=GAP_MD * 1.6)
        uses = serif("tax · tips · discounts · interest · growth", LABEL_SIZE, GREY)
        uses.next_to(head, DOWN, buff=GAP_MD)

        with self.beat("pct") as t:
            self.clear_section(t)
            self.play(Write(head), run_time=t.fill(0.3))
            self.play(Write(uses), run_time=t.fill(0.2))
            t.hold()

        pct_def = MathTex(
            "20\\% = \\frac{20}{100} = 0.2",
            font_size=EQUATION_SIZE, color=CHARCOAL,
        )
        pct_def.next_to(uses, DOWN, buff=GAP_MD * 0.9)

        with self.beat("pct_def") as t:
            self.play(Write(pct_def), run_time=t.fill(0.35))
            t.hold()

        change = serif("loses 36% of its value every year", BODY_SIZE)
        change.next_to(pct_def, DOWN, buff=GAP_MD)
        wrong = serif("not: subtract 36 each year", LABEL_SIZE, TERRACOTTA)
        wrong.next_to(change, DOWN, buff=GAP_MD * 0.8)

        with self.beat("pct_change") as t:
            self.play(Write(change), run_time=t.fill(0.3))
            self.play(Write(wrong), run_time=t.fill(0.2))
            t.hold()

        keep = MathTex(
            "\\text{keeps } 64\\% \\;\\Rightarrow\\; \\times\\, 0.64 \\text{ each year}",
            font_size=EQUATION_SIZE, color=CHARCOAL,
        )
        keep.next_to(wrong, DOWN, buff=GAP_MD * 0.9)

        with self.beat("keep64") as t:
            self.play(wrong.animate.set_color(GREY), run_time=t.fill(0.08))
            self.play(Write(keep), run_time=t.fill(0.3))
            t.hold()

        decay1 = MathTex(
            "1000", "\\times 0.64", "=", "640",
            font_size=EQUATION_SIZE, color=CHARCOAL,
        )
        decay1.next_to(keep, DOWN, buff=GAP_MD).shift(LEFT * 2.8)

        with self.beat("decay1") as t:
            self.play(Write(decay1), run_time=t.fill(0.35))
            t.hold()

        decay2 = MathTex(
            "640", "\\times 0.64", "= \\; ?",
            font_size=EQUATION_SIZE, color=CHARCOAL,
        )
        decay2.next_to(decay1, RIGHT, buff=GAP_MD * 1.6)
        decay2[0].set_color(TERRACOTTA)
        from_note = serif("from 640, not 1000", LABEL_SIZE, GREY)
        from_note.next_to(decay2, DOWN, buff=GAP_SM * 1.4)

        with self.beat("decay2") as t:
            self.play(Write(decay2), run_time=t.fill(0.3))
            self.play(Write(from_note), run_time=t.fill(0.2))
            t.hold()

        with self.beat("pct_rule") as t:
            self.clear_section(t)
            rule = serif("Each change is based on its own starting value.",
                         BODY_SIZE)
            rule.move_to(ORIGIN)
            self.play(Write(rule), run_time=t.fill(0.35))
            self.play(Create(underline(rule)), run_time=t.fill(0.15))
            t.hold()

    def multivariable(self):
        head = serif("More than one variable", TITLE_SIZE)
        head.to_edge(UP, buff=GAP_MD * 1.6)

        with self.beat("multi") as t:
            self.clear_section(t)
            self.play(Write(head), run_time=t.fill(0.35))
            t.hold()

        study = serif("how much do students sleep?", BODY_SIZE)
        study.next_to(head, DOWN, buff=GAP_MD * 1.6)
        factors = serif("hours · age · year group · study habits", LABEL_SIZE, GREY)
        factors.next_to(study, DOWN, buff=GAP_MD)
        question = serif("same average, different variation?", LABEL_SIZE)
        question.next_to(factors, DOWN, buff=GAP_MD * 1.4)

        with self.beat("sleep") as t:
            self.play(Write(study), run_time=t.fill(0.25))
            self.play(Write(factors), run_time=t.fill(0.2))
            self.play(Write(question), run_time=t.fill(0.2))
            t.hold()

    def centre_and_spread(self):
        head = serif("Centre and spread", TITLE_SIZE)
        head.to_edge(UP, buff=GAP_MD * 1.6)
        charts = serif("tables · scatterplots · dot plots · bar graphs · box plots",
                       LABEL_SIZE, GREY)
        charts.next_to(head, DOWN, buff=GAP_MD)

        with self.beat("charts") as t:
            self.clear_section(t)
            self.play(Write(head), run_time=t.fill(0.3))
            self.play(Write(charts), run_time=t.fill(0.2))
            t.hold()

        centre = VGroup(
            serif("mean — add all values, divide by the count", LABEL_SIZE),
            serif("median — the middle value in order", LABEL_SIZE),
        ).arrange(DOWN, buff=GAP_SM * 1.4, aligned_edge=LEFT)
        centre.next_to(charts, DOWN, buff=GAP_MD * 1.3)
        centre.move_to(np.array([-2.0, centre.get_center()[1], 0]))

        with self.beat("centre") as t:
            self.play(Write(centre), run_time=t.fill(0.4))
            t.hold()

        spread = serif("range — highest minus lowest", LABEL_SIZE)
        spread.next_to(centre, DOWN, buff=GAP_SM * 1.4, aligned_edge=LEFT)

        with self.beat("spread") as t:
            self.play(Write(spread), run_time=t.fill(0.35))
            t.hold()

        # Two dot rows: same centre, different standard deviation.
        def dot_row(values, y):
            line = Line(np.array([-4.5, y, 0]), np.array([1.5, y, 0]),
                        color=CHARCOAL, stroke_width=2)
            dots = VGroup(*[Dot(np.array([x, y, 0]), color=SLATE, radius=0.09)
                            for x in values])
            return line, dots

        base = -2.1
        line1, dots1 = dot_row([-2.2, -1.9, -1.5, -1.3, -1.0], base)
        line2, dots2 = dot_row([-4.2, -2.9, -1.6, -0.3, 1.2], base - 1.2)
        label1 = serif("small — close together", LABEL_SIZE, GREY)
        label1.next_to(line1, RIGHT, buff=GAP_MD)
        label2 = serif("large — spread out", LABEL_SIZE, GREY)
        label2.next_to(line2, RIGHT, buff=GAP_MD)
        stdev_head = serif("standard deviation — distance from the mean", LABEL_SIZE)
        stdev_head.next_to(spread, DOWN, buff=GAP_MD, aligned_edge=LEFT)

        with self.beat("stdev") as t:
            self.play(Write(stdev_head), run_time=t.fill(0.35))
            t.hold()

        with self.beat("stdev_small") as t:
            self.play(Create(line1), run_time=t.fill(0.15))
            self.play(Create(dots1), run_time=t.fill(0.25))
            self.play(Write(label1), run_time=t.fill(0.15))
            t.hold()

        with self.beat("stdev_large") as t:
            self.play(Create(line2), run_time=t.fill(0.15))
            self.play(Create(dots2), run_time=t.fill(0.25))
            self.play(Write(label2), run_time=t.fill(0.15))
            t.hold()

        note = mono("interpret it — you won't compute it", MARGIN_SIZE)
        note.to_edge(DOWN, buff=GAP_SM * 1.4)

        with self.beat("stdev_note") as t:
            self.play(Write(note), run_time=t.fill(0.3))
            t.hold()

    def probability(self):
        head = serif("Probability", TITLE_SIZE)
        head.to_edge(UP, buff=GAP_MD * 1.6)

        with self.beat("prob") as t:
            self.clear_section(t)
            self.play(Write(head), run_time=t.fill(0.35))
            t.hold()

        coin = serif("1,000 coin flips — roughly half heads, half tails", BODY_SIZE)
        coin.next_to(head, DOWN, buff=GAP_MD * 1.5)
        coin_note = serif("long-term patterns, not single results", LABEL_SIZE, GREY)
        coin_note.next_to(coin, DOWN, buff=GAP_MD)

        with self.beat("coin") as t:
            self.play(Write(coin), run_time=t.fill(0.3))
            self.play(Write(coin_note), run_time=t.fill(0.2))
            t.hold()

        prob1 = MathTex(
            "P(4)", "=",
            "\\frac{\\text{favourable outcomes}}{\\text{possible outcomes}}",
            font_size=DISPLAY_SIZE, color=CHARCOAL,
        )
        prob1.next_to(coin_note, DOWN, buff=GAP_MD * 1.8)

        with self.beat("dice") as t:
            self.play(Write(prob1), run_time=t.fill(0.4))
            t.hold()

        prob2 = MathTex(
            "P(4)", "=", "\\frac{1}{6}",
            font_size=DISPLAY_SIZE, color=CHARCOAL,
        )
        prob2.move_to(prob1)

        with self.beat("dice_result") as t:
            self.play(TransformMatchingTex(prob1, prob2), run_time=t.fill(0.4))
            t.hold()

    def inference(self):
        head = serif("Statistical inference", TITLE_SIZE)
        head.to_edge(UP, buff=GAP_MD * 1.6)
        defs = VGroup(
            serif("population — the entire group we want to study", LABEL_SIZE),
            serif("sample — the smaller group we actually measure", LABEL_SIZE),
        ).arrange(DOWN, buff=GAP_SM * 1.4, aligned_edge=LEFT)
        defs.next_to(head, DOWN, buff=GAP_MD * 1.3)

        with self.beat("inference") as t:
            self.clear_section(t)
            self.play(Write(head), run_time=t.fill(0.3))
            self.play(Write(defs), run_time=t.fill(0.3))
            t.hold()

        survey = serif("400 employees — survey 20 of them", BODY_SIZE)
        survey.next_to(defs, DOWN, buff=GAP_MD * 1.3)

        with self.beat("survey") as t:
            self.play(Write(survey), run_time=t.fill(0.35))
            t.hold()

        random_line = serif("random: every member has a fair chance", BODY_SIZE)
        random_line.next_to(survey, DOWN, buff=GAP_MD * 1.2)

        with self.beat("random") as t:
            self.play(Write(random_line), run_time=t.fill(0.3))
            self.play(Create(underline(random_line)), run_time=t.fill(0.15))
            t.hold()

        biased = VGroup(
            serif("one department only — may not represent", LABEL_SIZE, GREY),
            serif("randomly selected — represents the workforce", LABEL_SIZE, SAGE),
        ).arrange(DOWN, buff=GAP_SM * 1.4, aligned_edge=LEFT)
        biased.next_to(random_line, DOWN, buff=GAP_MD * 1.2)

        with self.beat("biased") as t:
            self.play(Write(biased), run_time=t.fill(0.4))
            t.hold()

        questions = VGroup(
            serif("how was the sample selected?", LABEL_SIZE),
            serif("is it large enough?", LABEL_SIZE),
            serif("does it represent the population?", LABEL_SIZE),
            serif("was the selection biased?", LABEL_SIZE),
        ).arrange(DOWN, buff=GAP_SM * 1.3, aligned_edge=LEFT)
        head2 = serif("Evaluating a study", TITLE_SIZE)
        head2.to_edge(UP, buff=GAP_MD * 1.6)
        questions.next_to(head2, DOWN, buff=GAP_MD * 1.4)

        with self.beat("questions") as t:
            self.clear_section(t)
            self.play(Write(head2), run_time=t.fill(0.2))
            self.play(Write(questions), run_time=t.fill(0.4))
            t.hold()

        gen = serif("a random sample generalises to its population", LABEL_SIZE, GREY)
        gen.next_to(questions, DOWN, buff=GAP_MD * 1.3, aligned_edge=LEFT)

        with self.beat("generalise") as t:
            self.play(Write(gen), run_time=t.fill(0.35))
            t.hold()

        cause = serif("cause and effect needs random assignment", LABEL_SIZE, GREY)
        cause.next_to(gen, DOWN, buff=GAP_SM * 1.4, aligned_edge=LEFT)

        with self.beat("causation") as t:
            self.play(Write(cause), run_time=t.fill(0.35))
            t.hold()

        with self.beat("distinction") as t:
            self.clear_section(t)
            pair = VGroup(
                serif("random selection  →  generalise to a population", BODY_SIZE),
                serif("random assignment  →  conclude cause and effect", BODY_SIZE),
            ).arrange(DOWN, buff=GAP_MD * 1.2, aligned_edge=LEFT)
            pair.move_to(ORIGIN)
            self.play(Write(pair), run_time=t.fill(0.4))
            self.play(Create(underline(pair[0])), Create(underline(pair[1])),
                      run_time=t.fill(0.15))
            t.hold()

    def investigator(self):
        head = serif("Think like an investigator", TITLE_SIZE)
        head.to_edge(UP, buff=GAP_MD * 1.6)

        with self.beat("investigator") as t:
            self.clear_section(t)
            self.play(Write(head), run_time=t.fill(0.35))
            t.hold()

        left = VGroup(
            serif("what is compared?", LABEL_SIZE),
            serif("what are the units?", LABEL_SIZE),
            serif("proportional?", LABEL_SIZE),
            serif("additive or multiplicative?", LABEL_SIZE),
            serif("linear or exponential?", LABEL_SIZE),
        ).arrange(DOWN, buff=GAP_SM * 1.3, aligned_edge=LEFT)
        right = VGroup(
            serif("mean or median?", LABEL_SIZE),
            serif("how spread out?", LABEL_SIZE),
            serif("random sample?", LABEL_SIZE),
            serif("does the evidence support it?", LABEL_SIZE),
        ).arrange(DOWN, buff=GAP_SM * 1.3, aligned_edge=LEFT)
        left.next_to(head, DOWN, buff=GAP_MD * 1.5)
        left.move_to(np.array([-3.6, left.get_center()[1], 0]))
        right.next_to(head, DOWN, buff=GAP_MD * 1.5)
        right.move_to(np.array([3.0, right.get_center()[1], 0]))

        with self.beat("ask_list") as t:
            self.play(Write(left), run_time=t.fill(0.35))
            self.play(Write(right), run_time=t.fill(0.35))
            t.hold()

        motto = serif("understand first, then calculate", BODY_SIZE)
        motto.to_edge(DOWN, buff=GAP_MD * 1.3)

        with self.beat("investigator2") as t:
            self.play(Write(motto), run_time=t.fill(0.3))
            self.play(Create(underline(motto)), run_time=t.fill(0.15))
            t.hold()

    def closing(self):
        head = serif("Review", TITLE_SIZE)
        head.to_edge(UP, buff=GAP_MD * 1.6)

        with self.beat("review") as t:
            self.clear_section(t)
            self.play(Write(head), run_time=t.fill(0.35))
            t.hold()

        lines = [
            "1  proportional means a constant rate of change",
            "2  units are part of the calculation",
            "3  percentage change is multiplicative",
            "4  compare centre and spread",
            "5  probability describes long-term patterns",
            "6  inference: sample to population",
            "7  selection generalises; assignment shows cause",
        ]
        review_lines = VGroup(
            *[serif(line, LABEL_SIZE) for line in lines]
        ).arrange(DOWN, buff=GAP_SM * 1.4, aligned_edge=LEFT)
        review_lines.next_to(head, DOWN, buff=GAP_MD * 1.3)

        for name, line in zip(
            ["rev1", "rev2", "rev3", "rev4", "rev5", "rev6", "rev7"], review_lines
        ):
            with self.beat(name) as t:
                self.play(Write(line), run_time=t.fill(0.35))
                t.hold()

        key = serif("Understand the relationship the numbers represent.",
                    BODY_SIZE)
        key.move_to(ORIGIN)

        with self.beat("key") as t:
            self.clear_section(t)
            self.play(Write(key), run_time=t.fill(0.35))
            self.play(Create(underline(key)), run_time=t.fill(0.15))
            t.hold()

        upcoming = serif("next: Advanced Math — nonlinear equations and functions",
                         LABEL_SIZE, GREY)
        upcoming.next_to(key, DOWN, buff=GAP_MD * 1.6)

        with self.beat("next") as t:
            self.play(Write(upcoming), run_time=t.fill(0.35))
            t.hold()

        end = mono("end of lecture", MARGIN_SIZE)
        end.to_edge(DOWN, buff=GAP_MD)

        with self.beat("end") as t:
            self.play(Write(end), run_time=t.fill(0.4))
            t.hold()
