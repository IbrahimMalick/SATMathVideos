"""YouTube Short: the biggest rectangle under y = 12 - x^2 (music-driven, vertical).

Edexcel A Level Maths. There is no narration on this one — it is read, not
listened to — so the beats are hand-authored to the music rather than
resolved against a recording, the way shorts.direct_variation already is.
That is not a departure from the house rule: the rule exists so animation
is never hand-tuned to guess at a delivery, and here there is no delivery
to guess at.

The figure stays on screen for the whole Short and changes once, when the
optimum is found: the rectangle grows to its best shape and its labels
become numbers. A student who watches one picture settle has a chance of
remembering why x = 2 mattered.

Checked before building:

  * A(x) = 2x(12 - x^2) = 24x - 2x^3, and A(3) = 18 either way.
  * A'(x) = 24 - 6x^2 = 0 gives x^2 = 4, so x = 2 for a positive width.
  * at x = 2: width 4, height 12 - 4 = 8, area 32.
  * A''(2) = -24 < 0, so it really is a maximum, and a sweep over the
    whole valid range 0 < x < sqrt(12) peaks at 32.000000 at x = 2.

The second-derivative check is the one thing the written script leaves
out; it earns a mark at A Level and is not on screen here because it was
not in the script.

Timing: timings/shorts.max_rectangle.json
Render vertical: python -m manim render -r 1080,1920 --fps 60 \\
    scenes/shorts/max_rectangle.py MaxRectangle
Frame is 4.5 wide by 8 tall. Portrait pixels-per-unit is 1.78x the lecture
frame, so these font sizes read larger on screen than the numbers suggest.
"""

from manim import (
    Create,
    FadeIn,
    FadeOut,
    MathTex,
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

from brand import (  # noqa: E402
    CHARCOAL,
    GAP_SM,
    GREY,
    SAGE,
    SLATE,
    TERRACOTTA,
    mono,
    serif,
)
from components.optimisation import CurveRectangle  # noqa: E402
from scenes.base import SATScene  # noqa: E402

STRAP = 28       # the running series label
Q = 34           # the question
CAPTION = 30     # the running line of explanation
LABEL = 24       # labels on the figure
EQ = 46          # working equations
EQ_CURVE = 42    # the curve's own equation, under the strap
EQ_BIG = 60      # the boxed answer
SIGN_OFF = 64    # the closing shout

MAX_W = 4.0      # widest anything may run in a 4.5-unit frame

# The item. A new question is new numbers here, not a new drawing.
TOP = 12                     # y = TOP - x^2
ROOT = TOP ** 0.5            # where the curve meets the axis
START_HALF = 2.6             # a rectangle that is plainly not the best one
BEST_HALF = 2                # 24 - 6x^2 = 0
BEST_WIDTH = 2 * BEST_HALF   # 4
BEST_HEIGHT = TOP - BEST_HALF ** 2   # 8
BEST_AREA = BEST_WIDTH * BEST_HEIGHT  # 32

FIGURE_LIFT = 1.72   # puts the figure's top just under the curve's equation
CAPTION_Y = -0.45
EQ1_Y = -1.30
EQ2_Y = -2.05
# Nothing goes below this: the bottom of a Short is covered by YouTube's
# own title, channel name and buttons, and working printed under them is
# working the student never sees.
EQ3_Y = -2.78


def curve(x):
    return TOP - x * x


def fit(mobject, max_width=MAX_W):
    """Guard rail: nothing may run off the 4.5-unit-wide frame."""
    if mobject.width > max_width:
        mobject.scale_to_fit_width(max_width)
    return mobject


def stanza(*mobjects, buff=GAP_SM * 1.1):
    return VGroup(*mobjects).arrange(DOWN, buff=buff)


class MaxRectangle(SATScene):
    scene_id = "shorts.max_rectangle"

    def construct(self):
        strap = fit(mono("Edexcel A Level Maths", STRAP, GREY))
        strap.to_edge(UP, buff=GAP_SM)

        equation = MathTex(f"y = {TOP} - x^2", font_size=EQ_CURVE, color=SLATE)
        equation.move_to(UP * 3.08)

        figure = CurveRectangle(curve, ROOT, START_HALF)
        figure.shift(UP * FIGURE_LIFT)

        self.caption_holder = None

        # ------------------------------------------------------------ open
        with self.beat("open") as t:
            self.add(strap)
            self.play(Write(equation), run_time=t.fill(0.22))
            self.play(Create(figure.axes), run_time=t.fill(0.2))
            self.play(Create(figure.graph), run_time=t.fill(0.26))
            self.play(Create(figure.rect), FadeIn(figure.corner),
                      run_time=t.fill(0.22))
            t.hold()

        # -------------------------------------------------------- question
        ask = stanza(
            serif("What is the biggest", Q, CHARCOAL),
            serif("area this rectangle", Q, CHARCOAL),
            serif("can have?", Q, TERRACOTTA),
        )
        fit(ask)
        ask.move_to(DOWN * 1.9)

        with self.beat("question") as t:
            self.play(Write(ask), run_time=t.fill(0.45))
            t.hold()

        # ------------------------------------------- x is half the width
        tick = figure.tick(START_HALF)
        x_label = figure.below("x", START_HALF / 2)

        with self.beat("half_width") as t:
            self.play(FadeOut(ask), run_time=t.fill(0.08))
            self.say(t, "It is centred on the y-axis,", "so let x be half the width.",
                     fraction=0.22)
            self.play(Create(tick), run_time=t.fill(0.12))
            self.play(Write(x_label), run_time=t.fill(0.2))
            t.hold()

        # ------------------------------------------------- the full width
        width_label = figure.below("2x", 0, level=1)

        with self.beat("width") as t:
            self.say(t, "So the full width is 2x.", fraction=0.25)
            self.play(Write(width_label), run_time=t.fill(0.25))
            t.hold()

        # ------------------------------------- the curve gives the height
        height_label = figure.inside(f"{TOP} - x^2", at_x=-START_HALF / 2)

        with self.beat("height") as t:
            self.say(t, "The curve gives the height.", fraction=0.22)
            self.play(Write(height_label), run_time=t.fill(0.25))
            t.hold()

        # --------------------------------------------- area = width x height
        area1 = MathTex("A", "=", "2x(12 - x^2)", font_size=EQ,
                        color=CHARCOAL)
        area1.move_to([0, EQ1_Y, 0])
        area2 = MathTex("A", "=", "24x - 2x^3", font_size=EQ, color=CHARCOAL)
        area2.move_to([0, EQ1_Y, 0])

        with self.beat("area") as t:
            self.say(t, "Area is width times height.", fraction=0.16)
            self.play(Write(area1), run_time=t.fill(0.3))
            self.play(TransformMatchingTex(area1, area2), run_time=t.fill(0.26))
            t.hold()

        # ----------------------------------------- differentiate, set to 0
        # \tfrac, not \frac: a display fraction here stands nearly a
        # unit tall and closes the gap to the lines above and below it.
        derivative = MathTex(r"\tfrac{dA}{dx}", "=", "24 - 6x^2", "=", "0",
                             font_size=EQ, color=CHARCOAL)
        derivative.move_to([0, EQ2_Y, 0])

        with self.beat("diff") as t:
            self.say(t, "Differentiate, then set it to zero.", fraction=0.16)
            self.play(Write(derivative), run_time=t.fill(0.4))
            t.hold()

        # ----------------------------------------------------------- x = 2
        root = MathTex(f"x = {BEST_HALF}", font_size=EQ, color=TERRACOTTA)
        root.move_to([0, EQ3_Y, 0])

        with self.beat("solve") as t:
            self.play(Write(root), run_time=t.fill(0.35))
            t.hold()

        # ------------------------------------- the rectangle finds its shape
        best_rect, best_dot = figure.grown_to(BEST_HALF)
        new_tick = figure.tick(BEST_HALF)
        new_width = figure.below(str(BEST_WIDTH), 0, level=1)
        new_half = figure.below(str(BEST_HALF), BEST_HALF / 2)
        new_height = figure.inside(str(BEST_HEIGHT), at_x=-BEST_HALF / 2)

        with self.beat("dims") as t:
            # The chain stays up while the picture settles: clearing it
            # here leaves a band of empty frame between the caption and
            # the x = 2 that earned these numbers.
            self.say(t, f"Width {BEST_WIDTH}, height {BEST_HEIGHT}.",
                     fraction=0.16)
            self.play(
                Transform(figure.rect, best_rect),
                Transform(figure.corner, best_dot),
                Transform(tick, new_tick),
                Transform(x_label, new_half),
                Transform(width_label, new_width),
                Transform(height_label, new_height),
                run_time=t.fill(0.4),
            )
            t.hold()

        # ---------------------------------------------------------- answer
        answer = MathTex(
            rf"{BEST_WIDTH} \times {BEST_HEIGHT} = \boxed{{{BEST_AREA}}}",
            font_size=EQ_BIG, color=SAGE,
        )
        fit(answer)
        answer.move_to([0, -1.55, 0])
        units = fit(serif("square units", CAPTION, GREY))
        units.next_to(answer, DOWN, buff=GAP_SM * 1.3)

        with self.beat("answer") as t:
            self.play(FadeOut(area2), FadeOut(derivative), FadeOut(root),
                      run_time=t.fill(0.1))
            self.say(t, "Maximum area:", fraction=0.12)
            self.play(Write(answer), run_time=t.fill(0.35))
            self.play(FadeIn(units), run_time=t.fill(0.18))
            t.hold()

        # ----------------------------------------------------- bhalay bhalay
        card = stanza(
            serif("Bhalay Bhalay!", SIGN_OFF, TERRACOTTA),
            serif("Edexcel A Level Maths", CAPTION, GREY),
            serif("The Digital Tutor", Q, CHARCOAL),
            buff=GAP_SM * 2.2,
        )
        fit(card)

        with self.beat("bhalay") as t:
            keep = {id(strap)}
            going = [m for m in self.mobjects if id(m) not in keep]
            self.play(*[FadeOut(m) for m in going], run_time=t.fill(0.12))
            self.play(Write(card[0]), run_time=t.fill(0.3))
            self.play(FadeIn(card[1]), FadeIn(card[2]), run_time=t.fill(0.2))
            t.hold()

    # ---------------------------------------------------------------- helper

    def say(self, t, *texts, fraction=0.2, color=GREY, size=CAPTION):
        """The running line under the figure, swapped in place.

        One slot rather than a growing column: the figure takes the top
        half of a portrait frame and the working takes the rest, so an
        explanation that accumulated would push the algebra off the bottom.

        One Text with newlines rather than a group of them, because the
        slot is swapped by Transform: transforming a two-line group into a
        one-line group leaves both of the old lines morphing onto the same
        spot, and they sit there on top of each other for the rest of the
        Short.
        """
        line = fit(serif("\n".join(texts), size, color))
        line.move_to([0, CAPTION_Y, 0])
        if self.caption_holder is None:
            self.caption_holder = line
            self.play(FadeIn(line), run_time=t.fill(fraction))
        else:
            self.play(Transform(self.caption_holder, line),
                      run_time=t.fill(fraction))
        return self.caption_holder
