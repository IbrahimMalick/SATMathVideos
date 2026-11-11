"""The shape of an exam, drawn: how a paper splits, and where its marks sit.

Two figures that keep coming back in exam-strategy lectures, parameterised
so a different board or paper is different numbers rather than a different
drawing.

``SectionSplit`` is a single bar cut in proportion to the sections' weight.
A student who is told "fifty-five percent and forty-five percent" hears two
numbers; one who sees the bar sees that the two halves are nearly equal and
that the shorter one is worth almost as much per minute.

``WeightBars`` puts each topic's mark range on a shared scale. The exam
board publishes ranges, not points, so the figure draws ranges: a bar that
starts at ten and ends at eighteen says something a single number cannot,
which is that the paper is allowed to vary.

Sized for the 16:9 lecture frame at scale 1.0, because a figure scaled to
fit takes its labels with it and a 28px caption inside a group scaled to
0.9 renders at 25px. ``measure()`` checks the sizing still holds.
"""

from manim import (
    Line,
    Rectangle,
    VGroup,
    DOWN,
    LEFT,
    RIGHT,
    UP,
)

from brand import (
    CHARCOAL,
    GAP_MD,
    GAP_SM,
    GREY,
    LABEL_SIZE,
    MARGIN_SIZE,
    SLATE,
    TERRACOTTA,
    serif,
)

FRAME_SAFE = 12.6


def fit(mobject, width=FRAME_SAFE):
    if mobject.width > width:
        mobject.scale_to_fit_width(width)
    return mobject


class SectionSplit(VGroup):
    """One bar, cut in proportion to what each section is worth.

    ``parts`` is a list of (name, detail, weight). The weights set the
    widths, so the picture cannot disagree with the percentages printed on
    it: both come from the same numbers.
    """

    def __init__(self, parts, width=11.0, height=1.05, size=LABEL_SIZE,
                 color=SLATE, text_color=CHARCOAL, fills=(0.18, 0.08)):
        super().__init__()
        total = sum(weight for _, _, weight in parts)
        self.blocks, self.captions = VGroup(), VGroup()

        left = -width / 2
        for index, (name, detail, weight) in enumerate(parts):
            span = width * weight / total
            block = Rectangle(width=span, height=height, color=color,
                              stroke_width=2.5)
            block.set_fill(color, opacity=fills[index % len(fills)])
            block.move_to([left + span / 2, 0, 0])

            share = serif(f"{round(weight)}%", size * 1.25, text_color)
            share.move_to(block)

            # A caption is held to the width of the block it belongs to, or
            # it reaches into the next section's caption. That means the
            # narrow block decides the wording: ``detail`` takes newlines
            # so a long caption breaks into lines instead of being shrunk
            # under the legibility floor.
            caption = VGroup(serif(name, size * 0.9, text_color))
            for piece in str(detail).split("\n"):
                caption.add(serif(piece, MARGIN_SIZE, GREY))
            caption.arrange(DOWN, buff=GAP_SM * 0.45)
            caption.next_to(block, DOWN, buff=GAP_SM * 1.2)
            if caption.width > span - 0.1:
                raise ValueError(
                    f"Section '{name}' has a caption {caption.width:.2f} "
                    f"units wide under a block only {span:.2f} wide. "
                    "Break the detail over more lines rather than letting "
                    "it shrink."
                )

            self.blocks.add(VGroup(block, share))
            self.captions.add(caption)
            left += span

        self.add(self.blocks, self.captions)


class WeightBars(VGroup):
    """Each topic's mark range on one scale, label above its own bar.

    The label sits above rather than beside because a unit's full name runs
    wider than any sensible left-hand column, and shrinking it to fit a
    column is how a label ends up under the legibility floor.
    """

    def __init__(self, rows, top=40, track=10.5, pitch=0.86, size=LABEL_SIZE,
                 color=SLATE, lit=TERRACOTTA, rail=GREY, bar_height=0.26,
                 highlight=None):
        super().__init__()
        self.top = top
        self.track = track
        self.bars, self.labels, self.ranges = VGroup(), VGroup(), VGroup()
        left = -track / 2

        body = VGroup()
        for index, (name, low, high) in enumerate(rows):
            accent = lit if index == highlight else color

            label = serif(name, size, CHARCOAL)
            rail_line = Line([left, 0, 0], [left + track, 0, 0],
                             color=rail, stroke_width=2)
            bar = Rectangle(width=track * (high - low) / top,
                            height=bar_height, color=accent, stroke_width=2)
            bar.set_fill(accent, opacity=0.25)
            bar.move_to([left + track * (low + high) / (2 * top), 0, 0])

            span = serif(f"{low}–{high}%", MARGIN_SIZE,
                         accent if index == highlight else GREY)
            span.next_to(rail_line, RIGHT, buff=GAP_SM * 0.9)

            row = VGroup(rail_line, bar, span)
            label.next_to(row, UP, buff=GAP_SM * 0.55)
            label.align_to(rail_line, LEFT)

            self.bars.add(bar)
            self.labels.add(label)
            self.ranges.add(span)
            body.add(VGroup(label, row))

        body.arrange(DOWN, buff=pitch - bar_height, aligned_edge=LEFT)
        self.add(body)

    def row(self, index):
        return VGroup(self.labels[index], self.bars[index], self.ranges[index])

    def light(self, index, color=TERRACOTTA):
        return [self.bars[index].animate.set_color(color).set_fill(
            color, opacity=0.25),
            self.ranges[index].animate.set_color(color)]

    def settle(self, index, color=SLATE):
        return [self.bars[index].animate.set_color(color).set_fill(
            color, opacity=0.25),
            self.ranges[index].animate.set_color(GREY)]


def chip_row(tokens, size=MARGIN_SIZE, color=CHARCOAL, accent=GREY,
             gap=GAP_MD * 0.8, width=FRAME_SAFE, rows=2):
    """Short terms laid out as a block — the things to watch for.

    Wrapped over rows rather than run across one line, because a single
    line of eight terms across this frame shrinks every one of them.
    """
    chips = [serif(token, size, color) for token in tokens]
    per_row = -(-len(chips) // rows)
    lines = VGroup()
    for start in range(0, len(chips), per_row):
        line = VGroup(*chips[start:start + per_row])
        line.arrange(RIGHT, buff=gap)
        lines.add(line)
    lines.arrange(DOWN, buff=GAP_SM * 1.3)
    return fit(lines, width)


def measure():
    """Check both figures sit in the frame with their labels at full size.

    Run as ``python -m components.exam_shape`` from the repo root.
    """
    from manim import config

    half_w, half_h = config.frame_width / 2, config.frame_height / 2
    split = SectionSplit([
        ("Section I", "42 questions · 90 min", 55),
        ("Section II", "4 questions · 90 min", 45),
    ])
    bars = WeightBars([
        ("Unit 1: Using Objects and Methods", 15, 25),
        ("Unit 2: Selection and Iteration", 25, 35),
        ("Unit 3: Class Creation", 10, 18),
        ("Unit 4: Data Collections", 30, 40),
    ], highlight=3)

    for name, group in (("split", split), ("bars", bars)):
        left, right = group.get_left()[0], group.get_right()[0]
        bottom, top = group.get_bottom()[1], group.get_top()[1]
        ok = (left > -half_w and right < half_w
              and bottom > -half_h and top < half_h)
        print(f"{name:6} x [{left:6.2f}, {right:6.2f}]  "
              f"y [{bottom:6.2f}, {top:6.2f}]  size {group.width:.2f} x "
              f"{group.height:.2f}  {'ok' if ok else 'OFF FRAME'}")

    # A caption squeezed under a narrow block is the first thing to drop
    # below the floor, and the narrower block is the one to check.
    for index, caption in enumerate(split.captions):
        scale = caption[1].font_size
        print(f"split caption {index}: narrowest text renders at "
              f"{scale:.1f} nominal  "
              f"{'ok' if scale >= 28 else 'BELOW THE 28px FLOOR'}")

    # Bars must not collide with the row above, and the range label must
    # stay inside the frame.
    for index in range(len(bars.bars) - 1):
        gap = (bars.bars[index].get_bottom()[1]
               - bars.labels[index + 1].get_top()[1])
        print(f"row {index} to label {index + 1}: {gap:5.2f}  "
              f"{'ok' if gap > 0.05 else 'ROWS COLLIDE'}")
    widest = max(bars.ranges, key=lambda r: r.get_right()[0])
    print(f"range labels end at {widest.get_right()[0]:.2f}  "
          f"{'ok' if widest.get_right()[0] < half_w else 'OFF FRAME'}")


if __name__ == "__main__":
    measure()
