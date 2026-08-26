"""YouTube Short: rearrange the cone volume formula (music-driven, vertical).

Make r the subject of V = (1/3) pi r^2 h. The trap answer forgets the
square root.

Timing: timings/shorts.rearrange_cone.json (hand-authored to the music).
Render vertical: python -m manim render -r 1080,1920 --fps 60 \\
    scenes/shorts/rearrange_cone.py RearrangeConeShort
Frame is 4.5 wide by 8 tall. Portrait pixels-per-unit is 1.8x the lecture
frame, so these font sizes read larger on screen than the numbers suggest.
"""

from manim import (
    FadeIn,
    FadeOut,
    Line,
    MathTex,
    TransformMatchingTex,
    VGroup,
    Write,
    DOWN,
    LEFT,
    RIGHT,
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
EQ = 60          # working equations
CHOICE = 44      # answer-choice rows
SIDE_NOTE = 44   # arithmetic asides
STEP = 28        # mono step headers

MAX_W = 4.0      # widest anything may run in a 4.5-unit frame


def fit(mobject, max_width=MAX_W):
    """Guard rail: nothing may run off the 4.5-unit-wide frame."""
    if mobject.width > max_width:
        mobject.scale_to_fit_width(max_width)
    return mobject


def stanza(*lines):
    return VGroup(*lines).arrange(DOWN, buff=0.14)


def choice_row(letter, tex):
    row = MathTex("\\text{" + letter + ".}\\;\\;", tex, font_size=CHOICE,
                  color=CHARCOAL)
    return fit(row)


class RearrangeConeShort(SATScene):
    scene_id = "shorts.rearrange_cone"

    def step_header(self, text):
        header = mono(text, STEP, GREY)
        header.move_to(UP * 3.55)
        return fit(header)

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

        # -------------------------------------------------------- choices
        ch_head = self.step_header("THE OPTIONS")
        rows = VGroup(
            choice_row("A", "r = \\frac{V}{3\\pi h}"),
            choice_row("B", "r = \\frac{3V}{\\pi h}"),
            choice_row("C", "r = \\sqrt{\\frac{3V}{\\pi h}}"),
            choice_row("D", "r = \\left(\\frac{3V}{\\pi h}\\right)^2"),
        ).arrange(DOWN, buff=0.4)
        for row in rows:
            row.align_to(rows, LEFT)
        rows.move_to(DOWN * 0.9)

        with self.beat("choices") as t:
            self.play(FadeOut(headline), FadeOut(ask),
                      cone.animate.scale(0.75).move_to(UP * 2.9),
                      run_time=t.fill(0.12))
            self.play(Write(ch_head), run_time=t.fill(0.08))
            for row in rows:
                self.play(Write(row), run_time=t.fill(0.12))
            t.hold()

        # ---------------------------------------------------------- clear
        cl_head = self.step_header("STEP 1: TIMES 3")
        cl_note = stanza(
            serif("multiply both", CAPTION, GREY),
            serif("sides by 3", CAPTION, GREY),
        )
        cl_note.move_to(DOWN * 2.9)
        m1 = MathTex("3V", "=", "\\pi r^2 h", font_size=EQ, color=CHARCOAL)
        m1.move_to(DOWN * 1.0)

        with self.beat("clear") as t:
            self.play(FadeOut(rows), FadeOut(ch_head),
                      run_time=t.fill(0.1))
            self.play(Write(cl_head), run_time=t.fill(0.08))
            self.play(FadeIn(cl_note), run_time=t.fill(0.12))
            self.play(Write(m1), run_time=t.fill(0.25))
            t.hold()

        # -------------------------------------------------------- isolate
        iso_head = self.step_header("STEP 2: ISOLATE")
        iso_note = stanza(
            serif("divide both", CAPTION, GREY),
            serif("sides by πh", CAPTION, GREY),
        )
        iso_note.move_to(DOWN * 2.9)
        m2 = MathTex("r^2", "=", "\\frac{3V}{\\pi h}", font_size=EQ,
                     color=CHARCOAL)
        m2.move_to(DOWN * 1.0)

        with self.beat("isolate") as t:
            self.play(FadeOut(cl_head), FadeOut(cl_note),
                      FadeIn(iso_note), run_time=t.fill(0.1))
            self.play(Write(iso_head), run_time=t.fill(0.08))
            self.play(TransformMatchingTex(m1, m2), run_time=t.fill(0.3))
            t.hold()

        # ----------------------------------------------------------- root
        rt_head = self.step_header("STEP 3: ROOT IT")
        rt_note = stanza(
            serif("undo the square —", CAPTION, GREY),
            serif("root both sides", CAPTION, GREY),
        )
        rt_note.move_to(DOWN * 2.9)
        m3 = MathTex("r", "=", "\\sqrt{\\frac{3V}{\\pi h}}", font_size=EQ,
                     color=CHARCOAL)
        m3.move_to(DOWN * 1.0)

        with self.beat("root") as t:
            self.play(FadeOut(iso_head), FadeOut(iso_note),
                      FadeIn(rt_note), run_time=t.fill(0.1))
            self.play(Write(rt_head), run_time=t.fill(0.08))
            self.play(TransformMatchingTex(m2, m3), run_time=t.fill(0.3))
            t.hold()

        # ----------------------------------------------------------- pick
        pk_head = self.step_header("THE ANSWER")
        rows2 = VGroup(
            choice_row("A", "r = \\frac{V}{3\\pi h}"),
            choice_row("B", "r = \\frac{3V}{\\pi h}"),
            choice_row("C", "r = \\sqrt{\\frac{3V}{\\pi h}}"),
            choice_row("D", "r = \\left(\\frac{3V}{\\pi h}\\right)^2"),
        ).arrange(DOWN, buff=0.4)
        for row in rows2:
            row.align_to(rows2, LEFT)
        rows2.move_to(DOWN * 0.9)

        def strike(row):
            return Line(row.get_left() + LEFT * 0.1,
                        row.get_right() + RIGHT * 0.1,
                        color=GREY, stroke_width=5)

        with self.beat("pick") as t:
            self.play(FadeOut(rt_head), FadeOut(rt_note), FadeOut(m3),
                      run_time=t.fill(0.08))
            self.play(Write(pk_head), FadeIn(rows2), run_time=t.fill(0.15))
            for idx in (0, 1, 3):
                self.play(rows2[idx].animate.set_color(GREY),
                          Write(strike(rows2[idx])),
                          run_time=t.fill(0.1))
            self.play(rows2[2].animate.set_color(SAGE),
                      run_time=t.fill(0.15))
            t.hold()

        # --------------------------------------------------------- answer
        boxed = MathTex("\\boxed{r = \\sqrt{\\tfrac{3V}{\\pi h}}}",
                        font_size=EQ_BIG, color=SAGE)
        fit(boxed)
        boxed.move_to(UP * 1.4)
        zinger = stanza(
            serif("the trap: B", Q),
            serif("forgets the root", Q),
        )
        for line in zinger:
            fit(line)
        zinger.arrange(DOWN, buff=0.14)
        zinger.move_to(DOWN * 1.2)

        with self.beat("answer") as t:
            self.play(*[FadeOut(m) for m in self.mobjects
                        if m is not None],
                      run_time=t.fill(0.1))
            self.play(Write(boxed), run_time=t.fill(0.25))
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
