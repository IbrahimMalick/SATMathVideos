"""AnswerChoices — A to D, strikethrough elimination, sage confirmation.

The component holds the mobjects and returns animations; the scene decides
when to play them (inside beats) and with what run_time.
"""

from manim import Create, Line, VGroup, DOWN, LEFT

from brand import CHARCOAL, GAP_SM, GREY, LABEL_SIZE, SAGE, serif

LETTERS = "ABCD"


class AnswerChoices(VGroup):
    def __init__(self, choices, font_size=LABEL_SIZE):
        super().__init__()
        self.rows = {}
        for letter, text in zip(LETTERS, choices):
            row = serif(f"{letter}.  {text}", font_size)
            self.rows[letter] = row
            self.add(row)
        self.arrange(DOWN, buff=GAP_SM * 1.4, aligned_edge=LEFT)

    def eliminate(self, letter):
        """Grey the row and strike through it. Returns animations."""
        row = self.rows[letter]
        strike = Line(
            row.get_left() + LEFT * 0.1,
            row.get_right() - LEFT * 0.1,
            color=GREY,
            stroke_width=3,
        )
        return [row.animate.set_color(GREY), Create(strike)]

    def confirm(self, letter):
        """Mark the row as the correct answer. Returns animations."""
        return [self.rows[letter].animate.set_color(SAGE)]

    def reset_color(self, letter, color=CHARCOAL):
        return [self.rows[letter].animate.set_color(color)]
