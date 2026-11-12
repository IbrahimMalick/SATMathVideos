"""The AP CSA cohort ad, house style: no footage, the teaching on screen.

Same voiceover and the same beats as scenes/ads/apcsa_cohort.py, but with
nothing borrowed. Where that cut keeps the client's AI b-roll of a family
at a kitchen table, this one puts up the thing the family is paying for:
a loop, and a trace table filling in beside it, one pass at a time. A
parent watching sees what two hours a week actually look like.

The through-line is that table. It appears empty while the problem is
being stated, goes away while the offer is made, and comes back to be
filled while the voice describes how the course teaches. The last row
produces the answer the println was waiting for, and that lands on "it
runs".

Its numbers are not typed. components.ad_house runs the loop in Python
and the table takes the result, so the figures on screen cannot drift
away from the code above them.

Nothing is scaled to fit. Each figure raises if a label will not fit the
width it is given, which is why the code is spaced tightly: at the 28px
floor the roomier spacing leaves no frame for the table beside it.

    python build/render.py scripts/APCSA-cohort-ad.md \\
        audio/APCSA-cohort-ad.m4a --scene ads.apcsa_house

Timing: timings/ads.apcsa_house.json
"""

from contextlib import contextmanager

from manim import (
    AnimationGroup,
    Create,
    FadeIn,
    FadeOut,
    Line,
    VGroup,
    Write,
    DOWN,
    RIGHT,
    config,
)

from brand import (
    BODY_SIZE,
    CHARCOAL,
    DISPLAY_SIZE,
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
from components.ad_caption import (
    ACCENTS_CREAM,
    BRAND,
    COHORT,
    EXAM,
    FACTS,
    PHONE,
    SCRIPT,
    URL,
    plain_block,
)
from components.ad_house import (
    LOOP_ANSWER,
    LOOP_ROWS,
    dots_row,
    java_block,
    price_compare,
    strike,
    tick,
    timeline,
)
from components.trace_table import TraceTable
from scenes.base import SATScene

SAFE = 12.6
CAPTION = BODY_SIZE
CAP_TOP = -1.52      # captions hang from here
FLOOR = -3.45       # no chapter strip on an ad, so the band runs lower

CODE_X = -2.9
TABLE_X = 4.05
# The hero sits high enough that the output line under the code panel
# clears the caption band. At 1.15 the "?" landed on the first caption,
# which the overlap check caught eleven times over.
HERO_Y = 1.5

WEEKS = "25 weeks"   # Nov 16 2026 to May 12 2027 is 177 days


def fit(mobject, width=SAFE, what="this"):
    if mobject.width > width:
        raise ValueError(
            f"{what} is {mobject.width:.2f} units wide, over the "
            f"{width:.2f} the frame allows. Shorten the copy.")
    return mobject


class ApcsaHouse(SATScene):
    scene_id = "ads.apcsa_house"

    def construct(self):
        self.shown = []
        self.hero = []
        self.build_figures()

        self.the_problem()
        self.the_offer()
        self.the_teaching()
        self.the_plan()
        self.end_card()

    # -------------------------------------------------------------- figures

    def build_figures(self):
        self.code = java_block()
        self.code.move_to([0, HERO_Y, 0])

        self.table = TraceTable(
            ["i", "sum"], LOOP_ROWS, start=("-", 0), row_height=0.55)
        self.table.hidden()
        self.table.move_to([TABLE_X, HERO_Y, 0])

        self.answer = mono(LOOP_ANSWER, LABEL_SIZE, SLATE)
        self.answer.next_to(self.code, DOWN, buff=GAP_SM * 1.4)
        self.answer.move_to([self.code.get_center()[0],
                             self.answer.get_center()[1], 0])
        self.check = tick()

        self.unknown = serif("?", TITLE_SIZE, TERRACOTTA)

    # ------------------------------------------------------------ the problem

    def the_problem(self):
        with self.beat("stuck") as t:
            self.play(Create(self.code.box), Write(self.code.body),
                      run_time=t.fill(0.55))
            self.hero = [self.code]
            self.caption(t, "stuck", fraction=0.28)
            t.hold()

        with self.beat("alone") as t:
            # The code slides over to make room for the table it is about
            # to be traced into.
            self.play(self.code.animate.move_to([CODE_X, HERO_Y, 0]),
                      run_time=t.fill(0.22))
            self.unknown.next_to(self.code, DOWN, buff=GAP_SM * 1.4)
            self.unknown.move_to([CODE_X, self.unknown.get_center()[1], 0])
            self.play(Write(self.table.head), Create(self.table.rule),
                      FadeIn(self.unknown), run_time=t.fill(0.3))
            self.hero = [self.code, self.table, self.unknown]
            self.caption(t, "alone", fraction=0.22)
            t.hold()

        for beat in ("first_ap", "opens"):
            with self.beat(beat) as t:
                self.caption(t, beat, fraction=0.42)
                t.hold()

        with self.beat("structure") as t:
            self.clear_hero(t, fraction=0.14)
            self.caption(t, "structure", fraction=0.35)
            t.hold()

        with self.beat("not_200") as t:
            amount = serif("$200 / hour", DISPLAY_SIZE, CHARCOAL)
            amount.move_to([0, HERO_Y - 0.2, 0])
            self.play(Write(amount), run_time=t.fill(0.3))
            # Keep the line that goes on screen. Calling strike() again
            # for self.hero makes a second, different object, and then
            # clear_hero fades a line nobody can see while the real one
            # stays up for the rest of the ad.
            mark = strike(amount)
            self.play(Create(mark), run_time=t.fill(0.18))
            self.hero = [amount, mark]
            self.caption(t, "not_200", fraction=0.2)
            t.hold()

    # -------------------------------------------------------------- the offer

    def the_offer(self):
        with self.beat("capped") as t:
            self.clear_hero(t, fraction=0.12)
            seats = dots_row(10, lit=10, lit_color=SLATE)
            seats.move_to([0, HERO_Y - 0.1, 0])
            self.play(FadeIn(seats), run_time=t.fill(0.3))
            self.hero = [seats]
            self.caption(t, "capped", fraction=0.26)
            t.hold()

        for beat in ("tutor", "two_hours"):
            with self.beat(beat) as t:
                self.caption(t, beat, fraction=0.45)
                t.hold()

    # ----------------------------------------------------------- the teaching

    def the_teaching(self):
        with self.beat("trace") as t:
            self.clear_hero(t, fraction=0.1)
            self.code.move_to([CODE_X, HERO_Y, 0])
            self.unknown.next_to(self.code, DOWN, buff=GAP_SM * 1.4)
            self.unknown.move_to([CODE_X, self.unknown.get_center()[1], 0])
            self.play(FadeIn(self.code), FadeIn(self.table.head),
                      FadeIn(self.table.rule), FadeIn(self.unknown),
                      run_time=t.fill(0.26))
            self.hero = [self.code, self.table, self.unknown]
            # The starting state and the first pass arrive together, so
            # that when the voice asks what i is on the second pass the
            # table is about to answer rather than still on the first.
            self.play(*self.table.step(0), *self.table.step(1),
                      run_time=t.fill(0.22))
            self.caption(t, "trace", fraction=0.2)
            t.hold()

        # One row per beat after that, so the table fills at the speed the
        # voice describes it rather than all at once at the end.
        for beat, row in (("second_pass", 2), ("topics", 3), ("frq", 4)):
            with self.beat(beat) as t:
                self.play(*self.table.step(row), run_time=t.fill(0.3))
                self.caption(t, beat, fraction=0.3)
                t.hold()

        with self.beat("one_line") as t:
            self.answer.move_to(self.unknown)
            self.play(FadeOut(self.unknown), FadeIn(self.answer),
                      run_time=t.fill(0.2))
            self.hero = [self.code, self.table, self.answer]
            self.caption(t, "one_line", fraction=0.25)
            t.hold()

        with self.beat("it_runs") as t:
            self.check.next_to(self.answer, RIGHT, buff=GAP_MD)
            self.play(self.answer.animate.set_color(SAGE),
                      Create(self.check),
                      *[cell.animate.set_color(CHARCOAL)
                        for cell in self.table.rows[-1]],
                      run_time=t.fill(0.3))
            self.hero = [self.code, self.table, self.answer, self.check]
            self.caption(t, "it_runs", fraction=0.25)
            t.hold()

    # --------------------------------------------------------------- the plan

    def the_plan(self):
        with self.beat("exam_day") as t:
            self.clear_hero(t, fraction=0.12)
            line = timeline([("Starts Nov 16", 0.0), ("AP exam May 12", 1.0)])
            line.move_to([0, HERO_Y - 0.1, 0])
            self.weeks = serif(WEEKS, LABEL_SIZE, GREY)
            self.weeks.next_to(line.rail, DOWN, buff=GAP_SM * 1.2)
            self.weeks.move_to([0, self.weeks.get_center()[1], 0])
            self.play(Create(line.rail), run_time=t.fill(0.22))
            self.play(FadeIn(line.ticks), FadeIn(line.labels),
                      run_time=t.fill(0.28))
            self.hero = [line]
            self.caption(t, "exam_day", fraction=0.25)
            t.hold()

        with self.beat("a_plan") as t:
            self.play(FadeIn(self.weeks), run_time=t.fill(0.25))
            self.hero = self.hero + [self.weeks]
            self.caption(t, "a_plan", fraction=0.35)
            t.hold()

        with self.beat("price") as t:
            self.clear_hero(t, fraction=0.1)
            table = price_compare([("One-to-one tutor", "$200 / hour"),
                                   ("This cohort", "$100 / month")])
            table.move_to([0, HERO_Y - 0.1, 0])
            table[1][0].set_color(CHARCOAL)
            table[1][1].set_color(SAGE)
            self.play(FadeIn(table[0]), run_time=t.fill(0.16))
            mark = strike(table.amounts[0])
            self.play(Create(mark), run_time=t.fill(0.12))
            self.play(FadeIn(table[1]), run_time=t.fill(0.22))
            self.hero = [table, mark]
            self.caption(t, "price", fraction=0.2)
            t.hold()

        with self.beat("when") as t:
            self.caption(t, "when", fraction=0.4)
            t.hold()

    # --------------------------------------------------------------- end card

    def end_card(self):
        half_h = config.frame_height / 2
        brand = fit(serif(BRAND, DISPLAY_SIZE, CHARCOAL), what="the brand")
        brand.move_to([0, half_h * 0.59, 0])
        cohort = fit(serif(COHORT, 38, SLATE), what="the cohort line")
        cohort.move_to([0, half_h * 0.36, 0])
        rule = Line([-4.0, 0, 0], [4.0, 0, 0], color=GREY, stroke_width=2)
        rule.move_to([0, half_h * 0.24, 0])
        facts = VGroup(*[fit(serif(line, LABEL_SIZE, GREY), what=line)
                         for line in FACTS])
        facts.arrange(DOWN, buff=GAP_SM * 1.1)
        facts.move_to([0, half_h * 0.03, 0])
        url = fit(serif(URL, DISPLAY_SIZE, TERRACOTTA), what="the url")
        url.move_to([0, -half_h * 0.29, 0])
        phone = fit(serif(PHONE, TITLE_SIZE, CHARCOAL), what="the phone")
        phone.move_to([0, -half_h * 0.53, 0])
        exam = fit(serif(EXAM, MARGIN_SIZE, GREY), what="the exam line")
        exam.move_to([0, -half_h * 0.78, 0])

        rows = [brand, cohort, rule, facts, url, phone, exam]
        for upper, lower in zip(rows, rows[1:]):
            if upper.get_bottom()[1] - lower.get_top()[1] < 0.08:
                raise ValueError("End card rows overlap.")

        with self.beat("brand") as t:
            self.wipe(t, fraction=0.5)
            self.play(FadeIn(brand), run_time=t.fill(0.3))
            t.hold()

        with self.beat("cohort") as t:
            self.play(FadeIn(cohort), FadeIn(rule), FadeIn(facts),
                      run_time=t.fill(0.35))
            t.hold()

        with self.beat("url") as t:
            self.play(FadeIn(url), run_time=t.fill(0.3))
            t.hold()

        with self.beat("phone") as t:
            self.play(FadeIn(phone), FadeIn(exam), run_time=t.fill(0.26))
            t.hold()

    # --------------------------------------------------------------- helpers

    CAPTIONS = {beat: (mode, lines) for beat, mode, lines in SCRIPT}

    def caption(self, t, beat, fraction=0.3):
        """The line under the figure, in the same copy as the other cuts."""
        mode, lines = self.CAPTIONS[beat]
        wanted = (list(lines) if mode == "set"
                  else [text for text, _ in self.shown] + list(lines))
        block = plain_block(wanted, CAPTION, SAFE, ACCENTS_CREAM)
        block.move_to([0, CAP_TOP - block.height / 2, 0])
        if block.get_bottom()[1] < FLOOR:
            raise ValueError(
                f"Beat '{beat}': the caption reaches "
                f"y={block.get_bottom()[1]:.2f}, below y={FLOOR}.")

        if mode == "set":
            arriving = AnimationGroup(*[FadeIn(line) for line in block])
            if self.shown:
                moves = [AnimationGroup(
                    AnimationGroup(*[FadeOut(m) for _, m in self.shown]),
                    arriving, lag_ratio=0.55)]
            else:
                moves = [arriving]
            self.shown = list(zip(wanted, block))
        else:
            kept = len(self.shown)
            moves = [old.animate.move_to(new.get_center())
                     for (_, old), new in zip(self.shown, block[:kept])]
            moves += [FadeIn(line) for line in block[kept:]]
            self.shown = (list(self.shown)
                          + list(zip(wanted[kept:], block[kept:])))
        self.play(*moves, run_time=t.fill(fraction))

    def clear_hero(self, t, fraction=0.12):
        """Fade the figure, leaving the caption alone.

        Create() on a group's children puts the children in the scene and
        not the group, so this matches both ways round rather than asking
        the scene for something it never held.
        """
        family = set()
        for group in self.hero:
            family.update(id(m) for m in group.get_family())
        present = [m for m in self.mobjects
                   if any(id(child) in family for child in m.get_family())]
        if present:
            self.play(*[FadeOut(m) for m in present],
                      run_time=t.fill(fraction))
        self.hero = []

    def wipe(self, t, fraction=0.1):
        old = list(self.mobjects)
        if old:
            self.play(*[FadeOut(m) for m in old], run_time=t.fill(fraction))
        self.hero, self.shown = [], []

    _beat_name = "(before the first beat)"

    @contextmanager
    def beat(self, name):
        self._beat_name = name
        with super().beat(name) as timer:
            yield timer
