"""Chapter 4, Software: Cambridge O Level 2210, delivered in English.

Fourteen numbered sections and an opening, each anchored to the recording
by build/beats_ch04.py. Nothing here waits a fixed number of seconds.

The chapter is mostly definitions and comparisons, so the work is in
turning each comparison into a shape that can be remembered and then
reproduced in an exam. Four of those shapes already existed for the
operating-system lectures and are reused rather than redrawn, which is
the point of having them: ``SortBench`` sorts system from application
software and then, unchanged, sorts hardware interrupts from software
ones; ``LayerStack`` carries a request down to the hardware here exactly
as it did there; ``FunctionList`` holds the functions one lit at a time.

Three places where the captions do not match the audio, on purpose. The
delivery has small slips and the beats are anchored to the slips, because
that is what is in the recording, while the screen carries the correct
word:

  * at 357s "when the computer is switched off, firmware runs first" --
    it is switched *on*, and the screen says so.
  * at 1110s "it may also exclude a run-time environment" -- include.
  * at 1121s "point to the location where a program was found" -- the
    problem, not the program.

Each of those is one wrong word in an otherwise correct sentence, and a
student reading the screen gets the right one. They are listed here
rather than silently fixed so that the next person knows the mismatch is
deliberate and does not "correct" the anchors into phrases that are not
in the audio.

One stretch of the delivery repeats itself: at 660-672 a sentence is
started, abandoned and restarted. It was checked against a fresh
transcription of those thirty seconds alone and it is genuinely what was
said, not the decoder looping, so it is left alone and ``low_control``
anchors on the finished version.

The one number worth saying out loud: the opcodes in the machine-code
block are invented for the lesson, and the screen says so in as many
words. The binary operands are not invented -- 200 is 11001000 and 5 is
00000101, and they are computed here rather than typed, so the column
cannot drift away from the decimal it claims to be.

Timing: timings/cs.software.json
Render: python build/render.py scripts/CH04-software.md \\
    audio/CH04-software.m4a
"""

import textwrap
from contextlib import contextmanager

from manim import (
    Create,
    FadeIn,
    FadeOut,
    Line,
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
from components.os_core import Chain, callout
from components.os_shape import FunctionList, LayerStack, SortBench, chips, grid
from components.software import (
    BootStack,
    CodeBlock,
    IDEWindow,
    InterruptTimeline,
    Ladder,
    PollVsSignal,
    TranslatorFlow,
)
from components.syllabus_map import TopicStrip
from scenes.base import SATScene

FRAME_SAFE = 12.6
FLOOR = -3.05          # the numbered strip owns everything below this
BARE_FLOOR = -3.5      # before the strip exists

PARTS = ["Two kinds of software", "The OS as the link",
         "What the OS manages", "Start-up", "What an interrupt is",
         "Handling an interrupt", "High and low level",
         "Machine code and assembly", "The compiler", "The interpreter",
         "Side by side", "The IDE", "One example", "Recap"]
(SYSAPP, LINK, MANAGES, STARTUP, INTERRUPT, HANDLING, LEVELS, ASM,
 COMPILER, INTERPRETER, SIDEBYSIDE, IDE, EXAMPLE, RECAP) = range(14)

HARDWARE = ["Processor", "Memory", "Storage", "Input devices",
            "Output devices"]
BEFORE = ["Open a browser", "Write a document", "Play a game"]
# Short enough for two columns at LABEL_SIZE. grep the longest entry in
# each column, not overall: grid() lays items 0,2,4,6 down the left and
# 1,3,5,7 down the right, so it is those two maxima that have to fit.
AGENDA = ["System and application", "The operating system",
          "Start-up and bootloader", "Interrupts and the ISR",
          "High and low level", "Compiler and interpreter",
          "Assembly and assemblers", "The IDE"]

SYSTEM_EXAMPLES = ["Operating systems", "Device drivers",
                   "Utility programs"]
APP_EXAMPLES = ["Word processor", "Web browser", "Database application",
                "Game"]

COORDINATES = ["Processor", "Memory", "Files", "Connected devices"]

# The four the lecture numbers off, and then the four it gathers up as
# "and also". Split because they are delivered that way, and because all
# eight as one numbered column at this size reaches into the commentary
# band at the bottom of the frame.
MANAGES_LIST = ["File management", "Memory management", "Multitasking",
                "Peripheral management"]
ALSO_MANAGES = ["User interface", "User accounts", "Security",
                "Interrupt handling"]

HW_INTERRUPTS = ["A key press", "A mouse movement",
                 "Network data arrives", "A printer finishing"]
SW_INTERRUPTS = ["Division by zero", "A request to the OS"]

STEPS = ["Finish the instruction", "Save the state",
         "Handle the interrupt", "Restore the state",
         "Resume the program"]

HIGH_NOTES = ["easier to read and write",
              "portable across processors",
              "still has to be translated"]
# Four, because low level has four beats to fill and one note per beat
# reads better than two notes and a recolour.
LOW_NOTES = ["precise hardware control",
             "useful when timing matters",
             "harder to write",
             "tied to one processor"]

# An invented instruction set. The mnemonics are the ordinary Cambridge
# ones; the four-bit opcodes are made up for the lesson and the screen
# says so. The operands are computed from the decimals below so the
# binary column cannot drift away from what it claims to be.
ASSEMBLY_CODE = [("LDD", 200, "0011"), ("ADD", 5, "0101"),
                 ("STO", 200, "0100")]

# A program that obeys every rule of its language and still answers the
# wrong question: the error is a minus where a plus belongs. This is the
# one thing a compiler cannot find, and the syllabus asks for it.
WRONG_SUM = ["total = 0", "FOR each mark", "   total = total - mark",
             "NEXT mark", "average = total / count"]

RAGGED = ["IF mark >= 50 THEN", "OUTPUT \"pass\"", "ELSE",
          "OUTPUT \"fail\"", "ENDIF"]
TIDY = ["IF mark >= 50 THEN", "   OUTPUT \"pass\"", "ELSE",
        "   OUTPUT \"fail\"", "ENDIF"]

IDE_TOOLS = ["Code editor", "Translator", "Run-time environment",
             "Error diagnostics", "Auto-completion", "Auto-correction",
             "Prettyprinting"]

# Every row compares the same feature on both sides, because that is
# exactly what the lecture says a comparison answer has to do.
COMPARISON = [
    ("Translates", "whole program first", "one line at a time"),
    ("Produces", "an executable file", "no separate file"),
    ("Reports errors", "after compiling", "it stops at the error"),
    ("Running speed", "already translated", "translating as it runs"),
    ("Best for", "finished programs", "developing and testing"),
]

RECAP_CARDS = [
    ("Two kinds of software", [
        "System software serves the computer.",
        "Application software serves the user.",
    ]),
    ("The operating system", [
        "It manages files, memory and processor time.",
        "It manages peripherals, accounts and security.",
        "Applications ask it for the services they need.",
    ]),
    ("Start-up", [
        "Firmware initialises the hardware.",
        "The bootloader loads the OS into RAM.",
        "The OS then supports the applications.",
    ]),
    ("An interrupt", [
        "Finish the instruction, save the state,",
        "run the ISR, restore the state, resume.",
        "The original program is never discarded.",
    ]),
    ("Languages and translators", [
        "High-level: easier to read and portable.",
        "Low-level: closer control of the hardware.",
        "An assembler makes machine code from assembly.",
        "A compiler translates the whole program first.",
        "An interpreter translates a line at a time.",
    ]),
]

QUESTIONS = [
    "What makes a utility program system software?",
    "Name three functions of an operating system.",
    "Put firmware, bootloader and the OS in order.",
    "List the five steps of handling an interrupt.",
    "Give one reason to choose a low-level language.",
    "Compare a compiler and an interpreter.",
    "Name two IDE features, and say what each does.",
]


def fit(mobject, width=FRAME_SAFE):
    if mobject.width > width:
        mobject.scale_to_fit_width(width)
    return mobject


def prose(text, size=BODY_SIZE, color=CHARCOAL, width=FRAME_SAFE):
    """A sentence that wraps to fit rather than shrinking to fit."""
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


def machine_code():
    """The binary beside the mnemonics, computed rather than typed."""
    assembly = [f"{name}  {operand}" for name, operand, _ in ASSEMBLY_CODE]
    binary = [f"{opcode} {operand:08b}" for _, operand, opcode in ASSEMBLY_CODE]
    return assembly, binary


class Software(SATScene):
    scene_id = "cs.software"

    def construct(self):
        self.margin = mono("Software · Chapter 4", MARGIN_SIZE)
        self.margin.to_corner(UP + LEFT, buff=GAP_SM)
        self.add(self.margin)

        self.strip = TopicStrip(len(PARTS), lit=SLATE, side=0.56)
        self.strip.to_edge(DOWN, buff=GAP_SM * 0.5)

        self.keep = [self.margin]
        self.floor = BARE_FLOOR
        self.head = None
        self.note = None
        self.side = None

        self.opening()
        self.two_kinds()
        self.the_link()
        self.what_it_manages()
        self.start_up()
        self.what_an_interrupt_is()
        self.handling_an_interrupt()
        self.high_and_low()
        self.machine_and_assembly()
        self.the_compiler()
        self.the_interpreter()
        self.side_by_side()
        self.the_ide()
        self.one_example()
        self.recap()
        self.self_check()

    # --------------------------------------------------------------- opening

    def opening(self):
        with self.beat("open") as t:
            chapter = serif("Chapter 4", LABEL_SIZE, SLATE)
            title = serif("Software", DISPLAY_SIZE, CHARCOAL)
            board = prose("Cambridge O Level Computer Science 2210",
                          LABEL_SIZE, GREY)
            card = VGroup(chapter, title, board).arrange(DOWN, buff=GAP_MD)
            card.move_to(ORIGIN)
            self.play(FadeIn(chapter), run_time=t.fill(0.1))
            self.play(Write(title), run_time=t.fill(0.26))
            self.play(FadeIn(board), run_time=t.fill(0.16))
            t.hold()

        with self.beat("hardware") as t:
            self.wipe(t)
            self.title(t, "A computer is physical components", fraction=0.14)
            bits, each = chips(HARDWARE, size=LABEL_SIZE, rows=2)
            self.place(bits, self.head, buff=GAP_LG * 0.9)
            self.hardware = bits
            for chip in each:
                self.play(FadeIn(chip), run_time=t.fill(0.11))
            t.hold()

        with self.beat("needs_instructions") as t:
            self.say(t, "But hardware alone cannot perform a useful task",
                     fraction=0.3)
            t.hold()

        with self.beat("provided_by") as t:
            answer = serif("It needs instructions", TITLE_SIZE, CHARCOAL)
            word = serif("Software", TITLE_SIZE, TERRACOTTA)
            pair = VGroup(answer, word).arrange(DOWN, buff=GAP_MD)
            self.place(pair, self.hardware, buff=GAP_MD * 1.2)
            self.play(FadeIn(answer), run_time=t.fill(0.22))
            self.play(Write(word), run_time=t.fill(0.3))
            t.hold()

        with self.beat("switch_on") as t:
            self.wipe(t)
            self.title(t, "You switch the computer on", fraction=0.14)
            t.hold()

        with self.beat("before_browser") as t:
            tasks, each = chips(BEFORE, size=LABEL_SIZE, rows=1)
            self.place(tasks, self.head, buff=GAP_LG)
            self.tasks = tasks
            for chip in each:
                self.play(FadeIn(chip), run_time=t.fill(0.2))
            t.hold()

        with self.beat("must_start") as t:
            self.say(t, "first it has to start up and organise its "
                        "resources", fraction=0.3)
            t.hold()

        with self.beat("makes_possible") as t:
            line = serif("Software makes that possible", TITLE_SIZE,
                         TERRACOTTA)
            self.place(line, self.tasks, buff=GAP_LG * 0.9)
            self.play(Write(line), run_time=t.fill(0.4))
            t.hold()

        with self.beat("agenda_sysapp") as t:
            self.wipe(t)
            self.title(t, "What this chapter covers", fraction=0.11)
            plan, items = grid(AGENDA, columns=2, size=LABEL_SIZE,
                               h_gap=GAP_MD * 1.2, v_gap=GAP_SM * 1.6)
            self.place(plan, self.head, buff=GAP_MD * 1.4)
            self.plan_items = items
            for item in items[:2]:
                self.play(FadeIn(item), run_time=t.fill(0.18))
            t.hold()

        with self.beat("agenda_os") as t:
            for item in items[2:4]:
                self.play(FadeIn(item), run_time=t.fill(0.2))
            t.hold()

        with self.beat("agenda_interrupt") as t:
            for item in items[4:6]:
                self.play(FadeIn(item), run_time=t.fill(0.2))
            t.hold()

        with self.beat("agenda_lang") as t:
            for item in items[6:]:
                self.play(FadeIn(item), run_time=t.fill(0.2))
            t.hold()

        with self.beat("focus") as t:
            self.say(t, "For each one: what is its purpose, and how do "
                        "the parts work together", fraction=0.34)
            t.hold()

    # ------------------------------------------- 1. two kinds of software

    def two_kinds(self):
        bench = None

        with self.beat("two_categories") as t:
            self.section(t, "Two kinds of software", SYSAPP)
            bench = SortBench("System software", "Application software")
            bench.next_to(self.head, DOWN, buff=GAP_MD)
            self.bench = bench
            self.play(Write(bench.heads[0]), Write(bench.heads[1]),
                      run_time=t.fill(0.3))
            self.play(Create(bench.rules), run_time=t.fill(0.22))
            t.hold()

        with self.beat("sys_defn") as t:
            self.play(FadeIn(bench.caption(
                0, "serves the computer")), run_time=t.fill(0.3))
            t.hold()

        with self.beat("sys_helps") as t:
            self.say(t, "it helps the computer operate and manage its "
                        "own resources", fraction=0.3)
            t.hold()

        with self.beat("sys_examples") as t:
            for text in SYSTEM_EXAMPLES:
                self.play(FadeIn(bench.item(0, text)),
                          run_time=t.fill(0.16))
            t.hold()

        with self.beat("app_defn") as t:
            self.play(FadeIn(bench.caption(1, "serves the user")),
                      run_time=t.fill(0.34))
            t.hold()

        for beat_name, text in zip(
                ("app_word", "app_browser", "app_db", "app_game"),
                APP_EXAMPLES):
            with self.beat(beat_name) as t:
                self.play(FadeIn(bench.item(1, text)), run_time=t.fill(0.3))
                t.hold()

        with self.beat("purpose_not_person") as t:
            self.say(t, "The test is purpose, not whether a person opens it",
                     fraction=0.3)
            t.hold()

        with self.beat("utility_case") as t:
            self.wipe(t)
            self.title(t, "So which is a backup utility?", fraction=0.14)
            case = self.lines(
                "You open it yourself, from the menu.",
                "Its purpose is to protect the computer.",
            )
            self.stack(case, self.head, buff=GAP_LG * 0.8)
            self.case = case
            self.play(FadeIn(case[0]), run_time=t.fill(0.34))
            t.hold()

        with self.beat("even_though") as t:
            self.play(FadeIn(self.case[1]), run_time=t.fill(0.4))
            t.hold()

        with self.beat("therefore_system") as t:
            verdict = serif("System software", TITLE_SIZE, SAGE)
            self.place(verdict, self.case, buff=GAP_LG * 0.8)
            self.play(Write(verdict), run_time=t.fill(0.4))
            t.hold()

        with self.beat("exam_rule_1") as t:
            self.wipe(t)
            self.title(t, "In the exam, say what it does", fraction=0.12)
            rule = callout([
                "System software supports the computer.",
                "Application software helps the user",
                "perform a task.",
            ], size=LABEL_SIZE, width=10.4)
            self.place(rule, self.head, buff=GAP_LG)
            self.play(Create(rule[0]), run_time=t.fill(0.2))
            for line in rule[1]:
                self.play(FadeIn(line), run_time=t.fill(0.14))
            t.hold()

    # ----------------------------------------- 2. the OS as the link

    def the_link(self):
        # Narrow, and pushed left, because the commentary for this
        # section sits beside the figure rather than under it: a 7.2-unit
        # stack centred on zero reaches x=3.6 and runs straight into a
        # note at x=4.3.
        stack = LayerStack(["Application program", "Operating system",
                            "Device driver", "Hardware"], width=5.6)

        with self.beat("os_central") as t:
            self.section(t, "The operating system", LINK)
            self.say(t, "the central part of the system software",
                     fraction=0.3)
            t.hold()

        with self.beat("os_link") as t:
            self.clear(t, self.note, fraction=0.08)
            self.note = None
            self.place(stack, self.head, buff=GAP_MD * 1.1)
            stack.shift(LEFT * 2.9)
            self.stack_fig = stack
            self.play(Create(stack.boxes), run_time=t.fill(0.3))
            self.play(*[FadeIn(label) for label in stack.labels],
                      run_time=t.fill(0.18))
            t.hold()

        with self.beat("suppose_save") as t:
            self.side_note(t, "A word processor needs to save a document.",
                           fraction=0.3, x=3.6, y=1.9, width=5.2)
            t.hold()

        with self.beat("app_requests") as t:
            self.play(*stack.light(0), run_time=t.fill(0.2))
            self.play(Create(stack.arrows[0]), run_time=t.fill(0.2))
            t.hold()

        with self.beat("os_manages") as t:
            self.play(*stack.settle(0), *stack.light(1),
                      run_time=t.fill(0.18))
            self.play(Create(stack.arrows[1]), run_time=t.fill(0.16))
            self.play(*stack.settle(1), *stack.light(2),
                      run_time=t.fill(0.16))
            self.play(Create(stack.arrows[2]), run_time=t.fill(0.16))
            t.hold()

        with self.beat("no_direct") as t:
            self.play(*stack.settle(2), run_time=t.fill(0.12))
            self.side_note(t, "The application never drives the device "
                              "itself.", fraction=0.3, x=3.6, y=1.9,
                           width=5.2)
            t.hold()

        with self.beat("no_tech_detail") as t:
            self.side_note(t, "It does not need the technical details of "
                              "the storage device.", fraction=0.36,
                           x=3.6, y=1.9, width=5.2)
            t.hold()

        with self.beat("coordinates") as t:
            self.wipe(t)
            self.title(t, "It coordinates all of this", fraction=0.12)
            parts, each = chips(COORDINATES, size=LABEL_SIZE, rows=2)
            self.place(parts, self.head, buff=GAP_LG)
            self.parts = parts
            for chip in each:
                self.play(FadeIn(chip), run_time=t.fill(0.14))
            t.hold()

        with self.beat("appear_same_time") as t:
            self.say(t, "Programs appear to run at once, while the "
                        "processor shares its time between them",
                     fraction=0.4)
            t.hold()

        with self.beat("resource_manager") as t:
            line = serif("a resource manager", TITLE_SIZE, TERRACOTTA)
            self.place(line, self.parts, buff=GAP_LG * 0.9)
            self.play(Write(line), run_time=t.fill(0.4))
            t.hold()

    # ------------------------------------ 3. what the OS manages

    def what_it_manages(self):
        listing = FunctionList(MANAGES_LIST, size=LABEL_SIZE)

        with self.beat("functions_open") as t:
            self.section(t, "What the operating system manages", MANAGES)
            self.place(listing, self.head, buff=GAP_MD * 1.2)
            self.listing = listing
            # All eight at once, not one at a time: the beat is 4.6s and
            # the pacing floor is 0.5s a play, so eight plays plus the
            # heading and the strip would need 5.5s and push the next
            # reveal off its word. The lighting that follows walks down
            # the list one function at a time anyway, which is where the
            # one-at-a-time reading belongs.
            self.play(FadeIn(listing.rows), run_time=t.fill(0.3))
            t.hold()

        details = [
            ("fn_file", 0, None),
            ("file_detail", None, "It names files, stores them and "
                                  "retrieves them when asked"),
            ("file_access", None, "and it controls who is allowed to "
                                  "open them"),
            ("fn_memory", 1, None),
            ("ram_alloc", None, "It gives programs and their data space "
                                "in RAM"),
            ("virtual_memory", None, "Virtual memory borrows secondary "
                                     "storage when RAM runs short"),
            ("vm_detail", None, "so a workload larger than RAM can still "
                                "run"),
            ("fn_multitask", 2, None),
            ("mt_detail", None, "It shares processor time between "
                                "processes"),
            ("mt_switch", None, "switching between them so you can use "
                                "several programs"),
            ("fn_peripheral", 3, None),
            ("drivers_help", None, "usually through a device driver"),
            ("driver_defn", None, "A driver holds the instructions for "
                                  "talking to one particular device"),
        ]

        for beat_name, index, text in details:
            with self.beat(beat_name) as t:
                if index is not None:
                    self.play(*listing.focus(index), run_time=t.fill(0.24))
                if text is not None:
                    self.say(t, text, fraction=0.3)
                t.hold()

        with self.beat("and_more") as t:
            self.play(*listing.focus(-1), run_time=t.fill(0.12))
            more, each = chips(ALSO_MANAGES, size=LABEL_SIZE, rows=2)
            self.place(more, listing, buff=GAP_MD * 1.2)
            self.play(FadeIn(more), run_time=t.fill(0.3))
            self.say(t, "and it does all of these too", fraction=0.2)
            t.hold()

        with self.beat("exam_rule_2") as t:
            self.wipe(t)
            self.title(t, "Not enough on its own", fraction=0.12)
            bad = serif("“The operating system manages the computer.”",
                        LABEL_SIZE, GREY)
            bad = fit(bad)
            self.place(bad, self.head, buff=GAP_LG)
            self.bad = bad
            self.play(FadeIn(bad), run_time=t.fill(0.26))
            strike = Line(bad.get_left() + LEFT * GAP_SM * 0.5,
                          bad.get_right() + RIGHT * GAP_SM * 0.5,
                          color=TERRACOTTA, stroke_width=3)
            self.play(Create(strike), run_time=t.fill(0.22))
            t.hold()

        with self.beat("name_a_function") as t:
            good = prose("Name a function, then say what it manages.",
                         TITLE_SIZE, SAGE)
            self.place(good, self.bad, buff=GAP_LG)
            self.play(Write(good), run_time=t.fill(0.45))
            t.hold()

    # ------------------------------------------------- 4. start-up

    def start_up(self):
        # Five boxes have to fit between a heading and the numbered
        # strip, which is 5.4 units, and the default height and gap run
        # 6.32: the stack reached y=-3.95 and sat on the strip.
        boot = BootStack(height=0.68, gap=0.40)
        arrows = boot.starts()

        with self.beat("startup_open") as t:
            self.section(t, "What happens at start-up", STARTUP)
            boot.next_to(self.head, DOWN, buff=GAP_SM * 0.7)
            boot.move_to([-2.4, boot.get_center()[1], 0])
            self.boot = boot
            t.hold()

        reveals = [
            ("base_hardware", 4, "At the base: the processor, memory, "
                                 "storage and devices."),
            ("firmware_first", 3, "Switched on, firmware in non-volatile "
                                  "memory runs first."),
        ]
        for beat_name, index, text in reveals:
            with self.beat(beat_name) as t:
                self.play(Create(boot.boxes[index]), run_time=t.fill(0.2))
                self.play(FadeIn(boot.labels[index]), run_time=t.fill(0.14))
                if index < 4:
                    self.play(Create(arrows[3 - index]),
                              run_time=t.fill(0.14))
                self.side_note(t, text, fraction=0.3, x=4.1, y=1.5,
                               width=5.0)
                t.hold()

        with self.beat("firmware_defn") as t:
            self.side_note(t, "Firmware is software stored in hardware.",
                           fraction=0.4, x=4.1, y=1.5, width=5.0)
            t.hold()

        with self.beat("firmware_tasks") as t:
            self.side_note(t, "It tests and initialises the hardware,",
                           fraction=0.4, x=4.1, y=1.5, width=5.0)
            t.hold()

        with self.beat("begins_boot") as t:
            self.side_note(t, "then it begins the boot process.",
                           fraction=0.4, x=4.1, y=1.5, width=5.0)
            t.hold()

        with self.beat("starts_bootloader") as t:
            self.play(Create(boot.boxes[2]), run_time=t.fill(0.22))
            self.play(FadeIn(boot.labels[2]), run_time=t.fill(0.16))
            self.play(Create(arrows[2]), run_time=t.fill(0.16))
            t.hold()

        with self.beat("bootloader_job") as t:
            self.side_note(t, "Its job: find the operating system in "
                              "secondary storage", fraction=0.4,
                           x=4.1, y=1.5, width=5.0)
            t.hold()

        with self.beat("into_ram") as t:
            self.side_note(t, "and load it into RAM.", fraction=0.4,
                           x=4.1, y=1.5, width=5.0)
            t.hold()

        with self.beat("os_takes_control") as t:
            self.play(Create(boot.boxes[1]), run_time=t.fill(0.2))
            self.play(FadeIn(boot.labels[1]), run_time=t.fill(0.14))
            self.play(Create(arrows[1]), run_time=t.fill(0.14))
            self.side_note(t, "Loaded, the OS takes control of the "
                              "machine's resources.", fraction=0.3,
                           x=4.1, y=1.5, width=5.0)
            t.hold()

        with self.beat("app_can_run") as t:
            self.play(Create(boot.boxes[0]), run_time=t.fill(0.22))
            self.play(FadeIn(boot.labels[0]), run_time=t.fill(0.16))
            self.play(Create(arrows[0]), run_time=t.fill(0.16))
            t.hold()

        with self.beat("app_uses_services") as t:
            self.side_note(t, "and only now can an application ask for "
                              "files, memory and devices.", fraction=0.45,
                           x=4.1, y=1.5, width=5.0)
            t.hold()

        with self.beat("order_matters") as t:
            self.title_swap(t, "The order is the answer", fraction=0.2)
            t.hold()

        with self.beat("order_recap") as t:
            for index in (3, 2, 1, 0):
                self.play(*boot.light(index), run_time=t.fill(0.1))
                self.play(*boot.settle(index), run_time=t.fill(0.08))
            t.hold()

        with self.beat("request_down") as t:
            # A running request takes a different path from a start-up:
            # it goes down through a driver, and the bootloader has
            # finished and is not on it. Drawing it over the boot stack
            # would be tidier and would say something false, so the
            # request gets its own stack -- the same one as section 2.
            self.wipe(t)
            self.title(t, "A running request goes the other way",
                       fraction=0.12)
            # Tighter than the default so the stack clears the
            # commentary band: four boxes at the default height and gap
            # run 4.96 units and reach y=-2.96.
            route = LayerStack(["Application program", "Operating system",
                                "Device driver", "Hardware"],
                               height=0.72, gap=0.44)
            self.place(route, self.head, buff=GAP_MD * 1.1)
            self.play(Create(route.boxes), run_time=t.fill(0.26))
            self.play(*[FadeIn(label) for label in route.labels],
                      run_time=t.fill(0.16))
            self.route = route
            t.hold()

        with self.beat("driver_to_hw") as t:
            self.play(Create(self.route.arrows), run_time=t.fill(0.3))
            self.say(t, "Application, then operating system, then driver, "
                        "then hardware", fraction=0.34)
            t.hold()

    # --------------------------------------- 5. what an interrupt is

    def what_an_interrupt_is(self):
        with self.beat("interrupt_open") as t:
            self.section(t, "What is an interrupt?", INTERRUPT)
            t.hold()

        with self.beat("interrupt_defn") as t:
            defn = prose("A signal or event that needs the processor's "
                         "attention.", BODY_SIZE, CHARCOAL, 11.6)
            self.place(defn, self.head, buff=GAP_LG * 0.9)
            self.defn = defn
            self.play(FadeIn(defn), run_time=t.fill(0.34))
            t.hold()

        with self.beat("why_needed") as t:
            ask = serif("Why not just keep asking?", TITLE_SIZE, SLATE)
            self.place(ask, self.defn, buff=GAP_LG * 0.9)
            self.play(Write(ask), run_time=t.fill(0.4))
            t.hold()

        figure = PollVsSignal()

        with self.beat("polling") as t:
            self.wipe(t)
            self.title(t, "The processor asks every device in turn",
                       fraction=0.12)
            self.place(figure, self.head, buff=GAP_MD * 1.4)
            self.figure = figure
            self.play(Create(figure.cpu_box), FadeIn(figure.cpu_label),
                      run_time=t.fill(0.14))
            self.play(Create(figure.boxes), run_time=t.fill(0.14))
            self.play(*[FadeIn(label) for label in figure.labels],
                      run_time=t.fill(0.1))
            for arrow in figure.asks:
                self.play(Create(arrow), run_time=t.fill(0.11))
            t.hold()

        with self.beat("waste") as t:
            self.say(t, "“Anything for me now?”  —  and all "
                        "that asking wastes processor time", fraction=0.4)
            t.hold()

        with self.beat("instead_signal") as t:
            self.title_swap(t, "So the device speaks up instead",
                            fraction=0.14)
            self.play(*[FadeOut(arrow) for arrow in figure.asks],
                      run_time=t.fill(0.14))
            self.play(Create(figure.signal), run_time=t.fill(0.22))
            self.play(*figure.light_device(0), run_time=t.fill(0.16))
            t.hold()

        with self.beat("deal_with_event") as t:
            self.say(t, "and the processor deals with the event when it "
                        "arrives", fraction=0.34)
            t.hold()

        bench = None

        with self.beat("hw_interrupt") as t:
            self.wipe(t)
            self.title(t, "Two sources", fraction=0.1)
            bench = SortBench("Hardware interrupt", "Software interrupt")
            bench.next_to(self.head, DOWN, buff=GAP_MD)
            self.bench2 = bench
            self.play(Write(bench.heads[0]), Write(bench.heads[1]),
                      run_time=t.fill(0.24))
            self.play(Create(bench.rules), run_time=t.fill(0.18))
            self.play(FadeIn(bench.caption(0, "from a device")),
                      run_time=t.fill(0.2))
            t.hold()

        with self.beat("hw_examples") as t:
            for text in HW_INTERRUPTS[:2]:
                self.play(FadeIn(bench.item(0, text)), run_time=t.fill(0.22))
            t.hold()

        with self.beat("hw_more") as t:
            for text in HW_INTERRUPTS[2:]:
                self.play(FadeIn(bench.item(0, text)), run_time=t.fill(0.22))
            t.hold()

        with self.beat("sw_interrupt") as t:
            self.play(FadeIn(bench.caption(1, "from a program")),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("sw_error") as t:
            self.play(FadeIn(bench.item(1, SW_INTERRUPTS[0])),
                      run_time=t.fill(0.34))
            t.hold()

        with self.beat("sw_request") as t:
            self.play(FadeIn(bench.item(1, SW_INTERRUPTS[1])),
                      run_time=t.fill(0.34))
            t.hold()

        with self.beat("isr_intro") as t:
            self.wipe(t)
            self.title(t, "The processor runs a routine for it",
                       fraction=0.1)
            name = serif("Interrupt service routine", TITLE_SIZE, CHARCOAL)
            short = serif("ISR", DISPLAY_SIZE, TERRACOTTA)
            pair = VGroup(name, short).arrange(DOWN, buff=GAP_MD)
            self.place(pair, self.head, buff=GAP_LG)
            self.isr_card = pair
            self.play(FadeIn(name), run_time=t.fill(0.2))
            self.play(Write(short), run_time=t.fill(0.26))
            t.hold()

        with self.beat("isr_contains") as t:
            self.say(t, "It holds the instructions for dealing with that "
                        "one interrupt", fraction=0.36)
            t.hold()

    # ------------------------------------ 6. handling an interrupt

    def handling_an_interrupt(self):
        timeline = InterruptTimeline()

        with self.beat("steps_open") as t:
            self.section(t, "Handling an interrupt", HANDLING)
            # Not moved. The figure is built at the coordinates the frame
            # needs and its ISR box, arrows and card are attributes
            # rather than group members, so shifting the group would
            # slide the rails out from under them.
            self.timeline = timeline
            self.play(Create(timeline.before), run_time=t.fill(0.24))
            self.play(FadeIn(timeline.running), run_time=t.fill(0.16))
            t.hold()

        with self.beat("step_generated") as t:
            self.play(Create(timeline.flag_line), run_time=t.fill(0.18))
            self.play(FadeIn(timeline.flag_label), run_time=t.fill(0.18))
            t.hold()

        with self.beat("step_finish") as t:
            self.play(Create(timeline.gap_marks[0]), run_time=t.fill(0.3))
            self.title_swap(t, "1  Finish the current instruction",
                            fraction=0.26)
            t.hold()

        with self.beat("not_abandon") as t:
            self.side_note(t, "An instruction is never abandoned "
                              "halfway through.", fraction=0.34,
                           x=4.6, y=-1.9, width=4.5)
            t.hold()

        with self.beat("step_save") as t:
            self.title_swap(t, "2  Save the state of the process",
                            fraction=0.2)
            self.clear(t, self.note, fraction=0.08)
            self.note = None
            self.play(FadeIn(timeline.card), run_time=t.fill(0.34))
            t.hold()

        with self.beat("state_contains") as t:
            self.play(timeline.card_head.animate.set_color(TERRACOTTA),
                      run_time=t.fill(0.3))
            t.hold()

        with self.beat("state_detail") as t:
            self.play(timeline.card_head.animate.set_color(SLATE),
                      run_time=t.fill(0.2))
            self.play(*[row.animate.set_color(SLATE)
                        for row in timeline.card_rows],
                      run_time=t.fill(0.3))
            t.hold()

        with self.beat("priorities") as t:
            self.play(*[row.animate.set_color(CHARCOAL)
                        for row in timeline.card_rows],
                      run_time=t.fill(0.14))
            self.side_note(t, "Several waiting? Priorities decide "
                              "which is handled first.", fraction=0.4,
                           x=4.6, y=-1.9, width=4.5)
            t.hold()

        with self.beat("step_isr") as t:
            self.clear(t, self.note, fraction=0.06)
            self.note = None
            self.title_swap(t, "3  Run the interrupt service routine",
                            fraction=0.18)
            self.play(Create(timeline.into), run_time=t.fill(0.2))
            self.play(Create(timeline.isr_box), run_time=t.fill(0.2))
            self.play(FadeIn(timeline.isr_label), run_time=t.fill(0.14))
            t.hold()

        with self.beat("isr_deals") as t:
            self.side_note(t, "It deals with the event — reading "
                              "the data the device sent, say.",
                           fraction=0.4, x=4.6, y=-1.9, width=4.5)
            t.hold()

        with self.beat("cleared") as t:
            self.side_note(t, "Dealt with, the interrupt is cleared.",
                           fraction=0.4, x=4.6, y=-1.9, width=4.5)
            t.hold()

        with self.beat("step_restore") as t:
            self.clear(t, self.note, fraction=0.07)
            self.note = None
            self.title_swap(t, "4  Restore the saved state", fraction=0.18)
            # The side commentary has said its piece and the card is about
            # to move into the space it occupies, so it goes first.
            self.clear(t, self.side, fraction=0.08)
            self.side = None
            self.play(timeline.card.animate.move_to(
                [timeline.after.get_center()[0], -0.95, 0]),
                run_time=t.fill(0.3))
            self.play(FadeOut(timeline.card), run_time=t.fill(0.2))
            t.hold()

        with self.beat("step_resume") as t:
            self.title_swap(t, "5  Resume the program", fraction=0.14)
            self.play(Create(timeline.gap_marks[1]), run_time=t.fill(0.14))
            self.play(Create(timeline.out_of), run_time=t.fill(0.16))
            self.play(Create(timeline.after), run_time=t.fill(0.2))
            self.play(FadeIn(timeline.resumes), run_time=t.fill(0.16))
            t.hold()

        with self.beat("sequence_open") as t:
            self.wipe(t)
            self.title(t, "Remember the sequence", fraction=0.12)
            steps, rows = numbered(STEPS)
            self.place(steps, self.head, buff=GAP_LG * 0.8)
            self.steps, self.step_rows = steps, rows
            t.hold()

        for beat_name, index in zip(("seq_1", "seq_2", "seq_3", "seq_4",
                                     "seq_5"), range(5)):
            with self.beat(beat_name) as t:
                self.play(FadeIn(self.step_rows[index]),
                          run_time=t.fill(0.4))
                t.hold()

        # Both lines go in the commentary band and swap in place. Placed
        # under the five-step list they would not fit: the list already
        # reaches y=-1.78 and two stacked lines below it land on the strip.
        with self.beat("not_discarded") as t:
            self.title_swap(t, "And the program is not discarded",
                            fraction=0.2)
            self.say(t, "The original program is never discarded.",
                     fraction=0.4, color=TERRACOTTA)
            t.hold()

        with self.beat("correct_point") as t:
            self.say(t, "Its saved state lets it resume at the right point",
                     fraction=0.4, color=SAGE)
            t.hold()

    # ----------------------------------- 7. high level and low level

    def high_and_low(self):
        ladder = Ladder("High-level language", "Low-level language",
                        HIGH_NOTES, LOW_NOTES)

        with self.beat("lang_open") as t:
            self.section(t, "Programming languages", LEVELS)
            self.say(t, "A programmer writes instructions in a language",
                     fraction=0.3)
            t.hold()

        with self.beat("how_close") as t:
            self.clear(t, self.note, fraction=0.07)
            self.note = None
            self.place(ladder, self.head, buff=GAP_MD * 1.4)
            self.ladder = ladder
            self.play(Create(ladder.axis), run_time=t.fill(0.26))
            near = mono("closer to human language", MARGIN_SIZE, GREY)
            far = mono("closer to the processor", MARGIN_SIZE, GREY)
            near.next_to(ladder.ends[0], UP, buff=GAP_SM * 0.9)
            far.next_to(ladder.ends[1], DOWN, buff=GAP_SM * 0.9)
            self.poles = VGroup(near, far)
            self.play(FadeIn(near), FadeIn(far), run_time=t.fill(0.26))
            t.hold()

        with self.beat("high_level") as t:
            self.play(Create(ladder.ends[0][0]), run_time=t.fill(0.22))
            self.play(FadeIn(ladder.ends[0][1]), run_time=t.fill(0.2))
            t.hold()

        for beat_name, index in (("high_easy", 0), ("high_portable", 1),
                                 ("still_translated", 2)):
            with self.beat(beat_name) as t:
                self.play(FadeIn(ladder.notes[0][index]),
                          run_time=t.fill(0.4))
                t.hold()

        with self.beat("low_level") as t:
            self.play(Create(ladder.ends[1][0]), run_time=t.fill(0.22))
            self.play(FadeIn(ladder.ends[1][1]), run_time=t.fill(0.2))
            t.hold()

        with self.beat("low_control") as t:
            self.play(FadeIn(ladder.notes[1][0]), run_time=t.fill(0.4))
            t.hold()

        with self.beat("low_timing") as t:
            self.play(FadeIn(ladder.notes[1][1]), run_time=t.fill(0.4))
            t.hold()

        with self.beat("low_harder") as t:
            self.play(FadeIn(ladder.notes[1][2]), run_time=t.fill(0.4))
            t.hold()

        with self.beat("low_dependent") as t:
            self.play(FadeIn(ladder.notes[1][3]), run_time=t.fill(0.4))
            t.hold()

        with self.beat("choose_open") as t:
            self.wipe(t)
            self.title(t, "Tie your choice to the situation", fraction=0.12)
            t.hold()

        with self.beat("choose_high") as t:
            high = callout(["Readability,",
                            "portability, speed",
                            "→ high-level"],
                           size=LABEL_SIZE, accent=SLATE, width=6.1)
            high.move_to([-3.3, 0.1, 0])
            self.high_card = high
            self.play(Create(high[0]), run_time=t.fill(0.2))
            for line in high[1]:
                self.play(FadeIn(line), run_time=t.fill(0.16))
            t.hold()

        with self.beat("choose_low") as t:
            low = callout(["Hardware control,",
                           "precise timing",
                           "→ low-level"],
                          size=LABEL_SIZE, accent=TERRACOTTA, width=6.1)
            low.move_to([3.3, 0.1, 0])
            self.play(Create(low[0]), run_time=t.fill(0.2))
            for line in low[1]:
                self.play(FadeIn(line), run_time=t.fill(0.16))
            t.hold()

    # --------------------------- 8. machine code, assembly, the assembler

    def machine_and_assembly(self):
        assembly, binary = machine_code()

        with self.beat("machine_open") as t:
            self.section(t, "Machine code and assembly language", ASM)
            t.hold()

        with self.beat("machine_defn") as t:
            block = CodeBlock(binary, MARGIN_SIZE, CHARCOAL)
            head = serif("Machine code", LABEL_SIZE, SLATE)
            group = VGroup(head, block).arrange(DOWN, buff=GAP_MD)
            group.move_to([3.1, 0.35, 0])
            self.binary_block, self.binary_group = block, group
            self.play(FadeIn(head), run_time=t.fill(0.18))
            for line in block.lines:
                self.play(FadeIn(line), run_time=t.fill(0.16))
            self.say(t, "Binary instructions the processor runs directly",
                     fraction=0.22)
            t.hold()

        with self.beat("binary_hard") as t:
            self.say(t, "A whole program written like that is no way to "
                        "work", fraction=0.4)
            t.hold()

        with self.beat("assembly_easier") as t:
            block = CodeBlock(assembly, MARGIN_SIZE, CHARCOAL)
            head = serif("Assembly language", LABEL_SIZE, SLATE)
            group = VGroup(head, block).arrange(DOWN, buff=GAP_MD)
            group.move_to([-3.4, 0.35, 0])
            self.asm_block, self.asm_group = block, group
            self.play(FadeIn(head), run_time=t.fill(0.2))
            for line in block.lines:
                self.play(FadeIn(line), run_time=t.fill(0.18))
            t.hold()

        with self.beat("mnemonic_defn") as t:
            self.say(t, "A mnemonic is a short code for one operation",
                     fraction=0.4)
            t.hold()

        with self.beat("mnemonic_eg") as t:
            self.play(*self.asm_block.light(1), run_time=t.fill(0.22))
            self.say(t, "ADD adds; LDD loads; STO stores", fraction=0.3)
            t.hold()

        with self.beat("symbolic") as t:
            self.play(*self.asm_block.settle(), run_time=t.fill(0.14))
            self.say(t, "and an address can be a name instead of a number",
                     fraction=0.4)
            t.hold()

        with self.beat("not_raw") as t:
            note = mono("opcodes here are invented for the lesson",
                        MARGIN_SIZE, GREY)
            note.move_to([0, -2.35, 0])
            self.play(FadeIn(note), run_time=t.fill(0.3))
            t.hold()

        with self.beat("not_executed") as t:
            self.say(t, "But the processor cannot run a mnemonic",
                     fraction=0.4)
            t.hold()

        with self.beat("must_translate") as t:
            self.say(t, "It has to be translated into machine code first",
                     fraction=0.4)
            t.hold()

        with self.beat("assembler") as t:
            self.wipe(t)
            self.title(t, "An assembler does that translation",
                       fraction=0.12)
            flow = TranslatorFlow("Assembly\nlanguage", "Assembler",
                                  "Machine\ncode")
            self.place(flow, self.head, buff=GAP_LG)
            self.flow = flow
            self.play(Create(flow.source[0]), FadeIn(flow.source[1]),
                      run_time=t.fill(0.2))
            self.play(Create(flow.arrows[0]), run_time=t.fill(0.12))
            self.play(Create(flow.engine[0]), FadeIn(flow.engine[1]),
                      run_time=t.fill(0.2))
            t.hold()

        with self.beat("assembler_detail") as t:
            self.play(Create(self.flow.arrows[1]), run_time=t.fill(0.2))
            self.play(Create(self.flow.output[0]),
                      FadeIn(self.flow.output[1]), run_time=t.fill(0.3))
            t.hold()

        with self.beat("processor_specific") as t:
            self.say(t, "and the machine code it makes runs on one "
                        "kind of processor only", fraction=0.4)
            t.hold()

        with self.beat("not_portable") as t:
            warn = prose("An assembler does not turn assembly language "
                         "into a portable high-level program.",
                         LABEL_SIZE, TERRACOTTA, 11.4)
            self.place(warn, self.flow, buff=GAP_LG * 0.85)
            self.play(FadeIn(warn), run_time=t.fill(0.4))
            t.hold()

    # ------------------------------------------------- 9. the compiler

    def the_compiler(self):
        flow = TranslatorFlow("Source\ncode", "Compiler", "Executable")

        with self.beat("compiler_open") as t:
            self.section(t, "The compiler", COMPILER)
            t.hold()

        with self.beat("compiler_defn") as t:
            whole = prose("It translates the whole program before the "
                          "program runs.", BODY_SIZE, CHARCOAL, 11.6)
            self.place(whole, self.head, buff=GAP_MD * 1.3)
            self.whole = whole
            self.play(FadeIn(whole), run_time=t.fill(0.34))
            self.place(flow, whole, buff=GAP_LG * 0.8)
            self.flow2 = flow
            t.hold()

        with self.beat("writes_source") as t:
            self.play(Create(flow.source[0]), FadeIn(flow.source[1]),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("checks_translates") as t:
            self.play(Create(flow.arrows[0]), run_time=t.fill(0.16))
            self.play(Create(flow.engine[0]), FadeIn(flow.engine[1]),
                      run_time=t.fill(0.3))
            t.hold()

        with self.beat("errors_found") as t:
            self.say(t, "Errors found? Correct the source and compile "
                        "again", fraction=0.4)
            t.hold()

        with self.beat("run_without") as t:
            self.play(Create(flow.arrows[1]), run_time=t.fill(0.16))
            self.play(Create(flow.output[0]), FadeIn(flow.output[1]),
                      run_time=t.fill(0.3))
            self.say(t, "Once compiled, it runs without translating "
                        "every line again", fraction=0.3)
            t.hold()

        with self.beat("execute_quickly") as t:
            self.play(self.flow2.output[1].animate.set_color(SAGE),
                      run_time=t.fill(0.3))
            self.say(t, "which is why compiled code runs quickly",
                     fraction=0.4)
            t.hold()

        with self.beat("compiler_useful") as t:
            self.say(t, "Good for a finished program, run many times or "
                        "given to users", fraction=0.45)
            t.hold()

        with self.beat("cannot_guarantee") as t:
            self.wipe(t)
            self.title(t, "What a compiler cannot tell you", fraction=0.12)
            t.hold()

        with self.beat("syntax_errors") as t:
            found = serif("Syntax errors  —  found", LABEL_SIZE, SAGE)
            found.move_to([0, 2.0, 0])
            self.found = found
            self.play(FadeIn(found), run_time=t.fill(0.4))
            t.hold()

        with self.beat("logic_wrong") as t:
            missed = serif("A wrong algorithm  —  not found",
                           LABEL_SIZE, TERRACOTTA)
            missed.next_to(self.found, DOWN, buff=GAP_MD)
            self.play(FadeIn(missed), run_time=t.fill(0.3))
            self.missed = missed
            t.hold()

        with self.beat("wrong_formula") as t:
            block = CodeBlock(WRONG_SUM, MARGIN_SIZE, CHARCOAL)
            self.place(block, self.missed, buff=GAP_MD * 1.2)
            self.wrong = block
            for line in block.lines:
                self.play(FadeIn(line), run_time=t.fill(0.12))
            self.play(*block.light(2), run_time=t.fill(0.22))
            t.hold()

        with self.beat("wont_reveal") as t:
            self.say(t, "A minus where a plus belongs. Every rule obeyed, "
                        "the wrong answer out.", fraction=0.45)
            t.hold()

    # ---------------------------------------------- 10. the interpreter

    def the_interpreter(self):
        with self.beat("interp_open") as t:
            self.section(t, "The interpreter", INTERPRETER)
            one = prose("It translates and runs one line at a time.",
                        BODY_SIZE, CHARCOAL, 11.6)
            self.place(one, self.head, buff=GAP_MD * 1.2)
            self.one = one
            self.play(FadeIn(one), run_time=t.fill(0.3))
            block = CodeBlock(WRONG_SUM, MARGIN_SIZE, GREY, gutter=True)
            self.place(block, one, buff=GAP_LG * 0.8)
            self.running = block
            for line in block.lines:
                self.play(FadeIn(line), run_time=t.fill(0.08))
            self.play(FadeIn(block.numbers), run_time=t.fill(0.1))
            t.hold()

        with self.beat("reads_translates") as t:
            self.play(*self.running.light(0), run_time=t.fill(0.4))
            t.hold()

        with self.beat("next_statement") as t:
            self.play(*self.running.light(1), run_time=t.fill(0.4))
            t.hold()

        with self.beat("stops_at_error") as t:
            self.play(*self.running.light(2), run_time=t.fill(0.26))
            self.say(t, "and if it meets an error it stops right there "
                        "and reports it", fraction=0.4)
            t.hold()

        with self.beat("no_executable") as t:
            self.wipe(t)
            self.title(t, "Nothing comes out the other end", fraction=0.12)
            flow = TranslatorFlow("Source\ncode", "Interpreter")
            self.place(flow, self.head, buff=GAP_LG)
            self.flow3 = flow
            self.play(Create(flow.source[0]), FadeIn(flow.source[1]),
                      run_time=t.fill(0.2))
            self.play(Create(flow.arrows[0]), run_time=t.fill(0.14))
            self.play(Create(flow.engine[0]), FadeIn(flow.engine[1]),
                      run_time=t.fill(0.22))
            t.hold()

        with self.beat("as_it_runs") as t:
            none = prose("No separate translated file. Translation "
                         "happens as the program runs.", LABEL_SIZE,
                         GREY, 10.6)
            self.place(none, self.flow3, buff=GAP_LG * 0.9)
            self.none = none
            self.play(FadeIn(none), run_time=t.fill(0.4))
            t.hold()

        with self.beat("useful_dev") as t:
            self.say(t, "Which suits you while you are still writing and "
                        "testing it", fraction=0.4)
            t.hold()

        with self.beat("change_and_test") as t:
            self.say(t, "Find an error, change the code, run it again",
                     fraction=0.4)
            t.hold()

        with self.beat("tradeoff") as t:
            self.play(self.none.animate.set_color(CHARCOAL),
                      run_time=t.fill(0.3))
            self.say(t, "The trade-off: translating happens while it runs",
                     fraction=0.4)
            t.hold()

        with self.beat("slower") as t:
            slow = serif("so it runs more slowly than compiled code",
                         LABEL_SIZE, TERRACOTTA)
            slow = fit(slow, 11.4)
            self.place(slow, self.none, buff=GAP_MD * 1.2)
            self.play(FadeIn(slow), run_time=t.fill(0.4))
            t.hold()

        with self.beat("scenario_interp") as t:
            self.say(t, "Question describes interactive testing? "
                        "Interpreter.", fraction=0.4)
            t.hold()

        with self.beat("scenario_compile") as t:
            self.say(t, "Question describes a finished program, run "
                        "repeatedly? Compiler.", fraction=0.45)
            t.hold()

    # ------------------------------------------------ 11. side by side

    def side_by_side(self):
        with self.beat("compare_open") as t:
            self.section(t, "Side by side", SIDEBYSIDE)
            table, cells, heads = comparison(COMPARISON)
            self.place(table, self.head, buff=GAP_MD * 1.2)
            self.table, self.cells = table, cells
            self.play(*[FadeIn(head) for head in heads],
                      run_time=t.fill(0.24))
            self.play(Create(table.rule), run_time=t.fill(0.2))
            t.hold()

        pairs = [("cmp_when", "cmp_when_i"), ("cmp_output", "cmp_output_i"),
                 ("cmp_errors", "cmp_errors_i"), ("cmp_speed", "cmp_speed_i")]
        for index, (left_beat, right_beat) in enumerate(pairs):
            with self.beat(left_beat) as t:
                self.play(FadeIn(self.cells[index][0]),
                          run_time=t.fill(0.22))
                self.play(FadeIn(self.cells[index][1]),
                          run_time=t.fill(0.3))
                t.hold()
            with self.beat(right_beat) as t:
                self.play(FadeIn(self.cells[index][2]),
                          run_time=t.fill(0.45))
                t.hold()

        with self.beat("cmp_use_i") as t:
            self.play(FadeIn(self.cells[4][0]), run_time=t.fill(0.2))
            self.play(FadeIn(self.cells[4][2]), run_time=t.fill(0.34))
            t.hold()

        with self.beat("cmp_use_c") as t:
            self.play(FadeIn(self.cells[4][1]), run_time=t.fill(0.45))
            t.hold()

        with self.beat("exam_compare") as t:
            self.say(t, "Never describe one side and leave the other "
                        "unstated", fraction=0.4)
            t.hold()

        with self.beat("same_feature") as t:
            self.wipe(t)
            self.title(t, "Compare the same feature on both sides",
                       fraction=0.12)
            model = prose("“A compiler translates the whole program "
                          "before running it, whereas an interpreter "
                          "translates and executes one line at a time.”",
                          BODY_SIZE, CHARCOAL, 11.8)
            self.place(model, self.head, buff=GAP_LG)
            self.play(FadeIn(model), run_time=t.fill(0.5))
            t.hold()

    # -------------------------------------------------------- 12. the IDE

    def the_ide(self):
        window = IDEWindow(["x = 10", "y = 0", "PRINT x / y"])

        with self.beat("ide_open") as t:
            self.section(t, "The integrated development environment",
                         IDE, fraction=0.12)
            t.hold()

        with self.beat("ide_combines") as t:
            tools, each = chips(IDE_TOOLS[:4], size=LABEL_SIZE, rows=2)
            self.place(tools, self.head, buff=GAP_LG * 0.85)
            self.tools, self.tool_chips = tools, each
            for chip in each:
                self.play(FadeIn(chip), run_time=t.fill(0.14))
            self.say(t, "tools gathered in one place", fraction=0.2)
            t.hold()

        with self.beat("ide_editor") as t:
            self.play(self.tool_chips[0].animate.set_color(TERRACOTTA),
                      run_time=t.fill(0.2))
            self.say(t, "Write and change the source code", fraction=0.4)
            t.hold()

        with self.beat("ide_highlight") as t:
            self.say(t, "Keywords picked out, so the code is easier to "
                        "read", fraction=0.45)
            t.hold()

        with self.beat("ide_translator") as t:
            self.play(self.tool_chips[0].animate.set_color(CHARCOAL),
                      self.tool_chips[1].animate.set_color(TERRACOTTA),
                      run_time=t.fill(0.26))
            self.say(t, "A compiler or an interpreter, built in",
                     fraction=0.4)
            t.hold()

        with self.beat("ide_runtime") as t:
            self.play(self.tool_chips[1].animate.set_color(CHARCOAL),
                      self.tool_chips[2].animate.set_color(TERRACOTTA),
                      run_time=t.fill(0.26))
            self.say(t, "and somewhere to run it and watch what it does",
                     fraction=0.4)
            t.hold()

        with self.beat("ide_diagnostics") as t:
            self.wipe(t)
            self.title(t, "Error diagnostics", fraction=0.1)
            self.place(window, self.head, buff=GAP_MD * 1.1)
            self.window = window
            self.play(Create(window.frame), run_time=t.fill(0.14))
            self.play(Create(window.bar), FadeIn(window.title),
                      run_time=t.fill(0.1))
            self.play(FadeIn(window.code), run_time=t.fill(0.12))
            self.play(Create(window.strip), run_time=t.fill(0.1))
            self.play(*window.mark_line(2), run_time=t.fill(0.14))
            message = window.message("Line 3: division by zero")
            self.play(FadeIn(message), run_time=t.fill(0.2))
            t.hold()

        with self.beat("ide_helps") as t:
            self.say(t, "It says where the problem was found, so it can "
                        "be investigated", fraction=0.4)
            t.hold()

        with self.beat("ide_autocomplete") as t:
            popup = self.window.completion(["x", "y"], index=2)
            self.popup = popup
            self.play(FadeIn(popup), run_time=t.fill(0.4))
            t.hold()

        with self.beat("ide_autocorrect") as t:
            self.play(FadeOut(self.popup), run_time=t.fill(0.14))
            self.say(t, "Auto-correction fixes the common syntax slips",
                     fraction=0.4)
            t.hold()

        with self.beat("ide_pretty") as t:
            self.wipe(t)
            self.title(t, "Prettyprinting", fraction=0.1)
            ragged = CodeBlock(RAGGED, MARGIN_SIZE, CHARCOAL)
            self.place(ragged, self.head, buff=GAP_LG)
            self.ragged = ragged
            for line in ragged.lines:
                self.play(FadeIn(line), run_time=t.fill(0.1))
            tidy = CodeBlock(TIDY, MARGIN_SIZE, CHARCOAL)
            tidy.move_to(ragged)
            self.play(Transform(ragged, tidy), run_time=t.fill(0.3))
            t.hold()

        with self.beat("ide_colour") as t:
            self.say(t, "Consistent indentation, and colour to tell the "
                        "parts apart", fraction=0.45)
            t.hold()

        with self.beat("exam_ide") as t:
            self.wipe(t)
            self.title(t, "Name the feature, and what it does",
                       fraction=0.12)
            t.hold()

        with self.beat("too_general") as t:
            bad = serif("“The IDE makes programming easier.”",
                        LABEL_SIZE, GREY)
            self.place(bad, self.head, buff=GAP_LG)
            self.play(FadeIn(bad), run_time=t.fill(0.26))
            strike = Line(bad.get_left() + LEFT * GAP_SM * 0.5,
                          bad.get_right() + RIGHT * GAP_SM * 0.5,
                          color=TERRACOTTA, stroke_width=3)
            self.play(Create(strike), run_time=t.fill(0.2))
            self.say(t, "earns nothing on its own", fraction=0.26)
            t.hold()

    # -------------------------------------------- 13. one example, all of it

    def one_example(self):
        route = Chain(["Application", "Operating\nsystem", "Device\ndriver",
                       "Sensor"], width=2.9, height=1.2)

        with self.beat("together_open") as t:
            self.section(t, "One example, all of it", EXAMPLE)
            t.hold()

        with self.beat("sensor_scene") as t:
            brief = prose("A program that reads the temperature from a "
                          "sensor.", BODY_SIZE, CHARCOAL, 11.6)
            self.place(brief, self.head, buff=GAP_LG * 0.9)
            self.brief = brief
            self.play(FadeIn(brief), run_time=t.fill(0.4))
            t.hold()

        steps = [
            ("ide_provides", "While writing it: an editor, a translator "
                             "and somewhere to run it."),
            ("interp_linebyline", "With an interpreter, step through it "
                                  "one line at a time."),
            ("diag_help", "Diagnostics say where the problem was."),
            ("needs_timing", "The sensor needs precise timing and direct "
                             "control."),
            ("choose_low2", "So reach for a low-level language."),
            ("assembler2", "Assembly language? An assembler turns the "
                           "mnemonics into machine code."),
        ]
        anchor = None
        for beat_name, text in steps:
            with self.beat(beat_name) as t:
                line = prose(text, LABEL_SIZE, CHARCOAL, 11.4)
                self.place(line, anchor or self.brief,
                           buff=GAP_MD * (1.2 if anchor is None else 0.75))
                if anchor is None:
                    self.example_first = line
                self.play(FadeIn(line), run_time=t.fill(0.45))
                anchor = line
                t.hold()

        with self.beat("not_alone") as t:
            self.wipe(t)
            self.title(t, "And when it runs?", fraction=0.1)
            self.place(route, self.head, buff=GAP_LG)
            self.route2 = route
            self.play(Create(route.boxes), run_time=t.fill(0.26))
            self.play(*[FadeIn(label) for label in route.labels],
                      run_time=t.fill(0.18))
            self.say(t, "It does not drive the sensor itself",
                     fraction=0.26)
            t.hold()

        with self.beat("through_os") as t:
            self.play(*self.route2.light(0), run_time=t.fill(0.18))
            self.play(Create(self.route2.arrows[0]), run_time=t.fill(0.18))
            self.play(*self.route2.settle(0), *self.route2.light(1),
                      run_time=t.fill(0.22))
            t.hold()

        with self.beat("driver_sensor") as t:
            self.play(Create(self.route2.arrows[1]), run_time=t.fill(0.16))
            self.play(*self.route2.settle(1), *self.route2.light(2),
                      run_time=t.fill(0.18))
            self.play(Create(self.route2.arrows[2]), run_time=t.fill(0.16))
            self.play(*self.route2.settle(2), run_time=t.fill(0.12))
            t.hold()

        with self.beat("connects_all") as t:
            joined, each = chips(["Language", "Translator", "IDE",
                                  "Operating system", "Driver"],
                                 size=LABEL_SIZE, rows=2)
            self.place(joined, self.route2, buff=GAP_MD * 1.2)
            for chip in each:
                self.play(FadeIn(chip), run_time=t.fill(0.12))
            t.hold()

    # ----------------------------------------------------------- 14. recap

    def recap(self):
        with self.beat("recap_open") as t:
            self.section(t, "Recap", RECAP)
            t.hold()

        groups = [
            (["recap_sys", "recap_app"], 0),
            (["recap_os", "recap_services"], 1),
            (["recap_boot", "recap_loader", "recap_os_runs"], 2),
            (["recap_interrupt", "recap_steps", "recap_restore"], 3),
            (["recap_high", "recap_low", "recap_assembler",
              "recap_compiler", "recap_interp"], 4),
        ]

        for beats, index in groups:
            heading, lines = RECAP_CARDS[index]
            card = None
            rows = None
            for position, beat_name in enumerate(beats):
                with self.beat(beat_name) as t:
                    if position == 0:
                        self.wipe(t)
                        self.title_swap(t, heading, fraction=0.14)
                        rows = self.lines(*lines, size=BODY_SIZE)
                        self.stack(rows, self.head, buff=GAP_MD * 1.1)
                        card = rows
                    # Each beat shows its share of the card's lines, so a
                    # two-beat card of five lines still arrives in two
                    # pieces rather than all at once on the first.
                    share = len(lines) * (position + 1) // len(beats)
                    already = len(lines) * position // len(beats)
                    for line in card[already:share]:
                        self.play(FadeIn(line),
                                  run_time=t.fill(0.7 / max(1, share - already)))
                    t.hold()

        with self.beat("recap_ide") as t:
            self.wipe(t)
            self.title_swap(t, "The IDE", fraction=0.12)
            tools, each = chips(IDE_TOOLS[:4], size=LABEL_SIZE, rows=2)
            self.place(tools, self.head, buff=GAP_LG * 0.9)
            for chip in each:
                self.play(FadeIn(chip), run_time=t.fill(0.16))
            t.hold()

    def self_check(self):
        with self.beat("pause") as t:
            self.wipe(t)
            self.title(t, "Pause, and answer these yourself", fraction=0.1)
            asked, rows = numbered(QUESTIONS, size=MARGIN_SIZE)
            self.place(asked, self.head, buff=GAP_MD)
            self.asked = asked
            for row in rows:
                self.play(FadeIn(row), run_time=t.fill(0.11))
            t.hold()

        with self.beat("close") as t:
            self.wipe(t)
            line = prose("Clear definitions and precise comparisons are "
                         "the whole of this chapter.", TITLE_SIZE,
                         CHARCOAL, 11.8)
            line.move_to([0, 0.5, 0])
            self.play(Write(line), run_time=t.fill(0.5))
            self.closing = line
            t.hold()

        with self.beat("see_you") as t:
            nxt = serif("Chapter 5 next", TITLE_SIZE, SLATE)
            self.place(nxt, self.closing, buff=GAP_LG)
            self.play(FadeIn(nxt), run_time=t.fill(0.45))
            t.hold()

    # ------------------------------------------------------- scaffolding

    @contextmanager
    def beat(self, name):
        self._beat_name = name
        with super().beat(name) as timer:
            yield timer

    def section(self, t, text, index, fraction=0.14):
        """Open one of the fourteen: clear, move the strip, name it."""
        self.wipe(t)
        if self.strip not in self.mobjects:
            self.play(FadeIn(self.strip), run_time=t.fill(0.05))
            self.keep = [self.margin, self.strip]
            self.floor = FLOOR
        self.play(*self.strip.focus(index), run_time=t.fill(0.05))
        self.title(t, text, fraction=fraction)

    def side_note(self, t, text, fraction=0.25, color=CHARCOAL,
                  size=LABEL_SIZE, x=3.6, y=0.6, width=5.4):
        """A line of commentary beside a figure rather than under it."""
        line = prose(text, size, color, width)
        line.move_to([x, y, 0])
        if self.side is None or self.side not in self.mobjects:
            self.side = line
            self.play(FadeIn(line), run_time=t.fill(fraction))
        else:
            line.move_to(self.side)
            self.play(Transform(self.side, line), run_time=t.fill(fraction))
        return self.side

    def title(self, t, text, fraction=0.1, color=CHARCOAL):
        head = fit(serif(text, TITLE_SIZE, color))
        head.to_edge(UP, buff=GAP_MD * 1.7)
        self.play(Write(head), run_time=t.fill(fraction))
        self.head = head
        return head

    def title_swap(self, t, text, fraction=0.1, color=CHARCOAL):
        """Replace the heading without clearing the rest of the frame."""
        head = fit(serif(text, TITLE_SIZE, color))
        head.to_edge(UP, buff=GAP_MD * 1.7)
        if self.head is not None and self.head in self.mobjects:
            self.play(Transform(self.head, head), run_time=t.fill(fraction))
        else:
            self.play(Write(head), run_time=t.fill(fraction))
            self.head = head
        return self.head

    def lines(self, *texts, size=BODY_SIZE, color=CHARCOAL,
              buff=GAP_SM * 1.3, align=None, width=FRAME_SAFE):
        group = VGroup(*[prose(x, size, color, width) for x in texts])
        if align is None:
            group.arrange(DOWN, buff=buff)
        else:
            group.arrange(DOWN, buff=buff, aligned_edge=align)
        return group

    def stack(self, group, top=None, buff=GAP_MD, floor=None, align=ORIGIN):
        floor = self.floor if floor is None else floor
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
            f"Beat '{self._beat_name}': a stack {group.height:.2f} units "
            f"tall cannot clear y={floor} under this heading. Shorten it.")

    def place(self, mobject, top=None, buff=GAP_MD, floor=None):
        floor = self.floor if floor is None else floor
        for factor in (1.0, 0.9, 0.78, 0.66, 0.55, 0.45, 0.35):
            if top is None:
                mobject.move_to(ORIGIN)
            else:
                mobject.next_to(top, DOWN, buff=buff * factor)
                mobject.move_to([0, mobject.get_center()[1], 0])
            if mobject.get_bottom()[1] >= floor:
                return mobject
        raise ValueError(
            f"Beat '{self._beat_name}': there is no room under this content "
            f"for something {mobject.height:.2f} units tall above "
            f"y={floor}. It would land on the numbered strip.")

    def clear(self, t, *groups, fraction=0.1, with_note=False):
        family = set()
        for group in groups:
            if group is None:
                continue
            family.update(id(m) for m in group.get_family())
        present = [m for m in self.mobjects
                   if any(id(child) in family for child in m.get_family())]
        if with_note and self.note is not None and self.note in self.mobjects:
            present.append(self.note)
        if present:
            self.play(*[FadeOut(m) for m in present],
                      run_time=t.fill(fraction))
        if with_note:
            self.note = None

    def wipe(self, t, fraction=0.05):
        old = [m for m in self.mobjects if m not in self.keep]
        if old:
            self.play(*[FadeOut(m) for m in old], run_time=t.fill(fraction))
        self.head = self.note = self.side = None

    def say(self, t, text, fraction=0.2, color=GREY, size=LABEL_SIZE,
            y=None, anchor=None, buff=GAP_MD):
        """The running line of commentary, swapped in place."""
        line = prose(text, size, color, 12.0)
        if anchor is not None:
            self.place(line, anchor, buff=buff)
        else:
            line.move_to([0, self.floor + 0.35 if y is None else y, 0])
            self.band_is_clear(line)
        if self.note is None or self.note not in self.mobjects:
            self.note = line
            self.play(FadeIn(line), run_time=t.fill(fraction))
        else:
            line.move_to(self.note)
            self.play(Transform(self.note, line), run_time=t.fill(fraction))
        return self.note

    def band_is_clear(self, line, tol=0.05):
        """Refuse to print commentary through whatever is already there.

        The acceptance check compares writing against writing, so a
        caption laid across a diagram reads as clean: a box is a shape,
        not text. The band at the bottom of the frame is reserved for one
        line of commentary, and this is what reserves it.
        """
        for mobject in self.mobjects:
            if mobject in self.keep or mobject is self.note:
                continue
            wide = (min(line.get_right()[0], mobject.get_right()[0])
                    - max(line.get_left()[0], mobject.get_left()[0]))
            high = (min(line.get_top()[1], mobject.get_top()[1])
                    - max(line.get_bottom()[1], mobject.get_bottom()[1]))
            if wide > tol and high > tol:
                # Name the obstruction. "runs through something already on
                # screen" sends you measuring every figure in the section
                # by hand; the label and the overlap say which one it is
                # and by how much.
                what = getattr(mobject, "text", None) or type(mobject).__name__
                raise ValueError(
                    f"Beat '{self._beat_name}': the commentary band at "
                    f"y={line.get_center()[1]:.2f} "
                    f"(y {line.get_bottom()[1]:.2f} to "
                    f"{line.get_top()[1]:.2f}) runs through {what!r} "
                    f"(y {mobject.get_bottom()[1]:.2f} to "
                    f"{mobject.get_top()[1]:.2f}), overlapping "
                    f"{wide:.2f} x {high:.2f} units. Move the figure or "
                    f"drop the line."
                )


# ----------------------------------------------------- local furniture

def numbered(items, size=LABEL_SIZE, color=CHARCOAL, number_color=GREY,
             gap=GAP_SM * 1.4, width=FRAME_SAFE):
    """A numbered list with a hanging indent, like ``FunctionList``.

    Returns the group and the rows, so a scene can bring them in one at
    a time. Each row is placed from one origin rather than next to the
    row above, because a row whose text has no descender sits higher
    than one that does and a column built with ``next_to`` walks.
    """
    rows, numbers, labels = VGroup(), [], []
    for index, text in enumerate(items):
        number = serif(f"{index + 1}", size, number_color)
        label = prose(text, size, color, width - 1.0)
        numbers.append(number)
        labels.append(label)

    widest = max(number.width for number in numbers)
    pitch = max(label.height for label in labels) + gap
    for index, (number, label) in enumerate(zip(numbers, labels)):
        y = -index * pitch
        number.move_to([-width / 2 + widest, y, 0], aligned_edge=RIGHT)
        label.move_to([-width / 2 + widest + GAP_SM * 1.4, y, 0],
                      aligned_edge=LEFT)
        # A wrapped label is taller than one line, so its centre is not
        # its first line. Lift it so the first line sits on the number.
        if label.height > pitch - gap + 0.01:
            label.shift(UP * (label.height - (pitch - gap)) / 2)
        row = VGroup(number, label)
        rows.add(row)
    group = VGroup(rows)
    group.move_to(ORIGIN)
    if group.width > width:
        raise ValueError(
            f"A numbered list is {group.width:.2f} units wide, over the "
            f"{width:.2f} the frame allows.")
    return group, rows


def comparison(entries, size=MARGIN_SIZE, row_gap=GAP_SM * 1.7,
               col_gap=GAP_MD * 0.8, width=FRAME_SAFE):
    """Feature, compiler, interpreter: three columns on one left edge.

    ``make_table`` in components.table right-aligns its cells, which is
    right for numbers and wrong for prose, so the columns here are laid
    out on their left edges instead.

    The column positions are measured rather than chosen. Hardcoded x
    values were wrong twice over: the serif face is wider per character
    than it looks, so a table that was supposed to fit in 12.6 units
    came out at 12.97, and the fix by eye then put two columns 4
    hundredths apart. Taking each column's width from its own widest
    cell makes both faults impossible to reintroduce.
    """
    heads = ("Feature", "Compiler", "Interpreter")
    # Build every cell first, then let the widest in each column set the
    # column's x.
    table = [list(heads)] + [list(row) for row in entries]
    made = [[serif(text, size, GREY if i == 0 or j == 0 else CHARCOAL)
             for j, text in enumerate(row)]
            for i, row in enumerate(table)]
    spans = [max(row[j].width for row in made) for j in range(3)]

    total = sum(spans) + col_gap * 2
    if total > width:
        raise ValueError(
            f"The comparison needs {total:.2f} units and the frame allows "
            f"{width:.2f}. Shorten the longest cell in the widest column: "
            + ", ".join(f"{span:.2f}" for span in spans))

    left = -total / 2
    xs = []
    for span in spans:
        xs.append(left)
        left += span + col_gap

    pitch = made[0][0].height + row_gap
    group, cells = VGroup(), []
    for i, row in enumerate(made):
        y = 0.0 if i == 0 else -(i * pitch + row_gap)
        for j, cell in enumerate(row):
            cell.move_to([xs[j], y, 0], aligned_edge=LEFT)
            group.add(cell)
        if i:
            cells.append(row)

    rule = Line([xs[0] - GAP_SM, -pitch / 2 - row_gap / 2, 0],
                [xs[2] + spans[2] + GAP_SM, -pitch / 2 - row_gap / 2, 0],
                color=GREY, stroke_width=1.5)
    group.add(rule)
    group.rule = rule
    group.move_to(ORIGIN)
    return group, cells, made[0]
