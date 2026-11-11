"""AP Computer Science A — exam strategy, the video companion.

A strategy lecture has no worked example to carry it, so the spine is the
exam itself: how it splits, where the marks sit, what changed, and what to
do in each section. The two figures that do real work are the section
split and the unit weighting, because both turn numbers a student would
otherwise just hear into a shape they can remember.

Every claim on screen was checked against College Board pages before this
was built, and every one held:

  * 42 multiple-choice questions, 90 minutes, 55%; four free-response
    questions, 90 minutes, 45%; digital, in Bluebook; Java Quick Reference
    provided.
  * the four units and their multiple-choice ranges, exactly as named:
    Using Objects and Methods 15-25%, Selection and Iteration 25-35%,
    Class Creation 10-18%, Data Collections 30-40%.
  * the free-response focuses: Methods and Control Structures, Class
    Design, Data Analysis with ArrayList, 2D Array.
  * inheritance removed; text files and data sets added; five
    computational thinking practices.
  * College Board's own wording that earlier questions "do not completely
    align with the current AP CSA Exam".

No newer Course and Exam Description has been issued since the one
effective Fall 2025, so the lecture's framing is current for 2026-27.

Where the delivery slips, the screen carries the correct form. Four,
each confirmed on a second pass with a larger model:

  * "it has two scenarios" — two SECTIONS.
  * "four free response questions worth 45 minutes" — 45 PERCENT, which
    he corrects himself one sentence later.
  * "a fifth computational thinking practice, using computers reasonably"
    — the practice is Use Computers RESPONSIBLY.
  * in the wrap-up the list runs together and comes out saying text-file
    reading is out of scope. It is inheritance that is out; text files are
    in. The recap card says so, and this is the one line worth a pickup.

The rest are transcription artefacts over a delivery that was right:
"exam authority" is exam strategy, "multiple choice waiting" is weighting,
"every list" and "ArrayLess" are ArrayList, "Tacing" is pacing, "math and
return values" is method return values, "court problem solving" is core
problem solving, and "the current CD" is the current CED.

The recording carried a false start on the wrap-up, slated out loud as
"take two, wrap up"; build/retake.py removed the attempt and the slate
together. There was one opening take, not two: the first twenty-six
seconds of the file are silence.

Timing: timings/cs.ap_csa_strategy.json
Render: python build/render.py scripts/APCSA-exam-strategy.md \\
    audio/APCSA-exam-strategy.m4a
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
from components.exam_shape import SectionSplit, WeightBars, chip_row
from components.syllabus_map import TopicStrip
from scenes.base import SATScene

FRAME_SAFE = 12.6
FLOOR = -3.1          # the chapter strip owns everything below this

PARTS = ["Format", "Weighting", "Changes", "Multiple choice",
         "Free response", "Practice"]

UNITS = [
    ("Unit 1: Using Objects and Methods", 15, 25),
    ("Unit 2: Selection and Iteration", 25, 35),
    ("Unit 3: Class Creation", 10, 18),
    ("Unit 4: Data Collections", 30, 40),
]

SECTIONS = [
    ("Section I", "Multiple choice\n42 questions · 90 min", 55),
    ("Section II", "Free response\n4 questions · 90 min", 45),
]

WATCH = ["integer division", "casts", "operator order",
         "String comparisons", "method return values", "array indexes",
         "loop bounds"]

FRQ = [
    ("1", "Methods and Control Structures"),
    ("2", "Class Design"),
    ("3", "Data Analysis with ArrayList"),
    ("4", "2D Array"),
]


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


def strike(mobject, color=GREY, stroke=3):
    """A line through a claim that no longer applies."""
    return Line(mobject.get_left() + LEFT * 0.08,
                mobject.get_right() + RIGHT * 0.08,
                color=color, stroke_width=stroke)


class ApCsaStrategy(SATScene):
    scene_id = "cs.ap_csa_strategy"

    def construct(self):
        self.margin = mono("AP Computer Science A · Exam Strategy",
                           MARGIN_SIZE)
        self.margin.to_corner(UP + LEFT, buff=GAP_SM)
        self.add(self.margin)

        self.strip = TopicStrip(len(PARTS), lit=SLATE, side=0.6)
        self.strip.to_edge(DOWN, buff=GAP_SM * 0.5)
        self.add(self.strip)

        self.keep = [self.margin, self.strip]
        self.head = None
        self.note = None

        self.opening()
        self.the_goal()
        self.exam_shape()
        self.quick_reference()
        self.four_units()
        self.weighting()
        self.study_advice()
        self.additions()
        self.in_and_out()
        self.current_materials()
        self.trace_the_code()
        self.trace_method()
        self.watch_for()
        self.when_stuck()
        self.frq_checklist()
        self.write_clearly()
        self.four_focuses()
        self.practice_routine()
        self.wrap_up()

    # -------------------------------------------------------------- helpers

    _beat_name = "(before the first beat)"

    @contextmanager
    def beat(self, name):
        self._beat_name = name
        with super().beat(name) as timer:
            yield timer

    def clear(self, t, *groups, fraction=0.1):
        """Fade a figure that was drawn child by child.

        Create() on a group's children adds the children to the scene, not
        the group, so FadeOut(group) removes something the scene never held.
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
        self.head = self.note = None

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
    # would leave content sitting over the chapter strip. They say so.

    def stack(self, group, top=None, buff=GAP_MD, floor=FLOOR, align=ORIGIN):
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

    def place(self, mobject, top=None, buff=GAP_MD, floor=FLOOR):
        for factor in (1.0, 0.9, 0.78, 0.66, 0.55, 0.45, 0.35):
            if top is None:
                mobject.move_to(ORIGIN)
            else:
                mobject.next_to(top, DOWN, buff=buff * factor)
            if mobject.get_bottom()[1] >= floor:
                return mobject
        raise ValueError(
            f"Beat '{self._beat_name}': no room under this content for "
            f"something {mobject.height:.2f} units tall above y={floor}."
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

    def say(self, t, text, fraction=0.2, color=GREY, size=LABEL_SIZE,
            y=None, anchor=None, buff=GAP_MD):
        """The running line of commentary, swapped in place."""
        line = prose(text, size, color)
        if anchor is not None:
            self.place(line, anchor, buff=buff)
        else:
            line.move_to([0, FLOOR + 0.35 if y is None else y, 0])
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
        laid across a chart's bars reads as clean: a bar is a shape, not
        text. The band at the bottom of the frame is reserved for one line
        of commentary, and this is what reserves it.
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
                    f"Beat '{self._beat_name}': the commentary band is not "
                    f"clear \u2014 something already reaches down into it by "
                    f"{high:.2f} units. Raise the content above the band."
                )

    def drop_note(self, t, fraction=0.05):
        if self.note is not None and self.note in self.mobjects:
            self.play(FadeOut(self.note), run_time=t.fill(fraction))
        self.note = None

    # ------------------------------------------------ welcome and alignment

    def opening(self):
        with self.beat("open") as t:
            self.part(t, 0)
            head = VGroup(
                serif("AP Computer Science A", TITLE_SIZE, CHARCOAL),
                serif("Exam Strategy", DISPLAY_SIZE, TERRACOTTA),
            ).arrange(DOWN, buff=GAP_SM * 1.4)
            fit(head)
            head.move_to(UP * 1.5)
            self.play(Write(head[0]), run_time=t.fill(0.3))
            self.play(Write(head[1]), run_time=t.fill(0.35))
            self.card_head = head
            t.hold()
        with self.beat("right_exam") as t:
            check = prose("First, let's make sure you are preparing for the "
                          "right exam.", LABEL_SIZE, GREY)
            self.place(check, self.card_head, buff=GAP_LG * 0.8)
            self.play(FadeIn(check), run_time=t.fill(0.3))
            self.check_line = check
            t.hold()
        with self.beat("aligned") as t:
            self.play(FadeOut(self.check_line), run_time=t.fill(0.06))
            stamp = self.lines(
                "Aligned with the College Board CED",
                "Effective Fall 2025",
                "Current for the 2026–27 school year",
                size=LABEL_SIZE, color=CHARCOAL,
            )
            stamp[1].set_color(SLATE)
            stamp[2].set_color(SLATE)
            self.stack(stamp, self.card_head, buff=GAP_MD * 1.1)
            self.hide(stamp)
            self.reveal(t, stamp, 0, 1, 0.3)
            self.stamp = stamp
            t.hold()
        with self.beat("ced") as t:
            self.reveal(t, self.stamp, 1, 2, 0.4)
            t.hold()
        with self.beat("digital_note") as t:
            self.reveal(t, self.stamp, 2, 3, 0.35)
            t.hold()

    def the_goal(self):
        with self.beat("goal") as t:
            self.wipe(t)
            head = self.title(t, "The goal today", fraction=0.14)
            wrong = prose("memorise a pile of tricks", BODY_SIZE, GREY)
            self.place(wrong, head, buff=GAP_LG * 0.9)
            self.play(FadeIn(wrong), run_time=t.fill(0.2))
            self.play(Create(strike(wrong)), run_time=t.fill(0.2))
            self.wrong = VGroup(wrong)
            t.hold()
        with self.beat("goal_real") as t:
            right = self.lines(
                "a reliable way to read, reason about",
                "and write Java under timed conditions",
                size=BODY_SIZE, color=CHARCOAL,
            )
            self.stack(right, self.wrong, buff=GAP_LG * 0.8)
            self.play(Write(right), run_time=t.fill(0.4))
            t.hold()

    # ------------------------------------------------- the shape of the exam

    def exam_shape(self):
        with self.beat("exam") as t:
            self.wipe(t)
            head = self.title(t, "The exam you are taking", fraction=0.12)
            digital = prose("Fully digital, taken in Bluebook",
                            LABEL_SIZE, SLATE)
            self.place(digital, head, buff=GAP_MD * 0.9)
            self.play(FadeIn(digital), run_time=t.fill(0.3))
            self.digital = digital
            t.hold()
        with self.beat("two_sections") as t:
            # He says "two scenarios"; the exam has two SECTIONS.
            self.say(t, "Two sections", fraction=0.25, color=CHARCOAL,
                     size=BODY_SIZE, anchor=self.digital, buff=GAP_MD * 1.1)
            t.hold()

        split = SectionSplit(SECTIONS)
        split.move_to([0, -1.25, 0])

        with self.beat("mcq") as t:
            self.play(Create(split.blocks[0][0]), run_time=t.fill(0.2))
            self.play(FadeIn(split.captions[0]), run_time=t.fill(0.25))
            t.hold()
        with self.beat("mcq_pct") as t:
            self.play(Write(split.blocks[0][1]), run_time=t.fill(0.3))
            t.hold()
        with self.beat("frq") as t:
            self.play(Create(split.blocks[1][0]), run_time=t.fill(0.2))
            self.play(FadeIn(split.captions[1]), run_time=t.fill(0.25))
            t.hold()
        with self.beat("split") as t:
            # "worth 45 minutes" in the delivery; it is 45 PERCENT, and he
            # says so himself in the next breath.
            self.play(Write(split.blocks[1][1]), run_time=t.fill(0.3))
            self.split = split
            t.hold()

    def quick_reference(self):
        with self.beat("quickref") as t:
            self.wipe(t)
            head = self.title(t, "Two things to use well", fraction=0.1)
            rows = self.lines(
                "The Java Quick Reference is in Bluebook",
                "About two minutes per question",
                size=BODY_SIZE, align=LEFT,
            )
            self.stack(rows, head, buff=GAP_LG * 0.9, align=LEFT, floor=-2.35)
            self.hide(rows)
            self.reveal(t, rows, 0, 1, 0.3)
            self.two_things = rows
            t.hold()
        with self.beat("quickref_use") as t:
            self.say(t, "Confirm a method with it, do not reason with it.",
                     fraction=0.3)
            t.hold()
        with self.beat("pacing") as t:
            self.drop_note(t)
            self.reveal(t, self.two_things, 1, 2, 0.3)
            t.hold()
        with self.beat("keep_moving") as t:
            self.say(t, "One hard question, three easy ones lost.", fraction=0.3)
            t.hold()

    # ------------------------------------------------ the four units, weighted

    def four_units(self):
        with self.beat("units") as t:
            self.part(t, 1)
            self.wipe(t)
            head = self.title(t, "Four units", fraction=0.12)
            rows = self.lines(*[name for name, _, _ in UNITS],
                              size=BODY_SIZE, align=LEFT)
            self.stack(rows, head, buff=GAP_MD * 1.3, align=LEFT, floor=-2.35)
            self.hide(rows)
            self.unit_rows = rows
            t.hold()
        for index, name in enumerate(["u1", "u2", "u3", "u4"]):
            with self.beat(name) as t:
                self.reveal(t, self.unit_rows, index, index + 1, 0.35)
                t.hold()

    def weighting(self):
        # The bars stop well above the commentary band: at the full
        # pitch the last row's bar runs straight under the caption.
        bars = WeightBars(UNITS, pitch=0.72, highlight=3)

        with self.beat("weighting") as t:
            self.wipe(t)
            head = self.title(t, "Where the marks are", fraction=0.09)
            self.place(bars, head, buff=GAP_MD * 0.8, floor=-2.3)
            self.play(Create(bars), run_time=t.fill(0.45))
            self.bars = bars
            t.hold()
        with self.beat("w2") as t:
            self.play(*bars.settle(3), *bars.light(1), run_time=t.fill(0.3))
            t.hold()
        with self.beat("w13") as t:
            self.play(*bars.settle(1), run_time=t.fill(0.3))
            t.hold()
        with self.beat("plan") as t:
            self.say(t, "Use the ranges to plan your review.", fraction=0.3,
                     color=CHARCOAL, size=BODY_SIZE)
            t.hold()

    def study_advice(self):
        with self.beat("arrays_time") as t:
            self.wipe(t)
            head = self.title(t, "So plan your review like this",
                              fraction=0.1)
            rows = self.lines(
                "Give arrays, ArrayList and 2D arrays serious time",
                "Keep practising loops and conditionals",
                "Do not skip methods, objects or class design",
                size=BODY_SIZE, align=LEFT,
            )
            self.stack(rows, head, buff=GAP_MD * 1.3, align=LEFT, floor=-2.35)
            self.hide(rows)
            self.reveal(t, rows, 0, 1, 0.35)
            self.advice = rows
            t.hold()
        with self.beat("loops_too") as t:
            self.reveal(t, self.advice, 1, 2, 0.35)
            t.hold()
        with self.beat("dont_skip") as t:
            self.reveal(t, self.advice, 2, 3, 0.3)
            every = prose("Every unit can appear.", LABEL_SIZE, TERRACOTTA)
            self.place(every, self.advice, buff=GAP_MD * 1.2)
            self.play(FadeIn(every), run_time=t.fill(0.25))
            t.hold()

    # ----------------------------------------------------- what changed

    def additions(self):
        with self.beat("changed") as t:
            self.part(t, 2)
            self.wipe(t)
            head = self.title(t, "What the revision added", fraction=0.1)
            rows = self.lines(
                "Data sets and data analysis",
                "How data was collected, and whether it is biased",
                "Reading text files with File and Scanner",
                "A fifth practice: Use Computers Responsibly",
                size=BODY_SIZE, align=LEFT,
            )
            self.stack(rows, head, buff=GAP_MD * 1.2, align=LEFT, floor=-2.35)
            self.hide(rows)
            self.reveal(t, rows, 0, 1, 0.3)
            self.added = rows
            t.hold()
        with self.beat("datasets") as t:
            self.reveal(t, self.added, 1, 2, 0.35)
            t.hold()
        with self.beat("conclusions") as t:
            t.hold()
        with self.beat("files") as t:
            self.reveal(t, self.added, 2, 3, 0.35)
            t.hold()
        with self.beat("practice5") as t:
            # "using computers reasonably" in the delivery; the practice is
            # Use Computers RESPONSIBLY.
            self.reveal(t, self.added, 3, 4, 0.35)
            t.hold()
        with self.beat("ethics") as t:
            self.say(t, "Expect questions on computing and data ethics.", fraction=0.3)
            t.hold()

    def in_and_out(self):
        with self.beat("inheritance") as t:
            self.wipe(t)
            head = self.title(t, "One topic is out", fraction=0.1)
            gone = prose("designing and implementing inheritance "
                         "relationships", BODY_SIZE, GREY)
            self.place(gone, head, buff=GAP_LG * 0.8)
            self.play(FadeIn(gone), run_time=t.fill(0.25))
            self.play(Create(strike(gone)), run_time=t.fill(0.2))
            self.gone = gone
            t.hold()
        with self.beat("still_in") as t:
            keep_head = prose("Still in the framework:", LABEL_SIZE, CHARCOAL)
            self.place(keep_head, self.gone, buff=GAP_LG * 0.8)
            self.play(FadeIn(keep_head), run_time=t.fill(0.3))
            self.keep_head = keep_head
            t.hold()
        with self.beat("still_list") as t:
            kept = chip_row(["arrays", "ArrayList", "2D arrays", "searching",
                             "sorting", "recursion"], size=LABEL_SIZE,
                            color=SAGE, rows=2)
            self.place(kept, self.keep_head, buff=GAP_MD * 0.9)
            self.play(FadeIn(kept), run_time=t.fill(0.4))
            t.hold()

    def current_materials(self):
        with self.beat("lesson") as t:
            self.wipe(t)
            head = self.title(t, "So use current materials", fraction=0.14)
            self.materials_head = head
            t.hold()
        with self.beat("older") as t:
            quote = self.lines(
                "College Board: earlier questions",
                "“do not completely align with",
                "the current AP CSA Exam”",
                size=BODY_SIZE, color=CHARCOAL,
            )
            quote[1].set_color(TERRACOTTA)
            quote[2].set_color(TERRACOTTA)
            self.stack(quote, self.materials_head, buff=GAP_LG * 0.85)
            self.play(Write(quote), run_time=t.fill(0.45))
            t.hold()

    # --------------------------------------------- multiple choice: trace it

    def trace_the_code(self):
        steps = [
            "1.  Read what the question actually asks",
            "2.  Track the variables that change",
            "3.  Check loop conditions and array indexes",
            "4.  Eliminate choices the code rules out",
            "5.  Mark it and come back if needed",
        ]
        with self.beat("trace") as t:
            self.part(t, 3)
            self.wipe(t)
            head = self.title(t, "Multiple choice: trace the code",
                              fraction=0.1)
            rows = self.lines(*steps, size=BODY_SIZE, align=LEFT)
            self.stack(rows, head, buff=GAP_MD * 1.15, align=LEFT, floor=-2.35)
            self.hide(rows)
            self.steps = rows
            t.hold()
        with self.beat("dont_skim") as t:
            self.say(t, "Not what the program looks like it is doing.",
                     fraction=0.3, color=TERRACOTTA)
            t.hold()
        with self.beat("read_stem") as t:
            self.drop_note(t)
            self.reveal(t, self.steps, 0, 1, 0.3)
            t.hold()
        with self.beat("what_asked") as t:
            self.say(t, "Printed output? A final value? A valid segment?",
                     fraction=0.3)
            t.hold()
        with self.beat("walk") as t:
            self.drop_note(t)
            self.reveal(t, self.steps, 1, 2, 0.3)
            t.hold()

    def trace_method(self):
        with self.beat("trace_table") as t:
            self.reveal(t, self.steps, 2, 3, 0.3)
            self.say(t, "A small trace table. One statement at a time.",
                     fraction=0.3)
            t.hold()
        with self.beat("one_stmt") as t:
            t.hold()
        with self.beat("loop_check") as t:
            self.say(t, "Each pass: value before, value after, condition.", fraction=0.35)
            t.hold()

    def watch_for(self):
        with self.beat("watch") as t:
            self.wipe(t)
            head = self.title(t, "Where the marks are lost", fraction=0.1)
            chips = chip_row(WATCH, size=LABEL_SIZE, color=CHARCOAL, rows=2)
            self.place(chips, head, buff=GAP_LG * 0.85)
            self.play(FadeIn(chips), run_time=t.fill(0.4))
            self.chips = chips
            t.hold()
        with self.beat("last_index") as t:
            rule = prose("The last valid index is one less than the length.",
                         BODY_SIZE, TERRACOTTA)
            self.place(rule, self.chips, buff=GAP_LG * 0.85)
            self.play(Write(rule), run_time=t.fill(0.4))
            t.hold()

    def when_stuck(self):
        with self.beat("eliminate") as t:
            self.wipe(t)
            head = self.title(t, "When you are stuck", fraction=0.12)
            rows = self.lines(
                "Eliminate a choice only when the code rules it out",
                "Mark it, collect the easier points, come back",
                size=BODY_SIZE, align=LEFT,
            )
            self.stack(rows, head, buff=GAP_LG * 0.8, align=LEFT, floor=-2.35)
            self.hide(rows)
            self.reveal(t, rows, 0, 1, 0.35)
            self.stuck = rows
            t.hold()
        with self.beat("mark_return") as t:
            self.reveal(t, self.stuck, 1, 2, 0.35)
            t.hold()
        with self.beat("no_debate") as t:
            self.say(t, "Do not negotiate with yourself.", fraction=0.3,
                     color=TERRACOTTA, size=BODY_SIZE,)
            t.hold()

    # ---------------------------------------- free response: follow the spec

    def frq_checklist(self):
        with self.beat("frq_spec") as t:
            self.part(t, 4)
            self.wipe(t)
            head = self.title(t, "Free response: the prompt is a checklist",
                              fraction=0.1)
            rows = self.lines(
                "The required method or constructor",
                "Its parameters and its return type",
                "Every condition it must handle",
                "The examples, used as test cases",
                "The boundary cases",
                size=BODY_SIZE, align=LEFT,
            )
            self.stack(rows, head, buff=GAP_MD * 1.1, align=LEFT, floor=-2.35)
            self.hide(rows)
            self.frq_rows = rows
            t.hold()
        with self.beat("checklist") as t:
            self.reveal(t, self.frq_rows, 0, 1, 0.3)
            t.hold()
        with self.beat("identify") as t:
            self.reveal(t, self.frq_rows, 1, 3, 0.3)
            t.hold()
        with self.beat("examples") as t:
            self.reveal(t, self.frq_rows, 3, 4, 0.3)
            t.hold()
        with self.beat("boundary") as t:
            self.reveal(t, self.frq_rows, 4, 5, 0.25)
            self.say(t, "Empty collection. First or last index. No match.", fraction=0.3)
            t.hold()

    def write_clearly(self):
        with self.beat("clear_java") as t:
            self.wipe(t)
            head = self.title(t, "Write it so it can be read", fraction=0.1)
            rows = self.lines(
                "Braces and indentation, so the structure is obvious",
                "Nothing is compiled during the exam",
                "No reader will repair your punctuation",
                size=BODY_SIZE, align=LEFT,
            )
            self.stack(rows, head, buff=GAP_MD * 1.25, align=LEFT)
            self.hide(rows)
            self.reveal(t, rows, 0, 1, 0.3)
            self.clear_rows = rows
            t.hold()
        with self.beat("braces") as t:
            t.hold()
        with self.beat("not_compiled") as t:
            self.reveal(t, self.clear_rows, 1, 3, 0.3)
            t.hold()
        with self.beat("partial") as t:
            self.say(t, "Stuck? Write the parts you can make correct.", fraction=0.3, color=CHARCOAL)
            t.hold()
        with self.beat("credit") as t:
            self.say(t, "A clear loop or component still earns credit.", fraction=0.35, color=SAGE)
            t.hold()

    def four_focuses(self):
        with self.beat("four_frq") as t:
            self.wipe(t)
            head = self.title(t, "The four free-response focuses",
                              fraction=0.1)
            rows = VGroup()
            for number, name in FRQ:
                row = VGroup(
                    serif(number, TITLE_SIZE, SLATE),
                    prose(name, BODY_SIZE, CHARCOAL, 10.4),
                ).arrange(RIGHT, buff=GAP_MD * 1.1)
                rows.add(row)
            rows.arrange(DOWN, buff=GAP_MD * 1.1, aligned_edge=LEFT)
            fit(rows)
            self.stack(rows, head, buff=GAP_MD * 1.1, align=LEFT)
            self.hide(rows)
            self.focus_rows = rows
            t.hold()
        for index, name in enumerate(["q1", "q2", "q3"]):
            with self.beat(name) as t:
                self.reveal(t, self.focus_rows, index, index + 1, 0.35)
                t.hold()
        with self.beat("q3_shift") as t:
            self.say(t, "Removing as you traverse? The indexes shift.", fraction=0.3, color=TERRACOTTA)
            t.hold()
        with self.beat("q4") as t:
            self.drop_note(t)
            self.reveal(t, self.focus_rows, 3, 4, 0.3)
            t.hold()
        with self.beat("q4_bounds") as t:
            self.say(t, "Keep row and column apart. Match the bounds.", fraction=0.35)
            t.hold()

    # ----------------------------------------------------- practice routine

    def practice_routine(self):
        with self.beat("practice") as t:
            self.part(t, 5)
            self.wipe(t)
            head = self.title(t, "Practise for the exam you are sitting",
                              fraction=0.1)
            rows = self.lines(
                "Use Bluebook, so the digital setting is familiar",
                "Time your multiple-choice sets",
                "Review every answer you missed or guessed",
                "Write FRQs on a timer, then read the mark scheme",
                "Check older questions against the current CED",
                size=BODY_SIZE, align=LEFT,
            )
            self.stack(rows, head, buff=GAP_MD * 1.1, align=LEFT)
            self.hide(rows)
            self.routine = rows
            t.hold()
        with self.beat("bluebook") as t:
            self.reveal(t, self.routine, 0, 1, 0.3)
            t.hold()
        with self.beat("timed") as t:
            self.reveal(t, self.routine, 1, 3, 0.3)
            t.hold()
        with self.beat("frq_timer") as t:
            self.reveal(t, self.routine, 3, 4, 0.3)
            t.hold()
        with self.beat("compare") as t:
            t.hold()
        with self.beat("exact_req") as t:
            self.say(t, "Find the exact requirement you missed. Redo it.", fraction=0.35)
            t.hold()
        with self.beat("current_mats") as t:
            self.drop_note(t)
            t.hold()
        with self.beat("check_old") as t:
            self.reveal(t, self.routine, 4, 5, 0.3)
            t.hold()

    # ------------------------------------------------------------- wrap-up

    def wrap_up(self):
        with self.beat("recap") as t:
            self.wipe(t)
            head = self.title(t, "Your exam strategy", fraction=0.14)
            self.wrap_head = head
            t.hold()
        with self.beat("carry") as t:
            rows = self.lines(
                "Know the current format",
                "Trace code carefully",
                "Follow the FRQ specification",
                "Practise with current materials",
                size=BODY_SIZE, align=LEFT,
            )
            self.stack(rows, head, buff=GAP_MD * 1.2, align=LEFT)
            self.hide(rows)
            self.reveal(t, rows, 0, 2, 0.3)
            self.wrap_rows = rows
            t.hold()
        with self.beat("prioritise") as t:
            self.reveal(t, self.wrap_rows, 2, 4, 0.3)
            t.hold()
        with self.beat("changes") as t:
            self.wipe(t)
            head = self.title(t, "And the changes", fraction=0.1)
            self.changes_head = head
            t.hold()
        with self.beat("changes_list") as t:
            # The delivery runs this list together and ends up saying
            # text-file reading is out of scope. It is inheritance that is
            # out; text files are in. The screen says so.
            rows = self.lines(
                "In: data sets, data ethics, reading text files",
                "Out: designing and implementing inheritance",
                size=BODY_SIZE, align=LEFT,
            )
            rows[0].set_color(SAGE)
            rows[1].set_color(GREY)
            self.stack(rows, self.changes_head, buff=GAP_MD * 1.3, align=LEFT)
            self.play(FadeIn(rows[0]), run_time=t.fill(0.3))
            self.play(FadeIn(rows[1]), run_time=t.fill(0.3))
            self.change_rows = rows
            t.hold()
        with self.beat("four_focus") as t:
            # Numbered even here: two names side by side on one line read
            # as a single item without them.
            focuses = chip_row([f"{number} {name}" for number, name in FRQ],
                               size=LABEL_SIZE, color=CHARCOAL, rows=2)
            self.place(focuses, self.change_rows, buff=GAP_LG * 0.8)
            self.play(FadeIn(focuses), run_time=t.fill(0.4))
            t.hold()
        with self.beat("aligned_again") as t:
            self.wipe(t)
            card = self.lines(
                "Aligned with the AP CSA CED",
                "Effective Fall 2025",
                "Current for the 2026–27 school year",
                size=BODY_SIZE, color=CHARCOAL,
            )
            card[1].set_color(SLATE)
            card[2].set_color(SLATE)
            card.move_to(UP * 0.9)
            self.play(Write(card), run_time=t.fill(0.4))
            self.final_card = card
            t.hold()
        with self.beat("close") as t:
            sign = self.lines(
                "Work from the current framework.",
                "Make every line of code say what you mean.",
                size=BODY_SIZE, color=TERRACOTTA,
            )
            self.stack(sign, self.final_card, buff=GAP_LG * 0.9)
            self.play(Write(sign), run_time=t.fill(0.45))
            t.hold()
