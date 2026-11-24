"""Chapter 7, Algorithm Design and Problem Solving: Cambridge O Level 2210.

Fifteen numbered sections and an opening, every reveal anchored to the
narration by build/beats_ch07.py.

This chapter is the one where the pictures have to do the work, because
every topic in it is a process rather than a fact:

  * ``ControlLoop``-style box rows will not do here. ``ValueRow`` is a
    list with a finger on one item, and that single figure carries three
    sections: linear search walks it, bubble sort swaps along it, and the
    test-data section colours what the range accepts.
  * ``MiniFlow`` draws the grade-A algorithm as a flowchart, branches and
    all, and ``CodeBlock`` draws the same logic as pseudocode. A student
    who has seen both knows they are two notations for one algorithm.
  * ``TraceTable`` fills a row at a time beside the code it is tracing,
    which is the only honest way to show a trace table: the finished
    answer teaches nothing.
  * ``StructureTree`` breaks a library system into parts and then breaks
    one part again.

The reading is a clean synthetic one and is correct throughout. Where a
caption and the audio seem to disagree, the transcriber is what the
beats were anchored to: it heard "structured diagram" for structure
diagram, "grade day" for grade A and "Suda code" for pseudocode.
build/beats_ch07.py lists them.

Timing: timings/cs.algorithms.json
Render: python build/render.py scripts/CH07-algorithms.md \\
    audio/CH07-algorithms.mp3
"""

from contextlib import contextmanager

from manim import (
    Create,
    FadeIn,
    FadeOut,
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
from components.algorithms import (
    AGES,
    FlowShapes,
    MiniFlow,
    StructureTree,
    ValueRow,
)
from components.editorial import columns, fit, numbered, prose
from components.os_core import Chain, callout
from components.os_shape import SortBench, chips, grid
from components.software import CodeBlock
from components.syllabus_map import TopicStrip
from components.trace_table import TraceTable
from scenes.base import SATScene

FRAME_SAFE = 12.6
FLOOR = -3.05
BARE_FLOOR = -3.5

PARTS = ["The life cycle", "Breaking it down", "In, out, stored",
         "What an algorithm is", "Three ways", "Flowchart symbols",
         "One algorithm", "Linear search", "Bubble sort", "Counting",
         "Validation", "Test data", "Trace tables", "Errors", "Recap"]
(PDLC, BREAK, IPOS, ALGO, WAYS, SYMBOLS, PRECISE, SEARCH, SORT, COUNT,
 CHECK, TESTDATA, TRACE, ERRORS, RECAP) = range(15)

AGENDA = ["The life cycle", "Breaking it down",
          "Flowcharts, pseudocode", "Search, sort and test"]

STAGES = ["Analysis", "Design", "Coding", "Testing"]
ANALYSIS_ASKS = ["Inputs", "Processes", "Outputs", "Storage"]
DESIGN_TOOLS = ["Structure diagram", "Flowchart", "Pseudocode",
                "Test plan"]

PAYROLL_ROWS = [
    ("Inputs", "staff number, hours, hourly rate"),
    ("Processes", "gross pay, then the deductions"),
    ("Outputs", "a payslip, and the amount paid"),
    ("Storage", "staff details, past payments"),
]

FOUR_QUESTIONS = [
    "What data enters the system?",
    "What does the system do with it?",
    "What information comes out?",
    "What must be kept for later?",
]

ALGORITHM_STEPS = [
    "Receive the mark.",
    "Compare it with eighty.",
    "Assign the grade.",
    "Output the grade.",
]

WAYS_ROWS = [
    ("Structure diagram", "the hierarchy", "the modules"),
    ("Flowchart", "the flow of control", "seeing the path"),
    ("Pseudocode", "the exact logic", "precision"),
]

# The search, written the way the syllabus writes it. The order of the
# two tests in the WHILE is the point of the section: swap them and the
# algorithm reads past the end of the list.
SEARCH_CODE = [
    "Found <- FALSE",
    "Index <- 1",
    "WHILE Index <= Count AND Found = FALSE DO",
    "    IF List[Index] = Target THEN",
    "        Found <- TRUE",
    "    ENDIF",
    "    Index <- Index + 1",
    "ENDWHILE",
]

NAMES = ["Ravi", "Sara", "Amina", "Joel", "Mei"]
TO_SORT = [7, 3, 5, 2]

COUNT_ROWS = [
    ("Count", "start at 0, add 1 when it matches"),
    ("Total", "start at 0, add each value"),
    ("Maximum", "start at the first value"),
    ("Average", "the total divided by the count"),
]

CHECKS = ["range check", "length check", "type check", "presence check",
          "format check", "check digit"]

TRACE_CODE = [
    "Total <- 0",
    "FOR X <- 2 TO 6 STEP 2",
    "    Total <- Total + X",
    "    OUTPUT Total",
    "NEXT X",
]

ERROR_ROWS = [
    ("Syntax", "the notation itself is wrong"),
    ("Logic", "it runs, and the answer is wrong"),
    ("Boundary", "a loop starts or stops one out"),
    ("Initialization", "a variable starts at the wrong value"),
    ("Update", "a counter or index changes wrongly"),
    ("Condition", "the comparison is the wrong one"),
]

RECAP_CARDS = [
    ("The life cycle", [
        "Analysis finds the requirements.",
        "Design plans the solution.",
        "Coding writes it.",
        "Testing compares actual with expected.",
    ]),
    ("Breaking it down", [
        "Abstraction drops what does not matter.",
        "Decomposition splits what is left.",
        "Structure diagram, flowchart, pseudocode.",
    ]),
    ("The standard methods", [
        "Linear search, bubble sort, count, total, max, min.",
        "Validation: does the data follow the rules?",
        "Verification: was it copied correctly?",
    ]),
    ("Testing and tracing", [
        "Normal, abnormal, extreme and boundary data.",
        "A trace table finds the step that went wrong.",
    ]),
]

EXAM_RULES = [
    "A stage: what happens, and what it produces.",
    "An algorithm: every instruction, in order.",
    "Test data: find the range, then pick values.",
    "Validation or verification: which question?",
    "A trace: update only when the code does.",
]

ASK_YOURSELF = [
    "Name the four stages of the life cycle.",
    "What does abstraction remove?",
    "Which flowchart symbol holds a condition?",
    "Do the first pass of a bubble sort on 7, 3, 5, 2.",
    "Why is a maximum not initialized to zero?",
    "For ages 12 to 18, name one boundary value.",
    "Which error stops a loop one step early?",
]


class Algorithms(SATScene):
    scene_id = "cs.algorithms"

    def construct(self):
        self.margin = mono("Algorithms · Chapter 7", MARGIN_SIZE)
        self.margin.to_corner(UP + LEFT, buff=GAP_SM)
        self.add(self.margin)

        # 0.56, not 0.5: at 0.5 the two-digit numbers are scaled down
        # to 27px, under the floor.
        self.strip = TopicStrip(len(PARTS), lit=SLATE, side=0.56)
        self.strip.to_edge(DOWN, buff=GAP_SM * 0.5)

        self.keep = [self.margin]
        self.floor = BARE_FLOOR
        self.head = None
        self.note = None
        self.side = None

        self.opening()
        self.life_cycle()
        self.breaking_down()
        self.in_out_stored()
        self.what_an_algorithm_is()
        self.three_ways()
        self.flowchart_symbols()
        self.one_algorithm()
        self.linear_search()
        self.bubble_sort()
        self.counting()
        self.validation()
        self.test_data()
        self.trace_tables()
        self.errors()
        self.recap()

    # --------------------------------------------------------- opening

    def opening(self):
        with self.beat("open") as t:
            chapter = serif("Chapter 7", LABEL_SIZE, SLATE)
            title = fit(serif("Algorithm Design and Problem Solving",
                              DISPLAY_SIZE, CHARCOAL))
            board = prose("Cambridge O Level Computer Science 2210",
                          LABEL_SIZE, GREY)
            card = VGroup(chapter, title, board).arrange(DOWN, buff=GAP_MD)
            card.move_to(ORIGIN)
            self.play(FadeIn(chapter), run_time=t.fill(0.2))
            self.play(Write(title), run_time=t.fill(0.4))
            self.board = board
            t.hold()

        with self.beat("turning") as t:
            self.play(FadeIn(self.board), run_time=t.fill(0.3))
            t.hold()

        with self.beat("cycle_promise") as t:
            self.wipe(t)
            self.title(t, "What this chapter covers", fraction=0.12)
            plan, items = grid(AGENDA, columns=2, size=LABEL_SIZE,
                               h_gap=GAP_MD * 1.2, v_gap=GAP_SM * 1.8)
            self.place(plan, self.head, buff=GAP_LG)
            self.plan_items = items
            self.play(FadeIn(items[0]), run_time=t.fill(0.35))
            t.hold()

        with self.beat("represent") as t:
            self.play(FadeIn(self.plan_items[1]),
                      FadeIn(self.plan_items[2]), run_time=t.fill(0.4))
            t.hold()

        with self.beat("also_testing") as t:
            self.play(FadeIn(self.plan_items[3]), run_time=t.fill(0.4))
            t.hold()

        with self.beat("precision") as t:
            self.wipe(t)
            self.title(t, "One habit above the rest", fraction=0.12)
            word = fit(serif("Precision", DISPLAY_SIZE, TERRACOTTA))
            self.place(word, self.head, buff=GAP_LG)
            self.word = word
            self.play(Write(word), run_time=t.fill(0.4))
            t.hold()

        with self.beat("without_guessing") as t:
            line = prose("Clear enough that a person, or a computer, can "
                         "follow it without guessing.", BODY_SIZE, CHARCOAL,
                         11.4)
            self.place(line, self.word, buff=GAP_LG * 0.8)
            self.play(FadeIn(line), run_time=t.fill(0.45))
            t.hold()

    # ------------------------------------------------- 1. the life cycle

    def life_cycle(self):
        chain = Chain(STAGES, width=2.7, height=1.1)

        with self.beat("pdlc_open") as t:
            self.section(t, "The development life cycle", PDLC)
            t.hold()

        with self.beat("four_stages") as t:
            self.place(chain, self.head, buff=GAP_LG * 0.9)
            self.chain = chain
            self.play(Create(chain.boxes), FadeIn(chain.labels),
                      Create(chain.arrows), run_time=t.fill(0.4))
            t.hold()

        with self.beat("analysis") as t:
            self.play(*chain.light(0), run_time=t.fill(0.3))
            self.say(t, "what problem is this, and what must it do?",
                     fraction=0.3)
            t.hold()

        with self.beat("analysis_ipos") as t:
            asks, each = chips(ANALYSIS_ASKS, size=LABEL_SIZE, rows=1)
            self.place(asks, chain, buff=GAP_LG * 0.8)
            self.asks = asks
            self.play(FadeIn(asks), run_time=t.fill(0.4))
            t.hold()

        with self.beat("requirements") as t:
            self.say(t, "and it ends in a clear set of requirements",
                     fraction=0.4)
            t.hold()

        with self.beat("design") as t:
            self.play(*chain.settle(0), *chain.light(1),
                      FadeOut(self.asks), run_time=t.fill(0.3))
            t.hold()

        with self.beat("design_tools") as t:
            tools, each = chips(DESIGN_TOOLS, size=LABEL_SIZE, rows=2)
            self.place(tools, chain, buff=GAP_LG * 0.8)
            self.tools = tools
            self.play(FadeIn(tools), run_time=t.fill(0.4))
            t.hold()

        with self.beat("design_detail") as t:
            self.say(t, "detailed enough to code from", fraction=0.4)
            t.hold()

        with self.beat("coding") as t:
            self.play(*chain.settle(1), *chain.light(2),
                      FadeOut(self.tools), run_time=t.fill(0.35))
            t.hold()

        with self.beat("code_checked") as t:
            self.say(t, "the design becomes a program, and is checked",
                     fraction=0.4)
            t.hold()

        with self.beat("testing") as t:
            self.play(*chain.settle(2), *chain.light(3),
                      run_time=t.fill(0.35))
            t.hold()

        with self.beat("compare_results") as t:
            self.say(t, "actual results against expected results",
                     fraction=0.4)
            t.hold()

        with self.beat("connected") as t:
            self.wipe(t)
            self.title(t, "Not a straight line", fraction=0.12)
            t.hold()

        with self.beat("not_wait") as t:
            line = prose("Testing does not wait for the last line of code.",
                         BODY_SIZE, CHARCOAL, 11.4)
            self.place(line, self.head, buff=GAP_LG * 0.9)
            self.first_line = line
            self.play(FadeIn(line), run_time=t.fill(0.4))
            t.hold()

        with self.beat("test_parts") as t:
            line = prose("Design a part, code it, test it, and go round "
                         "again.", BODY_SIZE, CHARCOAL, 11.4)
            self.place(line, self.first_line, buff=GAP_MD * 1.3)
            self.second_line = line
            self.play(FadeIn(line), run_time=t.fill(0.4))
            t.hold()

        with self.beat("iterative") as t:
            named = fit(serif("iterative development", TITLE_SIZE,
                              TERRACOTTA))
            self.place(named, self.second_line, buff=GAP_LG * 0.8)
            self.play(Write(named), run_time=t.fill(0.45))
            t.hold()

    # ------------------------------------ 2. abstraction and decomposition

    def breaking_down(self):
        with self.beat("break_open") as t:
            self.section(t, "Making a big problem smaller", BREAK)
            t.hold()

        with self.beat("two_techniques") as t:
            pair, each = chips(["Abstraction", "Decomposition"],
                               size=LABEL_SIZE, rows=1)
            self.place(pair, self.head, buff=GAP_LG)
            self.play(FadeIn(pair), run_time=t.fill(0.4))
            t.hold()

        bench = None
        with self.beat("abstraction_is") as t:
            self.wipe(t)
            self.title(t, "Abstraction: drop what does not matter",
                       fraction=0.14)
            bench = SortBench("Keep", "Leave out")
            bench.next_to(self.head, DOWN, buff=GAP_MD)
            self.bench = bench
            self.play(Write(bench.heads[0]), Write(bench.heads[1]),
                      Create(bench.rules), run_time=t.fill(0.35))
            t.hold()

        with self.beat("library_image") as t:
            self.say(t, "a school library, and the job of issuing a book",
                     fraction=0.4)
            t.hold()

        with self.beat("walls") as t:
            self.play(FadeIn(bench.item(1, "the colour of the walls")),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("keep_these") as t:
            self.play(FadeIn(bench.item(0, "the book")),
                      FadeIn(bench.item(0, "the borrower")),
                      FadeIn(bench.item(0, "the issue date")),
                      run_time=t.fill(0.45))
            t.hold()

        tree = StructureTree()
        with self.beat("decomposition_is") as t:
            self.wipe(t)
            self.title(t, "Decomposition: split what is left",
                       fraction=0.14)
            self.tree = tree
            self.play(Create(tree.root_box), FadeIn(tree.root_label),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("four_parts") as t:
            self.play(Create(tree.children), FadeIn(tree.child_labels),
                      Create(tree.trunks), run_time=t.fill(0.45))
            t.hold()

        with self.beat("divided_again") as t:
            self.play(*tree.light(tree.parent_index), run_time=t.fill(0.4))
            t.hold()

        with self.beat("book_tasks") as t:
            self.play(Create(tree.branches), Create(tree.leaves),
                      FadeIn(tree.leaf_labels), run_time=t.fill(0.45))
            t.hold()

        with self.beat("easier") as t:
            self.say(t, "easier to understand, to design, and to test",
                     fraction=0.4)
            t.hold()

        with self.beat("different_people") as t:
            self.say(t, "and different people can take different parts",
                     fraction=0.4)
            t.hold()

        with self.beat("must_fit") as t:
            self.play(*tree.settle(tree.parent_index),
                      run_time=t.fill(0.25))
            self.say(t, "but the parts have to agree with each other",
                     fraction=0.3, color=TERRACOTTA)
            t.hold()

        with self.beat("overdue") as t:
            self.say(t, "books and fines must record an overdue return "
                        "the same way", fraction=0.4)
            t.hold()

    # --------------------------------- 3. inputs, processes, outputs, storage

    def in_out_stored(self):
        with self.beat("ipos_open") as t:
            self.section(t, "In, out, and kept", IPOS)
            t.hold()

        with self.beat("payroll") as t:
            table, cells, heads = columns(["Part", "In a payroll system"],
                                          PAYROLL_ROWS, size=LABEL_SIZE,
                                          row_gap=GAP_SM * 1.4)
            self.place(table, self.head, buff=GAP_MD * 1.4)
            self.rows = cells
            self.play(FadeIn(VGroup(*heads)), Create(table.rule),
                      run_time=t.fill(0.35))
            t.hold()

        for index, name in enumerate(["inputs", "processes", "outputs",
                                      "storage"]):
            with self.beat(name) as t:
                self.play(FadeIn(VGroup(*self.rows[index])),
                          run_time=t.fill(0.4))
                t.hold()

        with self.beat("four_questions") as t:
            self.wipe(t)
            self.title(t, "Four questions, every time", fraction=0.12)
            asked, rows = numbered(FOUR_QUESTIONS, size=BODY_SIZE,
                                   gap=GAP_SM * 1.5)
            self.place(asked, self.head, buff=GAP_LG * 0.9)
            self.asked = rows
            self.play(FadeIn(rows[0]), run_time=t.fill(0.4))
            t.hold()

        for index, name in enumerate(["what_does", "comes_out", "kept"]):
            with self.beat(name) as t:
                self.play(FadeIn(self.asked[index + 1]),
                          run_time=t.fill(0.4))
                t.hold()

        with self.beat("define_first") as t:
            self.say(t, "answer these before writing a single step",
                     fraction=0.4)
            t.hold()

    # ------------------------------------------ 4. what an algorithm is

    def what_an_algorithm_is(self):
        with self.beat("algo_open") as t:
            self.section(t, "Finite, and precise", ALGO)
            t.hold()

        with self.beat("finite") as t:
            line = prose("Finite: it stops.", TITLE_SIZE, CHARCOAL)
            self.place(line, self.head, buff=GAP_LG * 0.9)
            self.finite = line
            self.play(Write(line), run_time=t.fill(0.4))
            t.hold()

        with self.beat("precise_means") as t:
            line = prose("Precise: each step means one thing.", TITLE_SIZE,
                         CHARCOAL)
            self.place(line, self.finite, buff=GAP_MD * 1.4)
            self.precise = line
            self.play(Write(line), run_time=t.fill(0.4))
            t.hold()

        with self.beat("describes_how") as t:
            line = prose("It says how to get the result.", BODY_SIZE, SAGE)
            self.place(line, self.precise, buff=GAP_LG * 0.8)
            self.play(FadeIn(line), run_time=t.fill(0.4))
            t.hold()

        with self.beat("not_repeat") as t:
            self.say(t, "not the question again in other words",
                     fraction=0.4)
            t.hold()

        with self.beat("grade_example") as t:
            self.wipe(t)
            self.title(t, "Grade A at eighty", fraction=0.12)
            t.hold()

        with self.beat("needs_to") as t:
            steps, rows = numbered(ALGORITHM_STEPS, size=BODY_SIZE,
                                   gap=GAP_SM * 1.5)
            self.place(steps, self.head, buff=GAP_LG * 0.9)
            self.play(FadeIn(steps), run_time=t.fill(0.45))
            t.hold()

        bench = None
        with self.beat("specific") as t:
            self.wipe(t)
            self.title(t, "The condition decides the mark", fraction=0.14)
            bench = SortBench("Too vague", "Exact")
            bench.next_to(self.head, DOWN, buff=GAP_MD)
            self.vague = bench
            self.play(Write(bench.heads[0]), Write(bench.heads[1]),
                      Create(bench.rules), run_time=t.fill(0.35))
            t.hold()

        with self.beat("not_precise") as t:
            self.play(FadeIn(bench.item(0, "the mark is high")),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("exact") as t:
            self.play(FadeIn(bench.item(1, "Mark >= 80", color=SAGE)),
                      run_time=t.fill(0.45))
            t.hold()

    # ------------------------------------------------- 5. three ways

    def three_ways(self):
        with self.beat("ways_open") as t:
            self.section(t, "Three ways to write one", WAYS)
            table, cells, heads = columns(
                ["", "Shows", "Best for"], WAYS_ROWS, size=LABEL_SIZE,
                row_gap=GAP_SM * 1.4)
            self.place(table, self.head, buff=GAP_MD * 1.5)
            self.ways = cells
            self.play(FadeIn(VGroup(*heads)), Create(table.rule),
                      run_time=t.fill(0.3))
            t.hold()

        with self.beat("structure_is") as t:
            self.play(FadeIn(self.ways[0][0]), FadeIn(self.ways[0][1]),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("structure_use") as t:
            self.play(FadeIn(self.ways[0][2]), run_time=t.fill(0.4))
            t.hold()

        with self.beat("structure_not") as t:
            self.say(t, "it does not show the order of decisions and loops",
                     fraction=0.4)
            t.hold()

        with self.beat("flow_is") as t:
            self.play(FadeIn(self.ways[1][0]), FadeIn(self.ways[1][1]),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("flow_shows") as t:
            self.play(FadeIn(self.ways[1][2]), run_time=t.fill(0.4))
            t.hold()

        with self.beat("flow_limit") as t:
            self.say(t, "a big one is hard to edit", fraction=0.4)
            t.hold()

        with self.beat("pseudo_is") as t:
            self.play(FadeIn(self.ways[2][0]), FadeIn(self.ways[2][1]),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("pseudo_conventions") as t:
            self.say(t, "no one language, but the conventions are fixed",
                     fraction=0.4)
            t.hold()

        with self.beat("pseudo_useful") as t:
            self.play(FadeIn(self.ways[2][2]), run_time=t.fill(0.4))
            t.hold()

    # ------------------------------------------- 6. the flowchart symbols

    def flowchart_symbols(self):
        shapes = FlowShapes()

        with self.beat("symbols_open") as t:
            self.section(t, "The symbols, and what each one means",
                         SYMBOLS)
            self.place(shapes, self.head, buff=GAP_MD)
            self.shapes = shapes
            t.hold()

        names = ["terminator", "process", "io", "decision", "subroutine",
                 "flowlines"]
        for index, name in enumerate(names):
            with self.beat(name) as t:
                self.play(Create(shapes.shapes[index]),
                          FadeIn(shapes.labels[index]),
                          run_time=t.fill(0.3))
                self.say(t, shapes.USES[index], fraction=0.3)
                t.hold()

        with self.beat("correct_symbol") as t:
            self.say(t, "the shape is part of the answer", fraction=0.4,
                     color=TERRACOTTA)
            t.hold()

        with self.beat("connect") as t:
            self.say(t, "and the arrows say which way it runs",
                     fraction=0.4)
            t.hold()

    # ------------------------------------------- 7. one algorithm, drawn

    def one_algorithm(self):
        flow = MiniFlow()

        with self.beat("precise_open") as t:
            self.section(t, "One algorithm, drawn", PRECISE)
            self.flow = flow
            t.hold()

        # No commentary under this figure: it reaches y -2.83 and the band
        # starts at -2.48, so a line there would be printed over the STOP
        # terminator. The narration carries these beats on its own.
        with self.beat("suppose") as t:
            self.play(Create(flow.start), FadeIn(flow.labels[0]),
                      run_time=t.fill(0.35))
            t.hold()

        with self.beat("read_mark") as t:
            self.play(Create(flow.arrows[0]), Create(flow.read),
                      FadeIn(flow.labels[1]), run_time=t.fill(0.4))
            t.hold()

        with self.beat("test_mark") as t:
            self.play(Create(flow.arrows[1]), Create(flow.decide),
                      FadeIn(flow.labels[2]), run_time=t.fill(0.4))
            t.hold()

        with self.beat("assign_a") as t:
            self.play(Create(flow.yes_path), FadeIn(flow.yes),
                      Create(flow.assign), FadeIn(flow.assign_label),
                      run_time=t.fill(0.45))
            t.hold()

        with self.beat("otherwise") as t:
            self.play(Create(flow.no_path), FadeIn(flow.no),
                      Create(flow.other), FadeIn(flow.other_label),
                      run_time=t.fill(0.45))
            t.hold()

        with self.beat("output_grade") as t:
            self.play(Create(flow.rejoin), Create(flow.output),
                      FadeIn(flow.labels[3]), run_time=t.fill(0.35))
            self.play(Create(flow.arrows[2]), Create(flow.stop),
                      FadeIn(flow.labels[4]), run_time=t.fill(0.3))
            t.hold()

        with self.beat("notice") as t:
            self.play(flow.decide.animate.set_stroke(TERRACOTTA)
                      .set_fill(TERRACOTTA, opacity=0.16),
                      flow.labels[2].animate.set_color(TERRACOTTA),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("not_enough") as t:
            self.wipe(t)
            self.title(t, "Exact, or not a condition at all",
                       fraction=0.14)
            vague = prose("“the mark is high”", TITLE_SIZE, GREY)
            self.place(vague, self.head, buff=GAP_LG)
            self.vague_card = vague
            self.play(FadeIn(vague), run_time=t.fill(0.4))
            t.hold()

        with self.beat("unambiguous") as t:
            exact = mono("IF Mark >= 80 THEN", TITLE_SIZE, TERRACOTTA)
            exact = fit(exact)
            self.place(exact, self.vague_card, buff=GAP_LG * 0.9)
            self.exact_card = exact
            self.play(Write(exact), run_time=t.fill(0.45))
            t.hold()

        with self.beat("both") as t:
            self.say(t, "selection and repetition both need this",
                     fraction=0.45)
            t.hold()

    # ---------------------------------------------------- 8. linear search

    def linear_search(self):
        row = ValueRow(NAMES, width=2.3)

        with self.beat("search_open") as t:
            self.section(t, "Linear search", SEARCH)
            t.hold()

        with self.beat("search_is") as t:
            self.place(row, self.head, buff=GAP_LG)
            row.pointer.move_to([row.at(0),
                                 row.get_bottom()[1] - 0.62, 0])
            self.row = row
            self.play(Create(row.boxes), FadeIn(row.texts),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("names_example") as t:
            target = serif("looking for: Amina", LABEL_SIZE, TERRACOTTA)
            self.place(target, row, buff=GAP_LG * 0.9)
            self.target = target
            self.play(FadeIn(target), run_time=t.fill(0.4))
            t.hold()

        with self.beat("start_first") as t:
            self.play(FadeIn(row.pointer), *row.light(0),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("if_matches") as t:
            self.say(t, "no: move on", fraction=0.4, y=-2.35)
            t.hold()

        with self.beat("if_not") as t:
            self.play(*row.settle(0), row.point_to(1), *row.light(1),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("stops") as t:
            self.play(*row.settle(1), row.point_to(2),
                      run_time=t.fill(0.25))
            self.play(*row.lock(2), run_time=t.fill(0.25))
            self.say(t, "found, and the search stops", fraction=0.3,
                     y=-2.35)
            t.hold()

        with self.beat("unsorted") as t:
            self.say(t, "it does not need sorted data", fraction=0.4,
                     y=-2.35)
            t.hold()

        with self.beat("limitation") as t:
            self.say(t, "but it may have to look at every item",
                     fraction=0.4, y=-2.35)
            t.hold()

        # Tighter leading than the default: eight lines at the usual
        # spacing reach y -2.54 and the commentary band starts at
        # -2.53, and two of these beats are commentary.
        code = CodeBlock(SEARCH_CODE, size=MARGIN_SIZE,
                         leading=GAP_SM * 0.9)
        with self.beat("found_var") as t:
            self.wipe(t)
            self.title(t, "The same search, in pseudocode", fraction=0.14)
            self.place(code, self.head, buff=GAP_MD)
            self.code = code
            self.play(FadeIn(code), run_time=t.fill(0.4))
            t.hold()

        with self.beat("found_false") as t:
            self.play(*code.light(0), run_time=t.fill(0.4))
            t.hold()

        with self.beat("while_loop") as t:
            self.play(*code.light(2), run_time=t.fill(0.4))
            t.hold()

        with self.beat("found_true") as t:
            self.play(*code.light(4), run_time=t.fill(0.4))
            t.hold()

        with self.beat("not_present") as t:
            self.play(*code.light(7), run_time=t.fill(0.4))
            t.hold()

        with self.beat("order_matters") as t:
            self.play(*code.light(2), run_time=t.fill(0.25))
            self.say(t, "the order of the two tests matters", fraction=0.3,
                     color=TERRACOTTA)
            t.hold()

        with self.beat("beyond_end") as t:
            self.say(t, "check the index first, or you read past the end",
                     fraction=0.45)
            t.hold()

    # ----------------------------------------------------- 9. bubble sort

    def bubble_sort(self):
        row = ValueRow(TO_SORT)

        with self.beat("sort_open") as t:
            self.section(t, "Bubble sort", SORT)
            t.hold()

        with self.beat("sort_is") as t:
            self.say(t, "compare neighbours, swap the ones out of order",
                     fraction=0.45)
            t.hold()

        with self.beat("lets_sort") as t:
            self.place(row, self.head, buff=GAP_LG)
            self.sorting = row
            self.play(Create(row.boxes), FadeIn(row.texts),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("seven_three") as t:
            self.play(*row.light(0), *row.light(1), run_time=t.fill(0.4))
            t.hold()

        with self.beat("swap1") as t:
            self.play(*row.swap(0), run_time=t.fill(0.45))
            t.hold()

        with self.beat("list_now") as t:
            self.play(*row.settle(0), *row.settle(1), run_time=t.fill(0.3))
            self.say(t, "3  7  5  2", fraction=0.3)
            t.hold()

        with self.beat("seven_five") as t:
            self.play(*row.light(1), *row.light(2), run_time=t.fill(0.4))
            t.hold()

        with self.beat("swap2") as t:
            self.play(*row.swap(1), run_time=t.fill(0.3))
            self.say(t, "3  5  7  2", fraction=0.3)
            t.hold()

        with self.beat("seven_two") as t:
            self.play(*row.settle(1), *row.light(2), *row.light(3),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("swap3") as t:
            # The caption from the last beat reads the list as it was
            # before this swap, and this swap makes it false while it
            # is still on screen. A caption a figure has moved out from
            # under is not something any check can see.
            self.drop_note(t, fraction=0.06)
            self.play(*row.swap(2), run_time=t.fill(0.4))
            t.hold()

        with self.beat("after_pass") as t:
            self.play(*row.settle(2), *row.lock(3), run_time=t.fill(0.3))
            self.say(t, "3  5  2  7, and the largest is home",
                     fraction=0.3, color=SAGE)
            t.hold()

        with self.beat("next_pass") as t:
            self.say(t, "pass two", fraction=0.45)
            t.hold()

        with self.beat("three_five") as t:
            self.play(*row.light(0), *row.light(1), run_time=t.fill(0.3))
            self.say(t, "3 and 5 are already in order", fraction=0.3)
            t.hold()

        with self.beat("five_two") as t:
            self.play(*row.settle(0), *row.light(1), *row.light(2),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("becomes") as t:
            self.play(*row.swap(1), run_time=t.fill(0.3))
            self.say(t, "3  2  5  7", fraction=0.3)
            t.hold()

        with self.beat("next_comparison") as t:
            self.play(*row.settle(1), *row.settle(2), run_time=t.fill(0.4))
            t.hold()

        with self.beat("continues") as t:
            self.say(t, "and it keeps passing until nothing swaps",
                     fraction=0.45)
            t.hold()

        with self.beat("exam_passes") as t:
            self.wipe(t)
            self.title(t, "In the exam", fraction=0.12)
            t.hold()

        with self.beat("show_each") as t:
            line = prose("Show every comparison and every swap, in order. "
                         "Never jump to the sorted list.", BODY_SIZE,
                         CHARCOAL, 11.4)
            self.place(line, self.head, buff=GAP_LG)
            self.play(Write(line), run_time=t.fill(0.5))
            t.hold()

    # ------------------------------- 10. counting, totalling, max, average

    def counting(self):
        with self.beat("count_open") as t:
            self.section(t, "Count, total, largest, average", COUNT)
            table, cells, heads = columns(["Job", "How it works"],
                                          COUNT_ROWS, size=LABEL_SIZE,
                                          row_gap=GAP_SM * 1.4)
            self.place(table, self.head, buff=GAP_MD * 1.4)
            self.jobs = cells
            self.play(FadeIn(VGroup(*heads)), Create(table.rule),
                      run_time=t.fill(0.3))
            t.hold()

        with self.beat("counter") as t:
            self.play(FadeIn(self.jobs[0][0]), run_time=t.fill(0.4))
            t.hold()

        with self.beat("increase") as t:
            self.play(FadeIn(self.jobs[0][1]), run_time=t.fill(0.4))
            t.hold()

        with self.beat("above_fifty") as t:
            self.say(t, "how many marks are above fifty?", fraction=0.4)
            t.hold()

        with self.beat("check_each") as t:
            self.say(t, "check each one, add one when it qualifies",
                     fraction=0.4)
            t.hold()

        with self.beat("total_zero") as t:
            self.play(FadeIn(VGroup(*self.jobs[1])), run_time=t.fill(0.4))
            t.hold()

        with self.beat("add_value") as t:
            self.say(t, "a total adds the value, not one", fraction=0.4)
            t.hold()

        with self.beat("max_init") as t:
            self.play(FadeIn(VGroup(*self.jobs[2])), run_time=t.fill(0.4))
            t.hold()

        with self.beat("compare_rest") as t:
            self.say(t, "then look at each remaining value", fraction=0.4)
            t.hold()

        with self.beat("replace_max") as t:
            self.say(t, "bigger than the maximum: replace it",
                     fraction=0.4)
            t.hold()

        with self.beat("replace_min") as t:
            self.say(t, "smaller than the minimum: replace that",
                     fraction=0.4)
            t.hold()

        with self.beat("not_zero") as t:
            self.wipe(t)
            self.title(t, "Never start a maximum at zero", fraction=0.14,
                       color=TERRACOTTA)
            t.hold()

        with self.beat("negatives") as t:
            line = prose("If every value could be negative, zero is not a "
                         "value in the data.", BODY_SIZE, CHARCOAL, 11.4)
            self.place(line, self.head, buff=GAP_LG)
            self.negatives = line
            self.play(Write(line), run_time=t.fill(0.5))
            t.hold()

        with self.beat("average") as t:
            line = prose("An average needs both: a total, and a count.",
                         BODY_SIZE, CHARCOAL, 11.4)
            self.place(line, self.negatives, buff=GAP_LG * 0.8)
            self.average = line
            self.play(FadeIn(line), run_time=t.fill(0.4))
            t.hold()

        with self.beat("divide") as t:
            line = mono("Average <- Total / Count", TITLE_SIZE, SAGE)
            self.place(fit(line), self.average, buff=GAP_MD * 1.3)
            self.play(Write(line), run_time=t.fill(0.45))
            t.hold()

    # -------------------------------------- 11. validation and verification

    def validation(self):
        bench = SortBench("Validation", "Verification")

        with self.beat("check_open") as t:
            self.section(t, "Two different checks", CHECK)
            bench.next_to(self.head, DOWN, buff=GAP_MD)
            self.checks = bench
            self.play(Write(bench.heads[0]), Write(bench.heads[1]),
                      Create(bench.rules), run_time=t.fill(0.35))
            t.hold()

        with self.beat("validation_is") as t:
            self.play(FadeIn(bench.caption(0, "does it follow the rules?")),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("not_true") as t:
            self.say(t, "which is not the same as being true",
                     fraction=0.4)
            t.hold()

        with self.beat("range_check") as t:
            # The band line goes before the items arrive: six of them
            # reach y -2.27 and the line would still be sitting there.
            self.drop_note(t)
            self.play(FadeIn(bench.item(0, CHECKS[0])),
                      run_time=t.fill(0.3))
            t.hold()

        with self.beat("range_example") as t:
            self.say(t, "a mark between 0 and 100", fraction=0.4)
            t.hold()

        with self.beat("length_check") as t:
            self.play(FadeIn(bench.item(0, CHECKS[1])),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("password") as t:
            self.say(t, "a password of at least eight characters",
                     fraction=0.4)
            t.hold()

        with self.beat("type_check") as t:
            # And again here. The asides either side of the first two
            # items are fine; from the third item down the bench is
            # into the band, so the band has to be empty from here on.
            self.drop_note(t)
            self.play(FadeIn(bench.item(0, CHECKS[2])),
                      run_time=t.fill(0.3))
            t.hold()

        with self.beat("presence_check") as t:
            self.play(FadeIn(bench.item(0, CHECKS[3])),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("format_check") as t:
            self.play(FadeIn(bench.item(0, CHECKS[4])),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("check_digit") as t:
            self.play(FadeIn(bench.item(0, CHECKS[5])),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("verification_is") as t:
            self.play(FadeIn(bench.caption(1, "was it copied correctly?")),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("visual") as t:
            self.play(FadeIn(bench.item(1, "read it against the source")),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("double_entry") as t:
            self.play(FadeIn(bench.item(1, "type it twice, compare")),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("key_distinction") as t:
            self.wipe(t)
            self.title(t, "Two different questions", fraction=0.12)
            t.hold()

        with self.beat("validation_asks") as t:
            first = prose("Validation: does this data follow the rules?",
                          BODY_SIZE, CHARCOAL, 11.4)
            self.place(first, self.head, buff=GAP_LG * 0.9)
            self.first_ask = first
            self.play(FadeIn(first), run_time=t.fill(0.45))
            t.hold()

        with self.beat("verification_asks") as t:
            second = prose("Verification: was this data copied correctly?",
                           BODY_SIZE, CHARCOAL, 11.4)
            self.place(second, self.first_ask, buff=GAP_MD * 1.3)
            self.second_ask = second
            self.play(FadeIn(second), run_time=t.fill(0.45))
            t.hold()

        with self.beat("dob") as t:
            line = prose("A date of birth can pass a format check and "
                         "still be the wrong date.", BODY_SIZE, TERRACOTTA,
                         11.4)
            self.place(line, self.second_ask, buff=GAP_LG * 0.8)
            self.play(Write(line), run_time=t.fill(0.5))
            t.hold()

    # ------------------------------------------------------ 12. test data

    def test_data(self):
        row = ValueRow(AGES, width=1.2)

        with self.beat("test_open") as t:
            self.section(t, "Four kinds of test data", TESTDATA)
            self.place(row, self.head, buff=GAP_LG)
            self.ages = row
            self.play(Create(row.boxes), FadeIn(row.texts),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("normal") as t:
            self.say(t, "normal: an ordinary value the program accepts",
                     fraction=0.4)
            t.hold()

        with self.beat("ages_example") as t:
            self.play(*row.light(3), run_time=t.fill(0.4))
            t.hold()

        with self.beat("abnormal") as t:
            self.play(*row.settle(3), run_time=t.fill(0.2))
            self.say(t, "abnormal: it should be refused", fraction=0.3)
            t.hold()

        with self.beat("outside") as t:
            self.play(*row.light(0), *row.light(8), run_time=t.fill(0.4))
            t.hold()

        with self.beat("extreme") as t:
            self.play(*row.settle(0), *row.settle(8), run_time=t.fill(0.2))
            self.say(t, "extreme: the edge of what is allowed",
                     fraction=0.3)
            t.hold()

        with self.beat("extreme_values") as t:
            self.play(*row.light(1), *row.light(7), run_time=t.fill(0.4))
            t.hold()

        with self.beat("boundary") as t:
            self.say(t, "boundary: the edge, and the step past it",
                     fraction=0.4)
            t.hold()

        with self.beat("boundary_values") as t:
            self.play(*row.lock(1), *row.lock(7), *row.light(0),
                      *row.light(8), run_time=t.fill(0.45))
            t.hold()

        with self.beat("accepted_limits") as t:
            self.say(t, "12 and 18 are accepted", fraction=0.4, color=SAGE)
            t.hold()

        with self.beat("just_outside") as t:
            self.say(t, "11 and 19 are refused", fraction=0.4,
                     color=TERRACOTTA)
            t.hold()

        with self.beat("remember_diff") as t:
            self.wipe(t)
            self.title(t, "Extreme, or boundary?", fraction=0.12)
            t.hold()

        with self.beat("extreme_acceptable") as t:
            first = prose("Extreme values are accepted. They sit on the "
                          "edge.", BODY_SIZE, SAGE, 11.4)
            self.place(first, self.head, buff=GAP_LG * 0.9)
            self.extreme_line = first
            self.play(FadeIn(first), run_time=t.fill(0.45))
            t.hold()

        with self.beat("beyond_edges") as t:
            second = prose("Boundary testing adds the first value past "
                           "each edge.", BODY_SIZE, CHARCOAL, 11.4)
            self.place(second, self.extreme_line, buff=GAP_MD * 1.3)
            self.boundary_line = second
            self.play(FadeIn(second), run_time=t.fill(0.45))
            t.hold()

        with self.beat("cover_cases") as t:
            self.say(t, "good test data covers all four", fraction=0.4)
            t.hold()

        with self.beat("only_normal") as t:
            self.say(t, "normal data alone hides the mistakes at the "
                        "limits", fraction=0.45, color=TERRACOTTA)
            t.hold()

    # ---------------------------------------------------- 13. trace tables

    def trace_tables(self):
        with self.beat("trace_open") as t:
            self.section(t, "A trace table", TRACE)
            t.hold()

        with self.beat("records") as t:
            self.say(t, "every variable, every condition, every output",
                     fraction=0.45)
            t.hold()

        code = CodeBlock(TRACE_CODE, size=MARGIN_SIZE)
        table = TraceTable(["X", "Total", "OUTPUT"],
                           [(2, 2, 2), (4, 6, 6), (6, 12, 12)],
                           start=("-", 0, "-"), size=MARGIN_SIZE,
                           col_width=1.5)

        with self.beat("lets_trace") as t:
            code.move_to([-3.6, 0.2, 0])
            self.code = code
            self.play(FadeIn(code), run_time=t.fill(0.4))
            t.hold()

        with self.beat("total_starts") as t:
            table.move_to([3.6, 0.2, 0])
            table.hidden()
            self.table = table
            self.play(Write(table.head), Create(table.rule),
                      run_time=t.fill(0.25))
            self.play(*table.step(0), run_time=t.fill(0.25))
            t.hold()

        with self.beat("each_time") as t:
            self.play(*code.light(2), run_time=t.fill(0.4))
            t.hold()

        for index, name in enumerate(["x_two", "x_four", "x_six"]):
            with self.beat(name) as t:
                self.play(*table.step(index + 1), run_time=t.fill(0.45))
                t.hold()

        with self.beat("outputs_are") as t:
            self.play(*code.light(3), run_time=t.fill(0.4))
            t.hold()

        with self.beat("follow_order") as t:
            self.wipe(t)
            self.title(t, "Filling one in", fraction=0.12)
            rules, rows = numbered(
                ["Follow the algorithm in order.",
                 "Change a variable only when the code changes it.",
                 "Write an output only when the code outputs."],
                size=BODY_SIZE, gap=GAP_SM * 1.5)
            self.place(rules, self.head, buff=GAP_LG * 0.9)
            self.rules = rows
            self.play(FadeIn(rows[0]), run_time=t.fill(0.4))
            t.hold()

        with self.beat("only_when") as t:
            self.play(FadeIn(self.rules[1]), run_time=t.fill(0.4))
            t.hold()

        with self.beat("record_output") as t:
            self.play(FadeIn(self.rules[2]), run_time=t.fill(0.4))
            t.hold()

        with self.beat("not_every_cell") as t:
            self.say(t, "an unchanged value leaves its cell empty",
                     fraction=0.45)
            t.hold()

    # ------------------------------------------- 14. errors and debugging

    def errors(self):
        with self.beat("errors_open") as t:
            self.section(t, "Six ways an algorithm goes wrong", ERRORS)
            # At MARGIN_SIZE: six rows at LABEL_SIZE stand five units
            # tall, which reaches into the commentary band, and three of
            # these beats are commentary.
            table, cells, heads = columns(["Error", "What it means"],
                                          ERROR_ROWS, size=MARGIN_SIZE,
                                          row_gap=GAP_SM * 0.8)
            self.place(table, self.head, buff=GAP_MD * 1.2)
            self.errors_rows = cells
            self.play(FadeIn(VGroup(*heads)), Create(table.rule),
                      run_time=t.fill(0.3))
            t.hold()

        with self.beat("syntax") as t:
            self.play(FadeIn(VGroup(*self.errors_rows[0])),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("may_not_run") as t:
            self.say(t, "it may not run at all", fraction=0.4)
            t.hold()

        for index, name in enumerate(["logic", "boundary_err", "init_err",
                                      "update_err", "condition_err"]):
            with self.beat(name) as t:
                if index == 0:
                    self.drop_note(t)
                self.play(FadeIn(VGroup(*self.errors_rows[index + 1])),
                          run_time=t.fill(0.35))
                t.hold()

        with self.beat("loop_example") as t:
            self.say(t, "a loop that needed <= 10 and was written < 10",
                     fraction=0.45)
            t.hold()

        with self.beat("that_is") as t:
            self.say(t, "one step short: a boundary error from a wrong "
                        "condition", fraction=0.45, color=TERRACOTTA)
            t.hold()

        with self.beat("debugging") as t:
            self.wipe(t)
            self.title(t, "Debugging is tracing", fraction=0.12)
            t.hold()

        with self.beat("first_step") as t:
            line = prose("Trace it with chosen data, and find the first "
                         "step where actual and expected part company.",
                         BODY_SIZE, CHARCOAL, 11.4)
            self.place(line, self.head, buff=GAP_LG)
            self.play(Write(line), run_time=t.fill(0.5))
            t.hold()

    # ---------------------------------------------------------- 15. recap

    def recap(self):
        groups = [
            (["recap_open", "r_pdlc", "r_analysis", "r_design",
              "r_testing"], 0),
            (["r_abstraction", "r_decomposition", "r_represent"], 1),
            (["r_methods", "r_validation", "r_verification"], 2),
            (["r_testdata", "r_trace"], 3),
        ]
        for beats, index in groups:
            heading, lines = RECAP_CARDS[index]
            card = None
            for position, beat_name in enumerate(beats):
                with self.beat(beat_name) as t:
                    if position == 0:
                        if index == 0:
                            self.section(t, heading, RECAP)
                        else:
                            self.wipe(t)
                            self.title_swap(t, heading, fraction=0.14)
                        card = self.lines(*lines, size=BODY_SIZE)
                        self.stack(card, self.head, buff=GAP_MD * 1.1)
                    share = len(lines) * (position + 1) // len(beats)
                    already = len(lines) * position // len(beats)
                    for line in card[already:share]:
                        self.play(FadeIn(line),
                                  run_time=t.fill(
                                      0.5 / max(1, share - already)))
                    t.hold()

        with self.beat("exam_open") as t:
            self.wipe(t)
            self.title(t, "In the exam", fraction=0.1)
            rules, rows = numbered(EXAM_RULES, size=MARGIN_SIZE,
                                   gap=GAP_SM * 1.3)
            self.place(rules, self.head, buff=GAP_MD * 1.2)
            self.exam_rows = rows
            self.play(FadeIn(rows[0]), run_time=t.fill(0.35))
            t.hold()

        for index, name in enumerate(["exam_stage", "exam_algo",
                                      "exam_test", "exam_valid"]):
            with self.beat(name) as t:
                self.play(FadeIn(self.exam_rows[index + 1]),
                          run_time=t.fill(0.4))
                t.hold()

        with self.beat("exam_trace") as t:
            self.say(t, "and never guess the final answer", fraction=0.4,
                     color=TERRACOTTA)
            t.hold()

        with self.beat("pause") as t:
            self.wipe(t)
            self.title(t, "Answer these yourself", fraction=0.1)
            asked, rows = numbered(ASK_YOURSELF, size=MARGIN_SIZE,
                                   gap=GAP_SM * 0.9)
            self.place(asked, self.head, buff=GAP_MD)
            self.play(FadeIn(asked), run_time=t.fill(0.4))
            t.hold()

        with self.beat("close") as t:
            self.say(t, "one step at a time, and the long ones come apart",
                     fraction=0.45)
            t.hold()

    # ------------------------------------------------------- scaffolding

    @contextmanager
    def beat(self, name):
        self._beat_name = name
        with super().beat(name) as timer:
            yield timer

    def section(self, t, text, index, fraction=0.14):
        """Open one of the fifteen: clear, light the strip, name it."""
        self.wipe(t)
        if self.strip not in self.mobjects:
            self.play(FadeIn(self.strip), run_time=t.fill(0.05))
            self.keep = [self.margin, self.strip]
            self.floor = FLOOR
        head = fit(serif(text, TITLE_SIZE, CHARCOAL))
        head.to_edge(UP, buff=GAP_MD * 1.7)
        self.play(*self.strip.focus(index), Write(head),
                  run_time=t.fill(fraction))
        self.head = head
        return head

    def title(self, t, text, fraction=0.1, color=CHARCOAL):
        head = fit(serif(text, TITLE_SIZE, color))
        head.to_edge(UP, buff=GAP_MD * 1.7)
        self.play(Write(head), run_time=t.fill(fraction))
        self.head = head
        return head

    def title_swap(self, t, text, fraction=0.1, color=CHARCOAL):
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

    def drop_note(self, t, fraction=0.08):
        """Take the commentary line away before a figure grows into it.

        ``say`` swaps one line for the next, so a line stays until
        something replaces it -- and a table or a bench that keeps
        growing downwards will reach it. Nothing in the acceptance
        checks sees a caption a figure has since grown into, because
        the check runs once per beat on what is there.
        """
        if self.note is not None and self.note in self.mobjects:
            self.play(FadeOut(self.note), run_time=t.fill(fraction))
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

    def band_is_clear(self, line, tol=0.05, clearance=0.08):
        """Refuse to print commentary through whatever is already there.

        The acceptance check compares writing against writing, so a
        caption laid across a diagram reads as clean to it: a box is a
        shape, not text. This reserves the band at the foot of the frame
        for one line of commentary, and it demands a positive gap rather
        than merely the absence of overlap -- a caption whose ascenders
        stop two hundredths of a unit under a box reads as touching it.
        """
        for mobject in self.mobjects:
            if mobject in self.keep or mobject is self.note:
                continue
            wide = (min(line.get_right()[0], mobject.get_right()[0])
                    - max(line.get_left()[0], mobject.get_left()[0]))
            high = (min(line.get_top()[1], mobject.get_top()[1])
                    - max(line.get_bottom()[1], mobject.get_bottom()[1]))
            if wide > tol and high > -clearance:
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
