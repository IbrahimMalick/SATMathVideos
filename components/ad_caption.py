"""Captions that sit over footage, and the copy for the cohort ad.

The ad this replaces failed on four counts, all of them in the text layer
and all of them visible in a single still: the block was anchored past the
left edge so the first letter of every line was sliced off, it overflowed
downward so second lines were cut through the middle, it wrapped
mid-phrase, and the end card put a URL across a busy calendar while the
phone number the voice reads out never appeared at all.

So the rules here are the opposite of each of those:

  * Nothing is positioned by eye. A line is laid out from the frame's own
    edges with a margin that is declared once, and ``measure()`` checks
    the result against the frame rather than trusting it.
  * A line never wraps. ``CaptionLine`` raises if its text will not fit
    the width it is given, so an overlong line fails the build instead of
    folding into the footage. Line breaks are in the copy below, chosen at
    sense boundaries.
  * Every line carries its own pill, so white type stays legible over a
    lamp, a window or a white fridge door, and so a block can grow line by
    line without the backing resizing under it.
  * The call to action is not over footage at all. It is the house card.

The copy is the client's wherever his was good. It is re-broken, and the
end card gains the phone number his was missing.
"""

from manim import RoundedRectangle, VGroup, DOWN, LEFT

from brand import (
    CHARCOAL,
    CREAM,
    GAP_SM,
    SAGE,
    TERRACOTTA,
    serif,
)

# ---------------------------------------------------------------- the copy

# Each entry is a beat name and what the frame says once that beat has
# played. "add" grows the block that is already up; "set" replaces it.
# Accent colours a single line, and is used three times in fifty seconds:
# the price objection, the moment the program runs, and the price itself.
SCRIPT = [
    ("stuck", "set", ["Gets it in class."]),
    ("alone", "add", ["Freezes on the homework."]),

    ("first_ap", "set", ["First AP in the family."]),
    ("opens", "add", ["This one opens engineering."]),

    ("structure", "set", ["Structure, not guesswork."]),
    ("not_200", "add", ["Not $200 an hour."]),

    ("capped", "set", ["A live group, capped at 10."]),
    ("tutor", "add", ["Dr. Ibrahim Malik, PhD"]),
    ("two_hours", "add", ["Two hours a week."]),

    ("trace", "set", ["Tracing, not telling."]),
    ("second_pass", "add", ["\u201cWhat is i on pass two?\u201d"]),

    ("topics", "set", ["Java \u00b7 Code tracing \u00b7 Arrays"]),
    ("frq", "add", ["Free-response questions"]),

    ("one_line", "set", ["One line at a time,",
                         "until she can do it alone."]),

    ("it_runs", "set", ["It runs."]),

    ("exam_day", "set", ["AP exam: May 12, 2027"]),
    ("a_plan", "add", ["Now there is a plan."]),

    ("price", "set", ["$100 / month \u00b7 $600 in all"]),
    ("when", "add", ["Evenings or weekends.",
                     "Starts November 16."]),
]

# Which lines are coloured rather than cream, by their text. Sage is the
# house colour for a thing confirmed, and on the dark pills of the
# landscape cut it reads clearly.
ACCENTS = {
    "Not $200 an hour.": SAGE,
    "It runs.": SAGE,
    "$100 / month · $600 in all": SAGE,
}

# The end card, which is the house card and not an overlay on footage.
BRAND = "The Digital Tutor"
COHORT = "AP Computer Science A · Support Cohort"
FACTS = [
    "Live online · max 10 students · two hours a week",
    "$100 / month · $600 in all · starts November 16",
]
URL = "ap.thedigitaltutor.net"
# Heard as "646 704 4513" on the unchunked transcript of the client's own
# voiceover, and as "704 4513" on the chunked one. Confirm before airing:
# it is the single thing in the ad that cannot be wrong.
PHONE = "or call 646 704 4513"
EXAM = "AP exam: Wednesday, May 12, 2027"


class CaptionLine(VGroup):
    """One line of caption on its own pill.

    A pill per line rather than one behind the block, because a block that
    grows line by line would otherwise have to resize its backing under
    the text already on screen, and because a pill that hugs its own line
    leaves more of the picture showing.
    """

    def __init__(self, text, size, width, color=CREAM, pill=CHARCOAL,
                 opacity=0.76, pad=0.24, radius=0.1):
        super().__init__()
        body = serif(text, size, color)
        if body.width > width:
            raise ValueError(
                f"Caption line {text!r} is {body.width:.2f} units wide at "
                f"size {size}, over the {width:.2f} it is given. Break it in "
                "the copy rather than letting it wrap into the footage."
            )
        back = RoundedRectangle(
            width=body.width + 2 * pad, height=body.height + 1.5 * pad,
            corner_radius=radius, stroke_width=0)
        back.set_fill(pill, opacity=opacity)
        back.move_to(body)
        self.body, self.back = body, back
        self.add(back, body)


def caption_block(lines, size, width, accents=None, **kwargs):
    """Several caption lines, stacked and left-aligned on their pills."""
    accents = accents or {}
    block = VGroup()
    for text in lines:
        colour = accents.get(text, CREAM)
        block.add(CaptionLine(text, size, width, color=colour, **kwargs))
    block.arrange(DOWN, buff=GAP_SM * 0.5, aligned_edge=LEFT)
    return block


def states():
    """The caption copy as (beat, lines-on-screen-after-this-beat).

    Resolves the add/set shorthand once, so a scene never has to track
    what was up a beat ago.
    """
    out, current = [], []
    for beat, mode, lines in SCRIPT:
        current = (list(lines) if mode == "set" else current + list(lines))
        out.append((beat, list(current)))
    return out


# ---------------------------------------------------- the copy, re-broken

# Vertical is not a crop of horizontal, and neither is its copy. A 4.5-unit
# frame takes about 22 characters on a line at a size a phone can read, so
# lines that were comfortable in the landscape cut have to break again or
# lose a word. Kept as its own table rather than wrapped automatically,
# because where a line breaks is a writing decision.
SCRIPT_PORTRAIT = [
    ("stuck", "set", ["Gets it in class."]),
    ("alone", "add", ["Freezes on homework."]),

    ("first_ap", "set", ["First AP in the family."]),
    ("opens", "add", ["It opens engineering."]),

    ("structure", "set", ["Structure,", "not guesswork."]),
    ("not_200", "add", ["Not $200 an hour."]),

    ("capped", "set", ["A group capped at 10."]),
    ("tutor", "add", ["Dr. Ibrahim Malik, PhD"]),
    ("two_hours", "add", ["Two hours a week."]),

    ("trace", "set", ["Tracing, not telling."]),
    ("second_pass", "add", ["\u201cWhat is i", "on pass two?\u201d"]),

    ("topics", "set", ["Java \u00b7 Code tracing"]),
    ("frq", "add", ["Arrays \u00b7 Free response"]),

    ("one_line", "set", ["One line at a time,", "until she gets it."]),

    ("it_runs", "set", ["It runs."]),

    ("exam_day", "set", ["AP exam: May 12, 2027"]),
    ("a_plan", "add", ["Now there is a plan."]),

    ("price", "set", ["$100/mo \u00b7 $600 in all"]),
    ("when", "add", ["Evenings or weekends.", "Starts November 16."]),
]

# The end card, broken for the narrow frame.
COHORT_PORTRAIT = ["AP Computer Science A", "Support Cohort"]
FACTS_PORTRAIT = [
    "Live online \u00b7 max 10 students",
    "Two hours a week",
    "$100 / month \u00b7 $600 in all",
    "Starts November 16",
]


# The vertical cut puts the same lines on cream instead, where sage is
# too close in tone to the paper to carry an accent. Terracotta is the
# house colour for "look here" and it is what the eye needs on cream.
# Still one accented line on screen at a time, which is the rule that
# matters.
ACCENTS_PORTRAIT = {text: TERRACOTTA for text in (
    "Not $200 an hour.",
    "It runs.",
    "$100/mo \u00b7 $600 in all",
)}


def plain_block(lines, size, width, accents=None, color=CHARCOAL,
                buff=GAP_SM * 0.9):
    """Caption lines with no pill behind them.

    The vertical cut puts its words on the house cream rather than over
    the picture, and a dark pill on cream is a bruise. Same raise-rather-
    than-wrap contract as CaptionLine.
    """
    accents = accents or {}
    block = VGroup()
    for text in lines:
        body = serif(text, size, accents.get(text, color))
        if body.width > width:
            raise ValueError(
                f"Caption line {text!r} is {body.width:.2f} units wide at "
                f"size {size}, over the {width:.2f} it is given. Break it in "
                "the copy."
            )
        block.add(body)
    block.arrange(DOWN, buff=buff, aligned_edge=LEFT)
    return block


def states_portrait():
    """SCRIPT_PORTRAIT with its add/set shorthand resolved."""
    out, current = [], []
    for beat, mode, lines in SCRIPT_PORTRAIT:
        current = (list(lines) if mode == "set" else current + list(lines))
        out.append((beat, list(current)))
    return out


def measure(frame_width=14.22, frame_height=8.0, size=40, width=8.9,
            margin=0.95, floor=-3.3):
    """Check every caption fits, and where the tallest block reaches.

    Run as ``python -m components.ad_caption`` from the repo root.
    """
    half_w, half_h = frame_width / 2, frame_height / 2
    tallest, worst = 0.0, None
    for beat, lines in states():
        block = caption_block(lines, size, width, ACCENTS)
        block.move_to([-half_w + margin + block.width / 2,
                       floor + block.height / 2, 0])
        fits = (block.get_right()[0] < half_w - margin * 0.6
                and block.get_top()[1] < half_h)
        if block.height > tallest:
            tallest, worst = block.height, beat
        print(f"{beat:12} {len(lines)} line(s)  "
              f"x [{block.get_left()[0]:6.2f}, {block.get_right()[0]:6.2f}]  "
              f"y [{block.get_bottom()[1]:6.2f}, {block.get_top()[1]:6.2f}]  "
              f"{'ok' if fits else 'OFF FRAME'}")
    print(f"tallest block is {worst!r} at {tallest:.2f} units")


if __name__ == "__main__":
    measure()
