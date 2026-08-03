"""Concept lecture: mastering transitions (Reading & Writing, L05).

Narration script: scripts/L05-transitions.md
Twelve sections; a heading persists per section while passages and notes
rotate through the work area beneath it.
"""

import numpy as np

from manim import (
    Create,
    FadeOut,
    Line,
    Text,
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
from components.answer_choices import AnswerChoices
from components.passage import PassageHighlight
from scenes.base import SATScene


def underline(mobject, color=SAGE):
    return Line(
        mobject.get_corner(DOWN + LEFT) + DOWN * GAP_SM,
        mobject.get_corner(DOWN + RIGHT) + DOWN * GAP_SM,
        color=color,
        stroke_width=3,
    )


class Transitions(SATScene):
    scene_id = "concept.transitions"

    def construct(self):
        self.margin_note = mono("L05 · transitions", MARGIN_SIZE)
        self.margin_note.to_corner(UP + LEFT, buff=GAP_SM)
        self.add(self.margin_note)
        self.section_head = None
        self.work = VGroup()

        self.intro()
        self.airport_story()
        self.strategy_section()
        self.method()
        self.families_overview()
        self.continuers()
        self.cause_effect()
        self.contradictors()
        self.detective()
        self.punctuation()
        self.synonym_shortcut()
        self.antarctica()

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

    def set_head(self, t, text, fraction=0.25, size=TITLE_SIZE):
        head = serif(text, size)
        head.to_edge(UP, buff=GAP_MD * 1.6)
        self.play(Write(head), run_time=t.fill(fraction))
        self.section_head = head

    # ------------------------------------------------------------- sections

    def intro(self):
        title = serif("Transitions", TITLE_SIZE * 1.35)
        subtitle = serif("L05 · Reading and Writing", BODY_SIZE, GREY)
        subtitle.next_to(title, DOWN, buff=GAP_MD)
        VGroup(title, subtitle).move_to(UP * 1.3)

        with self.beat("title") as t:
            self.play(Write(title), run_time=t.fill(0.4))
            self.play(Write(subtitle), run_time=t.fill(0.25))
            t.hold()

        trap = serif('"that sounds right" is the trap', BODY_SIZE)
        trap.next_to(subtitle, DOWN, buff=GAP_MD * 1.6)
        logic = serif("stop guessing — use logic", LABEL_SIZE, GREY)
        logic.next_to(trap, DOWN, buff=GAP_MD)

        with self.beat("sounds_right") as t:
            self.play(Write(trap), run_time=t.fill(0.3))
            self.play(Write(logic), run_time=t.fill(0.2))
            t.hold()

        formula = serif("relationship  →  transition  →  punctuation", BODY_SIZE)
        formula.next_to(logic, DOWN, buff=GAP_MD * 1.4)
        formula_line = underline(formula)

        with self.beat("formula") as t:
            self.play(Write(formula), run_time=t.fill(0.3))
            self.play(Create(formula_line), run_time=t.fill(0.12))
            t.hold()

    def airport_story(self):
        signs = VGroup(
            *[serif(s, LABEL_SIZE) for s in
              ["immigration", "baggage claim", "connecting flights",
               "restaurants", "exit"]]
        ).arrange(DOWN, buff=GAP_SM * 1.3, aligned_edge=LEFT)

        with self.beat("airport") as t:
            self.clear_all(t)
            self.set_head(t, "An airport with no signs")
            signs.next_to(self.section_head, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(signs), run_time=t.fill(0.4))
            self.work.add(signs)
            t.hold()

        gone = serif("every sign disappears — you loop back to the gate",
                     LABEL_SIZE, TERRACOTTA)
        gone.next_to(signs, DOWN, buff=GAP_MD * 1.2)

        with self.beat("lost") as t:
            self.play(signs.animate.set_color(GREY), run_time=t.fill(0.12))
            self.play(Write(gone), run_time=t.fill(0.25))
            self.work.add(gone)
            t.hold()

        tells = VGroup(
            *[serif(s, LABEL_SIZE) for s in
              ['"I am adding another idea"', '"here is an example"',
               '"this happened because of that"',
               '"careful — the direction is changing"']]
        ).arrange(DOWN, buff=GAP_SM * 1.3, aligned_edge=LEFT)

        with self.beat("signs") as t:
            self.swap_work(t)
            tells.next_to(self.section_head, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(tells), run_time=t.fill(0.45))
            self.work.add(tells)
            t.hold()

        job = serif("find the direction of the writer's thinking", BODY_SIZE)
        job.next_to(tells, DOWN, buff=GAP_MD * 1.3)
        job_line = underline(job)

        with self.beat("job") as t:
            self.play(Write(job), run_time=t.fill(0.3))
            self.play(Create(job_line), run_time=t.fill(0.12))
            self.work.add(job, job_line)
            t.hold()

    def strategy_section(self):
        rule = serif("Do not begin with the answer choices.", TITLE_SIZE * 0.95)
        rule.to_edge(UP, buff=GAP_MD * 1.6)
        rule_line = underline(rule)

        with self.beat("strategy") as t:
            self.clear_all(t)
            self.play(Write(rule), run_time=t.fill(0.3))
            self.play(Create(rule_line), run_time=t.fill(0.12))
            self.section_head = VGroup(rule, rule_line)
            t.hold()

        ex = PassageHighlight(
            "I studied for six hours.  _______  I failed the exam.",
            highlight="_______",
        )
        ex.next_to(rule, DOWN, buff=GAP_MD * 1.6)

        with self.beat("example1") as t:
            self.play(Write(ex), run_time=t.fill(0.35))
            self.work.add(ex)
            t.hold()

        expect = VGroup(
            serif("expectation: six hours of study → a good result", LABEL_SIZE, GREY),
            serif("reality: failed — the direction reverses", LABEL_SIZE),
        ).arrange(DOWN, buff=GAP_SM * 1.4, aligned_edge=LEFT)
        expect.next_to(ex, DOWN, buff=GAP_MD * 1.2)

        with self.beat("expectation") as t:
            self.play(Write(expect), run_time=t.fill(0.4))
            self.work.add(expect)
            t.hold()

        answer = PassageHighlight(
            "I studied for six hours. However, I failed the exam.",
            highlight="However,",
            highlight_color=SAGE,
        )
        answer.next_to(expect, DOWN, buff=GAP_MD * 1.2)

        with self.beat("example1_answer") as t:
            self.play(Write(answer), run_time=t.fill(0.35))
            self.work.add(answer)
            t.hold()

        choices = AnswerChoices(["Therefore", "Furthermore", "However", "For example"])
        choices.scale(0.9)

        with self.beat("choices1") as t:
            self.swap_work(t)
            choices.next_to(self.section_head, DOWN, buff=GAP_MD * 1.3)
            choices.move_to(np.array([-3.6, choices.get_center()[1], 0]))
            self.play(Write(choices), run_time=t.fill(0.35))
            self.play(*choices.confirm("C"), run_time=t.fill(0.2))
            self.work.add(choices)
            t.hold()

        warning = VGroup(
            serif("do not invent a story to rescue", LABEL_SIZE, TERRACOTTA),
            serif("a wrong answer — use the passage", LABEL_SIZE, TERRACOTTA),
        ).arrange(DOWN, buff=GAP_SM, aligned_edge=LEFT)
        warning.move_to(np.array([3.4, choices.get_center()[1], 0]))

        with self.beat("invent") as t:
            self.play(Write(warning), run_time=t.fill(0.35))
            self.work.add(warning)
            t.hold()

    def method(self):
        steps = [
            "1  read the full passage",
            "2  ignore the blank — read the two ideas",
            "3  describe the relationship simply",
            "4  now pick the word that does that job",
        ]
        lines = VGroup(*[serif(s, BODY_SIZE) for s in steps])
        lines.arrange(DOWN, buff=GAP_MD, aligned_edge=LEFT)

        with self.beat("method") as t:
            self.clear_all(t)
            self.set_head(t, "The four-step method")
            lines.next_to(self.section_head, DOWN, buff=GAP_MD * 1.5)
            self.work.add(lines)
            t.hold()

        hints = serif("same direction · opposite · this caused that · an example",
                      LABEL_SIZE, GREY)
        hints.next_to(lines, DOWN, buff=GAP_MD * 1.2)

        for name, line in zip(["m1", "m2", "m3", "m4"], lines):
            with self.beat(name) as t:
                self.play(Write(line), run_time=t.fill(0.35))
                if name == "m3":
                    self.play(Write(hints), run_time=t.fill(0.2))
                    self.work.add(hints)
                t.hold()

    def families_overview(self):
        cols = VGroup(
            VGroup(serif("continuers", BODY_SIZE),
                   serif("agrees with everyone", MARGIN_SIZE, GREY)),
            VGroup(serif("cause and effect", BODY_SIZE),
                   serif("causes everything", MARGIN_SIZE, GREY)),
            VGroup(serif("contradictors", BODY_SIZE),
                   serif("argues with everyone", MARGIN_SIZE, GREY)),
        )
        for col in cols:
            col.arrange(DOWN, buff=GAP_SM)
        cols.arrange(RIGHT, buff=GAP_MD * 2.2)
        cols.move_to(ORIGIN)

        with self.beat("families") as t:
            self.clear_all(t)
            self.set_head(t, "Three families")
            self.play(Write(cols), run_time=t.fill(0.5))
            self.work.add(cols)
            t.hold()

    def continuers(self):
        with self.beat("cont") as t:
            self.clear_all(t)
            self.set_head(t, "Family one: continuers")
            jobs = serif("add · exemplify · clarify · emphasize · sequence",
                         LABEL_SIZE, GREY)
            jobs.next_to(self.section_head, DOWN, buff=GAP_MD)
            self.play(Write(jobs), run_time=t.fill(0.3))
            self.section_head = VGroup(self.section_head, jobs)
            t.hold()

        add_words = serif("moreover · furthermore · in addition · also",
                          BODY_SIZE)
        add_words.next_to(self.section_head, DOWN, buff=GAP_MD * 1.3)

        with self.beat("add_words") as t:
            self.play(Write(add_words), run_time=t.fill(0.35))
            self.work.add(add_words)
            t.hold()

        malik = PassageHighlight(
            "Malik is an excellent mathematics student. Moreover, he is an "
            "accomplished musician.",
            highlight="Moreover,",
            highlight_color=SAGE,
        )
        malik.next_to(add_words, DOWN, buff=GAP_MD * 1.2)

        with self.beat("malik") as t:
            self.play(Write(malik), run_time=t.fill(0.35))
            self.work.add(malik)
            t.hold()

        restaurant = PassageHighlight(
            "Our restaurant serves delicious food. In addition, we have "
            "free parking.",
            highlight="In addition,",
            highlight_color=SAGE,
        )
        restaurant.next_to(malik, DOWN, buff=GAP_MD)

        with self.beat("restaurant") as t:
            self.play(Write(restaurant), run_time=t.fill(0.35))
            self.work.add(restaurant)
            t.hold()

        with self.beat("example_words") as t:
            self.swap_work(t)
            ex_words = serif("for example · for instance · specifically",
                             BODY_SIZE)
            ex_words.next_to(self.section_head, DOWN, buff=GAP_MD * 1.3)
            chimp = PassageHighlight(
                "Some animals use tools to obtain food. For example, certain "
                "chimpanzees use sticks to collect termites.",
                highlight="For example,",
                highlight_color=SAGE,
            )
            chimp.next_to(ex_words, DOWN, buff=GAP_MD * 1.2)
            ask = serif("is the second idea one specific case of the first?",
                        LABEL_SIZE, GREY)
            ask.next_to(chimp, DOWN, buff=GAP_MD)
            self.play(Write(ex_words), run_time=t.fill(0.2))
            self.play(Write(chimp), run_time=t.fill(0.3))
            self.play(Write(ask), run_time=t.fill(0.2))
            self.work.add(ex_words, chimp, ask)
            t.hold()

        with self.beat("clarify") as t:
            self.swap_work(t)
            cl_words = serif("in fact · indeed · in other words · that is",
                             BODY_SIZE)
            cl_words.next_to(self.section_head, DOWN, buff=GAP_MD * 1.3)
            scientist = PassageHighlight(
                "The scientist's discovery was significant. In fact, it "
                "changed how researchers understood the disease.",
                highlight="In fact,",
                highlight_color=SAGE,
            )
            scientist.next_to(cl_words, DOWN, buff=GAP_MD * 1.2)
            self.play(Write(cl_words), run_time=t.fill(0.2))
            self.play(Write(scientist), run_time=t.fill(0.3))
            self.work.add(cl_words, scientist)
            t.hold()

        device = PassageHighlight(
            "The device is portable. In other words, users can easily carry "
            "it from one location to another.",
            highlight="In other words,",
            highlight_color=SAGE,
        )
        distinction = serif(
            "in fact strengthens — in other words restates", LABEL_SIZE, GREY
        )

        with self.beat("clarify2") as t:
            device.next_to(self.work[1], DOWN, buff=GAP_MD)
            distinction.next_to(device, DOWN, buff=GAP_MD)
            self.play(Write(device), run_time=t.fill(0.3))
            self.play(Write(distinction), run_time=t.fill(0.2))
            self.work.add(device, distinction)
            t.hold()

        with self.beat("sequence") as t:
            self.swap_work(t)
            seq_words = serif("first · next · subsequently · finally · meanwhile",
                              BODY_SIZE)
            seq_words.next_to(self.section_head, DOWN, buff=GAP_MD * 1.3)
            soil = PassageHighlight(
                "The researchers collected soil samples. Next, they analyzed "
                "the samples in a laboratory.",
                highlight="Next,",
                highlight_color=SAGE,
            )
            soil.next_to(seq_words, DOWN, buff=GAP_MD * 1.2)
            joke = serif("finally, call your mother — that is sequence",
                         LABEL_SIZE, GREY)
            joke.next_to(soil, DOWN, buff=GAP_MD)
            self.play(Write(seq_words), run_time=t.fill(0.2))
            self.play(Write(soil), run_time=t.fill(0.3))
            self.play(Write(joke), run_time=t.fill(0.15))
            self.work.add(seq_words, soil, joke)
            t.hold()

    def cause_effect(self):
        with self.beat("cause") as t:
            self.clear_all(t)
            self.set_head(t, "Family two: cause and effect")
            words = serif(
                "therefore · consequently · thus · hence · as a result",
                BODY_SIZE,
            )
            words.next_to(self.section_head, DOWN, buff=GAP_MD)
            self.play(Write(words), run_time=t.fill(0.3))
            self.section_head = VGroup(self.section_head, words)
            t.hold()

        ice = PassageHighlight(
            "The road was covered with ice. Therefore, the school closed "
            "for the day.",
            highlight="Therefore,",
            highlight_color=SAGE,
        )
        ice.next_to(self.section_head, DOWN, buff=GAP_MD * 1.3)

        with self.beat("ice") as t:
            self.play(Write(ice), run_time=t.fill(0.35))
            self.work.add(ice)
            t.hold()

        sara = PassageHighlight(
            "Sara forgot to charge her phone. Consequently, she could not "
            "use it during the trip.",
            highlight="Consequently,",
            highlight_color=SAGE,
        )
        sara.next_to(ice, DOWN, buff=GAP_MD)

        with self.beat("sara") as t:
            self.play(Write(sara), run_time=t.fill(0.35))
            self.work.add(sara)
            t.hold()

        with self.beat("domino") as t:
            self.swap_work(t)
            domino = serif("the domino test", BODY_SIZE)
            domino.next_to(self.section_head, DOWN, buff=GAP_MD * 1.3)
            domino_q = serif("did the first idea produce the second?",
                             LABEL_SIZE, GREY)
            domino_q.next_to(domino, DOWN, buff=GAP_MD)
            domino_line = underline(domino)
            self.play(Write(domino), run_time=t.fill(0.2))
            self.play(Create(domino_line), run_time=t.fill(0.1))
            self.play(Write(domino_q), run_time=t.fill(0.2))
            self.work.add(domino, domino_line, domino_q)
            t.hold()

        sales = PassageHighlight(
            "The company reduced the price. As a result, sales increased.",
            highlight="As a result,",
            highlight_color=SAGE,
        )
        sales.next_to(self.work[2], DOWN, buff=GAP_MD * 1.2)

        with self.beat("price_sales") as t:
            self.play(Write(sales), run_time=t.fill(0.35))
            self.work.add(sales)
            t.hold()

        logo = PassageHighlight(
            "The company reduced the price. It changed the color of its "
            "logo — probably not a result.",
            highlight="probably not a result.",
            highlight_color=TERRACOTTA,
        )
        logo.next_to(sales, DOWN, buff=GAP_MD)

        with self.beat("price_logo") as t:
            self.play(Write(logo), run_time=t.fill(0.35))
            self.work.add(logo)
            t.hold()

        with self.beat("sequence_rule") as t:
            self.swap_work(t)
            rule = serif("sequence is not automatically cause and effect",
                         BODY_SIZE)
            rule.move_to(DOWN * 0.6)
            rule_line = underline(rule)
            self.play(Write(rule), run_time=t.fill(0.3))
            self.play(Create(rule_line), run_time=t.fill(0.12))
            self.work.add(rule, rule_line)
            t.hold()

    def contradictors(self):
        with self.beat("contra") as t:
            self.clear_all(t)
            self.set_head(t, "Family three: contradictors")
            words = serif(
                "however · nevertheless · in contrast · still · yet",
                BODY_SIZE,
            )
            words.next_to(self.section_head, DOWN, buff=GAP_MD)
            self.play(Write(words), run_time=t.fill(0.3))
            self.section_head = VGroup(self.section_head, words)
            t.hold()

        apartment = PassageHighlight(
            "The apartment is small. However, it receives plenty of natural "
            "light.",
            highlight="However,",
            highlight_color=SAGE,
        )
        apartment.next_to(self.section_head, DOWN, buff=GAP_MD * 1.3)

        with self.beat("apartment") as t:
            self.play(Write(apartment), run_time=t.fill(0.35))
            self.work.add(apartment)
            t.hold()

        surprise = serif("the surprise test — does idea two defy the "
                         "expectation?", LABEL_SIZE, GREY)
        surprise.next_to(apartment, DOWN, buff=GAP_MD)

        with self.beat("surprise") as t:
            self.play(Write(surprise), run_time=t.fill(0.3))
            self.work.add(surprise)
            t.hold()

        runner = PassageHighlight(
            "The runner injured her ankle before the race. Nevertheless, "
            "she finished in first place.",
            highlight="Nevertheless,",
            highlight_color=SAGE,
        )
        runner.next_to(surprise, DOWN, buff=GAP_MD)

        with self.beat("runner") as t:
            self.play(Write(runner), run_time=t.fill(0.35))
            self.work.add(runner)
            t.hold()

        with self.beat("however_vs") as t:
            self.swap_work(t)
            duo = VGroup(
                PassageHighlight(
                    "The software is expensive. However, it is extremely "
                    "reliable.",
                    highlight="However,",
                    highlight_color=SAGE,
                ),
                PassageHighlight(
                    "Desert temperatures exceed 45°C. In contrast, polar "
                    "regions remain extremely cold.",
                    highlight="In contrast,",
                    highlight_color=SAGE,
                ),
            ).arrange(DOWN, buff=GAP_MD * 1.2)
            duo.next_to(self.section_head, DOWN, buff=GAP_MD * 1.3)
            note = serif("two subjects directly compared → in contrast",
                         LABEL_SIZE, GREY)
            note.next_to(duo, DOWN, buff=GAP_MD)
            self.play(Write(duo[0]), run_time=t.fill(0.25))
            self.play(Write(duo[1]), run_time=t.fill(0.25))
            self.play(Write(note), run_time=t.fill(0.2))
            self.work.add(duo, note)
            t.hold()

    def detective(self):
        cases = [
            ("case1",
             "Students believe reading quickly is the best way to finish on "
             "time. However, reading too quickly can cause students to miss "
             "important details.",
             "However,",
             "a belief, then a problem with it — contrast"),
            ("case2",
             "The museum wanted to attract more young visitors. Therefore, "
             "it created an interactive mobile app.",
             "Therefore,",
             "the app is a result of the goal — cause and effect"),
            ("case3",
             "Many birds migrate over long distances. For example, the "
             "Arctic tern travels from the Arctic to the Antarctic and back.",
             "For example,",
             "one specific case of the broad idea — example"),
        ]

        with self.beat("detective") as t:
            self.clear_all(t)
            self.set_head(t, "Become a transition detective")
            t.hold()

        for i, (name, text, hl, verdict) in enumerate(cases):
            with self.beat(name) as t:
                self.swap_work(t)
                label = mono(f"case {i + 1}", MARGIN_SIZE)
                label.next_to(self.section_head, DOWN, buff=GAP_MD)
                passage = PassageHighlight(text, highlight=hl,
                                           highlight_color=SAGE)
                passage.next_to(label, DOWN, buff=GAP_MD)
                verdict_line = serif(verdict, LABEL_SIZE, GREY)
                verdict_line.next_to(passage, DOWN, buff=GAP_MD)
                self.play(Write(label), run_time=t.fill(0.1))
                self.play(Write(passage), run_time=t.fill(0.35))
                self.play(Write(verdict_line), run_time=t.fill(0.2))
                self.work.add(label, passage, verdict_line)
                t.hold()

    def punctuation(self):
        with self.beat("punct") as t:
            self.clear_all(t)
            self.set_head(t, "Punctuation")
            t.hold()

        conj = serif("however · therefore · moreover — conjunctive adverbs",
                     LABEL_SIZE)
        conj2 = serif("they cannot join two sentences with only a comma",
                      LABEL_SIZE, GREY)
        conj_group = VGroup(conj, conj2).arrange(DOWN, buff=GAP_SM * 1.4)
        conj_group.next_to(self.section_head, DOWN, buff=GAP_MD)

        with self.beat("conj") as t:
            self.play(Write(conj_group), run_time=t.fill(0.4))
            self.work.add(conj_group)
            t.hold()

        splice = PassageHighlight(
            "The city is old, however, it contains many modern buildings.",
            highlight=", however,",
            highlight_color=TERRACOTTA,
        )
        splice_note = serif("a comma splice — the comma is not qualified",
                            LABEL_SIZE, TERRACOTTA)
        splice_group = VGroup(splice, splice_note).arrange(DOWN, buff=GAP_SM * 1.4)
        splice_group.next_to(conj_group, DOWN, buff=GAP_MD * 1.2)

        with self.beat("splice") as t:
            self.play(Write(splice), run_time=t.fill(0.3))
            self.play(Write(splice_note), run_time=t.fill(0.2))
            self.work.add(splice_group)
            t.hold()

        with self.beat("pattern1") as t:
            self.swap_work(t)
            p1 = PassageHighlight(
                "The city is old. However, it contains many modern buildings.",
                highlight=". However,",
                highlight_color=SAGE,
            )
            p1_note = serif("pattern one: period, then the transition",
                            LABEL_SIZE, GREY)
            group1 = VGroup(p1, p1_note).arrange(DOWN, buff=GAP_SM * 1.4)
            group1.next_to(self.section_head, DOWN, buff=GAP_MD * 1.2)
            self.play(Write(p1), run_time=t.fill(0.3))
            self.play(Write(p1_note), run_time=t.fill(0.15))
            self.work.add(group1)
            t.hold()

        p2 = PassageHighlight(
            "The city is old; however, it contains many modern buildings.",
            highlight="; however,",
            highlight_color=SAGE,
        )
        p2_rule = serif("semicolon before · comma after", BODY_SIZE)
        p2_group = VGroup(p2, p2_rule).arrange(DOWN, buff=GAP_MD)
        p2_group.next_to(self.work[0], DOWN, buff=GAP_MD * 1.2)
        p2_line = underline(p2_rule)

        with self.beat("pattern2") as t:
            self.play(Write(p2), run_time=t.fill(0.3))
            self.play(Write(p2_rule), run_time=t.fill(0.2))
            self.play(Create(p2_line), run_time=t.fill(0.1))
            self.work.add(p2_group, p2_line)
            t.hold()

        with self.beat("interrupt") as t:
            self.swap_work(t)
            inter = PassageHighlight(
                "The city is old; it does, however, contain many modern "
                "buildings.",
                highlight=", however,",
                highlight_color=SAGE,
            )
            inter_note = serif("an interruption — nonessential, so commas "
                               "surround it", LABEL_SIZE, GREY)
            group = VGroup(inter, inter_note).arrange(DOWN, buff=GAP_SM * 1.4)
            group.next_to(self.section_head, DOWN, buff=GAP_MD * 1.2)
            self.play(Write(inter), run_time=t.fill(0.3))
            self.play(Write(inter_note), run_time=t.fill(0.2))
            self.work.add(group)
            t.hold()

        fanboys_word = serif("FANBOYS — for, and, nor, but, or, yet, so",
                             BODY_SIZE)
        fb = PassageHighlight(
            "The city is old, but it contains many modern buildings.",
            highlight=", but",
            highlight_color=SAGE,
        )
        fb_group = VGroup(fanboys_word, fb).arrange(DOWN, buff=GAP_MD)
        fb_group.next_to(self.work[0], DOWN, buff=GAP_MD * 1.2)

        with self.beat("fanboys") as t:
            self.play(Write(fanboys_word), run_time=t.fill(0.25))
            self.play(Write(fb), run_time=t.fill(0.3))
            self.work.add(fb_group)
            t.hold()

        with self.beat("fanboys2") as t:
            self.swap_work(t)
            wrong = PassageHighlight(
                "The city is old, however it contains modern buildings.",
                highlight=", however",
                highlight_color=TERRACOTTA,
            )
            right1 = PassageHighlight(
                "The city is old, but it contains modern buildings.",
                highlight=", but",
                highlight_color=SAGE,
            )
            right2 = PassageHighlight(
                "The city is old; however, it contains modern buildings.",
                highlight="; however,",
                highlight_color=SAGE,
            )
            trio = VGroup(wrong, right1, right2).arrange(
                DOWN, buff=GAP_MD, aligned_edge=LEFT
            )
            trio.next_to(self.section_head, DOWN, buff=GAP_MD * 1.2)
            note = serif("do not treat however like but", LABEL_SIZE, GREY)
            note.next_to(trio, DOWN, buff=GAP_MD)
            self.play(Write(wrong), run_time=t.fill(0.2))
            self.play(Write(right1), run_time=t.fill(0.2))
            self.play(Write(right2), run_time=t.fill(0.2))
            self.play(Write(note), run_time=t.fill(0.12))
            self.work.add(trio, note)
            t.hold()

    def synonym_shortcut(self):
        choices = AnswerChoices(
            ["Therefore", "Consequently", "However", "For example"]
        )
        choices.scale(0.9)

        with self.beat("shortcut") as t:
            self.clear_all(t)
            self.set_head(t, "The synonym shortcut")
            choices.next_to(self.section_head, DOWN, buff=GAP_MD * 1.3)
            choices.move_to(np.array([-3.8, choices.get_center()[1], 0]))
            note = VGroup(
                serif("true synonyms cannot both be right —", LABEL_SIZE),
                serif("they eliminate each other", LABEL_SIZE),
            ).arrange(DOWN, buff=GAP_SM, aligned_edge=LEFT)
            note.move_to(np.array([3.2, choices.get_center()[1], 0]))
            self.play(Write(choices), run_time=t.fill(0.3))
            self.play(*choices.eliminate("A"), run_time=t.fill(0.1))
            self.play(*choices.eliminate("B"), run_time=t.fill(0.1))
            self.play(Write(note), run_time=t.fill(0.2))
            self.work.add(choices, note)
            t.hold()

        pairs = VGroup(
            serif("therefore = consequently", LABEL_SIZE, GREY),
            serif("however = nevertheless", LABEL_SIZE, GREY),
            serif("moreover = furthermore", LABEL_SIZE, GREY),
            serif("for example = for instance", LABEL_SIZE, GREY),
        ).arrange(DOWN, buff=GAP_SM * 1.2, aligned_edge=LEFT)
        pairs.next_to(choices, DOWN, buff=GAP_MD * 1.2, aligned_edge=LEFT)

        with self.beat("pairs") as t:
            self.play(Write(pairs), run_time=t.fill(0.4))
            self.work.add(pairs)
            t.hold()

        caution = VGroup(
            serif("but: in fact emphasizes · in other words restates", LABEL_SIZE),
            serif("similar-looking words can do different jobs", LABEL_SIZE, GREY),
        ).arrange(DOWN, buff=GAP_SM * 1.2, aligned_edge=LEFT)
        caution.next_to(pairs, DOWN, buff=GAP_MD)

        with self.beat("caution") as t:
            self.play(Write(caution), run_time=t.fill(0.35))
            self.work.add(caution)
            t.hold()

    def antarctica(self):
        passage = PassageHighlight(
            "Conditions in the interior of Antarctica are extremely "
            "inhospitable. Temperatures remain far below freezing, the air "
            "is exceptionally dry, and strong winds are common.  _______  "
            "The Antarctic Peninsula experiences relatively mild "
            "temperatures and contains areas of liquid water.",
            highlight="_______",
        )

        with self.beat("antarctica") as t:
            self.clear_all(t)
            self.set_head(t, "Antarctica", size=TITLE_SIZE)
            passage.next_to(self.section_head, DOWN, buff=GAP_MD)
            self.play(Write(passage), run_time=t.fill(0.5))
            self.work.add(passage)
            t.hold()

        analysis = VGroup(
            serif("interior: inhospitable · peninsula: mild", LABEL_SIZE),
            serif("two regions compared — we need contrast", LABEL_SIZE, GREY),
        ).arrange(DOWN, buff=GAP_SM * 1.3, aligned_edge=LEFT)
        analysis.next_to(passage, DOWN, buff=GAP_MD)
        analysis.move_to(np.array([-2.9, analysis.get_center()[1], 0]))

        with self.beat("ant_ignore") as t:
            self.play(Write(analysis), run_time=t.fill(0.4))
            self.work.add(analysis)
            t.hold()

        choices = AnswerChoices(["Therefore", "For instance", "Indeed", "In contrast"])
        choices.scale(0.9)
        choices.next_to(analysis, DOWN, buff=GAP_MD)
        choices.move_to(np.array([-3.8, choices.get_center()[1], 0]))

        with self.beat("ant_choices") as t:
            self.play(Write(choices), run_time=t.fill(0.4))
            self.work.add(choices)
            t.hold()

        reasons = {
            "ant_elimA": ("A", "harsh interior did not cause mild peninsula"),
            "ant_elimB": ("B", "the peninsula is not an example of the interior"),
            "ant_elimC": ("C", "nothing is being strengthened or confirmed"),
        }
        reason_pos = np.array([3.3, choices.get_top()[1] - 0.2, 0])

        for name, (letter, why) in reasons.items():
            with self.beat(name) as t:
                note = serif(why, MARGIN_SIZE, GREY)
                note.move_to(reason_pos, aligned_edge=UP + LEFT)
                reason_pos = reason_pos + DOWN * 0.55
                self.play(*choices.eliminate(letter), run_time=t.fill(0.2))
                self.play(Write(note), run_time=t.fill(0.2))
                self.work.add(note)
                t.hold()

        with self.beat("ant_answer") as t:
            self.play(*choices.confirm("D"), run_time=t.fill(0.25))
            final = serif("a direct comparison — in contrast", BODY_SIZE)
            final.to_edge(DOWN, buff=GAP_MD)
            final_line = underline(final)
            self.play(Write(final), run_time=t.fill(0.25))
            self.play(Create(final_line), run_time=t.fill(0.12))
            self.work.add(final, final_line)
            t.hold()
