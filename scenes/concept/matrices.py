"""Matrices — beyond a table of numbers.

Narrated in Urdu, captioned in English: the slides carry the same lesson
in the language the student will sit the exam in, and the beats are
anchored to the Urdu words that motivate each reveal.

One worked example carries the whole thing. A school cricket tournament
needs refreshments for three kinds of people, and the table of who needs
what is the matrix; the headcount is the vector; the shopping list is the
product. Scaling, additivity and the word "linear" all come out of the
same table rather than from a definition.

Every number on screen is computed from that table, never typed twice:
MatrixGrid.working() builds each row's line from the row and the vector,
and MatrixGrid.product() builds the output. Checked before building:

    [[1,1,2],[2,1,3],[1,1,1]] x [3,2,4] = [13, 20, 9]

which is the 13 bottles, 20 samosas and 9 bananas the narration arrives
at, and doubling the headcount gives 26 bottles, as it says. The two
groups in the additivity section are [2,1,1] and [1,1,3], which really do
sum to [3,2,4], so adding first and multiplying first really do agree.

The delivery names stretch and rotate in the geometry section; the written
plan also had shear and project, and they are not said, so they are not on
screen. The transformations shown are applied with the matrices beside
them rather than drawn to look right.

Timing: timings/concept.matrices.json
Render: python build/render.py scripts/M01-matrices.md audio/M01-matrices.m4a
"""

import numpy as np

from manim import (
    Arrow,
    Create,
    FadeIn,
    FadeOut,
    Line,
    Polygon,
    Transform,
    VGroup,
    Write,
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
)

from brand import (
    BODY_SIZE,
    CHARCOAL,
    GAP_LG,
    GAP_MD,
    GAP_SM,
    GREY,
    LABEL_SIZE,
    MARGIN_SIZE,
    SAGE,
    SLATE,
    TERRACOTTA,
    TITLE_SIZE,
    mono,
    serif,
)
from components.matrix_grid import ColumnVector, MatrixGrid
from scenes.base import SATScene

FRAME_SAFE = 12.6
FLOOR = -3.3

ROWS = ["water bottles", "samosas", "bananas"]
COLS = ["students", "teachers", "players"]

# What one person of each group needs, item by item. Everything the lesson
# asserts is derived from this table and the headcount beside it.
NEEDS = [[1, 1, 2],
         [2, 1, 3],
         [1, 1, 1]]
HEADS = [3, 2, 4]

# The two groups in the additivity section. They sum to HEADS, so "add the
# groups then multiply" and "multiply each then add" are the same sum.
GROUP_A = [2, 1, 1]
GROUP_B = [1, 1, 3]

# Real transformations, applied with apply_matrix rather than drawn to
# look right, so the shape on screen is what the matrix beside it does.
STRETCH = [[1.75, 0.0], [0.0, 1.0]]
ROTATE = [[0.766, -0.643], [0.643, 0.766]]   # 40 degrees, to 3 places


def fit(mobject, width=FRAME_SAFE):
    if mobject.width > width:
        mobject.scale_to_fit_width(width)
    return mobject


class Matrices(SATScene):
    scene_id = "concept.matrices"

    def construct(self):
        self.margin = mono("Matrices · The Digital Tutor", MARGIN_SIZE)
        self.margin.to_corner(UP + LEFT, buff=GAP_SM)
        self.add(self.margin)
        self.keep = [self.margin]
        self.head = None

        self.opening()
        self.first_count()
        self.three_groups()
        self.build_matrix()
        self.the_vector()
        self.the_product()
        self.the_order()
        self.as_function()
        self.scaling()
        self.additivity()
        self.geometry()
        self.closing()

    # -------------------------------------------------------------- helpers

    def clear(self, t, *groups, fraction=0.1):
        """Fade a diagram that was drawn child by child.

        Create() on a group's children adds the children, not the group, so
        FadeOut(group) removes a mobject the scene never held and leaves
        the drawing on screen.
        """
        family = set()
        for group in groups:
            family.update(id(m) for m in group.get_family())
        present = [m for m in self.mobjects if id(m) in family]
        if present:
            self.play(*[FadeOut(m) for m in present],
                      run_time=t.fill(fraction))

    def wipe(self, t, fraction=0.05):
        old = [m for m in self.mobjects if m not in self.keep]
        if old:
            self.play(*[FadeOut(m) for m in old], run_time=t.fill(fraction))
        self.head = None

    def title(self, t, text, fraction=0.09, color=CHARCOAL):
        head = fit(serif(text, TITLE_SIZE, color))
        head.to_edge(UP, buff=GAP_MD * 1.9)
        self.play(Write(head), run_time=t.fill(fraction))
        self.head = head
        return head

    def lines(self, *texts, size=BODY_SIZE, color=CHARCOAL, buff=GAP_SM * 1.3,
              align=None):
        group = VGroup(*[fit(serif(x, size, color)) for x in texts])
        if align is None:
            group.arrange(DOWN, buff=buff)
        else:
            group.arrange(DOWN, buff=buff, aligned_edge=align)
        return group

    def stack(self, group, top=None, buff=GAP_MD, floor=FLOOR, align=ORIGIN):
        """Place under `top`, tightening the group's gaps to clear the floor.

        Only ever tightens, so a floor it cannot reach squeezes the gaps to
        nothing. Pass a floor the group can actually clear.
        """
        for factor in (1.0, 0.85, 0.7, 0.55, 0.42, 0.32, 0.24):
            gap = buff * factor
            group.arrange(DOWN, buff=gap, aligned_edge=align)
            if top is None:
                group.move_to(ORIGIN)
            else:
                group.next_to(top, DOWN, buff=gap)
            if group.get_bottom()[1] >= floor:
                break
        return group

    def place(self, mobject, top=None, buff=GAP_MD, floor=FLOOR):
        for factor in (1.0, 0.9, 0.78, 0.66, 0.55):
            if top is None:
                mobject.move_to(ORIGIN)
            else:
                mobject.next_to(top, DOWN, buff=buff * factor)
            if mobject.get_bottom()[1] >= floor:
                break
        return mobject

    def caption(self, text, color=GREY, size=BODY_SIZE):
        return fit(serif(text, size, color))

    def recaption(self, t, holder, text, color=GREY, fraction=0.2,
                  size=BODY_SIZE):
        nxt = self.caption(text, color, size)
        nxt.move_to(holder)
        self.play(Transform(holder, nxt), run_time=t.fill(fraction))
        return holder

    def foot(self, mobject, buff=GAP_MD * 1.1):
        mobject.to_edge(DOWN, buff=buff)
        return mobject

    def hide(self, group):
        for row in group:
            row.set_opacity(0)
        return group

    def reveal(self, t, group, start, stop, fraction):
        for row in group[start:stop]:
            row.set_opacity(1)
            self.play(FadeIn(row), run_time=t.fill(fraction))

    def sums(self, rows, left_x=-3.6, mid_x=-0.9, right_x=2.4,
             size=BODY_SIZE, gap=GAP_MD * 0.9, floor=FLOOR, top=None):
        """Three aligned columns placed by coordinate: label, working, result.

        By coordinate because Pango collapses runs of whitespace, so a
        space-padded column is not actually aligned, and because arranging
        by bounding box makes a row without descenders sit closer to its
        neighbour than one with them.
        """
        built = []
        for label, working, result in rows:
            built.append((
                fit(serif(label, size, GREY), mid_x - left_x - 0.3),
                fit(serif(working, size, CHARCOAL), right_x - mid_x - 0.3),
                fit(serif(result, size, SAGE), 2.6),
            ))
        line = max(max(m.height for m in row) for row in built)
        group = VGroup()
        for factor in (1.0, 0.8, 0.62, 0.48, 0.36):
            pitch = line + gap * factor
            group = VGroup()
            for i, row in enumerate(built):
                y = -i * pitch
                for mob, x in zip(row, (left_x, mid_x, right_x)):
                    mob.move_to([x + mob.width / 2, y, 0])
                group.add(VGroup(*row))
            if top is None:
                group.move_to(ORIGIN)
            else:
                group.next_to(top, DOWN, buff=gap * factor)
            if group.get_bottom()[1] >= floor:
                break
        return group

    def rule_under(self, group, color=GREY, buff=GAP_SM * 0.7):
        rule = Line(group.get_left() + LEFT * 0.1,
                    group.get_right() + RIGHT * 0.1,
                    color=color, stroke_width=2)
        rule.next_to(group, DOWN, buff=buff)
        return rule

    # ------------------------------------------------------------- sections

    def opening(self):
        with self.beat("title") as t:
            head = fit(serif("MATRICES", TITLE_SIZE * 1.4, CHARCOAL))
            sub = serif("beyond a table of numbers", BODY_SIZE, GREY)
            card = VGroup(head, sub).arrange(DOWN, buff=GAP_MD * 1.4)
            card.move_to(ORIGIN)
            self.play(Write(head), run_time=t.fill(0.35))
            self.play(FadeIn(sub), run_time=t.fill(0.25))
            t.hold()

        with self.beat("misconception") as t:
            self.wipe(t)
            rows = self.lines("a difficult table of numbers",
                              "with no use in real life",
                              size=BODY_SIZE, color=GREY)
            rows.move_to(UP * 0.6)
            self.play(Write(rows), run_time=t.fill(0.45))
            self.wrong = rows
            t.hold()

        with self.beat("not_true") as t:
            note = self.caption("not true", TERRACOTTA, TITLE_SIZE)
            self.stack(VGroup(note), self.wrong, buff=GAP_LG)
            self.play(Write(note), run_time=t.fill(0.45))
            t.hold()

        with self.beat("tournament") as t:
            self.wipe(t)
            card = self.lines("a school cricket tournament",
                              size=TITLE_SIZE, color=CHARCOAL)
            card.move_to(UP * 0.3)
            self.play(Write(card), run_time=t.fill(0.5))
            t.hold()

    def first_count(self):
        with self.beat("students_come") as t:
            self.wipe(t)
            self.title(t, "Three students come to watch", fraction=0.2)
            t.hold()

        with self.beat("two_each") as t:
            note = self.caption("two samosas each", CHARCOAL)
            self.stack(VGroup(note), self.head, buff=GAP_LG)
            self.play(Write(note), run_time=t.fill(0.5))
            self.note = note
            t.hold()

        with self.beat("multiply") as t:
            line = fit(serif("3  x  2  =  6", TITLE_SIZE * 1.2, TERRACOTTA))
            self.place(line, self.note, buff=GAP_LG)
            self.play(Write(line), run_time=t.fill(0.5))
            t.hold()

    def three_groups(self):
        with self.beat("not_only") as t:
            self.wipe(t)
            self.title(t, "Not only students", fraction=0.2)
            t.hold()

        with self.beat("also") as t:
            note = self.caption("teachers and cricket players too", CHARCOAL)
            self.stack(VGroup(note), self.head, buff=GAP_LG)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

        with self.beat("headcount") as t:
            self.wipe(t)
            self.title(t, "How many of each", fraction=0.12)
            self.heads = ColumnVector(HEADS, COLS)
            self.place(self.heads, self.head, buff=GAP_LG * 0.9)
            self.play(Create(self.heads.brackets), run_time=t.fill(0.2))
            self.play(Write(self.heads.entries), Write(self.heads.labels),
                      run_time=t.fill(0.45))
            t.hold()

        with self.beat("needs_differ") as t:
            self.wipe(t)
            self.title(t, "They do not all need the same", fraction=0.12)
            t.hold()

        with self.beat("per_person") as t:
            rows = self.sums([(COLS[i], f"{NEEDS[1][i]} samosas", "")
                              for i in range(3)], left_x=-3.2, mid_x=0.2,
                             right_x=3.0)
            self.hide(rows)
            self.place(rows, self.head, buff=GAP_LG * 0.9)
            self.reveal(t, rows, 0, 3, 0.2)
            t.hold()

        with self.beat("calc_students") as t:
            self.wipe(t)
            self.title(t, "Samosas", fraction=0.1)
            # Each line is the row of the table, worked for one group.
            self.work = self.sums(
                [(COLS[i], f"{HEADS[i]}  x  {NEEDS[1][i]}",
                  f"=  {HEADS[i] * NEEDS[1][i]}") for i in range(3)])
            self.hide(self.work)
            self.place(self.work, self.head, buff=GAP_LG * 0.8)
            self.reveal(t, self.work, 0, 1, 0.4)
            t.hold()

        with self.beat("calc_teachers") as t:
            self.reveal(t, self.work, 1, 2, 0.5)
            t.hold()

        with self.beat("calc_players") as t:
            self.reveal(t, self.work, 2, 3, 0.5)
            t.hold()

        with self.beat("total") as t:
            rule = self.rule_under(self.work)
            terms = [HEADS[i] * NEEDS[1][i] for i in range(3)]
            text = ("  +  ".join(str(x) for x in terms)
                    + f"  =  {sum(terms)}")
            total = fit(serif(text, TITLE_SIZE, TERRACOTTA))
            total.next_to(rule, DOWN, buff=GAP_MD)
            self.play(Create(rule), run_time=t.fill(0.12))
            self.play(Write(total), run_time=t.fill(0.45))
            t.hold()

    def build_matrix(self):
        with self.beat("more_items") as t:
            self.wipe(t)
            self.title(t, "Water bottles and bananas too", fraction=0.2)
            t.hold()

        with self.beat("arrange") as t:
            note = self.caption("put every need in one table", CHARCOAL)
            self.stack(VGroup(note), self.head, buff=GAP_LG)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

        with self.beat("matrix_named") as t:
            self.wipe(t)
            self.grid = MatrixGrid(NEEDS, ROWS, COLS)
            self.grid.move_to(UP * 1.2)
            self.play(Create(self.grid.brackets), run_time=t.fill(0.14))
            self.play(Write(self.grid.col_labels),
                      Write(self.grid.row_labels), run_time=t.fill(0.25))
            self.play(Write(self.grid.entries), run_time=t.fill(0.3))
            name = self.caption("a MATRIX", TERRACOTTA, TITLE_SIZE)
            self.foot(name)
            self.play(Write(name), run_time=t.fill(0.2))
            self.name = name
            t.hold()

        with self.beat("columns") as t:
            self.play(*self.grid.light_col(0), run_time=t.fill(0.18))
            self.recaption(t, self.name, "each column is a group",
                           TERRACOTTA, 0.22, BODY_SIZE)
            self.play(*self.grid.light_col(2), run_time=t.fill(0.18))
            t.hold()

        with self.beat("rows") as t:
            self.play(*self.grid.light_row(0), run_time=t.fill(0.18))
            self.recaption(t, self.name, "each row is an item",
                           TERRACOTTA, 0.22, BODY_SIZE)
            self.play(*self.grid.light_row(2), run_time=t.fill(0.18))
            t.hold()

        with self.beat("each_number") as t:
            self.play(*self.grid.settle(), run_time=t.fill(0.14))
            self.recaption(t, self.name,
                           "each number: what one person of that group needs",
                           CHARCOAL, 0.4, LABEL_SIZE)
            t.hold()

        with self.beat("entry_eg") as t:
            # Two bottles for every player: the water row against the
            # players column, read off the table rather than asserted.
            row = [self.grid.entry(0, c) for c in range(len(COLS))]
            col = [self.grid.entry(r, 2) for r in range(len(ROWS))]
            self.play(*[c.animate.set_color(SLATE) for c in row],
                      self.grid.row_labels[0].animate.set_color(SLATE),
                      run_time=t.fill(0.16))
            self.play(*[c.animate.set_color(SLATE) for c in col],
                      self.grid.col_labels[2].animate.set_color(SLATE),
                      run_time=t.fill(0.16))
            self.play(self.grid.entry(0, 2).animate.set_color(TERRACOTTA),
                      run_time=t.fill(0.16))
            self.recaption(t, self.name,
                           f"{NEEDS[0][2]} bottles for every player",
                           CHARCOAL, 0.25, LABEL_SIZE)
            t.hold()

    def the_vector(self):
        with self.beat("vector") as t:
            self.play(*self.grid.settle(), run_time=t.fill(0.1))
            self.vec = ColumnVector(HEADS)
            self.vec.next_to(self.grid, RIGHT, buff=GAP_MD * 1.2)
            self.play(Create(self.vec.brackets), run_time=t.fill(0.16))
            self.play(Write(self.vec.entries), run_time=t.fill(0.3))
            self.recaption(t, self.name, "how many people in each group",
                           CHARCOAL, 0.25, BODY_SIZE)
            t.hold()

        with self.beat("vector_meaning") as t:
            # The vector's entries line up with the matrix's columns, so
            # the colours are the link rather than a caption saying so.
            for i in range(3):
                self.play(*self.grid.light_col(i, others=GREY),
                          *self.vec.light(i, others=GREY),
                          run_time=t.fill(0.2))
            t.hold()

    def the_product(self):
        with self.beat("how") as t:
            self.play(*self.grid.settle(), *self.vec.settle(),
                      run_time=t.fill(0.1))
            self.recaption(t, self.name,
                           "multiply along the row, then add",
                           CHARCOAL, 0.3, BODY_SIZE)
            t.hold()

        self.lines_out = []
        for name, row in (("water_row", 0), ("samosa_row", 1),
                          ("banana_row", 2)):
            with self.beat(name) as t:
                self.play(*self.grid.light_row(row), run_time=t.fill(0.16))
                line = self.grid.working(row, HEADS)
                # Centred under the matrix's brackets, not under the frame
                # and not under the matrix-plus-vector: the row labels hang
                # off the left, so the grid's own middle is well right of
                # x = 0, and including the vector pushes these lines into
                # the right-hand margin.
                line.move_to([self.grid.brackets.get_center()[0],
                              -1.15 - row * 0.6, 0])
                self.play(Write(line), run_time=t.fill(0.45))
                self.lines_out.append(line)
                t.hold()

        with self.beat("output") as t:
            self.wipe(t)
            self.title(t, "The shopping list", fraction=0.1)
            out = ColumnVector(self.grid.product(HEADS), ROWS,
                               color=TERRACOTTA)
            self.place(out, self.head, buff=GAP_LG * 0.9)
            self.play(Create(out.brackets), run_time=t.fill(0.18))
            self.play(Write(out.entries), Write(out.labels),
                      run_time=t.fill(0.45))
            self.out = out
            t.hold()

        with self.beat("mathematically") as t:
            note = self.caption("matrix  x  people  =  what to buy",
                                CHARCOAL, BODY_SIZE)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.45))
            self.note = note
            t.hold()

        with self.beat("idea_simple") as t:
            self.recaption(t, self.note,
                           "the matrix holds the needs, the vector holds "
                           "the people", GREY, 0.45, LABEL_SIZE)
            t.hold()

    def the_order(self):
        with self.beat("order") as t:
            self.wipe(t)
            self.title(t, "The order of the columns matters", fraction=0.14)
            self.grid = MatrixGrid(NEEDS, ROWS, COLS)
            self.grid.move_to(DOWN * 0.3)
            self.vec = ColumnVector(HEADS)
            self.vec.next_to(self.grid, RIGHT, buff=GAP_MD * 1.2)
            self.play(Create(self.grid.brackets), Create(self.vec.brackets),
                      run_time=t.fill(0.14))
            self.play(Write(self.grid.entries), Write(self.grid.col_labels),
                      Write(self.grid.row_labels), Write(self.vec.entries),
                      run_time=t.fill(0.3))
            t.hold()

        with self.beat("order_match") as t:
            for i in range(3):
                self.play(*self.grid.light_col(i, others=GREY),
                          *self.vec.light(i, others=GREY),
                          run_time=t.fill(0.22))
            t.hold()

        with self.beat("order_wrong") as t:
            self.play(*self.grid.settle(), *self.vec.settle(),
                      run_time=t.fill(0.1))
            note = self.caption("wrong order, wrong answer", TERRACOTTA,
                                BODY_SIZE)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.4))
            t.hold()

    def as_function(self):
        with self.beat("function") as t:
            self.wipe(t)
            self.title(t, "A matrix is a function", fraction=0.12)
            box = fit(serif("MATRIX", BODY_SIZE, CHARCOAL))
            frame = Polygon([-1.3, -0.55, 0], [1.3, -0.55, 0],
                            [1.3, 0.55, 0], [-1.3, 0.55, 0],
                            color=SLATE, stroke_width=3)
            box.move_to(frame)
            middle = VGroup(frame, box)
            left = fit(serif("people in", LABEL_SIZE, GREY))
            right = fit(serif("things to buy", LABEL_SIZE, TERRACOTTA))
            left.move_to([-4.6, 0, 0])
            right.move_to([4.6, 0, 0])
            lane = VGroup(left, middle, right)
            arrows = VGroup(
                Arrow(left.get_right(), frame.get_left(), color=GREY,
                      stroke_width=3.5, buff=GAP_SM * 0.8,
                      max_tip_length_to_length_ratio=0.14),
                Arrow(frame.get_right(), right.get_left(), color=GREY,
                      stroke_width=3.5, buff=GAP_SM * 0.8,
                      max_tip_length_to_length_ratio=0.14),
            )
            whole = VGroup(lane, arrows)
            whole.move_to(DOWN * 0.1)
            self.play(Create(frame), Write(box), run_time=t.fill(0.2))
            self.play(Write(left), Create(arrows[0]), run_time=t.fill(0.22))
            self.play(Write(right), Create(arrows[1]), run_time=t.fill(0.22))
            self.lane = whole
            t.hold()

        with self.beat("three_three") as t:
            note = self.lines("three inputs, because there are three groups",
                              "three outputs, because there are three items",
                              size=LABEL_SIZE, color=CHARCOAL)
            self.stack(note, self.lane, buff=GAP_LG * 0.8)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

    def scaling(self):
        with self.beat("scaling") as t:
            self.wipe(t)
            self.title(t, "Double the people", fraction=0.12)
            t.hold()

        with self.beat("scaling_eg") as t:
            before = self.grid.product(HEADS)
            after = self.grid.product([2 * h for h in HEADS])
            rows = self.sums(
                [(ROWS[i], f"{before[i]}  becomes", str(after[i]))
                 for i in range(3)], left_x=-4.2, mid_x=-1.0, right_x=2.0)
            self.hide(rows)
            self.place(rows, self.head, buff=GAP_LG * 0.8)
            self.reveal(t, rows, 0, 3, 0.22)
            t.hold()

        with self.beat("scaling_name") as t:
            note = self.caption("SCALING", TERRACOTTA, TITLE_SIZE)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.45))
            t.hold()

    def additivity(self):
        with self.beat("additivity") as t:
            self.wipe(t)
            self.title(t, "Two groups arrive", fraction=0.12)
            t.hold()

        with self.beat("additivity_two_ways") as t:
            # Both routes are computed from the same table, so the two
            # columns agree because the arithmetic agrees.
            together = self.grid.product(
                [a + b for a, b in zip(GROUP_A, GROUP_B)])
            apart = [a + b for a, b in zip(self.grid.product(GROUP_A),
                                           self.grid.product(GROUP_B))]
            rows = self.sums(
                [("add the groups, then multiply", "", str(together)),
                 ("multiply each, then add", "", str(apart))],
                left_x=-5.9, mid_x=1.5, right_x=1.8, size=LABEL_SIZE)
            self.hide(rows)
            self.place(rows, self.head, buff=GAP_LG * 0.9)
            self.reveal(t, rows, 0, 2, 0.3)
            self.ways = rows
            t.hold()

        with self.beat("additivity_same") as t:
            note = self.caption("the same answer either way", SAGE,
                                BODY_SIZE)
            self.stack(VGroup(note), self.ways, buff=GAP_LG * 0.8)
            self.play(Write(note), run_time=t.fill(0.45))
            t.hold()

        with self.beat("linear") as t:
            self.wipe(t)
            rows = self.lines("scaling", "+  additivity", size=BODY_SIZE,
                              color=CHARCOAL)
            name = fit(serif("a LINEAR function", TITLE_SIZE, TERRACOTTA))
            block = VGroup(rows, name).arrange(DOWN, buff=GAP_LG)
            block.move_to(UP * 0.2)
            self.play(Write(rows), run_time=t.fill(0.3))
            self.play(Write(name), run_time=t.fill(0.3))
            t.hold()

    def geometry(self):
        with self.beat("geometry") as t:
            self.wipe(t)
            self.title(t, "Not only event planning", fraction=0.12)
            note = self.caption("in geometry, a matrix moves a shape", GREY)
            self.stack(VGroup(note), self.head, buff=GAP_MD * 1.2)
            self.play(Write(note), run_time=t.fill(0.35))
            self.note = note
            t.hold()

        with self.beat("shapes") as t:
            self.shape = self.unit_shape()
            # apply_matrix works about the origin unless told otherwise, so
            # a shape sitting below centre gets swung across the frame
            # rather than turned where it stands. Everything here pivots
            # about this one point.
            self.pivot = np.array([0.0, -0.75, 0.0])
            self.shape.move_to(self.pivot)
            self.play(Create(self.shape), run_time=t.fill(0.5))
            t.hold()

        with self.beat("transform") as t:
            self.recaption(t, self.note, "STRETCH", TERRACOTTA, 0.1,
                           BODY_SIZE)
            self.play(self.shape.animate.apply_matrix(
                np.array(STRETCH), about_point=self.pivot),
                run_time=t.fill(0.22))
            self.recaption(t, self.note, "ROTATE", TERRACOTTA, 0.1,
                           BODY_SIZE)
            # Undo the stretch and rotate in one move: the shape is
            # currently STRETCH.p, and ROTATE.p is ROTATE.inv(STRETCH)
            # applied to that. One play, so a short beat can hold both.
            back = np.array(ROTATE) @ np.linalg.inv(np.array(STRETCH))
            self.play(self.shape.animate.apply_matrix(
                back, about_point=self.pivot), run_time=t.fill(0.25))
            t.hold()

        with self.beat("dimensions") as t:
            self.recaption(t, self.note, "in two dimensions, and in three",
                           CHARCOAL, 0.45, BODY_SIZE)
            t.hold()

    def unit_shape(self):
        """A square with one corner cut, so a rotation is visible as one."""
        points = [[-1.3, -1.3, 0], [1.3, -1.3, 0], [1.3, 0.6, 0],
                  [0.0, 1.3, 0], [-1.3, 0.6, 0]]
        return Polygon(*points, color=SLATE, stroke_width=4)

    def closing(self):
        with self.beat("not_just") as t:
            self.wipe(t)
            self.title(t, "So, next time you see a matrix", fraction=0.14)
            t.hold()

        with self.beat("three_uses") as t:
            rows = self.lines("a way to arrange information",
                              "a way to turn inputs into outputs",
                              "a way to understand change",
                              size=BODY_SIZE, color=CHARCOAL, align=LEFT)
            self.hide(rows)
            self.stack(rows, self.head, buff=GAP_MD * 1.4, align=LEFT)
            self.reveal(t, rows, 0, 3, 0.22)
            t.hold()

        with self.beat("maths_interesting") as t:
            self.wipe(t)
            rows = self.lines("maths gets interesting",
                              "when you see what the formula is doing",
                              size=TITLE_SIZE, color=CHARCOAL)
            rows.move_to(UP * 0.3)
            self.play(Write(rows), run_time=t.fill(0.5))
            t.hold()

        with self.beat("cta") as t:
            self.wipe(t)
            rows = self.lines("like the video", "ask your question below",
                              size=BODY_SIZE, color=CHARCOAL)
            name = fit(serif("The Digital Tutor", TITLE_SIZE * 1.1,
                             TERRACOTTA))
            sub = serif("subscribe", BODY_SIZE, GREY)
            card = VGroup(rows, name, sub).arrange(DOWN, buff=GAP_LG * 0.8)
            card.move_to(ORIGIN)
            self.play(Write(rows), run_time=t.fill(0.3))
            self.play(Write(name), run_time=t.fill(0.25))
            self.play(FadeIn(sub), run_time=t.fill(0.2))
            t.hold()
