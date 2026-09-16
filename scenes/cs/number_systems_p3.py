"""CS lecture: number systems and data representation, part 3 (CS01).

Narration script: scripts/CS01-number-systems-p3.md
Binary addition column by column, overflow, logical shifts in both
directions, bits falling off the end, and MSB / LSB.
"""

import numpy as np

from manim import (
    Create,
    FadeIn,
    FadeOut,
    Line,
    MathTex,
    Transform,
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

CELL = 0.95


def bit_row(bits, color=CHARCOAL, size=DISPLAY_SIZE, cell=CELL):
    """Digits laid out on a fixed column grid so rows line up."""
    n = len(bits)
    row = VGroup(*[
        MathTex(b, font_size=size, color=color) for b in bits
    ])
    for i, cell_mob in enumerate(row):
        cell_mob.move_to(RIGHT * (i - (n - 1) / 2) * cell)
    return row


class NumberSystemsP3(SATScene):
    scene_id = "cs.number_systems_p3"

    def construct(self):
        self.margin_note = mono("CS · number systems · part 3", MARGIN_SIZE)
        self.margin_note.to_corner(UP + LEFT, buff=GAP_SM)
        self.add(self.margin_note)
        self.section_head = None
        self.work = VGroup()

        self.addition_rules()
        self.full_addition()
        self.overflow()
        self.left_shifts()
        self.right_shifts()
        self.losing_bits()
        self.msb_lsb()

    # -------------------------------------------------------------- helpers

    def clear_all(self, t, fraction=0.06):
        old = [m for m in self.mobjects if m is not self.margin_note]
        if old:
            self.play(*[FadeOut(m) for m in old], run_time=t.fill(fraction))
        self.work = VGroup()
        self.section_head = None

    def swap_work(self, t, fraction=0.05):
        if len(self.work) > 0:
            self.play(*[FadeOut(m) for m in self.work],
                      run_time=t.fill(fraction))
            self.work = VGroup()

    def set_head(self, t, text, fraction=0.1):
        head = serif(text, TITLE_SIZE)
        head.to_edge(UP, buff=GAP_MD * 1.5)
        self.play(Write(head), run_time=t.fill(fraction))
        self.section_head = head
        return head

    def underline(self, mobject, color=SAGE):
        return Line(
            mobject.get_corner(DOWN + LEFT) + DOWN * GAP_SM,
            mobject.get_corner(DOWN + RIGHT) + DOWN * GAP_SM,
            color=color, stroke_width=3,
        )

    def below_head(self, mobject, buff=GAP_MD * 1.3):
        if self.section_head is None:
            mobject.move_to(ORIGIN)
        else:
            mobject.next_to(self.section_head, DOWN, buff=buff)
        return mobject

    # ------------------------------------------------------------ sections

    def addition_rules(self):
        with self.beat("add_rules") as t:
            self.set_head(t, "Part 17 — Binary addition")
            rules = VGroup(*[
                MathTex(line, font_size=DISPLAY_SIZE, color=CHARCOAL)
                for line in ("0 + 0 = 0", "0 + 1 = 1", "1 + 0 = 1")
            ]).arrange(DOWN, buff=GAP_SM * 1.3)
            self.below_head(rules, buff=GAP_MD * 1.4)
            for rule in rules:
                self.play(Write(rule), run_time=t.fill(0.14))
            problem = MathTex("1 + 1 = \\;?", font_size=DISPLAY_SIZE,
                              color=TERRACOTTA)
            problem.next_to(rules, DOWN, buff=GAP_MD * 1.3)
            note = serif("binary has no digit 2", LABEL_SIZE, GREY)
            note.next_to(problem, DOWN, buff=GAP_MD)
            self.play(Write(problem), run_time=t.fill(0.18))
            self.play(Write(note), run_time=t.fill(0.15))
            self.work.add(rules, problem, note)
            self.add_rules_group = rules
            t.hold()

        with self.beat("carry_analogy") as t:
            self.swap_work(t)
            denary = MathTex("9 + 1 = 10", font_size=DISPLAY_SIZE,
                             color=GREY)
            binary = MathTex("1 + 1 = 10", font_size=DISPLAY_SIZE,
                             color=CHARCOAL)
            pair = VGroup(denary, binary).arrange(DOWN, buff=GAP_MD * 1.2)
            self.below_head(pair, buff=GAP_MD * 1.4)
            same = serif("write 0, carry 1 — the same move",
                         BODY_SIZE, TERRACOTTA)
            same.next_to(pair, DOWN, buff=GAP_MD * 1.3)
            self.play(Write(denary), run_time=t.fill(0.2))
            self.play(Write(binary), run_time=t.fill(0.2))
            self.play(Write(same), run_time=t.fill(0.2))
            self.work.add(pair, same)
            t.hold()

        with self.beat("triple") as t:
            self.swap_work(t)
            full = VGroup(*[
                MathTex(line, font_size=EQUATION_SIZE, color=CHARCOAL)
                for line in ("0 + 0 = 0", "0 + 1 = 1", "1 + 0 = 1",
                             "1 + 1 = 10", "1 + 1 + 1 = 11")
            ]).arrange(DOWN, buff=GAP_SM * 1.2)
            full[4].set_color(SAGE)
            self.below_head(full, buff=GAP_MD * 1.3)
            why = serif("three in denary is 11 in binary — "
                        "result 1, carry 1", LABEL_SIZE, GREY)
            why.next_to(full, DOWN, buff=GAP_MD * 1.2)
            self.play(Write(full), run_time=t.fill(0.35))
            self.play(Write(why), run_time=t.fill(0.2))
            self.work.add(full, why)
            t.hold()

    def full_addition(self):
        a, b = "00110101", "00101110"
        total = "01100011"
        # carries into columns 1..4 (0 is the leftmost column)
        carries = {1: "1", 2: "1", 3: "1", 4: "1"}

        with self.beat("add_setup") as t:
            self.clear_all(t)
            self.set_head(t, "Part 18 — A complete addition")
            row_a = bit_row(a)
            row_b = bit_row(b)
            row_a.move_to(UP * 0.9)
            row_b.next_to(row_a, DOWN, buff=GAP_SM * 1.2)
            plus = MathTex("+", font_size=DISPLAY_SIZE, color=CHARCOAL)
            plus.next_to(row_b, LEFT, buff=GAP_SM * 1.5)
            bar = Line(
                row_b.get_left() + LEFT * 0.4, row_b.get_right() + RIGHT * 0.2,
                color=GREY, stroke_width=3,
            )
            bar.next_to(row_b, DOWN, buff=GAP_SM)
            checks = VGroup(
                MathTex("32 + 16 + 4 + 1 = 53", font_size=LABEL_SIZE,
                        color=GREY),
                MathTex("32 + 8 + 4 + 2 = 46", font_size=LABEL_SIZE,
                        color=GREY),
            )
            checks[0].next_to(row_a, RIGHT, buff=GAP_MD * 1.4)
            checks[1].next_to(row_b, RIGHT, buff=GAP_MD * 1.4)
            # The check labels hang off the right, so centre the whole
            # assembly before anything is drawn or it clips the frame edge.
            block = VGroup(row_a, row_b, plus, bar, checks)
            block.move_to(ORIGIN).shift(UP * 0.55 + LEFT * 0.6)
            expect = MathTex("53 + 46 = 99", font_size=EQUATION_SIZE,
                             color=TERRACOTTA)
            expect.next_to(bar, DOWN, buff=GAP_MD * 1.6)
            self.play(Write(row_a), run_time=t.fill(0.15))
            self.play(Write(row_b), Write(plus), run_time=t.fill(0.15))
            self.play(Create(bar), run_time=t.fill(0.05))
            self.play(Write(checks), run_time=t.fill(0.22))
            self.play(Write(expect), run_time=t.fill(0.18))
            self.rows = VGroup(row_a, row_b, plus, bar, checks)
            self.expect = expect
            self.work.add(self.rows, expect)
            t.hold()

        with self.beat("add_columns") as t:
            self.play(FadeOut(self.expect), run_time=t.fill(0.04))
            self.work.remove(self.expect)
            row_b = self.rows[1]
            bar = self.rows[3]
            sum_row = bit_row(total)
            sum_row.next_to(bar, DOWN, buff=GAP_SM * 1.1)
            box = None
            carry_marks = VGroup()
            for i in range(7, -1, -1):
                target = VGroup(self.rows[0][i], row_b[i], sum_row[i])
                spotlight = self._column_spotlight(target)
                if box is None:
                    box = spotlight
                    self.play(Create(box), run_time=t.fill(0.03))
                else:
                    self.play(Transform(box, spotlight), run_time=t.fill(0.02))
                self.play(Write(sum_row[i]), run_time=t.fill(0.03))
                if i in carries:
                    mark = MathTex(carries[i], font_size=LABEL_SIZE,
                                   color=SLATE)
                    mark.move_to(self.rows[0][i])
                    mark.shift(UP * 0.85)
                    carry_marks.add(mark)
                    self.play(Write(mark), run_time=t.fill(0.02))
            self.play(FadeOut(box), run_time=t.fill(0.03))
            self.sum_row = sum_row
            self.work.add(sum_row, carry_marks)
            t.hold()

        with self.beat("add_verify") as t:
            check = MathTex("64 + 32 + 2 + 1 = 99", font_size=EQUATION_SIZE,
                            color=SAGE)
            check.next_to(self.sum_row, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(check), run_time=t.fill(0.35))
            self.play(Create(self.underline(check)), run_time=t.fill(0.12))
            self.work.add(check)
            t.hold()

        with self.beat("why_verify") as t:
            self.clear_all(t)
            self.set_head(t, "Always check by converting")
            why = VGroup(
                serif("converting back catches arithmetic slips", BODY_SIZE),
                serif("if the bits say 103 but the denary says 99,",
                      BODY_SIZE, GREY),
                serif("something went wrong", BODY_SIZE, GREY),
            ).arrange(DOWN, buff=GAP_SM * 1.3)
            self.below_head(why, buff=GAP_MD * 1.8)
            self.play(Write(why), run_time=t.fill(0.5))
            self.work.add(why)
            t.hold()

    def _column_spotlight(self, target):
        pad = 0.28
        left = target.get_left() + LEFT * pad
        right = target.get_right() + RIGHT * pad
        top = target.get_top() + UP * pad
        bottom = target.get_bottom() + DOWN * pad
        corners = [
            np.array([left[0], top[1], 0]),
            np.array([right[0], top[1], 0]),
            np.array([right[0], bottom[1], 0]),
            np.array([left[0], bottom[1], 0]),
        ]
        box = VGroup(*[
            Line(corners[i], corners[(i + 1) % 4], color=TERRACOTTA,
                 stroke_width=3)
            for i in range(4)
        ])
        return box

    def overflow(self):
        with self.beat("overflow_intro") as t:
            self.clear_all(t)
            self.set_head(t, "Part 19 — Overflow")
            reg = serif("an 8-bit register", BODY_SIZE)
            self.below_head(reg, buff=GAP_MD * 1.3)
            biggest = MathTex("11111111 = 255", font_size=DISPLAY_SIZE,
                              color=CHARCOAL)
            biggest.next_to(reg, DOWN, buff=GAP_MD * 1.3)
            self.play(Write(reg), run_time=t.fill(0.2))
            self.play(Write(biggest), run_time=t.fill(0.3))
            self.work.add(reg, biggest)
            self.biggest = biggest
            t.hold()

        with self.beat("overflow_def") as t:
            ask = MathTex("300 \\;\\rightarrow\\; \\text{8 bits?}",
                          font_size=DISPLAY_SIZE, color=CHARCOAL)
            ask.next_to(self.biggest, DOWN, buff=GAP_MD * 1.4)
            no = serif("no — the maximum is 255", BODY_SIZE, TERRACOTTA)
            no.next_to(ask, DOWN, buff=GAP_MD * 1.2)
            word = serif("this is OVERFLOW", BODY_SIZE)
            word.next_to(no, DOWN, buff=GAP_MD * 1.2)
            self.play(Write(ask), run_time=t.fill(0.22))
            self.play(Write(no), run_time=t.fill(0.2))
            self.play(Write(word), run_time=t.fill(0.2))
            self.work.add(ask, no, word)
            t.hold()

        with self.beat("overflow_wording") as t:
            self.clear_all(t)
            self.set_head(t, "Say it precisely")
            good = VGroup(
                serif("the result is outside the range representable",
                      BODY_SIZE),
                serif("by the available number of bits", BODY_SIZE),
            ).arrange(DOWN, buff=GAP_SM)
            self.below_head(good, buff=GAP_MD * 1.5)
            bad = serif('not: "the number gets really big"',
                        BODY_SIZE, GREY)
            bad.next_to(good, DOWN, buff=GAP_MD * 1.6)
            self.play(Write(good), run_time=t.fill(0.4))
            self.play(Create(self.underline(good)), run_time=t.fill(0.1))
            self.play(Write(bad), run_time=t.fill(0.25))
            self.work.add(good, bad)
            t.hold()

        with self.beat("overflow_carry") as t:
            self.clear_all(t)
            self.set_head(t, "The tell-tale sign")
            sign = VGroup(
                serif("a carry beyond the eighth bit", BODY_SIZE),
                serif("means the result will not fit", BODY_SIZE, TERRACOTTA),
            ).arrange(DOWN, buff=GAP_MD)
            self.below_head(sign, buff=GAP_MD * 1.8)
            self.play(Write(sign), run_time=t.fill(0.5))
            self.work.add(sign)
            t.hold()

    def shift_demo(self, t, before, after, before_val, after_val,
                   sum_tex, head_buff=GAP_MD * 1.3):
        """Two bit rows with the value underneath each."""
        top = bit_row(before)
        self.below_head(top, buff=head_buff)
        top_val = MathTex(before_val, font_size=EQUATION_SIZE, color=GREY)
        top_val.next_to(top, RIGHT, buff=GAP_MD * 1.6)
        bottom = bit_row(after)
        bottom.next_to(top, DOWN, buff=GAP_MD * 1.4)
        bottom_val = MathTex(after_val, font_size=EQUATION_SIZE, color=SAGE)
        bottom_val.next_to(bottom, RIGHT, buff=GAP_MD * 1.6)
        sums = MathTex(sum_tex, font_size=EQUATION_SIZE, color=CHARCOAL)
        sums.next_to(bottom, DOWN, buff=GAP_MD * 1.4)
        self.play(Write(top), Write(top_val), run_time=t.fill(0.18))
        self.play(Write(bottom), run_time=t.fill(0.18))
        self.play(Write(sums), Write(bottom_val), run_time=t.fill(0.2))
        group = VGroup(top, top_val, bottom, bottom_val, sums)
        self.work.add(group)
        return group

    def left_shifts(self):
        with self.beat("shift_left") as t:
            self.clear_all(t)
            self.set_head(t, "Part 20 — Logical left shift")
            self.shift_demo(
                t, "00001101", "00011010", "13", "26",
                "16 + 8 + 2 = 26",
            )
            t.hold()

        with self.beat("shift_left2") as t:
            self.clear_all(t)
            self.set_head(t, "Shift again")
            self.shift_demo(
                t, "00011010", "00110100", "26", "52",
                "32 + 16 + 4 = 52",
            )
            chain = MathTex("13 \\;\\rightarrow\\; 26 \\;\\rightarrow\\; 52",
                            font_size=DISPLAY_SIZE, color=TERRACOTTA)
            chain.next_to(self.work[0], DOWN, buff=GAP_MD * 1.4)
            self.play(Write(chain), run_time=t.fill(0.2))
            self.work.add(chain)
            t.hold()

        with self.beat("shift_n") as t:
            self.clear_all(t)
            self.set_head(t, "Part 21 — Shifting further")
            rows = VGroup(*[
                MathTex(line, font_size=EQUATION_SIZE, color=CHARCOAL)
                for line in (
                    "1 \\text{ place} \\;\\rightarrow\\; \\times 2",
                    "2 \\text{ places} \\;\\rightarrow\\; \\times 2^2 = 4",
                    "3 \\text{ places} \\;\\rightarrow\\; \\times 2^3 = 8",
                    "4 \\text{ places} \\;\\rightarrow\\; \\times 2^4 = 16",
                )
            ]).arrange(DOWN, buff=GAP_SM * 1.2, aligned_edge=LEFT)
            self.below_head(rows, buff=GAP_MD * 1.3)
            general = MathTex("n \\text{ places} \\;\\rightarrow\\; "
                              "\\times 2^n", font_size=DISPLAY_SIZE,
                              color=SAGE)
            general.next_to(rows, DOWN, buff=GAP_MD * 1.4)
            for row in rows:
                self.play(Write(row), run_time=t.fill(0.12))
            self.play(Write(general), run_time=t.fill(0.2))
            self.work.add(rows, general)
            t.hold()

        with self.beat("shift_caveat") as t:
            caveat = serif("provided no significant bits are lost",
                           BODY_SIZE, TERRACOTTA)
            caveat.next_to(self.work[1], DOWN, buff=GAP_MD * 1.4)
            self.play(Write(caveat), run_time=t.fill(0.45))
            self.work.add(caveat)
            t.hold()

    def right_shifts(self):
        with self.beat("shift_right") as t:
            self.clear_all(t)
            self.set_head(t, "Part 22 — Logical right shift")
            self.shift_demo(
                t, "01100000", "00110000", "96", "48",
                "32 + 16 = 48",
            )
            t.hold()

        with self.beat("shift_right2") as t:
            self.clear_all(t)
            self.set_head(t, "Shift again")
            self.shift_demo(
                t, "00110000", "00011000", "48", "24",
                "16 + 8 = 24",
            )
            chain = MathTex("96 \\;\\rightarrow\\; 48 \\;\\rightarrow\\; 24",
                            font_size=DISPLAY_SIZE, color=TERRACOTTA)
            chain.next_to(self.work[0], DOWN, buff=GAP_MD * 1.4)
            self.play(Write(chain), run_time=t.fill(0.2))
            self.work.add(chain)
            t.hold()

        with self.beat("shift_right_n") as t:
            self.clear_all(t)
            self.set_head(t, "Right shift divides")
            rows = VGroup(*[
                MathTex(line, font_size=EQUATION_SIZE, color=CHARCOAL)
                for line in (
                    "1 \\text{ place} \\;\\rightarrow\\; \\div 2",
                    "2 \\text{ places} \\;\\rightarrow\\; \\div 2^2 = 4",
                    "3 \\text{ places} \\;\\rightarrow\\; \\div 2^3 = 8",
                )
            ]).arrange(DOWN, buff=GAP_SM * 1.2, aligned_edge=LEFT)
            self.below_head(rows, buff=GAP_MD * 1.6)
            for row in rows:
                self.play(Write(row), run_time=t.fill(0.18))
            self.work.add(rows)
            t.hold()

    def losing_bits(self):
        with self.beat("bits_lost") as t:
            self.clear_all(t)
            self.set_head(t, "Part 23 — Bits can fall off")
            row = bit_row("11010110")
            row.move_to(DOWN * 0.2)
            left_note = serif("a 1 shifted past either edge is lost",
                              LABEL_SIZE, TERRACOTTA)
            left_note.next_to(row, UP, buff=GAP_MD * 1.3)
            right_note = serif("nothing wraps around", LABEL_SIZE, GREY)
            right_note.next_to(row, DOWN, buff=GAP_MD * 1.2)
            consequence = VGroup(
                serif("once bits are discarded, the neat", BODY_SIZE),
                serif("×2 or ÷2 reading breaks", BODY_SIZE),
            ).arrange(DOWN, buff=GAP_SM)
            consequence.next_to(right_note, DOWN, buff=GAP_MD * 1.3)
            self.play(Write(row), run_time=t.fill(0.2))
            self.play(Write(left_note), run_time=t.fill(0.18))
            self.play(Write(right_note), run_time=t.fill(0.15))
            self.play(Write(consequence), run_time=t.fill(0.25))
            self.work.add(row, left_note, right_note, consequence)
            t.hold()

        with self.beat("precise_statement") as t:
            self.clear_all(t)
            self.set_head(t, "The precise statement")
            statement = VGroup(
                serif("a logical left shift by n places multiplies",
                      BODY_SIZE),
                serif("by 2ⁿ — provided no significant bits", BODY_SIZE),
                serif("are lost from the representation", BODY_SIZE),
            ).arrange(DOWN, buff=GAP_SM)
            self.below_head(statement, buff=GAP_MD * 1.4)
            right = VGroup(
                serif("right shifts can discard low-order bits,",
                      LABEL_SIZE, GREY),
                serif("losing integer information", LABEL_SIZE, GREY),
            ).arrange(DOWN, buff=GAP_SM * 0.8)
            right.next_to(statement, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(statement), run_time=t.fill(0.45))
            self.play(Create(self.underline(statement)),
                      run_time=t.fill(0.1))
            self.play(Write(right), run_time=t.fill(0.22))
            self.work.add(statement, right)
            t.hold()

    def msb_lsb(self):
        with self.beat("msb_lsb") as t:
            self.clear_all(t)
            self.set_head(t, "Part 24 — MSB and LSB")
            row = bit_row("10110110")
            row.move_to(DOWN * 0.3)
            msb_line = Line(
                row[0].get_top() + UP * 1.1, row[0].get_top() + UP * 0.25,
                color=TERRACOTTA, stroke_width=3,
            )
            msb = serif("MSB", BODY_SIZE, TERRACOTTA)
            msb.next_to(msb_line, UP, buff=GAP_SM * 0.8)
            lsb_line = Line(
                row[7].get_bottom() + DOWN * 1.1,
                row[7].get_bottom() + DOWN * 0.25,
                color=SLATE, stroke_width=3,
            )
            lsb = serif("LSB", BODY_SIZE, SLATE)
            lsb.next_to(lsb_line, DOWN, buff=GAP_SM * 0.8)
            self.play(Write(row), run_time=t.fill(0.2))
            self.play(Create(msb_line), Write(msb), run_time=t.fill(0.22))
            self.play(Create(lsb_line), Write(lsb), run_time=t.fill(0.22))
            self.work.add(row, msb_line, msb, lsb_line, lsb)
            t.hold()

        with self.beat("msb_why") as t:
            self.clear_all(t)
            self.set_head(t, "Why those names?")
            rows = VGroup(
                serif("MSB — the highest-value position (left)", BODY_SIZE),
                serif("LSB — the lowest-value position (right)", BODY_SIZE),
            ).arrange(DOWN, buff=GAP_MD * 1.2)
            self.below_head(rows, buff=GAP_MD * 1.8)
            self.play(Write(rows[0]), run_time=t.fill(0.25))
            self.play(Write(rows[1]), run_time=t.fill(0.25))
            self.work.add(rows)
            t.hold()
