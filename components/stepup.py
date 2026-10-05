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

from manim import DOWN, LEFT, SurroundingRectangle, VGroup

from brand import (
    CHARCOAL,
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
