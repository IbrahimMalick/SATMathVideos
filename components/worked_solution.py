"""WorkedSolution — the problem stays put while the working accumulates.

Structurally different from a concept scene, and the difference is the
whole point: a concept scene shows one idea and clears, while a worked
solution keeps the question on screen for a minute or two and grows a
column of working underneath it. The state that needs keeping is where the
next line goes and what to do when the column reaches the bottom of the
frame, so it lives here rather than being re-derived in every scene.

    sol = WorkedSolution(MathTex(r"x^2+x-12"), title="Factorize")
    self.play(Write(sol.header), run_time=t.fill(0.2))
    ...
    line = MathTex(r"x^2+4x-3x-12", font_size=EQUATION_SIZE)
    scroll = sol.place(line)            # positions it, may need a scroll
    if scroll:
        self.play(*scroll, run_time=t.fill(0.1))
    self.play(Write(line), run_time=t.fill(0.4))

A LaTeX expression has to ask for a larger nominal size than Pango text to
render the same height — Computer Modern sets about 1.43x smaller — so
brand.EQUATION_SIZE sits exactly on the 28px mobile floor and nothing here
goes below it.
"""

from manim import (
    DOWN,
    FadeOut,
    LEFT,
    RIGHT,
    SurroundingRectangle,
    UP,
    VGroup,
)

from brand import (
    CHARCOAL,
    EQUATION_SIZE,
    GAP_LG,
    GAP_MD,
    GAP_SM,
    GREY,
    LABEL_SIZE,
    SAGE,
    SLATE,
    TERRACOTTA,
    TITLE_SIZE,
    serif,
)

FRAME_SAFE = 12.6
TOP = 3.05          # where a pinned question sits
FLOOR = -3.25       # the last line may not go below this


def fit(mobject, width=FRAME_SAFE):
    if mobject.width > width:
        mobject.scale_to_fit_width(width)
    return mobject


class WorkedSolution(VGroup):
    """A pinned question with a growing column of working beneath it."""

    def __init__(self, problem, title=None, title_size=TITLE_SIZE,
                 title_color=CHARCOAL, top=TOP, floor=FLOOR,
                 pitch=GAP_MD * 1.15, width=FRAME_SAFE):
        super().__init__()
        self.floor, self.pitch, self.max_width = floor, pitch, width

        self.header = VGroup()
        self.title = None
        if title is not None:
            self.title = fit(serif(title, title_size, title_color), width)
            self.header.add(self.title)
        self.problem = fit(problem, width)
        self.header.add(self.problem)
        self.header.arrange(DOWN, buff=GAP_MD * 0.9)
        self.header.move_to([0, top - self.header.height / 2, 0])

        self.steps = VGroup()
        self.add(self.header, self.steps)

    # ------------------------------------------------------------ layout

    @property
    def _last(self):
        return self.steps[-1] if len(self.steps) else self.header

    def place(self, mobject, buff=None, align=None):
        """Position one line under the working so far.

        Returns the animations needed to make room for it, which is usually
        nothing. When the column has reached the floor the whole stack of
        working slides up by exactly the overflow, so the question stays
        pinned and the newest line is always the lowest one visible.

        A long solution scrolls more than it has room for, and the oldest
        lines would slide up through the question and out of the top of the
        frame. So any line the scroll would push above the question is
        retired on the way past: it fades, instead of leaving over the
        header or off the frame entirely.
        """
        fit(mobject, self.max_width)
        buff = self.pitch if buff is None else buff
        if align is None:
            mobject.next_to(self._last, DOWN, buff=buff)
        else:
            mobject.next_to(self._last, DOWN, buff=buff, aligned_edge=align)
        self.steps.add(mobject)

        overflow = self.floor - mobject.get_bottom()[1]
        if overflow <= 0:
            return []
        # Shift everything already written, and this line with it, so the
        # new line lands exactly on the floor.
        moves = [self.steps.animate.shift(UP * overflow)]
        ceiling = self.header.get_bottom()[1] - GAP_SM * 1.2
        for old_step in self.retired(overflow, ceiling, keep=mobject):
            moves.append(FadeOut(old_step))
        return moves

    def retired(self, overflow, ceiling, keep=None):
        """The lines this scroll would push up past the question."""
        gone = []
        for step in self.steps:
            if step is keep:
                continue
            if step.get_top()[1] + overflow > ceiling:
                gone.append(step)
        return gone

    def clear_steps(self):
        """Forget the working but keep the question. Returns what to fade."""
        old = self.steps
        self.remove(old)
        self.steps = VGroup()
        self.add(self.steps)
        return old

    # ------------------------------------------------------------- parts

    def note(self, text, size=LABEL_SIZE, color=GREY):
        """A plain-language line beside the algebra — why, not what."""
        return fit(serif(text, size, color), self.max_width)


def answer_box(mobject, color=SAGE, buff=GAP_SM * 1.2, stroke=3.5,
               width=FRAME_SAFE):
    """The final answer, boxed. One per solution, and the only box on it."""
    fit(mobject, width - 0.6)
    box = SurroundingRectangle(mobject, color=color, buff=buff,
                               stroke_width=stroke)
    return fit(VGroup(box, mobject), width)


def mcq_card(stem, choices, stem_size=EQUATION_SIZE, choice_size=LABEL_SIZE,
             top=TOP, width=FRAME_SAFE):
    """A model-paper multiple choice: the stem, then A to D beneath it.

    ``stem`` may be a string or a ready-made mobject (a MathTex, usually),
    and so may each choice — the paper mixes prose options with algebraic
    ones and both have to sit in the same column.
    """
    from components.answer_choices import AnswerChoices

    head = stem if not isinstance(stem, str) else serif(stem, stem_size,
                                                        CHARCOAL)
    fit(head, width)
    rows = AnswerChoices(choices, font_size=choice_size)
    fit(rows, width)
    card = VGroup(head, rows).arrange(DOWN, buff=GAP_LG * 0.9)
    card.move_to([0, top - card.height / 2, 0])
    return card, head, rows


def label_pair(left, right, left_color=GREY, right_color=CHARCOAL,
               size=LABEL_SIZE, gap=GAP_MD):
    """'product: -12' style — a named quantity and its value, side by side."""
    a = serif(left, size, left_color)
    b = right if not isinstance(right, str) else serif(right, size,
                                                       right_color)
    return VGroup(a, b).arrange(RIGHT, buff=gap)


def subset_grid(subsets, size=LABEL_SIZE, color=CHARCOAL, row_buff=GAP_MD,
                col_buff=GAP_MD * 1.1, width=FRAME_SAFE):
    """Subsets laid out one row per size — the shape of a power set.

    Grouped by size because that is how the count is argued: one empty
    set, four singletons, six pairs, four triples, one full set. The rows
    are the argument, not decoration.
    """
    rows = VGroup()
    for group in subsets:
        row = VGroup(*[serif(s, size, color) for s in group])
        row.arrange(RIGHT, buff=col_buff)
        fit(row, width)
        rows.add(row)
    rows.arrange(DOWN, buff=row_buff)
    return fit(rows, width)
