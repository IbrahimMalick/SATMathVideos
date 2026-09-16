"""BitTable — column headings with digits underneath.

The workhorse of the number-systems lecture: a row of place values
(128 64 32 ... 1, or Thousands Hundreds Tens Units) with an optional second
heading row and an optional row of digits beneath.

    table = BitTable([128, 64, 32, 16, 8, 4, 2, 1], bits="10110101")
    self.play(Write(table.headings))
    self.play(Write(table.digits))
    self.play(Create(table.column_box(0)))     # spotlight one column

Headings that look like numbers render as MathTex; anything else renders as
serif Text, so the same component draws the denary table in Part 2 and the
binary table everywhere after it.
"""

from manim import DOWN, LEFT, Line, MathTex, RIGHT, SurroundingRectangle, UP, VGroup

from brand import (
    CHARCOAL,
    EQUATION_SIZE,
    GAP_MD,
    GAP_SM,
    GREY,
    LABEL_SIZE,
    TERRACOTTA,
    serif,
)


def _is_number(value):
    return str(value).strip().lstrip("-").replace(",", "").isdigit()


def _cell(value, font_size, color):
    if _is_number(value):
        return MathTex(str(value), font_size=font_size, color=color)
    return serif(str(value), font_size, color)


class BitTable(VGroup):
    def __init__(
        self,
        headings,
        subheadings=None,
        bits=None,
        cell_width=1.2,
        heading_size=LABEL_SIZE,
        digit_size=EQUATION_SIZE,
        heading_color=CHARCOAL,
        digit_color=CHARCOAL,
        rule=True,
    ):
        super().__init__()
        self.cell_width = cell_width
        self.n = len(headings)

        def row(values, size, color):
            cells = VGroup(*[_cell(v, size, color) for v in values])
            for i, cell in enumerate(cells):
                cell.move_to(RIGHT * (i - (self.n - 1) / 2) * cell_width)
            return cells

        self.headings = row(headings, heading_size, heading_color)
        self.add(self.headings)

        self.subheadings = None
        if subheadings is not None:
            self.subheadings = row(subheadings, heading_size, heading_color)
            self.subheadings.next_to(self.headings, DOWN, buff=GAP_SM)
            self.add(self.subheadings)

        anchor = self.subheadings if self.subheadings is not None else self.headings

        self.rule = None
        if rule:
            half = self.n * cell_width / 2
            self.rule = Line(
                LEFT * half, RIGHT * half, color=GREY, stroke_width=2,
            )
            self.rule.next_to(anchor, DOWN, buff=GAP_SM * 0.8)
            self.add(self.rule)
            anchor = self.rule

        self.digits = None
        if bits is not None:
            self.digits = row(list(bits), digit_size, digit_color)
            self.digits.next_to(anchor, DOWN, buff=GAP_SM)
            self.add(self.digits)

    # ------------------------------------------------------------- access

    def heading(self, i):
        return self.headings[i]

    def digit(self, i):
        if self.digits is None:
            raise ValueError("this BitTable was built without digits")
        return self.digits[i]

    def column(self, i):
        """Heading and digit for one column, as a group."""
        parts = [self.headings[i]]
        if self.subheadings is not None:
            parts.append(self.subheadings[i])
        if self.digits is not None:
            parts.append(self.digits[i])
        return VGroup(*parts)

    def column_box(self, i, color=TERRACOTTA, buff=GAP_SM * 0.7):
        return SurroundingRectangle(
            self.column(i), color=color, buff=buff, stroke_width=3,
        )

    def caption(self, text, color=GREY, size=LABEL_SIZE, buff=GAP_MD):
        note = serif(text, size, color)
        note.next_to(self, DOWN, buff=buff)
        return note
