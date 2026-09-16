"""CS lecture: number systems and data representation, part 4 (CS01).

Narration script: scripts/CS01-number-systems-p4.md
Two's complement: the negative leftmost column, the sign clue, and the
8-bit range. The worked conversions (Parts 28-34) are not in this
recording and will follow in their own video.
"""

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
from components.bit_table import BitTable
from scenes.base import SATScene

UNSIGNED = [128, 64, 32, 16, 8, 4, 2, 1]
SIGNED = ["-128", 64, 32, 16, 8, 4, 2, 1]


class NumberSystemsP4(SATScene):
    scene_id = "cs.number_systems_p4"

    def construct(self):
        self.margin_note = mono("CS · number systems · part 4", MARGIN_SIZE)
        self.margin_note.to_corner(UP + LEFT, buff=GAP_SM)
        self.add(self.margin_note)
        self.section_head = None
        self.work = VGroup()

        self.where_negatives()
        self.sign_clue()
        self.the_range()

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

    def where_negatives(self):
        with self.beat("where_negatives") as t:
            self.set_head(t, "Part 25 — Where are the negatives?")
            so_far = MathTex("\\text{unsigned 8 bits} \\;\\rightarrow\\; "
                             "0 \\text{ to } 255", font_size=EQUATION_SIZE,
                             color=GREY)
            self.below_head(so_far, buff=GAP_MD * 1.4)
            needed = VGroup(*[
                MathTex(v, font_size=DISPLAY_SIZE, color=CHARCOAL)
                for v in ("-1", "-25", "-100")
            ]).arrange(RIGHT, buff=GAP_MD * 2.0)
            needed.next_to(so_far, DOWN, buff=GAP_MD * 1.5)
            ask = serif("how do we store a minus sign in bits?",
                        BODY_SIZE, TERRACOTTA)
            ask.next_to(needed, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(so_far), run_time=t.fill(0.2))
            self.play(Write(needed), run_time=t.fill(0.25))
            self.play(Write(ask), run_time=t.fill(0.22))
            self.work.add(so_far, needed, ask)
            t.hold()

        with self.beat("name") as t:
            self.clear_all(t)
            name = serif("Two's complement", TITLE_SIZE * 1.4)
            name.move_to(UP * 0.6)
            calm = serif("one change to understand — that's all",
                         BODY_SIZE, GREY)
            calm.next_to(name, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(name), run_time=t.fill(0.35))
            self.play(Create(self.underline(name)), run_time=t.fill(0.12))
            self.play(Write(calm), run_time=t.fill(0.25))
            t.hold()

        with self.beat("negative_column") as t:
            self.clear_all(t)
            self.set_head(t, "The one change")
            unsigned = BitTable(UNSIGNED, rule=False)
            unsigned_label = serif("unsigned", LABEL_SIZE, GREY)
            signed = BitTable(SIGNED, rule=False)
            signed_label = serif("two's complement", LABEL_SIZE, GREY)
            unsigned_label.next_to(unsigned, LEFT, buff=GAP_MD)
            signed_label.next_to(signed, LEFT, buff=GAP_MD)
            top = VGroup(unsigned_label, unsigned)
            bottom = VGroup(signed_label, signed)
            stack = VGroup(top, bottom).arrange(DOWN, buff=GAP_MD * 2.0)
            self.below_head(stack, buff=GAP_MD * 1.6)
            self.play(Write(unsigned.headings), Write(unsigned_label),
                      run_time=t.fill(0.22))
            self.play(Write(signed.headings), Write(signed_label),
                      run_time=t.fill(0.22))
            self.play(signed.heading(0).animate.set_color(TERRACOTTA),
                      run_time=t.fill(0.12))
            note = serif("only the leftmost column changes sign",
                         BODY_SIZE, TERRACOTTA)
            note.next_to(stack, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(note), run_time=t.fill(0.2))
            self.work.add(stack, note)
            t.hold()

    def sign_clue(self):
        with self.beat("sign_clue") as t:
            self.clear_all(t)
            self.set_head(t, "Part 26 — The sign clue")
            rules = VGroup(
                serif("MSB = 0  →  non-negative", BODY_SIZE),
                serif("MSB = 1  →  negative", BODY_SIZE),
            ).arrange(DOWN, buff=GAP_MD * 1.2)
            self.below_head(rules, buff=GAP_MD * 1.8)
            self.play(Write(rules[0]), run_time=t.fill(0.25))
            self.play(Write(rules[1]), run_time=t.fill(0.25))
            self.work.add(rules)
            t.hold()

        with self.beat("sign_examples") as t:
            self.clear_all(t)
            self.set_head(t, "Read the first bit")
            rows = VGroup()
            for bits, verdict, colour in (
                ("00110110", "non-negative", SAGE),
                ("10110110", "negative", TERRACOTTA),
            ):
                digits = mono(bits, DISPLAY_SIZE, CHARCOAL)
                label = serif(verdict, BODY_SIZE, colour)
                label.next_to(digits, RIGHT, buff=GAP_MD * 1.6)
                rows.add(VGroup(digits, label))
            rows.arrange(DOWN, buff=GAP_MD * 1.6, aligned_edge=LEFT)
            self.below_head(rows, buff=GAP_MD * 1.8)
            for row in rows:
                self.play(Write(row), run_time=t.fill(0.25))
            self.work.add(rows)
            t.hold()

        with self.beat("sign_warning") as t:
            self.clear_all(t)
            self.set_head(t, "Careful")
            wrong = serif("the first bit is not a minus-sign character",
                          BODY_SIZE, GREY)
            self.below_head(wrong, buff=GAP_MD * 1.6)
            right = VGroup(
                serif("it is a column with weight", BODY_SIZE),
                MathTex("-128", font_size=TITLE_SIZE * 1.3,
                        color=TERRACOTTA),
            ).arrange(DOWN, buff=GAP_MD)
            right.next_to(wrong, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(wrong), run_time=t.fill(0.3))
            self.play(Write(right), run_time=t.fill(0.3))
            self.work.add(wrong, right)
            t.hold()

    def the_range(self):
        with self.beat("largest") as t:
            self.clear_all(t)
            self.set_head(t, "Part 27 — The range")
            table = BitTable(SIGNED, bits="01111111")
            self.below_head(table, buff=GAP_MD * 1.4)
            table.heading(0).set_color(GREY)
            sums = MathTex("64 + 32 + 16 + 8 + 4 + 2 + 1 = +127",
                           font_size=EQUATION_SIZE, color=CHARCOAL)
            sums.next_to(table, DOWN, buff=GAP_MD * 1.4)
            note = serif("the largest positive — MSB must stay 0",
                         LABEL_SIZE, GREY)
            note.next_to(sums, DOWN, buff=GAP_MD * 1.1)
            self.play(Write(table.headings), Create(table.rule),
                      run_time=t.fill(0.18))
            self.play(Write(table.digits), run_time=t.fill(0.18))
            self.play(Write(sums), run_time=t.fill(0.22))
            self.play(Write(note), run_time=t.fill(0.15))
            self.work.add(table, sums, note)
            t.hold()

        with self.beat("most_negative") as t:
            self.clear_all(t)
            self.set_head(t, "The most negative")
            table = BitTable(SIGNED, bits="10000000")
            self.below_head(table, buff=GAP_MD * 1.4)
            table.heading(0).set_color(TERRACOTTA)
            value = MathTex("= -128", font_size=DISPLAY_SIZE, color=CHARCOAL)
            value.next_to(table, DOWN, buff=GAP_MD * 1.5)
            note = serif("only the −128 column is switched on",
                         LABEL_SIZE, GREY)
            note.next_to(value, DOWN, buff=GAP_MD * 1.1)
            self.play(Write(table.headings), Create(table.rule),
                      run_time=t.fill(0.18))
            self.play(Write(table.digits), run_time=t.fill(0.18))
            self.play(Write(value), run_time=t.fill(0.22))
            self.play(Write(note), run_time=t.fill(0.15))
            self.work.add(table, value, note)
            t.hold()

        with self.beat("range") as t:
            self.clear_all(t)
            self.set_head(t, "Same bits, different meaning")
            rows = VGroup(
                MathTex("\\text{unsigned:} \\quad 0 \\text{ to } 255",
                        font_size=DISPLAY_SIZE, color=GREY),
                MathTex("\\text{two's complement:} \\quad -128 "
                        "\\text{ to } +127", font_size=DISPLAY_SIZE,
                        color=CHARCOAL),
            ).arrange(DOWN, buff=GAP_MD * 1.4)
            self.below_head(rows, buff=GAP_MD * 1.8)
            self.play(Write(rows[0]), run_time=t.fill(0.25))
            self.play(Write(rows[1]), run_time=t.fill(0.3))
            self.work.add(rows)
            self.range_rows = rows
            t.hold()

        with self.beat("same_bits") as t:
            closing = serif("Same eight bits. Different interpretation.",
                            BODY_SIZE * 1.15)
            closing.next_to(self.range_rows, DOWN, buff=GAP_MD * 2.0)
            self.play(Write(closing), run_time=t.fill(0.4))
            self.play(Create(self.underline(closing, TERRACOTTA)),
                      run_time=t.fill(0.2))
            self.work.add(closing)
            t.hold()
