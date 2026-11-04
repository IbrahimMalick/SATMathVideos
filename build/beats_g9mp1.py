"""Beat placement for the Grade 9 model paper, Chapters 1 to 4.

Run from the repo root:

    python build/beats_g9mp1.py

The delivery mixes Urdu and English, and the anchors are copied from the
transcript as it came out rather than from the written plan. The English
survives well enough to anchor on; the Urdu stretches come back as
nonsense ("I won't go I'm going to cut my game in the beach with or not"),
so no anchor is placed inside one.

The transcript is the chunked one — build/transcribe.py --chunk 90. The
single-pass transcript of the same audio dropped 188 seconds across
fourteen stretches, one of which was the 23 seconds that give Question
6(b) its answer, so anchors written against it would have been placed
against speech that was not there.
"""

from mkbeats import build

BEATS = [
    # ----------------------------------------------------------- opening
    ("open", "Assalamu alaikum, welcome to the digital"),
    ("topics", "We'll cover real numbers logarithms sets and functions"),
    ("method", "I explain each step for you"),
    ("disclaimer", "It's not a prediction of the exact annual exam"),

    # ------------------------------------------------------------- route
    ("route", "So let us begin with the moral paper multiple choice"),
    ("notebook", "I want her up video could pause get all"),

    # ------------------------------------------------- MCQ 1: conjugates
    ("mcq1", "first question ask us too multiply three plus the square root"),
    ("mcq1_identity", "These expressions are conjugates, okay We can use this identity"),
    ("mcq1_work", "So we get the 3 squared minus the square root of 5"),
    ("mcq1_answer", "which equals 4 right for you have a rational number"),
    ("mcq1_habit", "When you see conjugates remember that The middle terms cancel"),

    # -------------------------------------------- MCQ 2: common logarithm
    ("mcq2", "A common logarithm has based at"),
    ("mcq2_answer", "So the correct answer is 10"),

    # ------------------------------------------------- MCQ 3: power set
    ("mcq3", "give the empty set It contains no elements"),
    ("mcq3_reason", "So, there is exactly one subset that's empty"),
    ("mcq3_answer", "The what the power said Is a set whose only element"),
    ("mcq3_trap", "but be careful read the empty set and this set containing"),

    # ---------------------------------------------- MCQ 4: intersection
    ("mcq4", "So we are given that the number of elements in A union B"),
    ("mcq4_formula", "The Number a union b equals the number a Plus"),
    ("mcq4_substitute", "Values go substitute grow 50 equals 30 plus 30 plus 35"),
    ("mcq4_work", "30 plus thirty five is 65, so So the intersection"),
    ("mcq4_answer", "is sixty five minus fifty, which is fifteen"),
    ("mcq4_why", "So we subtract The intersection because those shared elements"),

    # ----------------------------------------------------- MCQ 5: the LCM
    ("mcq5", "so find the least common multiple of 16 x squared 4x 30 x y"),
    ("mcq5_numbers", "find the least common multiple Of the numerical coefficients"),
    ("mcq5_vars", "Next we will take each variable with its greatest power"),
    ("mcq5_answer", "So the least common multiple Is 240 X squared"),

    # ------------------------------------------------ MCQ 6: common factor
    ("mcq6", "Okay now it's factorized 12X plus 36"),
    ("mcq6_divide", "12x divided by 12 is x, 36 divided by 12 is 3"),
    ("mcq6_answer", "the answer is 12 multiplied by the quantity X plus three"),
    ("mcq6_check", "I'm just going to multiply back right twelve times x"),

    # ------------------------------------------ short: rational numbers
    ("sq1", "Now, find two rational numbers between 2 and 3"),
    ("sq1_pick", "One possible answer is 2 point 25 And Two point five"),
    ("sq1_fractions", "Two point two is nine over four and 2 .5 is"),
    ("sq1_answer", "the correct answers 9 over 4 and five over two"),
    ("sq1_note", "or be answers get possible"),

    # --------------------------------------- short: fractional indices
    ("sq2", "simplify three over four to the power negative 2 divided by"),
    ("sq2_negative", "so a negative exponent means we take the reciprocal"),
    ("sq2_cube", "four over nine cubed is 64 Over seven hundred and twenty"),
    ("sq2_divide", "fraction means multiplying by its reciprocal"),
    ("sq2_cancel", "729 divided by 27 is 27 and 16 divided by 64"),
    ("sq2_answer", "so after that what remaining multiplication the answer is 12"),

    # ----------------------------------------- short: logarithmic equation
    ("sq3", "if log base 10 of x equals negative three find X"),
    ("sq3_rewrite", "this means ten must be raised to the power negative 3"),
    ("sq3_answer", "Therefore, x equals 0 .001"),

    # ------------------------------------------- short: the characteristic
    ("sq4", "Now find the characteristics of 0 .000049"),
    ("sq4_rule", "So for a positive number less than one characteristic is negative"),
    ("sq4_move", "move decimal point till first non -zero digit is left"),
    ("sq4_answer", "So the characteristic is negative five in bar notation"),
    ("sq4_note", "if you use a log table that the characteristic is negative"),

    # ------------------------------------------------- short: power set
    ("sq5", "Next question, write the power set of"),
    ("sq5_count", "Again there are four elements So The numbers Of subsets"),
    ("sq5_list", "The single element subsets are part plus minus multiplication"),
    ("sq5_sum", "So what does that give you? That gives 16 subsets all together"),

    # --------------------------------------------- short: set difference
    ("sq6", "next question and define a minus B"),
    ("sq6_words", "The difference of two sets written A minus be contains the elements"),
    ("sq6_notation", "to a but do not belong to be"),
    ("sq6_example", "if a contains one two three and four and B contains"),
    ("sq6_answer", "then A minus B contains 1 into right"),

    # ----------------------------------------- short: quadratic factorize
    ("sq7", "now let's factorize x squared plus or X minus 12"),
    ("sq7_find", "we need two numbers whose product is negative 12"),
    ("sq7_numbers", "those numbers are positive four and negative three"),
    ("sq7_split", "middle term into 4x minus 3 x"),
    ("sq7_group", "Now let's group them. x times the quantity x plus 4"),
    ("sq7_answer", "The answer is x plus four multiplied by X minus three"),

    # ------------------------------------------- short: difference of cubes
    ("sq8", "Now we will factorize 125 a cubed minus 1"),
    ("sq8_cubes", "125 a cubed is the cube of 5a"),
    ("sq8_identity", "Use The Difference of Cubes Identity A cubed minus b cubed"),
    # He says "five minus 1" here; it is 5a - 1, and the screen says so.
    ("sq8_answer", "so factorization factorization is five minus 1 multiplied by 25"),

    # ------------------------------------------- long 5(a): indices
    ("lq1", "next test simplify 25 to the power 3 over 2 multiplied by"),
    ("lq1_rule", "So First of All What Will You Do"),
    ("lq1_a", "25 to the Power 3 over 2 means the square root"),
    ("lq1_b", "next check again 243 to The Power 3 Over 5"),
    ("lq1_c", "so denominator 16 to the power five over four fourth root"),
    ("lq1_d", "So finally eight to The power four over three"),
    # "165 times 27" is said here; the working needs 125, and so does the
    # 3375 he gives next. The screen carries 125.
    ("lq1_combine", "twenty seven divided by thirty two times sixteen the numerator"),
    ("lq1_answer", "fraction cannot be simplified further So the answer is"),

    # --------------------------------------- long 5(b): the antilogarithm
    ("lq2", "okay now here's a question find x if log of x equals"),
    ("lq2_undo", "first undo a common logarithm raise 10 to the two both sides"),
    ("lq2_split", "write negative Two point zero One Eight Four as negative three plus"),
    ("lq2_parts", "x equals 10 to the negative 3 multiplied by ten"),
    ("lq2_antilog", "Now we will use the algorithm table"),
    ("lq2_answer", "the three significant figures X is me zero point zero zero nine"),

    # ----------------------------------------- long 6(a): overlapping sets
    ("lq3", "Club has 98 students 58 joint swimming and 50 joined tug of war"),
    ("lq3_setup", "So let A represent this student's who joined swimming"),
    ("lq3_formula", "The number in A plus the number in B minus a number in both"),
    ("lq3_substitute", "substitute values carrying 98 equals 58 plus 50 minus the overlap"),
    ("lq3_work", "108 and 108 minus 98"),
    ("lq3_answer", "so 10 is students join both"),

    # -------------------------------------------- long 6(b): the quartic
    ("lq4", "I mean look for a difference of squares"),
    ("lq4_rewrite", "you can write the expression as X squared plus 3Y is squared"),
    ("lq4_expand", "Let's check the first square it expands to x to the fourth"),
    ("lq4_check", "subtracting gives us 6 minus 36 which is negative 30"),
    ("lq4_identity", "now use the difference of squares identity a squared minus b squared"),
    ("lq4_answer", "The answer is x squared plus three y squared minus six"),

    # ----------------------------------------------------------- closing
    ("recap", "Now let's recap this"),
    ("recap_methods", "So we used conjugates to simplify an expression with the square"),
    ("recap_sets", "Then we used the set overlap formula and practiced least common"),
    ("next", "We will complete the model paper of 2026"),
    ("close", "Insha Allah we shall meet in next session"),
]

NOTE = ("Grade 9 Mathematics 2026 model paper, Chapters 1 to 4. Mixed Urdu "
        "and English delivery, English slides. Transcribed with --chunk 90; "
        "beats placed by anchor phrase, see build/beats_g9mp1.py.")

if __name__ == "__main__":
    build("G9MP1-chapters-1-4", "concept.g9_model_paper", BEATS,
          "G9MP1-chapters-1-4", NOTE)
