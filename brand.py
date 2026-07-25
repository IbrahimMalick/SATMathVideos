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

# ---------------------------------------------------------------- spacing

GAP_SM = 0.25   # scene units; tight spacing within a group
GAP_MD = 0.5    # between related elements
GAP_LG = 1.0    # between distinct regions of the frame

# ---------------------------------------------------------------- pacing

MIN_RUN_TIME = 0.5   # the calm-pacing floor; beat timers clamp to this
