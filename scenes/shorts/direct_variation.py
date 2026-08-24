"""YouTube Short: direct variation with the square (music-driven, vertical).

Timing: timings/shorts.direct_variation.json (hand-authored to the music).
Render vertical: python -m manim render -r 1080,1920 --fps 60 \\
    scenes/shorts/direct_variation.py DirectVariationShort
Frame is 4.5 wide by 8 tall.
"""

import numpy as np

from manim import (
    Create,
    FadeOut,
    MathTex,
    Square,
    TransformMatchingTex,
    VGroup,
    Write,
    DOWN,
    UP,
)

from brand import (
    BODY_SIZE,
    CHARCOAL,
    DISPLAY_SIZE,
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
from scenes.base import SATScene


class DirectVariationShort(SATScene):
    scene_id = "shorts.direct_variation"

    def construct(self):
        # ---------------------------------------------------------- hook
        line1 = serif("This panel", TITLE_SIZE)
        line2 = serif("costs $18.", TITLE_SIZE)
        hook = VGroup(line1, line2).arrange(DOWN, buff=GAP_SM)
        hook.move_to(UP * 3.0)
        tease = serif("The big one?", TITLE_SIZE, TERRACOTTA)
        tease.next_to(hook, DOWN, buff=GAP_MD)

        small = Square(side_length=1.2, color=SLATE, stroke_width=5)
        small.move_to(np.array([-1.1, 0.9, 0]))
        small_side = serif("30 cm", MARGIN_SIZE, GREY)
        small_side.next_to(small, DOWN, buff=GAP_SM)
        small_cost = serif("$18", LABEL_SIZE, SAGE)
        small_cost.move_to(small)

        with self.beat("hook") as t:
            self.play(Write(hook), run_time=t.fill(0.3))
            self.play(Create(small), run_time=t.fill(0.2))
            self.play(Write(small_side), Write(small_cost), run_time=t.fill(0.15))
            self.play(Write(tease), run_time=t.fill(0.2))
            t.hold()

        # -------------------------------------------------------- squares
        big = Square(side_length=2.0, color=SLATE, stroke_width=5)
        big.move_to(np.array([0.7, -1.6, 0]))
        big_side = serif("50 cm", MARGIN_SIZE, GREY)
        big_side.next_to(big, DOWN, buff=GAP_SM)
        big_cost = serif("?", TITLE_SIZE * 1.3, TERRACOTTA)
        big_cost.move_to(big)

        with self.beat("squares") as t:
            self.play(Create(big), run_time=t.fill(0.3))
            self.play(Write(big_side), run_time=t.fill(0.1))
            self.play(Write(big_cost), run_time=t.fill(0.2))
            t.hold()

        # ----------------------------------------------------------- rule
        rule = serif("cost grows with the SQUARE", LABEL_SIZE)
        rule.move_to(UP * 0.0)

        with self.beat("rule") as t:
            self.play(FadeOut(hook), FadeOut(tease), FadeOut(small),
                      FadeOut(small_side), FadeOut(small_cost), FadeOut(big),
                      FadeOut(big_side), FadeOut(big_cost),
                      run_time=t.fill(0.12))
            eq0 = MathTex("C = k\\,s^2", font_size=DISPLAY_SIZE * 1.2,
                          color=CHARCOAL)
            eq0.move_to(UP * 1.6)
            self.play(Write(eq0), run_time=t.fill(0.3))
            self.play(Write(rule), run_time=t.fill(0.2))
            self.eq0 = eq0
            t.hold()

        # --------------------------------------------------------- find k
        k1 = MathTex("18", "=", "k(30)^2", font_size=DISPLAY_SIZE,
                     color=CHARCOAL)
        k2 = MathTex("18", "=", "900k", font_size=DISPLAY_SIZE, color=CHARCOAL)
        k3 = MathTex("k", "=", "\\frac{1}{50}", font_size=DISPLAY_SIZE,
                     color=CHARCOAL)
        for m in (k1, k2, k3):
            m.move_to(DOWN * 0.9)

        with self.beat("find_k") as t:
            self.play(FadeOut(rule), run_time=t.fill(0.08))
            self.play(Write(k1), run_time=t.fill(0.22))
            self.play(TransformMatchingTex(k1, k2), run_time=t.fill(0.22))
            self.play(TransformMatchingTex(k2, k3), run_time=t.fill(0.25))
            t.hold()

        # -------------------------------------------------------- formula
        formula = MathTex("C = \\frac{s^2}{50}", font_size=DISPLAY_SIZE * 1.2,
                          color=CHARCOAL)
        formula.move_to(UP * 1.6)

        with self.beat("formula") as t:
            self.play(FadeOut(k3), run_time=t.fill(0.08))
            self.play(TransformMatchingTex(self.eq0, formula),
                      run_time=t.fill(0.35))
            t.hold()

        # ---------------------------------------------------------- solve
        s1 = MathTex("C", "=", "\\frac{(50)^2}{50}", font_size=DISPLAY_SIZE,
                     color=CHARCOAL)
        s2 = MathTex("C", "=", "\\frac{2500}{50}", font_size=DISPLAY_SIZE,
                     color=CHARCOAL)
        s3 = MathTex("C", "=", "50", font_size=DISPLAY_SIZE, color=CHARCOAL)
        for m in (s1, s2, s3):
            m.move_to(DOWN * 0.9)

        with self.beat("solve") as t:
            self.play(Write(s1), run_time=t.fill(0.22))
            self.play(TransformMatchingTex(s1, s2), run_time=t.fill(0.22))
            self.play(TransformMatchingTex(s2, s3), run_time=t.fill(0.25))
            t.hold()

        # --------------------------------------------------------- answer
        boxed = MathTex("\\boxed{\\$50}", font_size=DISPLAY_SIZE * 1.6,
                        color=SAGE)
        boxed.move_to(DOWN * 0.9)
        zinger = serif("not 30:50 — it's squared", LABEL_SIZE)
        zinger.next_to(boxed, DOWN, buff=GAP_MD * 1.4)

        with self.beat("answer") as t:
            self.play(TransformMatchingTex(s3, boxed), run_time=t.fill(0.3))
            self.play(Write(zinger), run_time=t.fill(0.25))
            t.hold()

        # ------------------------------------------------------------ cta
        cta = mono("daily exam math — follow", MARGIN_SIZE)
        cta.move_to(DOWN * 3.3)

        with self.beat("cta") as t:
            self.play(Write(cta), run_time=t.fill(0.35))
            t.hold()
