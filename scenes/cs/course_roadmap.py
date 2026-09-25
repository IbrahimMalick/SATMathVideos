"""CS lecture: Cambridge O Level Computer Science 2210 — course roadmap.

Narration script: scripts/CS00-course-roadmap.md

This is the introduction to the whole course, so the visuals are a map
rather than a topic. Everything hangs on ordered sequences the student
should leave holding, each of which returns later in the course:

    DATA -> ALGORITHM -> PROGRAM -> SYSTEM        how a problem grows
    PROBLEM -> PLAN -> ALGORITHM -> CODE -> TEST  how Paper 2 works
    KNOW / APPLY / JUDGE                          what Cambridge marks
    SENSE -> PROCESS -> ACT -> REPEAT             an automated system
    CLAIM -> REASON -> CONTEXT -> CONCLUSION      an evaluation
    LEARN -> USE -> EXPLAIN -> EXAMINE            how to study
    UNDERSTAND -> VISUALISE -> CONNECT -> APPLY -> ANSWER   how we teach
    BITS -> DATA -> ... -> SOLUTIONS              the journey itself

The ten syllabus topics are the spine. They appear in full once, as a
two-column SyllabusMap, and then as a TopicStrip along the bottom that
tracks which topic is being described.

Note where the recording and the screen differ: the narration says
"the internet and its users" (the syllabus says "uses"), "Topic A"
(topic eight), "farming" (pharming) and "why backers" (why packets).
The screen carries the correct wording in each case.
"""

import numpy as np

from manim import (
    Arrow,
    Create,
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
from components.syllabus_map import SyllabusMap, TopicStrip
from components.word_arc import WordArc
from scenes.base import SATScene

TOPICS_P1 = [
    (1, "Data representation"),
    (2, "Data transmission"),
    (3, "Hardware"),
    (4, "Software"),
    (5, "The internet and its uses"),
    (6, "Automated and emerging technologies"),
]
TOPICS_P2 = [
    (7, "Algorithm design and problem-solving"),
    (8, "Programming"),
    (9, "Databases"),
    (10, "Boolean logic"),
]

DAPS = ["Data", "Algorithm", "Program", "System"]
PPACT = ["Problem", "Plan", "Algorithm", "Code", "Test"]
KAJ = ["Know", "Apply", "Judge"]
SPAR = ["Sense", "Process", "Act", "Repeat"]
CRCC = ["Claim", "Reason", "Context", "Conclusion"]
LUEE = ["Learn it", "Use it", "Explain it", "Examine it"]
UVCAA = ["Understand", "Visualise", "Connect", "Apply", "Answer"]
JOURNEY = ["Bits", "Data", "Systems", "Networks",
           "Algorithms", "Programs", "Solutions"]

FRAME_SAFE = 12.6


def fit(mobject, width=FRAME_SAFE):
    if mobject.width > width:
        mobject.scale_to_fit_width(width)
    return mobject


def lines(*texts, size=BODY_SIZE, color=CHARCOAL, buff=GAP_SM * 1.3,
          align=None):
    group = VGroup(*[fit(serif(t, size, color)) for t in texts])
    if align is None:
        group.arrange(DOWN, buff=buff)
    else:
        group.arrange(DOWN, buff=buff, aligned_edge=align)
    return group


def box(text, width=3.0, height=1.1, color=SLATE, size=LABEL_SIZE,
        text_color=CHARCOAL):
    rect = Rectangle(width=width, height=height, color=color,
                     stroke_width=3)
    label = serif(text, size, text_color)
    if label.width > width - 0.3:
        label.scale_to_fit_width(width - 0.3)
    label.move_to(rect)
    return VGroup(rect, label)


def chain(labels, width=2.6, height=1.0, color=SLATE, size=LABEL_SIZE,
          buff=GAP_SM * 1.4):
    """A left-to-right run of boxes joined by arrows."""
    group = VGroup()
    boxes = VGroup()
    for i, text in enumerate(labels):
        if i:
            group.add(Arrow(LEFT, RIGHT, buff=0, color=GREY,
                            stroke_width=3, max_tip_length_to_length_ratio=0.35)
                      .scale(0.5))
        cell = box(text, width, height, color, size)
        boxes.add(cell)
        group.add(cell)
    group.arrange(RIGHT, buff=buff)
    fit(group)
    group.boxes = boxes
    return group


class CourseRoadmap(SATScene):
    scene_id = "cs.course_roadmap"

    def construct(self):
        self.margin_note = mono("O Level CS 2210 · course roadmap",
                                MARGIN_SIZE)
        self.margin_note.to_corner(UP + LEFT, buff=GAP_SM)
        self.add(self.margin_note)
        self.persistent = [self.margin_note]
        self.section_head = None
        self.strip = None

        self.opening()
        self.what_it_is()
        self.school_case()
        self.papers()
        self.paper_one_topics()
        self.paper_two_topics()
        self.skills()
        self.traps()
        self.method()
        self.programming()
        self.roadmap()
        self.rules()
        self.closing()

    # -------------------------------------------------------------- helpers

    def clear_all(self, t, fraction=0.05):
        old = [m for m in self.mobjects if m not in self.persistent]
        if old:
            self.play(*[FadeOut(m) for m in old], run_time=t.fill(fraction))
        self.section_head = None

    def set_head(self, t, text, fraction=0.08, color=CHARCOAL):
        head = fit(serif(text, TITLE_SIZE, color))
        head.to_edge(UP, buff=GAP_MD * 1.9)
        self.play(Write(head), run_time=t.fill(fraction))
        self.section_head = head
        return head

    def below_head(self, mobject, buff=GAP_MD * 1.4):
        if self.section_head is None:
            mobject.move_to(ORIGIN)
        else:
            mobject.next_to(self.section_head, DOWN, buff=buff)
        return mobject

    def column(self, items, top=None, buff=GAP_MD * 1.2, floor=-3.15):
        """Stack items under ``top``, tightening the gaps if the column
        would run into the topic strip along the bottom of the frame.

        Shrinking the text instead would take it under the 28px floor, so
        the spacing is what gives.
        """
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

    def underline(self, mobject, color=SAGE):
        return Line(
            mobject.get_corner(DOWN + LEFT) + DOWN * GAP_SM,
            mobject.get_corner(DOWN + RIGHT) + DOWN * GAP_SM,
            color=color, stroke_width=3,
        )

    def bullets(self, t, items, per=0.1, size=BODY_SIZE, color=CHARCOAL,
                buff=GAP_SM * 1.3):
        group = lines(*items, size=size, color=color, buff=buff, align=LEFT)
        self.below_head(group)
        for item in group:
            self.play(Write(item), run_time=t.fill(per))
        return group

    def arc(self, t, words, index=None, fraction=0.1, size=LABEL_SIZE,
            edge=DOWN, rows=1):
        bar = WordArc(words, size=size, rows=rows, lit=TERRACOTTA)
        bar.to_edge(edge, buff=GAP_MD * 0.9)
        moves = bar.focus(index) if index is not None else []
        self.play(FadeIn(bar), *moves, run_time=t.fill(fraction))
        return bar

    def topic_frame(self, t, index, question=None):
        """Clear to a topic page: strip advances, header and question land."""
        self.clear_all(t)
        if self.strip is None:
            # The strip only makes sense once we start walking the topics,
            # and before that the full map needs the whole frame.
            # The lit cell is a position marker, not the thing to look at,
            # so it stays slate and leaves terracotta free for the content.
            self.strip = TopicStrip(10, split=6, lit=SLATE)
            self.strip.to_edge(DOWN, buff=GAP_SM * 0.5)
            self.add(self.strip)
            self.persistent.append(self.strip)
        number, title = (TOPICS_P1 + TOPICS_P2)[index]
        head = fit(serif(f"{number}  ·  {title}", TITLE_SIZE, CHARCOAL))
        head.to_edge(UP, buff=GAP_MD * 1.9)
        self.play(Write(head), *self.strip.focus(index), run_time=t.fill(0.09))
        self.section_head = head
        if question:
            ask = fit(serif(question, BODY_SIZE, SLATE))
            self.below_head(ask, buff=GAP_MD * 1.1)
            self.play(Write(ask), run_time=t.fill(0.1))
            self.section_head = VGroup(head, ask)
        return head

    # ------------------------------------------------------------- sections

    def opening(self):
        with self.beat("hook") as t:
            pile = lines("ten chapters",
                         "hundreds of definitions",
                         "a confusing amount of programming",
                         size=TITLE_SIZE, color=GREY)
            pile.move_to(UP * 0.9)
            ask = serif("give me the next forty minutes",
                        TITLE_SIZE * 1.1, TERRACOTTA)
            fit(ask)
            ask.next_to(pile, DOWN, buff=GAP_LG)
            self.play(Write(pile), run_time=t.fill(0.35))
            self.play(Write(ask), run_time=t.fill(0.25))
            t.hold()

        with self.beat("promise") as t:
            self.clear_all(t)
            title = lines("Cambridge O Level", "Computer Science 2210",
                          size=TITLE_SIZE * 1.4)
            title.move_to(UP * 1.1)
            sub = serif("the entire course, turned into a map",
                        BODY_SIZE, GREY)
            sub.next_to(title, DOWN, buff=GAP_MD * 1.6)
            self.play(Write(title), run_time=t.fill(0.3))
            self.play(Write(sub), run_time=t.fill(0.2))
            self.promise_anchor = sub
            t.hold()

        with self.beat("one_map") as t:
            stamp = serif("ONE MAP", TITLE_SIZE * 1.3, TERRACOTTA)
            stamp.next_to(self.promise_anchor, DOWN, buff=GAP_MD * 1.6)
            self.play(Write(stamp), run_time=t.fill(0.4))
            t.hold()

        with self.beat("you_will_know") as t:
            self.clear_all(t)
            self.set_head(t, "By the end of this lesson you will know")
            self.bullets(t, [
                "what you actually need to learn",
                "why Paper 1 and Paper 2 need different skills",
                "where students commonly lose marks",
                "how programming fits into the examination",
                "the order in which to learn everything",
            ], per=0.1)
            t.hold()

        with self.beat("scattered") as t:
            self.clear_all(t)
            words = ["binary", "packets", "CPU registers", "phishing",
                     "algorithms", "pseudocode", "arrays", "SQL",
                     "logic gates"]
            # A jittered grid, not free scatter: the longest label is over
            # three units wide, so random placement overlaps words.
            rng = np.random.default_rng(7)
            self.cloud = VGroup()
            for i, word in enumerate(words):
                label = serif(word, LABEL_SIZE, GREY)
                col, row = i % 3, i // 3
                label.move_to(np.array([
                    (col - 1) * 4.4 + rng.uniform(-0.35, 0.35),
                    1.7 - row * 1.5 + rng.uniform(-0.2, 0.2), 0]))
                self.cloud.add(label)
            caption = serif("twenty unrelated topics?", BODY_SIZE, GREY)
            caption.to_edge(DOWN, buff=GAP_MD)
            self.play(Write(self.cloud), run_time=t.fill(0.45))
            self.play(Write(caption), run_time=t.fill(0.15))
            self.cloud_caption = caption
            t.hold()

        with self.beat("connect") as t:
            links = VGroup()
            for a, b in ((0, 1), (1, 2), (2, 4), (4, 5), (5, 6), (6, 7),
                         (7, 8), (3, 7), (0, 8), (1, 3)):
                links.add(Line(self.cloud[a].get_center(),
                               self.cloud[b].get_center(),
                               color=SLATE, stroke_width=2, stroke_opacity=0.7,
                               buff=GAP_SM * 1.2))
            new_caption = serif("see how they connect", BODY_SIZE, TERRACOTTA)
            new_caption.move_to(self.cloud_caption)
            self.play(Create(links), run_time=t.fill(0.4))
            self.play(FadeOut(self.cloud_caption), Write(new_caption),
                      run_time=t.fill(0.15))
            t.hold()

        with self.beat("one_story") as t:
            self.clear_all(t)
            claim = lines("It is not a collection of chapters.",
                          size=TITLE_SIZE, color=GREY)
            claim.move_to(UP * 0.9)
            story = serif("It is one story.", TITLE_SIZE * 1.5, TERRACOTTA)
            story.next_to(claim, DOWN, buff=GAP_LG)
            note = lines("and a subject that looks complicated",
                         "becomes surprisingly logical",
                         size=LABEL_SIZE, color=GREY)
            note.next_to(story, DOWN, buff=GAP_LG)
            self.play(Write(claim), run_time=t.fill(0.2))
            self.play(Write(story), run_time=t.fill(0.25))
            self.play(Write(note), run_time=t.fill(0.2))
            t.hold()

        with self.beat("three_rules_tease") as t:
            self.clear_all(t)
            self.set_head(t, "Three rules for every student on this course")
            slots = lines("1", "2", "3", size=TITLE_SIZE, color=GREY,
                          buff=GAP_MD * 1.1, align=LEFT)
            self.below_head(slots)
            note = serif("we come back to these at the end",
                         BODY_SIZE, GREY)
            note.to_edge(DOWN, buff=GAP_MD * 1.2)
            gain = serif("follow them and you never have to "
                         "blindly memorise notes", BODY_SIZE, TERRACOTTA)
            fit(gain)
            gain.next_to(slots, DOWN, buff=GAP_LG)
            self.play(Write(slots), run_time=t.fill(0.2))
            self.play(Write(gain), run_time=t.fill(0.25))
            self.play(Write(note), run_time=t.fill(0.12))
            t.hold()

    def what_it_is(self):
        with self.beat("not_about_computers") as t:
            self.clear_all(t)
            claim = lines("Computer science is not really",
                          "about computers.", size=TITLE_SIZE * 1.2)
            claim.move_to(UP * 0.7)
            note = serif("a computer is simply the machine we happen to use",
                         BODY_SIZE, GREY)
            fit(note)
            note.next_to(claim, DOWN, buff=GAP_LG)
            self.play(Write(claim), run_time=t.fill(0.35))
            self.play(Write(note), run_time=t.fill(0.2))
            t.hold()

        with self.beat("about_information") as t:
            self.clear_all(t)
            head = serif("It is about INFORMATION", TITLE_SIZE * 1.2,
                         TERRACOTTA)
            head.to_edge(UP, buff=GAP_MD * 1.9)
            self.section_head = head
            self.play(Write(head), run_time=t.fill(0.15))
            self.info_questions = self.bullets(t, [
                "How do we represent it?",
                "How do we store it?",
                "How do we move it?",
                "How do we protect it?",
                "How do we make decisions with it?",
            ], per=0.11)
            t.hold()

        with self.beat("break_problem") as t:
            last = lines("How do we break a complicated problem",
                         "into steps a machine can follow?",
                         size=BODY_SIZE, color=TERRACOTTA, align=LEFT)
            last.next_to(self.info_questions, DOWN, buff=GAP_MD * 1.3)
            last.align_to(self.info_questions, LEFT)
            self.play(Write(last), run_time=t.fill(0.3))
            self.play(Create(self.underline(last)), run_time=t.fill(0.12))
            t.hold()

        with self.beat("before_watching") as t:
            self.clear_all(t)
            self.set_head(t, "Before you started watching this lesson")
            self.bullets(t, [
                "you opened a website",
                "you tapped a link",
                "you searched for the course",
            ], per=0.12)
            simple = serif("it looks simple", BODY_SIZE, GREY)
            simple.to_edge(DOWN, buff=GAP_LG)
            self.play(Write(simple), run_time=t.fill(0.15))
            t.hold()

        with self.beat("underneath") as t:
            self.clear_all(t)
            self.set_head(t, "Underneath, all of this happened",
                          color=TERRACOTTA)
            layers = lines(
                "your device represented information in binary",
                "your network divided it into packets",
                "packets travelled across a network",
                "routers found their destination",
                "security systems protected the communication",
                "processors executed instructions",
                "software controlled the hardware",
                "pixels and sound produced this lesson",
                size=LABEL_SIZE, color=CHARCOAL, buff=GAP_SM, align=LEFT)
            self.below_head(layers, buff=GAP_MD)
            for layer in layers:
                self.play(Write(layer), run_time=t.fill(0.075))
            t.hold()

        with self.beat("pressed_play") as t:
            self.clear_all(t)
            said = serif("You simply pressed play.", TITLE_SIZE * 1.2, GREY)
            said.move_to(UP * 1.5)
            law = lines("the easier technology becomes for the user,",
                        "the more complicated the systems underneath",
                        size=TITLE_SIZE * 0.95, color=CHARCOAL)
            law.move_to(DOWN * 0.1)
            going = serif("and on this course, we are going underneath",
                          BODY_SIZE, TERRACOTTA)
            fit(going)
            going.next_to(law, DOWN, buff=GAP_LG)
            self.play(Write(said), run_time=t.fill(0.2))
            self.play(Write(law), run_time=t.fill(0.3))
            self.play(Write(going), run_time=t.fill(0.2))
            t.hold()

        with self.beat("dont_memorise") as t:
            self.clear_all(t)
            rule = lines("Don't memorise the machine.",
                         "Understand the system.",
                         size=TITLE_SIZE * 1.3)
            rule.move_to(UP * 0.6)
            rule[1].set_color(TERRACOTTA)
            tag = serif("the first principle of this course",
                        BODY_SIZE, GREY)
            tag.next_to(rule, DOWN, buff=GAP_LG)
            self.play(Write(rule), run_time=t.fill(0.35))
            self.play(Write(tag), run_time=t.fill(0.15))
            t.hold()

    def school_case(self):
        with self.beat("school_problem") as t:
            self.clear_all(t)
            self.set_head(t, "A school with two thousand students")
            self.bullets(t, [
                "calculate grades",
                "identify students who need support",
                "produce reports for parents",
                "keep the information secure",
                "let teachers reach the right records",
            ], per=0.09)
            choice = serif("employ hundreds of people — or design a system",
                           BODY_SIZE, TERRACOTTA)
            fit(choice)
            choice.to_edge(DOWN, buff=GAP_LG)
            self.play(Write(choice), run_time=t.fill(0.22))
            t.hold()

        with self.beat("data") as t:
            self.clear_all(t)
            self.daps = self.arc(t, DAPS, 0, fraction=0.14,
                                 size=LABEL_SIZE * 1.1)
            self.set_head(t, "What information do we need?", fraction=0.1)
            self.bullets(t, [
                "student name · student ID",
                "subject · marks · grade",
            ], per=0.14)
            t.hold()

        with self.beat("algorithm") as t:
            old = [m for m in self.mobjects
                   if m not in self.persistent and m is not self.daps]
            self.play(*[FadeOut(m) for m in old], *self.daps.focus(1),
                      run_time=t.fill(0.09))
            self.section_head = None
            self.set_head(t, "How is it stored, and by what rules?",
                          fraction=0.1)
            self.bullets(t, [
                "store the data in a database",
                "if the mark is above this value, assign this grade",
                "if it is below that value, assign another",
            ], per=0.13)
            t.hold()

        with self.beat("program") as t:
            old = [m for m in self.mobjects
                   if m not in self.persistent and m is not self.daps]
            self.play(*[FadeOut(m) for m in old], *self.daps.focus(2),
                      run_time=t.fill(0.1))
            self.section_head = None
            step = lines("instructions a computer can execute",
                         size=TITLE_SIZE)
            step.move_to(UP * 0.4)
            self.play(Write(step), run_time=t.fill(0.35))
            t.hold()

        with self.beat("system") as t:
            old = [m for m in self.mobjects
                   if m not in self.persistent and m is not self.daps]
            self.play(*[FadeOut(m) for m in old], *self.daps.focus(3),
                      run_time=t.fill(0.08))
            self.section_head = None
            self.set_head(t, "Now thousands of people use it", fraction=0.09)
            ring = VGroup(*[box(name, 3.7, 0.9, SLATE, LABEL_SIZE)
                            for name in ("hardware", "networks", "security",
                                         "storage", "software", "backup",
                                         "authentication")])
            ring.arrange_in_grid(rows=3, buff=(GAP_SM * 1.4, GAP_SM * 1.4))
            fit(ring, 12.2)
            self.below_head(ring, buff=GAP_MD)
            self.play(FadeIn(ring), run_time=t.fill(0.3))
            t.hold()

        with self.beat("daps") as t:
            self.clear_all(t)
            big = WordArc(DAPS, size=TITLE_SIZE, dim=CHARCOAL,
                          lit=TERRACOTTA)
            big.move_to(UP * 0.4)
            note = serif("a computer scientist thinks across all four",
                         BODY_SIZE, TERRACOTTA)
            fit(note)
            note.next_to(big, DOWN, buff=GAP_LG)
            self.play(Write(big), run_time=t.fill(0.3))
            self.play(Write(note), run_time=t.fill(0.2))
            t.hold()

    def papers(self):
        with self.beat("two_worlds") as t:
            self.clear_all(t)
            left = VGroup(
                serif("World one", TITLE_SIZE, TERRACOTTA),
                serif("how computers work", BODY_SIZE, CHARCOAL),
                serif("computer systems", LABEL_SIZE, GREY),
            ).arrange(DOWN, buff=GAP_MD)
            right = VGroup(
                serif("World two", TITLE_SIZE, SLATE),
                serif("how we make computers", BODY_SIZE, CHARCOAL),
                serif("solve problems", BODY_SIZE, CHARCOAL),
                serif("algorithms, programming, logic", LABEL_SIZE, GREY),
            ).arrange(DOWN, buff=GAP_MD)
            panels = VGroup(left, right).arrange(RIGHT, buff=GAP_LG * 1.4,
                                                 aligned_edge=UP)
            fit(panels)
            panels.move_to(UP * 0.3)
            divider = Line(panels.get_top() + UP * GAP_SM,
                           panels.get_bottom() + DOWN * GAP_SM,
                           color=GREY, stroke_width=2)
            divider.move_to([panels.get_center()[0], divider.get_center()[1],
                             0])
            tested = serif("Cambridge tests the two worlds separately",
                           BODY_SIZE, GREY)
            tested.to_edge(DOWN, buff=GAP_MD * 1.2)
            self.play(Write(left), run_time=t.fill(0.2))
            self.play(Create(divider), run_time=t.fill(0.08))
            self.play(Write(right), run_time=t.fill(0.2))
            self.play(Write(tested), run_time=t.fill(0.15))
            t.hold()

        with self.beat("paper1") as t:
            self.clear_all(t)
            self.set_head(t, "Paper 1  ·  Computer Systems",
                          color=TERRACOTTA)
            self.bullets(t, [
                "1 hour 45 minutes",
                "75 marks",
                "50% of the qualification",
                "topics 1 to 6",
                "all questions compulsory",
                "no calculator",
            ], per=0.1)
            t.hold()

        with self.beat("paper2") as t:
            self.clear_all(t)
            self.set_head(t, "Paper 2  ·  Algorithms, Programming and Logic",
                          color=TERRACOTTA)
            self.bullets(t, [
                "1 hour 45 minutes",
                "75 marks",
                "50% of the qualification",
                "topics 7 to 10",
                "all questions compulsory",
                "no calculator",
            ], per=0.1)
            t.hold()

        with self.beat("scenario") as t:
            self.clear_all(t)
            self.set_head(t, "But Paper 2 ends with something Paper 1 has not")
            card = VGroup(
                serif("a scenario-based programming question",
                      BODY_SIZE, CHARCOAL),
                serif("worth 15 marks", TITLE_SIZE, TERRACOTTA),
                serif("Cambridge expects roughly 30 minutes on it",
                      LABEL_SIZE, GREY),
            ).arrange(DOWN, buff=GAP_MD)
            fit(card)
            self.below_head(card)
            frame = Rectangle(width=card.width + GAP_LG,
                              height=card.height + GAP_MD * 1.6,
                              color=SLATE, stroke_width=3).move_to(card)
            emphasis = serif("marked on the logic of the solution, "
                             "not memorised syntax", BODY_SIZE, SLATE)
            fit(emphasis)
            emphasis.to_edge(DOWN, buff=GAP_LG)
            self.play(Create(frame), run_time=t.fill(0.12))
            self.play(Write(card), run_time=t.fill(0.3))
            self.play(Write(emphasis), run_time=t.fill(0.22))
            t.hold()

        with self.beat("fifty_fifty") as t:
            self.clear_all(t)
            bar = VGroup(
                box("Paper 1     50%", 5.6, 1.3, SLATE, TITLE_SIZE),
                box("Paper 2     50%", 5.6, 1.3, SLATE, TITLE_SIZE),
            ).arrange(RIGHT, buff=0)
            fit(bar, 11.6)
            bar.move_to(UP * 0.5)
            warn = serif("ignore one half and you give away "
                         "half the qualification", BODY_SIZE, TERRACOTTA)
            fit(warn)
            warn.next_to(bar, DOWN, buff=GAP_LG)
            self.play(Create(bar), run_time=t.fill(0.3))
            self.play(Write(warn), run_time=t.fill(0.25))
            t.hold()

    def paper_one_topics(self):
        with self.beat("the_map") as t:
            self.clear_all(t)
            # One column, not two: the real syllabus titles are long enough
            # that side-by-side columns only fit by shrinking the text below
            # the legibility floor.
            self.map = SyllabusMap([
                ("Paper 1 · Computer Systems", TOPICS_P1),
                ("Paper 2 · Algorithms, Programming and Logic", TOPICS_P2),
            ], size=LABEL_SIZE, head_size=LABEL_SIZE, stacked=True)
            self.map.move_to(DOWN * 0.15)
            note = lines("don't try to memorise this list —",
                         "just see the shape of the journey",
                         size=BODY_SIZE, color=GREY)
            self.play(Write(note), run_time=t.fill(0.2))
            self.play(FadeOut(note), FadeIn(self.map), run_time=t.fill(0.25))
            t.hold()

        with self.beat("paper1_topics") as t:
            self.play(*self.map.focus_range(0, 6), run_time=t.fill(0.25))
            t.hold()

        with self.beat("topic1") as t:
            self.topic_frame(t, 0, "How does a computer represent the world?")
            row = chain(["letter", "photograph", "music"], 3.0, 1.0)
            gap = serif("the computer sees none of these",
                        BODY_SIZE, GREY)
            binary = serif("0  1", TITLE_SIZE * 1.8, TERRACOTTA)
            begins = serif("this is where our journey begins",
                           LABEL_SIZE, GREY)
            self.column([row, gap, binary, begins], self.section_head)
            self.play(Create(row), run_time=t.fill(0.2))
            self.play(Write(gap), run_time=t.fill(0.14))
            self.play(Write(binary), run_time=t.fill(0.16))
            self.play(Write(begins), run_time=t.fill(0.12))
            t.hold()

        with self.beat("topic2") as t:
            self.topic_frame(t, 1, "Now the data has to travel.")
            packets = VGroup(*[box(f"packet {i}", 2.2, 0.8, SLATE)
                               for i in range(1, 5)])
            packets.arrange(RIGHT, buff=GAP_SM)
            fit(packets)
            needs = lines("each packet carries addressing information",
                          "errors happen — data can be corrupted",
                          "messages can fail to arrive",
                          "so we need error detection and recovery",
                          size=LABEL_SIZE, color=CHARCOAL, buff=GAP_SM,
                          align=LEFT)
            secure = serif("and if somebody intercepts it — encryption",
                           BODY_SIZE, TERRACOTTA)
            self.column([packets, needs, secure], self.section_head)
            self.play(Create(packets), run_time=t.fill(0.14))
            for need in needs:
                self.play(Write(need), run_time=t.fill(0.08))
            self.play(Write(secure), run_time=t.fill(0.14))
            t.hold()

        with self.beat("topic3") as t:
            self.topic_frame(t, 2, "Now we meet the machine itself.")
            parts = VGroup(*[box(name, 2.8, 0.85, SLATE, LABEL_SIZE)
                             for name in ("CPU", "memory", "storage",
                                          "input", "output", "sensors")])
            parts.arrange_in_grid(rows=2, buff=(GAP_SM * 1.3, GAP_SM * 1.3))
            fit(parts, 11.0)
            cycle = chain(["Fetch", "Decode", "Execute"], 2.6, 0.9,
                          color=TERRACOTTA)
            extras = serif("registers · why cache exists · RAM vs storage",
                           LABEL_SIZE, GREY)
            self.column([parts, cycle, extras], self.section_head)
            self.play(FadeIn(parts), run_time=t.fill(0.18))
            self.play(Create(cycle), run_time=t.fill(0.2))
            self.play(Write(extras), run_time=t.fill(0.14))
            t.hold()

        with self.beat("topic4") as t:
            self.topic_frame(t, 3)
            claim = serif("hardware without software is expensive "
                          "electronics", BODY_SIZE, GREY)
            fit(claim)
            bridge = chain(["human", "software", "machine"], 3.2, 1.0,
                           color=TERRACOTTA)
            items = lines("operating systems · utilities · languages",
                          "compilers · interpreters · interrupts",
                          size=LABEL_SIZE, color=GREY)
            self.column([claim, bridge, items], self.section_head)
            self.play(Write(claim), run_time=t.fill(0.18))
            self.play(Create(bridge), run_time=t.fill(0.2))
            self.play(Write(items), run_time=t.fill(0.18))
            t.hold()

        with self.beat("topic5") as t:
            self.topic_frame(t, 4,
                             "Could you explain what happens after you "
                             "type an address?")
            asks = lines("internet or World Wide Web?",
                         "what does DNS do?",
                         "what is a URL?",
                         "why do websites use cookies?",
                         size=LABEL_SIZE, color=CHARCOAL, buff=GAP_SM,
                         align=LEFT)
            threats = VGroup(*[box(name, 2.8, 0.85, TERRACOTTA, LABEL_SIZE)
                               for name in ("phishing", "pharming",
                                            "malware")])
            threats.arrange(RIGHT, buff=GAP_SM * 1.3)
            fit(threats)
            defend = serif("and how do we defend ourselves?",
                           BODY_SIZE, GREY)
            self.column([asks, threats, defend], self.section_head)
            for ask in asks:
                self.play(Write(ask), run_time=t.fill(0.07))
            self.play(Create(threats), run_time=t.fill(0.16))
            self.play(Write(defend), run_time=t.fill(0.12))
            t.hold()

        with self.beat("topic6") as t:
            self.topic_frame(t, 5)
            items = VGroup(*[box(name, 5.2, 0.85, SLATE, LABEL_SIZE)
                             for name in ("sensors", "microprocessors",
                                          "actuators", "automated systems",
                                          "robotics",
                                          "artificial intelligence")])
            items.arrange_in_grid(rows=3, buff=(GAP_SM * 1.3, GAP_SM * 1.3))
            fit(items, 12.2)
            note = serif("machines that interact with the world around them",
                         BODY_SIZE, TERRACOTTA)
            fit(note)
            self.column([items, note], self.section_head)
            self.play(FadeIn(items), run_time=t.fill(0.3))
            self.play(Write(note), run_time=t.fill(0.22))
            t.hold()

        with self.beat("sense_process_act") as t:
            self.clear_all(t)
            self.set_head(t, "An automated system", fraction=0.07)
            story = lines("a temperature sensor detects heat",
                          "a processor makes a decision",
                          "an actuator turns something on",
                          "the environment changes — and we measure again",
                          size=LABEL_SIZE, color=CHARCOAL, align=LEFT)
            loop = WordArc(SPAR, size=TITLE_SIZE, dim=CHARCOAL,
                           lit=TERRACOTTA)
            done = serif("that completes world one: computer systems",
                         BODY_SIZE, GREY)
            self.column([story, loop, done], self.section_head)
            for step in story:
                self.play(Write(step), run_time=t.fill(0.08))
            self.play(Write(loop), run_time=t.fill(0.2))
            self.play(Write(done), run_time=t.fill(0.14))
            t.hold()

    def paper_two_topics(self):
        with self.beat("world_two") as t:
            self.clear_all(t)
            self.set_head(t, "World two  ·  Algorithms, Programming, Logic",
                          color=TERRACOTTA)
            four = lines("7   Algorithm design and problem-solving",
                         "8   Programming",
                         "9   Databases",
                         "10  Boolean logic",
                         size=BODY_SIZE, color=CHARCOAL, align=LEFT)
            self.below_head(four)
            self.play(Write(four), run_time=t.fill(0.35))
            self.play(*self.strip.focus(6), run_time=t.fill(0.1))
            t.hold()

        with self.beat("not_programming_first") as t:
            self.clear_all(t)
            self.set_head(t, "We do not begin with programming")
            bad = serif("a weak programmer starts typing immediately",
                        BODY_SIZE, GREY)
            good = lines("a good programmer asks",
                         size=BODY_SIZE, color=TERRACOTTA)
            asks = lines("what exactly is the problem?",
                         "what information goes in?",
                         "what result comes out?",
                         "what processing is required?",
                         "can I break it into smaller pieces?",
                         size=LABEL_SIZE, color=CHARCOAL,
                         buff=GAP_SM, align=LEFT)
            only = serif("only then do we think about code",
                         BODY_SIZE, SLATE)
            self.column([bad, good, asks, only], self.section_head)
            self.play(Write(bad), run_time=t.fill(0.16))
            self.play(Write(good), run_time=t.fill(0.12))
            self.play(Write(asks), run_time=t.fill(0.28))
            self.play(Write(only), run_time=t.fill(0.15))
            t.hold()

        with self.beat("problem_plan") as t:
            self.clear_all(t)
            arc = WordArc(PPACT, size=TITLE_SIZE * 0.95,
                          dim=CHARCOAL, lit=TERRACOTTA)
            arc.move_to(UP * 0.3)
            note = serif("this sequence follows us through all of Paper 2",
                         BODY_SIZE, GREY)
            fit(note)
            note.next_to(arc, DOWN, buff=GAP_LG)
            self.play(Write(arc), run_time=t.fill(0.35))
            self.play(Write(note), run_time=t.fill(0.2))
            t.hold()

        with self.beat("topic7") as t:
            self.topic_frame(t, 6)
            defn = serif("a precise sequence of instructions "
                         "for solving a problem", BODY_SIZE, CHARCOAL)
            fit(defn)
            weak = serif('"make tea"', TITLE_SIZE, GREY)
            asks = lines("what kind of tea?  how much water?",
                         "when do I boil it?  when do I add the tea?",
                         "how long do I wait?",
                         size=LABEL_SIZE, color=TERRACOTTA)
            self.column([defn, weak, asks], self.section_head)
            self.play(Write(defn), run_time=t.fill(0.2))
            self.play(Write(weak), run_time=t.fill(0.12))
            self.play(Write(asks), run_time=t.fill(0.25))
            t.hold()

        with self.beat("literal") as t:
            self.clear_all(t)
            panels = VGroup(
                lines("a human being", "can guess what you meant",
                      size=BODY_SIZE, color=GREY),
                lines("a computer", "cannot",
                      size=BODY_SIZE, color=CHARCOAL),
            ).arrange(RIGHT, buff=GAP_LG * 1.6, aligned_edge=UP)
            fit(panels)
            panels.move_to(UP * 0.6)
            rule = serif("so our instructions must be precise",
                         TITLE_SIZE, TERRACOTTA)
            fit(rule)
            rule.next_to(panels, DOWN, buff=GAP_LG)
            self.play(Write(panels), run_time=t.fill(0.35))
            self.play(Write(rule), run_time=t.fill(0.22))
            t.hold()

        with self.beat("topic7_tools") as t:
            self.clear_all(t)
            self.set_head(t, "The tools of topic 7", fraction=0.07)
            tools = VGroup(*[box(name, 3.6, 0.8, SLATE, LABEL_SIZE)
                             for name in ("pseudocode", "flowcharts",
                                          "trace tables", "validation",
                                          "verification", "test data",
                                          "searching", "sorting",
                                          "decomposition")])
            tools.arrange_in_grid(rows=3, buff=(GAP_SM * 1.2, GAP_SM * 1.2))
            fit(tools, 12.2)
            expect = serif("not just recognise algorithms — "
                           "write and amend them", BODY_SIZE, TERRACOTTA)
            fit(expect)
            self.column([tools, expect], self.section_head)
            self.play(FadeIn(tools), run_time=t.fill(0.3))
            self.play(Write(expect), run_time=t.fill(0.22))
            t.hold()

        with self.beat("topic8") as t:
            self.topic_frame(t, 7, "Thinking, turned into something "
                                   "executable.")
            words = VGroup(*[box(name, 2.6, 0.75, SLATE, LABEL_SIZE)
                             for name in ("variables", "constants",
                                          "data types", "input", "output",
                                          "selection", "loops", "strings",
                                          "procedures", "functions",
                                          "arrays", "files")])
            words.arrange_in_grid(rows=3, buff=(GAP_SM * 1.1, GAP_SM * 1.1))
            fit(words, 11.5)
            promise = serif("intimidating now — ordinary by the end "
                            "of this course", BODY_SIZE, TERRACOTTA)
            fit(promise)
            self.column([words, promise], self.section_head)
            self.play(FadeIn(words), run_time=t.fill(0.3))
            self.play(Write(promise), run_time=t.fill(0.2))
            t.hold()

        with self.beat("loop_selection") as t:
            self.clear_all(t)
            self.set_head(t, "You already understand this", fraction=0.06)
            left = VGroup(
                serif("write this sentence", LABEL_SIZE, CHARCOAL),
                serif("ten times", LABEL_SIZE, CHARCOAL),
                serif("repetition", BODY_SIZE, GREY),
                serif("a LOOP", TITLE_SIZE, TERRACOTTA),
            ).arrange(DOWN, buff=GAP_SM * 1.4)
            right = VGroup(
                serif("if your mark is at least 80,", LABEL_SIZE, CHARCOAL),
                serif("display A", LABEL_SIZE, CHARCOAL),
                serif("choosing", BODY_SIZE, GREY),
                serif("SELECTION", TITLE_SIZE, TERRACOTTA),
            ).arrange(DOWN, buff=GAP_SM * 1.4)
            panels = VGroup(left, right).arrange(RIGHT, buff=GAP_LG * 1.2,
                                                 aligned_edge=UP)
            fit(panels)
            claim = lines("programming is logical ideas humans already have,",
                          "expressed precisely enough for a computer",
                          size=BODY_SIZE, color=SLATE)
            self.column([panels, claim], self.section_head)
            self.play(Write(left), run_time=t.fill(0.2))
            self.play(Write(right), run_time=t.fill(0.2))
            self.play(Write(claim), run_time=t.fill(0.25))
            t.hold()

        with self.beat("topic9") as t:
            self.topic_frame(t, 8, "Modern life generates enormous "
                                   "amounts of information.")
            who = lines("schools · hospitals · banks",
                        "airlines · governments · online stores",
                        size=LABEL_SIZE, color=GREY)
            learn = VGroup(*[box(name, 2.8, 0.85, SLATE, LABEL_SIZE)
                             for name in ("fields", "records", "data types",
                                          "primary keys", "SQL")])
            learn.arrange_in_grid(rows=2, buff=(GAP_SM * 1.3, GAP_SM * 1.3))
            fit(learn, 10.5)
            needle = serif("instead of searching for a needle in a haystack",
                           BODY_SIZE, TERRACOTTA)
            fit(needle)
            self.column([who, learn, needle], self.section_head)
            self.play(Write(who), run_time=t.fill(0.14))
            self.play(FadeIn(learn), run_time=t.fill(0.18))
            self.play(Write(needle), run_time=t.fill(0.16))
            t.hold()

        with self.beat("topic10") as t:
            self.topic_frame(t, 9)
            values = serif("true   false   1   0", TITLE_SIZE * 1.2,
                           CHARCOAL)
            gates = serif("AND   OR   NOT   NAND   NOR   XOR",
                          TITLE_SIZE, TERRACOTTA)
            fit(gates)
            tables = serif("and truth tables", BODY_SIZE, GREY)
            self.column([values, gates, tables], self.section_head)
            self.play(Write(values), run_time=t.fill(0.2))
            self.play(Write(gates), run_time=t.fill(0.22))
            self.play(Write(tables), run_time=t.fill(0.14))
            t.hold()

        with self.beat("simple_combined") as t:
            self.clear_all(t)
            self.play(FadeOut(self.strip), run_time=t.fill(0.05))
            self.persistent.remove(self.strip)
            top = lines("computers look fantastically complicated",
                        size=TITLE_SIZE, color=GREY)
            top.move_to(UP * 1.6)
            under = lines("underneath: billions of very simple",
                          "logical decisions",
                          size=TITLE_SIZE)
            under.move_to(UP * 0.1)
            pair = serif("true or false   ·   one or zero",
                         BODY_SIZE, TERRACOTTA)
            pair.next_to(under, DOWN, buff=GAP_MD * 1.4)
            law = lines("take something simple, combine it,",
                        "and something extraordinary emerges",
                        size=LABEL_SIZE, color=SLATE)
            law.to_edge(DOWN, buff=GAP_MD * 1.4)
            self.play(Write(top), run_time=t.fill(0.18))
            self.play(Write(under), run_time=t.fill(0.2))
            self.play(Write(pair), run_time=t.fill(0.14))
            self.play(Write(law), run_time=t.fill(0.2))
            t.hold()

    def skills(self):
        with self.beat("three_skills") as t:
            self.clear_all(t)
            self.set_head(t, "Knowing the syllabus is not enough",
                          fraction=0.06)
            note = serif("Cambridge divides assessment into three "
                         "objectives", BODY_SIZE, GREY)
            fit(note)
            self.below_head(note, buff=GAP_MD)
            self.kaj = WordArc(KAJ, size=TITLE_SIZE * 1.3, arrow="·",
                               dim=CHARCOAL, lit=TERRACOTTA)
            self.kaj.next_to(note, DOWN, buff=GAP_LG)
            plain = serif("three ordinary words", LABEL_SIZE, GREY)
            plain.next_to(self.kaj, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(note), run_time=t.fill(0.15))
            self.play(Write(self.kaj), run_time=t.fill(0.3))
            self.play(Write(plain), run_time=t.fill(0.15))
            t.hold()

        with self.beat("know") as t:
            old = [m for m in self.mobjects
                   if m not in self.persistent and m is not self.kaj]
            self.play(*[FadeOut(m) for m in old],
                      self.kaj.animate.to_edge(UP, buff=GAP_MD * 1.2),
                      run_time=t.fill(0.09))
            self.play(*self.kaj.focus(0), run_time=t.fill(0.05))
            self.section_head = self.kaj
            tag = serif("AO1  ·  demonstrate knowledge and understanding",
                        BODY_SIZE, SLATE)
            fit(tag)
            self.below_head(tag, buff=GAP_MD * 1.2)
            asks = lines("what is RAM?", "what is phishing?",
                         "what is a MAC address?", "what is a compiler?",
                         size=LABEL_SIZE, color=CHARCOAL, align=LEFT)
            asks.next_to(tag, DOWN, buff=GAP_MD * 1.2)
            limit = serif("knowledge alone does not produce the "
                          "highest marks", BODY_SIZE, TERRACOTTA)
            fit(limit)
            limit.to_edge(DOWN, buff=GAP_MD * 1.2)
            self.play(Write(tag), run_time=t.fill(0.14))
            self.play(Write(asks), run_time=t.fill(0.2))
            self.play(Write(limit), run_time=t.fill(0.16))
            t.hold()

        with self.beat("apply") as t:
            old = [m for m in self.mobjects
                   if m not in self.persistent and m is not self.kaj]
            self.play(*[FadeOut(m) for m in old], *self.kaj.focus(1),
                      run_time=t.fill(0.08))
            self.section_head = self.kaj
            tag = serif("AO2  ·  use what you know in a situation "
                        "you haven't memorised", BODY_SIZE, SLATE)
            fit(tag)
            self.below_head(tag, buff=GAP_MD * 1.2)
            story = lines("Cambridge describes a security system "
                          "in a warehouse",
                          "you have never seen that exact system",
                          size=LABEL_SIZE, color=GREY)
            story.next_to(tag, DOWN, buff=GAP_MD * 1.2)
            have = chain(["sensors", "processors", "actuators"], 3.0, 0.9,
                         color=TERRACOTTA)
            have.next_to(story, DOWN, buff=GAP_MD * 1.2)
            ask = serif("can you apply those ideas?", BODY_SIZE, CHARCOAL)
            ask.next_to(have, DOWN, buff=GAP_MD * 1.2)
            self.play(Write(tag), run_time=t.fill(0.16))
            self.play(Write(story), run_time=t.fill(0.16))
            self.play(Create(have), run_time=t.fill(0.16))
            self.play(Write(ask), run_time=t.fill(0.12))
            t.hold()

        with self.beat("weightings") as t:
            old = [m for m in self.mobjects
                   if m not in self.persistent and m is not self.kaj]
            self.play(*[FadeOut(m) for m in old], *self.kaj.dim_all(),
                      run_time=t.fill(0.07))
            self.section_head = self.kaj
            # The widths carry the weighting, so the labels sit underneath
            # rather than being squeezed inside a 20%-wide box.
            bar = VGroup(
                Rectangle(width=4.4, height=1.0, color=SLATE,
                          stroke_width=3),
                Rectangle(width=4.4, height=1.0, color=SLATE,
                          stroke_width=3),
                Rectangle(width=2.2, height=1.0, color=SLATE,
                          stroke_width=3),
            ).arrange(RIGHT, buff=0)
            self.below_head(bar, buff=GAP_MD * 1.4)
            rects = list(bar)
            for rect, text in zip(rects, ("AO1  40%", "AO2  40%",
                                          "AO3  20%")):
                label = serif(text, LABEL_SIZE, CHARCOAL)
                label.next_to(rect, DOWN, buff=GAP_SM * 0.8)
                bar.add(label)
            lean = lines("Paper 1 leans on AO1     Paper 2 leans on AO2",
                         size=BODY_SIZE, color=GREY)
            lean.next_to(bar, DOWN, buff=GAP_MD * 1.3)
            plain = lines("Paper 1 asks: what do you know?",
                          "Paper 2 asks: what can you do with it?",
                          size=BODY_SIZE, color=TERRACOTTA)
            plain.next_to(lean, DOWN, buff=GAP_MD * 1.3)
            self.play(Create(bar), run_time=t.fill(0.2))
            self.play(Write(lean), run_time=t.fill(0.18))
            self.play(Write(plain), run_time=t.fill(0.25))
            t.hold()

        with self.beat("judge") as t:
            old = [m for m in self.mobjects
                   if m not in self.persistent and m is not self.kaj]
            self.play(*[FadeOut(m) for m in old], *self.kaj.focus(2),
                      run_time=t.fill(0.08))
            self.section_head = self.kaj
            tag = serif("AO3  ·  evaluate, reason, conclude",
                        BODY_SIZE, SLATE)
            self.below_head(tag, buff=GAP_MD * 1.2)
            case = lines("a company considers replacing workers",
                         "with an automated system",
                         size=LABEL_SIZE, color=GREY)
            case.next_to(tag, DOWN, buff=GAP_MD * 1.3)
            weak = serif('"automation is good because it is faster"',
                         BODY_SIZE, TERRACOTTA)
            fit(weak)
            weak.next_to(case, DOWN, buff=GAP_MD * 1.3)
            verdict = serif("that is not enough", BODY_SIZE, CHARCOAL)
            verdict.next_to(weak, DOWN, buff=GAP_MD * 1.1)
            self.play(Write(tag), run_time=t.fill(0.14))
            self.play(Write(case), run_time=t.fill(0.16))
            self.play(Write(weak), run_time=t.fill(0.16))
            self.play(Write(verdict), run_time=t.fill(0.12))
            t.hold()

        with self.beat("evaluation_chain") as t:
            self.clear_all(t)
            self.set_head(t, "A stronger answer asks", fraction=0.06)
            asks = lines("faster in what way?",
                         "what happens to accuracy? to cost? to jobs?",
                         "what if the system fails?",
                         "what about security? who is affected?",
                         "and given this situation, what follows?",
                         size=LABEL_SIZE, color=CHARCOAL, align=LEFT)
            self.below_head(asks, buff=GAP_MD)
            arc = WordArc(CRCC, size=TITLE_SIZE * 0.9, dim=CHARCOAL,
                          lit=TERRACOTTA)
            arc.next_to(asks, DOWN, buff=GAP_LG)
            label = serif("that is evaluation", BODY_SIZE, GREY)
            label.next_to(arc, DOWN, buff=GAP_MD * 1.2)
            for ask in asks:
                self.play(Write(ask), run_time=t.fill(0.07))
            self.play(Write(arc), run_time=t.fill(0.2))
            self.play(Write(label), run_time=t.fill(0.12))
            t.hold()

    def traps(self):
        with self.beat("fool") as t:
            self.clear_all(t)
            self.set_head(t, "Computer science can fool students",
                          fraction=0.06)
            steps = lines("you read the chapter — it makes sense",
                          "you read your notes — still makes sense",
                          "you watch a video — yes, I understand that",
                          size=BODY_SIZE, color=GREY, align=LEFT)
            self.below_head(steps, buff=GAP_MD * 1.2)
            then = lines("then you open a past paper —",
                         "and you cannot answer the question",
                         size=BODY_SIZE, color=TERRACOTTA)
            then.next_to(steps, DOWN, buff=GAP_LG)
            for step in steps:
                self.play(Write(step), run_time=t.fill(0.12))
            self.play(Write(then), run_time=t.fill(0.25))
            t.hold()

        with self.beat("recognise_retrieve") as t:
            self.clear_all(t)
            claim = lines("recognising an idea", "is not the same as",
                          "retrieving and applying it",
                          size=TITLE_SIZE * 1.1)
            claim[0].set_color(GREY)
            claim[2].set_color(TERRACOTTA)
            claim.move_to(UP * 0.4)
            note = serif("four habits we are going to avoid",
                         BODY_SIZE, CHARCOAL)
            note.next_to(claim, DOWN, buff=GAP_LG)
            self.play(Write(claim), run_time=t.fill(0.4))
            self.play(Write(note), run_time=t.fill(0.18))
            t.hold()

        self.trap(1, "Memorising without understanding",
                  ["RAM is volatile memory — memorised",
                   "but what does volatile actually mean?",
                   "Cambridge rewords the question, and you are stuck"],
                  "trap1")
        self.trap(2, "Understanding without precision",
                  ['"the router sends internet around"',
                   "roughly right — and worth no marks",
                   "marks are awarded for particular ideas"],
                  "trap2", highlight=0)
        self.trap(3, "Watching without practising",
                  ["you cannot learn to swim by watching swimming videos",
                   "at some point you get into the water",
                   "Cambridge calls this a practical subject",
                   "writing, running, testing and debugging programs"],
                  "trap3")
        self.trap(4, "Waiting until the end to use past papers",
                  ["learn the concept",
                   "learn how Cambridge asks about the concept",
                   "learn how the marks are awarded"],
                  "trap4")

        with self.beat("learn_use") as t:
            self.clear_all(t)
            arc = WordArc(LUEE, size=TITLE_SIZE, dim=CHARCOAL,
                          lit=TERRACOTTA)
            arc.move_to(ORIGIN)
            self.play(Write(arc), run_time=t.fill(0.4))
            t.hold()

    def trap(self, number, title, points, beat_name, highlight=None):
        with self.beat(beat_name) as t:
            self.clear_all(t)
            head = fit(serif(f"Trap {number}  ·  {title}", TITLE_SIZE,
                             TERRACOTTA))
            head.to_edge(UP, buff=GAP_MD * 1.9)
            self.play(Write(head), run_time=t.fill(0.09))
            self.section_head = head
            body = lines(*points, size=BODY_SIZE, color=CHARCOAL,
                         align=LEFT)
            if highlight is not None:
                body[highlight].set_color(GREY)
            self.below_head(body, buff=GAP_MD * 1.5)
            for point in body:
                self.play(Write(point), run_time=t.fill(0.13))
            t.hold()

    def method(self):
        with self.beat("teaching_method") as t:
            self.clear_all(t)
            self.set_head(t, "How we will learn", fraction=0.06)
            steps = lines("begin with a problem, a situation, a story",
                          "then build the idea",
                          "then give the idea its technical name",
                          "then connect it to another idea",
                          "then apply it",
                          "then turn it into examination language",
                          size=BODY_SIZE, color=CHARCOAL, align=LEFT)
            self.below_head(steps, buff=GAP_MD * 1.2)
            not_this = serif("not: definitions thrown onto the screen",
                             LABEL_SIZE, GREY)
            not_this.to_edge(DOWN, buff=GAP_MD * 1.2)
            for step in steps:
                self.play(Write(step), run_time=t.fill(0.1))
            self.play(Write(not_this), run_time=t.fill(0.12))
            t.hold()

        with self.beat("five_steps") as t:
            self.clear_all(t)
            arc = WordArc(UVCAA, size=TITLE_SIZE * 0.85,
                          dim=CHARCOAL, lit=TERRACOTTA)
            arc.move_to(ORIGIN)
            self.play(Write(arc), run_time=t.fill(0.45))
            t.hold()

        with self.beat("packets_example") as t:
            self.clear_all(t)
            self.set_head(t, "An example: what a packet really is",
                          fraction=0.04)
            not_this = lines("not: a packet is a unit of data transmitted "
                             "across a network",
                             size=LABEL_SIZE, color=GREY)
            story = lines("instead: a five-hundred-page book, "
                          "ten pages per envelope",
                          size=BODY_SIZE, color=CHARCOAL)
            problems = lines("we need many envelopes",
                             "we need to know where they are going",
                             "which pages belong in what order?",
                             "one envelope might disappear",
                             "different envelopes take different routes",
                             "somebody has to rebuild the book",
                             size=LABEL_SIZE, color=CHARCOAL,
                             buff=GAP_SM, align=LEFT)
            after = serif("the terminology comes after the mental model",
                          BODY_SIZE, TERRACOTTA)
            self.column([not_this, story, problems, after],
                        self.section_head, floor=-3.5)
            self.play(Write(not_this), run_time=t.fill(0.08))
            self.play(Write(story), run_time=t.fill(0.12))
            for problem in problems:
                self.play(Write(problem), run_time=t.fill(0.07))
            self.play(Write(after), run_time=t.fill(0.12))
            t.hold()

    def programming(self):
        with self.beat("programming_promise") as t:
            self.clear_all(t)
            self.set_head(t, "If you are worried about programming",
                          fraction=0.05)
            fears = lines("perhaps you have never programmed before",
                          "perhaps pseudocode looks like a foreign language",
                          'perhaps you think: I am just not a programmer',
                          size=BODY_SIZE, color=GREY, align=LEFT)
            self.below_head(fears, buff=GAP_MD * 1.3)
            answer = lines("programming is a skill",
                           "and skills improve through deliberate practice",
                           size=TITLE_SIZE * 0.95, color=CHARCOAL)
            answer[1].set_color(TERRACOTTA)
            answer.next_to(fears, DOWN, buff=GAP_LG)
            for fear in fears:
                self.play(Write(fear), run_time=t.fill(0.11))
            self.play(Write(answer), run_time=t.fill(0.3))
            t.hold()

        with self.beat("start_small") as t:
            self.clear_all(t)
            small = lines("store one value",
                          "display one value",
                          "make one decision",
                          "repeat one instruction",
                          size=BODY_SIZE, color=CHARCOAL, align=LEFT)
            small.move_to(UP * 0.4)
            then = serif("then combine them", BODY_SIZE, TERRACOTTA)
            then.next_to(small, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(small), run_time=t.fill(0.35))
            self.play(Write(then), run_time=t.fill(0.2))
            t.hold()

        with self.beat("build_up") as t:
            self.clear_all(t)
            rows = lines("one decision  →  an IF statement",
                         "repetition  →  a loop",
                         "repeated logic  →  a procedure",
                         "many related values  →  an array",
                         "information that must survive  →  a file",
                         size=BODY_SIZE, color=CHARCOAL, align=LEFT)
            rows.move_to(UP * 0.5)
            end = serif("and the small pieces combine into "
                        "a complete solution", BODY_SIZE, TERRACOTTA)
            fit(end)
            end.next_to(rows, DOWN, buff=GAP_LG)
            for row in rows:
                self.play(Write(row), run_time=t.fill(0.12))
            self.play(Write(end), run_time=t.fill(0.18))
            t.hold()

        with self.beat("logic_first") as t:
            self.clear_all(t)
            order = VGroup(
                serif("Logic first.", TITLE_SIZE * 1.4, TERRACOTTA),
                serif("Syntax second.", TITLE_SIZE * 1.4, GREY),
            ).arrange(DOWN, buff=GAP_MD * 1.4)
            order.move_to(UP * 0.7)
            note = lines("we learn how programmers think,",
                         "then how to express that thinking precisely",
                         size=BODY_SIZE, color=CHARCOAL)
            note.next_to(order, DOWN, buff=GAP_LG)
            self.play(Write(order), run_time=t.fill(0.3))
            self.play(Write(note), run_time=t.fill(0.25))
            t.hold()

    def roadmap(self):
        with self.beat("roadmap_q") as t:
            self.clear_all(t)
            below = lines("before databases, before artificial intelligence,",
                          "before cybersecurity, before programming",
                          size=LABEL_SIZE, color=GREY)
            below.to_edge(UP, buff=GAP_LG * 1.2)
            ask = lines("What language does a computer",
                        "actually understand?",
                        size=TITLE_SIZE * 1.1)
            ask.next_to(below, DOWN, buff=GAP_LG)
            self.play(Write(below), run_time=t.fill(0.2))
            self.play(Write(ask), run_time=t.fill(0.3))
            self.roadmap_ask = ask
            t.hold()

        with self.beat("binary") as t:
            answer = serif("0    1", TITLE_SIZE * 2.4, TERRACOTTA)
            answer.next_to(self.roadmap_ask, DOWN, buff=GAP_LG)
            self.play(Write(answer), run_time=t.fill(0.5))
            t.hold()

        with self.beat("roadmap") as t:
            self.clear_all(t)
            outward = lines("binary becomes data",
                            "data becomes text, images and sound",
                            "data travels across networks",
                            "hardware processes it",
                            "software controls the hardware",
                            "networks connect machines",
                            "security protects information",
                            "automated systems touch the physical world",
                            size=LABEL_SIZE, color=CHARCOAL,
                            buff=GAP_SM * 0.7, align=LEFT)
            turn = lines("then we turn it around:",
                         "how do I make the computer solve my problem?",
                         size=BODY_SIZE, color=SLATE)
            arc = WordArc(JOURNEY, size=LABEL_SIZE, rows=2,
                          dim=CHARCOAL, lit=TERRACOTTA)
            self.column([outward, turn, arc], buff=GAP_MD,
                        floor=-3.5).shift(DOWN * GAP_SM)
            for step in outward:
                self.play(Write(step), run_time=t.fill(0.055))
            self.play(Write(turn), run_time=t.fill(0.12))
            self.play(Write(arc), run_time=t.fill(0.2))
            t.hold()

    def rules(self):
        with self.beat("rule1") as t:
            self.clear_all(t)
            head = fit(serif("Rule 1  ·  Ask why", TITLE_SIZE, TERRACOTTA))
            head.to_edge(UP, buff=GAP_MD * 1.9)
            self.play(Write(head), run_time=t.fill(0.1))
            self.section_head = head
            whys = lines("Why binary?   Why packets?   Why cache?",
                         "Why encryption?   Why validation?   Why loops?",
                         size=BODY_SIZE, color=CHARCOAL)
            self.below_head(whys, buff=GAP_MD * 1.6)
            turn = serif("the word why turns facts into understanding",
                         BODY_SIZE, SLATE)
            fit(turn)
            turn.next_to(whys, DOWN, buff=GAP_LG)
            self.play(Write(whys), run_time=t.fill(0.3))
            self.play(Write(turn), run_time=t.fill(0.2))
            t.hold()

        with self.beat("rule2") as t:
            self.clear_all(t)
            head = fit(serif("Rule 2  ·  Connect everything", TITLE_SIZE,
                             TERRACOTTA))
            head.to_edge(UP, buff=GAP_MD * 1.9)
            self.play(Write(head), run_time=t.fill(0.07))
            self.section_head = head
            links = lines("hexadecimal  →  MAC addresses",
                          "sensors  →  automated systems",
                          "Boolean logic  →  programming",
                          "file handling  →  data",
                          "cybersecurity  →  networks",
                          size=BODY_SIZE, color=CHARCOAL, align=LEFT)
            self.below_head(links, buff=GAP_MD * 1.4)
            gain = serif("connect two ideas and both become "
                         "easier to remember", BODY_SIZE, SLATE)
            fit(gain)
            gain.to_edge(DOWN, buff=GAP_MD * 1.2)
            for link in links:
                self.play(Write(link), run_time=t.fill(0.11))
            self.play(Write(gain), run_time=t.fill(0.16))
            t.hold()

        with self.beat("rule3") as t:
            self.clear_all(t)
            head = fit(serif("Rule 3  ·  Solve problems", TITLE_SIZE,
                             TERRACOTTA))
            head.to_edge(UP, buff=GAP_MD * 1.9)
            self.play(Write(head), run_time=t.fill(0.1))
            self.section_head = head
            doing = lines("calculate · convert · trace · design",
                          "write · debug · evaluate",
                          size=BODY_SIZE, color=CHARCOAL)
            self.below_head(doing, buff=GAP_MD * 1.6)
            note = serif("computer science is not a spectator sport",
                         BODY_SIZE, SLATE)
            note.next_to(doing, DOWN, buff=GAP_LG)
            self.play(Write(doing), run_time=t.fill(0.3))
            self.play(Write(note), run_time=t.fill(0.2))
            t.hold()

        with self.beat("not_failure") as t:
            self.clear_all(t)
            wrong = serif("and sometimes you will get it completely wrong",
                          BODY_SIZE, GREY)
            fit(wrong)
            wrong.move_to(UP * 1.3)
            fine = lines("That is not failure.",
                         "That is programming.",
                         size=TITLE_SIZE * 1.3)
            fine[1].set_color(TERRACOTTA)
            fine.move_to(DOWN * 0.2)
            self.play(Write(wrong), run_time=t.fill(0.2))
            self.play(Write(fine), run_time=t.fill(0.35))
            t.hold()

    def closing(self):
        with self.beat("closing") as t:
            self.clear_all(t)
            back = serif("computer science is not really about computers",
                         BODY_SIZE, GREY)
            fit(back)
            back.to_edge(UP, buff=GAP_LG * 1.2)
            four = WordArc(["information", "logic", "systems",
                            "problem-solving"], size=TITLE_SIZE * 0.85,
                           arrow="·", dim=CHARCOAL, lit=TERRACOTTA)
            four.next_to(back, DOWN, buff=GAP_LG)
            tool = lines("a computer is one of the most powerful tools",
                         "we have for putting those ideas into action",
                         size=BODY_SIZE, color=CHARCOAL)
            tool.next_to(four, DOWN, buff=GAP_LG)
            self.play(Write(back), run_time=t.fill(0.16))
            self.play(Write(four), run_time=t.fill(0.25))
            self.play(Write(tool), run_time=t.fill(0.25))
            t.hold()

        with self.beat("think_like") as t:
            self.clear_all(t)
            self.set_head(t, "Look at any system and ask", fraction=0.05)
            asks = lines("what information is going in?",
                         "how is it represented?",
                         "how is it processed?",
                         "how is it stored?",
                         "how is it transmitted?",
                         "how is it protected?",
                         "how could I design a better solution?",
                         size=BODY_SIZE, color=CHARCOAL, align=LEFT)
            goal = serif("Think like a computer scientist.",
                         TITLE_SIZE, TERRACOTTA)
            fit(goal)
            self.column([asks, goal], self.section_head, floor=-3.5)
            for ask in asks:
                self.play(Write(ask), run_time=t.fill(0.09))
            self.play(Write(goal), run_time=t.fill(0.2))
            t.hold()

        with self.beat("next") as t:
            self.clear_all(t)
            simplest = serif("the simplest idea in the entire course",
                             BODY_SIZE, GREY)
            simplest.to_edge(UP, buff=GAP_LG * 1.3)
            two = serif("two symbols", TITLE_SIZE, CHARCOAL)
            two.next_to(simplest, DOWN, buff=GAP_LG)
            digits = serif("0    1", TITLE_SIZE * 2.4, TERRACOTTA)
            digits.next_to(two, DOWN, buff=GAP_MD * 1.4)
            lesson = serif("Lesson 1  ·  the world of binary",
                           TITLE_SIZE, SLATE)
            lesson.next_to(digits, DOWN, buff=GAP_LG)
            self.play(Write(simplest), run_time=t.fill(0.14))
            self.play(Write(two), run_time=t.fill(0.12))
            self.play(Write(digits), run_time=t.fill(0.16))
            self.play(Write(lesson), run_time=t.fill(0.18))
            t.hold()

        with self.beat("thanks") as t:
            self.clear_all(t)
            thanks = serif("Thank you for joining.", TITLE_SIZE * 1.2)
            thanks.move_to(UP * 0.8)
            nextweek = serif("Next week: Chapter 1", BODY_SIZE, GREY)
            nextweek.next_to(thanks, DOWN, buff=GAP_MD * 1.4)
            where = serif("academy.thedigitaltutor.net", BODY_SIZE,
                          TERRACOTTA)
            where.next_to(nextweek, DOWN, buff=GAP_LG)
            self.play(Write(thanks), run_time=t.fill(0.25))
            self.play(Write(nextweek), run_time=t.fill(0.15))
            self.play(Write(where), run_time=t.fill(0.2))
            t.hold()
