"""A Level 9618 Short: take one wide relation to third normal form.

Two steps, and students stop after the first. Removing the partial
dependencies on a composite key gets you to 2NF and feels finished; the
transitive dependency hiding inside the Course table is what 3NF is
actually about, and it is the mark that goes missing.

The decomposition was checked against the stated dependencies before
building: StudentID -> StudentName and CourseID -> CourseName, TutorID,
Room are partial on the composite key StudentID + CourseID, and
CourseID -> TutorID -> TutorName is transitive.

Where the transcriber is loose the screen carries the correct form: the
audio says "tutor ID determines tutor name", and the third dependency is
TutorID -> TutorName.

Timing: timings/shorts.normal_form.json
Render: python build/render.py scripts/AL3-normal-form.md \\
    audio/AL3-normal-form.m4a -r 1080,1920
"""

from manim import (
    FadeIn,
    LEFT,
    VGroup,
    Write,
    DOWN,
    UP,
)

from scenes.shorts.alevel_base import (  # pins the portrait frame on import
    CAPTION,
    LEAD,
    ALevelShort,
)
from brand import (CHARCOAL, GAP_MD, GAP_SM, GREY, SAGE, SLATE,
                   TERRACOTTA, mono, serif)
from components.alevel import ANSWER, QUESTION, fit, spec_block, table_card

RELATIONS = {
    "STUDENT": (["StudentID", "StudentName"], [0]),
    "COURSE": (["CourseID", "CourseName", "TutorID", "Room"], [0]),
    "TUTOR": (["TutorID", "TutorName"], [0]),
    "ENROLMENT": (["StudentID", "CourseID"], [0, 1]),
}


class NormalForm(ALevelShort):
    scene_id = "shorts.normal_form"
    strap_text = "A Level 9618 · normalisation"

    def construct(self):
        self.open_strap()
        self.the_question()
        self.the_partials()
        self.the_transitive()
        self.the_answer()

    # -------------------------------------------------------------- helpers

    def relation(self, name, width=3.4, accent=SAGE):
        fields, key = RELATIONS[name]
        return table_card(name, fields, key=key, accent=accent, width=width)

    def relation_lines(self, name, rows, color=SAGE, size=24):
        """A relation as a heading over its fields, for the final list.

        The four tables will not fit as boxed cards: COURSE's field list on
        one line is width-bound at 21px in portrait whatever font size it
        is given, so it wraps and the boxes go.
        """
        title = serif(name, size * 1.1, color)
        body = VGroup(*[mono(r, size, CHARCOAL) for r in rows])
        body.arrange(DOWN, buff=GAP_SM * 0.4, aligned_edge=LEFT)
        return VGroup(title, body).arrange(DOWN, buff=GAP_SM * 0.45,
                                           aligned_edge=LEFT)

    # ------------------------------------------------------------- sections

    def the_question(self):
        with self.beat("hook") as t:
            self.hook(t, fraction=0.5)
            t.hold()

        with self.beat("table") as t:
            self.wipe(t, 0.1)
            self.schema = spec_block([
                "ENROLMENT", "  StudentID", "  StudentName", "  CourseID",
                "  CourseName", "  TutorID", "  TutorName", "  Room",
            ], accent=SLATE)
            self.schema.move_to(UP * 1.2)
            self.play(FadeIn(self.schema[0]), run_time=t.fill(0.16))
            self.play(Write(self.schema[1]), run_time=t.fill(0.5))
            t.hold()

        with self.beat("fields") as t:
            t.hold()

        with self.beat("key") as t:
            note = self.lines("key:  StudentID + CourseID",
                              size=CAPTION, color=TERRACOTTA)
            self.under(note, self.schema, buff=GAP_MD * 0.9)
            self.play(Write(note), run_time=t.fill(0.5))
            self.key_note = note
            t.hold()

        with self.beat("fd1") as t:
            self.wipe(t, 0.1)
            self.fds = spec_block([
                "StudentID -> StudentName",
            ], accent=GREY)
            self.fds.move_to(UP * 1.6)
            self.play(FadeIn(self.fds[0]), run_time=t.fill(0.16))
            self.play(Write(self.fds[1]), run_time=t.fill(0.45))
            t.hold()

        with self.beat("fd2") as t:
            block = spec_block([
                "CourseID -> CourseName,",
                "            TutorID, Room",
            ], accent=GREY)
            self.under(block, self.fds, buff=GAP_MD * 0.7)
            self.play(FadeIn(block[0]), run_time=t.fill(0.14))
            self.play(Write(block[1]), run_time=t.fill(0.45))
            self.fd2 = block
            t.hold()

        with self.beat("fd3") as t:
            # The audio says "tutor ID determines tutor name".
            block = spec_block(["TutorID -> TutorName"], accent=GREY)
            self.under(block, self.fd2, buff=GAP_MD * 0.7)
            self.play(FadeIn(block[0]), run_time=t.fill(0.16))
            self.play(Write(block[1]), run_time=t.fill(0.45))
            t.hold()

        with self.beat("question") as t:
            self.wipe(t, 0.14)
            ask = self.lines("Convert this to", size=QUESTION)
            target = fit(serif("3NF", ANSWER * 1.4, TERRACOTTA))
            block = VGroup(ask, target).arrange(DOWN, buff=GAP_MD)
            block.move_to(UP * 0.8)
            self.play(Write(ask), run_time=t.fill(0.25))
            self.play(Write(target), run_time=t.fill(0.3))
            t.hold()

        with self.beat("pause") as t:
            self.pause_card(t, fraction=0.45)
            t.hold()

    def the_partials(self):
        with self.beat("solve") as t:
            self.wipe(t, 0.3)
            t.hold()

        with self.beat("partial1") as t:
            note = self.lines("StudentName needs only",
                              "half of the key",
                              size=LEAD, color=CHARCOAL)
            note.move_to(UP * 1.6)
            self.play(Write(note), run_time=t.fill(0.5))
            self.note = note
            t.hold()

        with self.beat("partial_rule") as t:
            label = self.caption("PARTIAL DEPENDENCY", TERRACOTTA, 26)
            self.under(label, self.note, buff=GAP_MD)
            self.play(Write(label), run_time=t.fill(0.5))
            self.rule_label = label
            t.hold()

        with self.beat("student_table") as t:
            card = self.relation("STUDENT")
            self.under(card, self.rule_label, buff=GAP_MD)
            self.play(FadeIn(card), run_time=t.fill(0.5))
            t.hold()

        with self.beat("course_fd") as t:
            self.wipe(t, 0.12)
            note = self.lines("CourseName, TutorID and Room",
                              "need only CourseID",
                              size=CAPTION, color=CHARCOAL)
            note.move_to(UP * 1.8)
            self.play(Write(note), run_time=t.fill(0.5))
            self.note = note
            t.hold()

        with self.beat("course_table") as t:
            card = self.relation("COURSE")
            self.under(card, self.note, buff=GAP_MD)
            self.play(FadeIn(card), run_time=t.fill(0.5))
            self.course_card = card
            t.hold()

        with self.beat("enrol_table") as t:
            card = self.relation("ENROLMENT")
            self.under(card, self.course_card, buff=GAP_MD * 0.8)
            self.play(FadeIn(card), run_time=t.fill(0.5))
            t.hold()

    def the_transitive(self):
        with self.beat("not_finished") as t:
            self.wipe(t, 0.2)
            note = fit(serif("not finished", ANSWER, TERRACOTTA))
            note.move_to(UP * 1.4)
            self.play(Write(note), run_time=t.fill(0.5))
            self.note = note
            t.hold()

        with self.beat("transitive") as t:
            chain = spec_block(["CourseID -> TutorID",
                                "          -> TutorName"], accent=SLATE)
            self.under(chain, self.note, buff=GAP_MD)
            self.play(FadeIn(chain[0]), run_time=t.fill(0.16))
            self.play(Write(chain[1]), run_time=t.fill(0.45))
            self.chain = chain
            t.hold()

        with self.beat("transitive_rule") as t:
            label = self.caption("TRANSITIVE DEPENDENCY", TERRACOTTA, 26)
            self.under(label, self.chain, buff=GAP_MD)
            self.play(Write(label), run_time=t.fill(0.5))
            self.rule_label = label
            t.hold()

        with self.beat("tutor_table") as t:
            card = self.relation("TUTOR")
            self.under(card, self.rule_label, buff=GAP_MD)
            self.play(FadeIn(card), run_time=t.fill(0.5))
            t.hold()

    def the_answer(self):
        with self.beat("four_tables") as t:
            self.wipe(t, 0.14)
            cards = VGroup(
                self.relation_lines("STUDENT", ["StudentID, StudentName"]),
                self.relation_lines("COURSE", ["CourseID, CourseName,",
                                               "TutorID, Room"]),
                self.relation_lines("TUTOR", ["TutorID, TutorName"]),
                self.relation_lines("ENROLMENT", ["StudentID, CourseID"]),
            )
            cards.arrange(DOWN, buff=GAP_MD * 0.75, aligned_edge=LEFT)
            fit(cards, 3.7)
            cards.move_to(UP * 1.1)
            self.cards = cards
            self.play(FadeIn(cards[0]), FadeIn(cards[1]),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("names") as t:
            self.play(FadeIn(self.cards[2]), FadeIn(self.cards[3]),
                      run_time=t.fill(0.5))
            t.hold()

        with self.beat("trap") as t:
            trap = self.lines("stop after the partials",
                              "and you have 2NF",
                              size=LEAD, color=TERRACOTTA)
            trap.next_to(self.cards, DOWN, buff=GAP_MD)
            self.play(Write(trap), run_time=t.fill(0.5))
            t.hold()

        with self.beat("close") as t:
            self.wipe(t, 0.2)
            self.close_series(t, fraction=0.45)
            t.hold()
