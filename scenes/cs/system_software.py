"""System software, application software, and what an operating system does.

Cambridge O Level Computer Science 2210, topic 4.1, syllabus for
examination in 2026, 2027 and 2028. The lecture is two halves: a sorting
rule, and then the nine jobs the syllabus names.

Checked against the syllabus before building, and every claim on screen
matches its wording:

  * "System software provides the services that the computer requires,
    including operating system and utility software"; "Application
    software provides the services that the user requires".
  * the nine functions, in the syllabus's own order: managing files,
    handling interrupts, providing an interface, managing peripherals and
    drivers, managing memory, managing multitasking, providing a platform
    for running applications, providing system security, managing user
    accounts.

The lecture covers those nine in a different order from the syllabus, so
the numbered strip along the bottom jumps about rather than running one to
nine. That is deliberate: the numbers are the syllabus's, and the strip is
there so a student watching section six can see which of the nine it is.

One thing the syllabus asks for that this script does not cover: bullet
three of 4.1, "Understand how hardware, firmware and an operating system
are required to run applications software" — applications run on the
operating system, the operating system runs on the firmware, and the
bootloader (firmware) runs on the hardware. Nothing on screen claims
otherwise; the layer stack here is the peripheral path the narration
describes (application, operating system, driver, device), which is a
different stack from the firmware one. It wants its own section.

Virtual memory is not in the 2026-2028 notes for 2210 either. It is not
wrong, and the narration teaches it well, so it stays — but it is
enrichment, not a thing the mark scheme will be looking for at this level.

Where the read-aloud slips, the screen carries the correct form. The
narration is an ElevenLabs read, so these are the voice's, not a
presenter's: "organizers" for organizes, "and force passwords" for enforce
passwords, "this cleanup software" for disk-cleanup software. None of them
reach the screen.

Timing: timings/cs.system_software.json
Render: python build/render.py scripts/OS01-system-software.md \\
    audio/OS01-system-software.m4a
"""

import textwrap
from contextlib import contextmanager

from manim import (
    Create,
    FadeIn,
    FadeOut,
    Line,
    Rectangle,
    SurroundingRectangle,
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
    CREAM,
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
from components.os_shape import (
    FunctionList,
    LayerStack,
    MemoryBar,
    SortBench,
    TimeSlices,
    chips,
    grid,
    screen,
)
from components.syllabus_map import TopicStrip
from scenes.base import SATScene

FRAME_SAFE = 12.6
FLOOR = -3.05        # the numbered strip owns everything below this
BARE_FLOOR = -3.45   # before the strip exists, in part one

# Which of the nine syllabus functions each section is. The lecture's order
# is not the syllabus's, so these are not consecutive.
FILES, INTERRUPTS, INTERFACE, PERIPHERALS = 0, 1, 2, 3
MEMORY, MULTITASKING, PLATFORM, SECURITY, ACCOUNTS = 4, 5, 6, 7, 8

SYSTEM_EXAMPLES = ["Operating systems", "Utility software", "Device drivers"]
APP_EXAMPLES = ["Word processors", "Web browsers", "Database software",
                "Games", "Presentation software", "Video editing software"]

FILE_VERBS = ["creates", "names", "stores", "retrieves", "organizes",
              "protects"]
FILE_ALSO = ["file names", "file types", "file permissions",
             "folder structures", "access rights"]
WIMP = ["windows", "icons", "menus", "buttons", "pointers"]
PERIPHERALS_EG = ["printers", "keyboards", "mice", "scanners", "speakers",
                  "storage devices"]
SECURITY_JOBS = ["authenticate users", "enforce passwords",
                 "control access permissions", "restrict access to files",
                 "protect system resources", "maintain separate user accounts"]
ACCOUNT_FIELDS = ["username", "password", "permissions", "files", "settings",
                  "preferences"]
PLATFORM_JOBS = ["displaying information", "reading keyboard input",
                 "saving files", "using memory", "accessing the network",
                 "printing documents"]
PROCESSES = ["music", "download", "document", "notifications"]
SLICE_ORDER = [0, 1, 2, 3, 0, 1, 2, 3]


def fit(mobject, width=FRAME_SAFE):
    if mobject.width > width:
        mobject.scale_to_fit_width(width)
    return mobject


def prose(text, size=BODY_SIZE, color=CHARCOAL, width=FRAME_SAFE):
    """A sentence that wraps to fit rather than shrinking to fit.

    Shrink-to-fit is how a 32px caption quietly becomes a 26px one: the
    layout still looks balanced, so nothing catches it but the acceptance
    check.
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


def strike(mobject, color=TERRACOTTA, stroke=3.5):
    """A line through a claim that does not hold."""
    return Line(mobject.get_left() + LEFT * 0.1,
                mobject.get_right() + RIGHT * 0.1,
                color=color, stroke_width=stroke)


def boxed(mobject, color=SLATE, pad=GAP_SM * 1.3):
    return SurroundingRectangle(mobject, color=color, stroke_width=2.5,
                                buff=pad, corner_radius=0.0)


class SystemSoftware(SATScene):
    scene_id = "cs.system_software"

    def construct(self):
        self.margin = mono("O Level 2210 · 4.1 Software", MARGIN_SIZE)
        self.margin.to_corner(UP + LEFT, buff=GAP_SM)
        self.add(self.margin)

        # The strip is furniture, not emphasis, so it is lit in slate and
        # terracotta stays free for the one thing being pointed at.
        self.strip = TopicStrip(9, lit=SLATE, side=0.52)
        self.strip.to_edge(DOWN, buff=GAP_SM * 0.5)

        self.keep = [self.margin]
        self.floor = BARE_FLOOR
        self.head = None
        self.note = None

        self.opening()
        self.what_software_is()
        self.the_two_bins()
        self.the_rule()
        self.the_antivirus_test()
        self.the_common_mistake()
        self.quick_check()

        self.part_two()
        self.the_nine_functions()
        self.managing_files()
        self.providing_an_interface()
        self.peripherals_and_drivers()
        self.managing_memory()
        self.multitasking()
        self.system_security()
        self.user_accounts()
        self.the_platform()
        self.handling_interrupts()

    # ---------------------------------------------------------------- part one

    def opening(self):
        with self.beat("open") as t:
            title = serif("Software", DISPLAY_SIZE, CHARCOAL)
            under = serif("system software and application software",
                          LABEL_SIZE, SLATE)
            board = serif("Cambridge O Level · Topic 4.1", MARGIN_SIZE, GREY)
            card = VGroup(title, under, board).arrange(DOWN, buff=GAP_MD)
            card.move_to(ORIGIN)
            self.play(Write(title), run_time=t.fill(0.3))
            self.play(FadeIn(under), run_time=t.fill(0.18))
            self.play(FadeIn(board), run_time=t.fill(0.14))
            t.hold()

    def what_software_is(self):
        with self.beat("software_is") as t:
            self.wipe(t)
            word = serif("Software", TITLE_SIZE, SLATE)
            body = self.lines(
                "a collection of programs and instructions",
                "that tell a computer what to do",
            )
            card = VGroup(word, body).arrange(DOWN, buff=GAP_MD * 1.3)
            card.move_to(ORIGIN)
            self.play(Write(word), run_time=t.fill(0.2))
            self.play(FadeIn(body), run_time=t.fill(0.3))
            t.hold()

    def the_two_bins(self):
        with self.beat("distinguish") as t:
            self.wipe(t)
            self.title(t, "Two kinds of software", fraction=0.3)
            t.hold()

        # Built complete before anything is shown. Each item is positioned
        # relative to whatever is already in its column, so adding them as
        # the narration arrives would fix the first one's place before the
        # bench knew how tall it was going to be.
        bench = SortBench("System software", "Application software",
                          size=MARGIN_SIZE)
        bench.caption(0, "provides the services that the computer requires")
        bench.caption(1, "provides the services that the user requires")
        for text in SYSTEM_EXAMPLES:
            bench.item(0, text)
        for text in APP_EXAMPLES:
            bench.item(1, text)
        bench.next_to(self.head, DOWN, buff=GAP_MD * 1.1)
        self.bench = bench
        self.guard_floor(bench, "the sorting bench")

        with self.beat("bins") as t:
            self.play(Write(bench.heads), run_time=t.fill(0.35))
            self.play(Create(bench.rules), run_time=t.fill(0.22))
            t.hold()

        with self.beat("sys_def") as t:
            self.play(FadeIn(bench.captions[0]), run_time=t.fill(0.3))
            t.hold()

        for name, item in zip(("sys_eg1", "sys_eg2", "sys_eg3"),
                              bench.items[0]):
            with self.beat(name) as t:
                self.play(FadeIn(item), run_time=t.fill(0.35))
                t.hold()

        with self.beat("app_def") as t:
            self.play(FadeIn(bench.captions[1]), run_time=t.fill(0.3))
            t.hold()

        for index, item in enumerate(bench.items[1]):
            with self.beat(f"app_eg{index + 1}") as t:
                self.play(FadeIn(item), run_time=t.fill(0.4))
                t.hold()

    def the_rule(self):
        """The one sentence a student should leave this half holding."""
        with self.beat("simplest") as t:
            self.wipe(t)
            self.title(t, "The simplest way to remember", fraction=0.28)
            t.hold()

        span = 5.6
        self.rule_cards = VGroup()
        bodies = []
        for index, (name, lines) in enumerate((
                ("System software", ("helps the", "computer operate")),
                ("Application software", ("helps the user", "complete a task")))):
            head = serif(name, LABEL_SIZE, SLATE)
            body = VGroup(*[serif(line, BODY_SIZE, CHARCOAL)
                            for line in lines])
            body.arrange(DOWN, buff=GAP_SM * 0.9)
            column = VGroup(head, body).arrange(DOWN, buff=GAP_MD * 1.2)
            column.move_to([(index - 0.5) * (span + GAP_LG), 0, 0])
            for piece in (head, body):
                if piece.width > span:
                    raise ValueError(
                        f"{name!r}'s card is {piece.width:.2f} units wide in "
                        f"a column only {span:.2f} wide.")
            self.rule_cards.add(column)
            bodies.append(body)

        divider = Line(UP * 0.95, DOWN * 0.95, color=GREY, stroke_width=2)
        self.rule_cards.add(divider)
        self.rule_cards.next_to(self.head, DOWN, buff=GAP_MD * 1.4)
        divider.move_to([0, self.rule_cards.get_center()[1], 0])

        with self.beat("rule_sys") as t:
            self.play(Write(self.rule_cards[0][0]), run_time=t.fill(0.22))
            self.play(Create(divider), run_time=t.fill(0.12))
            self.play(FadeIn(bodies[0]), run_time=t.fill(0.26))
            t.hold()

        with self.beat("rule_app") as t:
            self.play(Write(self.rule_cards[1][0]), run_time=t.fill(0.22))
            self.play(FadeIn(bodies[1]), run_time=t.fill(0.3))
            t.hold()

    def the_antivirus_test(self):
        """The case that breaks the lazy rule: a visible interface, and
        still system software."""
        chip = serif("Antivirus software", LABEL_SIZE, CHARCOAL)
        box = boxed(chip)
        token = VGroup(box, chip)
        token.move_to([0, self.rule_cards.get_bottom()[1] - GAP_LG * 0.9, 0])

        with self.beat("antivirus") as t:
            self.play(FadeIn(token), run_time=t.fill(0.35))
            t.hold()

        with self.beat("can_open") as t:
            self.say(t, "you can open it and click around in it",
                     anchor=token, buff=GAP_MD * 0.8, fraction=0.4)
            t.hold()

        with self.beat("still_system") as t:
            target = [self.rule_cards[0].get_center()[0],
                      token.get_center()[1], 0]
            self.play(token.animate.move_to(target), run_time=t.fill(0.35))
            self.play(box.animate.set_stroke(SAGE),
                      chip.animate.set_color(SAGE), run_time=t.fill(0.2))
            t.hold()

        with self.beat("its_role") as t:
            self.say(t, "its job is to maintain and protect the computer",
                     fraction=0.4)
            t.hold()

    def the_common_mistake(self):
        with self.beat("mistake") as t:
            self.wipe(t)
            self.title(t, "A common mistake", fraction=0.12)
            claim = prose("Every program the user can open is application "
                          "software.", BODY_SIZE, CHARCOAL, 11.0)
            self.place(claim, self.head, buff=GAP_LG)
            self.claim = claim
            self.play(Write(claim), run_time=t.fill(0.4))
            t.hold()

        with self.beat("incorrect") as t:
            self.play(Create(strike(self.claim)), run_time=t.fill(0.3))
            t.hold()

        with self.beat("by_purpose") as t:
            right = serif("Classify by purpose.", TITLE_SIZE, SAGE)
            self.place(right, self.claim, buff=GAP_LG * 0.9)
            self.right_rule = right
            self.play(Write(right), run_time=t.fill(0.55))
            t.hold()

        with self.beat("not_open") as t:
            self.say(t, "Not by whether the user can open it.",
                     anchor=self.right_rule, buff=GAP_MD, fraction=0.35)
            t.hold()

    def quick_check(self):
        with self.beat("quick_check") as t:
            self.wipe(t)
            self.title(t, "Quick check", fraction=0.45, color=SLATE)
            t.hold()

        with self.beat("qc_item") as t:
            item = prose("A student uses spreadsheet software to calculate "
                         "monthly expenses.", BODY_SIZE, CHARCOAL, 11.4)
            self.place(item, self.head, buff=GAP_MD * 1.6)
            self.item = item
            self.play(Write(item), run_time=t.fill(0.45))
            t.hold()

        with self.beat("qc_ask") as t:
            ask = serif("System, or application?", LABEL_SIZE, TERRACOTTA)
            self.place(ask, self.item, buff=GAP_MD * 1.2)
            self.ask = ask
            self.play(FadeIn(ask), run_time=t.fill(0.3))
            t.hold()

        with self.beat("qc_answer") as t:
            answer = serif("Application software", TITLE_SIZE, SAGE)
            self.place(answer, self.ask, buff=GAP_MD)
            self.play(Write(answer), run_time=t.fill(0.3))
            self.answer = answer
            self.say(t, "it helps the user finish a task", fraction=0.25)
            t.hold()

        with self.beat("qc2") as t:
            going = [self.item, self.ask, answer]
            if self.note is not None:
                going.append(self.note)
                self.note = None
            self.play(*[FadeOut(m) for m in going], run_time=t.fill(0.14))
            item = prose("Disk-cleanup software.", BODY_SIZE, CHARCOAL, 11.4)
            self.place(item, self.head, buff=GAP_MD * 1.6)
            self.item = item
            self.play(Write(item), run_time=t.fill(0.4))
            t.hold()

        with self.beat("qc2_what") as t:
            self.say(t, "it removes unnecessary files and tidies up", fraction=0.4)
            t.hold()

        with self.beat("qc2_answer") as t:
            chain = VGroup(
                serif("utility software", LABEL_SIZE, CHARCOAL),
                serif("→", LABEL_SIZE, GREY),
                serif("system software", TITLE_SIZE, SAGE),
            ).arrange(RIGHT, buff=GAP_MD)
            self.place(chain, self.item, buff=GAP_LG * 0.8)
            self.play(FadeIn(chain[0]), run_time=t.fill(0.2))
            self.play(FadeIn(chain[1]), Write(chain[2]), run_time=t.fill(0.3))
            t.hold()

    # ---------------------------------------------------------------- part two

    def part_two(self):
        with self.beat("part2") as t:
            self.wipe(t)
            label = serif("Part 2", LABEL_SIZE, GREY)
            title = serif("The operating system", DISPLAY_SIZE, CHARCOAL)
            card = VGroup(label, title).arrange(DOWN, buff=GAP_MD)
            card.move_to(ORIGIN)
            self.play(FadeIn(label), run_time=t.fill(0.14))
            self.play(Write(title), run_time=t.fill(0.4))
            self.card = card
            t.hold()

        with self.beat("most_important") as t:
            self.say(t, "the most important piece of system software",
                     anchor=self.card, buff=GAP_MD * 1.2, fraction=0.35)
            t.hold()

        stack = LayerStack(["Application software", "Operating system",
                            "Hardware"], width=6.8)
        stack.move_to(ORIGIN)
        self.os_stack = stack

        with self.beat("manages") as t:
            self.wipe(t)
            self.play(Create(stack.boxes[1]), Write(stack.labels[1]),
                      run_time=t.fill(0.24))
            self.play(Create(stack.boxes[2]), Write(stack.labels[2]),
                      Create(stack.arrows[1]), run_time=t.fill(0.24))
            self.say(t, "it manages the hardware and the software on it",
                     fraction=0.17)
            t.hold()

        with self.beat("platform_intro") as t:
            self.play(Create(stack.boxes[0]), Write(stack.labels[0]),
                      Create(stack.arrows[0]), run_time=t.fill(0.3))
            self.say(t, "and gives applications a platform to run on",
                     fraction=0.28)
            t.hold()

        with self.beat("examples") as t:
            self.clear(t, stack, with_note=True)
            names, each = chips(["Windows", "macOS", "Linux", "Android",
                                 "iOS"], size=LABEL_SIZE, color=GREY, rows=1)
            names.move_to(ORIGIN)
            self.names = names
            for chip in each:
                self.play(FadeIn(chip), run_time=t.fill(0.11))
            t.hold()

        with self.beat("no_memorise") as t:
            self.say(t, "you are not asked to memorise product names",
                     anchor=self.names, buff=GAP_LG * 0.8, fraction=0.4)
            t.hold()

        with self.beat("understand") as t:
            answer = serif("You are asked what it does.", TITLE_SIZE, SAGE)
            answer.move_to([0, self.names.get_top()[1] + GAP_LG * 0.9, 0])
            self.play(Write(answer), run_time=t.fill(0.5))
            t.hold()

    def the_nine_functions(self):
        with self.beat("functions") as t:
            self.wipe(t)
            head = fit(serif("Functions of an operating system", TITLE_SIZE,
                             CHARCOAL))
            head.to_edge(UP, buff=GAP_MD * 1.6)
            self.head = head
            self.play(Write(head), run_time=t.fill(0.22))

            self.functions = FunctionList()
            self.functions.move_to([0, -0.35, 0])
            self.play(FadeIn(self.functions), run_time=t.fill(0.35))
            self.play(FadeIn(self.strip), run_time=t.fill(0.1))

            # From here on the strip owns the bottom of the frame.
            self.keep = [self.margin, self.strip]
            self.floor = FLOOR
            t.hold()

    # ------------------------------------------------- 1. managing files

    def managing_files(self):
        with self.beat("files") as t:
            self.section(t, "Managing files", FILES)
            t.hold()

        with self.beat("files_verbs") as t:
            verbs, each = chips(FILE_VERBS, size=LABEL_SIZE, rows=2)
            self.place(verbs, self.head, buff=GAP_LG * 0.9)
            self.verbs = verbs
            for chip in each:
                self.play(FadeIn(chip), run_time=t.fill(0.1))
            t.hold()

        with self.beat("files_folders") as t:
            self.say(t, "and the folders, and where the data actually sits", fraction=0.4)
            t.hold()

        stack = LayerStack(["Application software", "Operating system",
                            "Storage device"], width=6.8, height=0.76,
                           gap=0.52)

        with self.beat("files_save") as t:
            self.clear(t, self.verbs, with_note=True)
            self.place(stack, self.head, buff=GAP_MD * 1.2)
            self.save_stack = stack
            self.play(Create(stack.boxes), Write(stack.labels),
                      run_time=t.fill(0.3))
            self.play(Create(stack.arrows), run_time=t.fill(0.14))
            self.say(t, "the application does not choose where it goes", fraction=0.26)
            t.hold()

        with self.beat("files_asks") as t:
            self.play(*stack.light(1), run_time=t.fill(0.25))
            self.say(t, "it asks the operating system to handle it",
                     fraction=0.3)
            t.hold()

        with self.beat("files_also") as t:
            self.clear(t, stack, with_note=True)
            also, each = chips(FILE_ALSO, size=LABEL_SIZE, rows=2)
            self.place(also, self.head, buff=GAP_LG)
            for chip in each:
                self.play(FadeIn(chip), run_time=t.fill(0.11))
            self.also = also
            t.hold()

        with self.beat("files_weak") as t:
            self.wipe(t)
            self.title(t, "In the exam", fraction=0.1, color=SLATE)
            weak = serif("“It manages files.”", BODY_SIZE, CHARCOAL)
            self.place(weak, self.head, buff=GAP_LG * 0.9)
            self.weak = weak
            self.play(Write(weak), run_time=t.fill(0.3))
            self.play(Create(strike(weak)), run_time=t.fill(0.2))
            t.hold()

        with self.beat("files_stronger") as t:
            self.say(t, "say what managing files actually means",
                     anchor=self.weak, buff=GAP_MD, fraction=0.45)
            t.hold()

        with self.beat("files_strong") as t:
            strong = prose("It creates, names, organizes, stores, retrieves "
                           "and protects files.", BODY_SIZE, SAGE, 11.6)
            self.place(strong, self.note, buff=GAP_MD * 1.4)
            self.play(Write(strong), run_time=t.fill(0.5))
            t.hold()

    # ------------------------------------------- 3. providing an interface

    def providing_an_interface(self):
        """The two ways of telling a computer what to do, side by side.

        Laid out whole before anything is drawn. Built piece by piece, the
        screens took the height they wanted and the terms underneath them
        ended up in the commentary band.
        """
        gui, cli = screen("gui", width=5.0, height=2.4), screen(
            "cli", width=5.0, height=2.4)
        left = VGroup(serif("Graphical user interface", MARGIN_SIZE, SLATE),
                      gui).arrange(DOWN, buff=GAP_SM)
        right = VGroup(serif("Command line interface", MARGIN_SIZE, SLATE),
                       cli).arrange(DOWN, buff=GAP_SM)
        wimp, terms = chips(WIMP, size=MARGIN_SIZE, rows=2, width=5.0,
                            gap=GAP_SM * 1.4)
        typed = serif("you type the commands", MARGIN_SIZE, GREY)

        for column, under, x in ((left, wimp, -2.75), (right, typed, 2.75)):
            column.move_to([x, 0, 0])
            under.next_to(column, DOWN, buff=GAP_SM * 1.2)
            under.move_to([x, under.get_center()[1], 0])

        panel = VGroup(left, right, wimp, typed)

        with self.beat("ui") as t:
            self.section(t, "Providing an interface", INTERFACE)
            self.place(panel, self.head, buff=GAP_MD * 0.9,
                       floor=self.floor + 0.75)
            self.play(FadeIn(left[0]), run_time=t.fill(0.07))
            self.play(Create(gui), run_time=t.fill(0.3))
            self.say(t, "the way you and the computer talk to each other",
                     fraction=0.2)
            t.hold()

        with self.beat("gui") as t:
            for term in terms:
                self.play(FadeIn(term), run_time=t.fill(0.12))
            t.hold()

        with self.beat("cli") as t:
            self.play(FadeIn(right[0]), run_time=t.fill(0.08))
            self.play(Create(cli), run_time=t.fill(0.35))
            self.play(FadeIn(typed), run_time=t.fill(0.14))
            t.hold()

        with self.beat("ui_converts") as t:
            self.say(t, "it turns your actions into instructions",
                     fraction=0.35)
            t.hold()

    # --------------------------------- 4. managing peripherals and drivers

    def peripherals_and_drivers(self):
        with self.beat("periph") as t:
            self.section(t, "Managing peripherals and drivers", PERIPHERALS)
            t.hold()

        with self.beat("periph_def") as t:
            self.say(t, "a peripheral is a hardware device connected to, or "
                        "used with, a computer", anchor=self.head,
                     buff=GAP_MD * 1.3, size=BODY_SIZE, color=CHARCOAL,
                     fraction=0.4)
            t.hold()

        with self.beat("periph_eg") as t:
            devices, each = chips(PERIPHERALS_EG, size=LABEL_SIZE, rows=2)
            self.place(devices, self.note, buff=GAP_LG * 0.8)
            self.devices = devices
            for chip in each:
                self.play(FadeIn(chip), run_time=t.fill(0.11))
            t.hold()

        with self.beat("driver_def") as t:
            self.wipe(t)
            self.title(t, "Drivers, and the path to hardware",
                       fraction=0.1)
            body = prose("A device driver lets the operating system talk "
                         "to one particular piece of hardware.", BODY_SIZE,
                         CHARCOAL, 11.6)
            self.place(body, self.head, buff=GAP_MD * 1.4)
            self.driver_line = body
            self.play(Write(body), run_time=t.fill(0.42))
            t.hold()

        with self.beat("diff_printers") as t:
            pairs = VGroup()
            for name in ("Printer A", "Printer B"):
                device = serif(name, LABEL_SIZE, CHARCOAL)
                driver = serif("its own driver", MARGIN_SIZE, GREY)
                column = VGroup(device, driver).arrange(DOWN, buff=GAP_SM)
                pairs.add(VGroup(boxed(column, color=SLATE), column))
            pairs.arrange(RIGHT, buff=GAP_LG * 1.4)
            self.place(pairs, self.driver_line, buff=GAP_MD * 1.3)
            self.play(FadeIn(pairs), run_time=t.fill(0.3))
            self.say(t, "different commands inside, so different drivers",
                     fraction=0.25)
            t.hold()

        stack = LayerStack(["Application software", "Operating system",
                            "Device driver", "Hardware device"], width=6.8,
                           height=0.74, gap=0.52)
        stack.move_to([0, -0.15, 0])
        self.path_stack = stack

        with self.beat("not_direct") as t:
            self.wipe(t, keep_head=True)
            self.play(Create(stack.boxes[0]), Write(stack.labels[0]),
                      run_time=t.fill(0.2))
            self.play(Create(stack.boxes[3]), Write(stack.labels[3]),
                      run_time=t.fill(0.2))
            direct = Line(stack.boxes[0].get_left() + LEFT * 0.3,
                          stack.boxes[3].get_left() + LEFT * 0.3,
                          color=GREY, stroke_width=3)
            cross = VGroup(
                Line(LEFT * 0.22 + UP * 0.22, RIGHT * 0.22 + DOWN * 0.22,
                     color=TERRACOTTA, stroke_width=4),
                Line(LEFT * 0.22 + DOWN * 0.22, RIGHT * 0.22 + UP * 0.22,
                     color=TERRACOTTA, stroke_width=4),
            )
            cross.move_to(direct.get_center())
            self.play(Create(direct), run_time=t.fill(0.16))
            self.play(Create(cross), run_time=t.fill(0.16))
            self.direct = VGroup(direct, cross)
            t.hold()

        with self.beat("path") as t:
            self.play(FadeOut(self.direct), run_time=t.fill(0.12))
            self.play(*stack.light(0), run_time=t.fill(0.3))
            t.hold()

        for name, index in (("path_os", 1), ("path_driver", 2)):
            with self.beat(name) as t:
                self.play(Create(stack.arrows[index - 1]),
                          run_time=t.fill(0.2))
                self.play(Create(stack.boxes[index]),
                          Write(stack.labels[index]), run_time=t.fill(0.4))
                t.hold()

        with self.beat("path_hw") as t:
            self.play(Create(stack.arrows[2]), run_time=t.fill(0.25))
            self.play(*stack.light(3), run_time=t.fill(0.3))
            t.hold()

        with self.beat("separation") as t:
            self.play(*stack.settle(0), *stack.settle(3),
                      run_time=t.fill(0.08))
            self.say(t, "no instructions for every printer ever made", fraction=0.25)
            t.hold()

    # ---------------------------------------------------- 5. managing memory

    def managing_memory(self):
        ram = MemoryBar(width=8.6)
        self.ram = ram

        with self.beat("memory") as t:
            self.section(t, "Managing memory", MEMORY)
            self.place(ram, self.head, buff=GAP_LG * 1.1)
            self.play(Create(ram.frame), FadeIn(ram.name),
                      run_time=t.fill(0.3))
            self.say(t, "the memory that running programs share", fraction=0.22)
            t.hold()

        blocks = {}
        for name, (process, share) in zip(
                ("mem_decides", "mem_how_much", "mem_where"),
                (("text editor", 0.3), ("browser", 0.36),
                 ("music player", 0.34))):
            with self.beat(name) as t:
                block = ram.allocate(process, share)
                blocks[process] = block
                self.play(FadeIn(block), run_time=t.fill(0.45))
                t.hold()

        with self.beat("mem_release") as t:
            freed = blocks["browser"]
            self.play(freed[0].animate.set_stroke(GREY)
                      .set_fill(GREY, opacity=0.14),
                      run_time=t.fill(0.25))
            label = serif("free", MARGIN_SIZE, GREY)
            label.move_to(freed[1])
            self.play(Transform(freed[1], label), run_time=t.fill(0.2))
            self.say(t, "when a program is done with it, it goes back", fraction=0.25)
            t.hold()

        with self.beat("mem_protect") as t:
            reach = Line(blocks["text editor"][0].get_top() + UP * 0.12,
                         blocks["music player"][0].get_top() + UP * 0.12,
                         color=GREY, stroke_width=3)
            cross = VGroup(
                Line(LEFT * 0.2 + UP * 0.2, RIGHT * 0.2 + DOWN * 0.2,
                     color=TERRACOTTA, stroke_width=4),
                Line(LEFT * 0.2 + DOWN * 0.2, RIGHT * 0.2 + UP * 0.2,
                     color=TERRACOTTA, stroke_width=4),
            ).move_to(reach.get_center())
            self.play(Create(reach), run_time=t.fill(0.16))
            self.play(Create(cross), run_time=t.fill(0.16))
            self.guard = VGroup(reach, cross)
            self.say(t, "one process cannot reach into another's memory", fraction=0.25)
            t.hold()

        disk = MemoryBar(width=8.6, height=0.8, label="Secondary storage",
                         color=GREY)
        disk.next_to(ram, DOWN, buff=GAP_LG * 0.95)
        disk.move_to([ram.get_center()[0], disk.get_center()[1], 0])
        self.disk = disk

        with self.beat("virtual") as t:
            self.play(FadeOut(self.guard), run_time=t.fill(0.08))
            self.play(Create(disk.frame), FadeIn(disk.name),
                      run_time=t.fill(0.3))
            borrowed = disk.allocate("virtual memory", 0.42, color=SLATE)
            self.borrowed = borrowed
            self.play(FadeIn(borrowed), run_time=t.fill(0.3))
            t.hold()

        with self.beat("virtual_what") as t:
            self.say(t, "part of the disk, used as if it were extra RAM",
                     fraction=0.4)
            t.hold()

        with self.beat("slower") as t:
            slower = serif("slower than RAM", LABEL_SIZE, TERRACOTTA)
            slower.move_to([disk.frame.get_right()[0] - slower.width / 2,
                            disk.name.get_center()[1], 0])
            self.play(FadeIn(slower), run_time=t.fill(0.4))
            t.hold()

        with self.beat("excessive") as t:
            self.say(t, "lean on it too hard and performance drops",
                     fraction=0.4)
            t.hold()

        with self.beat("mem_exam") as t:
            self.wipe(t)
            self.title(t, "In the exam", fraction=0.1, color=SLATE)
            strong, each = chips(["allocation", "protection", "virtual memory"],
                                 size=TITLE_SIZE, color=SAGE, rows=2)
            self.place(strong, self.head, buff=GAP_LG * 0.9)
            for chip in each:
                self.play(Write(chip), run_time=t.fill(0.17))
            self.strong = strong
            t.hold()

        with self.beat("mem_weak") as t:
            weak = serif("“It controls RAM.”", BODY_SIZE, CHARCOAL)
            self.place(weak, self.strong, buff=GAP_LG * 0.9)
            self.play(Write(weak), run_time=t.fill(0.25))
            self.play(Create(strike(weak)), run_time=t.fill(0.14))
            self.say(t, "name the jobs, do not just name the hardware",
                     fraction=0.2)
            t.hold()

    # ----------------------------------------------- 6. managing multitasking

    def multitasking(self):
        with self.beat("multi") as t:
            self.section(t, "Managing multitasking", MULTITASKING)
            # Two rows, because the sentence with "appears" picked out of
            # it runs wider than the frame on one.
            top_row = VGroup(
                serif("more than one process", BODY_SIZE, CHARCOAL),
                serif("appears", BODY_SIZE, TERRACOTTA),
            ).arrange(RIGHT, buff=GAP_SM * 0.5)
            line = VGroup(
                top_row,
                serif("to run at the same time", BODY_SIZE, CHARCOAL),
            ).arrange(DOWN, buff=GAP_SM)
            fit(line, 12.0)
            self.place(line, self.head, buff=GAP_MD * 1.3)
            self.claim = line
            self.play(FadeIn(line), run_time=t.fill(0.45))
            t.hold()

        with self.beat("process_def") as t:
            definition = prose("A process is a program that is currently "
                               "being executed.", LABEL_SIZE, GREY, 11.6)
            self.place(definition, self.claim, buff=GAP_MD)
            self.definition = definition
            self.play(FadeIn(definition), run_time=t.fill(0.5))
            t.hold()

        lanes = TimeSlices(PROCESSES, SLICE_ORDER, width=8.4)

        with self.beat("single_core") as t:
            self.play(FadeOut(self.claim), FadeOut(self.definition),
                      run_time=t.fill(0.08))
            # The slices stay in the group so place() measures the finished
            # figure, but they are not shown until the next beat.
            self.place(lanes, self.head, buff=GAP_MD * 1.2)
            self.lanes = lanes
            self.play(FadeIn(lanes.labels), run_time=t.fill(0.2))
            self.play(Create(lanes.lanes), Create(lanes.axis),
                      FadeIn(lanes.time), run_time=t.fill(0.3))
            self.say(t, "one core, so one process at a time", fraction=0.22)
            t.hold()

        with self.beat("allocates") as t:
            for block in lanes.slices:
                self.play(FadeIn(block), run_time=t.fill(0.07))
            t.hold()

        with self.beat("impression") as t:
            self.say(t, "fast enough that it looks simultaneous",
                     fraction=0.5)
            t.hold()

        with self.beat("multi_eg") as t:
            self.say(t, "music, a download, a document, notifications", fraction=0.4)
            t.hold()

        with self.beat("share") as t:
            self.wipe(t)
            self.title(t, "What gets shared", fraction=0.12, color=SLATE)
            shared, each = chips(["processor time", "memory",
                                  "other resources"], size=TITLE_SIZE,
                                 rows=2)
            self.place(shared, self.head, buff=GAP_LG)
            for chip in each:
                self.play(Write(chip), run_time=t.fill(0.2))
            t.hold()

    # ---------------------------------------------- 8. providing system security

    def system_security(self):
        with self.beat("security") as t:
            self.section(t, "Providing system security", SECURITY)
            self.say(t, "it protects the computer and what is on it",
                     anchor=self.head, buff=GAP_MD * 1.2, size=BODY_SIZE,
                     color=CHARCOAL, fraction=0.4)
            t.hold()

        with self.beat("sec_list") as t:
            rows = VGroup(*[serif(f"·  {job}", LABEL_SIZE, CHARCOAL)
                            for job in SECURITY_JOBS])
            rows.arrange(DOWN, buff=GAP_SM * 0.9, aligned_edge=LEFT)
            self.place(rows, self.note, buff=GAP_MD * 1.1)
            for row in rows:
                self.play(FadeIn(row), run_time=t.fill(0.11))
            t.hold()

        with self.beat("sec_not_all") as t:
            self.wipe(t)
            claim = prose("It does not mean nothing can ever get in.",
                          TITLE_SIZE, TERRACOTTA, 12.0)
            claim.move_to([0, 0.95, 0])
            self.claim = claim
            self.play(Write(claim), run_time=t.fill(0.55))
            t.hold()

        with self.beat("sec_mechanisms") as t:
            answer = prose("It means there are mechanisms for controlling "
                           "and protecting access.", BODY_SIZE, SAGE, 11.8)
            self.place(answer, self.claim, buff=GAP_LG * 0.8)
            self.play(Write(answer), run_time=t.fill(0.6))
            t.hold()

    # ------------------------------------------------ 9. managing user accounts

    def user_accounts(self):
        with self.beat("accounts") as t:
            self.section(t, "Managing user accounts", ACCOUNTS)
            t.hold()

        cards = VGroup()
        for name in ("Administrator", "Standard user"):
            label = serif(name, LABEL_SIZE, CHARCOAL)
            cards.add(VGroup(boxed(label, pad=GAP_MD * 0.8), label))
        cards.arrange(RIGHT, buff=GAP_LG * 1.5)
        self.cards = cards

        with self.beat("acct_maintain") as t:
            self.place(cards, self.head, buff=GAP_MD * 1.4)
            self.play(FadeIn(cards), run_time=t.fill(0.45))
            t.hold()

        with self.beat("acct_each") as t:
            fields, each = chips(ACCOUNT_FIELDS, size=LABEL_SIZE, rows=2)
            self.place(fields, cards, buff=GAP_MD * 1.4)
            self.fields = fields
            for chip in each:
                self.play(FadeIn(chip), run_time=t.fill(0.1))
            t.hold()

        with self.beat("admin") as t:
            self.play(cards[0][0].animate.set_stroke(TERRACOTTA),
                      cards[0][1].animate.set_color(TERRACOTTA),
                      run_time=t.fill(0.2))
            self.say(t, "more control than a standard user", fraction=0.4)
            t.hold()

        with self.beat("admin_why") as t:
            self.say(t, "so not every user can change what matters",
                     fraction=0.5)
            t.hold()

    # ------------------------- 7. providing a platform for running applications

    def the_platform(self):
        with self.beat("platform") as t:
            self.section(t, "A platform for applications", PLATFORM)
            t.hold()

        # A wider gap than the default: "asks for" has to sit beside the
        # arrow without touching either box.
        stack = LayerStack(["Application software", "Operating system"],
                           width=6.4, height=0.78, gap=0.8)
        self.plat_stack = stack

        with self.beat("plat_services") as t:
            # Tight under the heading on purpose: the six services below
            # need the rest of the frame, and place() tightening this gap
            # for them would push the boxes and the list together.
            self.place(stack, self.head, buff=GAP_MD * 0.7)
            self.play(Create(stack.boxes), Write(stack.labels),
                      run_time=t.fill(0.3))
            self.play(Create(stack.arrows), run_time=t.fill(0.14))
            asks = serif("asks for", MARGIN_SIZE, GREY)
            asks.next_to(stack.arrows[0], RIGHT, buff=GAP_SM * 0.8)
            self.play(FadeIn(asks), run_time=t.fill(0.18))
            t.hold()

        with self.beat("plat_list") as t:
            jobs, each = grid(PLATFORM_JOBS, columns=2, size=MARGIN_SIZE)
            self.place(jobs, stack, buff=GAP_MD * 1.1)
            self.jobs = jobs
            for chip in each:
                self.play(FadeIn(chip), run_time=t.fill(0.1))
            t.hold()

        with self.beat("why_platform") as t:
            self.wipe(t)
            line = prose("Everything an application needs, it asks the "
                         "operating system for.", TITLE_SIZE, SAGE, 12.0)
            line.move_to([0, 0.3, 0])
            self.play(Write(line), run_time=t.fill(0.6))
            t.hold()

    # ------------------------------------------------- 2. handling interrupts

    def handling_interrupts(self):
        with self.beat("interrupts") as t:
            self.section(t, "Handling interrupts", INTERRUPTS)
            t.hold()

        with self.beat("int_manage") as t:
            self.say(t, "the operating system manages these too",
                     anchor=self.head, buff=GAP_MD * 1.3, size=BODY_SIZE,
                     color=CHARCOAL, fraction=0.45)
            t.hold()

        with self.beat("int_def") as t:
            word = serif("An interrupt", TITLE_SIZE, TERRACOTTA)
            body = prose("a signal or event that requires the processor's "
                         "attention.", BODY_SIZE, CHARCOAL, 11.6)
            card = VGroup(word, body).arrange(DOWN, buff=GAP_MD)
            self.place(card, self.note, buff=GAP_MD * 1.4)
            self.play(Write(word), run_time=t.fill(0.25))
            self.play(Write(body), run_time=t.fill(0.4))
            self.card = card
            t.hold()

        with self.beat("next_time") as t:
            # All nine, lit at once: the strip has been counting them off
            # one at a time for five minutes and this is the moment it adds
            # up to the syllabus list.
            self.play(*[cell.animate.set_stroke(SLATE)
                        .set_fill(SLATE, opacity=1)
                        for cell in self.strip.cells],
                      *[number.animate.set_color(CREAM)
                        for number in self.strip.numbers],
                      run_time=t.fill(0.2))
            nxt = serif("Next: how an interrupt is handled", LABEL_SIZE, GREY)
            self.place(nxt, self.card, buff=GAP_MD * 1.2)
            self.play(FadeIn(nxt), run_time=t.fill(0.35))
            t.hold()

    # ---------------------------------------------------------------- helpers

    _beat_name = "(before the first beat)"

    @contextmanager
    def beat(self, name):
        self._beat_name = name
        with super().beat(name) as timer:
            yield timer

    def section(self, t, text, index, fraction=0.22):
        """Open one of the nine: clear the frame, move the strip, name it."""
        self.wipe(t)
        self.play(*self.strip.focus(index), run_time=t.fill(0.06))
        self.title(t, text, fraction=fraction)

    def clear(self, t, *groups, fraction=0.1, with_note=False):
        """Fade a figure that was drawn child by child.

        Create() on a group's children adds the children to the scene, not
        the group, so FadeOut(group) removes something the scene never held.

        ``with_note`` takes the running commentary line with it. Dropping
        the figure and leaving its caption is how a sentence about the last
        picture ends up underneath the next one.
        """
        family = set()
        for group in groups:
            family.update(id(m) for m in group.get_family())
        # Matched both ways round. A figure drawn with Create(stack.boxes)
        # puts that container in the scene, and the container is a sibling
        # of the figure rather than a child of it, so looking for it inside
        # the figure's family does not find it and the boxes stay on screen
        # under whatever comes next.
        present = [m for m in self.mobjects
                   if any(id(child) in family for child in m.get_family())]
        if with_note and self.note is not None and self.note in self.mobjects:
            present.append(self.note)
        if present:
            self.play(*[FadeOut(m) for m in present], run_time=t.fill(fraction))
        if with_note:
            self.note = None

    def wipe(self, t, fraction=0.06, keep_head=False):
        spared = list(self.keep)
        if keep_head and self.head is not None:
            spared.append(self.head)
        old = [m for m in self.mobjects if m not in spared]
        if old:
            self.play(*[FadeOut(m) for m in old], run_time=t.fill(fraction))
        self.note = None
        if not keep_head:
            self.head = None

    def title(self, t, text, fraction=0.1, color=CHARCOAL):
        head = fit(serif(text, TITLE_SIZE, color))
        head.to_edge(UP, buff=GAP_MD * 1.7)
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
    # would leave content sitting over the strip. They say so.

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
            f"Beat '{self._beat_name}': a stack {group.height:.2f} units tall "
            f"cannot clear y={floor} under this heading. Shorten it."
        )

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
            f"for something {mobject.height:.2f} units tall above y={floor}. "
            "It would land on the numbered strip."
        )

    def guard_floor(self, mobject, what):
        if mobject.get_bottom()[1] < self.floor:
            raise ValueError(
                f"Beat '{self._beat_name}': {what} reaches "
                f"y={mobject.get_bottom()[1]:.2f}, below the floor at "
                f"y={self.floor:.2f}."
            )

    def say(self, t, text, fraction=0.2, color=GREY, size=LABEL_SIZE,
            y=None, anchor=None, buff=GAP_MD):
        """The running line of commentary, swapped in place."""
        line = prose(text, size, color, 12.0)
        if anchor is not None:
            self.place(line, anchor, buff=buff)
        else:
            line.move_to([0, self.floor + 0.35 if y is None else y, 0])
            self.band_is_clear(line)
        if self.note is None:
            self.note = line
            self.play(FadeIn(line), run_time=t.fill(fraction))
        else:
            line.move_to(self.note)
            self.play(Transform(self.note, line), run_time=t.fill(fraction))
        return self.note

    def band_is_clear(self, line, tol=0.05):
        """Refuse to print commentary through whatever is already there.

        The acceptance check compares writing against writing, so a caption
        laid across a diagram reads as clean: a box is a shape, not text.
        The band at the bottom of the frame is reserved for one line of
        commentary, and this is what reserves it.
        """
        for mobject in self.mobjects:
            if mobject in self.keep or mobject is self.note:
                continue
            wide = (min(line.get_right()[0], mobject.get_right()[0])
                    - max(line.get_left()[0], mobject.get_left()[0]))
            high = (min(line.get_top()[1], mobject.get_top()[1])
                    - max(line.get_bottom()[1], mobject.get_bottom()[1]))
            if wide > tol and high > tol:
                raise ValueError(
                    f"Beat '{self._beat_name}': the commentary band at "
                    f"y={line.get_center()[1]:.2f} runs through something "
                    "already on screen. Clear the frame first, or anchor the "
                    "line under the figure."
                )
