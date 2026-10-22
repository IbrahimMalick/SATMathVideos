"""Chapter 1 — Data Representation, the video companion.

Follows the chapter companion deck: why binary, number systems, binary
operations, then text, sound, images and storage. The recording stops
after storage units, so this is parts one to three of the chapter's four;
compression is not in the narration and is not invented here.

The spine is the place-value row. Conversion, unsigned range, shifts and
two's complement are all the same picture with one thing changed, so
BitRow carries them and the sum underneath is derived from the bits rather
than written out by hand.

Where the delivery or the transcriber is loose, the screen carries the
correct form. Two of these are real slips rather than transcription:

  * the hexadecimal example is 1101 0110 1011 = D6B. The narration says
    "B6B"; 1101 is D.
  * 00110111 shifted left twice is 11011100 = 220, not 225.

The rest are misreadings of a pattern he had right on the slide: the
binary-to-denary value is 10110110, the denary-to-binary result is
10011101, the sum is 10100100, 7A3 is 0111 1010 0011, the two's
complement patterns are 11101011 and 11011011, and the checkpoint answers
are 107, 00101101, BCA and 11001010. Storage units are KiB, MiB and GiB,
as the deck has them: with 1024 as the multiplier those are the syllabus
names, and the narration says kilobyte, megabyte and gigabyte.

Timing: timings/concept.data_representation.json

The delivered recording is derived from the raw one in two steps, both
reproducible:

    python build/segment.py audio/CH01-data-representation-raw.words.json \\
        --audio audio/CH01-data-representation-raw.m4a \\
        --cut CH01-data-representation-trim="All right guys welcome to \\
chapter one data representation" --pad 0.5

    python build/retake.py audio/CH01-data-representation-trim.words.json \\
        --audio audio/CH01-data-representation-trim.m4a \\
        --out CH01-data-representation \\
        --drop "All right guys welcome to chapter one data representation \\
for Cambridge"="It's basically you know 2020 10 2210 I could take two" \\
        --drop "Now hexadecimal is based 16 It uses a symbol 0 to 9"=\\
"retakes slide 7"

Render: python build/render.py scripts/CH01-data-representation.md \\
    audio/CH01-data-representation.m4a
"""

from manim import (
    Arrow,
    Circle,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    Line,
    Rectangle,
    SurroundingRectangle,
    Transform,
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
    CREAM,
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
from components.bit_row import BitRow
from components.stepup import code_block, rule_card
from components.syllabus_map import TopicStrip
from scenes.base import SATScene

FRAME_SAFE = 12.6
WIDE = 11.5
FLOOR = -2.9

PARTS = ["Number systems", "Binary operations", "Media and storage",
         "Compression"]


def fit(mobject, width=FRAME_SAFE):
    if mobject.width > width:
        mobject.scale_to_fit_width(width)
    return mobject


class DataRepresentation(SATScene):
    scene_id = "concept.data_representation"

    def construct(self):
        self.margin = mono("O Level CS 2210 · Data Representation",
                           MARGIN_SIZE)
        self.margin.to_corner(UP + LEFT, buff=GAP_SM)
        self.add(self.margin)
        self.keep = [self.margin]
        self.strip = None
        self.head = None

        self.opening()
        self.why_binary()
        self.chapter_map()
        self.place_values()
        self.binary_to_denary()
        self.denary_to_binary()
        self.hexadecimal()
        self.hex_place_value()
        self.binary_addition()
        self.overflow()
        self.logical_shifts()
        self.twos_complement()
        self.invert_add_one()
        self.checkpoint()
        self.text()
        self.sound()
        self.sound_size()
        self.images()
        self.image_size()
        self.storage()

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

    def stack(self, group, top=None, buff=GAP_MD, floor=FLOOR, align=ORIGIN):
        """Place under `top`, tightening the group's own gaps to clear the floor."""
        for factor in (1.0, 0.85, 0.7, 0.55, 0.42, 0.32, 0.24):
            gap = buff * factor
            group.arrange(DOWN, buff=gap, aligned_edge=align)
            if top is None:
                group.move_to(ORIGIN)
            else:
                group.next_to(top, DOWN, buff=gap)
            if group.get_bottom()[1] >= floor:
                break
        return group

    def column(self, items, top=None, buff=GAP_MD * 1.2, floor=FLOOR):
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

    def pairs(self, rows, top=None, size=LABEL_SIZE, left_x=-5.8,
              right_x=-0.9, cue=GREY, answer=CHARCOAL, gap=GAP_SM * 1.4,
              floor=FLOOR):
        """Two aligned columns on a fixed pitch, placed by coordinate.

        Pango may collapse runs of whitespace, so space-padded columns are
        not actually aligned; and arranging by bounding box makes rows
        without descenders sit closer than their neighbours.
        """
        gutter = right_x - left_x - 0.35
        built = []
        for left_text, right_text in rows:
            left = fit(serif(left_text, size, cue), gutter)
            right = fit(serif(right_text, size, answer),
                        FRAME_SAFE / 2 - right_x - 0.4)
            built.append((left, right))
        line = max(max(l.height, r.height) for l, r in built)
        group = VGroup()
        for factor in (1.0, 0.85, 0.7, 0.55, 0.42, 0.32, 0.24):
            pitch = line + gap * factor
            group = VGroup()
            for i, (left, right) in enumerate(built):
                y = -i * pitch
                left.move_to([left_x, y, 0], aligned_edge=LEFT)
                right.move_to([right_x, y, 0], aligned_edge=LEFT)
                group.add(VGroup(left, right))
            if top is None:
                group.move_to(ORIGIN)
            else:
                group.next_to(top, DOWN, buff=gap * factor)
            for sub in group:
                sub[0].set_x(left_x + sub[0].width / 2)
                sub[1].set_x(right_x + sub[1].width / 2)
            if group.get_bottom()[1] >= floor:
                break
        return group

    def hide(self, group):
        for row in group:
            row.set_opacity(0)
        return group

    def reveal(self, t, group, start, stop, fraction):
        for row in group[start:stop]:
            row.set_opacity(1)
            self.play(FadeIn(row), run_time=t.fill(fraction))

    def foot(self, mobject, buff=GAP_MD * 1.1):
        if self.strip in self.mobjects:
            mobject.next_to(self.strip, UP, buff=buff)
        else:
            mobject.to_edge(DOWN, buff=buff)
        return mobject

    def part(self, t, number, fraction=0.09):
        """Advance the chapter strip along the bottom."""
        if self.strip is None:
            self.strip = TopicStrip(4, lit=SLATE, side=0.6)
            self.strip.to_edge(DOWN, buff=GAP_SM * 0.6)
            self.add(self.strip)
            self.keep.append(self.strip)
        self.play(*self.strip.focus(number - 1), run_time=t.fill(fraction))

    def caption(self, text, color=GREY, size=BODY_SIZE):
        return fit(serif(text, size, color))

    def recaption(self, t, holder, text, color=GREY, fraction=0.18):
        nxt = self.caption(text, color)
        nxt.move_to(holder)
        self.play(Transform(holder, nxt), run_time=t.fill(fraction))
        return holder

    def panel(self, t, rows, top=None, accent=SLATE, draw=0.12, write=0.45):
        block = code_block(rows, size=LABEL_SIZE, accent=accent, width=WIDE)
        if top is None:
            self.column([block], self.head)
        else:
            block.next_to(top, DOWN, buff=GAP_MD)
        self.play(Create(block[0]), run_time=t.fill(draw))
        self.play(Write(block[1]), run_time=t.fill(write))
        return block

    def big_rule(self, t, rows, draw=0.16, write=0.45, y=0.4):
        card = rule_card(rows, size=TITLE_SIZE, color=TERRACOTTA, width=WIDE)
        card.move_to(UP * y)
        self.play(Create(card[0]), run_time=t.fill(draw))
        self.play(Write(card[1]), run_time=t.fill(write))
        return card

    def bits(self, pattern, top=None, signed=False, y=0.9, **kw):
        row = BitRow(pattern, signed=signed, width=WIDE, **kw)
        if top is None:
            row.move_to(UP * y)
        else:
            row.next_to(top, DOWN, buff=GAP_MD * 1.2)
        return row

    def show_bits(self, t, row, places=0.18, digits=0.25):
        self.play(Write(row.places), run_time=t.fill(places))
        self.play(Write(row.bits), run_time=t.fill(digits))
        return row

    def sum_under(self, t, row, fraction=0.3, color=CHARCOAL, result=True):
        line = fit(row.sum_line(size=BODY_SIZE, color=color, result=result))
        line.next_to(row, DOWN, buff=GAP_MD * 1.3)
        self.play(Write(line), run_time=t.fill(fraction))
        return line

    def calc(self, text, size=BODY_SIZE, color=CHARCOAL):
        return fit(serif(text, size, color))

    # ------------------------------------------------------------- opening

    def opening(self):
        with self.beat("open_title") as t:
            head = self.lines("Data Representation", size=TITLE_SIZE * 1.6)
            head.move_to(UP * 1.5)
            sub = self.caption("How text, sound, images and numbers "
                               "become binary")
            sub.next_to(head, DOWN, buff=GAP_MD * 1.4)
            tag = mono("CAMBRIDGE O LEVEL  ·  2210  ·  CHAPTER 1",
                       MARGIN_SIZE, GREY)
            tag.next_to(sub, DOWN, buff=GAP_LG)
            self.play(Write(head), run_time=t.fill(0.34))
            self.play(Write(sub), run_time=t.fill(0.2))
            self.play(FadeIn(tag), run_time=t.fill(0.12))
            t.hold()

        with self.beat("open_book") as t:
            note = self.caption("open the chapter  ·  keep a pen nearby",
                                TERRACOTTA)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.45))
            t.hold()

        with self.beat("open_scope") as t:
            self.wipe(t)
            self.title(t, "What this lesson connects", fraction=0.06)
            items = self.lines("number systems", "binary arithmetic and shifts",
                               "two's complement", "text, sound and images",
                               "storage units", size=BODY_SIZE, align=LEFT)
            self.stack(items, self.head, align=LEFT)
            self.hide(items)
            self.reveal(t, items, 0, len(items), 0.14)
            t.hold()

        with self.beat("open_goal") as t:
            note = self.caption("more than remembering definitions")
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

        with self.beat("open_by_end") as t:
            self.wipe(t)
            self.title(t, "By the end you can", fraction=0.06)
            items = self.lines("explain each idea in examination language",
                               "carry out the calculations accurately",
                               "recognise the traps that cost marks",
                               size=BODY_SIZE, align=LEFT)
            self.stack(items, self.head, align=LEFT)
            self.hide(items)
            self.reveal(t, items, 0, len(items), 0.22)
            t.hold()

        with self.beat("open_pause") as t:
            self.wipe(t)
            self.big_rule(t, ["PAUSE AT EVERY",
                              "STOP AND CHECK"], y=0.3)
            t.hold()

    def why_binary(self):
        with self.beat("why_display") as t:
            self.wipe(t)
            self.title(t, "Why binary", fraction=0.1)
            note = self.lines("Photographs, music, text and video —",
                              "the circuits understand none of them.",
                              size=BODY_SIZE)
            self.stack(note, self.head)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

        with self.beat("why_states") as t:
            self.wipe(t)
            self.title(t, "A circuit tells two states apart", fraction=0.14)
            t.hold()

        with self.beat("why_switch") as t:
            boxes = VGroup()
            for digit, label, colour in (("0", "LOW  ·  OFF", GREY),
                                         ("1", "HIGH  ·  ON", SLATE)):
                number = serif(digit, TITLE_SIZE * 1.6, colour)
                caption = serif(label, LABEL_SIZE, GREY)
                inner = VGroup(number, caption).arrange(DOWN, buff=GAP_SM)
                box = SurroundingRectangle(inner, color=colour,
                                           buff=GAP_MD, stroke_width=3)
                boxes.add(VGroup(box, inner))
            boxes.arrange(RIGHT, buff=GAP_LG * 1.4)
            boxes.next_to(self.head, DOWN, buff=GAP_LG)
            for pair in boxes:
                self.play(Create(pair[0]), run_time=t.fill(0.14))
                self.play(Write(pair[1]), run_time=t.fill(0.16))
            self.states = boxes
            t.hold()

        with self.beat("why_bit") as t:
            note = self.caption("one binary digit  =  one bit", TERRACOTTA)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

        with self.beat("why_reliable") as t:
            self.wipe(t)
            note = self.lines("Small electrical variations still read",
                              "as the intended high or low state.",
                              size=TITLE_SIZE)
            note.move_to(UP * 0.6)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

        with self.beat("why_answer") as t:
            self.wipe(t)
            self.big_rule(t, ["PROCESSED BY LOGIC GATES",
                              "STORED IN REGISTERS"], y=0.6)
            t.hold()

        with self.beat("why_vague") as t:
            note = self.lines('"computers understand 0 and 1" is too vague',
                              "name the hardware reason: two stable states",
                              size=LABEL_SIZE, color=GREY)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

    def chapter_map(self):
        with self.beat("map_intro") as t:
            self.wipe(t)
            self.title(t, "The chapter has four connected parts",
                       fraction=0.3)
            t.hold()

        self.map_rows = self.pairs(
            [(f"0{i + 1}", name) for i, name in enumerate(PARTS)],
            top=self.head, size=BODY_SIZE, left_x=-5.2, right_x=-3.8,
            cue=SLATE, gap=GAP_MD)
        self.hide(self.map_rows)

        for name, index in (("map_1", 0), ("map_2", 1), ("map_3", 2),
                            ("map_4", 3)):
            with self.beat(name) as t:
                self.reveal(t, self.map_rows, index, index + 1, 0.5)
                t.hold()

        with self.beat("map_connected") as t:
            note = self.caption("a sound sample becomes a binary number")
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

        with self.beat("map_question") as t:
            self.wipe(t)
            self.big_rule(t, ["WHAT IS BEING ENCODED?",
                              "HOW MANY BITS?"], y=0.4)
            t.hold()

    # ------------------------------------------------------ number systems

    def place_values(self):
        with self.beat("pv_base") as t:
            self.wipe(t)
            self.part(t, 1, fraction=0.1)
            self.title(t, "Place value depends on the base", fraction=0.3)
            t.hold()

        with self.beat("pv_denary") as t:
            row = self.pairs([("denary", "base 10    1   10   100   1000")],
                             top=self.head, size=BODY_SIZE, left_x=-5.4,
                             right_x=-2.8, cue=SLATE)
            self.hide(row)
            self.reveal(t, row, 0, 1, 0.5)
            self.denary_row = row
            t.hold()

        with self.beat("pv_binary") as t:
            note = self.caption("binary is base 2 — every column doubles")
            note.next_to(self.denary_row, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

        with self.beat("pv_row") as t:
            self.wipe(t)
            self.title(t, "The row to learn by heart", fraction=0.08)
            row = self.bits("00000000")
            row.next_to(self.head, DOWN, buff=GAP_LG)
            self.play(Write(row.places), run_time=t.fill(0.5))
            self.place_row = row
            t.hold()

        with self.beat("pv_contrib") as t:
            note = self.lines("a 1 contributes its place value",
                              "a 0 contributes nothing",
                              size=BODY_SIZE, color=GREY)
            note.next_to(self.place_row, DOWN, buff=GAP_LG)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

        with self.beat("pv_learn") as t:
            note = self.caption("conversion · range · shifts · two's complement",
                                TERRACOTTA, LABEL_SIZE)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

    def binary_to_denary(self):
        with self.beat("b2d_intro") as t:
            self.wipe(t)
            self.title(t, "Binary to denary", fraction=0.2)
            t.hold()

        with self.beat("b2d_write") as t:
            # 10110110 — the narration reads a short pattern aloud.
            row = self.bits("10110110")
            row.next_to(self.head, DOWN, buff=GAP_LG)
            self.play(Write(row.places), run_time=t.fill(0.4))
            self.b2d = row
            t.hold()

        with self.beat("b2d_ones") as t:
            self.play(Write(self.b2d.bits), run_time=t.fill(0.5))
            t.hold()

        with self.beat("b2d_add") as t:
            self.play(*self.b2d.light(), run_time=t.fill(0.6))
            t.hold()

        with self.beat("b2d_result") as t:
            self.sum_under(t, self.b2d, fraction=0.5, color=SAGE)
            t.hold()

        with self.beat("b2d_show") as t:
            note = self.caption("show the place values, or show the addition")
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

        with self.beat("b2d_check") as t:
            self.wipe(t)
            self.big_rule(t, ["UNSIGNED 8 BITS", "0 TO 255"], y=0.4)
            t.hold()

    def denary_to_binary(self):
        with self.beat("d2b_intro") as t:
            self.wipe(t)
            self.title(t, "Denary 157 to 8-bit binary", fraction=0.3)
            t.hold()

        steps = ["157 - 128 = 29", "29 - 16 = 13", "13 - 8 = 5",
                 "5 - 4 = 1", "1 - 1 = 0"]
        self.ladder = self.lines(*steps, size=BODY_SIZE, color=SLATE,
                                 align=LEFT)
        self.stack(self.ladder, self.head, align=LEFT)
        self.hide(self.ladder)

        with self.beat("d2b_128") as t:
            self.reveal(t, self.ladder, 0, 1, 0.5)
            t.hold()

        with self.beat("d2b_6432") as t:
            note = self.caption("64 and 32 do not fit — write 0 in both",
                                GREY, LABEL_SIZE)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

        with self.beat("d2b_rest") as t:
            self.reveal(t, self.ladder, 1, 5, 0.12)
            t.hold()

        with self.beat("d2b_result") as t:
            self.wipe(t)
            self.title(t, "157  =  10011101", fraction=0.1)
            row = self.bits("10011101")
            row.next_to(self.head, DOWN, buff=GAP_LG)
            self.show_bits(t, row, places=0.2, digits=0.3)
            self.play(*row.light(), run_time=t.fill(0.2))
            t.hold()

        with self.beat("d2b_leading") as t:
            self.wipe(t)
            self.big_rule(t, ["EIGHT BITS MEANS",
                              "KEEP THE LEADING ZEROS"], y=0.7)
            t.hold()

        with self.beat("d2b_13") as t:
            row = self.bits("00001101")
            row.to_edge(DOWN, buff=GAP_LG * 1.3)
            label = self.caption("13", GREY, LABEL_SIZE)
            label.next_to(row, LEFT, buff=GAP_MD)
            self.play(Write(row.bits), FadeIn(label), run_time=t.fill(0.5))
            t.hold()

    def hexadecimal(self):
        with self.beat("hex_base") as t:
            self.wipe(t)
            self.title(t, "Hexadecimal is base 16", fraction=0.1)
            digits = self.lines("0 1 2 3 4 5 6 7 8 9",
                                "A  B  C  D  E  F",
                                size=TITLE_SIZE, color=SLATE)
            self.stack(digits, self.head)
            self.play(Write(digits[0]), run_time=t.fill(0.2))
            self.play(Write(digits[1]), run_time=t.fill(0.2))
            note = self.caption("A to F carry the values 10 to 15",
                                GREY, LABEL_SIZE)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.2))
            t.hold()

        with self.beat("hex_nibble") as t:
            self.wipe(t)
            self.big_rule(t, ["ONE HEX DIGIT", "IS FOUR BITS  ·  A NIBBLE"],
                          y=0.5)
            t.hold()

        with self.beat("hex_shorter") as t:
            note = self.caption("shorter to write, easier to read")
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

        with self.beat("hex_example") as t:
            self.wipe(t)
            self.title(t, "Group the bits in fours", fraction=0.14)
            # D6B. The narration says "B6B"; 1101 is D.
            groups = VGroup()
            for nib, hexd in (("1101", "D"), ("0110", "6"), ("1011", "B")):
                top_bits = serif(nib, TITLE_SIZE, CHARCOAL)
                letter = serif(hexd, TITLE_SIZE * 1.5, TERRACOTTA)
                groups.add(VGroup(top_bits, letter).arrange(DOWN,
                                                            buff=GAP_MD))
            groups.arrange(RIGHT, buff=GAP_LG * 1.2)
            groups.next_to(self.head, DOWN, buff=GAP_LG)
            for group in groups:
                self.play(Write(group[0]), run_time=t.fill(0.1))
                self.play(Write(group[1]), run_time=t.fill(0.12))
            t.hold()

        with self.beat("hex_reverse") as t:
            self.wipe(t)
            self.title(t, "7A3 back to binary", fraction=0.1)
            groups = VGroup()
            for hexd, nib in (("7", "0111"), ("A", "1010"), ("3", "0011")):
                letter = serif(hexd, TITLE_SIZE * 1.5, SLATE)
                low_bits = serif(nib, TITLE_SIZE, CHARCOAL)
                groups.add(VGroup(letter, low_bits).arrange(DOWN,
                                                            buff=GAP_MD))
            groups.arrange(RIGHT, buff=GAP_LG * 1.2)
            groups.next_to(self.head, DOWN, buff=GAP_LG)
            for group in groups:
                self.play(Write(group[0]), run_time=t.fill(0.1))
                self.play(Write(group[1]), run_time=t.fill(0.14))
            t.hold()

        with self.beat("hex_where") as t:
            self.wipe(t)
            self.title(t, "Where you meet it", fraction=0.08)
            items = self.lines("memory addresses", "machine code",
                               "MAC addresses", "IPv6 addresses",
                               "colour codes", size=BODY_SIZE, align=LEFT)
            self.stack(items, self.head, align=LEFT)
            self.hide(items)
            self.reveal(t, items, 0, len(items), 0.14)
            t.hold()

        with self.beat("hex_storage") as t:
            self.wipe(t)
            self.big_rule(t, ["HEX SAVES NO STORAGE",
                              "THE DATA IS STILL BINARY"], y=0.4)
            t.hold()

    def hex_place_value(self):
        with self.beat("hp_two") as t:
            self.wipe(t)
            self.title(t, "Two hex digits: sixteens and ones", fraction=0.3)
            t.hold()

        with self.beat("hp_4d") as t:
            line = self.calc("4D  =  (4 x 16)  +  13", TITLE_SIZE)
            line.next_to(self.head, DOWN, buff=GAP_LG)
            self.play(Write(line), run_time=t.fill(0.5))
            self.hp_line = line
            t.hold()

        with self.beat("hp_77") as t:
            result = self.calc("=  77", TITLE_SIZE * 1.2, SAGE)
            result.next_to(self.hp_line, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(result), run_time=t.fill(0.5))
            t.hold()

        with self.beat("hp_206") as t:
            self.wipe(t)
            self.title(t, "Denary 206 to hexadecimal", fraction=0.14)
            line = self.calc("206  /  16", TITLE_SIZE)
            line.next_to(self.head, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(line), run_time=t.fill(0.4))
            self.div = line
            t.hold()

        with self.beat("hp_quotient") as t:
            rows = self.pairs([("quotient", "12"), ("remainder", "14")],
                              top=self.div, size=BODY_SIZE, left_x=-3.4,
                              right_x=-0.2, cue=GREY)
            self.hide(rows)
            self.reveal(t, rows, 0, 2, 0.25)
            self.qr = rows
            t.hold()

        with self.beat("hp_ce") as t:
            answer = self.calc("206  =  CE", TITLE_SIZE * 1.2, TERRACOTTA)
            self.foot(answer)
            self.play(Write(answer), run_time=t.fill(0.5))
            t.hold()

        with self.beat("hp_check") as t:
            self.wipe(t)
            self.title(t, "Check by converting back", fraction=0.1)
            steps = self.lines("C x 16  =  192", "192  +  14  =  206",
                               size=TITLE_SIZE, color=SAGE)
            self.stack(steps, self.head)
            self.hide(steps)
            self.reveal(t, steps, 0, 2, 0.3)
            t.hold()

    # --------------------------------------------------- binary operations

    def binary_addition(self):
        with self.beat("add_rules") as t:
            self.wipe(t)
            self.part(t, 2, fraction=0.1)
            self.title(t, "Binary addition has four rules", fraction=0.3)
            t.hold()

        self.rules = self.lines("0 + 0  =  0", "0 + 1  =  1",
                                "1 + 1  =  10", "1 + 1 + 1  =  11",
                                size=TITLE_SIZE, color=SLATE)
        self.stack(self.rules, self.head)
        self.hide(self.rules)

        with self.beat("add_r1") as t:
            self.reveal(t, self.rules, 0, 2, 0.25)
            t.hold()

        with self.beat("add_r2") as t:
            self.reveal(t, self.rules, 2, 3, 0.4)
            note = self.caption("write 0, carry 1", GREY, LABEL_SIZE)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.2))
            self.carry_note = note
            t.hold()

        with self.beat("add_r3") as t:
            self.reveal(t, self.rules, 3, 4, 0.35)
            self.recaption(t, self.carry_note, "write 1, carry 1",
                           GREY, 0.2)
            t.hold()

        with self.beat("add_dir") as t:
            self.wipe(t)
            self.big_rule(t, ["WORK RIGHT TO LEFT"], y=0.5)
            t.hold()

        with self.beat("add_example") as t:
            self.wipe(t)
            # 01101101 + 00110111 = 10100100. The narration misreads the
            # sum aloud; the columns are what the slide has.
            block = code_block(["  01101101",
                                "+ 00110111",
                                "----------",
                                "  10100100"], size=TITLE_SIZE, accent=SLATE,
                               width=WIDE * 0.7)
            block.move_to(UP * 0.5)
            self.play(Create(block[0]), run_time=t.fill(0.1))
            self.play(Write(block[1]), run_time=t.fill(0.5))
            self.sum_block = block
            t.hold()

        with self.beat("add_check") as t:
            check = self.calc("109  +  55  =  164", TITLE_SIZE, SAGE)
            self.foot(check)
            self.play(Write(check), run_time=t.fill(0.5))
            t.hold()

        with self.beat("add_carry") as t:
            self.wipe(t)
            self.big_rule(t, ["A CARRY IS NOT", "AUTOMATICALLY OVERFLOW"],
                          y=0.4)
            t.hold()

    def overflow(self):
        with self.beat("ov_range") as t:
            self.wipe(t)
            self.title(t, "Overflow", fraction=0.1)
            band = self.pairs([("00000000", "0"), ("11111111", "255")],
                              top=self.head, size=TITLE_SIZE, left_x=-4.4,
                              right_x=0.6, cue=CHARCOAL, answer=SLATE)
            self.hide(band)
            self.reveal(t, band, 0, 2, 0.25)
            self.band = band
            t.hold()

        with self.beat("ov_def") as t:
            note = self.caption("bigger than 255 needs more than 8 bits")
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

        with self.beat("ov_example") as t:
            self.wipe(t)
            block = code_block(["  11001010",
                                "+ 01011101"], size=TITLE_SIZE, accent=SLATE,
                               width=WIDE * 0.7)
            block.move_to(UP * 1.2)
            self.play(Create(block[0]), run_time=t.fill(0.14))
            self.play(Write(block[1]), run_time=t.fill(0.4))
            self.ov_block = block
            t.hold()

        with self.beat("ov_values") as t:
            line = self.calc("202  +  93", TITLE_SIZE, GREY)
            line.next_to(self.ov_block, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(line), run_time=t.fill(0.5))
            self.ov_values = line
            t.hold()

        with self.beat("ov_sum") as t:
            line = self.calc("=  295", TITLE_SIZE * 1.2, TERRACOTTA)
            line.next_to(self.ov_values, DOWN, buff=GAP_MD)
            self.play(Write(line), run_time=t.fill(0.5))
            t.hold()

        with self.beat("ov_ninth") as t:
            self.wipe(t)
            self.big_rule(t, ["295 NEEDS 9 BITS", "OVERFLOW"], y=0.6)
            t.hold()

        with self.beat("ov_explain") as t:
            note = self.lines("outside the available range",
                              "and it cannot fit in the register",
                              size=BODY_SIZE, color=GREY)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

        with self.beat("ov_notcarry") as t:
            self.wipe(t)
            note = self.lines("Do not describe every carry",
                              "as overflow.", size=TITLE_SIZE * 1.1,
                              color=TERRACOTTA)
            note.move_to(UP * 0.5)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

    def logical_shifts(self):
        with self.beat("sh_intro") as t:
            self.wipe(t)
            self.title(t, "Logical shifts", fraction=0.5)
            t.hold()

        with self.beat("sh_def") as t:
            note = self.caption("every bit moves left or right")
            self.stack(VGroup(note), self.head)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

        with self.beat("sh_lost") as t:
            note = self.lines("bits leaving the register are lost",
                              "zeros enter at the opposite end",
                              size=BODY_SIZE, color=GREY)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

        with self.beat("sh_mult") as t:
            self.wipe(t)
            rows = self.pairs([("left by 1", "x 2"), ("right by 1", "/ 2")],
                              size=TITLE_SIZE, left_x=-4.0, right_x=0.4,
                              cue=GREY, answer=SLATE)
            rows.move_to(UP * 0.8)
            self.hide(rows)
            self.reveal(t, rows, 0, 1, 0.5)
            self.shift_rows = rows
            t.hold()

        with self.beat("sh_div") as t:
            self.reveal(t, self.shift_rows, 1, 2, 0.5)
            t.hold()

        with self.beat("sh_example") as t:
            self.wipe(t)
            self.title(t, "Shift 00110111 left by two", fraction=0.1)
            before = self.bits("00110111", show_places=False)
            before.next_to(self.head, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(before.bits), run_time=t.fill(0.4))
            self.before = before
            t.hold()

        with self.beat("sh_result") as t:
            after = self.bits("11011100", show_places=False)
            after.next_to(self.before, DOWN, buff=GAP_LG * 1.1)
            arrow = Arrow(self.before.get_bottom(), after.get_top(),
                          color=GREY, buff=GAP_SM, stroke_width=3,
                          max_tip_length_to_length_ratio=0.18)
            self.play(Create(arrow), run_time=t.fill(0.14))
            self.play(Write(after.bits), run_time=t.fill(0.3))
            # 55 x 4 = 220. The narration says 225.
            note = self.calc("55  x  4  =  220", TITLE_SIZE, SAGE)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.2))
            t.hold()

        with self.beat("sh_inspect") as t:
            self.wipe(t)
            self.big_rule(t, ["A DISCARDED 1", "CANNOT BE RECOVERED"], y=0.4)
            t.hold()

    def twos_complement(self):
        with self.beat("tc_intro") as t:
            self.wipe(t)
            self.title(t, "Two's complement", fraction=0.5)
            t.hold()

        with self.beat("tc_def") as t:
            note = self.caption("positive and negative, in a fixed number "
                                "of bits")
            self.stack(VGroup(note), self.head)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

        with self.beat("tc_msb") as t:
            self.wipe(t)
            self.title(t, "Only the first column changes", fraction=0.08)
            row = self.bits("11101011", signed=True)
            row.next_to(self.head, DOWN, buff=GAP_LG)
            self.play(Write(row.places), run_time=t.fill(0.4))
            self.tc_row = row
            self.play(self.tc_row.places[0].animate.set_color(TERRACOTTA),
                      run_time=t.fill(0.25))
            t.hold()

        with self.beat("tc_rest") as t:
            note = self.caption("the rest keep their positive values",
                                GREY, LABEL_SIZE)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

        with self.beat("tc_range") as t:
            self.wipe(t)
            self.big_rule(t, ["8 BITS SIGNED", "-128 TO +127"], y=0.5)
            t.hold()

        with self.beat("tc_leading") as t:
            rows = self.pairs([("leading 0", "not negative"),
                               ("leading 1", "negative")],
                              size=TITLE_SIZE, left_x=-4.6, right_x=-0.4,
                              cue=SLATE)
            self.foot(rows)
            self.hide(rows)
            self.reveal(t, rows, 0, 2, 0.25)
            t.hold()

        with self.beat("tc_read") as t:
            self.wipe(t)
            self.title(t, "Read 11101011", fraction=0.08)
            row = self.bits("11101011", signed=True)
            row.next_to(self.head, DOWN, buff=GAP_MD * 1.4)
            self.show_bits(t, row, places=0.2, digits=0.25)
            self.play(*row.light(), run_time=t.fill(0.2))
            self.tc_read_row = row
            t.hold()

        with self.beat("tc_result") as t:
            self.sum_under(t, self.tc_read_row, fraction=0.5, color=SAGE)
            t.hold()

    def invert_add_one(self):
        with self.beat("ia_intro") as t:
            self.wipe(t)
            self.title(t, "Write negative 37", fraction=0.4)
            t.hold()

        with self.beat("ia_write") as t:
            label = self.caption("1   write +37", GREY, LABEL_SIZE)
            row = BitRow("00100101", show_places=False, width=WIDE)
            group = VGroup(label, row.bits).arrange(DOWN, buff=GAP_SM * 1.2)
            group.next_to(self.head, DOWN, buff=GAP_MD)
            self.play(Write(label), run_time=t.fill(0.15))
            self.play(Write(row.bits), run_time=t.fill(0.3))
            self.ia_1 = group
            t.hold()

        with self.beat("ia_invert") as t:
            label = self.caption("2   invert every bit", GREY, LABEL_SIZE)
            row = BitRow("11011010", show_places=False, width=WIDE)
            group = VGroup(label, row.bits).arrange(DOWN, buff=GAP_SM * 1.2)
            group.next_to(self.ia_1, DOWN, buff=GAP_MD)
            self.play(Write(label), run_time=t.fill(0.15))
            self.play(Write(row.bits), run_time=t.fill(0.3))
            self.ia_2 = group
            t.hold()

        with self.beat("ia_add") as t:
            label = self.caption("3   add 1", GREY, LABEL_SIZE)
            row = BitRow("11011011", show_places=False, width=WIDE,
                         dim=TERRACOTTA)
            group = VGroup(label, row.bits).arrange(DOWN, buff=GAP_SM * 1.2)
            group.next_to(self.ia_2, DOWN, buff=GAP_MD)
            self.play(Write(label), run_time=t.fill(0.15))
            self.play(Write(row.bits), run_time=t.fill(0.35))
            t.hold()

        with self.beat("ia_check") as t:
            self.wipe(t)
            self.title(t, "Check with the signed place values", fraction=0.1)
            row = self.bits("11011011", signed=True)
            row.next_to(self.head, DOWN, buff=GAP_MD * 1.2)
            self.show_bits(t, row, places=0.16, digits=0.2)
            self.play(*row.light(), run_time=t.fill(0.14))
            self.sum_under(t, row, fraction=0.3, color=SAGE)
            t.hold()

        with self.beat("ia_never") as t:
            self.wipe(t)
            self.big_rule(t, ["NEVER WRITE A MINUS SIGN",
                              "THE PATTERN CARRIES THE SIGN"], y=0.6)
            t.hold()

        with self.beat("ia_limit") as t:
            note = self.caption("the positive limit is 127 — one bit is "
                                "spent on the sign", GREY, LABEL_SIZE)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

    def checkpoint(self):
        with self.beat("sc_intro") as t:
            self.wipe(t)
            self.title(t, "Stop and check", fraction=0.4, color=TERRACOTTA)
            t.hold()

        questions = [
            "01101011  ->  denary",
            "45  ->  8-bit binary",
            "101111001010  ->  hexadecimal",
            "-54  ->  8-bit two's complement",
        ]
        self.qs = self.lines(*questions, size=BODY_SIZE, align=LEFT)
        self.stack(self.qs, self.head, align=LEFT)
        self.hide(self.qs)

        with self.beat("sc_pause") as t:
            note = self.caption("pause  ·  show every step", TERRACOTTA)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

        for name, index in (("sc_q1", 0), ("sc_q2", 1), ("sc_q3", 2),
                            ("sc_q4", 3)):
            with self.beat(name) as t:
                self.reveal(t, self.qs, index, index + 1, 0.5)
                t.hold()

        with self.beat("sc_resume") as t:
            t.hold()

        with self.beat("sc_answers") as t:
            self.wipe(t)
            self.title(t, "Answers", fraction=0.06)
            rows = self.pairs(
                [("01101011", "107"),
                 ("45", "00101101"),
                 ("101111001010", "BCA"),
                 ("-54", "11001010")], top=self.head, size=BODY_SIZE,
                left_x=-5.4, right_x=0.6, cue=GREY, answer=SAGE,
                gap=GAP_MD)
            self.hide(rows)
            self.reveal(t, rows, 0, 4, 0.2)
            t.hold()

        with self.beat("sc_differs") as t:
            note = self.caption("find the first step where your method "
                                "changed", GREY, LABEL_SIZE)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

    # ---------------------------------------------------- media and storage

    def text(self):
        with self.beat("tx_intro") as t:
            self.wipe(t)
            self.part(t, 3, fraction=0.1)
            self.title(t, "Text", fraction=0.3)
            t.hold()

        with self.beat("tx_stored") as t:
            chain = VGroup()
            for label in ("character", "numerical code", "binary"):
                chain.add(serif(label, BODY_SIZE, CHARCOAL))
            arrows = VGroup()
            chain.arrange(RIGHT, buff=GAP_LG * 1.5)
            fit(chain)
            chain.next_to(self.head, DOWN, buff=GAP_LG)
            for a, b in zip(chain[:-1], chain[1:]):
                arrows.add(Arrow(a.get_right(), b.get_left(), color=GREY,
                                 buff=GAP_SM * 0.8, stroke_width=3,
                                 max_tip_length_to_length_ratio=0.3))
            self.play(Write(chain[0]), run_time=t.fill(0.16))
            for arrow, word in zip(arrows, chain[1:]):
                self.play(Create(arrow), run_time=t.fill(0.1))
                self.play(Write(word), run_time=t.fill(0.14))
            self.chain = VGroup(chain, arrows)
            t.hold()

        with self.beat("tx_examples") as t:
            note = self.caption("letters, digits, punctuation, "
                                "control characters", GREY, LABEL_SIZE)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

        with self.beat("tx_ascii") as t:
            self.wipe(t)
            self.title(t, "ASCII", fraction=0.1)
            items = self.lines("common English letters",
                               "digits and punctuation",
                               "control characters",
                               size=BODY_SIZE, align=LEFT)
            self.stack(items, self.head, align=LEFT)
            self.hide(items)
            self.reveal(t, items, 0, len(items), 0.2)
            t.hold()

        with self.beat("tx_unicode") as t:
            self.wipe(t)
            self.title(t, "Unicode", fraction=0.1)
            items = self.lines("many writing systems", "symbols and emoji",
                               "may use more bits per character",
                               size=BODY_SIZE, align=LEFT)
            self.stack(items, self.head, align=LEFT)
            self.hide(items)
            self.reveal(t, items, 0, len(items), 0.2)
            t.hold()

        with self.beat("tx_compare") as t:
            self.wipe(t)
            self.big_rule(t, ["MORE CHARACTERS",
                              "MORE BITS PER CHARACTER"], y=0.5)
            t.hold()

        with self.beat("tx_avoid") as t:
            note = self.lines("Avoid saying text is stored as letters.",
                              "It is stored as the character set's codes.",
                              size=LABEL_SIZE, color=GREY)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

    def sound(self):
        with self.beat("sn_intro") as t:
            self.wipe(t)
            self.title(t, "Sound", fraction=0.4)
            t.hold()

        with self.beat("sn_wave") as t:
            wave = self.wave_curve()
            wave.next_to(self.head, DOWN, buff=GAP_MD * 1.4)
            self.play(Create(wave), run_time=t.fill(0.6))
            self.wave = wave
            t.hold()

        with self.beat("sn_adc") as t:
            stems, dots = self.wave_samples(self.wave)
            self.play(Create(stems), run_time=t.fill(0.4))
            self.play(FadeIn(dots), run_time=t.fill(0.2))
            t.hold()

        with self.beat("sn_sample") as t:
            note = self.caption("each measurement is a sample, stored as "
                                "binary", GREY, LABEL_SIZE)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

        with self.beat("sn_rate") as t:
            self.wipe(t)
            self.title(t, "Two different numbers", fraction=0.06)
            self.sound_rows = self.pairs(
                [("sample rate", "samples per second  ·  hertz"),
                 ("sample resolution", "bits for each sample")],
                top=self.head, size=BODY_SIZE, left_x=-6.0, right_x=-1.4,
                cue=SLATE, gap=GAP_MD)
            self.hide(self.sound_rows)
            self.reveal(t, self.sound_rows, 0, 1, 0.5)
            t.hold()

        with self.beat("sn_44k") as t:
            note = self.caption("44 000 Hz  =  44 000 samples every second",
                                GREY, LABEL_SIZE)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.5))
            self.hz_note = note
            t.hold()

        with self.beat("sn_res") as t:
            self.reveal(t, self.sound_rows, 1, 2, 0.25)
            self.recaption(t, self.hz_note,
                           "sample resolution is also called bit depth",
                           GREY, 0.25)
            t.hold()

        with self.beat("sn_increase") as t:
            self.wipe(t)
            rows = self.pairs(
                [("more samples", "the wave captured more often"),
                 ("more bits", "more possible amplitude values"),
                 ("either one", "a bigger file")],
                size=BODY_SIZE, left_x=-5.8, right_x=-1.8, cue=SLATE,
                gap=GAP_MD)
            rows.move_to(UP * 0.2)
            self.hide(rows)
            self.reveal(t, rows, 0, 3, 0.2)
            t.hold()

        with self.beat("sn_separate") as t:
            self.wipe(t)
            self.big_rule(t, ["SAMPLES PER SECOND",
                              "IS NOT BITS PER SAMPLE"], y=0.4)
            t.hold()

    def wave_curve(self, width=9.0, height=1.0):
        """An analogue wave, drawn rather than faded in."""
        import numpy as np
        points = []
        for i in range(161):
            x = -width / 2 + width * i / 160
            y = height * (0.62 * np.sin(2.4 * x) + 0.38 * np.sin(1.1 * x + 1))
            points.append([x, y, 0])
        curve = VGroup()
        line = Line(points[0], points[1], color=SLATE, stroke_width=4)
        line.set_points_as_corners(points)
        curve.add(line)
        return curve

    def wave_samples(self, wave, count=13):
        """Vertical stems at regular intervals — the sampling picture."""
        line = wave[0]
        stems, dots = VGroup(), VGroup()
        base = wave.get_bottom()[1] - GAP_SM
        for i in range(count):
            point = line.point_from_proportion(i / (count - 1))
            stems.add(Line([point[0], base, 0], point, color=GREY,
                           stroke_width=2))
            dots.add(Dot(point, radius=0.055, color=TERRACOTTA))
        return stems, dots

    def sound_size(self):
        with self.beat("sf_intro") as t:
            self.wipe(t)
            self.title(t, "Uncompressed sound file size", fraction=0.4)
            t.hold()

        with self.beat("sf_formula") as t:
            formula = self.calc("rate  x  resolution  x  duration  x  channels",
                                TITLE_SIZE, SLATE)
            formula.next_to(self.head, DOWN, buff=GAP_LG)
            self.play(Write(formula), run_time=t.fill(0.5))
            self.formula = formula
            t.hold()

        with self.beat("sf_again") as t:
            note = self.caption("the answer is in bits", GREY, LABEL_SIZE)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

        with self.beat("sf_example") as t:
            self.wipe(t)
            self.title(t, "Mono  ·  44 000 Hz  ·  16 bits  ·  30 s",
                       fraction=0.4)
            t.hold()

        with self.beat("sf_mono") as t:
            note = self.caption("mono is one channel", GREY, LABEL_SIZE)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

        with self.beat("sf_calc") as t:
            steps = self.lines("44 000  x  16  x  30  x  1",
                               "=  21 120 000 bits",
                               size=TITLE_SIZE, color=CHARCOAL)
            self.stack(steps, self.head)
            self.hide(steps)
            self.reveal(t, steps, 0, 2, 0.3)
            self.sf_steps = steps
            t.hold()

        with self.beat("sf_bytes") as t:
            line = self.calc("/  8   =   2 640 000 bytes", TITLE_SIZE, SAGE)
            line.next_to(self.sf_steps, DOWN, buff=GAP_MD * 1.3)
            self.play(Write(line), run_time=t.fill(0.5))
            t.hold()

        with self.beat("sf_units") as t:
            self.wipe(t)
            self.big_rule(t, ["BITS ARE NOT BYTES"], y=0.5)
            t.hold()

        with self.beat("sf_stereo") as t:
            note = self.caption("stereo  ·  multiply by two channels",
                                GREY)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

    def images(self):
        with self.beat("im_intro") as t:
            self.wipe(t)
            self.title(t, "Images", fraction=0.4)
            t.hold()

        with self.beat("im_grid") as t:
            grid = self.pixel_grid()
            grid.next_to(self.head, DOWN, buff=GAP_MD * 1.2)
            self.play(Create(grid), run_time=t.fill(0.6))
            self.grid = grid
            t.hold()

        with self.beat("im_pixel") as t:
            note = self.caption("every pixel holds a binary colour value",
                                GREY, LABEL_SIZE)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

        with self.beat("im_res") as t:
            self.wipe(t)
            self.title(t, "Two different numbers", fraction=0.06)
            rows = self.pairs(
                [("resolution", "width x height  ·  how many pixels"),
                 ("colour depth", "bits for each pixel")],
                top=self.head, size=BODY_SIZE, left_x=-6.0, right_x=-1.6,
                cue=SLATE, gap=GAP_MD)
            self.hide(rows)
            self.reveal(t, rows, 0, 2, 0.3)
            self.im_rows = rows
            t.hold()

        with self.beat("im_phone") as t:
            note = self.caption("\"1080\" is a pixel count, not a file size",
                                GREY, LABEL_SIZE)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

        with self.beat("im_detail") as t:
            self.wipe(t)
            rows = self.pairs(
                [("more pixels", "finer spatial detail"),
                 ("more bits per pixel", "a larger range of colours"),
                 ("either one", "a bigger file")],
                size=BODY_SIZE, left_x=-6.0, right_x=-1.6, cue=SLATE,
                gap=GAP_MD)
            rows.move_to(UP * 0.2)
            self.hide(rows)
            self.reveal(t, rows, 0, 1, 0.5)
            self.im_more = rows
            t.hold()

        with self.beat("im_depth") as t:
            self.reveal(t, self.im_more, 1, 2, 0.5)
            t.hold()

        with self.beat("im_meta") as t:
            self.reveal(t, self.im_more, 2, 3, 0.2)
            note = self.caption("metadata counts only when the question "
                                "gives you its size", GREY, LABEL_SIZE)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.3))
            t.hold()

    def pixel_grid(self, cols=10, rows=6, cell=0.42):
        """A small bitmap: a grid of pixels, some filled."""
        filled = {(1, 1), (2, 1), (3, 2), (4, 2), (5, 3), (6, 3),
                  (2, 4), (3, 4), (7, 2), (8, 1), (4, 0), (5, 0)}
        grid = VGroup()
        for r in range(rows):
            for c in range(cols):
                square = Rectangle(width=cell, height=cell,
                                   stroke_color=GREY, stroke_width=1.5)
                if (c, r) in filled:
                    square.set_fill(SLATE, opacity=0.85)
                square.move_to([(c - (cols - 1) / 2) * cell,
                                ((rows - 1) / 2 - r) * cell, 0])
                grid.add(square)
        return grid

    def image_size(self):
        with self.beat("if_formula") as t:
            self.wipe(t)
            self.title(t, "Bitmap file size", fraction=0.1)
            formula = self.calc("width  x  height  x  colour depth",
                                TITLE_SIZE, SLATE)
            formula.next_to(self.head, DOWN, buff=GAP_MD * 1.4)
            self.play(Write(formula), run_time=t.fill(0.5))
            self.if_formula = formula
            t.hold()

        with self.beat("if_example") as t:
            spec = self.calc("1920  x  1080  ·  24-bit colour", BODY_SIZE,
                             GREY)
            spec.next_to(self.if_formula, DOWN, buff=GAP_MD * 1.3)
            self.play(Write(spec), run_time=t.fill(0.5))
            self.if_spec = spec
            t.hold()

        with self.beat("if_calc") as t:
            line = self.calc("1920  x  1080  x  24", TITLE_SIZE, CHARCOAL)
            line.next_to(self.if_spec, DOWN, buff=GAP_MD * 1.3)
            self.play(Write(line), run_time=t.fill(0.5))
            self.if_line = line
            t.hold()

        with self.beat("if_bits") as t:
            line = self.calc("=  49 766 400 bits", TITLE_SIZE, CHARCOAL)
            self.foot(line)
            self.play(Write(line), run_time=t.fill(0.5))
            t.hold()

        with self.beat("if_bytes") as t:
            self.wipe(t)
            line = self.calc("/  8   =   6 220 800 bytes", TITLE_SIZE * 1.1,
                             SAGE)
            line.move_to(UP * 0.6)
            self.play(Write(line), run_time=t.fill(0.5))
            t.hold()

        with self.beat("if_errors") as t:
            note = self.lines("forgetting the colour depth",
                              "going to bytes without dividing by 8",
                              size=BODY_SIZE, color=TERRACOTTA)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

    def storage(self):
        with self.beat("st_intro") as t:
            self.wipe(t)
            self.title(t, "Storage units", fraction=0.4)
            t.hold()

        with self.beat("st_binary") as t:
            note = self.caption("this syllabus uses binary multiples")
            self.stack(VGroup(note), self.head)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

        with self.beat("st_ladder") as t:
            self.wipe(t)
            # The deck uses the 1024-based names; the narration says
            # kilobyte, megabyte and gigabyte.
            units = ["bit", "byte", "KiB", "MiB", "GiB"]
            steps = ["/ 8", "/ 1024", "/ 1024", "/ 1024"]
            names = VGroup(*[serif(u, TITLE_SIZE, CHARCOAL) for u in units])
            names.arrange(RIGHT, buff=GAP_LG * 1.5)
            fit(names)
            names.move_to(UP * 0.8)
            arrows, labels = VGroup(), VGroup()
            for a, b, step in zip(names[:-1], names[1:], steps):
                arrow = Arrow(a.get_right(), b.get_left(), color=GREY,
                              buff=GAP_SM * 0.7, stroke_width=3,
                              max_tip_length_to_length_ratio=0.35)
                tag = mono(step, MARGIN_SIZE, GREY)
                tag.next_to(arrow, UP, buff=GAP_SM * 0.5)
                arrows.add(arrow)
                labels.add(tag)
            self.play(Write(names[0]), run_time=t.fill(0.1))
            for arrow, tag, name in zip(arrows, labels, names[1:]):
                self.play(Create(arrow), FadeIn(tag), run_time=t.fill(0.08))
                self.play(Write(name), run_time=t.fill(0.08))
            self.ladder = VGroup(names, arrows, labels)
            t.hold()

        with self.beat("st_1024") as t:
            note = self.caption("1024 at every step above the byte",
                                GREY, LABEL_SIZE)
            note.next_to(self.ladder, DOWN, buff=GAP_LG)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

        with self.beat("st_direction") as t:
            self.wipe(t)
            rows = self.pairs([("smaller to larger", "divide"),
                               ("larger to smaller", "multiply")],
                              size=TITLE_SIZE, left_x=-5.4, right_x=0.6,
                              cue=GREY, answer=SLATE)
            rows.move_to(UP * 0.6)
            self.hide(rows)
            self.reveal(t, rows, 0, 2, 0.3)
            t.hold()

        with self.beat("st_example") as t:
            self.wipe(t)
            steps = self.lines("2 764 800 bytes  /  1024",
                               "=  2700 KiB",
                               size=TITLE_SIZE, color=CHARCOAL)
            steps.move_to(UP * 0.5)
            steps[1].set_color(SAGE)
            self.hide(steps)
            self.reveal(t, steps, 0, 2, 0.3)
            t.hold()

        with self.beat("st_unit") as t:
            self.wipe(t)
            self.big_rule(t, ["WRITE THE UNIT",
                              "AFTER EVERY ANSWER"], y=0.4)
            t.hold()
