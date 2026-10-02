"""YouTube Short: ordinary notation -> scientific notation (Urdu narration).

Punjab Board Class 9, Unit 2. One exam skill only: move the decimal until a
single digit sits before it, count the places, and let the direction decide
the sign of the exponent.

The narration is Urdu with English maths terms, so the screen carries
numerals and English words only — nothing on screen needs an Urdu font.
Timing comes from the recording: timings/shorts.scientific_notation.json.

Render vertical: python build/render.py scripts/G9-scientific-notation.md \\
    audio/G9-scientific-notation.m4a --language ur
Frame is 4.5 wide by 8 tall. Portrait pixels-per-unit is 1.8x the lecture
frame, so these font sizes read larger on screen than the numbers suggest.
"""

from manim import (
    Create,
    FadeIn,
    FadeOut,
    Line,
    MathTex,
    SurroundingRectangle,
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

TITLE = 44       # the hook headline
HERO = 68        # the one number the viewer must look at
EQ = 50          # worked equations
BADGE = 46       # LEFT -> + / RIGHT -> - cards
CAPTION = 32     # short English captions under the maths
TAG = 28         # mono strap line

MAX_W = 3.9      # widest anything may run in a 4.5-unit frame


def fit(mobject, width=MAX_W):
    if mobject.width > width:
        mobject.scale_to_fit_width(width)
    return mobject


def stack(*mobjects, buff=GAP_MD):
    return VGroup(*mobjects).arrange(DOWN, buff=buff)


class ScientificNotation(SATScene):
    scene_id = "shorts.scientific_notation"

    def construct(self):
        # Kept short so fit() never shrinks it: at 4.5 units wide, a
        # longer strap scales under the 28px floor.
        self.strap = mono("Punjab Board · Class 9", TAG)
        fit(self.strap)
        self.strap.to_edge(UP, buff=GAP_MD)
        self.keep = [self.strap]

        self.opening()
        self.big_number_half()
        self.small_number_half()
        self.memory_trick()
        self.quick_test()
        self.closing()

    # -------------------------------------------------------------- helpers

    def wipe(self, t, fraction=0.08):
        old = [m for m in self.mobjects if m not in self.keep]
        if old:
            self.play(*[FadeOut(m) for m in old], run_time=t.fill(fraction))

    def badge(self, text, colour=TERRACOTTA):
        label = serif(text, BADGE, colour)
        fit(label)
        box = SurroundingRectangle(label, color=colour, buff=GAP_SM * 0.9,
                                   stroke_width=3)
        return VGroup(box, label)

    # ------------------------------------------------------------- sections

    def opening(self):
        with self.beat("hook") as t:
            self.add(self.strap)
            title = stack(
                serif("SCIENTIFIC", TITLE, CHARCOAL),
                serif("NOTATION", TITLE, CHARCOAL),
                buff=GAP_SM,
            )
            easy = serif("— EASY —", TITLE * 0.8, TERRACOTTA)
            block = stack(title, easy, buff=GAP_MD * 1.6)
            fit(block)
            block.move_to(UP * 0.6)
            self.play(Write(title), run_time=t.fill(0.32))
            self.play(Write(easy), run_time=t.fill(0.2))
            t.hold()

    def big_number_half(self):
        with self.beat("big_number") as t:
            self.wipe(t, 0.25)
            self.big = MathTex(r"78{,}000{,}000", font_size=HERO,
                               color=CHARCOAL)
            fit(self.big)
            self.big.move_to(UP * 1.6)
            self.play(Write(self.big), run_time=t.fill(0.5))
            t.hold()

        with self.beat("move_rule") as t:
            rule = stack(
                serif("move the decimal until", CAPTION, GREY),
                serif("ONE digit is before it", CAPTION, GREY),
                buff=GAP_SM * 0.8,
            )
            fit(rule)
            rule.next_to(self.big, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(rule), run_time=t.fill(0.22))
            moved = MathTex(r"7.8", font_size=HERO, color=SLATE)
            moved.next_to(rule, DOWN, buff=GAP_MD * 1.4)
            arrow = Line(rule.get_bottom() + DOWN * GAP_SM * 0.6,
                         moved.get_top() + UP * GAP_SM * 0.6,
                         color=GREY, stroke_width=3)
            self.play(Create(arrow), run_time=t.fill(0.1))
            self.play(Write(moved), run_time=t.fill(0.22))
            self.moved = moved
            t.hold()

        with self.beat("count") as t:
            ask = serif("how many places?", CAPTION, CHARCOAL)
            fit(ask)
            ask.next_to(self.moved, DOWN, buff=GAP_MD * 1.2)
            self.play(Write(ask), run_time=t.fill(0.3))
            t.hold()

        with self.beat("seven") as t:
            seven = serif("7 places", BADGE, TERRACOTTA)
            fit(seven)
            seven.move_to(DOWN * 3.0)
            self.play(Write(seven), run_time=t.fill(0.5))
            t.hold()

        with self.beat("answer1") as t:
            # Keep the 7.8 and grow the power onto it — one step becoming the
            # next is what TransformMatchingTex is for.
            old = [m for m in self.mobjects
                   if m not in self.keep and m is not self.moved]
            self.play(*[FadeOut(m) for m in old],
                      self.moved.animate.move_to(UP * 0.6),
                      run_time=t.fill(0.14))
            target = MathTex(r"7.8 \times 10^{7}", font_size=HERO,
                             color=CHARCOAL)
            fit(target)
            target.move_to(UP * 0.6)
            self.play(TransformMatchingTex(self.moved, target),
                      run_time=t.fill(0.3))
            source = MathTex(r"78{,}000{,}000 \;=", font_size=EQ, color=GREY)
            fit(source)
            source.next_to(target, UP, buff=GAP_MD * 1.4)
            self.play(Write(source), run_time=t.fill(0.2))
            self.answer1 = VGroup(source, target)
            t.hold()

        with self.beat("left_plus") as t:
            card = self.badge("LEFT  →  +")
            card.next_to(self.answer1, DOWN, buff=GAP_MD * 2.0)
            self.play(FadeIn(card), run_time=t.fill(0.22))
            t.hold()

    def small_number_half(self):
        with self.beat("small") as t:
            self.wipe(t, 0.14)
            self.small = MathTex(r"0.0000000315", font_size=EQ * 1.1,
                                 color=CHARCOAL)
            fit(self.small)
            self.small.move_to(UP * 1.8)
            same = serif("same rule", CAPTION, GREY)
            same.next_to(self.small, DOWN, buff=GAP_MD)
            self.play(Write(self.small), run_time=t.fill(0.4))
            self.play(Write(same), run_time=t.fill(0.16))
            self.same = same
            t.hold()

        with self.beat("move2") as t:
            moved = MathTex(r"3.15", font_size=HERO, color=SLATE)
            moved.next_to(self.same, DOWN, buff=GAP_MD * 1.6)
            arrow = Line(self.same.get_bottom() + DOWN * GAP_SM * 0.6,
                         moved.get_top() + UP * GAP_SM * 0.6,
                         color=GREY, stroke_width=3)
            self.play(Create(arrow), run_time=t.fill(0.14))
            self.play(Write(moved), run_time=t.fill(0.26))
            self.moved2 = moved
            t.hold()

        with self.beat("eight_right") as t:
            eight = serif("8 places RIGHT", BADGE * 0.9, TERRACOTTA)
            fit(eight)
            eight.next_to(self.moved2, DOWN, buff=GAP_MD * 1.6)
            self.play(Write(eight), run_time=t.fill(0.3))
            t.hold()

        with self.beat("answer2") as t:
            old = [m for m in self.mobjects
                   if m not in self.keep and m is not self.moved2]
            self.play(*[FadeOut(m) for m in old],
                      self.moved2.animate.move_to(UP * 0.8),
                      run_time=t.fill(0.14))
            target = MathTex(r"3.15 \times 10^{-8}", font_size=HERO * 0.95,
                             color=CHARCOAL)
            fit(target)
            target.move_to(UP * 0.8)
            self.play(TransformMatchingTex(self.moved2, target),
                      run_time=t.fill(0.3))
            card = self.badge("RIGHT  →  −")
            card.next_to(target, DOWN, buff=GAP_MD * 2.2)
            self.play(FadeIn(card), run_time=t.fill(0.22))
            t.hold()

    def memory_trick(self):
        with self.beat("trick") as t:
            self.wipe(t, 0.08)
            left = serif("LEFT  =  PLUS", BADGE, CHARCOAL)
            right = serif("RIGHT  =  MINUS", BADGE, CHARCOAL)
            block = stack(fit(left), fit(right), buff=GAP_MD * 1.8)
            block.move_to(UP * 0.8)
            rule = Line(block.get_left(), block.get_right(), color=GREY,
                        stroke_width=2)
            rule.move_to(block.get_center())
            self.play(Write(left), run_time=t.fill(0.2))
            self.play(Create(rule), run_time=t.fill(0.08))
            self.play(Write(right), run_time=t.fill(0.2))
            self.trick_block = block
            t.hold()

        with self.beat("trick2") as t:
            plus = serif("←  +", BADGE * 1.3, TERRACOTTA)
            minus = serif("−  →", BADGE * 1.3, SLATE)
            pair = stack(plus, minus, buff=GAP_MD * 1.4)
            fit(pair)
            pair.next_to(self.trick_block, DOWN, buff=GAP_MD * 2.2)
            self.play(Write(plus), run_time=t.fill(0.26))
            self.play(Write(minus), run_time=t.fill(0.26))
            t.hold()

    def quick_test(self):
        with self.beat("quiz") as t:
            self.wipe(t, 0.07)
            your_turn = serif("your turn", CAPTION, GREY)
            question = MathTex(r"29{,}000{,}000 \;=\; ?", font_size=EQ,
                               color=CHARCOAL)
            fit(question)
            block = stack(your_turn, question, buff=GAP_MD * 1.6)
            block.move_to(UP * 1.0)
            self.play(Write(your_turn), run_time=t.fill(0.12))
            self.play(Write(question), run_time=t.fill(0.26))
            self.quiz_block = block
            t.hold()

        with self.beat("reveal") as t:
            answer = MathTex(r"2.9 \times 10^{7}", font_size=HERO,
                             color=TERRACOTTA)
            fit(answer)
            answer.next_to(self.quiz_block, DOWN, buff=GAP_MD * 2.0)
            # \checkmark via LaTeX: DejaVu Serif has no reliable U+2713.
            tick = MathTex(r"\checkmark", font_size=HERO, color=SAGE)
            tick.next_to(answer, DOWN, buff=GAP_MD)
            self.play(Write(answer), run_time=t.fill(0.3))
            self.play(Write(tick), run_time=t.fill(0.16))
            t.hold()

    def closing(self):
        with self.beat("closing") as t:
            self.wipe(t, 0.05)
            line = stack(
                serif("Punjab Board Maths", TITLE * 0.9, CHARCOAL),
                serif("itni mushkil nahi!", TITLE * 0.9, TERRACOTTA),
                buff=GAP_SM * 1.4,
            )
            fit(line)
            line.move_to(UP * 0.4)
            self.play(Write(line), run_time=t.fill(0.26))
            self.wait(t.fill(0.14))

            # The outro card the recording stops short of — on screen only,
            # over the bhangra sting added in post.
            self.play(FadeOut(line), run_time=t.fill(0.05))
            balay = serif("BHALAY BHALAY!", TITLE, TERRACOTTA)
            fit(balay)
            balay.move_to(UP * 0.5)
            logo = serif("The Digital Tutor", CAPTION, GREY)
            logo.next_to(balay, DOWN, buff=GAP_MD * 1.6)
            self.play(Write(balay), run_time=t.fill(0.12))
            self.play(FadeIn(logo), run_time=t.fill(0.08))
            t.hold()
