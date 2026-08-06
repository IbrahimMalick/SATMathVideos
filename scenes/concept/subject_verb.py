"""Concept lecture: subject-verb agreement (Reading & Writing, L06).

Narration script: scripts/L06-subject-verb.md
The Lonely Subject Rule, then bodyguard phrases, then practice.
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


class SubjectVerb(SATScene):
    scene_id = "concept.subject_verb"

    def construct(self):
        self.margin_note = mono("L06 · agreement", MARGIN_SIZE)
        self.margin_note.to_corner(UP + LEFT, buff=GAP_SM)
        self.add(self.margin_note)
        self.section_head = None
        self.work = VGroup()

        self.opening()
        self.lonely_subject()
        self.bodyguards()
        self.strategy_and_practice()
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
        trap = serif("the closest noun is often a trap", BODY_SIZE)
        trap.move_to(UP * 1.0)
        trap_line = underline(trap, TERRACOTTA)

        with self.beat("hook") as t:
            self.play(Write(trap), run_time=t.fill(0.35))
            self.play(Create(trap_line), run_time=t.fill(0.12))
            t.hold()

        promise = VGroup(
            serif("find the real subject in any sentence", LABEL_SIZE, GREY),
            serif("one trick to eliminate wrong verbs fast", LABEL_SIZE, GREY),
        ).arrange(DOWN, buff=GAP_SM * 1.3)
        promise.next_to(trap, DOWN, buff=GAP_MD * 1.5)

        with self.beat("promise") as t:
            self.play(Write(promise), run_time=t.fill(0.4))
            t.hold()

        challenge = mono("a hidden error is coming — stay alert", MARGIN_SIZE)
        challenge.next_to(promise, DOWN, buff=GAP_MD * 1.3)

        with self.beat("challenge") as t:
            self.play(Write(challenge), run_time=t.fill(0.3))
            t.hold()

        title = serif("Subject–Verb Agreement", TITLE_SIZE * 1.2)
        subtitle = serif("the lonely subject rule", BODY_SIZE, GREY)
        subtitle.next_to(title, DOWN, buff=GAP_MD)
        card = VGroup(title, subtitle).move_to(ORIGIN)

        with self.beat("title") as t:
            self.play(FadeOut(trap), FadeOut(trap_line), FadeOut(promise),
                      FadeOut(challenge), run_time=t.fill(0.1))
            self.play(Write(title), run_time=t.fill(0.35))
            self.play(Write(subtitle), run_time=t.fill(0.2))
            self.work.add(card)
            t.hold()

    def lonely_subject(self):
        with self.beat("traveler") as t:
            self.clear_all(t)
            self.set_head(t, "A lonely traveler and a tiny pet")
            traveler = serif("one lonely subject", BODY_SIZE)
            pet = serif("+ S", TITLE_SIZE * 1.1, TERRACOTTA)
            row = VGroup(traveler, pet).arrange(RIGHT, buff=GAP_MD * 1.4)
            row.next_to(self.section_head, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(traveler), run_time=t.fill(0.25))
            self.play(Write(pet), run_time=t.fill(0.2))
            self.work.add(row)
            t.hold()

        rule = serif("one person, place, object, or idea → verb + s",
                     LABEL_SIZE, GREY)
        rule.next_to(self.work[0], DOWN, buff=GAP_MD)

        with self.beat("rule") as t:
            self.play(Write(rule), run_time=t.fill(0.3))
            self.work.add(rule)
            t.hold()

        one = PassageHighlight(
            "The researcher believes the evidence.",
            highlight="believes",
            highlight_color=SAGE,
        )
        one.next_to(rule, DOWN, buff=GAP_MD * 1.2)

        with self.beat("researcher") as t:
            self.play(Write(one), run_time=t.fill(0.35))
            self.work.add(one)
            t.hold()

        many = PassageHighlight(
            "The researchers believe the evidence.",
            highlight="believe",
            highlight_color=SAGE,
        )
        many.next_to(one, DOWN, buff=GAP_MD)

        with self.beat("researchers") as t:
            self.play(Write(many), run_time=t.fill(0.35))
            self.work.add(many)
            t.hold()

        with self.beat("lonely_rule") as t:
            self.swap_work(t)
            lonely = serif("one → verb + s   ·   many → verb", BODY_SIZE)
            lonely.next_to(self.section_head, DOWN, buff=GAP_MD * 1.5)
            lonely_line = underline(lonely)
            self.play(Write(lonely), run_time=t.fill(0.3))
            self.play(Create(lonely_line), run_time=t.fill(0.12))
            self.work.add(lonely, lonely_line)
            t.hold()

        dog = PassageHighlight(
            "The dog runs through the park.", highlight="runs",
            highlight_color=SAGE,
        )
        dog.next_to(self.work[0], DOWN, buff=GAP_MD * 1.3)

        with self.beat("dog") as t:
            self.play(Write(dog), run_time=t.fill(0.35))
            self.work.add(dog)
            t.hold()

        dogs = PassageHighlight(
            "The dogs run through the park.", highlight="run",
            highlight_color=SAGE,
        )
        dogs.next_to(dog, DOWN, buff=GAP_MD)

        with self.beat("dogs") as t:
            self.play(Write(dogs), run_time=t.fill(0.35))
            self.work.add(dogs)
            t.hold()

    def bodyguards(self):
        with self.beat("bodyguard") as t:
            self.clear_all(t)
            self.set_head(t, "The bodyguard phrase")
            intro = serif("it stands between subject and verb — to distract you",
                          LABEL_SIZE, GREY)
            intro.next_to(self.section_head, DOWN, buff=GAP_MD)
            self.play(Write(intro), run_time=t.fill(0.3))
            self.section_head = VGroup(self.section_head, intro)
            t.hold()

        wood_wrong = PassageHighlight(
            "The feathers of the woodpecker has evolved over time.",
            highlight="of the woodpecker",
            highlight_color=TERRACOTTA,
        )
        wood_wrong.next_to(self.section_head, DOWN, buff=GAP_MD * 1.3)
        wood_q = serif("what has evolved? not the woodpecker — the feathers",
                       LABEL_SIZE, GREY)
        wood_q.next_to(wood_wrong, DOWN, buff=GAP_MD)

        with self.beat("woodpecker") as t:
            self.play(Write(wood_wrong), run_time=t.fill(0.35))
            self.play(Write(wood_q), run_time=t.fill(0.25))
            self.work.add(wood_wrong, wood_q)
            t.hold()

        wood_right = PassageHighlight(
            "The feathers have evolved over time.",
            highlight="have",
            highlight_color=SAGE,
        )
        wood_right.next_to(wood_q, DOWN, buff=GAP_MD)

        with self.beat("woodpecker2") as t:
            self.play(Write(wood_right), run_time=t.fill(0.35))
            self.work.add(wood_right)
            t.hold()

        with self.beat("box") as t:
            self.swap_work(t)
            box = PassageHighlight(
                "The box of old photographs sits in the attic.",
                highlight="of old photographs",
                highlight_color=TERRACOTTA,
            )
            box.next_to(self.section_head, DOWN, buff=GAP_MD * 1.3)
            box_note = PassageHighlight(
                "The box sits in the attic.", highlight="sits",
                highlight_color=SAGE,
            )
            box_note.next_to(box, DOWN, buff=GAP_MD)
            self.play(Write(box), run_time=t.fill(0.35))
            self.play(Write(box_note), run_time=t.fill(0.3))
            self.work.add(box, box_note)
            t.hold()

        with self.beat("players") as t:
            self.swap_work(t)
            players_wrong = PassageHighlight(
                "The players on the field runs every morning.",
                highlight="on the field",
                highlight_color=TERRACOTTA,
            )
            players_wrong.next_to(self.section_head, DOWN, buff=GAP_MD * 1.3)
            players_right = PassageHighlight(
                "The players on the field run every morning.",
                highlight="run",
                highlight_color=SAGE,
            )
            players_right.next_to(players_wrong, DOWN, buff=GAP_MD)
            self.play(Write(players_wrong), run_time=t.fill(0.35))
            self.play(Write(players_right), run_time=t.fill(0.3))
            self.work.add(players_wrong, players_right)
            t.hold()

    def strategy_and_practice(self):
        steps = VGroup(
            serif("1  find the verb", BODY_SIZE),
            serif("2  ask: who or what performs the action?", BODY_SIZE),
            serif("3  ignore the phrase in between", BODY_SIZE),
        ).arrange(DOWN, buff=GAP_MD, aligned_edge=LEFT)

        with self.beat("strategy") as t:
            self.clear_all(t)
            self.set_head(t, "The strategy")
            steps.next_to(self.section_head, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(steps), run_time=t.fill(0.45))
            self.work.add(steps)
            t.hold()

        preps = serif("of · in · on · by · with · near — bodyguard words",
                      LABEL_SIZE, GREY)
        preps.next_to(steps, DOWN, buff=GAP_MD * 1.2)

        with self.beat("preps") as t:
            self.play(Write(preps), run_time=t.fill(0.3))
            self.work.add(preps)
            t.hold()

        with self.beat("coins") as t:
            self.swap_work(t)
            coins = PassageHighlight(
                "The collection of rare coins belongs to the museum.",
                highlight="belongs",
                highlight_color=SAGE,
            )
            coins.next_to(self.section_head, DOWN, buff=GAP_MD * 1.3)
            coins_note = serif("the collection belongs — singular", LABEL_SIZE, GREY)
            coins_note.next_to(coins, DOWN, buff=GAP_MD)
            self.play(Write(coins), run_time=t.fill(0.35))
            self.play(Write(coins_note), run_time=t.fill(0.2))
            self.work.add(coins, coins_note)
            t.hold()

        effects = PassageHighlight(
            "The effects of the new policy concern many employees.",
            highlight="concern",
            highlight_color=SAGE,
        )
        effects.next_to(self.work[1], DOWN, buff=GAP_MD * 1.2)
        effects_note = serif("the effects concern — plural", LABEL_SIZE, GREY)
        effects_note.next_to(effects, DOWN, buff=GAP_MD)

        with self.beat("effects") as t:
            self.play(Write(effects), run_time=t.fill(0.35))
            self.play(Write(effects_note), run_time=t.fill(0.2))
            self.work.add(effects, effects_note)
            t.hold()

    def wrap_up(self):
        with self.beat("habit") as t:
            self.clear_all(t)
            self.set_head(t, "The habit")
            habit = VGroup(
                serif("never match the verb to the closest noun", BODY_SIZE),
                serif("find the true subject, then apply the rule", LABEL_SIZE, GREY),
            ).arrange(DOWN, buff=GAP_SM * 1.5)
            habit.next_to(self.section_head, DOWN, buff=GAP_MD * 1.4)
            habit_line = underline(habit[0])
            self.play(Write(habit[0]), run_time=t.fill(0.3))
            self.play(Create(habit_line), run_time=t.fill(0.1))
            self.play(Write(habit[1]), run_time=t.fill(0.2))
            self.work.add(habit, habit_line)
            t.hold()

        pairs = VGroup(
            serif("the bird sings · the birds sing", LABEL_SIZE),
            serif("the teacher explains · the teachers explain", LABEL_SIZE),
            serif("the machine works · the machines work", LABEL_SIZE),
        ).arrange(DOWN, buff=GAP_SM * 1.4, aligned_edge=LEFT)
        pairs.next_to(self.work[0], DOWN, buff=GAP_MD * 1.2)

        with self.beat("pairs") as t:
            self.play(Write(pairs), run_time=t.fill(0.45))
            self.work.add(pairs)
            t.hold()

        closing = serif("calmly move past the bodyguard", BODY_SIZE)
        closing.next_to(pairs, DOWN, buff=GAP_MD * 1.2)
        closing_line = underline(closing)

        with self.beat("closing") as t:
            self.play(Write(closing), run_time=t.fill(0.3))
            self.play(Create(closing_line), run_time=t.fill(0.12))
            t.hold()
