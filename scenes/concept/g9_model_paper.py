"""Punjab Board Grade 9 Mathematics 2026 — model paper, Chapters 1 to 4.

Narrated in mixed Urdu and English, captioned in English: the algebra is
the same in both languages and the student sits the paper in English.

Twenty questions, and nearly all of them the same shape — a question
pinned at the top of the frame while a column of working grows underneath
it. That shape is components/worked_solution.py, which keeps the state the
brief calls for: where the next line goes, and what to do when the column
reaches the floor.

Every number was checked before anything was drawn, and all of it stands:

    (3+V5)(3-V5) = 4            lcm(16,4,30) = 240
    30+35-50 = 15               (3/4)^-2 / (4/9)^3 x 16/27 = 12
    floor(log10 0.000049) = -5  2^4 = 1+4+6+4+1 = 16
    25^(3/2)=125, 243^(3/5)=27, 16^(5/4)=32, 8^(4/3)=16
    125x27/32x16 = 3375/512, and gcd(3375,512) = 1
    10^-2.0184 = 0.00958517..., which is 0.00959 to 3 s.f.
    58+50-98 = 10
    (x^2+3y^2)^2 - (6xy)^2 = x^4 - 30x^2y^2 + 9y^4

LaTeX sets about 1.43x smaller than Pango at the same nominal size, so
every expression here is at brand.EQUATION_SIZE or above — that is exactly
the 28px mobile floor, and verify.py now holds LaTeX to it.

Timing: timings/concept.g9_model_paper.json
Render: python build/render.py scripts/G9MP1-chapters-1-4.md \\
    audio/G9MP1-chapters-1-4.m4a
"""

from manim import (
    Create,
    FadeIn,
    FadeOut,
    Line,
    MathTex,
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
    DISPLAY_SIZE,
    EQUATION_SIZE,
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
from components.syllabus_map import TopicStrip
from components.worked_solution import (
    WorkedSolution,
    answer_box,
    mcq_card,
    subset_grid,
)
from scenes.base import SATScene

FRAME_SAFE = 12.6
FLOOR = -2.95          # above the section strip

PARTS = ["MCQs", "Short questions", "Long questions"]

# The sixteen subsets of {+, -, x, /}, grouped by size, because that
# grouping is the argument for why there are sixteen of them.
POWER_SET = [
    ["{ }"],
    ["{+}", "{-}", "{x}", "{/}"],
    ["{+, -}", "{+, x}", "{+, /}", "{-, x}", "{-, /}", "{x, /}"],
    ["{+, -, x}", "{+, -, /}", "{+, x, /}", "{-, x, /}"],
    ["{+, -, x, /}"],
]


def fit(mobject, width=FRAME_SAFE):
    if mobject.width > width:
        mobject.scale_to_fit_width(width)
    return mobject


def tex(expression, size=EQUATION_SIZE, color=CHARCOAL):
    """A LaTeX expression, never smaller than the legibility floor.

    Computer Modern sets about 1.43x smaller than the Pango text beside it,
    so EQUATION_SIZE is not a comfortable default — it is exactly 28px at
    1080p, the mobile floor. Asking for less than that is always a mistake,
    so the request is clamped rather than honoured. If an expression then
    runs wider than the frame, shrink-to-fit will take it under the floor
    again and verify.py will say so, which is the right place to find out.
    """
    return MathTex(expression, font_size=max(size, EQUATION_SIZE),
                   color=color)


class G9ModelPaper(SATScene):
    scene_id = "concept.g9_model_paper"

    def construct(self):
        self.margin = mono("Grade 9 Maths 2026 · Model Paper", MARGIN_SIZE)
        self.margin.to_corner(UP + LEFT, buff=GAP_SM)
        self.add(self.margin)
        self.keep = [self.margin]
        self.strip = None
        self.head = None
        self.sol = None

        self.opening()
        self.route()
        self.mcq_conjugate()
        self.mcq_logarithm()
        self.mcq_power_set()
        self.mcq_intersection()
        self.mcq_lcm()
        self.mcq_common_factor()
        self.sq_rationals()
        self.sq_indices()
        self.sq_logarithm()
        self.sq_characteristic()
        self.sq_power_set()
        self.sq_difference()
        self.sq_quadratic()
        self.sq_cubes()
        self.lq_indices()
        self.lq_logarithm()
        self.lq_sets()
        self.lq_quartic()
        self.closing()

    # -------------------------------------------------------------- helpers

    def wipe(self, t, fraction=0.05):
        old = [m for m in self.mobjects if m not in self.keep]
        if old:
            self.play(*[FadeOut(m) for m in old], run_time=t.fill(fraction))
        self.head = None
        self.sol = None

    def clear(self, t, *groups, fraction=0.08):
        """Fade a diagram drawn child by child.

        Create() on a group's children adds the children, not the group, so
        FadeOut(group) removes something the scene never held.
        """
        family = set()
        for group in groups:
            family.update(id(m) for m in group.get_family())
        present = [m for m in self.mobjects if id(m) in family]
        if present:
            self.play(*[FadeOut(m) for m in present],
                      run_time=t.fill(fraction))

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
        """Place under `top`, tightening the gaps to clear the floor.

        Only ever tightens, so a floor the group cannot reach squeezes the
        gaps to nothing. Pass one it can clear.
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

    def caption(self, text, color=GREY, size=BODY_SIZE):
        return fit(serif(text, size, color))

    def recaption(self, t, holder, text, color=GREY, fraction=0.2,
                  size=BODY_SIZE):
        nxt = self.caption(text, color, size)
        nxt.move_to(holder)
        self.play(Transform(holder, nxt), run_time=t.fill(fraction))
        return holder

    def foot(self, mobject, buff=GAP_MD * 1.1):
        if self.strip in self.mobjects:
            mobject.next_to(self.strip, UP, buff=buff)
        else:
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

    def part(self, t, number, fraction=0.07):
        if self.strip is None:
            self.strip = TopicStrip(len(PARTS), lit=SLATE, side=0.6)
            self.strip.to_edge(DOWN, buff=GAP_SM * 0.6)
            self.add(self.strip)
            self.keep.append(self.strip)
        self.play(*self.strip.focus(number - 1), run_time=t.fill(fraction))

    # --- the worked-solution shape, used by almost every question ---------

    def ask(self, t, problem, title=None, draw=0.2, write=0.3):
        """Pin a question at the top and return its solution holder."""
        self.wipe(t)
        self.sol = WorkedSolution(problem, title=title, floor=FLOOR)
        if self.sol.title is not None:
            self.play(Write(self.sol.title), run_time=t.fill(draw))
        self.play(Write(self.sol.problem), run_time=t.fill(write))
        return self.sol

    def step(self, t, mobject, fraction=0.35, scroll=0.08, buff=None,
             align=None):
        """Add one line of working, scrolling the column if it is full."""
        moves = self.sol.place(mobject, buff=buff, align=align)
        if moves:
            self.play(*moves, run_time=t.fill(scroll))
        self.play(Write(mobject), run_time=t.fill(fraction))
        return mobject

    def final(self, t, mobject, fraction=0.3, draw=0.15):
        """The boxed answer, placed under the working."""
        card = answer_box(mobject)
        moves = self.sol.place(card, buff=GAP_MD * 1.2)
        if moves:
            self.play(*moves, run_time=t.fill(draw))
        self.play(Create(card[0]), run_time=t.fill(draw))
        self.play(Write(card[1]), run_time=t.fill(fraction))
        return card

    # ------------------------------------------------------------- opening

    def opening(self):
        with self.beat("open") as t:
            board = serif("Punjab Board · Grade 9 Mathematics 2026",
                          LABEL_SIZE, GREY)
            head = fit(serif("MODEL PAPER SOLUTIONS", TITLE_SIZE * 1.2,
                             CHARCOAL))
            sub = serif("Chapters 1 to 4", BODY_SIZE, TERRACOTTA)
            foot = serif("The Digital Tutor", LABEL_SIZE, GREY)
            card = VGroup(board, head, sub, foot).arrange(DOWN,
                                                          buff=GAP_MD * 1.3)
            card.move_to(ORIGIN)
            self.play(Write(board), run_time=t.fill(0.14))
            self.play(Write(head), run_time=t.fill(0.3))
            self.play(Write(sub), run_time=t.fill(0.18))
            self.play(FadeIn(foot), run_time=t.fill(0.14))
            t.hold()

        with self.beat("topics") as t:
            self.wipe(t)
            self.title(t, "What this paper covers", fraction=0.12)
            rows = self.lines("1   real numbers",
                              "2   logarithms",
                              "3   sets and functions",
                              "4   factorization",
                              size=BODY_SIZE, color=CHARCOAL, align=LEFT)
            self.hide(rows)
            self.stack(rows, self.head, buff=GAP_MD, align=LEFT)
            self.reveal(t, rows, 0, 4, 0.16)
            t.hold()

        with self.beat("method") as t:
            note = self.caption("every step, and why it works", TERRACOTTA,
                                BODY_SIZE)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.4))
            t.hold()

        with self.beat("disclaimer") as t:
            self.wipe(t)
            rows = self.lines("This is the official model paper",
                              "for preparation.",
                              "It shows the announced format,",
                              "not the questions of the annual exam.",
                              size=BODY_SIZE, color=CHARCOAL)
            rows.move_to(UP * 0.2)
            self.play(Write(rows), run_time=t.fill(0.5))
            t.hold()

    def route(self):
        with self.beat("route") as t:
            self.wipe(t)
            self.title(t, "Our route through the paper", fraction=0.12)
            rows = self.lines("MCQs from Chapters 1 to 4",
                              "short questions from Question 2",
                              "long questions: 5(a), 5(b), 6(a), 6(b)",
                              size=BODY_SIZE, color=CHARCOAL, align=LEFT)
            self.hide(rows)
            self.stack(rows, self.head, buff=GAP_MD * 1.3, align=LEFT)
            self.reveal(t, rows, 0, 3, 0.2)
            t.hold()

        with self.beat("notebook") as t:
            note = self.caption("pause before each solution and try it",
                                TERRACOTTA, BODY_SIZE)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.45))
            t.hold()

    # ---------------------------------------------------------------- MCQs

    def mcq_conjugate(self):
        with self.beat("mcq1") as t:
            self.wipe(t)
            self.part(t, 1)
            card, head, rows = mcq_card(
                tex(r"(3+\sqrt{5})(3-\sqrt{5})", DISPLAY_SIZE),
                ["rational number", "irrational number",
                 "natural number", "whole number"])
            self.play(Write(head), run_time=t.fill(0.3))
            self.play(Write(rows), run_time=t.fill(0.3))
            self.card, self.rows = card, rows
            t.hold()

        with self.beat("mcq1_identity") as t:
            note = fit(tex(r"(a+b)(a-b) = a^2 - b^2", EQUATION_SIZE, SLATE))
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.4))
            self.note = note
            t.hold()

        with self.beat("mcq1_work") as t:
            work = fit(tex(r"3^2 - (\sqrt{5})^2 = 9 - 5 = 4", EQUATION_SIZE))
            work.move_to(self.note)
            self.play(FadeOut(self.note), run_time=t.fill(0.08))
            self.play(Write(work), run_time=t.fill(0.4))
            self.note = work
            t.hold()

        with self.beat("mcq1_answer") as t:
            self.play(*self.rows.confirm("A"), run_time=t.fill(0.3))
            t.hold()

        with self.beat("mcq1_habit") as t:
            self.play(FadeOut(self.note), run_time=t.fill(0.08))
            note = self.caption("spot conjugates: the middle terms cancel",
                                TERRACOTTA, BODY_SIZE)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.4))
            t.hold()

    def mcq_logarithm(self):
        with self.beat("mcq2") as t:
            self.wipe(t)
            card, head, rows = mcq_card(
                "The base of a common logarithm is:",
                ["2", "10", "0", "1"])
            self.play(Write(head), run_time=t.fill(0.3))
            self.play(Write(rows), run_time=t.fill(0.3))
            self.rows = rows
            t.hold()

        with self.beat("mcq2_answer") as t:
            self.play(*self.rows.confirm("B"), run_time=t.fill(0.3))
            note = fit(tex(r"\log x \;=\; \log_{10} x", EQUATION_SIZE,
                           TERRACOTTA))
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.3))
            t.hold()

    def mcq_power_set(self):
        with self.beat("mcq3") as t:
            self.wipe(t)
            card, head, rows = mcq_card(
                tex(r"\text{If } A = \varnothing, \text{ what is } P(A)?",
                    EQUATION_SIZE),
                [tex(r"\varnothing", LABEL_SIZE * 1.3),
                 tex(r"\{\varnothing\}", LABEL_SIZE * 1.3),
                 tex(r"\{1\}", LABEL_SIZE * 1.3),
                 tex(r"\{0\}", LABEL_SIZE * 1.3)])
            self.play(Write(head), run_time=t.fill(0.3))
            self.play(Write(rows), run_time=t.fill(0.3))
            self.rows = rows
            t.hold()

        with self.beat("mcq3_reason") as t:
            note = self.caption("the empty set has exactly one subset: "
                                "itself", CHARCOAL, LABEL_SIZE)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.4))
            self.note = note
            t.hold()

        with self.beat("mcq3_answer") as t:
            self.play(*self.rows.confirm("B"), run_time=t.fill(0.35))
            t.hold()

        with self.beat("mcq3_trap") as t:
            trap = fit(tex(r"\varnothing \;\neq\; \{\varnothing\}",
                           DISPLAY_SIZE * 0.8, TERRACOTTA))
            trap.move_to(self.note)
            self.play(FadeOut(self.note), run_time=t.fill(0.08))
            self.play(Write(trap), run_time=t.fill(0.4))
            t.hold()

    def mcq_intersection(self):
        with self.beat("mcq4") as t:
            sol = self.ask(t, tex(r"n(A\cup B)=50,\quad n(A)=30,"
                                  r"\quad n(B)=35", EQUATION_SIZE),
                           title="Find n(A ∩ B)")
            t.hold()

        with self.beat("mcq4_formula") as t:
            self.step(t, tex(r"n(A\cup B) = n(A) + n(B) - n(A\cap B)",
                             EQUATION_SIZE, SLATE), fraction=0.45)
            t.hold()

        with self.beat("mcq4_substitute") as t:
            self.step(t, tex(r"50 = 30 + 35 - n(A\cap B)", EQUATION_SIZE),
                      fraction=0.45)
            t.hold()

        with self.beat("mcq4_work") as t:
            self.step(t, tex(r"n(A\cap B) = 65 - 50", EQUATION_SIZE),
                      fraction=0.45)
            t.hold()

        with self.beat("mcq4_answer") as t:
            self.final(t, tex(r"n(A\cap B) = 15", DISPLAY_SIZE * 0.85, SAGE))
            t.hold()

        with self.beat("mcq4_why") as t:
            note = self.caption("the shared elements were counted twice",
                                TERRACOTTA, LABEL_SIZE)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.45))
            t.hold()

    def mcq_lcm(self):
        with self.beat("mcq5") as t:
            self.ask(t, tex(r"16x^2, \quad 4x, \quad 30xy", DISPLAY_SIZE),
                     title="Find the LCM")
            t.hold()

        with self.beat("mcq5_numbers") as t:
            self.step(t, tex(r"\text{LCM}(16, 4, 30) = 240", EQUATION_SIZE),
                      fraction=0.45)
            t.hold()

        with self.beat("mcq5_vars") as t:
            self.step(t, tex(r"\text{highest powers: } x^2 \text{ and } y",
                             EQUATION_SIZE, SLATE), fraction=0.45)
            t.hold()

        with self.beat("mcq5_answer") as t:
            self.final(t, tex(r"240x^2y", DISPLAY_SIZE * 0.9, SAGE))
            t.hold()

    def mcq_common_factor(self):
        with self.beat("mcq6") as t:
            self.ask(t, tex(r"12x + 36", DISPLAY_SIZE), title="Factorize")
            t.hold()

        with self.beat("mcq6_divide") as t:
            self.step(t, tex(r"\frac{12x}{12} = x, \qquad "
                             r"\frac{36}{12} = 3", EQUATION_SIZE),
                      fraction=0.45)
            t.hold()

        with self.beat("mcq6_answer") as t:
            self.final(t, tex(r"12(x+3)", DISPLAY_SIZE * 0.9, SAGE))
            t.hold()

        with self.beat("mcq6_check") as t:
            self.step(t, tex(r"12 \cdot x + 12 \cdot 3 = 12x + 36",
                             EQUATION_SIZE, GREY), fraction=0.45)
            t.hold()

    # ------------------------------------------------------ short questions

    def sq_rationals(self):
        with self.beat("sq1") as t:
            self.wipe(t)
            self.part(t, 2)
            self.ask(t, tex(r"\text{Two rational numbers between }"
                            r"2 \text{ and } 3", EQUATION_SIZE),
                     title="Short question")
            t.hold()

        with self.beat("sq1_pick") as t:
            self.step(t, tex(r"2.25 \quad \text{and} \quad 2.5",
                             EQUATION_SIZE), fraction=0.45)
            t.hold()

        with self.beat("sq1_fractions") as t:
            self.step(t, tex(r"2.25 = \frac{9}{4}, \qquad 2.5 = \frac{5}{2}",
                             EQUATION_SIZE), fraction=0.45)
            t.hold()

        with self.beat("sq1_answer") as t:
            self.final(t, tex(r"\frac{9}{4} \quad \text{and} \quad "
                              r"\frac{5}{2}", DISPLAY_SIZE * 0.8, SAGE))
            t.hold()

        with self.beat("sq1_note") as t:
            note = self.lines("many answers are correct —",
                              "each must be rational, and strictly between",
                              size=LABEL_SIZE, color=GREY)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.45))
            t.hold()

    def sq_indices(self):
        with self.beat("sq2") as t:
            self.ask(t, tex(r"\left(\tfrac34\right)^{-2} \div "
                            r"\left(\tfrac49\right)^{3} \times "
                            r"\tfrac{16}{27}", DISPLAY_SIZE * 0.9),
                     title="Simplify")
            t.hold()

        with self.beat("sq2_negative") as t:
            self.step(t, tex(r"\left(\tfrac34\right)^{-2} = "
                             r"\left(\tfrac43\right)^{2} = \tfrac{16}{9}",
                             EQUATION_SIZE), fraction=0.45)
            t.hold()

        with self.beat("sq2_cube") as t:
            self.step(t, tex(r"\left(\tfrac49\right)^{3} = \tfrac{64}{729}",
                             EQUATION_SIZE), fraction=0.45)
            t.hold()

        with self.beat("sq2_divide") as t:
            self.step(t, tex(r"\tfrac{16}{9} \times \tfrac{729}{64} "
                             r"\times \tfrac{16}{27}", EQUATION_SIZE),
                      fraction=0.45)
            t.hold()

        with self.beat("sq2_cancel") as t:
            self.step(t, tex(r"\tfrac{729}{27} = 27, \qquad "
                             r"\tfrac{16}{64} = \tfrac14", EQUATION_SIZE,
                             SLATE), fraction=0.45)
            t.hold()

        with self.beat("sq2_answer") as t:
            self.final(t, tex(r"12", DISPLAY_SIZE, SAGE))
            t.hold()

    def sq_logarithm(self):
        with self.beat("sq3") as t:
            self.ask(t, tex(r"\log_{10} x = -3", DISPLAY_SIZE),
                     title="Find x")
            t.hold()

        with self.beat("sq3_rewrite") as t:
            self.step(t, tex(r"x = 10^{-3}", EQUATION_SIZE), fraction=0.45)
            t.hold()

        with self.beat("sq3_answer") as t:
            self.final(t, tex(r"x = \frac{1}{1000} = 0.001",
                              DISPLAY_SIZE * 0.8, SAGE))
            t.hold()

    def sq_characteristic(self):
        with self.beat("sq4") as t:
            self.ask(t, tex(r"0.000049", DISPLAY_SIZE),
                     title="Find the characteristic")
            t.hold()

        with self.beat("sq4_rule") as t:
            self.step(t, self.sol.note("a positive number below 1 has a "
                                       "negative characteristic"),
                      fraction=0.45)
            t.hold()

        with self.beat("sq4_move") as t:
            self.step(t, tex(r"0.000049 = 4.9 \times 10^{-5}",
                             EQUATION_SIZE), fraction=0.45)
            t.hold()

        with self.beat("sq4_answer") as t:
            self.final(t, tex(r"\text{characteristic} = -5 = \bar{5}",
                              DISPLAY_SIZE * 0.75, SAGE))
            t.hold()

        with self.beat("sq4_note") as t:
            note = self.caption("characteristic negative, mantissa positive",
                                GREY, LABEL_SIZE)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.45))
            t.hold()

    def sq_power_set(self):
        with self.beat("sq5") as t:
            self.wipe(t)
            self.title(t, "Write the power set", fraction=0.1)
            problem = fit(tex(r"\{\,+,\; -,\; \times,\; \div\,\}",
                              DISPLAY_SIZE * 0.9))
            self.stack(VGroup(problem), self.head, buff=GAP_MD)
            self.play(Write(problem), run_time=t.fill(0.35))
            self.problem = problem
            t.hold()

        with self.beat("sq5_count") as t:
            count = fit(tex(r"4 \text{ elements} \;\Rightarrow\; 2^4 = 16"
                            r"\text{ subsets}", EQUATION_SIZE, SLATE))
            self.stack(VGroup(count), self.problem, buff=GAP_MD)
            self.play(Write(count), run_time=t.fill(0.45))
            self.count = count
            t.hold()

        with self.beat("sq5_list") as t:
            grid = subset_grid(POWER_SET, size=LABEL_SIZE)
            self.hide(grid)
            self.stack(grid, self.count, buff=GAP_MD * 0.9)
            self.reveal(t, grid, 0, len(POWER_SET), 0.15)
            self.grid = grid
            t.hold()

        with self.beat("sq5_sum") as t:
            total = fit(tex(r"1 + 4 + 6 + 4 + 1 = 16", EQUATION_SIZE,
                            TERRACOTTA))
            self.foot(total)
            self.play(Write(total), run_time=t.fill(0.45))
            t.hold()

    def sq_difference(self):
        with self.beat("sq6") as t:
            self.ask(t, tex(r"A - B", DISPLAY_SIZE), title="Define")
            t.hold()

        with self.beat("sq6_words") as t:
            self.step(t, self.sol.note("the elements of A that are not in B",
                                       size=BODY_SIZE, color=CHARCOAL),
                      fraction=0.45)
            t.hold()

        with self.beat("sq6_builder") as t:
            self.step(t, tex(r"A - B = \{\, x \mid x \in A "
                             r"\text{ and } x \notin B \,\}",
                             EQUATION_SIZE), fraction=0.45)
            t.hold()

        with self.beat("sq6_example") as t:
            self.step(t, tex(r"A = \{1,2,3,4\}, \quad B = \{3,4,5\}",
                             EQUATION_SIZE, SLATE), fraction=0.45)
            t.hold()

        with self.beat("sq6_answer") as t:
            self.final(t, tex(r"A - B = \{1, 2\}", DISPLAY_SIZE * 0.8, SAGE))
            t.hold()

    def sq_quadratic(self):
        with self.beat("sq7") as t:
            self.ask(t, tex(r"x^2 + x - 12", DISPLAY_SIZE),
                     title="Factorize")
            t.hold()

        with self.beat("sq7_find") as t:
            self.step(t, tex(r"\text{product } -12, \quad \text{sum } +1",
                             EQUATION_SIZE, SLATE), fraction=0.45)
            t.hold()

        with self.beat("sq7_numbers") as t:
            self.step(t, tex(r"4 \times (-3) = -12, \quad 4 + (-3) = 1",
                             EQUATION_SIZE), fraction=0.45)
            t.hold()

        with self.beat("sq7_split") as t:
            self.step(t, tex(r"x^2 + 4x - 3x - 12", EQUATION_SIZE),
                      fraction=0.45)
            t.hold()

        with self.beat("sq7_group") as t:
            self.step(t, tex(r"x(x+4) - 3(x+4)", EQUATION_SIZE),
                      fraction=0.45)
            t.hold()

        with self.beat("sq7_answer") as t:
            self.final(t, tex(r"(x+4)(x-3)", DISPLAY_SIZE * 0.9, SAGE))
            t.hold()

    def sq_cubes(self):
        with self.beat("sq8") as t:
            self.ask(t, tex(r"125a^3 - 1", DISPLAY_SIZE), title="Factorize")
            t.hold()

        with self.beat("sq8_cubes") as t:
            self.step(t, tex(r"125a^3 = (5a)^3, \qquad 1 = 1^3",
                             EQUATION_SIZE), fraction=0.45)
            t.hold()

        with self.beat("sq8_identity") as t:
            self.step(t, tex(r"a^3 - b^3 = (a-b)(a^2 + ab + b^2)",
                             EQUATION_SIZE, SLATE), fraction=0.45)
            t.hold()

        with self.beat("sq8_answer") as t:
            self.final(t, tex(r"(5a-1)(25a^2 + 5a + 1)", DISPLAY_SIZE * 0.75,
                              SAGE))
            t.hold()

    # ------------------------------------------------------- long questions

    def lq_indices(self):
        with self.beat("lq1") as t:
            self.wipe(t)
            self.part(t, 3)
            self.ask(t, tex(r"\frac{25^{3/2} \times 243^{3/5}}"
                            r"{16^{5/4} \times 8^{4/3}}", DISPLAY_SIZE),
                     title="Question 5(a) — simplify")
            t.hold()

        with self.beat("lq1_rule") as t:
            self.step(t, self.sol.note("a fractional power is a root, "
                                       "then a power"), fraction=0.4)
            t.hold()

        with self.beat("lq1_a") as t:
            self.step(t, tex(r"25^{3/2} = (\sqrt{25})^3 = 5^3 = 125",
                             EQUATION_SIZE), fraction=0.4)
            t.hold()

        with self.beat("lq1_b") as t:
            self.step(t, tex(r"243^{3/5} = (\sqrt[5]{243})^3 = 3^3 = 27",
                             EQUATION_SIZE), fraction=0.4)
            t.hold()

        with self.beat("lq1_c") as t:
            self.step(t, tex(r"16^{5/4} = (\sqrt[4]{16})^5 = 2^5 = 32",
                             EQUATION_SIZE), fraction=0.4)
            t.hold()

        with self.beat("lq1_d") as t:
            self.step(t, tex(r"8^{4/3} = (\sqrt[3]{8})^4 = 2^4 = 16",
                             EQUATION_SIZE), fraction=0.4)
            t.hold()

        with self.beat("lq1_combine") as t:
            self.step(t, tex(r"\frac{125 \times 27}{32 \times 16} = "
                             r"\frac{3375}{512}", EQUATION_SIZE),
                      fraction=0.4)
            t.hold()

        with self.beat("lq1_answer") as t:
            self.final(t, tex(r"\frac{3375}{512}", DISPLAY_SIZE * 0.85,
                              SAGE))
            t.hold()

    def lq_logarithm(self):
        with self.beat("lq2") as t:
            self.ask(t, tex(r"\log x = -2.0184", DISPLAY_SIZE),
                     title="Question 5(b) — find x")
            t.hold()

        with self.beat("lq2_undo") as t:
            self.step(t, tex(r"x = 10^{-2.0184}", EQUATION_SIZE),
                      fraction=0.45)
            t.hold()

        with self.beat("lq2_split") as t:
            self.step(t, tex(r"-2.0184 = -3 + 0.9816", EQUATION_SIZE, SLATE),
                      fraction=0.45)
            t.hold()

        with self.beat("lq2_parts") as t:
            self.step(t, tex(r"x = 10^{-3} \times 10^{\,0.9816}",
                             EQUATION_SIZE), fraction=0.45)
            t.hold()

        with self.beat("lq2_antilog") as t:
            self.step(t, tex(r"10^{\,0.9816} \approx 9.585", EQUATION_SIZE),
                      fraction=0.45)
            t.hold()

        with self.beat("lq2_answer") as t:
            self.final(t, tex(r"x \approx 0.00959", DISPLAY_SIZE * 0.85,
                              SAGE))
            t.hold()

    def lq_sets(self):
        with self.beat("lq3") as t:
            self.ask(t, tex(r"\text{98 students} \;:\; "
                            r"\text{58 swim}, \; \text{50 tug-of-war}",
                            EQUATION_SIZE),
                     title="Question 6(a) — how many did both?")
            t.hold()

        with self.beat("lq3_setup") as t:
            self.step(t, tex(r"A = \text{swimming}, \quad "
                             r"B = \text{tug-of-war}", EQUATION_SIZE, SLATE),
                      fraction=0.4)
            t.hold()

        with self.beat("lq3_formula") as t:
            self.step(t, tex(r"n(A\cup B) = n(A) + n(B) - n(A\cap B)",
                             EQUATION_SIZE), fraction=0.4)
            t.hold()

        with self.beat("lq3_substitute") as t:
            self.step(t, tex(r"98 = 58 + 50 - n(A\cap B)", EQUATION_SIZE),
                      fraction=0.4)
            t.hold()

        with self.beat("lq3_work") as t:
            self.step(t, tex(r"n(A\cap B) = 108 - 98", EQUATION_SIZE),
                      fraction=0.4)
            t.hold()

        with self.beat("lq3_answer") as t:
            self.final(t, tex(r"10 \text{ students did both}",
                              EQUATION_SIZE * 1.1, SAGE))
            t.hold()

    def lq_quartic(self):
        with self.beat("lq4") as t:
            self.ask(t, tex(r"x^4 - 30x^2y^2 + 9y^4", DISPLAY_SIZE),
                     title="Question 6(b) — factorize")
            t.hold()

        with self.beat("lq4_rewrite") as t:
            self.step(t, tex(r"= (x^2 + 3y^2)^2 - (6xy)^2", EQUATION_SIZE,
                             SLATE), fraction=0.4)
            t.hold()

        with self.beat("lq4_expand") as t:
            self.step(t, tex(r"(x^2+3y^2)^2 = x^4 + 6x^2y^2 + 9y^4",
                             EQUATION_SIZE), fraction=0.4)
            t.hold()

        with self.beat("lq4_check") as t:
            self.step(t, tex(r"6x^2y^2 - 36x^2y^2 = -30x^2y^2",
                             EQUATION_SIZE), fraction=0.4)
            t.hold()

        with self.beat("lq4_identity") as t:
            self.step(t, tex(r"A^2 - B^2 = (A-B)(A+B)", EQUATION_SIZE,
                             SLATE), fraction=0.4)
            t.hold()

        with self.beat("lq4_answer") as t:
            self.final(t, tex(r"(x^2+3y^2-6xy)(x^2+3y^2+6xy)",
                              EQUATION_SIZE * 1.1, SAGE))
            t.hold()

    # ------------------------------------------------------------- closing

    def closing(self):
        with self.beat("recap") as t:
            self.wipe(t)
            self.title(t, "What we practised", fraction=0.1)
            rows = self.lines("conjugates",
                              "common logarithms",
                              "power sets, and set overlap",
                              "LCM and factorization",
                              "fractional indices",
                              size=BODY_SIZE, color=CHARCOAL, align=LEFT)
            self.hide(rows)
            self.stack(rows, self.head, buff=GAP_MD, align=LEFT)
            self.reveal(t, rows, 0, 5, 0.14)
            t.hold()

        with self.beat("practise") as t:
            self.wipe(t)
            rows = self.lines("Try these again without the solutions.",
                              "If you get stuck, pause at that step",
                              "and name the rule you need.",
                              size=BODY_SIZE, color=CHARCOAL)
            rows.move_to(UP * 0.3)
            self.play(Write(rows), run_time=t.fill(0.5))
            t.hold()

        with self.beat("next") as t:
            self.wipe(t)
            note = self.caption("Video 2: the next chapter group",
                                CHARCOAL, TITLE_SIZE)
            note.move_to(UP * 0.4)
            self.play(Write(note), run_time=t.fill(0.45))
            t.hold()

        with self.beat("close") as t:
            self.wipe(t)
            name = fit(serif("The Digital Tutor", TITLE_SIZE * 1.2, CHARCOAL))
            motto = serif("Learn today. Lead tomorrow.", BODY_SIZE,
                          TERRACOTTA)
            card = VGroup(name, motto).arrange(DOWN, buff=GAP_LG * 0.8)
            card.move_to(ORIGIN)
            self.play(Write(name), run_time=t.fill(0.3))
            self.play(Write(motto), run_time=t.fill(0.25))
            t.hold()
