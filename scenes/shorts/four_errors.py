"""STEP-UP Short 3: find the four pseudocode errors.

Four debugging fixes, each shown as the broken line in terracotta and the
corrected line in sage directly beneath, so the viewer sees the swap
rather than being told about it.

The pseudocode is our own recreation of the archetype — an account search
over a 2D array — not a reproduction of the Cambridge question, which is
referred to only in the strap line.

Timing: timings/shorts.four_errors.json
"""

from manim import FadeIn, FadeOut, UP, DOWN

from scenes.shorts.stepup_base import (  # pins the portrait frame on import
    CAPTION,
    HOOK,
    LEAD,
    StepUpShort,
)
from brand import CHARCOAL, GAP_MD, GREY, SAGE, TERRACOTTA, serif
from components.stepup import code_block, fit
from components.word_arc import WordArc

DEBUG = ["Purpose", "Line", "Effect"]


class FourErrors(StepUpShort):
    scene_id = "shorts.four_errors"
    strap_text = "O Level CS · Paper 2 · debugging"

    def construct(self):
        self.open_strap()
        self.opening()
        self.error_one()
        self.error_two()
        self.error_three()
        self.error_four()
        self.closing()

    # -------------------------------------------------------------- helpers

    def swap(self, t, label, broken, fixed, label_fraction=0.22,
             code_fraction=0.24):
        """Name the error, show the broken line, then the corrected one."""
        self.wipe(t, 0.08)
        head = serif(label, LEAD, CHARCOAL)
        fit(head)
        head.move_to(UP * 2.4)
        self.show(t, head, label_fraction)
        wrong = code_block([broken], accent=TERRACOTTA)
        wrong.next_to(head, DOWN, buff=GAP_MD * 1.5)
        self.show(t, wrong, code_fraction, how=FadeIn)
        return head, wrong

    def correction(self, t, after, fixed, fraction=0.3):
        right = code_block([fixed], accent=SAGE)
        right.next_to(after, DOWN, buff=GAP_MD * 1.5)
        self.show(t, right, fraction, how=FadeIn)
        return right

    # ------------------------------------------------------------- sections

    def opening(self):
        with self.beat("hook") as t:
            head = self.lines("4 ERRORS", size=HOOK * 1.3, color=CHARCOAL)
            sub = self.lines("can you find them", "before I do?", size=CAPTION,
                             color=GREY)
            block = self.stack(head, sub, buff=GAP_MD * 1.4)
            block.move_to(UP * 1.4)
            self.show(t, head, 0.28)
            self.show(t, sub, 0.2)
            t.hold()

        with self.beat("context") as t:
            self.wipe(t, 0.1)
            what = self.lines("the program searches for", "an account ID,",
                              "then shows the customer", size=CAPTION,
                              color=CHARCOAL)
            what.move_to(UP * 0.8)
            self.show(t, what, 0.44)
            t.hold()

    def error_one(self):
        with self.beat("err1") as t:
            head, wrong = self.swap(
                t, "error 1 · the data type",
                "DECLARE AccountID : INTEGER", None,
                label_fraction=0.16, code_fraction=0.18)
            note = serif("letters AND numbers", CAPTION, GREY)
            fit(note)
            note.next_to(wrong, DOWN, buff=GAP_MD * 1.2)
            self.show(t, note, 0.18)
            self.anchor = note
            t.hold()

        with self.beat("fix1") as t:
            self.correction(t, self.anchor, "DECLARE AccountID : STRING", 0.5)
            t.hold()

    def error_two(self):
        with self.beat("err2") as t:
            self.wipe(t, 0.1)
            head = serif("error 2 · the wrong verb", LEAD, CHARCOAL)
            fit(head)
            head.move_to(UP * 2.4)
            self.show(t, head, 0.26)
            note = serif("the user must enter it", CAPTION, GREY)
            fit(note)
            note.next_to(head, DOWN, buff=GAP_MD * 1.2)
            self.show(t, note, 0.26)
            self.anchor = note
            t.hold()

        with self.beat("wrong2") as t:
            wrong = code_block(["OUTPUT AccountID"], accent=TERRACOTTA)
            wrong.next_to(self.anchor, DOWN, buff=GAP_MD * 1.4)
            self.show(t, wrong, 0.5, how=FadeIn)
            self.anchor = wrong
            t.hold()

        with self.beat("fix2") as t:
            self.correction(t, self.anchor, "INPUT AccountID", 0.5)
            t.hold()

    def error_three(self):
        with self.beat("err3") as t:
            self.wipe(t, 0.08)
            head = serif("error 3 · one condition", LEAD, CHARCOAL)
            fit(head)
            head.move_to(UP * 2.4)
            self.show(t, head, 0.18)
            note = serif("testing one thing — so not CASE", CAPTION, GREY)
            fit(note)
            note.next_to(head, DOWN, buff=GAP_MD * 1.2)
            self.show(t, note, 0.18)
            # Show the broken line too, so this error reads the same way as
            # the other three: terracotta wrong, sage right, directly below.
            wrong = code_block(["CASE OF AccountID"], accent=TERRACOTTA)
            wrong.next_to(note, DOWN, buff=GAP_MD * 1.3)
            self.show(t, wrong, 0.22, how=FadeIn)
            self.anchor = wrong
            t.hold()

        with self.beat("fix3") as t:
            self.correction(t, self.anchor,
                            "IF AccountID = Accounts[Row, 1] THEN", 0.5)
            t.hold()

    def error_four(self):
        with self.beat("err4") as t:
            self.wipe(t, 0.12)
            head = serif("error 4 · the sneaky one", LEAD, TERRACOTTA)
            fit(head)
            head.move_to(UP * 2.4)
            self.show(t, head, 0.5)
            self.anchor = head
            t.hold()

        with self.beat("why4") as t:
            wrong = code_block(["OUTPUT Accounts[1, 2]"], accent=TERRACOTTA)
            wrong.next_to(self.anchor, DOWN, buff=GAP_MD * 1.4)
            self.show(t, wrong, 0.22, how=FadeIn)
            note = self.lines("found on row 427 —", "so why show row 1?",
                              size=CAPTION, color=GREY)
            note.next_to(wrong, DOWN, buff=GAP_MD * 1.2)
            self.show(t, note, 0.3)
            self.anchor = note
            t.hold()

        with self.beat("fix4") as t:
            self.correction(t, self.anchor, "OUTPUT Accounts[Row, 2]", 0.3)
            t.hold()

    def closing(self):
        with self.beat("memory") as t:
            self.wipe(t, 0.06)
            line = self.lines("when debugging,", "don't stare at the code",
                              size=LEAD, color=CHARCOAL)
            line.move_to(UP * 2.0)
            self.show(t, line, 0.3)
            self.line = line
            t.hold()

        with self.beat("ple") as t:
            arc = WordArc(DEBUG, size=LEAD, dim=CHARCOAL, lit=TERRACOTTA)
            fit(arc)
            arc.next_to(self.line, DOWN, buff=GAP_MD * 1.8)
            self.show(t, arc, 0.55, how=FadeIn)
            t.hold()

        with self.beat("close") as t:
            self.wipe(t, 0.08)
            self.close_series(t, 0.3)
            t.hold()
