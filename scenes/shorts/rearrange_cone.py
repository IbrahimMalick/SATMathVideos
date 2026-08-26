"""YouTube Short: rearrange the cone volume formula (music-driven, vertical).

Make r the subject of V = (1/3) pi r^2 h. Every algebraic move is shown
explicitly: the times-3 written out and cancelling, the divide-by-pi-h
written out and cancelling, the side swap, then the square root. A dance
outro clip is appended after this scene in post, so the timing file runs
112 s, not 120.

Timing: timings/shorts.rearrange_cone.json (hand-authored to the music).
Render vertical: python -m manim render -r 1080,1920 --fps 60 \\
    scenes/shorts/rearrange_cone.py RearrangeConeShort
Frame is 4.5 wide by 8 tall. Portrait pixels-per-unit is 1.8x the lecture
frame, so these font sizes read larger on screen than the numbers suggest.
"""

from manim import (
    FadeIn,
    FadeOut,
    MathTex,
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
    GREY,
    SAGE,
    TERRACOTTA,
    mono,
    serif,
)
from scenes.base import SATScene

HEADLINE = 36    # hook headline lines
Q = 34           # question / zinger lines
CAPTION = 32     # step captions and explanations
EQ_BIG = 64      # the boxed answer
EQ = 56          # working equations (wide intermediates need the room)
OP = 52          # the operation badge (x3, / pi h, sqrt)
SIDE_NOTE = 44   # arithmetic asides
STEP = 28        # mono step headers

MAX_W = 4.0      # widest anything may run in a 4.5-unit frame

WORK = DOWN * 1.0    # where the working equation lives
NOTES = DOWN * 2.8   # operation badges and asides


def fit(mobject, max_width=MAX_W):
    """Guard rail: nothing may run off the 4.5-unit-wide frame."""
    if mobject.width > max_width:
        mobject.scale_to_fit_width(max_width)
    return mobject


def stanza(*lines):
    return VGroup(*lines).arrange(DOWN, buff=0.14)


class RearrangeConeShort(SATScene):
    scene_id = "shorts.rearrange_cone"

    def step_header(self, text):
        header = mono(text, STEP, GREY)
        header.move_to(UP * 3.55)
        return fit(header)

    def op_badge(self, tex):
        """The operation being applied — the one thing to look at."""
        badge = MathTex(tex, font_size=OP, color=TERRACOTTA)
        label = serif("on both sides", CAPTION, GREY)
        group = VGroup(badge, label).arrange(DOWN, buff=0.2)
        group.move_to(NOTES)
        return group

    def construct(self):
        # ------------------------------------------------------- question
        headline = stanza(
            serif("Only A* O Level", HEADLINE),
            serif("students will", HEADLINE),
            serif("get this right.", HEADLINE),
        )
        for line in headline:
            fit(line)
        headline.arrange(DOWN, buff=0.14)
        headline.move_to(UP * 2.7)

        cone = MathTex("V = \\frac{1}{3}\\pi r^2 h", font_size=EQ,
                       color=CHARCOAL)
        fit(cone)
        cone.move_to(UP * 0.3)
        ask = stanza(
            serif("make r the", 38, TERRACOTTA),
            serif("subject.", 38, TERRACOTTA),
        )
        ask.move_to(DOWN * 1.6)

        with self.beat("question") as t:
            self.play(Write(headline), run_time=t.fill(0.25))
            self.play(Write(cone), run_time=t.fill(0.2))
            self.play(Write(ask), run_time=t.fill(0.15))
            t.hold()

        # ----------------------------------------------------------- goal
        g_head = self.step_header("THE GOAL")
        goal = MathTex("r = \\;?", font_size=EQ, color=CHARCOAL)
        goal.move_to(WORK)
        g_cap = stanza(
            serif("peel everything", CAPTION, GREY),
            serif("away from r", CAPTION, GREY),
        )
        g_cap.move_to(NOTES)

        with self.beat("goal") as t:
            self.play(FadeOut(headline), FadeOut(ask),
                      cone.animate.scale(0.85).move_to(UP * 2.6),
                      run_time=t.fill(0.15))
            self.play(Write(g_head), run_time=t.fill(0.1))
            self.play(Write(goal), run_time=t.fill(0.2))
            self.play(FadeIn(g_cap), run_time=t.fill(0.15))
            t.hold()

        # -------------------------------------------------------- times 3
        t3_head = self.step_header("STEP 1: TIMES 3")
        w0 = MathTex("V", "=", "\\frac{1}{3}\\pi r^2 h",
                     font_size=EQ, color=CHARCOAL)
        w1 = MathTex("3V", "=", "3\\cdot\\frac{1}{3}", "\\pi r^2 h",
                     font_size=EQ, color=CHARCOAL)
        for m in (w0, w1):
            fit(m)
            m.move_to(WORK)
        t3_op = self.op_badge("\\times\\,3")

        with self.beat("times3") as t:
            self.play(FadeOut(g_head), FadeOut(g_cap), FadeOut(goal),
                      run_time=t.fill(0.08))
            self.play(Write(t3_head), run_time=t.fill(0.08))
            self.play(Write(w0), run_time=t.fill(0.18))
            self.play(FadeIn(t3_op), run_time=t.fill(0.12))
            self.play(TransformMatchingTex(w0, w1), run_time=t.fill(0.25))
            t.hold()

        # ------------------------------------------------------- cancel 3
        c3_head = self.step_header("THE 3s CANCEL")
        c3_note = MathTex("3\\cdot\\tfrac{1}{3} = 1", font_size=SIDE_NOTE,
                          color=GREY)
        c3_note.move_to(NOTES)
        w2 = MathTex("3V", "=", "\\pi r^2 h", font_size=EQ, color=CHARCOAL)
        w2.move_to(WORK)

        with self.beat("cancel3") as t:
            self.play(FadeOut(t3_head), FadeOut(t3_op), FadeIn(c3_note),
                      run_time=t.fill(0.1))
            self.play(Write(c3_head), run_time=t.fill(0.08))
            self.play(TransformMatchingTex(w1, w2), run_time=t.fill(0.3))
            t.hold()

        # ---------------------------------------------------- divide pi h
        dv_head = self.step_header("STEP 2: DIVIDE")
        w3 = MathTex("\\frac{3V}{\\pi h}", "=",
                     "\\frac{\\pi r^2 h}{\\pi h}",
                     font_size=EQ, color=CHARCOAL)
        fit(w3)
        w3.move_to(WORK)
        dv_op = self.op_badge("\\div\\,\\pi h")

        with self.beat("divide") as t:
            self.play(FadeOut(c3_head), FadeOut(c3_note), FadeIn(dv_op),
                      run_time=t.fill(0.1))
            self.play(Write(dv_head), run_time=t.fill(0.08))
            self.play(TransformMatchingTex(w2, w3), run_time=t.fill(0.3))
            t.hold()

        # ---------------------------------------------------- cancel pi h
        cp_head = self.step_header("PI AND h CANCEL")
        cp_note = MathTex("\\tfrac{\\pi h}{\\pi h} = 1",
                          font_size=SIDE_NOTE, color=GREY)
        cp_note.move_to(NOTES)
        w4 = MathTex("\\frac{3V}{\\pi h}", "=", "r^2", font_size=EQ,
                     color=CHARCOAL)
        w4.move_to(WORK)
        w5 = MathTex("r^2", "=", "\\frac{3V}{\\pi h}", font_size=EQ,
                     color=CHARCOAL)
        w5.move_to(WORK)
        swap_cap = serif("swap sides", CAPTION, GREY)
        swap_cap.move_to(NOTES)

        with self.beat("cancelpi") as t:
            self.play(FadeOut(dv_head), FadeOut(dv_op), FadeIn(cp_note),
                      run_time=t.fill(0.1))
            self.play(Write(cp_head), run_time=t.fill(0.08))
            self.play(TransformMatchingTex(w3, w4), run_time=t.fill(0.22))
            self.play(FadeOut(cp_note), FadeIn(swap_cap),
                      run_time=t.fill(0.1))
            self.play(TransformMatchingTex(w4, w5), run_time=t.fill(0.2))
            t.hold()

        # ----------------------------------------------------------- root
        rt_head = self.step_header("STEP 3: ROOT IT")
        rt_op = self.op_badge("\\sqrt{\\;\\;\\;}")
        w6 = MathTex("r", "=", "\\sqrt{\\frac{3V}{\\pi h}}", font_size=EQ,
                     color=CHARCOAL)
        w6.move_to(WORK)
        trap = stanza(
            serif("most students", CAPTION, TERRACOTTA),
            serif("forget this √!", CAPTION, TERRACOTTA),
        )
        trap.move_to(NOTES)

        with self.beat("root") as t:
            self.play(FadeOut(cp_head), FadeOut(swap_cap), FadeIn(rt_op),
                      run_time=t.fill(0.1))
            self.play(Write(rt_head), run_time=t.fill(0.08))
            self.play(TransformMatchingTex(w5, w6), run_time=t.fill(0.25))
            self.play(FadeOut(rt_op), FadeIn(trap), run_time=t.fill(0.12))
            t.hold()

        # --------------------------------------------------------- answer
        boxed = MathTex("\\boxed{r = \\sqrt{\\tfrac{3V}{\\pi h}}}",
                        font_size=EQ_BIG, color=SAGE)
        fit(boxed)
        boxed.move_to(UP * 1.4)
        zinger = stanza(
            serif("the √ is where", Q),
            serif("marks are lost.", Q),
        )
        for line in zinger:
            fit(line)
        zinger.arrange(DOWN, buff=0.14)
        zinger.move_to(DOWN * 1.2)

        with self.beat("answer") as t:
            self.play(FadeOut(cone), FadeOut(rt_head), FadeOut(trap),
                      run_time=t.fill(0.1))
            self.play(TransformMatchingTex(w6, boxed),
                      run_time=t.fill(0.25))
            self.play(Write(zinger), run_time=t.fill(0.25))
            t.hold()

        # ------------------------------------------------------------ cta
        cta_lines = stanza(
            serif("Want the full", Q),
            serif("O Level course?", Q),
        )
        cta_lines.move_to(UP * 1.6)
        register = serif("Register at:", CAPTION, GREY)
        fit(register)
        register.move_to(UP * 0.2)
        url = VGroup(
            mono("academy.thedigitaltutor.net", 24, TERRACOTTA),
            mono("/o-level", 24, TERRACOTTA),
        ).arrange(DOWN, buff=0.18)
        for line in url:
            fit(line, 4.15)
        url.move_to(DOWN * 0.8)

        with self.beat("cta") as t:
            self.play(FadeOut(boxed), FadeOut(zinger),
                      run_time=t.fill(0.08))
            self.play(Write(cta_lines), run_time=t.fill(0.2))
            self.play(Write(register), run_time=t.fill(0.12))
            self.play(Write(url), run_time=t.fill(0.2))
            t.hold()
