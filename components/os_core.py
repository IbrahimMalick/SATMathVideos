"""Inside the operating system: scheduling, the kernel, processes, files.

Chapter 1 of this course goes a layer below the O Level material in
os_shape.py. It wants pictures os_shape has no use for: a Gantt chart for
scheduling, the kernel-and-shell rings, the life of a process, threads
inside one, and a file tree.

Two of these derive their content rather than taking it as text, because
what is on screen is exactly what the exam asks the student to compute
and a hand-typed number can drift from the table above it:

  * ``schedule()`` runs first-come-first-served over the arrival and burst
    times and returns the starts, completions and waiting times. The Gantt
    chart and the results table are both built from its output, so the
    chart cannot disagree with the arithmetic.
  * ``Gantt`` places every bar and every tick from the same seconds-to-
    units scale, so a bar is as long as its burst time says.

Sized for the 14.22 x 8 landscape frame at scale 1.0, and sized so that
nothing here needs scaling down by a scene. Every label that will not fit
raises: a figure scaled to 0.9 takes its 28px labels to 25px, and the
whole repo gates on 28px.

``measure()`` checks the arithmetic and the sizing together; run it as
``python -m components.os_core`` from the repo root.
"""

from manim import (
    Arrow,
    Circle,
    Line,
    Rectangle,
    RoundedRectangle,
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


def schedule(rows):
    """First-come, first-served, run rather than asserted.

    ``rows`` is [(name, arrival, burst)]. Returns
    [(name, arrival, burst, start, complete, waiting)] in execution order,
    which for FCFS is arrival order with ties broken by the order given.
    """
    out, clock = [], 0
    # Sorted by arrival, ties broken by the order the table lists them,
    # which is what "first come" means when two arrive in the same second.
    ordered = [row for _, row in sorted(
        enumerate(rows), key=lambda pair: (pair[1][1], pair[0]))]
    for name, arrival, burst in ordered:
        start = max(clock, arrival)
        complete = start + burst
        out.append((name, arrival, burst, start, complete, start - arrival))
        clock = complete
    return out


def average_wait(runs):
    return sum(run[5] for run in runs) / len(runs)


class Gantt(VGroup):
    """A scheduling chart: one bar per process, on a shared second scale.

    Bars and ticks share one seconds-to-units factor, so a bar is exactly
    as long as its burst time. Arrival markers sit above the bars because
    an arrival is not a bar: it is an instant.
    """

    def __init__(self, runs, width=10.0, height=0.82, size=LABEL_SIZE,
                 tick_size=MARGIN_SIZE, color=SLATE, lit=TERRACOTTA,
                 rail=GREY):
        super().__init__()
        total = max(run[4] for run in runs)
        self.scale_factor = width / total
        self.total = total
        left = -width / 2

        self.bars, self.labels, self.arrivals = VGroup(), VGroup(), VGroup()
        for name, arrival, burst, start, complete, _ in runs:
            span = burst * self.scale_factor
            bar = Rectangle(width=span, height=height, color=color,
                            stroke_width=2.5)
            bar.set_fill(color, opacity=0.2)
            bar.move_to([left + (start + burst / 2) * self.scale_factor,
                         0, 0])
            label = serif(name, size, CHARCOAL)
            if label.width > span - 0.12:
                raise ValueError(
                    f"Process {name!r} is {label.width:.2f} units wide in a "
                    f"bar only {span:.2f} wide. Widen the chart.")
            label.move_to(bar)
            self.bars.add(bar)
            self.labels.add(label)
            self.add(bar, label)

        self.axis = Line([left, -height / 2, 0], [left + width, -height / 2, 0],
                         color=rail, stroke_width=2.5)
        self.ticks, self.numbers = VGroup(), VGroup()
        for second in range(total + 1):
            x = left + second * self.scale_factor
            tick = Line([x, -height / 2, 0], [x, -height / 2 - 0.14, 0],
                        color=rail, stroke_width=2)
            number = serif(str(second), tick_size, GREY)
            number.next_to(tick, DOWN, buff=GAP_SM * 0.5)
            self.ticks.add(tick)
            self.numbers.add(number)
        self.add(self.axis, self.ticks, self.numbers)
        self.left_edge, self.width_units = left, width
        self.lit_color = lit

    def at(self, second):
        """The x of a moment on the chart."""
        return self.left_edge + second * self.scale_factor

    def arrival_marks(self, runs, size=MARGIN_SIZE, color=SAGE):
        """A caret above the chart for each arrival instant."""
        marks = VGroup()
        for name, arrival, *_ in runs:
            x = self.at(arrival)
            stem = Line([x, self.bars[0].get_top()[1] + 0.12, 0],
                        [x, self.bars[0].get_top()[1] + 0.42, 0],
                        color=color, stroke_width=3)
            label = serif(name, size, color)
            label.next_to(stem, UP, buff=GAP_SM * 0.4)
            marks.add(VGroup(stem, label))
        self.arrivals = marks
        return marks

    def light(self, index, color=None):
        color = self.lit_color if color is None else color
        return [self.bars[index].animate.set_stroke(color)
                .set_fill(color, opacity=0.28)]

    def settle(self, index, color=SLATE):
        return [self.bars[index].animate.set_stroke(color)
                .set_fill(color, opacity=0.2)]


class RingModel(VGroup):
    """Hardware at the centre, and what wraps it on the way to the user.

    A ring picture rather than a stack, because the claim is containment:
    the shell does not sit on top of the kernel, it surrounds it, and the
    user never touches the middle.
    """

    def __init__(self, names=None, radii=(0.95, 1.55, 2.15, 2.72),
                 size=LABEL_SIZE, colors=None, width=FRAME_SAFE):
        super().__init__()
        names = names or ["Hardware", "Kernel", "Shell", "You"]
        colors = colors or [CHARCOAL, SLATE, SAGE, GREY]
        if len(names) != len(radii):
            raise ValueError("One radius per ring, please.")

        self.rings, self.labels = VGroup(), VGroup()
        # Outermost first, so the inner discs paint over the outer ones.
        for radius, name, colour in reversed(
                list(zip(radii, names, colors))):
            ring = Circle(radius=radius, color=colour, stroke_width=3)
            ring.set_fill(CREAM, opacity=1)
            self.rings.add(ring)
            self.add(ring)

        for index, (radius, name, colour) in enumerate(
                zip(radii, names, colors)):
            label = serif(name, size, colour)
            if index == 0:
                label.move_to(ORIGIN)
            else:
                band = radius - radii[index - 1]
                if label.height > band - 0.08:
                    raise ValueError(
                        f"Label {name!r} is {label.height:.2f} units tall in "
                        f"a band only {band:.2f} wide.")
                label.move_to([0, radius - band / 2, 0])
            self.labels.add(label)
            self.add(label)

        if self.width > width:
            raise ValueError(
                f"The ring model is {self.width:.2f} units across.")

    def light(self, index, color=TERRACOTTA):
        # Rings were added outermost first, so index counts back from the end.
        ring = self.rings[len(self.rings) - 1 - index]
        return [ring.animate.set_stroke(color, width=5),
                self.labels[index].animate.set_color(color)]


class Lifecycle(VGroup):
    """Boxes in a row with arrows: what happens to a process, in order."""

    def __init__(self, stages, width=3.3, height=1.0, gap=0.62,
                 size=LABEL_SIZE, note_size=MARGIN_SIZE, color=SLATE,
                 safe=FRAME_SAFE):
        super().__init__()
        self.boxes, self.labels, self.notes, self.arrows = (
            VGroup(), VGroup(), VGroup(), VGroup())

        for name, note in stages:
            box = RoundedRectangle(width=width, height=height, color=color,
                                   stroke_width=2.5, corner_radius=0.1)
            box.set_fill(color, opacity=0.1)
            label = serif(name, size, CHARCOAL)
            if label.width > width - GAP_SM * 2:
                raise ValueError(
                    f"Stage {name!r} is {label.width:.2f} units wide in a "
                    f"{width:.2f}-unit box.")
            label.move_to(box)
            self.boxes.add(box)
            self.labels.add(label)
            self.notes.add(serif(note, note_size, GREY))

        self.boxes.arrange(RIGHT, buff=gap)
        for box, label, note in zip(self.boxes, self.labels, self.notes):
            label.move_to(box)
            if note.width > width + gap * 0.8:
                raise ValueError(
                    f"The note {note.text!r} is {note.width:.2f} units wide "
                    f"under a {width:.2f}-unit box.")
            note.next_to(box, DOWN, buff=GAP_SM * 1.1)
            note.move_to([box.get_center()[0], note.get_center()[1], 0])

        for left, right in zip(self.boxes, self.boxes[1:]):
            self.arrows.add(Arrow(left.get_right(), right.get_left(),
                                  color=GREY, stroke_width=4, buff=0.06,
                                  max_tip_length_to_length_ratio=0.45))
        self.add(self.boxes, self.labels, self.notes, self.arrows)
        if self.width > safe:
            raise ValueError(
                f"The lifecycle runs {self.width:.2f} units.")

    def light(self, index, color=TERRACOTTA):
        return [self.boxes[index].animate.set_stroke(color)
                .set_fill(color, opacity=0.14),
                self.labels[index].animate.set_color(color)]

    def settle(self, index, color=SLATE):
        return [self.boxes[index].animate.set_stroke(color)
                .set_fill(color, opacity=0.1),
                self.labels[index].animate.set_color(CHARCOAL)]


class ThreadBox(VGroup):
    """One process, several threads, and the memory they share.

    Drawn as threads inside the process rather than beside it, because
    that containment is the whole difference being taught.
    """

    def __init__(self, process, threads, width=7.6, size=LABEL_SIZE,
                 note_size=MARGIN_SIZE, color=SLATE, lane=SAGE):
        super().__init__()
        title = serif(process, size, CHARCOAL)
        lanes = VGroup()
        for name in threads:
            label = serif(name, note_size, CHARCOAL)
            track = Line(ORIGIN, RIGHT * (width - 3.3), color=lane,
                         stroke_width=4)
            row = VGroup(label, track).arrange(RIGHT, buff=GAP_SM * 1.2)
            lanes.add(row)
        lanes.arrange(DOWN, buff=GAP_SM * 1.3, aligned_edge=LEFT)

        shared = serif("shared memory and resources", note_size, GREY)
        inner = VGroup(title, lanes, shared).arrange(DOWN, buff=GAP_SM * 1.4)
        box = Rectangle(width=width, height=inner.height + GAP_MD * 1.6,
                        color=color, stroke_width=3)
        box.set_fill(color, opacity=0.07)
        box.move_to(inner)
        if inner.width > width - GAP_MD:
            raise ValueError(
                f"The threads run {inner.width:.2f} units inside a "
                f"{width:.2f}-unit process box.")
        self.box, self.title, self.lanes, self.shared = box, title, lanes, shared
        self.add(box, inner)


class FileTree(VGroup):
    """Folders, files, and the fact that a file knows things about itself."""

    def __init__(self, rows, size=LABEL_SIZE, indent=0.62, color=CHARCOAL,
                 folder=SLATE, width=FRAME_SAFE):
        super().__init__()
        self.rows = VGroup()
        for depth, name, is_folder in rows:
            glyph = serif("▸" if is_folder else "·", size,
                          folder if is_folder else GREY)
            label = serif(name, size, folder if is_folder else color)
            row = VGroup(glyph, label).arrange(RIGHT, buff=GAP_SM * 0.8)
            row.shift(RIGHT * depth * indent)
            self.rows.add(row)
        # arrange() would pull every row back to a shared edge and undo
        # the indents, which are the only thing making this a tree.
        step = self.rows[0].height + GAP_SM * 1.1
        for index, row in enumerate(self.rows):
            row.move_to([row.get_center()[0], -index * step, 0])
        self.add(self.rows)
        if self.width > width:
            raise ValueError(f"The tree is {self.width:.2f} units wide.")


def callout(lines, size=MARGIN_SIZE, color=CHARCOAL, accent=TERRACOTTA,
            width=5.6):
    """A small boxed aside — what metadata a file carries, and the like."""
    body = VGroup(*[serif(line, size, color) for line in lines])
    body.arrange(DOWN, buff=GAP_SM * 0.7, aligned_edge=LEFT)
    if body.width > width - GAP_MD:
        raise ValueError(
            f"The callout runs {body.width:.2f} units inside {width:.2f}.")
    box = RoundedRectangle(width=width, height=body.height + GAP_MD * 1.4,
                           color=accent, stroke_width=2.5, corner_radius=0.1)
    box.move_to(body)
    return VGroup(box, body)


class Chain(VGroup):
    """A request's route, one labelled box per hop."""

    def __init__(self, stops, width=2.3, height=1.15, gap=0.26,
                 size=MARGIN_SIZE, color=SLATE, safe=FRAME_SAFE):
        super().__init__()
        self.boxes, self.labels, self.arrows = VGroup(), VGroup(), VGroup()
        for text in stops:
            box = Rectangle(width=width, height=height, color=color,
                            stroke_width=2.5)
            box.set_fill(color, opacity=0.1)
            label = serif(text, size, CHARCOAL)
            if label.width > width - GAP_SM:
                raise ValueError(
                    f"Stop {text!r} is {label.width:.2f} units wide in a "
                    f"{width:.2f}-unit box. Break it over a second line.")
            self.boxes.add(box)
            self.labels.add(label)
        self.boxes.arrange(RIGHT, buff=gap)
        for box, label in zip(self.boxes, self.labels):
            label.move_to(box)
        for left, right in zip(self.boxes, self.boxes[1:]):
            self.arrows.add(Arrow(left.get_right(), right.get_left(),
                                  color=GREY, stroke_width=3.5, buff=0.03,
                                  max_tip_length_to_length_ratio=0.5))
        self.add(self.boxes, self.labels, self.arrows)
        if self.width > safe:
            raise ValueError(f"The chain runs {self.width:.2f} units.")

    def light(self, index, color=TERRACOTTA):
        return [self.boxes[index].animate.set_stroke(color)
                .set_fill(color, opacity=0.16),
                self.labels[index].animate.set_color(color)]

    def settle(self, index, color=SLATE):
        return [self.boxes[index].animate.set_stroke(color)
                .set_fill(color, opacity=0.1),
                self.labels[index].animate.set_color(CHARCOAL)]


FCFS_ROWS = [("P1", 0, 4), ("P2", 1, 3), ("P3", 2, 1)]


def measure():
    """Check the scheduling arithmetic and every figure's sizing."""
    from manim import config

    runs = schedule(FCFS_ROWS)
    print("FCFS order:", " ".join(run[0] for run in runs))
    for name, arrival, burst, start, complete, wait in runs:
        print(f"  {name}  arrives {arrival}  burst {burst}  "
              f"starts {start}  completes {complete}  waits {wait}")
    print(f"average waiting time {average_wait(runs):.4f} "
          f"-> {average_wait(runs):.2f}")

    half_w, half_h = config.frame_width / 2, config.frame_height / 2
    chart = Gantt(runs)
    chart.add(chart.arrival_marks(runs))
    figures = [
        ("gantt", chart),
        ("rings", RingModel()),
        ("lifecycle", Lifecycle([("Creation", "resources ready"),
                                 ("Execution", "instructions run"),
                                 ("Termination", "resources back")])),
        ("threads", ThreadBox("Word processor",
                              ["typing", "auto-save"])),
        ("tree", FileTree([(0, "Documents", True), (1, "School", True),
                           (2, "notes.txt", False), (1, "photo.jpg", False)])),
        ("callout", callout(["name", "size", "type", "date created"])),
        ("chain", Chain(["You type", "Browser", "Operating\nsystem",
                         "Network\ncard", "Server"])),
    ]
    for name, group in figures:
        group.move_to(ORIGIN)
        fits = (group.get_left()[0] > -half_w
                and group.get_right()[0] < half_w
                and group.get_bottom()[1] > -half_h
                and group.get_top()[1] < half_h)
        print(f"{name:10} {group.width:5.2f} x {group.height:5.2f}  "
              f"{'ok' if fits else 'OFF FRAME'}")


if __name__ == "__main__":
    measure()
