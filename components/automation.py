"""Chapter 6 drawn: a control loop, an expert system, and training stages.

Three figures. Everything else this chapter needs already exists --
``SortBench`` weighs automation's advantages against its costs and then,
unchanged, an expert system's strengths against its limits; ``columns``
lays out the four automated systems and the expert-system-against-machine-
learning table; ``chips`` and ``grid`` carry the robot material.

  * ``ControlLoop``   sensor, microprocessor, actuator, and the arrow
                      back to the sensor. The return arrow is the whole
                      figure: three boxes in a row is an open chain, and
                      an open chain is exactly the answer the syllabus
                      marks down -- a system that acts and never checks
                      the result. It is drawn as its own elbow below the
                      row so it cannot be mistaken for another forward
                      step.
  * ``ExpertSystem``  the four named components, placed so that each one
                      does its own job: facts and rules sit on the right
                      and feed the inference engine, the engine is the
                      only box the arrows converge on, and the advice
                      returns to the interface by a different path than
                      it came. A student who can see which box an arrow
                      leaves can answer "what does the inference engine
                      do" without reciting it.
  * ``StageFlow``     the machine-learning stages, three to a row, with
                      the wrap drawn in the gap between the rows.

Sized for the 14.22 x 8 landscape frame at scale 1.0, like every other
figure here. Where a label will not fit these raise rather than shrink,
so the fix is a shorter label and never a quietly illegible frame.

``measure()`` prints every figure's extents; run it as
``python -m components.automation`` from the repo root after any change.
"""

from manim import (
    Arrow,
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
    GAP_LG,
    GAP_MD,
    GAP_SM,
    GREY,
    LABEL_SIZE,
    MARGIN_SIZE,
    SAGE,
    SLATE,
    TERRACOTTA,
    serif,
)

FRAME_SAFE = 12.6

# The three stages in the order the lecture takes them, and the order
# every exam answer wants them in.
STAGES = ("Sensor", "Microprocessor", "Actuator")

# The four components of an expert system, named as the syllabus names
# them. The order here is the order the lecture introduces them.
PARTS = ("Knowledge base", "Rule base", "Inference engine",
         "User interface")

# The machine-learning stages, in the lecture's own order. Two lines
# each: one line of "Prepare and label" is 3.48 units, and a box wide
# enough for it puts a row of three over the frame.
TRAINING = ("Collect\ndata", "Prepare\nand label", "Train the\nmodel",
            "Evaluate\nit", "Use on\nnew data", "Monitor\nand update")


def _fits(label, box_width, what):
    if label.width > box_width - GAP_SM:
        raise ValueError(
            f"{what} is {label.width:.2f} units wide in a "
            f"{box_width:.2f}-unit box. Shorten it or split the line.")
    return label


def _panel(text, centre, width, height, size, color):
    """One labelled box, built at an absolute position."""
    box = Rectangle(width=width, height=height, color=color,
                    stroke_width=2.5)
    box.set_fill(color, opacity=0.1)
    box.move_to(centre)
    label = _fits(serif(text, size, CHARCOAL), width, f"Box label {text!r}")
    label.move_to(centre)
    return box, label


class ControlLoop:
    """Sensor, microprocessor, actuator -- and the reading taken again.

    The forward arrows and the return arrow are different objects and are
    handed out separately, because the lecture earns the return arrow
    several sentences after the row: the system acts first, and only then
    does the point get made that it measures again.

    Not a VGroup, and deliberately. Everything here is built at absolute
    coordinates and the return path is not a member of any group, so a
    scene that moved the figure would move the boxes and leave the path
    behind -- which is exactly what Chapter 4 did with an arrow it had
    forgotten to add, and nothing in the acceptance checks can see an
    arrow that is somewhere else. A plain object cannot be moved by
    accident.
    """

    def __init__(self, stages=STAGES, width=3.4, height=1.2, gap=1.1,
                 size=MARGIN_SIZE, color=SLATE, drop=1.15, y=0.35,
                 safe=FRAME_SAFE):
        span = len(stages) * width + (len(stages) - 1) * gap
        if span > safe:
            raise ValueError(
                f"The row runs {span:.2f} units and the frame allows "
                f"{safe:.2f}. Narrow the boxes or close the gap.")

        left = -span / 2 + width / 2
        self.gap = gap
        self.boxes, self.labels = VGroup(), VGroup()
        for index, text in enumerate(stages):
            centre = [left + index * (width + gap), y, 0]
            box, label = _panel(text, centre, width, height, size, color)
            self.boxes.add(box)
            self.labels.add(label)

        self.arrows = VGroup()
        for first, second in zip(self.boxes, self.boxes[1:]):
            self.arrows.add(Arrow(first.get_right(), second.get_left(),
                                  color=GREY, stroke_width=3.5, buff=0.08,
                                  max_tip_length_to_length_ratio=0.32))

        # The return path: down from the actuator, back along underneath
        # the row, and up into the sensor. Three segments rather than a
        # curve, so the depth it reaches is a number here and not
        # whatever a sag happens to come out at.
        floor_y = y - height / 2 - drop
        start = self.boxes[-1].get_bottom()
        finish = self.boxes[0].get_bottom()
        self.feedback = VGroup(
            Line([start[0], start[1], 0], [start[0], floor_y, 0],
                 color=SAGE, stroke_width=3.5),
            Line([start[0], floor_y, 0], [finish[0], floor_y, 0],
                 color=SAGE, stroke_width=3.5),
            Arrow([finish[0], floor_y, 0], [finish[0], finish[1], 0],
                  color=SAGE, stroke_width=3.5, buff=0,
                  max_tip_length_to_length_ratio=0.22),
        )
        self.feedback_label = serif("measure again", size, SAGE)
        self.feedback_label.move_to([0, floor_y - GAP_SM * 1.4, 0])

        self.details = VGroup()
        # Every piece, for a scene that wants to fade the lot at once.
        self.all = VGroup(self.boxes, self.labels, self.arrows,
                          self.feedback, self.feedback_label, self.details)

    def arrow_into(self, index):
        """The forward arrow that points into box ``index``.

        Arrow k runs from box k to box k + 1, so the arrow arriving at a
        box is the one before it. Writing that subtraction out in a scene
        is how Chapter 4 drew one arrow twice and another never, so it
        lives here where it can only be wrong once.
        """
        if index < 1 or index >= len(self.boxes):
            raise ValueError(
                f"Box {index} has no arrow into it; the first box is "
                "where the loop starts.")
        return self.arrows[index - 1]

    def detail(self, index, text, color=GREY, size=None):
        """A small caption above a box -- what it is in this example.

        Above, never below: below is where the return path runs, and a
        caption there would sit on it. It may be a little wider than its
        box, because the gaps either side are empty, but it wraps rather
        than growing into its neighbour.
        """
        size = MARGIN_SIZE if size is None else size
        from components.editorial import prose
        allowed = self.boxes[index].width + self.gap * 0.7
        note = prose(text, size, color, allowed)
        if note.width > allowed:
            raise ValueError(
                f"Detail {text!r} is {note.width:.2f} units wide and only "
                f"{allowed:.2f} fit above the box. Shorten it.")
        note.next_to(self.boxes[index], UP, buff=GAP_SM * 0.9)
        self.details.add(note)
        return note

    def light(self, index, color=TERRACOTTA):
        return [self.boxes[index].animate.set_stroke(color)
                .set_fill(color, opacity=0.16),
                self.labels[index].animate.set_color(color)]

    def settle(self, index, color=SLATE):
        return [self.boxes[index].animate.set_stroke(color)
                .set_fill(color, opacity=0.1),
                self.labels[index].animate.set_color(CHARCOAL)]


class ExpertSystem:
    """The four components, and which way the information travels.

    Knowledge base and rule base on the right, the inference engine in
    the middle, the interface on the left. Everything the user supplies
    enters along the top arrow; everything the system concludes leaves
    along the return path underneath. Two arrows between the same pair of
    boxes on the same line would read as one double-headed arrow, which
    is the mistake Chapter 5's journey figure had to be rescued from, so
    the return is an elbow and not a second straight line.

    A plain object rather than a VGroup, for the reason ``ControlLoop``
    gives: the arrows here are not members of any group, so a figure that
    could be moved would leave them behind.
    """

    def __init__(self, size=MARGIN_SIZE, width=3.0, height=1.3,
                 size_small=MARGIN_SIZE, safe=FRAME_SAFE):
        self.boxes, self.labels = VGroup(), VGroup()
        # Two lines each. "Knowledge base" on one line is 3.18 units and
        # the box it has room for is 3.0, and widening the boxes instead
        # closes the gap the arrows need.
        places = [
            ("Knowledge\nbase", [4.3, 1.25, 0], SLATE),
            ("Rule\nbase", [4.3, -0.55, 0], SLATE),
            ("Inference\nengine", [0.0, 0.35, 0], SLATE),
            ("User\ninterface", [-4.3, 0.35, 0], GREY),
        ]
        for text, centre, color in places:
            box, label = _panel(text, centre, width, height, size, color)
            self.boxes.add(box)
            self.labels.add(label)
        self.knowledge, self.rules, self.engine, self.interface = self.boxes

        # Facts in along the top, rules and knowledge down into the
        # engine from the right.
        self.asks = Arrow(self.interface.get_right(), self.engine.get_left(),
                          color=GREY, stroke_width=3.5, buff=0.08,
                          max_tip_length_to_length_ratio=0.22)
        self.from_knowledge = Arrow(
            self.knowledge.get_left(), self.engine.get_right(),
            color=GREY, stroke_width=3.5, buff=0.12,
            max_tip_length_to_length_ratio=0.22)
        self.from_rules = Arrow(
            self.rules.get_left(), self.engine.get_right(),
            color=GREY, stroke_width=3.5, buff=0.12,
            max_tip_length_to_length_ratio=0.22)

        floor_y = -1.6
        start = self.engine.get_bottom()
        finish = self.interface.get_bottom()
        self.advice = VGroup(
            Line([start[0], start[1], 0], [start[0], floor_y, 0],
                 color=SAGE, stroke_width=3.5),
            Line([start[0], floor_y, 0], [finish[0], floor_y, 0],
                 color=SAGE, stroke_width=3.5),
            Arrow([finish[0], floor_y, 0], [finish[0], finish[1], 0],
                  color=SAGE, stroke_width=3.5, buff=0,
                  max_tip_length_to_length_ratio=0.22),
        )
        self.advice_label = serif("the conclusion", size_small, SAGE)
        self.advice_label.move_to([(start[0] + finish[0]) / 2,
                                   floor_y - GAP_SM * 1.4, 0])
        # No label on the arrow into the engine. The gap between the
        # interface and the engine is 1.3 units and the shortest honest
        # caption is three times that, so it would have to be printed
        # over a box. What goes in is a sentence the narration says, not
        # a word the picture has room for.

        self.all = VGroup(self.boxes, self.labels, self.asks,
                          self.from_knowledge, self.from_rules,
                          self.advice, self.advice_label)
        if self.all.width > safe:
            raise ValueError(
                f"The expert system runs {self.all.width:.2f} units.")

    def light(self, index, color=TERRACOTTA):
        return [self.boxes[index].animate.set_stroke(color)
                .set_fill(color, opacity=0.16),
                self.labels[index].animate.set_color(color)]

    def settle(self, index, color=None):
        color = SLATE if index != 3 else GREY
        return [self.boxes[index].animate.set_stroke(color)
                .set_fill(color, opacity=0.1),
                self.labels[index].animate.set_color(CHARCOAL)]


class StageFlow(VGroup):
    """A process too long for one row, wrapped into two.

    The wrap is drawn in the gap between the rows: down from the last box
    of the first row, back along the middle of the gap, and down into the
    first box of the second row. It crosses nothing, which is the only
    reason to prefer it to a serpentine that reverses direction and
    leaves the reader working out which way to read row two.
    """

    def __init__(self, stages=TRAINING, per_row=3, width=3.1, height=1.25,
                 gap=0.8, row_gap=2.05, size=MARGIN_SIZE, color=SLATE,
                 safe=FRAME_SAFE):
        super().__init__()
        rows = [list(stages[i:i + per_row])
                for i in range(0, len(stages), per_row)]
        span = per_row * width + (per_row - 1) * gap
        if span > safe:
            raise ValueError(
                f"A row of {per_row} runs {span:.2f} units and the frame "
                f"allows {safe:.2f}.")

        self.boxes, self.labels, self.arrows = VGroup(), VGroup(), VGroup()
        top = (len(rows) - 1) * row_gap / 2
        self.rows = []
        for r, row in enumerate(rows):
            left = -span / 2 + width / 2
            made = []
            for c, text in enumerate(row):
                centre = [left + c * (width + gap), top - r * row_gap, 0]
                box, label = _panel(text, centre, width, height, size, color)
                self.boxes.add(box)
                self.labels.add(label)
                made.append(box)
            self.rows.append(made)
            for first, second in zip(made, made[1:]):
                self.arrows.add(Arrow(
                    first.get_right(), second.get_left(), color=GREY,
                    stroke_width=3.5, buff=0.08,
                    max_tip_length_to_length_ratio=0.32))

        self.wraps = VGroup()
        for upper, lower in zip(self.rows, self.rows[1:]):
            start, finish = upper[-1], lower[0]
            middle = (start.get_bottom()[1] + finish.get_top()[1]) / 2
            self.wraps.add(VGroup(
                Line(start.get_bottom(), [start.get_center()[0], middle, 0],
                     color=GREY, stroke_width=3.5),
                Line([start.get_center()[0], middle, 0],
                     [finish.get_center()[0], middle, 0],
                     color=GREY, stroke_width=3.5),
                Arrow([finish.get_center()[0], middle, 0],
                      finish.get_top(), color=GREY, stroke_width=3.5,
                      buff=0, max_tip_length_to_length_ratio=0.3),
            ))

        self.add(self.boxes, self.labels, self.arrows, self.wraps)

    def light(self, index, color=TERRACOTTA):
        return [self.boxes[index].animate.set_stroke(color)
                .set_fill(color, opacity=0.16),
                self.labels[index].animate.set_color(color)]

    def settle(self, index, color=SLATE):
        return [self.boxes[index].animate.set_stroke(color)
                .set_fill(color, opacity=0.1),
                self.labels[index].animate.set_color(CHARCOAL)]


def measure():
    """Print every figure's extents. The guards above check widths; this
    is for the vertical room, which only a scene can really judge."""
    from manim import config

    config.background_color = "#F4F0E6"

    loop = ControlLoop()
    whole = loop.all
    print(f"ControlLoop  row {loop.boxes.width:6.2f} x "
          f"{loop.boxes.height:5.2f}  with return path "
          f"{whole.width:6.2f} x {whole.height:5.2f}  "
          f"(y {whole.get_bottom()[1]:.2f} to {whole.get_top()[1]:.2f})")

    expert = ExpertSystem()
    full = expert.all
    print(f"ExpertSystem {full.width:6.2f} x {full.height:5.2f}  "
          f"(y {full.get_bottom()[1]:.2f} to {full.get_top()[1]:.2f})")

    flow = StageFlow()
    print(f"StageFlow    {flow.width:6.2f} x {flow.height:5.2f}  "
          f"(y {flow.get_bottom()[1]:.2f} to {flow.get_top()[1]:.2f})")

    # The two things no width guard can see: a caption sitting on the
    # return path, and the wrap arrow touching a box it does not belong
    # to.
    gap = loop.boxes[0].get_bottom()[1] - loop.feedback[1].get_center()[1]
    print(f"return path runs {gap:.2f} units below the boxes, "
          f"label another {loop.feedback[1].get_center()[1] - loop.feedback_label.get_top()[1]:.2f} below that")
    for index, row in enumerate(flow.rows):
        print(f"  row {index}: y {row[0].get_center()[1]:+.2f}")


if __name__ == "__main__":
    measure()
