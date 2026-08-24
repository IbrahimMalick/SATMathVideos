"""YouTube Short: direct variation with the square (music-driven, vertical).

Timing: timings/shorts.direct_variation.json (hand-authored to the music).
Render vertical: python -m manim render -r 1080,1920 --fps 60 \\
    scenes/shorts/direct_variation.py DirectVariationShort
Frame is 4.5 wide by 8 tall; type runs much larger than lecture scale.
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
    config,
)

# Portrait: manim keeps frame_width fixed by default, which would make the
# frame 25 units tall. Pin the intended 4.5 x 8 frame instead.
config.frame_height = 8.0
config.frame_width = 4.5

from brand import (
    CHARCOAL,
    GAP_MD,
    GAP_SM,
    GREY,
    SAGE,
    SLATE,
    TERRACOTTA,
    mono,
    serif,
)
from scenes.base import SATScene

HERO = 48        # hook lines (frame is 4.5 wide; 64 overflows it)
EQ_BIG = 96      # the formula the short is about
EQ = 72          # working equations
NOTE = 40        # captions
SMALL = 36       # cm labels, cta


class DirectVariationShort(SATScene):
    scene_id = "shorts.direct_variation"

    def construct(self):
        # ---------------------------------------------------------- hook
        hook = VGroup(
            serif("This panel", HERO),
            serif("costs $18.", HERO),
        ).arrange(DOWN, buff=GAP_SM)
        hook.move_to(UP * 3.15)
        tease = serif("The big one?", HERO, TERRACOTTA)
        if tease.width > 4.1:
            tease.scale_to_fit_width(4.1)
        tease.next_to(hook, DOWN, buff=0.35)

        small = Square(side_length=1.35, color=SLATE, stroke_width=6)
        small.move_to(np.array([-1.05, 0.5, 0]))
        small_side = serif("30 cm", SMALL, GREY)
        small_side.next_to(small, DOWN, buff=0.2)
        small_cost = serif("$18", NOTE, SAGE)
        small_cost.move_to(small)

        with self.beat("hook") as t:
            self.play(Write(hook), run_time=t.fill(0.3))
            self.play(Create(small), run_time=t.fill(0.2))
            self.play(Write(small_side), Write(small_cost), run_time=t.fill(0.15))
            self.play(Write(tease), run_time=t.fill(0.2))
            t.hold()

        # -------------------------------------------------------- squares
        # Same 30:50 proportion as the small square; sized so its "50 cm"
        # label still clears the bottom frame edge.
        big = Square(side_length=2.25, color=SLATE, stroke_width=6)
        big.move_to(np.array([0.7, -2.05, 0]))
        big_side = serif("50 cm", SMALL, GREY)
        big_side.next_to(big, DOWN, buff=0.2)
        big_cost = serif("?", HERO * 1.3, TERRACOTTA)
        big_cost.move_to(big)

        with self.beat("squares") as t:
            self.play(tease.animate.set_color(CHARCOAL), run_time=t.fill(0.08))
            self.play(Create(big), run_time=t.fill(0.3))
            self.play(Write(big_side), run_time=t.fill(0.1))
            self.play(Write(big_cost), run_time=t.fill(0.2))
            t.hold()

        # ----------------------------------------------------------- rule
        eq0 = MathTex("C = k\\,s^2", font_size=EQ_BIG, color=CHARCOAL)
        eq0.move_to(UP * 2.0)
        rule = serif("cost grows with", NOTE)
        rule2 = serif("the SQUARE", NOTE, TERRACOTTA)
        rule_group = VGroup(rule, rule2).arrange(DOWN, buff=GAP_SM)
        if rule_group.width > 4.0:
            rule_group.scale_to_fit_width(4.0)
        rule_group.move_to(UP * 0.3)

        with self.beat("rule") as t:
            self.play(FadeOut(hook), FadeOut(tease), FadeOut(small),
                      FadeOut(small_side), FadeOut(small_cost), FadeOut(big),
                      FadeOut(big_side), FadeOut(big_cost),
                      run_time=t.fill(0.12))
            self.play(Write(eq0), run_time=t.fill(0.3))
            self.play(Write(rule_group), run_time=t.fill(0.2))
            self.eq0 = eq0
            t.hold()

        # --------------------------------------------------------- find k
        k1 = MathTex("18", "=", "k(30)^2", font_size=EQ, color=CHARCOAL)
        k2 = MathTex("18", "=", "900k", font_size=EQ, color=CHARCOAL)
        k3 = MathTex("k", "=", "\\frac{1}{50}", font_size=EQ, color=CHARCOAL)
        for m in (k1, k2, k3):
            m.move_to(DOWN * 1.6)

        with self.beat("find_k") as t:
            self.play(FadeOut(rule_group), run_time=t.fill(0.08))
            self.play(Write(k1), run_time=t.fill(0.22))
            self.play(TransformMatchingTex(k1, k2), run_time=t.fill(0.22))
            self.play(TransformMatchingTex(k2, k3), run_time=t.fill(0.25))
            t.hold()

        # -------------------------------------------------------- formula
        formula = MathTex("C = \\frac{s^2}{50}", font_size=EQ_BIG,
                          color=CHARCOAL)
        formula.move_to(UP * 2.0)

        with self.beat("formula") as t:
            self.play(FadeOut(k3), run_time=t.fill(0.08))
            self.play(TransformMatchingTex(self.eq0, formula),
                      run_time=t.fill(0.35))
            t.hold()

        # ---------------------------------------------------------- solve
        s1 = MathTex("C", "=", "\\frac{(50)^2}{50}", font_size=EQ,
                     color=CHARCOAL)
        s2 = MathTex("C", "=", "\\frac{2500}{50}", font_size=EQ, color=CHARCOAL)
        s3 = MathTex("C", "=", "50", font_size=EQ, color=CHARCOAL)
        for m in (s1, s2, s3):
            m.move_to(DOWN * 1.4)

        with self.beat("solve") as t:
            self.play(Write(s1), run_time=t.fill(0.22))
            self.play(TransformMatchingTex(s1, s2), run_time=t.fill(0.22))
            self.play(TransformMatchingTex(s2, s3), run_time=t.fill(0.25))
            t.hold()

        # --------------------------------------------------------- answer
        boxed = MathTex("\\boxed{\\$50}", font_size=EQ_BIG * 1.2, color=SAGE)
        boxed.move_to(DOWN * 1.3)
        zinger = VGroup(
            serif("not 30:50 —", NOTE),
            serif("it's squared", NOTE, TERRACOTTA),
        ).arrange(DOWN, buff=GAP_SM)
        zinger.next_to(boxed, DOWN, buff=GAP_MD * 1.3)

        with self.beat("answer") as t:
            self.play(TransformMatchingTex(s3, boxed), run_time=t.fill(0.3))
            self.play(Write(zinger), run_time=t.fill(0.25))
            t.hold()

        # ------------------------------------------------------------ cta
        cta = mono("daily exam math — follow", SMALL)
        cta.move_to(DOWN * 3.5)

        with self.beat("cta") as t:
            self.play(Write(cta), run_time=t.fill(0.35))
            t.hold()
