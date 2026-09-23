"""CS lecture: Introduction to Systems (Punjab Board Grade 9, Chapter 1).

Narration script: scripts/CS02-intro-to-systems.md

The chapter is one idea repeated at different scales, so the visuals lean
on five anchors the student should leave holding:

    SYSTEM = parts + purpose
    OCEC   = Objective, Components, Environment, Communication
    natural = exists  |  artificial = designed
    DAC    = Data, Address, Control bus
    FDES   = Fetch, Decode, Execute, Store

The three ordered anchors run through WordArc so the student can see which
step of a sequence is being explained.
"""

import numpy as np

from manim import (
    Arrow,
    Create,
    FadeIn,
    FadeOut,
    Line,
    Polygon,
    Rectangle,
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
from components.word_arc import WordArc
from scenes.base import SATScene

OCEC = ["Objective", "Components", "Environment", "Communication"]
DAC = ["Data bus", "Address bus", "Control bus"]
FDES = ["Fetch", "Decode", "Execute", "Store"]
FRAME_SAFE = 12.6


def fit(mobject, width=FRAME_SAFE):
    if mobject.width > width:
        mobject.scale_to_fit_width(width)
    return mobject


def lines(*texts, size=BODY_SIZE, color=CHARCOAL, buff=GAP_SM * 1.3,
          align=None):
    group = VGroup(*[fit(serif(t, size, color)) for t in texts])
    if align is None:
        group.arrange(DOWN, buff=buff)
    else:
        group.arrange(DOWN, buff=buff, aligned_edge=align)
    return group


def box(text, width=3.0, height=1.1, color=SLATE, size=LABEL_SIZE):
    rect = Rectangle(width=width, height=height, color=color,
                     stroke_width=3)
    label = serif(text, size)
    if label.width > width - 0.3:
        label.scale_to_fit_width(width - 0.3)
    label.move_to(rect)
    return VGroup(rect, label)


class IntroToSystems(SATScene):
    scene_id = "cs.intro_to_systems"

    def construct(self):
        self.margin_note = mono("Grade 9 CS · Ch 1 · systems", MARGIN_SIZE)
        self.margin_note.to_corner(UP + LEFT, buff=GAP_SM)
        self.add(self.margin_note)
        self.section_head = None

        self.opening()
        self.systems_theory()
        self.ocec_detail()
        self.characteristics()
        self.natural_artificial()
        self.science()
        self.computer_as_system()
        self.buses_section()
        self.von_neumann()
        self.vn_properties()
        self.computing_systems()
        self.recap()
        self.closing()

    # -------------------------------------------------------------- helpers

    def clear_all(self, t, fraction=0.06):
        old = [m for m in self.mobjects if m is not self.margin_note]
        if old:
            self.play(*[FadeOut(m) for m in old], run_time=t.fill(fraction))
        self.section_head = None

    def set_head(self, t, text, fraction=0.09):
        head = fit(serif(text, TITLE_SIZE))
        head.to_edge(UP, buff=GAP_MD * 1.4)
        self.play(Write(head), run_time=t.fill(fraction))
        self.section_head = head
        return head

    def below_head(self, mobject, buff=GAP_MD * 1.4):
        if self.section_head is None:
            mobject.move_to(ORIGIN)
        else:
            mobject.next_to(self.section_head, DOWN, buff=buff)
        return mobject

    def underline(self, mobject, color=SAGE):
        return Line(
            mobject.get_corner(DOWN + LEFT) + DOWN * GAP_SM,
            mobject.get_corner(DOWN + RIGHT) + DOWN * GAP_SM,
            color=color, stroke_width=3,
        )

    def arc(self, t, words, index, fraction=0.1, size=LABEL_SIZE):
        bar = WordArc(words, size=size, lit=CHARCOAL)
        bar.to_edge(DOWN, buff=GAP_MD * 0.9)
        self.play(FadeIn(bar), *bar.focus(index), run_time=t.fill(fraction))
        return bar

    def bullets(self, t, items, per=0.12, size=BODY_SIZE, color=CHARCOAL,
                buff=GAP_SM * 1.3):
        group = lines(*items, size=size, color=color, buff=buff,
                      align=LEFT)
        self.below_head(group)
        for item in group:
            self.play(Write(item), run_time=t.fill(per))
        return group

    # ------------------------------------------------------------- sections

    def opening(self):
        with self.beat("open") as t:
            title = lines("Introduction to Systems", size=TITLE_SIZE * 1.3)
            title.move_to(UP * 1.2)
            sub = serif("Grade 9 Computer Science · Chapter 1",
                        BODY_SIZE, GREY)
            sub.next_to(title, DOWN, buff=GAP_MD * 1.2)
            note = serif("we don't begin with computers — "
                         "we begin with something bigger",
                         LABEL_SIZE, TERRACOTTA)
            fit(note)
            note.next_to(sub, DOWN, buff=GAP_MD * 1.8)
            self.play(Write(title), run_time=t.fill(0.25))
            self.play(Write(sub), run_time=t.fill(0.15))
            self.play(Write(note), run_time=t.fill(0.25))
            t.hold()

        with self.beat("everything_system") as t:
            self.clear_all(t)
            self.set_head(t, "Everything around you is a system")
            items = self.bullets(t, [
                "your school", "your family", "a car or motorcycle",
                "the human body", "your mobile phone", "the internet",
                "a computer",
            ], per=0.08)
            t.hold()

        with self.beat("system_def") as t:
            self.clear_all(t)
            defn = lines("A system is a collection of",
                         "interconnected components that work",
                         "together to achieve a common objective.",
                         size=TITLE_SIZE * 0.95)
            defn.move_to(UP * 0.3)
            self.play(Write(defn), run_time=t.fill(0.55))
            self.play(Create(self.underline(defn)), run_time=t.fill(0.12))
            t.hold()

        with self.beat("parts_purpose") as t:
            self.clear_all(t)
            anchor = serif("PARTS  +  PURPOSE", TITLE_SIZE * 1.5,
                           TERRACOTTA)
            anchor.move_to(UP * 0.8)
            rules = lines("no parts — no system",
                          "no purpose — no meaningful system",
                          size=BODY_SIZE, color=GREY)
            rules.next_to(anchor, DOWN, buff=GAP_MD * 1.8)
            self.play(Write(anchor), run_time=t.fill(0.3))
            self.play(Write(rules), run_time=t.fill(0.3))
            t.hold()

        with self.beat("car_parts") as t:
            self.clear_all(t)
            self.set_head(t, "Parts in a room")
            rng = np.random.default_rng(3)
            parts = VGroup()
            for name in ("engine", "tyres", "steering wheel", "battery"):
                label = serif(name, LABEL_SIZE, GREY)
                label.move_to(np.array([rng.uniform(-4.2, 4.2),
                                        rng.uniform(-1.8, 0.8), 0]))
                parts.add(label)
            room = Rectangle(width=11.0, height=4.2, color=SLATE,
                             stroke_width=3)
            room.move_to(DOWN * 0.5)
            ask = serif("do I have a car?  No — I have components.",
                        BODY_SIZE, TERRACOTTA)
            fit(ask)
            ask.next_to(room, DOWN, buff=GAP_MD * 1.1)
            self.play(Create(room), run_time=t.fill(0.15))
            self.play(Write(parts), run_time=t.fill(0.3))
            self.play(Write(ask), run_time=t.fill(0.25))
            t.hold()

        with self.beat("car_objective") as t:
            self.clear_all(t)
            self.set_head(t, "What turns parts into a system?")
            needs = self.bullets(t, [
                "they must be connected",
                "they must interact",
                "they must work toward an objective",
            ], per=0.15)
            obj = serif("the car's objective: transportation",
                        BODY_SIZE, TERRACOTTA)
            obj.next_to(needs, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(obj), run_time=t.fill(0.22))
            t.hold()

        with self.beat("computer_parts") as t:
            self.clear_all(t)
            self.set_head(t, "None of these alone is the computer")
            grid = VGroup(*[
                box(name, width=3.1, height=0.95)
                for name in ("keyboard", "mouse", "CPU", "memory",
                             "storage", "monitor", "operating system",
                             "applications")
            ]).arrange_in_grid(rows=2, cols=4, buff=(GAP_MD, GAP_MD))
            fit(grid)
            self.below_head(grid, buff=GAP_MD * 1.6)
            self.play(Create(grid), run_time=t.fill(0.4))
            t.hold()

        with self.beat("together") as t:
            self.clear_all(t)
            self.set_head(t, "Press one key")
            flow = VGroup(*[
                box(name, width=2.5, height=1.0)
                for name in ("input", "processor", "memory", "monitor")
            ]).arrange(RIGHT, buff=GAP_MD * 1.5)
            fit(flow)
            self.below_head(flow, buff=GAP_MD * 1.8)
            arrows = VGroup(*[
                Arrow(flow[i].get_right(), flow[i + 1].get_left(),
                      color=GREY, stroke_width=3, buff=0.12,
                      max_tip_length_to_length_ratio=0.2)
                for i in range(3)
            ])
            idea = serif("parts working together for a purpose",
                         BODY_SIZE, TERRACOTTA)
            idea.next_to(flow, DOWN, buff=GAP_MD * 1.8)
            self.play(Create(flow), run_time=t.fill(0.3))
            self.play(Create(arrows), run_time=t.fill(0.15))
            self.play(Write(idea), run_time=t.fill(0.25))
            t.hold()

    def systems_theory(self):
        with self.beat("systems_theory") as t:
            self.clear_all(t)
            self.set_head(t, "Systems theory")
            idea = lines("study complicated things as systems:",
                         "their parts, their relationships,",
                         "how they interact, how they change",
                         size=BODY_SIZE)
            self.below_head(idea, buff=GAP_MD * 1.4)
            ask = serif("not: how does this one part work?",
                        LABEL_SIZE, GREY)
            ask2 = serif("but: how does everything work together?",
                         BODY_SIZE, TERRACOTTA)
            pair = VGroup(ask, ask2).arrange(DOWN, buff=GAP_SM * 1.4)
            pair.next_to(idea, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(idea), run_time=t.fill(0.35))
            self.play(Write(pair), run_time=t.fill(0.3))
            t.hold()

        with self.beat("body_example") as t:
            self.clear_all(t)
            self.set_head(t, "A doctor cannot study only the heart")
            parts = self.bullets(t, [
                "the heart interacts with blood vessels",
                "the lungs provide oxygen",
                "the nervous system sends signals",
                "the digestive system provides nutrients",
                "the brain coordinates activities",
            ], per=0.1)
            why = serif("the body works because its subsystems interact",
                        BODY_SIZE, TERRACOTTA)
            fit(why)
            why.next_to(parts, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(why), run_time=t.fill(0.25))
            t.hold()

        with self.beat("ocec") as t:
            self.clear_all(t)
            words = VGroup(*[
                serif(w, TITLE_SIZE * 1.1) for w in OCEC
            ]).arrange(DOWN, buff=GAP_MD * 0.9)
            words.move_to(UP * 0.5)
            for word in words:
                self.play(Write(word), run_time=t.fill(0.12))
            anchor = serif("O · C · E · C", TITLE_SIZE * 1.2, TERRACOTTA)
            anchor.next_to(words, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(anchor), run_time=t.fill(0.25))
            t.hold()

    def ocec_detail(self):
        with self.beat("objective") as t:
            self.clear_all(t)
            self.set_head(t, "Objective — the purpose")
            rows = self.bullets(t, [
                "a vehicle → transportation",
                "a thermostat → keep the room at 26°C",
                "a computer → process data, perform tasks",
                "a school → provide education",
            ], per=0.1)
            ask = serif("always ask: what is this system trying "
                        "to accomplish?", LABEL_SIZE, GREY)
            fit(ask)
            ask.next_to(rows, DOWN, buff=GAP_MD * 1.3)
            self.play(Write(ask), run_time=t.fill(0.2))
            self.arc(t, OCEC, 0)
            t.hold()

        with self.beat("objective_cats") as t:
            self.clear_all(t)
            self.set_head(t, "Three kinds of objective")
            rows = self.bullets(t, [
                "information processing — a computer, your brain",
                "supporting another system — a phone hosting apps",
                "achieving a specific goal — a thermostat, an engine",
            ], per=0.18)
            t.hold()

        with self.beat("no_destination") as t:
            self.clear_all(t)
            idea = lines("A system without an objective",
                         "is like a journey without a destination.",
                         size=TITLE_SIZE)
            idea.move_to(UP * 0.2)
            self.play(Write(idea), run_time=t.fill(0.5))
            self.play(Create(self.underline(idea, TERRACOTTA)),
                      run_time=t.fill(0.15))
            t.hold()

        with self.beat("components") as t:
            self.clear_all(t)
            self.set_head(t, "Components — the building blocks")
            team = lines("goalkeeper · defenders · midfielders · forwards",
                         size=BODY_SIZE, color=GREY)
            self.below_head(team, buff=GAP_MD * 1.2)
            comp = lines("keyboard · CPU · RAM · storage · monitor",
                         size=BODY_SIZE)
            comp.next_to(team, DOWN, buff=GAP_MD * 1.5)
            idea = serif("different jobs — one system", BODY_SIZE,
                         TERRACOTTA)
            idea.next_to(comp, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(team), run_time=t.fill(0.25))
            self.play(Write(comp), run_time=t.fill(0.25))
            self.play(Write(idea), run_time=t.fill(0.2))
            self.arc(t, OCEC, 1)
            t.hold()

        with self.beat("environment") as t:
            self.clear_all(t)
            self.set_head(t, "Environment — everything outside")
            outer = Rectangle(width=9.5, height=4.4, color=GREY,
                              stroke_width=3)
            inner = Rectangle(width=5.0, height=2.2, color=SLATE,
                              stroke_width=4)
            group = VGroup(outer, inner)
            inner.move_to(outer)
            self.below_head(group, buff=GAP_MD * 1.4)
            sys_label = serif("the system", BODY_SIZE)
            sys_label.move_to(inner)
            env_label = serif("the environment", LABEL_SIZE, GREY)
            env_label.next_to(outer.get_top(), DOWN, buff=GAP_SM * 1.2)
            self.play(Create(outer), Write(env_label),
                      run_time=t.fill(0.22))
            self.play(Create(inner), Write(sys_label),
                      run_time=t.fill(0.22))
            note = serif("inside and outside — but the two interact",
                         BODY_SIZE, TERRACOTTA)
            note.next_to(outer, DOWN, buff=GAP_MD * 1.1)
            self.play(Write(note), run_time=t.fill(0.22))
            t.hold()

        with self.beat("env_examples") as t:
            self.clear_all(t)
            self.set_head(t, "A computer's environment")
            rows = self.bullets(t, [
                "the user", "electricity", "the network connection",
                "external devices",
            ], per=0.09)
            zoom = lines("we are on Zoom right now —",
                         "no power or no internet, and we cannot talk",
                         size=LABEL_SIZE, color=GREY)
            zoom.next_to(rows, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(zoom), run_time=t.fill(0.3))
            self.arc(t, OCEC, 2)
            t.hold()

        with self.beat("communication") as t:
            self.clear_all(t)
            self.set_head(t, "Communication — or nothing happens")
            story = lines("the keyboard detects the letter A",
                          "but cannot tell the computer",
                          size=BODY_SIZE)
            self.below_head(story, buff=GAP_MD * 1.3)
            nothing = serif("result: nothing", BODY_SIZE, TERRACOTTA)
            nothing.next_to(story, DOWN, buff=GAP_MD * 1.3)
            carriers = lines("in the body — nerves carry signals",
                             "in a computer — buses and circuits",
                             "in a network — cables, wireless, protocols",
                             size=LABEL_SIZE, color=GREY)
            carriers.next_to(nothing, DOWN, buff=GAP_MD * 1.3)
            self.play(Write(story), run_time=t.fill(0.22))
            self.play(Write(nothing), run_time=t.fill(0.12))
            self.play(Write(carriers), run_time=t.fill(0.25))
            self.arc(t, OCEC, 3)
            t.hold()

    def characteristics(self):
        with self.beat("static_dynamic") as t:
            self.clear_all(t)
            self.set_head(t, "Static or dynamic?")
            left = lines("static", "the environment does not",
                         "change by itself", size=BODY_SIZE, color=GREY)
            right = lines("dynamic", "the environment can",
                          "change independently", size=BODY_SIZE)
            pair = VGroup(left, right).arrange(RIGHT, buff=GAP_MD * 3.4)
            fit(pair)
            self.below_head(pair, buff=GAP_MD * 1.8)
            self.play(Write(left), run_time=t.fill(0.28))
            self.play(Write(right), run_time=t.fill(0.28))
            t.hold()

        with self.beat("weather") as t:
            self.clear_all(t)
            self.set_head(t, "Weather is highly dynamic")
            rows = self.bullets(t, [
                "temperature changes", "humidity changes",
                "wind changes", "rain begins and stops",
            ], per=0.1)
            note = serif("a weather system must respond continuously",
                         BODY_SIZE, TERRACOTTA)
            fit(note)
            note.next_to(rows, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(note), run_time=t.fill(0.25))
            t.hold()

        with self.beat("deterministic") as t:
            self.clear_all(t)
            self.set_head(t, "Deterministic or non-deterministic?")
            left = lines("deterministic", "predictable —", "known result",
                         size=BODY_SIZE)
            right = lines("non-deterministic", "uncertainty",
                          "or randomness", size=BODY_SIZE, color=GREY)
            pair = VGroup(left, right).arrange(RIGHT, buff=GAP_MD * 3.4)
            fit(pair)
            self.below_head(pair, buff=GAP_MD * 1.8)
            self.play(Write(left), run_time=t.fill(0.28))
            self.play(Write(right), run_time=t.fill(0.28))
            t.hold()

        with self.beat("d_definite") as t:
            self.clear_all(t)
            trick = lines("Deterministic  =  Definite",
                          size=TITLE_SIZE * 1.3)
            trick.move_to(UP * 0.5)
            both = serif("both begin with D", BODY_SIZE, TERRACOTTA)
            both.next_to(trick, DOWN, buff=GAP_MD * 1.6)
            self.play(Write(trick), run_time=t.fill(0.4))
            self.play(Write(both), run_time=t.fill(0.25))
            t.hold()

        with self.beat("dont_confuse") as t:
            self.clear_all(t)
            self.set_head(t, "Don't confuse the two pairs")
            rows = lines("static / dynamic  —  does the environment change?",
                         "deterministic / non-deterministic  —  "
                         "can we predict the result?",
                         size=BODY_SIZE, buff=GAP_MD)
            self.below_head(rows, buff=GAP_MD * 1.8)
            self.play(Write(rows[0]), run_time=t.fill(0.25))
            self.play(Write(rows[1]), run_time=t.fill(0.25))
            marks = serif("that distinction can save you marks",
                          LABEL_SIZE, TERRACOTTA)
            marks.next_to(rows, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(marks), run_time=t.fill(0.18))
            t.hold()

    def natural_artificial(self):
        with self.beat("natural_artificial") as t:
            self.clear_all(t)
            ask = serif("Who made it?", TITLE_SIZE * 1.4, TERRACOTTA)
            ask.move_to(UP * 1.5)
            pair = VGroup(
                lines("natural", "it exists without us", size=BODY_SIZE),
                lines("artificial", "humans designed it", size=BODY_SIZE),
            ).arrange(RIGHT, buff=GAP_MD * 4)
            pair.next_to(ask, DOWN, buff=GAP_MD * 1.8)
            self.play(Write(ask), run_time=t.fill(0.3))
            self.play(Write(pair), run_time=t.fill(0.35))
            t.hold()

        with self.beat("natural_kinds") as t:
            self.clear_all(t)
            self.set_head(t, "Natural systems")
            rows = self.bullets(t, [
                "physical — atoms, stars, planets, galaxies",
                "chemical — hydrogen and oxygen becoming H₂O",
                "biological — cells, organs, plants, animals, the body",
                "psychological — mind, behaviour, thoughts, emotions",
            ], per=0.15)
            t.hold()

        with self.beat("levels") as t:
            self.clear_all(t)
            self.set_head(t, "Think of it as levels")
            ladder = WordArc(["matter", "chemistry", "life", "mind"],
                             size=TITLE_SIZE, lit=CHARCOAL)
            for cell in ladder.cells:
                cell.set_color(CHARCOAL)
            self.below_head(ladder, buff=GAP_MD * 1.8)
            under = serif("physical → chemical → biological → "
                          "psychological", LABEL_SIZE, GREY)
            fit(under)
            under.next_to(ladder, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(ladder), run_time=t.fill(0.35))
            self.play(Write(under), run_time=t.fill(0.25))
            t.hold()

        with self.beat("artificial") as t:
            self.clear_all(t)
            defn = lines("Artificial systems are deliberately",
                         "designed and built by human beings",
                         "to perform functions or solve problems.",
                         size=BODY_SIZE * 1.05)
            defn.move_to(UP * 0.2)
            self.play(Write(defn), run_time=t.fill(0.5))
            t.hold()

        with self.beat("artificial_kinds") as t:
            self.clear_all(t)
            groups = VGroup(*[
                box(name, width=3.6, height=1.3, size=BODY_SIZE)
                for name in ("knowledge", "engineering", "social")
            ]).arrange(RIGHT, buff=GAP_MD * 1.4)
            fit(groups)
            groups.move_to(UP * 0.3)
            self.play(Create(groups), run_time=t.fill(0.45))
            t.hold()

        with self.beat("knowledge") as t:
            self.clear_all(t)
            self.set_head(t, "Knowledge systems")
            rows = self.bullets(t, [
                "mathematics", "logic", "databases",
                "information management systems",
            ], per=0.1)
            lib = lines("a library database — thousands of books",
                        "without organization, information is unusable",
                        size=LABEL_SIZE, color=GREY)
            lib.next_to(rows, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(lib), run_time=t.fill(0.3))
            t.hold()

        with self.beat("engineering") as t:
            self.clear_all(t)
            self.set_head(t, "Engineering systems")
            rows = self.bullets(t, [
                "a bridge", "a water treatment plant",
                "a robotic arm in a factory", "a home automation system",
            ], per=0.1)
            idea = serif("engineering takes knowledge and builds solutions",
                         BODY_SIZE, TERRACOTTA)
            fit(idea)
            idea.next_to(rows, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(idea), run_time=t.fill(0.25))
            t.hold()

        with self.beat("social") as t:
            self.clear_all(t)
            self.set_head(t, "Social systems")
            rows = self.bullets(t, [
                "a school", "a university", "a government",
                "a corporation",
            ], per=0.09)
            each = serif("each has people · roles · rules · objectives",
                         BODY_SIZE, GREY)
            fit(each)
            each.next_to(rows, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(each), run_time=t.fill(0.25))
            t.hold()

        with self.beat("systems_thinking") as t:
            self.clear_all(t)
            idea = lines("A system does not have to contain",
                         "wires and processors.", size=TITLE_SIZE)
            idea.move_to(UP * 0.8)
            examples = serif("a university · a country · the internet · "
                             "your body", BODY_SIZE, GREY)
            fit(examples)
            examples.next_to(idea, DOWN, buff=GAP_MD * 1.6)
            why = serif("this is why systems thinking is powerful",
                        BODY_SIZE, TERRACOTTA)
            why.next_to(examples, DOWN, buff=GAP_MD * 1.3)
            self.play(Write(idea), run_time=t.fill(0.32))
            self.play(Write(examples), run_time=t.fill(0.2))
            self.play(Write(why), run_time=t.fill(0.2))
            t.hold()

    def science(self):
        with self.beat("science") as t:
            self.clear_all(t)
            self.set_head(t, "Systems and science")
            pair = VGroup(
                serif("Natural science", TITLE_SIZE),
                serif("Design science", TITLE_SIZE),
            ).arrange(RIGHT, buff=GAP_MD * 3.6)
            fit(pair)
            self.below_head(pair, buff=GAP_MD * 2.0)
            self.play(Write(pair[0]), run_time=t.fill(0.25))
            self.play(Write(pair[1]), run_time=t.fill(0.25))
            t.hold()

        with self.beat("understand_create") as t:
            self.clear_all(t)
            left = lines("Natural science", "studies what exists",
                         size=BODY_SIZE, color=GREY)
            right = lines("Design science", "creates what should exist",
                          size=BODY_SIZE)
            pair = VGroup(left, right).arrange(RIGHT, buff=GAP_MD * 3.2)
            fit(pair)
            pair.move_to(UP * 0.8)
            verbs = lines("understand", "create", size=TITLE_SIZE)
            verbs[0].set_color(GREY)
            verbs[1].set_color(TERRACOTTA)
            verbs.arrange(RIGHT, buff=GAP_MD * 5.4)
            verbs.next_to(pair, DOWN, buff=GAP_MD * 1.8)
            self.play(Write(pair), run_time=t.fill(0.35))
            self.play(Write(verbs), run_time=t.fill(0.3))
            t.hold()

        with self.beat("forest") as t:
            self.clear_all(t)
            self.set_head(t, "Scientists enter a forest")
            left = lines("study how species interact",
                         "→ natural science", size=BODY_SIZE, color=GREY)
            right = lines("build software to monitor it",
                          "→ design science", size=BODY_SIZE)
            pair = VGroup(left, right).arrange(RIGHT, buff=GAP_MD * 2.6)
            fit(pair)
            self.below_head(pair, buff=GAP_MD * 1.6)
            kinds = serif("descriptive  ·  prescriptive", BODY_SIZE,
                          TERRACOTTA)
            kinds.next_to(pair, DOWN, buff=GAP_MD * 1.6)
            self.play(Write(left), run_time=t.fill(0.25))
            self.play(Write(right), run_time=t.fill(0.25))
            self.play(Write(kinds), run_time=t.fill(0.2))
            t.hold()

        with self.beat("cycles") as t:
            self.clear_all(t)
            self.set_head(t, "Two cycles")
            left = lines("empirical cycle", "observation", "question",
                         "hypothesis", "experiment", "analysis",
                         "conclusion", size=LABEL_SIZE, color=GREY,
                         buff=GAP_SM)
            right = lines("design cycle", "identify a problem",
                          "design a solution", "implement it",
                          "evaluate it", "improve it",
                          size=LABEL_SIZE, buff=GAP_SM)
            pair = VGroup(left, right).arrange(RIGHT, buff=GAP_MD * 3.6)
            fit(pair)
            self.below_head(pair, buff=GAP_MD * 1.3)
            self.play(Write(left), run_time=t.fill(0.3))
            self.play(Write(right), run_time=t.fill(0.3))
            t.hold()

        with self.beat("cs_fits") as t:
            self.clear_all(t)
            self.set_head(t, "Computer science uses both")
            left = lines("which sorting algorithm is faster?",
                         "which uses less memory?",
                         "→ understanding", size=LABEL_SIZE, color=GREY)
            right = lines("a language · an application",
                          "an algorithm · a database · an AI system",
                          "→ creating", size=LABEL_SIZE)
            pair = VGroup(left, right).arrange(RIGHT, buff=GAP_MD * 2.4)
            fit(pair)
            self.below_head(pair, buff=GAP_MD * 1.6)
            self.play(Write(left), run_time=t.fill(0.3))
            self.play(Write(right), run_time=t.fill(0.3))
            t.hold()

        with self.beat("not_just_using") as t:
            self.clear_all(t)
            idea = lines("Computer science is not",
                         "simply using computers.", size=TITLE_SIZE)
            idea.move_to(UP * 1.0)
            what = lines("understanding computation",
                         "and designing computational solutions",
                         size=BODY_SIZE, color=TERRACOTTA)
            what.next_to(idea, DOWN, buff=GAP_MD * 1.6)
            joke = serif("otherwise everyone on WhatsApp would be a "
                         "computer scientist", LABEL_SIZE, GREY)
            fit(joke)
            joke.next_to(what, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(idea), run_time=t.fill(0.3))
            self.play(Write(what), run_time=t.fill(0.25))
            self.play(Write(joke), run_time=t.fill(0.2))
            t.hold()

    def computer_as_system(self):
        with self.beat("computer_system") as t:
            self.clear_all(t)
            defn = lines("A computer is a complex system designed",
                         "to process data and perform tasks",
                         "according to instructions.", size=BODY_SIZE * 1.05)
            defn.move_to(UP * 1.2)
            checks = lines("it has an objective", "it has components",
                           "its components communicate",
                           "it operates in an environment",
                           size=LABEL_SIZE, color=SAGE, buff=GAP_SM)
            checks.next_to(defn, DOWN, buff=GAP_MD * 1.6)
            self.play(Write(defn), run_time=t.fill(0.4))
            self.play(Write(checks), run_time=t.fill(0.3))
            t.hold()

        with self.beat("computer_objective") as t:
            self.clear_all(t)
            self.set_head(t, "Its objective")
            obj = lines("process data · perform calculations",
                        "execute tasks efficiently", size=BODY_SIZE)
            self.below_head(obj, buff=GAP_MD * 1.5)
            examples = serif("a browser · a document · a video · a game",
                             LABEL_SIZE, GREY)
            examples.next_to(obj, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(obj), run_time=t.fill(0.35))
            self.play(Write(examples), run_time=t.fill(0.25))
            t.hold()

        with self.beat("interface_components") as t:
            self.clear_all(t)
            self.set_head(t, "Interface components")
            left = lines("input", "keyboard · mouse · microphone",
                         size=BODY_SIZE)
            right = lines("output", "monitor · printer", size=BODY_SIZE)
            pair = VGroup(left, right).arrange(RIGHT, buff=GAP_MD * 3.0)
            fit(pair)
            self.below_head(pair, buff=GAP_MD * 1.8)
            self.play(Write(left), run_time=t.fill(0.28))
            self.play(Write(right), run_time=t.fill(0.28))
            t.hold()

        with self.beat("cpu") as t:
            self.clear_all(t)
            self.set_head(t, "CPU — central processing unit")
            role = lines("the component responsible for",
                         "carrying out instructions", size=BODY_SIZE)
            self.below_head(role, buff=GAP_MD * 1.8)
            self.play(Write(role), run_time=t.fill(0.45))
            t.hold()

        with self.beat("ram") as t:
            self.clear_all(t)
            self.set_head(t, "RAM — random access memory")
            what = serif("holds what is being used right now",
                         BODY_SIZE, GREY)
            self.below_head(what, buff=GAP_MD * 1.3)
            anchor = lines("a working area —", "not a warehouse",
                           size=TITLE_SIZE)
            anchor.next_to(what, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(what), run_time=t.fill(0.2))
            self.play(Write(anchor), run_time=t.fill(0.35))
            self.play(Create(self.underline(anchor, TERRACOTTA)),
                      run_time=t.fill(0.12))
            t.hold()

        with self.beat("storage_os_apps") as t:
            self.clear_all(t)
            self.set_head(t, "Storage, OS and applications")
            rows = self.bullets(t, [
                "storage (SSD, hard drive) — keeps data for later",
                "operating system — coordinates the hardware",
                "applications — do the user's specific task",
            ], per=0.18)
            t.hold()

    def buses_section(self):
        with self.beat("buses") as t:
            self.clear_all(t)
            self.set_head(t, "The motherboard and the buses")
            note = serif("a bus is simply that which connects",
                         BODY_SIZE, GREY)
            self.below_head(note, buff=GAP_MD * 1.2)
            self.play(Write(note), run_time=t.fill(0.2))
            names = VGroup(*[
                box(name, width=3.4, height=1.1) for name in DAC
            ]).arrange(RIGHT, buff=GAP_MD * 1.2)
            fit(names)
            names.next_to(note, DOWN, buff=GAP_MD * 1.4)
            self.play(Create(names), run_time=t.fill(0.3))
            anchor = serif("D · A · C", TITLE_SIZE, TERRACOTTA)
            anchor.next_to(names, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(anchor), run_time=t.fill(0.2))
            t.hold()

        with self.beat("dac_meaning") as t:
            self.clear_all(t)
            self.set_head(t, "What each bus carries")
            rows = self.bullets(t, [
                "data bus — transports the data",
                "address bus — where it goes or comes from",
                "control bus — the control signals",
            ], per=0.2)
            t.hold()

        with self.beat("delivery") as t:
            self.clear_all(t)
            self.set_head(t, "Think of a delivery")
            rows = lines("the package  →  the data",
                         "the address  →  the destination",
                         "the instructions  →  the control signals",
                         size=BODY_SIZE, buff=GAP_MD * 0.9)
            self.below_head(rows, buff=GAP_MD * 1.6)
            for row in rows:
                self.play(Write(row), run_time=t.fill(0.18))
            self.arc(t, DAC, 0, fraction=0.1)
            t.hold()

        with self.beat("interaction") as t:
            self.clear_all(t)
            self.set_head(t, "You double-click a document")
            steps = self.bullets(t, [
                "the mouse receives your action",
                "the operating system recognizes the request",
                "the application is launched",
                "instructions and data move into memory",
                "the CPU processes them",
                "the result is sent to the display",
            ], per=0.09, size=BODY_SIZE)
            why = serif("one action — many components working together",
                        BODY_SIZE, TERRACOTTA)
            fit(why)
            why.next_to(steps, DOWN, buff=GAP_MD * 1.2)
            self.play(Write(why), run_time=t.fill(0.22))
            t.hold()

        with self.beat("environment2") as t:
            self.clear_all(t)
            self.set_head(t, "The computer's environment")
            rows = self.bullets(t, [
                "power supply — no electricity, no computer",
                "network — wired or wireless",
                "peripherals — printers, scanners, external storage",
                "the user — you type, it responds",
            ], per=0.15)
            never = serif("it never simply sits there on its own",
                          BODY_SIZE, TERRACOTTA)
            never.next_to(rows, DOWN, buff=GAP_MD * 1.3)
            self.play(Write(never), run_time=t.fill(0.2))
            t.hold()

    def von_neumann(self):
        with self.beat("von_neumann") as t:
            self.clear_all(t)
            title = lines("Von Neumann Architecture", size=TITLE_SIZE * 1.3)
            title.move_to(UP * 0.8)
            who = serif("John von Neumann · the stored-program computer",
                        BODY_SIZE, GREY)
            fit(who)
            who.next_to(title, DOWN, buff=GAP_MD * 1.6)
            self.play(Write(title), run_time=t.fill(0.35))
            self.play(Write(who), run_time=t.fill(0.25))
            t.hold()

        with self.beat("vn_components") as t:
            self.clear_all(t)
            self.set_head(t, "Four main components")
            cpu_box = box("CPU", width=4.4, height=2.2, color=SLATE,
                          size=BODY_SIZE)
            # Label sits high so the ALU and CU can be drawn inside later.
            cpu_box[1].next_to(cpu_box[0].get_top(), DOWN, buff=GAP_SM)
            mem = box("Memory", width=4.4, height=1.2, size=BODY_SIZE)
            inp = box("Input", width=2.8, height=1.1, size=BODY_SIZE)
            out = box("Output", width=2.8, height=1.1, size=BODY_SIZE)
            cpu_box.move_to(ORIGIN)
            mem.next_to(cpu_box, UP, buff=GAP_MD * 1.3)
            inp.next_to(cpu_box, LEFT, buff=GAP_MD * 1.6)
            out.next_to(cpu_box, RIGHT, buff=GAP_MD * 1.6)
            diagram = VGroup(mem, inp, cpu_box, out)
            diagram.move_to(DOWN * 0.15)
            links = VGroup(
                Arrow(inp.get_right(), cpu_box.get_left(), color=GREY,
                      buff=0.1, stroke_width=3,
                      max_tip_length_to_length_ratio=0.25),
                Arrow(cpu_box.get_right(), out.get_left(), color=GREY,
                      buff=0.1, stroke_width=3,
                      max_tip_length_to_length_ratio=0.25),
                Line(cpu_box.get_top(), mem.get_bottom(), color=GREY,
                     stroke_width=3),
            )
            self.play(Create(mem), run_time=t.fill(0.12))
            self.play(Create(cpu_box), run_time=t.fill(0.12))
            self.play(Create(inp), Create(out), run_time=t.fill(0.14))
            self.play(Create(links), run_time=t.fill(0.14))
            self.vn_cpu = cpu_box
            self.vn_diagram = VGroup(diagram, links)
            t.hold()

        with self.beat("alu_cu") as t:
            alu = box("ALU", width=1.8, height=0.8, color=TERRACOTTA,
                      size=LABEL_SIZE)
            cu = box("CU", width=1.8, height=0.8, color=TERRACOTTA,
                     size=LABEL_SIZE)
            inner = VGroup(alu, cu).arrange(RIGHT, buff=GAP_SM * 1.4)
            inner.next_to(self.vn_cpu[0].get_bottom(), UP, buff=GAP_SM * 1.2)
            roles = lines("ALU — arithmetic and logic",
                          "CU — coordinates execution, like a conductor",
                          size=LABEL_SIZE, color=GREY)
            roles.next_to(self.vn_diagram, DOWN, buff=GAP_MD * 1.1)
            self.play(Create(inner), run_time=t.fill(0.25))
            self.play(Write(roles), run_time=t.fill(0.3))
            t.hold()

        with self.beat("io_flow") as t:
            self.clear_all(t)
            flow = VGroup(*[
                box(name, width=3.0, height=1.2, size=BODY_SIZE)
                for name in ("INPUT", "PROCESS", "OUTPUT")
            ]).arrange(RIGHT, buff=GAP_MD * 1.8)
            fit(flow)
            flow.move_to(UP * 0.5)
            arrows = VGroup(*[
                Arrow(flow[i].get_right(), flow[i + 1].get_left(),
                      color=GREY, buff=0.1, stroke_width=3,
                      max_tip_length_to_length_ratio=0.25)
                for i in range(2)
            ])
            mem = serif("with memory supporting the process",
                        BODY_SIZE, GREY)
            mem.next_to(flow, DOWN, buff=GAP_MD * 1.6)
            self.play(Create(flow), run_time=t.fill(0.3))
            self.play(Create(arrows), run_time=t.fill(0.15))
            self.play(Write(mem), run_time=t.fill(0.22))
            t.hold()

        with self.beat("fdes") as t:
            self.clear_all(t)
            words = VGroup(*[
                serif(w.upper(), TITLE_SIZE * 1.15) for w in FDES
            ]).arrange(DOWN, buff=GAP_MD * 0.8)
            words.move_to(UP * 0.4)
            for word in words:
                self.play(Write(word), run_time=t.fill(0.12))
            hear = serif("you should hear this rhythm in the exam",
                         BODY_SIZE, TERRACOTTA)
            hear.next_to(words, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(hear), run_time=t.fill(0.22))
            t.hold()

        with self.beat("fetch") as t:
            self.clear_all(t)
            self.set_head(t, "Fetch")
            what = serif("the CPU retrieves an instruction from memory",
                         BODY_SIZE)
            fit(what)
            self.below_head(what, buff=GAP_MD * 1.2)
            regs = lines("PC — program counter", "IR — instruction register",
                         size=BODY_SIZE, color=GREY)
            regs.next_to(what, DOWN, buff=GAP_MD * 1.3)
            trick = serif("PC points  ·  IR holds", TITLE_SIZE, TERRACOTTA)
            trick.next_to(regs, DOWN, buff=GAP_MD * 1.3)
            self.play(Write(what), run_time=t.fill(0.2))
            self.play(Write(regs), run_time=t.fill(0.25))
            self.play(Write(trick), run_time=t.fill(0.22))
            self.arc(t, FDES, 0)
            t.hold()

        with self.beat("decode") as t:
            self.clear_all(t)
            self.set_head(t, "Decode")
            what = lines("the control unit examines the instruction",
                         "and works out what must happen",
                         size=BODY_SIZE)
            self.below_head(what, buff=GAP_MD * 1.4)
            like = serif("like understanding an instruction before "
                         "you act on it", LABEL_SIZE, GREY)
            fit(like)
            like.next_to(what, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(what), run_time=t.fill(0.3))
            self.play(Write(like), run_time=t.fill(0.22))
            self.arc(t, FDES, 1)
            t.hold()

        with self.beat("execute") as t:
            self.clear_all(t)
            self.set_head(t, "Execute")
            what = lines("the instruction is actually carried out",
                         "arithmetic → the ALU performs it",
                         "data to move → the components coordinate",
                         size=BODY_SIZE)
            self.below_head(what, buff=GAP_MD * 1.5)
            self.play(Write(what), run_time=t.fill(0.45))
            self.arc(t, FDES, 2)
            t.hold()

        with self.beat("store") as t:
            self.clear_all(t)
            self.set_head(t, "Store")
            what = lines("the result is stored in memory",
                         "or sent to an output device", size=BODY_SIZE)
            self.below_head(what, buff=GAP_MD * 1.4)
            self.play(Write(what), run_time=t.fill(0.3))
            self.arc(t, FDES, 3)
            again = serif("fetch · decode · execute · store",
                          BODY_SIZE, TERRACOTTA)
            again.next_to(what, DOWN, buff=GAP_MD * 1.6)
            self.play(Write(again), run_time=t.fill(0.22))
            t.hold()

    def vn_properties(self):
        with self.beat("vn_characteristics") as t:
            self.clear_all(t)
            self.set_head(t, "Three characteristics")
            rows = self.bullets(t, [
                "single memory store — instructions and data share it",
                "sequential execution — one instruction after another",
            ], per=0.22)
            t.hold()

        with self.beat("stored_program") as t:
            self.clear_all(t)
            self.set_head(t, "The stored program concept")
            what = lines("programs themselves are stored in memory",
                         size=BODY_SIZE)
            self.below_head(what, buff=GAP_MD * 1.4)
            why = lines("so a program can be changed —",
                        "instead of building a new machine every time",
                        size=BODY_SIZE, color=GREY)
            why.next_to(what, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(what), run_time=t.fill(0.3))
            self.play(Write(why), run_time=t.fill(0.3))
            t.hold()

        with self.beat("advantages") as t:
            self.clear_all(t)
            self.set_head(t, "Advantages")
            rows = self.bullets(t, [
                "simplified design — data and instructions share memory",
                "flexibility — install, update, run different software",
            ], per=0.25)
            t.hold()

        with self.beat("flexibility_example") as t:
            self.clear_all(t)
            self.set_head(t, "Imagine if it were not so")
            silly = lines("one computer to run Word",
                          "another computer to run Chrome",
                          "another computer to run a game",
                          size=BODY_SIZE, color=GREY)
            self.below_head(silly, buff=GAP_MD * 1.5)
            gift = serif("the stored program concept gives us flexibility",
                         BODY_SIZE, TERRACOTTA)
            fit(gift)
            gift.next_to(silly, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(silly), run_time=t.fill(0.35))
            self.play(Write(gift), run_time=t.fill(0.25))
            t.hold()

        with self.beat("bottleneck") as t:
            self.clear_all(t)
            self.set_head(t, "The von Neumann bottleneck")
            statement = lines(
                "instructions and data share the same",
                "memory pathway — so access to them limits",
                "how fast the CPU can actually work",
                size=BODY_SIZE)
            self.below_head(statement, buff=GAP_MD * 1.6)
            self.play(Write(statement), run_time=t.fill(0.5))
            t.hold()

        with self.beat("motorway") as t:
            self.clear_all(t)
            self.set_head(t, "A motorway into one toll gate")
            road = Polygon(
                np.array([-5.6, 1.5, 0]), np.array([-0.4, 0.45, 0]),
                np.array([-0.4, -0.45, 0]), np.array([-5.6, -1.5, 0]),
                color=SLATE, stroke_width=3,
            )
            gate = Rectangle(width=1.0, height=0.9, color=TERRACOTTA,
                             stroke_width=4)
            gate.move_to(np.array([0.2, 0, 0]))
            after = Line(np.array([0.8, 0, 0]), np.array([5.4, 0, 0]),
                         color=SLATE, stroke_width=3)
            drawing = VGroup(road, gate, after)
            drawing.move_to(DOWN * 0.3)
            note = serif("it does not matter how fast the cars can travel",
                         BODY_SIZE, GREY)
            fit(note)
            note.next_to(drawing, DOWN, buff=GAP_MD * 1.4)
            self.play(Create(road), run_time=t.fill(0.2))
            self.play(Create(gate), Create(after), run_time=t.fill(0.18))
            self.play(Write(note), run_time=t.fill(0.25))
            t.hold()

        with self.beat("security") as t:
            self.clear_all(t)
            self.set_head(t, "And a security risk")
            risk = lines("instructions and data sit in the same",
                         "memory architecture — so malicious",
                         "modification of instructions can cause harm",
                         size=BODY_SIZE)
            self.below_head(risk, buff=GAP_MD * 1.6)
            self.play(Write(risk), run_time=t.fill(0.5))
            t.hold()

    def computing_systems(self):
        with self.beat("computing_systems") as t:
            self.clear_all(t)
            self.set_head(t, "A computing system")
            three = VGroup(*[
                box(name, width=3.4, height=1.3, size=BODY_SIZE)
                for name in ("hardware", "software", "electricity")
            ]).arrange(RIGHT, buff=GAP_MD * 1.4)
            fit(three)
            self.below_head(three, buff=GAP_MD * 1.8)
            self.play(Create(three), run_time=t.fill(0.4))
            zoom = serif("this Zoom class is using all three right now",
                         LABEL_SIZE, GREY)
            zoom.next_to(three, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(zoom), run_time=t.fill(0.25))
            t.hold()

        with self.beat("hardware_software") as t:
            self.clear_all(t)
            self.set_head(t, "What each one means")
            left = lines("hardware", "CPU · RAM · storage",
                         "keyboard · screen", size=BODY_SIZE)
            right = lines("software", "operating system",
                          "applications", size=BODY_SIZE)
            pair = VGroup(left, right).arrange(RIGHT, buff=GAP_MD * 3.2)
            fit(pair)
            self.below_head(pair, buff=GAP_MD * 1.5)
            self.play(Write(left), run_time=t.fill(0.28))
            self.play(Write(right), run_time=t.fill(0.28))
            power = serif("and power — mains electricity or a battery",
                          LABEL_SIZE, GREY)
            power.next_to(pair, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(power), run_time=t.fill(0.2))
            t.hold()

        with self.beat("kinds") as t:
            self.clear_all(t)
            kinds = serif("computers · software systems · networks · "
                          "the internet", BODY_SIZE)
            fit(kinds)
            kinds.move_to(ORIGIN)
            self.play(Write(kinds), run_time=t.fill(0.5))
            t.hold()

        with self.beat("networks") as t:
            self.clear_all(t)
            self.set_head(t, "Why connect computers?")
            rows = self.bullets(t, [
                "resource sharing", "communication",
                "data management and collaboration",
            ], per=0.15)
            made = serif("hardware: routers, switches, cables  ·  "
                         "software: protocols", LABEL_SIZE, GREY)
            fit(made)
            made.next_to(rows, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(made), run_time=t.fill(0.25))
            t.hold()

        with self.beat("lan_wan") as t:
            self.clear_all(t)
            self.set_head(t, "LAN and WAN")
            left = lines("LAN", "local area network",
                         "a school computer lab", size=BODY_SIZE)
            right = lines("WAN", "wide area network",
                          "a much larger area", size=BODY_SIZE)
            pair = VGroup(left, right).arrange(RIGHT, buff=GAP_MD * 3.2)
            fit(pair)
            self.below_head(pair, buff=GAP_MD * 1.5)
            self.play(Write(left), run_time=t.fill(0.25))
            self.play(Write(right), run_time=t.fill(0.25))
            net = serif("the internet — networks of networks, worldwide",
                        BODY_SIZE, TERRACOTTA)
            fit(net)
            net.next_to(pair, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(net), run_time=t.fill(0.22))
            t.hold()

        with self.beat("protocols") as t:
            self.clear_all(t)
            self.set_head(t, "Four protocols to remember")
            rows = self.bullets(t, [
                "TCP/IP — internet communication",
                "UDP — faster, less reliable delivery",
                "FTP — transferring files",
                "POP — retrieving email",
            ], per=0.14)
            enough = serif("for chapter one, that much is enough",
                           LABEL_SIZE, GREY)
            enough.next_to(rows, DOWN, buff=GAP_MD * 1.3)
            self.play(Write(enough), run_time=t.fill(0.2))
            t.hold()

    def recap(self):
        with self.beat("recap_start") as t:
            self.clear_all(t)
            one = lines("A system is a collection of components",
                        "working together toward an objective.",
                        size=BODY_SIZE * 1.1)
            one.move_to(ORIGIN)
            self.play(Write(one), run_time=t.fill(0.55))
            t.hold()

        with self.beat("recap_ocec") as t:
            self.clear_all(t)
            arc = WordArc(OCEC, size=BODY_SIZE, lit=CHARCOAL)
            for cell in arc.cells:
                cell.set_color(CHARCOAL)
            arc.move_to(UP * 0.5)
            self.play(Write(arc), run_time=t.fill(0.5))
            t.hold()

        with self.beat("recap_natural") as t:
            self.clear_all(t)
            left = lines("natural", "physical · chemical",
                         "biological · psychological",
                         size=BODY_SIZE, color=GREY)
            right = lines("artificial", "knowledge · engineering",
                          "social", size=BODY_SIZE)
            pair = VGroup(left, right).arrange(RIGHT, buff=GAP_MD * 3.0)
            fit(pair)
            pair.move_to(ORIGIN)
            self.play(Write(pair), run_time=t.fill(0.55))
            t.hold()

        with self.beat("recap_science") as t:
            self.clear_all(t)
            rows = lines("natural science — understand what exists",
                         "design science — create what should exist",
                         "computer science — both",
                         size=BODY_SIZE, buff=GAP_MD * 0.9)
            rows.move_to(ORIGIN)
            self.play(Write(rows), run_time=t.fill(0.55))
            t.hold()

        with self.beat("recap_computer") as t:
            self.clear_all(t)
            self.set_head(t, "The computer as a system")
            parts = serif("inputs · processing · memory · storage · "
                          "outputs", BODY_SIZE)
            fit(parts)
            self.below_head(parts, buff=GAP_MD * 1.5)
            arc = WordArc(DAC, size=BODY_SIZE, lit=CHARCOAL)
            for cell in arc.cells:
                cell.set_color(CHARCOAL)
            arc.next_to(parts, DOWN, buff=GAP_MD * 1.6)
            self.play(Write(parts), run_time=t.fill(0.25))
            self.play(Write(arc), run_time=t.fill(0.3))
            t.hold()

        with self.beat("recap_vn") as t:
            self.clear_all(t)
            arc = WordArc(FDES, size=TITLE_SIZE, lit=CHARCOAL)
            for cell in arc.cells:
                cell.set_color(CHARCOAL)
            arc.move_to(ORIGIN)
            self.play(Write(arc), run_time=t.fill(0.55))
            t.hold()

        with self.beat("recap_internet") as t:
            self.clear_all(t)
            ladder = VGroup(*[
                serif(name, BODY_SIZE)
                for name in ("a computer", "networks",
                             "networks of networks", "the internet")
            ]).arrange(DOWN, buff=GAP_MD * 0.9)
            ladder.move_to(ORIGIN)
            ladder[-1].set_color(TERRACOTTA)
            for step in ladder:
                self.play(Write(step), run_time=t.fill(0.14))
            t.hold()

        with self.beat("one_idea") as t:
            self.clear_all(t)
            head = serif("One idea, at different scales", TITLE_SIZE)
            head.to_edge(UP, buff=GAP_MD * 1.4)
            scales = serif("a body · a car · a computer · a network · "
                           "the internet", BODY_SIZE, GREY)
            fit(scales)
            scales.next_to(head, DOWN, buff=GAP_MD * 1.4)
            anchors = lines(
                "SYSTEM = parts + purpose",
                "OCEC = objective · components · environment · "
                "communication",
                "natural = exists   |   artificial = designed",
                "DAC = data · address · control bus",
                "FDES = fetch · decode · execute · store",
                size=LABEL_SIZE, buff=GAP_SM * 1.3)
            anchors.next_to(scales, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(head), run_time=t.fill(0.1))
            self.play(Write(scales), run_time=t.fill(0.15))
            for row in anchors:
                self.play(Write(row), run_time=t.fill(0.1))
            t.hold()

    def closing(self):
        with self.beat("questions") as t:
            self.clear_all(t)
            head = serif("Answer these before we meet again", TITLE_SIZE)
            fit(head)
            head.to_edge(UP, buff=GAP_MD * 1.4)
            qs = lines(
                "1. Define a system and explain its objective,",
                "     components, environment and communication.",
                "2. Differentiate between natural and artificial",
                "     systems with examples.",
                "3. Explain the main components of the von",
                "     Neumann architecture.",
                "4. Describe the fetch–decode–execute–store cycle.",
                "5. What is the von Neumann bottleneck?",
                size=LABEL_SIZE, buff=GAP_SM * 1.25, align=LEFT)
            qs.next_to(head, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(head), run_time=t.fill(0.09))
            for q in qs:
                self.play(Write(q), run_time=t.fill(0.08))
            t.hold()

        with self.beat("homework") as t:
            self.clear_all(t)
            send = lines("Send me your answers before the exam.",
                         "If a topic is unclear, tell us.",
                         size=BODY_SIZE * 1.1)
            send.move_to(ORIGIN)
            self.play(Write(send), run_time=t.fill(0.5))
            t.hold()
