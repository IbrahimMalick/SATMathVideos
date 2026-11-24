"""Chapter 7 drawn: a structure diagram, flowchart symbols, and rows of data.

Four figures. Everything else this chapter needs already exists --
``TraceTable`` fills a row at a time, which is the whole point of a trace
table; ``CodeBlock`` lights one line of pseudocode at a time; ``columns``
lays out the error table and ``SortBench`` sorts validation from
verification.

  * ``StructureTree``  the hierarchy a system decomposes into. Boxes and
                       the lines between them, with the third level
                       hanging off one named parent rather than all of
                       them, because that is what a worked example does.
  * ``FlowShapes``     the six symbols, each drawn as the shape the
                       syllabus expects and labelled with what it is
                       for. A student who answers "box" for a decision
                       loses the mark, so the shapes are the content.
  * ``MiniFlow``       one small flowchart, drawn vertically as a
                       flowchart is drawn, with the two branches of a
                       decision rejoining before the output.
  * ``ValueRow``       a row of boxed values that can be pointed at,
                       lit, swapped and locked. Linear search walks it,
                       bubble sort swaps along it, and the test-data
                       section colours the accepted values in it. One
                       figure, three jobs, because they are the same
                       picture: a list, and a finger on one item.

Sized for the 14.22 x 8 landscape frame at scale 1.0. Where a label will
not fit these raise rather than shrink, so the fix is a shorter label and
never a quietly illegible frame.

``MiniFlow`` is deliberately tall. A terminator, an input, a decision,
two branches, an output and a second terminator do not fit between a
heading and the commentary band as well, so a scene that draws it leaves
the band empty. ``measure()`` prints the numbers that say so.

Run ``python -m components.algorithms`` from the repo root after any
change.
"""

from manim import (
    Arrow,
    Line,
    Polygon,
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

# The worked decomposition, in the lecture's own words.
LIBRARY = ("Library system",
           ["Members", "Books", "Fines", "Reports"],
           ["Add a book", "Search", "Issue", "Return"])

# The four values the lecture sorts, in its own order.
TO_SORT = [7, 3, 5, 2]

# The accepted range in the test-data section, with the values just
# outside it that boundary testing adds.
AGES = [11, 12, 13, 14, 15, 16, 17, 18, 19]
ACCEPTED = (12, 18)


def _fits(label, width, what):
    if label.width > width - GAP_SM * 0.8:
        raise ValueError(
            f"{what} is {label.width:.2f} units wide in a {width:.2f}-unit "
            "shape. Shorten it.")
    return label


class StructureTree(VGroup):
    """A system broken into parts, and one part broken again.

    The third level hangs off one named parent, not off every box: a
    full tree of sixteen leaves is unreadable at this size, and the
    lecture only opens one of them anyway.
    """

    def __init__(self, root=LIBRARY[0], children=None, leaves=None,
                 under=1, width=2.7, leaf_width=2.6, height=0.8, gap=0.34,
                 size=MARGIN_SIZE, safe=FRAME_SAFE):
        super().__init__()
        children = LIBRARY[1] if children is None else children
        leaves = LIBRARY[2] if leaves is None else leaves

        span = len(children) * width + (len(children) - 1) * gap
        leaf_span = len(leaves) * leaf_width + (len(leaves) - 1) * gap
        if max(span, leaf_span) > safe:
            raise ValueError(
                f"The tree runs {max(span, leaf_span):.2f} units and the "
                f"frame allows {safe:.2f}.")

        # Root at 1.85, not 2.1: a section heading's descenders reach
        # 2.55 and a box top at 2.5 leaves five hundredths between them,
        # which reads as touching.
        self.root_box, root_label = self._box(root, [0, 1.85, 0],
                                              width + 1.4, height, size,
                                              SLATE)
        self.children, self.child_labels = VGroup(), VGroup()
        left = -span / 2 + width / 2
        for index, text in enumerate(children):
            box, label = self._box(text, [left + index * (width + gap),
                                          0.35, 0], width, height, size,
                                  SLATE)
            self.children.add(box)
            self.child_labels.add(label)

        self.leaves, self.leaf_labels = VGroup(), VGroup()
        left = -leaf_span / 2 + leaf_width / 2
        for index, text in enumerate(leaves):
            box, label = self._box(text, [left + index * (leaf_width + gap),
                                          -1.45, 0], leaf_width, height,
                                  size, GREY)
            self.leaves.add(box)
            self.leaf_labels.add(label)

        self.trunks = VGroup(*[self._link(self.root_box, box)
                               for box in self.children])
        # Every leaf hangs off the one parent the lecture opens, so the
        # picture says "this box, broken down" and not "all of them".
        self.parent_index = under
        self.branches = VGroup(*[self._link(self.children[under], box)
                                 for box in self.leaves])

        self.add(self.root_box, root_label, self.children, self.child_labels)
        self.root_label = root_label

    def _box(self, text, centre, width, height, size, color):
        box = Rectangle(width=width, height=height, color=color,
                        stroke_width=2.5)
        box.set_fill(color, opacity=0.1)
        box.move_to(centre)
        label = _fits(serif(text, size, CHARCOAL), width, f"Box {text!r}")
        label.move_to(centre)
        return box, label

    def _link(self, upper, lower):
        return Line(upper.get_bottom(), lower.get_top(), color=GREY,
                    stroke_width=2.5)

    def light(self, index, color=TERRACOTTA):
        return [self.children[index].animate.set_stroke(color)
                .set_fill(color, opacity=0.16),
                self.child_labels[index].animate.set_color(color)]

    def settle(self, index, color=SLATE):
        return [self.children[index].animate.set_stroke(color)
                .set_fill(color, opacity=0.1),
                self.child_labels[index].animate.set_color(CHARCOAL)]


class FlowShapes(VGroup):
    """The six flowchart symbols, drawn and named.

    Three to a row. The shapes are the content here -- a decision drawn
    as a rectangle is the mistake this figure exists to prevent -- so
    each one is the real shape at a size that reads on a phone, with its
    name under it rather than inside it.
    """

    NAMES = ["Terminator", "Process", "Input / output",
             "Decision", "Subroutine", "Flow line"]
    USES = ["start or stop", "an action", "data in or out",
            "a condition", "a defined process", "the direction"]

    def __init__(self, width=2.6, height=0.9, h_gap=1.5, v_gap=1.95,
                 size=MARGIN_SIZE, color=SLATE, safe=FRAME_SAFE):
        super().__init__()
        makers = [self._terminator, self._process, self._io,
                  self._decision, self._subroutine, self._flow_line]
        span = 3 * width + 2 * h_gap
        if span > safe:
            raise ValueError(f"A row of three runs {span:.2f} units.")

        self.shapes, self.labels = VGroup(), VGroup()
        left = -span / 2 + width / 2
        for index, make in enumerate(makers):
            row, column = divmod(index, 3)
            centre = [left + column * (width + h_gap),
                      0.95 - row * v_gap, 0]
            shape = make(width, height, color)
            shape.move_to(centre)
            # The name only. A second line saying what each symbol is
            # for costs half a unit a row, and two rows of that put the
            # bottom row's caption into the commentary band. What each
            # one is for is what the narration is saying at the time;
            # ``USES`` is there for a scene that wants to print it.
            text = serif(self.NAMES[index], size, CHARCOAL)
            text.next_to(shape, DOWN, buff=GAP_SM * 0.8)
            self.shapes.add(shape)
            self.labels.add(text)
        self.add(self.shapes, self.labels)

    def _fill(self, shape, color):
        shape.set_stroke(color, width=2.5)
        shape.set_fill(color, opacity=0.1)
        return shape

    def _terminator(self, width, height, color):
        return self._fill(
            RoundedRectangle(width=width, height=height, corner_radius=0.4),
            color)

    def _process(self, width, height, color):
        return self._fill(Rectangle(width=width, height=height), color)

    def _io(self, width, height, color):
        slant = 0.34
        return self._fill(Polygon(
            [-width / 2 + slant, height / 2, 0],
            [width / 2, height / 2, 0],
            [width / 2 - slant, -height / 2, 0],
            [-width / 2, -height / 2, 0]), color)

    def _decision(self, width, height, color):
        return self._fill(Polygon(
            [0, height / 2 + 0.12, 0], [width / 2, 0, 0],
            [0, -height / 2 - 0.12, 0], [-width / 2, 0, 0]), color)

    def _subroutine(self, width, height, color):
        outer = Rectangle(width=width, height=height)
        inset = 0.22
        bars = VGroup(
            Line([-width / 2 + inset, height / 2, 0],
                 [-width / 2 + inset, -height / 2, 0]),
            Line([width / 2 - inset, height / 2, 0],
                 [width / 2 - inset, -height / 2, 0]))
        group = VGroup(self._fill(outer, color))
        for bar in bars:
            bar.set_stroke(color, width=2.5)
            group.add(bar)
        return group

    def _flow_line(self, width, height, color):
        return Arrow([-width / 2, 0, 0], [width / 2, 0, 0], color=color,
                     stroke_width=3.5, buff=0,
                     max_tip_length_to_length_ratio=0.22)

    def light(self, index, color=TERRACOTTA):
        shape = self.shapes[index]
        animations = [shape.animate.set_stroke(color)]
        if not isinstance(shape, Arrow):
            animations = [shape.animate.set_stroke(color)
                          .set_fill(color, opacity=0.18)]
        return animations + [self.labels[index].animate.set_color(color)]

    def settle(self, index, color=SLATE):
        shape = self.shapes[index]
        if isinstance(shape, Arrow):
            return [shape.animate.set_stroke(color),
                    self.labels[index].animate.set_color(CHARCOAL)]
        return [shape.animate.set_stroke(color).set_fill(color, opacity=0.1),
                self.labels[index].animate.set_color(CHARCOAL)]


class MiniFlow(VGroup):
    """One flowchart: read a mark, decide a grade, output it.

    Vertical, as a flowchart is drawn, with the two branches of the
    decision rejoining above the output. The "No" branch runs down the
    right-hand side rather than crossing anything.

    It is tall. A scene that draws this one leaves the commentary band
    empty -- there is no room for both, and a caption printed over a
    flow line is exactly the fault nothing in the acceptance checks can
    see.
    """

    def __init__(self, width=3.4, height=0.56, size=MARGIN_SIZE,
                 color=SLATE, branch_x=3.7):
        super().__init__()
        shapes = FlowShapes.__new__(FlowShapes)   # the drawing helpers only

        # Explicit heights rather than a running total. The column has to
        # start under a heading whose descenders reach 2.55 and finish
        # above a numbered strip at -3.05, and five shapes plus a
        # branching row only fit between them if each y is chosen rather
        # than accumulated.
        plan = [
            ("terminator", "START", 2.00),
            ("io", "INPUT Mark", 1.20),
            ("decision", "Mark >= 80", 0.25),
            ("io", "OUTPUT Grade", -1.75),
            ("terminator", "STOP", -2.55),
        ]
        self.boxes, self.labels = VGroup(), VGroup()
        for kind, text, y in plan:
            if kind == "terminator":
                shape = shapes._terminator(width * 0.72, height, color)
            elif kind == "io":
                # Wider than the text it holds: a parallelogram's slant
                # eats into the corners, so a label sized to the box
                # touches both sloping edges.
                shape = shapes._io(width + 0.55, height, color)
            else:
                shape = shapes._decision(width + 0.5, height + 0.3, color)
            shape.move_to([0, y, 0])
            label = _fits(serif(text, size, CHARCOAL),
                          width + (0.5 if kind == "decision" else 0.0),
                          f"Flowchart label {text!r}")
            label.move_to(shape.get_center())
            self.boxes.add(shape)
            self.labels.add(label)

        self.start, self.read, self.decide, self.output, self.stop = \
            self.boxes

        # The two branches sit either side of the column at one height,
        # so the picture is symmetric and neither branch crosses the
        # other. An earlier version ran one branch diagonally into a box
        # under the diamond: the arrow cut through its own "Yes" label,
        # and the figure sat a unit and a half off centre.
        branch_y = -0.85
        self.assign = shapes._process(width, height, color)
        self.assign.move_to([-branch_x, branch_y, 0])
        self.assign_label = _fits(serif('Grade <- "A"', size, CHARCOAL),
                                  width, "The first branch")
        self.assign_label.move_to(self.assign.get_center())

        self.other = shapes._process(width, height, color)
        self.other.move_to([branch_x, branch_y, 0])
        self.other_label = _fits(serif('Grade <- "B"', size, CHARCOAL),
                                 width, "The second branch")
        self.other_label.move_to(self.other.get_center())

        self.arrows = VGroup(
            self._down(self.start, self.read),
            self._down(self.read, self.decide),
            self._down(self.output, self.stop),
        )

        join_y = (self.assign.get_bottom()[1] + self.output.get_top()[1]) / 2
        self.yes_path = self._elbow(self.decide.get_left(), -branch_x,
                                    self.assign)
        self.no_path = self._elbow(self.decide.get_right(), branch_x,
                                   self.other)
        self.rejoin = VGroup(
            self._leg(self.assign.get_bottom(), [-branch_x, join_y, 0]),
            self._leg([-branch_x, join_y, 0], [0, join_y, 0]),
            self._leg(self.other.get_bottom(), [branch_x, join_y, 0]),
            self._leg([branch_x, join_y, 0], [0, join_y, 0]),
            Arrow([0, join_y, 0], self.output.get_top(), color=GREY,
                  stroke_width=3, buff=0,
                  max_tip_length_to_length_ratio=0.4),
        )

        self.yes = serif("Yes", size, SAGE)
        self.yes.next_to(self.yes_path[0], UP, buff=GAP_SM * 0.4)
        self.no = serif("No", size, GREY)
        self.no.next_to(self.no_path[0], UP, buff=GAP_SM * 0.4)

        self.add(self.boxes, self.labels)
        self.all = VGroup(self.boxes, self.labels, self.arrows,
                          self.assign, self.assign_label, self.other,
                          self.other_label, self.yes_path, self.no_path,
                          self.rejoin, self.yes, self.no)

    def _elbow(self, from_point, to_x, box):
        """Out of the diamond sideways, then down into a branch box."""
        corner = [to_x, from_point[1], 0]
        return VGroup(
            self._leg(from_point, corner),
            Arrow(corner, box.get_top(), color=GREY, stroke_width=3,
                  buff=0, max_tip_length_to_length_ratio=0.4),
        )

    def _leg(self, start, end):
        return Line(start, end, color=GREY, stroke_width=3)

    def _down(self, upper, lower):
        return Arrow(upper.get_bottom(), lower.get_top(), color=GREY,
                     stroke_width=3, buff=0.02,
                     max_tip_length_to_length_ratio=0.3)


class ValueRow(VGroup):
    """A row of boxed values: pointed at, lit, swapped, locked.

    Linear search walks it, bubble sort swaps along it, and the
    test-data section colours the values inside and outside a range. The
    swap moves the two cells past each other and then swaps them in this
    object's own list, so ``cells[i]`` always means "the box in position
    i" and a scene never has to track where a value went.
    """

    def __init__(self, values, width=1.5, height=0.95, gap=0.22,
                 size=LABEL_SIZE, color=SLATE, safe=FRAME_SAFE):
        super().__init__()
        span = len(values) * width + (len(values) - 1) * gap
        if span > safe:
            raise ValueError(
                f"A row of {len(values)} runs {span:.2f} units and the "
                f"frame allows {safe:.2f}. Narrow the cells.")
        self.cell_width, self.cell_gap = width, gap
        self.left = -span / 2 + width / 2
        self.cells, self.labels = [], []
        for index, value in enumerate(values):
            box = Rectangle(width=width, height=height, color=color,
                            stroke_width=2.5)
            box.set_fill(color, opacity=0.1)
            box.move_to([self.left + index * (width + gap), 0, 0])
            label = _fits(serif(str(value), size, CHARCOAL), width,
                          f"Cell {value!r}")
            label.move_to(box.get_center())
            self.cells.append(box)
            self.labels.append(label)
        self.boxes = VGroup(*self.cells)
        self.texts = VGroup(*self.labels)
        self.add(self.boxes, self.texts)

        # A long enough shaft for the head to be drawn at a size the
        # eye finds: Manim scales an arrow's head to its length, and a
        # six-tenths arrow renders as a tick mark.
        self.pointer = Arrow([0, -height / 2 - 1.15, 0],
                             [0, -height / 2 - 0.14, 0], color=TERRACOTTA,
                             stroke_width=6, buff=0,
                             max_tip_length_to_length_ratio=0.4)
        self.pointer.move_to([self.cells[0].get_center()[0],
                              self.pointer.get_center()[1], 0])

    def at(self, index):
        """Where position ``index`` is on screen, whatever is in it."""
        return self.left + index * (self.cell_width + self.cell_gap)

    def point_to(self, index):
        return self.pointer.animate.move_to(
            [self.at(index), self.pointer.get_center()[1], 0])

    def light(self, index, color=TERRACOTTA):
        return [self.cells[index].animate.set_stroke(color)
                .set_fill(color, opacity=0.18),
                self.labels[index].animate.set_color(color)]

    def settle(self, index, color=SLATE):
        return [self.cells[index].animate.set_stroke(color)
                .set_fill(color, opacity=0.1),
                self.labels[index].animate.set_color(CHARCOAL)]

    def lock(self, index, color=SAGE):
        return [self.cells[index].animate.set_stroke(color)
                .set_fill(color, opacity=0.2),
                self.labels[index].animate.set_color(color)]

    def swap(self, index):
        """Animations that exchange positions ``index`` and ``index + 1``.

        The two cells move past each other and the lists are reordered
        afterwards, so the caller keeps talking in positions.
        """
        if index < 0 or index + 1 >= len(self.cells):
            raise ValueError(
                f"There is no pair at position {index} in a row of "
                f"{len(self.cells)}.")
        here, there = self.at(index), self.at(index + 1)
        first_box, second_box = self.cells[index], self.cells[index + 1]
        first_text, second_text = self.labels[index], self.labels[index + 1]
        moves = [
            first_box.animate.move_to([there, 0, 0]),
            first_text.animate.move_to([there, 0, 0]),
            second_box.animate.move_to([here, 0, 0]),
            second_text.animate.move_to([here, 0, 0]),
        ]
        self.cells[index], self.cells[index + 1] = second_box, first_box
        self.labels[index], self.labels[index + 1] = second_text, first_text
        return moves


def measure():
    """Print every figure's extents, and the two numbers that decide
    whether a commentary line fits under it."""
    from manim import config

    config.background_color = "#F4F0E6"

    tree = StructureTree()
    whole = VGroup(tree, tree.trunks, tree.branches, tree.leaves,
                   tree.leaf_labels)
    print(f"StructureTree {whole.width:6.2f} x {whole.height:5.2f}  "
          f"(y {whole.get_bottom()[1]:.2f} to {whole.get_top()[1]:.2f})")

    shapes = FlowShapes()
    print(f"FlowShapes    {shapes.width:6.2f} x {shapes.height:5.2f}  "
          f"(y {shapes.get_bottom()[1]:.2f} to {shapes.get_top()[1]:.2f})")

    flow = MiniFlow()
    print(f"MiniFlow      {flow.all.width:6.2f} x {flow.all.height:5.2f}  "
          f"(y {flow.all.get_bottom()[1]:.2f} to "
          f"{flow.all.get_top()[1]:.2f})  "
          f"-- band at -2.70 is {'FREE' if flow.all.get_bottom()[1] > -2.4 else 'TAKEN'}")

    row = ValueRow(TO_SORT)
    with_pointer = VGroup(row, row.pointer)
    print(f"ValueRow(4)   {with_pointer.width:6.2f} x "
          f"{with_pointer.height:5.2f}  "
          f"(y {with_pointer.get_bottom()[1]:.2f} to "
          f"{with_pointer.get_top()[1]:.2f})")
    ages = ValueRow(AGES, width=1.2)
    print(f"ValueRow(9)   {ages.width:6.2f} x {ages.height:5.2f}")
    names = ValueRow(["Ravi", "Sara", "Amina", "Joel", "Mei"], width=2.3)
    print(f"ValueRow(names) {names.width:6.2f} x {names.height:5.2f}")

    # The swap has to leave the row in the order the eye sees.
    check = ValueRow([7, 3, 5, 2])
    check.swap(0)
    order = [label.text for label in check.labels]
    print(f"after swapping positions 0 and 1: {order}")


if __name__ == "__main__":
    measure()
