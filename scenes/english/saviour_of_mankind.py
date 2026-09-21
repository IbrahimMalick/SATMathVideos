"""English lecture: The Saviour of Mankind (Grade 9, Chapter 1).

Narration script: scripts/EN09-saviour-of-mankind.md

A monologue lecture, so the visuals carry the structure the talk relies on:
seven remembered words — Beauty, Brilliance, Breakdown, Cave, Calling,
Courage, Change — with the arc returning between scenes so the student can
see where in the story they are.

The honorific is rendered with U+FDFA, which DejaVu Serif lacks; Pango
falls back to Amiri (fonts-hosny-amiri), matching the serif weight.
"""

import numpy as np

from manim import (
    ArcBetweenPoints,
    Circle,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    Line,
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
from components.vocab_card import VocabCard
from components.word_arc import WordArc
from scenes.base import SATScene

SEVEN = ["Beauty", "Brilliance", "Breakdown", "Cave", "Calling", "Courage",
         "Change"]
PBUH = "ﷺ"
FRAME_SAFE = 12.6


def fit(mobject, width=FRAME_SAFE):
    if mobject.width > width:
        mobject.scale_to_fit_width(width)
    return mobject


def lines(*texts, size=BODY_SIZE, color=CHARCOAL, buff=GAP_SM * 1.3):
    group = VGroup(*[fit(serif(t, size, color)) for t in texts])
    group.arrange(DOWN, buff=buff)
    return group


class SaviourOfMankind(SATScene):
    scene_id = "english.saviour_of_mankind"

    def construct(self):
        self.margin_note = mono("Grade 9 English · Chapter 1", MARGIN_SIZE)
        self.margin_note.to_corner(UP + LEFT, buff=GAP_SM)
        self.add(self.margin_note)
        self.section_head = None
        self.arc = None

        self.opening()
        self.scene_beauty()
        self.scene_brilliance()
        self.scene_breakdown()
        self.scene_cave()
        self.scene_calling()
        self.scene_message()
        self.scene_courage()
        self.scene_change()
        self.the_title()
        self.vocabulary()
        self.grammar()
        self.reading_skill()
        self.recap()
        self.closing()

    # -------------------------------------------------------------- helpers

    def clear_all(self, t, fraction=0.06, keep=()):
        keep = set(keep) | {self.margin_note}
        old = [m for m in self.mobjects if m not in keep]
        if old:
            self.play(*[FadeOut(m) for m in old], run_time=t.fill(fraction))
        self.section_head = None

    def set_head(self, t, text, fraction=0.1):
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

    def build_arc(self):
        """The seven-word spine, parked along the bottom of the frame."""
        arc = WordArc(SEVEN, size=LABEL_SIZE, lit=CHARCOAL)
        arc.to_edge(DOWN, buff=GAP_MD)
        return arc

    def word_moment(self, t, index, caption=None, hero_fraction=0.3):
        """A big terracotta word plus the arc, advanced to that step."""
        hero = serif(SEVEN[index].upper(), TITLE_SIZE * 1.7, TERRACOTTA)
        hero.move_to(UP * 0.9)
        self.play(Write(hero), run_time=t.fill(hero_fraction))
        arc = self.build_arc()
        self.play(FadeIn(arc), *arc.focus(index), run_time=t.fill(0.18))
        self.arc = arc
        if caption:
            note = fit(serif(caption, BODY_SIZE, GREY))
            note.next_to(hero, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(note), run_time=t.fill(0.2))
            return hero, note
        return (hero,)

    def two_columns(self, t, title_left, left_items, title_right,
                    right_items, fraction=0.2):
        left = lines(*left_items, size=BODY_SIZE, color=GREY)
        right = lines(*right_items, size=BODY_SIZE)
        lhead = serif(title_left, BODY_SIZE, GREY)
        rhead = serif(title_right, BODY_SIZE, TERRACOTTA)
        lcol = VGroup(lhead, left).arrange(DOWN, buff=GAP_MD)
        rcol = VGroup(rhead, right).arrange(DOWN, buff=GAP_MD)
        pair = VGroup(lcol, rcol).arrange(RIGHT, buff=GAP_MD * 3.2)
        fit(pair)
        self.below_head(pair)
        self.play(Write(lcol), run_time=t.fill(fraction))
        self.play(Write(rcol), run_time=t.fill(fraction))
        return pair

    # ------------------------------------------------------------- sections

    def opening(self):
        title = lines("The Saviour of Mankind", size=TITLE_SIZE * 1.4)
        title.move_to(UP * 0.8)
        sub = serif("Grade 9 English · Chapter 1", BODY_SIZE, GREY)
        sub.next_to(title, DOWN, buff=GAP_MD * 1.4)

        with self.beat("open") as t:
            self.play(Write(title), run_time=t.fill(0.3))
            self.play(Write(sub), run_time=t.fill(0.2))
            t.hold()

        with self.beat("imagine") as t:
            self.clear_all(t)
            gone = lines("no cars", "no phones", "no electricity",
                         "no television", "no internet",
                         size=BODY_SIZE, color=GREY)
            gone.move_to(LEFT * 3.4)
            when = lines("1400 years ago", size=TITLE_SIZE)
            where = serif("Arabia", TITLE_SIZE * 1.3, TERRACOTTA)
            right = VGroup(when, where).arrange(DOWN, buff=GAP_MD * 1.4)
            right.move_to(RIGHT * 3.2)
            for item in gone:
                self.play(Write(item), run_time=t.fill(0.08))
            self.play(Write(when), run_time=t.fill(0.15))
            self.play(Write(where), run_time=t.fill(0.18))
            t.hold()

        with self.beat("arabia") as t:
            self.clear_all(t)
            ground = Line(LEFT * 6.6, RIGHT * 6.6, color=GREY,
                          stroke_width=2)
            ground.move_to(DOWN * 2.2)
            dunes = VGroup(*[
                ArcBetweenPoints(
                    np.array([x - w, -2.2, 0]), np.array([x + w, -2.2, 0]),
                    angle=-np.pi * 0.55, color=SLATE, stroke_width=4,
                )
                for x, w in ((-4.2, 2.0), (-0.6, 2.4), (3.4, 2.2))
            ])
            sun = Circle(radius=0.6, color=TERRACOTTA, stroke_width=5)
            sun.move_to(np.array([4.2, 1.9, 0]))
            rng = np.random.default_rng(9)
            stars = VGroup(*[
                Dot(np.array([rng.uniform(-6.2, 6.2),
                              rng.uniform(0.4, 3.3), 0]),
                    radius=0.045, color=GREY)
                for _ in range(26)
            ])
            self.play(Create(ground), run_time=t.fill(0.08))
            self.play(Create(dunes), run_time=t.fill(0.25))
            self.play(Create(sun), run_time=t.fill(0.12))
            self.play(FadeIn(stars), run_time=t.fill(0.2))
            self.landscape = VGroup(ground, dunes, sun, stars)
            t.hold()

        with self.beat("makkah") as t:
            marker = Dot(np.array([-0.6, -1.15, 0]), radius=0.09,
                         color=CHARCOAL)
            stem = Line(np.array([-0.6, -1.15, 0]),
                        np.array([-0.6, -0.15, 0]),
                        color=CHARCOAL, stroke_width=3)
            label = serif("Makkah Mukarramah", BODY_SIZE)
            label.next_to(stem, UP, buff=GAP_SM)
            note = serif("a city that will change the world",
                         LABEL_SIZE, GREY)
            note.next_to(self.landscape, DOWN, buff=GAP_MD)
            self.play(Create(stem), Create(marker), run_time=t.fill(0.15))
            self.play(Write(label), run_time=t.fill(0.22))
            self.play(Write(note), run_time=t.fill(0.2))
            t.hold()

        with self.beat("chapter") as t:
            self.clear_all(t)
            card = lines("The Saviour of Mankind", size=TITLE_SIZE * 1.3)
            card.move_to(UP * 0.5)
            sub2 = serif("Chapter 1 — where our story begins",
                         BODY_SIZE, GREY)
            sub2.next_to(card, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(card), run_time=t.fill(0.35))
            self.play(Write(sub2), run_time=t.fill(0.22))
            t.hold()

    def scene_beauty(self):
        with self.beat("beauty_word") as t:
            self.clear_all(t)
            self.word_moment(
                t, 0, "beautiful land · beautiful sky · beautiful language")
            t.hold()

        with self.beat("beauty_inside") as t:
            self.clear_all(t)
            self.set_head(t, "But beauty outside…")
            idea = lines("beauty on the outside does not mean",
                         "everything is right on the inside")
            self.below_head(idea, buff=GAP_MD * 1.8)
            self.play(Write(idea), run_time=t.fill(0.4))
            self.play(Create(self.underline(idea, TERRACOTTA)),
                      run_time=t.fill(0.12))
            t.hold()

        with self.beat("unparalleled") as t:
            self.clear_all(t)
            card = VocabCard(
                "unparalleled",
                "so outstanding that nothing is quite equal to it",
                weak='"He was a good speaker."',
                strong='"His eloquence was unparalleled."',
            )
            card.move_to(ORIGIN)
            self.play(Write(card.word), run_time=t.fill(0.18))
            self.play(Write(card.meaning), run_time=t.fill(0.22))
            self.play(Write(card.contrast), run_time=t.fill(0.25))
            t.hold()

        with self.beat("unparalleled_sense") as t:
            self.clear_all(t)
            self.set_head(t, "What the writer is really saying")
            not_this = serif('not "it was a nice city"', BODY_SIZE, GREY)
            but_this = lines("a beauty difficult to match")
            stack = VGroup(not_this, but_this).arrange(DOWN,
                                                       buff=GAP_MD * 1.6)
            self.below_head(stack, buff=GAP_MD * 1.6)
            self.play(Write(not_this), run_time=t.fill(0.25))
            self.play(Write(but_this), run_time=t.fill(0.28))
            t.hold()

    def scene_brilliance(self):
        with self.beat("surprising") as t:
            self.clear_all(t)
            self.set_head(t, "The chapter does something interesting")
            idea = lines("it does not begin with religion",
                         "it begins with the people", color=CHARCOAL)
            self.below_head(idea, buff=GAP_MD * 1.8)
            self.play(Write(idea), run_time=t.fill(0.45))
            t.hold()

        with self.beat("memory") as t:
            self.clear_all(t)
            self.set_head(t, "A remarkable memory")
            no_tools = lines("no Google", "no phone", "no ChatGPT",
                             size=BODY_SIZE, color=GREY)
            tech = lines("memory itself was the technology")
            stack = VGroup(no_tools, tech).arrange(DOWN, buff=GAP_MD * 1.8)
            self.below_head(stack, buff=GAP_MD * 1.4)
            for item in no_tools:
                self.play(Write(item), run_time=t.fill(0.09))
            self.play(Write(tech), run_time=t.fill(0.28))
            t.hold()

        with self.beat("ukaz") as t:
            self.clear_all(t)
            self.set_head(t, "The fair at Ukaz")
            facts = lines("a poetry competition, every year",
                          "poems of hundreds of lines",
                          "recited entirely from memory")
            self.below_head(facts, buff=GAP_MD * 1.6)
            for line in facts:
                self.play(Write(line), run_time=t.fill(0.16))
            t.hold()

        with self.beat("eloquence") as t:
            self.clear_all(t)
            card = VocabCard(
                "eloquence",
                "expressing thoughts beautifully, clearly and powerfully",
                weak="not simply talking a lot",
            )
            card.move_to(ORIGIN)
            self.play(Write(card.word), run_time=t.fill(0.2))
            self.play(Write(card.meaning), run_time=t.fill(0.25))
            self.play(Write(card.contrast), run_time=t.fill(0.2))
            t.hold()

        with self.beat("brilliance_word") as t:
            self.clear_all(t)
            self.word_moment(t, 1, "memory · speech · poetry · rich language")
            t.hold()

    def scene_breakdown(self):
        with self.beat("contradiction") as t:
            self.clear_all(t)
            self.set_head(t, "The great contradiction")
            row = VGroup(
                serif("Beauty", TITLE_SIZE),
                serif("+", TITLE_SIZE, GREY),
                serif("Brilliance", TITLE_SIZE),
            ).arrange(RIGHT, buff=GAP_MD)
            ask = serif("…and still a serious problem?", BODY_SIZE,
                        TERRACOTTA)
            stack = VGroup(row, ask).arrange(DOWN, buff=GAP_MD * 1.8)
            self.below_head(stack, buff=GAP_MD * 1.6)
            self.play(Write(row), run_time=t.fill(0.3))
            self.play(Write(ask), run_time=t.fill(0.25))
            t.hold()

        with self.beat("wisdom") as t:
            self.clear_all(t)
            self.set_head(t, "Cleverness is not wisdom")
            idea = lines("intelligence and eloquence alone",
                         "do not guarantee wisdom")
            self.below_head(idea, buff=GAP_MD * 1.5)
            examples = lines(
                "a person can be clever and still choose badly",
                "a society can be impressive and still be morally lost",
                size=LABEL_SIZE, color=GREY)
            examples.next_to(idea, DOWN, buff=GAP_MD * 1.6)
            self.play(Write(idea), run_time=t.fill(0.3))
            self.play(Write(examples), run_time=t.fill(0.3))
            t.hold()

        with self.beat("breakdown_word") as t:
            self.clear_all(t)
            self.word_moment(t, 2, "on the verge of chaos")
            t.hold()

        with self.beat("verge") as t:
            self.clear_all(t)
            self.set_head(t, "verge")
            cliff = VGroup(
                Line(LEFT * 2.6, RIGHT * 1.4, color=SLATE, stroke_width=5),
                Line(RIGHT * 1.4, RIGHT * 1.4 + DOWN * 1.6,
                     color=SLATE, stroke_width=5),
            )
            edge = Dot(RIGHT * 1.25 + UP * 0.14, radius=0.08,
                       color=TERRACOTTA)
            drawing = VGroup(cliff, edge)
            self.below_head(drawing, buff=GAP_MD * 1.5)
            meaning = serif("the edge of something — one more step",
                            BODY_SIZE, GREY)
            meaning.next_to(drawing, DOWN, buff=GAP_MD * 1.3)
            chaos = serif("chaos — complete confusion and disorder",
                          BODY_SIZE)
            chaos.next_to(meaning, DOWN, buff=GAP_MD)
            self.play(Create(cliff), run_time=t.fill(0.2))
            self.play(Create(edge), run_time=t.fill(0.08))
            self.play(Write(meaning), run_time=t.fill(0.2))
            self.play(Write(chaos), run_time=t.fill(0.22))
            t.hold()

        with self.beat("crumbling") as t:
            self.clear_all(t)
            self.set_head(t, "A civilization crumbling")
            blocks = VGroup()
            for row_i in range(4):
                for col_i in range(4):
                    block = Rectangle(width=1.25, height=0.6, color=SLATE,
                                      stroke_width=3)
                    block.move_to(np.array([
                        -2.1 + col_i * 1.35, -2.1 + row_i * 0.72, 0]))
                    blocks.add(block)
            blocks.move_to(ORIGIN)
            cracks = VGroup(
                Line(blocks[5].get_corner(DOWN + LEFT),
                     blocks[9].get_corner(UP + RIGHT),
                     color=TERRACOTTA, stroke_width=4),
                Line(blocks[2].get_corner(DOWN + LEFT),
                     blocks[6].get_corner(UP + RIGHT),
                     color=TERRACOTTA, stroke_width=4),
            )
            note = serif("thousands of years to build — cracking apart",
                         LABEL_SIZE, GREY)
            note.next_to(blocks, DOWN, buff=GAP_MD)
            VGroup(blocks, cracks, note).move_to(DOWN * 0.7)
            self.play(Create(blocks), run_time=t.fill(0.25))
            self.play(Create(cracks[0]), run_time=t.fill(0.1))
            self.play(Create(cracks[1]), run_time=t.fill(0.1))
            self.play(FadeOut(blocks[13]), FadeOut(blocks[15]),
                      run_time=t.fill(0.1))
            self.play(Write(note), run_time=t.fill(0.15))
            t.hold()

        with self.beat("contrast_sentence") as t:
            self.clear_all(t)
            self.set_head(t, "Memorize this contrast")
            good = VGroup(
                serif("The Arabs possessed brilliant language,", BODY_SIZE),
                serif("but humanity faced a moral crisis.", BODY_SIZE),
            ).arrange(DOWN, buff=GAP_SM)
            fit(good)
            self.below_head(good, buff=GAP_MD * 1.6)
            weak = serif('stronger than: "people were bad before Islam"',
                         LABEL_SIZE, GREY)
            weak.next_to(good, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(good), run_time=t.fill(0.4))
            self.play(Create(self.underline(good)), run_time=t.fill(0.1))
            self.play(Write(weak), run_time=t.fill(0.2))
            t.hold()

        with self.beat("sophisticated") as t:
            self.clear_all(t)
            self.set_head(t, "What was missing?")
            had = lines("there was ability", "there was civilization",
                        "there was culture", size=BODY_SIZE, color=GREY)
            missing = lines("direction · purpose · moral guidance",
                            size=BODY_SIZE, color=TERRACOTTA)
            stack = VGroup(had, missing).arrange(DOWN, buff=GAP_MD * 1.8)
            self.below_head(stack, buff=GAP_MD * 1.4)
            self.play(Write(had), run_time=t.fill(0.3))
            self.play(Write(missing), run_time=t.fill(0.3))
            t.hold()

        with self.beat("three_words") as t:
            self.clear_all(t)
            arc = self.build_arc()
            arc.move_to(ORIGIN)
            self.play(FadeIn(arc), run_time=t.fill(0.2))
            self.play(*[arc.cell(i).animate.set_color(CHARCOAL)
                        for i in range(3)], run_time=t.fill(0.25))
            t.hold()

    def scene_cave(self):
        with self.beat("cave_scene") as t:
            self.clear_all(t)
            self.set_head(t, "Makkah — and one man apart from it")
            self.two_columns(
                t, "the city",
                ["markets and trade", "arguments", "poetry", "noise"],
                "the cave",
                ["one man", "deep thought"],
            )
            t.hold()

        with self.beat("solitude") as t:
            self.clear_all(t)
            card = VocabCard(
                "solitude",
                "being alone — but by choice",
                weak="not loneliness",
                strong="you deliberately move away from people and noise",
            )
            card.move_to(ORIGIN)
            self.play(Write(card.word), run_time=t.fill(0.2))
            self.play(Write(card.meaning), run_time=t.fill(0.22))
            self.play(Write(card.contrast), run_time=t.fill(0.25))
            t.hold()

        with self.beat("meditation") as t:
            card = VocabCard("meditation", "deep reflection, deep thinking")
            card.move_to(ORIGIN)
            self.clear_all(t, fraction=0.12)
            self.play(Write(card), run_time=t.fill(0.45))
            t.hold()

        with self.beat("inside_outside") as t:
            self.clear_all(t)
            self.set_head(t, "The contrast")
            self.two_columns(
                t, "outside the cave",
                ["noise", "society rushing", "a world of problems"],
                "inside the cave",
                ["silence", "reflection", "thinking about them"],
            )
            t.hold()

        with self.beat("cave_word") as t:
            self.clear_all(t)
            hero, _ = self.word_moment(
                t, 3, "solitude and meditation in the cave of Hira",
                hero_fraction=0.2)
            quiet = lines("great change often begins quietly",
                          size=BODY_SIZE)
            quiet.next_to(self.arc, UP, buff=GAP_MD * 1.3)
            self.play(Write(quiet), run_time=t.fill(0.25))
            t.hold()

    def scene_calling(self):
        with self.beat("compassion") as t:
            self.clear_all(t)
            card = VocabCard(
                "compassion",
                "recognizing another's suffering — and genuinely caring",
            )
            card.move_to(UP * 0.6)
            troubled = serif("troubled by wrong beliefs and social evils",
                             LABEL_SIZE, GREY)
            troubled.next_to(card, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(card.word), run_time=t.fill(0.2))
            self.play(Write(card.meaning), run_time=t.fill(0.25))
            self.play(Write(troubled), run_time=t.fill(0.2))
            t.hold()

        with self.beat("sympathy") as t:
            self.clear_all(t)
            self.set_head(t, "Sympathy is not compassion")
            self.two_columns(
                t, "sympathy",
                ['"that\'s unfortunate"', "feeling sorry", "it stops there"],
                "compassion",
                ["you feel their place", "concern", "it moves you to act"],
            )
            t.hold()

        with self.beat("revelation") as t:
            self.clear_all(t)
            self.set_head(t, "The turning point")
            where = serif("in the cave of Hira — Hazrat Jibril came",
                          BODY_SIZE, GREY)
            self.below_head(where, buff=GAP_MD * 1.4)
            command = serif("Read", TITLE_SIZE * 1.8, TERRACOTTA)
            command.next_to(where, DOWN, buff=GAP_MD * 1.6)
            iqra = serif("Iqra — the first revelation", BODY_SIZE)
            iqra.next_to(command, DOWN, buff=GAP_MD * 1.3)
            self.play(Write(where), run_time=t.fill(0.2))
            self.play(Write(command), run_time=t.fill(0.3))
            self.play(Write(iqra), run_time=t.fill(0.2))
            t.hold()

        with self.beat("calling_word") as t:
            self.clear_all(t)
            self.word_moment(
                t, 4, "quiet reflection becomes a public mission")
            t.hold()

    def scene_message(self):
        with self.beat("message") as t:
            self.clear_all(t)
            self.set_head(t, "The message")
            years = serif("revelation continued for 23 years",
                          LABEL_SIZE, GREY)
            self.below_head(years, buff=GAP_MD * 1.1)
            core = lines("the Oneness of Allah", "the unity of mankind",
                         size=TITLE_SIZE)
            core.next_to(years, DOWN, buff=GAP_MD * 1.5)
            against = serif("against a nexus of superstition, ignorance "
                            "and disbelief", LABEL_SIZE, GREY)
            fit(against)
            against.next_to(core, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(years), run_time=t.fill(0.12))
            self.play(Write(core), run_time=t.fill(0.32))
            self.play(Write(against), run_time=t.fill(0.22))
            t.hold()

        with self.beat("direction_change") as t:
            self.clear_all(t)
            self.set_head(t, "The chapter changes direction")
            self.two_columns(
                t, "at the beginning",
                ["chaos", "confusion", "moral darkness"],
                "now",
                ["direction", "clarity", "guidance"],
            )
            t.hold()

    def scene_courage(self):
        with self.beat("resistance") as t:
            self.clear_all(t)
            self.set_head(t, "Scene 7 — Resistance")
            idea = lines("great change usually creates resistance")
            self.below_head(idea, buff=GAP_MD * 1.4)
            when = lines("when it challenges beliefs, habits,",
                         "status or power", size=BODY_SIZE, color=GREY)
            when.next_to(idea, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(idea), run_time=t.fill(0.3))
            self.play(Write(when), run_time=t.fill(0.3))
            t.hold()

        with self.beat("renounce") as t:
            self.clear_all(t)
            card = VocabCard(
                "renounce",
                "to give something up publicly or formally",
            )
            card.move_to(UP * 0.7)
            meaning = lines("stop · give up · walk away · return to the "
                            "old way", size=BODY_SIZE, color=GREY)
            meaning.next_to(card, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(card.word), run_time=t.fill(0.2))
            self.play(Write(card.meaning), run_time=t.fill(0.22))
            self.play(Write(meaning), run_time=t.fill(0.25))
            t.hold()

        with self.beat("sun_moon") as t:
            self.clear_all(t)
            sun = Circle(radius=0.75, color=TERRACOTTA, stroke_width=5)
            sun.move_to(LEFT * 3.4 + UP * 1.5)
            moon = Circle(radius=0.75, color=SLATE, stroke_width=5)
            moon.move_to(RIGHT * 3.4 + UP * 1.5)
            sun_label = serif("the sun", LABEL_SIZE, GREY)
            sun_label.next_to(sun, DOWN, buff=GAP_SM)
            moon_label = serif("the moon", LABEL_SIZE, GREY)
            moon_label.next_to(moon, DOWN, buff=GAP_SM)
            quote = lines(
                "even then, he would not abandon",
                "the proclamation of the Oneness of Allah",
                size=BODY_SIZE)
            quote.move_to(DOWN * 1.4)
            self.play(Create(sun), Create(moon), run_time=t.fill(0.2))
            self.play(Write(sun_label), Write(moon_label),
                      run_time=t.fill(0.12))
            self.play(Write(quote), run_time=t.fill(0.35))
            t.hold()

        with self.beat("courage_word") as t:
            self.clear_all(t)
            self.word_moment(t, 5, "courage when stopping would be easier")
            t.hold()

        with self.beat("conviction") as t:
            self.clear_all(t)
            idea = lines("Conviction is easy to claim",
                         "when it costs nothing.", size=TITLE_SIZE)
            idea.move_to(UP * 0.3)
            self.play(Write(idea), run_time=t.fill(0.45))
            self.play(Create(self.underline(idea, TERRACOTTA)),
                      run_time=t.fill(0.15))
            t.hold()

    def scene_change(self):
        with self.beat("transformation") as t:
            self.clear_all(t)
            self.set_head(t, "The final movement")
            idea = lines("the mission continued despite every challenge",
                         size=BODY_SIZE)
            self.below_head(idea, buff=GAP_MD * 1.3)
            hart = lines("Michael H. Hart, The 100: A Ranking of the",
                         "Most Influential Persons in History",
                         size=LABEL_SIZE, color=GREY)
            hart.next_to(idea, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(idea), run_time=t.fill(0.3))
            self.play(Write(hart), run_time=t.fill(0.3))
            t.hold()

        with self.beat("change_word") as t:
            self.clear_all(t)
            self.word_moment(t, 6, "not improvement — a complete change",
                             hero_fraction=0.22)
            cat = serif("caterpillar  →  butterfly", BODY_SIZE, GREY)
            cat.next_to(self.arc, UP, buff=GAP_MD * 1.2)
            self.play(Write(cat), run_time=t.fill(0.2))
            t.hold()

        with self.beat("whole_story") as t:
            self.clear_all(t)
            arc = WordArc(SEVEN, size=BODY_SIZE, rows=2, lit=CHARCOAL)
            arc.move_to(UP * 0.8)
            glosses = lines(
                "a remarkable land · a remarkable people · a crisis",
                "solitude · revelation · defiance · transformation",
                size=LABEL_SIZE, color=GREY)
            glosses.next_to(arc, DOWN, buff=GAP_MD * 1.6)
            one = serif("not twenty disconnected facts — one story",
                        BODY_SIZE, TERRACOTTA)
            one.next_to(glosses, DOWN, buff=GAP_MD * 1.3)
            self.play(Write(arc), run_time=t.fill(0.3))
            self.play(Write(glosses), run_time=t.fill(0.25))
            self.play(Write(one), run_time=t.fill(0.2))
            t.hold()

    def the_title(self):
        with self.beat("title") as t:
            self.clear_all(t)
            self.set_head(t, "Why this title?")
            title = serif("The Saviour of Mankind", TITLE_SIZE * 1.2)
            self.below_head(title, buff=GAP_MD * 1.5)
            because = lines("divine guidance brought to humanity",
                            "at a time of moral and spiritual crisis",
                            size=BODY_SIZE, color=GREY)
            because.next_to(title, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(title), run_time=t.fill(0.3))
            self.play(Write(because), run_time=t.fill(0.3))
            t.hold()

        with self.beat("theme_box") as t:
            self.clear_all(t)
            self.set_head(t, "The textbook's theme")
            theme = lines(
                f"Hazrat Muhammad {PBUH}, the last Rasool of Allah Almighty,",
                "had the greatest influence on mankind.",
                size=BODY_SIZE)
            self.below_head(theme, buff=GAP_MD * 1.8)
            self.play(Write(theme), run_time=t.fill(0.5))
            t.hold()

        with self.beat("exam_question") as t:
            self.clear_all(t)
            self.set_head(t, "In the exam")
            question = lines(
                '"Explain the appropriateness of the title',
                'The Saviour of Mankind."', size=BODY_SIZE)
            self.below_head(question, buff=GAP_MD * 1.4)
            method = serif("don't recite the page — remember the story",
                           BODY_SIZE, GREY)
            method.next_to(question, DOWN, buff=GAP_MD * 1.4)
            chain = serif("breakdown  →  guidance  →  transformation",
                          BODY_SIZE, TERRACOTTA)
            chain.next_to(method, DOWN, buff=GAP_MD * 1.2)
            self.play(Write(question), run_time=t.fill(0.25))
            self.play(Write(method), run_time=t.fill(0.2))
            self.play(Write(chain), run_time=t.fill(0.22))
            t.hold()

        with self.beat("model_answer") as t:
            self.clear_all(t)
            self.set_head(t, "Turn it into prose")
            answer = lines(
                "The title is appropriate because the chapter presents",
                f"Rasoolullah {PBUH} as bringing divine guidance at a time",
                "when humanity faced moral and spiritual decline. His",
                "message of the Oneness of Allah, moral reform and human",
                "unity transformed individuals and society.",
                size=LABEL_SIZE, color=SAGE, buff=GAP_SM * 1.1)
            self.below_head(answer, buff=GAP_MD * 1.4)
            self.play(Write(answer), run_time=t.fill(0.55))
            t.hold()

    def vocabulary(self):
        with self.beat("vocab_story") as t:
            self.clear_all(t)
            self.set_head(t, "The vocabulary tells the story")
            rows = lines(
                "The land was unparalleled — without equal.",
                "The people possessed eloquence — powerful expression.",
                "Civilization approached chaos — complete disorder.",
                "It stood on the verge — the edge.",
                size=BODY_SIZE, buff=GAP_SM * 1.3)
            self.below_head(rows, buff=GAP_MD * 1.4)
            for row in rows:
                self.play(Write(row), run_time=t.fill(0.16))
            self.vocab_first = rows
            t.hold()

        with self.beat("vocab_story2") as t:
            self.clear_all(t)
            rows = lines(
                f"He entered solitude — alone by choice.",
                "He spent time in meditation — deep reflection.",
                "He felt compassion — concern for humanity.",
                "Revelation was bestowed — given as a gift.",
                "He began to proclaim — announce publicly.",
                "Opponents wanted him to renounce — give up.",
                "The result was transformation — complete change.",
                size=LABEL_SIZE, buff=GAP_SM * 1.2)
            rows.move_to(ORIGIN)
            for row in rows:
                self.play(Write(row), run_time=t.fill(0.11))
            t.hold()

        with self.beat("vocab_point") as t:
            self.clear_all(t)
            point = lines("The vocabulary itself now tells",
                          "the chapter's story.", size=TITLE_SIZE)
            point.move_to(UP * 0.3)
            how = serif("that is how you remember words", BODY_SIZE, GREY)
            how.next_to(point, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(point), run_time=t.fill(0.35))
            self.play(Write(how), run_time=t.fill(0.25))
            t.hold()

    def grammar(self):
        with self.beat("grammar_noun") as t:
            self.clear_all(t)
            self.set_head(t, "Noun — it names something")
            rows = lines(
                f"person — Muhammad {PBUH}",
                "place — Makkah",
                "thing — cave",
                "idea — compassion",
                size=BODY_SIZE)
            self.below_head(rows, buff=GAP_MD * 1.6)
            for row in rows:
                self.play(Write(row), run_time=t.fill(0.14))
            t.hold()

        with self.beat("grammar_verb") as t:
            self.clear_all(t)
            self.set_head(t, "Verb — what happens, what is done")
            verbs = lines("lived · possessed · recited",
                          "proclaimed · changed", size=TITLE_SIZE)
            self.below_head(verbs, buff=GAP_MD * 1.8)
            self.play(Write(verbs), run_time=t.fill(0.45))
            t.hold()

        with self.beat("grammar_conj") as t:
            self.clear_all(t)
            self.set_head(t, "Conjunction — it joins ideas")
            words = serif("and · but · because", TITLE_SIZE)
            self.below_head(words, buff=GAP_MD * 1.3)
            example = VGroup(
                serif("The Arabs were eloquent,", BODY_SIZE),
                serif("but civilization was facing a crisis.", BODY_SIZE),
            ).arrange(DOWN, buff=GAP_SM)
            fit(example)
            example.next_to(words, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(words), run_time=t.fill(0.22))
            self.play(Write(example), run_time=t.fill(0.35))
            t.hold()

        with self.beat("but_idea") as t:
            self.clear_all(t)
            self.set_head(t, "One little conjunction")
            but = serif("but", TITLE_SIZE * 2.0, TERRACOTTA)
            self.below_head(but, buff=GAP_MD * 1.4)
            carries = lines("The Arabs were talented,",
                            "but the society was troubled.",
                            size=BODY_SIZE)
            carries.next_to(but, DOWN, buff=GAP_MD * 1.5)
            half = serif("that word is almost the entire first half "
                         "of this chapter", LABEL_SIZE, GREY)
            fit(half)
            half.next_to(carries, DOWN, buff=GAP_MD * 1.3)
            self.play(Write(but), run_time=t.fill(0.2))
            self.play(Write(carries), run_time=t.fill(0.3))
            self.play(Write(half), run_time=t.fill(0.22))
            t.hold()

    def reading_skill(self):
        with self.beat("main_idea") as t:
            self.clear_all(t)
            self.set_head(t, "Main idea")
            ask = lines("If I could remember only ONE idea",
                        "from this paragraph, what would it be?",
                        size=BODY_SIZE)
            self.below_head(ask, buff=GAP_MD * 1.5)
            rest = serif("everything that explains or proves it "
                         "= supporting detail", LABEL_SIZE, GREY)
            fit(rest)
            rest.next_to(ask, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(ask), run_time=t.fill(0.35))
            self.play(Write(rest), run_time=t.fill(0.25))
            t.hold()

        with self.beat("drama") as t:
            drama = serif("like a drama: one main character, "
                          "the rest supporting", BODY_SIZE, TERRACOTTA)
            fit(drama)
            drama.to_edge(DOWN, buff=GAP_MD * 1.6)
            self.play(Write(drama), run_time=t.fill(0.45))
            t.hold()

        with self.beat("main_idea_example") as t:
            self.clear_all(t)
            self.set_head(t, "Paragraph 2")
            details = lines("Ukaz · poetry competition · long poems",
                            "memory · eloquence",
                            size=BODY_SIZE, color=GREY)
            self.below_head(details, buff=GAP_MD * 1.3)
            label = serif("supporting detail", LABEL_SIZE, GREY)
            label.next_to(details, DOWN, buff=GAP_SM * 1.2)
            main = lines("The Arabs possessed remarkable memory",
                         "and linguistic ability.", size=BODY_SIZE)
            main.next_to(label, DOWN, buff=GAP_MD * 1.4)
            main_label = serif("main idea", LABEL_SIZE, TERRACOTTA)
            main_label.next_to(main, DOWN, buff=GAP_SM * 1.2)
            self.play(Write(details), Write(label), run_time=t.fill(0.25))
            self.play(Write(main), run_time=t.fill(0.3))
            self.play(Write(main_label), run_time=t.fill(0.12))
            t.hold()

    def recap(self):
        with self.beat("recap_intro") as t:
            self.clear_all(t)
            intro = lines("Before you leave,", "I want seven words",
                          "stored in your mind.", size=TITLE_SIZE)
            intro.move_to(ORIGIN)
            self.play(Write(intro), run_time=t.fill(0.5))
            t.hold()

        with self.beat("recap_words") as t:
            self.clear_all(t)
            arc = WordArc(SEVEN, size=BODY_SIZE, rows=2, lit=CHARCOAL)
            arc.move_to(ORIGIN)
            self.play(Write(arc), run_time=t.fill(0.55))
            self.recap_arc = arc
            t.hold()

        def gloss(t, index, text, extra=None):
            note = lines(*text, size=BODY_SIZE, color=GREY)
            note.to_edge(DOWN, buff=GAP_MD * 1.5)
            self.play(*self.recap_arc.focus(index), run_time=t.fill(0.12))
            self.play(Write(note), run_time=t.fill(0.3))
            return note

        with self.beat("recap_beauty") as t:
            self.recap_arc.to_edge(UP, buff=GAP_MD * 2.2)
            note = gloss(t, 0, ["beautiful nights, stars, the blazing sun"])
            note2 = lines("brilliance — long poems, spoken eloquently",
                          size=BODY_SIZE, color=GREY)
            note2.next_to(note, UP, buff=GAP_MD)
            self.play(*self.recap_arc.focus(1), Write(note2),
                      run_time=t.fill(0.25))
            self.last_note = VGroup(note, note2)
            t.hold()

        with self.beat("recap_breakdown") as t:
            self.play(FadeOut(self.last_note), run_time=t.fill(0.07))
            note = lines("chaos and moral crisis —",
                         "the building cracks, then falls",
                         size=BODY_SIZE, color=GREY)
            note.to_edge(DOWN, buff=GAP_MD * 1.5)
            self.play(*self.recap_arc.focus(2), run_time=t.fill(0.12))
            self.play(Write(note), run_time=t.fill(0.3))
            self.last_note = note
            t.hold()

        with self.beat("recap_cave") as t:
            self.play(FadeOut(self.last_note), run_time=t.fill(0.07))
            note = lines("solitude in the cave — not loneliness",
                         "then the calling: revelation and mission",
                         size=BODY_SIZE, color=GREY)
            note.to_edge(DOWN, buff=GAP_MD * 1.5)
            self.play(*self.recap_arc.focus(3), run_time=t.fill(0.1))
            self.play(Write(note), run_time=t.fill(0.28))
            self.play(*self.recap_arc.focus(4), run_time=t.fill(0.12))
            self.last_note = note
            t.hold()

        with self.beat("recap_courage") as t:
            self.play(FadeOut(self.last_note), run_time=t.fill(0.07))
            note = lines("they demanded he renounce it —",
                         "the sun in one hand, the moon in the other",
                         size=BODY_SIZE, color=GREY)
            note.to_edge(DOWN, buff=GAP_MD * 1.5)
            self.play(*self.recap_arc.focus(5), run_time=t.fill(0.12))
            self.play(Write(note), run_time=t.fill(0.32))
            self.last_note = note
            t.hold()

        with self.beat("recap_change") as t:
            self.play(FadeOut(self.last_note), run_time=t.fill(0.07))
            note = lines("an entire civilization transformed —",
                         "and 1400 years later, still spreading",
                         size=BODY_SIZE, color=GREY)
            note.to_edge(DOWN, buff=GAP_MD * 1.5)
            self.play(*self.recap_arc.focus(6), run_time=t.fill(0.12))
            self.play(Write(note), run_time=t.fill(0.32))
            self.last_note = note
            t.hold()

        with self.beat("seven_again") as t:
            self.play(FadeOut(self.last_note), run_time=t.fill(0.06))
            self.play(*self.recap_arc.dim_all(), run_time=t.fill(0.1))
            self.play(*[self.recap_arc.cell(i).animate.set_color(CHARCOAL)
                        for i in range(7)], run_time=t.fill(0.2))
            rebuild = serif("remember these — and you can rebuild "
                            "the chapter", BODY_SIZE, TERRACOTTA)
            fit(rebuild)
            rebuild.to_edge(DOWN, buff=GAP_MD * 1.8)
            self.play(Write(rebuild), run_time=t.fill(0.3))
            t.hold()

    def closing(self):
        with self.beat("final_line") as t:
            self.clear_all(t)
            quote = lines(
                "History remembers great events.",
                "But great events often begin with an idea,",
                "a conviction, and one person who refuses",
                "to abandon what he believes is true.",
                size=BODY_SIZE, buff=GAP_SM * 1.2)
            quote.move_to(UP * 0.5)
            journey = serif("from chaos to guidance — and from guidance "
                            "to transformation", LABEL_SIZE, GREY)
            fit(journey)
            journey.next_to(quote, DOWN, buff=GAP_MD * 1.6)
            self.play(Write(quote), run_time=t.fill(0.5))
            self.play(Write(journey), run_time=t.fill(0.25))
            t.hold()

        with self.beat("next_class") as t:
            self.clear_all(t)
            self.set_head(t, "Next class — board marks")
            items = lines("comprehension answers",
                          "main idea and supporting details",
                          "summary writing", "vocabulary",
                          size=BODY_SIZE)
            self.below_head(items, buff=GAP_MD * 1.4)
            read = serif("read the chapter again before then",
                         BODY_SIZE, TERRACOTTA)
            read.next_to(items, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(items), run_time=t.fill(0.35))
            self.play(Write(read), run_time=t.fill(0.22))
            t.hold()

        with self.beat("framework") as t:
            self.clear_all(t)
            title = serif("THE SAVIOUR OF MANKIND", TITLE_SIZE)
            title.to_edge(UP, buff=GAP_MD * 1.4)
            arc = WordArc(SEVEN, size=BODY_SIZE, rows=2, lit=CHARCOAL)
            arc.next_to(title, DOWN, buff=GAP_MD * 1.4)
            for cell in arc.cells:
                cell.set_color(CHARCOAL)
            main = serif("Main idea: a gifted society can still "
                         "need moral guidance", LABEL_SIZE, TERRACOTTA)
            fit(main)
            main.next_to(arc, DOWN, buff=GAP_MD * 1.5)
            anchors = lines(
                "unparalleled · eloquence · chaos · solitude",
                "compassion · proclaim · renounce · transformation",
                size=LABEL_SIZE, color=GREY, buff=GAP_SM)
            anchors.next_to(main, DOWN, buff=GAP_MD * 1.2)
            self.play(Write(title), run_time=t.fill(0.12))
            self.play(Write(arc), run_time=t.fill(0.28))
            self.play(Write(main), run_time=t.fill(0.2))
            self.play(Write(anchors), run_time=t.fill(0.25))
            self.framework = VGroup(title, arc, main, anchors)
            t.hold()

        with self.beat("skills") as t:
            skills = serif("skills: main idea · supporting detail · "
                           "noun · verb · conjunction", LABEL_SIZE, GREY)
            fit(skills)
            skills.to_edge(DOWN, buff=GAP_MD)
            self.play(Write(skills), run_time=t.fill(0.45))
            t.hold()

        with self.beat("homework") as t:
            self.clear_all(t)
            head = serif("Your homework", TITLE_SIZE)
            head.to_edge(UP, buff=GAP_MD * 1.8)
            items = lines("check your email for the workbook",
                          "download it and practise",
                          "bring your questions next class",
                          size=BODY_SIZE)
            items.next_to(head, DOWN, buff=GAP_MD * 1.6)
            bye = serif("see you next week, inshallah", BODY_SIZE, GREY)
            bye.next_to(items, DOWN, buff=GAP_MD * 1.8)
            self.play(Write(head), run_time=t.fill(0.15))
            self.play(Write(items), run_time=t.fill(0.35))
            self.play(Write(bye), run_time=t.fill(0.25))
            t.hold()
