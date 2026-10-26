"""A Level 9618 Short: trace a recursive function for its value and its call count.

Two marks, and students drop the second one. The value falls out of the
tree easily enough; the number of calls only falls out if you actually
drew the tree and counted every node, base cases included. So the tree is
the visual, and each node on screen is one call — 11 nodes, 11 calls.

Verified before building by running the function: Mystery(6) = 4, with the
call sequence 6, 3, 1, 1, 4, 2, 1, 0, 2, 1, 0 — one call for 6, three in
the Mystery(3) branch and seven in the Mystery(4) branch.

The narration says "Mystery of four returns four". It returns 2:
Mystery(4) = Mystery(2) + Mystery(2) = 1 + 1. The next sentence relies on
that 2 ("two plus two, which is four"), so the slip is in the saying, not
in the working. The screen carries 2.

Timing: timings/shorts.recursion.json
Render: python build/render.py scripts/AL2-recursion.md \\
    audio/AL2-recursion.m4a -r 1080,1920
"""

from manim import FadeIn, Write, DOWN, UP

from scenes.shorts.alevel_base import (  # pins the portrait frame on import
    CAPTION,
    LEAD,
    ALevelShort,
)
from brand import CHARCOAL, GAP_MD, GREY, SAGE, SLATE, TERRACOTTA, serif
from components.alevel import ANSWER, QUESTION, CallTree, fit, spec_block

# One node per call, laid out by hand: the portrait frame is too narrow to
# trust an automatic layout to stay inside it.
LAYOUT = [
    [("6", 0.0)],
    [("3", -1.15), ("4", 1.0)],
    [("1", -1.6), ("1", -0.7), ("2", 0.45), ("2", 1.55)],
    [("1", 0.15), ("0", 0.75), ("1", 1.25), ("0", 1.85)],
]
EDGES = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6),
         (5, 7), (5, 8), (6, 9), (6, 10)]

ROOT, B3, B4 = 0, [1, 3, 4], [2, 5, 6, 7, 8, 9, 10]


class Recursion(ALevelShort):
    scene_id = "shorts.recursion"
    strap_text = "A Level 9618 · recursion"

    def construct(self):
        self.open_strap()
        self.the_question()
        self.the_tree()
        self.the_count()

    # ------------------------------------------------------------- sections

    def the_question(self):
        with self.beat("hook") as t:
            self.hook(t, fraction=0.5)
            t.hold()

        with self.beat("study") as t:
            self.wipe(t, 0.1)
            self.code = spec_block([
                "FUNCTION Mystery(N)",
                "  IF N <= 1 THEN",
                "    RETURN N",
                "  ENDIF",
                "  RETURN Mystery(N DIV 2)",
                "       + Mystery(N - 2)",
                "ENDFUNCTION",
            ], accent=SLATE)
            self.code.move_to(UP * 1.1)
            self.play(FadeIn(self.code[0]), run_time=t.fill(0.18))
            self.play(Write(self.code[1]), run_time=t.fill(0.5))
            t.hold()

        with self.beat("base") as t:
            note = self.lines("N <= 1 returns N", size=CAPTION, color=GREY)
            self.under(note, self.code, buff=GAP_MD * 0.9)
            self.play(Write(note), run_time=t.fill(0.5))
            self.base_note = note
            t.hold()

        with self.beat("recurse") as t:
            self.recaption(t, self.base_note,
                           "otherwise it calls itself twice",
                           GREY, CAPTION, 0.5)
            t.hold()

        with self.beat("question") as t:
            self.wipe(t, 0.12)
            ask = fit(serif("Mystery(6)", ANSWER * 1.1, TERRACOTTA))
            ask.move_to(UP * 1.4)
            self.play(Write(ask), run_time=t.fill(0.5))
            self.ask = ask
            t.hold()

        with self.beat("two_parts") as t:
            parts = self.lines("what value is returned?",
                               "how many calls in total?",
                               size=QUESTION, color=CHARCOAL,
                               buff=GAP_MD * 0.9)
            self.under(parts, self.ask, buff=GAP_MD * 1.4)
            self.play(Write(parts[0]), run_time=t.fill(0.3))
            self.play(Write(parts[1]), run_time=t.fill(0.3))
            t.hold()

        with self.beat("pause") as t:
            self.pause_card(t, fraction=0.45)
            t.hold()

    def the_tree(self):
        with self.beat("solve") as t:
            self.wipe(t, 0.3)
            self.tree = CallTree(LAYOUT, EDGES, width=3.85)
            self.tree.hidden()
            self.tree.move_to(UP * 0.75)
            self.add(self.tree)
            self.note = self.caption("", GREY)
            t.hold()

        with self.beat("tree6") as t:
            self.play(FadeIn(self.tree.show_level(0)), run_time=t.fill(0.2))
            self.play(FadeIn(self.tree.show_level(1)),
                      FadeIn(self.tree.show_edges([0, 1])),
                      run_time=t.fill(0.45))
            t.hold()

        with self.beat("tree3") as t:
            self.play(FadeIn(self.tree.show_nodes([3, 4])),
                      FadeIn(self.tree.show_edges([2, 3])),
                      *self.tree.light([1]), run_time=t.fill(0.6))
            t.hold()

        with self.beat("tree3_val") as t:
            label = self.caption("Mystery(3) = 2", SAGE, 26)
            label.next_to(self.tree, DOWN, buff=GAP_MD * 0.8)
            self.play(Write(label), run_time=t.fill(0.5))
            self.value_note = label
            t.hold()

        with self.beat("tree4") as t:
            self.play(FadeIn(self.tree.show_nodes([5, 6])),
                      FadeIn(self.tree.show_edges([4, 5])),
                      *self.tree.settle([1]), *self.tree.light([2]),
                      run_time=t.fill(0.6))
            t.hold()

        with self.beat("tree2") as t:
            self.play(FadeIn(self.tree.show_nodes([7, 8, 9, 10])),
                      FadeIn(self.tree.show_edges([6, 7, 8, 9])),
                      run_time=t.fill(0.6))
            t.hold()

        with self.beat("tree2_val") as t:
            self.recaption(t, self.value_note, "each Mystery(2) = 1",
                           SAGE, 26, 0.5)
            t.hold()

        with self.beat("tree4_val") as t:
            # The narration says "returns four" here; it returns 2.
            self.recaption(t, self.value_note, "Mystery(4) = 1 + 1 = 2",
                           SAGE, 26, 0.5)
            t.hold()

        with self.beat("value") as t:
            self.recaption(t, self.value_note, "Mystery(6) = 2 + 2 = 4",
                           TERRACOTTA, 26, 0.5)
            t.hold()

    def the_count(self):
        with self.beat("count_intro") as t:
            note = self.caption("every call counts — base cases too",
                                GREY, CAPTION)
            note.next_to(self.value_note, DOWN, buff=GAP_MD * 0.8)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

        with self.beat("count_6") as t:
            self.play(*self.tree.settle(B3 + B4),
                      *self.tree.light([ROOT]), run_time=t.fill(0.5))
            t.hold()

        with self.beat("count_3") as t:
            self.play(*self.tree.settle([ROOT]), *self.tree.light(B3),
                      run_time=t.fill(0.5))
            t.hold()

        with self.beat("count_4") as t:
            self.play(*self.tree.settle(B3), *self.tree.light(B4),
                      run_time=t.fill(0.5))
            t.hold()

        with self.beat("total") as t:
            self.play(*self.tree.light([ROOT] + B3 + B4),
                      run_time=t.fill(0.5))
            t.hold()

        with self.beat("answer") as t:
            self.wipe(t, 0.14)
            self.reveal_answer(t, ["value  4", "calls  11"], y=0.7,
                               draw=0.2, write=0.45)
            t.hold()

        with self.beat("trap") as t:
            trap = self.lines("1  +  3  +  7  =  11",
                              size=LEAD, color=SAGE)
            trap.move_to(DOWN * 1.1)
            self.play(Write(trap), run_time=t.fill(0.5))
            t.hold()

        with self.beat("close") as t:
            self.wipe(t, 0.2)
            self.close_series(t, fraction=0.45)
            t.hold()
