"""What an operating system is, drawn: the sort, the stack, the nine jobs.

Cambridge O Level 2210 topic 4.1 is taught almost entirely as lists — two
categories of software, nine functions of an operating system, six things a
peripheral might be. A list read aloud is a list forgotten, so each one here
becomes a shape the student can picture when the question comes.

Five figures, each parameterised so a different board or chapter is
different strings rather than a different drawing:

  * ``SortBench``   two bins and the rule that decides which bin a thing
                    goes in. The whole of part one is this one picture.
  * ``FunctionList`` the nine syllabus functions as a numbered column, one
                    lit at a time. The order is the syllabus's own.
  * ``LayerStack``  application, operating system, driver, hardware: the
                    path a request takes, with the arrows that say why the
                    application never talks to the printer itself.
  * ``MemoryBar``   RAM as a bar that fills, with a second bar for the
                    secondary storage virtual memory borrows from.
  * ``TimeSlices``  one core, three processes, and the hop between them
                    that multitasking actually is.

Sized for the 14.22 x 8 landscape frame at scale 1.0. Nothing here is built
to be scaled down by the scene: a figure scaled to 0.9 takes its 28px
labels to 25px, which fails the mobile legibility gate for a saving nobody
asked for. Where a label will not fit, these raise rather than shrink, so
the fix is a shorter label and not a quietly illegible frame.

``measure()`` renders every figure's extents and label sizes; run it as
``python -m components.os_shape`` from the repo root after any change here.
"""

import textwrap

from manim import (
    Arrow,
    Dot,
    Line,
    Rectangle,
    VGroup,
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
)

from brand import (
    CHARCOAL,
    CREAM,
    GAP_LG,
    GAP_MD,
    GAP_SM,
    GREY,
    LABEL_SIZE,
    MARGIN_SIZE,
    SAGE,
    SLATE,
    TERRACOTTA,
    mono,
    serif,
)

FRAME_SAFE = 12.6

# The nine functions, in the order and the wording of the 2210 syllabus for
# examination in 2026, 2027 and 2028 (topic 4.1, "Describe the role and
# basic functions of an operating system"). The lecture covers them in a
# different order; the list stays in the syllabus's, because this is the
# list the student is being asked to reproduce.
OS_FUNCTIONS = [
    "managing files",
    "handling interrupts",
    "providing an interface",
    "managing peripherals and drivers",
    "managing memory",
    "managing multitasking",
    "providing a platform for running applications",
    "providing system security",
    "managing user accounts",
]


# Letters that reach below the baseline. A word made only of x-height
# letters has a shorter ink box than its neighbours, and arrange(RIGHT)
# lines up centres, so "menus" floats above "windows" beside it.
DESCENDER_CHARS = set("gjpqy,;()[]{}/\\@")


def align_baselines(items, tokens, size):
    """Sit a row of words on one line rather than on one centre.

    Manim exposes no baseline, but a word's ink bottom IS its baseline
    unless the word contains a descender, and the depth of a descender is
    measurable: the height of "xp" less the height of "x".
    """
    drop = serif("xp", size).height - serif("x", size).height

    def baseline(item, token):
        return item.get_bottom()[1] + (
            drop if set(token) & DESCENDER_CHARS else 0.0)

    anchor = baseline(items[0], tokens[0])
    for item, token in zip(items, tokens):
        item.shift(UP * (anchor - baseline(item, token)))
    return items


def wrapped(text, size=LABEL_SIZE, color=CHARCOAL, width=FRAME_SAFE):
    """A line that breaks to fit rather than shrinking to fit."""
    body = serif(text, size, color)
    if body.width <= width:
        return body
    budget = max(8, int(len(text) * width / body.width))
    while budget >= 8:
        body = serif(textwrap.fill(text, budget), size, color)
        if body.width <= width:
            return body
        budget -= 1
    raise ValueError(
        f"{text!r} will not fit {width:.2f} units at size {size} however it "
        "is wrapped. Shorten it rather than letting it shrink."
    )


class SortBench(VGroup):
    """Two bins, their defining rule, and the things that go in them.

    Items are added one at a time, because the lecture adds them one at a
    time: the bench is a running record of a sort in progress, not a
    finished table revealed at once.
    """

    def __init__(self, left_name, right_name, width=12.6, gap=GAP_MD,
                 size=LABEL_SIZE, head_size=LABEL_SIZE):
        super().__init__()
        self.span = (width - gap) / 2
        self.size = size

        self.heads, self.rules, self.captions, self.columns = (
            VGroup(), VGroup(), VGroup(), VGroup())
        self.items = [VGroup(), VGroup()]
        self._anchor = []

        for index, name in enumerate((left_name, right_name)):
            centre = (index - 0.5) * (self.span + gap)
            head = serif(name, head_size, CHARCOAL)
            if head.width > self.span:
                raise ValueError(
                    f"Bin heading {name!r} is {head.width:.2f} units wide in "
                    f"a column only {self.span:.2f} wide."
                )
            head.move_to([centre, 0, 0])
            rule = Line([centre - self.span / 2, 0, 0],
                        [centre + self.span / 2, 0, 0],
                        color=GREY, stroke_width=2)
            rule.next_to(head, DOWN, buff=GAP_SM * 0.8)

            self.heads.add(head)
            self.rules.add(rule)
            self._anchor.append(rule)
            self.columns.add(VGroup(head, rule))

        self.add(self.heads, self.rules)

    def caption(self, side, text, color=GREY, size=MARGIN_SIZE):
        """The rule that decides this bin, under its heading."""
        body = wrapped(text, size, color, self.span)
        body.next_to(self._anchor[side], DOWN, buff=GAP_SM)
        self.captions.add(body)
        self.add(body)
        self._anchor[side] = body
        return body

    def item(self, side, text, color=CHARCOAL, size=None):
        """One more thing in this bin, under whatever is already there."""
        size = self.size if size is None else size
        body = serif(text, size, color)
        if body.width > self.span:
            raise ValueError(
                f"Item {text!r} is {body.width:.2f} units wide in a column "
                f"only {self.span:.2f} wide. Shorten it."
            )
        body.next_to(self._anchor[side], DOWN, buff=GAP_SM * 0.85)
        # next_to centres on whatever was above, which for a column of
        # different-length items walks the left edge about. Re-centre every
        # item on the bin's own axis instead.
        body.move_to([self.heads[side].get_center()[0],
                      body.get_center()[1], 0])
        self.items[side].add(body)
        self.add(body)
        self._anchor[side] = body
        return body

    def bottom(self):
        """The lowest point anything currently reaches."""
        return min(group.get_bottom()[1] for group in self._anchor)


class FunctionList(VGroup):
    """The nine functions as a numbered column, one lit at a time.

    Numbered because the strip along the bottom of the frame uses the same
    numbers: the student can look down at cell seven and look back up to
    find out what seven was.
    """

    def __init__(self, functions=None, size=LABEL_SIZE, width=FRAME_SAFE,
                 color=CHARCOAL, number_color=GREY, lit=TERRACOTTA):
        super().__init__()
        self.lit_color, self.rest_color, self.number_color = (
            lit, color, number_color)
        functions = OS_FUNCTIONS if functions is None else functions

        self.numbers, self.labels, self.rows = VGroup(), VGroup(), VGroup()
        for index, name in enumerate(functions):
            number = serif(f"{index + 1}", size, number_color)
            label = serif(name, size, color)
            row = VGroup(number, label).arrange(RIGHT, buff=GAP_SM * 1.4)
            align_baselines([number, label], [str(index + 1), name], size)
            self.numbers.add(number)
            self.labels.add(label)
            self.rows.add(row)

        # Hanging indent: the numbers share a column and the labels share a
        # column, so a one-digit list reads as a list and not as a ragged
        # left edge.
        left = min(row.get_left()[0] for row in self.rows)
        for row in self.rows:
            row.shift(RIGHT * (left - row.get_left()[0]))
        widest = max(number.width for number in self.numbers)
        for number, label in zip(self.numbers, self.labels):
            label.move_to([left + widest + GAP_SM * 1.4,
                           label.get_center()[1], 0], aligned_edge=LEFT)

        self.rows.arrange(DOWN, buff=GAP_SM * 0.75, aligned_edge=LEFT)
        self.add(self.rows)
        if self.width > width:
            raise ValueError(
                f"The function list is {self.width:.2f} units wide at size "
                f"{size}, over the {width:.2f} the frame allows."
            )

    def focus(self, index, lit=None):
        """Light one function and send the rest back to grey."""
        lit = self.lit_color if lit is None else lit
        moves = []
        for i, (number, label) in enumerate(zip(self.numbers, self.labels)):
            on = i == index
            moves.append(label.animate.set_color(
                lit if on else self.rest_color))
            moves.append(number.animate.set_color(
                lit if on else self.number_color))
        return moves

    def dim_all(self):
        return [m.animate.set_color(self.number_color)
                for m in [*self.labels, *self.numbers]]


class LayerStack(VGroup):
    """Boxes stacked with arrows between: who asks whom, in order.

    The arrows point down by default because the lecture reads the path
    downward — the application asks, the hardware finally acts.
    """

    def __init__(self, layers, width=7.2, height=0.82, gap=0.56,
                 size=LABEL_SIZE, color=SLATE, text_color=CHARCOAL,
                 fill=0.1):
        super().__init__()
        self.boxes, self.labels, self.arrows = VGroup(), VGroup(), VGroup()

        for name in layers:
            box = Rectangle(width=width, height=height, color=color,
                            stroke_width=2.5)
            box.set_fill(color, opacity=fill)
            label = serif(name, size, text_color)
            if label.width > width - GAP_MD:
                raise ValueError(
                    f"Layer {name!r} is {label.width:.2f} units wide in a "
                    f"box only {width:.2f} wide. Shorten it."
                )
            label.move_to(box)
            self.boxes.add(box)
            self.labels.add(label)
            self.add(VGroup(box, label))

        self.boxes.arrange(DOWN, buff=gap)
        for box, label in zip(self.boxes, self.labels):
            label.move_to(box)

        for upper, lower in zip(self.boxes, self.boxes[1:]):
            # The head is sized as a fraction of the shaft, so a tight
            # gap makes an arrow with no visible point. Both numbers here
            # are set for a gap of about half a unit; narrow the gap and
            # the arrow stops reading as an arrow.
            arrow = Arrow(upper.get_bottom(), lower.get_top(),
                          color=GREY, stroke_width=4.5,
                          buff=0.04, max_tip_length_to_length_ratio=0.5)
            self.arrows.add(arrow)
        self.add(self.arrows)

    def light(self, index, color=TERRACOTTA):
        return [self.boxes[index].animate.set_stroke(color)
                .set_fill(color, opacity=0.14),
                self.labels[index].animate.set_color(color)]

    def settle(self, index, color=SLATE):
        return [self.boxes[index].animate.set_stroke(color)
                .set_fill(color, opacity=0.1),
                self.labels[index].animate.set_color(CHARCOAL)]


class MemoryBar(VGroup):
    """RAM as a bar that fills, and the disk that stands in when it cannot.

    ``allocate`` returns the block rather than adding it to the scene, so
    the caller decides which beat each allocation lands on.
    """

    def __init__(self, width=8.4, height=1.0, size=MARGIN_SIZE,
                 label="RAM", color=SLATE, free=GREY):
        super().__init__()
        self.width_units, self.height_units = width, height
        self.size, self.color = size, color
        self.used = 0.0

        self.frame = Rectangle(width=width, height=height, color=CHARCOAL,
                               stroke_width=2.5)
        self.name = serif(label, size, GREY)
        self.name.next_to(self.frame, UP, buff=GAP_SM * 0.7)
        self.name.align_to(self.frame, LEFT)
        self.blocks, self.block_labels = VGroup(), VGroup()
        self.add(self.frame, self.name)

    def allocate(self, text, fraction, color=None):
        """A block taking ``fraction`` of the whole bar, left to right."""
        color = self.color if color is None else color
        if self.used + fraction > 1.0001:
            raise ValueError(
                f"Allocating {fraction:.2f} of RAM to {text!r} takes the bar "
                f"past full ({self.used:.2f} already used)."
            )
        span = self.width_units * fraction
        block = Rectangle(width=span, height=self.height_units,
                          color=color, stroke_width=2)
        block.set_fill(color, opacity=0.22)
        block.move_to([self.frame.get_left()[0]
                       + self.width_units * self.used + span / 2,
                       self.frame.get_center()[1], 0])
        label = serif(text, self.size, CHARCOAL)
        if label.width > span - 0.12:
            label.next_to(block, DOWN, buff=GAP_SM * 0.6)
        else:
            label.move_to(block)
        self.used += fraction
        self.blocks.add(block)
        self.block_labels.add(label)
        return VGroup(block, label)

    def spare(self, text="free", color=GREY):
        """Whatever is left of the bar, marked as free."""
        return self.allocate(text, max(0.0, 1.0 - self.used), color)


class TimeSlices(VGroup):
    """One core, several processes, and the hop between them over time.

    Each process gets a lane; the slices show which one holds the processor
    in each instant. The point the picture has to make is that no two
    slices ever overlap in time — that is the whole difference between
    "appears to run at the same time" and "runs at the same time".
    """

    def __init__(self, processes, order, width=9.0, lane=0.52, gap=0.22,
                 size=MARGIN_SIZE, color=SLATE, lit=TERRACOTTA,
                 rail=GREY, label_gap=GAP_MD):
        super().__init__()
        self.slices, self.lanes, self.labels = VGroup(), VGroup(), VGroup()
        slot = width / len(order)

        names = VGroup(*[serif(name, size, CHARCOAL) for name in processes])
        names.arrange(DOWN, buff=gap + lane - 0.0, aligned_edge=RIGHT)
        widest = max(name.width for name in names)

        left = -width / 2 + widest / 2 + label_gap / 2
        for index, name in enumerate(names):
            y = (len(processes) - 1 - index) * (lane + gap)
            name.move_to([left - widest / 2 - label_gap, y, 0],
                         aligned_edge=RIGHT)
            track = Line([left, y - lane / 2 - 0.02, 0],
                         [left + width, y - lane / 2 - 0.02, 0],
                         color=rail, stroke_width=1.5)
            self.labels.add(name)
            self.lanes.add(track)
            self.add(name, track)

        for step, which in enumerate(order):
            y = (len(processes) - 1 - which) * (lane + gap)
            block = Rectangle(width=slot * 0.9, height=lane, color=color,
                              stroke_width=1.5)
            block.set_fill(color, opacity=0.3)
            block.move_to([left + slot * (step + 0.5), y, 0])
            self.slices.add(block)
            self.add(block)

        self.axis = Arrow([left, -lane / 2 - gap - 0.3, 0],
                          [left + width, -lane / 2 - gap - 0.3, 0],
                          color=rail, stroke_width=3, buff=0,
                          max_tip_length_to_length_ratio=0.03)
        self.time = serif("time", size, GREY)
        self.time.next_to(self.axis, DOWN, buff=GAP_SM * 0.6)
        self.time.move_to([left + width / 2, self.time.get_center()[1], 0])
        self.add(self.axis, self.time)
        self.lit_color = lit

    def light(self, step, color=None):
        color = self.lit_color if color is None else color
        return [self.slices[step].animate.set_stroke(color)
                .set_fill(color, opacity=0.45)]


def chips(tokens, size=LABEL_SIZE, color=CHARCOAL, gap=GAP_MD,
          width=FRAME_SAFE, rows=2):
    """Short terms as a block of lines, not one long run across the frame.

    Returns the group and the individual chips, so a scene can reveal them
    one at a time without taking the group apart again.
    """
    made = [serif(token, size, color) for token in tokens]
    per_row = -(-len(made) // rows)
    lines = VGroup()
    for start in range(0, len(made), per_row):
        members = made[start:start + per_row]
        line = VGroup(*members)
        line.arrange(RIGHT, buff=gap)
        align_baselines(members, tokens[start:start + per_row], size)
        lines.add(line)
    lines.arrange(DOWN, buff=GAP_SM * 1.4)
    if lines.width > width:
        raise ValueError(
            f"A row of {tokens!r} is {lines.width:.2f} units wide at size "
            f"{size}, over the {width:.2f} the frame allows. Use more rows."
        )
    return lines, made


def grid(tokens, columns=2, size=MARGIN_SIZE, color=CHARCOAL,
         h_gap=GAP_LG * 0.9, v_gap=GAP_SM * 1.5, width=FRAME_SAFE):
    """Short terms in aligned columns, not rows each centred on their own.

    ``chips`` centres every row independently, which is right for two or
    three words and wrong for six: the left edges wander and the block
    reads as scattered. Here every column shares a left edge.
    """
    made = [serif(token, size, color) for token in tokens]
    rows = -(-len(made) // columns)
    spans = []
    for column in range(columns):
        members = [made[row * columns + column] for row in range(rows)
                   if row * columns + column < len(made)]
        spans.append(max(m.width for m in members) if members else 0.0)

    total = sum(spans) + h_gap * (columns - 1)
    if total > width:
        raise ValueError(
            f"A {columns}-column grid of {tokens!r} is {total:.2f} units "
            f"wide at size {size}, over the {width:.2f} the frame allows."
        )
    left = -total / 2
    offsets = []
    for column in range(columns):
        offsets.append(left)
        left += spans[column] + h_gap

    block = VGroup(*made)
    height = max(m.height for m in made)
    for index, item in enumerate(made):
        row, column = divmod(index, columns)
        item.move_to([offsets[column], -row * (height + v_gap), 0],
                     aligned_edge=LEFT)
    for row in range(rows):
        members = made[row * columns:(row + 1) * columns]
        align_baselines(members, tokens[row * columns:(row + 1) * columns],
                        size)
    block.move_to(ORIGIN)
    return block, made


def screen(kind="gui", width=5.2, height=3.0, size=MARGIN_SIZE):
    """A window with its furniture, or a prompt waiting for a command.

    Deliberately crude: the point is the contrast between the two ways of
    telling a computer what to do, not a convincing screenshot.
    """
    body = Rectangle(width=width, height=height, color=CHARCOAL,
                     stroke_width=2.5)
    body.set_fill(CREAM, opacity=1)
    group = VGroup(body)

    if kind == "gui":
        bar = Rectangle(width=width, height=0.44, color=CHARCOAL,
                        stroke_width=2.5)
        bar.set_fill(SLATE, opacity=0.18)
        bar.move_to([body.get_center()[0], body.get_top()[1] - 0.22, 0])
        dots = VGroup(*[Dot(radius=0.065, color=GREY) for _ in range(3)])
        dots.arrange(RIGHT, buff=GAP_SM * 0.5)
        dots.move_to([body.get_left()[0] + 0.46, bar.get_center()[1], 0])

        menu = VGroup(*[serif(word, size, GREY)
                        for word in ("File", "Edit", "View")])
        menu.arrange(RIGHT, buff=GAP_MD)
        menu.move_to([body.get_left()[0] + menu.width / 2 + 0.3,
                      bar.get_bottom()[1] - 0.34, 0])

        icons = VGroup(*[
            Rectangle(width=0.62, height=0.62, color=SLATE, stroke_width=2)
            .set_fill(SLATE, opacity=0.16) for _ in range(3)])
        icons.arrange(RIGHT, buff=GAP_MD * 0.8)
        icons.move_to([body.get_center()[0], body.get_center()[1] - 0.25, 0])

        pointer = VGroup(
            Line(ORIGIN, UP * 0.34 + RIGHT * 0.1, color=CHARCOAL,
                 stroke_width=3),
            Line(ORIGIN, UP * 0.24 + RIGHT * 0.26, color=CHARCOAL,
                 stroke_width=3),
        )
        pointer.move_to([body.get_center()[0] + 1.25,
                         body.get_bottom()[1] + 0.62, 0])
        group.add(bar, dots, menu, icons, pointer)
    else:
        prompt = mono("C:\\> dir", size, CHARCOAL)
        second = mono("C:\\> copy a.txt", size, CHARCOAL)
        caret = Rectangle(width=0.13, height=0.3, color=CHARCOAL,
                          stroke_width=0).set_fill(CHARCOAL, opacity=1)
        text = VGroup(prompt, second).arrange(DOWN, buff=GAP_SM * 1.2,
                                              aligned_edge=LEFT)
        text.move_to([body.get_left()[0] + text.width / 2 + 0.34,
                      body.get_top()[1] - text.height / 2 - 0.4, 0])
        caret.next_to(second, RIGHT, buff=GAP_SM * 0.4)
        if text.width > width - 0.5:
            raise ValueError(
                f"The command line sample is {text.width:.2f} units wide in "
                f"a {width:.2f}-unit screen."
            )
        group.add(text, caret)
    return group


def measure():
    """Check every figure fits the frame with its labels at full size.

    Run as ``python -m components.os_shape`` from the repo root.
    """
    from manim import config

    half_w, half_h = config.frame_width / 2, config.frame_height / 2

    bench = SortBench("System software", "Application software")
    bench.caption(0, "provides the services that the computer requires")
    bench.caption(1, "provides the services that the user requires")
    for text in ("Operating systems", "Utility software", "Device drivers"):
        bench.item(0, text)
    for text in ("Word processors", "Web browsers", "Database software",
                 "Games", "Presentation software", "Video editing software"):
        bench.item(1, text)

    stack = LayerStack(["Application software", "Operating system",
                        "Device driver", "Hardware device"])
    functions = FunctionList()
    ram = MemoryBar()
    for name, share in (("word processor", 0.22), ("browser", 0.3),
                        ("music player", 0.18)):
        ram.allocate(name, share)
    ram.spare()
    slices = TimeSlices(["music", "download", "document"],
                        [0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2])
    gui, cli = screen("gui"), screen("cli")

    figures = [("bench", bench), ("stack", stack), ("functions", functions),
               ("ram", ram), ("slices", slices), ("gui", gui), ("cli", cli)]
    for name, group in figures:
        # Every one of these is built around its own natural anchor and
        # placed by the scene, so centre before asking whether it fits.
        group.move_to(ORIGIN)
        left, right = group.get_left()[0], group.get_right()[0]
        low, high = group.get_bottom()[1], group.get_top()[1]
        fits = (left > -half_w and right < half_w
                and low > -half_h and high < half_h)
        print(f"{name:10} x [{left:6.2f}, {right:6.2f}]  "
              f"y [{low:6.2f}, {high:6.2f}]  "
              f"{group.width:5.2f} x {group.height:5.2f}  "
              f"{'ok' if fits else 'OFF FRAME'}")

    # Two bins of different lengths is the normal case, so the one that
    # reaches lowest is the one that decides where the figure can sit.
    print(f"bench reaches down to y={bench.bottom():.2f} "
          f"(as placed at the origin)")

    gap = min(
        slices.lanes[i].get_top()[1] - slices.slices[i + 1].get_bottom()[1]
        for i in range(len(slices.lanes) - 1))
    print(f"slice lanes clear each other by {gap:+.2f}")


if __name__ == "__main__":
    measure()
