"""SyllabusMap and TopicStrip — the shape of a whole course, on one frame.

The roadmap lecture's spine is the ten Cambridge topics. The student sees
them twice: once in full, as a two-column map of the two papers, and then
as a thin numbered strip along the bottom that says "you are here" while
each topic is explained.

    mapping = SyllabusMap([("Paper 1 · Computer Systems", rows1),
                           ("Paper 2 · Algorithms, Programming & Logic", rows2)])
    self.play(*mapping.focus(0))     # topic 1 in terracotta, the rest grey

    strip = TopicStrip(10, split=6)
    self.play(*strip.focus(0))

Row indices are global across the columns, so topic seven is index 6 in
both the map and the strip — the caller never has to know which column a
topic lives in.
"""

from manim import DOWN, LEFT, RIGHT, UP, Square, VGroup

from brand import (
    CHARCOAL,
    CREAM,
    GAP_LG,
    GAP_SM,
    GREY,
    LABEL_SIZE,
    MARGIN_SIZE,
    TERRACOTTA,
    serif,
)

FRAME_SAFE = 12.6


class SyllabusMap(VGroup):
    """Two columns of numbered topics, one lit at a time."""

    def __init__(self, columns, size=LABEL_SIZE, head_size=LABEL_SIZE,
                 dim=GREY, lit=TERRACOTTA, stacked=False):
        """``stacked`` puts the groups one above the other instead of side
        by side. Real syllabus titles are long: two columns of them only
        fit by shrinking the text under the 28px floor, so a list that
        runs down the frame is usually the legible choice."""
        super().__init__()
        self.dim_color, self.lit_color = dim, lit

        self.heads = VGroup()
        self.rows = VGroup()
        stacks = VGroup()
        for heading, entries in columns:
            head = serif(heading, head_size, CHARCOAL)
            self.heads.add(head)
            stack = VGroup(head)
            for number, title in entries:
                row = serif(f"{number}   {title}", size, dim)
                self.rows.add(row)
                stack.add(row)
            stack.arrange(DOWN, buff=GAP_SM * 0.8, aligned_edge=LEFT)
            stacks.add(stack)
        if stacked:
            stacks.arrange(DOWN, buff=GAP_SM * 1.6, aligned_edge=LEFT)
        else:
            stacks.arrange(RIGHT, buff=GAP_LG, aligned_edge=UP)
        if stacks.width > FRAME_SAFE:
            stacks.scale_to_fit_width(FRAME_SAFE)
        self.add(stacks)

    def head(self, index):
        return self.heads[index]

    def row(self, index):
        return self.rows[index]

    def focus(self, index):
        moves = []
        for i, row in enumerate(self.rows):
            moves.append(row.animate.set_color(
                self.lit_color if i == index else self.dim_color))
        return moves

    def focus_range(self, start, stop):
        """Light a contiguous block — used when a whole paper is in view."""
        moves = []
        for i, row in enumerate(self.rows):
            colour = CHARCOAL if start <= i < stop else self.dim_color
            moves.append(row.animate.set_color(colour))
        return moves

    def dim_all(self):
        return [row.animate.set_color(self.dim_color) for row in self.rows]


class TopicStrip(VGroup):
    """A numbered square per topic, with a gap at the paper boundary.

    Persistent furniture: it stays on screen while the topics are explained
    so the student always knows how far through the map we are.
    """

    def __init__(self, count, split=None, side=0.62, size=MARGIN_SIZE,
                 dim=GREY, lit=TERRACOTTA):
        super().__init__()
        self.dim_color, self.lit_color = dim, lit
        self.cells = VGroup()
        self.numbers = VGroup()

        row = VGroup()
        for i in range(count):
            if split is not None and i == split:
                row.add(Square(side_length=side, stroke_opacity=0,
                               fill_opacity=0))   # spacer at the paper break
            cell = Square(side_length=side, color=dim, stroke_width=2)
            number = serif(str(i + 1), size, dim)
            if number.width > side * 0.82:
                number.scale_to_fit_width(side * 0.82)
            number.move_to(cell)
            self.cells.add(cell)
            self.numbers.add(number)
            row.add(VGroup(cell, number))
        row.arrange(RIGHT, buff=GAP_SM * 0.7)
        self.add(row)

    def focus(self, index):
        moves = []
        for i, (cell, number) in enumerate(zip(self.cells, self.numbers)):
            if i == index:
                moves.append(cell.animate.set_stroke(self.lit_color)
                             .set_fill(self.lit_color, opacity=1))
                moves.append(number.animate.set_color(CREAM))
            else:
                moves.append(cell.animate.set_stroke(self.dim_color)
                             .set_fill(self.dim_color, opacity=0))
                moves.append(number.animate.set_color(self.dim_color))
        return moves
