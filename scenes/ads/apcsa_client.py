"""The AP CSA cohort ad in the client's own template, carrying the offer.

His design, my copy. The geometry, the palette and the type sizes were
measured off his second export rather than guessed; see
components/ad_client.py for the numbers and for the two places this
departs from him on purpose.

What this fixes is not the typography, which he had already solved, but
what the typography was carrying. His band never shows the price, the
start date, the instructor's name, or the "not $200 an hour" comparison,
all four of which his own voice says. Here each one lands on the beat
that says it, because the beats come from that voiceover.

The picture is his footage cropped to the top 736 rows, which is what his
template's window wants anyway and which has the side effect of removing
his first ad's burned-in captions entirely: they start at row 795.

    python -m manim render -t -r 1920,1080 --fps 30 \\
        scenes/ads/apcsa_client.py ApcsaClient
    python build/ad_composite.py --base <the client's mp4> --cut client

Timing: timings/ads.apcsa_client.json
"""

from contextlib import contextmanager

from manim import (
    AnimationGroup,
    FadeIn,
    FadeOut,
    VGroup,
    DOWN,
    config,
)

from brand import (
    AD_MUTED,
    AD_PAPER,
    AD_TEAL,
    GAP_SM,
    sans,
)
from components.ad_client import (
    BAND_BOTTOM,
    DETAIL,
    END_EXAM,
    END_FACTS,
    END_KICKER,
    END_PHONE,
    END_URL,
    KICKER,
    LEFT_EDGE,
    RULE_BOTTOM,
    SAFE,
    arc,
    backdrop,
    chip,
    detail,
    fit,
    headline,
    kicker,
    panel,
    states,
    teal_rule,
)
from scenes.base import SATScene

FACT_SIZE = DETAIL
EXAM_SIZE = KICKER


class ApcsaClient(SATScene):
    scene_id = "ads.apcsa_client"

    def setup(self):
        super().setup()
        # Everything here goes over his picture, so the background has to
        # carry alpha rather than the house cream.
        self.camera.background_opacity = 0
        self.camera.init_background()

    def construct(self):
        self.rule = teal_rule()
        self.add(self.rule)
        self.card = None          # (kicker, headline, [details]) on screen
        self.cards()
        self.end_card()

    # ------------------------------------------------------------- captions

    def cards(self):
        previous = None
        for beat, k, h, details in states():
            with self.beat(beat) as t:
                rows = VGroup(kicker(k), headline(h),
                              *[detail(text, i)
                                for i, text in enumerate(details)])
                self.guard_band(rows, beat)

                if previous is None or previous[1] != h:
                    # A new headline is a new card: out, then in, inside
                    # one play. A plain crossfade leaves both cards at
                    # half strength on top of each other, and the
                    # shortest beat here is 0.84s.
                    arriving = AnimationGroup(*[FadeIn(row) for row in rows])
                    if self.card is not None:
                        moves = [AnimationGroup(
                            AnimationGroup(
                                *[FadeOut(row) for row in self.card]),
                            arriving, lag_ratio=0.55)]
                    else:
                        moves = [arriving]
                    self.card = rows
                else:
                    # Only the detail lines grew. The kicker and headline
                    # already on screen stay exactly where they are, so
                    # nothing above the new line moves.
                    kept = len(self.card)
                    moves = [FadeIn(row) for row in rows[kept:]]
                    self.card = VGroup(*self.card, *rows[kept:])

                self.play(*moves, run_time=t.fill(0.42))
                previous = (k, h, details)
                t.hold()

    # ------------------------------------------------------------- end card

    def end_card(self):
        sheet = backdrop()
        ring = arc()
        mark = chip()
        mark.move_to([LEFT_EDGE + mark.width / 2, 2.95, 0])

        head = fit(sans(END_KICKER, KICKER, AD_TEAL, bold=True), SAFE,
                   "the end card kicker")
        head.move_to([LEFT_EDGE + head.width / 2, 2.2, 0])

        # URL above number, against his order: the voice gives the URL
        # first and revealing the lower line before the upper one reads
        # backwards.
        card = panel([END_URL, END_PHONE])
        card.move_to([0, 0.35, 0])
        url_line, phone_line = card.body[0], card.body[1]
        phone_line.set_opacity(0)

        facts = VGroup(*[fit(sans(line, FACT_SIZE, AD_MUTED), SAFE, line)
                         for line in END_FACTS])
        facts.arrange(DOWN, buff=GAP_SM * 1.2)
        facts.move_to([0, -1.8, 0])

        exam = fit(sans(END_EXAM, EXAM_SIZE, AD_MUTED), SAFE,
                   "the end card exam line")
        exam.move_to([0, -2.78, 0])

        self.guard_card([mark, head, card, facts, exam])

        with self.beat("brand") as t:
            self.play(*[FadeOut(row) for row in self.card],
                      FadeOut(self.rule), FadeIn(sheet), FadeIn(ring),
                      FadeIn(mark), run_time=t.fill(0.5))
            self.card = VGroup()
            t.hold()

        with self.beat("cohort") as t:
            self.play(FadeIn(head), FadeIn(facts), run_time=t.fill(0.35))
            t.hold()

        with self.beat("url") as t:
            self.play(FadeIn(card.back), FadeIn(url_line),
                      run_time=t.fill(0.3))
            t.hold()

        with self.beat("phone") as t:
            phone_line.set_opacity(1)
            self.play(FadeIn(phone_line), FadeIn(exam), run_time=t.fill(0.26))
            t.hold()

    # --------------------------------------------------------------- guards

    @staticmethod
    def guard_card(rows):
        """Nothing on the end card may touch the row above it.

        His first ad lost its phone number off the bottom of a card. This
        is the check that says so before a frame is rendered.
        """
        for upper, lower in zip(rows, rows[1:]):
            gap = upper.get_bottom()[1] - lower.get_top()[1]
            if gap < 0.1:
                raise ValueError(
                    f"End card rows overlap by {gap:+.2f} units. Move them "
                    "apart or shorten the copy.")
        if rows[-1].get_bottom()[1] < -config.frame_height / 2 + 0.3:
            raise ValueError("The end card's last row runs off the bottom.")

    def guard_band(self, rows, beat):
        low = min(row.get_bottom()[1] for row in rows)
        high = max(row.get_top()[1] for row in rows)
        if high > RULE_BOTTOM - 0.02 or low < BAND_BOTTOM + 0.08:
            raise ValueError(
                f"Beat '{beat}': the card runs from {low:.2f} to {high:.2f}, "
                f"outside the band between {BAND_BOTTOM:.2f} and "
                f"{RULE_BOTTOM:.2f}.")

    _beat_name = "(before the first beat)"

    @contextmanager
    def beat(self, name):
        self._beat_name = name
        with super().beat(name) as timer:
            yield timer
