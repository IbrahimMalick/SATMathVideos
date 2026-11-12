"""The AP CSA cohort ad, house style, vertical: the trace table on a phone.

Same voiceover, same beats and the same argument as
scenes/ads/apcsa_house.py: no borrowed footage, and the thing the family
is paying for on screen instead. Laid out for 9:16.

Three things change for the narrow frame, and none of them is a crop.

The code loses a line. "System.out.println(sum);" is 24 characters of
monospace and the frame is 4.5 units wide, so printing it at a size a
phone can read leaves nothing for the trace table underneath. The loop
survives, which is the part being traced; the println becomes the big
answer at the end instead, which is where the eye wants it anyway.

The code and the table stack rather than sitting side by side.

The payoff replaces the figure rather than joining it. In landscape the
answer appears under the code with the filled table still beside it; here
there is no room for all three, so the table hands over to a single large
number and a tick.

Everything stays above y = -2.55, where a Short's own title, channel name
and buttons start.

    python build/render.py scripts/APCSA-cohort-ad-house-vertical.md \\
        audio/APCSA-cohort-ad.m4a -q h -r 1080,1920

Timing: timings/ads.apcsa_house_vertical.json
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

# Portrait: pin the intended 4.5 x 8 frame before anything reads it.
config.frame_height = 8.0
config.frame_width = 4.5

from brand import (  # noqa: E402
    CHARCOAL,
    GAP_MD,
    GAP_SM,
    GREY,
    SAGE,
    SLATE,
    TERRACOTTA,
    mono,
    serif,
)
from components.ad_caption import (  # noqa: E402
    ACCENTS_PORTRAIT,
    BRAND,
    COHORT_PORTRAIT,
    FACTS_PORTRAIT,
    PHONE,
    SCRIPT_PORTRAIT,
    URL,
    plain_block,
)
from components.ad_house import (  # noqa: E402
    LOOP_ANSWER,
    LOOP_ROWS,
    dots_row,
    java_block,
    strike,
    tick,
    timeline,
)
from components.trace_table import TraceTable  # noqa: E402
from scenes.base import SATScene  # noqa: E402

SAFE = 4.1
CAP_TOP = -1.12
FLOOR = -2.55        # a Short's own furniture starts here

CODE = 17            # 17 nominal is 30px at 1080x1920, above the floor
CODE_Y = 2.55
TABLE_Y = 0.55
CAPTION = 24

BRAND_SIZE = 30
COHORT_SIZE = 24
FACT_SIZE = 18
URL_SIZE = 23
PHONE_SIZE = 24
EXAM_SIZE = 18
EXAM_SHORT = "AP exam: May 12, 2027"

# The println is dropped: at a readable size it is wider than the frame,
# and the number it would print is the payoff anyway.
LOOP_ONLY = """int sum = 0;
for (int i=1; i<=4; i++)
    sum += i;"""

WEEKS = "25 weeks"


def fit(mobject, width=SAFE, what="this"):
    if mobject.width > width:
        raise ValueError(
            f"{what} is {mobject.width:.2f} units wide, over the "
            f"{width:.2f} this frame allows. Shorten the copy.")
    return mobject


class ApcsaHouseVertical(SATScene):
    scene_id = "ads.apcsa_house_vertical"

    def construct(self):
        self.shown = []
        self.hero = []

        self.code = java_block(LOOP_ONLY, size=CODE, width=SAFE)
        self.code.move_to([0, CODE_Y, 0])
        self.table = TraceTable(["i", "sum"], LOOP_ROWS, start=("-", 0),
                                size=22, col_width=1.3, row_height=0.42)
        self.table.hidden()
        self.table.move_to([0, TABLE_Y, 0])

        self.the_problem()
        self.the_offer()
        self.the_teaching()
        self.the_plan()
        self.end_card()

    # ------------------------------------------------------------ the problem

    def the_problem(self):
        with self.beat("stuck") as t:
            self.play(Create(self.code.box), Write(self.code.body),
                      run_time=t.fill(0.5))
            self.hero = [self.code]
            self.caption(t, "stuck", fraction=0.3)
            t.hold()

        with self.beat("alone") as t:
            self.play(Write(self.table.head), Create(self.table.rule),
                      run_time=t.fill(0.3))
            self.hero = [self.code, self.table]
            self.caption(t, "alone", fraction=0.3)
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
            amount = fit(serif("$200 / hour", 36, CHARCOAL),
                         what="the hourly rate")
            amount.move_to([0, 1.6, 0])
            self.play(Write(amount), run_time=t.fill(0.3))
            mark = strike(amount)
            self.play(Create(mark), run_time=t.fill(0.18))
            self.hero = [amount, mark]
            self.caption(t, "not_200", fraction=0.2)
            t.hold()

    # -------------------------------------------------------------- the offer

    def the_offer(self):
        with self.beat("capped") as t:
            self.clear_hero(t, fraction=0.12)
            seats = dots_row(10, lit=10, lit_color=SLATE, radius=0.11,
                             gap=GAP_SM * 0.64, width=SAFE)
            seats.move_to([0, 1.6, 0])
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
            self.play(FadeIn(self.code), FadeIn(self.table.head),
                      FadeIn(self.table.rule), run_time=t.fill(0.26))
            self.hero = [self.code, self.table]
            self.play(*self.table.step(0), *self.table.step(1),
                      run_time=t.fill(0.22))
            self.caption(t, "trace", fraction=0.2)
            t.hold()

        for beat, row in (("second_pass", 2), ("topics", 3), ("frq", 4)):
            with self.beat(beat) as t:
                self.play(*self.table.step(row), run_time=t.fill(0.3))
                self.caption(t, beat, fraction=0.3)
                t.hold()

        with self.beat("one_line") as t:
            self.caption(t, "one_line", fraction=0.4)
            t.hold()

        with self.beat("it_runs") as t:
            # The table hands over rather than sharing the frame: three
            # figures do not fit above the caption band here.
            self.clear_hero(t, fraction=0.1)
            answer = mono(LOOP_ANSWER, 64, SAGE)
            mark = tick(size=0.4)
            payoff = VGroup(answer, mark).arrange(RIGHT, buff=GAP_MD)
            payoff.move_to([0, 1.5, 0])
            self.play(FadeIn(answer), Create(mark), run_time=t.fill(0.35))
            self.hero = [payoff]
            self.caption(t, "it_runs", fraction=0.25)
            t.hold()

    # --------------------------------------------------------------- the plan

    def the_plan(self):
        with self.beat("exam_day") as t:
            self.clear_hero(t, fraction=0.12)
            line = timeline([("Nov 16", 0.0), ("May 12", 1.0)],
                            width=3.4, size=EXAM_SIZE)
            line.move_to([0, 1.5, 0])
            self.weeks = serif(WEEKS, EXAM_SIZE, GREY)
            self.weeks.next_to(line.rail, DOWN, buff=GAP_SM)
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
            # Stacked, not side by side: a label and an amount on one line
            # runs wider than this frame at any size worth reading.
            was = fit(serif("$200 / hour", 26, GREY), what="the old price")
            now = fit(serif("$100 / month", 40, SAGE), what="the new price")
            stack = VGroup(was, now).arrange(DOWN, buff=GAP_MD)
            stack.move_to([0, 1.5, 0])
            self.play(FadeIn(was), run_time=t.fill(0.16))
            mark = strike(was)
            self.play(Create(mark), run_time=t.fill(0.12))
            self.play(Write(now), run_time=t.fill(0.25))
            self.hero = [stack, mark]
            self.caption(t, "price", fraction=0.2)
            t.hold()

        with self.beat("when") as t:
            self.caption(t, "when", fraction=0.4)
            t.hold()

    # --------------------------------------------------------------- end card

    def end_card(self):
        brand = fit(serif(BRAND, BRAND_SIZE, CHARCOAL), what="the brand")
        brand.move_to([0, 2.55, 0])
        cohort = VGroup(*[fit(serif(line, COHORT_SIZE, SLATE), what=line)
                          for line in COHORT_PORTRAIT])
        cohort.arrange(DOWN, buff=GAP_SM * 0.8)
        cohort.move_to([0, 1.65, 0])
        rule = Line([-1.5, 0, 0], [1.5, 0, 0], color=GREY, stroke_width=2)
        rule.move_to([0, 1.14, 0])
        facts = VGroup(*[fit(serif(line, FACT_SIZE, GREY), what=line)
                         for line in FACTS_PORTRAIT])
        facts.arrange(DOWN, buff=GAP_SM * 0.75)
        facts.move_to([0, 0.28, 0])
        url = fit(serif(URL, URL_SIZE, TERRACOTTA), what="the url")
        url.move_to([0, -0.85, 0])
        phone = fit(serif(PHONE, PHONE_SIZE, CHARCOAL), what="the phone")
        phone.move_to([0, -1.55, 0])
        exam = fit(serif(EXAM_SHORT, EXAM_SIZE, GREY), what="the exam line")
        exam.move_to([0, -2.25, 0])

        rows = [brand, cohort, rule, facts, url, phone, exam]
        for upper, lower in zip(rows, rows[1:]):
            if upper.get_bottom()[1] - lower.get_top()[1] < 0.06:
                raise ValueError("End card rows overlap.")
        if exam.get_bottom()[1] < FLOOR:
            raise ValueError("The end card runs into the Shorts UI band.")

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

    CAPTIONS = {beat: (mode, lines) for beat, mode, lines in SCRIPT_PORTRAIT}

    def caption(self, t, beat, fraction=0.3):
        mode, lines = self.CAPTIONS[beat]
        wanted = (list(lines) if mode == "set"
                  else [text for text, _ in self.shown] + list(lines))
        block = plain_block(wanted, CAPTION, SAFE, ACCENTS_PORTRAIT)
        block.move_to([0, CAP_TOP - block.height / 2, 0])
        if block.get_bottom()[1] < FLOOR:
            raise ValueError(
                f"Beat '{beat}': the caption reaches "
                f"y={block.get_bottom()[1]:.2f}, below y={FLOOR}, where a "
                "Short's own title and buttons sit.")

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
