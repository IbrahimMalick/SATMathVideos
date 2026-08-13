"""Concept lecture: turning the plan into high marks (Functional Writing, FW02).

Narration script: scripts/FW02-plan-to-marks.md
Development, balance, organization, register, vocabulary, grammar,
word limits, and the six-step checking system.
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


class PlanToMarks(SATScene):
    scene_id = "concept.plan_to_marks"

    def construct(self):
        self.margin_note = mono("FW02 · writing for marks", MARGIN_SIZE)
        self.margin_note.to_corner(UP + LEFT, buff=GAP_SM)
        self.add(self.margin_note)
        self.section_head = None
        self.work = VGroup()

        self.opening()
        self.development()
        self.balance_and_structure()
        self.register_section()
        self.language()
        self.grammar()
        self.checking()
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
        recap = serif("A · P · F · K", TITLE_SIZE)
        recap.move_to(UP * 1.2)
        half = serif("decoding the question is only half the battle",
                     LABEL_SIZE, GREY)
        half.next_to(recap, DOWN, buff=GAP_MD * 1.2)

        with self.beat("recap") as t:
            self.play(Write(recap), run_time=t.fill(0.3))
            self.play(Write(half), run_time=t.fill(0.25))
            t.hold()

        title = serif("From Plan to High Marks", TITLE_SIZE * 1.1)
        title.to_edge(UP, buff=GAP_MD * 1.8)
        agenda = serif("develop · organize · tone · language · check",
                       LABEL_SIZE)
        agenda.next_to(title, DOWN, buff=GAP_MD * 1.2)

        with self.beat("goal") as t:
            self.play(FadeOut(recap), FadeOut(half), run_time=t.fill(0.08))
            self.play(Write(title), run_time=t.fill(0.3))
            self.play(Write(agenda), run_time=t.fill(0.25))
            self.work.add(title, agenda)
            t.hold()

        weak = PassageHighlight(
            '"Students enjoyed the sports day because it was fun."',
            highlight="because it was fun.",
            highlight_color=TERRACOTTA,
        )
        weak.next_to(agenda, DOWN, buff=GAP_MD * 1.3)
        weak_note = serif("not wrong — just not strong", LABEL_SIZE, GREY)
        weak_note.next_to(weak, DOWN, buff=GAP_SM * 1.4)

        with self.beat("basic") as t:
            self.play(Write(weak), run_time=t.fill(0.35))
            self.play(Write(weak_note), run_time=t.fill(0.2))
            self.work.add(weak, weak_note)
            t.hold()

        strong = PassageHighlight(
            '"Students particularly enjoyed the inter-house competitions '
            'because everyone had an opportunity to participate rather than '
            'simply watch."',
            highlight="because everyone had an opportunity",
            highlight_color=SAGE,
        )
        strong.next_to(weak_note, DOWN, buff=GAP_MD)
        strong_note = serif("it develops the idea", LABEL_SIZE, GREY)
        strong_note.next_to(strong, DOWN, buff=GAP_SM * 1.4)

        with self.beat("developed") as t:
            self.play(Write(strong), run_time=t.fill(0.4))
            self.play(Write(strong_note), run_time=t.fill(0.15))
            self.work.add(strong, strong_note)
            t.hold()

    def development(self):
        with self.beat("pee") as t:
            self.clear_all(t)
            self.set_head(t, "Point — Explain — Effect")
            steps = VGroup(
                PassageHighlight("Point: The new computer room was useful.",
                                 highlight="Point:", highlight_color=SAGE),
                PassageHighlight(
                    "Explain: it allowed students to research information "
                    "more quickly.",
                    highlight="Explain:", highlight_color=SAGE),
                PassageHighlight(
                    "Effect: as a result, students completed group projects "
                    "more efficiently.",
                    highlight="Effect:", highlight_color=SAGE),
            ).arrange(DOWN, buff=GAP_MD * 0.9, aligned_edge=LEFT)
            steps.next_to(self.section_head, DOWN, buff=GAP_MD * 1.2)
            for s in steps:
                self.play(Write(s), run_time=t.fill(0.16))
            self.work.add(steps)
            t.hold()

        questions = serif("why? · how? · what happened because of this?",
                          BODY_SIZE)
        questions.next_to(self.work[0], DOWN, buff=GAP_MD * 1.2)
        q_line = underline(questions)

        with self.beat("three_q") as t:
            self.play(Write(questions), run_time=t.fill(0.3))
            self.play(Create(q_line), run_time=t.fill(0.12))
            self.work.add(questions, q_line)
            t.hold()

    def balance_and_structure(self):
        with self.beat("boxes") as t:
            self.clear_all(t)
            self.set_head(t, "Three bullet points, three boxes")
            boxes = VGroup(
                serif("☐  what students enjoyed", BODY_SIZE),
                serif("☐  problems during the trip", BODY_SIZE),
                serif("☐  suggestions for future trips", BODY_SIZE),
            ).arrange(DOWN, buff=GAP_SM * 1.5, aligned_edge=LEFT)
            boxes.next_to(self.section_head, DOWN, buff=GAP_MD * 1.3)
            note = serif("all three must be checked before you finish",
                         LABEL_SIZE, GREY)
            note.next_to(boxes, DOWN, buff=GAP_MD)
            self.play(Write(boxes), run_time=t.fill(0.4))
            self.play(Write(note), run_time=t.fill(0.15))
            self.work.add(boxes, note)
            t.hold()

        warning = serif("too long on point one → points two and three rushed",
                        LABEL_SIZE, TERRACOTTA)
        warning.next_to(self.work[1], DOWN, buff=GAP_MD)

        with self.beat("unbalanced") as t:
            self.play(Write(warning), run_time=t.fill(0.35))
            self.work.add(warning)
            t.hold()

        with self.beat("organization") as t:
            self.clear_all(t)
            self.set_head(t, "Every paragraph has a job")
            org = VGroup(
                serif("1 — purpose of the report", BODY_SIZE),
                serif("2 — what went well", BODY_SIZE),
                serif("3 — the problems", BODY_SIZE),
                serif("4 — recommendations", BODY_SIZE),
            ).arrange(DOWN, buff=GAP_SM * 1.3, aligned_edge=LEFT)
            org.next_to(self.section_head, DOWN, buff=GAP_MD * 1.3)
            self.play(Write(org), run_time=t.fill(0.45))
            self.work.add(org)
            t.hold()

        with self.beat("progression") as t:
            self.swap_work(t)
            loop = PassageHighlight(
                '"The library was crowded. There were many students. A lot '
                'of people were inside. The library had too many students."',
                highlight="too many students.",
                highlight_color=TERRACOTTA,
            )
            loop.next_to(self.section_head, DOWN, buff=GAP_MD * 1.2)
            loop_note = serif("the same idea, four times", LABEL_SIZE, GREY)
            loop_note.next_to(loop, DOWN, buff=GAP_SM * 1.4)
            self.play(Write(loop), run_time=t.fill(0.4))
            self.play(Write(loop_note), run_time=t.fill(0.15))
            self.work.add(loop, loop_note)
            t.hold()

        forward = PassageHighlight(
            '"The library was extremely crowded during lunch breaks, leaving '
            'many students without a suitable place to work. Additional '
            'seating could help reduce this problem."',
            highlight="Additional seating",
            highlight_color=SAGE,
        )
        forward.next_to(self.work[1], DOWN, buff=GAP_MD)
        forward_note = serif("problem → effect → solution", LABEL_SIZE, GREY)
        forward_note.next_to(forward, DOWN, buff=GAP_SM * 1.4)

        with self.beat("progression2") as t:
            self.play(Write(forward), run_time=t.fill(0.4))
            self.play(Write(forward_note), run_time=t.fill(0.15))
            self.work.add(forward, forward_note)
            t.hold()

    def register_section(self):
        with self.beat("register") as t:
            self.clear_all(t)
            self.set_head(t, "Register")
            good = PassageHighlight(
                '"I would recommend increasing the number of supervised '
                'study areas available after school."',
                highlight="I would recommend",
                highlight_color=SAGE,
            )
            good.next_to(self.section_head, DOWN, buff=GAP_MD * 1.2)
            bad = PassageHighlight(
                '"You guys seriously need to sort this out."',
                highlight="You guys seriously",
                highlight_color=TERRACOTTA,
            )
            bad.next_to(good, DOWN, buff=GAP_MD)
            self.play(Write(good), run_time=t.fill(0.35))
            self.play(Write(bad), run_time=t.fill(0.25))
            self.work.add(good, bad)
            t.hold()

        rule = serif("good writing is appropriate writing", BODY_SIZE)
        rule.next_to(self.work[1], DOWN, buff=GAP_MD * 1.1)
        rule_line = underline(rule)

        with self.beat("appropriate") as t:
            self.play(Write(rule), run_time=t.fill(0.3))
            self.play(Create(rule_line), run_time=t.fill(0.12))
            self.work.add(rule, rule_line)
            t.hold()

        with self.beat("collapse") as t:
            self.swap_work(t)
            open_line = PassageHighlight(
                '"Dear Sir, I am writing to express my concern regarding '
                'the recent changes to the school timetable."',
                highlight="Dear Sir,",
                highlight_color=SAGE,
            )
            open_line.next_to(self.section_head, DOWN, buff=GAP_MD * 1.2)
            slip = PassageHighlight(
                'Three paragraphs later: "Anyway, the whole thing is pretty '
                'annoying."',
                highlight="Anyway, the whole thing",
                highlight_color=TERRACOTTA,
            )
            slip.next_to(open_line, DOWN, buff=GAP_MD)
            note = serif("the tone has collapsed — stay consistent",
                         LABEL_SIZE, GREY)
            note.next_to(slip, DOWN, buff=GAP_MD)
            self.play(Write(open_line), run_time=t.fill(0.3))
            self.play(Write(slip), run_time=t.fill(0.3))
            self.play(Write(note), run_time=t.fill(0.15))
            self.work.add(open_line, slip, note)
            t.hold()

    def language(self):
        with self.beat("vocab") as t:
            self.clear_all(t)
            self.set_head(t, "Precision, not difficulty")
            pairs = VGroup(
                serif('"very heavy rain"  →  "the rain hammered"', BODY_SIZE),
                serif('"walked quickly"  →  "rushed"', BODY_SIZE),
                serif('"looked carefully at"  →  "examined"', BODY_SIZE),
            ).arrange(DOWN, buff=GAP_MD * 0.9, aligned_edge=LEFT)
            pairs.next_to(self.section_head, DOWN, buff=GAP_MD * 1.3)
            note = serif("a strong verb replaces several weak words",
                         LABEL_SIZE, GREY)
            note.next_to(pairs, DOWN, buff=GAP_MD)
            self.play(Write(pairs), run_time=t.fill(0.45))
            self.play(Write(note), run_time=t.fill(0.15))
            self.work.add(pairs, note)
            t.hold()

        with self.beat("overblown") as t:
            self.swap_work(t)
            drama = PassageHighlight(
                '"The cafeteria situation created a catastrophic '
                'humanitarian predicament."',
                highlight="catastrophic humanitarian predicament.",
                highlight_color=TERRACOTTA,
                width=40,
            )
            drama.next_to(self.section_head, DOWN, buff=GAP_MD * 1.2)
            reality = serif("what happened: the cafeteria ran out of sandwiches",
                            LABEL_SIZE, GREY)
            reality.next_to(drama, DOWN, buff=GAP_SM * 1.5)
            control = serif("sophistication is precision and control", BODY_SIZE)
            control.next_to(reality, DOWN, buff=GAP_MD)
            control_line = underline(control)
            self.play(Write(drama), run_time=t.fill(0.3))
            self.play(Write(reality), run_time=t.fill(0.2))
            self.play(Write(control), run_time=t.fill(0.2))
            self.play(Create(control_line), run_time=t.fill(0.1))
            self.work.add(drama, reality, control, control_line)
            t.hold()

        with self.beat("variety") as t:
            self.swap_work(t)
            robot = PassageHighlight(
                '"The event started at nine. Students arrived. Teachers '
                'arrived. The competition started."',
                highlight="Students arrived.",
                highlight_color=TERRACOTTA,
            )
            robot.next_to(self.section_head, DOWN, buff=GAP_MD * 1.2)
            flow = PassageHighlight(
                '"By nine o\'clock, students and teachers had filled the '
                'field. As the first competition began, the atmosphere '
                'quickly became energetic."',
                highlight="By nine o'clock,",
                highlight_color=SAGE,
            )
            flow.next_to(robot, DOWN, buff=GAP_MD)
            emphasis = serif('short for emphasis: "We cannot ignore this '
                             'problem."', LABEL_SIZE, GREY)
            emphasis.next_to(flow, DOWN, buff=GAP_MD)
            self.play(Write(robot), run_time=t.fill(0.3))
            self.play(Write(flow), run_time=t.fill(0.3))
            self.play(Write(emphasis), run_time=t.fill(0.15))
            self.work.add(robot, flow, emphasis)
            t.hold()

    def grammar(self):
        with self.beat("tenses") as t:
            self.clear_all(t)
            self.set_head(t, "Grammar under control")
            tense = PassageHighlight(
                '"By the time the teachers arrived, the students had '
                'already entered the hall."',
                highlight="had already entered",
                highlight_color=SAGE,
                width=50,
            )
            tense.next_to(self.section_head, DOWN, buff=GAP_MD * 1.2)
            tense_note = serif("consistency first — no random tense jumps",
                               LABEL_SIZE, GREY)
            tense_note.next_to(tense, DOWN, buff=GAP_SM * 1.5)
            self.play(Write(tense), run_time=t.fill(0.35))
            self.play(Write(tense_note), run_time=t.fill(0.2))
            self.work.add(tense, tense_note)
            t.hold()

        sva = VGroup(
            PassageHighlight("The list of recommendations is attached.",
                             highlight="is", highlight_color=SAGE),
            PassageHighlight("The group of students was waiting outside.",
                             highlight="was", highlight_color=SAGE),
        ).arrange(DOWN, buff=GAP_SM * 1.5, aligned_edge=LEFT)
        sva.next_to(self.work[1], DOWN, buff=GAP_MD)
        sva_note = serif("find the real subject before choosing the verb",
                         LABEL_SIZE, GREY)
        sva_note.next_to(sva, DOWN, buff=GAP_SM * 1.5)

        with self.beat("sva") as t:
            self.play(Write(sva), run_time=t.fill(0.4))
            self.play(Write(sva_note), run_time=t.fill(0.15))
            self.work.add(sva, sva_note)
            t.hold()

        with self.beat("punctuation") as t:
            self.swap_work(t)
            punct = VGroup(
                serif("control your full stops, commas, apostrophes",
                      BODY_SIZE),
                serif("four lines with no full stop?  end the sentence",
                      LABEL_SIZE, GREY),
            ).arrange(DOWN, buff=GAP_SM * 1.5, aligned_edge=LEFT)
            punct.next_to(self.section_head, DOWN, buff=GAP_MD * 1.3)
            self.play(Write(punct), run_time=t.fill(0.4))
            self.work.add(punct)
            t.hold()

        conj = serif("And, But, So — use them deliberately, not automatically",
                     LABEL_SIZE)
        conj.next_to(self.work[0], DOWN, buff=GAP_MD)

        with self.beat("conjunctions") as t:
            self.play(Write(conj), run_time=t.fill(0.35))
            self.work.add(conj)
            t.hold()

        contr = serif("don't / can't — fine informally · do not / cannot — formal",
                      LABEL_SIZE)
        contr.next_to(conj, DOWN, buff=GAP_SM * 1.5)

        with self.beat("contractions") as t:
            self.play(Write(contr), run_time=t.fill(0.35))
            self.work.add(contr)
            t.hold()

        with self.beat("word_limits") as t:
            self.swap_work(t)
            limits = VGroup(
                serif("the examiner is not paying you by the word", BODY_SIZE),
                serif("extra sentences = extra chances for mistakes",
                      LABEL_SIZE, GREY),
                serif("write the most effectively, not the most", BODY_SIZE),
            ).arrange(DOWN, buff=GAP_SM * 1.6, aligned_edge=LEFT)
            limits.next_to(self.section_head, DOWN, buff=GAP_MD * 1.3)
            limits_line = underline(limits[2])
            self.play(Write(limits[0]), run_time=t.fill(0.2))
            self.play(Write(limits[1]), run_time=t.fill(0.15))
            self.play(Write(limits[2]), run_time=t.fill(0.2))
            self.play(Create(limits_line), run_time=t.fill(0.1))
            self.work.add(limits, limits_line)
            t.hold()

    def checking(self):
        checks = [
            ("checking", "1  content — every bullet point covered?"),
            ("check2", "2  audience and register appropriate?"),
            ("check3", "3  tenses consistent?"),
            ("check4", "4  verbs agree with the true subject?"),
            ("check5", "5  punctuation — full stops, commas, apostrophes"),
            ("check6", "6  missing words — read what is on the page"),
        ]
        lines = VGroup(*[serif(text, BODY_SIZE) for _, text in checks])
        lines.arrange(DOWN, buff=GAP_SM * 1.4, aligned_edge=LEFT)

        for i, (name, _) in enumerate(checks):
            with self.beat(name) as t:
                if i == 0:
                    self.clear_all(t)
                    self.set_head(t, "The checking system")
                    lines.next_to(self.section_head, DOWN, buff=GAP_MD * 1.2)
                self.play(Write(lines[i]), run_time=t.fill(0.3))
                self.work.add(lines[i])
                t.hold()

    def wrap_up(self):
        with self.beat("together") as t:
            self.clear_all(t)
            self.set_head(t, "All together")
            phases = VGroup(
                serif("before — A · P · F · K", BODY_SIZE),
                serif("while — cover, develop, organize, register, precision",
                      BODY_SIZE),
                serif("after — check your work", BODY_SIZE),
            ).arrange(DOWN, buff=GAP_MD, aligned_edge=LEFT)
            phases.next_to(self.section_head, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(phases), run_time=t.fill(0.5))
            self.work.add(phases)
            t.hold()

        with self.beat("control") as t:
            self.clear_all(t)
            control = serif("It is about control.", TITLE_SIZE)
            control.move_to(UP * 0.6)
            control_line = underline(control)
            closing = serif("you are not just writing an answer — you are "
                            "writing for marks", LABEL_SIZE, GREY)
            closing.next_to(control, DOWN, buff=GAP_MD * 1.5)
            self.play(Write(control), run_time=t.fill(0.3))
            self.play(Create(control_line), run_time=t.fill(0.1))
            self.play(Write(closing), run_time=t.fill(0.25))
            t.hold()
