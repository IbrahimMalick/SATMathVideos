"""Concept lecture: the inference question (O Level English, ~2 minutes).

Rendered SILENT — the narrator records over it in Camtasia, so the timing
file is hand-authored to the script's section stamps rather than synced to
a recording. Beats land where the script's [0:12], [0:40], [1:05], [1:38]
marks fall.

Render: python -m manim render -qh scenes/concept/inference.py Inference
Deliver media/videos/inference/1080p60/Inference.mp4 as-is (no mux).
"""

from manim import (
    Create,
    FadeIn,
    FadeOut,
    Line,
    VGroup,
    Write,
    DOWN,
    LEFT,
    ORIGIN,
    UP,
)

from brand import (
    BODY_SIZE,
    GAP_MD,
    GAP_SM,
    GREY,
    LABEL_SIZE,
    MARGIN_SIZE,
    SAGE,
    TERRACOTTA,
    TITLE_SIZE,
    mono,
    serif,
)
from components.passage import PassageHighlight
from scenes.base import SATScene

PASSAGE_1 = (
    "Hamza glanced at the clock for the third time. He tapped his "
    "fingers on the table as the waiter walked past him again."
)
PASSAGE_2 = (
    "Sara smiled as she unfolded the results sheet. A moment later, she "
    "quietly folded it again and slipped it into her bag before her "
    "friends could see it."
)
WRAP = 48


class Inference(SATScene):
    scene_id = "concept.inference"

    def underline(self, mobject, color=SAGE):
        from manim import RIGHT
        return Line(
            mobject.get_corner(DOWN + LEFT) + DOWN * GAP_SM,
            mobject.get_corner(DOWN + RIGHT) + DOWN * GAP_SM,
            color=color,
            stroke_width=3,
        )

    def construct(self):
        margin = mono("O Level English · inference", MARGIN_SIZE)
        margin.to_corner(UP + LEFT, buff=GAP_SM)
        self.add(margin)

        # ----------------------------------------------------------- hook
        title = serif("The Inference Question", TITLE_SIZE * 1.25)
        title.to_edge(UP, buff=GAP_MD * 1.9)
        sub = VGroup(
            serif("it destroys marks — even when you", BODY_SIZE, GREY),
            serif("understood the passage perfectly", BODY_SIZE, GREY),
        ).arrange(DOWN, buff=GAP_SM)
        sub.next_to(title, DOWN, buff=GAP_MD)
        promise = serif("two minutes — and you'll know exactly what to do",
                        LABEL_SIZE, TERRACOTTA)
        promise.next_to(sub, DOWN, buff=GAP_MD * 1.4)

        with self.beat("hook") as t:
            self.play(Write(title), run_time=t.fill(0.3))
            self.play(Write(sub), run_time=t.fill(0.25))
            self.play(Write(promise), run_time=t.fill(0.2))
            t.hold()

        # ------------------------------------------------------- passage 1
        head1 = serif("Example 1", TITLE_SIZE)
        head1.to_edge(UP, buff=GAP_MD * 1.6)
        pass1 = PassageHighlight(PASSAGE_1, width=WRAP)
        pass1.next_to(head1, DOWN, buff=GAP_MD * 1.3)
        q1 = serif("What can you infer about Hamza?", BODY_SIZE)
        q1.next_to(pass1, DOWN, buff=GAP_MD * 1.3)

        with self.beat("passage1") as t:
            self.play(FadeOut(title), FadeOut(sub), FadeOut(promise),
                      run_time=t.fill(0.1))
            self.play(Write(head1), run_time=t.fill(0.12))
            self.play(Write(pass1), run_time=t.fill(0.4))
            self.play(Write(q1), run_time=t.fill(0.2))
            t.hold()

        # ----------------------------------------------------------- wrong
        attempt = serif('"Hamza looked at the clock three times."',
                        BODY_SIZE)
        attempt.next_to(q1, DOWN, buff=GAP_MD * 1.3)
        strike = Line(
            attempt.get_left() + LEFT * 0.15,
            attempt.get_right() - LEFT * 0.15,
            color=TERRACOTTA, stroke_width=4,
        )
        why = serif("that's not inference — the passage already told us that",
                    LABEL_SIZE, GREY)
        why.next_to(attempt, DOWN, buff=GAP_MD)

        with self.beat("wrong") as t:
            self.play(Write(attempt), run_time=t.fill(0.3))
            self.play(Create(strike), run_time=t.fill(0.12))
            self.play(Write(why), run_time=t.fill(0.25))
            t.hold()

        # ---------------------------------------------------------- method
        mnemonic = serif("CLUE  →  THINK  →  INFER", TITLE_SIZE * 1.15)
        mnemonic.move_to(ORIGIN)

        with self.beat("method") as t:
            self.play(FadeOut(head1), FadeOut(pass1), FadeOut(q1),
                      FadeOut(attempt), FadeOut(strike), FadeOut(why),
                      run_time=t.fill(0.12))
            self.play(Write(mnemonic), run_time=t.fill(0.4))
            self.play(Create(self.underline(mnemonic)), run_time=t.fill(0.15))
            t.hold()

        # ----------------------------------------------------------- clue 1
        pass1a = PassageHighlight(PASSAGE_1, highlight="glanced at the clock",
                                  width=WRAP)
        pass1a.to_edge(UP, buff=GAP_MD * 2.2)
        think1 = serif("clue: he keeps checking the clock → he's waiting",
                       BODY_SIZE)
        think1.next_to(pass1a, DOWN, buff=GAP_MD * 1.4)

        with self.beat("clue1") as t:
            old = [m for m in self.mobjects if m is not margin]
            self.play(*[FadeOut(m) for m in old], run_time=t.fill(0.1))
            self.play(FadeIn(pass1a), run_time=t.fill(0.2))
            self.play(Write(think1), run_time=t.fill(0.3))
            t.hold()

        # ----------------------------------------------------------- clue 2
        pass1b = PassageHighlight(PASSAGE_1, highlight="tapped his fingers",
                                  width=WRAP)
        pass1b.move_to(pass1a)
        think2 = serif("clue: tapping his fingers → he's getting impatient",
                       BODY_SIZE)
        think2.next_to(think1, DOWN, buff=GAP_MD)

        with self.beat("clue2") as t:
            self.play(FadeOut(pass1a), FadeIn(pass1b), run_time=t.fill(0.15))
            self.play(Write(think2), run_time=t.fill(0.35))
            t.hold()

        # ---------------------------------------------------------- model 1
        model1 = PassageHighlight(
            "Hamza is becoming impatient because he has been waiting "
            "longer than he expected.",
            width=WRAP, color=SAGE,
        )
        model1.next_to(think2, DOWN, buff=GAP_MD * 1.3)
        tag1 = serif("that is inference — the hidden meaning behind the clues",
                     LABEL_SIZE, GREY)
        tag1.next_to(model1, DOWN, buff=GAP_MD)

        with self.beat("model1") as t:
            self.play(Write(model1), run_time=t.fill(0.4))
            self.play(Write(tag1), run_time=t.fill(0.2))
            t.hold()

        # ------------------------------------------------------- passage 2
        head2 = serif("Example 2 — harder", TITLE_SIZE)
        head2.to_edge(UP, buff=GAP_MD * 1.6)
        pass2 = PassageHighlight(PASSAGE_2, width=WRAP)
        pass2.next_to(head2, DOWN, buff=GAP_MD * 1.3)
        q2 = serif("What can we infer?", BODY_SIZE)
        q2.next_to(pass2, DOWN, buff=GAP_MD * 1.2)

        with self.beat("passage2") as t:
            old = [m for m in self.mobjects if m is not margin]
            self.play(*[FadeOut(m) for m in old], run_time=t.fill(0.1))
            self.play(Write(head2), run_time=t.fill(0.12))
            self.play(Write(pass2), run_time=t.fill(0.4))
            self.play(Write(q2), run_time=t.fill(0.15))
            t.hold()

        # --------------------------------------------------------- careful
        never = VGroup(
            serif("careful — the passage never says", BODY_SIZE, TERRACOTTA),
            serif('"Sara was disappointed"', BODY_SIZE, TERRACOTTA),
        ).arrange(DOWN, buff=GAP_SM)
        never.next_to(q2, DOWN, buff=GAP_MD * 1.1)

        with self.beat("careful") as t:
            self.play(Write(never), run_time=t.fill(0.4))
            t.hold()

        # ---------------------------------------------------------- clues 2
        pass2a = PassageHighlight(PASSAGE_2, highlight="folded it again",
                                  width=WRAP)
        pass2a.move_to(pass2)
        pass2b = PassageHighlight(PASSAGE_2,
                                  highlight="slipped it into her bag",
                                  width=WRAP)
        pass2b.move_to(pass2)
        hints = serif("she hides the result · she doesn't show her friends",
                      LABEL_SIZE, GREY)
        hints.next_to(never, DOWN, buff=GAP_MD)

        with self.beat("clues2") as t:
            self.play(FadeOut(pass2), FadeIn(pass2a), run_time=t.fill(0.15))
            self.play(FadeOut(pass2a), FadeIn(pass2b), run_time=t.fill(0.2))
            self.play(Write(hints), run_time=t.fill(0.25))
            t.hold()

        # ---------------------------------------------------------- model 2
        model2 = PassageHighlight(
            "Sara is probably disappointed or embarrassed by her result "
            "and does not want her friends to see it.",
            width=WRAP, color=SAGE,
        )
        model2.next_to(hints, DOWN, buff=GAP_MD * 1.1)

        with self.beat("model2") as t:
            self.play(Write(model2), run_time=t.fill(0.45))
            t.hold()

        # --------------------------------------------------------- evidence
        used = serif("we didn't invent a story — we used evidence",
                     BODY_SIZE)
        used.next_to(model2, DOWN, buff=GAP_MD * 1.1)

        with self.beat("evidence") as t:
            self.play(Write(used), run_time=t.fill(0.3))
            self.play(Create(self.underline(used)), run_time=t.fill(0.15))
            t.hold()

        # --------------------------------------------------------- triggers
        trig_head = serif("Whenever the exam asks:", TITLE_SIZE)
        trig_head.to_edge(UP, buff=GAP_MD * 1.6)
        trigs = VGroup(
            serif('"What does this suggest?"', BODY_SIZE),
            serif('"What impression do you get?"', BODY_SIZE),
            serif('"What can you infer?"', BODY_SIZE),
        ).arrange(DOWN, buff=GAP_SM * 1.5, aligned_edge=LEFT)
        trigs.next_to(trig_head, DOWN, buff=GAP_MD * 1.2)
        answer = serif("CLUE  →  THINK  →  INFER", TITLE_SIZE)
        answer.next_to(trigs, DOWN, buff=GAP_MD * 1.4)

        with self.beat("triggers") as t:
            old = [m for m in self.mobjects if m is not margin]
            self.play(*[FadeOut(m) for m in old], run_time=t.fill(0.1))
            self.play(Write(trig_head), run_time=t.fill(0.12))
            for line in trigs:
                self.play(Write(line), run_time=t.fill(0.12))
            self.play(Write(answer), run_time=t.fill(0.25))
            t.hold()

        # ------------------------------------------------------------- rule
        dont = serif("Don't tell the examiner what happened.", BODY_SIZE)
        tell = serif("Tell the examiner what it means.", BODY_SIZE,
                     TERRACOTTA)
        pair = VGroup(dont, tell).arrange(DOWN, buff=GAP_SM * 1.6)
        pair.next_to(answer, DOWN, buff=GAP_MD * 1.4)

        with self.beat("rule") as t:
            self.play(Write(dont), run_time=t.fill(0.3))
            self.play(Write(tell), run_time=t.fill(0.3))
            t.hold()

        # -------------------------------------------------------------- end
        with self.beat("end") as t:
            self.play(Create(self.underline(tell)), run_time=t.fill(0.25))
            t.hold()
