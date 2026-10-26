"""Shared furniture for the A Level 9618 challenge Shorts.

One recurring format: a hard question, a countdown while the viewer tries
it, the working, then the answer. Three Shorts, one visual language, so
the third looks like the first — consistency across a series is the
quality signal, not any single Short's polish.

Sized for the portrait frame (4.5 x 8 units). Portrait is 1.78x denser
than the lecture frame, so a nominal size here reads larger on screen than
the number suggests; the floor that matters is 28px at 1080x1920, which
works out at a nominal ~15.8.
"""

from manim import DOWN, LEFT, Line, SurroundingRectangle, VGroup

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

PORTRAIT_SAFE = 3.9      # widest anything may run in a 4.5-unit frame

QUESTION = 32            # the question card's body
CODE = 26                # pseudocode and table definitions
ANSWER = 44              # the bit pattern or value being revealed
COUNT = 88               # the countdown digit
SERIES = 28              # the closing card


def fit(mobject, width=PORTRAIT_SAFE):
    if mobject.width > width:
        mobject.scale_to_fit_width(width)
    return mobject


def spec_block(rows, size=CODE, color=CHARCOAL, accent=SLATE,
               width=PORTRAIT_SAFE):
    """A boxed monospace panel: pseudocode, a schema, a bit pattern.

    Left-aligned, because code and schemas are read line by line rather
    than centred on each other. Fitted including the border — the box adds
    its buff on top of the text, so fitting only the text leaves the panel
    over-wide.
    """
    body = VGroup(*[mono(line, size, color) for line in rows])
    body.arrange(DOWN, buff=GAP_SM * 0.85, aligned_edge=LEFT)
    fit(body, width - 0.45)
    box = SurroundingRectangle(body, color=accent, buff=GAP_SM * 1.1,
                               stroke_width=3)
    return fit(VGroup(box, body), width)


def answer_card(rows, size=ANSWER, color=TERRACOTTA, width=PORTRAIT_SAFE):
    """The boxed result — the one terracotta thing on its screen."""
    body = VGroup(*[serif(line, size, color) for line in rows])
    body.arrange(DOWN, buff=GAP_SM * 1.1)
    fit(body, width - 0.5)
    box = SurroundingRectangle(body, color=color, buff=GAP_SM * 1.3,
                               stroke_width=4)
    return fit(VGroup(box, body), width)


def table_card(name, fields, key=None, size=CODE, accent=SAGE,
               width=PORTRAIT_SAFE):
    """One normalised relation: its name over its field list.

    The primary key is underlined, which is how a database answer is
    expected to be written.
    """
    title = serif(name, size * 1.15, accent)
    body = VGroup(*[mono(f, size, CHARCOAL) for f in fields])
    body.arrange(DOWN, buff=GAP_SM * 0.6, aligned_edge=LEFT)
    if key is not None:
        for i in key:
            rule = Line(body[i].get_left(), body[i].get_right(),
                        color=accent, stroke_width=2)
            rule.next_to(body[i], DOWN, buff=GAP_SM * 0.25)
            body.add(rule)
    inner = VGroup(title, body).arrange(DOWN, buff=GAP_SM * 0.9)
    box = SurroundingRectangle(inner, color=accent, buff=GAP_SM,
                               stroke_width=2.5)
    return fit(VGroup(box, inner), width)


class CallTree(VGroup):
    """A recursive call tree: one labelled node per call, revealed by level.

    The question asks for the returned value *and* the number of calls, and
    students lose the second mark by not drawing this. So the tree is the
    answer to the counting question as much as to the value question —
    every node on screen is one call.

    `layout` is a list of levels, each a list of (label, x) pairs; `edges`
    names parent and child by their index in a flat left-to-right ordering.
    Explicit rather than computed: one tree, and the portrait frame is too
    narrow to trust an automatic layout to stay inside it.
    """

    def __init__(self, layout, edges, radius=0.2, size=20, top=1.5,
                 pitch=1.0, color=SLATE, lit=TERRACOTTA, width=None):
        super().__init__()
        from manim import Circle, Line

        self.lit_color, self.dim_color = lit, color
        self.nodes, self.levels = VGroup(), []
        centres = []
        for depth, level in enumerate(layout):
            row = VGroup()
            for label, x in level:
                y = top - depth * pitch
                ring = Circle(radius=radius, color=color, stroke_width=2.5)
                ring.move_to([x, y, 0])
                text = serif(str(label), size, CHARCOAL)
                text.move_to(ring)
                node = VGroup(ring, text)
                row.add(node)
                self.nodes.add(node)
                centres.append([x, y, 0])
            self.levels.append(row)

        self.edges = VGroup()
        for parent, child in edges:
            line = Line(centres[parent], centres[child], color=GREY,
                        stroke_width=2)
            # Stop the line at the rings rather than running through them.
            line.set_length(max(0.01, line.get_length() - 2 * radius - 0.04))
            self.edges.add(line)

        self.add(self.edges, self.nodes)
        if width and self.width > width:
            self.scale_to_fit_width(width)

    # Visibility is stroke-only. set_opacity() sets fill as well, which
    # turns the rings into filled discs; and FadeIn interpolates towards a
    # mobject's current state, so anything hidden by opacity has to be
    # restored before it is faded in or it fades from nothing to nothing.

    def hidden(self):
        for node in self.nodes:
            node[0].set_stroke(opacity=0)
            node[1].set_opacity(0)
        for edge in self.edges:
            edge.set_stroke(opacity=0)
        return self

    def show_level(self, depth):
        """Make one level of the tree visible; returns it for FadeIn."""
        return self.show_nodes(range(len(self.levels[depth])),
                               level=depth)

    def show_nodes(self, indices, level=None):
        """Restore some nodes to visible and hand them back for FadeIn."""
        group = VGroup()
        source = self.levels[level] if level is not None else self.nodes
        for i in indices:
            node = source[i]
            node[0].set_stroke(opacity=1)
            node[1].set_opacity(1)
            group.add(node)
        return group

    def show_edges(self, indices):
        group = VGroup()
        for i in indices:
            self.edges[i].set_stroke(opacity=1)
            group.add(self.edges[i])
        return group

    def light(self, indices):
        """Highlight some nodes — one branch at a time."""
        return [self.nodes[i][0].animate.set_color(self.lit_color)
                for i in indices]

    def settle(self, indices):
        return [self.nodes[i][0].animate.set_color(self.dim_color)
                for i in indices]


def series_card(size=SERIES, width=PORTRAIT_SAFE):
    """The card that closes every Short in the series."""
    head = VGroup(
        serif("CAMBRIDGE INTERNATIONAL", size * 0.85, GREY),
        serif("A LEVEL 9618", size * 1.5, CHARCOAL),
        serif("A* CHALLENGE", size * 1.8, TERRACOTTA),
    ).arrange(DOWN, buff=GAP_SM)
    foot = serif("The Digital Tutor", size, GREY)
    card = VGroup(head, foot).arrange(DOWN, buff=GAP_MD * 1.6)
    return fit(card, width)


def hook_lines(size=QUESTION, width=PORTRAIT_SAFE):
    """The recurring promise every Short opens on."""
    lines = VGroup(
        serif("You should be able", size, CHARCOAL),
        serif("to solve this if you're", size, CHARCOAL),
        serif("an A* student", size, TERRACOTTA),
    ).arrange(DOWN, buff=GAP_SM * 1.1)
    return fit(lines, width)
