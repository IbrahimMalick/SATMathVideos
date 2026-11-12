"""The AP CSA cohort ad: caption layer, rendered over the client's footage.

This scene renders nothing but text on a transparent background. The
footage and the voice are the client's, from an AI-generated ad; what
failed there was the text layer, so that is all this replaces.
``build/ad_composite.py`` lays the result back over the original.

The whole point is that nothing here can clip, so nothing is positioned by
eye:

  * captions are laid out from the frame's own edges, with one declared
    margin, and ``components.ad_caption.measure()`` checks every state
    against the frame before a frame is rendered.
  * a line that will not fit raises rather than wrapping, so an overlong
    caption fails the build instead of folding into the picture. The copy
    in ad_caption.py was re-broken until it passed.
  * the call to action is not over footage at all. The last eleven
    seconds cut to the house card, which is also how the channel's own
    videos end, and which is the only way to put a URL and a phone number
    on screen over a shot of a fridge door.

Captions sit on the left and run no wider than 8.9 units, so the right
third of the frame keeps showing the picture that is paying for the
caption. They are bottom-anchored and grow upward, so a block that gains
a line pushes its own earlier lines up rather than reaching down toward
the edge.

Rendered at 30fps to match the source footage, not the house 60: the
composite has to land on the client's frame grid.

    python -m manim render -t -r 1920,1080 --fps 30 \\
        scenes/ads/apcsa_cohort.py ApcsaCohort
    python build/ad_composite.py --landscape <the client's mp4>

Timing: timings/ads.apcsa_cohort.json
"""

from contextlib import contextmanager

from manim import (
    AnimationGroup,
    FadeIn,
    FadeOut,
    Line,
    Rectangle,
    VGroup,
    DOWN,
    LEFT,
    UP,
    config,
)

from brand import (
    CHARCOAL,
    CREAM,
    DISPLAY_SIZE,
    GAP_SM,
    GREY,
    LABEL_SIZE,
    MARGIN_SIZE,
    SLATE,
    TERRACOTTA,
    TITLE_SIZE,
    serif,
)
from components.ad_caption import (
    ACCENTS,
    BRAND,
    COHORT,
    EXAM,
    FACTS,
    PHONE,
    SCRIPT,
    URL,
    caption_block,
)
from scenes.base import SATScene

CAPTION = 40        # the running captions over footage
CAPTION_WIDTH = 8.9  # measured against every state in ad_caption.measure()
MARGIN = 0.95        # from the frame's left edge to the first pill
FLOOR = -3.30        # the bottom of the lowest pill

COHORT_SIZE = 38


def fit(mobject, width):
    if mobject.width > width:
        raise ValueError(
            f"{mobject} is {mobject.width:.2f} units wide, over the "
            f"{width:.2f} the card allows. Shorten the copy."
        )
    return mobject


class ApcsaCohort(SATScene):
    scene_id = "ads.apcsa_cohort"

    def setup(self):
        super().setup()
        # Everything this scene draws goes over someone else's picture, so
        # the background has to carry alpha rather than the house cream.
        # Rendered with -t; this makes the scene honest if it is not.
        self.camera.background_opacity = 0
        self.camera.init_background()

    def construct(self):
        self.shown = []        # [(text, mobject)] currently on screen
        self.captions()
        self.end_card()

    # ------------------------------------------------------------- captions

    def captions(self):
        for beat, mode, lines in SCRIPT:
            with self.beat(beat) as t:
                wanted = (list(lines) if mode == "set"
                          else [text for text, _ in self.shown] + list(lines))
                block = caption_block(wanted, CAPTION, CAPTION_WIDTH, ACCENTS)
                block.move_to([-config.frame_width / 2 + MARGIN
                               + block.width / 2,
                               FLOOR + block.height / 2, 0])

                if mode == "set":
                    # Out, then in, inside a single play. A plain
                    # crossfade leaves the old caption and the new one
                    # both at half strength on top of each other for most
                    # of a second, which reads as a mistake rather than a
                    # transition. Two plays would cost a second, and the
                    # shortest beat here is 0.84s, so the stagger has to
                    # happen inside one.
                    arriving = AnimationGroup(
                        *[FadeIn(line) for line in block])
                    if self.shown:
                        moves = [AnimationGroup(
                            AnimationGroup(
                                *[FadeOut(m) for _, m in self.shown]),
                            arriving,
                            lag_ratio=0.55,
                        )]
                    else:
                        # The first caption has nothing to replace, and an
                        # empty AnimationGroup is an error, not a no-op.
                        moves = [arriving]
                    self.shown = list(zip(wanted, block))
                else:
                    # The block grows upward, so the lines already up have
                    # to rise by exactly the height of what is joining
                    # them. Animated, not cut, or the caption jumps.
                    kept = len(self.shown)
                    moves = [
                        old.animate.move_to(new.get_center())
                        for (_, old), new in zip(self.shown, block[:kept])
                    ]
                    moves += [FadeIn(line) for line in block[kept:]]
                    self.shown = (
                        [(text, old) for (text, old) in self.shown]
                        + list(zip(wanted[kept:], block[kept:])))

                # One play per beat: two would cost a second, and the
                # shortest beat here is 0.84s.
                self.play(*moves, run_time=t.fill(0.42))
                t.hold()

    # ------------------------------------------------------------- end card

    def end_card(self):
        half_w, half_h = config.frame_width / 2, config.frame_height / 2
        safe = config.frame_width - 2 * MARGIN

        # Two per cent past every edge, so no sliver of the footage
        # survives at the border when the overlay is composited back.
        card = Rectangle(width=config.frame_width * 1.02,
                         height=config.frame_height * 1.02, stroke_width=0)
        card.set_fill(CREAM, opacity=1)
        card.full_bleed = True

        brand = fit(serif(BRAND, DISPLAY_SIZE, CHARCOAL), safe)
        brand.move_to([0, half_h * 0.59, 0])

        cohort = fit(serif(COHORT, COHORT_SIZE, SLATE), safe)
        cohort.move_to([0, half_h * 0.36, 0])

        rule = Line([-4.0, 0, 0], [4.0, 0, 0], color=GREY, stroke_width=2)
        rule.move_to([0, half_h * 0.24, 0])

        facts = VGroup(*[fit(serif(line, LABEL_SIZE, GREY), safe)
                         for line in FACTS])
        facts.arrange(DOWN, buff=GAP_SM * 1.1)
        facts.move_to([0, half_h * 0.03, 0])

        url = fit(serif(URL, DISPLAY_SIZE, TERRACOTTA), safe)
        url.move_to([0, -half_h * 0.29, 0])

        phone = fit(serif(PHONE, TITLE_SIZE, CHARCOAL), safe)
        phone.move_to([0, -half_h * 0.53, 0])

        exam = fit(serif(EXAM, MARGIN_SIZE, GREY), safe)
        exam.move_to([0, -half_h * 0.78, 0])

        self.guard_card([brand, cohort, facts, url, phone, exam], half_h)

        with self.beat("brand") as t:
            self.play(*[FadeOut(m) for _, m in self.shown],
                      FadeIn(card), FadeIn(brand), run_time=t.fill(0.5))
            self.shown = []
            t.hold()

        with self.beat("cohort") as t:
            self.play(FadeIn(cohort), FadeIn(rule), FadeIn(facts),
                      run_time=t.fill(0.35))
            t.hold()

        with self.beat("url") as t:
            self.play(FadeIn(url), run_time=t.fill(0.3))
            t.hold()

        with self.beat("phone") as t:
            self.play(FadeIn(phone), FadeIn(exam), run_time=t.fill(0.26))
            t.hold()

    # --------------------------------------------------------------- guards

    @staticmethod
    def guard_card(rows, half_h):
        """Nothing on the card may touch the one above or the frame edge.

        The ad this replaces put its URL across a calendar and lost its
        phone number off the bottom. This is the check that says so before
        a frame is rendered rather than after it is uploaded.
        """
        for upper, lower in zip(rows, rows[1:]):
            gap = upper.get_bottom()[1] - lower.get_top()[1]
            if gap < 0.08:
                raise ValueError(
                    f"End card rows overlap: {gap:+.2f} units between "
                    f"these two. Move them apart or shorten the copy."
                )
        if rows[0].get_top()[1] > half_h - 0.3:
            raise ValueError("The end card's first row runs off the top.")
        if rows[-1].get_bottom()[1] < -half_h + 0.3:
            raise ValueError("The end card's last row runs off the bottom.")

    _beat_name = "(before the first beat)"

    @contextmanager
    def beat(self, name):
        self._beat_name = name
        with super().beat(name) as timer:
            yield timer
