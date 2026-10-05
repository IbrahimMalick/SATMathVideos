"""STEP-UP Short 1: the trace-table mistake that costs easy marks.

Resetting a variable the algorithm never told you to. The lesson is one
line long — no assignment means no change — so the Short spends its time
on a worked trace the viewer can follow a pair at a time.

The example word is our own (BALLOON); the Cambridge question is referred
to in the strap line only, never shown.

Timing: timings/shorts.trace_table.json
Render: python build/render.py scripts/P2S1-trace-table.md \\
    audio/P2S1-trace-table.m4a -r 1080,1920
"""

from manim import (
    FadeIn,
    FadeOut,
    SurroundingRectangle,
    Transform,
    VGroup,
    Write,
    DOWN,
    RIGHT,
    UP,
)

from scenes.shorts.stepup_base import (  # pins the portrait frame on import
    ANSWER,
    CAPTION,
    HOOK,
    LEAD,
    StepUpShort,
)
from brand import CHARCOAL, GAP_MD, GAP_SM, GREY, SAGE, SLATE, TERRACOTTA, serif
from components.stepup import code_block, fit, rule_card
from components.word_arc import WordArc

WORD = "BALLOON"
# the pairs he walks, and what Count is after each
TRACE = [(0, "no match", 0), (1, "no match", 0), (2, "MATCH", 1),
         (3, "no match", 1), (4, "MATCH", 2)]
STEPS = ["Read", "Execute", "Record", "Move"]


class TraceTable(StepUpShort):
    scene_id = "shorts.trace_table"
    strap_text = "O Level CS · Paper 2 · trace tables"

    def construct(self):
        self.open_strap()
        self.opening()
        self.the_rule()
        self.worked_trace()
        self.closing()

    # -------------------------------------------------------------- helpers

    def letter_row(self):
        row = VGroup(*[serif(ch, ANSWER, CHARCOAL) for ch in WORD])
        row.arrange(RIGHT, buff=GAP_SM * 0.7)
        return fit(row)

    def count_label(self, value, colour=SLATE):
        label = serif(f"Count = {value}", LEAD, colour)
        return fit(label)

    # ------------------------------------------------------------- sections

    def opening(self):
        with self.beat("hook") as t:
            head = self.lines("ONE TRACE TABLE", "MISTAKE", size=HOOK,
                              color=CHARCOAL)
            cost = serif("that costs easy marks", CAPTION, GREY)
            block = self.stack(head, fit(cost), buff=GAP_MD * 1.4)
            block.move_to(UP * 1.2)
            self.show(t, head, 0.3)
            self.show(t, cost, 0.16)
            t.hold()

        with self.beat("reset") as t:
            self.wipe(t, 0.1)
            mistake = self.lines("resetting a variable", "the algorithm never",
                                 "told you to", size=LEAD, color=TERRACOTTA)
            mistake.move_to(UP * 0.8)
            self.show(t, mistake, 0.4)
            t.hold()

        with self.beat("count0") as t:
            self.wipe(t, 0.12)
            self.code = code_block(["Count ← 0"])
            self.code.move_to(UP * 1.6)
            self.show(t, self.code, 0.4, how=FadeIn)
            t.hold()

        with self.beat("match") as t:
            pair = serif("two neighbouring letters match", CAPTION, GREY)
            fit(pair)
            pair.next_to(self.code, DOWN, buff=GAP_MD * 1.4)
            self.show(t, pair, 0.3)
            self.pair_note = pair
            t.hold()

        with self.beat("increment") as t:
            step = code_block(["Count ← Count + 1"])
            step.next_to(self.pair_note, DOWN, buff=GAP_MD * 1.3)
            self.show(t, step, 0.26, how=FadeIn)
            now = self.count_label(1)
            now.next_to(step, DOWN, buff=GAP_MD * 1.3)
            self.show(t, now, 0.26)
            self.now = now
            t.hold()

    def the_rule(self):
        with self.beat("next_pair") as t:
            ask = serif("next pair does NOT match", CAPTION, CHARCOAL)
            fit(ask)
            ask.next_to(self.now, DOWN, buff=GAP_MD * 1.2)
            self.show(t, ask, 0.4)
            t.hold()

        with self.beat("rule") as t:
            self.wipe(t, 0.08)
            stays = self.count_label(1, CHARCOAL)
            stays.move_to(UP * 2.0)
            card = rule_card(["NO ASSIGNMENT", "=", "NO CHANGE"])
            card.next_to(stays, DOWN, buff=GAP_MD * 1.8)
            self.show(t, stays, 0.14)
            self.show(t, card, 0.3, how=FadeIn)
            t.hold()

    def worked_trace(self):
        with self.beat("example") as t:
            self.wipe(t, 0.1)
            self.row = self.letter_row()
            self.row.move_to(UP * 1.8)
            self.count = self.count_label(0)
            self.count.next_to(self.row, DOWN, buff=GAP_MD * 2.2)
            self.show(t, self.row, 0.34)
            self.show(t, self.count, 0.2)
            self.box = None
            self.verdict = None
            t.hold()

        for name, (index, verdict, value) in zip(
                ("trace_ba", "trace_al", "trace_ll", "trace_lo", "trace_oo"),
                TRACE):
            with self.beat(name) as t:
                pair = VGroup(self.row[index], self.row[index + 1])
                colour = SAGE if verdict == "MATCH" else GREY
                box = SurroundingRectangle(pair, color=TERRACOTTA,
                                           buff=GAP_SM * 0.5, stroke_width=4)
                if self.box is None:
                    self.play(FadeIn(box), run_time=t.fill(0.18))
                    self.box = box
                else:
                    self.play(Transform(self.box, box), run_time=t.fill(0.2))
                said = serif(verdict, CAPTION, colour)
                fit(said)
                said.next_to(self.count, DOWN, buff=GAP_MD * 1.2)
                if self.verdict is None:
                    self.play(Write(said), run_time=t.fill(0.18))
                    self.verdict = said
                else:
                    self.play(Transform(self.verdict, said),
                              run_time=t.fill(0.18))
                new_count = self.count_label(value)
                new_count.move_to(self.count)
                self.play(Transform(self.count, new_count),
                          run_time=t.fill(0.18))
                t.hold()

    def closing(self):
        with self.beat("steps") as t:
            self.wipe(t, 0.07)
            dont = serif("do not trace in your head", CAPTION, GREY)
            fit(dont)
            dont.move_to(UP * 2.2)
            arc = WordArc(STEPS, size=LEAD, rows=2, dim=CHARCOAL,
                          lit=TERRACOTTA)
            fit(arc)
            arc.next_to(dont, DOWN, buff=GAP_MD * 1.8)
            self.show(t, dont, 0.14)
            self.show(t, arc, 0.3)
            t.hold()

        with self.beat("close") as t:
            self.wipe(t, 0.05)
            line = self.lines("if the program does not", "change the variable,",
                              "neither do you", size=LEAD, color=CHARCOAL)
            line.move_to(UP * 1.6)
            self.show(t, line, 0.22)
            self.wait(t.fill(0.1))
            self.play(FadeOut(line), run_time=t.fill(0.05))
            self.close_series(t, 0.22)
            t.hold()
