"""Text furniture shared between lectures: wrapping, lists and columns.

These four started life inside scenes/cs/software.py and moved here when
Chapter 5 needed the same list and the same table. Nothing about them is
specific to a chapter.

  * ``fit``       shrink to the frame, as a last resort.
  * ``prose``     a sentence that wraps to fit rather than shrinking,
                  because shrinking is how text ends up under the 28px
                  floor without anyone deciding that it should.
  * ``numbered``  a numbered list with a hanging indent.
  * ``columns``   any number of columns of prose on one left edge each.

``columns`` replaces an earlier three-column ``comparison``. Its column
positions are measured rather than chosen, and that is the whole point of
it: hardcoded x values were wrong twice over in the chapter it was
written for. The serif face is wider per character than it looks, so a
table meant to fit 12.6 units came out at 12.97; the fix by eye then put
two columns four hundredths apart. Taking each column's width from its
own widest cell makes both faults impossible to reintroduce, and the
error message names the column to shorten.
"""

import textwrap

from manim import Line, VGroup, LEFT, ORIGIN, RIGHT, UP

from brand import (
    BODY_SIZE,
    CHARCOAL,
    GAP_MD,
    GAP_SM,
    GREY,
    LABEL_SIZE,
    MARGIN_SIZE,
    serif,
)
from components.os_shape import align_baselines

FRAME_SAFE = 12.6


def fit(mobject, width=FRAME_SAFE):
    if mobject.width > width:
        mobject.scale_to_fit_width(width)
    return mobject


def prose(text, size=BODY_SIZE, color=CHARCOAL, width=FRAME_SAFE):
    """A sentence that wraps to fit rather than shrinking to fit."""
    body = serif(text, size, color)
    if body.width <= width:
        return body
    budget = max(10, int(len(text) * width / body.width))
    while budget >= 10:
        body = serif(textwrap.fill(text, budget), size, color)
        if body.width <= width:
            return body
        budget -= 2
    return fit(body, width)


def numbered(items, size=LABEL_SIZE, color=CHARCOAL, number_color=GREY,
             gap=GAP_SM * 1.4, width=FRAME_SAFE):
    """A numbered list with a hanging indent, like ``FunctionList``.

    Returns the group and the rows, so a scene can bring them in one at
    a time. Each row is placed from one origin rather than next to the
    row above, because a row whose text has no descender sits higher
    than one that does and a column built with ``next_to`` walks.
    """
    rows, numbers, labels = VGroup(), [], []
    for index, text in enumerate(items):
        number = serif(f"{index + 1}", size, number_color)
        label = prose(text, size, color, width - 1.0)
        numbers.append(number)
        labels.append(label)

    widest = max(number.width for number in numbers)
    pitch = max(label.height for label in labels) + gap
    for index, (number, label) in enumerate(zip(numbers, labels)):
        y = -index * pitch
        number.move_to([-width / 2 + widest, y, 0], aligned_edge=RIGHT)
        label.move_to([-width / 2 + widest + GAP_SM * 1.4, y, 0],
                      aligned_edge=LEFT)
        # A wrapped label is taller than one line, so its centre is not
        # its first line. Lift it so the first line sits on the number.
        if label.height > pitch - gap + 0.01:
            label.shift(UP * (label.height - (pitch - gap)) / 2)
        row = VGroup(number, label)
        rows.add(row)
    group = VGroup(rows)
    group.move_to(ORIGIN)
    if group.width > width:
        raise ValueError(
            f"A numbered list is {group.width:.2f} units wide, over the "
            f"{width:.2f} the frame allows.")
    return group, rows


def columns(heads, entries, size=MARGIN_SIZE, row_gap=GAP_SM * 1.7,
            col_gap=GAP_MD * 0.8, width=FRAME_SAFE, rule=True):
    """Columns of prose, each on its own left edge, under a header row.

    ``make_table`` in components.table right-aligns its cells, which is
    right for numbers and wrong for prose.

    Returns (group, cells, headers). ``cells[r][c]`` is one body cell, so
    a scene can reveal a column at a time or a row at a time. The first
    column and the header row are grey: they label, they do not inform.
    """
    width_count = len(heads)
    table = [list(heads)] + [list(row) for row in entries]
    for index, row in enumerate(table):
        if len(row) != width_count:
            raise ValueError(
                f"Row {index} has {len(row)} cells and the header has "
                f"{width_count}.")

    made = [[serif(text, size, GREY if i == 0 or j == 0 else CHARCOAL)
             for j, text in enumerate(row)]
            for i, row in enumerate(table)]
    spans = [max(row[j].width for row in made) for j in range(width_count)]

    total = sum(spans) + col_gap * (width_count - 1)
    if total > width:
        raise ValueError(
            f"The table needs {total:.2f} units and the frame allows "
            f"{width:.2f}. Shorten the longest cell in the widest column: "
            + ", ".join(f"{span:.2f}" for span in spans))

    left = -total / 2
    xs = []
    for span in spans:
        xs.append(left)
        left += span + col_gap

    pitch = made[0][0].height + row_gap
    group, cells = VGroup(), []
    for i, row in enumerate(made):
        y = 0.0 if i == 0 else -(i * pitch + row_gap)
        for j, cell in enumerate(row):
            cell.move_to([xs[j], y, 0], aligned_edge=LEFT)
            group.add(cell)
        # One baseline per row. move_to centres on the ink box, so a cell
        # with a descender sits a few pixels off one without.
        align_baselines(row, list(table[i]), size)
        if i:
            cells.append(row)

    if rule:
        line = Line([xs[0] - GAP_SM, -pitch / 2 - row_gap / 2, 0],
                    [xs[-1] + spans[-1] + GAP_SM, -pitch / 2 - row_gap / 2, 0],
                    color=GREY, stroke_width=1.5)
        group.add(line)
        group.rule = line
    else:
        group.rule = None
    group.move_to(ORIGIN)
    return group, cells, made[0]
