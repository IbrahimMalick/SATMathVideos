"""BitRow — eight bits with their place values above, drawn as the syllabus draws them.

Nearly every number-systems question in 2210 Paper 1 is answered by writing
the place values over the bits and adding the active columns, so that
picture is the component rather than something each scene rebuilds.

    row = BitRow("10110110")
    self.play(Write(row.places), Write(row.bits))
    self.play(*row.light())              # the columns that contribute
    self.play(Write(row.sum_line()))     # 128 + 32 + 16 + 4 + 2 = 182

Two's complement is the same picture with one changed label, which is the
whole point of the topic — so `signed=True` only flips the leading place
value to -128 and the arithmetic follows.
"""

from manim import DOWN, UP, VGroup

from brand import (
    CHARCOAL,
    GAP_SM,
    GREY,
    LABEL_SIZE,
    SLATE,
    TERRACOTTA,
    serif,
)

PLACES_8 = [128, 64, 32, 16, 8, 4, 2, 1]


class BitRow(VGroup):
    def __init__(self, bits, size=LABEL_SIZE, cell=1.15, signed=False,
                 lit=TERRACOTTA, dim=CHARCOAL, place_color=GREY,
                 width=None, show_places=True):
        super().__init__()
        self.lit_color, self.dim_color = lit, dim
        self.pattern = str(bits).replace(" ", "")
        self.signed = signed

        values = list(PLACES_8[:len(self.pattern)])
        if signed:
            values[0] = -values[0]
        self.values = values

        self.bits = VGroup(*[serif(b, size, dim) for b in self.pattern])
        self.places = VGroup(*[serif(str(v), size, place_color)
                               for v in values])
        for i, (bit, place) in enumerate(zip(self.bits, self.places)):
            x = (i - (len(self.pattern) - 1) / 2) * cell
            place.move_to([x, 0, 0])
            bit.move_to([x, 0, 0])
        self.places.shift(UP * GAP_SM * 1.6)
        self.bits.shift(DOWN * GAP_SM * 1.6)

        if show_places:
            self.add(self.places)
        self.add(self.bits)
        if width and self.width > width:
            self.scale_to_fit_width(width)

    # ------------------------------------------------------------ queries

    @property
    def active(self):
        """Indices of the bits set to 1 — the columns that contribute."""
        return [i for i, b in enumerate(self.pattern) if b == "1"]

    @property
    def total(self):
        return sum(self.values[i] for i in self.active)

    def terms(self):
        """The place values that are actually added up, in column order."""
        return [self.values[i] for i in self.active]

    # --------------------------------------------------------- animations

    def light(self, indices=None, color=None):
        """Colour the contributing columns; the zero columns stay quiet."""
        indices = self.active if indices is None else indices
        color = color or self.lit_color
        moves = []
        for i in indices:
            moves.append(self.bits[i].animate.set_color(color))
            if self.places in self.submobjects:
                moves.append(self.places[i].animate.set_color(color))
        return moves

    def dim_all(self):
        moves = [bit.animate.set_color(self.dim_color) for bit in self.bits]
        if self.places in self.submobjects:
            moves += [p.animate.set_color(GREY) for p in self.places]
        return moves

    def sum_line(self, size=LABEL_SIZE, color=CHARCOAL, result=True):
        """'128 + 32 + 16 + 4 + 2 = 182', built from the bits themselves.

        Derived rather than passed in, so the line on screen cannot drift
        from the pattern above it.
        """
        terms = self.terms()
        if not terms:
            text = "0"
        else:
            # A leading -128 reads as "-128 + 64", not "+ -128 + 64".
            text = str(terms[0]) + "".join(f" + {t}" for t in terms[1:])
        if result:
            text += f" = {self.total}"
        return serif(text, size, color)


def bit_label(text, size=LABEL_SIZE, color=SLATE):
    """A caption that sits under a BitRow without fighting it for weight."""
    return serif(text, size, color)
