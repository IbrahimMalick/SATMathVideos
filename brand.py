"""House style: palette, fonts, size constants, spacing scale.

Single source of truth. Scenes and components import from here and never
define their own colour literals — verify.py enforces this.
"""

# ---------------------------------------------------------------- palette

CREAM      = "#F4F0E6"   # background, always
CHARCOAL   = "#2E2C2A"   # axes, primary text, equations
SLATE      = "#4A6D8C"   # primary curves, functions, main subject
TERRACOTTA = "#C1663F"   # the one thing the viewer should look at
SAGE       = "#6B8F71"   # confirmation, correct answers, underline sweeps
GREY       = "#8A857E"   # margin annotations, de-emphasized material

PALETTE = [CREAM, CHARCOAL, SLATE, TERRACOTTA, SAGE, GREY]

# ---------------------------------------------------------------- fonts

SERIF_FONT = "DejaVu Serif"   # body and labels (Pango Text)
MONO_FONT  = "DejaVu Sans Mono"   # margin annotations

# Manim font_size values. The floor of MARGIN_SIZE keeps rendered text at or
# above 28px at 1080p — the mobile legibility gate. Do not go below it.
TITLE_SIZE  = 44
BODY_SIZE   = 36
LABEL_SIZE  = 32
MARGIN_SIZE = 28

# MathTex font_size. LaTeX glyphs render slightly smaller than Pango at the
# same nominal size, so the equation default sits higher than BODY_SIZE.
EQUATION_SIZE = 40

# For the one equation a section is about — the hero of the frame.
DISPLAY_SIZE = 56

# ------------------------------------------------- the client's ad identity

# The Digital Tutor's advertising palette, sampled from the client's own
# ad template rather than chosen here. It is NOT the course house style
# and must never appear in a lecture scene: the palette above is what
# this repo is about, and section 2 of CLAUDE.md is about that palette.
#
# It lives in brand.py anyway for two reasons. verify.py enforces that
# every colour literal under scenes/ and components/ is imported from
# here, and that check is worth more than the tidiness of keeping this
# out; and when he changes his brand there is one place to change it.
AD_NAVY = "#0A1320"    # the caption band, and the end card
AD_DEEP = "#0B1F2F"    # the decorative arc, a shade off the navy
AD_TEAL = "#49E8C8"    # the rule under the picture, and the kickers
AD_PAPER = "#FFFFFF"   # headlines, and the panel the phone number sits on
AD_MUTED = "#8FA3B5"   # the small print under a headline

AD_FONT = "Inter"          # his headline face, and it is installed here

# ---------------------------------------------------------------- spacing

GAP_SM = 0.25   # scene units; tight spacing within a group
GAP_MD = 0.5    # between related elements
GAP_LG = 1.0    # between distinct regions of the frame

# ---------------------------------------------------------------- pacing

MIN_RUN_TIME = 0.5   # the calm-pacing floor; beat timers clamp to this

# ---------------------------------------------------------------- text factories


def serif(text, size=BODY_SIZE, color=CHARCOAL):
    from manim import Text

    return Text(text, font=SERIF_FONT, font_size=size, color=color)


def sans(text, size=BODY_SIZE, color=CHARCOAL, bold=False):
    """Inter, for the client's ad only. Lectures use serif() and mono()."""
    from manim import Text

    # Weight as a Pango weight, not as a family name: manim only knows
    # "Inter" as a family and warns loudly on every render if handed
    # "Inter SemiBold", even though Pango then resolves it anyway.
    return Text(text, font=AD_FONT, weight="SEMIBOLD" if bold else "NORMAL",
                font_size=size, color=color)


def mono(text, size=MARGIN_SIZE, color=GREY):
    from manim import Text

    return Text(text, font=MONO_FONT, font_size=size, color=color)
