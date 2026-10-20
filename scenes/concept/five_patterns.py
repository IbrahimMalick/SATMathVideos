"""Paper 2 Without Panic — the five patterns that keep coming back.

Episode 1 of the series. Where the walkthrough says "let's solve this
paper", this says "here are the reusable patterns underneath it", so the
spine of the lecture is STEP-UP and each pattern hands over one of the six
habits rather than one more answer.

No Cambridge page is reproduced. Every algorithm, trace table and dataset
on screen is our own recreation of what the narration describes.

Lists arrive row by row, but they are laid out in full first and then
revealed. Growing a stack downwards a row at a time pushes the last rows
off the frame, and nothing on screen should move once it has landed.

Where the delivery or the transcriber is loose, the screen carries the
correct form:

  * the fitness dataset is 12, 15, 35, 10, 8, 7 throughout. The narration
    calls day three 55 while walking it; both are above the quiet
    threshold, so QuietCount = 5 and LongestQuiet = 3 either way.
  * TEAR, not "steer" — the T of STEP-UP, said loosely on the way in.
  * CurrentQuiet <- 0 for "current zero gets zero".
  * Y <- X1 AND X2 for the challenge answer, which trails off on tape.
  * Age >= 10 OR Age <= 18 for the bad condition: the narration drops the
    lower bound when restating it, and the whole point is that both halves
    are present and OR still lets 50 through.
  * the validation challenge is 0 to 75, as recorded.

Timing: timings/concept.five_patterns.json
Render: python build/render.py scripts/P2-five-patterns.md \\
    audio/P2-five-patterns.m4a
"""

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
from components.stepup import StepUpSpine, code_block, rule_card
from components.syllabus_map import TopicStrip
from components.trace_table import TraceTable
from scenes.base import SATScene

FRAME_SAFE = 12.6
WIDE = 11.5          # width for code panels and rule cards in landscape
FLOOR = -2.9         # above the pattern strip along the bottom

PATTERNS = ["Trace tables", "Validation", "Searching and flags",
            "Boolean logic", "The 15-mark question"]

# index into the STEP-UP spine
S, T, E, P_PRESERVE, U, P_PLAN = 0, 1, 2, 3, 4, 5


def fit(mobject, width=FRAME_SAFE):
    if mobject.width > width:
        mobject.scale_to_fit_width(width)
    return mobject


class FivePatterns(SATScene):
    scene_id = "concept.five_patterns"

    def construct(self):
        self.margin = mono("O Level CS 2210 · Paper 2 patterns", MARGIN_SIZE)
        self.margin.to_corner(UP + LEFT, buff=GAP_SM)
        self.add(self.margin)
        self.keep = [self.margin]
        self.strip = None
        self.head = None

        self.cold_open()
        self.agenda()
        self.step_up()
        self.pattern1_trace()
        self.pattern2_validation()
        self.pattern3_flags()
        self.pattern4_boolean()
        self.pattern5_fifteen()
        self.recap()
        self.checklist()
        self.call_to_action()

    # -------------------------------------------------------------- helpers

    def wipe(self, t, fraction=0.05):
        old = [m for m in self.mobjects if m not in self.keep]
        if old:
            self.play(*[FadeOut(m) for m in old], run_time=t.fill(fraction))
        self.head = None

    def title(self, t, text, fraction=0.08, color=CHARCOAL):
        head = fit(serif(text, TITLE_SIZE, color))
        head.to_edge(UP, buff=GAP_MD * 1.9)
        self.play(Write(head), run_time=t.fill(fraction))
        self.head = head
        return head

    def lines(self, *texts, size=BODY_SIZE, color=CHARCOAL, buff=GAP_SM * 1.3,
              align=None):
        group = VGroup(*[fit(serif(x, size, color)) for x in texts])
        if align is None:
            group.arrange(DOWN, buff=buff)
        else:
            group.arrange(DOWN, buff=buff, aligned_edge=align)
        return group

    def column(self, items, top=None, buff=GAP_MD * 1.2, floor=FLOOR):
        """Stack under the head, tightening gaps rather than shrinking text."""
        group = VGroup(*items)
        for factor in (1.0, 0.85, 0.7, 0.55, 0.42, 0.32):
            gap = buff * factor
            group.arrange(DOWN, buff=gap)
            if top is None:
                group.move_to(ORIGIN)
            else:
                group.next_to(top, DOWN, buff=gap)
            if group.get_bottom()[1] >= floor:
                break
        return group

    def foot(self, mobject, buff=GAP_MD * 1.1):
        """Place at the bottom, clear of the pattern strip."""
        if self.strip in self.mobjects:
            mobject.next_to(self.strip, UP, buff=buff)
        else:
            mobject.to_edge(DOWN, buff=buff)
        return mobject

    def pairs(self, rows, size=LABEL_SIZE, left_x=-5.8, right_x=-0.9,
              cue=GREY, answer=CHARCOAL, buff=GAP_SM * 1.4):
        """Two aligned columns: a cue on the left, its answer on the right.

        Placed by coordinate rather than padded with spaces — Pango is free
        to collapse runs of whitespace, so space-aligned columns are not
        actually aligned.
        """
        group = VGroup()
        gutter = right_x - left_x - 0.35
        for left_text, right_text in rows:
            left = fit(serif(left_text, size, cue), gutter)
            right = fit(serif(right_text, size, answer),
                        FRAME_SAFE / 2 - right_x - 0.4)
            left.move_to([left_x, 0, 0], aligned_edge=LEFT)
            right.move_to([right_x, 0, 0], aligned_edge=LEFT)
            group.add(VGroup(left, right))
        group.arrange(DOWN, buff=buff, aligned_edge=LEFT)
        return group

    def stack(self, group, top=None, buff=GAP_MD, floor=FLOOR, align=ORIGIN):
        """Place a group under `top`, tightening its own gaps to clear the floor.

        column() only tightens the gap above a block it treats as one unit;
        a long list has to close up between its own rows instead.
        """
        for factor in (1.0, 0.85, 0.7, 0.55, 0.42, 0.32, 0.24):
            gap = buff * factor
            group.arrange(DOWN, buff=gap, aligned_edge=align)
            if top is None:
                group.move_to(ORIGIN)
            else:
                group.next_to(top, DOWN, buff=gap)
            if group.get_bottom()[1] >= floor:
                break
        return group

    def hide(self, group):
        """Lay a group out in full, then make it invisible."""
        for row in group:
            row.set_opacity(0)
        return group

    def reveal(self, t, group, start, stop, fraction):
        """Fade in a slice of an already-placed group, one row at a time."""
        for row in group[start:stop]:
            row.set_opacity(1)
            self.play(FadeIn(row), run_time=t.fill(fraction))

    def pattern(self, t, number, label, fraction=0.09):
        """Clear to a new pattern and advance the strip along the bottom."""
        self.wipe(t)
        if self.strip is None:
            self.strip = TopicStrip(5, lit=SLATE, side=0.6)
            self.strip.to_edge(DOWN, buff=GAP_SM * 0.6)
            self.add(self.strip)
            self.keep.append(self.strip)
        head = fit(serif(f"Pattern {number}  ·  {label}", TITLE_SIZE,
                         CHARCOAL))
        head.to_edge(UP, buff=GAP_MD * 1.9)
        self.play(Write(head), *self.strip.focus(number - 1),
                  run_time=t.fill(fraction))
        self.head = head
        return head

    def rule(self, t, index, caption, fraction=0.16):
        """Flash the STEP-UP letter the narration has just earned."""
        spine = StepUpSpine(size=TITLE_SIZE, width=8.4)
        label = fit(serif(caption, LABEL_SIZE, TERRACOTTA))
        block = VGroup(spine, label).arrange(DOWN, buff=GAP_MD)
        self.foot(block)
        self.play(FadeIn(block), *spine.focus(index), run_time=t.fill(fraction))
        return block

    def code(self, lines, accent=SLATE):
        return code_block(lines, size=LABEL_SIZE, accent=accent, width=WIDE)

    def card(self, lines, color=TERRACOTTA):
        return rule_card(lines, size=TITLE_SIZE, color=color, width=WIDE)

    def caption(self, text, color=GREY, size=BODY_SIZE):
        return fit(serif(text, size, color))

    def recaption(self, t, holder, text, color=GREY, fraction=0.18):
        """Swap the running commentary line without moving it."""
        nxt = self.caption(text, color)
        nxt.move_to(holder)
        self.play(Transform(holder, nxt), run_time=t.fill(fraction))
        return holder

    def panel(self, t, lines, top=None, accent=SLATE, draw=0.12, write=0.45):
        """A pseudocode panel: box drawn on, lines written on."""
        block = self.code(lines, accent=accent)
        if top is None:
            self.column([block], self.head)
        else:
            block.next_to(top, DOWN, buff=GAP_MD)
        self.play(Create(block[0]), run_time=t.fill(draw))
        self.play(Write(block[1]), run_time=t.fill(write))
        return block

    def big_rule(self, t, lines, draw=0.16, write=0.45, y=0.4):
        """The one boxed rule the viewer should leave holding."""
        card = self.card(lines)
        card.move_to(UP * y)
        self.play(Create(card[0]), run_time=t.fill(draw))
        self.play(Write(card[1]), run_time=t.fill(write))
        return card

    def table(self, headers, rows, start=None, top=None, **kw):
        table = TraceTable(headers, rows, start=start, size=LABEL_SIZE,
                           width=WIDE, **kw)
        table.hidden()
        if top is not None:
            table.next_to(top, DOWN, buff=GAP_MD)
        return table

    # ------------------------------------------------------------ cold open

    def cold_open(self):
        with self.beat("cold_code") as t:
            head = fit(serif("Count  <-  3", TITLE_SIZE * 1.3, CHARCOAL))
            head.move_to(UP * 1.4)
            self.play(Write(head), run_time=t.fill(0.45))
            self.counter = head
            t.hold()

        with self.beat("cold_if") as t:
            self.panel(t, ["IF A = B THEN",
                           "    Count <- Count + 1",
                           "ENDIF"], top=self.counter, write=0.3)
            t.hold()

        with self.beat("cold_ask") as t:
            self.wipe(t)
            head = self.title(t, "Suppose A is not equal to B.", fraction=0.14)
            ask = fit(serif("What is Count now?", TITLE_SIZE, CHARCOAL))
            options = self.lines("zero?", "four?", "still three?",
                                 size=TITLE_SIZE, color=SLATE)
            self.column([ask, options], head)
            self.play(Write(ask), run_time=t.fill(0.16))
            for option in options:
                self.play(Write(option), run_time=t.fill(0.14))
            t.hold()

        with self.beat("cold_answer") as t:
            self.wipe(t)
            answer = fit(serif("It is still three.", TITLE_SIZE * 1.4,
                               TERRACOTTA))
            answer.move_to(UP * 0.9)
            why = self.caption("The program was never instructed to change it.")
            why.next_to(answer, DOWN, buff=GAP_LG)
            self.play(Write(answer), run_time=t.fill(0.3))
            self.play(Write(why), run_time=t.fill(0.24))
            t.hold()

        with self.beat("cold_cost") as t:
            cost = self.caption("This one mistake costs easy marks in Paper 2.",
                                CHARCOAL)
            self.foot(cost)
            self.play(Write(cost), run_time=t.fill(0.4))
            t.hold()

        with self.beat("cold_rule") as t:
            self.wipe(t)
            self.big_rule(t, ["NO ASSIGNMENT", "MEANS NO CHANGE"],
                          draw=0.2, write=0.45, y=0.0)
            t.hold()

    def agenda(self):
        with self.beat("agenda") as t:
            self.wipe(t)
            head = fit(serif("Paper 2 Without Panic", TITLE_SIZE * 1.5,
                             CHARCOAL))
            head.move_to(UP * 1.6)
            sub = self.caption("five patterns that keep coming back")
            sub.next_to(head, DOWN, buff=GAP_LG)
            self.play(Write(head), run_time=t.fill(0.34))
            self.play(Write(sub), run_time=t.fill(0.22))
            t.hold()

        with self.beat("agenda_list") as t:
            self.wipe(t)
            rows = self.pairs([(str(i + 1), name)
                               for i, name in enumerate(PATTERNS)],
                              size=BODY_SIZE, left_x=-4.4, right_x=-3.4,
                              cue=SLATE, buff=GAP_MD)
            rows.move_to(ORIGIN)
            self.hide(rows)
            self.reveal(t, rows, 0, len(rows), 0.16)
            t.hold()

        with self.beat("agenda_learn") as t:
            self.wipe(t)
            self.promise = self.big_rule(
                t, ["DO NOT MEMORISE ANSWERS", "LEARN THE PATTERN"],
                draw=0.14, write=0.3, y=0.4)
            t.hold()

        with self.beat("agenda_similar") as t:
            note = self.lines("Cambridge changes the scenario.",
                              "The patterns stay remarkably similar.",
                              size=BODY_SIZE, color=GREY)
            note.next_to(self.promise, DOWN, buff=GAP_LG)
            self.play(Write(note), run_time=t.fill(0.45))
            t.hold()

    def step_up(self):
        with self.beat("su_intro") as t:
            self.wipe(t)
            word = fit(serif("STEP-UP", TITLE_SIZE * 2.4, TERRACOTTA), 8.0)
            word.to_edge(UP, buff=GAP_MD * 1.6)
            self.play(Write(word), run_time=t.fill(0.5))
            self.word = word
            t.hold()

        # Laid out in full, revealed a letter at a time: the grid must not
        # reflow as letters five and six arrive.
        spine = StepUpSpine(size=TITLE_SIZE * 1.1, width=FRAME_SAFE,
                            labels=True)
        spine.next_to(self.word, DOWN, buff=GAP_LG)
        columns = spine[0]
        self.hide(columns)

        letters = (("su_s", S), ("su_t", T), ("su_e", E),
                   ("su_p1", P_PRESERVE), ("su_u", U), ("su_p2", P_PLAN))
        for position, (name, index) in enumerate(letters):
            with self.beat(name) as t:
                column = columns[index]
                column.set_opacity(1)
                column[0].set_color(TERRACOTTA)
                anims = [FadeIn(column)]
                if position:
                    previous = columns[letters[position - 1][1]][0]
                    anims.append(previous.animate.set_color(GREY))
                self.play(*anims, run_time=t.fill(0.5))
                t.hold()

        with self.beat("su_again") as t:
            again = self.caption("six habits, over and over")
            self.foot(again)
            last = columns[letters[-1][1]][0]
            self.play(Write(again), last.animate.set_color(GREY),
                      run_time=t.fill(0.4))
            t.hold()

    # ------------------------------------------------- pattern 1: tracing

    def pattern1_trace(self):
        with self.beat("p1_title") as t:
            self.pattern(t, 1, "Trace tables", fraction=0.5)
            t.hold()

        with self.beat("p1_mistake") as t:
            warn = self.lines("The biggest mistake is running",
                              "the algorithm in your head.",
                              size=TITLE_SIZE)
            self.column([warn], self.head)
            self.play(Write(warn), run_time=t.fill(0.5))
            t.hold()

        with self.beat("p1_rule") as t:
            self.wipe(t)
            self.rerm = self.big_rule(t, ["READ  ->  EXECUTE",
                                          "RECORD  ->  MOVE"],
                                      draw=0.14, write=0.4, y=0.6)
            t.hold()

        with self.beat("p1_rule_detail") as t:
            detail = self.lines("read the instruction",
                                "execute exactly that instruction",
                                "record what changed",
                                "move to the next one",
                                size=LABEL_SIZE, color=GREY, align=LEFT)
            self.stack(detail, self.rerm, align=LEFT)
            self.hide(detail)
            self.reveal(t, detail, 0, len(detail), 0.2)
            t.hold()

        with self.beat("p1_code") as t:
            self.wipe(t)
            block = self.code(["Value <- 2", "Count <- 0"])
            block.move_to(UP * 1.4)
            self.play(Create(block[0]), run_time=t.fill(0.14))
            self.play(Write(block[1]), run_time=t.fill(0.4))
            self.init_block = block
            t.hold()

        with self.beat("p1_while") as t:
            self.panel(t, ["WHILE Value < 20 DO",
                           "    Value <- Value * 2",
                           "    Count <- Count + 1",
                           "ENDWHILE"], top=self.init_block)
            t.hold()

        with self.beat("p1_notjump") as t:
            warn = self.caption("Do not jump to the answer.", TERRACOTTA)
            self.foot(warn)
            self.play(Write(warn), run_time=t.fill(0.4))
            t.hold()

        with self.beat("p1_start") as t:
            self.wipe(t)
            self.title(t, "Value <- 2    Count <- 0", fraction=0.12)
            trace = self.table(["Value", "Count"],
                               [(4, 1), (8, 2), (16, 3), (32, 4)],
                               start=(2, 0), top=self.head)
            self.play(Write(trace.head), Create(trace.rule),
                      run_time=t.fill(0.2))
            self.play(*trace.step(0), run_time=t.fill(0.2))
            self.trace = trace
            self.check = self.caption("is 2 < 20 ?  yes", SLATE)
            self.foot(self.check)
            self.play(Write(self.check), run_time=t.fill(0.2))
            t.hold()

        with self.beat("p1_r1") as t:
            self.recaption(t, self.check, "Value <- 2 * 2", SLATE, 0.5)
            t.hold()

        with self.beat("p1_r1b") as t:
            self.play(*self.trace.step(1), run_time=t.fill(0.4))
            t.hold()

        with self.beat("p1_r2") as t:
            self.recaption(t, self.check, "is 4 < 20 ?  yes", SLATE, 0.35)
            t.hold()

        with self.beat("p1_r2b") as t:
            self.play(*self.trace.step(2), run_time=t.fill(0.4))
            t.hold()

        with self.beat("p1_r3") as t:
            self.recaption(t, self.check, "is 8 < 20 ?  yes", SLATE, 0.3)
            self.play(*self.trace.step(3), run_time=t.fill(0.3))
            t.hold()

        with self.beat("p1_r4") as t:
            self.recaption(t, self.check, "is 16 < 20 ?  yes", SLATE, 0.3)
            self.play(*self.trace.step(4), run_time=t.fill(0.3))
            t.hold()

        with self.beat("p1_stop") as t:
            self.recaption(t, self.check, "is 32 < 20 ?  no  —  the loop stops",
                           TERRACOTTA, 0.5)
            t.hold()

        with self.beat("p1_final") as t:
            self.wipe(t)
            final = self.lines("Value  =  32", "Count  =  4",
                               size=TITLE_SIZE * 1.3, color=SAGE)
            final.move_to(UP * 0.8)
            self.play(Write(final), run_time=t.fill(0.5))
            t.hold()

        with self.beat("p1_notice") as t:
            self.rule(t, S, "one instruction at a time", fraction=0.4)
            t.hold()

        with self.beat("p1_persist_code") as t:
            self.wipe(t)
            self.title(t, "Count is 1. The characters differ.", fraction=0.12)
            self.panel(t, ["IF Character1 = Character2 THEN",
                           "    Count <- Count + 1",
                           "ENDIF"], write=0.35)
            t.hold()

        with self.beat("p1_persist_ask") as t:
            ask = self.caption("What happens to Count?", CHARCOAL)
            self.foot(ask)
            self.play(Write(ask), run_time=t.fill(0.4))
            self.ask = ask
            t.hold()

        with self.beat("p1_persist_ans") as t:
            self.recaption(t, self.ask,
                           "Nothing. The IF is skipped, so Count stays 1.",
                           TERRACOTTA, 0.5)
            t.hold()

        with self.beat("p1_persist_rule") as t:
            self.wipe(t)
            self.big_rule(t, ["VARIABLE VALUES PERSIST",
                              "UNTIL AN INSTRUCTION",
                              "CHANGES THEM"], draw=0.14, write=0.4, y=0.3)
            t.hold()

        with self.beat("p1_chal") as t:
            self.wipe(t)
            self.title(t, "Pause and trace this yourself", fraction=0.14,
                       color=TERRACOTTA)
            self.chal_init = self.panel(t, ["Number <- 3", "Total <- 0"],
                                        draw=0.14, write=0.35)
            t.hold()

        with self.beat("p1_chal_for") as t:
            self.panel(t, ["FOR i <- 1 TO 3",
                           "    Total <- Total + Number",
                           "    Number <- Number + 2",
                           "NEXT i"], top=self.chal_init, draw=0.14)
            t.hold()

        with self.beat("p1_chal_q") as t:
            ask = self.caption("What is the final value of Total?", CHARCOAL)
            self.foot(ask)
            self.play(Write(ask), run_time=t.fill(0.4))
            t.hold()

        with self.beat("p1_chal_start") as t:
            self.wipe(t)
            self.title(t, "Number <- 3    Total <- 0", fraction=0.12)
            trace = self.table(["i", "Total", "Number"],
                               [(1, 3, 5), (2, 8, 7), (3, 15, 9)],
                               start=("-", 0, 3), top=self.head)
            self.play(Write(trace.head), Create(trace.rule),
                      run_time=t.fill(0.22))
            self.play(*trace.step(0), run_time=t.fill(0.25))
            self.chal_trace = trace
            t.hold()

        self.step_note = None
        for name, index, note in (
                ("p1_chal_i1", 1, "Total <- 0 + 3     Number <- 3 + 2"),
                ("p1_chal_i2", 2, "Total <- 3 + 5     Number <- 5 + 2"),
                ("p1_chal_i3", 3, "Total <- 8 + 7     Number <- 7 + 2")):
            with self.beat(name) as t:
                self.play(*self.chal_trace.step(index), run_time=t.fill(0.35))
                if self.step_note is None:
                    self.step_note = self.caption(note, SLATE, LABEL_SIZE)
                    self.foot(self.step_note)
                    self.play(Write(self.step_note), run_time=t.fill(0.3))
                else:
                    self.recaption(t, self.step_note, note, SLATE, 0.3)
                t.hold()

        with self.beat("p1_chal_ans") as t:
            self.wipe(t)
            answer = fit(serif("Total  =  15", TITLE_SIZE * 1.5, SAGE))
            answer.move_to(UP * 0.8)
            self.play(Write(answer), run_time=t.fill(0.45))
            self.answer = answer
            t.hold()

        with self.beat("p1_chal_sum") as t:
            sums = fit(serif("3 + 5 + 7  =  15", TITLE_SIZE, GREY))
            sums.next_to(self.answer, DOWN, buff=GAP_LG)
            self.play(Write(sums), run_time=t.fill(0.45))
            t.hold()

        with self.beat("p1_close") as t:
            close = self.caption("Follow the instructions. Don't guess.",
                                 TERRACOTTA)
            self.foot(close)
            self.play(Write(close), run_time=t.fill(0.45))
            t.hold()

    # ---------------------------------------------- pattern 2: validation

    def pattern2_validation(self):
        with self.beat("p2_title") as t:
            self.pattern(t, 2, "Validation", fraction=0.5)
            t.hold()

        with self.beat("p2_range") as t:
            spec = fit(serif("Valid age:  10 to 18 inclusive", TITLE_SIZE,
                             CHARCOAL))
            self.column([spec], self.head)
            self.play(Write(spec), run_time=t.fill(0.5))
            self.spec = spec
            t.hold()

        with self.beat("p2_options") as t:
            option_a = self.code(["A    Age >= 10 OR Age <= 18"], accent=GREY)
            option_b = self.code(["B    Age >= 10 AND Age <= 18"], accent=GREY)
            pair = VGroup(option_a, option_b).arrange(DOWN, buff=GAP_MD)
            pair.next_to(self.spec, DOWN, buff=GAP_LG)
            self.play(Create(option_a[0]), Write(option_a[1]),
                      run_time=t.fill(0.3))
            self.play(Create(option_b[0]), Write(option_b[1]),
                      run_time=t.fill(0.3))
            self.option_a, self.option_b = option_a, option_b
            t.hold()

        with self.beat("p2_answer") as t:
            self.play(self.option_b[0].animate.set_color(TERRACOTTA),
                      self.option_b[1].animate.set_color(TERRACOTTA),
                      FadeOut(self.option_a), run_time=t.fill(0.5))
            t.hold()

        with self.beat("p2_both") as t:
            both = self.lines("at least 10", "and at most 18",
                              size=BODY_SIZE, color=GREY)
            self.foot(both)
            self.play(Write(both), run_time=t.fill(0.5))
            t.hold()

        with self.beat("p2_rule") as t:
            self.wipe(t)
            self.inside_card = self.big_rule(
                t, ["INSIDE  =  AND", "OUTSIDE  =  OR"], y=0.4)
            t.hold()

        with self.beat("p2_rule_again") as t:
            again = self.caption("worth saying twice")
            again.next_to(self.inside_card, DOWN, buff=GAP_LG)
            self.play(Write(again), run_time=t.fill(0.45))
            t.hold()

        with self.beat("p2_fifty") as t:
            self.wipe(t)
            self.title(t, "Why OR is dangerous", fraction=0.14)
            case = fit(serif("Age = 50", TITLE_SIZE, CHARCOAL))
            block = self.code(["Age >= 10 OR Age <= 18"], accent=TERRACOTTA)
            self.column([case, block], self.head)
            self.play(Write(case), run_time=t.fill(0.2))
            self.play(Create(block[0]), Write(block[1]), run_time=t.fill(0.3))
            self.bad_cond = block
            t.hold()

        with self.beat("p2_eval1") as t:
            line = fit(serif("50 >= 10    ->    TRUE", BODY_SIZE, SAGE))
            line.next_to(self.bad_cond, DOWN, buff=GAP_MD)
            self.play(Write(line), run_time=t.fill(0.5))
            self.eval1 = line
            t.hold()

        with self.beat("p2_eval2") as t:
            line = fit(serif("50 <= 18    ->    FALSE", BODY_SIZE, GREY))
            line.next_to(self.eval1, DOWN, buff=GAP_SM * 1.4)
            self.play(Write(line), run_time=t.fill(0.5))
            self.eval2 = line
            t.hold()

        with self.beat("p2_or") as t:
            line = fit(serif("TRUE  OR  FALSE    =    TRUE", BODY_SIZE,
                             TERRACOTTA))
            line.next_to(self.eval2, DOWN, buff=GAP_MD)
            self.play(Write(line), run_time=t.fill(0.5))
            t.hold()

        with self.beat("p2_accepts") as t:
            self.wipe(t)
            bad = self.lines("The wrong condition", "accepts age 50.",
                             size=TITLE_SIZE * 1.2, color=TERRACOTTA)
            bad.move_to(UP * 0.5)
            self.play(Write(bad), run_time=t.fill(0.5))
            t.hold()

        with self.beat("p2_invalid") as t:
            self.wipe(t)
            self.title(t, "Outside the range", fraction=0.14)
            block = self.code(["Age < 10 OR Age > 18"], accent=SLATE)
            note = self.caption("too low, or too high")
            self.column([block, note], self.head)
            self.play(Create(block[0]), Write(block[1]), run_time=t.fill(0.3))
            self.play(Write(note), run_time=t.fill(0.25))
            t.hold()

        with self.beat("p2_loop") as t:
            self.wipe(t)
            self.title(t, "Keep asking until the value is valid",
                       fraction=0.3)
            t.hold()

        with self.beat("p2_loop_code") as t:
            self.repeat_block = self.panel(
                t, ["REPEAT", "    INPUT Mark",
                    "UNTIL Mark >= 0 AND Mark <= 100"],
                draw=0.1, write=0.4)
            t.hold()

        with self.beat("p2_loop_why") as t:
            why = self.lines("the INPUT runs at least once",
                             "the condition is checked after it",
                             size=BODY_SIZE, color=GREY)
            why.next_to(self.repeat_block, DOWN, buff=GAP_MD)
            self.play(Write(why), run_time=t.fill(0.5))
            t.hold()

        with self.beat("p2_three") as t:
            self.wipe(t)
            self.title(t, "The three loops", fraction=0.1)
            rows = self.pairs([
                ("FOR", "you know how many repetitions"),
                ("WHILE", "check the condition first"),
                ("REPEAT", "do the body first")], size=BODY_SIZE,
                left_x=-5.4, right_x=-2.6)
            rows.next_to(self.head, DOWN, buff=GAP_LG)
            self.hide(rows)
            self.reveal(t, rows, 0, len(rows), 0.22)
            t.hold()

        with self.beat("p2_chal") as t:
            self.wipe(t)
            self.title(t, "Your challenge", fraction=0.4, color=TERRACOTTA)
            t.hold()

        with self.beat("p2_chal_q") as t:
            spec = fit(serif("Valid score:  0 to 75 inclusive", TITLE_SIZE,
                             CHARCOAL))
            block = self.code(["REPEAT", "    INPUT Score", "UNTIL  ?"],
                              accent=GREY)
            self.column([spec, block], self.head)
            self.play(Write(spec), run_time=t.fill(0.25))
            self.play(Create(block[0]), Write(block[1]), run_time=t.fill(0.3))
            t.hold()

        with self.beat("p2_chal_ans") as t:
            self.wipe(t)
            answer = self.code(["UNTIL Score >= 0 AND Score <= 75"],
                               accent=SAGE)
            answer.move_to(UP * 0.6)
            self.play(Create(answer[0]), run_time=t.fill(0.14))
            self.play(Write(answer[1]), run_time=t.fill(0.4))
            self.chal_answer = answer
            t.hold()

        with self.beat("p2_chal_rule") as t:
            again = fit(serif("inside the range  =  AND", TITLE_SIZE,
                              TERRACOTTA))
            again.next_to(self.chal_answer, DOWN, buff=GAP_LG)
            self.play(Write(again), run_time=t.fill(0.45))
            t.hold()

    # ------------------------------------ pattern 3: searching and flags

    def pattern3_flags(self):
        with self.beat("p3_title") as t:
            self.pattern(t, 3, "Searching and Boolean flags", fraction=0.5)
            t.hold()

        with self.beat("p3_data") as t:
            spec = fit(serif("500 student records", TITLE_SIZE, CHARCOAL))
            self.column([spec], self.head)
            self.play(Write(spec), run_time=t.fill(0.5))
            self.spec = spec
            t.hold()

        with self.beat("p3_cols") as t:
            self.panel(t, ["Students[Row, 1]     StudentID",
                           "Students[Row, 2]     StudentName"],
                       top=self.spec, draw=0.12)
            t.hold()

        with self.beat("p3_problem") as t:
            ask = self.lines("Search all 500 and find nothing.",
                             "How does the program remember?",
                             size=BODY_SIZE, color=CHARCOAL)
            self.foot(ask)
            self.play(Write(ask), run_time=t.fill(0.5))
            t.hold()

        with self.beat("p3_flag") as t:
            self.wipe(t)
            self.big_rule(t, ["A BOOLEAN FLAG", "IS MEMORY"], y=0.5)
            t.hold()

        with self.beat("p3_false") as t:
            self.wipe(t)
            block = self.code(["Found <- FALSE"], accent=SLATE)
            block.move_to(UP * 1.4)
            why = self.caption("before we search, we have found nothing")
            why.next_to(block, DOWN, buff=GAP_LG)
            self.play(Create(block[0]), Write(block[1]), run_time=t.fill(0.35))
            self.play(Write(why), run_time=t.fill(0.3))
            t.hold()

        with self.beat("p3_loop") as t:
            self.wipe(t)
            block = self.code([
                "Found <- FALSE",
                "FOR Row <- 1 TO 500",
                "    IF SearchID = Students[Row, 1] THEN",
                "        OUTPUT Students[Row, 2]",
                "        Found <- TRUE",
                "    ENDIF",
                "NEXT Row",
            ])
            block.move_to(UP * 0.4)
            self.play(Create(block[0]), run_time=t.fill(0.1))
            self.play(Write(block[1]), run_time=t.fill(0.5))
            t.hold()

        with self.beat("p3_after") as t:
            self.wipe(t)
            block = self.code(["IF Found = FALSE THEN",
                               '    OUTPUT "Student not found"',
                               "ENDIF"], accent=TERRACOTTA)
            block.move_to(UP * 0.5)
            self.play(Create(block[0]), run_time=t.fill(0.12))
            self.play(Write(block[1]), run_time=t.fill(0.45))
            t.hold()

        with self.beat("p3_rule") as t:
            self.wipe(t)
            self.flag_card = self.big_rule(
                t, ["FALSE  ->  TRUE  ->  CHECK"], draw=0.14, write=0.4, y=0.6)
            t.hold()

        with self.beat("p3_memory") as t:
            note = self.lines("false before the search", "true when found",
                              "checked after it",
                              size=LABEL_SIZE, color=GREY)
            note.next_to(self.flag_card, DOWN, buff=GAP_MD)
            self.play(Write(note), run_time=t.fill(0.45))
            t.hold()

        with self.beat("p3_persist") as t:
            self.wipe(t)
            self.title(t, "Found becomes TRUE on row 200", fraction=0.14)
            ask = fit(serif("Row 201 does not match. Does Found go back?",
                            BODY_SIZE, CHARCOAL))
            self.column([ask], self.head)
            self.play(Write(ask), run_time=t.fill(0.4))
            t.hold()

        with self.beat("p3_persist_ans") as t:
            answer = self.lines("No instruction says Found <- FALSE,",
                                "so Found stays TRUE.",
                                size=TITLE_SIZE, color=TERRACOTTA)
            answer.move_to(ORIGIN)
            self.play(Write(answer), run_time=t.fill(0.5))
            t.hold()

        with self.beat("p3_trap") as t:
            self.wipe(t)
            self.title(t, "The matching-row trap", fraction=0.3,
                       color=TERRACOTTA)
            t.hold()

        with self.beat("p3_trap_detail") as t:
            self.panel(t, ["FOR Row <- 1 TO 500",
                           "    IF SearchID = Students[Row, 1] THEN",
                           "        Found <- TRUE",
                           "    ENDIF",
                           "NEXT Row",
                           "OUTPUT Students[Row, 2]"],
                       accent=TERRACOTTA, draw=0.1, write=0.45)
            note = self.caption("the match was at row 247", GREY, LABEL_SIZE)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.2))
            t.hold()

        with self.beat("p3_trap_problem") as t:
            self.wipe(t)
            bad = self.lines("After the loop, Row no longer",
                             "refers to row 247.",
                             size=TITLE_SIZE, color=TERRACOTTA)
            bad.move_to(UP * 0.6)
            self.play(Write(bad), run_time=t.fill(0.5))
            t.hold()

        with self.beat("p3_safe1") as t:
            self.wipe(t)
            self.title(t, "Two safe approaches", fraction=0.14)
            label = self.caption("1    output as soon as you find it",
                                 GREY, LABEL_SIZE)
            block = self.code(["OUTPUT Students[Row, 2]", "Found <- TRUE"],
                              accent=SAGE)
            group = VGroup(label, block).arrange(DOWN, buff=GAP_SM * 1.4)
            group.next_to(self.head, DOWN, buff=GAP_MD)
            self.play(Write(label), run_time=t.fill(0.2))
            self.play(Create(block[0]), Write(block[1]), run_time=t.fill(0.35))
            self.safe1 = group
            t.hold()

        with self.beat("p3_safe2") as t:
            label = self.caption("2    store the matching row",
                                 GREY, LABEL_SIZE)
            block = self.code(["FoundRow <- Row"], accent=SAGE)
            group = VGroup(label, block).arrange(DOWN, buff=GAP_SM * 1.4)
            group.next_to(self.safe1, DOWN, buff=GAP_MD)
            self.play(Write(label), run_time=t.fill(0.2))
            self.play(Create(block[0]), Write(block[1]), run_time=t.fill(0.35))
            t.hold()

        with self.beat("p3_rule2") as t:
            self.wipe(t)
            self.big_rule(t, ["IF YOU NEED A VALUE LATER,",
                              "STORE IT BEFORE YOU LOSE IT"],
                          draw=0.14, write=0.4, y=0.4)
            t.hold()

    # ------------------------------------------- pattern 4: boolean logic

    def pattern4_boolean(self):
        with self.beat("p4_title") as t:
            self.pattern(t, 4, "Boolean logic", fraction=0.5)
            t.hold()

        with self.beat("p4_expr") as t:
            self.panel(t, ["Z = NOT(A AND B) OR (B XOR C)"], accent=CHARCOAL,
                       draw=0.14, write=0.45)
            t.hold()

        with self.beat("p4_dont") as t:
            warn = self.caption("Don't try to jump straight to Z.", TERRACOTTA)
            self.foot(warn)
            self.play(Write(warn), run_time=t.fill(0.45))
            t.hold()

        with self.beat("p4_one") as t:
            self.wipe(t)
            self.big_rule(t, ["ONE GATE  ->  ONE RESULT", "ONE COLUMN"],
                          y=0.5)
            t.hold()

        with self.beat("p4_break") as t:
            self.wipe(t)
            self.title(t, "Break it apart", fraction=0.3)
            t.hold()

        with self.beat("p4_x1") as t:
            self.split = self.panel(t, ["X1 <- A AND B",
                                        "X2 <- NOT X1",
                                        "X3 <- B XOR C"], draw=0.12, write=0.5)
            t.hold()

        with self.beat("p4_z") as t:
            self.panel(t, ["Z  <- X2 OR X3"], top=self.split,
                       accent=TERRACOTTA, draw=0.14, write=0.45)
            t.hold()

        with self.beat("p4_easier") as t:
            self.rule(t, U, "use intermediate results", fraction=0.45)
            t.hold()

        with self.beat("p4_gates") as t:
            self.wipe(t)
            self.title(t, "The gate rules", fraction=0.5)
            t.hold()

        self.gate_rows = self.pairs([
            ("AND", "both inputs are 1"),
            ("OR", "at least one input is 1"),
            ("XOR", "the inputs are different"),
            ("NOT", "flip it")], size=BODY_SIZE, left_x=-5.0, right_x=-2.4,
            buff=GAP_MD)

        with self.beat("p4_and_or") as t:
            self.stack(self.gate_rows, self.head, buff=GAP_MD, align=LEFT)
            self.hide(self.gate_rows)
            self.reveal(t, self.gate_rows, 0, 2, 0.3)
            t.hold()

        with self.beat("p4_xor_not") as t:
            self.reveal(t, self.gate_rows, 2, 4, 0.3)
            t.hold()

        with self.beat("p4_xor_table") as t:
            self.wipe(t)
            self.title(t, "XOR, all four rows", fraction=0.08)
            rows = self.lines("0  XOR  0   =   0",
                              "0  XOR  1   =   1",
                              "1  XOR  0   =   1",
                              "1  XOR  1   =   0",
                              size=BODY_SIZE, color=SLATE)
            self.column([rows], self.head)
            self.hide(rows)
            self.reveal(t, rows, 0, len(rows), 0.18)
            t.hold()

        with self.beat("p4_xor_rule") as t:
            self.wipe(t)
            self.big_rule(t, ["DIFFERENT  =  1", "SAME  =  0"], y=0.4)
            t.hold()

        with self.beat("p4_row") as t:
            self.wipe(t)
            self.title(t, "Work one row", fraction=0.4)
            t.hold()

        with self.beat("p4_row_vals") as t:
            given = fit(serif("A = 1        B = 0        C = 1", TITLE_SIZE,
                              CHARCOAL))
            given.next_to(self.head, DOWN, buff=GAP_MD)
            self.play(Write(given), run_time=t.fill(0.5))
            self.given = given
            t.hold()

        work = self.lines("X1  =  1 AND 0  =  0",
                          "X2  =  NOT 0  =  1",
                          "X3  =  0 XOR 1  =  1",
                          size=BODY_SIZE, color=SLATE, buff=GAP_SM * 1.5)
        self.stack(work, self.given)
        self.hide(work)
        for position, name in enumerate(("p4_row_x1", "p4_row_x2",
                                         "p4_row_x3")):
            with self.beat(name) as t:
                self.reveal(t, work, position, position + 1, 0.5)
                t.hold()

        with self.beat("p4_row_z") as t:
            line = fit(serif("Z  =  1 OR 1  =  1", TITLE_SIZE, TERRACOTTA))
            self.foot(line)
            self.play(Write(line), run_time=t.fill(0.5))
            t.hold()

        with self.beat("p4_mech") as t:
            self.wipe(t)
            note = self.lines("Notice how boring that was.",
                              "That is the point.",
                              size=TITLE_SIZE * 1.1)
            note.move_to(UP * 0.5)
            self.play(Write(note), run_time=t.fill(0.5))
            self.mech = note
            t.hold()

        with self.beat("p4_clever") as t:
            note = self.caption("Boolean logic should be mechanical.")
            note.next_to(self.mech, DOWN, buff=GAP_LG)
            self.play(Write(note), run_time=t.fill(0.45))
            t.hold()

        self.circuit()

        with self.beat("p4_chal") as t:
            self.wipe(t)
            self.title(t, "Your challenge", fraction=0.14, color=TERRACOTTA)
            block = self.code(["Y = (A XOR B) AND NOT C"], accent=CHARCOAL)
            self.column([block], self.head)
            self.play(Create(block[0]), Write(block[1]), run_time=t.fill(0.45))
            t.hold()

        with self.beat("p4_chal_q") as t:
            ask = self.caption("What are your intermediate columns?",
                               CHARCOAL)
            self.foot(ask)
            self.play(Write(ask), run_time=t.fill(0.45))
            t.hold()

        with self.beat("p4_chal_ans") as t:
            self.wipe(t)
            block = self.code(["X1 <- A XOR B", "X2 <- NOT C"], accent=SAGE)
            block.move_to(UP * 0.9)
            self.play(Create(block[0]), run_time=t.fill(0.12))
            self.play(Write(block[1]), run_time=t.fill(0.5))
            self.chal_cols = block
            t.hold()

        with self.beat("p4_chal_y") as t:
            self.panel(t, ["Y  <- X1 AND X2"], top=self.chal_cols,
                       accent=TERRACOTTA, draw=0.14, write=0.5)
            t.hold()

    def gate(self, label, color=SLATE):
        text = mono(label, LABEL_SIZE, CHARCOAL)
        box = SurroundingRectangle(text, color=color, buff=GAP_SM,
                                   stroke_width=3)
        return VGroup(box, text)

    def wire(self, start, end, color=GREY):
        return Line(start, end, color=color, stroke_width=2.5)

    def circuit(self):
        """Build the circuit inside-out, one gate per beat."""
        with self.beat("p4_circuit") as t:
            self.wipe(t)
            self.title(t, "The same idea draws the circuit", fraction=0.4)
            t.hold()

        with self.beat("p4_brackets") as t:
            note = self.caption("The brackets tell you which gate comes first.")
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.45))
            t.hold()

        top, bottom = 0.95, -1.55
        a = fit(serif("A", BODY_SIZE, CHARCOAL)).move_to([-5.4, top + 0.5, 0])
        b1 = fit(serif("B", BODY_SIZE, CHARCOAL)).move_to([-5.4, top - 0.5, 0])
        b2 = fit(serif("B", BODY_SIZE, CHARCOAL)).move_to([-5.4,
                                                           bottom + 0.5, 0])
        c = fit(serif("C", BODY_SIZE, CHARCOAL)).move_to([-5.4,
                                                          bottom - 0.5, 0])
        and_gate = self.gate("AND").move_to([-3.1, top, 0])
        not_gate = self.gate("NOT").move_to([-0.6, top, 0])
        xor_gate = self.gate("XOR").move_to([-3.1, bottom, 0])
        or_gate = self.gate("OR", TERRACOTTA).move_to([2.4, -0.3, 0])
        z = fit(serif("Z", TITLE_SIZE, TERRACOTTA)).move_to([4.6, -0.3, 0])

        with self.beat("p4_and_gate") as t:
            wires = VGroup(
                self.wire(a.get_right(), and_gate.get_left() + UP * 0.22),
                self.wire(b1.get_right(), and_gate.get_left() + DOWN * 0.22))
            self.play(Write(VGroup(a, b1)), run_time=t.fill(0.2))
            self.play(Create(wires), run_time=t.fill(0.2))
            self.play(Create(and_gate[0]), Write(and_gate[1]),
                      run_time=t.fill(0.3))
            t.hold()

        with self.beat("p4_not_gate") as t:
            wire = self.wire(and_gate.get_right(), not_gate.get_left())
            self.play(Create(wire), run_time=t.fill(0.25))
            self.play(Create(not_gate[0]), Write(not_gate[1]),
                      run_time=t.fill(0.45))
            t.hold()

        with self.beat("p4_xor_gate") as t:
            wires = VGroup(
                self.wire(b2.get_right(), xor_gate.get_left() + UP * 0.22),
                self.wire(c.get_right(), xor_gate.get_left() + DOWN * 0.22))
            self.play(Write(VGroup(b2, c)), run_time=t.fill(0.18))
            self.play(Create(wires), run_time=t.fill(0.18))
            self.play(Create(xor_gate[0]), Write(xor_gate[1]),
                      run_time=t.fill(0.3))
            t.hold()

        with self.beat("p4_or_gate") as t:
            join_top = [1.3, top, 0]
            join_bottom = [1.3, bottom, 0]
            wires = VGroup(
                self.wire(not_gate.get_right(), join_top),
                self.wire(join_top, or_gate.get_left() + UP * 0.22),
                self.wire(xor_gate.get_right(), join_bottom),
                self.wire(join_bottom, or_gate.get_left() + DOWN * 0.22),
                self.wire(or_gate.get_right(), z.get_left()))
            self.play(Create(wires), run_time=t.fill(0.3))
            self.play(Create(or_gate[0]), Write(or_gate[1]),
                      run_time=t.fill(0.25))
            self.play(Write(z), run_time=t.fill(0.2))
            t.hold()

        with self.beat("p4_inside_out") as t:
            self.wipe(t)
            self.big_rule(t, ["BUILD FROM THE", "INSIDE OUTWARD"], y=0.4)
            t.hold()

    # --------------------------------------- pattern 5: the 15-mark question

    def pattern5_fifteen(self):
        with self.beat("p5_title") as t:
            self.pattern(t, 5, "The 15-mark question", fraction=0.5)
            t.hold()

        with self.beat("p5_scare") as t:
            note = self.caption("It frightens students before they start.")
            self.column([note], self.head)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

        with self.beat("p5_dont") as t:
            self.wipe(t)
            self.dont = self.big_rule(t, ["DO NOT START CODING"],
                                      draw=0.2, write=0.5, y=0.5)
            t.hold()

        with self.beat("p5_dont_again") as t:
            note = self.caption("not in the exam, and not at work either")
            note.next_to(self.dont, DOWN, buff=GAP_LG)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

        with self.beat("p5_break") as t:
            self.wipe(t)
            self.title(t, "Break the scenario into requirements",
                       fraction=0.4)
            t.hold()

        with self.beat("p5_scenario") as t:
            spec = self.lines("A fitness centre records the number",
                              "of visitors each day for 30 days.",
                              size=BODY_SIZE)
            spec.next_to(self.head, DOWN, buff=GAP_MD)
            self.play(Write(spec), run_time=t.fill(0.5))
            self.spec = spec
            t.hold()

        reqs = self.lines("store the values",
                          "total visitors",
                          "average visitors per day",
                          "count the quiet days, under 20 visitors",
                          "find the longest run of quiet days",
                          "warn if that run reaches four",
                          size=LABEL_SIZE, color=GREY, align=LEFT)
        self.stack(reqs, self.spec, align=LEFT)
        self.hide(reqs)

        with self.beat("p5_reqs") as t:
            self.reveal(t, reqs, 0, 3, 0.26)
            t.hold()

        with self.beat("p5_reqs2") as t:
            self.reveal(t, reqs, 3, 4, 0.5)
            t.hold()

        with self.beat("p5_reqs3") as t:
            self.reveal(t, reqs, 4, 6, 0.3)
            t.hold()

        with self.beat("p5_large") as t:
            self.wipe(t)
            note = self.lines("That looks like one huge problem.",
                              "It isn't.", size=TITLE_SIZE * 1.1)
            note.move_to(UP * 0.5)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

        with self.beat("p5_map1") as t:
            self.wipe(t)
            self.title(t, "Eight small patterns", fraction=0.1)
            self.map_rows = self.pairs([
                ("store 30 values", "ARRAY"),
                ("30 days", "FOR LOOP"),
                ("total", "ACCUMULATOR"),
                ("average", "CALCULATION"),
                ("quiet days", "COUNTER"),
                ("consecutive quiet days", "CURRENT STREAK"),
                ("longest quiet run", "MAXIMUM"),
                ("warning", "IF")], left_x=-5.8, right_x=-0.2,
                buff=GAP_SM * 1.2)
            self.stack(self.map_rows, self.head, buff=GAP_SM * 1.2,
                       align=LEFT)
            self.hide(self.map_rows)
            self.reveal(t, self.map_rows, 0, 2, 0.35)
            t.hold()

        with self.beat("p5_map2") as t:
            self.reveal(t, self.map_rows, 2, 4, 0.35)
            t.hold()

        with self.beat("p5_map3") as t:
            self.reveal(t, self.map_rows, 4, 6, 0.35)
            t.hold()

        with self.beat("p5_map4") as t:
            self.reveal(t, self.map_rows, 6, 8, 0.35)
            t.hold()

        with self.beat("p5_gone") as t:
            self.wipe(t)
            note = self.lines("No longer a 15-mark question.",
                              "Eight patterns you already know.",
                              size=TITLE_SIZE)
            note.move_to(UP * 0.4)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

        with self.beat("p5_init") as t:
            self.wipe(t)
            self.title(t, "Establish initial values", fraction=0.4)
            t.hold()

        with self.beat("p5_init_code") as t:
            self.panel(t, ["Total <- 0",
                           "QuietCount <- 0",
                           "CurrentQuiet <- 0",
                           "LongestQuiet <- 0"], draw=0.1, write=0.5)
            t.hold()

        with self.beat("p5_init_why") as t:
            why = self.caption("Counters and totals do not begin at zero "
                               "by magic.")
            self.foot(why)
            self.play(Write(why), run_time=t.fill(0.5))
            t.hold()

        with self.beat("p5_init_e") as t:
            self.wipe(t)
            self.rule(t, E, "establish initial values", fraction=0.45)
            t.hold()

        with self.beat("p5_loop") as t:
            self.wipe(t)
            self.title(t, "The accumulator", fraction=0.4)
            t.hold()

        with self.beat("p5_loop_code") as t:
            self.loop_block = self.panel(t, ["FOR Day <- 1 TO 30",
                                             "    INPUT Visitors[Day]"],
                                         draw=0.12, write=0.5)
            t.hold()

        with self.beat("p5_accum") as t:
            self.panel(t, ["    Total <- Total + Visitors[Day]"],
                       top=self.loop_block, accent=TERRACOTTA,
                       draw=0.14, write=0.5)
            t.hold()

        with self.beat("p5_contrast") as t:
            self.wipe(t)
            self.title(t, "Two statements, one difference", fraction=0.4)
            t.hold()

        with self.beat("p5_replace") as t:
            label = self.caption("replaces the total", GREY, LABEL_SIZE)
            block = self.code(["Total <- Visitors[Day]"], accent=GREY)
            group = VGroup(block, label).arrange(DOWN, buff=GAP_SM * 1.3)
            group.next_to(self.head, DOWN, buff=GAP_MD)
            self.play(Create(block[0]), Write(block[1]), run_time=t.fill(0.35))
            self.play(Write(label), run_time=t.fill(0.2))
            self.replace_group = group
            t.hold()

        with self.beat("p5_adds") as t:
            label = self.caption("accumulates", TERRACOTTA, LABEL_SIZE)
            block = self.code(["Total <- Total + Visitors[Day]"],
                              accent=TERRACOTTA)
            group = VGroup(block, label).arrange(DOWN, buff=GAP_SM * 1.3)
            group.next_to(self.replace_group, DOWN, buff=GAP_MD)
            self.play(Create(block[0]), Write(block[1]), run_time=t.fill(0.35))
            self.play(Write(label), run_time=t.fill(0.2))
            t.hold()

        with self.beat("p5_rule") as t:
            self.wipe(t)
            self.big_rule(t, ["ASSIGNMENT REPLACES", "ACCUMULATION ADDS"],
                          y=0.4)
            t.hold()

        with self.beat("p5_quiet") as t:
            self.wipe(t)
            self.title(t, "Counting the quiet days", fraction=0.4)
            t.hold()

        with self.beat("p5_quiet_code") as t:
            self.quiet_block = self.panel(
                t, ["IF Visitors[Day] < 20 THEN",
                    "    QuietCount <- QuietCount + 1"], draw=0.12, write=0.5)
            t.hold()

        with self.beat("p5_streak") as t:
            self.streak_line = self.panel(
                t, ["    CurrentQuiet <- CurrentQuiet + 1"],
                top=self.quiet_block, draw=0.14, write=0.5)
            t.hold()

        with self.beat("p5_record") as t:
            self.wipe(t)
            block = self.code(["    IF CurrentQuiet > LongestQuiet THEN",
                               "        LongestQuiet <- CurrentQuiet",
                               "    ENDIF"], accent=TERRACOTTA)
            block.move_to(UP * 0.3)
            self.play(Create(block[0]), run_time=t.fill(0.12))
            self.play(Write(block[1]), run_time=t.fill(0.5))
            t.hold()

        with self.beat("p5_reset") as t:
            self.wipe(t)
            block = self.code(["ELSE", "    CurrentQuiet <- 0", "ENDIF"],
                              accent=SLATE)
            block.move_to(UP * 0.7)
            self.play(Create(block[0]), run_time=t.fill(0.14))
            self.play(Write(block[1]), run_time=t.fill(0.5))
            self.reset_block = block
            t.hold()

        with self.beat("p5_why_reset") as t:
            why = self.caption("the consecutive streak has broken")
            why.next_to(self.reset_block, DOWN, buff=GAP_LG)
            self.play(Write(why), run_time=t.fill(0.5))
            t.hold()

        with self.beat("p5_survives") as t:
            self.wipe(t)
            self.big_rule(t, ["CURRENT RESETS", "LONGEST SURVIVES"], y=0.4)
            t.hold()

        with self.beat("p5_three") as t:
            self.wipe(t)
            self.title(t, "Count  ·  Current  ·  Longest", fraction=0.4)
            t.hold()

        three = self.pairs([
            ("COUNT", "how many in total"),
            ("CURRENT", "the streak right now"),
            ("LONGEST", "the best streak seen")], size=BODY_SIZE,
            left_x=-5.4, right_x=-1.6, cue=SLATE, buff=GAP_MD)
        self.stack(three, self.head, buff=GAP_MD, align=LEFT)
        self.hide(three)
        for position, name in enumerate(("p5_def_count", "p5_def_current",
                                         "p5_def_longest")):
            with self.beat(name) as t:
                self.reveal(t, three, position, position + 1, 0.5)
                t.hold()

        self.fitness_walk()
        self.after_the_loop()

    def fitness_walk(self):
        with self.beat("p5_data") as t:
            self.wipe(t)
            self.title(t, "Six days  ·  quiet is under 20", fraction=0.08)
            data = fit(serif("12    15    35    10    8    7", TITLE_SIZE,
                             CHARCOAL))
            data.next_to(self.head, DOWN, buff=GAP_SM * 1.4)
            self.play(Write(data), run_time=t.fill(0.3))
            trace = self.table(
                ["Day", "Visitors", "Count", "Current", "Longest"],
                [(2, 15, 2, 2, 2), (3, 35, 2, 0, 2), (4, 10, 3, 1, 2),
                 (5, 8, 4, 2, 2), (6, 7, 5, 3, 3)],
                start=(1, 12, 1, 1, 1), top=data, row_height=0.5)
            self.play(Write(trace.head), Create(trace.rule),
                      run_time=t.fill(0.25))
            self.fitness = trace
            t.hold()

        notes = (("p5_d1", 0, "12 is quiet"),
                 ("p5_d2", 1, "15 is quiet — the streak grows"),
                 ("p5_d3", 2, "35 is not quiet — Current resets"),
                 ("p5_d4", 3, "10 is quiet — a new streak"),
                 ("p5_d5", 4, "8 is quiet"),
                 ("p5_d6", 5, "7 is quiet"))
        self.day_note = None
        for name, index, text in notes:
            with self.beat(name) as t:
                self.play(*self.fitness.step(index), run_time=t.fill(0.3))
                if self.day_note is None:
                    self.day_note = self.caption(text, SLATE, LABEL_SIZE)
                    self.foot(self.day_note)
                    self.play(Write(self.day_note), run_time=t.fill(0.25))
                else:
                    self.recaption(t, self.day_note, text, SLATE, 0.25)
                t.hold()

        with self.beat("p5_d6_record") as t:
            self.recaption(t, self.day_note,
                           "3 beats 2 — Longest becomes 3", TERRACOTTA, 0.5)
            t.hold()

        with self.beat("p5_totals") as t:
            self.wipe(t)
            totals = self.lines("quiet days  =  5",
                                "longest quiet run  =  3",
                                size=TITLE_SIZE * 1.2, color=SAGE)
            totals.move_to(UP * 0.5)
            self.play(Write(totals), run_time=t.fill(0.5))
            t.hold()

        with self.beat("p5_proves") as t:
            note = self.caption("One counter cannot do both jobs.",
                                TERRACOTTA)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

    def after_the_loop(self):
        with self.beat("p5_avg") as t:
            self.wipe(t)
            self.title(t, "After all 30 days", fraction=0.4)
            t.hold()

        with self.beat("p5_avg_code") as t:
            self.panel(t, ["Average <- ROUND(Total / 30, 2)"],
                       draw=0.14, write=0.5)
            t.hold()

        with self.beat("p5_output") as t:
            self.wipe(t)
            block = self.code(["OUTPUT Total",
                               "OUTPUT Average",
                               "OUTPUT QuietCount",
                               "OUTPUT LongestQuiet"], accent=SLATE)
            block.move_to(UP * 0.3)
            self.play(Create(block[0]), run_time=t.fill(0.1))
            self.play(Write(block[1]), run_time=t.fill(0.5))
            t.hold()

        with self.beat("p5_warn") as t:
            self.wipe(t)
            block = self.code(["IF LongestQuiet >= 4 THEN",
                               '    OUTPUT "Low activity warning"'],
                              accent=TERRACOTTA)
            block.move_to(UP * 0.9)
            self.play(Create(block[0]), run_time=t.fill(0.14))
            self.play(Write(block[1]), run_time=t.fill(0.5))
            self.warn_block = block
            t.hold()

        with self.beat("p5_warn_else") as t:
            self.panel(t, ["ELSE", '    OUTPUT "Activity normal"', "ENDIF"],
                       top=self.warn_block, draw=0.14, write=0.5)
            t.hold()

        with self.beat("p5_why4") as t:
            self.wipe(t)
            ask = fit(serif("Why >= 4 and not > 4 ?", TITLE_SIZE * 1.2,
                            CHARCOAL))
            ask.move_to(UP * 1.0)
            answer = fit(serif("Because four itself qualifies.", TITLE_SIZE,
                               TERRACOTTA))
            answer.next_to(ask, DOWN, buff=GAP_LG)
            self.play(Write(ask), run_time=t.fill(0.3))
            self.play(Write(answer), run_time=t.fill(0.3))
            self.why4 = answer
            t.hold()

        with self.beat("p5_gt4") as t:
            note = self.caption("With > 4, a four-day run would wrongly pass.")
            note.next_to(self.why4, DOWN, buff=GAP_LG)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

        with self.beat("p5_boundary") as t:
            self.wipe(t)
            self.title(t, "Boundary words change the condition",
                       fraction=0.1)
            words = self.lines("at least", "more than", "less than",
                               "no more than", "inclusive",
                               size=BODY_SIZE, color=TERRACOTTA)
            self.column([words], self.head)
            self.hide(words)
            self.reveal(t, words, 0, len(words), 0.14)
            t.hold()

        with self.beat("p5_lesson") as t:
            self.wipe(t)
            note = self.lines("The 15-mark question is not",
                              "15 marks of new knowledge.",
                              size=TITLE_SIZE)
            note.move_to(UP * 0.8)
            self.play(Write(note), run_time=t.fill(0.5))
            self.lesson = note
            t.hold()

        with self.beat("p5_familiar") as t:
            note = self.caption("It is familiar patterns, connected.")
            note.next_to(self.lesson, DOWN, buff=GAP_LG)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

        with self.beat("p5_list") as t:
            self.wipe(t)
            items = self.lines("accumulator  ·  counter  ·  array  ·  loop",
                               "validation  ·  maximum  ·  streak",
                               "selection  ·  output",
                               size=BODY_SIZE, color=SLATE)
            items.move_to(UP * 0.3)
            self.hide(items)
            self.reveal(t, items, 0, len(items), 0.26)
            t.hold()

        with self.beat("p5_code_reqs") as t:
            self.wipe(t)
            self.big_rule(t, ["DO NOT CODE THE PARAGRAPH",
                              "CODE THE REQUIREMENTS"],
                          draw=0.14, write=0.45, y=0.3)
            t.hold()

    # ----------------------------------------------------------- the recap

    def recap(self):
        with self.beat("recap_intro") as t:
            if self.strip in self.keep:
                self.keep.remove(self.strip)
            self.strip = None
            self.wipe(t)
            word = fit(serif("STEP-UP", TITLE_SIZE * 1.8, TERRACOTTA), 7.0)
            word.to_edge(UP, buff=GAP_MD * 1.4)
            spine = StepUpSpine(size=TITLE_SIZE * 1.2, width=10.5)
            spine.next_to(word, DOWN, buff=GAP_MD)
            self.play(Write(word), run_time=t.fill(0.2))
            self.play(FadeIn(spine), run_time=t.fill(0.2))
            self.recap_spine = spine
            self.keep.extend([word, spine])
            t.hold()

        pairs = (("recap_s", S, "step through one instruction",
                  "trace tables"),
                 ("recap_t", T, "tear problems into requirements",
                  "the 15-marker"),
                 ("recap_e", E, "establish initial values",
                  "counters, totals, flags"),
                 ("recap_p", P_PRESERVE, "preserve values until changed",
                  "no assignment means no change"),
                 ("recap_u", U, "use intermediate results",
                  "Boolean logic"),
                 ("recap_p2", P_PLAN, "plan before you code",
                  "the long question"))
        self.recap_text = None
        for name, index, habit, where in pairs:
            with self.beat(name) as t:
                block = self.lines(habit, where, size=TITLE_SIZE,
                                   buff=GAP_SM * 1.6)
                block[1].set_color(GREY)
                block.move_to(DOWN * 1.3)
                focus = self.recap_spine.focus(index)
                if self.recap_text is None:
                    self.recap_text = block
                    self.play(*focus, run_time=t.fill(0.25))
                    self.play(Write(block), run_time=t.fill(0.4))
                else:
                    block.move_to(self.recap_text)
                    self.play(*focus, run_time=t.fill(0.2))
                    self.play(Transform(self.recap_text, block),
                              run_time=t.fill(0.4))
                t.hold()

        with self.beat("recap_easier") as t:
            self.wipe(t)
            note = self.lines("Stop seeing dozens of topics.",
                              "Start seeing recurring patterns.",
                              size=TITLE_SIZE * 1.1)
            note.move_to(DOWN * 1.3)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

    def checklist(self):
        with self.beat("check_intro") as t:
            self.keep = [self.margin]
            self.wipe(t, 0.14)
            self.title(t, "The exam checklist", fraction=0.3)
            t.hold()

        rows = self.pairs([
            ("trace", "READ · EXECUTE · RECORD · MOVE"),
            ("no instruction", "keep the old value"),
            ("valid range", "AND"),
            ("invalid range", "OR"),
            ("flag", "FALSE · TRUE · CHECK"),
            ("Boolean", "ONE GATE · ONE COLUMN"),
            ("running total", "Total <- Total + Value"),
            ("consecutive run", "CURRENT resets · LONGEST survives"),
            ("15-marker", "PLAN BEFORE YOU CODE")],
            left_x=-6.1, right_x=-2.4, buff=GAP_SM * 1.1)
        self.stack(rows, self.head, buff=GAP_SM * 1.1, align=LEFT)
        self.hide(rows)

        # Nine lines, eight beats: the valid and invalid range land together,
        # which is how they are said.
        slices = (("check_trace", 0, 1), ("check_persist", 1, 2),
                  ("check_range", 2, 4), ("check_flag", 4, 5),
                  ("check_bool", 5, 6), ("check_total", 6, 7),
                  ("check_streak", 7, 8), ("check_15", 8, 9))
        for name, start, stop in slices:
            with self.beat(name) as t:
                self.reveal(t, rows, start, stop, 0.45 / (stop - start))
                t.hold()

    def call_to_action(self):
        with self.beat("cta") as t:
            self.wipe(t)
            ask = self.lines("Which Paper 2 skill",
                             "still costs you marks?",
                             size=TITLE_SIZE * 1.3)
            ask.to_edge(UP, buff=GAP_LG)
            self.play(Write(ask), run_time=t.fill(0.5))
            self.ask = ask
            t.hold()

        with self.beat("cta_words") as t:
            words = self.lines("TRACE", "PSEUDOCODE", "BOOLEAN", "15-MARKER",
                               size=TITLE_SIZE, color=TERRACOTTA)
            self.column([words], self.ask)
            self.hide(words)
            self.reveal(t, words, 0, len(words), 0.2)
            t.hold()

        with self.beat("cta_decide") as t:
            note = self.caption("One word in the comments. "
                                "I'll solve the winner next.")
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

        with self.beat("cta_sub") as t:
            self.wipe(t)
            logo = fit(serif("The Digital Tutor", TITLE_SIZE * 1.4, CHARCOAL))
            logo.move_to(UP * 1.2)
            note = self.caption("Cambridge O Level Computer Science 2210")
            note.next_to(logo, DOWN, buff=GAP_MD)
            self.play(Write(logo), run_time=t.fill(0.3))
            self.play(Write(note), run_time=t.fill(0.25))
            self.logo = logo
            t.hold()

        with self.beat("outro") as t:
            close = self.lines("Learn the pattern.", "Apply the pattern.",
                               "Collect the marks.",
                               size=TITLE_SIZE, color=TERRACOTTA)
            close.next_to(self.logo, DOWN, buff=GAP_LG * 1.8)
            self.hide(close)
            self.reveal(t, close, 0, len(close), 0.22)
            t.hold()
