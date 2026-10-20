"""TraceTable — a trace table that fills one row at a time.

The whole point of a trace table is that it is filled mechanically, a row
per iteration, so a static table of the finished answer teaches nothing.
This builds the grid up front (so nothing shifts as rows arrive) and hands
back the animations to reveal each row in turn, with the newest row lit.

    table = TraceTable(["Value", "Count"], [(4, 1), (8, 2), (16, 3), (32, 4)],
                       start=(2, 0))
    self.play(Create(table.frame))
    for i in range(len(table.rows)):
        self.play(*table.reveal(i))

The starting state is a row like any other, so the student sees where the
variables began rather than being told.
"""

from manim import DOWN, LEFT, RIGHT, UP, Line, VGroup

from brand import (
    CHARCOAL,
    GAP_SM,
    GREY,
    LABEL_SIZE,
    SLATE,
    TERRACOTTA,
    serif,
)


class TraceTable(VGroup):
    def __init__(self, headers, rows, start=None, size=LABEL_SIZE,
                 col_width=1.9, row_height=0.62, width=None,
                 lit=TERRACOTTA, dim=CHARCOAL):
        super().__init__()
        self.lit_color, self.dim_color = lit, dim
        body = [start] + list(rows) if start is not None else list(rows)
        self.has_start = start is not None

        head = VGroup(*[serif(str(h), size, SLATE) for h in headers])
        for i, cell in enumerate(head):
            cell.move_to(RIGHT * (i - (len(headers) - 1) / 2) * col_width)

        self.rows = VGroup()
        for r, values in enumerate(body):
            row = VGroup(*[serif(str(v), size, dim) for v in values])
            for i, cell in enumerate(row):
                cell.move_to(
                    RIGHT * (i - (len(headers) - 1) / 2) * col_width
                    + DOWN * (r + 1) * row_height)
            self.rows.add(row)

        grid = VGroup(head, self.rows)
        rule = Line(grid.get_left() + LEFT * GAP_SM * 0.6,
                    grid.get_right() + RIGHT * GAP_SM * 0.6,
                    color=GREY, stroke_width=2)
        rule.next_to(head, DOWN, buff=GAP_SM * 0.5)
        rule.set_x(grid.get_x())
        self.head, self.rule = head, rule
        self.add(head, rule, self.rows)
        if width and self.width > width:
            self.scale_to_fit_width(width)

    def reveal(self, index):
        """Light the row that just happened and settle the ones before it."""
        moves = []
        for i, row in enumerate(self.rows):
            if i > index:
                continue
            target = self.lit_color if i == index else self.dim_color
            moves.extend(cell.animate.set_color(target) for cell in row)
        return moves

    def hidden(self):
        """Every row invisible — call before revealing the first one."""
        for row in self.rows:
            row.set_opacity(0)

    def show_row(self, index):
        """Make one row visible; pair with reveal() for the colour."""
        self.rows[index].set_opacity(1)
        return self.rows[index]
