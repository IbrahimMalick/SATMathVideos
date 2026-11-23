"""Chapter 5, The Internet and Its Uses: Cambridge O Level 2210.

Eleven numbered sections and an opening, every reveal anchored to the
narration by build/beats_ch05.py.

The chapter is built almost entirely out of distinctions the syllabus
marks students down for blurring, so the figures are chosen to make each
distinction hard to misread rather than merely stated:

  * the internet against the web, and later session cookies against
    persistent ones, and phishing against pharming -- all three are the
    same ``SortBench`` from components/os_shape.py, two bins and the rule
    that decides which bin a thing goes in.
  * ``Journey`` puts the DNS server off to one side on a round trip of
    its own. Drawn as a chain -- browser, DNS, server, page -- the
    picture would say DNS hands over the page, which is the single
    thing this topic keeps marking wrong.
  * ``BlockChain`` can be tampered with on screen: altering one block
    turns every link after it, which is the argument for why rewriting
    a ledger unnoticed is hard, rather than the claim that it cannot be
    done. The lecture is careful about that and so is the caption.

Where the captions and the audio disagree, the captions are right and
the mismatch is deliberate. The narration is correct throughout -- it is
a clean synthetic reading -- but the transcriber misheard parts of it,
and the beats are anchored to what it produced because that is what the
anchors are matched against. "Fishing" is phishing, "Farming" is
pharming, and "and Christian protects data as it travels between
devices" is encryption. build/beats_ch05.py lists them.

Timing: timings/cs.internet.json
Render: python build/render.py scripts/CH05-internet.md \\
    audio/CH05-internet.mp3
"""

from contextlib import contextmanager

from manim import (
    Create,
    FadeIn,
    FadeOut,
    Line,
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
    DISPLAY_SIZE,
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
from components.editorial import columns, fit, numbered, prose
from components.internet import BlockChain, Journey, UrlBar
from components.os_core import callout
from components.os_shape import SortBench, chips, grid
from components.syllabus_map import TopicStrip
from scenes.base import SATScene

FRAME_SAFE = 12.6
FLOOR = -3.05
BARE_FLOOR = -3.5

PARTS = ["Internet and web", "The web address", "From address to page",
         "Cookies", "Blockchain", "Threats", "Malware", "Deception",
         "Controls", "One example", "Recap"]
(WEB, URL_, JOURNEY, COOKIES, CHAIN, THREATS, MALWARE, DECEPTION,
 CONTROLS, EXAMPLE, RECAP) = range(11)

AGENDA = ["The internet and the web", "A web address",
          "How a page reaches you", "Cookies", "Digital currency",
          "Cybersecurity threats", "Security controls"]

BROWSER_JOBS = ["Requests resources", "Interprets the code",
                "Displays the page"]
BROWSER_TOOLS = ["Address bar", "Tabs", "Bookmarks", "History"]

# The six steps, in the lecture's own order and wording.
PROCESS = [
    "The user enters a URL.",
    "The browser extracts the domain name.",
    "DNS finds the server's IP address.",
    "The browser requests the page.",
    "The server returns the resources.",
    "The browser renders the page.",
]

# Two columns, because every row of this chapter's tables is a term and
# the mechanism that tells it apart from the term above it.
THREAT_ROWS = [
    ("Brute force", "tries many password combinations"),
    ("Data interception", "captures data in transit"),
    ("Hacking", "unauthorised access to systems"),
    ("DDoS", "floods a service with traffic"),
]
MALWARE_ROWS = [
    ("Virus", "attaches to a host file"),
    ("Worm", "copies itself across a network"),
    ("Trojan horse", "looks useful, acts maliciously"),
    ("Spyware", "secretly records what you do"),
    ("Adware", "unwanted adverts, may track you"),
    ("Ransomware", "locks data, demands payment"),
]
CONTROL_ROWS_A = [
    ("Authentication", "checks who the user is"),
    ("Two-step verification", "a stolen password is not enough"),
    ("Access levels", "limits what each user reaches"),
    ("Firewall", "filters traffic by rules"),
]
CONTROL_ROWS_B = [
    ("Anti-malware", "detects and removes malware"),
    ("Automatic updates", "closes known weaknesses"),
    ("Encryption", "protects data in transit"),
    ("Proxy server", "filters requests"),
]

CHECKS = [
    "Check who sent it.",
    "Check the wording.",
    "Check where the link really goes.",
    "Never use the link. Go to the bank yourself.",
]

RECAP_CARDS = [
    ("The internet and the web", [
        "The internet is the network infrastructure.",
        "The web is the pages you reach across it.",
    ]),
    ("From address to page", [
        "DNS resolves the domain name to an IP address.",
        "The web server returns the page resources.",
    ]),
    ("Cookies and blockchain", [
        "Session cookies go; persistent cookies stay.",
        "A blockchain is linked, timestamped records.",
    ]),
    ("The threats", [
        "A virus attaches to a host file.",
        "A worm copies itself across networks.",
        "Phishing deceives; pharming redirects.",
        "DDoS denies a service; ransomware locks data.",
    ]),
]

QUESTIONS = [
    "What is the difference between the internet and the web?",
    "What does DNS do, and what does it not do?",
    "How do session and persistent cookies differ?",
    "Why is an old block in a chain hard to alter?",
    "Name three malware types and how each spreads.",
    "Phishing or pharming: which redirects you?",
    "Match three controls to the risks they reduce.",
]


class Internet(SATScene):
    scene_id = "cs.internet"

    def construct(self):
        self.margin = mono("The Internet · Chapter 5", MARGIN_SIZE)
        self.margin.to_corner(UP + LEFT, buff=GAP_SM)
        self.add(self.margin)

        self.strip = TopicStrip(len(PARTS), lit=SLATE, side=0.56)
        self.strip.to_edge(DOWN, buff=GAP_SM * 0.5)

        self.keep = [self.margin]
        self.floor = BARE_FLOOR
        self.head = None
        self.note = None
        self.side = None

        self.opening()
        self.internet_and_web()
        self.the_url()
        self.the_journey()
        self.cookies()
        self.blockchain()
        self.threats()
        self.malware()
        self.deception()
        self.controls()
        self.one_example()
        self.recap()
        self.self_check()

    # --------------------------------------------------------- opening

    def opening(self):
        with self.beat("open") as t:
            chapter = serif("Chapter 5", LABEL_SIZE, SLATE)
            title = serif("The Internet and Its Uses", DISPLAY_SIZE,
                          CHARCOAL)
            title = fit(title)
            board = prose("Cambridge O Level Computer Science 2210",
                          LABEL_SIZE, GREY)
            card = VGroup(chapter, title, board).arrange(DOWN, buff=GAP_MD)
            card.move_to(ORIGIN)
            self.play(FadeIn(chapter), run_time=t.fill(0.14))
            self.play(Write(title), run_time=t.fill(0.3))
            t.hold()

        with self.beat("welcome") as t:
            self.play(FadeIn(board), run_time=t.fill(0.4))
            t.hold()

        with self.beat("journey_promise") as t:
            self.wipe(t)
            self.title(t, "What this chapter covers", fraction=0.12)
            plan, items = grid(AGENDA, columns=2, size=LABEL_SIZE,
                               h_gap=GAP_MD * 1.2, v_gap=GAP_SM * 1.6)
            self.place(plan, self.head, buff=GAP_MD * 1.4)
            self.plan_items = items
            self.play(FadeIn(items[0]), FadeIn(items[2]),
                      run_time=t.fill(0.34))
            t.hold()

        with self.beat("also_cookies") as t:
            self.play(FadeIn(self.plan_items[3]), run_time=t.fill(0.4))
            t.hold()

        with self.beat("also_threats") as t:
            self.play(FadeIn(self.plan_items[4]),
                      FadeIn(self.plan_items[5]), run_time=t.fill(0.4))
            t.hold()

        with self.beat("also_controls") as t:
            self.play(FadeIn(self.plan_items[1]),
                      FadeIn(self.plan_items[6]), run_time=t.fill(0.4))
            t.hold()

        with self.beat("easy_to_confuse") as t:
            self.wipe(t)
            self.title(t, "Terms that are easy to confuse", fraction=0.14)
            t.hold()

        with self.beat("naming_first_step") as t:
            first = serif("Naming the term is the first step.",
                          TITLE_SIZE, CHARCOAL)
            first = fit(first)
            self.place(first, self.head, buff=GAP_LG)
            self.first = first
            self.play(FadeIn(first), run_time=t.fill(0.4))
            t.hold()

        with self.beat("explain_it") as t:
            second = serif("Explaining what it does earns the mark.",
                           TITLE_SIZE, TERRACOTTA)
            second = fit(second)
            self.place(second, self.first, buff=GAP_MD * 1.4)
            self.play(Write(second), run_time=t.fill(0.45))
            t.hold()

    # ------------------------------------------ 1. the internet and the web

    def internet_and_web(self):
        bench = None

        with self.beat("distinguish") as t:
            self.section(t, "Two things, not one", WEB)
            bench = SortBench("The internet", "The World Wide Web")
            bench.next_to(self.head, DOWN, buff=GAP_MD)
            self.bench = bench
            # One play, not two: this beat also pays for the strip's
            # first appearance, and five plays at the 0.5s pacing floor
            # need 2.5s of a 2.4s beat.
            self.play(Write(bench.heads[0]), Write(bench.heads[1]),
                      Create(bench.rules), run_time=t.fill(0.4))
            t.hold()

        with self.beat("internet_is") as t:
            self.play(FadeIn(bench.caption(
                0, "the global network infrastructure")),
                run_time=t.fill(0.4))
            t.hold()

        with self.beat("web_is") as t:
            self.play(FadeIn(bench.caption(
                1, "the websites and pages you reach across it")),
                run_time=t.fill(0.4))
            t.hold()

        with self.beat("not_the_same") as t:
            self.play(FadeIn(bench.item(0, "the wires and the rules")),
                      run_time=t.fill(0.2))
            self.play(FadeIn(bench.item(1, "the content on top")),
                      run_time=t.fill(0.2))
            self.say(t, "The web uses the internet. They are not the "
                        "same thing.", fraction=0.3)
            t.hold()

        with self.beat("email_example") as t:
            self.say(t, "Email and online games use the internet with no "
                        "web page in sight", fraction=0.4)
            t.hold()

        with self.beat("browser_intro") as t:
            self.wipe(t)
            self.title(t, "What a browser does", fraction=0.12)
            t.hold()

        with self.beat("browser_jobs") as t:
            jobs, each = chips(BROWSER_JOBS, size=LABEL_SIZE, rows=2)
            self.place(jobs, self.head, buff=GAP_LG * 0.9)
            self.jobs = jobs
            for chip in each:
                self.play(FadeIn(chip), run_time=t.fill(0.14))
            t.hold()

        with self.beat("browser_tools") as t:
            tools, each = chips(BROWSER_TOOLS, size=LABEL_SIZE, rows=2)
            self.place(tools, self.jobs, buff=GAP_LG * 0.8)
            self.play(FadeIn(tools), run_time=t.fill(0.3))
            self.say(t, "and the tools around the page", fraction=0.26)
            t.hold()

    # ---------------------------------------------------- 2. the web address

    def the_url(self):
        bar = UrlBar()

        with self.beat("url_open") as t:
            self.section(t, "Uniform Resource Locator", URL_)
            t.hold()

        with self.beat("url_parts") as t:
            self.place(bar, self.head, buff=GAP_LG)
            self.bar = bar
            self.play(Create(bar.bar), run_time=t.fill(0.2))
            self.play(FadeIn(bar.text), run_time=t.fill(0.3))
            t.hold()

        with self.beat("three_parts") as t:
            self.play(*[Create(brace) for brace in bar.braces],
                      run_time=t.fill(0.22))
            self.play(*[FadeIn(label) for label in bar.labels],
                      run_time=t.fill(0.22))
            t.hold()

        details = [
            ("protocol_is", 0, "how the browser should talk to the server"),
            ("domain_is", 1, "which website the user wants"),
            ("path_is", 2, "which page or file on that website"),
        ]
        lit = None
        for beat_name, index, text in details:
            with self.beat(beat_name) as t:
                moves = list(bar.light(index))
                if lit is not None:
                    moves += bar.settle(lit)
                self.play(*moves, run_time=t.fill(0.26))
                lit = index
                self.say(t, text, fraction=0.34)
                t.hold()

    # ------------------------------------------- 3. from address to page

    def the_journey(self):
        trip = Journey()

        with self.beat("extract_domain") as t:
            self.section(t, "From an address to a page", JOURNEY)
            self.play(Create(trip.browser_box), FadeIn(trip.browser[1]),
                      run_time=t.fill(0.3))
            self.trip = trip
            t.hold()

        with self.beat("needs_ip") as t:
            self.say(t, "It needs the IP address of the server for that "
                        "domain", fraction=0.4)
            t.hold()

        with self.beat("asks_dns") as t:
            self.play(Create(trip.dns_box), FadeIn(trip.dns[1]),
                      run_time=t.fill(0.26))
            self.play(Create(trip.arrows[0]), FadeIn(trip.tags[0]),
                      run_time=t.fill(0.26))
            t.hold()

        with self.beat("resolving_means") as t:
            self.say(t, "Resolving means finding the IP address for a "
                        "domain name", fraction=0.4)
            t.hold()

        with self.beat("dns_returns") as t:
            self.play(Create(trip.arrows[1]), FadeIn(trip.tags[1]),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("dns_not_page") as t:
            warn = serif("DNS does not send the page", LABEL_SIZE,
                         TERRACOTTA)
            warn.move_to([trip.dns_box.get_center()[0],
                          trip.dns_box.get_top()[1] + GAP_MD * 1.1, 0])
            self.warn = warn
            self.play(FadeIn(warn), run_time=t.fill(0.4))
            t.hold()

        with self.beat("dns_job") as t:
            self.say(t, "Its whole job is to point the browser at the "
                        "right server", fraction=0.4)
            t.hold()

        with self.beat("connects") as t:
            self.play(Create(trip.server_box), FadeIn(trip.server[1]),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("sends_request") as t:
            self.play(Create(trip.arrows[2]), FadeIn(trip.tags[2]),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("http_is") as t:
            self.say(t, "HTTP carries web resources", fraction=0.4)
            t.hold()

        with self.beat("https_is") as t:
            self.say(t, "HTTPS carries them over a secure, encrypted "
                        "connection", fraction=0.4)
            t.hold()

        with self.beat("server_returns") as t:
            self.play(Create(trip.arrows[3]), FadeIn(trip.tags[3]),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("what_comes_back") as t:
            self.say(t, "HTML, images, styles and whatever else the page "
                        "needs", fraction=0.4)
            t.hold()

        with self.beat("renders") as t:
            self.say(t, "and the browser puts them together into the page "
                        "you see", fraction=0.4)
            t.hold()

        with self.beat("recap_1") as t:
            self.wipe(t)
            self.title(t, "The whole process", fraction=0.1)
            steps, rows = numbered(PROCESS, size=LABEL_SIZE,
                                   gap=GAP_SM * 1.1)
            self.place(steps, self.head, buff=GAP_MD * 1.2)
            self.steps, self.step_rows = steps, rows
            self.play(FadeIn(rows[0]), run_time=t.fill(0.4))
            t.hold()

        for beat_name, index in (("recap_2", 1), ("recap_3", 2),
                                 ("recap_4", 3), ("recap_5", 4),
                                 ("recap_6", 5)):
            with self.beat(beat_name) as t:
                self.play(FadeIn(self.step_rows[index]),
                          run_time=t.fill(0.45))
                t.hold()

        with self.beat("distinction") as t:
            self.wipe(t)
            self.title(t, "The distinction that gets marked",
                       fraction=0.12)
            t.hold()

        with self.beat("dns_does") as t:
            one = callout(["DNS", "resolves a domain name",
                           "to an IP address"], size=LABEL_SIZE,
                          accent=SLATE, width=6.4)
            one.move_to([-3.3, 0.1, 0])
            self.play(Create(one[0]), run_time=t.fill(0.2))
            for line in one[1]:
                self.play(FadeIn(line), run_time=t.fill(0.16))
            t.hold()

        with self.beat("server_does") as t:
            two = callout(["The web server", "returns the page",
                           "resources"], size=LABEL_SIZE,
                          accent=TERRACOTTA, width=6.0)
            two.move_to([3.3, 0.1, 0])
            self.play(Create(two[0]), run_time=t.fill(0.2))
            for line in two[1]:
                self.play(FadeIn(line), run_time=t.fill(0.16))
            t.hold()

    # --------------------------------------------------------- 4. cookies

    def cookies(self):
        with self.beat("cookies_open") as t:
            self.section(t, "Remembering you between requests", COOKIES)
            t.hold()

        with self.beat("cookie_is") as t:
            defn = prose("A cookie is a small piece of data the browser "
                         "stores for a website.", BODY_SIZE, CHARCOAL,
                         11.8)
            self.place(defn, self.head, buff=GAP_LG * 0.9)
            self.defn = defn
            self.play(FadeIn(defn), run_time=t.fill(0.4))
            t.hold()

        with self.beat("cookies_convenient") as t:
            self.say(t, "which is mostly a convenience", fraction=0.4)
            t.hold()

        with self.beat("basket") as t:
            uses, each = chips(["A shopping basket", "Preferences",
                                "Staying logged in"], size=LABEL_SIZE,
                               rows=1)
            self.place(uses, self.defn, buff=GAP_LG * 0.8)
            self.uses, self.use_chips = uses, each
            self.play(FadeIn(each[0]), run_time=t.fill(0.4))
            t.hold()

        with self.beat("preferences") as t:
            self.play(FadeIn(self.use_chips[1]), FadeIn(self.use_chips[2]),
                      run_time=t.fill(0.45))
            t.hold()

        bench = None

        with self.beat("two_types") as t:
            self.wipe(t)
            self.title(t, "Two kinds, and the difference is time",
                       fraction=0.12)
            t.hold()

        with self.beat("named") as t:
            bench = SortBench("Session cookie", "Persistent cookie")
            bench.next_to(self.head, DOWN, buff=GAP_MD)
            self.cookie_bench = bench
            self.play(Write(bench.heads[0]), Write(bench.heads[1]),
                      run_time=t.fill(0.3))
            self.play(Create(bench.rules), run_time=t.fill(0.26))
            t.hold()

        with self.beat("session_is") as t:
            self.play(FadeIn(bench.caption(0, "lasts while the browser "
                                              "session does")),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("session_deleted") as t:
            self.play(FadeIn(bench.item(0, "gone when you close it")),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("session_use") as t:
            self.play(FadeIn(bench.item(0, "a basket between pages")),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("persistent_is") as t:
            self.play(FadeIn(bench.caption(1, "stays after the browser "
                                              "closes")),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("persistent_until") as t:
            self.play(FadeIn(bench.item(1, "until it expires")),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("persistent_use") as t:
            self.play(FadeIn(bench.item(1, "a preference, a login")),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("privacy") as t:
            self.say(t, "Convenient, and a privacy question",
                     fraction=0.4)
            t.hold()

        with self.beat("tracking") as t:
            self.play(*[item.animate.set_color(TERRACOTTA)
                        for item in bench.items[1]],
                      run_time=t.fill(0.26))
            self.say(t, "because a cookie that stays can follow you",
                     fraction=0.34)
            t.hold()

        with self.beat("compare_cookies") as t:
            self.say(t, "Compare them on how long each lasts, and what "
                        "it is used for", fraction=0.45)
            t.hold()

    # ------------------------------------------------------ 5. blockchain

    def blockchain(self):
        chain = BlockChain(3)

        with self.beat("currency_open") as t:
            self.section(t, "Digital currency", CHAIN)
            t.hold()

        with self.beat("currency_is") as t:
            defn = prose("It exists electronically, and moves between "
                         "digital wallets.", BODY_SIZE, CHARCOAL, 11.8)
            self.place(defn, self.head, buff=GAP_LG)
            self.money = defn
            self.play(FadeIn(defn), run_time=t.fill(0.4))
            t.hold()

        with self.beat("uses_blockchain") as t:
            self.say(t, "and some of them record transactions on a "
                        "blockchain", fraction=0.45)
            t.hold()

        with self.beat("ledger") as t:
            self.wipe(t)
            self.title(t, "A ledger of linked records", fraction=0.12)
            self.place(chain, self.head, buff=GAP_LG * 0.9)
            self.chain = chain
            self.play(Create(chain.boxes), run_time=t.fill(0.3))
            self.play(FadeIn(chain.bodies), run_time=t.fill(0.22))
            t.hold()

        with self.beat("simplified") as t:
            self.play(Create(chain.links), run_time=t.fill(0.4))
            t.hold()

        for beat_name, text in (
                ("broadcast", "A transaction is requested, and broadcast "
                              "to the network"),
                ("network_checks", "The network checks it against the "
                                   "agreed rules"),
                ("grouped", "Valid transactions are grouped into a block"),
                ("timestamp_link", "Each block carries a timestamp and a "
                                   "link to the one before"),
                ("replicated", "and the accepted block is copied across "
                               "the network")):
            with self.beat(beat_name) as t:
                self.say(t, text, fraction=0.4)
                t.hold()

        with self.beat("changing_older") as t:
            self.play(*chain.tamper(0), run_time=t.fill(0.3))
            self.say(t, "Change an old record and every link after it "
                        "stops matching", fraction=0.4)
            t.hold()

        with self.beat("needs_network") as t:
            self.say(t, "and the network would have to accept the "
                        "altered record too", fraction=0.45)
            t.hold()

        with self.beat("difficult") as t:
            self.say(t, "which makes an undetected change hard",
                     fraction=0.4)
            t.hold()

        with self.beat("not_impossible") as t:
            self.wipe(t)
            self.title(t, "Say it accurately", fraction=0.1)
            bad = serif("“A blockchain cannot be attacked.”",
                        LABEL_SIZE, GREY)
            self.place(bad, self.head, buff=GAP_LG)
            self.bad = bad
            self.play(FadeIn(bad), run_time=t.fill(0.3))
            strike = Line(bad.get_left() + LEFT * GAP_SM * 0.5,
                          bad.get_right() + RIGHT * GAP_SM * 0.5,
                          color=TERRACOTTA, stroke_width=3)
            self.play(Create(strike), run_time=t.fill(0.26))
            t.hold()

        with self.beat("accurate") as t:
            good = prose("Linked records and network agreement make an "
                         "unauthorised change hard to carry out without "
                         "detection.", LABEL_SIZE, SAGE, 11.6)
            self.place(good, self.bad, buff=GAP_LG * 0.8)
            self.play(FadeIn(good), run_time=t.fill(0.5))
            t.hold()

    # --------------------------------------------------------- 6. threats

    def threats(self):
        with self.beat("threats_open") as t:
            self.section(t, "Cybersecurity threats", THREATS)
            t.hold()

        # The definition goes in the commentary band rather than on a
        # line of its own. Placed above the table it pushed four rows
        # down into the band, and there is no arrangement of the two
        # that fits: the table alone needs everything under the heading.
        with self.beat("threat_is") as t:
            self.say(t, "An action or a piece of software that puts data "
                        "or systems at risk.", fraction=0.4)
            t.hold()

        with self.beat("different_ways") as t:
            table, cells, heads = columns(
                ("Threat", "How it works"), THREAT_ROWS,
                row_gap=GAP_SM * 1.3)
            self.place(table, self.head, buff=GAP_MD * 1.2)
            self.table, self.cells = table, cells
            self.play(*[FadeIn(head) for head in heads],
                      Create(table.rule), run_time=t.fill(0.4))
            t.hold()

        for beat_name, index in (("brute_force", 0), ("interception", 1),
                                 ("hacking", 2), ("ddos", 3)):
            with self.beat(beat_name) as t:
                self.play(FadeIn(self.cells[index][0]),
                          run_time=t.fill(0.24))
                self.play(FadeIn(self.cells[index][1]),
                          run_time=t.fill(0.34))
                t.hold()

        with self.beat("ddos_flood") as t:
            self.play(*[cell.animate.set_color(TERRACOTTA)
                        for cell in self.cells[3]],
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("ddos_aim") as t:
            self.say(t, "Many machines at once, until the service cannot "
                        "answer", fraction=0.45)
            t.hold()

        with self.beat("availability") as t:
            aim = serif("A DDoS attack targets availability.", TITLE_SIZE,
                        TERRACOTTA)
            aim = fit(aim)
            self.wipe(t)
            self.play(Write(aim), run_time=t.fill(0.5))
            t.hold()

    # --------------------------------------------------------- 7. malware

    def malware(self):
        with self.beat("malware_open") as t:
            self.section(t, "Malware: malicious software", MALWARE)
            t.hold()

        with self.beat("malware_types") as t:
            table, cells, heads = columns(
                ("Type", "How it works"), MALWARE_ROWS,
                row_gap=GAP_SM * 1.1)
            self.place(table, self.head, buff=GAP_SM * 1.2)
            self.mal_table, self.mal_cells = table, cells
            self.play(*[FadeIn(head) for head in heads],
                      Create(table.rule), run_time=t.fill(0.4))
            t.hold()

        for beat_name, index in (("virus", 0), ("worm", 1), ("trojan", 2),
                                 ("spyware", 3), ("adware", 4),
                                 ("ransomware", 5)):
            with self.beat(beat_name) as t:
                self.play(FadeIn(self.mal_cells[index][0]),
                          run_time=t.fill(0.26))
                self.play(FadeIn(self.mal_cells[index][1]),
                          run_time=t.fill(0.4))
                t.hold()

        with self.beat("mechanisms") as t:
            self.say(t, "Each one works in a different way", fraction=0.4)
            t.hold()

        lit = None
        for beat_name, index in (("virus_host", 0), ("worm_self", 1),
                                 ("trojan_deceives", 2),
                                 ("ransomware_blocks", 5),
                                 ("spyware_collects", 3)):
            with self.beat(beat_name) as t:
                moves = [cell.animate.set_color(TERRACOTTA)
                         for cell in self.mal_cells[index]]
                if lit is not None:
                    moves += [self.mal_cells[lit][0].animate
                              .set_color(GREY),
                              self.mal_cells[lit][1].animate
                              .set_color(CHARCOAL)]
                self.play(*moves, run_time=t.fill(0.45))
                lit = index
                t.hold()

        with self.beat("too_vague") as t:
            self.wipe(t)
            self.title(t, "“It's a virus” is not an answer",
                       fraction=0.12)
            t.hold()

        with self.beat("name_it") as t:
            good = prose("Name the specific threat, and say how it "
                         "works.", TITLE_SIZE, SAGE, 11.8)
            self.place(good, self.head, buff=GAP_LG)
            self.play(Write(good), run_time=t.fill(0.5))
            t.hold()

    # ------------------------------------------------------- 8. deception

    def deception(self):
        bench = None

        with self.beat("deceive_open") as t:
            self.section(t, "Attacks that target people", DECEPTION)
            bench = SortBench("Phishing", "Pharming")
            bench.next_to(self.head, DOWN, buff=GAP_MD)
            self.deceive = bench
            self.play(Write(bench.heads[0]), Write(bench.heads[1]),
                      run_time=t.fill(0.3))
            self.play(Create(bench.rules), run_time=t.fill(0.22))
            t.hold()

        with self.beat("phishing_is") as t:
            self.play(FadeIn(bench.caption(
                0, "a fraudulent message that tricks you")),
                run_time=t.fill(0.4))
            t.hold()

        with self.beat("phishing_bank") as t:
            self.play(FadeIn(bench.item(0, "pretends to be your bank")),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("phishing_link") as t:
            self.play(FadeIn(bench.item(0, "links to a fake site")),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("pharming_is") as t:
            self.play(FadeIn(bench.caption(
                1, "redirects you, correct address and all")),
                run_time=t.fill(0.4))
            t.hold()

        with self.beat("pharming_how") as t:
            self.play(FadeIn(bench.item(1, "you type the real URL")),
                      run_time=t.fill(0.4))
            t.hold()

        with self.beat("pharming_cause") as t:
            self.play(FadeIn(bench.item(
                1, "malicious code, or poisoned DNS")),
                run_time=t.fill(0.4))
            t.hold()

        with self.beat("keep_clear") as t:
            self.wipe(t)
            self.title(t, "One sentence each", fraction=0.1)
            t.hold()

        with self.beat("phishing_short") as t:
            one = callout(["Phishing", "persuades you", "to act"],
                          size=LABEL_SIZE, accent=SLATE, width=5.4)
            one.move_to([-3.4, 0.6, 0])
            self.play(Create(one[0]), run_time=t.fill(0.22))
            for line in one[1]:
                self.play(FadeIn(line), run_time=t.fill(0.18))
            t.hold()

        with self.beat("pharming_short") as t:
            two = callout(["Pharming", "redirects you", "to a fake site"],
                          size=LABEL_SIZE, accent=TERRACOTTA, width=5.4)
            two.move_to([3.4, 0.6, 0])
            self.play(Create(two[0]), run_time=t.fill(0.22))
            for line in two[1]:
                self.play(FadeIn(line), run_time=t.fill(0.18))
            t.hold()

        with self.beat("social_is") as t:
            self.wipe(t)
            self.title(t, "Social engineering", fraction=0.12)
            defn = prose("Manipulating people into weakening security "
                         "themselves.", BODY_SIZE, CHARCOAL, 11.8)
            self.place(defn, self.head, buff=GAP_LG * 0.9)
            self.social = defn
            self.play(FadeIn(defn), run_time=t.fill(0.4))
            t.hold()

        with self.beat("pretend") as t:
            who, each = chips(["A colleague", "A technician",
                               "An official"], size=LABEL_SIZE, rows=1)
            self.place(who, self.social, buff=GAP_LG * 0.8)
            self.who = who
            for chip in each:
                self.play(FadeIn(chip), run_time=t.fill(0.16))
            t.hold()

        with self.beat("social_aim") as t:
            self.say(t, "to get a password, an approval, or an "
                        "attachment opened", fraction=0.45)
            t.hold()

        with self.beat("not_only_software") as t:
            line = serif("Security is not only technical.", TITLE_SIZE,
                         TERRACOTTA)
            line = fit(line)
            self.place(line, self.who, buff=GAP_LG * 0.8)
            self.play(Write(line), run_time=t.fill(0.45))
            t.hold()

        with self.beat("people_decide") as t:
            self.say(t, "People's decisions are part of it",
                     fraction=0.45)
            t.hold()

    # -------------------------------------------------------- 9. controls

    def controls(self):
        with self.beat("controls_open") as t:
            self.section(t, "Matching controls to risks", CONTROLS)
            table, cells, heads = columns(
                ("Control", "What it reduces"), CONTROL_ROWS_A,
                row_gap=GAP_SM * 1.3)
            self.place(table, self.head, buff=GAP_MD * 1.4)
            self.ctrl_cells = cells
            self.play(*[FadeIn(head) for head in heads],
                      Create(table.rule), run_time=t.fill(0.4))
            t.hold()

        with self.beat("authentication") as t:
            self.play(FadeIn(self.ctrl_cells[0][0]),
                      FadeIn(self.ctrl_cells[0][1]), run_time=t.fill(0.45))
            t.hold()

        with self.beat("auth_kinds") as t:
            self.say(t, "a password, a biometric check, or a second step",
                     fraction=0.45)
            t.hold()

        with self.beat("two_step") as t:
            self.play(FadeIn(self.ctrl_cells[1][0]),
                      FadeIn(self.ctrl_cells[1][1]), run_time=t.fill(0.45))
            t.hold()

        with self.beat("code_to_device") as t:
            self.say(t, "a code sent to a separate device, after the "
                        "password", fraction=0.45)
            t.hold()

        with self.beat("stolen_password") as t:
            self.play(*[cell.animate.set_color(TERRACOTTA)
                        for cell in self.ctrl_cells[1]],
                      run_time=t.fill(0.45))
            t.hold()

        with self.beat("access_levels") as t:
            self.play(*[self.ctrl_cells[1][0].animate.set_color(GREY),
                        self.ctrl_cells[1][1].animate.set_color(CHARCOAL)],
                      run_time=t.fill(0.2))
            self.play(FadeIn(self.ctrl_cells[2][0]),
                      FadeIn(self.ctrl_cells[2][1]), run_time=t.fill(0.34))
            t.hold()

        with self.beat("student_account") as t:
            self.say(t, "a student may read a file but not change the "
                        "settings", fraction=0.45)
            t.hold()

        with self.beat("firewall") as t:
            self.play(FadeIn(self.ctrl_cells[3][0]),
                      FadeIn(self.ctrl_cells[3][1]), run_time=t.fill(0.45))
            t.hold()

        with self.beat("firewall_limits") as t:
            self.say(t, "though no firewall stops every kind of attack",
                     fraction=0.45)
            t.hold()

        with self.beat("antimalware") as t:
            self.wipe(t)
            self.title(t, "And four more", fraction=0.1)
            table, cells, heads = columns(
                ("Control", "What it reduces"), CONTROL_ROWS_B,
                row_gap=GAP_SM * 1.3)
            self.place(table, self.head, buff=GAP_MD * 1.4)
            self.ctrl_b = cells
            self.play(*[FadeIn(head) for head in heads],
                      Create(table.rule), run_time=t.fill(0.2))
            self.play(FadeIn(cells[0][0]), FadeIn(cells[0][1]),
                      run_time=t.fill(0.3))
            t.hold()

        with self.beat("updates") as t:
            self.play(FadeIn(self.ctrl_b[1][0]),
                      FadeIn(self.ctrl_b[1][1]), run_time=t.fill(0.45))
            t.hold()

        with self.beat("updates_why") as t:
            self.say(t, "an unpatched weakness is one an attacker can "
                        "still use", fraction=0.45)
            t.hold()

        with self.beat("encryption") as t:
            self.play(FadeIn(self.ctrl_b[2][0]),
                      FadeIn(self.ctrl_b[2][1]), run_time=t.fill(0.45))
            t.hold()

        with self.beat("https_again") as t:
            self.say(t, "HTTPS is encryption plus a check on who the "
                        "server is", fraction=0.45)
            t.hold()

        with self.beat("certificate") as t:
            self.say(t, "which is what a valid security certificate is "
                        "for", fraction=0.45)
            t.hold()

        with self.beat("https_limit") as t:
            self.wipe(t)
            self.title(t, "What the padlock does not mean", fraction=0.12)
            t.hold()

        with self.beat("fake_still_lies") as t:
            line = prose("A fake website can lie to you over a perfectly "
                         "encrypted connection.", TITLE_SIZE, TERRACOTTA,
                         11.8)
            self.place(line, self.head, buff=GAP_LG)
            self.play(Write(line), run_time=t.fill(0.5))
            t.hold()

        with self.beat("proxy") as t:
            self.wipe(t)
            self.title(t, "Two more, and then the rule", fraction=0.1)
            rest, each = chips(["Proxy server", "Privacy settings"],
                               size=LABEL_SIZE, rows=1)
            self.place(rest, self.head, buff=GAP_LG * 0.9)
            self.rest, self.rest_chips = rest, each
            self.play(FadeIn(each[0]), run_time=t.fill(0.4))
            t.hold()

        with self.beat("proxy_does") as t:
            self.say(t, "it stands between you and the servers, "
                        "filtering and hiding addresses", fraction=0.45)
            t.hold()

        with self.beat("privacy_settings") as t:
            self.play(FadeIn(self.rest_chips[1]), run_time=t.fill(0.45))
            t.hold()

        with self.beat("check_message") as t:
            self.say(t, "and you can check the sender, the wording and "
                        "the destination yourself", fraction=0.45)
            t.hold()

        with self.beat("check_link") as t:
            self.say(t, "especially before any link that asks for bank "
                        "details", fraction=0.45)
            t.hold()

        with self.beat("no_single") as t:
            self.wipe(t)
            self.title(t, "No single control stops everything",
                       fraction=0.14)
            t.hold()

        with self.beat("layers") as t:
            line = serif("Security works in layers.", TITLE_SIZE, SAGE)
            self.place(line, self.head, buff=GAP_LG)
            self.play(Write(line), run_time=t.fill(0.5))
            t.hold()

    # ----------------------------------------------------- 10. one example

    def one_example(self):
        with self.beat("example_open") as t:
            self.section(t, "A message asking for bank details", EXAMPLE,
                         fraction=0.14)
            checks, rows = numbered(CHECKS, size=LABEL_SIZE,
                                    gap=GAP_SM * 1.2)
            self.place(checks, self.head, buff=GAP_MD * 1.3)
            self.checks, self.check_rows = checks, rows
            t.hold()

        with self.beat("check_sender") as t:
            self.play(FadeIn(self.check_rows[0]), run_time=t.fill(0.45))
            t.hold()

        with self.beat("sender_address") as t:
            self.say(t, "Is the address right, and was the message "
                        "expected?", fraction=0.45)
            t.hold()

        with self.beat("check_wording") as t:
            self.play(FadeIn(self.check_rows[1]), run_time=t.fill(0.45))
            t.hold()

        with self.beat("wording_signs") as t:
            self.say(t, "Poor spelling, a threat, or a demand to hurry",
                     fraction=0.45)
            t.hold()

        with self.beat("check_destination") as t:
            self.play(FadeIn(self.check_rows[2]), run_time=t.fill(0.45))
            t.hold()

        with self.beat("text_vs_address") as t:
            self.say(t, "The words of a link need not match where it "
                        "goes", fraction=0.45)
            t.hold()

        with self.beat("do_not_enter") as t:
            self.play(FadeIn(self.check_rows[3]), run_time=t.fill(0.45))
            t.hold()

        with self.beat("contact_directly") as t:
            self.say(t, "Use a number you already trust, or type the "
                        "address yourself", fraction=0.45)
            t.hold()

        with self.beat("two_step_helps") as t:
            self.say(t, "A second step helps if your password is stolen",
                     fraction=0.45)
            t.hold()

        with self.beat("but_not_the_code") as t:
            warn = prose("But nothing makes it safe to hand the code to "
                         "an attacker.", LABEL_SIZE, TERRACOTTA, 11.6)
            self.place(warn, self.checks, buff=GAP_MD * 1.2)
            self.play(FadeIn(warn), run_time=t.fill(0.45))
            t.hold()

        with self.beat("both_matter") as t:
            self.say(t, "The controls matter, and so does what you do",
                     fraction=0.45)
            t.hold()

    # ------------------------------------------------------------ recap

    def recap(self):
        with self.beat("recap_open") as t:
            self.section(t, "Recap", RECAP)
            t.hold()

        groups = [
            (["r_internet", "r_web"], 0),
            (["r_dns", "r_browser"], 1),
            (["r_cookies", "r_blockchain"], 2),
            (["r_threats", "r_virus", "r_worm", "r_phishing"], 3),
        ]
        for beats, index in groups:
            heading, lines = RECAP_CARDS[index]
            card = None
            for position, beat_name in enumerate(beats):
                with self.beat(beat_name) as t:
                    if position == 0:
                        self.wipe(t)
                        self.title_swap(t, heading, fraction=0.14)
                        card = self.lines(*lines, size=BODY_SIZE)
                        self.stack(card, self.head, buff=GAP_MD * 1.1)
                        self.last_card = card
                    share = len(lines) * (position + 1) // len(beats)
                    already = len(lines) * position // len(beats)
                    for line in card[already:share]:
                        self.play(FadeIn(line),
                                  run_time=t.fill(
                                      0.7 / max(1, share - already)))
                    t.hold()

        with self.beat("r_ddos") as t:
            self.play(FadeIn(self.lines_extra(
                "A DDoS attack denies a service.", self.last_card)),
                run_time=t.fill(0.45))
            t.hold()

        with self.beat("r_ransomware") as t:
            self.say(t, "and ransomware locks your data until you pay",
                     fraction=0.45)
            t.hold()

        with self.beat("r_layers") as t:
            self.wipe(t)
            self.title_swap(t, "Security works in layers", fraction=0.12)
            t.hold()

        with self.beat("r_controls") as t:
            kit, each = chips(["Authentication", "Access levels",
                               "Firewalls", "Anti-malware", "Updates",
                               "Encryption"], size=LABEL_SIZE, rows=2)
            self.place(kit, self.head, buff=GAP_LG * 0.9)
            self.kit = kit
            self.play(FadeIn(kit), run_time=t.fill(0.4))
            t.hold()

        with self.beat("r_each") as t:
            self.say(t, "each reducing a different risk", fraction=0.45)
            t.hold()

    def lines_extra(self, text, card):
        line = prose(text, BODY_SIZE, CHARCOAL, FRAME_SAFE)
        self.place(line, card, buff=GAP_MD)
        return line

    def self_check(self):
        with self.beat("exam_advice") as t:
            self.wipe(t)
            self.title(t, "In the exam", fraction=0.1)
            rule = callout(["Identify the threat precisely.",
                            "Describe how it works.",
                            "Connect the control to the risk."],
                           size=LABEL_SIZE, width=9.2)
            self.place(rule, self.head, buff=GAP_LG * 0.9)
            self.rule = rule
            self.play(Create(rule[0]), run_time=t.fill(0.2))
            self.play(FadeIn(rule[1][0]), run_time=t.fill(0.22))
            t.hold()

        with self.beat("connect_control") as t:
            self.play(FadeIn(self.rule[1][1]), FadeIn(self.rule[1][2]),
                      run_time=t.fill(0.45))
            t.hold()

        with self.beat("close") as t:
            self.wipe(t)
            self.title(t, "Answer these yourself", fraction=0.1)
            asked, rows = numbered(QUESTIONS, size=MARGIN_SIZE,
                                   gap=GAP_SM * 0.9)
            self.place(asked, self.head, buff=GAP_MD)
            self.play(FadeIn(asked), run_time=t.fill(0.4))
            t.hold()

    # ------------------------------------------------------- scaffolding

    @contextmanager
    def beat(self, name):
        self._beat_name = name
        with super().beat(name) as timer:
            yield timer

    def section(self, t, text, index, fraction=0.14):
        """Open one of the eleven: clear, light the strip, name it."""
        self.wipe(t)
        if self.strip not in self.mobjects:
            self.play(FadeIn(self.strip), run_time=t.fill(0.05))
            self.keep = [self.margin, self.strip]
            self.floor = FLOOR
        head = fit(serif(text, TITLE_SIZE, CHARCOAL))
        head.to_edge(UP, buff=GAP_MD * 1.7)
        # The strip lights while the heading writes, as one play: the
        # shortest section opening here cannot afford three.
        self.play(*self.strip.focus(index), Write(head),
                  run_time=t.fill(fraction))
        self.head = head
        return head

    def title(self, t, text, fraction=0.1, color=CHARCOAL):
        head = fit(serif(text, TITLE_SIZE, color))
        head.to_edge(UP, buff=GAP_MD * 1.7)
        self.play(Write(head), run_time=t.fill(fraction))
        self.head = head
        return head

    def title_swap(self, t, text, fraction=0.1, color=CHARCOAL):
        head = fit(serif(text, TITLE_SIZE, color))
        head.to_edge(UP, buff=GAP_MD * 1.7)
        if self.head is not None and self.head in self.mobjects:
            self.play(Transform(self.head, head), run_time=t.fill(fraction))
        else:
            self.play(Write(head), run_time=t.fill(fraction))
            self.head = head
        return self.head

    def lines(self, *texts, size=BODY_SIZE, color=CHARCOAL,
              buff=GAP_SM * 1.3, align=None, width=FRAME_SAFE):
        group = VGroup(*[prose(x, size, color, width) for x in texts])
        if align is None:
            group.arrange(DOWN, buff=buff)
        else:
            group.arrange(DOWN, buff=buff, aligned_edge=align)
        return group

    def stack(self, group, top=None, buff=GAP_MD, floor=None, align=ORIGIN):
        floor = self.floor if floor is None else floor
        for factor in (1.0, 0.85, 0.7, 0.55, 0.42, 0.32, 0.24):
            gap = buff * factor
            group.arrange(DOWN, buff=gap, aligned_edge=align)
            if top is None:
                group.move_to(ORIGIN)
            else:
                group.next_to(top, DOWN, buff=gap)
            if group.get_bottom()[1] >= floor:
                return group
        raise ValueError(
            f"Beat '{self._beat_name}': a stack {group.height:.2f} units "
            f"tall cannot clear y={floor} under this heading. Shorten it.")

    def place(self, mobject, top=None, buff=GAP_MD, floor=None):
        floor = self.floor if floor is None else floor
        for factor in (1.0, 0.9, 0.78, 0.66, 0.55, 0.45, 0.35):
            if top is None:
                mobject.move_to(ORIGIN)
            else:
                mobject.next_to(top, DOWN, buff=buff * factor)
                mobject.move_to([0, mobject.get_center()[1], 0])
            if mobject.get_bottom()[1] >= floor:
                return mobject
        raise ValueError(
            f"Beat '{self._beat_name}': there is no room under this content "
            f"for something {mobject.height:.2f} units tall above "
            f"y={floor}. It would land on the numbered strip.")

    def clear(self, t, *groups, fraction=0.1, with_note=False):
        family = set()
        for group in groups:
            if group is None:
                continue
            family.update(id(m) for m in group.get_family())
        present = [m for m in self.mobjects
                   if any(id(child) in family for child in m.get_family())]
        if with_note and self.note is not None and self.note in self.mobjects:
            present.append(self.note)
        if present:
            self.play(*[FadeOut(m) for m in present],
                      run_time=t.fill(fraction))
        if with_note:
            self.note = None

    def wipe(self, t, fraction=0.05):
        old = [m for m in self.mobjects if m not in self.keep]
        if old:
            self.play(*[FadeOut(m) for m in old], run_time=t.fill(fraction))
        self.head = self.note = self.side = None

    def say(self, t, text, fraction=0.2, color=GREY, size=LABEL_SIZE,
            y=None, anchor=None, buff=GAP_MD):
        """The running line of commentary, swapped in place."""
        line = prose(text, size, color, 12.0)
        if anchor is not None:
            self.place(line, anchor, buff=buff)
        else:
            line.move_to([0, self.floor + 0.35 if y is None else y, 0])
            self.band_is_clear(line)
        if self.note is None or self.note not in self.mobjects:
            self.note = line
            self.play(FadeIn(line), run_time=t.fill(fraction))
        else:
            line.move_to(self.note)
            self.play(Transform(self.note, line), run_time=t.fill(fraction))
        return self.note

    def band_is_clear(self, line, tol=0.05, clearance=0.08):
        """Refuse to print commentary through whatever is already there.

        The acceptance check compares writing against writing, so a
        caption laid across a diagram reads as clean to it: a box is a
        shape, not text. This reserves the band at the foot of the frame
        for one line of commentary, and it demands a positive gap rather
        than merely the absence of overlap -- a caption whose ascenders
        stop two hundredths of a unit under a box reads as touching it.
        """
        for mobject in self.mobjects:
            if mobject in self.keep or mobject is self.note:
                continue
            wide = (min(line.get_right()[0], mobject.get_right()[0])
                    - max(line.get_left()[0], mobject.get_left()[0]))
            high = (min(line.get_top()[1], mobject.get_top()[1])
                    - max(line.get_bottom()[1], mobject.get_bottom()[1]))
            if wide > tol and high > -clearance:
                what = getattr(mobject, "text", None) or type(mobject).__name__
                raise ValueError(
                    f"Beat '{self._beat_name}': the commentary band at "
                    f"y={line.get_center()[1]:.2f} "
                    f"(y {line.get_bottom()[1]:.2f} to "
                    f"{line.get_top()[1]:.2f}) runs through {what!r} "
                    f"(y {mobject.get_bottom()[1]:.2f} to "
                    f"{mobject.get_top()[1]:.2f}), overlapping "
                    f"{wide:.2f} x {high:.2f} units. Move the figure or "
                    f"drop the line."
                )
