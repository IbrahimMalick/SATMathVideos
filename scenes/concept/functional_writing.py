"""Concept lecture: functional writing and the APFK system (FW01).

Narration script: scripts/FW01-functional-writing.md
Audience, Purpose, Format, Key Instructions — decode the task before
writing a sentence.
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


class FunctionalWriting(SATScene):
    scene_id = "concept.functional_writing"

    def construct(self):
        self.margin_note = mono("FW01 · functional writing", MARGIN_SIZE)
        self.margin_note.to_corner(UP + LEFT, buff=GAP_SM)
        self.add(self.margin_note)
        self.section_head = None
        self.work = VGroup()

        self.opening()
        self.audience()
        self.purpose()
        self.format_section()
        self.key_instructions()
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
        hook = VGroup(
            serif("a beautiful answer", BODY_SIZE),
            serif("to the wrong task", BODY_SIZE, TERRACOTTA),
        ).arrange(DOWN, buff=GAP_SM * 1.4)
        hook.move_to(UP * 0.8)

        with self.beat("hook") as t:
            self.play(Write(hook[0]), run_time=t.fill(0.3))
            self.play(Write(hook[1]), run_time=t.fill(0.3))
            t.hold()

        title = serif("Functional Writing", TITLE_SIZE * 1.2)
        title.to_edge(UP, buff=GAP_MD * 1.8)
        letters = VGroup(
            VGroup(serif("A", TITLE_SIZE * 1.2), serif("audience", MARGIN_SIZE, GREY)),
            VGroup(serif("P", TITLE_SIZE * 1.2), serif("purpose", MARGIN_SIZE, GREY)),
            VGroup(serif("F", TITLE_SIZE * 1.2), serif("format", MARGIN_SIZE, GREY)),
            VGroup(serif("K", TITLE_SIZE * 1.2), serif("key instructions", MARGIN_SIZE, GREY)),
        )
        for col in letters:
            col.arrange(DOWN, buff=GAP_SM)
        letters.arrange(RIGHT, buff=GAP_MD * 2.2)
        letters.next_to(title, DOWN, buff=GAP_MD * 1.5)

        with self.beat("apfk") as t:
            self.play(FadeOut(hook), run_time=t.fill(0.08))
            self.play(Write(title), run_time=t.fill(0.25))
            self.play(Write(letters), run_time=t.fill(0.4))
            self.work.add(title, letters)
            t.hold()

        checks = VGroup(
            serif("understand the situation", LABEL_SIZE, GREY),
            serif("know who you are speaking to", LABEL_SIZE, GREY),
            serif("write for the correct purpose, in the correct format", LABEL_SIZE, GREY),
            serif("follow the instructions", LABEL_SIZE),
        ).arrange(DOWN, buff=GAP_SM * 1.2, aligned_edge=LEFT)
        checks.next_to(letters, DOWN, buff=GAP_MD * 1.3)

        with self.beat("what_is") as t:
            self.play(Write(checks), run_time=t.fill(0.45))
            self.work.add(checks)
            t.hold()

        forms = serif("letter · report · speech · article · account", LABEL_SIZE)
        forms.next_to(checks, DOWN, buff=GAP_MD * 1.1)
        decode = serif("first, decode the task", BODY_SIZE)
        decode.next_to(forms, DOWN, buff=GAP_MD * 0.9)
        decode_line = underline(decode)

        with self.beat("forms") as t:
            self.play(Write(forms), run_time=t.fill(0.25))
            self.play(Write(decode), run_time=t.fill(0.2))
            self.play(Create(decode_line), run_time=t.fill(0.1))
            self.work.add(forms, decode, decode_line)
            t.hold()

    def audience(self):
        with self.beat("audience") as t:
            self.clear_all(t)
            self.set_head(t, "A — Audience")
            q = serif("who am I writing to?  the audience controls the tone",
                      LABEL_SIZE, GREY)
            q.next_to(self.section_head, DOWN, buff=GAP_MD)
            self.play(Write(q), run_time=t.fill(0.3))
            self.section_head = VGroup(self.section_head, q)
            t.hold()

        friend = PassageHighlight(
            'To a friend: "The food was terrible today. I couldn\'t even '
            'finish it."',
            highlight="To a friend:",
            highlight_color=SAGE,
        )
        principal = PassageHighlight(
            'To the principal: "I would like to raise a concern regarding '
            'the quality of food currently being served."',
            highlight="To the principal:",
            highlight_color=SAGE,
        )
        pair = VGroup(friend, principal).arrange(DOWN, buff=GAP_MD,
                                                 aligned_edge=LEFT)
        pair.next_to(self.section_head, DOWN, buff=GAP_MD * 1.2)
        same = serif("same message — different tone", LABEL_SIZE, GREY)
        same.next_to(pair, DOWN, buff=GAP_MD)

        with self.beat("cafeteria") as t:
            self.play(Write(friend), run_time=t.fill(0.3))
            self.play(Write(principal), run_time=t.fill(0.3))
            self.play(Write(same), run_time=t.fill(0.15))
            self.work.add(pair, same)
            t.hold()

        with self.beat("audience_list") as t:
            self.swap_work(t)
            audiences = serif(
                "principal · teacher · friend · parents · readers · community",
                LABEL_SIZE,
            )
            audiences.next_to(self.section_head, DOWN, buff=GAP_MD * 1.2)
            ask = VGroup(
                serif("who is going to read this?", BODY_SIZE),
                serif("how would I realistically speak to them?", BODY_SIZE),
            ).arrange(DOWN, buff=GAP_SM * 1.4)
            ask.next_to(audiences, DOWN, buff=GAP_MD * 1.2)
            self.play(Write(audiences), run_time=t.fill(0.25))
            self.play(Write(ask), run_time=t.fill(0.35))
            self.work.add(audiences, ask)
            t.hold()

        with self.beat("register") as t:
            self.swap_work(t)
            reg_head = serif("register — the level and style of language",
                             BODY_SIZE)
            reg_head.next_to(self.section_head, DOWN, buff=GAP_MD * 1.2)
            formal = VGroup(
                serif("formal", MARGIN_SIZE, GREY),
                serif('"I would like to suggest..."', LABEL_SIZE),
                serif('"It has come to my attention..."', LABEL_SIZE),
            ).arrange(DOWN, buff=GAP_SM, aligned_edge=LEFT)
            informal = VGroup(
                serif("informal", MARGIN_SIZE, GREY),
                serif('"You won\'t believe what happened..."', LABEL_SIZE),
                serif('"The best part was..."', LABEL_SIZE),
            ).arrange(DOWN, buff=GAP_SM, aligned_edge=LEFT)
            cols = VGroup(formal, informal).arrange(RIGHT, buff=GAP_MD * 2.2,
                                                    aligned_edge=UP)
            cols.next_to(reg_head, DOWN, buff=GAP_MD * 1.2)
            self.play(Write(reg_head), run_time=t.fill(0.2))
            self.play(Write(formal), run_time=t.fill(0.25))
            self.play(Write(informal), run_time=t.fill(0.25))
            self.work.add(reg_head, cols)
            t.hold()

        rule = serif("a report is not a WhatsApp message", LABEL_SIZE)
        rule.next_to(self.work[1], DOWN, buff=GAP_MD * 1.1)
        rule_line = underline(rule)

        with self.beat("register_rule") as t:
            self.play(Write(rule), run_time=t.fill(0.3))
            self.play(Create(rule_line), run_time=t.fill(0.12))
            self.work.add(rule, rule_line)
            t.hold()

    def purpose(self):
        with self.beat("purpose") as t:
            self.clear_all(t)
            self.set_head(t, "P — Purpose")
            verbs = serif(
                "inform · persuade · complain · recommend · explain · evaluate",
                LABEL_SIZE,
            )
            verbs.next_to(self.section_head, DOWN, buff=GAP_MD)
            note = serif("purpose controls the language", LABEL_SIZE, GREY)
            note.next_to(verbs, DOWN, buff=GAP_SM * 1.4)
            self.play(Write(verbs), run_time=t.fill(0.3))
            self.play(Write(note), run_time=t.fill(0.2))
            self.section_head = VGroup(self.section_head, verbs, note)
            t.hold()

        persuade = PassageHighlight(
            'Persuading: "Imagine arriving at school every morning to a '
            'cleaner, greener campus."',
            highlight="Persuading:",
            highlight_color=SAGE,
        )
        persuade.next_to(self.section_head, DOWN, buff=GAP_MD * 1.2)

        with self.beat("persuade_ex") as t:
            self.play(Write(persuade), run_time=t.fill(0.4))
            self.work.add(persuade)
            t.hold()

        report = PassageHighlight(
            'Reporting: "The campaign began on Monday and involved '
            'approximately 80 students."',
            highlight="Reporting:",
            highlight_color=SAGE,
        )
        report.next_to(persuade, DOWN, buff=GAP_MD)
        diff = serif("different purpose — different language", LABEL_SIZE, GREY)
        diff.next_to(report, DOWN, buff=GAP_MD)

        with self.beat("report_ex") as t:
            self.play(Write(report), run_time=t.fill(0.3))
            self.play(Write(diff), run_time=t.fill(0.2))
            self.work.add(report, diff)
            t.hold()

        with self.beat("one_sentence") as t:
            self.swap_work(t)
            test = serif('"By the end of my writing, I want the reader to..."',
                         BODY_SIZE)
            test.next_to(self.section_head, DOWN, buff=GAP_MD * 1.2)
            test_line = underline(test)
            completions = VGroup(
                serif("...understand what happened", LABEL_SIZE, GREY),
                serif("...agree with my recommendation", LABEL_SIZE, GREY),
                serif("...take action", LABEL_SIZE, GREY),
            ).arrange(DOWN, buff=GAP_SM * 1.2, aligned_edge=LEFT)
            completions.next_to(test, DOWN, buff=GAP_MD * 1.1)
            self.play(Write(test), run_time=t.fill(0.3))
            self.play(Create(test_line), run_time=t.fill(0.1))
            self.play(Write(completions), run_time=t.fill(0.3))
            self.work.add(test, test_line, completions)
            t.hold()

    def format_section(self):
        with self.beat("format") as t:
            self.clear_all(t)
            self.set_head(t, "F — Format")
            q = serif("a letter? a report? a speech? an article?",
                      LABEL_SIZE, GREY)
            q.next_to(self.section_head, DOWN, buff=GAP_MD)
            self.play(Write(q), run_time=t.fill(0.3))
            self.section_head = VGroup(self.section_head, q)
            t.hold()

        wrong = PassageHighlight(
            'Asked for a speech — but you write: "To: The Principal. '
            'From: Student Council. Subject: School Facilities."',
            highlight="but you write:",
            highlight_color=TERRACOTTA,
        )
        wrong.next_to(self.section_head, DOWN, buff=GAP_MD * 1.2)
        wrong_note = serif("right topic, wrong format", LABEL_SIZE, TERRACOTTA)
        wrong_note.next_to(wrong, DOWN, buff=GAP_SM * 1.4)

        with self.beat("format_wrong") as t:
            self.play(Write(wrong), run_time=t.fill(0.35))
            self.play(Write(wrong_note), run_time=t.fill(0.2))
            self.work.add(wrong, wrong_note)
            t.hold()

        with self.beat("letters") as t:
            self.swap_work(t)
            letters = VGroup(
                serif("letters — one person speaking to another", BODY_SIZE),
                serif('formal: "Dear Sir or Madam,"  ·  informal: "Dear Ahmed,"',
                      LABEL_SIZE, GREY),
            ).arrange(DOWN, buff=GAP_SM * 1.4, aligned_edge=LEFT)
            letters.next_to(self.section_head, DOWN, buff=GAP_MD * 1.2)
            self.play(Write(letters), run_time=t.fill(0.4))
            self.work.add(letters)
            t.hold()

        reports = VGroup(
            serif("reports — organized, factual, direct, objective", BODY_SIZE),
            serif("open with the 4 Ws: who · what · where · when",
                  LABEL_SIZE, GREY),
            PassageHighlight(
                "On 15 March, members of the Student Council inspected the "
                "school library to assess its facilities.",
                highlight="On 15 March,",
                highlight_color=SAGE,
            ),
        ).arrange(DOWN, buff=GAP_SM * 1.4, aligned_edge=LEFT)
        reports.next_to(self.work[0], DOWN, buff=GAP_MD * 1.1)

        with self.beat("reports") as t:
            self.play(Write(reports[0]), run_time=t.fill(0.2))
            self.play(Write(reports[1]), run_time=t.fill(0.15))
            self.play(Write(reports[2]), run_time=t.fill(0.25))
            self.work.add(reports)
            t.hold()

        with self.beat("speeches") as t:
            self.swap_work(t)
            speeches = VGroup(
                serif("speeches — they must sound spoken", BODY_SIZE),
                PassageHighlight(
                    '"Good morning, teachers and fellow students."',
                    highlight="Good morning,",
                    highlight_color=SAGE,
                ),
                serif("rhetorical questions · repetition · direct address",
                      LABEL_SIZE, GREY),
                PassageHighlight(
                    '"How many of us have complained about litter around '
                    'the school?"',
                    highlight="How many of us",
                    highlight_color=SAGE,
                ),
            ).arrange(DOWN, buff=GAP_SM * 1.4, aligned_edge=LEFT)
            speeches.next_to(self.section_head, DOWN, buff=GAP_MD * 1.2)
            for part in speeches:
                self.play(Write(part), run_time=t.fill(0.14))
            self.work.add(speeches)
            t.hold()

    def key_instructions(self):
        with self.beat("key") as t:
            self.clear_all(t)
            self.set_head(t, "K — Key Instructions")
            example = VGroup(
                serif("write a report about a recent school event — include:",
                      LABEL_SIZE, GREY),
                serif("· what went well", BODY_SIZE),
                serif("· problems that occurred", BODY_SIZE),
                serif("· recommendations for next year", BODY_SIZE),
            ).arrange(DOWN, buff=GAP_SM * 1.2, aligned_edge=LEFT)
            example.next_to(self.section_head, DOWN, buff=GAP_MD * 1.2)
            self.play(Write(example), run_time=t.fill(0.45))
            self.work.add(example)
            t.hold()

        roadmap = serif("not suggestions — your marking roadmap", BODY_SIZE)
        roadmap.next_to(self.work[0], DOWN, buff=GAP_MD * 1.2)
        roadmap_line = underline(roadmap)

        with self.beat("roadmap") as t:
            self.play(Write(roadmap), run_time=t.fill(0.3))
            self.play(Create(roadmap_line), run_time=t.fill(0.12))
            self.work.add(roadmap, roadmap_line)
            t.hold()

        with self.beat("plan") as t:
            self.swap_work(t)
            plan = VGroup(
                serif("turn the bullets into a plan", BODY_SIZE),
                serif("paragraph 1 — purpose and context", LABEL_SIZE, GREY),
                serif("paragraph 2 — successes", LABEL_SIZE, GREY),
                serif("paragraph 3 — problems", LABEL_SIZE, GREY),
                serif("paragraph 4 — recommendations", LABEL_SIZE, GREY),
            ).arrange(DOWN, buff=GAP_SM * 1.2, aligned_edge=LEFT)
            plan.next_to(self.section_head, DOWN, buff=GAP_MD * 1.2)
            self.play(Write(plan), run_time=t.fill(0.45))
            self.work.add(plan)
            t.hold()

        with self.beat("command") as t:
            self.swap_work(t)
            commands = VGroup(
                serif("describe — tell what happened", BODY_SIZE),
                serif("explain — give the reasons why", BODY_SIZE),
                serif("evaluate — weigh strengths and weaknesses", BODY_SIZE),
            ).arrange(DOWN, buff=GAP_MD * 0.9, aligned_edge=LEFT)
            commands.next_to(self.section_head, DOWN, buff=GAP_MD * 1.3)
            caution = serif('no command word just means "mention"',
                            LABEL_SIZE, TERRACOTTA)
            caution.next_to(commands, DOWN, buff=GAP_MD)
            self.play(Write(commands), run_time=t.fill(0.4))
            self.play(Write(caution), run_time=t.fill(0.15))
            self.work.add(commands, caution)
            t.hold()

        with self.beat("scenario") as t:
            self.swap_work(t)
            given = PassageHighlight(
                'Given: "The event was held on Saturday and 150 students '
                'attended."',
                highlight="Saturday and 150 students",
                highlight_color=SAGE,
            )
            wrong = PassageHighlight(
                'Do not write: "On Friday, more than 500 students arrived."',
                highlight="Friday, more than 500",
                highlight_color=TERRACOTTA,
            )
            pair = VGroup(given, wrong).arrange(DOWN, buff=GAP_MD,
                                                aligned_edge=LEFT)
            pair.next_to(self.section_head, DOWN, buff=GAP_MD * 1.2)
            bounds = serif("the facts are the boundaries of the task",
                           LABEL_SIZE, GREY)
            bounds.next_to(pair, DOWN, buff=GAP_MD)
            self.play(Write(given), run_time=t.fill(0.25))
            self.play(Write(wrong), run_time=t.fill(0.25))
            self.play(Write(bounds), run_time=t.fill(0.15))
            self.work.add(pair, bounds)
            t.hold()

    def wrap_up(self):
        with self.beat("routine") as t:
            self.clear_all(t)
            self.set_head(t, "The 60-second routine")
            routine = VGroup(
                serif("A — who am I writing to?", BODY_SIZE),
                serif("P — what am I trying to achieve?", BODY_SIZE),
                serif("F — what type of writing is required?", BODY_SIZE),
                serif("K — what must I include?", BODY_SIZE),
            ).arrange(DOWN, buff=GAP_MD * 0.9, aligned_edge=LEFT)
            routine.next_to(self.section_head, DOWN, buff=GAP_MD * 1.3)
            self.play(Write(routine), run_time=t.fill(0.5))
            self.work.add(routine)
            t.hold()

        with self.beat("challenge") as t:
            self.swap_work(t)
            mini = PassageHighlight(
                "Your school is considering extending the school day. Write "
                "a speech to your classmates explaining the proposal, giving "
                "your opinion, and suggesting an alternative.",
            )
            mini.next_to(self.section_head, DOWN, buff=GAP_MD * 1.2)
            self.play(Write(mini), run_time=t.fill(0.5))
            self.work.add(mini)
            t.hold()

        answers = VGroup(
            serif("audience — your classmates", LABEL_SIZE),
            serif("purpose — explain, opine, suggest", LABEL_SIZE),
            serif("format — a speech", LABEL_SIZE),
            serif("key instructions — three of them", LABEL_SIZE),
        ).arrange(DOWN, buff=GAP_SM * 1.3, aligned_edge=LEFT)
        answers.next_to(self.work[0], DOWN, buff=GAP_MD * 1.1)

        with self.beat("challenge_answer") as t:
            self.play(Write(answers), run_time=t.fill(0.5))
            self.work.add(answers)
            t.hold()

        with self.beat("conclusion") as t:
            self.clear_all(t)
            closing = serif("answer the question that is actually on the page",
                            BODY_SIZE)
            closing.move_to(UP * 0.4)
            closing_line = underline(closing)
            apfk = serif("A · P · F · K", TITLE_SIZE)
            apfk.next_to(closing, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(closing), run_time=t.fill(0.3))
            self.play(Create(closing_line), run_time=t.fill(0.1))
            self.play(Write(apfk), run_time=t.fill(0.25))
            t.hold()
