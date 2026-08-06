"""Concept lecture: pronoun agreement and the mirror rule (R&W, L08).

Narration script: scripts/L08-pronoun-agreement.md
Antecedents as reflections, collective nouns, point of view, ambiguity,
and the distorted reflection challenge.
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


class PronounAgreement(SATScene):
    scene_id = "concept.pronoun_agreement"

    def construct(self):
        self.margin_note = mono("L08 · pronouns", MARGIN_SIZE)
        self.margin_note.to_corner(UP + LEFT, buff=GAP_SM)
        self.add(self.margin_note)
        self.section_head = None
        self.work = VGroup()

        self.opening()
        self.mismatches()
        self.collectives()
        self.point_of_view()
        self.ambiguity()
        self.challenges()
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
        hook = serif("one word can blur a whole paragraph", BODY_SIZE)
        hook.move_to(UP * 1.2)
        hook_line = underline(hook, TERRACOTTA)

        with self.beat("hook") as t:
            self.play(Write(hook), run_time=t.fill(0.35))
            self.play(Create(hook_line), run_time=t.fill(0.12))
            t.hold()

        promise = VGroup(
            serif("connect every pronoun to its noun", LABEL_SIZE, GREY),
            serif("why team, company, committee are tricky", LABEL_SIZE, GREY),
        ).arrange(DOWN, buff=GAP_SM * 1.3)
        promise.next_to(hook, DOWN, buff=GAP_MD * 1.4)

        with self.beat("promise") as t:
            self.play(Write(promise), run_time=t.fill(0.4))
            t.hold()

        challenge = mono("a distorted reflection is coming — stay alert",
                         MARGIN_SIZE)
        challenge.next_to(promise, DOWN, buff=GAP_MD * 1.2)

        with self.beat("challenge") as t:
            self.play(Write(challenge), run_time=t.fill(0.3))
            t.hold()

        title = serif("Pronoun Agreement", TITLE_SIZE * 1.2)
        subtitle = serif("the mirror rule", BODY_SIZE, GREY)
        subtitle.next_to(title, DOWN, buff=GAP_MD)
        card = VGroup(title, subtitle).move_to(UP * 1.4)
        giant = serif("a giant's mirror should not show a kitten",
                      LABEL_SIZE, GREY)
        giant.next_to(subtitle, DOWN, buff=GAP_MD * 1.4)

        with self.beat("mirror") as t:
            self.play(FadeOut(hook), FadeOut(hook_line), FadeOut(promise),
                      FadeOut(challenge), run_time=t.fill(0.1))
            self.play(Write(title), run_time=t.fill(0.3))
            self.play(Write(subtitle), run_time=t.fill(0.15))
            self.play(Write(giant), run_time=t.fill(0.2))
            self.work.add(card, giant)
            t.hold()

        defs = VGroup(
            serif("a pronoun replaces a noun — he, she, it, they, we, you",
                  LABEL_SIZE),
            serif("its antecedent is the noun that gave it identity",
                  LABEL_SIZE, GREY),
        ).arrange(DOWN, buff=GAP_SM * 1.4)
        defs.next_to(giant, DOWN, buff=GAP_MD * 1.3)

        with self.beat("pronoun_def") as t:
            self.play(Write(defs), run_time=t.fill(0.4))
            self.work.add(defs)
            t.hold()

        with self.beat("cacao") as t:
            self.swap_work(t)
            self.set_head(t, "The reflection must match", fraction=0.15)
            cacao = PassageHighlight(
                "The cacao bean develops its flavor during processing.",
                highlight="its",
                highlight_color=SAGE,
            )
            cacao.next_to(self.section_head, DOWN, buff=GAP_MD * 1.3)
            cacao_note = serif("one bean → its", LABEL_SIZE, GREY)
            cacao_note.next_to(cacao, DOWN, buff=GAP_SM * 1.5)
            self.play(Write(cacao), run_time=t.fill(0.3))
            self.play(Write(cacao_note), run_time=t.fill(0.15))
            self.work.add(cacao, cacao_note)
            t.hold()

        plural = PassageHighlight(
            "The cacao beans develop their flavor during processing.",
            highlight="their",
            highlight_color=SAGE,
        )
        plural.next_to(self.work[1], DOWN, buff=GAP_MD)
        plural_note = serif("many beans → their", LABEL_SIZE, GREY)
        plural_note.next_to(plural, DOWN, buff=GAP_SM * 1.5)

        with self.beat("cacao_plural") as t:
            self.play(Write(plural), run_time=t.fill(0.3))
            self.play(Write(plural_note), run_time=t.fill(0.15))
            self.work.add(plural, plural_note)
            t.hold()

        rule = serif("singular noun → singular pronoun · plural → plural",
                     BODY_SIZE)
        rule.to_edge(DOWN, buff=GAP_MD)
        rule_line = underline(rule)

        with self.beat("mirror_rule") as t:
            self.play(Write(rule), run_time=t.fill(0.3))
            self.play(Create(rule_line), run_time=t.fill(0.12))
            self.work.add(rule, rule_line)
            t.hold()

    def mismatches(self):
        with self.beat("bicycle") as t:
            self.clear_all(t)
            self.set_head(t, "Broken reflections")
            bike_wrong = PassageHighlight(
                "The bicycle lost their front wheel.",
                highlight="their",
                highlight_color=TERRACOTTA,
            )
            bike_wrong.next_to(self.section_head, DOWN, buff=GAP_MD * 1.3)
            self.play(Write(bike_wrong), run_time=t.fill(0.35))
            self.work.add(bike_wrong)
            t.hold()

        bike_right = PassageHighlight(
            "The bicycle lost its front wheel.",
            highlight="its",
            highlight_color=SAGE,
        )
        bike_right.next_to(self.work[0], DOWN, buff=GAP_MD)

        with self.beat("bicycle_fix") as t:
            self.play(Write(bike_right), run_time=t.fill(0.35))
            self.work.add(bike_right)
            t.hold()

        stu_wrong = PassageHighlight(
            "The students submitted her assignments before noon.",
            highlight="her",
            highlight_color=TERRACOTTA,
        )
        stu_right = PassageHighlight(
            "The students submitted their assignments before noon.",
            highlight="their",
            highlight_color=SAGE,
        )
        pair = VGroup(stu_wrong, stu_right).arrange(
            DOWN, buff=GAP_MD, aligned_edge=LEFT
        )
        pair.next_to(bike_right, DOWN, buff=GAP_MD * 1.2)

        with self.beat("students") as t:
            self.play(Write(stu_wrong), run_time=t.fill(0.3))
            self.play(Write(stu_right), run_time=t.fill(0.3))
            self.work.add(pair)
            t.hold()

        with self.beat("method1") as t:
            self.swap_work(t)
            method = VGroup(
                serif("see a pronoun?  look backward", BODY_SIZE),
                serif("find the noun it replaces", LABEL_SIZE, GREY),
                serif("singular or plural?  that decides", LABEL_SIZE, GREY),
            ).arrange(DOWN, buff=GAP_SM * 1.5, aligned_edge=LEFT)
            method.next_to(self.section_head, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(method), run_time=t.fill(0.45))
            self.work.add(method)
            t.hold()

    def collectives(self):
        with self.beat("collective") as t:
            self.clear_all(t)
            self.set_head(t, "Deceptive group nouns")
            words = serif("team · company · committee · family · jury · audience",
                          LABEL_SIZE)
            words.next_to(self.section_head, DOWN, buff=GAP_MD)
            note = serif("one unit acting together → treated as singular",
                         LABEL_SIZE, GREY)
            note.next_to(words, DOWN, buff=GAP_SM * 1.5)
            self.play(Write(words), run_time=t.fill(0.3))
            self.play(Write(note), run_time=t.fill(0.2))
            self.section_head = VGroup(self.section_head, words, note)
            t.hold()

        theater = PassageHighlight(
            "The theater company announced its new season.",
            highlight="its",
            highlight_color=SAGE,
        )
        theater.next_to(self.section_head, DOWN, buff=GAP_MD * 1.2)
        not_their = serif("not: announced their new season", LABEL_SIZE, TERRACOTTA)
        not_their.next_to(theater, DOWN, buff=GAP_SM * 1.5)

        with self.beat("theater") as t:
            self.play(Write(theater), run_time=t.fill(0.35))
            self.play(Write(not_their), run_time=t.fill(0.2))
            self.work.add(theater, not_their)
            t.hold()

        team = PassageHighlight(
            "The team changed its strategy during the second half.",
            highlight="its",
            highlight_color=SAGE,
        )
        team.next_to(not_their, DOWN, buff=GAP_MD)

        with self.beat("team_ex") as t:
            self.play(Write(team), run_time=t.fill(0.4))
            self.work.add(team)
            t.hold()

        with self.beat("more_collective") as t:
            self.swap_work(t)
            trio = VGroup(
                PassageHighlight("The committee published its final report.",
                                 highlight="its", highlight_color=SAGE),
                PassageHighlight("The jury reached its decision.",
                                 highlight="its", highlight_color=SAGE),
                PassageHighlight("The organization updated its policy.",
                                 highlight="its", highlight_color=SAGE),
            ).arrange(DOWN, buff=GAP_SM * 1.6, aligned_edge=LEFT)
            trio.next_to(self.section_head, DOWN, buff=GAP_MD * 1.2)
            self.play(Write(trio), run_time=t.fill(0.5))
            self.work.add(trio)
            t.hold()

    def point_of_view(self):
        with self.beat("camera") as t:
            self.clear_all(t)
            self.set_head(t, "Keep the camera still")
            note = serif("the point of view must not jump mid-scene",
                         LABEL_SIZE, GREY)
            note.next_to(self.section_head, DOWN, buff=GAP_MD)
            self.play(Write(note), run_time=t.fill(0.3))
            self.section_head = VGroup(self.section_head, note)
            t.hold()

        wrong = PassageHighlight(
            "When we prepare for an important presentation, you should "
            "practice several times.",
            highlight="you",
            highlight_color=TERRACOTTA,
        )
        wrong.next_to(self.section_head, DOWN, buff=GAP_MD * 1.2)
        who = serif("who is this about — us, or the listener?", LABEL_SIZE, GREY)
        who.next_to(wrong, DOWN, buff=GAP_SM * 1.5)

        with self.beat("we_you") as t:
            self.play(Write(wrong), run_time=t.fill(0.35))
            self.play(Write(who), run_time=t.fill(0.2))
            self.work.add(wrong, who)
            t.hold()

        fixes = VGroup(
            PassageHighlight(
                "When we prepare for an important presentation, we should "
                "practice several times.",
                highlight="we should",
                highlight_color=SAGE,
            ),
            PassageHighlight(
                "When you prepare for an important presentation, you should "
                "practice several times.",
                highlight="you should",
                highlight_color=SAGE,
            ),
        ).arrange(DOWN, buff=GAP_MD, aligned_edge=LEFT)
        fixes.next_to(who, DOWN, buff=GAP_MD)

        with self.beat("we_fix") as t:
            self.play(Write(fixes[0]), run_time=t.fill(0.3))
            self.play(Write(fixes[1]), run_time=t.fill(0.3))
            self.work.add(fixes)
            t.hold()

        with self.beat("person") as t:
            self.swap_work(t)
            person_wrong = PassageHighlight(
                "A person should carefully review your work before "
                "submitting it.",
                highlight="your",
                highlight_color=TERRACOTTA,
            )
            person_wrong.next_to(self.section_head, DOWN, buff=GAP_MD * 1.2)
            person_fix = PassageHighlight(
                "A person should carefully review their work before "
                "submitting it.",
                highlight="their",
                highlight_color=SAGE,
            )
            person_fix.next_to(person_wrong, DOWN, buff=GAP_MD)
            self.play(Write(person_wrong), run_time=t.fill(0.35))
            self.play(Write(person_fix), run_time=t.fill(0.3))
            self.work.add(person_wrong, person_fix)
            t.hold()

        pov = serif("we → we, us, our · you → you, your · they → they, them",
                    LABEL_SIZE)
        pov.next_to(self.work[1], DOWN, buff=GAP_MD * 1.2)
        pov_line = underline(pov)

        with self.beat("pov_rule") as t:
            self.play(Write(pov), run_time=t.fill(0.3))
            self.play(Create(pov_line), run_time=t.fill(0.12))
            self.work.add(pov, pov_line)
            t.hold()

    def ambiguity(self):
        with self.beat("maya") as t:
            self.clear_all(t)
            self.set_head(t, "Two people, one mirror")
            maya = PassageHighlight(
                "When Maya spoke to Elena, she seemed nervous.",
                highlight="she",
                highlight_color=TERRACOTTA,
            )
            maya.next_to(self.section_head, DOWN, buff=GAP_MD * 1.3)
            who = serif("who seemed nervous — Maya, or Elena?", LABEL_SIZE, GREY)
            who.next_to(maya, DOWN, buff=GAP_SM * 1.5)
            self.play(Write(maya), run_time=t.fill(0.35))
            self.play(Write(who), run_time=t.fill(0.2))
            self.work.add(maya, who)
            t.hold()

        fixes = VGroup(
            PassageHighlight("When Maya spoke to Elena, Maya seemed nervous.",
                             highlight="Maya seemed", highlight_color=SAGE),
            PassageHighlight("When Maya spoke to Elena, Elena seemed nervous.",
                             highlight="Elena seemed", highlight_color=SAGE),
        ).arrange(DOWN, buff=GAP_MD, aligned_edge=LEFT)
        fixes.next_to(self.work[1], DOWN, buff=GAP_MD)
        guess = serif("a pronoun should never force the reader to guess",
                      LABEL_SIZE, GREY)
        guess.next_to(fixes, DOWN, buff=GAP_MD)

        with self.beat("maya_fix") as t:
            self.play(Write(fixes[0]), run_time=t.fill(0.25))
            self.play(Write(fixes[1]), run_time=t.fill(0.25))
            self.play(Write(guess), run_time=t.fill(0.15))
            self.work.add(fixes, guess)
            t.hold()

    def challenges(self):
        with self.beat("distorted") as t:
            self.clear_all(t)
            self.set_head(t, "The distorted reflection")
            wrong = PassageHighlight(
                "The research team completed their investigation and "
                "published its findings.",
                highlight="their",
                highlight_color=TERRACOTTA,
            )
            wrong.next_to(self.section_head, DOWN, buff=GAP_MD * 1.3)
            note = serif("one team, one unit — but their, then its",
                         LABEL_SIZE, GREY)
            note.next_to(wrong, DOWN, buff=GAP_SM * 1.5)
            self.play(Write(wrong), run_time=t.fill(0.4))
            self.play(Write(note), run_time=t.fill(0.2))
            self.work.add(wrong, note)
            t.hold()

        fixed = PassageHighlight(
            "The research team completed its investigation and published "
            "its findings.",
            highlight="its",
            highlight_color=SAGE,
        )
        fixed.next_to(self.work[1], DOWN, buff=GAP_MD)

        with self.beat("distorted_fix") as t:
            self.play(Write(fixed), run_time=t.fill(0.4))
            self.work.add(fixed)
            t.hold()

        lab_wrong = PassageHighlight(
            "When we enter the laboratory, you must wear protective glasses.",
            highlight="you",
            highlight_color=TERRACOTTA,
        )
        lab_fix = PassageHighlight(
            "When we enter the laboratory, we must wear protective glasses.",
            highlight="we must",
            highlight_color=SAGE,
        )
        lab_pair = VGroup(lab_wrong, lab_fix).arrange(
            DOWN, buff=GAP_MD, aligned_edge=LEFT
        )
        lab_pair.next_to(fixed, DOWN, buff=GAP_MD * 1.2)

        with self.beat("lab") as t:
            self.play(Write(lab_wrong), run_time=t.fill(0.3))
            self.play(Write(lab_fix), run_time=t.fill(0.3))
            self.work.add(lab_pair)
            t.hold()

    def wrap_up(self):
        steps = VGroup(
            serif("1  locate the pronoun", BODY_SIZE),
            serif("2  find the noun it replaces", BODY_SIZE),
            serif("3  singular or plural?", BODY_SIZE),
            serif("4  is the point of view consistent?", BODY_SIZE),
            serif("5  is the antecedent unambiguous?", BODY_SIZE),
        ).arrange(DOWN, buff=GAP_SM * 1.6, aligned_edge=LEFT)

        with self.beat("strategy") as t:
            self.clear_all(t)
            self.set_head(t, "The strategy")
            steps.next_to(self.section_head, DOWN, buff=GAP_MD * 1.3)
            self.play(Write(steps), run_time=t.fill(0.5))
            self.work.add(steps)
            t.hold()

        reflections = serif(
            "singular → singular · plural → plural · collective → singular",
            LABEL_SIZE, GREY,
        )
        reflections.next_to(steps, DOWN, buff=GAP_MD * 1.2)

        with self.beat("reflections") as t:
            self.play(Write(reflections), run_time=t.fill(0.35))
            self.work.add(reflections)
            t.hold()

        closing = serif("make every reflection accurate", BODY_SIZE)
        closing.next_to(reflections, DOWN, buff=GAP_MD)
        closing_line = underline(closing)

        with self.beat("closing") as t:
            self.play(Write(closing), run_time=t.fill(0.3))
            self.play(Create(closing_line), run_time=t.fill(0.12))
            t.hold()
