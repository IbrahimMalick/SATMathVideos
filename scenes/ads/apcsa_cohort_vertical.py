"""The AP CSA cohort ad, vertical: footage in a window, words underneath.

The same voiceover and the same beats as scenes/ads/apcsa_cohort.py, laid
out for a phone. Rendered with alpha over a cream frame that
build/ad_composite.py builds, with the client's footage scaled to the full
width and pinned in the window this scene leaves for it.

Vertical is not a crop of horizontal. Cropping 16:9 to 9:16 keeps a third
of the picture and cuts the people in this footage in half, and every shot
in it is two people or a person and a screen. So the footage keeps its
own framing at the top, and the words go where a crop would have thrown
picture away.

Nor is the copy a crop. This frame takes about 22 characters on a line at
a size a phone can read, against 28 in the landscape cut, so
components.ad_caption carries a second table with the lines broken again.
Where a line breaks is a writing decision, not something to leave to a
wrapper.

Captions sit on cream rather than over the picture, so they have no pills:
a dark pill on cream is a bruise. Everything stays above y = -2.55, which
is where a Short's own title, channel name and buttons start.

    python -m manim render -t -r 1080,1920 --fps 30 \\
        scenes/ads/apcsa_cohort_vertical.py ApcsaCohortVertical
    python build/ad_composite.py --base <the client's mp4> --cut portrait

Timing: timings/ads.apcsa_cohort_vertical.json
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
    config,
)

# Portrait: manim holds frame_width fixed by default, which would make the
# frame 25 units tall. Pin the intended 4.5 x 8 before anything reads it.
config.frame_height = 8.0
config.frame_width = 4.5

from brand import (  # noqa: E402
    CHARCOAL,
    CREAM,
    GAP_SM,
    GREY,
    SLATE,
    TERRACOTTA,
    mono,
    serif,
)
from components.ad_caption import (  # noqa: E402
    ACCENTS_PORTRAIT,
    BRAND,
    COHORT_PORTRAIT,
    FACTS_PORTRAIT,
    PHONE,
    SCRIPT_PORTRAIT,
    URL,
    plain_block,
)
from scenes.base import SATScene  # noqa: E402

# The window the footage sits in, in frame units. 240 px to the unit at
# 1080x1920: the clip is 1080x432 placed at y = 300, which is these two
# numbers. Change one and change the portrait filter in ad_composite.py.
#
# 432 and not 608 because the footage is cropped before it is scaled: the
# client's own captions are burned into the bottom of his frame, and in a
# window this small blurring them out is more conspicuous than losing the
# desks they sit on.
CLIP_TOP = 2.75
CLIP_BOTTOM = 0.95

SAFE = 4.1           # widest any line may run in a 4.5-unit frame
LEFT_EDGE = -2.05    # where every caption line starts
CAPTION_TOP = CLIP_BOTTOM - 0.45
# Below this sit a Short's own title, channel name and buttons. Nothing
# the viewer needs goes here.
FLOOR = -2.55

STRAP = 20           # the running label above the window
CAPTION = 24         # the captions; 24 here reads like 43 in the lecture
                     # frame, because portrait is 1.78x the density

BRAND_SIZE = 30
COHORT_SIZE = 24
FACT_SIZE = 18       # 18 nominal is 32px at 1080x1920: above the floor
URL_SIZE = 23
PHONE_SIZE = 24
EXAM_SIZE = 18

EXAM_SHORT = "AP exam: May 12, 2027"


def fit(mobject, width=SAFE, what="a line"):
    if mobject.width > width:
        raise ValueError(
            f"{what} is {mobject.width:.2f} units wide, over the "
            f"{width:.2f} this frame allows. Break it in the copy."
        )
    return mobject


class ApcsaCohortVertical(SATScene):
    scene_id = "ads.apcsa_cohort_vertical"

    def setup(self):
        super().setup()
        # The cream and the footage are laid down by ffmpeg; this layer
        # carries only words, and has to be transparent to let them through.
        self.camera.background_opacity = 0
        self.camera.init_background()

    def construct(self):
        self.shown = []
        strap = fit(mono("AP Computer Science A", STRAP, GREY),
                    what="the strap")
        strap.move_to([0, (CLIP_TOP + config.frame_height / 2) / 2, 0])
        self.strap = strap
        self.add(strap)

        self.captions()
        self.end_card()

    # ------------------------------------------------------------- captions

    def captions(self):
        for beat, mode, lines in SCRIPT_PORTRAIT:
            with self.beat(beat) as t:
                wanted = (list(lines) if mode == "set"
                          else [text for text, _ in self.shown] + list(lines))
                block = plain_block(wanted, CAPTION, SAFE, ACCENTS_PORTRAIT)
                block.move_to([LEFT_EDGE + block.width / 2,
                               CAPTION_TOP - block.height / 2, 0])
                self.guard_floor(block, beat)

                if mode == "set":
                    arriving = AnimationGroup(
                        *[FadeIn(line) for line in block])
                    if self.shown:
                        moves = [AnimationGroup(
                            AnimationGroup(
                                *[FadeOut(m) for _, m in self.shown]),
                            arriving, lag_ratio=0.55)]
                    else:
                        moves = [arriving]
                    self.shown = list(zip(wanted, block))
                else:
                    # Captions hang from a fixed top edge here rather than
                    # standing on a floor, so a new line pushes nothing;
                    # the lines above it stay exactly where they were.
                    kept = len(self.shown)
                    moves = [
                        old.animate.move_to(new.get_center())
                        for (_, old), new in zip(self.shown, block[:kept])
                    ]
                    moves += [FadeIn(line) for line in block[kept:]]
                    self.shown = (list(self.shown)
                                  + list(zip(wanted[kept:], block[kept:])))

                self.play(*moves, run_time=t.fill(0.42))
                t.hold()

    # ------------------------------------------------------------- end card

    def end_card(self):
        card = Rectangle(width=config.frame_width * 1.03,
                         height=config.frame_height * 1.03, stroke_width=0)
        card.set_fill(CREAM, opacity=1)
        card.full_bleed = True

        brand = fit(serif(BRAND, BRAND_SIZE, CHARCOAL), what="the brand line")
        brand.move_to([0, 2.55, 0])

        cohort = VGroup(*[fit(serif(line, COHORT_SIZE, SLATE), what=line)
                          for line in COHORT_PORTRAIT])
        cohort.arrange(DOWN, buff=GAP_SM * 0.8)
        cohort.move_to([0, 1.65, 0])

        rule = Line([-1.5, 0, 0], [1.5, 0, 0], color=GREY, stroke_width=2)
        rule.move_to([0, 1.14, 0])

        facts = VGroup(*[fit(serif(line, FACT_SIZE, GREY), what=line)
                         for line in FACTS_PORTRAIT])
        facts.arrange(DOWN, buff=GAP_SM * 0.75)
        facts.move_to([0, 0.28, 0])

        url = fit(serif(URL, URL_SIZE, TERRACOTTA), what="the url")
        url.move_to([0, -0.85, 0])

        phone = fit(serif(PHONE, PHONE_SIZE, CHARCOAL), what="the phone line")
        phone.move_to([0, -1.55, 0])

        exam = fit(serif(EXAM_SHORT, EXAM_SIZE, GREY), what="the exam line")
        exam.move_to([0, -2.25, 0])

        rows = [brand, cohort, rule, facts, url, phone, exam]
        self.guard_card(rows)

        with self.beat("brand") as t:
            self.play(*[FadeOut(m) for _, m in self.shown],
                      FadeOut(self.strap), FadeIn(card), FadeIn(brand),
                      run_time=t.fill(0.5))
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

    def guard_floor(self, block, beat):
        if block.get_bottom()[1] < FLOOR:
            raise ValueError(
                f"Beat '{beat}': the caption reaches "
                f"y={block.get_bottom()[1]:.2f}, below y={FLOOR}, where a "
                "Short's own title and buttons sit. Shorten the copy."
            )

    @staticmethod
    def guard_card(rows):
        """Nothing on the card may touch the row above or the Shorts UI."""
        for upper, lower in zip(rows, rows[1:]):
            gap = upper.get_bottom()[1] - lower.get_top()[1]
            if gap < 0.06:
                raise ValueError(
                    f"End card rows overlap by {gap:+.2f} units. Move them "
                    "apart or shorten the copy."
                )
        if rows[-1].get_bottom()[1] < FLOOR:
            raise ValueError(
                "The end card's last row runs into the Shorts UI band.")

    _beat_name = "(before the first beat)"

    @contextmanager
    def beat(self, name):
        self._beat_name = name
        with super().beat(name) as timer:
            yield timer
