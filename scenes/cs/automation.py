"""Chapter 6, Automated and Emerging Technologies: Cambridge O Level 2210.

Twelve numbered sections and an opening, every reveal anchored to the
narration by build/beats_ch06.py.

The chapter is three topics that share one shape -- something measures,
something decides, something acts -- and the figures are picked to make
that shape visible rather than stated:

  * ``ControlLoop`` is the chapter's spine. It appears for the
    greenhouse, again for the heating system, and a third time to close
    the chapter, and each time the return arrow arrives last, because
    the lecture earns it last. Three boxes in a row is the answer the
    syllabus marks down: a system that acts and never checks.
  * ``ExpertSystem`` places the four components so that the arrows
    answer "what does the inference engine do" on their own -- it is the
    one box every arrow converges on.
  * ``StageFlow`` wraps the six machine-learning stages into two rows
    with the turn drawn in the gap, so neither row has to be read
    backwards.
  * ``SortBench`` weighs automation's gains against its costs, and then,
    unchanged, an expert system's strengths against its limits.

Where the captions and the audio disagree, the captions are right and
the mismatch is deliberate: the narration is correct, the transcriber
misheard parts of it, and the beats are anchored to what it produced
because that is what the anchors are matched against. "export systems"
is expert systems, "immunity" is humidity, "jams" are arms, "a pump or
wall" is a valve. build/beats_ch06.py lists them, along with the one cut
made inside the recording.

Timing: timings/cs.automation.json
Render: python build/render.py scripts/CH06-automation.md \\
    audio/CH06-automation.m4a
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
from components.automation import ControlLoop, ExpertSystem, StageFlow
from components.editorial import columns, fit, numbered, prose
from components.os_core import callout
from components.os_shape import SortBench, chips, grid
from components.syllabus_map import TopicStrip
from scenes.base import SATScene

FRAME_SAFE = 12.6
FLOOR = -3.05
BARE_FLOOR = -3.5

PARTS = ["Automated systems", "The feedback loop", "Where it is used",
         "Weighing automation", "What makes a robot", "Where robots work",
         "Artificial intelligence", "Expert systems", "Machine learning",
         "The comparison", "One example", "Recap"]
(AUTO, LOOP, USES, WEIGH, ROBOT, ROBOT_USES, AI, EXPERT, ML, COMPARE,
 EXAMPLE, RECAP) = range(12)

AREAS = ["Automated systems", "Robotics", "Artificial intelligence"]

# The three questions that fit every system in the chapter, which is the
# structure an answer is marked against.
QUESTIONS_OF_ANY = [
    "What does it receive?",
    "What does it process?",
    "What does it produce?",
]

# The loop in the lecture's own order and wording.
LOOP_STEPS = [
    "A sensor measures a physical property.",
    "The reading goes to the control system.",
    "It may be converted into digital data.",
    "The processor compares it with the target.",
    "The program decides whether to act.",
    "A signal goes to the actuator.",
    "The actuator changes the system.",
    "The sensor measures the result again.",
]

FIVE_WORDS = ["Sensor", "Process", "Decide", "Act", "Measure again"]

# Four systems, one shape. The point of the table is the middle column:
# name the sensor and the output and the answer is most of the way there.
SYSTEM_ROWS = [
    ("Lighting", "light or proximity", "a lamp on or off"),
    ("Weather", "temperature, wind", "records or warns"),
    ("Tank", "the level inside", "a pump or a valve"),
    ("Vehicle", "speed, proximity", "warns, or brakes"),
]

# Measured against the bench's own 6.05-unit column rather than judged
# by eye: the serif face is wider per character than it looks, and three
# of these were over before they were measured.
GAINS = ["never stops", "same task, same way",
         "handles dangerous places", "records as it goes"]
COSTS = ["costly to buy and run", "acts on a bad reading",
         "poor at the unexpected", "jobs displaced",
         "one more thing to attack"]

ROBOT_PARTS = ["Mechanical structure", "Sensors", "Processor",
               "Actuators", "Programmable"]

ROBOT_TEST = [
    "A mechanical structure.",
    "Sensors that read its surroundings.",
    "A processor or controller running a program.",
    "Actuators that move it.",
    "Instructions you can change.",
]

ROBOT_FIELDS = ["Industry", "Transport", "Agriculture", "Medicine",
                "Homes", "Entertainment"]

ROBOT_LIMITS = ["Cost", "What a failure costs", "The unexpected"]

EXPERT_ROLES = [
    ("Knowledge base", "holds the facts"),
    ("Rule base", "holds the logic"),
    ("Inference engine", "applies the rules to the facts"),
    ("User interface", "asks, and shows the answer"),
]

STRENGTHS = ["consistent every time", "available any time",
             "keeps expert knowledge", "shows the rules it used"]

LIMITS = ["only as good as its rules", "stale rules, stale answers",
          "stuck outside its rules", "no empathy or judgement",
          "slow to update"]

COMPARE_ROWS = [
    ("Knowledge", "facts and rules", "patterns in data"),
    ("Explaining", "trace the rules", "often harder"),
    ("Changing", "someone edits rules", "retrain on new data"),
    ("Best when", "the area is narrow", "examples are many"),
]

RECAP_CARDS = [
    ("An automated system", [
        "Sensors collect the data.",
        "A processor decides what to do.",
        "Actuators change the environment.",
        "In a feedback loop, it measures again.",
    ]),
    ("Weighing it", [
        "Fast, consistent, and safe where people are not.",
        "Costly, and poor at the unexpected.",
    ]),
    ("Robots and AI", [
        "A robot is programmable, with a mechanical structure.",
        "Sensors, a processor, actuators.",
        "AI uses data and rules to reach conclusions.",
        "Some of it learns from examples and adapts.",
    ]),
    ("The two AI systems", [
        "An expert system: knowledge base, rule base,",
        "inference engine, user interface.",
        "Machine learning finds patterns in data.",
        "Poor or biased data, unreliable results.",
    ]),
]

ASK_YOURSELF = [
    "Name the three parts of an automated system.",
    "Why does the sensor read again after the actuator acts?",
    "What makes something a robot rather than a machine?",
    "Name the four components of an expert system.",
    "Which one applies the rules?",
    "What are the stages of a machine-learning process?",
    "When is an expert system the better choice?",
]


class Automation(SATScene):
    scene_id = "cs.automation"

    def construct(self):
        self.margin = mono("Automation and AI · Chapter 6", MARGIN_SIZE)
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
        self.automated_system()
        self.feedback_loop()
        self.where_used()
        self.weighing()
        self.what_makes_a_robot()
        self.where_robots_work()
        self.artificial_intelligence()
        self.expert_systems()
        self.machine_learning()
        self.comparison()
        self.one_example()
        self.recap()

    # --------------------------------------------------------- opening

    def opening(self):
        with self.beat("open") as t:
            chapter = serif("Chapter 6", LABEL_SIZE, SLATE)
            title = fit(serif("Automated and Emerging Technologies",
                              DISPLAY_SIZE, CHARCOAL))
            board = prose("Cambridge O Level Computer Science 2210",
                          LABEL_SIZE, GREY)
            card = VGroup(chapter, title, board).arrange(DOWN, buff=GAP_MD)
            card.move_to(ORIGIN)
            self.play(FadeIn(chapter), run_time=t.fill(0.2))
            self.play(Write(title), run_time=t.fill(0.4))
            self.board = board
            t.hold()

        with self.beat("three_areas") as t:
            self.play(FadeIn(self.board), run_time=t.fill(0.25))
            t.hold()

        with self.beat("sensors_actuators") as t:
            self.wipe(t)
            self.title(t, "Three connected areas", fraction=0.12)
            areas, each = chips(AREAS, size=LABEL_SIZE, rows=1)
            self.place(areas, self.head, buff=GAP_LG)
            self.areas = each
            self.play(FadeIn(areas), run_time=t.fill(0.3))
            t.hold()

        with self.beat("robots_where") as t:
            self.say(t, "and the one shape they share", fraction=0.35)
            t.hold()

        with self.beat("focus_on") as t:
            self.wipe(t)
            self.title(t, "Ask three things of any system", fraction=0.12)
            asked, rows = numbered(QUESTIONS_OF_ANY, size=BODY_SIZE,
                                   gap=GAP_SM * 1.8)
            self.place(asked, self.head, buff=GAP_LG * 0.9)
            self.asked = rows
            self.play(FadeIn(rows[0]), FadeIn(rows[1]),
                      run_time=t.fill(0.35))
            t.hold()

        with self.beat("produces") as t:
            self.play(FadeIn(self.asked[2]), run_time=t.fill(0.4))
            t.hold()

    # ------------------------------------- 1. what an automated system is

    def automated_system(self):
        loop = ControlLoop()
        self.loop = loop

        with self.beat("auto_open") as t:
            self.section(t, "A process with little human control", AUTO)
            t.hold()

        with self.beat("follow_info") as t:
            self.say(t, "Follow the information through it", fraction=0.4)
            t.hold()

        with self.beat("sensor_gathers") as t:
            self.play(Create(loop.boxes[0]), FadeIn(loop.labels[0]),
                      run_time=t.fill(0.35))
            self.say(t, "it gathers data from the environment",
                     fraction=0.3)
            t.hold()

        with self.beat("micro_receives") as t:
            self.play(Create(loop.boxes[1]), FadeIn(loop.labels[1]),
                      Create(loop.arrow_into(1)), run_time=t.fill(0.4))
            t.hold()

        with self.beat("actuator_does") as t:
            self.play(Create(loop.boxes[2]), FadeIn(loop.labels[2]),
                      Create(loop.arrow_into(2)), run_time=t.fill(0.4))
            t.hold()

        with self.beat("greenhouse") as t:
            self.title_swap(t, "An automated greenhouse", fraction=0.3)
            t.hold()

        with self.beat("moisture") as t:
            note = loop.detail(0, "reads the soil")
            self.play(FadeIn(note), *loop.light(0), run_time=t.fill(0.4))
            t.hold()

        with self.beat("reading_sent") as t:
            self.play(*loop.settle(0), *loop.light(1), run_time=t.fill(0.4))
            t.hold()

        with self.beat("compares") as t:
            note = loop.detail(1, "checks the target")
            self.play(FadeIn(note), run_time=t.fill(0.4))
            t.hold()

        with self.beat("too_dry") as t:
            self.say(t, "too dry: the program decides to act", fraction=0.4)
            t.hold()

        with self.beat("opens_valve") as t:
            note = loop.detail(2, "opens the valve")
            self.play(FadeIn(note), *loop.settle(1), *loop.light(2),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("another_reading") as t:
            self.play(*loop.settle(2), Create(loop.feedback),
                      run_time=t.fill(0.45))
            t.hold()

        with self.beat("check_result") as t:
            self.play(FadeIn(loop.feedback_label), run_time=t.fill(0.3))
            self.say(t, "so it can check whether the action worked",
                     fraction=0.3)
            t.hold()

        with self.beat("still_dry") as t:
            self.say(t, "still too dry: keep watering", fraction=0.4)
            t.hold()

        with self.beat("target_reached") as t:
            self.say(t, "at the target: stop", fraction=0.4)
            t.hold()

        with self.beat("feedback_named") as t:
            self.wipe(t)
            named = fit(serif("Feedback control", DISPLAY_SIZE, TERRACOTTA))
            named.move_to([0, 0.6, 0])
            under = prose("measure, act, and measure again", BODY_SIZE,
                          CHARCOAL)
            self.place(under, named, buff=GAP_LG * 0.8)
            self.play(Write(named), run_time=t.fill(0.3))
            self.play(FadeIn(under), run_time=t.fill(0.3))
            t.hold()

    # ------------------------------------------------- 2. the feedback loop

    def feedback_loop(self):
        with self.beat("loop_open") as t:
            self.section(t, "The loop, step by step", LOOP)
            steps, rows = numbered(LOOP_STEPS, size=LABEL_SIZE,
                                   gap=GAP_SM * 0.9)
            self.place(steps, self.head, buff=GAP_MD)
            self.steps = rows
            t.hold()

        names = ["measures_property", "sends_reading", "converted",
                 "compare_preset", "decides", "signal_actuator",
                 "changes_system", "measures_again"]
        for index, name in enumerate(names):
            with self.beat(name) as t:
                self.play(FadeIn(self.steps[index]), run_time=t.fill(0.4))
                t.hold()

        heater = ControlLoop()
        self.heater = heater

        with self.beat("heating") as t:
            self.wipe(t)
            self.title(t, "A heating system", fraction=0.12)
            first = heater.detail(0, "reads the room")
            self.play(Create(heater.boxes), FadeIn(heater.labels),
                      Create(heater.arrows), FadeIn(first),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("room_temp") as t:
            note = heater.detail(1, "against the setting")
            self.play(FadeIn(note), *heater.light(1), run_time=t.fill(0.4))
            t.hold()

        with self.beat("too_cold") as t:
            note = heater.detail(2, "heater on")
            self.play(FadeIn(note), *heater.settle(1), *heater.light(2),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("switch_off") as t:
            self.play(*heater.settle(2), run_time=t.fill(0.2))
            self.say(t, "at the chosen temperature the heater goes off",
                     fraction=0.35)
            t.hold()

        with self.beat("essential") as t:
            self.play(Create(heater.feedback),
                      FadeIn(heater.feedback_label), run_time=t.fill(0.45))
            t.hold()

        with self.beat("without_feedback") as t:
            self.say(t, "without it, the heater never learns it has won",
                     fraction=0.4)
            t.hold()

        with self.beat("oven") as t:
            # In the band, not under the figure: the return path's own
            # label reaches y -1.56 and a second line below it has
            # nowhere to go that is not either on the label or on the
            # commentary.
            self.say(t, "and the room becomes an oven", fraction=0.4,
                     color=TERRACOTTA)
            t.hold()

        with self.beat("exam_cycle") as t:
            self.wipe(t)
            self.title(t, "What the exam wants back", fraction=0.12)
            t.hold()

        with self.beat("five_words") as t:
            five, each = chips(FIVE_WORDS, size=LABEL_SIZE, rows=1)
            self.place(five, self.head, buff=GAP_LG)
            self.play(FadeIn(five), run_time=t.fill(0.4))
            t.hold()

    # -------------------------------------------- 3. where automation is used

    def where_used(self):
        with self.beat("uses_open") as t:
            self.section(t, "Four systems, one shape", USES)
            table, cells, heads = columns(
                ["System", "What it senses", "What it does"], SYSTEM_ROWS,
                size=LABEL_SIZE, row_gap=GAP_SM * 1.2)
            self.place(table, self.head, buff=GAP_MD * 1.2)
            self.table, self.cells = table, cells
            self.play(FadeIn(VGroup(*heads)), Create(table.rule),
                      run_time=t.fill(0.3))
            t.hold()

        with self.beat("lighting") as t:
            self.play(FadeIn(self.cells[0][0]), FadeIn(self.cells[0][1]),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("proximity") as t:
            self.say(t, "a light sensor, or one that senses you coming",
                     fraction=0.4)
            t.hold()

        with self.beat("walking_near") as t:
            self.say(t, "the corridor light that comes on as you reach it",
                     fraction=0.4)
            t.hold()

        with self.beat("lamp_output") as t:
            self.play(FadeIn(self.cells[0][2]), run_time=t.fill(0.4))
            t.hold()

        with self.beat("weather") as t:
            self.play(FadeIn(self.cells[1][0]), FadeIn(self.cells[1][1]),
                      run_time=t.fill(0.3))
            # The corridor-light line belongs to the row above it, and
            # three more rows arrive under it before anything else would
            # replace it.
            self.say(t, "the same shape every time", fraction=0.25)
            t.hold()

        with self.beat("record_alarm") as t:
            self.play(FadeIn(self.cells[1][2]), run_time=t.fill(0.4))
            t.hold()

        with self.beat("tank") as t:
            self.play(FadeIn(VGroup(*self.cells[2])), run_time=t.fill(0.4))
            t.hold()

        with self.beat("vehicle") as t:
            self.play(FadeIn(self.cells[3][0]), FadeIn(self.cells[3][1]),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("warning_brake") as t:
            self.play(FadeIn(self.cells[3][2]), run_time=t.fill(0.4))
            t.hold()

        with self.beat("dashboard") as t:
            self.say(t, "the warning light on the dashboard is one of these",
                     fraction=0.4)
            t.hold()

        with self.beat("identify_three") as t:
            self.wipe(t)
            self.title(t, "Name three things, every time", fraction=0.12)
            three, rows = numbered(
                ["What the sensor measures.",
                 "What the processor decides.",
                 "What the actuator or output does."],
                size=BODY_SIZE, gap=GAP_SM * 1.6)
            self.place(three, self.head, buff=GAP_LG * 0.9)
            self.three = rows
            self.play(FadeIn(rows[0]), FadeIn(rows[1]), FadeIn(rows[2]),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("structure") as t:
            self.say(t, "that is the structure of the answer", fraction=0.4)
            t.hold()

    # ----------------------------------------------- 4. weighing automation

    def weighing(self):
        bench = None

        with self.beat("weigh_open") as t:
            self.section(t, "What it gives, what it costs", WEIGH)
            bench = SortBench("Advantages", "Disadvantages")
            bench.next_to(self.head, DOWN, buff=GAP_MD)
            self.bench = bench
            self.play(Write(bench.heads[0]), Write(bench.heads[1]),
                      Create(bench.rules), run_time=t.fill(0.4))
            t.hold()

        for index, name in enumerate(["continuous", "quick_precise",
                                      "dangerous_places", "record_data"]):
            with self.beat(name) as t:
                self.play(FadeIn(bench.item(0, GAINS[index])),
                          run_time=t.fill(0.4))
                t.hold()

        with self.beat("costs_open") as t:
            self.say(t, "and the other side of it", fraction=0.4)
            t.hold()

        with self.beat("expensive") as t:
            self.play(FadeIn(bench.item(1, COSTS[0])), run_time=t.fill(0.4))
            t.hold()

        with self.beat("wrong_action") as t:
            self.play(FadeIn(bench.item(1, COSTS[1])), run_time=t.fill(0.4))
            t.hold()

        with self.beat("dangerous_where") as t:
            self.say(t, "a heater, a car, a factory, a hospital",
                     fraction=0.4)
            t.hold()

        with self.beat("unexpected") as t:
            self.play(FadeIn(bench.item(1, COSTS[2])), run_time=t.fill(0.4))
            t.hold()

        with self.beat("jobs") as t:
            self.play(FadeIn(bench.item(1, COSTS[3])), run_time=t.fill(0.4))
            t.hold()

        with self.beat("cyber") as t:
            self.play(FadeIn(bench.item(1, COSTS[4])), run_time=t.fill(0.4))
            t.hold()

        with self.beat("not_good_bad") as t:
            self.wipe(t)
            self.title(t, "Never just good or bad", fraction=0.12,
                       color=TERRACOTTA)
            t.hold()

        with self.beat("connect_situation") as t:
            line = prose("Tie every point to the situation in the question.",
                         BODY_SIZE, CHARCOAL)
            self.place(line, self.head, buff=GAP_LG)
            self.play(Write(line), run_time=t.fill(0.45))
            t.hold()

    # ------------------------------------------------ 5. what makes a robot

    def what_makes_a_robot(self):
        with self.beat("robot_open") as t:
            self.section(t, "Robotics", ROBOT)
            t.hold()

        with self.beat("robotics_is") as t:
            line = prose("Designing, building and operating robots.",
                         BODY_SIZE, CHARCOAL)
            self.place(line, self.head, buff=GAP_LG * 0.8)
            self.robotics = line
            self.play(FadeIn(line), run_time=t.fill(0.4))
            t.hold()

        with self.beat("robot_is") as t:
            self.wipe(t)
            self.title(t, "What a robot has", fraction=0.12)
            kit, each = chips(ROBOT_PARTS, size=LABEL_SIZE, rows=2)
            self.place(kit, self.head, buff=GAP_LG * 0.9)
            self.kit, self.kit_each = kit, each
            t.hold()

        with self.beat("structure_parts") as t:
            self.play(FadeIn(self.kit_each[0]), run_time=t.fill(0.3))
            self.say(t, "a frame, joints, wheels, arms", fraction=0.3)
            t.hold()

        with self.beat("robot_sensors") as t:
            self.play(FadeIn(self.kit_each[1]), run_time=t.fill(0.4))
            t.hold()

        with self.beat("robot_processor") as t:
            self.play(FadeIn(self.kit_each[2]), run_time=t.fill(0.4))
            t.hold()

        with self.beat("robot_actuator") as t:
            self.play(FadeIn(self.kit_each[3]), run_time=t.fill(0.4))
            t.hold()

        with self.beat("programmable") as t:
            chip = self.kit_each[4]
            self.play(FadeIn(chip), run_time=t.fill(0.25))
            self.play(chip.animate.set_color(TERRACOTTA),
                      run_time=t.fill(0.25))
            t.hold()

        with self.beat("distinguish") as t:
            self.say(t, "these five are what separate a robot from a machine",
                     fraction=0.4)
            t.hold()

        with self.beat("washing_machine") as t:
            self.wipe(t)
            self.title(t, "Is a washing machine a robot?", fraction=0.14)
            asked = prose("It is automated. It runs a program.", BODY_SIZE,
                          CHARCOAL)
            self.place(asked, self.head, buff=GAP_LG * 0.9)
            self.asked_line = asked
            self.play(FadeIn(asked), run_time=t.fill(0.4))
            t.hold()

        with self.beat("not_a_robot") as t:
            answer = prose("But not with the mechanical structure and "
                           "changeable instructions this course means.",
                           BODY_SIZE, TERRACOTTA, 11.0)
            self.place(answer, self.asked_line, buff=GAP_MD * 1.2)
            self.play(Write(answer), run_time=t.fill(0.45))
            t.hold()

        with self.beat("checklist") as t:
            self.wipe(t)
            self.title(t, "The test to apply", fraction=0.12)
            test, rows = numbered(ROBOT_TEST, size=LABEL_SIZE,
                                  gap=GAP_SM * 1.1)
            self.place(test, self.head, buff=GAP_MD * 1.2)
            self.play(FadeIn(test), run_time=t.fill(0.4))
            t.hold()

    # ------------------------------------------------ 6. where robots work

    def where_robots_work(self):
        with self.beat("robot_uses_open") as t:
            self.section(t, "Where robots work", ROBOT_USES)
            fields, items = grid(ROBOT_FIELDS, columns=3, size=LABEL_SIZE,
                                 h_gap=GAP_MD * 1.2, v_gap=GAP_SM * 1.8)
            self.place(fields, self.head, buff=GAP_LG * 0.9)
            self.fields = items
            t.hold()

        with self.beat("industry") as t:
            self.play(FadeIn(self.fields[0]), run_time=t.fill(0.3))
            self.say(t, "assembling, welding, inspecting", fraction=0.3)
            t.hold()

        with self.beat("precise_moves") as t:
            self.say(t, "the same movement, and heat no one could stand",
                     fraction=0.4)
            t.hold()

        with self.beat("transport") as t:
            self.play(FadeIn(self.fields[1]), run_time=t.fill(0.4))
            t.hold()

        with self.beat("drones") as t:
            self.say(t, "delivery and monitoring by drone", fraction=0.4)
            t.hold()

        with self.beat("agriculture") as t:
            self.play(FadeIn(self.fields[2]), run_time=t.fill(0.4))
            t.hold()

        with self.beat("large_areas") as t:
            self.say(t, "large areas, and less exposure to chemicals",
                     fraction=0.4)
            t.hold()

        with self.beat("medicine") as t:
            self.play(FadeIn(self.fields[3]), run_time=t.fill(0.4))
            t.hold()

        with self.beat("homes") as t:
            self.play(FadeIn(self.fields[4]), run_time=t.fill(0.4))
            t.hold()

        with self.beat("entertainment") as t:
            self.play(FadeIn(self.fields[5]), run_time=t.fill(0.4))
            t.hold()

        with self.beat("depends") as t:
            self.wipe(t)
            self.title(t, "Which example to give", fraction=0.12)
            t.hold()

        with self.beat("factory_answer") as t:
            line = prose("A dangerous factory: repetitive or hazardous work.",
                         BODY_SIZE, CHARCOAL)
            self.place(line, self.head, buff=GAP_LG * 0.9)
            self.factory = line
            self.play(FadeIn(line), run_time=t.fill(0.4))
            t.hold()

        with self.beat("limitations") as t:
            limits, each = chips(ROBOT_LIMITS, size=LABEL_SIZE, rows=1)
            self.place(limits, self.factory, buff=GAP_LG * 0.8)
            self.play(FadeIn(limits), run_time=t.fill(0.4))
            t.hold()

        with self.beat("balanced") as t:
            self.say(t, "a balanced answer gives both sides", fraction=0.4)
            t.hold()

    # ------------------------------------------- 7. artificial intelligence

    def artificial_intelligence(self):
        with self.beat("ai_open") as t:
            self.section(t, "Artificial intelligence", AI)
            t.hold()

        with self.beat("ai_is") as t:
            line = prose("Simulating intelligent behaviour.", BODY_SIZE,
                         CHARCOAL)
            self.place(line, self.head, buff=GAP_LG * 0.8)
            self.ai_line = line
            self.play(Write(line), run_time=t.fill(0.4))
            t.hold()

        with self.beat("ai_uses") as t:
            self.wipe(t)
            self.title(t, "What an AI system does", fraction=0.12)
            flow, each = chips(["Data and rules in", "Processing",
                                "Conclusions or actions"],
                               size=LABEL_SIZE, rows=1)
            self.place(flow, self.head, buff=GAP_LG)
            self.flow = flow
            self.play(FadeIn(flow), run_time=t.fill(0.4))
            t.hold()

        with self.beat("ai_reasons") as t:
            self.say(t, "it reasons about what it is given", fraction=0.4)
            t.hold()

        with self.beat("mistake") as t:
            self.wipe(t)
            self.title(t, "The answer that earns nothing", fraction=0.12)
            quote = prose("“a computer that thinks like a human”",
                          BODY_SIZE, GREY)
            self.place(quote, self.head, buff=GAP_LG * 0.9)
            self.quote = quote
            self.play(FadeIn(quote), run_time=t.fill(0.4))
            t.hold()

        with self.beat("too_vague") as t:
            verdict = serif("Too vague.", BODY_SIZE, TERRACOTTA)
            self.place(verdict, self.quote, buff=GAP_MD * 1.2)
            self.play(Write(verdict), run_time=t.fill(0.4))
            t.hold()

        with self.beat("instead") as t:
            self.wipe(t)
            self.title(t, "Say this instead", fraction=0.1)
            better = prose("An AI system uses data and rules to process "
                           "information and produce conclusions or actions.",
                           BODY_SIZE, CHARCOAL, 11.4)
            self.place(better, self.head, buff=GAP_LG * 0.9)
            self.better = better
            self.play(Write(better), run_time=t.fill(0.5))
            t.hold()

        with self.beat("can_learn") as t:
            more = prose("Some also learn from examples and adapt.",
                         BODY_SIZE, SAGE)
            self.place(more, self.better, buff=GAP_MD * 1.2)
            self.play(FadeIn(more), run_time=t.fill(0.4))
            t.hold()

        with self.beat("two_examples") as t:
            self.wipe(t)
            self.title(t, "Two of them, in detail", fraction=0.1)
            pair, each = chips(["Expert systems", "Machine learning"],
                               size=LABEL_SIZE, rows=1)
            self.place(pair, self.head, buff=GAP_LG)
            self.play(FadeIn(pair), run_time=t.fill(0.4))
            t.hold()

    # ---------------------------------------------------- 8. expert systems

    def expert_systems(self):
        expert = ExpertSystem()
        self.expert = expert

        with self.beat("expert_open") as t:
            self.section(t, "Stored knowledge, and rules", EXPERT)
            t.hold()

        with self.beat("plant_disease") as t:
            self.say(t, "naming a plant disease from the symptoms you type "
                        "in", fraction=0.4)
            t.hold()

        with self.beat("four_parts") as t:
            self.title_swap(t, "Four components", fraction=0.3)
            t.hold()

        with self.beat("knowledge_base") as t:
            self.play(Create(expert.boxes[0]), FadeIn(expert.labels[0]),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("rule_base") as t:
            self.play(Create(expert.boxes[1]), FadeIn(expert.labels[1]),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("inference") as t:
            self.play(Create(expert.boxes[2]), FadeIn(expert.labels[2]),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("interface") as t:
            self.play(Create(expert.boxes[3]), FadeIn(expert.labels[3]),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("follow_open") as t:
            self.title_swap(t, "How it reaches an answer", fraction=0.3)
            t.hold()

        with self.beat("user_enters") as t:
            self.play(Create(expert.asks), *expert.light(3),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("engine_checks") as t:
            self.play(Create(expert.from_knowledge), *expert.settle(3),
                      *expert.light(0), run_time=t.fill(0.45))
            t.hold()

        with self.beat("applies_rules") as t:
            self.play(Create(expert.from_rules), *expert.settle(0),
                      *expert.light(1), run_time=t.fill(0.45))
            t.hold()

        with self.beat("presents") as t:
            self.play(*expert.settle(1), *expert.light(2),
                      run_time=t.fill(0.3))
            self.say(t, "it may ask more questions to narrow things down",
                     fraction=0.3)
            t.hold()

        with self.beat("displays") as t:
            self.play(Create(expert.advice), *expert.settle(2),
                      run_time=t.fill(0.3))
            self.play(FadeIn(expert.advice_label), run_time=t.fill(0.2))
            t.hold()

        with self.beat("engine_role") as t:
            self.wipe(t)
            self.title(t, "Keep the four roles apart", fraction=0.1)
            table, cells, heads = columns(
                ["Component", "What it is for"], EXPERT_ROLES,
                size=LABEL_SIZE, row_gap=GAP_SM * 1.2)
            self.place(table, self.head, buff=GAP_MD * 1.4)
            self.roles = cells
            self.play(FadeIn(VGroup(*heads)), Create(table.rule),
                      run_time=t.fill(0.2))
            self.play(FadeIn(VGroup(*cells[2])), run_time=t.fill(0.25))
            t.hold()

        with self.beat("kb_role") as t:
            self.play(FadeIn(VGroup(*self.roles[0])), run_time=t.fill(0.4))
            t.hold()

        with self.beat("rb_role") as t:
            self.play(FadeIn(VGroup(*self.roles[1])), run_time=t.fill(0.4))
            t.hold()

        with self.beat("ui_role") as t:
            self.play(FadeIn(VGroup(*self.roles[3])), run_time=t.fill(0.4))
            t.hold()

        with self.beat("distinct") as t:
            # No commentary line here: the four-row table reaches y -2.46
            # and the band starts at -2.48, which is a gap of two
            # hundredths of a unit and reads as touching. The row the
            # students confuse is the one to colour instead.
            row = VGroup(*self.roles[2])
            self.play(row.animate.set_color(TERRACOTTA),
                      run_time=t.fill(0.4))
            t.hold()

        bench = None
        with self.beat("strengths_open") as t:
            self.wipe(t)
            self.title(t, "Strengths, and limits", fraction=0.12)
            bench = SortBench("Strengths", "Limits")
            bench.next_to(self.head, DOWN, buff=GAP_MD)
            self.ebench = bench
            self.play(Write(bench.heads[0]), Write(bench.heads[1]),
                      Create(bench.rules), run_time=t.fill(0.35))
            t.hold()

        for index, name in enumerate(["consistent", "available", "preserve",
                                      "explain_rules"]):
            with self.beat(name) as t:
                self.play(FadeIn(bench.item(0, STRENGTHS[index])),
                          run_time=t.fill(0.4))
                t.hold()

        for index, name in enumerate(["depends_quality", "out_of_date",
                                      "not_covered", "no_empathy",
                                      "updating"]):
            with self.beat(name) as t:
                self.play(FadeIn(bench.item(1, LIMITS[index])),
                          run_time=t.fill(0.4))
                t.hold()

        with self.beat("narrow_area") as t:
            self.say(t, "useful in a narrow area, and no substitute for an "
                        "expert", fraction=0.4)
            t.hold()

    # --------------------------------------------------- 9. machine learning

    def machine_learning(self):
        with self.beat("ml_open") as t:
            self.section(t, "Patterns, not rules", ML)
            t.hold()

        with self.beat("finds_patterns") as t:
            line = prose("It learns from examples and data.", BODY_SIZE,
                         CHARCOAL)
            self.place(line, self.head, buff=GAP_LG * 0.8)
            self.ml_line = line
            self.play(FadeIn(line), run_time=t.fill(0.4))
            t.hold()

        with self.beat("during_training") as t:
            second = prose("Training adjusts a model inside the system.",
                           BODY_SIZE, CHARCOAL)
            self.place(second, self.ml_line, buff=GAP_MD * 1.2)
            self.ml_second = second
            self.play(FadeIn(second), run_time=t.fill(0.4))
            t.hold()

        with self.beat("predictions") as t:
            third = prose("The model then predicts, or classifies, new data.",
                          BODY_SIZE, SAGE)
            self.place(third, self.ml_second, buff=GAP_MD * 1.2)
            self.play(FadeIn(third), run_time=t.fill(0.4))
            t.hold()

        leaves = None
        with self.beat("leaves") as t:
            self.wipe(t)
            self.title(t, "Healthy, or unhealthy?", fraction=0.12)
            leaves = SortBench("Healthy leaves", "Unhealthy leaves")
            leaves.next_to(self.head, DOWN, buff=GAP_MD)
            self.leaves = leaves
            self.play(Write(leaves.heads[0]), Write(leaves.heads[1]),
                      Create(leaves.rules), run_time=t.fill(0.3))
            self.play(FadeIn(leaves.item(0, "labelled examples")),
                      FadeIn(leaves.item(1, "labelled examples")),
                      run_time=t.fill(0.3))
            t.hold()

        with self.beat("distinguishes") as t:
            self.say(t, "the model looks for what separates the two",
                     fraction=0.4)
            t.hold()

        with self.beat("new_image") as t:
            self.say(t, "a new leaf arrives: which group does it belong to?",
                     fraction=0.45, color=TERRACOTTA)
            t.hold()

        flow = StageFlow()
        with self.beat("stages_open") as t:
            self.wipe(t)
            self.title(t, "The stages, in order", fraction=0.12)
            flow.next_to(self.head, DOWN, buff=GAP_MD)
            flow.move_to([0, flow.get_center()[1], 0])
            self.flow_fig = flow
            t.hold()

        with self.beat("collect") as t:
            self.play(Create(flow.boxes[0]), FadeIn(flow.labels[0]),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("prepare") as t:
            self.play(Create(flow.boxes[1]), FadeIn(flow.labels[1]),
                      Create(flow.arrows[0]), run_time=t.fill(0.4))
            t.hold()

        with self.beat("train") as t:
            self.play(Create(flow.boxes[2]), FadeIn(flow.labels[2]),
                      Create(flow.arrows[1]), run_time=t.fill(0.4))
            t.hold()

        with self.beat("evaluate") as t:
            self.play(Create(flow.wraps[0]), Create(flow.boxes[3]),
                      FadeIn(flow.labels[3]), run_time=t.fill(0.45))
            t.hold()

        with self.beat("handle_new") as t:
            self.say(t, "on data it was not trained on", fraction=0.4)
            t.hold()

        with self.beat("use_model") as t:
            self.play(Create(flow.boxes[4]), FadeIn(flow.labels[4]),
                      Create(flow.arrows[2]), run_time=t.fill(0.4))
            t.hold()

        with self.beat("monitor") as t:
            self.play(Create(flow.boxes[5]), FadeIn(flow.labels[5]),
                      Create(flow.arrows[3]), run_time=t.fill(0.4))
            t.hold()

        with self.beat("update") as t:
            self.say(t, "and the model or its data is updated", fraction=0.4)
            t.hold()

        with self.beat("no_guarantee") as t:
            self.wipe(t)
            self.title(t, "No guarantee", fraction=0.1, color=TERRACOTTA)
            t.hold()

        with self.beat("biased") as t:
            line = prose("Incomplete, biased or poor data gives unreliable "
                         "and unfair results.", BODY_SIZE, CHARCOAL, 11.4)
            self.place(line, self.head, buff=GAP_LG * 0.9)
            self.bias_line = line
            self.play(Write(line), run_time=t.fill(0.5))
            t.hold()

        with self.beat("quality_matters") as t:
            line = prose("The quality of the data sets the quality of the "
                         "model.", BODY_SIZE, SAGE, 11.4)
            self.place(line, self.bias_line, buff=GAP_MD * 1.3)
            self.play(FadeIn(line), run_time=t.fill(0.45))
            t.hold()

    # ------------------------------------------------- 10. the comparison

    def comparison(self):
        with self.beat("compare_open") as t:
            self.section(t, "Side by side", COMPARE)
            table, cells, heads = columns(
                ["", "Expert system", "Machine learning"], COMPARE_ROWS,
                size=LABEL_SIZE, row_gap=GAP_SM * 1.2)
            self.place(table, self.head, buff=GAP_MD * 1.3)
            self.compare = cells
            self.play(FadeIn(VGroup(*heads)), Create(table.rule),
                      run_time=t.fill(0.3))
            t.hold()

        pairs = [("es_facts", "ml_patterns", 0),
                 ("es_traced", "ml_harder", 1),
                 ("es_static", "ml_adapts", 2)]
        for left_beat, right_beat, row in pairs:
            with self.beat(left_beat) as t:
                self.play(FadeIn(self.compare[row][0]),
                          FadeIn(self.compare[row][1]), run_time=t.fill(0.4))
                t.hold()
            with self.beat(right_beat) as t:
                self.play(FadeIn(self.compare[row][2]), run_time=t.fill(0.4))
                t.hold()

        with self.beat("es_narrow") as t:
            self.play(FadeIn(self.compare[3][0]),
                      FadeIn(self.compare[3][1]), run_time=t.fill(0.4))
            t.hold()

        with self.beat("store_example") as t:
            self.say(t, "a shop's products, prices and returns policy",
                     fraction=0.4)
            t.hold()

        with self.beat("ml_large") as t:
            self.play(FadeIn(self.compare[3][2]), run_time=t.fill(0.4))
            t.hold()

        with self.beat("neither") as t:
            self.wipe(t)
            self.title(t, "Neither suits every problem", fraction=0.12,
                       color=TERRACOTTA)
            t.hold()

        with self.beat("explain_how") as t:
            line = prose("Say how each one produces its result.", BODY_SIZE,
                         CHARCOAL)
            self.place(line, self.head, buff=GAP_LG)
            self.play(Write(line), run_time=t.fill(0.45))
            t.hold()

    # ---------------------------------------------------- 11. one example

    def one_example(self):
        house = ControlLoop()
        self.house = house

        with self.beat("example_open") as t:
            self.section(t, "Back to the greenhouse", EXAMPLE)
            t.hold()

        with self.beat("ex_sensor") as t:
            note = house.detail(0, "the soil")
            self.play(Create(house.boxes[0]), FadeIn(house.labels[0]),
                      FadeIn(note), run_time=t.fill(0.4))
            t.hold()

        with self.beat("ex_sends") as t:
            self.play(Create(house.boxes[1]), FadeIn(house.labels[1]),
                      Create(house.arrow_into(1)), run_time=t.fill(0.4))
            t.hold()

        with self.beat("ex_compares") as t:
            note = house.detail(1, "against the target")
            self.play(FadeIn(note), *house.light(1), run_time=t.fill(0.4))
            t.hold()

        with self.beat("ex_below") as t:
            self.say(t, "below the target: act", fraction=0.4)
            t.hold()

        with self.beat("ex_valve") as t:
            note = house.detail(2, "the water valve")
            self.play(Create(house.boxes[2]), FadeIn(house.labels[2]),
                      Create(house.arrow_into(2)), FadeIn(note),
                      *house.settle(1), run_time=t.fill(0.45))
            t.hold()

        with self.beat("ex_again") as t:
            self.play(Create(house.feedback),
                      FadeIn(house.feedback_label), run_time=t.fill(0.45))
            t.hold()

        with self.beat("ex_that_is") as t:
            self.say(t, "that is automated feedback control", fraction=0.4,
                     color=TERRACOTTA)
            t.hold()

        with self.beat("ex_robot") as t:
            self.wipe(t)
            self.title(t, "A robot in the same greenhouse", fraction=0.14)
            line = prose("It moves between the beds and reads several areas.",
                         BODY_SIZE, CHARCOAL, 11.4)
            self.place(line, self.head, buff=GAP_LG * 0.9)
            self.robot_line = line
            self.play(FadeIn(line), run_time=t.fill(0.4))
            t.hold()

        with self.beat("ex_robot_parts") as t:
            parts, each = chips(["Sensors", "A processor", "Actuators"],
                                size=LABEL_SIZE, rows=1)
            self.place(parts, self.robot_line, buff=GAP_LG * 0.8)
            self.play(FadeIn(parts), run_time=t.fill(0.4))
            t.hold()

        with self.beat("ex_ai") as t:
            self.wipe(t)
            self.title(t, "And AI on the readings", fraction=0.12)
            t.hold()

        with self.beat("ex_expert") as t:
            line = prose("A rule-based expert system: how much water this "
                         "crop needs.", BODY_SIZE, CHARCOAL, 11.4)
            self.place(line, self.head, buff=GAP_LG * 0.9)
            self.ai_first = line
            self.play(FadeIn(line), run_time=t.fill(0.45))
            t.hold()

        with self.beat("ex_ml") as t:
            line = prose("A machine-learning model: which conditions grew "
                         "the best crop before.", BODY_SIZE, CHARCOAL, 11.4)
            self.place(line, self.ai_first, buff=GAP_MD * 1.3)
            self.ai_second = line
            self.play(FadeIn(line), run_time=t.fill(0.45))
            t.hold()

        with self.beat("ex_depends") as t:
            self.say(t, "all of it rests on reliable sensors and suitable "
                        "data", fraction=0.4)
            t.hold()

    # ---------------------------------------------------------- 12. recap

    def recap(self):
        groups = [
            (["recap_open", "r_processor", "r_loop"], 0),
            (["r_benefits", "r_costs"], 1),
            (["r_robot", "r_robot_parts", "r_ai", "r_adapt"], 2),
            (["r_expert", "r_engine", "r_ml", "r_unreliable"], 3),
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

        with self.beat("exam_order") as t:
            self.wipe(t)
            self.title(t, "In the exam", fraction=0.1)
            rule = callout(["Describe the process in order.",
                            "Use the scenario's own details.",
                            "Give both the benefit and the limit."],
                           size=LABEL_SIZE, width=9.6)
            self.place(rule, self.head, buff=GAP_LG * 0.9)
            self.rule = rule
            self.play(Create(rule[0]), run_time=t.fill(0.2))
            self.play(FadeIn(rule[1][0]), run_time=t.fill(0.22))
            t.hold()

        with self.beat("evaluations") as t:
            self.play(FadeIn(self.rule[1][1]), FadeIn(self.rule[1][2]),
                      run_time=t.fill(0.45))
            t.hold()

        with self.beat("close") as t:
            self.wipe(t)
            self.title(t, "Answer these yourself", fraction=0.1)
            asked, rows = numbered(ASK_YOURSELF, size=MARGIN_SIZE,
                                   gap=GAP_SM * 0.9)
            self.place(asked, self.head, buff=GAP_MD)
            self.play(FadeIn(asked), run_time=t.fill(0.4))
            t.hold()

        with self.beat("questions") as t:
            # One line, not two: a wrapped band line under a seven-row
            # list leaves a gap the guard passes and the eye does not.
            self.say(t, "and work the book's questions too", fraction=0.4)
            t.hold()

    # ------------------------------------------------------- scaffolding

    @contextmanager
    def beat(self, name):
        self._beat_name = name
        with super().beat(name) as timer:
            yield timer

    def section(self, t, text, index, fraction=0.14):
        """Open one of the twelve: clear, light the strip, name it."""
        self.wipe(t)
        if self.strip not in self.mobjects:
            self.play(FadeIn(self.strip), run_time=t.fill(0.05))
            self.keep = [self.margin, self.strip]
            self.floor = FLOOR
        head = fit(serif(text, TITLE_SIZE, CHARCOAL))
        head.to_edge(UP, buff=GAP_MD * 1.7)
        # The strip lights while the heading writes, as one play: the
        # shortest section opening here cannot afford three.
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
