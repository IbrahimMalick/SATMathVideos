"""Concept lecture: the building blocks of mathematics (O Level, OL01).

Narration script: scripts/OL01-building-blocks.md
Types of numbers, then BODMAS, with worked order-of-operations chains.
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


class BuildingBlocks(SATScene):
    scene_id = "concept.building_blocks"

    def construct(self):
        self.margin_note = mono("OL01 · building blocks", MARGIN_SIZE)
        self.margin_note.to_corner(UP + LEFT, buff=GAP_SM)
        self.add(self.margin_note)
        self.section_head = None
        self.work = VGroup()

        self.opening()
        self.number_families()
        self.primes()
        self.rational_irrational()
        self.bodmas_section()

    # -------------------------------------------------------------- helpers

    def clear_all(self, t, fraction=0.1):
        old = [m for m in self.mobjects if m is not self.margin_note]
        if old:
            self.play(*[FadeOut(m) for m in old], run_time=t.fill(fraction))
        self.work = VGroup()
        self.section_head = None

    def swap_work(self, t, fraction=0.08):
        if len(self.work) > 0:
            self.play(*[FadeOut(m) for m in self.work], run_time=t.fill(fraction))
            self.work = VGroup()

    def set_head(self, t, text, fraction=0.25):
        head = serif(text, TITLE_SIZE)
        head.to_edge(UP, buff=GAP_MD * 1.6)
        self.play(Write(head), run_time=t.fill(fraction))
        self.section_head = head

    # ------------------------------------------------------------- sections

    def opening(self):
        title = serif("The Building Blocks", TITLE_SIZE * 1.2)
        title.to_edge(UP, buff=GAP_MD * 1.8)
        subtitle = serif("O Level Mathematics · Lecture 1", LABEL_SIZE, GREY)
        subtitle.next_to(title, DOWN, buff=GAP_MD)

        with self.beat("open") as t:
            self.play(Write(title), run_time=t.fill(0.35))
            self.play(Write(subtitle), run_time=t.fill(0.2))
            t.hold()

        quote = serif('"I know how to do this... but I got the wrong answer?"',
                      BODY_SIZE)
        quote.next_to(subtitle, DOWN, buff=GAP_MD * 1.6)

        with self.beat("hook") as t:
            self.play(Write(quote), run_time=t.fill(0.4))
            t.hold()

        traps = serif("a negative sign · the order · a fraction · a prime factor",
                      LABEL_SIZE, GREY)
        traps.next_to(quote, DOWN, buff=GAP_MD * 1.3)
        crack = serif("one small mistake — the whole answer falls apart",
                      LABEL_SIZE, TERRACOTTA)
        crack.next_to(traps, DOWN, buff=GAP_MD)

        with self.beat("small_mistakes") as t:
            self.play(Write(traps), run_time=t.fill(0.3))
            self.play(Write(crack), run_time=t.fill(0.25))
            t.hold()

        house = serif("a weak foundation cracks the whole house", BODY_SIZE)
        house.next_to(crack, DOWN, buff=GAP_MD * 1.3)
        house_line = underline(house)

        with self.beat("foundation") as t:
            self.play(Write(house), run_time=t.fill(0.3))
            self.play(Create(house_line), run_time=t.fill(0.12))
            t.hold()

        agenda = VGroup(
            serif("1  types of numbers", BODY_SIZE),
            serif("2  order of operations", BODY_SIZE),
            serif("3  comparing and ordering", BODY_SIZE),
            serif("4  prime factorisation", BODY_SIZE),
        ).arrange(DOWN, buff=GAP_SM * 1.4, aligned_edge=LEFT)
        agenda.next_to(subtitle, DOWN, buff=GAP_MD * 1.4)
        paper1 = mono("paper 1: no calculator to rescue you", MARGIN_SIZE)
        paper1.next_to(agenda, DOWN, buff=GAP_MD * 1.2)

        with self.beat("agenda") as t:
            self.play(FadeOut(quote), FadeOut(traps), FadeOut(crack),
                      FadeOut(house), FadeOut(house_line), run_time=t.fill(0.1))
            self.play(Write(agenda), run_time=t.fill(0.35))
            self.play(Write(paper1), run_time=t.fill(0.15))
            t.hold()

    def number_families(self):
        with self.beat("families") as t:
            self.clear_all(t)
            self.set_head(t, "Part 1 — Types of numbers")
            note = serif("numbers belong to families — and can belong to several",
                         LABEL_SIZE, GREY)
            note.next_to(self.section_head, DOWN, buff=GAP_MD)
            self.play(Write(note), run_time=t.fill(0.3))
            self.section_head = VGroup(self.section_head, note)
            t.hold()

        nat_label = serif("natural — the counting numbers", BODY_SIZE)
        nat = MathTex("1,\\ 2,\\ 3,\\ 4,\\ 5,\\ \\dots",
                      font_size=DISPLAY_SIZE, color=CHARCOAL)
        chai = serif('"bring me negative two cups of chai" — no',
                     LABEL_SIZE, GREY)
        nat_group = VGroup(nat_label, nat, chai).arrange(
            DOWN, buff=GAP_SM * 1.4
        )
        nat_group.next_to(self.section_head, DOWN, buff=GAP_MD * 1.2)

        with self.beat("natural") as t:
            self.play(Write(nat_label), run_time=t.fill(0.2))
            self.play(Write(nat), run_time=t.fill(0.25))
            self.play(Write(chai), run_time=t.fill(0.15))
            self.work.add(nat_group)
            t.hold()

        int_label = serif("integers — whole numbers, both directions", BODY_SIZE)
        ints = MathTex("\\dots,\\ -3,\\ -2,\\ -1,\\ 0,\\ 1,\\ 2,\\ 3,\\ \\dots",
                       font_size=DISPLAY_SIZE, color=CHARCOAL)
        int_group = VGroup(int_label, ints).arrange(DOWN, buff=GAP_SM * 1.4)
        int_group.next_to(nat_group, DOWN, buff=GAP_MD * 1.1)

        with self.beat("integers") as t:
            self.play(Write(int_label), run_time=t.fill(0.2))
            self.play(Write(ints), run_time=t.fill(0.3))
            self.work.add(int_group)
            t.hold()

        examples = serif("−5°C in Ziarat · owing the bank 2,000 rupees",
                         LABEL_SIZE, GREY)
        examples.next_to(int_group, DOWN, buff=GAP_MD)

        with self.beat("integers_ex") as t:
            self.play(Write(examples), run_time=t.fill(0.3))
            self.work.add(examples)
            t.hold()

        with self.beat("int_check") as t:
            self.swap_work(t)
            checks = VGroup(
                MathTex("4.5\\ ?", font_size=EQUATION_SIZE, color=TERRACOTTA),
                serif("no — integers have no decimal part", LABEL_SIZE, GREY),
                MathTex("-7\\ \\checkmark \\qquad 0\\ \\checkmark",
                        font_size=EQUATION_SIZE, color=SAGE),
                serif("zero is an integer — students forget that", LABEL_SIZE, GREY),
            ).arrange(DOWN, buff=GAP_SM * 1.4)
            checks.next_to(self.section_head, DOWN, buff=GAP_MD * 1.3)
            for c in checks:
                self.play(Write(c), run_time=t.fill(0.12))
            self.work.add(checks)
            t.hold()

    def primes(self):
        with self.beat("primes") as t:
            self.clear_all(t)
            self.set_head(t, "Prime numbers")
            rule = serif("exactly two positive factors: 1 and itself",
                         LABEL_SIZE, GREY)
            rule.next_to(self.section_head, DOWN, buff=GAP_MD)
            plist = MathTex("2,\\ 3,\\ 5,\\ 7", font_size=DISPLAY_SIZE,
                            color=SAGE)
            plist.next_to(rule, DOWN, buff=GAP_MD)
            six = MathTex("6:\\ 1,\\ 2,\\ 3,\\ 6", font_size=EQUATION_SIZE,
                          color=TERRACOTTA)
            six_note = serif("too many factors — not prime", LABEL_SIZE, GREY)
            six_group = VGroup(six, six_note).arrange(DOWN, buff=GAP_SM * 1.2)
            six_group.next_to(plist, DOWN, buff=GAP_MD)
            self.play(Write(rule), run_time=t.fill(0.2))
            self.play(Write(plist), run_time=t.fill(0.2))
            self.play(Write(six), run_time=t.fill(0.2))
            self.play(Write(six_note), run_time=t.fill(0.12))
            self.section_head = VGroup(self.section_head, rule)
            self.work.add(plist, six_group)
            t.hold()

        trap = serif("1 is not prime — it has only one factor", BODY_SIZE)
        trap.next_to(self.work[1], DOWN, buff=GAP_MD * 1.1)
        trap_line = underline(trap, TERRACOTTA)

        with self.beat("one_trap") as t:
            self.play(Write(trap), run_time=t.fill(0.3))
            self.play(Create(trap_line), run_time=t.fill(0.12))
            self.work.add(trap, trap_line)
            t.hold()

        even = serif("2 — the only even prime", LABEL_SIZE)
        even.next_to(trap, DOWN, buff=GAP_MD)

        with self.beat("two_even") as t:
            self.play(Write(even), run_time=t.fill(0.3))
            self.work.add(even)
            t.hold()

        with self.beat("prime_check") as t:
            self.swap_work(t)
            row = MathTex(
                "11\\ \\checkmark \\quad 13\\ \\checkmark \\quad "
                "15\\ \\times \\quad 17\\ \\checkmark \\quad 21\\ \\times",
                font_size=EQUATION_SIZE, color=CHARCOAL,
            )
            row.next_to(self.section_head, DOWN, buff=GAP_MD * 1.4)
            why = serif("15 = 3 × 5 · 21 = 3 × 7", LABEL_SIZE, GREY)
            why.next_to(row, DOWN, buff=GAP_MD)
            self.play(Write(row), run_time=t.fill(0.4))
            self.play(Write(why), run_time=t.fill(0.2))
            self.work.add(row, why)
            t.hold()

    def rational_irrational(self):
        with self.beat("rational") as t:
            self.clear_all(t)
            self.set_head(t, "Rational and irrational")
            rat = VGroup(
                MathTex("\\frac{1}{2},\\quad \\frac{3}{4},\\quad 5 = \\frac{5}{1}",
                        font_size=DISPLAY_SIZE, color=CHARCOAL),
                MathTex("0.75 = \\frac{3}{4},\\quad 0.333\\dots = \\frac{1}{3}",
                        font_size=DISPLAY_SIZE, color=CHARCOAL),
            ).arrange(DOWN, buff=GAP_MD)
            rat.next_to(self.section_head, DOWN, buff=GAP_MD * 1.1)
            rat_note = serif("rational — it can be written as a fraction of "
                             "integers", LABEL_SIZE, GREY)
            rat_note.next_to(rat, DOWN, buff=GAP_MD)
            self.play(Write(rat), run_time=t.fill(0.4))
            self.play(Write(rat_note), run_time=t.fill(0.2))
            self.work.add(rat, rat_note)
            t.hold()

        irr = MathTex(
            "\\pi = 3.14159\\dots \\qquad \\sqrt{2} = 1.4142\\dots",
            font_size=EQUATION_SIZE, color=CHARCOAL,
        )
        irr.next_to(self.work[1], DOWN, buff=GAP_MD * 1.1)
        irr_note = serif("forever, with no repeating pattern — irrational",
                         LABEL_SIZE, GREY)
        irr_note.next_to(irr, DOWN, buff=GAP_MD)

        with self.beat("irrational") as t:
            self.play(Write(irr), run_time=t.fill(0.35))
            self.play(Write(irr_note), run_time=t.fill(0.2))
            self.work.add(irr, irr_note)
            t.hold()

        memory = serif("ratio → fraction → rational", BODY_SIZE)
        memory.next_to(irr_note, DOWN, buff=GAP_MD)
        memory_line = underline(memory)

        with self.beat("ratio_memory") as t:
            self.play(Write(memory), run_time=t.fill(0.3))
            self.play(Create(memory_line), run_time=t.fill(0.12))
            self.work.add(memory, memory_line)
            t.hold()

        with self.beat("overlap") as t:
            self.swap_work(t)
            five = MathTex("5", font_size=TITLE_SIZE * 1.6, color=CHARCOAL)
            tags = serif("natural · integer · prime · rational", BODY_SIZE)
            group = VGroup(five, tags).arrange(DOWN, buff=GAP_MD)
            group.next_to(self.section_head, DOWN, buff=GAP_MD * 1.4)
            note = serif("one number, several families", LABEL_SIZE, GREY)
            note.next_to(group, DOWN, buff=GAP_MD)
            self.play(Write(five), run_time=t.fill(0.2))
            self.play(Write(tags), run_time=t.fill(0.25))
            self.play(Write(note), run_time=t.fill(0.15))
            self.work.add(group, note)
            t.hold()

    def bodmas_section(self):
        with self.beat("bodmas") as t:
            self.clear_all(t)
            self.set_head(t, "Part 2 — BODMAS")
            letters = VGroup(
                serif("B — brackets", BODY_SIZE),
                serif("O — orders: powers and roots", BODY_SIZE),
                serif("D — division", BODY_SIZE),
                serif("M — multiplication", BODY_SIZE),
                serif("A — addition", BODY_SIZE),
                serif("S — subtraction", BODY_SIZE),
            ).arrange(DOWN, buff=GAP_SM * 1.2, aligned_edge=LEFT)
            letters.next_to(self.section_head, DOWN, buff=GAP_MD * 1.2)
            self.play(Write(letters), run_time=t.fill(0.5))
            self.work.add(letters)
            t.hold()

        agreed = serif("one agreed system — or answers disagree", LABEL_SIZE, GREY)
        agreed.next_to(self.work[0], DOWN, buff=GAP_MD)

        with self.beat("why_rule") as t:
            self.play(Write(agreed), run_time=t.fill(0.3))
            self.work.add(agreed)
            t.hold()

        with self.beat("samosa") as t:
            self.swap_work(t)
            right = MathTex("5 \\times 30 - 50 = 100",
                            font_size=DISPLAY_SIZE, color=CHARCOAL)
            right[0].set_color(SAGE)
            wrong = MathTex("5 \\times (30 - 50) = -100",
                            font_size=DISPLAY_SIZE, color=CHARCOAL)
            wrong[0].set_color(TERRACOTTA)
            pair = VGroup(right, wrong).arrange(DOWN, buff=GAP_MD)
            pair.next_to(self.section_head, DOWN, buff=GAP_MD * 1.3)
            joke = serif("the shopkeeper does not owe you money — order matters",
                         LABEL_SIZE, GREY)
            joke.next_to(pair, DOWN, buff=GAP_MD)
            self.play(Write(right), run_time=t.fill(0.25))
            self.play(Write(wrong), run_time=t.fill(0.25))
            self.play(Write(joke), run_time=t.fill(0.15))
            self.work.add(pair, joke)
            t.hold()

        step1 = MathTex("12 + 8 \\div (9 - 5)", font_size=DISPLAY_SIZE,
                        color=CHARCOAL)
        step2 = MathTex("12 + 8 \\div 4", font_size=DISPLAY_SIZE, color=CHARCOAL)
        step3 = MathTex("12 + 2", font_size=DISPLAY_SIZE, color=CHARCOAL)
        step4 = MathTex("14", font_size=DISPLAY_SIZE, color=SAGE)
        for s in (step1, step2, step3, step4):
            s.move_to(DOWN * 0.4)

        with self.beat("example1") as t:
            self.swap_work(t)
            label = serif("bracket → division → addition", LABEL_SIZE, GREY)
            label.move_to(UP * 0.8)
            self.play(Write(label), run_time=t.fill(0.12))
            self.play(Write(step1), run_time=t.fill(0.15))
            self.play(TransformMatchingTex(step1, step2), run_time=t.fill(0.15))
            self.play(TransformMatchingTex(step2, step3), run_time=t.fill(0.15))
            self.play(TransformMatchingTex(step3, step4), run_time=t.fill(0.15))
            self.work.add(label, step4)
            t.hold()

        with self.beat("example2") as t:
            self.swap_work(t)
            wrong2 = MathTex("(3 + 4) \\times 5 = 35",
                             font_size=DISPLAY_SIZE, color=CHARCOAL)
            wrong2[0].set_color(TERRACOTTA)
            right2 = MathTex("3 + 4 \\times 5 = 3 + 20 = 23",
                             font_size=DISPLAY_SIZE, color=CHARCOAL)
            right2[0].set_color(SAGE)
            pair2 = VGroup(wrong2, right2).arrange(DOWN, buff=GAP_MD)
            pair2.next_to(self.section_head, DOWN, buff=GAP_MD * 1.4)
            note2 = serif("multiplication before addition", LABEL_SIZE, GREY)
            note2.next_to(pair2, DOWN, buff=GAP_MD)
            self.play(Write(wrong2), run_time=t.fill(0.25))
            self.play(Write(right2), run_time=t.fill(0.25))
            self.play(Write(note2), run_time=t.fill(0.12))
            self.work.add(pair2, note2)
            t.hold()

        with self.beat("equal_priority") as t:
            self.swap_work(t)
            rule = serif("÷ and × are equal — work left to right", BODY_SIZE)
            rule.next_to(self.section_head, DOWN, buff=GAP_MD * 1.3)
            rule_line = underline(rule)
            chain = MathTex("24 \\div 6 \\times 2 = 4 \\times 2 = 8",
                            font_size=DISPLAY_SIZE, color=CHARCOAL)
            chain.next_to(rule, DOWN, buff=GAP_MD * 1.2)
            self.play(Write(rule), run_time=t.fill(0.25))
            self.play(Create(rule_line), run_time=t.fill(0.1))
            self.play(Write(chain), run_time=t.fill(0.3))
            self.work.add(rule, rule_line, chain)
            t.hold()

        p1 = MathTex("2 + 3^2 \\times 4", font_size=DISPLAY_SIZE, color=CHARCOAL)
        p2 = MathTex("2 + 9 \\times 4", font_size=DISPLAY_SIZE, color=CHARCOAL)
        p3 = MathTex("2 + 36", font_size=DISPLAY_SIZE, color=CHARCOAL)
        p4 = MathTex("38", font_size=DISPLAY_SIZE, color=SAGE)
        for s in (p1, p2, p3, p4):
            s.move_to(DOWN * 1.9)

        with self.beat("powers") as t:
            self.play(Write(p1), run_time=t.fill(0.15))
            self.play(TransformMatchingTex(p1, p2), run_time=t.fill(0.18))
            self.play(TransformMatchingTex(p2, p3), run_time=t.fill(0.18))
            self.play(TransformMatchingTex(p3, p4), run_time=t.fill(0.15))
            self.work.add(p4)
            t.hold()

        with self.beat("control") as t:
            self.clear_all(t)
            control = serif("You need control — it should become automatic.",
                            BODY_SIZE)
            control.move_to(ORIGIN)
            control_line = underline(control)
            self.play(Write(control), run_time=t.fill(0.35))
            self.play(Create(control_line), run_time=t.fill(0.12))
            t.hold()
