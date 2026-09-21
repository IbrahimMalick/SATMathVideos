"""WordArc — a remembered sequence of words, one lit at a time.

The Saviour of Mankind lecture hangs on seven words the student should
leave holding: Beauty, Brilliance, Breakdown, Cave, Calling, Courage,
Change. The arc returns between scenes, so it needs to look identical
every time and to highlight exactly one step.

    arc = WordArc(SEVEN)
    self.play(Write(arc))
    self.play(*arc.focus(2))        # Breakdown in terracotta, rest grey

One word carries TERRACOTTA at a time, which is also the house rule for
where the eye should go.
"""

from manim import DOWN, RIGHT, VGroup

from brand import GAP_SM, GREY, LABEL_SIZE, TERRACOTTA, serif

FRAME_SAFE = 12.8  # a little inside the 14.22-unit frame


class WordArc(VGroup):
    def __init__(self, words, size=LABEL_SIZE, rows=1, arrow="→",
                 dim=GREY, lit=TERRACOTTA):
        super().__init__()
        self.words = list(words)
        self.dim, self.lit = dim, lit

        self.cells = VGroup()
        chains = []
        per_row = -(-len(self.words) // rows)
        for r in range(rows):
            chunk = self.words[r * per_row:(r + 1) * per_row]
            if not chunk:
                continue
            row = VGroup()
            for i, word in enumerate(chunk):
                if i:
                    row.add(serif(arrow, size, dim))
                cell = serif(word, size, dim)
                row.add(cell)
                self.cells.add(cell)
            row.arrange(RIGHT, buff=GAP_SM * 1.2)
            chains.append(row)
        self.rows = VGroup(*chains).arrange(DOWN, buff=GAP_SM * 1.6)
        if self.rows.width > FRAME_SAFE:
            self.rows.scale_to_fit_width(FRAME_SAFE)
        self.add(self.rows)

    def cell(self, index):
        return self.cells[index]

    def focus(self, index):
        """Animations that light one word and dim the others."""
        moves = []
        for i, cell in enumerate(self.cells):
            target = self.lit if i == index else self.dim
            moves.append(cell.animate.set_color(target))
        return moves

    def dim_all(self):
        return [cell.animate.set_color(self.dim) for cell in self.cells]
