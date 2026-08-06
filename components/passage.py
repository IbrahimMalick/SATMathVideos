"""PassageHighlight — a wrapped passage with one emphasized word."""

import textwrap

from manim import Text, VGroup

from brand import CHARCOAL, LABEL_SIZE, SERIF_FONT, TERRACOTTA


class PassageHighlight(VGroup):
    def __init__(
        self,
        text,
        highlight=None,
        width=58,
        font_size=LABEL_SIZE,
        color=CHARCOAL,
        highlight_color=TERRACOTTA,
    ):
        super().__init__()
        wrapped = textwrap.fill(text, width)
        if highlight and highlight not in wrapped:
            raise ValueError(
                f"highlight {highlight!r} is split across lines at width "
                f"{width}; pass a width that keeps it on one line"
            )
        t2c = {highlight: highlight_color} if highlight else None
        self.text = Text(
            wrapped, font=SERIF_FONT, font_size=font_size, color=color, t2c=t2c
        )
        self.add(self.text)
