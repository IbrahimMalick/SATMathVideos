"""A minimal editorial table: header row, one grey rule, right-aligned cells."""

import numpy as np

from manim import Line, VGroup, ORIGIN, RIGHT

from brand import CHARCOAL, GAP_SM, GREY, LABEL_SIZE, serif


def make_table(headers, rows, row_height=0.6, col_widths=None):
    """Returns (group, cells); cells[(row, col)] is the cell mobject, row 0
    is the header."""
    n_cols = len(headers)
    col_widths = col_widths or [2.4] * n_cols
    x_right = np.cumsum(col_widths)
    cells = {}
    group = VGroup()
    for i, row in enumerate([headers] + [list(r) for r in rows]):
        for j, cell_text in enumerate(row):
            color = GREY if i == 0 else CHARCOAL
            cell = serif(str(cell_text), LABEL_SIZE, color)
            cell.move_to(np.array([x_right[j], -i * row_height, 0]), aligned_edge=RIGHT)
            cells[(i, j)] = cell
            group.add(cell)
    rule = Line(
        np.array([0, -row_height / 2, 0]),
        np.array([x_right[-1] + GAP_SM, -row_height / 2, 0]),
        color=GREY,
        stroke_width=1.5,
    )
    group.add(rule)
    group.move_to(ORIGIN)
    return group, cells
