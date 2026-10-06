"""Full walkthrough of a 2026 Cambridge O Level CS Paper 2, Q1 to Q10.

The lecture is organised by the paper, but anchored on STEP-UP: six habits
the student should leave holding instead of seventy-five answers. The spine
returns whenever a rule is named, so each habit arrives attached to the
question that earned it.

No Cambridge page is reproduced. Question numbers and topics appear as
captions; every algorithm, table and example on screen is our own
recreation of what the narration describes.

Where the delivery or the transcriber is loose, the screen carries the
correct form: TEAR not "tier", DROUGHT not "draw", ANNUAL not "animal",
and the whole-number test as Value MOD 1 <> 0.

Timing: timings/concept.paper2_walkthrough.json
Render: python build/render.py scripts/P2-crash-plan.md \\
    audio/P2-crash-plan.m4a
"""

from manim import (
    Create,
    FadeIn,
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
    GAP_LG,
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
from components.stepup import StepUpSpine, code_block, rule_card
from components.syllabus_map import TopicStrip
from components.word_arc import WordArc
from scenes.base import SATScene

FRAME_SAFE = 12.6
WIDE = 11.5          # width for code panels and rule cards in landscape

RERM = ["Read", "Execute", "Record", "Move"]
PLE = ["Purpose", "Line", "Effect"]
FAMILIES = ["Sequence", "Selection", "Iteration"]
FILE_SEQ = ["Declare", "Open", "Read", "Close"]

# index into the STEP-UP spine
S, T, E, P_PRESERVE, U, P_PLAN = 0, 1, 2, 3, 4, 5


def fit(mobject, width=FRAME_SAFE):
    if mobject.width > width:
        mobject.scale_to_fit_width(width)
    return mobject


class Paper2Walkthrough(SATScene):
    scene_id = "concept.paper2_walkthrough"

    def construct(self):
        self.margin = mono("O Level CS 2210 · Paper 2 walkthrough", MARGIN_SIZE)
        self.margin.to_corner(UP + LEFT, buff=GAP_SM)
        self.add(self.margin)
        self.keep = [self.margin]
        self.strip = None
        self.head = None

        self.opening()
        self.q1_q2()
        self.q3_validation()
        self.q4_coding_testing()
        self.q5_debugging()
        self.q6_trace()
        self.q7_files()
        self.q8_boolean()
        self.q9_sql()
        self.q10_fifteen_marker()
        self.closing()

    # -------------------------------------------------------------- helpers

    def wipe(self, t, fraction=0.05):
        old = [m for m in self.mobjects if m not in self.keep]
        if old:
            self.play(*[FadeOut(m) for m in old], run_time=t.fill(fraction))
        self.head = None

    def title(self, t, text, fraction=0.08, color=CHARCOAL):
        head = fit(serif(text, TITLE_SIZE, color))
        head.to_edge(UP, buff=GAP_MD * 1.9)
        self.play(Write(head), run_time=t.fill(fraction))
        self.head = head
        return head

    def lines(self, *texts, size=BODY_SIZE, color=CHARCOAL, buff=GAP_SM * 1.3,
              align=None):
        group = VGroup(*[fit(serif(x, size, color)) for x in texts])
        if align is None:
            group.arrange(DOWN, buff=buff)
        else:
            group.arrange(DOWN, buff=buff, aligned_edge=align)
        return group

    def column(self, items, top=None, buff=GAP_MD * 1.2, floor=-3.2):
        """Stack under the head, tightening gaps rather than shrinking text."""
        group = VGroup(*items)
        for factor in (1.0, 0.85, 0.7, 0.55, 0.42, 0.32):
            gap = buff * factor
            group.arrange(DOWN, buff=gap)
            if top is None:
                group.move_to(ORIGIN)
            else:
                group.next_to(top, DOWN, buff=gap)
            if group.get_bottom()[1] >= floor:
                break
        return group

    def foot(self, mobject, buff=GAP_MD * 1.1):
        """Place at the bottom, clear of the question strip.

        to_edge(DOWN) collides with the strip, which lives there for most
        of the lecture."""
        if self.strip in self.mobjects:
            mobject.next_to(self.strip, UP, buff=buff)
        else:
            mobject.to_edge(DOWN, buff=buff)
        return mobject

    def question(self, t, number, label, fraction=0.07):
        """Clear to a question page and advance the strip along the bottom."""
        self.wipe(t)
        if self.strip is None:
            self.strip = TopicStrip(10, lit=SLATE, side=0.58)
            self.strip.to_edge(DOWN, buff=GAP_SM * 0.6)
            self.add(self.strip)
            self.keep.append(self.strip)
        head = fit(serif(f"Q{number}  ·  {label}", TITLE_SIZE, CHARCOAL))
        head.to_edge(UP, buff=GAP_MD * 1.9)
        self.play(Write(head), *self.strip.focus(number - 1),
                  run_time=t.fill(fraction))
        self.head = head
        return head

    def rule(self, t, index, caption, fraction=0.16):
        """Flash the STEP-UP letter the narration has just earned."""
        spine = StepUpSpine(size=TITLE_SIZE, width=8.4)
        label = serif(caption, LABEL_SIZE, TERRACOTTA)
        fit(label)
        block = VGroup(spine, label).arrange(DOWN, buff=GAP_MD)
        block.to_edge(DOWN, buff=GAP_LG * 1.1)
        self.play(FadeIn(block), *spine.focus(index), run_time=t.fill(fraction))
        return block

    def code(self, lines, accent=SLATE):
        return code_block(lines, size=LABEL_SIZE, accent=accent, width=WIDE)

    def card(self, lines, color=TERRACOTTA):
        return rule_card(lines, size=TITLE_SIZE, color=color, width=WIDE)

    # ------------------------------------------------------------- sections

    def opening(self):
        with self.beat("hook") as t:
            head = self.lines("O Level Computer Science 2210",
                              "Paper 2 — the whole paper",
                              size=TITLE_SIZE * 1.25)
            head.move_to(UP * 1.2)
            sub = serif("not just the answers — how to think when you don't "
                        "know them", BODY_SIZE, GREY)
            fit(sub)
            sub.next_to(head, DOWN, buff=GAP_LG)
            self.play(Write(head), run_time=t.fill(0.3))
            self.play(Write(sub), run_time=t.fill(0.22))
            t.hold()

        with self.beat("promise") as t:
            self.wipe(t)
            note = self.lines("an actual 2026 Paper 2",
                              "worked end to end", size=TITLE_SIZE)
            note.move_to(UP * 0.6)
            self.play(Write(note), run_time=t.fill(0.4))
            t.hold()

        with self.beat("by_end") as t:
            self.wipe(t)
            self.title(t, "By the end you will have a method for")
            items = self.lines("trace tables", "validation", "debugging",
                               "searching", "Boolean logic", "databases",
                               "the 15-mark programming question",
                               size=BODY_SIZE, align=LEFT)
            self.column([items], self.head)
            for item in items:
                self.play(Write(item), run_time=t.fill(0.075))
            t.hold()

        with self.beat("stepup") as t:
            self.wipe(t)
            word = serif("STEP-UP", TITLE_SIZE * 2.2, TERRACOTTA)
            six = serif("six letters, six habits", BODY_SIZE, GREY)
            block = VGroup(word, six).arrange(DOWN, buff=GAP_LG)
            block.move_to(UP * 0.4)
            self.play(Write(word), run_time=t.fill(0.3))
            self.play(Write(six), run_time=t.fill(0.18))
            t.hold()

        with self.beat("s_step") as t:
            self.wipe(t)
            self.spine = StepUpSpine(labels=True)
            self.spine.move_to(ORIGIN)
            self.play(FadeIn(self.spine), *self.spine.focus(S),
                      run_time=t.fill(0.4))
            t.hold()

        for beat_name, index in (("t_tear", T), ("e_establish", E),
                                 ("p_preserve", P_PRESERVE), ("u_use", U),
                                 ("p_plan", P_PLAN)):
            with self.beat(beat_name) as t:
                self.play(*self.spine.focus(index), run_time=t.fill(0.45))
                t.hold()

        with self.beat("warning") as t:
            self.wipe(t)
            warn = self.lines("Do not memorise this paper.",
                              "Learn the pattern underneath the question.",
                              size=TITLE_SIZE)
            warn[0].set_color(GREY)
            warn[1].set_color(TERRACOTTA)
            warn.move_to(UP * 0.3)
            self.play(Write(warn), run_time=t.fill(0.45))
            t.hold()

    def q1_q2(self):
        with self.beat("q1") as t:
            self.question(t, 1, "which structures are iteration?")
            t.hold()

        with self.beat("q1_mean") as t:
            means = serif("iteration means repetition", BODY_SIZE, CHARCOAL)
            fit(means)
            rows = VGroup(
                self.code(["FOR ... TO ... NEXT"]),
                self.code(["WHILE ... DO ... ENDWHILE"]),
                self.code(["REPEAT ... UNTIL"]),
            ).arrange(DOWN, buff=GAP_SM * 1.2)
            # The note arrives next beat, but it is laid out now so the
            # column reserves room for it instead of dropping it on the code.
            self.q1note = serif("IF and CASE are selection, not iteration",
                                BODY_SIZE, GREY)
            fit(self.q1note)
            self.column([means, rows, self.q1note], self.head)
            self.play(Write(means), run_time=t.fill(0.16))
            self.play(FadeIn(rows), run_time=t.fill(0.3))
            t.hold()

        with self.beat("q1_answer") as t:
            self.play(Write(self.q1note), run_time=t.fill(0.45))
            t.hold()

        with self.beat("families") as t:
            self.wipe(t)
            self.title(t, "Classify every structure into three families")
            rows = VGroup(
                self.lines("Sequence", "one thing after another",
                           size=BODY_SIZE),
                self.lines("Selection", "decisions", size=BODY_SIZE),
                self.lines("Iteration", "repetition", size=BODY_SIZE),
            ).arrange(RIGHT, buff=GAP_LG * 1.4, aligned_edge=UP)
            for row in rows:
                row[0].set_color(TERRACOTTA)
                row[1].set_color(GREY)
            fit(rows)
            self.column([rows], self.head)
            self.play(Write(rows), run_time=t.fill(0.5))
            t.hold()

        with self.beat("q2") as t:
            self.question(t, 2, "which data type holds one character?")
            t.hold()

        with self.beat("q2_char") as t:
            answer = self.code(["DECLARE Letter : CHAR"])
            note = serif("one character — letter, symbol or digit",
                         BODY_SIZE, GREY)
            fit(note)
            self.column([answer, note], self.head)
            self.play(FadeIn(answer), run_time=t.fill(0.3))
            self.play(Write(note), run_time=t.fill(0.2))
            t.hold()

        with self.beat("q2_answer") as t:
            warn = serif("'7' as a CHAR is not the integer 7",
                         BODY_SIZE, TERRACOTTA)
            fit(warn)
            self.foot(warn, GAP_MD * 1.4)
            self.play(Write(warn), run_time=t.fill(0.45))
            t.hold()

    def q3_validation(self):
        with self.beat("q3") as t:
            self.question(t, 3, "validation")
            t.hold()

        with self.beat("presence") as t:
            row = self.lines("must not be left blank", size=BODY_SIZE,
                             color=GREY)
            name = serif("presence check", TITLE_SIZE, TERRACOTTA)
            self.column([row, name], self.head)
            self.play(Write(row), run_time=t.fill(0.3))
            self.play(Write(name), run_time=t.fill(0.3))
            t.hold()

        with self.beat("checkdigit") as t:
            self.wipe(t)
            row = self.lines("an extra calculated digit added to a number",
                             size=BODY_SIZE, color=GREY)
            name = serif("check digit", TITLE_SIZE, TERRACOTTA)
            block = VGroup(row, name).arrange(DOWN, buff=GAP_MD * 1.4)
            block.move_to(UP * 0.8)
            self.play(Write(row), run_time=t.fill(0.3))
            self.play(Write(name), run_time=t.fill(0.3))
            t.hold()

        with self.beat("format") as t:
            self.wipe(t)
            self.title(t, "Format check — does it follow the pattern?")
            shape = self.code(["dd/mm/yyyy"])
            self.column([shape], self.head)
            self.play(FadeIn(shape), run_time=t.fill(0.45))
            self.shape = shape
            t.hold()

        with self.beat("format_trap") as t:
            trap = self.code(["99/99/2036"], accent=TERRACOTTA)
            why = self.lines("the right shape —", "and not a real date",
                             size=BODY_SIZE, color=TERRACOTTA)
            block = VGroup(trap, why).arrange(DOWN, buff=GAP_MD)
            block.next_to(self.shape, DOWN, buff=GAP_MD * 1.4)
            self.play(FadeIn(trap), run_time=t.fill(0.2))
            self.play(Write(why), run_time=t.fill(0.3))
            t.hold()

        with self.beat("q3c") as t:
            self.wipe(t)
            self.title(t, "Q3(c)  ·  collect 15 valid whole numbers")
            key = serif("the keyword is VALID", BODY_SIZE, TERRACOTTA)
            fit(key)
            self.column([key], self.head)
            self.play(Write(key), run_time=t.fill(0.45))
            t.hold()

        with self.beat("valid_first") as t:
            card = self.card(["VALIDATE FIRST", "STORE SECOND"])
            card.move_to(DOWN * 0.6)
            self.play(FadeIn(card), run_time=t.fill(0.45))
            t.hold()

        with self.beat("two_loops") as t:
            self.wipe(t)
            self.title(t, "Two loops, doing two different jobs")
            rows = VGroup(
                self.lines("outer loop", "counts the 15 accepted values",
                           size=BODY_SIZE),
                self.lines("inner loop", "keeps asking until this one is valid",
                           size=BODY_SIZE),
            ).arrange(DOWN, buff=GAP_MD * 1.4)
            for row in rows:
                row[0].set_color(TERRACOTTA)
                row[1].set_color(GREY)
            self.column([rows], self.head)
            self.play(Write(rows), run_time=t.fill(0.5))
            t.hold()

        with self.beat("q3c_code") as t:
            self.wipe(t)
            code = self.code([
                "FOR Counter ← 1 TO 15",
                "    REPEAT",
                "        OUTPUT \"Enter a whole number\"",
                "        INPUT Value",
                "        IF Value MOD 1 <> 0 THEN",
                "            OUTPUT \"Invalid input\"",
                "        ENDIF",
                "    UNTIL Value MOD 1 = 0",
                "    Numbers[Counter] ← Value",
                "NEXT Counter",
            ])
            code.move_to(ORIGIN)
            self.play(FadeIn(code), run_time=t.fill(0.3))
            self.q3code = code
            t.hold()

        with self.beat("mod_why") as t:
            why = serif("a whole number divided by 1 leaves remainder 0",
                        BODY_SIZE, TERRACOTTA)
            fit(why)
            self.foot(why)
            self.play(Write(why), run_time=t.fill(0.4))
            t.hold()

        with self.beat("q3c_marks") as t:
            self.wipe(t)
            self.title(t, "Where the marks are")
            items = self.lines("the loop for 15 inputs",
                               "the whole-number test",
                               "repeating the input until valid",
                               "storing in the right place",
                               "an appropriate message",
                               size=BODY_SIZE, align=LEFT)
            self.column([items], self.head)
            for item in items:
                self.play(Write(item), run_time=t.fill(0.09))
            t.hold()

        with self.beat("and_or") as t:
            self.wipe(t)
            card = self.card(["INSIDE A RANGE = AND",
                              "OUTSIDE A RANGE = OR"])
            card.move_to(UP * 0.4)
            self.play(FadeIn(card), run_time=t.fill(0.5))
            t.hold()

    def q4_coding_testing(self):
        with self.beat("q4") as t:
            self.question(t, 4, "coding and testing")
            t.hold()

        with self.beat("coding") as t:
            head = serif("CODING  —  build it", TITLE_SIZE, TERRACOTTA)
            items = self.lines("turn the design into program code",
                               "use the pseudocode and flowcharts",
                               "write procedures and functions",
                               "comment it so it can be maintained",
                               size=BODY_SIZE, color=GREY, align=LEFT)
            self.column([head, items], self.head)
            self.play(Write(head), run_time=t.fill(0.14))
            for item in items:
                self.play(Write(item), run_time=t.fill(0.09))
            t.hold()

        with self.beat("testing") as t:
            self.wipe(t)
            head = serif("TESTING  —  try to break it", TITLE_SIZE, TERRACOTTA)
            items = self.lines("run it on data whose result you know",
                               "normal, abnormal, boundary and extreme data",
                               "compare actual against expected",
                               "debug, then test again",
                               size=BODY_SIZE, color=GREY, align=LEFT)
            block = VGroup(head, items).arrange(DOWN, buff=GAP_MD * 1.3)
            block.move_to(UP * 0.4)
            self.play(Write(head), run_time=t.fill(0.16))
            for item in items:
                self.play(Write(item), run_time=t.fill(0.1))
            t.hold()

        with self.beat("q4_marks") as t:
            split = serif("3 marks for coding   ·   3 marks for testing",
                          BODY_SIZE, SLATE)
            fit(split)
            self.foot(split, GAP_MD * 1.4)
            self.play(Write(split), run_time=t.fill(0.45))
            t.hold()

        with self.beat("q4_rule") as t:
            self.wipe(t)
            card = self.card(["CODING BUILDS IT",
                              "TESTING TRIES TO BREAK IT"])
            card.move_to(UP * 0.4)
            self.play(FadeIn(card), run_time=t.fill(0.5))
            t.hold()

    def q5_debugging(self):
        with self.beat("q5") as t:
            self.question(t, 5, "debugging, searching and flags")
            t.hold()

        with self.beat("q5_task") as t:
            task = self.lines("search a 2-D array for an account ID",
                              "and display the matching customer name",
                              size=BODY_SIZE, color=GREY)
            self.column([task], self.head)
            self.play(Write(task), run_time=t.fill(0.45))
            t.hold()

        with self.beat("ple") as t:
            self.wipe(t)
            arc = WordArc(PLE, size=TITLE_SIZE, dim=CHARCOAL, lit=TERRACOTTA)
            fit(arc)
            ask = self.lines("what is it supposed to do?",
                             "what does this line actually do?",
                             "do those two match?",
                             size=BODY_SIZE, color=GREY)
            block = VGroup(arc, ask).arrange(DOWN, buff=GAP_LG)
            block.move_to(UP * 0.3)
            self.play(Write(arc), run_time=t.fill(0.25))
            self.play(Write(ask), run_time=t.fill(0.3))
            t.hold()

        for beat_name, label, broken, fixed in (
            ("err1", "error 1 · the data type",
             "DECLARE AccountID : INTEGER", "DECLARE AccountID : STRING"),
            ("err2", "error 2 · the wrong verb",
             "OUTPUT AccountID", "INPUT AccountID"),
            ("err3", "error 3 · one condition, so not CASE",
             "CASE OF AccountID", "IF AccountID = Accounts[Row, 1] THEN"),
            ("err4", "error 4 · the sneaky one",
             "OUTPUT Accounts[1, 2]", "OUTPUT Accounts[Row, 2]"),
        ):
            with self.beat(beat_name) as t:
                self.wipe(t)
                head = fit(serif(label, TITLE_SIZE, CHARCOAL))
                head.to_edge(UP, buff=GAP_MD * 1.9)
                self.play(Write(head), run_time=t.fill(0.12))
                self.head = head
                wrong = self.code([broken], accent=TERRACOTTA)
                right = self.code([fixed], accent=SAGE)
                self.column([wrong, right], head, buff=GAP_MD * 1.5)
                self.play(FadeIn(wrong), run_time=t.fill(0.2))
                self.play(FadeIn(right), run_time=t.fill(0.26))
                if beat_name == "err4":
                    note = serif("found on row 427 — so why print row 1?",
                                 BODY_SIZE, GREY)
                    fit(note)
                    note.next_to(right, DOWN, buff=GAP_MD * 1.2)
                    self.play(Write(note), run_time=t.fill(0.14))
                t.hold()

        with self.beat("linear") as t:
            self.wipe(t)
            self.title(t, "Row 1, row 2, row 3 — one after another")
            name = serif("a LINEAR (sequential) search", TITLE_SIZE,
                         TERRACOTTA)
            fit(name)
            self.column([name], self.head)
            self.play(Write(name), run_time=t.fill(0.45))
            t.hold()

        with self.beat("q5c") as t:
            self.wipe(t)
            ask = self.lines("what if we search the whole array",
                             "and find nothing?", size=TITLE_SIZE)
            ask.move_to(UP * 0.6)
            self.play(Write(ask), run_time=t.fill(0.45))
            t.hold()

        with self.beat("flag") as t:
            self.wipe(t)
            self.title(t, "A Boolean flag remembers whether it happened")
            t.hold()

        with self.beat("flag_code") as t:
            code = self.code([
                "Found ← FALSE",
                "",
                "IF Accounts[Row, 1] = AccountID THEN",
                "    Found ← TRUE",
                "ENDIF",
                "",
                "IF Found = FALSE THEN",
                "    OUTPUT \"Account not found\"",
                "ENDIF",
            ])
            self.column([code], self.head)
            self.play(FadeIn(code), run_time=t.fill(0.45))
            t.hold()

        with self.beat("flag_marks") as t:
            marks = serif("initialise before · set on the match · check after",
                          BODY_SIZE, SLATE)
            fit(marks)
            self.foot(marks, GAP_MD * 1.4)
            self.play(Write(marks), run_time=t.fill(0.4))
            t.hold()

        with self.beat("rule_p") as t:
            self.wipe(t)
            self.rule(t, P_PRESERVE,
                      "once true it stays true until an instruction "
                      "changes it", fraction=0.3)
            t.hold()

    def q6_trace(self):
        with self.beat("q6") as t:
            self.question(t, 6, "the trace table")
            t.hold()

        with self.beat("rerm") as t:
            dont = serif("do not trace it in your head", BODY_SIZE, GREY)
            fit(dont)
            arc = WordArc(RERM, size=TITLE_SIZE, dim=CHARCOAL,
                          lit=TERRACOTTA)
            fit(arc)
            self.column([dont, arc], self.head)
            self.play(Write(dont), run_time=t.fill(0.16))
            self.play(Write(arc), run_time=t.fill(0.3))
            t.hold()

        with self.beat("numletter") as t:
            self.wipe(t)
            warn = self.lines("NumLetter is not the letter.",
                              "It is the position number.",
                              size=TITLE_SIZE)
            warn[1].set_color(TERRACOTTA)
            warn.move_to(UP * 0.5)
            self.play(Write(warn), run_time=t.fill(0.45))
            t.hold()

        with self.beat("post") as t:
            self.wipe(t)
            self.trace_word(t, "POST", [("P·O", "no", 0), ("O·S", "no", 0),
                                        ("S·T", "no", 0)], 0)
            t.hold()

        with self.beat("committee") as t:
            self.wipe(t)
            self.trace_word(t, "COMMITTEE",
                            [("C·O", "no", 0), ("O·M", "no", 0),
                             ("M·M", "MATCH", 1), ("M·I", "no", 1),
                             ("I·T", "no", 1), ("T·T", "MATCH", 2),
                             ("T·E", "no", 2), ("E·E", "MATCH", 3)], 3)
            t.hold()

        with self.beat("no_change") as t:
            # Its own frame: the COMMITTEE trace fills the one above it, and
            # this is one of the six habits, so it should stand alone.
            self.wipe(t)
            card = self.card(["NO ASSIGNMENT  =  NO CHANGE"])
            card.move_to(UP * 0.3)
            self.play(FadeIn(card), run_time=t.fill(0.5))
            t.hold()

        with self.beat("purpose") as t:
            self.wipe(t)
            self.title(t, "What is the algorithm for?")
            answer = serif("it counts pairs of identical consecutive letters",
                           TITLE_SIZE, TERRACOTTA)
            fit(answer)
            self.column([answer], self.head)
            self.play(Write(answer), run_time=t.fill(0.45))
            t.hold()

    def trace_word(self, t, word, pairs, final):
        """A compact trace: the word, the pairs, the running count."""
        letters = VGroup(*[serif(ch, TITLE_SIZE, CHARCOAL) for ch in word])
        letters.arrange(RIGHT, buff=GAP_SM)
        fit(letters, 8.0)
        rows = VGroup()
        for pair, verdict, count in pairs:
            colour = SAGE if verdict == "MATCH" else GREY
            rows.add(VGroup(
                serif(pair, LABEL_SIZE, CHARCOAL),
                serif(verdict, LABEL_SIZE, colour),
                serif(str(count), LABEL_SIZE, SLATE),
            ).arrange(RIGHT, buff=GAP_MD * 1.2))
        rows.arrange(DOWN, buff=GAP_SM * 0.9, aligned_edge=LEFT)
        fit(rows, 6.0)
        out = serif(f"OUTPUT  {final}", TITLE_SIZE, TERRACOTTA)
        block = VGroup(letters, rows, out).arrange(DOWN, buff=GAP_MD * 1.1)
        fit(block, FRAME_SAFE)
        block.move_to(UP * 0.2)
        # COMMITTEE has eight pair rows, which is tall enough to reach the
        # question strip. Lift the block clear rather than shrink the trace.
        floor = -3.05
        if block.get_bottom()[1] < floor:
            block.shift(UP * (floor - block.get_bottom()[1]))
        self.play(Write(letters), run_time=t.fill(0.14))
        self.play(FadeIn(rows), run_time=t.fill(0.3))
        self.play(Write(out), run_time=t.fill(0.16))

    def q7_files(self):
        with self.beat("q7") as t:
            self.question(t, 7, "file handling")
            t.hold()

        with self.beat("why_file") as t:
            why = self.lines("the data must outlive the program",
                             "persistent, non-volatile storage",
                             size=BODY_SIZE)
            why[1].set_color(TERRACOTTA)
            self.column([why], self.head)
            self.play(Write(why), run_time=t.fill(0.45))
            t.hold()

        with self.beat("file_seq") as t:
            self.wipe(t)
            arc = WordArc(FILE_SEQ, size=TITLE_SIZE, dim=CHARCOAL,
                          lit=TERRACOTTA)
            fit(arc)
            code = self.code([
                "DECLARE Name : STRING",
                "OPENFILE \"Names.txt\" FOR READ",
                "READFILE \"Names.txt\", Name",
                "CLOSEFILE \"Names.txt\"",
            ])
            block = VGroup(arc, code).arrange(DOWN, buff=GAP_MD * 1.5)
            block.move_to(UP * 0.2)
            self.play(Write(arc), run_time=t.fill(0.2))
            self.play(FadeIn(code), run_time=t.fill(0.35))
            t.hold()

    def q8_boolean(self):
        with self.beat("q8") as t:
            self.question(t, 8, "Boolean logic")
            t.hold()

        with self.beat("one_jump") as t:
            expr = self.code(["Z = NOT(B OR NOT C) XOR (A NAND C)"],
                             accent=TERRACOTTA)
            warn = serif("do not solve this in one mental jump",
                         BODY_SIZE, GREY)
            fit(warn)
            self.column([expr, warn], self.head)
            self.play(FadeIn(expr), run_time=t.fill(0.26))
            self.play(Write(warn), run_time=t.fill(0.2))
            t.hold()

        with self.beat("intermediates") as t:
            self.wipe(t)
            code = self.code([
                "X1 ← NOT C",
                "X2 ← B OR X1",
                "X3 ← NOT X2",
                "X4 ← A NAND C",
                "Z  ← X3 XOR X4",
            ])
            code.move_to(UP * 0.5)
            self.play(FadeIn(code), run_time=t.fill(0.45))
            self.boolcode = code
            t.hold()

        with self.beat("circuit") as t:
            note = serif("one operation at a time · one column at a time",
                         BODY_SIZE, SLATE)
            fit(note)
            note.next_to(self.boolcode, DOWN, buff=GAP_MD * 1.6)
            self.play(Write(note), run_time=t.fill(0.45))
            t.hold()

        with self.beat("mechanical") as t:
            self.wipe(t)
            card = self.card(["STOP BEING CLEVER", "ONE GATE, ONE RESULT"])
            card.move_to(UP * 0.3)
            self.play(FadeIn(card), run_time=t.fill(0.45))
            t.hold()

    def q9_sql(self):
        with self.beat("q9") as t:
            self.question(t, 9, "databases and SQL")
            t.hold()

        with self.beat("datatypes") as t:
            rows = VGroup()
            for field, kind in (("PartID", "TEXT"), ("PartName", "TEXT"),
                                ("Price", "REAL"), ("Colour", "CHAR"),
                                ("NumberInStock", "INTEGER"),
                                ("InStock", "BOOLEAN")):
                rows.add(VGroup(serif(field, LABEL_SIZE, CHARCOAL),
                                serif(kind, LABEL_SIZE, SLATE)))
            left = VGroup(*[r[0] for r in rows])
            left.arrange(DOWN, buff=GAP_SM, aligned_edge=LEFT)
            right = VGroup(*[r[1] for r in rows])
            right.arrange(DOWN, buff=GAP_SM, aligned_edge=LEFT)
            right.next_to(left, RIGHT, buff=GAP_LG * 1.4)
            for a, b in zip(left, right):
                b.set_y(a.get_y())
            table = VGroup(left, right)
            fit(table, 9.0)
            self.column([table], self.head)
            self.play(FadeIn(table), run_time=t.fill(0.5))
            t.hold()

        with self.beat("sql_three") as t:
            self.wipe(t)
            arc = WordArc(["what", "where", "which"], size=TITLE_SIZE,
                          arrow="·", dim=CHARCOAL, lit=TERRACOTTA)
            fit(arc)
            arc.move_to(UP * 1.4)
            self.play(Write(arc), run_time=t.fill(0.4))
            self.sqlarc = arc
            t.hold()

        with self.beat("sql_code") as t:
            code = self.code([
                "SELECT PartID, CarType, NumberInStock",
                "FROM   CarParts",
                "WHERE  PartName = 'brake pads'",
            ])
            code.next_to(self.sqlarc, DOWN, buff=GAP_MD * 1.6)
            self.play(FadeIn(code), run_time=t.fill(0.45))
            t.hold()

        with self.beat("redundant") as t:
            self.wipe(t)
            self.title(t, "Why InStock is not needed")
            why = self.lines("NumberInStock already says it:",
                             "0 means out of stock, more than 0 means in",
                             "storing both repeats the same fact",
                             size=BODY_SIZE, color=GREY)
            why[2].set_color(TERRACOTTA)
            self.column([why], self.head)
            self.play(Write(why), run_time=t.fill(0.5))
            t.hold()

        with self.beat("sql_rule") as t:
            self.wipe(t)
            card = self.card(["SELECT what", "FROM where", "WHERE which"])
            card.move_to(UP * 0.3)
            self.play(FadeIn(card), run_time=t.fill(0.45))
            t.hold()

    def q10_fifteen_marker(self):
        with self.beat("q10") as t:
            self.question(t, 10, "the 15-mark programming question")
            t.hold()

        with self.beat("fear") as t:
            fear = serif("the question most students fear", BODY_SIZE, GREY)
            fit(fear)
            self.column([fear], self.head)
            self.play(Write(fear), run_time=t.fill(0.45))
            t.hold()

        with self.beat("plan_first") as t:
            self.wipe(t)
            card = self.card(["THE FIRST THING WE WRITE", "IS NOT CODE"])
            card.move_to(UP * 0.4)
            self.play(FadeIn(card), run_time=t.fill(0.45))
            t.hold()

        with self.beat("requirements") as t:
            self.wipe(t)
            self.title(t, "A year of rainfall, in one paragraph")
            asks = self.lines("365 values · a total · a mean",
                              "days with no rain",
                              "the longest run of dry days",
                              "and a drought decision",
                              size=BODY_SIZE, color=GREY)
            self.column([asks], self.head)
            self.play(Write(asks), run_time=t.fill(0.5))
            t.hold()

        with self.beat("tear_down") as t:
            self.rule(t, T, "tear it into requirements", fraction=0.4)
            t.hold()

        with self.beat("patterns") as t:
            self.wipe(t)
            self.req_table(t)
            t.hold()

        with self.beat("blocks") as t:
            note = serif("now write it one block at a time", BODY_SIZE, SLATE)
            fit(note)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.45))
            t.hold()

        with self.beat("declare") as t:
            self.wipe(t)
            self.title(t, "Block 1  ·  declare and initialise")
            code = self.code([
                "DECLARE Rainfall : ARRAY[1:365] OF REAL",
                "DECLARE Day, NoRainDays : INTEGER",
                "DECLARE CurrentDryRun, LongestDryRun : INTEGER",
                "DECLARE TotalRain, TotalCM, AverageRain : REAL",
            ])
            self.column([code], self.head)
            self.play(FadeIn(code), run_time=t.fill(0.35))
            self.declcode = code
            t.hold()

        with self.beat("init") as t:
            # Its own screen: declarations plus initialisation plus the note
            # runs past the bottom of the frame.
            self.wipe(t)
            self.title(t, "Establish the starting values", fraction=0.07)
            init = self.code([
                "TotalRain ← 0",
                "NoRainDays ← 0",
                "CurrentDryRun ← 0",
                "LongestDryRun ← 0",
            ], accent=SAGE)
            note = serif("never assume a counter starts at zero",
                         BODY_SIZE, TERRACOTTA)
            fit(note)
            self.column([init, note], self.head)
            self.play(FadeIn(init), run_time=t.fill(0.3))
            self.play(Write(note), run_time=t.fill(0.22))
            t.hold()

        with self.beat("input_block") as t:
            self.wipe(t)
            self.title(t, "Block 2  ·  input")
            code = self.code([
                "FOR Day ← 1 TO 365",
                "    OUTPUT \"Enter rainfall in mm for day \", Day",
                "    INPUT Rainfall[Day]",
                "NEXT Day",
            ])
            note = serif("Day gives both the repetition and the array position",
                         BODY_SIZE, GREY)
            fit(note)
            self.column([code, note], self.head)
            self.play(FadeIn(code), run_time=t.fill(0.3))
            self.play(Write(note), run_time=t.fill(0.2))
            t.hold()

        with self.beat("total_avg") as t:
            self.wipe(t)
            self.title(t, "Block 3  ·  total and mean")
            code = self.code([
                "FOR Day ← 1 TO 365",
                "    TotalRain ← TotalRain + Rainfall[Day]",
                "NEXT Day",
                "AverageRain ← TotalRain / 365",
                "TotalCM ← ROUND(TotalRain / 10, 2)",
            ])
            self.column([code], self.head)
            self.play(FadeIn(code), run_time=t.fill(0.45))
            self.totcode = code
            t.hold()

        with self.beat("accumulator") as t:
            note = serif("an accumulator adds to itself — it never replaces",
                         BODY_SIZE, TERRACOTTA)
            fit(note)
            note.next_to(self.totcode, DOWN, buff=GAP_MD * 1.3)
            self.play(Write(note), run_time=t.fill(0.45))
            t.hold()

        with self.beat("rounding") as t:
            self.wipe(t)
            rows = self.lines("total in centimetres — 2 decimal places",
                              "mean in millimetres — 4 decimal places",
                              size=TITLE_SIZE, color=CHARCOAL)
            rows.move_to(UP * 0.4)
            self.play(Write(rows), run_time=t.fill(0.5))
            t.hold()

        with self.beat("dry_days") as t:
            self.wipe(t)
            self.title(t, "Block 4  ·  the longest dry run")
            story = self.lines("five dry days, then rain falls",
                               "the current streak dies",
                               "the record does not",
                               size=BODY_SIZE, color=GREY)
            self.column([story], self.head)
            self.play(Write(story), run_time=t.fill(0.45))
            t.hold()

        with self.beat("resets") as t:
            card = self.card(["CURRENT RESETS", "RECORD SURVIVES"])
            self.foot(card)
            self.play(FadeIn(card), run_time=t.fill(0.5))
            t.hold()

        with self.beat("dry_code") as t:
            self.wipe(t)
            code = self.code([
                "IF Rainfall[Day] = 0 THEN",
                "    NoRainDays ← NoRainDays + 1",
                "    CurrentDryRun ← CurrentDryRun + 1",
                "    IF CurrentDryRun > LongestDryRun THEN",
                "        LongestDryRun ← CurrentDryRun",
                "    ENDIF",
                "ELSE",
                "    CurrentDryRun ← 0",
                "ENDIF",
            ])
            code.move_to(UP * 0.2)
            self.play(FadeIn(code), run_time=t.fill(0.4))
            t.hold()

        with self.beat("three_patterns") as t:
            three = serif("counter  ·  consecutive counter  ·  maximum",
                          BODY_SIZE, TERRACOTTA)
            fit(three)
            self.foot(three)
            self.play(Write(three), run_time=t.fill(0.45))
            t.hold()

        with self.beat("output_block") as t:
            self.wipe(t)
            self.title(t, "Block 5  ·  output and the decision")
            code = self.code([
                "OUTPUT \"Total rainfall (cm): \", TotalCM",
                "OUTPUT \"Mean daily rainfall (mm): \", AverageRain",
                "OUTPUT \"Days with no rain: \", NoRainDays",
                "OUTPUT \"Longest dry period: \", LongestDryRun",
            ])
            self.column([code], self.head)
            self.play(FadeIn(code), run_time=t.fill(0.45))
            t.hold()

        with self.beat("drought") as t:
            self.wipe(t)
            code = self.code([
                "IF LongestDryRun >= 15 THEN",
                "    OUTPUT \"There was a drought\"",
                "ELSE",
                "    OUTPUT \"There was no drought\"",
                "ENDIF",
            ])
            code.move_to(UP * 0.6)
            self.play(FadeIn(code), run_time=t.fill(0.45))
            self.droughtcode = code
            t.hold()

        with self.beat("why_ge") as t:
            why = serif("15 itself qualifies — so >= 15, not > 15",
                        TITLE_SIZE, TERRACOTTA)
            fit(why)
            why.next_to(self.droughtcode, DOWN, buff=GAP_MD * 1.6)
            self.play(Write(why), run_time=t.fill(0.45))
            t.hold()

        with self.beat("bestfit") as t:
            self.wipe(t)
            self.title(t, "Cambridge marks this best-fit")
            t.hold()

        with self.beat("marks_split") as t:
            rows = self.lines("up to 9 marks — appropriate techniques "
                              "and data structures",
                              "up to 6 marks — logic, naming, comments, "
                              "completeness",
                              size=BODY_SIZE, color=CHARCOAL)
            self.column([rows], self.head)
            self.play(Write(rows), run_time=t.fill(0.5))
            t.hold()

        with self.beat("syntax") as t:
            note = serif("a minor syntax slip does not destroy a sound "
                         "solution", BODY_SIZE, SAGE)
            fit(note)
            self.foot(note, GAP_MD * 1.4)
            self.play(Write(note), run_time=t.fill(0.45))
            t.hold()

    def req_table(self, t):
        """The paragraph, turned into patterns the student already knows."""
        pairs = [("store 365 values", "ARRAY"),
                 ("enter them", "INPUT + LOOP"),
                 ("annual rainfall", "ACCUMULATOR"),
                 ("mean", "CALCULATION"),
                 ("days with no rain", "COUNTER"),
                 ("longest dry run", "CURRENT + MAXIMUM"),
                 ("drought?", "IF")]
        left = VGroup(*[serif(a, LABEL_SIZE, GREY) for a, _ in pairs])
        left.arrange(DOWN, buff=GAP_SM, aligned_edge=LEFT)
        right = VGroup(*[serif(b, LABEL_SIZE, SLATE) for _, b in pairs])
        right.arrange(DOWN, buff=GAP_SM, aligned_edge=LEFT)
        right.next_to(left, RIGHT, buff=GAP_LG * 1.6)
        for a, b in zip(left, right):
            b.set_y(a.get_y())
        table = VGroup(left, right)
        fit(table, 10.0)
        table.move_to(UP * 0.4)
        self.play(FadeIn(table), run_time=t.fill(0.45))

    def closing(self):
        with self.beat("close") as t:
            self.wipe(t)
            if self.strip in self.keep:
                self.keep.remove(self.strip)
                self.play(FadeOut(self.strip), run_time=t.fill(0.08))
            line = self.lines("a whole 75-mark paper,",
                              "and I don't want you remembering 75 answers",
                              size=TITLE_SIZE)
            line.move_to(UP * 0.4)
            self.play(Write(line), run_time=t.fill(0.45))
            t.hold()

        with self.beat("six_habits") as t:
            self.wipe(t)
            spine = StepUpSpine(labels=True)
            spine.move_to(UP * 0.2)
            self.play(FadeIn(spine), run_time=t.fill(0.2))
            for index in range(6):
                self.play(*spine.focus(index), run_time=t.fill(0.1))
            t.hold()

        with self.beat("cta") as t:
            self.wipe(t)
            line = self.lines("Work the paper yourself.",
                              "Every time you get stuck, ask which "
                              "STEP-UP rule applies.", size=TITLE_SIZE)
            line[1].set_color(TERRACOTTA)
            line.move_to(UP * 0.4)
            self.play(Write(line), run_time=t.fill(0.5))
            t.hold()

        with self.beat("signoff") as t:
            self.wipe(t)
            who = self.lines("Ibrahim", "The Digital Tutor",
                             size=TITLE_SIZE * 1.3)
            who[1].set_color(GREY)
            where = serif("academy.thedigitaltutor.net", BODY_SIZE, TERRACOTTA)
            block = VGroup(who, where).arrange(DOWN, buff=GAP_LG)
            block.move_to(UP * 0.2)
            self.play(Write(who), run_time=t.fill(0.3))
            self.play(Write(where), run_time=t.fill(0.2))
            t.hold()
