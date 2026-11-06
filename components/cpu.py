"""Processor furniture: the CPU, main memory, and the buses between them.

One picture carries this whole lesson. The processor sits on the left with
its registers visible, main memory sits on the right with its addresses
visible, and the three buses run across the gap. Every step of the
fetch-decode-execute cycle is then something moving along one of those
buses into one of those registers, so the student watches the same diagram
change rather than meeting a new drawing per stage.

Everything is sized for the 16:9 lecture frame as it stands, because a
diagram scaled to fit takes its captions with it: a 28px label inside a
group scaled to 0.9 renders at 25px and fails the mobile floor. So the
numbers here are chosen to fit at scale 1.0 and `measure()` at the bottom
of this file checks that they still do.

The register values are the one piece of mutable state. A register holds a
Text in its value slot and ``write()`` hands back a replacement positioned
on the same slot, so the scene plays ``Transform(reg.value, reg.write(...))``
and the diagram's geometry never shifts under it.

Positions are read off the mobjects at call time, never captured at
construction. A frame or a path built from coordinates taken when the group
was created points at where the group used to be the moment anything moves
it.
"""

import numpy as np

from manim import (
    Arrow,
    CurvedArrow,
    DoubleArrow,
    Line,
    Rectangle,
    RoundedRectangle,
    SurroundingRectangle,
    TAU,
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
    SAGE,
    SLATE,
    TERRACOTTA,
    mono,
    serif,
)

FRAME_SAFE = 12.6

# A register with nothing in it yet. An en dash reads as "empty" where a
# blank would read as "broken", and Pango gives a zero-width mobject for an
# empty string, which is awkward to Transform away from.
EMPTY = "–"


def fit(mobject, width=FRAME_SAFE):
    if mobject.width > width:
        mobject.scale_to_fit_width(width)
    return mobject


# ------------------------------------------------------------------ registers


class RegisterBox(VGroup):
    """One register: its name on the left, its contents on the right.

    Both inside a single rectangle rather than a two-cell grid — four of
    these stack inside the CPU and every extra rule is a line the eye has
    to discount.

    The default width holds the widest thing a register carries in this
    lesson, which is a whole instruction: "CIR" and "ADD 2040" side by side
    need every bit of it. A narrower box puts the name and the contents on
    top of each other, which looks like a rendering fault rather than a
    layout one.
    """

    def __init__(self, name, value=None, width=3.6, height=0.58,
                 size=LABEL_SIZE, color=SLATE, pad=0.16):
        super().__init__()
        self.size, self.pad = size, pad
        self.box = Rectangle(width=width, height=height, color=color,
                             stroke_width=2.5)
        self.label = mono(name, size, CHARCOAL)
        self.label.move_to(self.box.get_left() + RIGHT * pad,
                           aligned_edge=LEFT)
        self.value = self._slot(value)
        self.add(self.box, self.label, self.value)

    def _slot(self, value, color=None):
        text = EMPTY if value is None else str(value)
        shade = color or (GREY if value is None else CHARCOAL)
        slot = mono(text, self.size, shade)
        slot.move_to(self.box.get_right() + LEFT * self.pad,
                     aligned_edge=RIGHT)
        return slot

    def write(self, value, color=None):
        """A replacement for the value slot, on the same slot. For Transform."""
        return self._slot(value, color)

    def light(self, color=TERRACOTTA):
        return self.box.animate.set_color(color)

    def settle(self, color=SLATE):
        return self.box.animate.set_color(color)

    def frame(self, color=TERRACOTTA, buff=GAP_SM * 0.35):
        """A ring around this register, built from where it is now."""
        return SurroundingRectangle(self.box, color=color, buff=buff,
                                    stroke_width=3.5)


def unit_box(lines, width=2.3, height=1.12, size=MARGIN_SIZE, color=SLATE,
             text_color=CHARCOAL):
    """A named functional unit inside the CPU — the CU or the ALU."""
    body = VGroup(*[serif(line, size, text_color) for line in lines])
    body.arrange(DOWN, buff=GAP_SM * 0.3)
    box = Rectangle(width=width, height=height, color=color, stroke_width=2.5)
    body.move_to(box)
    return VGroup(box, body)


class CpuBlock(VGroup):
    """The processor: a register bank on the left, the CU and ALU on the right.

    ``registers`` is a list of names, or of (name, value) pairs. The block's
    height follows the register count so the bank always clears the walls.
    """

    def __init__(self, registers, centre=(-3.68, -0.25), width=6.7,
                 reg_width=3.6, reg_height=0.58, size=LABEL_SIZE,
                 units=(("Control", "unit"), ("Arithmetic", "logic unit")),
                 color=GREY, reg_color=SLATE, caption="CPU"):
        super().__init__()
        rows = [(r, None) if isinstance(r, str) else r for r in registers]

        self.regs = {}
        self.bank = VGroup()
        for name, value in rows:
            reg = RegisterBox(name, value, width=reg_width,
                              height=reg_height, size=size, color=reg_color)
            self.regs[name] = reg
            self.bank.add(reg)
        self.bank.arrange(DOWN, buff=GAP_SM * 0.55)

        self.units = VGroup(*[unit_box(lines, width=width - reg_width - 0.95)
                              for lines in units])
        self.units.arrange(DOWN, buff=GAP_SM * 1.15)

        self.caption = serif(caption, size, GREY)
        # The walls follow the contents: a caption band across the top, the
        # taller of the two columns below it, and the same pad underneath.
        inner = max(self.bank.height, self.units.height)
        band = self.caption.height + GAP_SM * 1.5
        pad = GAP_SM * 1.1
        height = band + inner + pad

        self.box = Rectangle(width=width, height=height, color=color,
                             stroke_width=2)
        self.box.move_to([centre[0], centre[1], 0])

        top_left = self.box.get_corner(UP + LEFT)
        self.caption.move_to(
            [top_left[0] + 0.22, top_left[1] - band / 2, 0],
            aligned_edge=LEFT,
        )

        body_top = top_left[1] - band
        self.bank.move_to([top_left[0] + 0.25 + self.bank.width / 2,
                           body_top - self.bank.height / 2, 0])
        self.units.move_to([self.box.get_right()[0] - 0.3
                            - self.units.width / 2,
                            body_top - inner / 2, 0])

        self.cu, self.alu = self.units[0], self.units[1]
        self.add(self.box, self.caption, self.bank, self.units)

    def reg(self, name):
        return self.regs[name]

    def value(self, name):
        return self.regs[name].value

    def write(self, name, value, color=None):
        return self.regs[name].write(value, color)


# -------------------------------------------------------------------- memory


class MemoryColumn(VGroup):
    """Main memory as addressed rows: the address, then what is stored there.

    A row whose address is None is drawn as a vertical ellipsis — the gap
    between address 1001 and address 2040 is thousands of locations, and
    pretending they are adjacent is the kind of quiet lie a student later
    has to unlearn.
    """

    def __init__(self, rows, centre=(5.3, -0.25), width=3.5,
                 row_height=0.8, addr_col=1.25, size=LABEL_SIZE,
                 title="Main memory", color=GREY, rule=GREY):
        super().__init__()
        self.size = size
        self.rows = list(rows)
        height = row_height * len(self.rows)

        self.box = Rectangle(width=width, height=height, color=color,
                             stroke_width=2)
        self.box.move_to([centre[0], centre[1], 0])
        left = self.box.get_left()[0]
        top = self.box.get_top()[1]

        self.divider = Line([left + addr_col, top, 0],
                            [left + addr_col, top - height, 0],
                            color=rule, stroke_width=1.5)

        self.rules = VGroup()
        self.addresses, self.values, self.centres = {}, {}, {}
        body = VGroup()
        for i, (addr, content) in enumerate(self.rows):
            y = top - row_height * (i + 0.5)
            if i:
                self.rules.add(Line([left, top - row_height * i, 0],
                                    [left + width, top - row_height * i, 0],
                                    color=rule, stroke_width=1.5))
            if addr is None:
                dots = mono("⋮", size, GREY)
                dots.move_to([left + addr_col / 2, y, 0])
                body.add(dots)
                continue
            key = str(addr)
            tag = mono(key, size, GREY)
            tag.move_to([left + addr_col / 2, y, 0])
            slot = self._slot(content, [left + addr_col, y, 0], width - addr_col)
            self.addresses[key] = tag
            self.values[key] = slot
            self.centres[key] = np.array([left + width / 2, y, 0])
            body.add(tag, slot)

        self.title = serif(title, size, GREY)
        self.title.next_to(self.box, UP, buff=GAP_SM * 1.1)
        self.add(self.box, self.divider, self.rules, body, self.title)

    def _slot(self, content, cell_left, cell_width, color=CHARCOAL):
        text = EMPTY if content is None else str(content)
        slot = mono(text, self.size, GREY if content is None else color)
        slot.move_to([cell_left[0] + cell_width / 2, cell_left[1], 0])
        return slot

    def value(self, addr):
        return self.values[str(addr)]

    def write(self, addr, content, color=CHARCOAL):
        """A replacement for one cell's contents, on the same cell."""
        slot = self.values[str(addr)]
        nxt = mono(str(content), self.size, color)
        nxt.move_to(slot)
        return nxt

    def frame(self, addr, color=TERRACOTTA, buff=GAP_SM * 0.3):
        """A ring around one row, measured now rather than at construction."""
        row = VGroup(self.addresses[str(addr)], self.values[str(addr)])
        return SurroundingRectangle(row, color=color, buff=buff,
                                    stroke_width=3.5)


# ---------------------------------------------------------------------- buses


class BusSet(VGroup):
    """The three buses, drawn across the gap between processor and memory.

    Labels sit above their line and payloads travel along it, so the two
    never share space. The lines are plain until the lesson is about the
    buses themselves, when ``arrow()`` lays direction over one of them.
    """

    def __init__(self, left_x, right_x, centre_y=-0.25, spread=1.1,
                 labels=("Address bus", "Data bus", "Control bus"),
                 size=MARGIN_SIZE, color=GREY, stroke=2.5):
        super().__init__()
        # Spread about the diagram's own centre, not about y = 0: the outer
        # buses have to meet the memory column, and a bus that stops short
        # of the box it connects to is a drawing of something else.
        ys = [centre_y + spread, centre_y, centre_y - spread]
        self.lines, self.captions = VGroup(), VGroup()
        for y, text in zip(ys, labels):
            line = Line([left_x, y, 0], [right_x, y, 0], color=color,
                        stroke_width=stroke)
            cap = serif(text, size, GREY)
            cap.next_to(line, UP, buff=GAP_SM * 1.2)
            self.lines.add(line)
            self.captions.add(cap)
        self.add(self.lines, self.captions)

    def line(self, index):
        return self.lines[index]

    def caption(self, index):
        return self.captions[index]

    def _ends(self, index, reverse, inset):
        """Where a payload starts and stops: short of both boxes.

        A chip that travels the full line ends with its centre on the
        memory column's edge and half of itself inside, printed across the
        address it has just been sent to look up. So the journey stops
        short at both ends, and the gap reads as the payload arriving.
        """
        line = self.lines[index]
        start = line.get_start() + RIGHT * inset
        end = line.get_end() - RIGHT * inset
        return (end, start) if reverse else (start, end)

    def path(self, index, reverse=False, inset=0.95):
        """A path along one bus, measured now. For MoveAlongPath."""
        start, end = self._ends(index, reverse, inset)
        return Line(start, end)

    def chip(self, index, text, color=TERRACOTTA, reverse=False,
             size=MARGIN_SIZE, pad=0.13, inset=0.95):
        """A payload sitting at one end of a bus, ready to travel."""
        label = mono(str(text), size, color)
        box = RoundedRectangle(
            corner_radius=0.08,
            width=label.width + pad * 2.6,
            height=label.height + pad * 1.9,
            color=color,
            stroke_width=2.5,
        )
        chip = VGroup(box, label)
        label.move_to(box)
        chip.move_to(self._ends(index, reverse, inset)[0])
        return chip

    def arrow(self, index, two_way=False, color=TERRACOTTA, reverse=False,
              stroke=4, tip=0.22):
        """Direction, laid over one bus."""
        line = self.lines[index]
        start, end = line.get_start(), line.get_end()
        if reverse:
            start, end = end, start
        maker = DoubleArrow if two_way else Arrow
        return maker(start, end, color=color, stroke_width=stroke,
                     buff=0, max_tip_length_to_length_ratio=tip / 4,
                     tip_length=tip)


# ------------------------------------------------------------- system picture


class SystemView(VGroup):
    """CPU between input/output and main memory, the way the chapter draws it.

    Memory is on the right because that is where it stays for the rest of
    the lesson — the trace diagram grows out of this one, so the two must
    not disagree about which side anything is on.
    """

    def __init__(self, width=3.0, height=1.35, gap=1.25, size=MARGIN_SIZE,
                 color=SLATE, boxes=(("Input and", "output"), ("CPU",),
                                     ("Main memory",))):
        super().__init__()
        self.boxes = VGroup(*[unit_box(lines, width=width, height=height,
                                       size=size, color=color)
                              for lines in boxes])
        self.boxes.arrange(RIGHT, buff=gap)
        self.links = VGroup()
        for left, right in zip(self.boxes, self.boxes[1:]):
            self.links.add(DoubleArrow(left.get_right(), right.get_left(),
                                       color=GREY, stroke_width=3, buff=0.12,
                                       tip_length=0.2))
        self.add(self.boxes, self.links)
        self.io, self.cpu, self.memory = self.boxes[0], self.boxes[1], self.boxes[2]


class CycleRing(VGroup):
    """FETCH, DECODE, EXECUTE, and the arrow back to the start.

    The loop is the point of the picture: a student who can name the three
    stages but not say what follows EXECUTE has not understood the cycle.
    """

    def __init__(self, labels=("FETCH", "DECODE", "EXECUTE"), width=2.9,
                 height=0.95, gap=0.9, size=LABEL_SIZE, color=SLATE,
                 lit=TERRACOTTA, repeat="repeat"):
        super().__init__()
        self.lit_color, self.dim_color = lit, color
        self.cards = VGroup()
        for text in labels:
            box = Rectangle(width=width, height=height, color=color,
                            stroke_width=3)
            label = serif(text, size, CHARCOAL)
            label.move_to(box)
            self.cards.add(VGroup(box, label))
        self.cards.arrange(RIGHT, buff=gap)

        self.arrows = VGroup()
        for left, right in zip(self.cards, self.cards[1:]):
            self.arrows.add(Arrow(left.get_right(), right.get_left(),
                                  color=GREY, stroke_width=3.5, buff=0.1,
                                  tip_length=0.2))

        # The return arc has to bow DOWNWARD, under the three cards. A
        # positive angle here sweeps it up and straight through the middle
        # card, which reads as a line struck through DECODE.
        first, last = self.cards[0], self.cards[-1]
        self.loop = CurvedArrow(last.get_bottom() + DOWN * 0.12,
                                first.get_bottom() + DOWN * 0.12,
                                angle=-TAU / 7, color=GREY, stroke_width=3.5,
                                tip_length=0.2)
        self.loop_label = serif(repeat, MARGIN_SIZE, GREY)
        self.loop_label.next_to(self.loop, DOWN, buff=GAP_SM * 0.5)
        self.add(self.cards, self.arrows, self.loop, self.loop_label)

    def light(self, index):
        return self.cards[index][0].animate.set_color(self.lit_color)

    def settle(self, index):
        return self.cards[index][0].animate.set_color(self.dim_color)


# --------------------------------------------------------------- small pieces


def rtn(line, size=LABEL_SIZE, color=CHARCOAL):
    """One line of register-transfer notation, in the mono family.

    Monospace because the notation is read symbol by symbol and the arrow
    has to line up with the arrow on the line above it.
    """
    return mono(line, size, color)


def given_block(rows, size=LABEL_SIZE, color=CHARCOAL, accent=SLATE,
                width=FRAME_SAFE, title=None):
    """The state a trace starts from, boxed. Left-aligned: it is a list."""
    body = VGroup(*[mono(row, size, color) for row in rows])
    body.arrange(DOWN, buff=GAP_SM * 0.65, aligned_edge=LEFT)
    if title is not None:
        head = serif(title, size, GREY)
        body = VGroup(head, body).arrange(DOWN, buff=GAP_SM * 1.1,
                                          aligned_edge=LEFT)
    fit(body, width - 0.6)
    box = SurroundingRectangle(body, color=accent, buff=GAP_SM * 1.15,
                               stroke_width=2.5)
    return fit(VGroup(box, body), width)


def role_rows(pairs, size=LABEL_SIZE, name_color=CHARCOAL, role_color=GREY,
              gap=GAP_MD, width=FRAME_SAFE):
    """'PC — address of the next instruction': a name against what it holds.

    The names are monospace and the roles are prose, which is the honest
    distinction: one is notation the exam expects back verbatim, the other
    is an explanation in the student's own words.
    """
    names = [mono(name, size, name_color) for name, _ in pairs]
    widest = max(n.width for n in names)
    rows = VGroup()
    for name, (_, role) in zip(names, pairs):
        text = serif(role, size, role_color)
        text.move_to(name.get_left() + RIGHT * (widest + gap),
                     aligned_edge=LEFT)
        rows.add(VGroup(name, text))
    rows.arrange(DOWN, buff=GAP_SM * 1.25, aligned_edge=LEFT)
    return fit(rows, width)


def strike(mobject, color=GREY, stroke=3):
    """A line through a claim that is wrong. Built from where it is now."""
    return Line(mobject.get_left() + LEFT * 0.08,
                mobject.get_right() + RIGHT * 0.08,
                color=color, stroke_width=stroke)


def tick_line(text, size=LABEL_SIZE, color=SAGE):
    return serif(text, size, color)


# ------------------------------------------------------------------- measuring


def measure():
    """Print the geometry this module promises, so the promise is checkable.

    Run as ``python -m components.cpu`` from the repo root. It renders
    nothing: it builds the diagram the lesson uses and reports whether it
    sits inside the frame with its captions at full size.
    """
    from manim import config

    half_w, half_h = config.frame_width / 2, config.frame_height / 2
    cpu = CpuBlock([("PC", 1000), ("MAR", 2040), ("MDR", 7),
                    ("CIR", "ADD 2040")])
    memory = MemoryColumn([(1000, "ADD 2040"), (1001, "..."), (None, None),
                           (2040, 7)])
    buses = BusSet(cpu.box.get_right()[0], memory.box.get_left()[0])

    print(f"frame            {config.frame_width:.3f} x {config.frame_height:.3f}")
    for name, group in (("cpu", cpu), ("memory", memory), ("buses", buses)):
        left, right = group.get_left()[0], group.get_right()[0]
        bottom, top = group.get_bottom()[1], group.get_top()[1]
        ok = (left > -half_w and right < half_w
              and bottom > -half_h and top < half_h)
        print(f"{name:8} x [{left:6.2f}, {right:6.2f}]  "
              f"y [{bottom:6.2f}, {top:6.2f}]  {'ok' if ok else 'OFF FRAME'}")
    gap = memory.box.get_left()[0] - cpu.box.get_right()[0]
    print(f"bus run  {gap:.2f} units between processor and memory")
    widest = max(buses.captions, key=lambda c: c.width)
    print(f"widest bus caption {widest.width:.2f} units")

    # Each bus has to arrive inside both boxes it joins. A line that stops
    # above the memory column is a picture of a bus connected to nothing.
    for i, line in enumerate(buses.lines):
        y = line.get_start()[1]
        inside = (memory.box.get_bottom()[1] < y < memory.box.get_top()[1]
                  and cpu.box.get_bottom()[1] < y < cpu.box.get_top()[1])
        print(f"bus {i} at y {y:6.2f}  "
              f"{'meets both boxes' if inside else 'MISSES A BOX'}")

    # The captions must clear the line above them and the memory's title.
    for i, cap in enumerate(buses.captions):
        above = buses.lines[i - 1].get_start()[1] if i else None
        clear = above is None or cap.get_top()[1] < above - 0.05
        print(f"caption {i} top {cap.get_top()[1]:6.2f}  "
              f"{'clear' if clear else 'TOUCHES THE BUS ABOVE'}")
    title_clash = (buses.captions[0].get_right()[0] > memory.title.get_left()[0]
                   and buses.captions[0].get_top()[1]
                   > memory.title.get_bottom()[1])
    print(f"memory title {'CLASHES with the address caption' if title_clash else 'clear'}")

    # A register has to hold its own name and its widest contents side by
    # side. "CIR" against "ADD 2040" is the pair that decides the width.
    for name, reg in cpu.regs.items():
        gap = reg.value.get_left()[0] - reg.label.get_right()[0]
        print(f"register {name:4} name-to-value gap {gap:5.2f}  "
              f"{'ok' if gap > 0.1 else 'NAME AND VALUE COLLIDE'}")

    # And a payload must stop before it prints over the address it was
    # sent to fetch.
    chip = buses.chip(1, "ADD 2040", reverse=True)
    ride = buses.path(1, reverse=True)
    landed = chip.copy().move_to(ride.get_end())
    print(f"data chip {chip.width:.2f} wide; lands with its right edge at "
          f"{landed.get_right()[0]:5.2f}, memory starts at "
          f"{memory.box.get_left()[0]:.2f}  "
          f"{'ok' if landed.get_right()[0] < memory.box.get_left()[0] else 'RUNS INTO MEMORY'}")
    out = buses.chip(0, "1000")
    print(f"address chip leaves with its left edge at "
          f"{out.get_left()[0]:5.2f}, the processor ends at "
          f"{cpu.box.get_right()[0]:.2f}  "
          f"{'ok' if out.get_left()[0] > cpu.box.get_right()[0] else 'STARTS INSIDE THE CPU'}")


if __name__ == "__main__":
    measure()
