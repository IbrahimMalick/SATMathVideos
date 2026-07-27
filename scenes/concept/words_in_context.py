"""Concept lecture: words in context (Reading & Writing, Lecture 4).

Narration script: scripts/L04-words-in-context.md
Five practice questions run through AnswerChoices + PassageHighlight; the
technique, trap, and process sections are text reveals.
"""

import textwrap

import numpy as np

from manim import (
    Create,
    FadeOut,
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
    SERIF_FONT,
    TERRACOTTA,
    TITLE_SIZE,
    mono,
    serif,
)
from components.answer_choices import AnswerChoices
from components.passage import PassageHighlight
from scenes.base import SATScene


def note_text(text, width=34, color=GREY, size=LABEL_SIZE):
    return Text(
        textwrap.fill(text, width),
        font=SERIF_FONT,
        font_size=size,
        color=color,
        line_spacing=1.1,
    )


def underline(mobject, color=SAGE):
    from manim import Line

    return Line(
        mobject.get_corner(DOWN + LEFT) + DOWN * GAP_SM,
        mobject.get_corner(DOWN + RIGHT) + DOWN * GAP_SM,
        color=color,
        stroke_width=3,
    )


class WordsInContext(SATScene):
    scene_id = "concept.words_in_context"

    NOTE_X = 3.6   # right-hand work column
    CHOICES_X = -3.6

    def clear_section(self, t, fraction=0.12):
        old = [m for m in self.mobjects if m is not self.margin_note]
        if old:
            self.play(*[FadeOut(m) for m in old], run_time=t.fill(fraction))

    def construct(self):
        self.margin_note = mono("L04 · words in context", MARGIN_SIZE)
        self.margin_note.to_corner(UP + LEFT, buff=GAP_SM)
        self.add(self.margin_note)

        self.intro()
        self.method()
        self.question_1()
        self.question_2()
        self.question_3()
        self.question_4()
        self.contrast_technique()
        self.explanation_technique()
        self.question_5()
        self.traps()
        self.closing()

    # ------------------------------------------------------- question plumbing

    def show_question(self, prefix, passage_text, word, choices):
        """The shared question opening: passage, stem, choices, pause."""
        passage = PassageHighlight(passage_text, highlight=word)
        passage.to_edge(UP, buff=GAP_MD * 2.2)

        with self.beat(f"{prefix}_passage") as t:
            self.clear_section(t)
            self.play(Write(passage), run_time=t.fill(0.5))
            t.hold()

        stem = serif(f"as used in the text, {word} most nearly means...",
                     LABEL_SIZE, GREY)
        stem.next_to(passage, DOWN, buff=GAP_MD * 1.4)

        with self.beat(f"{prefix}_stem") as t:
            self.play(Write(stem), run_time=t.fill(0.4))
            t.hold()

        ac = AnswerChoices(choices)
        ac.next_to(stem, DOWN, buff=GAP_MD * 1.4)
        ac.move_to(np.array([self.CHOICES_X, ac.get_center()[1], 0]))

        with self.beat(f"{prefix}_choices") as t:
            self.play(Write(ac), run_time=t.fill(0.5))
            t.hold()

        with self.beat(f"{prefix}_pause") as t:
            t.hold()

        return passage, stem, ac

    def note_column(self, ac):
        """Anchor for explanation notes, level with the top of the choices."""
        return np.array([self.NOTE_X, ac.get_top()[1], 0])

    # ------------------------------------------------------------ sections

    def intro(self):
        title = serif("Words in Context", TITLE_SIZE * 1.2)
        subtitle = serif("Lecture 4 · Reading and Writing", BODY_SIZE, GREY)
        subtitle.next_to(title, DOWN, buff=GAP_MD)
        VGroup(title, subtitle).move_to(UP * 1.2)

        with self.beat("title") as t:
            self.play(Write(title), run_time=t.fill(0.4))
            self.play(Write(subtitle), run_time=t.fill(0.2))
            t.hold()

        stem = PassageHighlight(
            "As used in the text, what does the word most nearly mean?",
            highlight="most nearly",
        )
        stem.next_to(subtitle, DOWN, buff=GAP_MD * 2)

        with self.beat("stem") as t:
            self.play(Write(stem), run_time=t.fill(0.4))
            t.hold()

        goal = serif("choose the definition that fits the sentence", LABEL_SIZE)
        goal.next_to(stem, DOWN, buff=GAP_MD * 1.5)

        with self.beat("goal") as t:
            self.play(Write(goal), run_time=t.fill(0.3))
            self.play(Create(underline(goal)), run_time=t.fill(0.2))
            t.hold()

        bright1 = note_text("bright — producing a lot of light", 40, CHARCOAL)
        bright2 = note_text("bright — intelligent", 40, CHARCOAL)
        bright1.move_to(DOWN * 2.6 + LEFT * 3.4)
        bright2.move_to(DOWN * 2.6 + RIGHT * 3.4)

        with self.beat("bright") as t:
            self.play(Write(bright1), run_time=t.fill(0.35))
            t.hold()

        with self.beat("bright2") as t:
            self.play(Write(bright2), run_time=t.fill(0.35))
            t.hold()

    def method(self):
        head = serif("Define the word inside the sentence.", BODY_SIZE)
        head.to_edge(UP, buff=GAP_MD * 1.8)

        with self.beat("strategy") as t:
            self.clear_section(t)
            self.play(Write(head), run_time=t.fill(0.3))
            self.play(Create(underline(head)), run_time=t.fill(0.15))
            t.hold()

        steps = [
            "1  read the entire sentence",
            "2  explain it in your own words",
            "3  replace the word with your own simple word",
            "4  pick the closest answer, then re-read",
        ]
        step_lines = VGroup(*[serif(s, BODY_SIZE) for s in steps])
        step_lines.arrange(DOWN, buff=GAP_MD, aligned_edge=LEFT)
        step_lines.next_to(head, DOWN, buff=GAP_MD * 2)

        for name, line in zip(["step1", "step2", "step3", "step4"], step_lines):
            with self.beat(name) as t:
                self.play(Write(line), run_time=t.fill(0.35))
                t.hold()

    def question_1(self):
        passage, stem, ac = self.show_question(
            "q1",
            "Although the scientist initially doubted the new theory, the "
            "results of several experiments compelled her to reconsider her "
            "position.",
            "compelled",
            ["Forced", "Invited", "Allowed", "Taught"],
        )

        with self.beat("q1_answer") as t:
            self.play(*ac.confirm("A"), run_time=t.fill(0.4))
            t.hold()

        anchor = self.note_column(ac)
        note1 = note_text("the results caused her to change her mind")
        note1.move_to(anchor, aligned_edge=UP + LEFT)

        with self.beat("q1_read") as t:
            self.play(Write(note1), run_time=t.fill(0.35))
            t.hold()

        note2 = note_text("the evidence was so strong she had to")
        note2.next_to(note1, DOWN, buff=GAP_MD, aligned_edge=LEFT)

        with self.beat("q1_explain") as t:
            self.play(Write(note2), run_time=t.fill(0.35))
            t.hold()

        note3 = note_text('"the results forced her to reconsider"', 34, SAGE)
        note3.next_to(note2, DOWN, buff=GAP_MD, aligned_edge=LEFT)

        with self.beat("q1_replace") as t:
            self.play(Write(note3), run_time=t.fill(0.35))
            t.hold()

        for name, letter in [("q1_elimB", "B"), ("q1_elimC", "C"), ("q1_elimD", "D")]:
            with self.beat(name) as t:
                self.play(*ac.eliminate(letter), run_time=t.fill(0.3))
                t.hold()

        lesson = serif("Only one meaning fits the context.", BODY_SIZE)
        lesson.to_edge(DOWN, buff=GAP_MD * 1.4)

        with self.beat("q1_lesson") as t:
            self.play(Write(lesson), run_time=t.fill(0.3))
            self.play(Create(underline(lesson)), run_time=t.fill(0.15))
            t.hold()

    def question_2(self):
        passage, stem, ac = self.show_question(
            "q2",
            "The town council adopted a flexible approach to the construction "
            "project, changing the plan whenever unexpected problems arose.",
            "flexible",
            ["Easy to bend", "Willing to adapt", "Weakly designed", "Carefully hidden"],
        )

        with self.beat("q2_answer") as t:
            self.play(*ac.confirm("B"), run_time=t.fill(0.4))
            t.hold()

        note1 = note_text("they changed the plan when problems appeared")
        note1.move_to(self.note_column(ac), aligned_edge=UP + LEFT)

        with self.beat("q2_expl") as t:
            self.play(Write(note1), run_time=t.fill(0.35))
            t.hold()

        note2 = note_text("an approach, not a physical object")
        note2.next_to(note1, DOWN, buff=GAP_MD, aligned_edge=LEFT)

        with self.beat("q2_elimA") as t:
            self.play(*ac.eliminate("A"), run_time=t.fill(0.25))
            self.play(Write(note2), run_time=t.fill(0.25))
            t.hold()

        with self.beat("q2_elimC") as t:
            self.play(*ac.eliminate("C"), run_time=t.fill(0.3))
            t.hold()

        with self.beat("q2_elimD") as t:
            self.play(*ac.eliminate("D"), run_time=t.fill(0.3))
            t.hold()

        trap = serif("Trap: the most familiar definition may be wrong.", BODY_SIZE)
        trap.to_edge(DOWN, buff=GAP_MD * 1.4)

        with self.beat("q2_trap") as t:
            self.play(Write(trap), run_time=t.fill(0.3))
            self.play(Create(underline(trap)), run_time=t.fill(0.15))
            t.hold()

    def question_3(self):
        passage, stem, ac = self.show_question(
            "q3",
            "After reviewing the evidence, the committee determined that the "
            "witness's account was sound.",
            "sound",
            ["A noise", "Healthy", "Reliable", "Deep"],
        )

        with self.beat("q3_answer") as t:
            self.play(*ac.confirm("C"), run_time=t.fill(0.4))
            t.hold()

        note1 = note_text("sound = reliable, well supported")
        note1.move_to(self.note_column(ac), aligned_edge=UP + LEFT)

        with self.beat("q3_expl") as t:
            self.play(Write(note1), run_time=t.fill(0.35))
            t.hold()

        with self.beat("q3_elims") as t:
            self.play(*ac.eliminate("A"), run_time=t.fill(0.15))
            self.play(*ac.eliminate("B"), run_time=t.fill(0.15))
            self.play(*ac.eliminate("D"), run_time=t.fill(0.15))
            t.hold()

    def question_4(self):
        passage, stem, ac = self.show_question(
            "q4",
            "The researcher gave a qualified response, explaining that the "
            "early results were promising but that more evidence was needed.",
            "qualified",
            ["Fully trained", "Limited by conditions", "Officially approved",
             "Highly intelligent"],
        )

        with self.beat("q4_answer") as t:
            self.play(*ac.confirm("B"), run_time=t.fill(0.4))
            t.hold()

        note1 = note_text("promising, but more evidence needed — a limitation")
        note1.move_to(self.note_column(ac), aligned_edge=UP + LEFT)

        with self.beat("q4_expl") as t:
            self.play(Write(note1), run_time=t.fill(0.35))
            t.hold()

        with self.beat("q4_elims") as t:
            self.play(*ac.eliminate("A"), run_time=t.fill(0.15))
            self.play(*ac.eliminate("C"), run_time=t.fill(0.15))
            self.play(*ac.eliminate("D"), run_time=t.fill(0.15))
            t.hold()

    def contrast_technique(self):
        head = serif("Look for contrast words", TITLE_SIZE)
        head.to_edge(UP, buff=GAP_MD * 1.6)
        words = serif("however · although · but · yet · despite", LABEL_SIZE, GREY)
        words.next_to(head, DOWN, buff=GAP_MD)

        with self.beat("contrast") as t:
            self.clear_section(t)
            self.play(Write(head), run_time=t.fill(0.25))
            self.play(Write(words), run_time=t.fill(0.25))
            t.hold()

        ex1 = PassageHighlight(
            "Although the professor was usually reserved, she became animated "
            "when discussing her research.",
            highlight="Although",
        )
        ex1.next_to(words, DOWN, buff=GAP_MD * 1.6)

        with self.beat("contrast_ex1") as t:
            self.play(Write(ex1), run_time=t.fill(0.4))
            t.hold()

        note1 = serif("animated  =  energetic, excited", LABEL_SIZE, SAGE)
        note1.next_to(ex1, DOWN, buff=GAP_MD)

        with self.beat("contrast_ex1b") as t:
            self.play(Write(note1), run_time=t.fill(0.3))
            t.hold()

        ex2 = PassageHighlight(
            "The evidence appeared convincing at first. However, later studies "
            "undermined the original conclusion.",
            highlight="However",
        )
        ex2.next_to(note1, DOWN, buff=GAP_MD * 1.6)

        with self.beat("contrast_ex2") as t:
            self.play(ex1.animate.set_color(GREY), run_time=t.fill(0.1))
            self.play(Write(ex2), run_time=t.fill(0.4))
            t.hold()

        note2 = serif("undermined  =  weakened", LABEL_SIZE, SAGE)
        note2.next_to(ex2, DOWN, buff=GAP_MD)

        with self.beat("contrast_ex2b") as t:
            self.play(Write(note2), run_time=t.fill(0.3))
            t.hold()

    def explanation_technique(self):
        head = serif("Look for explanations and examples", TITLE_SIZE)
        head.to_edge(UP, buff=GAP_MD * 1.6)

        with self.beat("explain_tech") as t:
            self.clear_section(t)
            self.play(Write(head), run_time=t.fill(0.35))
            t.hold()

        ex1 = PassageHighlight(
            "The animal is nocturnal, meaning that it is active mainly during "
            "the night.",
            highlight="meaning that",
        )
        ex1.next_to(head, DOWN, buff=GAP_MD * 1.8)

        with self.beat("explain_ex1") as t:
            self.play(Write(ex1), run_time=t.fill(0.4))
            t.hold()

        ex2 = PassageHighlight(
            "The region contains many indigenous plants, including species "
            "that developed naturally in the area.",
            highlight="including",
        )
        ex2.next_to(ex1, DOWN, buff=GAP_MD * 1.6)

        with self.beat("explain_ex2") as t:
            self.play(ex1.animate.set_color(GREY), run_time=t.fill(0.1))
            self.play(Write(ex2), run_time=t.fill(0.4))
            t.hold()

        note = serif("the clue is usually near the tested word", BODY_SIZE)
        note.next_to(ex2, DOWN, buff=GAP_MD * 1.5)

        with self.beat("explain_note") as t:
            self.play(ex2.animate.set_color(GREY), run_time=t.fill(0.1))
            self.play(Write(note), run_time=t.fill(0.3))
            self.play(Create(underline(note)), run_time=t.fill(0.15))
            t.hold()

    def question_5(self):
        passage, stem, ac = self.show_question(
            "q5",
            "The architect's original proposal was ambitious. After reviewing "
            "the limited budget, however, she presented a more modest design.",
            "modest",
            ["Shy", "Limited in size or cost", "Old fashioned", "Poorly constructed"],
        )

        with self.beat("q5_answer") as t:
            self.play(*ac.confirm("B"), run_time=t.fill(0.4))
            t.hold()

        note1 = note_text("however: ambitious, then modest — and the budget is the clue")
        note1.move_to(self.note_column(ac), aligned_edge=UP + LEFT)

        with self.beat("q5_expl") as t:
            self.play(Write(note1), run_time=t.fill(0.35))
            t.hold()

        note2 = note_text("a design, not a person")
        note2.next_to(note1, DOWN, buff=GAP_MD, aligned_edge=LEFT)

        with self.beat("q5_elimA") as t:
            self.play(*ac.eliminate("A"), run_time=t.fill(0.25))
            self.play(Write(note2), run_time=t.fill(0.25))
            t.hold()

        with self.beat("q5_elimCD") as t:
            self.play(*ac.eliminate("C"), run_time=t.fill(0.2))
            self.play(*ac.eliminate("D"), run_time=t.fill(0.2))
            t.hold()

    def traps(self):
        head = serif("The five traps", TITLE_SIZE)
        head.to_edge(UP, buff=GAP_MD * 1.6)

        with self.beat("traps") as t:
            self.clear_section(t)
            self.play(Write(head), run_time=t.fill(0.35))
            t.hold()

        lines = [
            "1  choosing the most common definition",
            "2  reading only the tested word",
            "3  picking the answer that sounds advanced",
            "4  picking a word with the wrong tone",
            "5  failing to test the answer in the sentence",
        ]
        trap_lines = VGroup(*[serif(s, BODY_SIZE) for s in lines])
        trap_lines.arrange(DOWN, buff=GAP_MD, aligned_edge=LEFT)
        trap_lines.next_to(head, DOWN, buff=GAP_MD * 1.6)

        for name, line in zip(["trap1", "trap2", "trap3", "trap4", "trap5"], trap_lines):
            with self.beat(name) as t:
                self.play(Write(line), run_time=t.fill(0.35))
                t.hold()

    def closing(self):
        steps = [
            "read the entire sentence",
            "explain it in your own words",
            "look for clues",
            "replace the word with your own",
            "match your prediction",
            "re-read with your answer",
        ]
        process_lines = VGroup(
            *[serif(f"{i + 1}  {s}", LABEL_SIZE) for i, s in enumerate(steps)]
        ).arrange(DOWN, buff=GAP_SM * 1.5, aligned_edge=LEFT)
        head = serif("On test day", TITLE_SIZE)
        head.to_edge(UP, buff=GAP_MD * 1.6)
        process_lines.next_to(head, DOWN, buff=GAP_MD * 1.5)

        with self.beat("process") as t:
            self.clear_section(t)
            self.play(Write(head), run_time=t.fill(0.2))
            self.play(Write(process_lines), run_time=t.fill(0.5))
            t.hold()

        key = serif("Context determines meaning.", TITLE_SIZE)
        key.move_to(ORIGIN)

        with self.beat("key") as t:
            self.clear_section(t)
            self.play(Write(key), run_time=t.fill(0.35))
            self.play(Create(underline(key)), run_time=t.fill(0.2))
            t.hold()

        end = mono("end of lecture 4", MARGIN_SIZE)
        end.to_edge(DOWN, buff=GAP_MD)

        with self.beat("end") as t:
            self.play(Write(end), run_time=t.fill(0.4))
            t.hold()
