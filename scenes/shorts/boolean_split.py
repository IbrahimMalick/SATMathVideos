"""STEP-UP Short 4: never solve a Boolean expression all at once.

The expression is taken apart one gate at a time, each intermediate given
its own name, so the truth table that follows has one column per gate.
The working lines accumulate on screen — the point is that the answer gets
built, not spotted.

Expression and working are our own; the Cambridge question is named in the
strap line only.

Timing: timings/shorts.boolean_split.json
"""

from manim import FadeIn, FadeOut, VGroup, UP, DOWN, LEFT

from scenes.shorts.stepup_base import (  # pins the portrait frame on import
    CAPTION,
    LEAD,
    StepUpShort,
)
from brand import CHARCOAL, GAP_MD, GAP_SM, GREY, SLATE, TERRACOTTA, mono, serif
from components.stepup import CODE, code_block, fit, rule_card

WORKING = [
    ("x1", "X1 ← NOT C"),
    ("x2", "X2 ← B OR X1"),
    ("x3", "X3 ← NOT X2"),
    ("x4", "X4 ← A NAND C"),
    ("final_z", "Z  ← X3 XOR X4"),
]


class BooleanSplit(StepUpShort):
    scene_id = "shorts.boolean_split"
    strap_text = "O Level CS · Paper 2 · Boolean logic"

    def construct(self):
        self.open_strap()
        self.opening()
        self.build_working()
        self.closing()

    def opening(self):
        with self.beat("hook") as t:
            warn = self.lines("don't solve it", "in your head", size=LEAD,
                              color=GREY)
            warn.move_to(UP * 2.6)
            expr = code_block(["Z = NOT(B OR NOT C)", "        XOR (A NAND C)"],
                              accent=TERRACOTTA)
            expr.next_to(warn, DOWN, buff=GAP_MD * 1.6)
            self.show(t, warn, 0.22)
            self.show(t, expr, 0.3, how=FadeIn)
            self.expr = expr
            t.hold()

        with self.beat("dont_panic") as t:
            tell = self.lines("don't panic.", "don't simplify.",
                              "break it apart.", size=LEAD, color=CHARCOAL)
            tell.next_to(self.expr, DOWN, buff=GAP_MD * 1.6)
            self.show(t, tell, 0.5)
            self.tell = tell
            t.hold()

    def build_working(self):
        """Each gate gets its own line, and the lines stay on screen.

        The whole block is laid out up front and revealed a line at a time,
        so the lines share one left edge instead of drifting as they arrive.
        """
        self.rows = VGroup(*[mono(text, CODE, CHARCOAL) for _, text in WORKING])
        self.rows.arrange(DOWN, buff=GAP_SM * 1.3, aligned_edge=LEFT)
        fit(self.rows, 3.6)
        self.rows[-1].set_color(TERRACOTTA)     # Z is the one to look at

        for i, (beat_name, _) in enumerate(WORKING):
            with self.beat(beat_name) as t:
                if i == 0:
                    self.wipe(t, 0.14)
                    head = serif("one gate at a time", CAPTION, GREY)
                    fit(head)
                    head.move_to(UP * 2.8)
                    self.show(t, head, 0.16)
                    self.rows.next_to(head, DOWN, buff=GAP_MD * 1.4)
                self.show(t, self.rows[i], 0.45 if i else 0.3)
                t.hold()

    def closing(self):
        with self.beat("table") as t:
            note = self.lines("every intermediate result",
                              "gets its own column", size=CAPTION,
                              color=GREY)
            note.next_to(self.rows, DOWN, buff=GAP_MD * 1.4)
            self.show(t, note, 0.3)
            t.hold()

        with self.beat("one_gate") as t:
            self.wipe(t, 0.14)
            card = rule_card(["ONE GATE", "=", "ONE COLUMN"])
            card.move_to(UP * 1.0)
            self.show(t, card, 0.6, how=FadeIn)
            self.card = card
            t.hold()

        with self.beat("never") as t:
            never = self.lines("never jump from A, B, C", "straight to Z",
                               size=LEAD, color=CHARCOAL)
            never.next_to(self.card, DOWN, buff=GAP_MD * 1.8)
            self.show(t, never, 0.42)
            t.hold()

        with self.beat("close") as t:
            self.wipe(t, 0.06)
            line = self.lines("STEP-UP rule U:", "use intermediate results",
                              size=CAPTION, color=CHARCOAL)
            line.move_to(UP * 1.6)
            self.show(t, line, 0.2)
            self.wait(t.fill(0.1))
            self.play(FadeOut(line), run_time=t.fill(0.06))
            self.close_series(t, 0.26)
            t.hold()
