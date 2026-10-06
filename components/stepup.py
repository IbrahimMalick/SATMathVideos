"""Shared furniture for the STEP-UP Paper 2 Shorts.

Five Shorts, one visual language: a pseudocode panel, a memory-rule card,
and the series card that closes every one of them. They live here rather
than in each scene so the fifth Short looks like the first — consistency
across the series is the quality signal, not any single Short's polish.

Sized for the portrait frame (4.5 x 8 units). Portrait is 1.78x denser
than the lecture frame, so a nominal size here reads larger on screen than
the number suggests; the floor that matters is 28px at 1080x1920, which
works out at a nominal ~15.8.
"""

from manim import DOWN, LEFT, ORIGIN, RIGHT, SurroundingRectangle, UP, VGroup

from brand import (
    MARGIN_SIZE,
    CHARCOAL,
    GAP_LG,
    GAP_MD,
    GAP_SM,
    GREY,
    SLATE,
    TERRACOTTA,
    mono,
    serif,
)

PORTRAIT_SAFE = 3.9   # widest anything may run in a 4.5-unit frame

CODE = 30             # pseudocode lines
RULE = 44             # the one rule the viewer should leave holding
SERIES = 30           # the closing series card


def fit(mobject, width=PORTRAIT_SAFE):
    if mobject.width > width:
        mobject.scale_to_fit_width(width)
    return mobject


def code_block(lines, size=CODE, color=CHARCOAL, accent=SLATE,
               width=PORTRAIT_SAFE):
    """Pseudocode in a slate panel. Monospace, left-aligned, boxed.

    Cambridge pseudocode is read line by line, so the lines keep their own
    left edge rather than being centred on each other.
    """
    body = VGroup(*[mono(line, size, color) for line in lines])
    body.arrange(DOWN, buff=GAP_SM * 0.9, aligned_edge=LEFT)
    fit(body, width - 0.45)
    box = SurroundingRectangle(body, color=accent, buff=GAP_SM * 1.1,
                               stroke_width=3)
    # Fit the panel including its border — the box adds its buff on top of
    # the text, so fitting only the text leaves the panel over-wide.
    return fit(VGroup(box, body), width)


def rule_card(lines, size=RULE, color=TERRACOTTA, width=PORTRAIT_SAFE):
    """The big boxed rule — one per Short, and the only terracotta on it."""
    body = VGroup(*[serif(line, size, color) for line in lines])
    body.arrange(DOWN, buff=GAP_SM * 1.2)
    fit(body, width - 0.5)
    box = SurroundingRectangle(body, color=color, buff=GAP_SM * 1.3,
                               stroke_width=3)
    return fit(VGroup(box, body), width)


def series_card(size=SERIES, width=PORTRAIT_SAFE):
    """The card that closes every Short in the series.

    Identical on all five, so the viewer starts recognising it.
    """
    head = VGroup(
        serif("CAMBRIDGE O LEVEL CS", size, GREY),
        serif("PAPER 2", size * 1.5, CHARCOAL),
        serif("STEP-UP", size * 1.9, TERRACOTTA),
    ).arrange(DOWN, buff=GAP_SM)
    steps = VGroup(
        serif("Step · Tear · Establish", size * 0.95, CHARCOAL),
        serif("Preserve · Use · Plan", size * 0.95, CHARCOAL),
    ).arrange(DOWN, buff=GAP_SM * 0.9)
    card = VGroup(head, steps).arrange(DOWN, buff=GAP_MD * 1.6)
    return fit(card, width)


# ------------------------------------------------------- the STEP-UP spine

STEP_UP = [
    ("S", "step through one\ninstruction at a time"),
    ("T", "tear problems\ninto requirements"),
    ("E", "establish\ninitial values"),
    ("P", "preserve values\nuntil changed"),
    ("U", "use intermediate\nresults"),
    ("P", "plan before\nyou code"),
]


class StepUpSpine(VGroup):
    """The six letters, one lit at a time.

    The lecture returns to this whenever a rule is named, so the student
    sees which of the six they are being handed rather than six unrelated
    pieces of advice. Labels are optional: the full form opens and closes
    the lecture, the bare letters flash inline.
    """

    def __init__(self, size=56, width=13.4, labels=False, label_size=MARGIN_SIZE,
                 dim=GREY, lit=TERRACOTTA):
        super().__init__()
        self.dim_color, self.lit_color = dim, lit
        self.letters = VGroup()
        columns = VGroup()
        for letter, meaning in STEP_UP:
            glyph = serif(letter, size, dim)
            self.letters.add(glyph)
            if labels:
                caption = VGroup(*[serif(line, label_size, GREY)
                                   for line in meaning.split("\n")])
                caption.arrange(DOWN, buff=GAP_SM * 0.5)
                columns.add(VGroup(glyph, caption).arrange(DOWN,
                                                           buff=GAP_SM * 1.2))
            else:
                columns.add(glyph)
        if labels:
            # Six labelled columns in one row only fit by scaling the
            # captions under the 28px floor, so they go two rows of three.
            columns.arrange_in_grid(rows=2, buff=(GAP_LG, GAP_MD * 1.3))
        else:
            columns.arrange(RIGHT, buff=GAP_MD * 2.2)
        self.add(columns)
        if self.width > width:
            self.scale_to_fit_width(width)

    def focus(self, index):
        return [glyph.animate.set_color(
            self.lit_color if i == index else self.dim_color)
            for i, glyph in enumerate(self.letters)]

    def dim_all(self):
        return [g.animate.set_color(self.dim_color) for g in self.letters]
