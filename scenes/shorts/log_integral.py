"""YouTube Short: evaluate the integral of x ln(1+x) from 0 to 1, exactly.

Music-driven, so the timing file is hand-authored rather than synced to a
delivery — there is no narration to derive it from. The countdown beat
runs a real ten seconds because the hook promises ten.

The whole point is that a messy-looking integral collapses to 1/4, so the
working is shown step by step and the answer gets the frame to itself.

Verified numerically before building: the integral is exactly 1/4, the
inner integral is ln 2 - 1/2, and x^2/(1+x) = x - 1 + 1/(1+x).

Timing: timings/shorts.log_integral.json
Render: python -m manim render -r 1080,1920 --fps 60 \\
    scenes/shorts/log_integral.py LogIntegral
"""

from manim import (
    FadeIn,
    FadeOut,
    MathTex,
    SurroundingRectangle,
    Transform,
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
    GAP_LG,
    GAP_MD,
    GAP_SM,
    GREY,
    MARGIN_SIZE,
    SAGE,
    SLATE,
    TERRACOTTA,
    mono,
    serif,
)
from scenes.base import SATScene

HOOK = 40        # the question
HERO = 48        # the integral itself — widest thing on screen
STEP = 40        # a line of working
LABEL = 34       # captions and substitutions
COUNT = 96       # the countdown digit
ANSWER = 80      # the boxed result

MAX_W = 3.9


def fit(mobject, width=MAX_W):
    if mobject.width > width:
        mobject.scale_to_fit_width(width)
    return mobject


class LogIntegral(SATScene):
    scene_id = "shorts.log_integral"

    def construct(self):
        self.strap = mono("exact value · no calculator", MARGIN_SIZE)
        fit(self.strap)
        self.strap.to_edge(UP, buff=GAP_MD)
        self.add(self.strap)
        self.keep = [self.strap]

        self.the_challenge()
        self.by_parts()
        self.the_trick()
        self.the_answer()

    # -------------------------------------------------------------- helpers

    def wipe(self, t, fraction=0.08):
        old = [m for m in self.mobjects if m not in self.keep]
        if old:
            self.play(*[FadeOut(m) for m in old], run_time=t.fill(fraction))

    # ------------------------------------------------------------- sections

    def the_challenge(self):
        with self.beat("hook") as t:
            ask = serif("Can you evaluate", HOOK, CHARCOAL)
            ask2 = serif("this exactly?", HOOK, CHARCOAL)
            head = VGroup(ask, ask2).arrange(DOWN, buff=GAP_SM)
            fit(head)
            head.move_to(UP * 2.4)
            self.integral = MathTex(r"\int_0^1 x\ln(1+x)\,dx",
                                    font_size=HERO, color=CHARCOAL)
            fit(self.integral)
            self.integral.next_to(head, DOWN, buff=GAP_LG * 1.2)
            self.play(Write(head), run_time=t.fill(0.3))
            self.play(Write(self.integral), run_time=t.fill(0.3))
            self.keep.append(self.integral)
            t.hold()

        with self.beat("challenge") as t:
            warn = serif("NO CALCULATOR", HOOK, TERRACOTTA)
            fit(warn)
            warn.next_to(self.integral, DOWN, buff=GAP_LG * 1.1)
            self.play(Write(warn), run_time=t.fill(0.5))
            self.warn = warn
            t.hold()

        with self.beat("timer") as t:
            # Ten seconds, counted honestly — the hook promised ten.
            digit = serif("10", COUNT, SLATE)
            digit.next_to(self.warn, DOWN, buff=GAP_MD * 1.4)
            self.play(FadeIn(digit), run_time=t.fill(0.05))
            for n in range(9, 0, -1):
                nxt = serif(str(n), COUNT,
                            TERRACOTTA if n <= 3 else SLATE)
                nxt.move_to(digit)
                self.play(Transform(digit, nxt), run_time=t.fill(0.094))
            t.hold()

    def by_parts(self):
        with self.beat("method") as t:
            self.keep.remove(self.integral)
            self.wipe(t, 0.14)
            head = serif("integration by parts", HOOK, CHARCOAL)
            fit(head)
            head.move_to(UP * 2.2)
            self.play(Write(head), run_time=t.fill(0.5))
            self.head = head
            t.hold()

        with self.beat("parts") as t:
            u = MathTex(r"u=\ln(1+x)", font_size=STEP, color=TERRACOTTA)
            dv = MathTex(r"dv = x\,dx", font_size=STEP, color=SLATE)
            pair = VGroup(u, dv).arrange(DOWN, buff=GAP_MD * 1.3)
            fit(pair)
            pair.next_to(self.head, DOWN, buff=GAP_LG)
            self.play(Write(u), run_time=t.fill(0.3))
            self.play(Write(dv), run_time=t.fill(0.3))
            self.pair = pair
            t.hold()

        with self.beat("applied") as t:
            self.wipe(t, 0.08)
            line1 = MathTex(r"\left[\tfrac{x^2}{2}\ln(1+x)\right]_0^1",
                            font_size=STEP, color=CHARCOAL)
            line2 = MathTex(r"-\;\tfrac12\int_0^1 \tfrac{x^2}{1+x}\,dx",
                            font_size=STEP, color=CHARCOAL)
            block = VGroup(fit(line1), fit(line2)).arrange(DOWN,
                                                           buff=GAP_MD * 1.2)
            block.move_to(UP * 1.4)
            self.play(Write(line1), run_time=t.fill(0.28))
            self.play(Write(line2), run_time=t.fill(0.28))
            self.applied = block
            t.hold()

        with self.beat("first_term") as t:
            got = MathTex(r"\left[\tfrac{x^2}{2}\ln(1+x)\right]_0^1"
                          r"=\tfrac{\ln 2}{2}",
                          font_size=STEP, color=SAGE)
            fit(got)
            got.next_to(self.applied, DOWN, buff=GAP_LG)
            self.play(Write(got), run_time=t.fill(0.5))
            t.hold()

    def the_trick(self):
        with self.beat("rewrite") as t:
            self.wipe(t, 0.1)
            head = serif("the trick", LABEL, GREY)
            fit(head)
            head.move_to(UP * 2.4)
            before = MathTex(r"\tfrac{x^2}{1+x}", font_size=HERO,
                             color=CHARCOAL)
            before.next_to(head, DOWN, buff=GAP_LG)
            self.play(Write(head), run_time=t.fill(0.12))
            self.play(Write(before), run_time=t.fill(0.2))
            after = MathTex(r"\tfrac{x^2}{1+x}", r"=", r"x-1+\tfrac{1}{1+x}",
                            font_size=STEP, color=TERRACOTTA)
            fit(after)
            after.move_to(before)
            # the signature morph: one form becoming the next
            self.play(TransformMatchingTex(before, after),
                      run_time=t.fill(0.34))
            self.rewrite = after
            t.hold()

        with self.beat("inner") as t:
            inner = MathTex(r"\int_0^1\tfrac{x^2}{1+x}\,dx"
                            r"=\ln 2-\tfrac12",
                            font_size=STEP, color=SLATE)
            fit(inner)
            inner.next_to(self.rewrite, DOWN, buff=GAP_LG * 1.1)
            self.play(Write(inner), run_time=t.fill(0.5))
            t.hold()

        with self.beat("combine") as t:
            self.wipe(t, 0.1)
            combine = MathTex(r"\tfrac{\ln 2}{2}",
                              r"-\tfrac12\left(\ln 2-\tfrac12\right)",
                              font_size=STEP, color=CHARCOAL)
            fit(combine)
            combine.move_to(UP * 1.2)
            note = serif("the logs cancel", LABEL, GREY)
            fit(note)
            note.next_to(combine, DOWN, buff=GAP_LG)
            self.play(Write(combine), run_time=t.fill(0.34))
            self.play(Write(note), run_time=t.fill(0.2))
            self.combine = combine
            t.hold()

    def the_answer(self):
        with self.beat("answer") as t:
            self.wipe(t, 0.08)
            result = MathTex(r"=\tfrac14", font_size=ANSWER,
                             color=TERRACOTTA)
            fit(result, 2.6)
            result.move_to(UP * 0.9)
            box = SurroundingRectangle(result, color=TERRACOTTA,
                                       buff=GAP_SM * 1.2, stroke_width=4)
            nice = serif("surprisingly simple", LABEL, GREY)
            fit(nice)
            nice.next_to(box, DOWN, buff=GAP_LG)
            self.play(Write(result), run_time=t.fill(0.3))
            self.play(FadeIn(box), run_time=t.fill(0.12))
            self.play(Write(nice), run_time=t.fill(0.2))
            t.hold()

        with self.beat("outro") as t:
            self.wipe(t, 0.12)
            balay = serif("BHALAY BHALAY!", HOOK, TERRACOTTA)
            fit(balay)
            balay.move_to(UP * 0.6)
            logo = serif("The Digital Tutor", LABEL, GREY)
            logo.next_to(balay, DOWN, buff=GAP_LG)
            self.play(Write(balay), run_time=t.fill(0.3))
            self.play(FadeIn(logo), run_time=t.fill(0.2))
            t.hold()
