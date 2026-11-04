"""A labelled matrix, a column vector, and the product of the two.

The whole lesson is one picture: a table whose columns are groups of
people, whose rows are things those people need, multiplied by a column of
headcounts. So the component carries the numbers and derives everything
said about them — the per-row working line and the output vector both come
out of the data, and cannot disagree with the grid they sit next to.

    grid = MatrixGrid(NEEDS, ROWS, COLS)
    self.play(Create(grid.brackets), Write(grid.entries))
    self.play(*grid.light_col(0))
    self.play(Write(grid.working(0, HEADS)))   # 1x3 + 1x2 + 2x4 = 13

Sized for the landscape lecture frame, and sized to its labels: nothing
here should ever be scaled down by the scene, because a diagram at 0.9
takes its 28px captions to 25px.
"""

from manim import DOWN, LEFT, Line, RIGHT, UP, VGroup

from brand import (
    BODY_SIZE,
    CHARCOAL,
    GAP_MD,
    GAP_SM,
    GREY,
    LABEL_SIZE,
    MARGIN_SIZE,
    SAGE,
    SLATE,
    TERRACOTTA,
    serif,
)

FRAME_SAFE = 12.6


def fit(mobject, width=FRAME_SAFE):
    if mobject.width > width:
        mobject.scale_to_fit_width(width)
    return mobject


def _bracket(left, right, top, bottom, color, stroke, tick):
    """A square bracket pair, drawn rather than set in LaTeX.

    Drawn so the grid can be built from Text and therefore measured by the
    legibility check, which only sees Text; a LaTeX matrix would render its
    numbers where nothing in the pipeline can check their size.
    """
    def side(x, direction):
        return VGroup(
            Line([x, top, 0], [x, bottom, 0], color=color,
                 stroke_width=stroke),
            Line([x, top, 0], [x + direction * tick, top, 0], color=color,
                 stroke_width=stroke),
            Line([x, bottom, 0], [x + direction * tick, bottom, 0],
                 color=color, stroke_width=stroke),
        )
    return VGroup(side(left, 1), side(right, -1))


class MatrixGrid(VGroup):
    """Rows of numbers in brackets, with a label beside each row and above
    each column."""

    # cell is the column pitch, and it is set by the column *labels*, not
    # by the digits: "students" and "teachers" are 1.67 units wide at the
    # 28px floor, so a narrower pitch runs one header into the next. The
    # overlap check misses it, because two headers touching by a tenth of
    # a unit is below the share of area it reports on.
    def __init__(self, data, row_labels=None, col_labels=None,
                 size=BODY_SIZE, label_size=MARGIN_SIZE, cell=1.95,
                 row_pitch=0.86, color=CHARCOAL, frame=SLATE, lit=TERRACOTTA,
                 dim=GREY, pad=0.42):
        super().__init__()
        self.data = [list(row) for row in data]
        self.n_rows, self.n_cols = len(self.data), len(self.data[0])
        if any(len(r) != self.n_cols for r in self.data):
            raise ValueError("every row of a matrix must be the same length")
        self.lit_color, self.dim_color, self.base_color = lit, dim, color

        self.entries, self.cells = VGroup(), {}
        for r, row in enumerate(self.data):
            for c, value in enumerate(row):
                text = serif(str(value), size, color)
                text.move_to([(c - (self.n_cols - 1) / 2) * cell,
                              -(r - (self.n_rows - 1) / 2) * row_pitch, 0])
                self.cells[(r, c)] = text
                self.entries.add(text)

        half_w = (self.n_cols - 1) / 2 * cell + cell / 2
        half_h = (self.n_rows - 1) / 2 * row_pitch + row_pitch / 2
        self.brackets = _bracket(-half_w - pad * 0.3, half_w + pad * 0.3,
                                 half_h, -half_h, frame, 3.5, 0.22)
        self.add(self.brackets, self.entries)

        self.row_labels, self.col_labels = VGroup(), VGroup()
        if row_labels:
            for r, name in enumerate(row_labels):
                label = serif(name, label_size, dim)
                label.next_to(self.brackets, LEFT, buff=GAP_MD * 0.8)
                label.set_y(self.cells[(r, 0)].get_center()[1])
                self.row_labels.add(label)
            self.add(self.row_labels)
        if col_labels:
            for c, name in enumerate(col_labels):
                label = serif(name, label_size, dim)
                label.next_to(self.brackets, UP, buff=GAP_SM * 0.9)
                label.set_x(self.cells[(0, c)].get_center()[0])
                self.col_labels.add(label)
            self.add(self.col_labels)

    # ------------------------------------------------------------ queries

    def entry(self, row, col):
        return self.cells[(row, col)]

    def column(self, col):
        return VGroup(*[self.cells[(r, col)] for r in range(self.n_rows)])

    def row(self, row):
        return VGroup(*[self.cells[(row, c)] for c in range(self.n_cols)])

    def product(self, vector):
        """The matrix times a column of numbers, computed not typed."""
        if len(vector) != self.n_cols:
            raise ValueError(
                f"a {self.n_rows}x{self.n_cols} matrix takes a vector of "
                f"{self.n_cols} numbers, got {len(vector)}")
        return [sum(self.data[r][c] * vector[c] for c in range(self.n_cols))
                for r in range(self.n_rows)]

    # --------------------------------------------------------- animations

    def light_col(self, col, color=None, others=None):
        color = color or self.lit_color
        others = others or self.base_color
        moves = []
        for c in range(self.n_cols):
            tint = color if c == col else others
            for r in range(self.n_rows):
                moves.append(self.cells[(r, c)].animate.set_color(tint))
            if len(self.col_labels):
                moves.append(self.col_labels[c].animate.set_color(
                    color if c == col else self.dim_color))
        return moves

    def light_row(self, row, color=None, others=None):
        color = color or self.lit_color
        others = others or self.base_color
        moves = []
        for r in range(self.n_rows):
            tint = color if r == row else others
            for c in range(self.n_cols):
                moves.append(self.cells[(r, c)].animate.set_color(tint))
            if len(self.row_labels):
                moves.append(self.row_labels[r].animate.set_color(
                    color if r == row else self.dim_color))
        return moves

    def settle(self):
        moves = [t.animate.set_color(self.base_color) for t in self.entries]
        moves += [l.animate.set_color(self.dim_color)
                  for l in list(self.row_labels) + list(self.col_labels)]
        return moves

    # -------------------------------------------------------------- lines

    def working(self, row, vector, size=LABEL_SIZE, color=CHARCOAL,
                result_color=SAGE, width=FRAME_SAFE):
        """'1x3 + 1x2 + 2x4 = 13', built from the row and the vector.

        Derived rather than passed in, so the line underneath the grid
        cannot drift from the numbers inside it.
        """
        terms = [f"{self.data[row][c]}x{vector[c]}" for c in range(self.n_cols)]
        total = self.product(vector)[row]
        head = serif("  +  ".join(terms) + "  =", size, color)
        tail = serif(str(total), size, result_color)
        # Spaced by the arrangement, not by spaces in the string: Pango
        # drops whitespace at the end of a run, so "... =  " and "... =" are
        # the same width and the result ends up jammed against the sign.
        line = VGroup(head, tail).arrange(RIGHT, buff=GAP_SM * 0.9)
        return fit(line, width)


class ColumnVector(VGroup):
    """A single bracketed column, optionally with a label beside each entry."""

    def __init__(self, values, labels=None, size=BODY_SIZE,
                 label_size=MARGIN_SIZE, row_pitch=0.86, color=CHARCOAL,
                 frame=SLATE, dim=GREY, pad=0.42, label_side=RIGHT):
        super().__init__()
        self.values = list(values)

        self.entries = VGroup()
        for i, value in enumerate(self.values):
            text = serif(str(value), size, color)
            text.move_to([0, -(i - (len(self.values) - 1) / 2) * row_pitch, 0])
            self.entries.add(text)

        half_w = max(0.42, max(t.width for t in self.entries) / 2 + 0.2)
        half_h = (len(self.values) - 1) / 2 * row_pitch + row_pitch / 2
        self.brackets = _bracket(-half_w - pad * 0.3, half_w + pad * 0.3,
                                 half_h, -half_h, frame, 3.5, 0.22)
        self.add(self.brackets, self.entries)

        self.labels = VGroup()
        if labels:
            for i, name in enumerate(labels):
                label = serif(name, label_size, dim)
                label.next_to(self.brackets, label_side, buff=GAP_MD * 0.7)
                label.set_y(self.entries[i].get_center()[1])
                self.labels.add(label)
            self.add(self.labels)

    def light(self, index, color=TERRACOTTA, others=CHARCOAL):
        moves = []
        for i, text in enumerate(self.entries):
            moves.append(text.animate.set_color(color if i == index
                                                else others))
        return moves

    def settle(self, color=CHARCOAL):
        return [t.animate.set_color(color) for t in self.entries]
