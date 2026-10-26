"""Data transmission furniture: packets, links, parity, handshakes, keys.

Chapter 2 is almost entirely diagrams. Every one of its topics is a picture
of something moving between two devices and being checked on arrival, so
the pictures live here rather than being rebuilt inside the scene.

Three of these derive their content rather than taking it as text, because
the thing on screen is exactly what the exam asks the student to compute
and a hand-typed label can drift from the bits above it:

  * ParityRow derives its parity bit from the data bits and the scheme.
  * ParityBlock derives every row parity, every column parity, and the
    corner, so a flipped bit really does break one row and one column.
  * Handshake numbers its own steps, so inserting one cannot misnumber
    the rest.

Sized for the landscape lecture frame (14.22 x 8 units), and sized so that
nothing here needs scaling down by the scene. Every box is built to fit its
label at the label's own size rather than shrinking the label to fit the
box: a diagram scaled to 0.9 takes its 28px captions down to 25px, which
fails the mobile legibility gate for a saving no one asked for. If one of
these does not fit a frame, the fix is a shorter label, not a smaller
drawing.
"""

import numpy as np

from manim import (
    Arrow,
    Circle,
    DashedLine,
    Dot,
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


def fit(mobject, width=FRAME_SAFE):
    if mobject.width > width:
        mobject.scale_to_fit_width(width)
    return mobject


def _caption(text, size, color, width):
    label = serif(text, size, color)
    if label.width > width:
        label.scale_to_fit_width(width)
    return label


# --------------------------------------------------------------- packets


class PacketFrame(VGroup):
    """One packet: header, payload, trailer, side by side and to scale.

    The payload is drawn widest because it carries the message and the
    other two carry control information — the proportions are part of the
    answer to "what is in a packet".

        frame = PacketFrame()
        self.play(Create(frame.boxes), Write(frame.labels))
        self.play(*frame.light(0))
        self.play(Write(frame.contents(0, ["destination address", ...])))
    """

    SECTIONS = ("HEADER", "PAYLOAD", "TRAILER")

    # 10.8 wide so the narrow end sections still hold HEADER and TRAILER at
    # LABEL_SIZE without shrinking: share 1.0 of 4.2 gives 2.57 units, and
    # the labels need 2.09.
    def __init__(self, shares=(1.0, 2.2, 1.0), height=1.15, width=10.8,
                 size=LABEL_SIZE, color=SLATE, lit=TERRACOTTA, dim=GREY):
        super().__init__()
        self.lit_color, self.dim_color, self.base_color = lit, dim, color

        total = sum(shares)
        self.boxes, self.labels = VGroup(), VGroup()
        x = -width / 2
        self.centres = []
        for name, share in zip(self.SECTIONS, shares):
            w = width * share / total
            box = Rectangle(width=w, height=height, color=color,
                            stroke_width=3)
            box.move_to([x + w / 2, 0, 0])
            label = _caption(name, size, CHARCOAL, w - GAP_SM * 1.4)
            label.move_to(box)
            self.boxes.add(box)
            self.labels.add(label)
            self.centres.append(box.get_center())
            x += w
        self.add(self.boxes, self.labels)

    def box(self, index):
        return self.boxes[index]

    def light(self, index):
        """One section in terracotta, the others quiet."""
        moves = []
        for i, (box, label) in enumerate(zip(self.boxes, self.labels)):
            on = i == index
            moves.append(box.animate.set_stroke(
                self.lit_color if on else self.dim_color))
            moves.append(label.animate.set_color(
                self.lit_color if on else self.dim_color))
        return moves

    def settle(self):
        return ([box.animate.set_stroke(self.base_color)
                 for box in self.boxes]
                + [label.animate.set_color(CHARCOAL) for label in self.labels])

    def contents(self, index, rows, size=MARGIN_SIZE, color=CHARCOAL,
                 buff=GAP_MD, width=5.2):
        """A list of what that section holds, hung under its box."""
        body = VGroup(*[_caption(f"·  {r}", size, color, width) for r in rows])
        body.arrange(DOWN, buff=GAP_SM * 0.9, aligned_edge=LEFT)
        body.next_to(self.boxes[index], DOWN, buff=buff)
        # Keep the list inside the frame even when it hangs off an edge box.
        half = FRAME_SAFE / 2
        if body.get_left()[0] < -half:
            body.shift(RIGHT * (-half - body.get_left()[0]))
        if body.get_right()[0] > half:
            body.shift(LEFT * (body.get_right()[0] - half))
        return body


def packet_chip(label, side=0.56, color=SLATE, size=LABEL_SIZE,
                fill=CREAM):
    """A numbered packet, small enough to travel a route diagram."""
    box = Rectangle(width=side, height=side, color=color, stroke_width=2.5,
                    fill_color=fill, fill_opacity=1)
    text = serif(str(label), size, CHARCOAL)
    if text.width > side * 0.62:
        text.scale_to_fit_width(side * 0.62)
    text.move_to(box)
    return VGroup(box, text)


class RouteMap(VGroup):
    """Sender, receiver, and several routes of routers between them.

    The point of the picture is that the routes differ in length, so
    packets sent in order can arrive out of order. The router positions are
    explicit rather than computed: three routes that look evenly spaced
    matter more here than a general layout.
    """

    ROUTES = (
        [(-2.3, 1.45), (0.0, 1.75), (2.3, 1.45)],
        [(-2.1, 0.0), (0.6, 0.0)],
        [(-2.3, -1.45), (-0.2, -1.8), (2.1, -1.4)],
    )

    def __init__(self, span=4.55, size=LABEL_SIZE, color=SLATE,
                 lit=TERRACOTTA, dim=GREY, node_radius=0.26):
        super().__init__()
        self.lit_color, self.dim_color = lit, dim
        self.radius = node_radius

        self.sender = self._end("SENDER", -span, color, size)
        self.receiver = self._end("RECEIVER", span, color, size)

        # The routers are kept as mobjects per route rather than as fixed
        # coordinates, so a packet's path is read off the diagram as it
        # stands. Coordinates captured at construction go stale the moment
        # the caller scales or repositions the map, and the packet then
        # travels to where the map used to be.
        self.routes, self.rings = VGroup(), []
        for points in self.ROUTES:
            stops = ([self.sender[0].get_right()]
                     + [np.array([x, y, 0]) for x, y in points]
                     + [self.receiver[0].get_left()])
            route = VGroup()
            for a, b in zip(stops, stops[1:]):
                route.add(Line(a, b, color=dim, stroke_width=2))
            rings = []
            for x, y in points:
                ring = Circle(radius=node_radius, color=color,
                              stroke_width=2.5, fill_color=CREAM,
                              fill_opacity=1)
                ring.move_to([x, y, 0])
                route.add(ring)
                rings.append(ring)
            self.routes.add(route)
            self.rings.append(rings)

        self.add(self.routes, self.sender, self.receiver)

    def _end(self, name, x, color, size):
        # Wide enough for RECEIVER at LABEL_SIZE (2.47 units) with padding,
        # so the label is never shrunk to fit the box.
        box = RoundedRectangle(width=3.1, height=1.0, corner_radius=0.12,
                               color=color, stroke_width=3,
                               fill_color=CREAM, fill_opacity=1)
        box.move_to([x, 0, 0])
        label = _caption(name, size, CHARCOAL, 2.7)
        label.move_to(box)
        return VGroup(box, label)

    def route(self, index):
        return self.routes[index]

    def light_route(self, index):
        moves = []
        for i, route in enumerate(self.routes):
            colour = self.lit_color if i == index else self.dim_color
            for part in route:
                moves.append(part.animate.set_stroke(colour))
        return moves

    def dim_routes(self):
        return [part.animate.set_stroke(self.dim_color)
                for route in self.routes for part in route]

    def dock(self, chips, pitch=0.65, gap=0.5):
        """Park packets in a column below the sender, waiting to be sent.

        Below rather than inside: a chip sitting on the sender's own label
        is two pieces of text in the same place, which reads as a mistake
        even though it is only a queue.
        """
        top = self.sender[0].get_bottom()[1] - gap
        x = self.sender[0].get_center()[0]
        for i, chip in enumerate(chips):
            chip.move_to([x, top - i * pitch, 0])
        return chips

    def path(self, index):
        """The stops along one route, read off the diagram as it stands."""
        return ([self.sender[0].get_right()]
                + [ring.get_center() for ring in self.rings[index]]
                + [self.receiver[0].get_left()])

    def wire(self, index, start=None, end=None):
        """The route as a single path, for one MoveAlongPath per packet.

        One animation rather than one per hop: a play per hop is a play per
        router, and the pacing floor then makes a three-router route cost
        two seconds of beat whether the narration has them or not.

        ``end`` carries the packet past the receiver into its own arrival
        slot. Without it every route finishes on the same point and the
        three packets land on top of each other.
        """
        from manim import VMobject

        stops = self.path(index)
        if start is not None:
            stops = [np.asarray(start, float)] + stops
        if end is not None:
            stops = stops + [np.asarray(end, float)]
        path = VMobject()
        path.set_points_as_corners(stops)
        return path

    def slots(self, count, at=None, pitch=None):
        """Target positions for a row of packets, left to right.

        Positions rather than a laid-out group: arranging the packets
        themselves would teleport them there, and the arrival into the
        buffer is the thing being animated.
        """
        pitch = pitch if pitch is not None else 0.52 + GAP_SM * 0.6
        centre = np.array([0.0, 0.0, 0.0]) if at is None else np.asarray(at,
                                                                         float)
        return [centre + RIGHT * ((i - (count - 1) / 2) * pitch)
                for i in range(count)]


# ----------------------------------------------------------------- links


class SerialLink(VGroup):
    """One channel, bits one after another: the serial picture.

    Deliberately the same two end boxes as ParallelLink at the same scale,
    because the comparison is the question — one wire with a queue on it
    against four wires with a bit on each.
    """

    def __init__(self, bits="10110010", span=3.9, size=LABEL_SIZE,
                 color=SLATE, dim=GREY, cell=0.5):
        super().__init__()
        self.pattern = str(bits).replace(" ", "")
        self.cell = cell

        self.left = self._end("A", -span, color, size)
        self.right = self._end("B", span, color, size)
        self.wire = Line(self.left.get_right(), self.right.get_left(),
                         color=dim, stroke_width=2.5)
        self.bits = VGroup(*[self._bit(b, color, size) for b in self.pattern])
        self.bits.arrange(RIGHT, buff=GAP_SM * 0.5)
        self.bits.move_to(self.wire.get_center())
        self.add(self.wire, self.bits, self.left, self.right)

    def _end(self, name, x, color, size):
        box = RoundedRectangle(width=1.3, height=1.3, corner_radius=0.1,
                               color=color, stroke_width=3,
                               fill_color=CREAM, fill_opacity=1)
        box.move_to([x, 0, 0])
        label = _caption(name, size, CHARCOAL, 1.0)
        label.move_to(box)
        return VGroup(box, label)

    def _bit(self, value, color, size):
        box = Rectangle(width=self.cell, height=self.cell, color=color,
                        stroke_width=2, fill_color=CREAM, fill_opacity=1)
        text = serif(value, size, CHARCOAL)
        if text.width > self.cell * 0.55:
            text.scale_to_fit_width(self.cell * 0.55)
        text.move_to(box)
        return VGroup(box, text)

    def shift_along(self, distance=None):
        """Walk the whole queue one cell towards the receiver."""
        step = distance if distance is not None else self.cell + GAP_SM * 0.5
        return self.bits.animate.shift(RIGHT * step)


class ParallelLink(VGroup):
    """Several channels, one bit abreast on each: the parallel picture.

    Four channels rather than eight. Eight lines inside an 8-unit frame
    puts the bit cells under the legibility floor, and four already carries
    the only idea that matters — more than one wire, more than one bit at
    a time.
    """

    def __init__(self, bits="1011", span=3.9, pitch=0.72, size=LABEL_SIZE,
                 color=SLATE, dim=GREY, cell=0.5):
        super().__init__()
        self.pattern = str(bits).replace(" ", "")
        self.cell = cell
        lanes = len(self.pattern)
        top = (lanes - 1) * pitch / 2

        self.left = self._end("A", -span, color, size, lanes, pitch)
        self.right = self._end("B", span, color, size, lanes, pitch)

        self.wires, self.bits = VGroup(), VGroup()
        for i, value in enumerate(self.pattern):
            y = top - i * pitch
            self.wires.add(Line([self.left.get_right()[0], y, 0],
                                [self.right.get_left()[0], y, 0],
                                color=dim, stroke_width=2.5))
            chip = self._bit(value, color, size)
            chip.move_to([-span / 2.6, y, 0])
            self.bits.add(chip)
        self.cell = cell
        self.add(self.wires, self.bits, self.left, self.right)

    def _end(self, name, x, color, size, lanes, pitch):
        height = max(1.3, lanes * pitch + 0.45)
        box = RoundedRectangle(width=1.3, height=height, corner_radius=0.1,
                               color=color, stroke_width=3,
                               fill_color=CREAM, fill_opacity=1)
        box.move_to([x, 0, 0])
        label = _caption(name, size, CHARCOAL, 1.0)
        label.move_to(box)
        return VGroup(box, label)

    def _bit(self, value, color, size):
        box = Rectangle(width=self.cell, height=self.cell, color=color,
                        stroke_width=2, fill_color=CREAM, fill_opacity=1)
        text = serif(value, size, CHARCOAL)
        if text.width > self.cell * 0.55:
            text.scale_to_fit_width(self.cell * 0.55)
        text.move_to(box)
        return VGroup(box, text)

    def lane_y(self, index):
        """A lane's height, read off the wire as it stands.

        Not stored at construction: the scene positions the diagram after
        building it, and a y captured beforehand puts every bit a third of
        a unit off its own wire.
        """
        return self.wires[index].get_center()[1]

    def arrival_x(self, clearance=0.35):
        """Where an in-step bit stops: short of the receiver, not inside it."""
        return self.right.get_left()[0] - self.cell / 2 - clearance

    def advance(self, to_x=None):
        """Send every bit off together — the tidy, in-step case."""
        to_x = self.arrival_x() if to_x is None else to_x
        return [chip.animate.move_to([to_x, self.lane_y(i), 0])
                for i, chip in enumerate(self.bits)]

    def skew(self, to_x=None, offsets=(0.0, -0.55, -1.15, -0.3)):
        """Arrive ragged. This is the whole argument against parallel.

        The offsets are negative — a skewed bit is *behind* the others, so
        it lands short of the receiver rather than inside it.
        """
        to_x = self.arrival_x() if to_x is None else to_x
        moves = []
        for i, chip in enumerate(self.bits):
            dx = offsets[i % len(offsets)]
            moves.append(chip.animate.move_to(
                [to_x + dx, self.lane_y(i), 0]))
        return moves

    def brace_skew(self, color=TERRACOTTA, stroke=2.5):
        """A dashed line through the arrival points, showing them unaligned."""
        xs = [chip.get_center()[0] for chip in self.bits]
        top = np.array([xs[0], self.lane_y(0) + 0.32, 0])
        bottom = np.array([xs[-1], self.lane_y(len(self.bits) - 1) - 0.32, 0])
        return DashedLine(top, bottom, color=color, stroke_width=stroke,
                          dash_length=0.12)


class DirectionLink(VGroup):
    """Two devices and the arrows between them: simplex to full duplex.

    One component for all three modes so the student sees the same two
    boxes each time and only the arrows change — which is the only thing
    that does change.
    """

    def __init__(self, left="DEVICE A", right="DEVICE B", span=3.6,
                 size=LABEL_SIZE, color=SLATE, lit=TERRACOTTA, dim=GREY,
                 gap=0.52):
        super().__init__()
        self.lit_color, self.dim_color = lit, dim

        self.left = self._end(left, -span, color, size)
        self.right = self._end(right, span, color, size)
        x0 = self.left.get_right()[0] + GAP_SM
        x1 = self.right.get_left()[0] - GAP_SM

        # Index 0 is left-to-right (the forward direction), index 1 is the
        # return path. Callers name them that way rather than by position.
        self.arrows = VGroup(
            Arrow([x0, gap, 0], [x1, gap, 0], color=dim, stroke_width=4,
                  buff=0, max_tip_length_to_length_ratio=0.07),
            Arrow([x1, -gap, 0], [x0, -gap, 0], color=dim, stroke_width=4,
                  buff=0, max_tip_length_to_length_ratio=0.07),
        )
        self.add(self.arrows, self.left, self.right)

    def _end(self, name, x, color, size):
        # Wide enough for RECEIVER at LABEL_SIZE without shrinking it.
        box = RoundedRectangle(width=3.1, height=1.25, corner_radius=0.12,
                               color=color, stroke_width=3,
                               fill_color=CREAM, fill_opacity=1)
        box.move_to([x, 0, 0])
        label = _caption(name, size, CHARCOAL, 2.7)
        label.move_to(box)
        return VGroup(box, label)

    def forward(self):
        return self.arrows[0]

    def back(self):
        return self.arrows[1]

    def light(self, indices):
        """Light the named directions, quiet the rest."""
        wanted = set(indices)
        return [arrow.animate.set_color(
                    self.lit_color if i in wanted else self.dim_color)
                for i, arrow in enumerate(self.arrows)]

    def label_arrow(self, index, text, size=MARGIN_SIZE, color=GREY,
                    buff=GAP_SM * 0.8):
        arrow = self.arrows[index]
        # The label sits clear above or below the boxes, so it may run wider
        # than the arrow it names; what it may not do is shrink below the
        # legibility floor to match a short arrow.
        label = _caption(text, size, color, FRAME_SAFE - 1.0)
        label.next_to(arrow, UP if index == 0 else DOWN, buff=buff)
        return label


# ---------------------------------------------------------------- parity


def parity_bit(bits, scheme="even"):
    """The bit that makes the total number of ones follow the scheme."""
    ones = str(bits).count("1")
    if scheme not in ("even", "odd"):
        raise ValueError(f"parity scheme must be even or odd, got {scheme!r}")
    if scheme == "even":
        return "0" if ones % 2 == 0 else "1"
    return "1" if ones % 2 == 0 else "0"


class ParityRow(VGroup):
    """Seven data bits and the parity bit that completes them.

    The parity bit is derived, not passed in, so the cell on screen is
    always the answer to the question being asked above it.
    """

    def __init__(self, data="1010110", scheme="even", cell=0.78,
                 size=LABEL_SIZE, color=CHARCOAL, accent=TERRACOTTA,
                 frame=SLATE, show_parity=True):
        super().__init__()
        self.data = str(data).replace(" ", "")
        self.scheme = scheme
        self.parity = parity_bit(self.data, scheme)
        self.cell = cell
        self.accent = accent

        self.cells, self.values = VGroup(), VGroup()
        pattern = self.data + (self.parity if show_parity else "")
        n = len(pattern)
        for i, value in enumerate(pattern):
            is_parity = show_parity and i == len(self.data)
            box = Rectangle(width=cell, height=cell,
                            color=accent if is_parity else frame,
                            stroke_width=3 if is_parity else 2)
            box.move_to([(i - (n - 1) / 2) * cell, 0, 0])
            text = serif(value, size, accent if is_parity else color)
            text.move_to(box)
            self.cells.add(box)
            self.values.add(text)
        self.add(self.cells, self.values)
        self.parity_index = len(self.data) if show_parity else None

    @property
    def ones(self):
        """Ones in the data bits alone — what the student counts first."""
        return self.data.count("1")

    @property
    def total(self):
        """Ones once the parity bit is in place."""
        return self.ones + (1 if self.parity == "1" else 0)

    def light_ones(self, color=None):
        color = color or self.accent
        return [self.values[i].animate.set_color(color)
                for i, b in enumerate(self.data) if b == "1"]

    def parity_cell(self):
        return VGroup(self.cells[self.parity_index],
                      self.values[self.parity_index])

    def label(self, text, size=MARGIN_SIZE, color=GREY, buff=GAP_SM):
        """A caption under the row, fitted to it."""
        label = _caption(text, size, color, self.width)
        label.next_to(self, DOWN, buff=buff)
        return label

    def bracket(self, start, stop, text, size=MARGIN_SIZE, color=GREY,
                buff=GAP_SM * 0.7):
        """Name a span of cells — 'data bits' against 'parity bit'."""
        left = self.cells[start].get_left()[0]
        right = self.cells[stop - 1].get_right()[0]
        y = self.cells[0].get_bottom()[1] - buff
        rule = Line([left, y, 0], [right, y, 0], color=color, stroke_width=2)
        label = _caption(text, size, color, max(1.2, right - left))
        label.next_to(rule, DOWN, buff=GAP_SM * 0.5)
        return VGroup(rule, label)

    def count_line(self, size=LABEL_SIZE, color=CHARCOAL, buff=GAP_MD):
        """'four ones, so even parity needs a 0' — built from the bits."""
        words = {0: "no", 1: "one", 2: "two", 3: "three", 4: "four",
                 5: "five", 6: "six", 7: "seven", 8: "eight"}
        text = (f"{words[self.ones]} ones  ->  {self.scheme} parity "
                f"needs  {self.parity}")
        label = _caption(text, size, color, FRAME_SAFE)
        label.next_to(self, DOWN, buff=buff)
        return label


class ParityBlock(VGroup):
    """Rows of bytes with a parity column and a parity row.

    Every parity bit is computed, including the corner, so flipping one
    data bit really does fail exactly one row check and one column check —
    the picture is doing the arithmetic rather than illustrating it.

    The corner is taken from the row-parity column. Under even parity that
    is the same bit the column-parity row would give, because each is the
    parity of the whole data block; under odd parity the two readings only
    agree when the block has the same number of rows as columns, modulo 2.
    Even parity is what the syllabus draws, and what the scene uses.
    """

    def __init__(self, rows, scheme="even", cell=0.62, size=MARGIN_SIZE,
                 color=CHARCOAL, frame=SLATE, accent=TERRACOTTA,
                 check=SAGE):
        super().__init__()
        self.rows_in = [str(r).replace(" ", "") for r in rows]
        self.scheme = scheme
        self.cell = cell
        self.accent, self.check_color = accent, check

        width = len(self.rows_in[0])
        if any(len(r) != width for r in self.rows_in):
            raise ValueError("every row of a parity block must be the same width")

        grid = [list(r) + [parity_bit(r, scheme)] for r in self.rows_in]
        columns = ["".join(r[c] for r in self.rows_in) for c in range(width)]
        parity_row = [parity_bit(c, scheme) for c in columns]
        # The corner closes both the row-parity column and the column-parity
        # row; both readings give the parity of the whole data block.
        parity_row.append(parity_bit("".join(grid[i][width]
                                             for i in range(len(grid))),
                                     scheme))
        grid.append(parity_row)
        self.grid = grid
        self.n_rows, self.n_cols = len(self.rows_in), width

        self.cells, self.values = {}, {}
        body = VGroup()
        for r, row in enumerate(grid):
            for c, value in enumerate(row):
                parity = r == self.n_rows or c == self.n_cols
                box = Rectangle(width=cell, height=cell,
                                color=frame if not parity else GREY,
                                stroke_width=2 if not parity else 1.8)
                box.move_to([(c - (len(row) - 1) / 2) * cell,
                             -(r - (len(grid) - 1) / 2) * cell, 0])
                text = serif(value, size, color if not parity else GREY)
                if text.width > cell * 0.52:
                    text.scale_to_fit_width(cell * 0.52)
                text.move_to(box)
                self.cells[(r, c)] = box
                self.values[(r, c)] = text
                body.add(box, text)
        self.add(body)

        # The parity column and row are furniture, not data — a light rule
        # separates them so the block reads as data plus its checks.
        self.rules = VGroup(
            Line(self.cells[(0, self.n_cols)].get_corner(UP + LEFT),
                 self.cells[(len(grid) - 1, self.n_cols)].get_corner(DOWN + LEFT),
                 color=GREY, stroke_width=2.5),
            Line(self.cells[(self.n_rows, 0)].get_corner(UP + LEFT),
                 self.cells[(self.n_rows, self.n_cols)].get_corner(UP + RIGHT),
                 color=GREY, stroke_width=2.5),
        )
        self.add(self.rules)

    # ------------------------------------------------------------- labels

    def side_label(self, text, size=MARGIN_SIZE, color=GREY,
                   buff=GAP_SM * 0.9):
        label = _caption(text, size, color, 3.0)
        label.next_to(self.cells[(0, self.n_cols)], UP, buff=buff)
        return label

    def flip(self, row, col):
        """Corrupt one data bit. Returns the animation that changes it."""
        if row >= self.n_rows or col >= self.n_cols:
            raise ValueError("flip a data bit, not a parity bit")
        was = self.grid[row][col]
        now = "0" if was == "1" else "1"
        self.grid[row][col] = now
        text = serif(now, self.values[(row, col)].font_size, self.accent)
        text.move_to(self.cells[(row, col)])
        self.values[(row, col)].become(text)
        return [self.cells[(row, col)].animate.set_stroke(self.accent,
                                                          width=3.5)]

    def row_check(self, row, color=None):
        """Highlight one row's cells — the check that now fails."""
        color = color or self.accent
        return [self.cells[(row, c)].animate.set_stroke(color, width=3)
                for c in range(self.n_cols + 1)]

    def col_check(self, col, color=None):
        color = color or self.accent
        return [self.cells[(r, col)].animate.set_stroke(color, width=3)
                for r in range(self.n_rows + 1)]

    def crosshair(self, row, col, color=None):
        """The cell where the failing row and column meet."""
        color = color or self.check_color
        box = Rectangle(width=self.cell, height=self.cell, color=color,
                        stroke_width=5)
        box.move_to(self.cells[(row, col)])
        return box


# ------------------------------------------------------------- handshake


class Handshake(VGroup):
    """A sender/receiver timeline: blocks down, acknowledgements back up.

    Automatic repeat request is a sequence, and sequence marks are lost by
    students who describe the parts without the order — so the component
    numbers its own steps and reveals them one at a time.

    Steps are (direction, label) with direction "down" for sender to
    receiver and "up" for receiver to sender.
    """

    def __init__(self, steps, span=3.0, height=4.2, size=MARGIN_SIZE,
                 color=SLATE, accent=TERRACOTTA, ok=SAGE, dim=GREY,
                 head_size=LABEL_SIZE):
        super().__init__()
        self.accent, self.ok_color = accent, ok

        self.heads = VGroup(
            _caption("SENDER", head_size, CHARCOAL, 2.6).move_to(
                [-span, height / 2 + GAP_MD * 0.9, 0]),
            _caption("RECEIVER", head_size, CHARCOAL, 2.6).move_to(
                [span, height / 2 + GAP_MD * 0.9, 0]),
        )
        self.spines = VGroup(
            DashedLine([-span, height / 2, 0], [-span, -height / 2, 0],
                       color=dim, stroke_width=2, dash_length=0.14),
            DashedLine([span, height / 2, 0], [span, -height / 2, 0],
                       color=dim, stroke_width=2, dash_length=0.14),
        )

        pitch = height / max(1, len(steps))
        self.arrows, self.labels, self.steps = VGroup(), VGroup(), VGroup()
        for i, (direction, text) in enumerate(steps):
            y = height / 2 - pitch * (i + 0.65)
            # Horizontal, not sloped. A sloped arrow passes straight through
            # its own label: the label is centred on the arrow's midpoint,
            # and at the label's left and right edges the line has risen or
            # fallen into the text. Order is carried by the numbering and by
            # the vertical sequence, which is what a sequence diagram does.
            if direction == "down":
                start, end = [-span, y, 0], [span, y, 0]
            elif direction == "up":
                start, end = [span, y, 0], [-span, y, 0]
            else:
                raise ValueError(f"direction must be up or down, got {direction!r}")
            arrow = Arrow(start, end, color=color, stroke_width=3.5, buff=0.1,
                          max_tip_length_to_length_ratio=0.045)
            label = _caption(f"{i + 1}.  {text}", size, CHARCOAL,
                             span * 2.14)
            label.next_to(arrow, UP, buff=GAP_SM * 0.5)
            self.arrows.add(arrow)
            self.labels.add(label)
            self.steps.add(VGroup(arrow, label))
        self.add(self.spines, self.heads, self.steps)

    def step(self, index):
        return self.steps[index]

    def hide_steps(self):
        """Hide the sequence, stroke-only, ready to be revealed in order.

        Stroke-only because set_opacity() fills as well, and because FadeIn
        interpolates towards a mobject's current state — anything hidden by
        opacity has to be restored before it is faded in or it fades from
        nothing to nothing.
        """
        for arrow, label in zip(self.arrows, self.labels):
            arrow.set_stroke(opacity=0)
            arrow.set_fill(opacity=0)
            label.set_opacity(0)
        return self

    def show_step(self, index):
        self.arrows[index].set_stroke(opacity=1)
        self.arrows[index].set_fill(opacity=1)
        self.labels[index].set_opacity(1)
        return self.steps[index]

    def light(self, index, color=None):
        color = color or self.accent
        return [self.arrows[index].animate.set_color(color),
                self.labels[index].animate.set_color(color)]

    def timer(self, index, text="timer running", size=MARGIN_SIZE,
              color=GREY, side=LEFT, buff=GAP_SM * 0.8):
        """A note beside one step — the timeout the sequence turns on."""
        label = _caption(text, size, color, 2.6)
        label.next_to(self.arrows[index].get_start(), side, buff=buff)
        half = FRAME_SAFE / 2
        if label.get_left()[0] < -half:
            label.shift(RIGHT * (-half - label.get_left()[0]))
        return label


# -------------------------------------------------------------- encryption


def key_glyph(color=TERRACOTTA, height=0.52, stroke=3):
    """A small key: ring, shaft, two teeth. Legible at caption scale."""
    ring = Circle(radius=height * 0.3, color=color, stroke_width=stroke)
    shaft = Line(ring.get_right(), ring.get_right() + RIGHT * height * 1.25,
                 color=color, stroke_width=stroke)
    teeth = VGroup(
        Line(shaft.get_end(), shaft.get_end() + DOWN * height * 0.38,
             color=color, stroke_width=stroke),
        Line(shaft.get_end() + LEFT * height * 0.32,
             shaft.get_end() + LEFT * height * 0.32 + DOWN * height * 0.28,
             color=color, stroke_width=stroke),
    )
    return VGroup(ring, shaft, teeth)


def labelled_key(text, color=TERRACOTTA, size=MARGIN_SIZE, height=0.52,
                 buff=GAP_SM * 0.7):
    key = key_glyph(color, height)
    label = _caption(text, size, color, 5.0)
    label.next_to(key, DOWN, buff=buff)
    return VGroup(key, label)


class EncryptLane(VGroup):
    """plaintext -> algorithm -> ciphertext, with the key above the box.

    Symmetric and asymmetric are the same lane with different keys, which
    is the comparison the syllabus wants: what changes is the key, not the
    pipeline.
    """

    def __init__(self, left="PLAINTEXT", middle="ENCRYPTION", right="CIPHERTEXT",
                 span=4.0, size=MARGIN_SIZE, color=SLATE, dim=GREY,
                 box_width=3.1, box_height=1.05):
        super().__init__()
        self.boxes, self.labels = VGroup(), VGroup()
        for i, name in enumerate((left, middle, right)):
            box = RoundedRectangle(width=box_width, height=box_height,
                                   corner_radius=0.1, color=color,
                                   stroke_width=3, fill_color=CREAM,
                                   fill_opacity=1)
            box.move_to([(i - 1) * span, 0, 0])
            label = _caption(name, size, CHARCOAL, box_width - GAP_SM * 1.2)
            label.move_to(box)
            self.boxes.add(box)
            self.labels.add(label)

        self.arrows = VGroup(*[
            Arrow(self.boxes[i].get_right(), self.boxes[i + 1].get_left(),
                  color=dim, stroke_width=3.5, buff=GAP_SM * 0.5,
                  max_tip_length_to_length_ratio=0.12)
            for i in range(2)
        ])
        self.add(self.arrows, self.boxes, self.labels)

    def key_slot(self, key, index=1, buff=GAP_MD * 0.8):
        """Hang a key over one box — the thing the algorithm needs."""
        key.next_to(self.boxes[index], UP, buff=buff)
        return key

    def light(self, index, color=TERRACOTTA):
        return [self.boxes[index].animate.set_stroke(color)]
