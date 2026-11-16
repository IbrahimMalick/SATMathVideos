"""Operating System, Chapter 1: Roman Urdu narration, English on screen.

The delivery is in Roman Urdu and every caption here is in English, as
asked. Nothing on screen is a translation of a sentence being spoken; the
captions are the English technical vocabulary the student has to be able
to write in an exam, landing on the word in the narration that motivates
it.

That split only works because the beats resolve against the recording.
build/textnorm.py folds words in whatever script they are written in, so
an Urdu anchor phrase matches honestly; the rule it replaced stripped
every non-ASCII character, folded every Urdu word to the empty string,
and matched anywhere at all.

The recording needed two repairs before a single beat could be trusted.
The recorder ran for three and a half minutes before the lecture started,
and the transcriber looped eleven times over 167 seconds of real speech.
Both are recorded in build/beats_osch01.py with the commands that undo
them.

The scheduling example is computed, not typed. components/os_core.py runs
first-come-first-served over the arrival and burst times, and the Gantt
chart, the results table and the average are all built from what it
returns, so the picture cannot drift away from the arithmetic beside it.
Checked against the lecture's own answer: order P1 P2 P3, starts 0/4/7,
completions 4/7/8, waiting 0/3/5, average 2.67.

Timing: timings/cs.os_chapter1.json
Render: python build/render.py scripts/OS-CH01-operating-system.md \\
    audio/OS-CH01-operating-system.m4a
"""

import textwrap
from contextlib import contextmanager

from manim import (
    Create,
    FadeIn,
    FadeOut,
    Line,
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
from components.os_core import (
    FCFS_ROWS,
    Chain,
    Gantt,
    Lifecycle,
    RingModel,
    ThreadBox,
    average_wait,
    callout,
    schedule,
)
from components.os_core import FileTree
from components.os_shape import (
    LayerStack,
    MemoryBar,
    TimeSlices,
    chips,
    grid,
    screen,
)
from components.syllabus_map import TopicStrip
from components.trace_table import TraceTable
from scenes.base import SATScene

FRAME_SAFE = 12.6
FLOOR = -3.05          # the numbered strip owns everything below this
BARE_FLOOR = -3.5      # before the strip exists

# The twelve sections, in the order the lecture takes them. The strip
# along the bottom counts these, not the syllabus.
PARTS = ["What an OS does", "User accounts", "Kernel and shell",
         "Layers and drivers", "Processes", "Scheduling", "Multitasking",
         "Memory", "Threads", "System calls", "File systems", "The journey"]
(WHAT, ACCOUNTS, KERNEL, LAYERS, PROCESS, SCHEDULING, MULTI, MEMORY,
 THREADS, SYSCALLS, FILES, JOURNEY) = range(12)

AGENDA = ["Kernel", "Shell", "OS layers", "User accounts", "Processes",
          "Threads", "Memory", "System calls", "File systems",
          "FCFS scheduling"]
HARDWARE = ["CPU", "RAM", "Storage drive", "Keyboard", "Screen",
            "Network card"]
APPS = ["Browser", "Games", "Word processor", "Messaging"]
OS_NAMES = ["Windows", "Linux", "macOS", "Android", "iOS"]
ACCOUNT_FIELDS = ["Username", "Settings", "Files", "Permissions"]
KERNEL_JOBS = ["CPU time", "Memory", "Devices"]
DRIVERS = ["Printer driver", "Sound driver", "Network driver"]
METADATA = ["Name", "Size", "Type", "Date created"]
SYSCALL_TYPES = [
    ("Process management", "create or end a process  ·  fork"),
    ("File management", "open, read, write"),
    ("Device management", "use a printer or another device"),
    ("Communication", "send and receive between programs"),
]
# Nine lines, each short enough to sit on one line of the frame at the
# 28px floor. place() only guards height, so an over-wide line would run
# off the side with nothing but the acceptance check to catch it; the
# recap builds its own width guard for that reason.
RECAP = [
    "The kernel is the core; the shell is the interface.",
    "The layers carry a request down to the hardware.",
    "User accounts keep files and permissions apart.",
    "A process is created, executed, then terminated.",
    "In FCFS the process that arrives first runs first.",
    "Multitasking manages tasks; concurrency overlaps.",
    "Threads run inside one process and share its memory.",
    "System calls ask the OS for a service.",
    "File systems organise; metadata describes.",
]

QUESTIONS = [
    "How does an operating system carry your request to the hardware?",
    "What do multiple user accounts and permissions give you?",
    "What is the difference between the kernel and the shell?",
    "How do you find waiting time in an FCFS question?",
    "What is the difference between a process and a thread?",
    "Name three types of system call.",
    "What do a file system and metadata do?",
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


class OsChapter1(SATScene):
    scene_id = "cs.os_chapter1"

    def construct(self):
        self.margin = mono("Operating System · Chapter 1", MARGIN_SIZE)
        self.margin.to_corner(UP + LEFT, buff=GAP_SM)
        self.add(self.margin)

        self.strip = TopicStrip(len(PARTS), lit=SLATE, side=0.56)
        self.strip.to_edge(DOWN, buff=GAP_SM * 0.5)

        self.keep = [self.margin]
        self.floor = BARE_FLOOR
        self.head = None
        self.note = None

        self.opening()
        self.what_an_os_does()
        self.user_accounts()
        self.kernel_and_shell()
        self.layers_and_drivers()
        self.processes()
        self.scheduling()
        self.multitasking()
        self.memory()
        self.threads()
        self.system_calls()
        self.file_systems()
        self.the_journey()
        self.recap()
        self.self_check()

    # --------------------------------------------------------------- opening

    def opening(self):
        with self.beat("open") as t:
            title = serif("Operating System", DISPLAY_SIZE, CHARCOAL)
            chapter = serif("Chapter 1", LABEL_SIZE, SLATE)
            under = prose("What it is, and how it carries your request to "
                          "the hardware", LABEL_SIZE, GREY)
            card = VGroup(chapter, title, under).arrange(DOWN, buff=GAP_MD)
            card.move_to(ORIGIN)
            self.play(FadeIn(chapter), run_time=t.fill(0.08))
            self.play(Write(title), run_time=t.fill(0.22))
            self.play(FadeIn(under), run_time=t.fill(0.14))
            t.hold()

        with self.beat("behind") as t:
            self.wipe(t)
            self.title(t, "Everything you do goes through it", fraction=0.1)
            doing, each = chips(["Open your account", "Run a browser",
                                 "Save a file", "Visit a website"],
                                size=LABEL_SIZE, rows=2)
            self.place(doing, self.head, buff=GAP_LG * 0.9)
            for chip in each:
                self.play(FadeIn(chip), run_time=t.fill(0.07))
            self.say(t, "Behind every one of them, the operating system "
                        "is working", fraction=0.14)
            t.hold()

        with self.beat("agenda") as t:
            self.wipe(t)
            self.title(t, "What this chapter covers", fraction=0.09)
            plan, items = grid(AGENDA, columns=2, size=LABEL_SIZE,
                               h_gap=GAP_LG * 1.3, v_gap=GAP_SM * 1.5)
            self.place(plan, self.head, buff=GAP_MD * 1.3)
            self.plan, self.plan_items = plan, items
            for item in items:
                self.play(FadeIn(item), run_time=t.fill(0.055))
            t.hold()

        with self.beat("fcfs_promise") as t:
            # The scheduling question is the one thing in this chapter the
            # student has to be able to *do*, so it is the one thing the
            # agenda points at.
            self.play(self.plan_items[-1].animate.set_color(TERRACOTTA),
                      run_time=t.fill(0.14))
            self.say(t, "and one scheduling question, solved together",
                     fraction=0.25)
            t.hold()

    # ------------------------------------------------- 1. what an OS does

    def what_an_os_does(self):
        with self.beat("definition") as t:
            self.section(t, "What an operating system does", WHAT)
            body = self.lines(
                "An operating system is system software.",
                "It manages the computer's hardware resources.",
            )
            self.stack(body, self.head, buff=GAP_MD * 1.4)
            self.defn = body
            self.play(FadeIn(body[0]), run_time=t.fill(0.2))
            self.play(FadeIn(body[1]), run_time=t.fill(0.2))
            t.hold()

        with self.beat("gives_access") as t:
            more = prose("And it gives you and your applications a way to "
                         "use them.", BODY_SIZE, CHARCOAL, 11.8)
            self.place(more, self.defn, buff=GAP_MD * 1.2)
            self.play(FadeIn(more), run_time=t.fill(0.3))
            t.hold()

        with self.beat("hardware") as t:
            self.wipe(t)
            self.title(t, "Hardware", fraction=0.1, color=SLATE)
            bits, each = chips(HARDWARE, size=LABEL_SIZE, rows=2)
            self.place(bits, self.head, buff=GAP_LG * 0.9)
            self.hardware = bits
            for chip in each:
                self.play(FadeIn(chip), run_time=t.fill(0.08))
            t.hold()

        with self.beat("apps") as t:
            apps_head = serif("Applications", TITLE_SIZE, SLATE)
            self.place(apps_head, self.hardware, buff=GAP_LG * 0.8)
            software, each = chips(APPS, size=LABEL_SIZE, rows=1)
            self.place(software, apps_head, buff=GAP_MD)
            self.play(Write(apps_head), run_time=t.fill(0.14))
            for chip in each:
                self.play(FadeIn(chip), run_time=t.fill(0.08))
            t.hold()

        route = Chain(["You\ndouble-click", "Application",
                       "Operating\nsystem", "Storage\nand screen"],
                      width=2.7, height=1.25)

        with self.beat("double_click") as t:
            self.wipe(t)
            self.title(t, "You double-click a file", fraction=0.1)
            self.place(route, self.head, buff=GAP_LG)
            self.route = route
            self.play(Create(route.boxes[0]), Write(route.labels[0]),
                      run_time=t.fill(0.25))
            self.say(t, "That is a user action", fraction=0.14)
            t.hold()

        with self.beat("request_travels") as t:
            for index in (1, 2):
                self.play(Create(route.arrows[index - 1]),
                          Create(route.boxes[index]),
                          Write(route.labels[index]), run_time=t.fill(0.2))
            self.say(t, "The request reaches the operating system",
                     fraction=0.2)
            t.hold()

        with self.beat("os_decides") as t:
            self.play(*route.light(2), run_time=t.fill(0.12))
            steps = self.lines(
                "Read the file from storage",
                "Put the data in memory",
                "Show it on the screen",
                size=LABEL_SIZE, color=GREY,
            )
            self.place(steps, route, buff=GAP_MD)
            self.play(FadeIn(steps), run_time=t.fill(0.3))
            self.steps = steps
            t.hold()

        with self.beat("no_detail") as t:
            self.play(Create(route.arrows[2]), Create(route.boxes[3]),
                      Write(route.labels[3]), run_time=t.fill(0.22))
            self.play(*route.settle(2), FadeOut(self.steps),
                      run_time=t.fill(0.1))
            self.say(t, "You never control the hardware yourself",
                     fraction=0.25)
            t.hold()

        with self.beat("waiter") as t:
            self.wipe(t)
            self.title(t, "Like ordering in a restaurant", fraction=0.1)
            table = Chain(["You", "The waiter", "The kitchen"],
                          width=3.0, height=1.2)
            self.place(table, self.head, buff=GAP_LG)
            self.play(Create(table.boxes), Write(table.labels),
                      run_time=t.fill(0.25))
            self.play(Create(table.arrows), run_time=t.fill(0.12))
            self.restaurant = table
            self.say(t, "The waiter carries your order, and brings the "
                        "food back", fraction=0.2)
            t.hold()

        with self.beat("os_examples") as t:
            self.wipe(t)
            self.title(t, "Operating systems you have used", fraction=0.1)
            names, each = chips(OS_NAMES, size=TITLE_SIZE, rows=2)
            self.place(names, self.head, buff=GAP_LG)
            for chip in each:
                self.play(FadeIn(chip), run_time=t.fill(0.1))
            t.hold()

    # --------------------------------------------------- 2. user accounts

    def user_accounts(self):
        with self.beat("many_users") as t:
            self.section(t, "Managing user accounts", ACCOUNTS)
            self.say(t, "One computer, and several people using it",
                     anchor=self.head, buff=GAP_MD * 1.3, size=BODY_SIZE,
                     color=CHARCOAL, fraction=0.4)
            t.hold()

        with self.beat("account_has") as t:
            fields, each = chips(ACCOUNT_FIELDS, size=LABEL_SIZE, rows=2)
            self.place(fields, self.note, buff=GAP_MD * 1.3)
            self.fields = fields
            for chip in each:
                self.play(FadeIn(chip), run_time=t.fill(0.1))
            t.hold()

        with self.beat("login_check") as t:
            self.wipe(t)
            self.title(t, "At login", fraction=0.1, color=SLATE)
            flow = Chain(["Who are you?", "Check the\npermissions",
                          "What may you\nopen?"], width=3.4, height=1.3)
            self.place(flow, self.head, buff=GAP_LG)
            self.login = flow
            self.play(Create(flow.boxes), Write(flow.labels),
                      run_time=t.fill(0.3))
            self.play(Create(flow.arrows), run_time=t.fill(0.14))
            t.hold()

        cards = VGroup()
        for name, note in (("Administrator", "changes system settings"),
                           ("Standard user", "own files and settings")):
            label = serif(name, LABEL_SIZE, CHARCOAL)
            under = serif(note, MARGIN_SIZE, GREY)
            column = VGroup(label, under).arrange(DOWN, buff=GAP_SM)
            box = SurroundingRectangle(column, color=SLATE, stroke_width=2.5,
                                       buff=GAP_MD * 0.8, corner_radius=0.0)
            cards.add(VGroup(box, column))
        cards.arrange(RIGHT, buff=GAP_LG)
        if cards.width > FRAME_SAFE:
            raise ValueError(
                f"The account cards run {cards.width:.2f} units.")

        with self.beat("admin") as t:
            self.wipe(t)
            self.title(t, "Not every account is equal", fraction=0.1)
            self.place(cards, self.head, buff=GAP_LG)
            self.cards = cards
            self.play(FadeIn(cards), run_time=t.fill(0.35))
            t.hold()

        with self.beat("siblings") as t:
            self.say(t, "Your brother's account cannot open your files",
                     fraction=0.4)
            t.hold()

        with self.beat("accounts_recap") as t:
            self.wipe(t)
            self.title(t, "So the operating system", fraction=0.1,
                       color=SLATE)
            jobs = self.lines(
                "manages the accounts",
                "checks who each user is",
                "controls access through permissions",
                size=BODY_SIZE, align=LEFT,
            )
            self.stack(jobs, self.head, buff=GAP_MD * 1.2, align=LEFT)
            for line in jobs:
                self.play(FadeIn(line), run_time=t.fill(0.14))
            t.hold()

    # ------------------------------------------------ 3. kernel and shell

    def kernel_and_shell(self):
        """Rings on the left, words on the right.

        A circular figure wants the frame's width, not its height. Stacked
        under a heading the rings reach past y=-2.8 and there is nowhere
        left for a line of commentary, which is what the band guard said
        the first time this was laid out.
        """
        rings = RingModel(radii=(1.15, 1.65, 2.15, 2.62))
        # Centred on zero, not above it: at 0.35 the outermost ring's
        # label reaches y=2.73 and the heading's underside is at 2.68.
        rings.move_to([-3.5, 0.0, 0])
        self.rings = rings
        self.side = None

        with self.beat("kernel_shell") as t:
            self.section(t, "The kernel and the shell", KERNEL)
            self.play(Create(rings.rings), run_time=t.fill(0.3))
            self.play(FadeIn(rings.labels), run_time=t.fill(0.18))
            t.hold()

        with self.beat("kernel") as t:
            self.play(*rings.light(1), run_time=t.fill(0.2))
            self.side_note(t, "The kernel is the central part of the "
                              "operating system.", fraction=0.3)
            t.hold()

        with self.beat("kernel_time") as t:
            jobs = VGroup(*[serif(f"\u00b7  {job}", LABEL_SIZE, CHARCOAL)
                            for job in KERNEL_JOBS])
            jobs.arrange(DOWN, buff=GAP_SM, aligned_edge=LEFT)
            jobs.move_to([3.6, -1.25, 0])
            self.kernel_jobs = jobs
            for job in jobs:
                self.play(FadeIn(job), run_time=t.fill(0.12))
            t.hold()

        with self.beat("shell") as t:
            self.play(*rings.settle_all(), *rings.light(2),
                      run_time=t.fill(0.18))
            # clear(), not FadeOut(group): the rows went on screen one
            # at a time, so the scene holds the rows and not the group
            # that owns them.
            self.clear(t, self.kernel_jobs, fraction=0.06)
            self.side_note(t, "The shell is the interface between you and "
                              "the operating system.", fraction=0.3)
            t.hold()

        panel = VGroup()
        for kind, name, note in (("gui", "Graphical shell",
                                  "windows, icons, menus"),
                                 ("cli", "Command-line shell",
                                  "you type the command")):
            shot = screen(kind, width=5.0, height=2.4)
            head = serif(name, LABEL_SIZE, SLATE)
            under = serif(note, MARGIN_SIZE, GREY)
            panel.add(VGroup(head, shot, under).arrange(DOWN, buff=GAP_SM))
        panel.arrange(RIGHT, buff=GAP_MD * 1.4)

        with self.beat("gui") as t:
            self.clear(t, rings, with_note=True, fraction=0.1)
            if self.side is not None:
                self.play(FadeOut(self.side), run_time=t.fill(0.05))
                self.side = None
            self.place(panel, self.head, buff=GAP_MD * 0.9)
            self.panel = panel
            self.play(FadeIn(panel[0][0]), run_time=t.fill(0.08))
            self.play(Create(panel[0][1]), run_time=t.fill(0.3))
            self.play(FadeIn(panel[0][2]), run_time=t.fill(0.1))
            t.hold()

        with self.beat("cli") as t:
            self.play(FadeIn(panel[1][0]), run_time=t.fill(0.1))
            self.play(Create(panel[1][1]), run_time=t.fill(0.32))
            self.play(FadeIn(panel[1][2]), run_time=t.fill(0.12))
            t.hold()

        with self.beat("one_line") as t:
            self.wipe(t)
            line = self.lines(
                "The shell takes your request.",
                "The kernel manages the resources.",
                size=TITLE_SIZE,
            )
            line.move_to(ORIGIN)
            self.play(Write(line[0]), run_time=t.fill(0.26))
            self.play(Write(line[1]), run_time=t.fill(0.26))
            t.hold()

    # -------------------------------------------- 4. layers and drivers

    def layers_and_drivers(self):
        stack = LayerStack(["You and your applications", "Operating system",
                            "Kernel and device drivers"], width=8.0)

        with self.beat("layers") as t:
            self.section(t, "The layers of an operating system", LAYERS)
            self.place(stack, self.head, buff=GAP_MD)
            self.stack_fig = stack
            self.play(Create(stack.boxes), Write(stack.labels),
                      run_time=t.fill(0.3))
            self.play(Create(stack.arrows), run_time=t.fill(0.14))
            t.hold()

        for beat, index, caption in (
                ("upper", 0, "The upper layer is closest to you"),
                ("middle", 1, "The middle layer manages the services"),
                ("lower", 2, "The lower layer is closest to the hardware")):
            with self.beat(beat) as t:
                if index:
                    self.play(*stack.settle(index - 1), run_time=t.fill(0.06))
                self.play(*stack.light(index), run_time=t.fill(0.14))
                self.say(t, caption, fraction=0.25)
                t.hold()

        printing = Chain(["Application", "Operating\nsystem",
                          "Printer\ndriver", "Printer"],
                         width=2.7, height=1.25)

        with self.beat("print_example") as t:
            self.clear(t, stack, with_note=True, fraction=0.1)
            self.title_swap(t, "Printing a document", fraction=0.1)
            self.place(printing, self.head, buff=GAP_LG)
            self.printing = printing
            self.play(Create(printing.boxes[:2]),
                      Write(printing.labels[:2]),
                      Create(printing.arrows[0]), run_time=t.fill(0.28))
            t.hold()

        with self.beat("printer_driver") as t:
            self.play(Create(printing.arrows[1]), Create(printing.boxes[2]),
                      Write(printing.labels[2]), run_time=t.fill(0.22))
            self.play(Create(printing.arrows[2]), Create(printing.boxes[3]),
                      Write(printing.labels[3]), run_time=t.fill(0.22))
            self.say(t, "The driver turns it into commands the printer "
                        "understands", fraction=0.2)
            t.hold()

        with self.beat("libraries") as t:
            self.wipe(t)
            self.title(t, "System libraries", fraction=0.1)
            body = prose("Ready-made functions and code that help programs "
                         "do ordinary jobs.", BODY_SIZE, CHARCOAL, 11.8)
            self.place(body, self.head, buff=GAP_LG)
            self.play(Write(body), run_time=t.fill(0.45))
            t.hold()

        with self.beat("driver_def") as t:
            self.wipe(t)
            self.title(t, "A device driver", fraction=0.1)
            body = prose("helps the operating system communicate with one "
                         "particular piece of hardware.", BODY_SIZE,
                         CHARCOAL, 11.8)
            self.place(body, self.head, buff=GAP_MD * 1.4)
            self.driver_line = body
            self.play(Write(body), run_time=t.fill(0.4))
            t.hold()

        with self.beat("driver_eg") as t:
            names, each = chips(DRIVERS, size=LABEL_SIZE, rows=1)
            self.place(names, self.driver_line, buff=GAP_LG * 0.9)
            for chip in each:
                self.play(FadeIn(chip), run_time=t.fill(0.12))
            t.hold()

    # ------------------------------------------------------ 5. processes

    def processes(self):
        with self.beat("process") as t:
            self.section(t, "Processes", PROCESS)
            t.hold()

        with self.beat("process_def") as t:
            body = prose("A program that has started running is called a "
                         "process.", BODY_SIZE, CHARCOAL, 11.8)
            self.place(body, self.head, buff=GAP_MD * 1.4)
            self.proc_line = body
            self.play(Write(body), run_time=t.fill(0.4))
            t.hold()

        with self.beat("browser_example") as t:
            move = Chain(["The browser\non storage", "Loaded into\nmemory",
                          "Running:\na process"], width=3.4, height=1.3)
            self.place(move, self.proc_line, buff=GAP_MD * 1.3)
            self.move = move
            self.play(Create(move.boxes), Write(move.labels),
                      run_time=t.fill(0.3))
            self.play(Create(move.arrows), run_time=t.fill(0.14))
            t.hold()

        life = Lifecycle([("Creation", "resources ready"),
                          ("Execution", "instructions run"),
                          ("Termination", "resources back")])

        with self.beat("lifecycle") as t:
            self.wipe(t)
            self.title(t, "The life of a process", fraction=0.1)
            self.place(life, self.head, buff=GAP_LG)
            self.life = life
            self.play(Create(life.boxes), Write(life.labels),
                      run_time=t.fill(0.3))
            self.play(Create(life.arrows), FadeIn(life.notes),
                      run_time=t.fill(0.18))
            t.hold()

        with self.beat("termination") as t:
            self.play(*life.light(2), run_time=t.fill(0.2))
            self.say(t, "It finishes, or it is closed", fraction=0.3)
            t.hold()

        with self.beat("resources_back") as t:
            self.say(t, "and the operating system takes its resources back",
                     fraction=0.4)
            t.hold()

        with self.beat("calculator") as t:
            self.play(*life.settle(2), run_time=t.fill(0.06))
            self.say(t, "Opening the calculator is creation", fraction=0.3)
            self.play(*life.light(0), run_time=t.fill(0.14))
            t.hold()

        with self.beat("calc_three") as t:
            self.play(*life.settle(0), *life.light(1), run_time=t.fill(0.14))
            self.say(t, "Doing a calculation is execution", fraction=0.2)
            self.play(*life.settle(1), *life.light(2), run_time=t.fill(0.14))
            self.say(t, "Closing it is termination", fraction=0.2)
            t.hold()

    # ----------------------------------------------------- 6. scheduling

    def scheduling(self):
        runs = schedule(FCFS_ROWS)

        with self.beat("fcfs") as t:
            self.section(t, "First come, first served", SCHEDULING)
            t.hold()

        with self.beat("waiting_cpu") as t:
            self.say(t, "Several processes, and one CPU to share",
                     anchor=self.head, buff=GAP_MD * 1.3, size=BODY_SIZE,
                     color=CHARCOAL, fraction=0.4)
            t.hold()

        with self.beat("scheduling") as t:
            body = prose("Deciding which process gets the CPU first is "
                         "called process scheduling.", BODY_SIZE, CHARCOAL,
                         11.8)
            self.place(body, self.note, buff=GAP_MD * 1.3)
            self.play(Write(body), run_time=t.fill(0.45))
            t.hold()

        with self.beat("first_come") as t:
            self.wipe(t)
            rule = prose("The process that arrives first runs first.",
                         TITLE_SIZE, CHARCOAL, 12.0)
            rule.move_to([0, 0.9, 0])
            self.play(Write(rule), run_time=t.fill(0.5))
            self.rule = rule
            t.hold()

        with self.beat("bakery") as t:
            self.say(t, "Like a queue at the bakery: your turn comes when "
                        "your number comes", anchor=self.rule,
                     buff=GAP_LG * 0.9, fraction=0.45)
            t.hold()

        table = TraceTable(
            ["Process", "Arrival", "Burst"],
            [(name, f"{arrival} s", f"{burst} s")
             for name, arrival, burst in FCFS_ROWS],
            row_height=0.62, col_width=2.2)
        table.hidden()

        with self.beat("the_table") as t:
            self.wipe(t)
            self.title(t, "The question", fraction=0.09, color=SLATE)
            self.place(table, self.head, buff=GAP_MD * 1.2)
            self.table = table
            self.play(Write(table.head), Create(table.rule),
                      run_time=t.fill(0.16))
            for index in range(len(table.rows)):
                self.play(*table.step(index), run_time=t.fill(0.12))
            t.hold()

        chart = Gantt(runs, width=9.4)

        with self.beat("order") as t:
            self.wipe(t)
            self.title(t, "Execution order", fraction=0.08, color=SLATE)
            order, each = chips(["P1", "P2", "P3"], size=DISPLAY_SIZE,
                                rows=1)
            self.place(order, self.head, buff=GAP_MD * 1.1)
            self.order = order
            for chip in each:
                self.play(Write(chip), run_time=t.fill(0.12))
            self.place(chart, order, buff=GAP_MD * 1.3)
            self.chart = chart
            self.play(Create(chart.axis), FadeIn(chart.ticks),
                      FadeIn(chart.numbers), run_time=t.fill(0.2))
            t.hold()

        for beat, index in (("p1_runs", 0), ("p2_runs", 1), ("p3_runs", 2)):
            name, arrival, burst, start, complete, _ = runs[index]
            with self.beat(beat) as t:
                self.play(FadeIn(chart.bars[index]),
                          FadeIn(chart.labels[index]), run_time=t.fill(0.3))
                self.say(t, f"{name} starts at {start} and completes "
                            f"at {complete}", fraction=0.3)
                t.hold()

        with self.beat("formula") as t:
            self.wipe(t)
            formula = serif("Waiting time  =  Start time  −  Arrival time",
                            TITLE_SIZE, CHARCOAL)
            fit(formula, 12.0)
            formula.move_to([0, 2.1, 0])
            self.formula = formula
            self.play(Write(formula), run_time=t.fill(0.45))
            t.hold()

        waits = TraceTable(
            ["Process", "Start", "Arrival", "Waiting"],
            [(name, f"{start}", f"{arrival}", f"{wait} s")
             for name, arrival, burst, start, complete, wait in runs],
            row_height=0.62, col_width=2.1)
        waits.hidden()

        with self.beat("p1_wait") as t:
            self.place(waits, self.formula, buff=GAP_MD * 1.3)
            self.waits = waits
            self.play(Write(waits.head), Create(waits.rule),
                      run_time=t.fill(0.14))
            self.play(*waits.step(0), run_time=t.fill(0.2))
            t.hold()

        with self.beat("p23_wait") as t:
            self.play(*waits.step(1), run_time=t.fill(0.3))
            self.play(*waits.step(2), run_time=t.fill(0.3))
            t.hold()

        with self.beat("average") as t:
            mean = average_wait(runs)
            total = " + ".join(str(run[5]) for run in runs)
            line = serif(f"({total}) ÷ {len(runs)}  =  {mean:.2f} s",
                         TITLE_SIZE, SAGE)
            fit(line, 12.0)
            self.place(line, self.waits, buff=GAP_MD * 1.1)
            self.play(Write(line), run_time=t.fill(0.45))
            t.hold()

        with self.beat("exam_order") as t:
            self.wipe(t)
            self.title(t, "In the exam, show all four", fraction=0.1,
                       color=SLATE)
            order_lines = self.lines(
                "1.  the execution order",
                "2.  each start and completion time",
                size=BODY_SIZE, align=LEFT,
            )
            self.stack(order_lines, self.head, buff=GAP_MD, align=LEFT)
            self.exam = order_lines
            for line in order_lines:
                self.play(FadeIn(line), run_time=t.fill(0.2))
            t.hold()

        with self.beat("exam_rest") as t:
            rest = self.lines(
                "3.  the waiting time for each process",
                "4.  the average waiting time",
                size=BODY_SIZE, align=LEFT,
            )
            rest.arrange(DOWN, buff=GAP_MD, aligned_edge=LEFT)
            rest.next_to(self.exam, DOWN, buff=GAP_MD)
            rest.align_to(self.exam, LEFT)
            for line in rest:
                self.play(FadeIn(line), run_time=t.fill(0.25))
            t.hold()

    # --------------------------------------------------- 7. multitasking

    def multitasking(self):
        with self.beat("multitasking") as t:
            self.section(t, "Multitasking and concurrency", MULTI)
            body = prose("Multitasking: the operating system manages "
                         "several programs at once.", BODY_SIZE, CHARCOAL,
                         11.8)
            self.place(body, self.head, buff=GAP_MD * 1.3)
            self.multi_line = body
            self.play(Write(body), run_time=t.fill(0.45))
            t.hold()

        with self.beat("multi_eg") as t:
            doing, each = chips(["Music", "Browsing", "Messaging",
                                 "A download"], size=LABEL_SIZE, rows=2)
            self.place(doing, self.multi_line, buff=GAP_MD * 1.3)
            self.doing = doing
            for chip in each:
                self.play(FadeIn(chip), run_time=t.fill(0.1))
            t.hold()

        with self.beat("concurrency") as t:
            self.wipe(t)
            self.title(t, "Concurrency", fraction=0.1)
            body = prose("Several tasks making progress in the same "
                         "stretch of time.", BODY_SIZE, CHARCOAL, 11.8)
            self.place(body, self.head, buff=GAP_MD * 1.2)
            self.conc_line = body
            self.play(Write(body), run_time=t.fill(0.4))
            t.hold()

        lanes = TimeSlices(["Music", "Browser", "Download"],
                           [0, 1, 2, 0, 1, 2, 0, 1], width=8.4)

        with self.beat("switching") as t:
            self.place(lanes, self.conc_line, buff=GAP_MD * 1.1)
            self.lanes = lanes
            self.play(FadeIn(lanes.labels), run_time=t.fill(0.1))
            self.play(Create(lanes.lanes), Create(lanes.axis),
                      FadeIn(lanes.time), run_time=t.fill(0.18))
            for block in lanes.slices:
                self.play(FadeIn(block), run_time=t.fill(0.05))
            t.hold()

        with self.beat("chef") as t:
            self.wipe(t)
            self.title(t, "Like one cook, several pots", fraction=0.1)
            body = prose("The daal goes on to cook, the roti is made, then "
                         "back to the daal.", BODY_SIZE, CHARCOAL, 11.8)
            self.place(body, self.head, buff=GAP_LG)
            self.play(Write(body), run_time=t.fill(0.45))
            t.hold()

    # ---------------------------------------------------------- 8. memory

    def memory(self):
        ram = MemoryBar(width=8.6)

        with self.beat("ram") as t:
            self.section(t, "RAM and virtual memory", MEMORY)
            self.place(ram, self.head, buff=GAP_LG)
            self.ram = ram
            self.play(Create(ram.frame), FadeIn(ram.name),
                      run_time=t.fill(0.25))
            t.hold()

        with self.beat("ram_def") as t:
            blocks = VGroup()
            for name, share in (("browser", 0.34), ("music", 0.3),
                                ("document", 0.36)):
                blocks.add(ram.allocate(name, share))
            for block in blocks:
                self.play(FadeIn(block), run_time=t.fill(0.1))
            self.blocks = blocks
            self.say(t, "Running programs and their data sit here",
                     fraction=0.2)
            t.hold()

        with self.beat("ram_fast") as t:
            self.say(t, "The CPU reaches RAM quickly", fraction=0.4)
            t.hold()

        disk = MemoryBar(width=8.6, height=0.8, label="Secondary storage",
                         color=GREY)
        disk.next_to(ram, DOWN, buff=GAP_LG * 0.9)
        disk.move_to([ram.get_center()[0], disk.get_center()[1], 0])

        with self.beat("virtual") as t:
            self.play(Create(disk.frame), FadeIn(disk.name),
                      run_time=t.fill(0.25))
            borrowed = disk.allocate("virtual memory", 0.42, color=SLATE)
            self.play(FadeIn(borrowed), run_time=t.fill(0.25))
            self.disk, self.borrowed = disk, borrowed
            self.say(t, "When RAM fills up, part of the disk stands in",
                     fraction=0.2)
            t.hold()

        with self.beat("virtual_slow") as t:
            slower = serif("slower than RAM", LABEL_SIZE, TERRACOTTA)
            slower.move_to([disk.frame.get_right()[0] - slower.width / 2,
                            disk.name.get_center()[1], 0])
            self.play(FadeIn(slower), run_time=t.fill(0.2))
            self.say(t, "so leaning on it too hard slows the computer down",
                     fraction=0.3)
            t.hold()

    # --------------------------------------------------------- 9. threads

    def threads(self):
        box = ThreadBox("Process: a word processor", ["typing", "auto-save"])

        with self.beat("thread_def") as t:
            self.section(t, "Threads", THREADS)
            body = prose("A thread is a small unit of execution inside a "
                         "process.", BODY_SIZE, CHARCOAL, 11.8)
            self.place(body, self.head, buff=GAP_MD * 1.2)
            self.thread_line = body
            self.play(Write(body), run_time=t.fill(0.4))
            t.hold()

        with self.beat("thread_share") as t:
            self.place(box, self.thread_line, buff=GAP_MD * 1.1)
            self.box = box
            self.play(Create(box.box), Write(box.title),
                      run_time=t.fill(0.26))
            self.play(FadeIn(box.shared), run_time=t.fill(0.14))
            t.hold()

        with self.beat("word_threads") as t:
            self.play(FadeIn(box.lanes[0]), run_time=t.fill(0.3))
            t.hold()

        with self.beat("autosave") as t:
            # No band caption here. The box reaches y=-2.72 and the band
            # starts at -2.49, and the line it would carry only repeats
            # what the box already says along its own bottom edge.
            self.play(FadeIn(box.lanes[1]), run_time=t.fill(0.3))
            self.play(box.shared.animate.set_color(TERRACOTTA),
                      run_time=t.fill(0.2))
            t.hold()

        with self.beat("office") as t:
            self.wipe(t)
            self.title(t, "Like one office", fraction=0.1)
            body = self.lines(
                "The process is the office.",
                "The threads are the people working in it.",
                "They share the same room and the same files.",
                size=BODY_SIZE,
            )
            self.stack(body, self.head, buff=GAP_MD * 1.1)
            for line in body:
                self.play(FadeIn(line), run_time=t.fill(0.16))
            t.hold()

        with self.beat("multithreading") as t:
            self.wipe(t)
            self.title(t, "Multithreading", fraction=0.1)
            body = prose("Several jobs of one application running inside "
                         "the same process.", BODY_SIZE, CHARCOAL, 11.8)
            self.place(body, self.head, buff=GAP_MD * 1.3)
            self.mt_line = body
            self.play(Write(body), run_time=t.fill(0.4))
            t.hold()

        with self.beat("responsive") as t:
            gain = prose("Auto-save can run while you keep typing.",
                         TITLE_SIZE, SAGE, 12.0)
            self.place(gain, self.mt_line, buff=GAP_LG * 0.9)
            self.play(Write(gain), run_time=t.fill(0.5))
            t.hold()

    # ---------------------------------------------------- 10. system calls

    def system_calls(self):
        with self.beat("syscalls") as t:
            self.section(t, "System calls", SYSCALLS)
            t.hold()

        with self.beat("syscall_def") as t:
            body = prose("A system call is how a program asks the "
                         "operating system for a service.", BODY_SIZE,
                         CHARCOAL, 11.8)
            self.place(body, self.head, buff=GAP_MD * 1.3)
            self.sc_line = body
            self.play(Write(body), run_time=t.fill(0.42))
            t.hold()

        with self.beat("syscall_when") as t:
            when, each = chips(["Open a file", "Read data", "Write data",
                                "Start a process"], size=LABEL_SIZE, rows=2)
            self.place(when, self.sc_line, buff=GAP_MD * 1.3)
            self.when = when
            for chip in each:
                self.play(FadeIn(chip), run_time=t.fill(0.1))
            t.hold()

        rows = VGroup()
        for name, detail in SYSCALL_TYPES:
            head = serif(name, LABEL_SIZE, CHARCOAL)
            under = serif(detail, MARGIN_SIZE, GREY)
            rows.add(VGroup(head, under).arrange(DOWN, buff=GAP_SM * 0.5,
                                                 aligned_edge=LEFT))
        rows.arrange(DOWN, buff=GAP_SM * 1.3, aligned_edge=LEFT)

        with self.beat("sc_process") as t:
            self.wipe(t)
            self.title(t, "Four kinds you should know", fraction=0.09,
                       color=SLATE)
            self.place(rows, self.head, buff=GAP_MD * 1.1)
            self.sc_rows = rows
            self.play(FadeIn(rows[0]), run_time=t.fill(0.3))
            t.hold()

        for beat, index in (("sc_file", 1), ("sc_device", 2),
                            ("sc_comm", 3)):
            with self.beat(beat) as t:
                self.play(FadeIn(rows[index]), run_time=t.fill(0.35))
                t.hold()

        with self.beat("fork_note") as t:
            # Its own card. Four two-line rows fill the frame down to
            # y=-2.51, and place() said plainly that nothing more fits
            # above the strip, which is what it is there to say.
            self.wipe(t)
            name = mono("fork", DISPLAY_SIZE, TERRACOTTA)
            body = self.lines(
                "creates a new process on Unix and Linux.",
                "The names differ between operating systems.",
                size=BODY_SIZE, color=CHARCOAL,
            )
            card = VGroup(name, body).arrange(DOWN, buff=GAP_MD * 1.3)
            card.move_to([0, 0.3, 0])
            self.play(Write(name), run_time=t.fill(0.2))
            self.play(FadeIn(body), run_time=t.fill(0.3))
            t.hold()

    # --------------------------------------------------- 11. file systems

    def file_systems(self):
        with self.beat("filesystem") as t:
            self.section(t, "File systems and metadata", FILES)
            t.hold()

        with self.beat("fs_def") as t:
            body = prose("A file system is how data is organised and found "
                         "in storage.", BODY_SIZE, CHARCOAL, 11.8)
            self.place(body, self.head, buff=GAP_MD * 1.2)
            self.fs_line = body
            self.play(Write(body), run_time=t.fill(0.42))
            t.hold()

        tree = FileTree([(0, "Documents", True), (1, "School", True),
                         (2, "notes.txt", False), (2, "report.docx", False),
                         (1, "photo.jpg", False)])

        with self.beat("file") as t:
            self.place(tree, self.fs_line, buff=GAP_MD * 1.1)
            tree.move_to([-3.4, tree.get_center()[1], 0])
            self.tree = tree
            self.play(FadeIn(tree), run_time=t.fill(0.3))
            self.say(t, "A file holds data: a document, a picture, a video",
                     fraction=0.22)
            t.hold()

        with self.beat("folder") as t:
            self.say(t, "A folder groups files and other folders",
                     fraction=0.4)
            t.hold()

        with self.beat("metadata") as t:
            card = callout(METADATA, width=4.4)
            card.move_to([3.5, tree.get_center()[1], 0])
            head = serif("Metadata", LABEL_SIZE, TERRACOTTA)
            head.next_to(card, UP, buff=GAP_SM * 0.9)
            self.meta = VGroup(card, head)
            self.play(FadeIn(head), run_time=t.fill(0.12))
            self.play(Create(card[0]), FadeIn(card[1]),
                      run_time=t.fill(0.28))
            t.hold()

        with self.beat("papers") as t:
            self.wipe(t)
            self.title(t, "A thousand papers on one desk", fraction=0.1)
            body = prose("Finding the one you want is hard.", BODY_SIZE,
                         CHARCOAL, 11.8)
            self.place(body, self.head, buff=GAP_LG)
            self.papers = body
            self.play(Write(body), run_time=t.fill(0.4))
            t.hold()

        with self.beat("labelled") as t:
            answer = prose("In labelled folders, it is easy.", TITLE_SIZE,
                           SAGE, 12.0)
            self.place(answer, self.papers, buff=GAP_LG * 0.9)
            self.play(Write(answer), run_time=t.fill(0.45))
            t.hold()

    # ---------------------------------------------------- 12. the journey

    def the_journey(self):
        route = Chain(["You type\na website", "Browser", "Operating\nsystem",
                       "Network\ncard", "Server"], width=2.3, height=1.25,
                      gap=0.17)

        with self.beat("journey") as t:
            self.section(t, "From your keyboard to a server", JOURNEY)
            self.place(route, self.head, buff=GAP_LG * 0.9)
            self.journey_route = route
            self.play(Create(route.boxes), Write(route.labels),
                      run_time=t.fill(0.3))
            self.play(Create(route.arrows), run_time=t.fill(0.14))
            t.hold()

        for beat, index, caption in (
                ("you_type", 1, "The browser asks the OS for a network "
                                "connection"),
                ("network_card", 3, "The network card sends the request out"),
                ("server_replies", 4, "The server sends its answer back")):
            with self.beat(beat) as t:
                self.play(*route.light(index), run_time=t.fill(0.14))
                self.say(t, caption, fraction=0.3)
                self.play(*route.settle(index), run_time=t.fill(0.08))
                t.hold()

        with self.beat("back_to_browser") as t:
            self.play(*route.light(2), run_time=t.fill(0.14))
            self.say(t, "The operating system hands the data to the browser",
                     fraction=0.35)
            t.hold()

        with self.beat("on_screen") as t:
            self.play(*route.settle(2), *route.light(1),
                      run_time=t.fill(0.14))
            self.say(t, "and the browser draws the page on your screen",
                     fraction=0.4)
            t.hold()

    # ----------------------------------------------------------- the recap

    def recap(self):
        with self.beat("recap") as t:
            self.wipe(t)
            self.title(t, "What we covered", fraction=0.08)
            lines = VGroup(*[serif(f"·  {text}", MARGIN_SIZE, CHARCOAL)
                             for text in RECAP])
            lines.arrange(DOWN, buff=GAP_SM * 0.78, aligned_edge=LEFT)
            widest = max(line.width for line in lines)
            if widest > FRAME_SAFE:
                raise ValueError(
                    f"A recap line runs {widest:.2f} units. Shorten it.")
            self.place(lines, self.head, buff=GAP_MD * 0.7)
            self.recap_lines = lines
            # Cream on slate, not sage on slate: sage and slate are close
            # enough in tone that the numbers all but vanished when every
            # cell lit at once.
            self.play(*[cell.animate.set_stroke(SLATE)
                        .set_fill(SLATE, opacity=1)
                        for cell in self.strip.cells],
                      *[number.animate.set_color(CREAM)
                        for number in self.strip.numbers],
                      run_time=t.fill(0.12))
            t.hold()

        order = ["recap_kernel", "recap_layers", "recap_accounts",
                 "recap_process", "recap_fcfs", "recap_multi",
                 "recap_threads", "recap_syscalls", "recap_files"]
        for index, beat in enumerate(order):
            with self.beat(beat) as t:
                self.play(FadeIn(self.recap_lines[index]),
                          run_time=t.fill(0.3))
                t.hold()

    # ------------------------------------------------------- the self-check

    def self_check(self):
        with self.beat("pause") as t:
            self.wipe(t)
            self.title(t, "Pause the video and answer these", fraction=0.14)
            t.hold()

        lines = VGroup(*[serif(f"{index + 1}.  {text}", MARGIN_SIZE,
                               CHARCOAL)
                         for index, text in enumerate(QUESTIONS)])
        lines.arrange(DOWN, buff=GAP_SM * 1.1, aligned_edge=LEFT)
        self.place(lines, self.head, buff=GAP_MD * 1.2)

        for index, beat in enumerate(
                ("q1", "q2", "q3", "q4", "q5", "q6", "q7")):
            with self.beat(beat) as t:
                self.play(FadeIn(lines[index]), run_time=t.fill(0.3))
                t.hold()

        with self.beat("close") as t:
            self.wipe(t)
            done = prose("If you can answer these in your own words, you "
                         "have Chapter 1.", TITLE_SIZE, SAGE, 12.0)
            done.move_to([0, 0.4, 0])
            self.play(Write(done), run_time=t.fill(0.4))
            t.hold()

    # --------------------------------------------------------------- helpers

    _beat_name = "(before the first beat)"

    @contextmanager
    def beat(self, name):
        self._beat_name = name
        with super().beat(name) as timer:
            yield timer

    def section(self, t, text, index, fraction=0.14):
        """Open one of the twelve: clear, move the strip, name it."""
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
        if self.side is None:
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
        self.head = self.note = None

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
                    "already on screen. Clear the frame first, or anchor "
                    "the line under the figure.")
