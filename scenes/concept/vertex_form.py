"""Concept explainer: vertex form of a quadratic.

Narration script: scripts/L03-vertex-form.md
Beats: axes -> curve -> equation -> vertex
"""

from manim import (
    Axes,
    Create,
    Dot,
    MathTex,
    Text,
    VGroup,
    Write,
    DOWN,
    LEFT,
    RIGHT,
    UP,
)

from brand import (
    CHARCOAL,
    GREY,
    MARGIN_SIZE,
    MONO_FONT,
    SLATE,
    TERRACOTTA,
    GAP_MD,
    GAP_SM,
    EQUATION_SIZE,
)
from scenes.base import SATScene

# The parabola we draw: y = 0.5(x - 1)^2 - 2, vertex at (1, -2).
H, K, A = 1, -2, 0.5


class VertexForm(SATScene):
    scene_id = "concept.vertex_form"

    def construct(self):
        margin_note = Text(
            "L03 · vertex form", font=MONO_FONT, font_size=MARGIN_SIZE, color=GREY
        )
        margin_note.to_corner(UP + LEFT, buff=GAP_SM)
        self.add(margin_note)

        axes = Axes(
            x_range=[-3, 5, 1],
            y_range=[-3, 5, 1],
            x_length=6,
            y_length=6,
            axis_config={"color": CHARCOAL, "include_ticks": False, "tip_length": 0.2},
        )
        axes.to_edge(LEFT, buff=GAP_MD)

        curve = axes.plot(lambda x: A * (x - H) ** 2 + K, x_range=[-2, 4], color=SLATE)

        equation = MathTex(
            "y", "=", "a", "(", "x", "-", "h", ")", "^2", "+", "k",
            font_size=EQUATION_SIZE,
            color=CHARCOAL,
        )
        equation.to_edge(RIGHT, buff=GAP_MD).shift(UP)

        vertex_dot = Dot(axes.c2p(H, K), color=TERRACOTTA)
        vertex_label = MathTex("(h,\\ k)", font_size=EQUATION_SIZE, color=TERRACOTTA)
        vertex_label.next_to(vertex_dot, DOWN, buff=GAP_SM)
        vertex = VGroup(vertex_dot, vertex_label)

        with self.beat("axes") as t:
            self.play(Create(axes), run_time=t.fill(0.6))

        with self.beat("curve") as t:
            self.play(Create(curve), run_time=t.fill(0.5))
            t.hold()

        with self.beat("equation") as t:
            self.play(Write(equation), run_time=t.fill(0.5))
            t.hold()

        with self.beat("vertex") as t:
            self.play(Create(vertex), run_time=t.fill(0.3))
            t.hold()
