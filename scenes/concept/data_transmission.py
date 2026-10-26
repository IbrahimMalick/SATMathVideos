"""Chapter 2 — Data Transmission, the video companion.

Follows the chapter's own order: packets, packet switching, serial against
parallel, direction of transmission, USB, why errors happen, parity,
the four detection methods, automatic repeat request, encryption, review.

The spine is the sender-to-receiver picture. Every topic in this chapter is
something happening to data on its way between two devices, so the same
two end boxes carry the whole lesson and only what sits between them
changes — one wire or four, one arrow or two, a packet or an
acknowledgement.

Everything the screen computes is derived rather than typed: the parity bit
comes from the data bits, every parity in the block comes from its row and
column, and the handshake numbers its own steps. A label that cannot drift
from the thing above it is one fewer place for an error to hide.

Checked before building:

  * 1010110 holds four ones, so even parity adds 0 and odd parity adds 1.
  * flipping two of those bits leaves four or two ones — still even, which
    is exactly the limitation the narration states.
  * every parity in the block diagram is computed, so the single flipped
    bit breaks one row check and one column check and no others.

Where the delivery is loose the screen carries the correct form. Two are
real slips rather than transcription, both confirmed on a second pass with
a larger model:

  * "systematic encryption uses the same secret key" — it is SYMMETRIC
    encryption. The screen says symmetric.
  * "generally fast and suitable to decrypt the data" — symmetric is fast
    and suitable for LARGE AMOUNTS of data, which is the point being made.
    The screen says that.

One point in the plan is missing from the recording and is therefore not on
screen: the challenge of sharing a symmetric key securely. There is no beat
for it, because a card the narration never earns is the one thing this
pipeline exists to prevent.

The rest are transcription artefacts over a delivery that was right:
"this Q" and "a skew" are skew, "ARL" is ARQ, "Pedal transmission" is
parallel, "checksims" and "eco-check" are checksums and echo check, "check
data" is check digit, "speak here and here" is speak and hear, "a secure
reader" is a security risk, and "academy.digitaltearer.net" is
academy.thedigitaltutor.net — which is what the screen shows.

Timing: timings/concept.data_transmission.json
Render: python build/render.py scripts/CH02-data-transmission.md \\
    audio/CH02-data-transmission.m4a
"""

from manim import (
    Create,
    MoveAlongPath,
    FadeIn,
    FadeOut,
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
from components.network import (
    DirectionLink,
    EncryptLane,
    Handshake,
    ParallelLink,
    PacketFrame,
    ParityBlock,
    ParityRow,
    RouteMap,
    SerialLink,
    labelled_key,
    packet_chip,
)
from components.syllabus_map import TopicStrip
from scenes.base import SATScene

FRAME_SAFE = 12.6
FLOOR = -2.9

PARTS = ["Packets", "Serial & parallel", "USB", "Error detection",
         "Repeat request", "Encryption"]

# The data bits the narration reads out. The parity bits are never written
# here — ParityRow derives them, so the screen cannot disagree with itself.
PARITY_DATA = "1010110"

BLOCK_ROWS = ["1011010", "0110101", "1100110", "0011011"]
BLOCK_FAULT = (2, 3)


def fit(mobject, width=FRAME_SAFE):
    if mobject.width > width:
        mobject.scale_to_fit_width(width)
    return mobject


class DataTransmission(SATScene):
    scene_id = "concept.data_transmission"

    def construct(self):
        self.margin = mono("O Level CS 2210 · Data Transmission", MARGIN_SIZE)
        self.margin.to_corner(UP + LEFT, buff=GAP_SM)
        self.add(self.margin)
        self.keep = [self.margin]
        self.strip = None
        self.head = None

        self.opening()
        self.packets()
        self.packet_switching()
        self.serial_parallel()
        self.direction()
        self.usb()
        self.why_errors()
        self.parity()
        self.parity_block()
        self.checksum()
        self.echo_check()
        self.check_digit()
        self.four_methods()
        self.arq()
        self.encryption_basics()
        self.symmetric()
        self.asymmetric()
        self.hybrid()
        self.review()
        self.practice()

    # -------------------------------------------------------------- helpers

    def clear(self, t, *groups, fraction=0.1):
        """Fade out a diagram that was drawn child by child.

        Create() on a group's children adds the children to the scene, not
        the group, so FadeOut(group) removes a mobject the scene never held
        and leaves the drawing exactly where it was. Fade what is present.
        """
        family = set()
        for group in groups:
            family.update(id(m) for m in group.get_family())
        present = [m for m in self.mobjects if id(m) in family]
        if present:
            self.play(*[FadeOut(m) for m in present],
                      run_time=t.fill(fraction))

    def wipe(self, t, fraction=0.05):
        old = [m for m in self.mobjects if m not in self.keep]
        if old:
            self.play(*[FadeOut(m) for m in old], run_time=t.fill(fraction))
        self.head = None

    def title(self, t, text, fraction=0.09, color=CHARCOAL):
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
        """Place under `top`, tightening the group's gaps to clear the floor."""
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

    def place(self, mobject, top=None, buff=GAP_MD, floor=FLOOR):
        """Hang a single mobject under `top`, tightening the gap to clear the floor."""
        for factor in (1.0, 0.9, 0.78, 0.66, 0.55):
            if top is None:
                mobject.move_to(ORIGIN)
            else:
                mobject.next_to(top, DOWN, buff=buff * factor)
            if mobject.get_bottom()[1] >= floor:
                break
        return mobject

    def caption(self, text, color=GREY, size=BODY_SIZE):
        return fit(serif(text, size, color))

    def recaption(self, t, holder, text, color=GREY, fraction=0.2,
                  size=BODY_SIZE):
        """Swap a running line without moving it."""
        nxt = self.caption(text, color, size)
        nxt.move_to(holder)
        self.play(Transform(holder, nxt), run_time=t.fill(fraction))
        return holder

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

    def part(self, t, number, fraction=0.08):
        """Advance the chapter strip along the bottom."""
        if self.strip is None:
            self.strip = TopicStrip(len(PARTS), lit=SLATE, side=0.6)
            self.strip.to_edge(DOWN, buff=GAP_SM * 0.6)
            self.add(self.strip)
            self.keep.append(self.strip)
        self.play(*self.strip.focus(number - 1), run_time=t.fill(fraction))

    def trap(self, t, *texts, fraction=0.3, top=None):
        """The 'do not write this' card. Terracotta, and only one per screen."""
        group = self.lines(*texts, size=LABEL_SIZE, color=TERRACOTTA)
        if top is None:
            self.foot(group)
        else:
            self.stack(group, top)
        self.play(Write(group), run_time=t.fill(fraction))
        return group

    # ------------------------------------------------------------- sections

    def opening(self):
        with self.beat("open") as t:
            head = fit(serif("DATA TRANSMISSION", TITLE_SIZE * 1.25, CHARCOAL))
            sub = serif("Cambridge O Level Computer Science 2210",
                        LABEL_SIZE, GREY)
            chapter = serif("CHAPTER 2", BODY_SIZE, TERRACOTTA)
            card = VGroup(chapter, head, sub).arrange(DOWN, buff=GAP_MD)
            card.move_to(ORIGIN)
            self.play(Write(chapter), run_time=t.fill(0.14))
            self.play(Write(head), run_time=t.fill(0.3))
            self.play(FadeIn(sub), run_time=t.fill(0.2))
            t.hold()

        with self.beat("hook") as t:
            self.wipe(t)
            self.map = RouteMap()
            self.map.move_to(UP * 1.0)
            self.play(Create(self.map.sender), Create(self.map.receiver),
                      run_time=t.fill(0.3))
            self.play(Create(self.map.routes), run_time=t.fill(0.35))
            t.hold()

        with self.beat("hook_q") as t:
            questions = self.lines("different routes?",
                                   "changed along the way?",
                                   "readable if intercepted?",
                                   size=LABEL_SIZE, color=GREY)
            self.hide(questions)
            self.stack(questions, self.map, buff=GAP_MD)
            self.reveal(t, questions, 0, 3, 0.2)
            self.questions = questions
            t.hold()

        with self.beat("map") as t:
            self.wipe(t)
            self.title(t, "What this chapter covers", fraction=0.12)
            rows = self.lines(*[f"{i + 1}   {name}"
                                for i, name in enumerate(PARTS)],
                              size=BODY_SIZE, color=CHARCOAL, align=LEFT)
            self.hide(rows)
            self.stack(rows, self.head, buff=GAP_MD, align=LEFT)
            self.reveal(t, rows, 0, len(PARTS), 0.10)
            self.rows = rows
            t.hold()

        with self.beat("exam_note") as t:
            note = self.caption("listen for the comparisons and the sequences",
                                TERRACOTTA, LABEL_SIZE)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.35))
            t.hold()

    def packets(self):
        with self.beat("part1") as t:
            self.wipe(t)
            self.part(t, 1)
            self.title(t, "Packets", fraction=0.2)
            t.hold()

        with self.beat("packet_def") as t:
            note = self.caption("a small unit of transmitted data", CHARCOAL)
            self.stack(VGroup(note), self.head, buff=GAP_LG)
            self.play(Write(note), run_time=t.fill(0.4))
            self.note = note
            t.hold()

        with self.beat("packet_why") as t:
            self.recaption(t, self.note,
                           "a large file is divided so links can be shared",
                           CHARCOAL, 0.4)
            t.hold()

        with self.beat("packet_routes") as t:
            self.recaption(t, self.note,
                           "a busy route sends packets another way",
                           CHARCOAL, 0.4)
            t.hold()

        with self.beat("three_parts") as t:
            self.wipe(t)
            self.title(t, "Three sections", fraction=0.14)
            self.frame = PacketFrame()
            self.place(self.frame, self.head, buff=GAP_LG)
            self.play(Create(self.frame.boxes), run_time=t.fill(0.3))
            self.play(Write(self.frame.labels), run_time=t.fill(0.3))
            t.hold()

        with self.beat("header") as t:
            self.play(*self.frame.light(0), run_time=t.fill(0.2))
            caption = self.caption("control information", TERRACOTTA,
                                   LABEL_SIZE)
            self.place(caption, self.frame, buff=GAP_MD * 1.2)
            self.play(Write(caption), run_time=t.fill(0.3))
            self.section_note = caption
            t.hold()

        with self.beat("header_list") as t:
            body = self.frame.contents(0, ["destination address",
                                           "originator address",
                                           "packet number"])
            self.hide(body)
            self.place(body, self.section_note, buff=GAP_MD * 0.7)
            self.reveal(t, body, 0, 3, 0.2)
            self.body = body
            t.hold()

        with self.beat("payload") as t:
            self.play(FadeOut(self.body), *self.frame.light(1),
                      run_time=t.fill(0.2))
            self.recaption(t, self.section_note,
                           "the useful data being carried", TERRACOTTA, 0.3,
                           LABEL_SIZE)
            t.hold()

        with self.beat("trailer") as t:
            self.play(*self.frame.light(2), run_time=t.fill(0.2))
            self.recaption(t, self.section_note,
                           "error checking, and an end marker", TERRACOTTA,
                           0.3, LABEL_SIZE)
            t.hold()

        with self.beat("exam_point") as t:
            self.play(*self.frame.settle(), FadeOut(self.section_note),
                      run_time=t.fill(0.2))
            self.play(*self.frame.light(0), run_time=t.fill(0.2))
            note = self.caption("the address and the packet number are HEADER",
                                CHARCOAL, LABEL_SIZE)
            self.place(note, self.frame, buff=GAP_MD * 1.3)
            self.play(Write(note), run_time=t.fill(0.35))
            self.section_note = note
            t.hold()

        with self.beat("exam_point2") as t:
            self.play(*self.frame.light(1), run_time=t.fill(0.2))
            self.recaption(t, self.section_note,
                           "the payload carries the useful data", CHARCOAL,
                           0.35, LABEL_SIZE)
            t.hold()

    def packet_switching(self):
        with self.beat("switching") as t:
            self.wipe(t)
            self.title(t, "Packet switching", fraction=0.2)
            t.hold()

        with self.beat("ps_divide") as t:
            self.map = RouteMap()
            self.place(self.map, self.head, buff=GAP_MD * 0.9)
            self.play(Create(self.map.sender), Create(self.map.receiver),
                      Create(self.map.routes), run_time=t.fill(0.3))
            self.chips = self.map.dock([packet_chip(i + 1) for i in range(3)])
            self.play(*[FadeIn(c) for c in self.chips], run_time=t.fill(0.3))
            t.hold()

        with self.beat("ps_add") as t:
            note = self.caption("each gets a header, payload and trailer",
                                GREY, LABEL_SIZE)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.4))
            self.note = note
            t.hold()

        with self.beat("ps_route") as t:
            self.recaption(t, self.note,
                           "a router reads the destination address",
                           GREY, 0.4, LABEL_SIZE)
            t.hold()

        with self.beat("ps_differ") as t:
            # Three packets, three routes, sent in order 1, 2, 3. One
            # play each: a play per hop would cost the pacing floor per
            # router and overrun a beat the narration keeps short.
            #
            # Each lands in its own slot, and in an order the routes
            # justify rather than the order they were sent — which is the
            # whole point of the next two beats.
            self.slots = self.map.slots(
                len(self.chips),
                at=self.map.receiver[0].get_bottom() + DOWN * 1.15)
            self.landing = [2, 0, 1]
            for i, chip in enumerate(self.chips):
                wire = self.map.wire(i, start=chip.get_center(),
                                     end=self.slots[self.landing[i]])
                self.play(MoveAlongPath(chip, wire),
                          *self.map.light_route(i), run_time=t.fill(0.24))
            self.play(*self.map.dim_routes(), run_time=t.fill(0.08))
            t.hold()

        with self.beat("ps_arrive") as t:
            self.recaption(t, self.note,
                           "so they can arrive out of order",
                           TERRACOTTA, 0.4, LABEL_SIZE)
            t.hold()

        with self.beat("ps_reorder") as t:
            # The packet numbers sort them. The ordering is read off the
            # chips' own labels, so the picture cannot end up claiming an
            # order the numbers do not support.
            by_number = sorted(self.chips, key=lambda chip: chip[1].text)
            self.play(*[chip.animate.move_to(self.slots[i])
                        for i, chip in enumerate(by_number)],
                      run_time=t.fill(0.35))
            self.recaption(t, self.note,
                           "the packet numbers put them back in order",
                           SAGE, 0.25, LABEL_SIZE)
            t.hold()

        with self.beat("ps_missing") as t:
            self.recaption(t, self.note,
                           "a missing packet is requested again",
                           GREY, 0.4, LABEL_SIZE)
            t.hold()

        with self.beat("ps_reconstruct") as t:
            self.recaption(t, self.note,
                           "then the original data is reconstructed",
                           SAGE, 0.4, LABEL_SIZE)
            t.hold()

        with self.beat("ps_sequence") as t:
            self.wipe(t)
            self.title(t, "The sequence", fraction=0.12)
            steps = self.lines("1   divide the data into packets",
                               "2   add the packet information",
                               "3   route the packets",
                               "4   reorder them by packet number",
                               "5   reconstruct the original message",
                               size=BODY_SIZE, color=CHARCOAL, align=LEFT)
            self.hide(steps)
            # A trap card lands under this list in the next beat, so the
            # list stops well short of the floor.
            self.stack(steps, self.head, buff=GAP_MD, align=LEFT, floor=-1.3)
            self.reveal(t, steps, 0, 5, 0.13)
            self.steps = steps
            t.hold()

        with self.beat("ps_trap") as t:
            self.trap(t, "packets do not choose their own routes",
                      "routers make the routing decisions", fraction=0.4)
            t.hold()

        with self.beat("ps_why") as t:
            self.wipe(t)
            self.title(t, "Why it helps", fraction=0.12)
            good = self.lines("many users share the network capacity",
                              "data can avoid congestion or a failed link",
                              size=BODY_SIZE, color=SAGE)
            self.hide(good)
            self.stack(good, self.head, buff=GAP_MD)
            self.reveal(t, good, 0, 2, 0.25)
            self.good = good
            t.hold()

        with self.beat("ps_limits") as t:
            bad = self.lines("it does not guarantee the shortest route",
                             "and it does not guarantee arrival in order",
                             size=LABEL_SIZE, color=TERRACOTTA)
            self.hide(bad)
            self.stack(bad, self.good, buff=GAP_LG)
            self.reveal(t, bad, 0, 2, 0.25)
            t.hold()

    def serial_parallel(self):
        with self.beat("part2") as t:
            self.wipe(t)
            self.part(t, 2)
            self.title(t, "Serial and parallel", fraction=0.2)
            t.hold()

        with self.beat("serial") as t:
            self.link = SerialLink()
            self.link.move_to(UP * 0.35)
            self.play(Create(self.link.left), Create(self.link.right),
                      Create(self.link.wire), run_time=t.fill(0.25))
            self.play(Write(self.link.bits), run_time=t.fill(0.3))
            note = self.caption("one bit at a time, one channel", SLATE,
                                LABEL_SIZE)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.2))
            self.note = note
            t.hold()

        with self.beat("parallel") as t:
            self.clear(t, self.link, fraction=0.1)
            self.par = ParallelLink()
            self.par.move_to(UP * 0.35)
            self.play(Create(self.par.left), Create(self.par.right),
                      Create(self.par.wires), run_time=t.fill(0.25))
            self.play(Write(self.par.bits), run_time=t.fill(0.25))
            self.recaption(t, self.note,
                           "several bits at once, several channels",
                           SLATE, 0.2, LABEL_SIZE)
            t.hold()

        with self.beat("wires") as t:
            self.recaption(t, self.note, "more channels means more wires",
                           GREY, 0.4, LABEL_SIZE)
            t.hold()

        with self.beat("not_same_time") as t:
            self.play(*self.par.skew(), run_time=t.fill(0.45))
            t.hold()

        with self.beat("skew") as t:
            self.rule = self.par.brace_skew()
            self.play(Create(self.rule), run_time=t.fill(0.2))
            self.recaption(t, self.note, "SKEW", TERRACOTTA, 0.3, TITLE_SIZE)
            t.hold()

        with self.beat("skew_group") as t:
            self.recaption(t, self.note,
                           "the receiver can group the bits wrongly",
                           TERRACOTTA, 0.4, LABEL_SIZE)
            t.hold()

        with self.beat("skew_distance") as t:
            self.recaption(t, self.note,
                           "worse over distance, worse at speed",
                           TERRACOTTA, 0.4, LABEL_SIZE)
            t.hold()

        with self.beat("serial_wins") as t:
            self.clear(t, self.par, self.rule, fraction=0.1)
            self.link = SerialLink()
            self.link.move_to(UP * 0.35)
            self.play(Create(self.link.wire), Create(self.link.left),
                      Create(self.link.right), Write(self.link.bits),
                      run_time=t.fill(0.3))
            self.recaption(t, self.note,
                           "fewer wires, no skew, better over distance",
                           SAGE, 0.3, LABEL_SIZE)
            t.hold()

        with self.beat("recommend") as t:
            self.wipe(t)
            self.title(t, "Recommending a method", fraction=0.12)
            t.hold()

        with self.beat("recommend_why") as t:
            note = self.caption("naming the method is not the answer",
                                TERRACOTTA, BODY_SIZE)
            self.stack(VGroup(note), self.head, buff=GAP_LG)
            self.play(Write(note), run_time=t.fill(0.4))
            self.note = note
            t.hold()

        with self.beat("recommend_eg") as t:
            answer = self.lines("a long link between two buildings:",
                                "serial — fewer wires, and no skew",
                                "between multiple channels",
                                size=LABEL_SIZE, color=CHARCOAL)
            self.hide(answer)
            self.stack(answer, self.note, buff=GAP_LG * 0.8, floor=-1.3)
            self.reveal(t, answer, 0, 3, 0.2)
            self.answer = answer
            t.hold()

        with self.beat("recommend_marks") as t:
            marks = self.caption("the mark is the reason tied to the scenario",
                                 SAGE, LABEL_SIZE)
            self.foot(marks)
            self.play(Write(marks), run_time=t.fill(0.4))
            t.hold()

    def direction(self):
        with self.beat("direction") as t:
            self.wipe(t)
            self.title(t, "Direction of transmission", fraction=0.2)
            t.hold()

        with self.beat("simplex") as t:
            self.dir = DirectionLink("SENSOR", "CONTROL")
            self.dir.move_to(UP * 0.5)
            self.play(Create(self.dir.left), Create(self.dir.right),
                      run_time=t.fill(0.2))
            self.play(Create(self.dir.forward()), *self.dir.light([0]),
                      run_time=t.fill(0.25))
            note = self.caption("SIMPLEX — one direction only", CHARCOAL,
                                LABEL_SIZE)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.25))
            self.note = note
            t.hold()

        with self.beat("simplex_eg") as t:
            self.recaption(t, self.note,
                           "a sensor sends readings and gets nothing back",
                           GREY, 0.4, LABEL_SIZE)
            t.hold()

        with self.beat("half") as t:
            self.clear(t, self.dir, fraction=0.08)
            self.dir = DirectionLink("RADIO A", "RADIO B")
            self.dir.move_to(UP * 0.5)
            self.play(Create(self.dir.left), Create(self.dir.right),
                      Create(self.dir.arrows), run_time=t.fill(0.25))
            # Both directions exist; they take turns, so one lights at a time.
            self.play(*self.dir.light([0]), run_time=t.fill(0.14))
            self.play(*self.dir.light([1]), run_time=t.fill(0.14))
            self.recaption(t, self.note,
                           "HALF-DUPLEX — both ways, taking turns",
                           CHARCOAL, 0.2, LABEL_SIZE)
            t.hold()

        with self.beat("half_eg") as t:
            self.play(*self.dir.light([0]), run_time=t.fill(0.14))
            self.play(*self.dir.light([1]), run_time=t.fill(0.14))
            self.recaption(t, self.note, "a push-to-talk walkie-talkie",
                           GREY, 0.2, LABEL_SIZE)
            t.hold()

        with self.beat("full") as t:
            self.clear(t, self.dir, fraction=0.08)
            self.dir = DirectionLink("CALLER", "CALLER")
            self.dir.move_to(UP * 0.5)
            self.play(Create(self.dir.left), Create(self.dir.right),
                      run_time=t.fill(0.2))
            self.play(Create(self.dir.arrows), *self.dir.light([0, 1]),
                      run_time=t.fill(0.25))
            self.recaption(t, self.note,
                           "FULL-DUPLEX — both ways at the same time",
                           CHARCOAL, 0.2, LABEL_SIZE)
            t.hold()

        with self.beat("full_eg") as t:
            self.recaption(t, self.note,
                           "a telephone call: both speak and both hear",
                           GREY, 0.4, LABEL_SIZE)
            t.hold()

        with self.beat("memory") as t:
            self.wipe(t)
            self.title(t, "The memory check", fraction=0.12)
            rows = self.lines("simplex          one way",
                              "half-duplex      two ways, taking turns",
                              "full-duplex      two ways, at the same time",
                              size=BODY_SIZE, color=CHARCOAL, align=LEFT)
            self.hide(rows)
            self.stack(rows, self.head, buff=GAP_LG * 0.75, align=LEFT)
            self.check = rows
            t.hold()

        with self.beat("mem_simplex") as t:
            self.reveal(t, self.check, 0, 1, 0.45)
            t.hold()

        with self.beat("mem_half") as t:
            self.reveal(t, self.check, 1, 2, 0.45)
            t.hold()

        with self.beat("mem_full") as t:
            self.reveal(t, self.check, 2, 3, 0.45)
            t.hold()

        with self.beat("dir_trap") as t:
            self.trap(t, "half-duplex is not one way",
                      "both sides send — just not at once", fraction=0.4)
            t.hold()

        with self.beat("dir_method") as t:
            self.wipe(t)
            self.title(t, "Choosing a mode", fraction=0.1)
            steps = self.lines("1   one direction, or both?",
                               "2   if both — at the same time?",
                               "3   name the mode",
                               "4   justify it from the scenario",
                               size=BODY_SIZE, color=CHARCOAL, align=LEFT)
            self.hide(steps)
            self.stack(steps, self.head, buff=GAP_MD, align=LEFT)
            self.reveal(t, steps, 0, 4, 0.19)
            t.hold()

    def usb(self):
        with self.beat("part3") as t:
            self.wipe(t)
            self.part(t, 3)
            self.title(t, "USB", fraction=0.14)
            sub = self.caption("Universal Serial Bus", GREY, BODY_SIZE)
            self.stack(VGroup(sub), self.head, buff=GAP_MD)
            self.play(Write(sub), run_time=t.fill(0.3))
            self.note = sub
            t.hold()

        with self.beat("usb_def") as t:
            self.recaption(t, self.note,
                           "a standard serial interface for connecting devices",
                           CHARCOAL, 0.45, LABEL_SIZE)
            t.hold()

        with self.beat("usb_seq") as t:
            self.wipe(t)
            self.title(t, "Connecting a device", fraction=0.1)
            steps = self.lines("1   the host detects the device",
                               "2   the operating system loads a driver",
                               "3   host and device use the USB protocol",
                               "4   data transfers serially, with checking",
                               size=BODY_SIZE, color=CHARCOAL, align=LEFT)
            self.hide(steps)
            self.stack(steps, self.head, buff=GAP_MD, align=LEFT)
            self.usb_steps = steps
            self.reveal(t, steps, 0, 1, 0.3)
            t.hold()

        with self.beat("usb_driver") as t:
            self.reveal(t, self.usb_steps, 1, 2, 0.5)
            t.hold()

        with self.beat("usb_proto") as t:
            self.reveal(t, self.usb_steps, 2, 4, 0.3)
            t.hold()

        with self.beat("usb_benefits") as t:
            self.wipe(t)
            self.title(t, "Benefits", fraction=0.1, color=SAGE)
            rows = self.lines("a widely supported standard",
                              "plug-and-play detection",
                              "carries power as well as data",
                              "connect or disconnect while running",
                              size=BODY_SIZE, color=CHARCOAL, align=LEFT)
            self.hide(rows)
            self.stack(rows, self.head, buff=GAP_MD, align=LEFT)
            self.benefits = rows
            self.reveal(t, rows, 0, 1, 0.4)
            t.hold()

        with self.beat("usb_pnp") as t:
            self.reveal(t, self.benefits, 1, 2, 0.5)
            t.hold()

        # The written plan puts "it also supplies power" straight after the
        # definition, but the delivery holds it back to here and names it as
        # a benefit. The beat follows the delivery, not the plan.
        with self.beat("usb_power") as t:
            self.reveal(t, self.benefits, 2, 3, 0.5)
            t.hold()

        with self.beat("usb_hot") as t:
            self.reveal(t, self.benefits, 3, 4, 0.5)
            t.hold()

        with self.beat("usb_limits") as t:
            self.wipe(t)
            self.title(t, "Limitations", fraction=0.1, color=TERRACOTTA)
            rows = self.lines("performance depends on the version",
                              "cable length is limited",
                              "a shared hub shares the bandwidth",
                              "connectors may need adapters",
                              "a malicious device is a security risk",
                              size=BODY_SIZE, color=CHARCOAL, align=LEFT)
            self.hide(rows)
            self.stack(rows, self.head, buff=GAP_MD, align=LEFT)
            self.limits = rows
            self.reveal(t, rows, 0, 2, 0.22)
            t.hold()

        with self.beat("usb_bandwidth") as t:
            self.reveal(t, self.limits, 2, 5, 0.18)
            t.hold()

        with self.beat("usb_serial") as t:
            self.wipe(t)
            self.title(t, "One thing to hold", fraction=0.1)
            card = self.lines("USB is SERIAL", size=TITLE_SIZE,
                              color=TERRACOTTA)
            self.stack(card, self.head, buff=GAP_LG)
            self.play(Write(card), run_time=t.fill(0.3))
            note = self.caption("never describe USB as parallel transmission",
                                GREY, LABEL_SIZE)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.3))
            t.hold()

    def why_errors(self):
        with self.beat("part4") as t:
            self.wipe(t)
            self.part(t, 4)
            self.title(t, "Why errors happen", fraction=0.2)
            t.hold()

        with self.beat("causes") as t:
            rows = self.lines("electrical noise",
                              "electromagnetic interference",
                              "a weak signal",
                              "damaged transmission media",
                              size=BODY_SIZE, color=CHARCOAL, align=LEFT)
            self.hide(rows)
            self.stack(rows, self.head, buff=GAP_MD, align=LEFT)
            self.reveal(t, rows, 0, 4, 0.2)
            t.hold()

        with self.beat("bit_change") as t:
            self.wipe(t)
            self.title(t, "Three ways data goes wrong", fraction=0.1)
            rows = self.lines("a bit changes — a 0 arrives as a 1",
                              "data is lost — bits never arrive",
                              "extra data appears",
                              size=BODY_SIZE, color=CHARCOAL, align=LEFT)
            self.hide(rows)
            self.stack(rows, self.head, buff=GAP_LG * 0.8, align=LEFT,
                       floor=-1.5)
            self.ways = rows
            self.reveal(t, rows, 0, 1, 0.4)
            t.hold()

        with self.beat("data_lost") as t:
            self.reveal(t, self.ways, 1, 2, 0.5)
            t.hold()

        with self.beat("data_extra") as t:
            self.reveal(t, self.ways, 2, 3, 0.5)
            t.hold()

        with self.beat("need_check") as t:
            note = self.caption("so the receiver needs a way to check",
                                SLATE, LABEL_SIZE)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.4))
            t.hold()

        with self.beat("detect_vs_correct") as t:
            self.wipe(t)
            self.title(t, "Detection is not correction", fraction=0.12)
            rows = self.lines("detection says the data is probably wrong",
                              "it does not repair the data",
                              "recovery needs retransmission",
                              size=BODY_SIZE, color=CHARCOAL)
            self.hide(rows)
            self.stack(rows, self.head, buff=GAP_LG * 0.8)
            self.detect = rows
            self.reveal(t, rows, 0, 2, 0.3)
            t.hold()

        with self.beat("detect_note") as t:
            self.reveal(t, self.detect, 2, 3, 0.5)
            t.hold()

    def parity(self):
        with self.beat("parity") as t:
            self.wipe(t)
            self.title(t, "Parity check", fraction=0.2)
            t.hold()

        with self.beat("parity_def") as t:
            note = self.caption("a bit added so the count of ones follows a rule",
                                CHARCOAL, LABEL_SIZE)
            self.stack(VGroup(note), self.head, buff=GAP_MD * 1.2)
            self.play(Write(note), run_time=t.fill(0.4))
            self.note = note
            t.hold()

        with self.beat("even") as t:
            rows = self.lines("even parity      the total must be even",
                              "odd parity       the total must be odd",
                              size=BODY_SIZE, color=CHARCOAL, align=LEFT)
            self.hide(rows)
            self.stack(rows, self.note, buff=GAP_LG * 0.9, align=LEFT)
            self.schemes = rows
            self.reveal(t, rows, 0, 1, 0.4)
            t.hold()

        with self.beat("odd") as t:
            self.reveal(t, self.schemes, 1, 2, 0.5)
            t.hold()

        with self.beat("example") as t:
            self.wipe(t)
            self.title(t, "Worked example", fraction=0.1)
            # Data bits only — the parity cell arrives when it is earned.
            self.row = ParityRow(PARITY_DATA, "even", show_parity=False)
            self.place(self.row, self.head, buff=GAP_LG * 0.9)
            self.play(Create(self.row.cells), run_time=t.fill(0.25))
            self.play(Write(self.row.values), run_time=t.fill(0.3))
            t.hold()

        with self.beat("count_ones") as t:
            self.play(*self.row.light_ones(), run_time=t.fill(0.3))
            count = self.caption(f"{self.row.ones} ones", TERRACOTTA,
                                 BODY_SIZE)
            self.place(count, self.row, buff=GAP_MD * 1.2)
            self.play(Write(count), run_time=t.fill(0.3))
            self.count = count
            t.hold()

        with self.beat("even_bit") as t:
            even = ParityRow(PARITY_DATA, "even")
            even.move_to(self.row)
            self.clear(t, self.row, self.count, fraction=0.1)
            self.play(Create(even.cells), Write(even.values),
                      run_time=t.fill(0.25))
            line = even.count_line()
            self.place(line, even, buff=GAP_MD * 1.2)
            self.play(Write(line), run_time=t.fill(0.3))
            self.row, self.count = even, line
            t.hold()

        with self.beat("odd_bit") as t:
            odd = ParityRow(PARITY_DATA, "odd")
            odd.move_to(self.row)
            line = odd.count_line()
            self.place(line, odd, buff=GAP_MD * 1.2)
            self.clear(t, self.row, self.count, fraction=0.1)
            self.play(Create(odd.cells), Write(odd.values),
                      run_time=t.fill(0.25))
            self.play(Write(line), run_time=t.fill(0.3))
            self.row, self.count = odd, line
            t.hold()

        with self.beat("receiver_counts") as t:
            note = self.caption("the receiver counts again and compares",
                                SAGE, LABEL_SIZE)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.4))
            t.hold()

        with self.beat("parity_limit") as t:
            self.wipe(t)
            self.title(t, "The limitation", fraction=0.1)
            rows = self.lines("an odd number of changed bits is detected",
                              "an even number can slip through",
                              size=BODY_SIZE, color=CHARCOAL)
            self.hide(rows)
            # Natural spacing: stack() only ever tightens, so a floor it
            # cannot reach squeezes the gap to nothing instead of holding
            # the lines high. These two lines fit as they are.
            self.stack(rows, self.head, buff=GAP_MD * 0.9)
            self.limit = rows
            self.reveal(t, rows, 0, 2, 0.3)
            t.hold()

        with self.beat("two_bits") as t:
            # Two bits flip and the count stays even: the parity still
            # checks out, which is the failure the syllabus wants named.
            # The parity cells are deliberately quiet here. The one thing
            # to look at is which two bits changed, so they get the
            # terracotta and nothing else does.
            changed = (0, 2)
            clean = ParityRow(PARITY_DATA, "even", accent=SLATE)
            flipped_data = list(PARITY_DATA)
            for i in changed:
                flipped_data[i] = "0" if flipped_data[i] == "1" else "1"
            dirty = ParityRow("".join(flipped_data), "even", accent=SLATE)
            pair = VGroup(clean, dirty).arrange(DOWN, buff=GAP_MD * 1.1)
            self.place(pair, self.limit, buff=GAP_MD, floor=-1.9)
            self.play(Create(clean.cells), Write(clean.values),
                      run_time=t.fill(0.2))
            self.play(Create(dirty.cells), Write(dirty.values),
                      run_time=t.fill(0.2))
            self.play(*[dirty.values[i].animate.set_color(TERRACOTTA)
                        for i in changed],
                      *[dirty.cells[i].animate.set_stroke(TERRACOTTA)
                        for i in changed],
                      run_time=t.fill(0.15))
            still = self.caption("still even — undetected", TERRACOTTA,
                                 LABEL_SIZE)
            self.foot(still)
            self.play(Write(still), run_time=t.fill(0.25))
            t.hold()

    def parity_block(self):
        with self.beat("block") as t:
            self.wipe(t)
            self.title(t, "Parity block check", fraction=0.12)
            self.block = ParityBlock(BLOCK_ROWS, "even")
            self.place(self.block, self.head, buff=GAP_MD * 1.1, floor=-1.9)
            self.play(Create(self.block), run_time=t.fill(0.45))
            t.hold()

        with self.beat("block_rows") as t:
            note = self.caption("a parity bit on every row, and every column",
                                GREY, LABEL_SIZE)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.4))
            self.note = note
            t.hold()

        with self.beat("block_single") as t:
            row, col = BLOCK_FAULT
            self.play(*self.block.flip(row, col), run_time=t.fill(0.2))
            self.play(*self.block.row_check(row), run_time=t.fill(0.2))
            self.play(*self.block.col_check(col), run_time=t.fill(0.2))
            self.recaption(t, self.note,
                           "one row fails, and one column fails",
                           TERRACOTTA, 0.2, LABEL_SIZE)
            t.hold()

        with self.beat("block_locate") as t:
            row, col = BLOCK_FAULT
            cross = self.block.crosshair(row, col)
            self.play(Create(cross), run_time=t.fill(0.25))
            self.recaption(t, self.note,
                           "they meet on the changed bit", SAGE, 0.3,
                           LABEL_SIZE)
            t.hold()

    def checksum(self):
        with self.beat("four") as t:
            self.wipe(t)
            self.title(t, "Four methods", fraction=0.1)
            rows = self.lines("parity        checksum",
                              "echo check    check digit",
                              size=TITLE_SIZE, color=SLATE)
            self.stack(rows, self.head, buff=GAP_LG)
            self.play(Write(rows), run_time=t.fill(0.5))
            t.hold()

        with self.beat("checksum") as t:
            self.wipe(t)
            self.title(t, "Checksum", fraction=0.1)
            steps = self.lines("the sender calculates a value from the block",
                               "it travels with the data",
                               size=BODY_SIZE, color=CHARCOAL, align=LEFT)
            self.hide(steps)
            self.stack(steps, self.head, buff=GAP_MD, align=LEFT)
            self.sum_steps = steps
            self.reveal(t, steps, 0, 2, 0.25)
            t.hold()

        with self.beat("checksum_recv") as t:
            more = self.lines("the receiver repeats the calculation",
                              "the two values are compared",
                              size=BODY_SIZE, color=CHARCOAL, align=LEFT)
            self.hide(more)
            self.stack(more, self.sum_steps, buff=GAP_MD, align=LEFT)
            self.reveal(t, more, 0, 2, 0.25)
            t.hold()

        with self.beat("checksum_limit") as t:
            note = self.lines("stronger than one parity bit —",
                              "but a match is not a guarantee",
                              size=LABEL_SIZE, color=TERRACOTTA)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.4))
            t.hold()

    def echo_check(self):
        with self.beat("echo") as t:
            self.wipe(t, 0.06)
            self.title(t, "Echo check", fraction=0.08)
            self.dir = DirectionLink("SENDER", "RECEIVER")
            self.dir.move_to(UP * 0.5)
            self.play(Create(self.dir.left), Create(self.dir.right),
                      Create(self.dir.forward()), *self.dir.light([0]),
                      run_time=t.fill(0.22))
            out = self.dir.label_arrow(0, "data")
            self.play(Write(out), run_time=t.fill(0.12))
            # The echo goes back inside the same sentence, so it is the same
            # beat — splitting it would put the return arrow on a clause
            # about something else.
            self.play(Create(self.dir.back()), *self.dir.light([1]),
                      run_time=t.fill(0.18))
            back = self.dir.label_arrow(1, "echoed back")
            self.play(Write(back), run_time=t.fill(0.15))
            t.hold()

        with self.beat("echo_compare") as t:
            note = self.caption("the sender compares the copy with the original",
                                CHARCOAL, LABEL_SIZE)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.4))
            self.note = note
            t.hold()

        with self.beat("echo_retx") as t:
            self.recaption(t, self.note, "they differ, so send it again",
                           SAGE, 0.45, LABEL_SIZE)
            t.hold()

        with self.beat("echo_cost") as t:
            self.recaption(t, self.note,
                           "sent twice: slower, and the echo can corrupt too",
                           TERRACOTTA, 0.45, LABEL_SIZE)
            t.hold()

    def check_digit(self):
        with self.beat("digit") as t:
            self.wipe(t)
            self.title(t, "Check digit", fraction=0.1)
            number = VGroup(serif("978140884873", TITLE_SIZE, CHARCOAL),
                            serif("9", TITLE_SIZE, TERRACOTTA))
            number.arrange(RIGHT, buff=GAP_SM * 0.7)
            fit(number, 9.0)
            self.place(number, self.head, buff=GAP_LG * 0.9)
            self.play(Write(number[0]), run_time=t.fill(0.3))
            self.play(Write(number[1]), run_time=t.fill(0.2))
            note = self.caption("an identifier: an ISBN, a bar code", GREY,
                                LABEL_SIZE)
            self.place(note, number, buff=GAP_MD)
            self.play(Write(note), run_time=t.fill(0.2))
            self.note = note
            t.hold()

        with self.beat("digit_calc") as t:
            self.recaption(t, self.note,
                           "calculated from the other digits, then rechecked",
                           CHARCOAL, 0.45, LABEL_SIZE)
            t.hold()

    def four_methods(self):
        with self.beat("digit_trap") as t:
            self.wipe(t)
            self.title(t, "Keep the uses distinct", fraction=0.1)
            rows = self.lines("parity         one bit, one rule",
                              "checksum       a value over a block",
                              "echo check     send it back and compare",
                              "check digit    identifiers and data entry",
                              size=BODY_SIZE, color=CHARCOAL, align=LEFT)
            self.hide(rows)
            self.stack(rows, self.head, buff=GAP_MD, align=LEFT, floor=-1.3)
            self.reveal(t, rows, 0, 4, 0.18)
            self.methods = rows
            t.hold()

        with self.beat("digit_not") as t:
            note = self.lines("not encryption — and no evidence",
                              "of who entered the data",
                              size=LABEL_SIZE, color=TERRACOTTA)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.45))
            t.hold()

    def arq(self):
        with self.beat("part5") as t:
            self.wipe(t)
            self.part(t, 5)
            self.title(t, "Automatic repeat request", fraction=0.14)
            sub = self.caption("ARQ", GREY, BODY_SIZE)
            self.stack(VGroup(sub), self.head, buff=GAP_MD * 0.8)
            self.play(Write(sub), run_time=t.fill(0.25))
            t.hold()

        with self.beat("arq_def") as t:
            self.wipe(t)
            rows = self.lines("error detection",
                              "+  acknowledgements",
                              "+  a timeout",
                              size=BODY_SIZE, color=CHARCOAL, align=LEFT)
            self.hide(rows)
            self.stack(rows, None, buff=GAP_MD, align=LEFT)
            self.reveal(t, rows, 0, 3, 0.25)
            t.hold()

        with self.beat("arq_send") as t:
            self.wipe(t)
            self.shake = Handshake([
                ("down", "data block + error check"),
                ("up", "positive acknowledgement"),
                ("up", "negative acknowledgement"),
                ("down", "retransmit after a NAK"),
                ("down", "retransmit on timeout"),
            ])
            self.shake.move_to(DOWN * 0.15)
            self.shake.hide_steps()
            self.play(Create(self.shake.spines), Write(self.shake.heads),
                      run_time=t.fill(0.2))
            self.play(FadeIn(self.shake.show_step(0)), run_time=t.fill(0.35))
            t.hold()

        with self.beat("arq_timer") as t:
            timer = self.shake.timer(0, "timer starts", color=TERRACOTTA)
            self.play(Write(timer), run_time=t.fill(0.4))
            t.hold()

        with self.beat("arq_check") as t:
            note = self.caption("the receiver checks the block", GREY,
                                LABEL_SIZE)
            self.foot(note, buff=GAP_MD * 0.7)
            self.play(Write(note), run_time=t.fill(0.4))
            self.note = note
            t.hold()

        with self.beat("arq_ack") as t:
            self.play(FadeIn(self.shake.show_step(1)), run_time=t.fill(0.3))
            self.recaption(t, self.note, "correct: a positive acknowledgement",
                           SAGE, 0.3, LABEL_SIZE)
            t.hold()

        with self.beat("arq_nak") as t:
            self.play(FadeIn(self.shake.show_step(2)), run_time=t.fill(0.4))
            self.recaption(t, self.note, "an error: a negative acknowledgement",
                           TERRACOTTA, 0.3, LABEL_SIZE)
            t.hold()

        with self.beat("arq_retx") as t:
            self.play(FadeIn(self.shake.show_step(3)), run_time=t.fill(0.4))
            t.hold()

        with self.beat("arq_timeout") as t:
            self.play(FadeIn(self.shake.show_step(4)), run_time=t.fill(0.4))
            self.recaption(t, self.note, "no acknowledgement: send it again",
                           TERRACOTTA, 0.3, LABEL_SIZE)
            t.hold()

        with self.beat("arq_repeat") as t:
            self.recaption(t, self.note,
                           "until it arrives, or a set limit is reached",
                           GREY, 0.45, LABEL_SIZE)
            t.hold()

        with self.beat("arq_why") as t:
            self.wipe(t)
            self.title(t, "Why the timeout matters", fraction=0.12)
            rows = self.lines("the data block can be lost",
                              "the acknowledgement can be lost too",
                              size=BODY_SIZE, color=CHARCOAL)
            self.hide(rows)
            self.stack(rows, self.head, buff=GAP_LG * 0.8)
            self.reveal(t, rows, 0, 2, 0.3)
            self.why = rows
            t.hold()

        with self.beat("arq_forever") as t:
            note = self.caption("without a timeout the sender waits forever",
                                TERRACOTTA, BODY_SIZE)
            self.stack(VGroup(note), self.why, buff=GAP_LG * 0.9)
            self.play(Write(note), run_time=t.fill(0.45))
            t.hold()

        with self.beat("arq_answer") as t:
            self.wipe(t)
            self.title(t, "The sequence to write", fraction=0.1)
            steps = self.lines("1   send the block",
                               "2   check it",
                               "3   acknowledge successful receipt",
                               "4   retransmit after an error or a timeout",
                               size=BODY_SIZE, color=CHARCOAL, align=LEFT)
            self.hide(steps)
            self.stack(steps, self.head, buff=GAP_MD, align=LEFT)
            self.reveal(t, steps, 0, 4, 0.19)
            t.hold()

    def encryption_basics(self):
        with self.beat("part6") as t:
            self.wipe(t)
            self.part(t, 6)
            self.title(t, "Encryption", fraction=0.2)
            t.hold()

        with self.beat("enc_def") as t:
            self.lane = EncryptLane()
            self.lane.move_to(DOWN * 0.2)
            self.play(Create(self.lane.boxes), Write(self.lane.labels),
                      run_time=t.fill(0.3))
            self.play(Create(self.lane.arrows), run_time=t.fill(0.2))
            note = self.caption("readable becomes unreadable", GREY,
                                LABEL_SIZE)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.2))
            self.note = note
            t.hold()

        with self.beat("enc_key") as t:
            key = labelled_key("KEY", TERRACOTTA)
            self.lane.key_slot(key)
            self.play(Create(key[0]), Write(key[1]), run_time=t.fill(0.4))
            self.key = key
            t.hold()

        with self.beat("enc_conf") as t:
            self.recaption(t, self.note,
                           "intercepted without the key, it means nothing",
                           SAGE, 0.45, LABEL_SIZE)
            t.hold()

        with self.beat("enc_not") as t:
            self.wipe(t)
            self.title(t, "What encryption does not do", fraction=0.12)
            rows = self.lines("it does not stop interception",
                              "it does not stop deletion or damage",
                              size=BODY_SIZE, color=CHARCOAL)
            self.hide(rows)
            self.stack(rows, self.head, buff=GAP_LG * 0.8)
            self.reveal(t, rows, 0, 2, 0.3)
            self.not_rows = rows
            t.hold()

        with self.beat("enc_diff") as t:
            note = self.caption("encryption and error detection solve "
                                "different problems", TERRACOTTA, LABEL_SIZE)
            self.stack(VGroup(note), self.not_rows, buff=GAP_LG * 0.9)
            self.play(Write(note), run_time=t.fill(0.45))
            t.hold()

    def symmetric(self):
        with self.beat("sym") as t:
            self.wipe(t)
            self.title(t, "Symmetric", fraction=0.1)
            self.lane = EncryptLane()
            self.lane.move_to(DOWN * 0.2)
            self.play(Create(self.lane.boxes), Write(self.lane.labels),
                      Create(self.lane.arrows), run_time=t.fill(0.3))
            key = labelled_key("the same secret key", TERRACOTTA)
            self.lane.key_slot(key)
            self.play(Create(key[0]), Write(key[1]), run_time=t.fill(0.3))
            t.hold()

        # The delivery says symmetric is "fast and suitable to decrypt the
        # data". The point is that it is suitable for *large amounts* of
        # data, so the screen carries that and not what was said.
        #
        # The plan's next line — the challenge of sharing the secret key —
        # is not in the recording at all. There is no beat for it and no
        # card: a visual the narration never earns is the one thing this
        # pipeline exists to prevent. Flagged for a pickup line instead.
        with self.beat("sym_fast") as t:
            note = self.caption("fast, and fine for large amounts of data",
                                SAGE, LABEL_SIZE)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.4))
            self.note = note
            t.hold()

    def asymmetric(self):
        with self.beat("asym") as t:
            self.wipe(t)
            self.title(t, "Asymmetric", fraction=0.1)
            keys = VGroup(labelled_key("PUBLIC - share it", SAGE),
                          labelled_key("PRIVATE - keep secret", TERRACOTTA))
            keys.arrange(RIGHT, buff=GAP_LG * 0.9)
            fit(keys, 11.5)
            self.place(keys, self.head, buff=GAP_LG)
            self.play(Create(keys[0][0]), Create(keys[1][0]),
                      run_time=t.fill(0.3))
            self.keys = keys
            t.hold()

        with self.beat("asym_public") as t:
            self.play(Write(self.keys[0][1]), run_time=t.fill(0.25))
            self.play(Write(self.keys[1][1]), run_time=t.fill(0.25))
            t.hold()

        with self.beat("asym_use") as t:
            self.wipe(t)
            self.title(t, "Sending it confidentially", fraction=0.1)
            self.lane = EncryptLane()
            self.lane.move_to(DOWN * 0.2)
            self.play(Create(self.lane.boxes), Write(self.lane.labels),
                      Create(self.lane.arrows), run_time=t.fill(0.25))
            key = labelled_key("recipient's PUBLIC key", SAGE)
            self.lane.key_slot(key)
            self.play(Create(key[0]), Write(key[1]), run_time=t.fill(0.3))
            self.key = key
            t.hold()

        with self.beat("asym_decrypt") as t:
            self.clear(t, self.lane, self.key, fraction=0.08)
            self.lane = EncryptLane("CIPHERTEXT", "DECRYPTION", "PLAINTEXT")
            self.lane.move_to(DOWN * 0.2)
            self.play(Create(self.lane.boxes), Write(self.lane.labels),
                      Create(self.lane.arrows), run_time=t.fill(0.25))
            key = labelled_key("their own PRIVATE key", TERRACOTTA)
            self.lane.key_slot(key)
            self.play(Create(key[0]), Write(key[1]), run_time=t.fill(0.3))
            t.hold()

        with self.beat("asym_slow") as t:
            note = self.caption("good for key distribution, but slower",
                                GREY, LABEL_SIZE)
            self.foot(note)
            self.play(Write(note), run_time=t.fill(0.4))
            t.hold()

    def hybrid(self):
        with self.beat("hybrid") as t:
            self.wipe(t)
            self.title(t, "Hybrid encryption", fraction=0.12)
            t.hold()

        with self.beat("hybrid_how") as t:
            rows = self.lines("asymmetric carries the symmetric key",
                              "symmetric then carries the data",
                              size=BODY_SIZE, color=CHARCOAL)
            self.hide(rows)
            self.stack(rows, self.head, buff=GAP_LG * 0.8)
            self.reveal(t, rows, 0, 2, 0.3)
            self.how = rows
            t.hold()

        with self.beat("hybrid_why") as t:
            note = self.lines("secure key exchange", "+  speed",
                              size=BODY_SIZE, color=SAGE)
            self.stack(note, self.how, buff=GAP_LG * 0.9)
            self.play(Write(note), run_time=t.fill(0.45))
            t.hold()

        with self.beat("enc_remember") as t:
            self.wipe(t)
            self.title(t, "One thing to hold", fraction=0.1)
            rows = self.lines("encrypted with the recipient's PUBLIC key",
                              "decrypted with their PRIVATE key",
                              size=BODY_SIZE, color=CHARCOAL)
            self.hide(rows)
            self.stack(rows, self.head, buff=GAP_LG * 0.8)
            self.reveal(t, rows, 0, 2, 0.3)
            t.hold()

    def review(self):
        with self.beat("review") as t:
            self.wipe(t)
            self.title(t, "The chapter in eight lines", fraction=0.12)
            self.recap = self.lines(
                "a packet has a header, a payload and a trailer",
                "routers direct packets; numbers reorder them",
                "serial is one bit at a time; parallel risks skew",
                "simplex, half-duplex, full-duplex",
                "USB is a serial interface carrying data and power",
                "parity, checksum, echo check, check digit",
                "ARQ uses acknowledgements and a timeout",
                "symmetric, asymmetric, hybrid",
                size=LABEL_SIZE, color=CHARCOAL, align=LEFT)
            self.hide(self.recap)
            self.stack(self.recap, self.head, buff=GAP_MD * 0.8, align=LEFT)
            t.hold()

        for name, start, stop, part in (("r_packet", 0, 1, 1),
                                        ("r_switching", 1, 2, 1),
                                        ("r_serial", 2, 3, 2),
                                        ("r_duplex", 3, 4, 2),
                                        ("r_usb", 4, 5, 3),
                                        ("r_errors", 5, 6, 4),
                                        ("r_arq", 6, 7, 5),
                                        ("r_enc", 7, 8, 6)):
            with self.beat(name) as t:
                self.play(*self.strip.focus(part - 1), run_time=t.fill(0.12))
                self.reveal(t, self.recap, start, stop, 0.35)
                t.hold()

    def practice(self):
        with self.beat("practise") as t:
            self.wipe(t)
            self.title(t, "How to practise", fraction=0.1)
            rows = self.lines("a sequence question — give the right order",
                              "a comparison — describe both methods",
                              "a scenario — justify from the scenario",
                              size=BODY_SIZE, color=CHARCOAL, align=LEFT)
            self.hide(rows)
            self.stack(rows, self.head, buff=GAP_MD * 1.2, align=LEFT)
            self.reveal(t, rows, 0, 1, 0.3)
            self.practice_rows = rows
            t.hold()

        with self.beat("pr_order") as t:
            self.reveal(t, self.practice_rows, 1, 3, 0.25)
            t.hold()

        with self.beat("pause") as t:
            self.wipe(t)
            self.title(t, "Your next step", fraction=0.1)
            rows = self.lines("pause after each workbook question",
                              "then the Chapter 2 diagnostic",
                              "academy.thedigitaltutor.net",
                              size=BODY_SIZE, color=CHARCOAL)
            self.hide(rows)
            self.stack(rows, self.head, buff=GAP_MD * 1.3)
            self.next_rows = rows
            self.reveal(t, rows, 0, 1, 0.4)
            t.hold()

        with self.beat("diagnostic") as t:
            self.reveal(t, self.next_rows, 1, 2, 0.3)
            self.next_rows[2].set_opacity(1)
            self.next_rows[2].set_color(TERRACOTTA)
            self.play(Write(self.next_rows[2]), run_time=t.fill(0.3))
            t.hold()

        with self.beat("ai") as t:
            self.wipe(t)
            self.title(t, "The Digital Tutor AI", fraction=0.1)
            rows = self.lines("photograph your written answer",
                              "it checks the explanation",
                              "names what is missing",
                              "and asks you a harder one",
                              size=BODY_SIZE, color=CHARCOAL, align=LEFT)
            self.hide(rows)
            self.stack(rows, self.head, buff=GAP_MD, align=LEFT)
            self.reveal(t, rows, 0, 4, 0.15)
            t.hold()

        with self.beat("close") as t:
            self.wipe(t)
            chapter = serif("CHAPTER 2 COMPLETE", BODY_SIZE, TERRACOTTA)
            head = fit(serif("DATA TRANSMISSION", TITLE_SIZE * 1.15, CHARCOAL))
            foot = serif("The Digital Tutor", LABEL_SIZE, GREY)
            card = VGroup(chapter, head, foot).arrange(DOWN, buff=GAP_MD * 1.3)
            card.move_to(ORIGIN)
            self.play(Write(chapter), run_time=t.fill(0.18))
            self.play(Write(head), run_time=t.fill(0.3))
            self.play(FadeIn(foot), run_time=t.fill(0.2))
            t.hold()
