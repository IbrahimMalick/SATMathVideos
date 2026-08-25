"""YouTube Short: systems of equations by substitution (music-driven, vertical).

Timing: timings/shorts.substitution.json (hand-authored to the music).
Render vertical: python -m manim render -r 1080,1920 --fps 60 \\
    scenes/shorts/substitution.py SubstitutionShort
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
EQ_BIG = 72      # the boxed answer
EQ = 60          # working equations
CHECK = 48       # check lines
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


class SubstitutionShort(SATScene):
    scene_id = "shorts.substitution"

    def step_header(self, text):
        header = mono(text, STEP, GREY)
        header.move_to(UP * 3.55)
        return fit(header)

    def construct(self):
        # ------------------------------------------------------- question
        headline = stanza(
            serif("Only A* O Level", HEADLINE),
            serif("students will", HEADLINE),
            serif("get this.", HEADLINE),
        )
        for line in headline:
            fit(line)
        headline.arrange(DOWN, buff=0.14)
        headline.move_to(UP * 2.7)

        e1 = MathTex("x", "+", "y", "=", "25", font_size=EQ, color=CHARCOAL)
        e1.move_to(UP * 0.6)
        e2 = MathTex("x = 4y", font_size=EQ, color=CHARCOAL)
        e2.move_to(DOWN * 0.4)
        ask = serif("What is y?", 38, TERRACOTTA)
        fit(ask)
        ask.move_to(DOWN * 1.9)

        with self.beat("question") as t:
            self.play(Write(headline), run_time=t.fill(0.25))
            self.play(Write(e1), run_time=t.fill(0.15))
            self.play(Write(e2), run_time=t.fill(0.15))
            self.play(Write(ask), run_time=t.fill(0.15))
            t.hold()

        # --------------------------------------------------------- method
        m_head = self.step_header("STEP 1: METHOD")
        m_cap = stanza(
            serif("x = 4y is already", CAPTION),
            serif("solved for x —", CAPTION),
            serif("use substitution!", CAPTION),
        )
        for line in m_cap:
            fit(line)
        m_cap.arrange(DOWN, buff=0.18)
        m_cap.move_to(UP * 0.2)

        with self.beat("method") as t:
            self.play(FadeOut(headline), FadeOut(ask),
                      e1.animate.move_to(UP * 2.5),
                      e2.animate.move_to(UP * 1.8),
                      run_time=t.fill(0.15))
            self.play(Write(m_head), run_time=t.fill(0.08))
            self.play(e2.animate.set_color(TERRACOTTA),
                      run_time=t.fill(0.1))
            self.play(Write(m_cap), run_time=t.fill(0.25))
            t.hold()

        # ----------------------------------------------------- substitute
        s_head = self.step_header("STEP 2: SUBSTITUTE")
        s_cap = serif("replace x with 4y", CAPTION)
        fit(s_cap)
        s_cap.move_to(UP * 0.3)
        w1 = MathTex("x", "+", "y", "=", "25", font_size=EQ, color=CHARCOAL)
        w2 = MathTex("4y", "+", "y", "=", "25", font_size=EQ, color=CHARCOAL)
        w3 = MathTex("5y", "=", "25", font_size=EQ, color=CHARCOAL)
        w4 = MathTex("y", "=", "\\frac{25}{5}", font_size=EQ, color=CHARCOAL)
        w5 = MathTex("y", "=", "5", font_size=EQ, color=CHARCOAL)
        for m in (w1, w2, w3, w4, w5):
            m.move_to(DOWN * 1.4)

        with self.beat("substitute") as t:
            self.play(FadeOut(m_cap), FadeOut(m_head),
                      e2.animate.set_color(CHARCOAL),
                      run_time=t.fill(0.1))
            self.play(Write(s_head), run_time=t.fill(0.08))
            self.play(Write(s_cap), run_time=t.fill(0.15))
            self.play(Write(w1), run_time=t.fill(0.18))
            self.play(TransformMatchingTex(w1, w2), run_time=t.fill(0.25))
            t.hold()

        # -------------------------------------------------------- combine
        c_head = self.step_header("STEP 3: COMBINE")
        combine_note = MathTex("4y + 1y = 5y", font_size=SIDE_NOTE,
                               color=GREY)
        combine_note.move_to(DOWN * 2.9)

        with self.beat("combine") as t:
            self.play(FadeOut(s_cap), FadeOut(s_head),
                      run_time=t.fill(0.08))
            self.play(Write(c_head), run_time=t.fill(0.08))
            self.play(FadeIn(combine_note), run_time=t.fill(0.15))
            self.play(TransformMatchingTex(w2, w3), run_time=t.fill(0.3))
            t.hold()

        # ---------------------------------------------------------- solve
        v_head = self.step_header("STEP 4: SOLVE")
        divide_note = stanza(
            serif("divide both", CAPTION, GREY),
            serif("sides by 5", CAPTION, GREY),
        )
        divide_note.move_to(DOWN * 2.9)

        with self.beat("solve") as t:
            self.play(FadeOut(c_head), FadeOut(combine_note),
                      FadeIn(divide_note), run_time=t.fill(0.1))
            self.play(Write(v_head), run_time=t.fill(0.08))
            self.play(TransformMatchingTex(w3, w4), run_time=t.fill(0.25))
            self.play(TransformMatchingTex(w4, w5), run_time=t.fill(0.25))
            t.hold()

        # ---------------------------------------------------------- check
        k_head = self.step_header("STEP 5: CHECK")
        k_cap = serif("quick check:", CAPTION)
        fit(k_cap)
        k_cap.move_to(UP * 0.3)
        c1 = MathTex("x = 4(5) = 20", font_size=CHECK, color=CHARCOAL)
        c1.move_to(DOWN * 2.4)
        c2 = MathTex("20 + 5 = 25\\;", "\\checkmark", font_size=CHECK,
                     color=CHARCOAL)
        c2.set_color_by_tex("\\checkmark", SAGE)
        c2.move_to(DOWN * 3.1)

        with self.beat("check") as t:
            self.play(FadeOut(v_head), FadeOut(divide_note),
                      run_time=t.fill(0.08))
            self.play(Write(k_head), run_time=t.fill(0.08))
            self.play(Write(k_cap), run_time=t.fill(0.12))
            self.play(Write(c1), run_time=t.fill(0.2))
            self.play(Write(c2), run_time=t.fill(0.2))
            t.hold()

        # --------------------------------------------------------- answer
        boxed = MathTex("\\boxed{y = 5}", font_size=EQ_BIG, color=SAGE)
        boxed.move_to(UP * 1.2)
        zinger = stanza(
            serif("substitute,", Q),
            serif("combine, solve.", Q),
        )
        fit(zinger)
        zinger.move_to(DOWN * 1.1)

        with self.beat("answer") as t:
            self.play(FadeOut(e1), FadeOut(e2), FadeOut(k_head),
                      FadeOut(k_cap), FadeOut(c1), FadeOut(c2),
                      run_time=t.fill(0.1))
            self.play(TransformMatchingTex(w5, boxed), run_time=t.fill(0.25))
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
