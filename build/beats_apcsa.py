"""Beat placement for the AP Computer Science A exam-strategy lecture.

Run from the repo root:

    python build/beats_apcsa.py

The recording carried a false start on the wrap-up, slated out loud as
"take two, wrap up". There was ONE opening take, not two: the first
twenty-six seconds of the file are silence at -68 dB.

The audio the pipeline reads is made from the raw file by these two
commands, in this order, so the same recording reproduces the same mp4:

    python build/transcribe.py audio/APCSA-exam-strategy-raw.m4a \\
        --language en --chunk 90

    python build/retake.py audio/APCSA-exam-strategy-raw.words.json \\
        --audio audio/APCSA-exam-strategy-raw.m4a \\
        --out APCSA-exam-strategy-cut \\
        --drop "Alright so here is this strategy to carry forward it"="take two wrap up"

    python build/segment.py audio/APCSA-exam-strategy-cut.words.json \\
        --audio audio/APCSA-exam-strategy-cut.m4a \\
        --cut APCSA-exam-strategy="Welcome to AP computer science exam" --pad 1.0

The drop starts at "Alright so", not at the strategy line: the aborted
take opens with it, and anchoring one phrase later leaves a stray "Alright,
so" stuck to the front of take two.

Anchors below are taken from the transcript of what remains, mis-hearings
included, never from the written script: "exam authority" is exam
strategy, "two scenarios" is two sections, "multiple choice waiting" is
weighting, "every list" is ArrayList, "Tacing" is pacing.
"""

from mkbeats import build

BEATS = [
    # ------------------------------------------------ welcome and alignment
    ("open", "Welcome to AP computer science exam"),
    ("right_exam", "before we begin, let's make sure we are preparing for the right exam"),
    ("aligned", "this lecture is aligned with the latest AP computer science"),
    ("ced", "The course and exam description effective fall 2025"),
    ("digital_note", "It also reflects the current digital exam format"),
    ("goal", "the goal today is not to memorize a pile of"),
    ("goal_real", "It is to practice a reliable way to read, reason about and write Java"),

    # ------------------------------------------------- the shape of the exam
    ("exam", "The APCSA exam is fully digital and taken in Blue Book"),
    # He says "two scenarios"; it is two SECTIONS, and the screen says so.
    ("two_sections", "It has two scenarios"),
    ("mcq", "You'll have 90 minutes for 42 multiple choice"),
    ("mcq_pct", "That section is, you know, 55"),
    # "worth 45 minutes" — it is 45 PERCENT, which he corrects himself
    # one sentence later.
    ("frq", "Then you'll have 90 minutes for the four"),
    ("split", "So First one is 55"),
    ("quickref", "The Java Quick reference is available in blue book"),
    ("quickref_use", "use it to confirm unfamiliar library methods when appropriate"),
    ("pacing", "target for multiple choices about two minutes per question"),
    ("keep_moving", "keep moving so one difficult question doesn't take time away"),

    # ------------------------------------------------ the four units, weighted
    ("units", "The framework organizes the course into four units"),
    ("u1", "Unit one covers using objects and methods"),
    ("u2", "two covers selection and iteration"),
    ("u3", "unit three covers class creation"),
    ("u4", "unit four covers data collections"),
    ("weighting", "The multiple choice waiting gives unit 4 the largest range"),
    ("w2", "unit 2 is also substantial at 25"),
    ("w13", "Unit 1 is 15"),
    ("plan", "Use these ranges to plan your review"),
    ("arrays_time", "Give Arrays Array List and"),
    ("loops_too", "Keep practicing, you know, practicing loops and conditionals"),
    ("dont_skip", "don't skip methods, objects, or class design"),

    # ----------------------------------------------------- what changed
    ("changed", "The revised framework adds more attention to data"),
    ("datasets", "You may need to reason about datasets, how data was collected"),
    ("conclusions", "What conclusions can reasonably be drawn from it"),
    ("files", "It also includes reading text files"),
    # "using computers reasonably" — the practice is called using computers
    # RESPONSIBLY, which is what the screen shows.
    ("practice5", "The framework also names a fifth computational thinking practice"),
    ("ethics", "Questions in this area can ask you to consider the ethical or social effects"),
    ("inheritance", "Designing and implementing inheritance relationships is outside the scope"),
    ("still_in", "don't take that to mean that"),
    ("still_list", "Searching, Sorting, and Recursion remain in the current framework"),
    ("lesson", "So the practical lesson is simple"),
    ("older", "college board says earlier release exams do not completely align"),

    # --------------------------------------------- multiple choice: trace it
    ("trace", "for multiple choice, your strongest habit is to trace the code"),
    ("dont_skim", "Don't skim and answer based on what the program seems to be doing"),
    ("read_stem", "Start by reading the question"),
    ("what_asked", "Are you being asked for printed output, a final variable value"),
    ("walk", "Then walk through the code in order"),
    ("trace_table", "make a small trace table"),
    ("one_stmt", "update them on a statement at a time"),
    ("loop_check", "For a loop, record the value before and after each iteration"),
    ("watch", "Watch closely for common sources of mistakes"),
    ("last_index", "With an array, remember that the final valid index is one less"),
    ("eliminate", "If you're stuck, eliminate choices only when the code rules them out"),
    ("mark_return", "Mark the question and return to it after you have collected the easier points"),
    ("no_debate", "Don't let uncertainty turn into a long, unstructured debate"),

    # ---------------------------------------- free response: follow the spec
    ("frq_spec", "The free response section asks you to write code that meets the specification"),
    ("checklist", "Treat the prompt as a checklist"),
    ("identify", "Identify the required method or constructor"),
    ("examples", "Use the example in the prompt as test"),
    ("boundary", "Then check boundary cases such as an empty collection"),
    ("clear_java", "Write the clearest correct"),
    ("braces", "Use braces and indent"),
    ("not_compiled", "Since your answer is typed and it and isn't compiled"),
    ("partial", "If you're unsure how to solve the whole problem"),
    ("credit", "A clear loop condition or class component may still earn credit"),

    # ------------------------------------------------- the four FRQ focuses
    ("four_frq", "The current free response section has four stated focuses"),
    ("q1", "Question one is method and control structure"),
    ("q2", "Question 2 is class design"),
    ("q3", "Question three is data analysis with every list"),
    ("q3_shift", "If your method removes elements while traversing"),
    ("q4", "question 4 is 2D array"),
    ("q4_bounds", "check that your loop bounds make the arrays dimensions"),

    # ----------------------------------------------------- practice routine
    ("practice", "The practice should look like the exam you are preparing for"),
    ("bluebook", "use blue book practice so that digital setting feels familiar"),
    ("timed", "do time sets of multiple choice questions"),
    ("frq_timer", "For free response, write complete answers on a timer"),
    ("compare", "compare your work with the scoring guidelines"),
    ("exact_req", "Look for the exact requirement you missed"),
    ("current_mats", "use Current AP classroom"),
    ("check_old", "Earlier exam questions can help you practice concepts"),

    # ------------------------------------------------------------- wrap-up
    ("recap", "All right, let's recap"),
    ("carry", "Here is the strategy to carry forward"),
    ("prioritise", "prioritize the higher weight content without ignoring any unit"),
    ("changes", "Remember the recent changes"),
    # The delivery garbles this line and ends up saying text-file reading is
    # out of scope. It is inheritance that is out; text files are IN. The
    # screen carries the correct form.
    ("changes_list", "the revised framework ads, data sets, data ethics"),
    ("four_focus", "the four current free response focuses are methods and control structures"),
    ("aligned_again", "This lecture is aligned with the latest AP computer science, a framework college board list for 2026"),
    ("close", "Work from the current framework, practice deliberately"),
]

NOTE = ("AP Computer Science A exam strategy, aligned with the CED "
        "effective Fall 2025 and current for 2026-27. Aborted wrap-up take "
        "removed with build/retake.py; beats placed by anchor phrase, see "
        "build/beats_apcsa.py.")

if __name__ == "__main__":
    build("APCSA-exam-strategy", "cs.ap_csa_strategy", BEATS,
          "APCSA-exam-strategy", NOTE)
