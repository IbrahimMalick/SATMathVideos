"""Concept lecture: building blocks of mathematics, part 2 (O Level, OL02).

Narration script: scripts/OL02-building-blocks-p2.md
Comparing and ordering numbers, then prime factorisation with HCF/LCM,
closing review and homework.
"""

import numpy as np

from manim import (
    Create,
    Dot,
    FadeOut,
    Line,
    MathTex,
    NumberLine,
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


class BuildingBlocksP2(SATScene):
    scene_id = "concept.building_blocks_p2"

    def construct(self):
        self.margin_note = mono("OL01 · building blocks · part 2", MARGIN_SIZE)
        self.margin_note.to_corner(UP + LEFT, buff=GAP_SM)
        self.add(self.margin_note)
        self.section_head = None
        self.work = VGroup()

        self.ordering_section()
        self.prime_section()
        self.review_section()

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

    # ------------------------------------------------------------- ordering

    def ordering_section(self):
        with self.beat("ordering") as t:
            self.set_head(t, "Part 3 — Comparing and ordering")
            symbols = MathTex(">\\qquad <\\qquad \\neq",
                              font_size=DISPLAY_SIZE * 1.2, color=CHARCOAL)
            labels = serif("greater than · less than · not equal to",
                           LABEL_SIZE, GREY)
            group = VGroup(symbols, labels).arrange(DOWN, buff=GAP_MD)
            group.next_to(self.section_head, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(symbols), run_time=t.fill(0.3))
            self.play(Write(labels), run_time=t.fill(0.2))
            self.work.add(group)
            t.hold()

        big = MathTex("12 > 10", font_size=DISPLAY_SIZE * 1.3, color=CHARCOAL)
        big.next_to(self.work[0], DOWN, buff=GAP_MD * 1.3)
        mouth = serif("the open side faces the larger number", BODY_SIZE)
        mouth.next_to(big, DOWN, buff=GAP_MD)
        mouth_line = underline(mouth)

        with self.beat("open_side") as t:
            self.play(Write(big), run_time=t.fill(0.25))
            self.play(Write(mouth), run_time=t.fill(0.25))
            self.play(Create(mouth_line), run_time=t.fill(0.1))
            self.work.add(big, mouth, mouth_line)
            t.hold()

        with self.beat("data_package") as t:
            self.swap_work(t)
            packages = serif("10 GB  vs  12 GB — same price", BODY_SIZE)
            packages.next_to(self.section_head, DOWN, buff=GAP_MD * 1.4)
            verdict = MathTex("12 > 10", font_size=DISPLAY_SIZE, color=SAGE)
            verdict.next_to(packages, DOWN, buff=GAP_MD)
            self.play(Write(packages), run_time=t.fill(0.3))
            self.play(Write(verdict), run_time=t.fill(0.25))
            self.work.add(packages, verdict)
            t.hold()

        messy = serif("fractions · decimals · negatives · percentages",
                      LABEL_SIZE, GREY)
        messy.next_to(self.work[1], DOWN, buff=GAP_MD * 1.2)
        strategy = serif("now you need a strategy", BODY_SIZE, TERRACOTTA)
        strategy.next_to(messy, DOWN, buff=GAP_MD)

        with self.beat("messy") as t:
            self.play(Write(messy), run_time=t.fill(0.3))
            self.play(Write(strategy), run_time=t.fill(0.2))
            self.work.add(messy, strategy)
            t.hold()

        c1 = MathTex("\\frac{3}{4}\\ \\text{vs}\\ 0.8",
                     font_size=DISPLAY_SIZE, color=CHARCOAL)
        c2 = MathTex("0.75\\ \\text{vs}\\ 0.8",
                     font_size=DISPLAY_SIZE, color=CHARCOAL)
        c3 = MathTex("0.75 < 0.8", font_size=DISPLAY_SIZE, color=SAGE)
        for c in (c1, c2, c3):
            c.move_to(DOWN * 0.6)

        with self.beat("compare_convert") as t:
            self.swap_work(t)
            hint = serif("don't guess — convert to the same form",
                         LABEL_SIZE, GREY)
            hint.move_to(UP * 0.9)
            self.play(Write(hint), run_time=t.fill(0.15))
            self.play(Write(c1), run_time=t.fill(0.2))
            self.play(TransformMatchingTex(c1, c2), run_time=t.fill(0.2))
            self.play(TransformMatchingTex(c2, c3), run_time=t.fill(0.2))
            self.work.add(hint, c3)
            t.hold()

        rule = serif("put numbers into the same language", BODY_SIZE)
        rule.next_to(c3, DOWN, buff=GAP_MD * 1.3)
        rule_line = underline(rule)

        with self.beat("same_language") as t:
            self.play(Write(rule), run_time=t.fill(0.3))
            self.play(Create(rule_line), run_time=t.fill(0.12))
            self.work.add(rule, rule_line)
            t.hold()

        with self.beat("negatives") as t:
            self.swap_work(t)
            ask = serif("which is larger: −2 or −7?", BODY_SIZE)
            ask.next_to(self.section_head, DOWN, buff=GAP_MD * 1.2)
            line = NumberLine(
                x_range=[-8, 1, 1],
                length=10,
                color=CHARCOAL,
                include_numbers=True,
                font_size=34,
            )
            line.numbers.set_color(CHARCOAL)
            line.move_to(DOWN * 0.6)
            d7 = Dot(line.n2p(-7), color=SLATE, radius=0.1)
            d2 = Dot(line.n2p(-2), color=SAGE, radius=0.1)
            closer = serif("−2 is closer to zero", LABEL_SIZE, GREY)
            closer.next_to(line, DOWN, buff=GAP_MD * 1.1)
            self.play(Write(ask), run_time=t.fill(0.15))
            self.play(Create(line), run_time=t.fill(0.3))
            self.play(Create(d7), Create(d2), run_time=t.fill(0.12))
            self.play(Write(closer), run_time=t.fill(0.15))
            self.work.add(ask, line, d7, d2, closer)
            t.hold()

        temp = serif("−2° is warmer than −7°", BODY_SIZE)
        temp.next_to(self.work[4], DOWN, buff=GAP_MD)
        verdict2 = MathTex("-2 > -7", font_size=DISPLAY_SIZE, color=SAGE)
        verdict2.next_to(temp, DOWN, buff=GAP_MD * 0.9)

        with self.beat("temperature") as t:
            self.play(Write(temp), run_time=t.fill(0.25))
            self.play(Write(verdict2), run_time=t.fill(0.25))
            self.work.add(temp, verdict2)
            t.hold()

        with self.beat("neg_rule") as t:
            self.swap_work(t)
            careful = MathTex("-10 < -3", font_size=DISPLAY_SIZE,
                              color=CHARCOAL)
            careful.next_to(self.section_head, DOWN, buff=GAP_MD * 1.5)
            note = serif("the larger absolute value can be the smaller number",
                         BODY_SIZE)
            note.next_to(careful, DOWN, buff=GAP_MD)
            note_line = underline(note, TERRACOTTA)
            self.play(Write(careful), run_time=t.fill(0.25))
            self.play(Write(note), run_time=t.fill(0.3))
            self.play(Create(note_line), run_time=t.fill(0.1))
            self.work.add(careful, note, note_line)
            t.hold()

        sense = serif("have a feeling for where numbers live",
                      LABEL_SIZE, GREY)
        sense.next_to(self.work[2], DOWN, buff=GAP_MD * 1.2)

        with self.beat("number_sense") as t:
            self.play(Write(sense), run_time=t.fill(0.35))
            self.work.add(sense)
            t.hold()

    # ---------------------------------------------------------------- primes

    def prime_section(self):
        with self.beat("prime_intro") as t:
            self.clear_all(t)
            self.set_head(t, "Part 4 — Prime factorisation")
            dna = serif("prime factors are the DNA of a number", BODY_SIZE)
            dna.next_to(self.section_head, DOWN, buff=GAP_MD * 1.2)
            dna_line = underline(dna)
            plan = serif("break it down until only primes remain",
                         LABEL_SIZE, GREY)
            plan.next_to(dna, DOWN, buff=GAP_MD * 1.1)
            self.play(Write(dna), run_time=t.fill(0.3))
            self.play(Create(dna_line), run_time=t.fill(0.1))
            self.play(Write(plan), run_time=t.fill(0.2))
            self.work.add(dna, dna_line, plan)
            t.hold()

        # Factor tree for 36. Primes land in sage.
        n36 = MathTex("36", font_size=EQUATION_SIZE, color=CHARCOAL)
        n36.move_to(np.array([0.0, 1.3, 0]))
        n2a = MathTex("2", font_size=EQUATION_SIZE, color=SAGE)
        n2a.move_to(np.array([-1.6, 0.1, 0]))
        n18 = MathTex("18", font_size=EQUATION_SIZE, color=CHARCOAL)
        n18.move_to(np.array([1.6, 0.1, 0]))
        n2b = MathTex("2", font_size=EQUATION_SIZE, color=SAGE)
        n2b.move_to(np.array([0.4, -1.1, 0]))
        n9 = MathTex("9", font_size=EQUATION_SIZE, color=CHARCOAL)
        n9.move_to(np.array([2.8, -1.1, 0]))
        n3a = MathTex("3", font_size=EQUATION_SIZE, color=SAGE)
        n3a.move_to(np.array([2.0, -2.3, 0]))
        n3b = MathTex("3", font_size=EQUATION_SIZE, color=SAGE)
        n3b.move_to(np.array([3.6, -2.3, 0]))

        def branch(a, b):
            return Line(
                a.get_bottom() + DOWN * 0.12, b.get_top() + UP * 0.12,
                color=GREY, stroke_width=3,
            )

        with self.beat("tree36") as t:
            self.swap_work(t)
            self.play(Write(n36), run_time=t.fill(0.08))
            self.play(Create(branch(n36, n2a)), Create(branch(n36, n18)),
                      run_time=t.fill(0.1))
            self.play(Write(n2a), Write(n18), run_time=t.fill(0.12))
            self.play(Create(branch(n18, n2b)), Create(branch(n18, n9)),
                      run_time=t.fill(0.1))
            self.play(Write(n2b), Write(n9), run_time=t.fill(0.12))
            self.play(Create(branch(n9, n3a)), Create(branch(n9, n3b)),
                      run_time=t.fill(0.1))
            self.play(Write(n3a), Write(n3b), run_time=t.fill(0.12))
            self.work.add(*[m for m in self.mobjects
                            if m is not self.margin_note
                            and m is not self.section_head])
            t.hold()

        r1 = MathTex("36 = 2 \\times 2 \\times 3 \\times 3",
                     font_size=DISPLAY_SIZE, color=CHARCOAL)
        r2 = MathTex("36 = 2^2 \\times 3^2", font_size=DISPLAY_SIZE,
                     color=CHARCOAL)
        for r in (r1, r2):
            r.move_to(np.array([-3.6, -1.1, 0]))

        with self.beat("tree_result") as t:
            self.play(Write(r1), run_time=t.fill(0.25))
            self.play(TransformMatchingTex(r1, r2), run_time=t.fill(0.25))
            self.work.add(r2)
            t.hold()

        with self.beat("routes") as t:
            self.swap_work(t)
            alt = MathTex(
                "36 = 4 \\times 9 = (2 \\times 2) \\times (3 \\times 3)"
                " = 2^2 \\times 3^2",
                font_size=EQUATION_SIZE, color=CHARCOAL,
            )
            alt.next_to(self.section_head, DOWN, buff=GAP_MD * 1.4)
            beauty = serif("different routes — the same building blocks",
                           BODY_SIZE)
            beauty.next_to(alt, DOWN, buff=GAP_MD * 1.1)
            beauty_line = underline(beauty)
            self.play(Write(alt), run_time=t.fill(0.35))
            self.play(Write(beauty), run_time=t.fill(0.25))
            self.play(Create(beauty_line), run_time=t.fill(0.1))
            self.work.add(alt, beauty, beauty_line)
            t.hold()

        care = VGroup(
            serif("HCF — highest common factor", BODY_SIZE),
            serif("LCM — lowest common multiple", BODY_SIZE),
        ).arrange(DOWN, buff=GAP_SM * 1.4, aligned_edge=LEFT)
        care.next_to(self.work[2], DOWN, buff=GAP_MD * 1.2)

        with self.beat("why_care") as t:
            self.play(Write(care), run_time=t.fill(0.35))
            self.work.add(care)
            t.hold()

        with self.beat("hcf") as t:
            self.swap_work(t)
            f12 = MathTex("12 = 2^2 \\times 3", font_size=DISPLAY_SIZE,
                          color=CHARCOAL)
            f18 = MathTex("18 = 2 \\times 3^2", font_size=DISPLAY_SIZE,
                          color=CHARCOAL)
            pair = VGroup(f12, f18).arrange(DOWN, buff=GAP_MD)
            pair.next_to(self.section_head, DOWN, buff=GAP_MD * 1.3)
            shared = serif("take the factors they share", LABEL_SIZE, GREY)
            shared.next_to(pair, DOWN, buff=GAP_MD)
            hcf = MathTex("\\text{HCF} = 2 \\times 3 = 6",
                          font_size=DISPLAY_SIZE, color=SAGE)
            hcf.next_to(shared, DOWN, buff=GAP_MD)
            self.play(Write(f12), run_time=t.fill(0.15))
            self.play(Write(f18), run_time=t.fill(0.15))
            self.play(Write(shared), run_time=t.fill(0.15))
            self.play(Write(hcf), run_time=t.fill(0.25))
            self.work.add(pair, shared, hcf)
            t.hold()

        with self.beat("lcm_buses") as t:
            self.swap_work(t)
            buses = VGroup(
                serif("Bus A — every 40 minutes", BODY_SIZE),
                serif("Bus B — every 15 minutes", BODY_SIZE),
                serif("both leave at 10:00", BODY_SIZE),
            ).arrange(DOWN, buff=GAP_SM * 1.4, aligned_edge=LEFT)
            buses.next_to(self.section_head, DOWN, buff=GAP_MD * 1.3)
            ask = serif("when do they next leave together? — that is the LCM",
                        LABEL_SIZE, GREY)
            ask.next_to(buses, DOWN, buff=GAP_MD * 1.1)
            self.play(Write(buses), run_time=t.fill(0.4))
            self.play(Write(ask), run_time=t.fill(0.2))
            self.work.add(buses, ask)
            t.hold()

        with self.beat("lcm_calc") as t:
            self.swap_work(t)
            f40 = MathTex("40 = 2^3 \\times 5", font_size=EQUATION_SIZE,
                          color=CHARCOAL)
            f15 = MathTex("15 = 3 \\times 5", font_size=EQUATION_SIZE,
                          color=CHARCOAL)
            pair = VGroup(f40, f15).arrange(DOWN, buff=GAP_SM * 1.4)
            pair.next_to(self.section_head, DOWN, buff=GAP_MD * 1.2)
            lcm1 = MathTex(
                "\\text{LCM} = 2^3 \\times 3 \\times 5",
                font_size=DISPLAY_SIZE, color=CHARCOAL,
            )
            lcm2 = MathTex("\\text{LCM} = 120", font_size=DISPLAY_SIZE,
                           color=SAGE)
            for m in (lcm1, lcm2):
                m.next_to(pair, DOWN, buff=GAP_MD * 1.1)
            when = serif("120 minutes = 2 hours → together again at 12:00",
                         BODY_SIZE)
            when.next_to(lcm1, DOWN, buff=GAP_MD * 1.1)
            self.play(Write(f40), run_time=t.fill(0.12))
            self.play(Write(f15), run_time=t.fill(0.12))
            self.play(Write(lcm1), run_time=t.fill(0.2))
            self.play(TransformMatchingTex(lcm1, lcm2),
                      run_time=t.fill(0.15))
            self.play(Write(when), run_time=t.fill(0.2))
            self.work.add(pair, lcm2, when)
            t.hold()

        with self.beat("recognition") as t:
            self.swap_work(t)
            disguise = serif("buses · flashing lights · repeating events",
                             BODY_SIZE)
            disguise.next_to(self.section_head, DOWN, buff=GAP_MD * 1.5)
            ah = serif('"ah — this is an LCM problem"', BODY_SIZE, TERRACOTTA)
            ah.next_to(disguise, DOWN, buff=GAP_MD)
            skill = serif("recognition separates knowing from using",
                          LABEL_SIZE, GREY)
            skill.next_to(ah, DOWN, buff=GAP_MD)
            self.play(Write(disguise), run_time=t.fill(0.25))
            self.play(Write(ah), run_time=t.fill(0.25))
            self.play(Write(skill), run_time=t.fill(0.15))
            self.work.add(disguise, ah, skill)
            t.hold()

    # ---------------------------------------------------------------- review

    def review_section(self):
        with self.beat("review") as t:
            self.clear_all(t)
            self.set_head(t, "Quick review")
            lines = VGroup(
                serif("natural — counting numbers from one", LABEL_SIZE),
                serif("integers — whole numbers, including zero", LABEL_SIZE),
                serif("prime — exactly two factors · 1 is not prime",
                      LABEL_SIZE),
                serif("2 — the only even prime", LABEL_SIZE),
                serif("rational — a fraction · irrational — never repeats",
                      LABEL_SIZE),
            ).arrange(DOWN, buff=GAP_SM * 1.3, aligned_edge=LEFT)
            lines.next_to(self.section_head, DOWN, buff=GAP_MD * 1.2)
            for line in lines:
                self.play(Write(line), run_time=t.fill(0.1))
            self.work.add(lines)
            t.hold()

        with self.beat("review_bodmas") as t:
            self.swap_work(t)
            bod = MathTex(
                "\\text{B} \\;\\to\\; \\text{O} \\;\\to\\; \\text{DM}"
                " \\;\\to\\; \\text{AS}",
                font_size=DISPLAY_SIZE, color=CHARCOAL,
            )
            bod.next_to(self.section_head, DOWN, buff=GAP_MD * 1.4)
            equal = serif("DM equal priority · AS equal priority — "
                          "left to right", BODY_SIZE)
            equal.next_to(bod, DOWN, buff=GAP_MD * 1.1)
            self.play(Write(bod), run_time=t.fill(0.3))
            self.play(Write(equal), run_time=t.fill(0.3))
            self.work.add(bod, equal)
            t.hold()

        compare = serif("comparing? — same form", BODY_SIZE)
        primes = serif("factorising? — break down until every factor is prime",
                       BODY_SIZE)
        both = VGroup(compare, primes).arrange(DOWN, buff=GAP_SM * 1.5)
        both.next_to(self.work[1], DOWN, buff=GAP_MD * 1.2)

        with self.beat("review_compare") as t:
            self.play(Write(compare), run_time=t.fill(0.25))
            self.play(Write(primes), run_time=t.fill(0.25))
            self.work.add(both)
            t.hold()

        with self.beat("homework") as t:
            self.swap_work(t)
            head = serif("Your homework", TITLE_SIZE)
            head.next_to(self.section_head, DOWN, buff=GAP_MD * 1.1)
            tasks = VGroup(
                serif("prime factorise: 24 · 36 · 45 · 60 · 72", BODY_SIZE),
                serif("pick any two — find their HCF and LCM", BODY_SIZE),
                serif("write five BODMAS questions — solve them", BODY_SIZE),
                serif("order fractions and decimals, smallest to largest",
                      BODY_SIZE),
            ).arrange(DOWN, buff=GAP_SM * 1.4, aligned_edge=LEFT)
            tasks.next_to(head, DOWN, buff=GAP_MD * 1.1)
            dont = serif("don't just watch — actually write them down",
                         LABEL_SIZE, GREY)
            dont.next_to(tasks, DOWN, buff=GAP_MD)
            self.play(Write(head), run_time=t.fill(0.12))
            for task in tasks:
                self.play(Write(task), run_time=t.fill(0.12))
            self.play(Write(dont), run_time=t.fill(0.12))
            self.work.add(head, tasks, dont)
            t.hold()

        paper = mono("paper 1: the calculator stays away", MARGIN_SIZE * 1.2)
        paper.next_to(self.work[2], DOWN, buff=GAP_MD * 1.1)

        with self.beat("paper1") as t:
            self.play(Write(paper), run_time=t.fill(0.35))
            self.work.add(paper)
            t.hold()

        with self.beat("closing") as t:
            self.clear_all(t)
            closing = serif("Not difficult mathematics. Strong foundations.",
                            BODY_SIZE * 1.1)
            closing.move_to(UP * 0.4)
            closing_line = underline(closing)
            bye = serif("see you in the next session · Allah Hafiz",
                        LABEL_SIZE, GREY)
            bye.next_to(closing, DOWN, buff=GAP_MD * 1.6)
            self.play(Write(closing), run_time=t.fill(0.3))
            self.play(Create(closing_line), run_time=t.fill(0.1))
            self.play(Write(bye), run_time=t.fill(0.25))
            t.hold()
