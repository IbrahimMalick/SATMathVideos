"""Base class for the five STEP-UP Paper 2 Shorts.

Each Short is a different lesson, but the frame, the strap line, the way a
screen is cleared and the closing series card are the same on all five.
Putting them here keeps the individual scenes down to their actual content.

Import this module BEFORE anything that reads the frame size: it pins the
portrait frame at import time, the way every Short in this repo does.
"""

from manim import (
    FadeIn,
    FadeOut,
    VGroup,
    Write,
    DOWN,
    UP,
    config,
)

# Portrait: manim keeps frame_width fixed by default, which would make the
# frame 25 units tall. Pin the intended 4.5 x 8 frame instead.
config.frame_height = 8.0
config.frame_width = 4.5

from brand import CHARCOAL, GAP_MD, GAP_SM, GREY, MARGIN_SIZE, TERRACOTTA, mono, serif
from components.stepup import fit, series_card
from scenes.base import SATScene

STRAP = MARGIN_SIZE      # the running series label
HOOK = 40                # the opening promise
LEAD = 36                # a line of narration support
CAPTION = 30             # small explanatory text
ANSWER = 56              # the number or word being revealed


class StepUpShort(SATScene):
    """Portrait Short with the series strap and closing card."""

    strap_text = "O Level CS · Paper 2"

    def setup(self):
        super().setup()
        self.strap = mono(self.strap_text, STRAP, GREY)
        fit(self.strap)
        self.strap.to_edge(UP, buff=GAP_MD * 0.9)
        self.keep = [self.strap]

    # -------------------------------------------------------------- helpers

    def open_strap(self):
        self.add(self.strap)

    def wipe(self, t, fraction=0.07):
        """Clear everything but the furniture."""
        old = [m for m in self.mobjects if m not in self.keep]
        if old:
            self.play(*[FadeOut(m) for m in old], run_time=t.fill(fraction))

    def show(self, t, mobject, fraction=0.2, how=Write):
        self.play(how(mobject), run_time=t.fill(fraction))
        return mobject

    def stack(self, *mobjects, buff=GAP_MD):
        return VGroup(*mobjects).arrange(DOWN, buff=buff)

    def lines(self, *texts, size=LEAD, color=CHARCOAL, buff=GAP_SM * 1.2):
        group = VGroup(*[serif(t, size, color) for t in texts])
        group.arrange(DOWN, buff=buff)
        return fit(group)

    def close_series(self, t, fraction=0.18):
        """The card every Short in the series ends on."""
        card = series_card()
        card.move_to(DOWN * 0.2)
        self.play(FadeIn(card), run_time=t.fill(fraction))
        return card
