"""The client's own ad template, rebuilt — and carrying the offer.

His second ad fixed the typography of his first: nothing clipped, nothing
wrapping, a phone number actually on screen. What it lost was the selling.
Three things his voice says and his screen never shows:

  * the price. At 35.5-38.2s the voice says "$100 a month, $600 in all"
    and the band reads "Practice with feedback that moves you forward".
  * the start date, spoken at 38.2-41.8s over the exam-date card.
  * "Not $200 an hour", the comparison that makes $100 a month feel
    cheap. Without it the price has nothing to be cheap against.

His instructor's name and PhD go unshown too.

So this is his design holding my copy. The geometry and the palette were
measured off his own export rather than guessed:

  picture       0 to 736 px of 1080      teal rule  736 to 748 px
  caption band  748 to 1080 px           left margin        85 px
  kicker centre 793 px                   headline centre   860 px
  navy #0A1320  teal #49E8C8             headline Inter, nominal 33

Two deliberate departures, both worth saying out loud:

  * his kicker measures about nominal 16, which renders near 12px of cap
    height. That is under the 28px mobile floor this repo gates every
    render on, so the kicker here is nominal 28 and reads chunkier than
    his. It is the one number in this file that is not his.
  * his band carries a kicker and one headline and leaves roughly 140px
    of empty navy beneath. That space is where the offer goes.

``measure()`` checks every card against the frame and against the band.
"""

from manim import (
    Annulus,
    Dot,
    Rectangle,
    RoundedRectangle,
    VGroup,
    DOWN,
    RIGHT,
)

from brand import (
    AD_DEEP,
    AD_MUTED,
    AD_NAVY,
    AD_PAPER,
    AD_TEAL,
    GAP_SM,
    sans,
)

# -------------------------------------------------------------- geometry

PPU = 135.0                      # pixels per frame unit at 1920x1080
FRAME_W, FRAME_H = 14.22, 8.0

WINDOW_PX = 736                  # the picture, cropped from the top of his
RULE_PX = 12                     # footage, which also loses his old captions

WINDOW_BOTTOM = FRAME_H / 2 - WINDOW_PX / PPU          # -1.452
RULE_BOTTOM = WINDOW_BOTTOM - RULE_PX / PPU            # -1.541
BAND_BOTTOM = -FRAME_H / 2

MARGIN_X = 85 / PPU                                    # 0.63
LEFT_EDGE = -FRAME_W / 2 + MARGIN_X                    # -6.48
SAFE = FRAME_W - 2 * MARGIN_X                          # 12.96

KICKER_Y = FRAME_H / 2 - 793 / PPU                     # -1.874
HEADLINE_Y = FRAME_H / 2 - 860 / PPU                   # -2.370
DETAIL_Y = FRAME_H / 2 - 938 / PPU                     # -2.948
DETAIL_STEP = 0.46

KICKER = 28          # his is ~16; 28 is the floor this repo renders to
HEADLINE = 33
DETAIL = 30

DOT = 0.045          # the teal dot that opens every kicker


# ----------------------------------------------------------------- copy

# (beat, kicker, headline, details to add). A headline starts a new card
# and clears the details under it; None keeps what is already up.
CLIENT_SCRIPT = [
    ("stuck", "AP COMPUTER SCIENCE A", "Gets it in class.", []),
    ("alone", None, None, ["Freezes on the homework."]),

    ("first_ap", "WHY IT MATTERS", "First AP in the family.", []),
    ("opens", None, None, ["Computer Science opens engineering."]),

    ("structure", "WHAT PARENTS ASK FOR", "Structure, not another guess.", []),
    # Both numbers are his. Stated together, because a viewer watching
    # muted never hears the $200 and the line has to carry the whole
    # comparison on its own -- which is the comparison his voiceover sets
    # up and his captions drop.
    ("not_200", None, None, ["At $200 an hour, $600 buys three hours."]),

    ("capped", "SMALL-GROUP CLASSES", "Live lessons, capped at 10 students.",
     []),
    ("tutor", None, None, ["Dr. Ibrahim Malik, PhD"]),
    ("two_hours", None, None, ["Two hours a week, live online."]),

    ("trace", "HOW IT IS TAUGHT", "Tracing, not telling.", []),
    ("second_pass", None, None, ["“What is i on the second pass?”"]),

    ("topics", "WHAT YOU COVER", "Java. Code tracing. Arrays. FRQs.", []),
    ("frq", None, None, ["Free-response questions, one at a time."]),

    ("one_line", "EXPERT FEEDBACK",
     "One line at a time, until she can do it alone.", []),
    ("it_runs", "THE MOMENT IT LANDS", "It runs.", []),

    ("exam_day", "AP COMPUTER SCIENCE A EXAM", "Wednesday, May 12, 2027", []),
    ("a_plan", None, None, ["25 weeks from the first lesson."]),

    ("price", "THE PRICE", "$100 / month · $600 in all", []),
    ("when", None, None,
     ["Evenings or weekends · starts November 16"]),
]

# ------------------------------------------------------------- end card

BRAND_CHIP = "THE DIGITAL TUTOR"
END_KICKER = "AP COMPUTER SCIENCE A · SUPPORT COHORT"
END_PHONE = "646-704-4513"
END_URL = "ap.thedigitaltutor.net"
END_FACTS = [
    "Live online · max 10 students · two hours a week",
    "$100 / month · $600 in all · starts November 16",
]
END_EXAM = "AP Exam  ·  Wednesday, May 12, 2027"


def fit(mobject, width=SAFE, what="this line"):
    if mobject.width > width:
        raise ValueError(
            f"{what} is {mobject.width:.2f} units wide, over the "
            f"{width:.2f} the band allows. Shorten the copy rather than "
            "letting it wrap, which is what went wrong the first time."
        )
    return mobject


def teal_rule():
    """The line between the picture and the band."""
    rule = Rectangle(width=FRAME_W * 1.02, height=RULE_PX / PPU,
                     stroke_width=0)
    rule.set_fill(AD_TEAL, opacity=1)
    rule.move_to([0, (WINDOW_BOTTOM + RULE_BOTTOM) / 2, 0])
    rule.full_bleed = True
    return rule


def kicker(text):
    """A teal dot and a line of small caps, left-aligned at the margin."""
    dot = Dot(radius=DOT, color=AD_TEAL)
    label = fit(sans(text.upper(), KICKER, AD_TEAL, bold=True),
                SAFE - 0.4, f"the kicker {text!r}")
    group = VGroup(dot, label).arrange(RIGHT, buff=GAP_SM * 0.75)
    group.move_to([LEFT_EDGE + group.width / 2, KICKER_Y, 0])
    return group


def headline(text):
    body = fit(sans(text, HEADLINE, AD_PAPER, bold=True), SAFE,
               f"the headline {text!r}")
    body.move_to([LEFT_EDGE + body.width / 2, HEADLINE_Y, 0])
    return body


def detail(text, index=0):
    body = fit(sans(text, DETAIL, AD_MUTED), SAFE, f"the detail {text!r}")
    body.move_to([LEFT_EDGE + body.width / 2,
                  DETAIL_Y - index * DETAIL_STEP, 0])
    return body


def chip(text=BRAND_CHIP, size=KICKER):
    label = sans(text.upper(), size, AD_TEAL, bold=True)
    back = RoundedRectangle(width=label.width + GAP_SM * 2.2,
                            height=label.height + GAP_SM * 1.6,
                            corner_radius=0.12, stroke_width=0)
    back.set_fill(AD_DEEP, opacity=1)
    back.move_to(label)
    return VGroup(back, label)


def panel(lines, size=52, width=9.2, pad=GAP_SM * 2.4):
    """The white card his phone number and URL sit on."""
    body = VGroup(*[sans(line, size, AD_NAVY) for line in lines])
    body.arrange(DOWN, buff=GAP_SM * 1.1)
    if body.width > width - 2 * pad:
        raise ValueError(
            f"The panel's contents run {body.width:.2f} units inside a "
            f"{width:.2f}-unit card.")
    back = RoundedRectangle(width=width, height=body.height + 2 * pad,
                            corner_radius=0.14, stroke_width=0)
    back.set_fill(AD_PAPER, opacity=1)
    back.move_to(body)
    group = VGroup(back, body)
    group.body, group.back = body, back
    return group


def arc():
    """The ring that bleeds off his top-right corner."""
    ring = Annulus(inner_radius=1.45, outer_radius=2.05, color=AD_DEEP,
                   stroke_width=0)
    ring.set_fill(AD_DEEP, opacity=1)
    ring.move_to([FRAME_W / 2 - 0.35, FRAME_H / 2 - 0.2, 0])
    ring.full_bleed = True
    return ring


def backdrop():
    """Navy over everything, for the end card."""
    card = Rectangle(width=FRAME_W * 1.02, height=FRAME_H * 1.02,
                     stroke_width=0)
    card.set_fill(AD_NAVY, opacity=1)
    card.full_bleed = True
    return card


def states():
    """CLIENT_SCRIPT with its keep-what-is-there shorthand resolved."""
    out, k, h, d = [], None, None, []
    for beat, new_k, new_h, add in CLIENT_SCRIPT:
        if new_h is not None:
            k, h, d = new_k or k, new_h, []
        if new_k is not None:
            k = new_k
        d = d + list(add)
        out.append((beat, k, h, list(d)))
    return out


def measure():
    """Check every card fits the band, and nothing reaches the frame edge.

    Run as ``python -m components.ad_client`` from the repo root.
    """
    print(f"window bottom {WINDOW_BOTTOM:+.3f}   rule bottom "
          f"{RULE_BOTTOM:+.3f}   band bottom {BAND_BOTTOM:+.3f}")
    worst = 0.0
    for beat, k, h, details in states():
        rows = [kicker(k), headline(h)]
        rows += [detail(text, i) for i, text in enumerate(details)]
        low = min(row.get_bottom()[1] for row in rows)
        high = max(row.get_top()[1] for row in rows)
        right = max(row.get_right()[0] for row in rows)
        clear = high < RULE_BOTTOM - 0.02 and low > BAND_BOTTOM + 0.08
        worst = min(worst, low) if low < 0 else worst
        print(f"{beat:12} {len(details)} detail(s)  "
              f"y [{low:6.2f}, {high:6.2f}]  right {right:6.2f}  "
              f"{'ok' if clear and right < FRAME_W / 2 else 'DOES NOT FIT'}")
    print(f"lowest line sits at y={worst:.2f}, band floor "
          f"{BAND_BOTTOM:.2f}")

    card = panel([END_PHONE, END_URL])
    print(f"end panel {card.width:.2f} x {card.height:.2f}")


if __name__ == "__main__":
    measure()
