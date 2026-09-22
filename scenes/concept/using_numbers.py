"""Concept lecture: from knowing numbers to using numbers (O Level, OL03).

Narration script: scripts/OL03-using-numbers.md

Lecture 2 of Chapter 1. The spine is four words — Represent, Operate,
Estimate, Judge — carried by the WordArc component, with fractions,
percentages, negative numbers, indices, standard form and estimation
hanging off them.

Where the delivery misspoke (cube root read as square root, 7846 to 2 s.f.
read as 78,000, one-fifth read as a half), the screen shows the correct
mathematics: students copy what they see.
"""

import numpy as np

from manim import (
    Create,
    Dot,
    FadeIn,
    FadeOut,
    Line,
    MathTex,
    NumberLine,
    Rectangle,
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
from components.word_arc import WordArc
from scenes.base import SATScene

FOUR = ["Represent", "Operate", "Estimate", "Judge"]
FRAME_SAFE = 12.6


def fit(mobject, width=FRAME_SAFE):
    if mobject.width > width:
        mobject.scale_to_fit_width(width)
    return mobject


def lines(*texts, size=BODY_SIZE, color=CHARCOAL, buff=GAP_SM * 1.3):
    group = VGroup(*[fit(serif(t, size, color)) for t in texts])
    group.arrange(DOWN, buff=buff)
    return group


def eqs(*texs, size=EQUATION_SIZE, color=CHARCOAL, buff=GAP_SM * 1.3):
    group = VGroup(*[MathTex(t, font_size=size, color=color) for t in texs])
    group.arrange(DOWN, buff=buff)
    return fit(group)


class UsingNumbers(SATScene):
    scene_id = "concept.using_numbers"

    def construct(self):
        self.margin_note = mono("O Level Maths · Ch 1 · Lecture 2",
                                MARGIN_SIZE)
        self.margin_note.to_corner(UP + LEFT, buff=GAP_SM)
        self.add(self.margin_note)
        self.section_head = None

        self.opening()
        self.represent()
        self.multipliers()
        self.negatives()
        self.powers()
        self.standard_form()
        self.rounding()
        self.challenges()
        self.closing()

    # -------------------------------------------------------------- helpers

    def clear_all(self, t, fraction=0.06):
        old = [m for m in self.mobjects if m is not self.margin_note]
        if old:
            self.play(*[FadeOut(m) for m in old], run_time=t.fill(fraction))
        self.section_head = None

    def set_head(self, t, text, fraction=0.1):
        head = fit(serif(text, TITLE_SIZE))
        head.to_edge(UP, buff=GAP_MD * 1.4)
        self.play(Write(head), run_time=t.fill(fraction))
        self.section_head = head
        return head

    def below_head(self, mobject, buff=GAP_MD * 1.4):
        if self.section_head is None:
            mobject.move_to(ORIGIN)
        else:
            mobject.next_to(self.section_head, DOWN, buff=buff)
        return mobject

    def underline(self, mobject, color=SAGE):
        return Line(
            mobject.get_corner(DOWN + LEFT) + DOWN * GAP_SM,
            mobject.get_corner(DOWN + RIGHT) + DOWN * GAP_SM,
            color=color, stroke_width=3,
        )

    def arc_focus(self, t, index, fraction=0.12):
        """Park the four words along the bottom, lit at one step."""
        arc = WordArc(FOUR, size=LABEL_SIZE, lit=CHARCOAL)
        arc.to_edge(DOWN, buff=GAP_MD * 0.9)
        self.play(FadeIn(arc), *arc.focus(index), run_time=t.fill(fraction))
        return arc

    def chain(self, t, steps, position, per=0.18, final_color=SAGE):
        """Write the first tex, then morph through the rest."""
        mobs = [MathTex(s, font_size=DISPLAY_SIZE, color=CHARCOAL)
                for s in steps]
        mobs[-1].set_color(final_color)
        for m in mobs:
            fit(m)
            m.move_to(position)
        self.play(Write(mobs[0]), run_time=t.fill(per))
        for a, b in zip(mobs, mobs[1:]):
            self.play(TransformMatchingTex(a, b), run_time=t.fill(per))
        return mobs[-1]

    # ------------------------------------------------------------- sections

    def opening(self):
        with self.beat("open") as t:
            title = lines("From Knowing Numbers", "to Using Numbers",
                          size=TITLE_SIZE * 1.25)
            title.move_to(UP * 1.5)
            sub = serif("O Level Mathematics · Chapter 1 · Lecture 2",
                        BODY_SIZE, GREY)
            sub.next_to(title, DOWN, buff=GAP_MD * 1.2)
            self.play(Write(title), run_time=t.fill(0.2))
            self.play(Write(sub), run_time=t.fill(0.12))
            recap = lines("last time: number families · BODMAS",
                          "ordering · prime factors · HCF and LCM",
                          size=LABEL_SIZE, color=GREY)
            recap.next_to(sub, DOWN, buff=GAP_MD * 1.6)
            self.play(Write(recap), run_time=t.fill(0.3))
            t.hold()

        with self.beat("hook_problem") as t:
            self.clear_all(t)
            self.set_head(t, "Two students")
            same = lines("same calculator", "same examination",
                         "same formula sheet", "same amount of time",
                         size=BODY_SIZE, color=GREY)
            self.below_head(same, buff=GAP_MD * 1.3)
            grades = VGroup(
                serif("C", TITLE_SIZE * 1.6, GREY),
                serif("A*", TITLE_SIZE * 1.6, TERRACOTTA),
            ).arrange(RIGHT, buff=GAP_MD * 4)
            grades.next_to(same, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(same), run_time=t.fill(0.3))
            self.play(Write(grades), run_time=t.fill(0.25))
            t.hold()

        with self.beat("why_difference") as t:
            self.clear_all(t)
            self.set_head(t, "The difference")
            one = serif("one knows which buttons to press", BODY_SIZE, GREY)
            two = serif("one knows why those buttons", BODY_SIZE)
            three = serif("should be pressed", BODY_SIZE)
            stack = VGroup(one, VGroup(two, three).arrange(
                DOWN, buff=GAP_SM)).arrange(DOWN, buff=GAP_MD * 1.8)
            self.below_head(stack, buff=GAP_MD * 1.6)
            self.play(Write(one), run_time=t.fill(0.25))
            self.play(Write(stack[1]), run_time=t.fill(0.3))
            self.play(Create(self.underline(stack[1], TERRACOTTA)),
                      run_time=t.fill(0.1))
            t.hold()

        with self.beat("four_words") as t:
            self.clear_all(t)
            words = VGroup(*[
                serif(w.upper(), TITLE_SIZE * 1.15) for w in FOUR
            ]).arrange(DOWN, buff=GAP_MD * 0.9)
            words.move_to(UP * 0.4)
            for word in words:
                self.play(Write(word), run_time=t.fill(0.12))
            note = serif("every hard number question is asking for one "
                         "of these", LABEL_SIZE, GREY)
            fit(note)
            note.next_to(words, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(note), run_time=t.fill(0.2))
            t.hold()

    def represent(self):
        with self.beat("represent_intro") as t:
            self.clear_all(t)
            self.set_head(t, "Represent")
            trio = VGroup(
                MathTex("\\tfrac{1}{2}", font_size=TITLE_SIZE * 1.5,
                        color=CHARCOAL),
                MathTex("0.5", font_size=TITLE_SIZE * 1.5, color=CHARCOAL),
                MathTex("50\\%", font_size=TITLE_SIZE * 1.5,
                        color=CHARCOAL),
            ).arrange(RIGHT, buff=GAP_MD * 3)
            self.below_head(trio, buff=GAP_MD * 1.6)
            labels = VGroup(*[
                serif(name, LABEL_SIZE, GREY)
                for name in ("fraction", "decimal", "percentage")
            ])
            for label, part in zip(labels, trio):
                label.next_to(part, DOWN, buff=GAP_SM * 1.2)
            for part, label in zip(trio, labels):
                self.play(Write(part), Write(label), run_time=t.fill(0.14))
            self.arc_focus(t, 0)
            self.trio = VGroup(trio, labels)
            t.hold()

        with self.beat("three_outfits") as t:
            idea = lines("one number wearing three outfits",
                         size=BODY_SIZE, color=TERRACOTTA)
            idea.next_to(self.trio, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(idea), run_time=t.fill(0.3))
            recognise = serif("the examiner changes the outfit — "
                              "recognise the person underneath",
                              LABEL_SIZE, GREY)
            fit(recognise)
            recognise.next_to(idea, DOWN, buff=GAP_MD)
            self.play(Write(recognise), run_time=t.fill(0.3))
            t.hold()

        with self.beat("frac_to_dec") as t:
            self.clear_all(t)
            self.set_head(t, "Fraction → decimal")
            bar = serif("the fraction bar means: divide", BODY_SIZE, GREY)
            self.below_head(bar, buff=GAP_MD * 1.2)
            self.play(Write(bar), run_time=t.fill(0.15))
            self.chain(t, ["\\tfrac{3}{4}", "3 \\div 4", "0.75"],
                       DOWN * 0.6, per=0.2)
            t.hold()

        with self.beat("dec_to_pct") as t:
            self.clear_all(t)
            self.set_head(t, "Decimal → percentage")
            meaning = serif("per cent means: out of a hundred",
                            BODY_SIZE, GREY)
            self.below_head(meaning, buff=GAP_MD * 1.2)
            self.play(Write(meaning), run_time=t.fill(0.15))
            self.chain(t, ["0.75", "0.75 \\times 100", "75\\%"],
                       DOWN * 0.6, per=0.2)
            t.hold()

        with self.beat("one_quantity") as t:
            whole = MathTex("\\tfrac{3}{4} \\;=\\; 0.75 \\;=\\; 75\\%",
                            font_size=DISPLAY_SIZE, color=SAGE)
            whole.move_to(DOWN * 2.4)
            self.play(Write(whole), run_time=t.fill(0.45))
            t.hold()

        with self.beat("pct_to_dec") as t:
            self.clear_all(t)
            self.set_head(t, "Percentage → decimal")
            warn = serif("don't multiply — we're going the other way",
                         BODY_SIZE, TERRACOTTA)
            self.below_head(warn, buff=GAP_MD * 1.2)
            self.play(Write(warn), run_time=t.fill(0.18))
            self.chain(t, ["8\\%", "\\tfrac{8}{100}", "0.08"],
                       DOWN * 0.6, per=0.2)
            t.hold()

        with self.beat("highway") as t:
            self.clear_all(t)
            self.set_head(t, "The conversion highway")
            nodes = VGroup(*[
                serif(name, BODY_SIZE)
                for name in ("Fraction", "Decimal", "Percentage")
            ]).arrange(RIGHT, buff=GAP_MD * 3.4)
            self.below_head(nodes, buff=GAP_MD * 1.8)
            ops = VGroup(
                MathTex("\\div", font_size=LABEL_SIZE, color=TERRACOTTA),
                MathTex("\\times 100", font_size=LABEL_SIZE,
                        color=TERRACOTTA),
            )
            arrows = VGroup()
            for i, op in enumerate(ops):
                a = Line(nodes[i].get_right() + RIGHT * 0.2,
                         nodes[i + 1].get_left() + LEFT * 0.2,
                         color=GREY, stroke_width=3)
                op.next_to(a, UP, buff=GAP_SM * 0.8)
                arrows.add(a)
            back = serif("percentage → decimal: ÷ 100", LABEL_SIZE, GREY)
            back.next_to(nodes, DOWN, buff=GAP_MD * 1.8)
            self.play(Write(nodes), run_time=t.fill(0.25))
            self.play(Create(arrows), Write(ops), run_time=t.fill(0.25))
            self.play(Write(back), run_time=t.fill(0.2))
            t.hold()

        with self.beat("half_pct_trap") as t:
            self.clear_all(t)
            self.set_head(t, "The 0.5% trap")
            wrong = MathTex("0.5\\% = 0.5", font_size=DISPLAY_SIZE,
                            color=GREY)
            self.below_head(wrong, buff=GAP_MD * 1.3)
            cross = Line(wrong.get_left() + LEFT * 0.2,
                         wrong.get_right() + RIGHT * 0.2,
                         color=TERRACOTTA, stroke_width=4)
            self.play(Write(wrong), run_time=t.fill(0.18))
            self.play(Create(cross), run_time=t.fill(0.08))
            right = MathTex("0.5 \\div 100 = 0.005",
                            font_size=DISPLAY_SIZE, color=SAGE)
            right.next_to(wrong, DOWN, buff=GAP_MD * 1.6)
            self.play(Write(right), run_time=t.fill(0.25))
            cost = serif("tiny mistakes cost marks", LABEL_SIZE, GREY)
            cost.next_to(right, DOWN, buff=GAP_MD * 1.2)
            self.play(Write(cost), run_time=t.fill(0.15))
            t.hold()

        with self.beat("benchmarks") as t:
            self.clear_all(t)
            self.set_head(t, "Know these on sight")
            rows = eqs(
                "\\tfrac{1}{2} = 0.5 = 50\\%",
                "\\tfrac{1}{4} = 0.25 = 25\\%",
                "\\tfrac{3}{4} = 0.75 = 75\\%",
                "\\tfrac{1}{5} = 0.2 = 20\\%",
                "\\tfrac{1}{10} = 0.1 = 10\\%",
                size=EQUATION_SIZE, buff=GAP_SM * 1.2,
            )
            self.below_head(rows, buff=GAP_MD * 1.2)
            for row in rows:
                self.play(Write(row), run_time=t.fill(0.1))
            note = serif("don't memorise — see them until they're familiar",
                         LABEL_SIZE, GREY)
            fit(note)
            note.next_to(rows, DOWN, buff=GAP_MD * 1.2)
            self.play(Write(note), run_time=t.fill(0.2))
            t.hold()

    def multipliers(self):
        with self.beat("multiplier_intro") as t:
            self.clear_all(t)
            self.set_head(t, "A jacket costs $80, 20% off")
            usual = eqs("20\\% \\text{ of } 80 = 16",
                        "80 - 16 = 64", size=EQUATION_SIZE)
            self.below_head(usual, buff=GAP_MD * 1.5)
            fine = serif("perfectly correct — nothing wrong with that",
                         LABEL_SIZE, GREY)
            fine.next_to(usual, DOWN, buff=GAP_MD * 1.3)
            self.play(Write(usual), run_time=t.fill(0.35))
            self.play(Write(fine), run_time=t.fill(0.2))
            self.arc_focus(t, 1)
            t.hold()

        with self.beat("multiplier") as t:
            self.clear_all(t)
            self.set_head(t, "A more powerful way")
            ask = serif("if 20% disappears, what remains?", BODY_SIZE, GREY)
            self.below_head(ask, buff=GAP_MD * 1.2)
            self.play(Write(ask), run_time=t.fill(0.15))
            self.chain(t, ["80\\%", "0.8", "80 \\times 0.8 = 64"],
                       DOWN * 0.4, per=0.18)
            name = serif("0.8 is the multiplier", BODY_SIZE, TERRACOTTA)
            name.move_to(DOWN * 2.4)
            self.play(Write(name), run_time=t.fill(0.2))
            t.hold()

        with self.beat("increase") as t:
            self.clear_all(t)
            self.set_head(t, "Now increase by 20%")
            warn = serif("don't multiply by 0.2 — that is only the increase",
                         BODY_SIZE, GREY)
            fit(warn)
            self.below_head(warn, buff=GAP_MD * 1.2)
            self.play(Write(warn), run_time=t.fill(0.18))
            self.chain(t, ["100\\% + 20\\%", "120\\%", "1.2",
                           "80 \\times 1.2 = 96"],
                       DOWN * 0.6, per=0.15)
            t.hold()

        with self.beat("multiplier_rule") as t:
            self.clear_all(t)
            rules = eqs("\\text{increase } 20\\% \\;\\rightarrow\\; "
                        "\\times 1.20",
                        "\\text{decrease } 20\\% \\;\\rightarrow\\; "
                        "\\times 0.80",
                        size=DISPLAY_SIZE, buff=GAP_MD)
            rules.move_to(UP * 0.3)
            self.play(Write(rules), run_time=t.fill(0.5))
            self.play(Create(self.underline(rules)), run_time=t.fill(0.12))
            t.hold()

        with self.beat("pct_trap") as t:
            self.clear_all(t)
            self.set_head(t, "The percentage trap")
            story = lines("a phone costs $100",
                          "the price rises 20%, then falls 20%",
                          size=BODY_SIZE)
            self.below_head(story, buff=GAP_MD * 1.4)
            ask = serif("are we back at $100?", BODY_SIZE, TERRACOTTA)
            ask.next_to(story, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(story), run_time=t.fill(0.3))
            self.play(Write(ask), run_time=t.fill(0.25))
            t.hold()

        with self.beat("pct_trap_calc") as t:
            self.clear_all(t)
            self.set_head(t, "Let's calculate")
            steps = eqs("100 \\times 1.2 = 120",
                        "120 \\times 0.8 = 96", size=DISPLAY_SIZE,
                        buff=GAP_MD)
            self.below_head(steps, buff=GAP_MD * 1.6)
            verdict = MathTex("\\$96 \\;\\neq\\; \\$100",
                              font_size=DISPLAY_SIZE, color=TERRACOTTA)
            verdict.next_to(steps, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(steps[0]), run_time=t.fill(0.2))
            self.play(Write(steps[1]), run_time=t.fill(0.2))
            self.play(Write(verdict), run_time=t.fill(0.22))
            t.hold()

        with self.beat("base_matters") as t:
            self.clear_all(t)
            self.set_head(t, "Percentages depend on their base")
            rows = eqs("20\\% \\text{ of } 100 = 20",
                       "20\\% \\text{ of } 120 = 24", size=DISPLAY_SIZE,
                       buff=GAP_MD)
            self.below_head(rows, buff=GAP_MD * 1.5)
            why = lines("the two percentages were applied",
                        "to different starting values",
                        size=BODY_SIZE, color=GREY)
            why.next_to(rows, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(rows), run_time=t.fill(0.3))
            self.play(Write(why), run_time=t.fill(0.3))
            t.hold()

        with self.beat("not_reversible") as t:
            self.clear_all(t)
            idea = lines("Percentage increase and decrease",
                         "are not automatically reversible.",
                         size=TITLE_SIZE)
            idea.move_to(UP * 0.3)
            self.play(Write(idea), run_time=t.fill(0.45))
            self.play(Create(self.underline(idea, TERRACOTTA)),
                      run_time=t.fill(0.15))
            t.hold()

    def negatives(self):
        with self.beat("neg_intro") as t:
            self.clear_all(t)
            self.set_head(t, "Stop memorising signs")
            tube = Rectangle(width=0.5, height=3.0, color=SLATE,
                             stroke_width=4)
            tube.move_to(LEFT * 4.2 + DOWN * 0.4)
            start = serif("5°C", BODY_SIZE)
            start.next_to(tube, UP, buff=GAP_SM)
            drop = serif("drops 8 degrees", LABEL_SIZE, GREY)
            drop.next_to(tube, RIGHT, buff=GAP_MD)
            end = serif("−3°C", BODY_SIZE, TERRACOTTA)
            end.next_to(tube, DOWN, buff=GAP_SM)
            result = MathTex("5 - 8 = -3", font_size=DISPLAY_SIZE,
                             color=CHARCOAL)
            result.move_to(RIGHT * 2.2 + DOWN * 0.4)
            self.play(Create(tube), Write(start), run_time=t.fill(0.2))
            self.play(Write(drop), Write(end), run_time=t.fill(0.2))
            self.play(Write(result), run_time=t.fill(0.25))
            t.hold()

        with self.beat("neg_numberline") as t:
            self.clear_all(t)
            self.set_head(t, "−4 + 7")
            line = NumberLine(x_range=[-6, 5, 1], length=11,
                              color=CHARCOAL, include_numbers=True,
                              font_size=32)
            line.numbers.set_color(CHARCOAL)
            line.move_to(DOWN * 0.4)
            a = Dot(line.n2p(-4), radius=0.09, color=SLATE)
            b = Dot(line.n2p(3), radius=0.09, color=SAGE)
            move = serif("move seven places to the right",
                         LABEL_SIZE, GREY)
            move.next_to(line, DOWN, buff=GAP_MD * 1.2)
            answer = MathTex("-4 + 7 = 3", font_size=DISPLAY_SIZE,
                             color=SAGE)
            answer.next_to(move, DOWN, buff=GAP_MD)
            self.play(Create(line), run_time=t.fill(0.22))
            self.play(Create(a), run_time=t.fill(0.06))
            self.play(Write(move), Create(b), run_time=t.fill(0.2))
            self.play(Write(answer), run_time=t.fill(0.2))
            t.hold()

        with self.beat("neg_pattern") as t:
            self.clear_all(t)
            self.set_head(t, "Look for the pattern")
            rows = eqs("3 \\times 2 = 6", "2 \\times 2 = 4",
                       "1 \\times 2 = 2", "0 \\times 2 = 0",
                       "-1 \\times 2 = -2", "-2 \\times 2 = -4",
                       size=EQUATION_SIZE, buff=GAP_SM * 1.1)
            self.below_head(rows, buff=GAP_MD * 1.2)
            for row in rows:
                self.play(Write(row), run_time=t.fill(0.1))
            forces = serif("the pattern forces the result",
                           LABEL_SIZE, GREY)
            forces.next_to(rows, DOWN, buff=GAP_MD)
            self.play(Write(forces), run_time=t.fill(0.15))
            t.hold()

        with self.beat("neg_pattern2") as t:
            self.clear_all(t)
            self.set_head(t, "Now with −2")
            rows = eqs("3 \\times (-2) = -6", "2 \\times (-2) = -4",
                       "1 \\times (-2) = -2", "0 \\times (-2) = 0",
                       size=EQUATION_SIZE, buff=GAP_SM * 1.1)
            self.below_head(rows, buff=GAP_MD * 1.2)
            for row in rows:
                self.play(Write(row), run_time=t.fill(0.1))
            ask = MathTex("-1 \\times (-2) = \\;?", font_size=EQUATION_SIZE,
                          color=GREY)
            ask.next_to(rows, DOWN, buff=GAP_SM * 1.4)
            answer = MathTex("-1 \\times (-2) = +2",
                             font_size=EQUATION_SIZE, color=SAGE)
            answer.move_to(ask)
            self.play(Write(ask), run_time=t.fill(0.15))
            self.play(TransformMatchingTex(ask, answer),
                      run_time=t.fill(0.2))
            t.hold()

        with self.beat("sign_rule") as t:
            self.clear_all(t)
            rules = lines("same signs  →  positive",
                          "different signs  →  negative",
                          size=TITLE_SIZE)
            rules.move_to(UP * 0.4)
            works = serif("for multiplication and division",
                          BODY_SIZE, GREY)
            works.next_to(rules, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(rules), run_time=t.fill(0.4))
            self.play(Write(works), run_time=t.fill(0.2))
            t.hold()

        with self.beat("bracket_trap") as t:
            self.clear_all(t)
            self.set_head(t, "A classic exam trap")
            left = eqs("-3^2", "-(3^2)", "-9", size=DISPLAY_SIZE,
                       buff=GAP_SM * 1.2)
            right = eqs("(-3)^2", "(-3)\\times(-3)", "+9",
                        size=DISPLAY_SIZE, buff=GAP_SM * 1.2)
            left[-1].set_color(TERRACOTTA)
            right[-1].set_color(SAGE)
            pair = VGroup(left, right).arrange(RIGHT, buff=GAP_MD * 3.6)
            self.below_head(pair, buff=GAP_MD * 1.5)
            self.play(Write(left[0]), Write(right[0]), run_time=t.fill(0.14))
            self.play(Write(left[1]), Write(right[1]), run_time=t.fill(0.16))
            self.play(Write(left[2]), Write(right[2]), run_time=t.fill(0.16))
            note = serif("one pair of brackets — completely different result",
                         LABEL_SIZE, GREY)
            fit(note)
            note.next_to(pair, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(note), run_time=t.fill(0.2))
            t.hold()

    def powers(self):
        with self.beat("powers_intro") as t:
            self.clear_all(t)
            self.set_head(t, "Powers")
            wrong = MathTex("2^3 \\neq 2 \\times 3", font_size=DISPLAY_SIZE,
                            color=GREY)
            self.below_head(wrong, buff=GAP_MD * 1.3)
            right = MathTex("2^3 = 2 \\times 2 \\times 2 = 8",
                            font_size=DISPLAY_SIZE, color=CHARCOAL)
            right.next_to(wrong, DOWN, buff=GAP_MD * 1.3)
            idx = serif("the small number is the index, or exponent",
                        LABEL_SIZE, GREY)
            idx.next_to(right, DOWN, buff=GAP_MD * 1.2)
            self.play(Write(wrong), run_time=t.fill(0.2))
            self.play(Write(right), run_time=t.fill(0.25))
            self.play(Write(idx), run_time=t.fill(0.2))
            t.hold()

        with self.beat("squares_roots") as t:
            self.clear_all(t)
            self.set_head(t, "Inverse operations")
            pair = eqs("5^2 = 25", "\\sqrt{25} = 5", size=DISPLAY_SIZE,
                       buff=GAP_MD)
            self.below_head(pair, buff=GAP_MD * 1.5)
            note = serif("squaring goes one way — rooting brings you back",
                         BODY_SIZE, GREY)
            fit(note)
            note.next_to(pair, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(pair[0]), run_time=t.fill(0.2))
            self.play(Write(pair[1]), run_time=t.fill(0.2))
            self.play(Write(note), run_time=t.fill(0.25))
            t.hold()

        with self.beat("cubes") as t:
            self.clear_all(t)
            self.set_head(t, "Cubes and cube roots")
            pair = eqs("3^3 = 27", "\\sqrt[3]{27} = 3", size=DISPLAY_SIZE,
                       buff=GAP_MD)
            self.below_head(pair, buff=GAP_MD * 1.6)
            note = serif("one builds — the other reverses", BODY_SIZE, GREY)
            note.next_to(pair, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(pair[0]), run_time=t.fill(0.22))
            self.play(Write(pair[1]), run_time=t.fill(0.22))
            self.play(Write(note), run_time=t.fill(0.2))
            t.hold()

        with self.beat("pm_root") as t:
            self.clear_all(t)
            self.set_head(t, "A crucial distinction")
            one = MathTex("\\sqrt{49} = 7", font_size=DISPLAY_SIZE,
                          color=CHARCOAL)
            self.below_head(one, buff=GAP_MD * 1.3)
            two = MathTex("x^2 = 49 \\;\\Rightarrow\\; x = 7 "
                          "\\;\\text{or}\\; x = -7",
                          font_size=DISPLAY_SIZE, color=CHARCOAL)
            fit(two)
            two.next_to(one, DOWN, buff=GAP_MD * 1.4)
            why = eqs("7^2 = 49 \\qquad (-7)^2 = 49",
                      size=EQUATION_SIZE, color=SAGE)
            why.next_to(two, DOWN, buff=GAP_MD * 1.3)
            self.play(Write(one), run_time=t.fill(0.18))
            self.play(Write(two), run_time=t.fill(0.28))
            self.play(Write(why), run_time=t.fill(0.22))
            t.hold()

        with self.beat("index_mult") as t:
            self.clear_all(t)
            self.set_head(t, "Multiplying powers")
            expand = eqs(
                "2^3 \\times 2^4",
                "(2\\!\\times\\!2\\!\\times\\!2)(2\\!\\times\\!2"
                "\\!\\times\\!2\\!\\times\\!2)",
                "2^7", size=EQUATION_SIZE, buff=GAP_SM * 1.3)
            expand[-1].set_color(SAGE)
            self.below_head(expand, buff=GAP_MD * 1.3)
            for row in expand:
                self.play(Write(row), run_time=t.fill(0.16))
            rule = MathTex("a^m \\times a^n = a^{m+n}",
                           font_size=DISPLAY_SIZE, color=CHARCOAL)
            rule.next_to(expand, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(rule), run_time=t.fill(0.25))
            t.hold()

        with self.beat("index_div") as t:
            self.clear_all(t)
            self.set_head(t, "Dividing powers")
            steps = eqs("2^7 \\div 2^3", "2^{7-3}", "2^4",
                        size=DISPLAY_SIZE, buff=GAP_SM * 1.3)
            steps[-1].set_color(SAGE)
            self.below_head(steps, buff=GAP_MD * 1.5)
            for row in steps:
                self.play(Write(row), run_time=t.fill(0.18))
            rule = MathTex("a^m \\div a^n = a^{m-n}",
                           font_size=DISPLAY_SIZE, color=CHARCOAL)
            rule.next_to(steps, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(rule), run_time=t.fill(0.22))
            t.hold()

        with self.beat("zero_index") as t:
            self.clear_all(t)
            self.set_head(t, "Where a⁰ = 1 comes from")
            steps = eqs("5^3 \\div 5^3 = 1", "5^{3-3} = 5^0",
                        "5^0 = 1", size=DISPLAY_SIZE, buff=GAP_SM * 1.3)
            steps[-1].set_color(SAGE)
            self.below_head(steps, buff=GAP_MD * 1.4)
            for row in steps:
                self.play(Write(row), run_time=t.fill(0.16))
            general = MathTex("a^0 = 1 \\qquad (a \\neq 0)",
                              font_size=DISPLAY_SIZE, color=CHARCOAL)
            general.next_to(steps, DOWN, buff=GAP_MD * 1.3)
            self.play(Write(general), run_time=t.fill(0.2))
            know = serif("now you know where it comes from",
                         LABEL_SIZE, GREY)
            know.next_to(general, DOWN, buff=GAP_MD)
            self.play(Write(know), run_time=t.fill(0.15))
            t.hold()

    def standard_form(self):
        with self.beat("std_form_why") as t:
            self.clear_all(t)
            self.set_head(t, "Standard form")
            big = MathTex("150{,}000{,}000 \\text{ km}",
                          font_size=DISPLAY_SIZE, color=CHARCOAL)
            self.below_head(big, buff=GAP_MD * 1.3)
            small = MathTex("0.0000001", font_size=DISPLAY_SIZE,
                            color=CHARCOAL)
            small.next_to(big, DOWN, buff=GAP_MD * 1.3)
            awkward = serif("awkward, very quickly — scientists needed "
                            "a compact language", LABEL_SIZE, GREY)
            fit(awkward)
            awkward.next_to(small, DOWN, buff=GAP_MD * 1.3)
            self.play(Write(big), run_time=t.fill(0.22))
            self.play(Write(small), run_time=t.fill(0.22))
            self.play(Write(awkward), run_time=t.fill(0.25))
            t.hold()

        with self.beat("std_form_def") as t:
            self.clear_all(t)
            form = MathTex("a \\times 10^n", font_size=TITLE_SIZE * 1.6,
                           color=CHARCOAL)
            form.move_to(UP * 0.9)
            cond = MathTex("1 \\leq a < 10", font_size=DISPLAY_SIZE,
                           color=TERRACOTTA)
            cond.next_to(form, DOWN, buff=GAP_MD * 1.6)
            matters = serif("that last condition is important",
                            LABEL_SIZE, GREY)
            matters.next_to(cond, DOWN, buff=GAP_MD * 1.2)
            self.play(Write(form), run_time=t.fill(0.3))
            self.play(Write(cond), run_time=t.fill(0.25))
            self.play(Write(matters), run_time=t.fill(0.15))
            t.hold()

        with self.beat("std_big") as t:
            self.clear_all(t)
            self.set_head(t, "A huge number")
            self.chain(t, ["45{,}000", "4.5 \\times 10^4"],
                       DOWN * 0.3, per=0.25)
            moved = serif("the point moved four places", LABEL_SIZE, GREY)
            moved.move_to(DOWN * 2.2)
            self.play(Write(moved), run_time=t.fill(0.2))
            t.hold()

        with self.beat("std_small") as t:
            self.clear_all(t)
            self.set_head(t, "A tiny number")
            self.chain(t, ["0.00072", "7.2 \\times 10^{-4}"],
                       DOWN * 0.3, per=0.25)
            moved = serif("four places the other way", LABEL_SIZE, GREY)
            moved.move_to(DOWN * 2.2)
            self.play(Write(moved), run_time=t.fill(0.2))
            t.hold()

        with self.beat("std_intuition") as t:
            self.clear_all(t)
            rules = lines("huge number  →  positive power",
                          "tiny number  →  negative power",
                          size=TITLE_SIZE)
            rules.move_to(ORIGIN)
            self.play(Write(rules), run_time=t.fill(0.55))
            t.hold()

        with self.beat("std_trap") as t:
            self.clear_all(t)
            self.set_head(t, "Is this standard form?")
            candidate = MathTex("45 \\times 10^3", font_size=DISPLAY_SIZE,
                                color=GREY)
            self.below_head(candidate, buff=GAP_MD * 1.3)
            why = serif("mathematically correct — but 45 is not "
                        "between 1 and 10", LABEL_SIZE, TERRACOTTA)
            fit(why)
            why.next_to(candidate, DOWN, buff=GAP_MD * 1.2)
            fixed = MathTex("= 4.5 \\times 10^4", font_size=DISPLAY_SIZE,
                            color=SAGE)
            fixed.next_to(why, DOWN, buff=GAP_MD * 1.3)
            self.play(Write(candidate), run_time=t.fill(0.2))
            self.play(Write(why), run_time=t.fill(0.25))
            self.play(Write(fixed), run_time=t.fill(0.22))
            t.hold()

    def rounding(self):
        with self.beat("rounding_intro") as t:
            self.clear_all(t)
            self.set_head(t, "The art of being approximately right")
            idea = lines("an approximate answer is not",
                         "an inferior answer", size=BODY_SIZE)
            self.below_head(idea, buff=GAP_MD * 1.6)
            self.play(Write(idea), run_time=t.fill(0.4))
            self.arc_focus(t, 2)
            t.hold()

        with self.beat("decimal_places") as t:
            self.clear_all(t)
            self.set_head(t, "Two decimal places")
            number = MathTex("7.846291\\ldots", font_size=DISPLAY_SIZE,
                             color=CHARCOAL)
            self.below_head(number, buff=GAP_MD * 1.3)
            look = serif("the third decimal digit is 6 — five or more, "
                         "round up", LABEL_SIZE, GREY)
            fit(look)
            look.next_to(number, DOWN, buff=GAP_MD * 1.3)
            answer = MathTex("7.85", font_size=DISPLAY_SIZE, color=SAGE)
            answer.next_to(look, DOWN, buff=GAP_MD * 1.3)
            self.play(Write(number), run_time=t.fill(0.22))
            self.play(Write(look), run_time=t.fill(0.25))
            self.play(Write(answer), run_time=t.fill(0.2))
            t.hold()

        with self.beat("sig_figs") as t:
            self.clear_all(t)
            self.set_head(t, "Two significant figures")
            number = MathTex("7{,}846", font_size=DISPLAY_SIZE,
                             color=CHARCOAL)
            self.below_head(number, buff=GAP_MD * 1.3)
            steps = serif("first is 7, second is 8 — the next digit is 4, "
                          "so 8 stays", LABEL_SIZE, GREY)
            fit(steps)
            steps.next_to(number, DOWN, buff=GAP_MD * 1.3)
            answer = MathTex("7{,}800", font_size=DISPLAY_SIZE, color=SAGE)
            answer.next_to(steps, DOWN, buff=GAP_MD * 1.3)
            self.play(Write(number), run_time=t.fill(0.2))
            self.play(Write(steps), run_time=t.fill(0.25))
            self.play(Write(answer), run_time=t.fill(0.2))
            t.hold()

        with self.beat("sf_distinction") as t:
            self.clear_all(t)
            rows = lines("decimal places count from the decimal point",
                         "significant figures count from the",
                         "first non-zero digit", size=BODY_SIZE)
            rows.move_to(ORIGIN)
            self.play(Write(rows), run_time=t.fill(0.55))
            t.hold()

        with self.beat("sf_small") as t:
            self.clear_all(t)
            self.set_head(t, "Small numbers")
            number = MathTex("0.004763", font_size=DISPLAY_SIZE,
                             color=CHARCOAL)
            self.below_head(number, buff=GAP_MD * 1.3)
            note = serif("leading zeros don't count — first is 4, "
                         "second is 7", LABEL_SIZE, GREY)
            fit(note)
            note.next_to(number, DOWN, buff=GAP_MD * 1.2)
            answer = MathTex("0.0048", font_size=DISPLAY_SIZE, color=SAGE)
            answer.next_to(note, DOWN, buff=GAP_MD * 1.3)
            self.play(Write(number), run_time=t.fill(0.2))
            self.play(Write(note), run_time=t.fill(0.25))
            self.play(Write(answer), run_time=t.fill(0.2))
            t.hold()

        with self.beat("estimation") as t:
            self.clear_all(t)
            self.set_head(t, "Estimate first")
            original = MathTex("\\frac{19.8 \\times 4.91}{0.203}",
                               font_size=DISPLAY_SIZE, color=CHARCOAL)
            self.below_head(original, buff=GAP_MD * 1.2)
            rounded = MathTex("\\frac{20 \\times 5}{0.2}",
                              font_size=DISPLAY_SIZE, color=CHARCOAL)
            rounded.next_to(original, DOWN, buff=GAP_MD * 1.2)
            answer = MathTex("= \\frac{100}{0.2} = 500",
                             font_size=DISPLAY_SIZE, color=SAGE)
            answer.next_to(rounded, DOWN, buff=GAP_MD * 1.2)
            self.play(Write(original), run_time=t.fill(0.25))
            self.play(Write(rounded), run_time=t.fill(0.22))
            self.play(Write(answer), run_time=t.fill(0.22))
            t.hold()

        with self.beat("lie_detector") as t:
            self.clear_all(t)
            self.set_head(t, "Your mathematical lie detector")
            bad = MathTex("4.92 \\;\\text{---something is wrong}",
                          font_size=EQUATION_SIZE, color=TERRACOTTA)
            fit(bad)
            self.below_head(bad, buff=GAP_MD * 1.3)
            good = MathTex("492.7 \\;\\text{---that looks reasonable}",
                           font_size=EQUATION_SIZE, color=SAGE)
            fit(good)
            good.next_to(bad, DOWN, buff=GAP_MD * 1.3)
            ask = serif('it asks: "does this answer make sense?"',
                        BODY_SIZE, GREY)
            ask.next_to(good, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(bad), run_time=t.fill(0.2))
            self.play(Write(good), run_time=t.fill(0.2))
            self.play(Write(ask), run_time=t.fill(0.25))
            t.hold()

    def challenges(self):
        def challenge(t, title, steps, tag=None, arc_index=None):
            self.clear_all(t)
            self.set_head(t, title)
            rows = eqs(*steps, size=DISPLAY_SIZE, buff=GAP_SM * 1.3)
            rows[-1].set_color(SAGE)
            self.below_head(rows, buff=GAP_MD * 1.5)
            for row in rows:
                self.play(Write(row), run_time=t.fill(0.16))
            if tag:
                label = serif(tag, BODY_SIZE, TERRACOTTA)
                label.next_to(rows, DOWN, buff=GAP_MD * 1.4)
                self.play(Write(label), run_time=t.fill(0.14))
            if arc_index is not None:
                self.arc_focus(t, arc_index, fraction=0.1)

        with self.beat("challenge1") as t:
            challenge(t, "Challenge 1 — convert 3/8",
                      ["3 \\div 8 = 0.375", "0.375 \\times 100 = 37.5\\%"],
                      tag="that's represent", arc_index=0)
            t.hold()

        with self.beat("challenge2") as t:
            challenge(t, "Challenge 2 — $800, reduced 15%",
                      ["100\\% - 15\\% = 85\\%",
                       "800 \\times 0.85 = \\$680"],
                      tag="that's operate", arc_index=1)
            t.hold()

        with self.beat("challenge3") as t:
            challenge(t, "Challenge 3 — mind the brackets",
                      ["(-4)^2 - 3^2", "16 - 9", "7"])
            t.hold()

        with self.beat("challenge4") as t:
            challenge(t, "Challenge 4 — standard form",
                      ["0.000056", "5.6 \\times 10^{-5}"])
            t.hold()

        with self.beat("challenge5") as t:
            challenge(t, "Challenge 5 — 2 significant figures",
                      ["0.007864", "0.0079"])
            t.hold()

        with self.beat("challenge6") as t:
            self.clear_all(t)
            self.set_head(t, "Challenge 6 — the A* question")
            story = lines("a shop raises a price by 25%",
                          "to return to the original price,",
                          "should it cut the new price by 25%?",
                          size=BODY_SIZE)
            self.below_head(story, buff=GAP_MD * 1.6)
            self.play(Write(story), run_time=t.fill(0.45))
            self.arc_focus(t, 3, fraction=0.12)
            t.hold()

        with self.beat("challenge6_calc") as t:
            self.clear_all(t)
            self.set_head(t, "Let's prove it")
            steps = eqs("100 \\times 1.25 = 125",
                        "125 - 100 = 25",
                        "\\tfrac{25}{125} \\times 100 = 20\\%",
                        size=DISPLAY_SIZE, buff=GAP_SM * 1.3)
            steps[-1].set_color(SAGE)
            self.below_head(steps, buff=GAP_MD * 1.4)
            for row in steps:
                self.play(Write(row), run_time=t.fill(0.18))
            verdict = serif("a 25% rise needs a 20% cut to undo it",
                            BODY_SIZE, TERRACOTTA)
            fit(verdict)
            verdict.next_to(steps, DOWN, buff=GAP_MD * 1.3)
            self.play(Write(verdict), run_time=t.fill(0.2))
            t.hold()

        with self.beat("never_cancel") as t:
            self.clear_all(t)
            rule = lines("Never assume percentages cancel.",
                         "Ask: percentage of what?", size=TITLE_SIZE)
            rule.move_to(UP * 0.2)
            self.play(Write(rule), run_time=t.fill(0.5))
            self.play(Create(self.underline(rule, TERRACOTTA)),
                      run_time=t.fill(0.15))
            t.hold()

    def closing(self):
        with self.beat("closing_choose") as t:
            self.clear_all(t)
            idea = lines("A strong mathematics student",
                         "doesn't just calculate.",
                         "A strong student chooses.", size=TITLE_SIZE)
            idea.move_to(ORIGIN)
            self.play(Write(idea), run_time=t.fill(0.6))
            t.hold()

        with self.beat("closing_list") as t:
            self.clear_all(t)
            self.set_head(t, "Today you chose")
            choices = lines(
                "the most useful representation",
                "the correct multiplier",
                "what the signs were actually doing",
                "the pattern underneath the powers",
                "standard form for the enormous and the tiny",
                size=BODY_SIZE, buff=GAP_SM * 1.2)
            self.below_head(choices, buff=GAP_MD * 1.3)
            for choice in choices:
                self.play(Write(choice), run_time=t.fill(0.12))
            judged = serif("and you didn't trust the calculator — "
                           "you estimated, you judged", LABEL_SIZE,
                           TERRACOTTA)
            fit(judged)
            judged.next_to(choices, DOWN, buff=GAP_MD * 1.3)
            self.play(Write(judged), run_time=t.fill(0.22))
            t.hold()

        with self.beat("closing_four") as t:
            self.clear_all(t)
            dont = lines("Don't become a human calculator.",
                         "Calculators already exist.",
                         size=BODY_SIZE, color=GREY)
            dont.move_to(UP * 2.2)
            arc = WordArc(FOUR, size=TITLE_SIZE, lit=CHARCOAL)
            for cell in arc.cells:
                cell.set_color(CHARCOAL)
            arc.move_to(DOWN * 0.2)
            self.play(Write(dont), run_time=t.fill(0.3))
            self.play(Write(arc), run_time=t.fill(0.35))
            t.hold()

        with self.beat("closing_think") as t:
            final = lines("You're learning to think mathematically.",
                          size=TITLE_SIZE)
            final.move_to(DOWN * 2.4)
            self.play(Write(final), run_time=t.fill(0.5))
            t.hold()
