"""STEP-UP Short 5: how to start a 15-mark programming question.

The answer is not to code. It is to break the paragraph into requirements,
each of which is a pattern the student already knows, and the Short builds
that mapping a row at a time.

The scenario (365 rainfall values, dry streaks, drought) is our own
recreation of the archetype; the Cambridge question is named in the strap
line only.

Timing: timings/shorts.fifteen_marker.json
"""

from manim import FadeIn, FadeOut, VGroup, UP, DOWN, LEFT, RIGHT

from scenes.shorts.stepup_base import (  # pins the portrait frame on import
    CAPTION,
    HOOK,
    LEAD,
    StepUpShort,
)
from brand import CHARCOAL, GAP_MD, GAP_SM, GREY, SLATE, TERRACOTTA, serif
from components.stepup import fit, rule_card

# the requirement the paragraph states, and the pattern that answers it
REQUIREMENTS = [
    ("r_array",   "store 365 values",   "ARRAY"),
    ("r_input",   "enter them",         "INPUT + LOOP"),
    ("r_accum",   "add them up",        "ACCUMULATOR"),
    ("r_count",   "count dry days",     "COUNTER"),
    ("r_streak",  "longest dry run",    "STREAK + MAX"),
    ("r_drought", "drought if 15+",     "IF"),
]


class FifteenMarker(StepUpShort):
    scene_id = "shorts.fifteen_marker"
    strap_text = "O Level CS · Paper 2 · the 15-marker"

    def construct(self):
        self.open_strap()
        self.opening()
        self.requirements()
        self.streak_rule()
        self.closing()

    def opening(self):
        with self.beat("hook") as t:
            head = self.lines("15 MARKS", size=HOOK * 1.3, color=CHARCOAL)
            sub = self.lines("and absolutely no idea", "where to start",
                             size=CAPTION, color=GREY)
            block = self.stack(head, sub, buff=GAP_MD * 1.4)
            block.move_to(UP * 1.4)
            self.show(t, head, 0.3)
            self.show(t, sub, 0.2)
            self.block = block
            t.hold()

        with self.beat("dont_code") as t:
            good = serif("Good. Don't code.", LEAD, TERRACOTTA)
            fit(good)
            good.next_to(self.block, DOWN, buff=GAP_MD * 1.8)
            self.show(t, good, 0.55)
            t.hold()

        with self.beat("destroy") as t:
            job = self.lines("your first job is to", "destroy the big problem",
                             size=CAPTION, color=CHARCOAL)
            job.to_edge(DOWN, buff=GAP_MD * 2.0)
            self.show(t, job, 0.5)
            t.hold()

        with self.beat("break_req") as t:
            self.wipe(t, 0.18)
            card = rule_card(["BREAK IT INTO", "REQUIREMENTS"])
            card.move_to(UP * 0.6)
            self.show(t, card, 0.55, how=FadeIn)
            t.hold()

    def requirements(self):
        """One row per requirement: what the paragraph asks, what answers it."""
        # Two real columns: the needs share a left edge and the patterns
        # share one too, so the eye can run down either side. Building them
        # as independent columns beats aligning row by row, which leaves the
        # right-hand column ragged.
        needs = VGroup(*[serif(n, CAPTION, GREY) for _, n, _ in REQUIREMENTS])
        needs.arrange(DOWN, buff=GAP_MD * 0.8, aligned_edge=LEFT)
        pats = VGroup(*[serif(p, CAPTION, SLATE) for _, _, p in REQUIREMENTS])
        pats.arrange(DOWN, buff=GAP_MD * 0.8, aligned_edge=LEFT)
        pats.next_to(needs, RIGHT, buff=GAP_SM * 1.3)
        for need, pat in zip(needs, pats):
            pat.set_y(need.get_y())

        table = VGroup(*[VGroup(n, p) for n, p in zip(needs, pats)])
        whole = VGroup(needs, pats)
        # A touch wider than the usual 3.9 guard: this table is the
        # densest thing in the series and 4.05 still leaves a clear
        # margin in a 4.5-unit frame, which buys back legibility.
        fit(whole, 4.05)
        whole.move_to(DOWN * 0.3)

        for i, (beat_name, _, _) in enumerate(REQUIREMENTS):
            with self.beat(beat_name) as t:
                if i == 0:
                    self.wipe(t, 0.12)
                self.show(t, table[i], 0.5 if i else 0.4)
                t.hold()
        self.table = table

        with self.beat("six") as t:
            note = self.lines("not one 15-mark problem —",
                              "six patterns you know", size=CAPTION,
                              color=CHARCOAL)
            note.next_to(self.table, DOWN, buff=GAP_MD * 1.4)
            self.show(t, note, 0.4)
            t.hold()

    def streak_rule(self):
        with self.beat("streak_rule") as t:
            self.wipe(t, 0.12)
            head = serif("the crucial streak rule", LEAD, CHARCOAL)
            fit(head)
            head.move_to(UP * 2.6)
            self.show(t, head, 0.5)
            self.head = head
            t.hold()

        with self.beat("current") as t:
            body = self.lines("the current streak resets", "when rain falls",
                              "the longest one does not", size=CAPTION,
                              color=GREY)
            body.next_to(self.head, DOWN, buff=GAP_MD * 1.6)
            self.show(t, body, 0.4)
            self.body = body
            t.hold()

        with self.beat("card") as t:
            card = rule_card(["CURRENT RESETS", "RECORD SURVIVES"])
            card.next_to(self.body, DOWN, buff=GAP_MD * 1.6)
            self.show(t, card, 0.55, how=FadeIn)
            t.hold()

    def closing(self):
        with self.beat("never_code") as t:
            self.wipe(t, 0.12)
            line = self.lines("never code the paragraph.",
                              "code the requirements.", size=LEAD,
                              color=CHARCOAL)
            line.move_to(UP * 1.0)
            self.show(t, line, 0.5)
            self.line = line
            t.hold()

        with self.beat("close") as t:
            self.play(FadeOut(self.line), run_time=t.fill(0.06))
            self.close_series(t, 0.3)
            t.hold()
