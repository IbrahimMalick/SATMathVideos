"""YouTube Short: direct variation with the square (music-driven, vertical).

Timing: timings/shorts.direct_variation.json (hand-authored to the music).
Render vertical: python -m manim render -r 1080,1920 --fps 60 \\
    scenes/shorts/direct_variation.py DirectVariationShort
Frame is 4.5 wide by 8 tall. Portrait pixels-per-unit is 1.8x the lecture
frame, so these font sizes read larger on screen than the numbers suggest.
"""

import numpy as np

from manim import (
    Create,
    FadeIn,
    FadeOut,
    MathTex,
    Square,
    TransformMatchingTex,
    VGroup,
    Write,
    DOWN,
    UP,
    config,
)

# Portrait: manim keeps frame_width fixed by default, which would make the
# frame 25 units tall. Pin the intended 4.5 x 8 frame instead.
config.frame_height = 8.0
config.frame_width = 4.5

from brand import (
    CHARCOAL,
    GAP_SM,
    GREY,
    SAGE,
    SLATE,
    TERRACOTTA,
    mono,
    serif,
)
from scenes.base import SATScene

Q = 34           # question lines
CAPTION = 32     # step captions and explanations
EQ_BIG = 72      # the pinned formula
EQ = 60          # working equations
KNOWN = 48       # "s = 30, C = 18" values
SIDE_NOTE = 44   # arithmetic asides
LABEL = 32       # cm labels, cta
STEP = 28        # mono step headers

MAX_W = 4.0      # widest anything may run in a 4.5-unit frame


def fit(mobject, max_width=MAX_W):
    """Guard rail: nothing may run off the 4.5-unit-wide frame."""
    if mobject.width > max_width:
        mobject.scale_to_fit_width(max_width)
    return mobject


def stanza(*lines):
    return VGroup(*lines).arrange(DOWN, buff=0.14)


class DirectVariationShort(SATScene):
    scene_id = "shorts.direct_variation"

    def step_header(self, text):
        header = mono(text, STEP, GREY)
        header.move_to(UP * 3.55)
        return fit(header)

    def construct(self):
        # ------------------------------------------------------- question
        q_head = self.step_header("QUESTION")
        q1 = stanza(
            serif("A square panel", Q),
            serif("of side 30 cm", Q),
            serif("costs $18.", Q),
        )
        q2 = stanza(
            serif("Cost varies as", Q),
            serif("the SQUARE", Q, TERRACOTTA),
            serif("of the side.", Q),
        )
        q3 = stanza(
            serif("Find the cost of", Q),
            serif("a 50 cm panel.", Q),
        )
        question = VGroup(q1, q2, q3).arrange(DOWN, buff=0.5)
        fit(question)
        question.move_to(DOWN * 0.2)

        with self.beat("question") as t:
            self.play(Write(q_head), run_time=t.fill(0.08))
            self.play(Write(q1), run_time=t.fill(0.22))
            self.play(Write(q2), run_time=t.fill(0.22))
            self.play(Write(q3), run_time=t.fill(0.18))
            t.hold()

        # -------------------------------------------------------- picture
        small = Square(side_length=1.35, color=SLATE, stroke_width=6)
        small.move_to(np.array([-1.05, 1.9, 0]))
        small_side = serif("30 cm", LABEL, GREY)
        small_side.next_to(small, DOWN, buff=0.2)
        small_cost = serif("$18", Q, SAGE)
        small_cost.move_to(small)

        # Same 30:50 proportion as the small square.
        big = Square(side_length=2.25, color=SLATE, stroke_width=6)
        big.move_to(np.array([0.7, -0.9, 0]))
        big_side = serif("50 cm", LABEL, GREY)
        big_side.next_to(big, DOWN, buff=0.2)
        big_cost = serif("?", Q * 1.8, TERRACOTTA)
        big_cost.move_to(big)

        with self.beat("picture") as t:
            self.play(FadeOut(question), FadeOut(q_head),
                      run_time=t.fill(0.1))
            self.play(Create(small), run_time=t.fill(0.18))
            self.play(Write(small_cost), Write(small_side),
                      run_time=t.fill(0.12))
            self.play(Create(big), run_time=t.fill(0.22))
            self.play(Write(big_side), run_time=t.fill(0.1))
            self.play(Write(big_cost), run_time=t.fill(0.12))
            t.hold()

        # ----------------------------------------------------------- rule
        rule_head = self.step_header("STEP 1: THE RULE")
        eq0 = MathTex("C = k\\,s^2", font_size=EQ_BIG, color=CHARCOAL)
        eq0.move_to(UP * 1.8)
        legend = stanza(
            serif("C = the cost", CAPTION),
            serif("s = the side", CAPTION),
            serif("k = a constant", CAPTION),
        )
        for line in legend:
            fit(line)
        legend.arrange(DOWN, buff=0.22)
        legend.move_to(DOWN * 0.4)

        with self.beat("rule") as t:
            self.play(FadeOut(small), FadeOut(small_side),
                      FadeOut(small_cost), FadeOut(big), FadeOut(big_side),
                      FadeOut(big_cost),
                      run_time=t.fill(0.1))
            self.play(Write(rule_head), run_time=t.fill(0.08))
            self.play(Write(eq0), run_time=t.fill(0.25))
            self.play(Write(legend), run_time=t.fill(0.3))
            t.hold()

        # -------------------------------------------------------- plug in
        k_head = self.step_header("STEP 2: FIND k")
        cap_small = serif("the small panel:", CAPTION)
        fit(cap_small)
        cap_small.move_to(UP * 0.7)
        known = MathTex("s = 30,\\quad C = 18", font_size=KNOWN,
                        color=CHARCOAL)
        fit(known)
        known.move_to(UP * 0.0)
        k1 = MathTex("18", "=", "k(30)^2", font_size=EQ, color=CHARCOAL)
        k2 = MathTex("18", "=", "900k", font_size=EQ, color=CHARCOAL)
        k3 = MathTex("k", "=", "\\frac{18}{900}", font_size=EQ,
                     color=CHARCOAL)
        k4 = MathTex("k", "=", "\\frac{1}{50}", font_size=EQ, color=CHARCOAL)
        for m in (k1, k2, k3, k4):
            m.move_to(DOWN * 1.5)

        with self.beat("plug_in") as t:
            self.play(FadeOut(legend), FadeOut(rule_head),
                      run_time=t.fill(0.08))
            self.play(Write(k_head), run_time=t.fill(0.08))
            self.play(Write(cap_small), Write(known), run_time=t.fill(0.22))
            self.play(Write(k1), run_time=t.fill(0.25))
            t.hold()

        # ------------------------------------------------------- simplify
        square_note = MathTex("(30)^2 = 900", font_size=SIDE_NOTE,
                              color=GREY)
        square_note.move_to(DOWN * 2.8)

        with self.beat("simplify") as t:
            self.play(FadeIn(square_note), run_time=t.fill(0.15))
            self.play(TransformMatchingTex(k1, k2), run_time=t.fill(0.3))
            t.hold()

        # -------------------------------------------------------- solve k
        divide_note = stanza(
            serif("divide both", CAPTION, GREY),
            serif("sides by 900", CAPTION, GREY),
        )
        divide_note.move_to(DOWN * 2.9)

        with self.beat("solve_k") as t:
            self.play(FadeOut(square_note), FadeIn(divide_note),
                      run_time=t.fill(0.1))
            self.play(TransformMatchingTex(k2, k3), run_time=t.fill(0.25))
            self.play(TransformMatchingTex(k3, k4), run_time=t.fill(0.25))
            t.hold()

        # -------------------------------------------------------- formula
        f_head = self.step_header("STEP 3: FORMULA")
        formula = MathTex("C = \\frac{s^2}{50}", font_size=EQ_BIG,
                          color=CHARCOAL)
        formula.move_to(UP * 1.8)
        f_cap = serif("for any panel", CAPTION, GREY)
        fit(f_cap)
        f_cap.move_to(DOWN * 0.2)

        with self.beat("formula") as t:
            self.play(FadeOut(k4), FadeOut(divide_note), FadeOut(cap_small),
                      FadeOut(known), FadeOut(k_head),
                      run_time=t.fill(0.1))
            self.play(Write(f_head), run_time=t.fill(0.08))
            self.play(TransformMatchingTex(eq0, formula),
                      run_time=t.fill(0.3))
            self.play(Write(f_cap), run_time=t.fill(0.2))
            t.hold()

        # -------------------------------------------------------- plug 50
        use_head = self.step_header("STEP 4: USE IT")
        cap_big = serif("the big panel:", CAPTION)
        fit(cap_big)
        cap_big.move_to(UP * 0.7)
        known2 = MathTex("s = 50", font_size=KNOWN, color=CHARCOAL)
        known2.move_to(UP * 0.0)
        s1 = MathTex("C", "=", "\\frac{(50)^2}{50}", font_size=EQ,
                     color=CHARCOAL)
        s2 = MathTex("C", "=", "\\frac{2500}{50}", font_size=EQ,
                     color=CHARCOAL)
        s3 = MathTex("C", "=", "50", font_size=EQ, color=CHARCOAL)
        for m in (s1, s2, s3):
            m.move_to(DOWN * 1.6)

        with self.beat("plug50") as t:
            self.play(FadeOut(f_cap), FadeOut(f_head),
                      run_time=t.fill(0.08))
            self.play(Write(use_head), run_time=t.fill(0.08))
            self.play(Write(cap_big), Write(known2), run_time=t.fill(0.2))
            self.play(Write(s1), run_time=t.fill(0.25))
            t.hold()

        # ------------------------------------------------------- square 50
        square_note2 = MathTex("(50)^2 = 2500", font_size=SIDE_NOTE,
                               color=GREY)
        square_note2.move_to(DOWN * 2.9)

        with self.beat("square50") as t:
            self.play(FadeIn(square_note2), run_time=t.fill(0.15))
            self.play(TransformMatchingTex(s1, s2), run_time=t.fill(0.3))
            t.hold()

        # --------------------------------------------------------- result
        with self.beat("result") as t:
            self.play(FadeOut(square_note2), run_time=t.fill(0.1))
            self.play(TransformMatchingTex(s2, s3), run_time=t.fill(0.3))
            t.hold()

        # --------------------------------------------------------- answer
        boxed = MathTex("\\boxed{\\$50}", font_size=EQ_BIG, color=SAGE)
        boxed.move_to(UP * 1.2)
        zinger = stanza(
            serif("not $30 —", Q),
            serif("cost grows with", Q),
            serif("the SQUARE", Q, TERRACOTTA),
        )
        fit(zinger)
        zinger.move_to(DOWN * 1.1)

        with self.beat("answer") as t:
            self.play(FadeOut(formula), FadeOut(cap_big), FadeOut(known2),
                      FadeOut(use_head),
                      run_time=t.fill(0.1))
            self.play(TransformMatchingTex(s3, boxed), run_time=t.fill(0.25))
            self.play(Write(zinger), run_time=t.fill(0.25))
            t.hold()

        # ------------------------------------------------------------ cta
        cta = mono("follow for more", 30)
        fit(cta)
        cta.move_to(DOWN * 3.4)

        with self.beat("cta") as t:
            self.play(Write(cta), run_time=t.fill(0.4))
            t.hold()
