"""Optimisation archetype: a rectangle inscribed under a curve.

The A Level optimisation question that keeps coming back — a shape sits
under a curve, one dimension is called x, and the area is maximised by
differentiating. The picture is the same every time, so it is parameterised
here: a new item is a new curve and a new half-width passed in, never a new
drawing.

Sized for the portrait Shorts frame (4.5 x 8 units). Portrait is 1.78x
denser than the lecture frame, so the floor that matters, 28px at
1080x1920, works out at a nominal ~15.8 for Pango text and ~22.5 for
MathTex, which sets about 1.43x smaller at the same nominal size.

Every position is read off the axes at call time. The rectangle changes
shape when the optimum is found, so a label placed from coordinates
captured at construction would stay where the old rectangle used to be.
"""

from manim import (
    Axes,
    Dot,
    Line,
    MathTex,
    Polygon,
    VGroup,
    DOWN,
    RIGHT,
)

from brand import (
    CHARCOAL,
    GAP_SM,
    GREY,
    SLATE,
)

PORTRAIT_SAFE = 4.0

# Nominal MathTex size at the 28px portrait floor, with a little headroom.
MATH_FLOOR = 24


class CurveRectangle(VGroup):
    """A curve, and a rectangle standing on the x-axis beneath it.

    ``curve`` is the function, ``root`` the positive x where it meets the
    axis, and ``half_width`` the rectangle's starting half-width. The
    rectangle is centred on the y-axis, which is what lets half its width
    be the single variable the whole question turns on.
    """

    def __init__(self, curve, root, half_width, width=3.4, height=2.1,
                 curve_color=SLATE, box_color=CHARCOAL, pad=0.3,
                 fill_opacity=0.1, stroke=3.5):
        super().__init__()
        self.curve_fn = curve
        self.root = root
        self.half_width = half_width
        self.box_color = box_color
        self.fill_opacity = fill_opacity
        self.stroke = stroke

        top = curve(0)
        self.axes = Axes(
            x_range=[-root - pad, root + pad, 1],
            y_range=[0, top * 1.15, top],
            x_length=width,
            y_length=height,
            axis_config={
                "include_ticks": False,
                "include_numbers": False,
                "color": GREY,
                "stroke_width": 2,
                "include_tip": True,
                "tip_width": 0.13,
                "tip_height": 0.13,
            },
        )
        self.graph = self.axes.plot(curve, x_range=[-root, root],
                                    color=curve_color, stroke_width=4)
        self.rect = self.rectangle(half_width)
        self.corner = self.dot(half_width)
        self.add(self.axes, self.graph, self.rect, self.corner)

    # ----------------------------------------------------------- the shape

    def rectangle(self, half_width, color=None):
        """The rectangle at this half-width, built from where the axes are."""
        top = self.curve_fn(half_width)
        corners = [
            self.axes.c2p(-half_width, 0),
            self.axes.c2p(half_width, 0),
            self.axes.c2p(half_width, top),
            self.axes.c2p(-half_width, top),
        ]
        box = Polygon(*corners, color=color or self.box_color,
                      stroke_width=self.stroke)
        box.set_fill(SLATE, opacity=self.fill_opacity)
        return box

    def dot(self, half_width, color=None, radius=0.045):
        """The corner that rides along the curve."""
        return Dot(self.axes.c2p(half_width, self.curve_fn(half_width)),
                   color=color or self.box_color, radius=radius)

    def grown_to(self, half_width, color=None):
        """The rectangle and corner at a new half-width. For Transform."""
        return self.rectangle(half_width, color), self.dot(half_width, color)

    # ---------------------------------------------------------- annotation

    def tick(self, x, color=GREY, length=0.09, stroke=2):
        """A short mark on the x-axis, so a labelled distance has an end."""
        foot = self.axes.c2p(x, 0)
        return Line(foot + DOWN * length, foot + DOWN * -length,
                    color=color, stroke_width=stroke)

    def below(self, tex, at_x, level=0, size=MATH_FLOOR, color=CHARCOAL,
              gap=0.2, pitch=0.3):
        """A label under the axis, centred on an x value.

        ``level`` stacks a second row underneath the first, which is how
        the half-width and the full width end up legible at once.
        """
        label = MathTex(tex, font_size=size, color=color)
        label.move_to(self.axes.c2p(at_x, 0) + DOWN * (gap + pitch * level))
        return label

    def inside(self, tex, at_x=0.0, size=MATH_FLOOR, color=CHARCOAL,
               lift=0.45):
        """A label within the rectangle — the height, written in the shape.

        Inside rather than alongside because the portrait frame has no room
        to the right of the box without the label running into the margin.
        ``at_x`` moves it off centre: the rectangle straddles the y-axis, so
        a label in the middle of it has the axis drawn straight through the
        glyphs.
        """
        label = MathTex(tex, font_size=size, color=color)
        middle = self.rect.get_center()[1]
        top = self.rect.get_top()[1]
        label.move_to([self.axes.c2p(at_x, 0)[0],
                       middle + (top - middle) * lift, 0])
        return label

    def beside_curve(self, tex, size=MATH_FLOOR, color=SLATE,
                     buff=GAP_SM * 0.6):
        """The curve's equation, parked off its left shoulder."""
        label = MathTex(tex, font_size=size, color=color)
        label.next_to(self.graph.get_left(), RIGHT, buff=buff)
        label.align_to(self.axes, DOWN).shift(DOWN * 0)
        return label


def measure():
    """Report whether the archetype fits the portrait frame at full size.

    Run as ``python -m components.optimisation`` from the repo root. It
    renders nothing: it builds the figure the Short uses and says whether
    it sits inside the frame with its labels above the legibility floor.
    """
    from manim import config

    config.frame_height = 8.0
    config.frame_width = 4.5
    half_w, half_h = config.frame_width / 2, config.frame_height / 2
    density = (1080 / config.frame_width) / 135.0

    figure = CurveRectangle(lambda x: 12 - x * x, 12 ** 0.5, 3.0)
    parts = {
        "figure": figure,
        "x label": figure.below("x", 1.5),
        "2x label": figure.below("2x", 0, level=1),
        "height": figure.inside("12 - x^2"),
    }
    print(f"frame {config.frame_width} x {config.frame_height}, "
          f"{density:.2f}x the lecture density")
    for name, part in parts.items():
        left, right = part.get_left()[0], part.get_right()[0]
        bottom, top = part.get_bottom()[1], part.get_top()[1]
        ok = (left > -half_w and right < half_w
              and bottom > -half_h and top < half_h)
        print(f"{name:9} x [{left:6.2f}, {right:6.2f}]  "
              f"y [{bottom:6.2f}, {top:6.2f}]  {'ok' if ok else 'OFF FRAME'}")

    # MathTex sets about 1.43x smaller than Pango at the same nominal size.
    rendered = MATH_FLOOR / 1.43 * density
    print(f"MathTex at {MATH_FLOOR} renders {rendered:.1f}px  "
          f"{'ok' if rendered >= 28 else 'BELOW THE 28px FLOOR'}")

    # The rectangle has to be able to grow without leaving the axes.
    for h in (1.0, 2.0, 3.0):
        box, _ = figure.grown_to(h)
        inside = (box.get_left()[0] > figure.axes.get_left()[0]
                  and box.get_right()[0] < figure.axes.get_right()[0])
        print(f"rectangle at half-width {h}: "
              f"{'inside the axes' if inside else 'OUTSIDE THE AXES'}")


if __name__ == "__main__":
    measure()
