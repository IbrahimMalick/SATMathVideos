"""CS lecture: number systems and data representation, part 1 (CS01).

Narration script: scripts/CS01-number-systems-p1.md
Why binary, denary place value, binary place value, binary <-> denary
conversion, the division-by-2 method, and the unsigned 8-bit range.
"""

from manim import (
    Create,
    FadeIn,
    FadeOut,
    Line,
    MathTex,
    Rectangle,
    Transform,
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
    CREAM,
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

COLUMNS = [128, 64, 32, 16, 8, 4, 2, 1]


class NumberSystemsP1(SATScene):
    scene_id = "cs.number_systems_p1"

    def construct(self):
        self.margin_note = mono("CS · number systems · part 1", MARGIN_SIZE)
        self.margin_note.to_corner(UP + LEFT, buff=GAP_SM)
        self.add(self.margin_note)
        self.section_head = None
        self.work = VGroup()

        self.opening()
        self.why_binary()
        self.denary_place_value()
        self.binary_columns()
        self.binary_to_denary()
        self.challenge_one()
        self.denary_to_binary()
        self.division_method()
        self.unsigned_range()

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

    def set_head(self, t, text, fraction=0.12):
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
        anchor = self.section_head if self.section_head is not None else None
        if anchor is None:
            mobject.move_to(ORIGIN)
        else:
            mobject.next_to(anchor, DOWN, buff=buff)
        return mobject

    # ------------------------------------------------------------ sections

    def opening(self):
        title = serif("Number Systems", TITLE_SIZE * 1.3)
        title2 = serif("& Data Representation", TITLE_SIZE * 1.3)
        stack = VGroup(title, title2).arrange(DOWN, buff=GAP_SM)
        stack.to_edge(UP, buff=GAP_MD * 1.8)
        sub = serif("binary · denary · hexadecimal", BODY_SIZE, GREY)
        sub.next_to(stack, DOWN, buff=GAP_MD * 1.2)

        with self.beat("open") as t:
            self.play(Write(stack), run_time=t.fill(0.248))
            self.play(Write(sub), run_time=t.fill(0.155))
            t.hold()

        things = VGroup(
            serif("a photograph", BODY_SIZE),
            serif("a song", BODY_SIZE),
            serif("a video", BODY_SIZE),
            serif("your name", BODY_SIZE),
        ).arrange(DOWN, buff=GAP_SM * 1.3, aligned_edge=LEFT)
        arrow = serif("→", TITLE_SIZE, GREY)
        stream = VGroup(
            mono("01001010", BODY_SIZE, SLATE),
            mono("11010011", BODY_SIZE, SLATE),
            mono("00101101", BODY_SIZE, SLATE),
        ).arrange(DOWN, buff=GAP_SM * 1.3)
        # Lay the whole row out first, then write the pieces into place —
        # positioning mid-beat pushed this group off the left edge.
        row = VGroup(things, arrow, stream).arrange(RIGHT, buff=GAP_MD * 1.6)
        row.move_to(UP * 1.4)

        with self.beat("common") as t:
            self.play(FadeOut(stack), FadeOut(sub), run_time=t.fill(0.037))
            for item in things:
                self.play(Write(item), run_time=t.fill(0.062))
            self.play(Write(arrow), run_time=t.fill(0.05))
            self.play(Write(stream), run_time=t.fill(0.186))
            t.hold()

        quotes = VGroup(
            serif('not "what a beautiful sunset"', BODY_SIZE, GREY),
            serif('not "I like that guitar"', BODY_SIZE, GREY),
        ).arrange(DOWN, buff=GAP_SM * 1.3)
        quotes.next_to(row, DOWN, buff=GAP_MD * 1.6)
        real = serif("patterns of binary digits", BODY_SIZE, TERRACOTTA)
        real.next_to(quotes, DOWN, buff=GAP_MD * 1.1)

        with self.beat("not_human") as t:
            self.play(Write(quotes), run_time=t.fill(0.248))
            self.play(Write(real), run_time=t.fill(0.186))
            t.hold()

        with self.beat("objectives") as t:
            self.clear_all(t)
            self.set_head(t, "By the end of this lesson")
            topics = VGroup(
                serif("binary and denary", BODY_SIZE),
                serif("hexadecimal", BODY_SIZE),
                serif("number conversion", BODY_SIZE),
                serif("binary addition", BODY_SIZE),
                serif("overflow", BODY_SIZE),
                serif("logical shifts", BODY_SIZE),
                serif("two's complement", BODY_SIZE),
            ).arrange(DOWN, buff=GAP_SM * 1.2, aligned_edge=LEFT)
            self.below_head(topics)
            for topic in topics:
                self.play(Write(topic), run_time=t.fill(0.05))
            pause_note = serif("when I set a challenge — pause and solve it",
                               LABEL_SIZE, GREY)
            pause_note.next_to(topics, DOWN, buff=GAP_MD * 1.1)
            self.play(Write(pause_note), run_time=t.fill(0.124))
            self.work.add(topics, pause_note)
            t.hold()

        with self.beat("workbook") as t:
            self.clear_all(t)
            card = VGroup(
                serif("FREE WORKBOOK", TITLE_SIZE),
                serif("practice along with this lesson", BODY_SIZE, GREY),
                mono("thedigitaltutor.net", BODY_SIZE, TERRACOTTA),
            ).arrange(DOWN, buff=GAP_MD)
            card.move_to(ORIGIN)
            box = Rectangle(
                width=card.width + GAP_MD * 3,
                height=card.height + GAP_MD * 3,
                color=SLATE, stroke_width=3, fill_color=CREAM, fill_opacity=0,
            )
            box.move_to(card)
            self.play(Create(box), run_time=t.fill(0.155))
            self.play(Write(card), run_time=t.fill(0.248))
            t.hold()

    def why_binary(self):
        with self.beat("switch") as t:
            self.clear_all(t)
            self.set_head(t, "Part 1 — Why binary?")
            body = Rectangle(width=1.6, height=2.6, color=SLATE,
                             stroke_width=4)
            body.move_to(LEFT * 3.4 + DOWN * 0.6)
            lever = Line(body.get_top() + DOWN * 0.45 + LEFT * 0.4,
                         body.get_top() + DOWN * 0.45 + RIGHT * 0.4,
                         color=SLATE, stroke_width=8)
            on = serif("ON", BODY_SIZE)
            on.next_to(body, UP, buff=GAP_SM)
            off = serif("OFF", BODY_SIZE)
            off.next_to(body, DOWN, buff=GAP_SM)
            self.play(Create(body), run_time=t.fill(0.124))
            self.play(Create(lever), run_time=t.fill(0.062))
            self.play(Write(on), Write(off), run_time=t.fill(0.093))
            mapping = VGroup(
                MathTex("\\text{ON} = 1", font_size=DISPLAY_SIZE,
                        color=CHARCOAL),
                MathTex("\\text{OFF} = 0", font_size=DISPLAY_SIZE,
                        color=CHARCOAL),
            ).arrange(DOWN, buff=GAP_MD)
            mapping.move_to(RIGHT * 2.4 + DOWN * 0.6)
            self.play(Write(mapping), run_time=t.fill(0.186))
            self.work.add(body, lever, on, off, mapping)
            t.hold()

        with self.beat("hardware") as t:
            self.swap_work(t)
            note = serif("hardware switches reliably between two states",
                         BODY_SIZE)
            self.below_head(note)
            digits = MathTex("0 \\qquad 1", font_size=TITLE_SIZE * 1.6,
                             color=CHARCOAL)
            digits.next_to(note, DOWN, buff=GAP_MD * 1.4)
            name = serif("the binary number system", BODY_SIZE, GREY)
            name.next_to(digits, DOWN, buff=GAP_MD * 1.2)
            self.play(Write(note), run_time=t.fill(0.186))
            self.play(Write(digits), run_time=t.fill(0.155))
            self.play(Write(name), run_time=t.fill(0.124))
            self.work.add(note, digits, name)
            t.hold()

        with self.beat("bit") as t:
            self.swap_work(t)
            defn = serif("bit — short for binary digit", BODY_SIZE)
            self.below_head(defn)
            rows = VGroup(
                MathTex("1 \\quad\\rightarrow\\quad \\text{1 bit}",
                        font_size=EQUATION_SIZE, color=CHARCOAL),
                MathTex("1011 \\quad\\rightarrow\\quad \\text{4 bits}",
                        font_size=EQUATION_SIZE, color=CHARCOAL),
                MathTex("11001010 \\quad\\rightarrow\\quad \\text{8 bits}",
                        font_size=EQUATION_SIZE, color=CHARCOAL),
            ).arrange(DOWN, buff=GAP_MD, aligned_edge=LEFT)
            rows.next_to(defn, DOWN, buff=GAP_MD * 1.3)
            self.play(Write(defn), run_time=t.fill(0.124))
            for row in rows:
                self.play(Write(row), run_time=t.fill(0.124))
            self.work.add(defn, rows)
            t.hold()

        byte = serif("8 bits = 1 byte", BODY_SIZE * 1.1, SAGE)

        with self.beat("byte") as t:
            byte.next_to(self.work[1], DOWN, buff=GAP_MD * 1.3)
            self.play(Write(byte), run_time=t.fill(0.217))
            self.work.add(byte)
            t.hold()

        with self.beat("base2") as t:
            self.swap_work(t)
            wrong = serif('not simply "a bunch of zeros and ones"',
                          BODY_SIZE, GREY)
            self.below_head(wrong, buff=GAP_MD * 1.6)
            right = serif("a base-2 positional number system", BODY_SIZE)
            right.next_to(wrong, DOWN, buff=GAP_MD * 1.3)
            rule = self.underline(right)
            self.play(Write(wrong), run_time=t.fill(0.186))
            self.play(Write(right), run_time=t.fill(0.186))
            self.play(Create(rule), run_time=t.fill(0.074))
            self.work.add(wrong, right, rule)
            t.hold()

    def denary_place_value(self):
        with self.beat("denary") as t:
            self.clear_all(t)
            self.set_head(t, "Part 2 — The system you already know")
            number = MathTex("5{,}274", font_size=TITLE_SIZE * 1.8,
                             color=CHARCOAL)
            self.below_head(number, buff=GAP_MD * 1.8)
            why = serif("the position of each digit gives it a value",
                        BODY_SIZE, GREY)
            why.next_to(number, DOWN, buff=GAP_MD * 1.3)
            self.play(Write(number), run_time=t.fill(0.217))
            self.play(Write(why), run_time=t.fill(0.186))
            self.work.add(number, why)
            t.hold()

        with self.beat("place_value") as t:
            self.swap_work(t)
            table = BitTable(
                ["Thousands", "Hundreds", "Tens", "Units"],
                subheadings=[1000, 100, 10, 1],
                bits="5274",
                cell_width=2.6,
            )
            self.below_head(table, buff=GAP_MD * 1.5)
            self.play(Write(table.headings), run_time=t.fill(0.186))
            self.play(Write(table.subheadings), run_time=t.fill(0.155))
            self.play(Create(table.rule), run_time=t.fill(0.05))
            self.play(Write(table.digits), run_time=t.fill(0.155))
            self.work.add(table)
            self.place_table = table
            t.hold()

        with self.beat("expand") as t:
            terms = MathTex(
                "5{\\times}1000", "+", "2{\\times}100", "+",
                "7{\\times}10", "+", "4{\\times}1",
                font_size=EQUATION_SIZE, color=CHARCOAL,
            )
            sums = MathTex(
                "5000", "+", "200", "+", "70", "+", "4",
                font_size=EQUATION_SIZE, color=CHARCOAL,
            )
            total = MathTex("5{,}274", font_size=DISPLAY_SIZE, color=SAGE)
            for m in (terms, sums, total):
                m.next_to(self.place_table, DOWN, buff=GAP_MD * 1.6)
            self.play(Write(terms), run_time=t.fill(0.186))
            self.play(TransformMatchingTex(terms, sums), run_time=t.fill(0.155))
            self.play(TransformMatchingTex(sums, total), run_time=t.fill(0.124))
            self.work.add(total)
            t.hold()

        with self.beat("powers10") as t:
            self.swap_work(t)
            powers = VGroup(
                MathTex("10^3 = 1000", font_size=EQUATION_SIZE,
                        color=CHARCOAL),
                MathTex("10^2 = 100", font_size=EQUATION_SIZE,
                        color=CHARCOAL),
                MathTex("10^1 = 10", font_size=EQUATION_SIZE, color=CHARCOAL),
                MathTex("10^0 = 1", font_size=EQUATION_SIZE, color=CHARCOAL),
            ).arrange(DOWN, buff=GAP_SM * 1.3, aligned_edge=LEFT)
            self.below_head(powers, buff=GAP_MD * 1.3)
            name = serif("base 10 — denary (or decimal)", BODY_SIZE)
            name.next_to(powers, DOWN, buff=GAP_MD * 1.2)
            digits = serif("ten available digits: 0 through 9",
                           LABEL_SIZE, GREY)
            digits.next_to(name, DOWN, buff=GAP_MD)
            for p in powers:
                self.play(Write(p), run_time=t.fill(0.062))
            self.play(Write(name), run_time=t.fill(0.124))
            self.play(Write(digits), run_time=t.fill(0.093))
            self.work.add(powers, name, digits)
            t.hold()

    def binary_columns(self):
        with self.beat("powers2") as t:
            self.clear_all(t)
            self.set_head(t, "Part 3 — The same idea, base 2")
            powers = VGroup(*[
                MathTex(f"2^{i} = {2 ** i}", font_size=EQUATION_SIZE,
                        color=CHARCOAL)
                for i in range(8)
            ]).arrange_in_grid(rows=2, cols=4, buff=(GAP_MD * 1.6, GAP_MD))
            self.below_head(powers, buff=GAP_MD * 1.5)
            for p in powers:
                self.play(Write(p), run_time=t.fill(0.056))
            self.work.add(powers)
            t.hold()

        with self.beat("columns") as t:
            self.swap_work(t)
            table = BitTable(COLUMNS, rule=False)
            self.below_head(table, buff=GAP_MD * 2.0)
            note = serif("the columns of an 8-bit unsigned number",
                         LABEL_SIZE, GREY)
            note.next_to(table, UP, buff=GAP_MD * 1.2)
            self.play(Write(note), run_time=t.fill(0.093))
            for heading in table.headings:
                self.play(Write(heading), run_time=t.fill(0.05))
            self.work.add(table, note)
            t.hold()

        with self.beat("doubling") as t:
            seq = MathTex("1, \\; 2, \\; 4, \\; 8, \\; 16, \\; 32, \\; "
                          "64, \\; 128", font_size=EQUATION_SIZE,
                          color=CHARCOAL)
            seq.next_to(self.work[0], DOWN, buff=GAP_MD * 1.8)
            rule = serif("every column is double the one on its right",
                         BODY_SIZE, TERRACOTTA)
            rule.next_to(seq, DOWN, buff=GAP_MD * 1.2)
            self.play(Write(rule), run_time=t.fill(0.186))
            self.play(Write(seq), run_time=t.fill(0.186))
            self.work.add(seq, rule)
            t.hold()

    def binary_to_denary(self):
        bits = "10110101"

        with self.beat("convert_intro") as t:
            self.clear_all(t)
            self.set_head(t, "Part 4 — Binary to denary")
            table = BitTable(COLUMNS, bits=bits)
            self.below_head(table, buff=GAP_MD * 1.6)
            self.play(Write(table.headings), run_time=t.fill(0.124))
            self.play(Create(table.rule), run_time=t.fill(0.037))
            self.play(Write(table.digits), run_time=t.fill(0.186))
            self.table = table
            self.work.add(table)
            t.hold()

        with self.beat("rule") as t:
            rules = VGroup(
                serif("1 → use the column value", BODY_SIZE),
                serif("0 → ignore it", BODY_SIZE, GREY),
            ).arrange(DOWN, buff=GAP_SM * 1.4, aligned_edge=LEFT)
            rules.next_to(self.table, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(rules), run_time=t.fill(0.279))
            self.work.add(rules)
            self.rules = rules
            t.hold()

        with self.beat("walk") as t:
            self.play(FadeOut(self.rules), run_time=t.fill(0.031))
            self.work.remove(self.rules)
            box = self.table.column_box(0)
            self.play(Create(box), run_time=t.fill(0.037))
            collected = VGroup()
            for i, bit in enumerate(bits):
                if i > 0:
                    self.play(Transform(box, self.table.column_box(i)),
                              run_time=t.fill(0.031))
                if bit == "1":
                    value = MathTex(str(COLUMNS[i]), font_size=EQUATION_SIZE,
                                    color=SAGE)
                    value.move_to(self.table.digit(i))
                    value.shift(DOWN * 1.5)
                    collected.add(value)
                    self.play(Write(value), run_time=t.fill(0.031))
            self.play(FadeOut(box), run_time=t.fill(0.025))
            self.work.add(collected)
            self.collected = collected
            t.hold()

        with self.beat("sum") as t:
            chain = VGroup(
                MathTex("128 + 32 + 16 + 4 + 1", font_size=EQUATION_SIZE,
                        color=CHARCOAL),
                MathTex("160 + 16 + 4 + 1", font_size=EQUATION_SIZE,
                        color=CHARCOAL),
                MathTex("176 + 4 + 1", font_size=EQUATION_SIZE,
                        color=CHARCOAL),
                MathTex("180 + 1", font_size=EQUATION_SIZE, color=CHARCOAL),
            )
            for m in chain:
                m.next_to(self.collected, DOWN, buff=GAP_MD * 1.4)
            self.play(FadeOut(self.collected), Write(chain[0]),
                      run_time=t.fill(0.124))
            self.work.remove(self.collected)
            for a, b in zip(chain, chain[1:]):
                self.play(TransformMatchingTex(a, b), run_time=t.fill(0.124))
            self.sum_line = chain[-1]
            self.work.add(self.sum_line)
            t.hold()

        with self.beat("total") as t:
            answer = MathTex("181", font_size=DISPLAY_SIZE, color=SAGE)
            answer.move_to(self.sum_line)
            self.play(TransformMatchingTex(self.sum_line, answer),
                      run_time=t.fill(0.186))
            self.work.remove(self.sum_line)
            self.work.add(answer)
            ask = serif("which powers of two are switched on?",
                        LABEL_SIZE, GREY)
            ask.next_to(answer, DOWN, buff=GAP_MD * 1.1)
            self.play(Write(ask), run_time=t.fill(0.186))
            self.work.add(ask)
            t.hold()

    def challenge_one(self):
        with self.beat("challenge1") as t:
            self.clear_all(t)
            head = serif("Pause & Try", TITLE_SIZE * 1.2, TERRACOTTA)
            head.to_edge(UP, buff=GAP_MD * 1.8)
            task = serif("convert this to denary", BODY_SIZE)
            task.next_to(head, DOWN, buff=GAP_MD * 1.3)
            bits = mono("01101010", TITLE_SIZE * 1.4, CHARCOAL)
            bits.next_to(task, DOWN, buff=GAP_MD * 1.4)
            hint = VGroup(
                serif("write the column values above the bits,",
                      LABEL_SIZE, GREY),
                serif("then add the active ones", LABEL_SIZE, GREY),
            ).arrange(DOWN, buff=GAP_SM)
            hint.next_to(bits, DOWN, buff=GAP_MD * 1.3)
            self.play(Write(head), run_time=t.fill(0.124))
            self.play(Write(task), run_time=t.fill(0.093))
            self.play(Write(bits), run_time=t.fill(0.155))
            self.play(Write(hint), run_time=t.fill(0.155))
            t.hold()

        with self.beat("challenge1_answer") as t:
            self.clear_all(t)
            self.set_head(t, "Challenge 1 — check")
            table = BitTable(COLUMNS, bits="01101010")
            self.below_head(table, buff=GAP_MD * 1.6)
            self.play(Write(table.headings), Create(table.rule),
                      run_time=t.fill(0.093))
            self.play(Write(table.digits), run_time=t.fill(0.093))
            chain = VGroup(
                MathTex("64 + 32 + 8 + 2", font_size=EQUATION_SIZE,
                        color=CHARCOAL),
                MathTex("96 + 8 + 2", font_size=EQUATION_SIZE,
                        color=CHARCOAL),
                MathTex("104 + 2", font_size=EQUATION_SIZE, color=CHARCOAL),
            )
            for m in chain:
                m.next_to(table, DOWN, buff=GAP_MD * 1.5)
            answer = MathTex("106", font_size=DISPLAY_SIZE, color=SAGE)
            answer.move_to(chain[0])
            self.play(Write(chain[0]), run_time=t.fill(0.093))
            self.play(TransformMatchingTex(chain[0], chain[1]),
                      run_time=t.fill(0.093))
            self.play(TransformMatchingTex(chain[1], chain[2]),
                      run_time=t.fill(0.093))
            self.play(TransformMatchingTex(chain[2], answer),
                      run_time=t.fill(0.093))
            self.work.add(table, answer)
            t.hold()

    def denary_to_binary(self):
        bits = "01011101"
        remainders = [93, 93, 29, 29, 13, 5, 1, 1]

        with self.beat("denary_to_binary") as t:
            self.clear_all(t)
            self.set_head(t, "Part 5 — Denary to binary")
            target = MathTex("93", font_size=TITLE_SIZE * 1.4,
                             color=CHARCOAL)
            self.below_head(target, buff=GAP_MD * 1.2)
            table = BitTable(COLUMNS)
            table.next_to(target, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(target), run_time=t.fill(0.155))
            self.play(Write(table.headings), Create(table.rule),
                      run_time=t.fill(0.186))
            self.table = table
            self.work.add(target, table)
            t.hold()

        with self.beat("subtract_walk") as t:
            note = serif("can I subtract this column without going negative?",
                         LABEL_SIZE, GREY)
            note.next_to(self.table, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(note), run_time=t.fill(0.062))
            box = self.table.column_box(0)
            self.play(Create(box), run_time=t.fill(0.025))
            digits = VGroup()
            for i, bit in enumerate(bits):
                if i > 0:
                    self.play(Transform(box, self.table.column_box(i)),
                              run_time=t.fill(0.022))
                digit = MathTex(
                    bit, font_size=EQUATION_SIZE,
                    color=SAGE if bit == "1" else GREY,
                )
                digit.move_to(self.table.heading(i))
                digit.shift(DOWN * 1.1)
                digits.add(digit)
                self.play(Write(digit), run_time=t.fill(0.025))
            self.play(FadeOut(box), FadeOut(note), run_time=t.fill(0.025))
            self.work.add(digits)
            self.answer_digits = digits
            t.hold()

        with self.beat("result93") as t:
            check = MathTex("64 + 16 + 8 + 4 + 1 = 93",
                            font_size=EQUATION_SIZE, color=SAGE)
            check.next_to(self.answer_digits, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(check), run_time=t.fill(0.248))
            self.play(Create(self.underline(check)), run_time=t.fill(0.093))
            self.work.add(check)
            t.hold()

    def division_method(self):
        with self.beat("division") as t:
            self.clear_all(t)
            self.set_head(t, "Part 6 — The division-by-2 method")
            lines = VGroup(*[
                MathTex(row, font_size=EQUATION_SIZE, color=CHARCOAL)
                for row in (
                    "26 \\div 2 = 13 \\;\\; \\text{r } 0",
                    "13 \\div 2 = 6 \\;\\; \\text{r } 1",
                    "6 \\div 2 = 3 \\;\\; \\text{r } 0",
                    "3 \\div 2 = 1 \\;\\; \\text{r } 1",
                    "1 \\div 2 = 0 \\;\\; \\text{r } 1",
                )
            ]).arrange(DOWN, buff=GAP_SM * 1.3, aligned_edge=LEFT)
            self.below_head(lines, buff=GAP_MD * 1.3)
            for line in lines:
                self.play(Write(line), run_time=t.fill(0.087))
            self.work.add(lines)
            self.division_lines = lines
            t.hold()

        with self.beat("read_up") as t:
            arrow = Line(
                self.division_lines.get_right() + RIGHT * 0.6 + DOWN * 0.9,
                self.division_lines.get_right() + RIGHT * 0.6 + UP * 0.9,
                color=TERRACOTTA, stroke_width=4,
            )
            label = serif("read bottom to top", LABEL_SIZE, TERRACOTTA)
            label.next_to(arrow, RIGHT, buff=GAP_SM)
            self.play(Create(arrow), Write(label), run_time=t.fill(0.124))
            result = mono("11010", TITLE_SIZE, CHARCOAL)
            result.next_to(self.division_lines, DOWN, buff=GAP_MD * 1.3)
            padded = mono("00011010", TITLE_SIZE, CHARCOAL)
            padded.move_to(result)
            self.play(Write(result), run_time=t.fill(0.124))
            self.play(FadeOut(result), FadeIn(padded), run_time=t.fill(0.093))
            check = MathTex("16 + 8 + 2 = 26", font_size=EQUATION_SIZE,
                            color=SAGE)
            check.next_to(padded, DOWN, buff=GAP_MD * 1.1)
            self.play(Write(check), run_time=t.fill(0.155))
            self.work.add(arrow, label, padded, check)
            t.hold()

        with self.beat("two_methods") as t:
            self.clear_all(t)
            self.set_head(t, "Two methods — know both")
            methods = VGroup(
                serif("the powers-of-two column method", BODY_SIZE),
                serif("successive division by 2", BODY_SIZE),
            ).arrange(DOWN, buff=GAP_MD * 1.4)
            self.below_head(methods, buff=GAP_MD * 2.0)
            self.play(Write(methods[0]), run_time=t.fill(0.186))
            self.play(Write(methods[1]), run_time=t.fill(0.186))
            self.work.add(methods)
            t.hold()

    def unsigned_range(self):
        with self.beat("range_min") as t:
            self.clear_all(t)
            self.set_head(t, "Part 7 — How large can 8 bits go?")
            smallest = MathTex("00000000 \\;\\rightarrow\\; 0",
                               font_size=DISPLAY_SIZE, color=CHARCOAL)
            self.below_head(smallest, buff=GAP_MD * 1.6)
            self.play(Write(smallest), run_time=t.fill(0.248))
            self.work.add(smallest)
            self.smallest = smallest
            t.hold()

        with self.beat("range_max") as t:
            largest = MathTex("11111111", font_size=DISPLAY_SIZE,
                              color=CHARCOAL)
            largest.next_to(self.smallest, DOWN, buff=GAP_MD * 1.3)
            total = MathTex("128 + 64 + 32 + 16 + 8 + 4 + 2 + 1 = 255",
                            font_size=EQUATION_SIZE, color=CHARCOAL)
            total.next_to(largest, DOWN, buff=GAP_MD * 1.2)
            span = serif("an unsigned 8-bit integer holds 0 to 255",
                         BODY_SIZE, SAGE)
            span.next_to(total, DOWN, buff=GAP_MD * 1.2)
            self.play(Write(largest), run_time=t.fill(0.124))
            self.play(Write(total), run_time=t.fill(0.186))
            self.play(Write(span), run_time=t.fill(0.155))
            self.work.add(largest, total, span)
            t.hold()

        with self.beat("formula") as t:
            self.clear_all(t)
            self.set_head(t, "The formula")
            steps = VGroup(
                MathTex("n \\text{ bits} \\;\\rightarrow\\; 2^n "
                        "\\text{ patterns}", font_size=DISPLAY_SIZE,
                        color=CHARCOAL),
                MathTex("2^8 = 256", font_size=DISPLAY_SIZE, color=CHARCOAL),
                MathTex("2^8 - 1 = 255", font_size=DISPLAY_SIZE, color=SAGE),
            ).arrange(DOWN, buff=GAP_MD * 1.3)
            self.below_head(steps, buff=GAP_MD * 1.6)
            self.play(Write(steps[0]), run_time=t.fill(0.186))
            self.play(Write(steps[1]), run_time=t.fill(0.155))
            why = serif("one pattern is used by zero", LABEL_SIZE, GREY)
            why.next_to(steps, DOWN, buff=GAP_MD * 1.2)
            self.play(Write(steps[2]), run_time=t.fill(0.124))
            self.play(Write(why), run_time=t.fill(0.093))
            self.work.add(steps, why)
            t.hold()

        with self.beat("overflow_tease") as t:
            self.clear_all(t)
            tease = serif("Remember this — it matters for overflow.",
                          BODY_SIZE * 1.15)
            tease.move_to(ORIGIN)
            self.play(Write(tease), run_time=t.fill(0.248))
            self.play(Create(self.underline(tease, TERRACOTTA)),
                      run_time=t.fill(0.124))
            t.hold()
