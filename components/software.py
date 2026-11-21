"""Chapter 4 drawn: the start-up order, the interrupt, and the translators.

Topic 4.1 and 4.2 of Cambridge O Level 2210 are mostly definitions and
comparisons, and a comparison read aloud is a comparison half-remembered.
Each one here becomes a shape, and the shapes that already existed for the
operating-system lectures are reused rather than redrawn:

  * ``SortBench``    (components.os_shape) system against application
  * ``FunctionList`` (components.os_shape) the nine functions, one lit
  * ``LayerStack``   (components.os_shape) a request on its way down
  * ``make_table``   (components.table)    compiler against interpreter

What this file adds is the six figures those lectures had no need for:

  * ``BootStack``        the start-up order, built from the hardware up.
                         Deliberately the same stack as ``LayerStack`` and
                         deliberately the other way round: at start-up the
                         firmware acts first and the application last,
                         which is the reverse of the order a running
                         request travels. Drawing both as one stack and
                         animating the arrows in opposite directions is
                         the point, not a coincidence.
  * ``PollVsSignal``     the processor asking every device in turn, and
                         then the device speaking up instead. This is the
                         only honest answer to "why do computers need
                         interrupts", and the syllabus asks for it.
  * ``InterruptTimeline`` the five steps as one picture: the program's own
                         timeline broken, the routine run above the break,
                         the state lifted out and put back, and the
                         program carrying on from the same point. The
                         saved-state card is the whole idea -- a student
                         who can see it leave and return does not write
                         that the original program is abandoned.
  * ``Ladder``           high-level and low-level as two ends of one axis,
                         with what each end buys written at that end.
  * ``CodeBlock``        mono lines that light one at a time, with the
                         indentation intact.
  * ``TranslatorFlow``   source, translator, and what comes out -- which
                         for an interpreter is nothing, and the figure has
                         to be able to say so.
  * ``IDEWindow``        an editor with a gutter and a diagnostics strip,
                         so an IDE feature can be pointed at rather than
                         only named.

Sized for the 14.22 x 8 landscape frame at scale 1.0, like every other
figure in this repo: nothing here is built to be scaled down by a scene,
because a figure at 0.9 takes its 28px labels to 25px and fails the
mobile legibility gate for a saving nobody asked for. Where a label will
not fit these raise rather than shrink, so the fix is a shorter label and
never a quietly illegible frame.

``measure()`` prints every figure's extents and its smallest label; run it
as ``python -m components.software`` from the repo root after any change.
"""

from manim import (
    Arrow,
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

# The start-up order, bottom first. The wording is the lecture's own, and
# the order is the one the syllabus asks a student to reproduce.
BOOT_LAYERS = [
    "Application software",
    "Operating system",
    "Bootloader",
    "Firmware",
    "Hardware",
]


def _char_width(size):
    """One monospace character, measured rather than assumed."""
    return mono("M" * 20, size).width / 20.0


class CodeBlock(VGroup):
    """Monospace lines that light one at a time, indentation intact.

    Handing each line to Pango separately and arranging them left-aligned
    silently strips the indentation, because a mobject's bounding box is
    its ink and a leading space is not ink. The usual fix is to hand Pango
    the whole block as one ``Text`` with newlines, but then there are no
    separate lines to light, and an interpreter that cannot light one line
    at a time cannot be told apart from a compiler on screen.

    So the indentation is measured instead: each line is stripped, and
    shifted right by its own leading spaces times the width of one
    character. The result lines up exactly and stays addressable.
    """

    def __init__(self, lines, size=MARGIN_SIZE, color=CHARCOAL,
                 gutter=False, lit=TERRACOTTA, dim=GREY, width=FRAME_SAFE,
                 leading=GAP_SM * 1.25):
        super().__init__()
        self.lit_color, self.rest_color = lit, color
        self.lines, self.numbers = VGroup(), VGroup()
        step = _char_width(size)

        for index, text in enumerate(lines):
            body = mono(text.strip() or " ", size, color)
            indent = len(text) - len(text.lstrip(" "))
            body.move_to([indent * step, -index * (body.height + leading), 0],
                         aligned_edge=LEFT)
            self.lines.add(body)

        # Every line is placed from one origin rather than next to the one
        # above, so a line of only x-height characters cannot float: the
        # row pitch is the first line's height, not each line's own.
        pitch = self.lines[0].height + leading
        for index, body in enumerate(self.lines):
            body.move_to([body.get_left()[0], -index * pitch, 0],
                         aligned_edge=LEFT)

        if gutter:
            for index, body in enumerate(self.lines):
                number = mono(f"{index + 1}", size, dim)
                number.move_to([-GAP_MD, body.get_center()[1], 0],
                               aligned_edge=RIGHT)
                self.numbers.add(number)
            self.add(self.numbers)

        self.add(self.lines)
        self.move_to(ORIGIN)
        if self.width > width:
            raise ValueError(
                f"The code block is {self.width:.2f} units wide at size "
                f"{size}, over the {width:.2f} the frame allows. Shorten "
                "the longest line rather than scaling the block down."
            )

    def light(self, index, color=None):
        """Light one line and send the rest back to where they started."""
        color = self.lit_color if color is None else color
        return [body.animate.set_color(color if i == index
                                       else self.rest_color)
                for i, body in enumerate(self.lines)]

    def light_all(self, color=None):
        color = self.lit_color if color is None else color
        return [body.animate.set_color(color) for body in self.lines]

    def settle(self):
        return [body.animate.set_color(self.rest_color)
                for body in self.lines]


class BootStack(VGroup):
    """The start-up order as one stack, read from the hardware up.

    ``starts`` hands back the arrows in start-up order, bottom to top:
    the firmware acts first and the application last.

    There is deliberately no method here for the other direction. Drawing
    a running request as downward arrows over these same five boxes would
    be neat and would be wrong -- it would say a request to save a file
    travels through the bootloader, which stops running once the
    operating system is loaded. The request path is a different stack
    with a device driver in it and no bootloader, and it is drawn by
    ``LayerStack`` in components.os_shape.
    """

    def __init__(self, layers=None, width=6.6, height=0.8, gap=0.58,
                 size=LABEL_SIZE, color=SLATE, fill=0.1):
        super().__init__()
        layers = BOOT_LAYERS if layers is None else layers
        self.boxes, self.labels = VGroup(), VGroup()

        for name in layers:
            box = Rectangle(width=width, height=height, color=color,
                            stroke_width=2.5)
            box.set_fill(color, opacity=fill)
            label = serif(name, size, CHARCOAL)
            if label.width > width - GAP_MD:
                raise ValueError(
                    f"Layer {name!r} is {label.width:.2f} units wide in a "
                    f"{width:.2f}-unit box. Shorten it."
                )
            self.boxes.add(box)
            self.labels.add(label)

        self.boxes.arrange(DOWN, buff=gap)
        for box, label in zip(self.boxes, self.labels):
            label.move_to(box)
        self.add(self.boxes, self.labels)

        # Arrow geometry: the head is a fraction of the shaft, so a tight
        # gap draws a line with no visible point. Both numbers are set for
        # a gap of about half a unit and were checked by eye at 1080p.
        self.up = VGroup()
        for upper, lower in zip(self.boxes, self.boxes[1:]):
            self.up.add(Arrow(lower.get_top(), upper.get_bottom(),
                              color=SAGE, stroke_width=4.5, buff=0.04,
                              max_tip_length_to_length_ratio=0.5))
        # In the group for the same reason as PollVsSignal's: a scene
        # shifts this stack sideways to make room for commentary, and
        # arrows left out of the group would stay where they were built.
        self.add(self.up)

    def starts(self):
        """The upward arrows, in start-up order: firmware first."""
        return list(self.up)[::-1]

    def row(self, index):
        return VGroup(self.boxes[index], self.labels[index])

    def light(self, index, color=TERRACOTTA):
        return [self.boxes[index].animate.set_stroke(color)
                .set_fill(color, opacity=0.14),
                self.labels[index].animate.set_color(color)]

    def settle(self, index, color=SLATE):
        return [self.boxes[index].animate.set_stroke(color)
                .set_fill(color, opacity=0.1),
                self.labels[index].animate.set_color(CHARCOAL)]


class PollVsSignal(VGroup):
    """One processor, three devices, and the two ways they can talk.

    ``asks`` is the processor going round every device in turn to ask
    whether it needs anything, which is the waste the syllabus wants
    named. ``signal`` is one device raising an interrupt instead. The
    figure is built once and the arrows are swapped, because the contrast
    is the lesson.
    """

    def __init__(self, devices=("Keyboard", "Printer", "Network"),
                 size=MARGIN_SIZE, box=2.9, height=0.82, gap=GAP_SM * 1.6):
        super().__init__()
        self.cpu_box = Rectangle(width=3.0, height=1.25, color=SLATE,
                                 stroke_width=2.5)
        self.cpu_box.set_fill(SLATE, opacity=0.12)
        self.cpu_label = serif("Processor", size, CHARCOAL)
        self.cpu_box.move_to([-3.7, 0, 0])
        self.cpu_label.move_to(self.cpu_box)
        self.cpu = VGroup(self.cpu_box, self.cpu_label)

        self.boxes, self.labels = VGroup(), VGroup()
        for name in devices:
            frame = Rectangle(width=box, height=height, color=GREY,
                              stroke_width=2.5)
            frame.set_fill(GREY, opacity=0.08)
            label = serif(name, size, CHARCOAL)
            if label.width > box - GAP_SM * 1.4:
                raise ValueError(
                    f"Device {name!r} is {label.width:.2f} units wide in a "
                    f"{box:.2f}-unit box.")
            self.boxes.add(frame)
            self.labels.add(label)
        self.boxes.arrange(DOWN, buff=gap)
        self.boxes.move_to([3.3, 0, 0])
        for frame, label in zip(self.boxes, self.labels):
            label.move_to(frame)

        self.add(self.cpu, self.boxes, self.labels)

        self.asks = VGroup(*[
            Arrow(self.cpu_box.get_right(), frame.get_left(), color=GREY,
                  stroke_width=3.0, buff=0.08,
                  max_tip_length_to_length_ratio=0.35)
            for frame in self.boxes])
        self.signal = Arrow(self.boxes[0].get_left(),
                            self.cpu_box.get_right(), color=TERRACOTTA,
                            stroke_width=4.5, buff=0.08,
                            max_tip_length_to_length_ratio=0.35)
        # The arrows join the group so that moving the figure moves them
        # too. They are still drawn only when a scene plays them: being a
        # member of a group that was never added to the scene puts nothing
        # on screen.
        self.add(self.asks, self.signal)

    def device(self, index):
        return VGroup(self.boxes[index], self.labels[index])

    def light_device(self, index, color=TERRACOTTA):
        return [self.boxes[index].animate.set_stroke(color)
                .set_fill(color, opacity=0.14),
                self.labels[index].animate.set_color(color)]


class InterruptTimeline(VGroup):
    """The five steps as one picture, around the break in a program.

    Reading left to right: the program runs, an interrupt arrives, the
    current instruction is allowed to finish, the state is lifted out onto
    a card, the routine runs above the break, the card goes back, and the
    program carries on from the same point.

    Everything is handed back rather than added, so each piece can land on
    the beat that names it. The card is the one part worth insisting on:
    a student who watches it leave and come back does not write that the
    interrupted program is discarded, which is the marked error here.
    """

    def __init__(self, size=MARGIN_SIZE, span=10.6, break_half=1.35,
                 bar=0.2):
        super().__init__()
        left, right = -span / 2, span / 2

        def rail(x0, x1, color=SLATE):
            piece = Rectangle(width=x1 - x0, height=bar, stroke_width=0)
            piece.set_fill(color, opacity=1)
            piece.move_to([(x0 + x1) / 2, 0, 0])
            return piece

        self.before = rail(left, -break_half)
        self.after = rail(break_half, right)
        self.gap_marks = VGroup(
            Line([-break_half, -bar * 1.6, 0], [-break_half, bar * 1.6, 0],
                 color=CHARCOAL, stroke_width=3),
            Line([break_half, -bar * 1.6, 0], [break_half, bar * 1.6, 0],
                 color=CHARCOAL, stroke_width=3),
        )

        self.isr_box = RoundedRectangle(width=break_half * 2.1, height=0.95,
                                        corner_radius=0.1, color=TERRACOTTA,
                                        stroke_width=2.5)
        self.isr_box.set_fill(TERRACOTTA, opacity=0.12)
        self.isr_box.move_to([0, 1.72, 0])
        self.isr_label = serif("I S R", size, TERRACOTTA)
        self.isr_label.move_to(self.isr_box)
        self.isr = VGroup(self.isr_box, self.isr_label)

        self.into = Arrow([-break_half, bar, 0], self.isr_box.get_left(),
                          color=TERRACOTTA, stroke_width=3.5, buff=0.06,
                          max_tip_length_to_length_ratio=0.4)
        self.out_of = Arrow(self.isr_box.get_right(), [break_half, bar, 0],
                            color=TERRACOTTA, stroke_width=3.5, buff=0.06,
                            max_tip_length_to_length_ratio=0.4)

        self.running = serif("the program runs", size, GREY)
        self.running.move_to([self.before.get_center()[0],
                              -bar - GAP_MD, 0])
        # Short on purpose. The sentence that matters -- that the program
        # carries on from the same point and was never discarded -- is the
        # scene's caption, where it has the width to be said properly. A
        # label under a rail only has to name the rail.
        self.resumes = serif("resumes here", size, SAGE)
        self.resumes.move_to([self.after.get_center()[0], -bar - GAP_MD, 0])
        for label, rail in ((self.running, self.before),
                            (self.resumes, self.after)):
            if label.width > rail.width + GAP_MD:
                raise ValueError(
                    f"The label {label!r} is {label.width:.2f} units wide "
                    f"under a rail only {rail.width:.2f} wide.")

        flag_x = -break_half - 0.95
        self.flag_line = Line([flag_x, bar * 1.1, 0], [flag_x, 1.25, 0],
                              color=CHARCOAL, stroke_width=2.5)
        self.flag_label = serif("interrupt", size, CHARCOAL)
        # Beside the mark, not above it. Centred above, the label's right
        # half runs under the ISR box -- which the acceptance check cannot
        # see, because it compares text against text and a box is a shape.
        # Only a frame pulled from the finished render shows it.
        self.flag_label.move_to([flag_x - GAP_SM * 0.7, 0.72, 0],
                                aligned_edge=RIGHT)
        self.flag = VGroup(self.flag_line, self.flag_label)

        rows = ["where it had reached", "the data it was using"]
        body = VGroup(*[serif(line, size, CHARCOAL) for line in rows])
        body.arrange(DOWN, buff=GAP_SM * 0.6, aligned_edge=LEFT)
        head = serif("saved state", size, SLATE)
        card_body = VGroup(head, body).arrange(DOWN, buff=GAP_SM * 0.8)
        back = RoundedRectangle(width=card_body.width + GAP_MD * 1.6,
                                height=card_body.height + GAP_MD * 1.4,
                                corner_radius=0.12, color=SLATE,
                                stroke_width=2.5)
        back.set_fill(CREAM, opacity=1)
        back.move_to(card_body)
        self.card = VGroup(back, card_body)
        # High enough that the card's bottom edge still clears the
        # commentary band and the numbered strip beneath it. The figure is
        # as tall as the frame allows and there is no room to spare here.
        self.card.move_to([0, -1.95, 0])
        self.card_head, self.card_rows = head, body

        self.add(self.before, self.after, self.gap_marks, self.running)

    def steps(self):
        """The five steps, in the words the lecture uses to remember them."""
        return ["Finish the instruction", "Save the state",
                "Handle the interrupt", "Restore the state",
                "Resume the program"]


class Ladder(VGroup):
    """Two ends of one axis, with what each end buys written at that end.

    A table of differences invites a student to learn six unconnected
    facts. An axis says the one thing that generates them all: how close
    the language sits to the processor.
    """

    def __init__(self, top, bottom, top_notes=(), bottom_notes=(),
                 size=LABEL_SIZE, note_size=MARGIN_SIZE, box=5.4,
                 height=0.9, rise=2.35, width=FRAME_SAFE):
        super().__init__()
        self.ends, self.notes = VGroup(), VGroup()

        for name, y, colour in ((top, rise / 2, SLATE),
                                (bottom, -rise / 2, SLATE)):
            frame = Rectangle(width=box, height=height, color=colour,
                              stroke_width=2.5)
            frame.set_fill(colour, opacity=0.1)
            label = serif(name, size, CHARCOAL)
            if label.width > box - GAP_MD:
                raise ValueError(
                    f"End {name!r} is {label.width:.2f} units wide in a "
                    f"{box:.2f}-unit box.")
            frame.move_to([-2.9, y, 0])
            label.move_to(frame)
            self.ends.add(VGroup(frame, label))

        self.axis = Arrow([-2.9 - box / 2 - GAP_MD, -rise / 2 - 0.1, 0],
                          [-2.9 - box / 2 - GAP_MD, rise / 2 + 0.1, 0],
                          color=GREY, stroke_width=3.5, buff=0,
                          max_tip_length_to_length_ratio=0.25)

        # The notes start just clear of the boxes rather than at a fixed x:
        # a hardcoded column left two and a half units of dead space in the
        # middle and still pushed the longest note off the frame.
        note_x = -2.9 + box / 2 + GAP_MD * 1.3
        for notes, y in ((top_notes, rise / 2), (bottom_notes, -rise / 2)):
            block = VGroup(*[serif(f"{line}", note_size, GREY)
                             for line in notes])
            block.arrange(DOWN, buff=GAP_SM * 0.6, aligned_edge=LEFT)
            block.move_to([note_x, y, 0], aligned_edge=LEFT)
            self.notes.add(block)

        self.add(self.axis, self.ends, self.notes)
        if self.width > width:
            raise ValueError(
                f"The ladder is {self.width:.2f} units wide, over the "
                f"{width:.2f} the frame allows.")

    def light(self, index, color=TERRACOTTA):
        frame, label = self.ends[index]
        return [frame.animate.set_stroke(color).set_fill(color, opacity=0.14),
                label.animate.set_color(color),
                self.notes[index].animate.set_color(color)]

    def settle(self, index):
        frame, label = self.ends[index]
        return [frame.animate.set_stroke(SLATE).set_fill(SLATE, opacity=0.1),
                label.animate.set_color(CHARCOAL),
                self.notes[index].animate.set_color(GREY)]


class TranslatorFlow(VGroup):
    """What goes in, the thing that translates it, and what comes out.

    An interpreter produces no separate translated file, and that absence
    is examinable, so ``output=None`` is a supported state and draws the
    absence rather than leaving a gap that looks like an oversight.
    """

    def __init__(self, source, translator, output=None, size=MARGIN_SIZE,
                 box=3.2, height=1.1, gap=GAP_LG * 0.85, width=FRAME_SAFE):
        super().__init__()

        def panel(text, colour, fill, dashed=False):
            frame = Rectangle(width=box, height=height, color=colour,
                              stroke_width=2.5)
            frame.set_fill(colour, opacity=fill)
            label = serif(text, size, CHARCOAL if not dashed else GREY)
            if label.width > box - GAP_SM * 1.2:
                raise ValueError(
                    f"Panel {text!r} is {label.width:.2f} units wide in a "
                    f"{box:.2f}-unit box. Shorten it.")
            label.move_to(frame)
            return VGroup(frame, label), frame, label

        self.source, self.source_box, _ = panel(source, GREY, 0.08)
        # The translator is the machine, not the material, so it is the one
        # panel drawn in the accent and the only one the eye lands on.
        self.engine, self.engine_box, self.engine_label = panel(
            translator, TERRACOTTA, 0.12)
        self.engine_label.set_color(TERRACOTTA)

        pieces = [self.source, self.engine]
        if output is not None:
            self.output, self.output_box, _ = panel(output, SAGE, 0.12)
            pieces.append(self.output)
        else:
            self.output = self.output_box = None

        row = VGroup(*pieces).arrange(RIGHT, buff=gap)
        self.add(row)

        self.arrows = VGroup()
        boxes = [self.source_box, self.engine_box]
        if self.output_box is not None:
            boxes.append(self.output_box)
        for left, right in zip(boxes, boxes[1:]):
            self.arrows.add(Arrow(left.get_right(), right.get_left(),
                                  color=GREY, stroke_width=3.5, buff=0.06,
                                  max_tip_length_to_length_ratio=0.45))
        self.add(self.arrows)
        self.move_to(ORIGIN)
        if self.width > width:
            raise ValueError(
                f"The flow is {self.width:.2f} units wide, over the "
                f"{width:.2f} the frame allows.")


class IDEWindow(VGroup):
    """An editor with a gutter and a diagnostics strip.

    "An IDE makes programming easier" earns nothing; the syllabus wants a
    named feature and what it does. So the window exists to be pointed
    at: the gutter for where an error was found, the strip for what it
    said, a popup for auto-completion.
    """

    def __init__(self, lines, size=MARGIN_SIZE, width=8.4, height=4.3):
        super().__init__()
        self.frame = Rectangle(width=width, height=height, color=CHARCOAL,
                               stroke_width=2.5)
        self.frame.set_fill(CREAM, opacity=1)

        self.bar = Rectangle(width=width, height=0.46, color=CHARCOAL,
                             stroke_width=2.5)
        self.bar.set_fill(SLATE, opacity=0.16)
        self.bar.move_to([0, height / 2 - 0.23, 0])
        self.title = serif("Code editor", size, GREY)
        self.title.move_to([-width / 2 + self.title.width / 2 + GAP_MD,
                            self.bar.get_center()[1], 0])

        self.strip = Rectangle(width=width, height=0.62, color=CHARCOAL,
                               stroke_width=2.5)
        self.strip.set_fill(GREY, opacity=0.1)
        self.strip.move_to([0, -height / 2 + 0.31, 0])

        self.code = CodeBlock(lines, size, CHARCOAL, gutter=True,
                              width=width - GAP_LG)
        top = self.bar.get_bottom()[1] - GAP_MD * 0.7
        self.code.move_to([-width / 2 + self.code.width / 2 + GAP_LG * 0.9,
                           top - self.code.height / 2, 0])
        if self.code.get_bottom()[1] < self.strip.get_top()[1] + GAP_SM:
            raise ValueError(
                f"The {len(lines)} code lines reach the diagnostics strip. "
                "Use fewer lines or a taller window.")

        self.add(self.frame, self.bar, self.title, self.strip, self.code)
        self.size, self.inner = size, width - GAP_MD * 2

    def message(self, text, color=TERRACOTTA):
        """What the diagnostics strip says, sized to the strip."""
        body = serif(text, self.size, color)
        if body.width > self.inner:
            raise ValueError(
                f"The diagnostics message is {body.width:.2f} units wide "
                f"in a strip {self.inner:.2f} wide. Shorten it.")
        body.move_to([self.frame.get_left()[0] + body.width / 2 + GAP_MD,
                      self.strip.get_center()[1], 0])
        return body

    def completion(self, options, index=0):
        """The auto-completion popup, under the line it belongs to."""
        rows = VGroup(*[mono(option, self.size, CHARCOAL)
                        for option in options])
        rows.arrange(DOWN, buff=GAP_SM * 0.5, aligned_edge=LEFT)
        back = Rectangle(width=rows.width + GAP_MD,
                         height=rows.height + GAP_MD * 0.8,
                         color=SLATE, stroke_width=2)
        back.set_fill(CREAM, opacity=1)
        back.move_to(rows)
        popup = VGroup(back, rows)
        anchor = self.code.lines[index]
        popup.move_to([anchor.get_right()[0] + popup.width / 2 + GAP_SM,
                       anchor.get_center()[1] - popup.height / 2, 0])
        return popup

    def mark_line(self, index, color=TERRACOTTA):
        """Point the gutter at one line, the way diagnostics do."""
        number = self.code.numbers[index]
        return [number.animate.set_color(color),
                self.code.lines[index].animate.set_color(color)]


def measure():
    """Print every figure's extents and smallest label.

    Run as ``python -m components.software`` from the repo root.
    """
    from manim import config

    half_w, half_h = config.frame_width / 2, config.frame_height / 2

    def report(name, figure, smallest=None):
        fits = (figure.width <= 2 * half_w - 0.4
                and figure.height <= 2 * half_h - 0.4)
        note = "" if smallest is None else f"  smallest {smallest}"
        print(f"{name:20} {figure.width:6.2f} x {figure.height:5.2f}  "
              f"{'ok' if fits else 'DOES NOT FIT'}{note}")

    report("BootStack", BootStack(), LABEL_SIZE)
    report("PollVsSignal", PollVsSignal(), MARGIN_SIZE)

    line = InterruptTimeline()
    line.add(line.isr, line.into, line.out_of, line.flag, line.card,
             line.resumes)
    report("InterruptTimeline", line, MARGIN_SIZE)

    ladder = Ladder(
        "High-level language", "Low-level language",
        ("easier to read and write", "portable between processors"),
        ("control over the hardware", "tied to one processor"))
    report("Ladder", ladder, MARGIN_SIZE)

    report("TranslatorFlow 3", TranslatorFlow(
        "Source code", "Compiler", "Executable"), MARGIN_SIZE)
    report("TranslatorFlow 2", TranslatorFlow(
        "Source code", "Interpreter"), MARGIN_SIZE)

    block = CodeBlock([
        "total = 0",
        "for row in table:",
        "    total = total + row",
        "print(total)",
    ])
    report("CodeBlock", block, MARGIN_SIZE)
    step = _char_width(MARGIN_SIZE)
    indent = block.lines[2].get_left()[0] - block.lines[1].get_left()[0]
    print(f"{'':20} indent {indent:.3f} units = "
          f"{indent / step:.2f} characters")

    window = IDEWindow([
        "x = 10",
        "y = 0",
        "print(x / y)",
    ])
    window.add(window.message("Line 3: division by zero"))
    report("IDEWindow", window, MARGIN_SIZE)


if __name__ == "__main__":
    measure()
