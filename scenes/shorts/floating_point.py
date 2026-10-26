"""A Level 9618 Short: represent -13.5 in normalized floating-point form.

Cambridge's format here is an 8-bit two's complement mantissa with the
binary point immediately after the sign bit, and a 4-bit two's complement
exponent. The whole question turns on one habit: normalize first, then
take the two's complement of the *mantissa*, not of the original number.

Verified before building: 10010100 reads as -0.84375, and -0.84375 x 2^4
is exactly -13.5. The positive mantissa 01101100 inverts to 10010011,
which plus one is 10010100.

Where the delivery or the transcriber is loose, the screen carries the
correct form: "sign bit" not "sine bit", and "mantissa" throughout.

Timing: timings/shorts.floating_point.json
Render: python build/render.py scripts/AL1-floating-point.md \\
    audio/AL1-floating-point.m4a -r 1080,1920
"""

from manim import FadeIn, VGroup, Write, DOWN, UP

from scenes.shorts.alevel_base import (  # pins the portrait frame on import
    CAPTION,
    LEAD,
    ALevelShort,
)
from brand import CHARCOAL, GAP_MD, GREY, SAGE, SLATE, TERRACOTTA, serif
from components.alevel import ANSWER, QUESTION, fit, spec_block

BITS = 34        # a bit pattern on its own line


class FloatingPoint(ALevelShort):
    scene_id = "shorts.floating_point"
    strap_text = "A Level 9618 · floating point"

    def construct(self):
        self.open_strap()
        self.the_question()
        self.the_working()
        self.the_answer()

    # -------------------------------------------------------------- helpers

    def pattern(self, text, color=CHARCOAL, size=BITS):
        return fit(serif(text, size, color))

    # ------------------------------------------------------------- sections

    def the_question(self):
        with self.beat("hook") as t:
            self.hook(t, fraction=0.5)
            t.hold()

        with self.beat("format") as t:
            self.fmt = self.spec(t, ["8-bit mantissa",
                                     "4-bit exponent",
                                     "both two's complement"],
                                 y=0.5, draw=0.16, write=0.45)
            t.hold()

        with self.beat("point") as t:
            note = self.lines("the binary point sits",
                              "straight after the sign bit",
                              size=CAPTION, color=GREY)
            self.under(note, self.fmt, buff=GAP_MD)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

        with self.beat("question") as t:
            self.wipe(t)
            ask = self.lines("Represent", size=QUESTION, color=CHARCOAL)
            value = fit(serif("-13.5", ANSWER * 1.3, TERRACOTTA))
            tail = self.lines("in normalized form", size=QUESTION,
                              color=CHARCOAL)
            block = VGroup(ask, value, tail).arrange(DOWN, buff=GAP_MD)
            block.move_to(UP * 0.6)
            self.play(Write(ask), run_time=t.fill(0.14))
            self.play(Write(value), run_time=t.fill(0.3))
            self.play(Write(tail), run_time=t.fill(0.18))
            t.hold()

        with self.beat("pause") as t:
            self.pause_card(t, fraction=0.4)
            t.hold()

    def the_working(self):
        with self.beat("solve") as t:
            self.wipe(t, 0.35)
            t.hold()

        with self.beat("binary") as t:
            line = self.pattern("13.5  =  1101.1")
            line.move_to(UP * 1.8)
            self.play(Write(line), run_time=t.fill(0.5))
            self.step_binary = line
            t.hold()

        with self.beat("normalize") as t:
            note = self.lines("move the point 4 places left",
                              size=CAPTION, color=GREY)
            self.under(note, self.step_binary, buff=GAP_MD * 0.8)
            self.play(Write(note), run_time=t.fill(0.5))
            self.step_note = note
            t.hold()

        with self.beat("normalized") as t:
            line = self.pattern("0.11011  x  2^4", SLATE)
            self.under(line, self.step_note, buff=GAP_MD * 0.9)
            self.play(Write(line), run_time=t.fill(0.5))
            self.step_norm = line
            t.hold()

        with self.beat("mantissa_pos") as t:
            label = self.lines("the mantissa is negative",
                               size=CAPTION, color=GREY)
            self.under(label, self.step_norm, buff=GAP_MD * 0.9)
            self.play(Write(label), run_time=t.fill(0.5))
            self.step_label = label
            t.hold()

        with self.beat("eight_bits") as t:
            block = spec_block(["+  0 1101100"], accent=SAGE)
            self.under(block, self.step_label, buff=GAP_MD * 0.8)
            self.play(FadeIn(block[0]), run_time=t.fill(0.16))
            self.play(Write(block[1]), run_time=t.fill(0.4))
            self.step_pos = block
            t.hold()

        with self.beat("invert") as t:
            block = spec_block(["invert   1 0010011",
                                "add 1    1 0010100"], accent=SLATE)
            self.under(block, self.step_pos, buff=GAP_MD * 0.7)
            self.play(FadeIn(block[0]), run_time=t.fill(0.14))
            self.play(Write(block[1]), run_time=t.fill(0.5))
            t.hold()

        with self.beat("result") as t:
            self.wipe(t, 0.14)
            line = self.pattern("mantissa   10010100", TERRACOTTA)
            line.move_to(UP * 1.0)
            self.play(Write(line), run_time=t.fill(0.5))
            self.mantissa = line
            t.hold()

        with self.beat("exponent") as t:
            line = self.pattern("exponent   0100", SLATE)
            self.under(line, self.mantissa, buff=GAP_MD * 1.4)
            self.play(Write(line), run_time=t.fill(0.5))
            t.hold()

    def the_answer(self):
        with self.beat("answer") as t:
            self.wipe(t, 0.14)
            self.reveal_answer(t, ["10010100", "0100"], y=0.9,
                               draw=0.2, write=0.45)
            t.hold()

        with self.beat("check") as t:
            note = self.lines("-0.84375  x  2^4  =  -13.5",
                              size=CAPTION, color=SAGE)
            note.move_to(DOWN * 0.9)
            self.play(Write(note), run_time=t.fill(0.5))
            t.hold()

        with self.beat("trap") as t:
            self.wipe(t, 0.12)
            trap = self.lines("a normalized negative",
                              "mantissa begins", size=LEAD, color=CHARCOAL)
            bits = fit(serif("1 0", ANSWER * 1.2, TERRACOTTA))
            block = VGroup(trap, bits).arrange(DOWN, buff=GAP_MD)
            block.move_to(UP * 0.4)
            self.play(Write(trap), run_time=t.fill(0.3))
            self.play(Write(bits), run_time=t.fill(0.25))
            t.hold()

        with self.beat("close") as t:
            self.wipe(t, 0.18)
            self.close_series(t, fraction=0.4)
            t.hold()
