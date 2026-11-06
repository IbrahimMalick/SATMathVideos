"""How the CPU executes an instruction — the shared O Level / AS Level lesson.

One machine carries the whole lesson. The processor is drawn once, with its
registers visible, main memory on the right with its addresses visible, and
the three buses across the gap; every stage of the cycle is then something
moving along one of those buses into one of those registers. A student who
watches one diagram change has a chance of holding it; a student who meets
a fresh drawing per stage has six pictures and no mechanism.

The fetch diagram carries exactly the four registers the fetch stage uses —
PC, MAR, MDR, CIR. The accumulator arrives with the execute stage, where it
is first needed, and the AS Level extras get a screen of their own. A box
on screen before the narration has earned it is a box the student has to
ignore.

Checked before building, because a trace that disagrees with itself teaches
the wrong thing:

  * worked example: ACC 12, Memory[2040] = 7, so 12 + 7 = 19, and the PC
    moves 1000 -> 1001.
  * challenge: ACC 9, Memory[700] = 6, so 9 + 6 = 15, and the PC moves
    300 -> 301.

Both are the plan's own numbers and both come out as he says they do.

Where the delivery slips, the screen carries the correct form. Four, each
confirmed on a second pass with a larger model:

  * "the program controller or PC" — it is the program COUNTER. The screen
    says Program Counter.
  * "the MDR receives instruction from address 2040" — the instruction ADD
    2040 is fetched FROM address 1000; 2040 is the address inside it. The
    screen shows it arriving from 1000.
  * "our CIR now holds address 2040" — the CIR holds the instruction ADD
    2040. The screen says ADD 2040.
  * "the operation is associated with address 2040" — it is the OPERAND
    that lives at 2040, and he says operand correctly a minute later. The
    screen says operand.

The rest are transcription artefacts over a delivery that was right: "the
more" is the MAR, "the DR" and "the empty R" and "the FDR" are the MDR,
"one Newman" is Von Neumann, "the CLR" and "the CER" are the CIR, "the BC"
is the PC, "comparations" is comparisons, "12 plus 7 is 90" is nineteen,
"restarts at night" is starts at nine, and "condense" is contains.

This take starts at the plan's "0:45 - the question we're answering" and
ends on the shared recap, so there is no opening card and no O Level or AS
Level sign-off: neither was recorded, and neither is invented here.

Timing: timings/concept.cpu_cycle.json
Render: python build/render.py scripts/CPU01-fetch-decode-execute.md \\
    audio/CPU01-fetch-decode-execute.m4a
"""

import textwrap
from contextlib import contextmanager

from manim import (
    Brace,
    Create,
    FadeIn,
    FadeOut,
    MathTex,
    MoveAlongPath,
    Transform,
    VGroup,
    Write,
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
)

from brand import (
    BODY_SIZE,
    CHARCOAL,
    DISPLAY_SIZE,
    GAP_LG,
    GAP_MD,
    GAP_SM,
    GREY,
    LABEL_SIZE,
    MARGIN_SIZE,
    SAGE,
    SLATE,
    TERRACOTTA,
    TITLE_SIZE,
    mono,
    serif,
)
from components.cpu import (
    BusSet,
    CpuBlock,
    CycleRing,
    MemoryColumn,
    RegisterBox,
    SystemView,
    given_block,
    rtn,
    strike,
)
from components.syllabus_map import TopicStrip
from components.table import make_table
from components.worked_solution import WorkedSolution, answer_box
from scenes.base import SATScene

FRAME_SAFE = 12.6
FLOOR = -3.1          # the chapter strip owns everything below this
DIAG_Y = -0.25        # the diagram's own centre line
BAND_Y = -2.9         # the notation and caption band under the diagram

PARTS = ["The cycle", "Registers", "Fetch", "Execute", "Buses", "Practice"]

# The trace, in the plan's numbers. Nothing on screen is typed twice: the
# instruction at 1000 and the operand address inside it come from here.
INSTRUCTION = "ADD 2040"
PROGRAM_ADDRESS = 1000
OPERAND_ADDRESS = 2040
OPERAND_VALUE = 7
ACC_BEFORE = 12

CHALLENGE = {"pc": 300, "operand": 700, "value": 6, "acc": 9}


def fit(mobject, width=FRAME_SAFE):
    if mobject.width > width:
        mobject.scale_to_fit_width(width)
    return mobject


def prose(text, size=BODY_SIZE, color=CHARCOAL, width=FRAME_SAFE):
    """A sentence that wraps to fit rather than shrinking to fit.

    Shrink-to-fit is how a 32px caption quietly becomes a 26px one: the
    layout still looks balanced, so nothing catches it but the acceptance
    check. House serif runs about a quarter of a unit per character at
    LABEL_SIZE, so a line of prose across the frame is roughly fifty
    characters and the long ones have to break. This measures the real
    mobject and wraps on the measurement, which beats guessing.
    """
    body = serif(text, size, color)
    if body.width <= width:
        return body
    budget = max(10, int(len(text) * width / body.width))
    while budget >= 10:
        body = serif(textwrap.fill(text, budget), size, color)
        if body.width <= width:
            return body
        budget -= 2
    return fit(body, width)


class CpuCycle(SATScene):
    scene_id = "concept.cpu_cycle"

    def construct(self):
        self.margin = mono("O Level 2210 · AS Level 9618 · The CPU cycle",
                           MARGIN_SIZE)
        self.margin.to_corner(UP + LEFT, buff=GAP_SM)
        self.add(self.margin)

        self.strip = TopicStrip(len(PARTS), lit=SLATE, side=0.6)
        self.strip.to_edge(DOWN, buff=GAP_SM * 0.5)
        self.add(self.strip)

        self.keep = [self.margin, self.strip]
        self.head = None
        self.note = None
        self.notation = None
        # Where a running caption sits in the band. It shares the band with
        # the notation on the fetch screen and has it to itself elsewhere,
        # so a caption alone is centred rather than left hanging to one side.
        self.band_x, self.band_width = 2.45, 8.6

        self.the_question()
        self.not_magic()
        self.four_things()
        self.the_cycle()
        self.the_plan()
        self.stored_program()
        self.basic_system()
        self.inside_cpu()
        self.four_registers()
        self.mar_and_mdr()
        self.fetch_stage()
        self.five_steps()
        self.decode()
        self.who_does_what()
        self.worked_example()
        self.the_buses()
        self.bus_roles()
        self.as_registers()
        self.notation_rules()
        self.challenge()
        self.challenge_answer()
        self.mistakes()
        self.recap()

    # -------------------------------------------------------------- helpers

    _beat_name = "(before the first beat)"

    @contextmanager
    def beat(self, name):
        """The base class's beat, remembering the name for error messages."""
        self._beat_name = name
        with super().beat(name) as timer:
            yield timer

    def clear(self, t, *groups, fraction=0.1):
        """Fade a diagram that was drawn child by child.

        Create() on a group's children adds the children to the scene, not
        the group, so FadeOut(group) removes something the scene never held
        and leaves the drawing exactly where it was. Fade what is present.
        """
        family = set()
        for group in groups:
            family.update(id(m) for m in group.get_family())
        present = [m for m in self.mobjects if id(m) in family]
        if present:
            self.play(*[FadeOut(m) for m in present], run_time=t.fill(fraction))

    def wipe(self, t, fraction=0.06):
        old = [m for m in self.mobjects if m not in self.keep]
        if old:
            self.play(*[FadeOut(m) for m in old], run_time=t.fill(fraction))
        self.head = self.note = self.notation = None

    def title(self, t, text, fraction=0.1, color=CHARCOAL):
        head = fit(serif(text, TITLE_SIZE, color))
        head.to_edge(UP, buff=GAP_MD * 1.9)
        self.play(Write(head), run_time=t.fill(fraction))
        self.head = head
        return head

    def lines(self, *texts, size=BODY_SIZE, color=CHARCOAL, buff=GAP_SM * 1.3,
              align=None, width=FRAME_SAFE):
        group = VGroup(*[prose(x, size, color, width) for x in texts])
        if align is None:
            group.arrange(DOWN, buff=buff)
        else:
            group.arrange(DOWN, buff=buff, aligned_edge=align)
        return group

    # stack() and place() only ever tighten, so a floor they cannot reach
    # used to leave the content sitting over the chapter strip — silently,
    # because the layout still looked deliberate. They now say so instead.

    def stack(self, group, top=None, buff=GAP_MD, floor=FLOOR, align=ORIGIN):
        """Place under `top`, tightening the group's gaps to clear the floor."""
        for factor in (1.0, 0.85, 0.7, 0.55, 0.42, 0.32, 0.24):
            gap = buff * factor
            group.arrange(DOWN, buff=gap, aligned_edge=align)
            if top is None:
                group.move_to(ORIGIN)
            else:
                group.next_to(top, DOWN, buff=gap)
            if group.get_bottom()[1] >= floor:
                return group
        raise ValueError(
            f"Beat '{self._beat_name}': a stack {group.height:.2f} units tall "
            f"cannot clear y={floor} under this heading even at the tightest "
            "gap. Shorten the content or raise the floor."
        )

    def place(self, mobject, top=None, buff=GAP_MD, floor=FLOOR):
        for factor in (1.0, 0.9, 0.78, 0.66, 0.55, 0.45, 0.35):
            if top is None:
                mobject.move_to(ORIGIN)
            else:
                mobject.next_to(top, DOWN, buff=buff * factor)
            if mobject.get_bottom()[1] >= floor:
                return mobject
        raise ValueError(
            f"Beat '{self._beat_name}': there is no room under this content "
            f"for something {mobject.height:.2f} units tall above y={floor}. "
            "It would land on the chapter strip."
        )

    def hide(self, group):
        for row in group:
            row.set_opacity(0)
        return group

    def reveal(self, t, group, start, stop, fraction):
        for row in group[start:stop]:
            row.set_opacity(1)
            self.play(FadeIn(row), run_time=t.fill(fraction))

    def part(self, t, number, fraction=0.05):
        self.play(*self.strip.focus(number), run_time=t.fill(fraction))

    # --- the band under the diagram: notation on the left, a caption right

    def notate(self, t, text, fraction=0.14, color=CHARCOAL):
        """Show one line of register-transfer notation under the processor."""
        line = rtn(text, LABEL_SIZE, color)
        line.move_to([-4.1, BAND_Y, 0])
        if self.notation is None:
            self.notation = line
            self.play(Write(line), run_time=t.fill(fraction))
        else:
            self.play(Transform(self.notation, line), run_time=t.fill(fraction))
        return self.notation

    def aside(self, t, text, fraction=0.12, color=GREY, size=LABEL_SIZE,
              x=None, y=BAND_Y, width=None):
        """Show a running caption beside the notation, swapping in place.

        The band under the diagram is one line tall — a second line would
        reach the chapter strip — so a caption that does not fit cannot be
        wrapped and must be rewritten shorter. Saying so beats shrinking it
        below the legibility floor.
        """
        x = self.band_x if x is None else x
        width = self.band_width if width is None else width
        line = serif(text, size, color)
        if line.width > width:
            raise ValueError(
                f"Beat '{self._beat_name}': the caption {text!r} needs "
                f"{line.width:.1f} units and the band is {width}. The band "
                "holds one line, so write it shorter."
            )
        line.move_to([x, y, 0])
        if self.note is None:
            self.note = line
            self.play(FadeIn(line), run_time=t.fill(fraction))
        else:
            self.play(Transform(self.note, line), run_time=t.fill(fraction))
        return self.note

    def drop_aside(self, t, fraction=0.06):
        if self.note is not None and self.note in self.mobjects:
            self.play(FadeOut(self.note), run_time=t.fill(fraction))
        self.note = None

    # ------------------------------------------------- the question we answer

    def the_question(self):
        with self.beat("open") as t:
            self.part(t, 0)
            head = self.title(t, "A simple question", fraction=0.2)
            t.hold()
        with self.beat("question") as t:
            ask = self.lines(
                "When you click Run, how does the computer",
                "turn a program into actions?",
                size=BODY_SIZE, color=CHARCOAL, buff=GAP_SM * 1.4,
            )
            # stack() uses one buff for the gap under the heading AND the
            # gaps inside the group, so a generous one here spreads a
            # two-line sentence over two units of frame.
            self.stack(ask, head, buff=GAP_MD * 1.1)
            self.play(Write(ask[0]), run_time=t.fill(0.3))
            self.play(Write(ask[1]), run_time=t.fill(0.45))
            self.ask = ask
            t.hold()
        with self.beat("think") as t:
            self.beat_note = fit(serif("Think about that for a moment.",
                                       LABEL_SIZE, GREY))
            self.place(self.beat_note, ask, buff=GAP_LG)
            self.play(FadeIn(self.beat_note), run_time=t.fill(0.12))
            t.hold()

    def not_magic(self):
        with self.beat("not_magic") as t:
            self.play(FadeOut(self.beat_note), run_time=t.fill(0.04))
            wrong = self.lines(
                "read the whole program, understand it all at once,",
                "then produce the result",
                size=LABEL_SIZE, color=GREY, buff=GAP_SM,
            )
            self.stack(wrong, self.ask, buff=GAP_MD)
            self.play(FadeIn(wrong), run_time=t.fill(0.2))
            marks = VGroup(*[strike(row, GREY) for row in wrong])
            self.play(Create(marks), run_time=t.fill(0.18))
            self.wrong = VGroup(wrong, marks)
            t.hold()
        with self.beat("sequence") as t:
            right = fit(serif("It works through instructions in an "
                              "organised sequence.", BODY_SIZE, CHARCOAL))
            right.move_to(self.wrong)
            self.play(FadeOut(self.wrong), run_time=t.fill(0.12))
            self.play(Write(right), run_time=t.fill(0.3))
            t.hold()

    def four_things(self):
        with self.beat("for_each") as t:
            self.wipe(t)
            head = self.title(t, "For each instruction, the processor:",
                              fraction=0.14)
            steps = self.lines(
                "finds it in memory",
                "brings it into the CPU",
                "works out what it means",
                "carries it out",
                size=BODY_SIZE, align=LEFT,
            )
            self.stack(steps, head, buff=GAP_MD * 1.3, align=LEFT)
            self.hide(steps)
            self.reveal(t, steps, 0, 4, 0.14)
            self.steps = steps
            t.hold()
        with self.beat("then_next") as t:
            nxt = fit(serif("then on to the next instruction",
                            LABEL_SIZE, TERRACOTTA))
            self.place(nxt, steps, buff=GAP_MD * 1.4)
            self.play(Write(nxt), run_time=t.fill(0.3))
            t.hold()

    def the_cycle(self):
        with self.beat("named") as t:
            self.wipe(t)
            head = self.title(t, "The fetch-decode-execute cycle",
                              fraction=0.14)
            ring = CycleRing()
            self.place(ring, head, buff=GAP_LG * 1.1)
            self.play(Create(ring.cards), run_time=t.fill(0.3))
            self.play(Create(ring.arrows), run_time=t.fill(0.14))
            self.play(Create(ring.loop), FadeIn(ring.loop_label),
                      run_time=t.fill(0.2))
            self.ring = ring
            t.hold()
        with self.beat("alias") as t:
            also = fit(serif("some books call it the fetch-execute cycle",
                             LABEL_SIZE, GREY))
            self.place(also, self.ring, buff=GAP_MD * 1.2)
            self.play(FadeIn(also), run_time=t.fill(0.2))
            t.hold()

    def the_plan(self):
        with self.beat("today") as t:
            self.wipe(t)
            head = self.title(t, "Today we make it visible", fraction=0.2)
            self.plan_head = head
            t.hold()
        with self.beat("agenda") as t:
            plan = self.lines(
                "name the parts of the CPU",
                "trace one instruction through the registers",
                "see what the buses carry between them",
                size=BODY_SIZE, align=LEFT,
            )
            self.stack(plan, self.plan_head, buff=GAP_MD * 1.3, align=LEFT)
            self.hide(plan)
            self.reveal(t, plan, 0, 3, 0.2)
            t.hold()

    # ------------------------------------------------- the stored-program idea

    def stored_program(self):
        with self.beat("stored") as t:
            self.wipe(t)
            head = self.title(t, "One key idea: the stored program",
                              fraction=0.12)
            self.stored_head = head
            self.stored_lines = self.lines(
                "a program is a set of instructions",
                "stored in memory, along with the data",
                "the processor fetches them as it needs them",
                size=BODY_SIZE, align=LEFT,
            )
            self.stack(self.stored_lines, head, buff=GAP_MD * 1.25, align=LEFT)
            self.hide(self.stored_lines)
            t.hold()
        with self.beat("program_is") as t:
            self.reveal(t, self.stored_lines, 0, 1, 0.3)
            t.hold()
        with self.beat("in_memory") as t:
            self.reveal(t, self.stored_lines, 1, 2, 0.3)
            t.hold()
        with self.beat("retrieves") as t:
            self.reveal(t, self.stored_lines, 2, 3, 0.3)
            t.hold()
        with self.beat("von_neumann") as t:
            vn = fit(prose("Von Neumann: instructions and data in one memory",
                      LABEL_SIZE, TERRACOTTA))
            self.place(vn, self.stored_lines, buff=GAP_LG * 0.9)
            self.play(Write(vn), run_time=t.fill(0.35))
            self.vn = vn
            t.hold()
        with self.beat("buses_intro") as t:
            via = fit(serif("and it reaches them through the buses", LABEL_SIZE, GREY))
            self.place(via, self.vn, buff=GAP_MD)
            self.play(FadeIn(via), run_time=t.fill(0.3))
            t.hold()

    def basic_system(self):
        with self.beat("system") as t:
            self.wipe(t)
            head = self.title(t, "The basic system", fraction=0.12)
            system = SystemView()
            self.place(system, head, buff=GAP_LG * 1.2)
            self.play(Create(system.boxes), run_time=t.fill(0.38))
            self.play(Create(system.links), run_time=t.fill(0.22))
            self.system = system
            t.hold()

    # ----------------------------------------------------------- inside the CPU

    def inside_cpu(self):
        with self.beat("inside") as t:
            self.part(t, 1)
            self.clear(t, self.system, fraction=0.06)
            if self.head is not None:
                self.play(FadeOut(self.head), run_time=t.fill(0.04))
            head = self.title(t, "Inside the processor", fraction=0.08)
            cpu = CpuBlock(["PC", "MAR", "MDR", "CIR"], centre=(-3.0, -0.45))
            self.play(Create(cpu.box), FadeIn(cpu.caption),
                      run_time=t.fill(0.14))
            self.play(Create(cpu.units), run_time=t.fill(0.18))
            self.play(Create(cpu.bank), run_time=t.fill(0.22))
            self.cpu = cpu
            t.hold()

        self.unit_caption = None

        def describe(t, target, text, fraction=0.25, color=CHARCOAL):
            # Beside the part being described, but clear of the whole box:
            # anchoring to the register bank would put the caption straight
            # on top of the CU and ALU, which sit to the bank's right.
            caption = fit(serif(text, LABEL_SIZE, color), 5.6)
            caption.next_to(self.cpu.box, RIGHT, buff=GAP_MD * 1.2)
            caption.set_y(target.get_center()[1])
            if caption.get_right()[0] > 6.9:
                caption.shift(LEFT * (caption.get_right()[0] - 6.9))
            if self.unit_caption is None:
                self.unit_caption = caption
                self.play(FadeIn(caption), run_time=t.fill(fraction))
            else:
                self.play(Transform(self.unit_caption, caption),
                          run_time=t.fill(fraction))

        with self.beat("cu") as t:
            self.play(self.cpu.cu[0].animate.set_color(TERRACOTTA),
                      run_time=t.fill(0.14))
            describe(t, self.cpu.cu, "the CU coordinates\nthe whole processor")
            t.hold()
        with self.beat("cu_role") as t:
            describe(t, self.cpu.cu,
                     "it interprets instructions\nand sends control signals")
            t.hold()
        with self.beat("alu") as t:
            self.play(self.cpu.cu[0].animate.set_color(SLATE),
                      self.cpu.alu[0].animate.set_color(TERRACOTTA),
                      run_time=t.fill(0.12))
            describe(t, self.cpu.alu, "the ALU does arithmetic\nand logic")
            t.hold()
        with self.beat("alu_logic") as t:
            describe(t, self.cpu.alu, "add, subtract,\nAND, comparisons")
            t.hold()
        with self.beat("regs_role") as t:
            self.play(self.cpu.alu[0].animate.set_color(SLATE),
                      *[reg.light() for reg in self.cpu.bank],
                      run_time=t.fill(0.14))
            describe(t, self.cpu.bank,
                     "registers hold what is\nin use right now")
            t.hold()
        with self.beat("regs_small") as t:
            describe(t, self.cpu.bank, "far smaller\nthan main memory")
            t.hold()
        with self.beat("regs_direct") as t:
            describe(t, self.cpu.bank,
                     "but directly available\nto the processor", color=SAGE)
            t.hold()

    # ---------------------------------------------------------- four registers

    def four_registers(self):
        rows = [
            ("PC", "Program Counter", "address of the next instruction"),
            ("MAR", "Memory Address Register", "the address being accessed"),
            ("MDR", "Memory Data Register", "data or instruction in transit"),
            ("CIR", "Current Instruction Register",
             "the instruction being executed"),
        ]
        with self.beat("four_regs") as t:
            self.play(*[reg.settle() for reg in self.cpu.bank],
                      run_time=t.fill(0.06))
            self.clear(t, self.cpu, fraction=0.06)
            if self.unit_caption is not None:
                self.play(FadeOut(self.unit_caption), run_time=t.fill(0.04))
            self.play(FadeOut(self.head), run_time=t.fill(0.04))
            head = self.title(t, "Four registers at the heart of the cycle",
                              fraction=0.1)
            self.reg_head = head

            self.reg_rows = VGroup()
            self.reg_boxes = {}
            for name, full, role in rows:
                box = RegisterBox(name, None)
                words = VGroup(
                    serif(full, LABEL_SIZE, CHARCOAL),
                    serif(role, MARGIN_SIZE, GREY),
                ).arrange(DOWN, buff=GAP_SM * 0.2, aligned_edge=LEFT)
                words.next_to(box, RIGHT, buff=GAP_MD * 1.1)
                self.reg_boxes[name] = box
                self.reg_rows.add(VGroup(box, words))
            self.reg_rows.arrange(DOWN, buff=GAP_MD * 0.85, aligned_edge=LEFT)
            fit(self.reg_rows)
            # Stop the four rows well above the floor: the bookmark line and
            # the MAR-against-MDR pair both have to fit underneath them.
            self.stack(self.reg_rows, head, buff=GAP_MD * 1.1, align=LEFT,
                       floor=-1.95)
            t.hold()

        def show_register(t, index, role=True):
            row = self.reg_rows[index]
            self.play(Create(row[0]), run_time=t.fill(0.3))
            self.play(FadeIn(row[1][0]), run_time=t.fill(0.2))
            if role:
                self.play(FadeIn(row[1][1]), run_time=t.fill(0.22))

        with self.beat("pc") as t:
            show_register(t, 0, role=False)
            t.hold()
        with self.beat("pc_role") as t:
            self.play(FadeIn(self.reg_rows[0][1][1]), run_time=t.fill(0.25))
            t.hold()
        with self.beat("pc_bookmark") as t:
            mark = fit(serif("the processor's bookmark in the program",
                             LABEL_SIZE, TERRACOTTA))
            self.place(mark, self.reg_rows, buff=GAP_MD * 1.2)
            self.play(FadeIn(mark), run_time=t.fill(0.2))
            self.bookmark = mark
            t.hold()
        with self.beat("mar") as t:
            show_register(t, 1, role=False)
            t.hold()
        with self.beat("mar_role") as t:
            self.play(FadeIn(self.reg_rows[1][1][1]), run_time=t.fill(0.25))
            t.hold()
        with self.beat("mar_example") as t:
            self.play(FadeOut(self.bookmark), run_time=t.fill(0.06))
            box = self.reg_boxes["MAR"]
            self.play(Transform(box.value, box.write(PROGRAM_ADDRESS)),
                      box.light(), run_time=t.fill(0.25))
            t.hold()
        with self.beat("mdr") as t:
            show_register(t, 2, role=False)
            t.hold()
        with self.beat("mdr_role") as t:
            self.play(FadeIn(self.reg_rows[2][1][1]), run_time=t.fill(0.25))
            t.hold()
        with self.beat("mdr_repeat") as t:
            self.play(self.reg_boxes["MAR"].settle(), run_time=t.fill(0.04))
            pair = self.lines(
                "MAR holds an address",
                "MDR holds the data or instruction being transferred",
                size=LABEL_SIZE, align=LEFT,
            )
            pair[0].set_color(SLATE)
            pair[1].set_color(SAGE)
            self.stack(pair, self.reg_rows, buff=GAP_MD, align=LEFT)
            self.play(FadeIn(pair[0]), run_time=t.fill(0.12))
            self.play(FadeIn(pair[1]), run_time=t.fill(0.12))
            self.pair = pair
            t.hold()
        with self.beat("cir") as t:
            show_register(t, 3)
            t.hold()

    def mar_and_mdr(self):
        with self.beat("mix_up") as t:
            self.wipe(t)
            head = self.title(t, "The two that get mixed up", fraction=0.14)
            group, cells = make_table(
                ["Register", "What it holds"],
                [["MAR", "an address"],
                 ["MDR", "data or an instruction"]],
                row_height=0.75, col_widths=[2.6, 5.4],
            )
            self.place(group, head, buff=GAP_MD * 1.3)
            self.play(FadeIn(group), run_time=t.fill(0.3))
            self.table, self.cells = group, cells
            t.hold()
        with self.beat("mar_holds") as t:
            self.play(self.cells[(1, 1)].animate.set_color(SLATE),
                      run_time=t.fill(0.2))
            self.play(self.cells[(2, 1)].animate.set_color(SAGE),
                      run_time=t.fill(0.2))
            t.hold()
        with self.beat("trick") as t:
            trick = self.lines(
                "A in MAR  →  Address",
                "D in MDR  →  Data",
                size=BODY_SIZE, align=LEFT,
            )
            trick[0].set_color(SLATE)
            trick[1].set_color(SAGE)
            self.stack(trick, self.table, buff=GAP_MD * 1.3, align=LEFT)
            self.play(Write(trick[0]), run_time=t.fill(0.22))
            self.play(Write(trick[1]), run_time=t.fill(0.22))
            self.trick = trick
            t.hold()
        with self.beat("exam_note") as t:
            note = prose("Keep them apart and the cycle writes itself.",
                         LABEL_SIZE, GREY)
            self.place(note, self.trick, buff=GAP_MD * 0.9)
            self.play(FadeIn(note), run_time=t.fill(0.25))
            t.hold()

    # ------------------------------------------------------- the fetch stage

    def build_diagram(self, t, registers, memory_rows, draw=0.5):
        """Draw the processor, memory and the buses between them."""
        cpu = CpuBlock(registers, centre=(-3.68, DIAG_Y))
        memory = MemoryColumn(memory_rows, centre=(5.3, DIAG_Y))
        buses = BusSet(cpu.box.get_right()[0], memory.box.get_left()[0],
                       centre_y=DIAG_Y)
        self.play(Create(cpu.box), FadeIn(cpu.caption),
                  Create(cpu.units), run_time=t.fill(draw * 0.3))
        self.play(Create(cpu.bank), Create(memory.box),
                  Create(memory.divider), Create(memory.rules),
                  FadeIn(memory.title), FadeIn(memory[3]),
                  run_time=t.fill(draw * 0.37))
        self.play(Create(buses.lines), FadeIn(buses.captions),
                  run_time=t.fill(draw * 0.33))
        self.cpu, self.memory, self.buses = cpu, memory, buses
        return cpu, memory, buses

    def send(self, t, index, payload, reverse=False, fraction=0.3,
             color=TERRACOTTA):
        """Run one payload along one bus and leave nothing behind."""
        chip = self.buses.chip(index, payload, color=color, reverse=reverse)
        path = self.buses.path(index, reverse=reverse)
        self.play(FadeIn(chip), run_time=t.fill(fraction * 0.2))
        self.play(MoveAlongPath(chip, path), run_time=t.fill(fraction * 0.6))
        self.play(FadeOut(chip), run_time=t.fill(fraction * 0.2))

    def fetch_stage(self):
        memory_rows = [
            (PROGRAM_ADDRESS, INSTRUCTION),
            (PROGRAM_ADDRESS + 1, "..."),
            (None, None),
            (OPERAND_ADDRESS, OPERAND_VALUE),
        ]
        with self.beat("follow") as t:
            self.part(t, 2)
            self.wipe(t)
            self.band_x, self.band_width = 2.45, 8.6
            self.title(t, "The fetch stage", fraction=0.07)
            self.build_diagram(t, ["PC", "MAR", "MDR", "CIR"], memory_rows,
                               draw=0.62)
            t.hold()
        with self.beat("pc_1000") as t:
            pc = self.cpu.reg("PC")
            self.play(Transform(pc.value, pc.write(PROGRAM_ADDRESS)),
                      pc.light(), run_time=t.fill(0.3))
            t.hold()
        with self.beat("mem_1000") as t:
            self.ring_1000 = self.memory.frame(PROGRAM_ADDRESS)
            self.play(Create(self.ring_1000), run_time=t.fill(0.25))
            t.hold()
        with self.beat("copy_mar") as t:
            self.notate(t, "MAR ← [PC]", fraction=0.2)
            mar = self.cpu.reg("MAR")
            self.play(Transform(mar.value, mar.write(PROGRAM_ADDRESS)),
                      run_time=t.fill(0.3))
            t.hold()
        with self.beat("brackets") as t:
            self.aside(t, "[ ] means: the contents of", fraction=0.2)
            t.hold()
        with self.beat("mar_receives") as t:
            self.play(self.cpu.reg("PC").settle(), self.cpu.reg("MAR").light(),
                      run_time=t.fill(0.2))
            t.hold()
        with self.beat("address_bus") as t:
            self.aside(t, "out on the address bus",
                       fraction=0.14)
            self.send(t, 0, PROGRAM_ADDRESS, fraction=0.55)
            t.hold()
        with self.beat("read_signal") as t:
            self.aside(t, "READ on the control bus", fraction=0.14)
            self.send(t, 2, "READ", fraction=0.55, color=SLATE)
            t.hold()
        with self.beat("memory_finds") as t:
            self.play(self.memory.value(PROGRAM_ADDRESS)
                      .animate.set_color(TERRACOTTA), run_time=t.fill(0.3))
            t.hold()
        with self.beat("data_bus") as t:
            self.aside(t, "the instruction comes back",
                       fraction=0.12)
            self.send(t, 1, INSTRUCTION, reverse=True, fraction=0.45)
            mdr = self.cpu.reg("MDR")
            self.play(Transform(mdr.value, mdr.write(INSTRUCTION)),
                      mdr.light(), self.cpu.reg("MAR").settle(),
                      run_time=t.fill(0.25))
            t.hold()
        with self.beat("double_brackets") as t:
            self.notate(t, "MDR ← [[MAR]]", fraction=0.16)
            self.aside(t, "[[ ]] means: read what is there", fraction=0.16)
            t.hold()
        with self.beat("mdr_gets") as t:
            # He says the MDR receives the instruction "from address 2040".
            # It came from 1000; 2040 is the address inside the instruction.
            self.aside(t, f"fetched from address {PROGRAM_ADDRESS}",
                       fraction=0.2, color=SAGE)
            t.hold()
        with self.beat("to_cir") as t:
            self.notate(t, "CIR ← [MDR]", fraction=0.16)
            cir = self.cpu.reg("CIR")
            self.play(Transform(cir.value, cir.write(INSTRUCTION)),
                      cir.light(), self.cpu.reg("MDR").settle(),
                      run_time=t.fill(0.3))
            self.drop_aside(t, fraction=0.06)
            t.hold()
        with self.beat("pc_update") as t:
            self.notate(t, "PC ← [PC] + 1", fraction=0.2)
            t.hold()
        with self.beat("pc_increment") as t:
            pc = self.cpu.reg("PC")
            self.play(Transform(pc.value, pc.write(PROGRAM_ADDRESS + 1)),
                      pc.light(), self.cpu.reg("CIR").settle(),
                      run_time=t.fill(0.3))
            t.hold()
        with self.beat("pc_note") as t:
            self.aside(t, "how much depends on the machine",
                       fraction=0.25)
            t.hold()
        with self.beat("convention") as t:
            self.aside(t, "here: the book's one-step rule",
                       fraction=0.25)
            t.hold()
        with self.beat("fetch_done") as t:
            self.play(self.cpu.reg("PC").settle(),
                      self.cpu.reg("CIR").light(SAGE),
                      run_time=t.fill(0.2))
            self.aside(t, "fetch done: it is in the CIR",
                       fraction=0.2, color=SAGE)
            t.hold()

    def five_steps(self):
        with self.beat("once_more") as t:
            self.wipe(t)
            head = self.title(t, "The fetch stage in five steps", fraction=0.1)
            steps = self.lines(
                "1.  the PC holds the address of the next instruction",
                "2.  that address is copied to the MAR",
                "3.  the instruction at that address goes to the MDR",
                "4.  the instruction is copied from the MDR to the CIR",
                "5.  the PC is updated",
                size=LABEL_SIZE, align=LEFT,
            )
            self.stack(steps, head, buff=GAP_MD * 1.15, align=LEFT)
            self.hide(steps)
            self.reveal(t, steps, 0, 1, 0.3)
            self.five = steps
            t.hold()
        for index, name in enumerate(["s_mar", "s_mdr", "s_cir"], start=1):
            with self.beat(name) as t:
                self.reveal(t, self.five, index, index + 1, 0.35)
                t.hold()
        with self.beat("s_update") as t:
            self.reveal(t, self.five, 4, 5, 0.3)
            ready = fit(serif("now the control unit can decode it",
                              LABEL_SIZE, TERRACOTTA))
            self.place(ready, self.five, buff=GAP_MD * 1.2)
            self.play(FadeIn(ready), run_time=t.fill(0.25))
            t.hold()

    # ------------------------------------------------------ decode and execute

    def decode(self):
        with self.beat("cir_holds") as t:
            self.part(t, 3)
            self.wipe(t)
            head = self.title(t, "Decode, then execute", fraction=0.08)

            # "CIR now holds address 2040" — it holds the instruction. The
            # operation and the operand address are the two halves of it.
            label = mono("CIR", LABEL_SIZE, GREY)
            op = mono("ADD", DISPLAY_SIZE * 0.6, CHARCOAL)
            operand = mono(str(OPERAND_ADDRESS), DISPLAY_SIZE * 0.6, CHARCOAL)
            # The two fields sit wide apart so each can carry its own
            # label underneath without the two labels colliding; the
            # register's name stays close to the contents it holds.
            fields = VGroup(op, operand).arrange(RIGHT, buff=2.0)
            card = VGroup(label, fields).arrange(RIGHT, buff=GAP_MD * 1.2)
            self.place(card, head, buff=GAP_MD * 0.9)
            self.play(FadeIn(label), run_time=t.fill(0.12))
            self.play(Write(op), Write(operand), run_time=t.fill(0.3))
            self.cir_card, self.op, self.operand = card, op, operand
            # One caption slot for this screen, below the braces and above
            # where the working will go.
            self.decode_slot = card.get_bottom()[1] - 1.9
            t.hold()
        with self.beat("cu_decodes") as t:
            self.aside(t, "the control unit works out what it means",
                       fraction=0.3, x=0, y=self.decode_slot, width=11.0)
            t.hold()
        with self.beat("operation") as t:
            brace = Brace(self.op, DOWN, color=GREY)
            tag = serif("operation", MARGIN_SIZE, SLATE)
            tag.next_to(brace, DOWN, buff=GAP_SM * 0.5)
            self.play(Create(brace), FadeIn(tag), run_time=t.fill(0.3))
            self.op_tag = VGroup(brace, tag)
            t.hold()
        with self.beat("operand") as t:
            brace = Brace(self.operand, DOWN, color=GREY)
            tag = serif("operand address", MARGIN_SIZE, TERRACOTTA)
            tag.next_to(brace, DOWN, buff=GAP_SM * 0.5)
            self.play(Create(brace), FadeIn(tag), run_time=t.fill(0.3))
            self.operand_tag = VGroup(brace, tag)
            t.hold()
        with self.beat("get_value") as t:
            self.aside(t, f"the processor must now fetch what is at {OPERAND_ADDRESS}", fraction=0.3, x=0,
                       y=self.decode_slot, width=11.0)
            t.hold()

        # Built as one left-aligned block and revealed a line at a time:
        # placed each under the last, every line centres itself on the one
        # above, and the column walks off under whichever tag it started
        # from instead of sitting square in the frame.
        self.decode_steps = VGroup(
            rtn(f"MAR ← {OPERAND_ADDRESS}", LABEL_SIZE),
            rtn("READ on the control bus", LABEL_SIZE, GREY),
            rtn(f"MDR ← [[MAR]]   gives {OPERAND_VALUE}", LABEL_SIZE),
            rtn("ACC ← ACC + MDR", LABEL_SIZE, TERRACOTTA),
        ).arrange(DOWN, buff=GAP_SM * 1.0, aligned_edge=LEFT)
        self.place(self.decode_steps, self.operand_tag, buff=GAP_MD * 0.8)
        self.decode_steps.set_x(0)

        with self.beat("mar_2040") as t:
            self.drop_aside(t, fraction=0.06)
            self.play(Write(self.decode_steps[0]), run_time=t.fill(0.35))
            t.hold()
        with self.beat("read_again") as t:
            self.play(FadeIn(self.decode_steps[1]), run_time=t.fill(0.3))
            t.hold()
        with self.beat("mdr_7") as t:
            self.play(Write(self.decode_steps[2]), run_time=t.fill(0.3))
            t.hold()
        with self.beat("alu_adds") as t:
            self.play(Write(self.decode_steps[3]), run_time=t.fill(0.35))
            t.hold()
        with self.beat("acc_result") as t:
            where = prose("the result lands in the accumulator",
                          LABEL_SIZE, SAGE)
            self.place(where, self.decode_steps, buff=GAP_MD * 0.8)
            self.play(FadeIn(where), run_time=t.fill(0.3))
            t.hold()

    def who_does_what(self):
        with self.beat("two_accesses") as t:
            self.wipe(t)
            head = self.title(t, "Two separate trips to memory", fraction=0.14)
            trips = self.lines(
                "first access   the instruction itself",
                "second access  the data the instruction needs",
                size=BODY_SIZE, align=LEFT,
            )
            self.stack(trips, head, buff=GAP_MD * 1.3, align=LEFT)
            self.hide(trips)
            self.trips = trips
            t.hold()
        with self.beat("first_access") as t:
            self.reveal(t, self.trips, 0, 1, 0.35)
            t.hold()
        with self.beat("second_access") as t:
            self.reveal(t, self.trips, 1, 2, 0.35)
            t.hold()
        with self.beat("who_does") as t:
            roles = self.lines(
                "the control unit coordinates",
                "the ALU performs the arithmetic",
                "the registers hold the values on the way through",
                size=LABEL_SIZE, color=GREY, align=LEFT,
            )
            self.stack(roles, self.trips, buff=GAP_LG * 0.85, align=LEFT)
            self.hide(roles)
            self.reveal(t, roles, 0, 2, 0.25)
            self.roles = roles
            t.hold()
        with self.beat("regs_hold") as t:
            self.reveal(t, self.roles, 2, 3, 0.3)
            t.hold()

    # ------------------------------------------------- the example with values

    def worked_example(self):
        given = given_block([
            f"PC             = {PROGRAM_ADDRESS}",
            f"Memory[{PROGRAM_ADDRESS}]  = {INSTRUCTION}",
            f"Memory[{OPERAND_ADDRESS}]  = {OPERAND_VALUE}",
            f"ACC            = {ACC_BEFORE}",
        ], size=LABEL_SIZE)

        with self.beat("example") as t:
            self.wipe(t)
            sol = WorkedSolution(given, title="One instruction, with values",
                                 floor=-2.9)
            self.play(Write(sol.title), run_time=t.fill(0.14))
            self.play(Create(sol.problem[0]), run_time=t.fill(0.14))
            self.sol = sol
            t.hold()
        for name in ["assume", "given_mem", "given_7", "given_acc"]:
            with self.beat(name) as t:
                index = ["assume", "given_mem", "given_7",
                         "given_acc"].index(name)
                self.play(FadeIn(self.sol.problem[1][index]),
                          run_time=t.fill(0.3))
                t.hold()
        with self.beat("means") as t:
            meaning = fit(serif(f"add what is at {OPERAND_ADDRESS} to what "
                                f"is in the ACC", LABEL_SIZE, GREY))
            scroll = self.sol.place(meaning, buff=GAP_MD * 1.1)
            if scroll:
                self.play(*scroll, run_time=t.fill(0.1))
            self.play(FadeIn(meaning), run_time=t.fill(0.3))
            t.hold()

        def step(t, text, color=CHARCOAL, size=LABEL_SIZE, fraction=0.35,
                 maker=rtn, buff=None):
            line = maker(text, size, color)
            scroll = self.sol.place(line, buff=buff)
            if scroll:
                self.play(*scroll, run_time=t.fill(0.08))
            self.play(Write(line), run_time=t.fill(fraction))
            return line

        with self.beat("ex_fetch") as t:
            self.clear(t, self.sol.clear_steps(), fraction=0.08)
            step(t, "FETCH", SLATE, fraction=0.3, maker=lambda s, z, c:
                 serif(s, z, c), buff=GAP_MD * 1.1)
            t.hold()
        with self.beat("ex_mar") as t:
            step(t, f"MAR ← {PROGRAM_ADDRESS}")
            t.hold()
        with self.beat("ex_pc") as t:
            step(t, f"PC  ← {PROGRAM_ADDRESS + 1}")
            t.hold()
        with self.beat("ex_mdr") as t:
            step(t, f"MDR ← {INSTRUCTION}")
            t.hold()
        with self.beat("ex_cir") as t:
            step(t, f"CIR ← {INSTRUCTION}")
            t.hold()
        with self.beat("ex_decode") as t:
            self.clear(t, self.sol.clear_steps(), fraction=0.1)
            step(t, "DECODE", SLATE, fraction=0.3, maker=lambda s, z, c:
                 serif(s, z, c), buff=GAP_MD * 1.1)
            t.hold()
        with self.beat("ex_identify") as t:
            step(t, "operation  ADD", fraction=0.25)
            step(t, f"operand    the value at {OPERAND_ADDRESS}", fraction=0.3)
            t.hold()
        with self.beat("ex_read") as t:
            self.clear(t, self.sol.clear_steps(), fraction=0.08)
            step(t, "EXECUTE", SLATE, fraction=0.22, maker=lambda s, z, c:
                 serif(s, z, c), buff=GAP_MD * 1.1)
            step(t, f"MAR ← {OPERAND_ADDRESS}", fraction=0.25)
            t.hold()
        with self.beat("ex_7") as t:
            step(t, f"MDR ← {OPERAND_VALUE}")
            t.hold()
        with self.beat("ex_add") as t:
            step(t, f"ACC ← {ACC_BEFORE} + {OPERAND_VALUE}", TERRACOTTA)
            t.hold()
        with self.beat("ex_sum") as t:
            total = MathTex(rf"{ACC_BEFORE} + {OPERAND_VALUE} = "
                            rf"{ACC_BEFORE + OPERAND_VALUE}",
                            font_size=DISPLAY_SIZE, color=CHARCOAL)
            scroll = self.sol.place(total, buff=GAP_MD * 0.9)
            if scroll:
                self.play(*scroll, run_time=t.fill(0.1))
            self.play(Write(total), run_time=t.fill(0.4))
            t.hold()
        with self.beat("ex_store") as t:
            step(t, f"ACC ← {ACC_BEFORE + OPERAND_VALUE}", SAGE)
            t.hold()
        with self.beat("ex_after") as t:
            self.clear(t, self.sol.clear_steps(), fraction=0.1)
            t.hold()
        with self.beat("ex_state") as t:
            final = answer_box(self.lines(
                f"ACC = {ACC_BEFORE + OPERAND_VALUE}",
                f"PC  = {PROGRAM_ADDRESS + 1}",
                size=BODY_SIZE, align=LEFT, buff=GAP_SM,
            ))
            scroll = self.sol.place(final, buff=GAP_MD * 1.2)
            if scroll:
                self.play(*scroll, run_time=t.fill(0.08))
            self.play(Create(final[0]), FadeIn(final[1]), run_time=t.fill(0.4))
            t.hold()
        with self.beat("one_complete") as t:
            done = fit(serif("one complete instruction, through the processor",
                             LABEL_SIZE, GREY))
            scroll = self.sol.place(done, buff=GAP_MD)
            if scroll:
                self.play(*scroll, run_time=t.fill(0.1))
            self.play(FadeIn(done), run_time=t.fill(0.3))
            t.hold()

    # ------------------------------------------------------------- the buses

    def the_buses(self):
        memory_rows = [
            (PROGRAM_ADDRESS, INSTRUCTION),
            (PROGRAM_ADDRESS + 1, "..."),
            (None, None),
            (OPERAND_ADDRESS, OPERAND_VALUE),
        ]
        with self.beat("buses") as t:
            self.part(t, 4)
            self.wipe(t)
            self.band_x, self.band_width = 0.0, 11.0
            self.title(t, "What the buses carry", fraction=0.08)
            self.build_diagram(
                t,
                [("PC", PROGRAM_ADDRESS + 1), ("MAR", OPERAND_ADDRESS),
                 ("MDR", OPERAND_VALUE), ("CIR", INSTRUCTION)],
                memory_rows, draw=0.6,
            )
            t.hold()
        with self.beat("buses_routes") as t:
            self.aside(t, "the routes between them",
                       fraction=0.25)
            t.hold()

        self.bus_arrow = None

        def show_bus(t, index, two_way, text, fraction=0.3):
            arrow = self.buses.arrow(index, two_way=two_way)
            if self.bus_arrow is not None:
                self.play(FadeOut(self.bus_arrow), run_time=t.fill(0.06))
            self.play(Create(arrow), run_time=t.fill(0.2))
            self.bus_arrow = arrow
            self.aside(t, text, fraction=fraction)

        with self.beat("addr_bus") as t:
            show_bus(t, 0, False, "an address, processor to memory")
            t.hold()
        with self.beat("addr_oneway") as t:
            self.aside(t, "one way: the processor asks",
                       fraction=0.3)
            t.hold()
        with self.beat("data_bus_role") as t:
            show_bus(t, 1, True, "instructions and data")
            t.hold()
        with self.beat("data_bidir") as t:
            self.aside(t, "both ways, in and out",
                       fraction=0.3)
            t.hold()
        with self.beat("ctrl_bus") as t:
            show_bus(t, 2, False, "control signals")
            t.hold()
        with self.beat("ctrl_examples") as t:
            self.aside(t, "read, write, clock, interrupt", fraction=0.3)
            t.hold()
        with self.beat("in_example") as t:
            self.play(FadeOut(self.bus_arrow), run_time=t.fill(0.06))
            self.bus_arrow = None
            self.aside(t, f"{PROGRAM_ADDRESS} on the address bus", fraction=0.12)
            self.send(t, 0, PROGRAM_ADDRESS, fraction=0.55)
            t.hold()
        with self.beat("ctrl_read") as t:
            self.aside(t, "READ on the control bus", fraction=0.12)
            self.send(t, 2, "READ", fraction=0.6, color=SLATE)
            t.hold()
        with self.beat("data_back") as t:
            self.aside(t, "the instruction comes back", fraction=0.1)
            self.send(t, 1, INSTRUCTION, reverse=True, fraction=0.6)
            t.hold()
        with self.beat("operand_trip") as t:
            self.aside(t, "again, for the operand", fraction=0.08)
            self.send(t, 0, OPERAND_ADDRESS, fraction=0.26)
            self.send(t, 2, "READ", fraction=0.26, color=SLATE)
            self.send(t, 1, OPERAND_VALUE, reverse=True, fraction=0.3)
            t.hold()

    def bus_roles(self):
        with self.beat("roles") as t:
            self.wipe(t)
            head = self.title(t, "Keep the three apart", fraction=0.12)
            rows = self.lines(
                "address bus   where to access",
                "data bus      what is being transferred",
                "control bus   what action should happen",
                size=BODY_SIZE, align=LEFT,
            )
            self.stack(rows, head, buff=GAP_MD * 1.4, align=LEFT)
            self.hide(rows)
            self.reveal(t, rows, 0, 1, 0.3)
            self.bus_rows = rows
            t.hold()
        with self.beat("where_what") as t:
            self.reveal(t, self.bus_rows, 1, 2, 0.4)
            t.hold()
        with self.beat("ctrl_what") as t:
            self.reveal(t, self.bus_rows, 2, 3, 0.4)
            t.hold()

    # --------------------------------------------------- AS Level: more registers

    def as_registers(self):
        rows = [
            ("ACC", "Accumulator", "intermediate results from the ALU"),
            ("IX", "Index Register", "an offset, for stepping through an array"),
            ("SR", "Status Register", "flags about the result of an operation"),
        ]
        with self.beat("as_level") as t:
            self.wipe(t)
            head = self.title(t, "AS Level: three more registers",
                              fraction=0.14)
            group = VGroup()
            for name, full, role in rows:
                box = RegisterBox(name, None, width=2.2)
                words = VGroup(
                    serif(full, LABEL_SIZE, CHARCOAL),
                    serif(role, MARGIN_SIZE, GREY),
                ).arrange(DOWN, buff=GAP_SM * 0.2, aligned_edge=LEFT)
                words.next_to(box, RIGHT, buff=GAP_MD * 1.1)
                group.add(VGroup(box, words))
            group.arrange(DOWN, buff=GAP_MD * 1.1, aligned_edge=LEFT)
            fit(group)
            self.stack(group, head, buff=GAP_MD * 1.2, align=LEFT, floor=-1.8)
            self.as_rows = group
            t.hold()
        for index, name in enumerate(["acc", "ix", "status"]):
            with self.beat(name) as t:
                row = self.as_rows[index]
                self.play(Create(row[0]), run_time=t.fill(0.3))
                self.play(FadeIn(row[1]), run_time=t.fill(0.3))
                t.hold()
        with self.beat("flags") as t:
            flags = prose("a zero flag, a carry flag, an overflow flag",
                          LABEL_SIZE, TERRACOTTA)
            self.place(flags, self.as_rows, buff=GAP_MD * 0.9)
            self.play(FadeIn(flags), run_time=t.fill(0.3))
            self.flags = flags
            t.hold()
        with self.beat("no_change") as t:
            same = fit(serif("None of them changes the cycle.",
                             BODY_SIZE, CHARCOAL))
            same.move_to(self.flags)
            self.play(Transform(self.flags, same), run_time=t.fill(0.3))
            t.hold()
        with self.beat("more_places") as t:
            more = fit(serif("They give the processor more places to hold "
                             "what it needs.", LABEL_SIZE, GREY))
            more.move_to(self.flags)
            self.play(Transform(self.flags, more), run_time=t.fill(0.3))
            t.hold()

    def notation_rules(self):
        pairs = [
            ("MAR ← [PC]", "copy the contents of the PC into the MAR"),
            ("MDR ← [[MAR]]",
             "read what is at the address in the MAR into the MDR"),
            ("CIR ← [MDR]", "copy the instruction from the MDR into the CIR"),
        ]
        with self.beat("rtn") as t:
            self.wipe(t)
            head = self.title(t, "Register-transfer notation", fraction=0.12)
            one_step = prose("Follow it one step at a time. Never skip "
                             "ahead.", LABEL_SIZE, TERRACOTTA)
            self.place(one_step, head, buff=GAP_MD * 0.8)
            self.play(FadeIn(one_step), run_time=t.fill(0.3))

            group = VGroup()
            for line, gloss in pairs:
                group.add(VGroup(
                    rtn(line, BODY_SIZE),
                    prose(gloss, MARGIN_SIZE, GREY, 11.0),
                ).arrange(DOWN, buff=GAP_SM * 0.5, aligned_edge=LEFT))
            group.arrange(DOWN, buff=GAP_MD * 1.05, aligned_edge=LEFT)
            fit(group)
            self.stack(group, one_step, buff=GAP_MD * 1.05, align=LEFT, floor=-2.3)
            self.hide(group)
            self.rtn_rows = group
            t.hold()
        for index, name in enumerate(["rtn_1", "rtn_2", "rtn_3"]):
            with self.beat(name) as t:
                row = self.rtn_rows[index]
                row.set_opacity(1)
                self.play(Write(row[0]), run_time=t.fill(0.3))
                self.play(FadeIn(row[1]), run_time=t.fill(0.25))
                t.hold()
        with self.beat("rtn_vary") as t:
            vary = prose("The notation varies between questions.",
                         LABEL_SIZE, GREY)
            self.place(vary, self.rtn_rows, buff=GAP_MD * 0.8)
            self.play(FadeIn(vary), run_time=t.fill(0.3))
            t.hold()

    # ----------------------------------------------------- student challenge

    def challenge(self):
        self.given = given_block([
            f"PC            = {CHALLENGE['pc']}",
            f"Memory[{CHALLENGE['pc']}]   = ADD {CHALLENGE['operand']}",
            f"Memory[{CHALLENGE['operand']}]   = {CHALLENGE['value']}",
            f"ACC           = {CHALLENGE['acc']}",
        ], size=LABEL_SIZE)

        with self.beat("challenge") as t:
            self.part(t, 5)
            self.wipe(t)
            self.ch_head = self.title(t, "Your turn", fraction=0.14)
            t.hold()
        with self.beat("ch_predict") as t:
            ask = prose("What is in the ACC after it executes?", BODY_SIZE)
            self.place(ask, self.ch_head, buff=GAP_MD * 0.9)
            self.play(Write(ask), run_time=t.fill(0.35))
            self.ch_ask = ask
            t.hold()

        self.place(self.given, self.ch_ask, buff=GAP_MD * 1.1)
        with self.beat("ch_given") as t:
            self.play(Create(self.given[0]), run_time=t.fill(0.2))
            self.play(FadeIn(self.given[1][0]), run_time=t.fill(0.3))
            t.hold()
        with self.beat("ch_mem") as t:
            self.play(FadeIn(self.given[1][1]), run_time=t.fill(0.4))
            t.hold()
        with self.beat("ch_700") as t:
            self.play(FadeIn(self.given[1][2]), run_time=t.fill(0.4))
            t.hold()
        with self.beat("ch_acc") as t:
            self.play(FadeIn(self.given[1][3]), run_time=t.fill(0.4))
            t.hold()
        with self.beat("ch_pause") as t:
            pause = serif("Pause here.", BODY_SIZE, TERRACOTTA)
            self.place(pause, self.given, buff=GAP_MD * 0.8)
            self.play(Write(pause), run_time=t.fill(0.12))
            self.pause_line = pause
            t.hold()

    def challenge_answer(self):
        """The givens move aside and the trace runs beside them.

        Stacked under the givens there is no room for five steps, a boxed
        answer and a closing line — two columns is not decoration here, it
        is the only way the whole trace and what it started from are on
        screen together at full size.
        """
        # One left-aligned block, revealed a line at a time: hung one off
        # the last, each line centres on the one above and the trace comes
        # out ragged.
        self.ch_steps = VGroup(
            rtn(f"CIR ← ADD {CHALLENGE['operand']}", LABEL_SIZE),
            rtn(f"PC  ← {CHALLENGE['pc'] + 1}", LABEL_SIZE),
            rtn(f"ADD, operand at {CHALLENGE['operand']}", LABEL_SIZE, GREY),
            rtn(f"MDR ← {CHALLENGE['value']}", LABEL_SIZE),
            rtn("ACC ← ACC + MDR", LABEL_SIZE, TERRACOTTA),
        ).arrange(DOWN, buff=GAP_SM * 1.35, aligned_edge=LEFT)
        self.ch_steps.move_to([3.6, 1.35, 0])

        with self.beat("ch_answer") as t:
            self.play(FadeOut(self.pause_line), FadeOut(self.ch_ask),
                      FadeOut(self.ch_head), run_time=t.fill(0.08))
            self.play(self.given.animate.move_to([-3.45, 1.0, 0]),
                      run_time=t.fill(0.14))
            self.play(Write(self.ch_steps[0]), run_time=t.fill(0.3))
            t.hold()
        with self.beat("ch_pc") as t:
            self.play(Write(self.ch_steps[1]), run_time=t.fill(0.4))
            t.hold()
        with self.beat("ch_decode") as t:
            self.play(Write(self.ch_steps[2]), run_time=t.fill(0.4))
            t.hold()
        with self.beat("ch_read") as t:
            self.play(Write(self.ch_steps[3]), run_time=t.fill(0.4))
            t.hold()
        with self.beat("ch_add") as t:
            self.play(Write(self.ch_steps[4]), run_time=t.fill(0.4))
            t.hold()
        with self.beat("ch_15") as t:
            total = CHALLENGE["acc"] + CHALLENGE["value"]
            final = answer_box(MathTex(
                rf"\text{{ACC}} = {CHALLENGE['acc']} + {CHALLENGE['value']} "
                rf"= {total}", font_size=DISPLAY_SIZE, color=CHARCOAL))
            final.move_to([0, -1.75, 0])
            self.play(Create(final[0]), Write(final[1]), run_time=t.fill(0.45))
            self.ch_final = final
            t.hold()
        with self.beat("ch_check") as t:
            got = prose("Fifteen means you followed it correctly.",
                        LABEL_SIZE, SAGE)
            got.move_to([0, -2.65, 0])
            self.play(FadeIn(got), run_time=t.fill(0.3))
            self.got = got
            t.hold()
        with self.beat("ch_else") as t:
            again = prose("If not, replay it and keep the registers apart.",
                          LABEL_SIZE, GREY)
            again.move_to(self.got)
            self.play(Transform(self.got, again), run_time=t.fill(0.35))
            t.hold()

    # ------------------------------------------------- mistakes, then the recap

    def mistakes(self):
        with self.beat("mistakes") as t:
            self.wipe(t)
            head = self.title(t, "Three mistakes to avoid", fraction=0.18)
            self.m_head = head
            t.hold()
        with self.beat("three_common") as t:
            seen = fit(serif("Strong students make all three.",
                             LABEL_SIZE, GREY))
            self.place(seen, self.m_head, buff=GAP_MD)
            self.play(FadeIn(seen), run_time=t.fill(0.2))
            self.seen = seen
            t.hold()
        with self.beat("all_the_time") as t:
            t.hold()

        pairs = [
            ("the MAR stores the instruction",
             "it stores the address being accessed"),
            ("the MDR stores the address",
             "it stores the data or instruction being transferred"),
            ("decode can be skipped",
             "the CU must interpret it before it runs"),
        ]
        self.m_rows = VGroup()
        for wrong, right in pairs:
            self.m_rows.add(VGroup(
                serif(wrong, LABEL_SIZE, GREY),
                prose(right, LABEL_SIZE, SAGE, 11.6),
            ).arrange(DOWN, buff=GAP_SM * 0.55, aligned_edge=LEFT))
        self.m_rows.arrange(DOWN, buff=GAP_MD * 1.15, aligned_edge=LEFT)
        fit(self.m_rows)
        self.stack(self.m_rows, self.seen, buff=GAP_MD * 1.1, align=LEFT)
        self.hide(self.m_rows)

        for index, (wrong_beat, right_beat) in enumerate(
                [("m1", "m1_right"), ("m2", "m2_right"), ("m3", "m3_right")]):
            with self.beat(wrong_beat) as t:
                row = self.m_rows[index]
                row.set_opacity(1)
                row[1].set_opacity(0)
                self.play(FadeIn(row[0]), run_time=t.fill(0.3))
                self.play(Create(strike(row[0], GREY)), run_time=t.fill(0.25))
                t.hold()
            with self.beat(right_beat) as t:
                row = self.m_rows[index]
                row[1].set_opacity(1)
                self.play(FadeIn(row[1]), run_time=t.fill(0.35))
                t.hold()

    def recap(self):
        with self.beat("recap") as t:
            self.wipe(t)
            head = self.title(t, "The whole cycle, once", fraction=0.14)
            steps = self.lines(
                "the PC holds the address of the next instruction",
                "that address is copied to the MAR",
                "the instruction goes to the MDR, then to the CIR",
                "the PC is updated, and the CU decodes the instruction",
                "the CPU executes it, using the ALU and the registers",
                size=LABEL_SIZE, align=LEFT,
            )
            self.stack(steps, head, buff=GAP_MD * 1.1, align=LEFT)
            self.hide(steps)
            self.recap_rows = steps
            t.hold()
        with self.beat("r_pc") as t:
            self.reveal(t, self.recap_rows, 0, 1, 0.4)
            t.hold()
        with self.beat("r_mar") as t:
            self.reveal(t, self.recap_rows, 1, 2, 0.4)
            t.hold()
        with self.beat("r_mdr") as t:
            self.reveal(t, self.recap_rows, 2, 3, 0.4)
            t.hold()
        with self.beat("r_pc_up") as t:
            self.reveal(t, self.recap_rows, 3, 4, 0.4)
            t.hold()
        with self.beat("r_execute") as t:
            self.reveal(t, self.recap_rows, 4, 5, 0.35)
            t.hold()
        with self.beat("r_repeat") as t:
            again = fit(serif("then it does it all again, for the next "
                              "instruction", BODY_SIZE, TERRACOTTA))
            self.place(again, self.recap_rows, buff=GAP_MD * 1.3)
            self.play(Write(again), run_time=t.fill(0.4))
            t.hold()
