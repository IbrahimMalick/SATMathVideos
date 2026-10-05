"""STEP-UP Short 2: AND or OR? The range trick.

One sentence to remember — inside a range is AND, outside is OR — then the
trap that proves it: swapping AND for OR in a valid-range check lets 50
through a 10-to-18 filter.

The delivery says "more than 10 and less than 18" loosely; the range he
describes is "from 10 to 18", which is inclusive, so the screen carries
>= and <= as his own brief specifies.

Timing: timings/shorts.and_or.json
"""

from manim import FadeIn, FadeOut, UP, DOWN

from scenes.shorts.stepup_base import (  # pins the portrait frame on import
    CAPTION,
    HOOK,
    LEAD,
    StepUpShort,
)
from brand import CHARCOAL, GAP_MD, GREY, SAGE, TERRACOTTA, serif
from components.stepup import code_block, fit, rule_card

RULE = ["INSIDE = AND", "OUTSIDE = OR"]


class AndOr(StepUpShort):
    scene_id = "shorts.and_or"
    strap_text = "O Level CS · Paper 2 · validation"

    def construct(self):
        self.open_strap()
        self.opening()
        self.the_range()
        self.the_trap()
        self.closing()

    def opening(self):
        with self.beat("hook") as t:
            head = self.lines("AND or OR?", size=HOOK, color=CHARCOAL)
            sub = serif("stop guessing in validation", CAPTION, GREY)
            block = self.stack(head, fit(sub), buff=GAP_MD * 1.4)
            block.move_to(UP * 1.4)
            self.show(t, head, 0.3)
            self.show(t, sub, 0.18)
            t.hold()

        with self.beat("rule") as t:
            self.wipe(t, 0.12)
            card = rule_card(RULE)
            card.move_to(UP * 0.8)
            self.show(t, card, 0.42, how=FadeIn)
            t.hold()

    def the_range(self):
        with self.beat("range") as t:
            self.wipe(t, 0.1)
            self.head = self.lines("a valid age is", "10 to 18", size=LEAD,
                                   color=CHARCOAL)
            self.head.move_to(UP * 2.2)
            self.show(t, self.head, 0.34)
            t.hold()

        with self.beat("and_cond") as t:
            self.valid = code_block(["Age >= 10 AND Age <= 18"])
            self.valid.next_to(self.head, DOWN, buff=GAP_MD * 1.6)
            self.show(t, self.valid, 0.26, how=FadeIn)
            t.hold()

        with self.beat("why_and") as t:
            why = serif("both boundaries must hold", CAPTION, GREY)
            fit(why)
            why.next_to(self.valid, DOWN, buff=GAP_MD * 1.2)
            self.show(t, why, 0.3)
            self.why = why
            t.hold()

        with self.beat("invalid") as t:
            # Clear here rather than keep stacking: the narration turns from
            # "valid" to "invalid", and six blocks will not fit the frame.
            self.wipe(t, 0.12)
            ask = serif("when is it INVALID?", LEAD, CHARCOAL)
            fit(ask)
            ask.move_to(UP * 2.2)
            self.show(t, ask, 0.4)
            self.ask = ask
            t.hold()

        with self.beat("or_cond") as t:
            self.invalid = code_block(["Age < 10 OR Age > 18"])
            self.invalid.next_to(self.ask, DOWN, buff=GAP_MD * 1.2)
            self.show(t, self.invalid, 0.26, how=FadeIn)
            t.hold()

        with self.beat("low_high") as t:
            note = serif("too low, or too high", CAPTION, GREY)
            fit(note)
            note.next_to(self.invalid, DOWN, buff=GAP_MD)
            self.show(t, note, 0.34)
            t.hold()

    def the_trap(self):
        with self.beat("trap") as t:
            self.wipe(t, 0.14)
            warn = serif("the dangerous mistake", LEAD, TERRACOTTA)
            fit(warn)
            warn.move_to(UP * 2.4)
            self.show(t, warn, 0.4)
            self.warn = warn
            t.hold()

        with self.beat("try50") as t:
            self.bad = code_block(["Age >= 10 OR Age <= 18"],
                                  accent=TERRACOTTA)
            self.bad.next_to(self.warn, DOWN, buff=GAP_MD * 1.4)
            self.show(t, self.bad, 0.5, how=FadeIn)
            t.hold()

        with self.beat("check") as t:
            test = self.lines("try Age = 50", "is 50 >= 10 ?   YES",
                              size=LEAD, color=CHARCOAL)
            test.next_to(self.bad, DOWN, buff=GAP_MD * 1.4)
            self.show(t, test, 0.4)
            self.test = test
            t.hold()

        with self.beat("accepted") as t:
            out = serif("so 50 is ACCEPTED", LEAD, TERRACOTTA)
            fit(out)
            out.next_to(self.test, DOWN, buff=GAP_MD * 1.2)
            self.show(t, out, 0.4)
            t.hold()

    def closing(self):
        with self.beat("why") as t:
            self.wipe(t, 0.08)
            line = self.lines("that is why a valid range", "uses AND",
                              size=LEAD, color=CHARCOAL)
            line.move_to(UP * 2.0)
            self.show(t, line, 0.4)
            self.line = line
            t.hold()

        with self.beat("again") as t:
            card = rule_card(RULE)
            card.next_to(self.line, DOWN, buff=GAP_MD * 1.8)
            self.show(t, card, 0.42, how=FadeIn)
            t.hold()

        with self.beat("close") as t:
            self.wipe(t, 0.05)
            line = self.lines("don't memorise twenty examples.",
                              "memorise the rule.", size=CAPTION,
                              color=CHARCOAL)
            line.move_to(UP * 1.6)
            self.show(t, line, 0.2)
            self.wait(t.fill(0.1))
            self.play(FadeOut(line), run_time=t.fill(0.05))
            self.close_series(t, 0.22)
            t.hold()
