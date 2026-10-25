"""Base class for the A Level 9618 challenge Shorts.

Three Shorts, one format: a hard question, a countdown while the viewer
tries it, the working, then the answer and the trap most students fall
into. The frame, the strap, the countdown and the closing card are the
same on all three, so they live here and each scene is only its content.

Import this module BEFORE anything that reads the frame size: it pins the
portrait frame at import time, the way every Short in this repo does.
"""

from manim import (
    FadeIn,
    FadeOut,
    Transform,
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

from brand import (  # noqa: E402
    CHARCOAL,
    GAP_LG,
    GAP_MD,
    GAP_SM,
    GREY,
    MARGIN_SIZE,
    SLATE,
    TERRACOTTA,
    mono,
    serif,
)
from components.alevel import (  # noqa: E402
    ANSWER,
    CODE,
    COUNT,
    QUESTION,
    answer_card,
    fit,
    hook_lines,
    series_card,
    spec_block,
)
from scenes.base import SATScene  # noqa: E402

LEAD = 30        # a line of narration support
CAPTION = 24     # small explanatory text


class ALevelShort(SATScene):
    """Portrait Short with the series strap, countdown and closing card."""

    strap_text = "A Level CS · 9618"

    def setup(self):
        super().setup()
        self.strap = mono(self.strap_text, MARGIN_SIZE, GREY)
        fit(self.strap)
        self.strap.to_edge(UP, buff=GAP_MD * 0.8)
        self.keep = [self.strap]

    # -------------------------------------------------------------- helpers

    def open_strap(self):
        self.add(self.strap)

    def wipe(self, t, fraction=0.08):
        """Clear everything but the furniture."""
        old = [m for m in self.mobjects if m not in self.keep]
        if old:
            self.play(*[FadeOut(m) for m in old], run_time=t.fill(fraction))

    def lines(self, *texts, size=LEAD, color=CHARCOAL, buff=GAP_SM * 1.1):
        group = VGroup(*[serif(x, size, color) for x in texts])
        group.arrange(DOWN, buff=buff)
        return fit(group)

    def stack(self, *mobjects, buff=GAP_MD):
        return VGroup(*mobjects).arrange(DOWN, buff=buff)

    def under(self, mobject, top, buff=GAP_MD):
        mobject.next_to(top, DOWN, buff=buff)
        return mobject

    def caption(self, text, color=GREY, size=CAPTION):
        return fit(serif(text, size, color))

    def recaption(self, t, holder, text, color=GREY, size=LEAD,
                  fraction=0.25):
        """Swap a running line without moving it."""
        nxt = fit(serif(text, size, color))
        nxt.move_to(holder)
        self.play(Transform(holder, nxt), run_time=t.fill(fraction))
        return holder

    # ------------------------------------------------------------- sections

    def hook(self, t, fraction=0.45, y=1.9):
        """The recurring promise every Short opens on."""
        lines = hook_lines()
        lines.move_to(UP * y)
        self.play(Write(lines), run_time=t.fill(fraction))
        return lines

    def countdown(self, t, start=10, y=-1.0, lit_from=3):
        """A real countdown, because the narration promises ten seconds."""
        digit = serif(str(start), COUNT, SLATE)
        digit.move_to([0, y, 0])
        self.play(FadeIn(digit), run_time=t.fill(0.05))
        share = 0.92 / max(1, start - 1)
        for n in range(start - 1, 0, -1):
            nxt = serif(str(n), COUNT,
                        TERRACOTTA if n <= lit_from else SLATE)
            nxt.move_to(digit)
            self.play(Transform(digit, nxt), run_time=t.fill(share))
        return digit

    def spec(self, t, rows, accent=SLATE, draw=0.14, write=0.4, top=None,
             y=0.4):
        block = spec_block(rows, accent=accent)
        if top is None:
            block.move_to([0, y, 0])
        else:
            block.next_to(top, DOWN, buff=GAP_MD)
        self.play(FadeIn(block[0]), run_time=t.fill(draw))
        self.play(Write(block[1]), run_time=t.fill(write))
        return block

    def reveal_answer(self, t, rows, draw=0.18, write=0.45, y=0.3):
        card = answer_card(rows)
        card.move_to([0, y, 0])
        self.play(FadeIn(card[0]), run_time=t.fill(draw))
        self.play(Write(card[1]), run_time=t.fill(write))
        return card

    def close_series(self, t, fraction=0.3):
        """The card every Short in the series ends on."""
        card = series_card()
        card.move_to(DOWN * 0.2)
        self.play(FadeIn(card), run_time=t.fill(fraction))
        return card
