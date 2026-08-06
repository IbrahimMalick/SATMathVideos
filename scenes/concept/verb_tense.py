"""Concept lecture: verb tense and the movie scene rule (R&W, L07).

Narration script: scripts/L07-verb-tense.md
Timeline consistency, the past perfect time machine, hypothetical would,
and the hidden time traveler challenge.
"""

import numpy as np

from manim import (
    Create,
    FadeOut,
    Line,
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
    TERRACOTTA,
    TITLE_SIZE,
    mono,
    serif,
)
from components.passage import PassageHighlight
from scenes.base import SATScene


def underline(mobject, color=SAGE):
    return Line(
        mobject.get_corner(DOWN + LEFT) + DOWN * GAP_SM,
        mobject.get_corner(DOWN + RIGHT) + DOWN * GAP_SM,
        color=color,
        stroke_width=3,
    )


class VerbTense(SATScene):
    scene_id = "concept.verb_tense"

    def construct(self):
        self.margin_note = mono("L07 · verb tense", MARGIN_SIZE)
        self.margin_note.to_corner(UP + LEFT, buff=GAP_SM)
        self.add(self.margin_note)
        self.section_head = None
        self.work = VGroup()

        self.opening()
        self.movie_scene()
        self.time_machine()
        self.hypotheticals()
        self.time_traveler()
        self.wrap_up()

    # -------------------------------------------------------------- helpers

    def clear_all(self, t, fraction=0.1):
        old = [m for m in self.mobjects if m is not self.margin_note]
        if old:
            self.play(*[FadeOut(m) for m in old], run_time=t.fill(fraction))
        self.work = VGroup()
        self.section_head = None

    def swap_work(self, t, fraction=0.08):
        if len(self.work) > 0:
            self.play(*[FadeOut(m) for m in self.work], run_time=t.fill(fraction))
            self.work = VGroup()

    def set_head(self, t, text, fraction=0.25):
        head = serif(text, TITLE_SIZE)
        head.to_edge(UP, buff=GAP_MD * 1.6)
        self.play(Write(head), run_time=t.fill(fraction))
        self.section_head = head

    # ------------------------------------------------------------- sections

    def opening(self):
        hook = serif("one verb can break the timeline", BODY_SIZE)
        hook.move_to(UP * 1.2)
        hook_line = underline(hook, TERRACOTTA)

        with self.beat("hook") as t:
            self.play(Write(hook), run_time=t.fill(0.35))
            self.play(Create(hook_line), run_time=t.fill(0.12))
            t.hold()

        watch = serif("a digital watch in an 1800s movie scene", LABEL_SIZE, GREY)
        watch.next_to(hook, DOWN, buff=GAP_MD * 1.4)

        with self.beat("watch") as t:
            self.play(Write(watch), run_time=t.fill(0.3))
            t.hold()

        challenge = mono("a hidden time traveler is coming — stay alert",
                         MARGIN_SIZE)
        challenge.next_to(watch, DOWN, buff=GAP_MD * 1.2)

        with self.beat("promise") as t:
            self.play(Write(challenge), run_time=t.fill(0.3))
            t.hold()

        title = serif("Verb Tense", TITLE_SIZE * 1.25)
        subtitle = serif("the movie scene rule", BODY_SIZE, GREY)
        subtitle.next_to(title, DOWN, buff=GAP_MD)
        card = VGroup(title, subtitle).move_to(UP * 1.6)

        with self.beat("title") as t:
            self.play(FadeOut(hook), FadeOut(hook_line), FadeOut(watch),
                      FadeOut(challenge), run_time=t.fill(0.1))
            self.play(Write(title), run_time=t.fill(0.3))
            self.play(Write(subtitle), run_time=t.fill(0.2))
            self.work.add(card)
            t.hold()

        maria = VGroup(
            PassageHighlight("Maria walked to the library.", highlight="walked",
                             highlight_color=SAGE),
            PassageHighlight("Maria walks to the library.", highlight="walks",
                             highlight_color=SAGE),
            PassageHighlight("Maria will walk to the library.",
                             highlight="will walk", highlight_color=SAGE),
        ).arrange(DOWN, buff=GAP_SM * 1.5, aligned_edge=LEFT)
        maria.next_to(card, DOWN, buff=GAP_MD * 1.4)
        labels = VGroup(
            serif("past", MARGIN_SIZE, GREY),
            serif("present", MARGIN_SIZE, GREY),
            serif("future", MARGIN_SIZE, GREY),
        )
        for label, line in zip(labels, maria):
            label.next_to(line, RIGHT, buff=GAP_MD * 1.4)

        with self.beat("maria") as t:
            for line, label in zip(maria, labels):
                self.play(Write(line), run_time=t.fill(0.16))
                self.play(Write(label), run_time=t.fill(0.06))
            self.work.add(maria, labels)
            t.hold()

        consistent = serif("the real challenge: keeping it consistent",
                           LABEL_SIZE)
        consistent.next_to(maria, DOWN, buff=GAP_MD * 1.2)
        consistent.move_to(np.array([0, consistent.get_center()[1], 0]))

        with self.beat("consistent") as t:
            self.play(Write(consistent), run_time=t.fill(0.3))
            self.work.add(consistent)
            t.hold()

    def movie_scene(self):
        with self.beat("movie") as t:
            self.clear_all(t)
            self.set_head(t, "Every paragraph is a scene")
            rule = serif("a scene that begins in the past stays in the past",
                         LABEL_SIZE, GREY)
            rule.next_to(self.section_head, DOWN, buff=GAP_MD)
            self.play(Write(rule), run_time=t.fill(0.3))
            self.section_head = VGroup(self.section_head, rule)
            t.hold()

        wrong = PassageHighlight(
            "The scientist entered the laboratory, examines the samples, "
            "and recorded the results.",
            highlight="examines",
            highlight_color=TERRACOTTA,
        )
        wrong.next_to(self.section_head, DOWN, buff=GAP_MD * 1.3)
        watch_note = serif("examines — the digital watch", LABEL_SIZE, GREY)
        watch_note.next_to(wrong, DOWN, buff=GAP_SM * 1.5)

        with self.beat("scientist") as t:
            self.play(Write(wrong), run_time=t.fill(0.35))
            self.play(Write(watch_note), run_time=t.fill(0.2))
            self.work.add(wrong, watch_note)
            t.hold()

        fixed = PassageHighlight(
            "The scientist entered the laboratory, examined the samples, "
            "and recorded the results.",
            highlight="examined",
            highlight_color=SAGE,
        )
        fixed.next_to(watch_note, DOWN, buff=GAP_MD)

        with self.beat("scientist_fix") as t:
            self.play(Write(fixed), run_time=t.fill(0.4))
            self.work.add(fixed)
            t.hold()

        with self.beat("plant") as t:
            self.swap_work(t)
            plant = PassageHighlight(
                "The plant belongs to a tropical family, grows in warm "
                "climates, and produces bright flowers.",
                highlight="belongs",
                highlight_color=SAGE,
            )
            plant.next_to(self.section_head, DOWN, buff=GAP_MD * 1.3)
            plant_note = serif("general facts — present tense throughout",
                               LABEL_SIZE, GREY)
            plant_note.next_to(plant, DOWN, buff=GAP_SM * 1.5)
            self.play(Write(plant), run_time=t.fill(0.35))
            self.play(Write(plant_note), run_time=t.fill(0.2))
            self.work.add(plant, plant_note)
            t.hold()

        plant_wrong = PassageHighlight(
            "The plant belongs to a tropical family, grew in warm climates, "
            "and produces bright flowers.",
            highlight="grew",
            highlight_color=TERRACOTTA,
        )
        plant_wrong.next_to(self.work[1], DOWN, buff=GAP_MD)

        with self.beat("plant_wrong") as t:
            self.play(Write(plant_wrong), run_time=t.fill(0.4))
            self.work.add(plant_wrong)
            t.hold()

        with self.beat("strategy1") as t:
            self.swap_work(t)
            strat = VGroup(
                serif("read the surrounding verbs — they set the timeline",
                      BODY_SIZE),
                serif("is · belongs · grows  →  present", LABEL_SIZE, GREY),
                serif("was · belonged · grew  →  past", LABEL_SIZE, GREY),
                serif("never judge one verb in isolation", LABEL_SIZE),
            ).arrange(DOWN, buff=GAP_SM * 1.5, aligned_edge=LEFT)
            strat.next_to(self.section_head, DOWN, buff=GAP_MD * 1.3)
            self.play(Write(strat), run_time=t.fill(0.5))
            self.work.add(strat)
            t.hold()

    def time_machine(self):
        with self.beat("shift") as t:
            self.clear_all(t)
            self.set_head(t, "When time really changes")
            note = serif("sometimes the story moves — then tense must move too",
                         LABEL_SIZE, GREY)
            note.next_to(self.section_head, DOWN, buff=GAP_MD)
            self.play(Write(note), run_time=t.fill(0.3))
            self.section_head = VGroup(self.section_head, note)
            t.hold()

        formula = serif("past perfect: had + past participle — the time machine",
                        BODY_SIZE)
        formula.next_to(self.section_head, DOWN, buff=GAP_MD * 1.2)
        formula_line = underline(formula)

        with self.beat("past_perfect") as t:
            self.play(Write(formula), run_time=t.fill(0.3))
            self.play(Create(formula_line), run_time=t.fill(0.12))
            self.work.add(formula, formula_line)
            t.hold()

        martha = PassageHighlight(
            "By the time Martha retired, she had given hundreds of "
            "performances.",
            highlight="had given",
            highlight_color=SAGE,
        )
        martha.next_to(formula, DOWN, buff=GAP_MD * 1.2)
        martha_note = serif("performances first, retirement later",
                            LABEL_SIZE, GREY)
        martha_note.next_to(martha, DOWN, buff=GAP_SM * 1.5)

        with self.beat("martha") as t:
            self.play(Write(martha), run_time=t.fill(0.35))
            self.play(Write(martha_note), run_time=t.fill(0.2))
            self.work.add(martha, martha_note)
            t.hold()

        fire = PassageHighlight(
            "By the time the firefighters arrived, the residents had left "
            "the building.",
            highlight="had left",
            highlight_color=SAGE,
            width=44,
        )
        fire.next_to(martha_note, DOWN, buff=GAP_MD)

        with self.beat("firefighters") as t:
            self.play(Write(fire), run_time=t.fill(0.4))
            self.work.add(fire)
            t.hold()

        with self.beat("meeting") as t:
            self.swap_work(t)
            meeting = PassageHighlight(
                "By the time the meeting began, the manager had reviewed "
                "the proposal.",
                highlight="had reviewed",
                highlight_color=SAGE,
            )
            meeting.next_to(self.section_head, DOWN, buff=GAP_MD * 1.3)
            signal = serif('"by the time" is the signal', LABEL_SIZE, GREY)
            signal.next_to(meeting, DOWN, buff=GAP_SM * 1.5)
            self.play(Write(meeting), run_time=t.fill(0.35))
            self.play(Write(signal), run_time=t.fill(0.2))
            self.work.add(meeting, signal)
            t.hold()

        caution = serif("only when one past event precedes another",
                        LABEL_SIZE, TERRACOTTA)
        caution.next_to(self.work[1], DOWN, buff=GAP_MD)

        with self.beat("pp_caution") as t:
            self.play(Write(caution), run_time=t.fill(0.3))
            self.work.add(caution)
            t.hold()

    def hypotheticals(self):
        with self.beat("hypo") as t:
            self.clear_all(t)
            self.set_head(t, "Hypotheticals: would")
            maya = PassageHighlight(
                "If Maya had more time, she would learn another language.",
                highlight="would learn",
                highlight_color=SAGE,
            )
            maya.next_to(self.section_head, DOWN, buff=GAP_MD * 1.3)
            maya_note = serif("imagined, not confirmed", LABEL_SIZE, GREY)
            maya_note.next_to(maya, DOWN, buff=GAP_SM * 1.5)
            self.play(Write(maya), run_time=t.fill(0.35))
            self.play(Write(maya_note), run_time=t.fill(0.2))
            self.work.add(maya, maya_note)
            t.hold()

        equip = PassageHighlight(
            "With better equipment, the team would complete the project "
            "more quickly.",
            highlight="would complete",
            highlight_color=SAGE,
        )
        equip.next_to(self.work[1], DOWN, buff=GAP_MD)

        with self.beat("equipment") as t:
            self.play(Write(equip), run_time=t.fill(0.4))
            self.work.add(equip)
            t.hold()

        inventor = PassageHighlight(
            "In 1995, the inventor did not know that her discovery would "
            "transform the industry.",
            highlight="would transform",
            highlight_color=SAGE,
        )
        inventor.next_to(equip, DOWN, buff=GAP_MD)
        inventor_note = serif("the future, seen from the past", LABEL_SIZE, GREY)
        inventor_note.next_to(inventor, DOWN, buff=GAP_SM * 1.5)

        with self.beat("would_past") as t:
            self.play(Write(inventor), run_time=t.fill(0.35))
            self.play(Write(inventor_note), run_time=t.fill(0.2))
            self.work.add(inventor, inventor_note)
            t.hold()

    def time_traveler(self):
        plain = PassageHighlight(
            "Last summer, Daniel traveled across the country, visited "
            "several national parks, and writes about the experience in "
            "his journal.",
        )

        with self.beat("traveler") as t:
            self.clear_all(t)
            self.set_head(t, "The hidden time traveler")
            plain.next_to(self.section_head, DOWN, buff=GAP_MD * 1.3)
            ask = mono("which verb does not belong?", MARGIN_SIZE)
            ask.next_to(plain, DOWN, buff=GAP_MD)
            self.play(Write(plain), run_time=t.fill(0.45))
            self.play(Write(ask), run_time=t.fill(0.15))
            self.work.add(plain, ask)
            t.hold()

        marked = PassageHighlight(
            "Last summer, Daniel traveled across the country, visited "
            "several national parks, and writes about the experience in "
            "his journal.",
            highlight="writes",
            highlight_color=TERRACOTTA,
        )
        marked.move_to(plain)

        with self.beat("reveal") as t:
            self.play(FadeOut(self.work[0]), run_time=t.fill(0.08))
            self.work.remove(self.work[0])
            self.play(Write(marked), run_time=t.fill(0.35))
            self.work.add(marked)
            t.hold()

        fixed = PassageHighlight(
            "Last summer, Daniel traveled across the country, visited "
            "several national parks, and wrote about the experience in "
            "his journal.",
            highlight="wrote",
            highlight_color=SAGE,
        )
        fixed.next_to(self.work[0], DOWN, buff=GAP_MD * 1.1)

        with self.beat("traveler_fix") as t:
            self.play(Write(fixed), run_time=t.fill(0.45))
            self.work.add(fixed)
            t.hold()

    def wrap_up(self):
        steps = VGroup(
            serif("1  identify the timeline", BODY_SIZE),
            serif("2  read the surrounding verbs", BODY_SIZE),
            serif("3  a real time change? had + participle", BODY_SIZE),
            serif("4  imagined result? would", BODY_SIZE),
        ).arrange(DOWN, buff=GAP_MD * 0.9, aligned_edge=LEFT)

        with self.beat("method") as t:
            self.clear_all(t)
            self.set_head(t, "The method")
            steps.next_to(self.section_head, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(steps), run_time=t.fill(0.5))
            self.work.add(steps)
            t.hold()

        director = serif("you are directing the scene", BODY_SIZE)
        director.next_to(steps, DOWN, buff=GAP_MD * 1.4)
        director_line = underline(director)

        with self.beat("director") as t:
            self.play(Write(director), run_time=t.fill(0.3))
            self.play(Create(director_line), run_time=t.fill(0.12))
            self.work.add(director, director_line)
            t.hold()

        end = mono("see you soon", MARGIN_SIZE)
        end.to_edge(DOWN, buff=GAP_MD)

        with self.beat("outro") as t:
            self.play(Write(end), run_time=t.fill(0.4))
            t.hold()
