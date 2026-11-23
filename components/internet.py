"""Chapter 5 drawn: a web address, the journey to a page, and a ledger.

Three figures the earlier lectures had no use for. Everything else this
chapter needs already exists -- ``SortBench`` sorts the internet from the
web and then, unchanged, sorts session cookies from persistent ones and
phishing from pharming; ``columns`` lays out the malware table and the
controls table; ``Chain`` and ``chips`` do the rest.

  * ``UrlBar``     a web address with its parts bracketed underneath.
                   The brackets are measured off the string itself, not
                   placed by eye: the protocol is characters 0 to 8 of
                   the URL and the figure works out where that is.
  * ``Journey``    browser, DNS server and web server as three places
                   rather than a straight line. This one is shaped by
                   the single thing the syllabus keeps marking wrong:
                   the DNS server does not send the page. Drawn as a
                   chain -- browser, DNS, server, page -- the picture
                   says it does. So DNS sits off to one side, on a
                   round trip of its own, and the page comes from the
                   other box entirely.
  * ``BlockChain`` blocks carrying a timestamp and a link to the one
                   before, and ``tamper`` to show what altering an old
                   record does to every link after it.

Sized for the 14.22 x 8 landscape frame at scale 1.0, like every other
figure here. Where a label will not fit these raise rather than shrink,
so the fix is a shorter label and never a quietly illegible frame.

``measure()`` prints every figure's extents; run it as
``python -m components.internet`` from the repo root after any change.
"""

from manim import (
    Arrow,
    Line,
    Rectangle,
    RoundedRectangle,
    VGroup,
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
)

from brand import (
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
    mono,
    serif,
)

FRAME_SAFE = 12.6

# An address invented for the lesson. example.org is the reserved
# documentation domain, so this cannot accidentally be somebody's site.
URL = "https://www.example.org/notes/chapter5.html"
# Invented, and distinct, so that each block's "prev" is the block
# before it rather than a decorative constant.
HASHES = ["4f2a", "9c1e", "b70d", "25fa", "8e03"]

URL_PARTS = [
    (0, 8, "protocol"),
    (8, 23, "domain name"),
    (23, len(URL), "path"),
]

# The four hops, in the order the lecture takes them. The numbers are the
# numbers the student sees on screen.
HOPS = [
    "the browser asks DNS for the address",
    "DNS returns the IP address",
    "the browser requests the page",
    "the server returns the resources",
]


def _char_width(size):
    """One monospace character, measured rather than assumed."""
    return mono("M" * 20, size).width / 20.0


class UrlBar(VGroup):
    """A web address, with its parts bracketed and named underneath.

    The brackets are computed from character offsets into the string, so
    naming a different span is a different pair of numbers and never a
    nudged x coordinate.
    """

    def __init__(self, url=URL, parts=None, size=MARGIN_SIZE,
                 label_size=MARGIN_SIZE, width=FRAME_SAFE):
        super().__init__()
        parts = URL_PARTS if parts is None else parts

        self.text = mono(url, size, CHARCOAL)
        self.bar = RoundedRectangle(width=self.text.width + GAP_LG,
                                    height=self.text.height + GAP_MD * 1.5,
                                    corner_radius=0.14, color=GREY,
                                    stroke_width=2.5)
        self.bar.set_fill(CREAM, opacity=1)
        self.bar.move_to(self.text)
        self.add(self.bar, self.text)

        step = _char_width(size)
        left = self.text.get_left()[0]
        bottom = self.bar.get_bottom()[1]

        self.spans, self.labels, self.braces = VGroup(), VGroup(), VGroup()
        for start, stop, name in parts:
            x0, x1 = left + start * step, left + stop * step
            y = bottom - GAP_SM * 0.9
            brace = VGroup(
                Line([x0, y, 0], [x1, y, 0], color=SLATE, stroke_width=2.5),
                Line([x0, y, 0], [x0, y + GAP_SM * 0.45, 0], color=SLATE,
                     stroke_width=2.5),
                Line([x1, y, 0], [x1, y + GAP_SM * 0.45, 0], color=SLATE,
                     stroke_width=2.5),
            )
            label = serif(name, label_size, SLATE)
            if label.width > x1 - x0:
                # A name wider than the span it points at reads as
                # pointing at the wrong span.
                raise ValueError(
                    f"The label {name!r} is {label.width:.2f} units wide "
                    f"over a span only {x1 - x0:.2f} wide. Shorten the "
                    "label or widen the span it names.")
            label.move_to([(x0 + x1) / 2, y - GAP_SM * 0.75, 0])
            self.braces.add(brace)
            self.labels.add(label)
            self.spans.add(VGroup(brace, label))
        self.add(self.braces, self.labels)

        self.move_to(ORIGIN)
        if self.width > width:
            raise ValueError(
                f"The address bar is {self.width:.2f} units wide, over the "
                f"{width:.2f} the frame allows. Use a shorter address.")

    def part(self, index):
        return self.spans[index]

    def light(self, index, color=TERRACOTTA):
        brace, label = self.spans[index]
        return [brace.animate.set_color(color),
                label.animate.set_color(color)]

    def settle(self, index):
        brace, label = self.spans[index]
        return [brace.animate.set_color(SLATE),
                label.animate.set_color(SLATE)]


class Journey:
    """Browser, DNS server and web server, and the four hops between.

    Not a VGroup: the pieces are handed back one at a time so each lands
    on the beat that names it, and a scene adds what it wants.

    The shape is the argument. A chain of four boxes would read
    "browser, then DNS, then the server, then the page", and the thing
    the syllabus marks wrong is exactly that -- students write that DNS
    sends the page. Here DNS is a round trip off to one side and the
    page comes from a different box, so the picture cannot be read that
    way.
    """

    def __init__(self, size=MARGIN_SIZE, box=3.3, height=1.2):
        self.browser, self.browser_box = self._panel(
            "Browser", [-4.4, 0.25, 0], box, height, size, SLATE)
        # 1.85 and -1.35, not 2.05 and -1.55. At 2.05 the top of the DNS
        # box sat at 2.65 and the descenders of a section heading placed
        # with to_edge(UP, 0.85) reach 2.60, so the box line was drawn
        # straight through the tail of a 'p' or 'g'. Nothing here could
        # catch it: a box is not text, and the acceptance check compares
        # text against text. Dropping both boxes by a fifth of a unit
        # keeps the browser at the midpoint and leaves the web server
        # 0.36 units clear of the commentary band below.
        self.dns, self.dns_box = self._panel(
            "DNS server", [3.2, 1.85, 0], box, height, size, GREY)
        self.server, self.server_box = self._panel(
            "Web server", [3.2, -1.35, 0], box, height, size, SLATE)

        # 0.45 apart, not 0.18. Over a diagonal of nearly eight units a
        # pair offset by a fifth of a unit renders as one line with a
        # head at each end -- which is exactly the double-headed arrow
        # the comment below used to warn against, drawn anyway.
        # The same lift for all four, not alternating signs. _hop takes
        # the perpendicular from the arrow's own direction, so a reversed
        # arrow already has a reversed perpendicular: negating the lift
        # as well flipped it back and laid the reply exactly on top of
        # the request. The pair rendered as one line with a head at each
        # end, and the second arrow drawn hid the first one's colour.
        self.ask = self._hop(self.browser_box, self.dns_box, GREY, 0.45)
        self.answer = self._hop(self.dns_box, self.browser_box, SAGE, 0.45)
        self.request = self._hop(self.browser_box, self.server_box, GREY,
                                 0.45)
        self.resources = self._hop(self.server_box, self.browser_box, SAGE,
                                   0.45)
        self.arrows = [self.ask, self.answer, self.request, self.resources]

        # A third of the way along each arrow from its own start, not at
        # the midpoint. All four midpoints cluster near the browser,
        # where the arrows meet, and 2 and 3 printed on top of one
        # another. Measured from each arrow's start they spread out,
        # because the four arrows start at four different places.
        self.tags = VGroup()
        for index, arrow in enumerate(self.arrows):
            tag = serif(str(index + 1), size, CHARCOAL)
            start, end = arrow.get_start(), arrow.get_end()
            spot = start + (end - start) * 0.32 + self._offset(arrow) * 0.8
            tag.move_to(spot)
            self.tags.add(tag)

        # Guard rather than trust: two numbers on top of each other is
        # not off-frame, does not overlap any *text* the acceptance
        # check knows about, and is not too small, so nothing else here
        # would notice.
        import numpy as np
        for i in range(len(self.tags)):
            for j in range(i + 1, len(self.tags)):
                apart = float(np.linalg.norm(
                    self.tags[i].get_center() - self.tags[j].get_center()))
                if apart < 0.6:
                    raise ValueError(
                        f"Hop labels {i + 1} and {j + 1} are {apart:.2f} "
                        "units apart and will read as one mark.")

    @staticmethod
    def _panel(name, centre, box, height, size, colour):
        frame = Rectangle(width=box, height=height, color=colour,
                          stroke_width=2.5)
        frame.set_fill(colour, opacity=0.1)
        frame.move_to(centre)
        label = serif(name, size, CHARCOAL)
        if label.width > box - GAP_SM * 1.4:
            raise ValueError(
                f"{name!r} is {label.width:.2f} units wide in a "
                f"{box:.2f}-unit box.")
        label.move_to(frame)
        return VGroup(frame, label), frame

    @staticmethod
    def _hop(start, end, colour, lift):
        """An arrow between two boxes, offset so a pair does not overlap.

        The two directions of a round trip drawn on the same line sit on
        top of each other and read as one double-headed arrow, which is
        not what a request and a reply are.
        """
        a, b = start.get_center(), end.get_center()
        import numpy as np
        along = (b - a)
        along = along / np.linalg.norm(along)
        across = np.array([-along[1], along[0], 0.0]) * lift
        # The boxes are 3.3 wide, so half of one is 1.65: a buff of 1.0
        # starts the arrow six tenths of a unit inside the box it leaves.
        return Arrow(a + across, b + across, color=colour, stroke_width=3.5,
                     buff=1.95, max_tip_length_to_length_ratio=0.28)

    @staticmethod
    def _offset(arrow):
        import numpy as np
        a, b = arrow.get_start(), arrow.get_end()
        along = (b - a)
        along = along / np.linalg.norm(along)
        return np.array([-along[1], along[0], 0.0]) * 0.42

    def hop(self, index):
        """One arrow and its number."""
        return VGroup(self.arrows[index], self.tags[index])

    def everything(self):
        return VGroup(self.browser, self.dns, self.server,
                      *self.arrows, self.tags)


class BlockChain(VGroup):
    """Blocks carrying a timestamp and a link back to the one before.

    ``tamper`` shows what altering an old record does: the block itself
    goes terracotta and so does every link after it, which is the whole
    argument for why a chain is hard to rewrite unnoticed.
    """

    def __init__(self, count=3, size=MARGIN_SIZE, box=3.3, height=2.35,
                 gap=0.72, width=FRAME_SAFE, first=1):
        super().__init__()
        self.boxes, self.bodies, self.links = VGroup(), VGroup(), VGroup()

        for index in range(count):
            frame = RoundedRectangle(width=box, height=height,
                                     corner_radius=0.12, color=SLATE,
                                     stroke_width=2.5)
            frame.set_fill(SLATE, opacity=0.08)
            title = serif(f"Block {first + index}", size, CHARCOAL)
            stamp = mono("09:4%d" % (index + 1), size, GREY)
            # Each block carries its own hash and the hash of the one
            # before, and they actually match up: block n's "prev" is
            # block n-1's "hash". The first draft printed the same
            # "prev" in every block, which says each block follows the
            # same predecessor -- not a chain at all, and the one thing
            # this figure exists to show.
            own = mono(f"hash: {HASHES[index]}", size, GREY)
            link = mono(
                f"prev: {HASHES[index - 1]}" if index else "prev: none",
                size, GREY)
            body = VGroup(title, stamp, own, link)
            body.arrange(DOWN, buff=GAP_SM * 0.6)
            if body.width > box - GAP_SM * 1.4:
                raise ValueError(
                    f"Block {first + index} contents run {body.width:.2f} "
                    f"units inside a {box:.2f}-unit block.")
            self.boxes.add(frame)
            self.bodies.add(body)

        self.boxes.arrange(RIGHT, buff=gap)
        for frame, body in zip(self.boxes, self.bodies):
            body.move_to(frame)

        for left, right in zip(self.boxes, self.boxes[1:]):
            self.links.add(Arrow(left.get_right(), right.get_left(),
                                 color=GREY, stroke_width=3.5, buff=0.04,
                                 max_tip_length_to_length_ratio=0.5))

        self.add(self.boxes, self.bodies, self.links)
        self.move_to(ORIGIN)
        if self.width > width:
            raise ValueError(
                f"The chain is {self.width:.2f} units wide, over the "
                f"{width:.2f} the frame allows.")

    def block(self, index):
        return VGroup(self.boxes[index], self.bodies[index])

    def tamper(self, index, color=TERRACOTTA):
        """Alter one block, and break every link that follows it."""
        moves = [self.boxes[index].animate.set_stroke(color)
                 .set_fill(color, opacity=0.14)]
        moves += [item.animate.set_color(color)
                  for item in self.bodies[index]]
        moves += [self.links[i].animate.set_color(color)
                  for i in range(index, len(self.links))]
        return moves


def measure():
    """Print every figure's extents.

    Run as ``python -m components.internet`` from the repo root.
    """
    from manim import config

    half_w, half_h = config.frame_width / 2, config.frame_height / 2

    def report(name, figure):
        fits = (figure.width <= 2 * half_w - 0.4
                and figure.height <= 2 * half_h - 0.4)
        print(f"{name:16} {figure.width:6.2f} x {figure.height:5.2f}  "
              f"{'ok' if fits else 'DOES NOT FIT'}")

    bar = UrlBar()
    report("UrlBar", bar)
    for index, (start, stop, name) in enumerate(URL_PARTS):
        span = bar.spans[index]
        print(f"{'':16} {name:12} {URL[start:stop]!r}")

    report("Journey", Journey().everything())
    report("BlockChain", BlockChain())


if __name__ == "__main__":
    measure()
