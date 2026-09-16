"""CS lecture: number systems and data representation, part 2 (CS01).

Narration script: scripts/CS01-number-systems-p2.md
Hexadecimal: why base 16 fits binary, the nibble table, all four
conversions, and where hex actually shows up.

Note on colour codes (Part 15): the palette in brand.py is the house
contract, so the RGB section names the colours rather than painting true
#FF0000 swatches. The hex value and the colour name carry the teaching
point without introducing an off-palette colour.
"""

from manim import (
    Create,
    FadeIn,
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
from components.bit_table import BitTable
from scenes.base import SATScene

NIBBLE = [8, 4, 2, 1]


class NumberSystemsP2(SATScene):
    scene_id = "cs.number_systems_p2"

    def construct(self):
        self.margin_note = mono("CS · number systems · part 2", MARGIN_SIZE)
        self.margin_note.to_corner(UP + LEFT, buff=GAP_SM)
        self.add(self.margin_note)
        self.section_head = None
        self.work = VGroup()

        self.enter_hex()
        self.nibbles()
        self.binary_to_hex()
        self.challenge_two()
        self.short_groups()
        self.hex_to_binary()
        self.hex_to_denary()
        self.denary_to_hex()
        self.why_hex()

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

    def nibble_group(self, bits, total_tex, symbol, t):
        """One four-bit group converted to a single hex digit."""
        table = BitTable(NIBBLE, bits=bits, cell_width=1.3)
        self.below_head(table, buff=GAP_MD * 1.5)
        self.play(Write(table.headings), Create(table.rule),
                  run_time=t.fill(0.12))
        self.play(Write(table.digits), run_time=t.fill(0.12))
        total = MathTex(total_tex, font_size=EQUATION_SIZE, color=CHARCOAL)
        total.next_to(table, DOWN, buff=GAP_MD * 1.3)
        self.play(Write(total), run_time=t.fill(0.2))
        result = MathTex(f"{bits}_2 = \\mathtt{{{symbol}}}_{{16}}",
                         font_size=DISPLAY_SIZE, color=SAGE)
        result.next_to(total, DOWN, buff=GAP_MD * 1.2)
        self.play(Write(result), run_time=t.fill(0.2))
        self.work.add(table, total, result)
        return result

    # ------------------------------------------------------------ sections

    def enter_hex(self):
        with self.beat("hex_intro") as t:
            self.set_head(t, "Part 8 — Enter hexadecimal")
            a = mono("1101011010111110", BODY_SIZE, CHARCOAL)
            b = mono("1101011011011110", BODY_SIZE, CHARCOAL)
            pair = VGroup(a, b).arrange(DOWN, buff=GAP_MD)
            self.below_head(pair, buff=GAP_MD * 1.8)
            note = serif("long binary is easy for humans to misread",
                         BODY_SIZE, TERRACOTTA)
            note.next_to(pair, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(a), run_time=t.fill(0.2))
            self.play(Write(b), run_time=t.fill(0.2))
            self.play(Write(note), run_time=t.fill(0.2))
            self.work.add(pair, note)
            t.hold()

        with self.beat("hex_symbols") as t:
            self.swap_work(t)
            base = serif("hexadecimal — base 16", BODY_SIZE)
            self.below_head(base, buff=GAP_MD * 1.4)
            need = MathTex("16 \\text{ symbols needed}",
                           font_size=EQUATION_SIZE, color=CHARCOAL)
            need.next_to(base, DOWN, buff=GAP_MD * 1.2)
            have = MathTex("0,1,2,3,4,5,6,7,8,9 \\;\\rightarrow\\; "
                           "\\text{only } 10", font_size=EQUATION_SIZE,
                           color=GREY)
            have.next_to(need, DOWN, buff=GAP_MD * 1.2)
            more = serif("so hexadecimal borrows letters", BODY_SIZE)
            more.next_to(have, DOWN, buff=GAP_MD * 1.2)
            self.play(Write(base), run_time=t.fill(0.15))
            self.play(Write(need), run_time=t.fill(0.15))
            self.play(Write(have), run_time=t.fill(0.18))
            self.play(Write(more), run_time=t.fill(0.15))
            self.work.add(base, need, have, more)
            t.hold()

        with self.beat("memorize") as t:
            self.swap_work(t)
            letters = BitTable(
                ["A", "B", "C", "D", "E", "F"],
                bits=None, cell_width=1.6,
            )
            values = BitTable(
                [10, 11, 12, 13, 14, 15], cell_width=1.6, rule=False,
            )
            letters.move_to(UP * 0.6)
            values.next_to(letters, DOWN, buff=GAP_MD * 0.9)
            self.play(Write(letters.headings), Create(letters.rule),
                      run_time=t.fill(0.25))
            self.play(Write(values.headings), run_time=t.fill(0.25))
            tip = serif("memorize these six", LABEL_SIZE, GREY)
            tip.next_to(values, DOWN, buff=GAP_MD * 1.3)
            self.play(Write(tip), run_time=t.fill(0.15))
            self.work.add(letters, values, tip)
            t.hold()

    def nibbles(self):
        with self.beat("four_bits") as t:
            self.clear_all(t)
            self.set_head(t, "Part 9 — Why hex fits binary")
            key = MathTex("16 = 2^4", font_size=TITLE_SIZE * 1.5,
                          color=CHARCOAL)
            self.below_head(key, buff=GAP_MD * 1.5)
            rule = serif("one hex digit = four binary bits", BODY_SIZE,
                         TERRACOTTA)
            rule.next_to(key, DOWN, buff=GAP_MD * 1.4)
            span = MathTex("0000 \\;\\text{to}\\; 1111 \\;\\rightarrow\\; "
                           "0 \\;\\text{to}\\; 15", font_size=EQUATION_SIZE,
                           color=CHARCOAL)
            span.next_to(rule, DOWN, buff=GAP_MD * 1.3)
            self.play(Write(key), run_time=t.fill(0.22))
            self.play(Write(rule), run_time=t.fill(0.2))
            self.play(Write(span), run_time=t.fill(0.2))
            self.work.add(key, rule, span)
            t.hold()

        with self.beat("full_table") as t:
            self.clear_all(t)
            self.set_head(t, "Binary · denary · hex")
            hexdigits = "0123456789ABCDEF"

            def half(lo, hi):
                rows = VGroup(*[
                    MathTex(
                        f"\\mathtt{{{i:04b}}} \\;\\;\\; {i} \\;\\;\\; "
                        f"\\mathtt{{{hexdigits[i]}}}",
                        font_size=LABEL_SIZE, color=CHARCOAL,
                    )
                    for i in range(lo, hi)
                ]).arrange(DOWN, buff=GAP_SM * 0.9)
                return rows

            left, right = half(0, 8), half(8, 16)
            table = VGroup(left, right).arrange(RIGHT, buff=GAP_MD * 3)
            self.below_head(table, buff=GAP_MD * 1.2)
            self.play(Write(left), run_time=t.fill(0.3))
            self.play(Write(right), run_time=t.fill(0.3))
            self.work.add(table)
            t.hold()

        with self.beat("fallback") as t:
            tip = serif("forgotten one? fall back on 8 · 4 · 2 · 1",
                        BODY_SIZE, TERRACOTTA)
            tip.next_to(self.work[0], DOWN, buff=GAP_MD * 1.2)
            self.play(Write(tip), run_time=t.fill(0.4))
            self.work.add(tip)
            t.hold()

    def binary_to_hex(self):
        with self.beat("group_intro") as t:
            self.clear_all(t)
            self.set_head(t, "Part 10 — Binary to hex")
            full = mono("110101101011", DISPLAY_SIZE, CHARCOAL)
            self.below_head(full, buff=GAP_MD * 1.5)
            grouped = mono("1101   0110   1011", DISPLAY_SIZE, CHARCOAL)
            grouped.move_to(full)
            rule = serif("always group in fours, starting from the right",
                         BODY_SIZE, TERRACOTTA)
            rule.next_to(full, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(full), run_time=t.fill(0.25))
            self.play(Write(rule), run_time=t.fill(0.2))
            self.play(FadeOut(full), FadeIn(grouped), run_time=t.fill(0.2))
            self.work.add(grouped, rule)
            t.hold()

        with self.beat("group1") as t:
            self.clear_all(t)
            self.set_head(t, "Group 1 — 1101")
            self.nibble_group("1101", "8 + 4 + 0 + 1 = 13", "D", t)
            t.hold()

        with self.beat("group2") as t:
            self.clear_all(t)
            self.set_head(t, "Group 2 — 0110")
            self.nibble_group("0110", "0 + 4 + 2 + 0 = 6", "6", t)
            t.hold()

        with self.beat("group3") as t:
            self.clear_all(t)
            self.set_head(t, "Group 3 — 1011")
            self.nibble_group("1011", "8 + 0 + 2 + 1 = 11", "B", t)
            t.hold()

        with self.beat("assemble") as t:
            self.clear_all(t)
            self.set_head(t, "Put them together")
            rows = VGroup(*[
                MathTex(f"\\mathtt{{{b}}} \\;\\rightarrow\\; "
                        f"\\mathtt{{{h}}}", font_size=EQUATION_SIZE,
                        color=CHARCOAL)
                for b, h in (("1101", "D"), ("0110", "6"), ("1011", "B"))
            ]).arrange(DOWN, buff=GAP_SM * 1.3)
            self.below_head(rows, buff=GAP_MD * 1.3)
            answer = MathTex("110101101011_2 = \\mathtt{D6B}_{16}",
                             font_size=DISPLAY_SIZE, color=SAGE)
            answer.next_to(rows, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(rows), run_time=t.fill(0.3))
            self.play(Write(answer), run_time=t.fill(0.25))
            self.play(Create(self.underline(answer)), run_time=t.fill(0.1))
            self.work.add(rows, answer)
            t.hold()

    def challenge_two(self):
        with self.beat("challenge2") as t:
            self.clear_all(t)
            head = serif("Pause & Try", TITLE_SIZE * 1.2, TERRACOTTA)
            head.to_edge(UP, buff=GAP_MD * 1.8)
            task = serif("convert this to hexadecimal", BODY_SIZE)
            task.next_to(head, DOWN, buff=GAP_MD * 1.3)
            bits = mono("1010  1111  0101", TITLE_SIZE * 1.2, CHARCOAL)
            bits.next_to(task, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(head), run_time=t.fill(0.2))
            self.play(Write(task), run_time=t.fill(0.2))
            self.play(Write(bits), run_time=t.fill(0.3))
            t.hold()

        with self.beat("challenge2_answer") as t:
            self.clear_all(t)
            self.set_head(t, "Challenge 2 — check")
            rows = VGroup(*[
                MathTex(line, font_size=EQUATION_SIZE, color=CHARCOAL)
                for line in (
                    "\\mathtt{1010}: \\; 8 + 2 = 10 \\;\\rightarrow\\; "
                    "\\mathtt{A}",
                    "\\mathtt{1111}: \\; 8 + 4 + 2 + 1 = 15 "
                    "\\;\\rightarrow\\; \\mathtt{F}",
                    "\\mathtt{0101}: \\; 4 + 1 = 5 \\;\\rightarrow\\; "
                    "\\mathtt{5}",
                )
            ]).arrange(DOWN, buff=GAP_SM * 1.4, aligned_edge=LEFT)
            self.below_head(rows, buff=GAP_MD * 1.4)
            answer = MathTex("\\mathtt{AF5}", font_size=TITLE_SIZE * 1.4,
                             color=SAGE)
            answer.next_to(rows, DOWN, buff=GAP_MD * 1.5)
            for row in rows:
                self.play(Write(row), run_time=t.fill(0.16))
            self.play(Write(answer), run_time=t.fill(0.2))
            self.work.add(rows, answer)
            t.hold()

    def short_groups(self):
        with self.beat("padding") as t:
            self.clear_all(t)
            self.set_head(t, "Part 11 — Groups shorter than four")
            steps = VGroup(
                mono("1011010110", DISPLAY_SIZE, CHARCOAL),
                mono("10   1101   0110", DISPLAY_SIZE, CHARCOAL),
                mono("0010   1101   0110", DISPLAY_SIZE, CHARCOAL),
            )
            for s in steps:
                self.below_head(s, buff=GAP_MD * 1.6)
            pad_note = serif("the left group is short — pad it with zeros "
                             "on the left", LABEL_SIZE, GREY)
            pad_note.next_to(steps[0], DOWN, buff=GAP_MD * 1.4)
            answer = MathTex("= \\mathtt{2D6}_{16}", font_size=DISPLAY_SIZE,
                             color=SAGE)
            answer.next_to(pad_note, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(steps[0]), run_time=t.fill(0.15))
            self.play(FadeOut(steps[0]), FadeIn(steps[1]),
                      run_time=t.fill(0.12))
            self.play(Write(pad_note), run_time=t.fill(0.15))
            self.play(FadeOut(steps[1]), FadeIn(steps[2]),
                      run_time=t.fill(0.12))
            self.play(Write(answer), run_time=t.fill(0.18))
            self.work.add(steps[2], pad_note, answer)
            t.hold()

        with self.beat("padding_warning") as t:
            self.clear_all(t)
            self.set_head(t, "Why on the left?")
            same = MathTex("\\mathtt{10} = \\mathtt{0010} = 2",
                           font_size=DISPLAY_SIZE, color=CHARCOAL)
            self.below_head(same, buff=GAP_MD * 1.6)
            ok = serif("leading zeros do not change the value", BODY_SIZE)
            ok.next_to(same, DOWN, buff=GAP_MD * 1.3)
            warn = serif("zeros on the right DO change it — "
                         "never add them there", BODY_SIZE, TERRACOTTA)
            warn.next_to(ok, DOWN, buff=GAP_MD * 1.3)
            self.play(Write(same), run_time=t.fill(0.22))
            self.play(Write(ok), run_time=t.fill(0.2))
            self.play(Write(warn), run_time=t.fill(0.25))
            self.work.add(same, ok, warn)
            t.hold()

    def hex_to_binary(self):
        with self.beat("hex_to_binary") as t:
            self.clear_all(t)
            self.set_head(t, "Part 12 — Hex to binary")
            rows = VGroup(*[
                MathTex(line, font_size=EQUATION_SIZE, color=CHARCOAL)
                for line in (
                    "\\mathtt{7}: \\; 4 + 2 + 1 \\;\\rightarrow\\; "
                    "\\mathtt{0111}",
                    "\\mathtt{A} = 10: \\; 8 + 2 \\;\\rightarrow\\; "
                    "\\mathtt{1010}",
                    "\\mathtt{C} = 12: \\; 8 + 4 \\;\\rightarrow\\; "
                    "\\mathtt{1100}",
                )
            ]).arrange(DOWN, buff=GAP_SM * 1.4, aligned_edge=LEFT)
            self.below_head(rows, buff=GAP_MD * 1.3)
            answer = MathTex("\\mathtt{7AC}_{16} = "
                             "\\mathtt{011110101100}_2",
                             font_size=DISPLAY_SIZE, color=SAGE)
            answer.next_to(rows, DOWN, buff=GAP_MD * 1.4)
            for row in rows:
                self.play(Write(row), run_time=t.fill(0.15))
            self.play(Write(answer), run_time=t.fill(0.2))
            self.work.add(rows, answer)
            t.hold()

        with self.beat("hex_binary_note") as t:
            warn = serif("never drop the zeros inside a four-bit group",
                         BODY_SIZE, TERRACOTTA)
            warn.next_to(self.work[1], DOWN, buff=GAP_MD * 1.4)
            self.play(Write(warn), run_time=t.fill(0.4))
            self.work.add(warn)
            t.hold()

    def hex_to_denary(self):
        with self.beat("hex_to_denary") as t:
            self.clear_all(t)
            self.set_head(t, "Part 13 — Hex to denary")
            powers = MathTex("16^2 \\qquad 16^1 \\qquad 16^0",
                             font_size=EQUATION_SIZE, color=GREY)
            self.below_head(powers, buff=GAP_MD * 1.2)
            table = BitTable([256, 16, 1], bits="3B7", cell_width=2.2)
            table.next_to(powers, DOWN, buff=GAP_MD * 0.9)
            self.play(Write(powers), run_time=t.fill(0.22))
            self.play(Write(table.headings), Create(table.rule),
                      run_time=t.fill(0.2))
            self.play(Write(table.digits), run_time=t.fill(0.2))
            self.work.add(powers, table)
            self.hex_table = table
            t.hold()

        with self.beat("hex_denary_calc") as t:
            remind = serif("B = 11", BODY_SIZE, TERRACOTTA)
            remind.next_to(self.hex_table, DOWN, buff=GAP_MD * 1.1)
            terms = VGroup(*[
                MathTex(line, font_size=EQUATION_SIZE, color=CHARCOAL)
                for line in ("3 \\times 256 = 768", "11 \\times 16 = 176",
                             "7 \\times 1 = 7")
            ]).arrange(DOWN, buff=GAP_SM * 1.2)
            terms.next_to(remind, DOWN, buff=GAP_MD * 1.1)
            answer = MathTex("768 + 176 + 7 = 951", font_size=DISPLAY_SIZE,
                             color=SAGE)
            answer.next_to(terms, DOWN, buff=GAP_MD * 1.2)
            self.play(Write(remind), run_time=t.fill(0.12))
            for term in terms:
                self.play(Write(term), run_time=t.fill(0.12))
            self.play(Write(answer), run_time=t.fill(0.2))
            self.work.add(remind, terms, answer)
            t.hold()

    def denary_to_hex(self):
        with self.beat("denary_to_hex") as t:
            self.clear_all(t)
            self.set_head(t, "Part 14 — Denary to hex")
            lines = VGroup(*[
                MathTex(line, font_size=EQUATION_SIZE, color=CHARCOAL)
                for line in (
                    "684 \\div 16 = 42 \\;\\; \\text{r } 12",
                    "42 \\div 16 = 2 \\;\\; \\text{r } 10",
                    "2 \\div 16 = 0 \\;\\; \\text{r } 2",
                )
            ]).arrange(DOWN, buff=GAP_SM * 1.3, aligned_edge=LEFT)
            self.below_head(lines, buff=GAP_MD * 1.4)
            for line in lines:
                self.play(Write(line), run_time=t.fill(0.2))
            self.work.add(lines)
            self.div_lines = lines
            t.hold()

        with self.beat("denary_hex_read") as t:
            translate = VGroup(*[
                MathTex(line, font_size=EQUATION_SIZE, color=CHARCOAL)
                for line in ("12 = \\mathtt{C}", "10 = \\mathtt{A}",
                             "2 = \\mathtt{2}")
            ]).arrange(DOWN, buff=GAP_SM * 1.2)
            translate.next_to(self.div_lines, RIGHT, buff=GAP_MD * 2.4)
            arrow = Line(
                self.div_lines.get_left() + LEFT * 0.5 + DOWN * 0.8,
                self.div_lines.get_left() + LEFT * 0.5 + UP * 0.8,
                color=TERRACOTTA, stroke_width=4,
            )
            label = serif("bottom to top", LABEL_SIZE, TERRACOTTA)
            label.next_to(arrow, LEFT, buff=GAP_SM)
            answer = MathTex("684 = \\mathtt{2AC}_{16}",
                             font_size=DISPLAY_SIZE, color=SAGE)
            answer.next_to(self.div_lines, DOWN, buff=GAP_MD * 1.5)
            check = MathTex("512 + 160 + 12 = 684", font_size=EQUATION_SIZE,
                            color=GREY)
            check.next_to(answer, DOWN, buff=GAP_MD * 1.1)
            self.play(Write(translate), run_time=t.fill(0.2))
            self.play(Create(arrow), Write(label), run_time=t.fill(0.12))
            self.play(Write(answer), run_time=t.fill(0.18))
            self.play(Write(check), run_time=t.fill(0.18))
            self.work.add(translate, arrow, label, answer, check)
            t.hold()

    def why_hex(self):
        with self.beat("why_hex") as t:
            self.clear_all(t)
            self.set_head(t, "Part 15 — Why we use hex")
            uses = VGroup(
                serif("MAC addresses", BODY_SIZE),
                serif("IPv6 addresses", BODY_SIZE),
                serif("colour codes", BODY_SIZE),
                serif("error and diagnostic codes", BODY_SIZE),
            ).arrange(DOWN, buff=GAP_SM * 1.3, aligned_edge=LEFT)
            self.below_head(uses, buff=GAP_MD * 1.4)
            why = serif("a compact representation of binary data",
                        BODY_SIZE, GREY)
            why.next_to(uses, DOWN, buff=GAP_MD * 1.3)
            for use in uses:
                self.play(Write(use), run_time=t.fill(0.12))
            self.play(Write(why), run_time=t.fill(0.18))
            self.work.add(uses, why)
            t.hold()

        with self.beat("colours") as t:
            self.clear_all(t)
            self.set_head(t, "Colour codes")
            code = mono("#FF0000", TITLE_SIZE * 1.3, CHARCOAL)
            self.below_head(code, buff=GAP_MD * 1.4)
            split = VGroup(
                mono("FF", TITLE_SIZE, CHARCOAL),
                mono("00", TITLE_SIZE, CHARCOAL),
                mono("00", TITLE_SIZE, CHARCOAL),
            ).arrange(RIGHT, buff=GAP_MD * 2.2)
            split.next_to(code, DOWN, buff=GAP_MD * 1.4)
            labels = VGroup(
                serif("Red", BODY_SIZE, GREY),
                serif("Green", BODY_SIZE, GREY),
                serif("Blue", BODY_SIZE, GREY),
            )
            for label, part in zip(labels, split):
                label.next_to(part, DOWN, buff=GAP_SM * 1.2)
            self.play(Write(code), run_time=t.fill(0.22))
            self.play(Write(split), run_time=t.fill(0.2))
            self.play(Write(labels), run_time=t.fill(0.2))
            self.work.add(code, split, labels)
            self.colour_split = VGroup(split, labels)
            t.hold()

        with self.beat("ff_value") as t:
            calc = MathTex("\\mathtt{FF} = 15 \\times 16 + 15 = 255",
                           font_size=DISPLAY_SIZE, color=CHARCOAL)
            calc.next_to(self.colour_split, DOWN, buff=GAP_MD * 1.5)
            span = serif("each component runs 0 to 255", BODY_SIZE, SAGE)
            span.next_to(calc, DOWN, buff=GAP_MD * 1.2)
            self.play(Write(calc), run_time=t.fill(0.3))
            self.play(Write(span), run_time=t.fill(0.25))
            self.work.add(calc, span)
            t.hold()

        with self.beat("colour_examples") as t:
            self.clear_all(t)
            self.set_head(t, "Reading a colour code")
            rows = VGroup(*[
                VGroup(
                    mono(code, BODY_SIZE, CHARCOAL),
                    serif(name, BODY_SIZE, GREY),
                ).arrange(RIGHT, buff=GAP_MD * 1.6)
                for code, name in (
                    ("#FF0000", "bright red"),
                    ("#00FF00", "green"),
                    ("#0000FF", "blue"),
                    ("#FFFFFF", "white — all three at maximum"),
                )
            ]).arrange(DOWN, buff=GAP_SM * 1.4, aligned_edge=LEFT)
            self.below_head(rows, buff=GAP_MD * 1.4)
            for row in rows:
                self.play(Write(row), run_time=t.fill(0.15))
            self.work.add(rows)
            t.hold()

        with self.beat("mac") as t:
            self.clear_all(t)
            self.set_head(t, "Part 16 — MAC and IP addresses")
            mac_addr = mono("3C:52:82:7A:91:F0", TITLE_SIZE * 1.1, CHARCOAL)
            self.below_head(mac_addr, buff=GAP_MD * 1.6)
            note = serif("six groups of two hex digits — 48 bits",
                         BODY_SIZE, GREY)
            note.next_to(mac_addr, DOWN, buff=GAP_MD * 1.3)
            ipv6 = serif("IPv6 addresses use hex too", BODY_SIZE)
            ipv6.next_to(note, DOWN, buff=GAP_MD * 1.3)
            self.play(Write(mac_addr), run_time=t.fill(0.3))
            self.play(Write(note), run_time=t.fill(0.2))
            self.play(Write(ipv6), run_time=t.fill(0.18))
            self.work.add(mac_addr, note, ipv6)
            t.hold()

        with self.beat("why_summary") as t:
            self.clear_all(t)
            answer = VGroup(
                serif("Hexadecimal gives a shorter,", BODY_SIZE * 1.1),
                serif("more manageable representation", BODY_SIZE * 1.1),
                serif("of binary values.", BODY_SIZE * 1.1),
            ).arrange(DOWN, buff=GAP_SM * 1.2)
            answer.move_to(ORIGIN)
            tag = mono("say exactly this in the exam", MARGIN_SIZE * 1.15,
                       TERRACOTTA)
            tag.next_to(answer, DOWN, buff=GAP_MD * 1.6)
            self.play(Write(answer), run_time=t.fill(0.4))
            self.play(Create(self.underline(answer)), run_time=t.fill(0.12))
            self.play(Write(tag), run_time=t.fill(0.2))
            t.hold()
