"""Furniture for the house-style cut of the cohort ad.

The other cut keeps the client's footage. This one has none, so the
pictures have to carry the argument themselves — and the argument is that
the course teaches code tracing, so the hero of the ad is a trace table
filling in beside the loop it traces. A parent watching sees exactly what
the two hours a week look like.

The loop is deliberately the smallest one that still has something to
trace, and its numbers are checked rather than typed:

    int sum = 0;
    for (int i = 1; i <= 4; i++) { sum += i; }   ->  1, 3, 6, 10

``LOOP_ROWS`` is derived from that in Python, so the table on screen and
the code above it cannot drift apart. ``measure()`` checks the derivation
and the sizing together.

Everything here raises rather than shrinks when a label will not fit. A
figure scaled to 0.9 takes its 28px labels to 25px, and an ad is watched
on a phone.
"""

from manim import (
    Dot,
    Line,
    SurroundingRectangle,
    VGroup,
    DOWN,
    LEFT,
    RIGHT,
    UP,
)

from brand import (
    CHARCOAL,
    GAP_MD,
    GAP_SM,
    GREY,
    LABEL_SIZE,
    MARGIN_SIZE,
    SAGE,
    SLATE,
    TERRACOTTA,
    mono,
    serif,
)

# Spaced tightly on purpose. At the 28px floor the roomier
# "for (int i = 1; i <= 4; i++) {" runs 6.98 units of monospace before the
# panel border, which leaves no frame for the trace table beside it, and
# the fix for that is never to shrink the code.
#
# One string with newlines, not a line per Text. A mobject's bounding box
# is its ink, so a line that starts with spaces has its box start at the
# first visible glyph, and arrange(aligned_edge=LEFT) then pulls the
# indent off the loop body. Handing Pango the whole block instead lets it
# lay the lines out itself, and the indent survives: measured at four
# character widths, which is what it should be.
JAVA = """int sum = 0;
for (int i=1; i<=4; i++) {
    sum += i;
}
System.out.println(sum);"""


def loop_rows():
    """The trace of the loop above, run rather than typed."""
    rows, total = [], 0
    for i in range(1, 5):
        total += i
        rows.append((i, total))
    return rows


LOOP_ROWS = loop_rows()
LOOP_ANSWER = str(LOOP_ROWS[-1][1])


def java_block(code=None, size=LABEL_SIZE, width=8.1, color=CHARCOAL,
               accent=SLATE):
    """A Java snippet in a panel, monospace and indented as written."""
    body = mono(JAVA if code is None else code, size, color)
    box = SurroundingRectangle(body, color=accent, buff=GAP_SM * 1.2,
                               stroke_width=2.5, corner_radius=0.0)
    panel = VGroup(box, body)
    if panel.width > width:
        raise ValueError(
            f"The code panel is {panel.width:.2f} units wide at size {size}, "
            f"over the {width:.2f} it is given. Drop the size or shorten a "
            "line; do not scale it, or the code goes under the floor."
        )
    panel.body, panel.box = body, box
    return panel


def dots_row(count=10, lit=1, radius=0.17, gap=GAP_SM * 1.5,
             color=SLATE, lit_color=TERRACOTTA, width=8.0):
    """One dot per seat, a few of them taken.

    "Capped at ten" is a number a listener forgets and a picture they do
    not: ten dots is small enough to count at a glance, which is the whole
    claim.
    """
    row = VGroup(*[Dot(radius=radius,
                       color=lit_color if i < lit else color)
                   for i in range(count)])
    for i, dot in enumerate(row):
        dot.set_fill(lit_color if i < lit else color,
                     opacity=1.0 if i < lit else 0.25)
    row.arrange(RIGHT, buff=gap)
    if row.width > width:
        raise ValueError(
            f"{count} dots run {row.width:.2f} units, over {width:.2f}.")
    return row


def timeline(points, width=9.6, size=MARGIN_SIZE, color=GREY,
             mark=SLATE, lit=TERRACOTTA, highlight=-1):
    """A line from one date to another, with the stops labelled.

    ``points`` is a list of (label, fraction along the line). The last one
    is lit by default, because the last one is the exam.
    """
    rail = Line([-width / 2, 0, 0], [width / 2, 0, 0], color=color,
                stroke_width=3)
    group = VGroup(rail)
    ticks, labels = VGroup(), VGroup()
    highlight = len(points) + highlight if highlight < 0 else highlight

    for index, (text, where) in enumerate(points):
        accent = lit if index == highlight else mark
        x = -width / 2 + width * where
        tick = Line([x, -0.16, 0], [x, 0.16, 0], color=accent,
                    stroke_width=4)
        label = serif(text, size, accent if index == highlight else CHARCOAL)
        label.next_to(tick, UP, buff=GAP_SM * 0.9)
        # The outer labels would otherwise hang off the ends of the rail.
        if where <= 0.02:
            label.move_to([x + label.width / 2 - 0.1,
                           label.get_center()[1], 0])
        elif where >= 0.98:
            label.move_to([x - label.width / 2 + 0.1,
                           label.get_center()[1], 0])
        ticks.add(tick)
        labels.add(label)
        group.add(tick, label)

    group.rail, group.ticks, group.labels = rail, ticks, labels
    return group


def price_compare(rows, size=LABEL_SIZE, width=10.0, gap=GAP_MD * 1.6):
    """Two offers side by side, so the cheaper one is seen and not claimed.

    ``rows`` is a list of (what, how much). Returns the group plus the
    amount mobjects, so a scene can strike one through.
    """
    table, amounts = VGroup(), []
    for what, amount in rows:
        left = serif(what, size, CHARCOAL)
        right = serif(amount, size, CHARCOAL)
        amounts.append(right)
        table.add(VGroup(left, right))

    widest_left = max(row[0].width for row in table)
    widest_right = max(row[1].width for row in table)
    span = widest_left + gap + widest_right
    if span > width:
        raise ValueError(
            f"The comparison runs {span:.2f} units, over {width:.2f}.")
    for row in table:
        row[0].move_to([-span / 2 + row[0].width / 2, 0, 0])
        row[1].move_to([span / 2 - row[1].width / 2, 0, 0])
    table.arrange(DOWN, buff=GAP_SM * 1.6)
    for row in table:
        row[0].move_to([-span / 2 + row[0].width / 2,
                        row[0].get_center()[1], 0])
        row[1].move_to([span / 2 - row[1].width / 2,
                        row[1].get_center()[1], 0])
    table.amounts = amounts
    return table


def strike(mobject, color=TERRACOTTA, stroke=3.5):
    return Line(mobject.get_left() + LEFT * 0.1,
                mobject.get_right() + RIGHT * 0.1,
                color=color, stroke_width=stroke)


def tick(size=0.34, color=SAGE, stroke=5):
    """A check mark, for the moment the program runs."""
    return VGroup(
        Line([-size, 0, 0], [-size * 0.3, -size * 0.7, 0],
             color=color, stroke_width=stroke),
        Line([-size * 0.3, -size * 0.7, 0], [size, size * 0.72, 0],
             color=color, stroke_width=stroke),
    )


def measure():
    """Check the loop's arithmetic and every figure's sizing.

    Run as ``python -m components.ad_house`` from the repo root.
    """
    from manim import config

    expected = [(1, 1), (2, 3), (3, 6), (4, 10)]
    print(f"loop rows {LOOP_ROWS}  "
          f"{'ok' if LOOP_ROWS == expected else 'WRONG'}")
    print(f"answer {LOOP_ANSWER}  {'ok' if LOOP_ANSWER == '10' else 'WRONG'}")

    half_w, half_h = config.frame_width / 2, config.frame_height / 2
    figures = [
        ("java", java_block()),
        ("java small", java_block(size=MARGIN_SIZE, width=6.7)),
        ("dots", dots_row()),
        ("timeline", timeline([("Nov 16", 0.0), ("May 12", 1.0)])),
        ("compare", price_compare([("One-to-one tutor", "$200 / hour"),
                                   ("This cohort", "$100 / month")])),
        ("tick", tick()),
    ]
    for name, group in figures:
        group.move_to([0, 0, 0])
        fits = (group.get_left()[0] > -half_w
                and group.get_right()[0] < half_w
                and group.get_bottom()[1] > -half_h
                and group.get_top()[1] < half_h)
        print(f"{name:11} {group.width:5.2f} x {group.height:5.2f}  "
              f"{'ok' if fits else 'OFF FRAME'}")


if __name__ == "__main__":
    measure()
