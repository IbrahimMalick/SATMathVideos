"""VocabCard — one word, its meaning, and optionally the weak version of it.

The English lectures teach vocabulary by contrast: an ordinary sentence
against the precise one. The card keeps that shape consistent so the
student learns to expect it.

    card = VocabCard(
        "unparalleled",
        "so outstanding that nothing is quite equal to it",
        weak='"He was a good speaker."',
        strong='"His eloquence was unparalleled."',
    )
    self.play(Write(card.word))
    self.play(Write(card.meaning))
    self.play(Write(card.contrast))
"""

from manim import DOWN, VGroup

from brand import (
    BODY_SIZE,
    GAP_MD,
    GAP_SM,
    GREY,
    LABEL_SIZE,
    SAGE,
    TITLE_SIZE,
    serif,
)

FRAME_SAFE = 12.8


def _fit(mobject, width=FRAME_SAFE):
    if mobject.width > width:
        mobject.scale_to_fit_width(width)
    return mobject


class VocabCard(VGroup):
    def __init__(self, word, meaning, weak=None, strong=None,
                 word_size=TITLE_SIZE * 1.2, meaning_size=BODY_SIZE):
        super().__init__()
        self.word = _fit(serif(word, word_size))
        self.meaning = _fit(serif(meaning, meaning_size, GREY))
        self.meaning.next_to(self.word, DOWN, buff=GAP_MD * 1.2)
        self.add(self.word, self.meaning)

        self.contrast = None
        if weak or strong:
            lines = VGroup()
            if weak:
                lines.add(_fit(serif(weak, LABEL_SIZE, GREY)))
            if strong:
                lines.add(_fit(serif(strong, LABEL_SIZE, SAGE)))
            lines.arrange(DOWN, buff=GAP_SM * 1.3)
            lines.next_to(self.meaning, DOWN, buff=GAP_MD * 1.3)
            self.contrast = lines
            self.add(lines)
