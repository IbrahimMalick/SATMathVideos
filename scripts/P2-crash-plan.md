---
scene: concept.paper2_walkthrough
---

<!-- Body is the transcript verbatim so the aligner matches exactly. The screen renders correct pseudocode and spelling where the delivery or transcriber is loose: TEAR not tier, DROUGHT not draw, ANNUAL not animal, MOD <> 0. -->

[[beat:hook]] If you have an old level computer science paper two exam coming up, I
want you to stay with me through this lecture. Okay, I'm going to [[beat:promise]]
take an actual 2026 paper two and show you not just what the answers are, but how to
think when you do not immediately know the answers, right? [[beat:by_end]] By the end
of this lesson, you should have a method to trace tables, validation, debugging,
searching, searching, boolean logic, databases, and most importantly, the 15 mark
programming code. And [[beat:stepup]] I want you to remember six letters, okay? Step
up. S, [[beat:s_step]] step through one instruction at a time. And then T is for tier,
[[beat:t_tear]] tier big problems and small requirements. [[beat:e_establish]] E is
for establish initial values. And [[beat:p_preserve]] P is for preserve variable
values until an instruction changes them. [[beat:u_use]] U is for use intermediate
results and [[beat:p_plan]] P is for plan before your code. The reason I share this
with you is that it helps me or, you know, larger problem if I had, you know, cute
little acronyms for them. So step up is what we're going to be talking, all right? And
one warning before we begin, all right, [[beat:warning]] do not memorize this paper.
Cambridge can change the scenario, you know, learn the pattern underneath the
question. All right, so I'm going to start with the question number one of the May
2026 computer a science exam or it's a paper too. So [[beat:q1]] question one, it
starts gently, right? Which pseudocoded structures are both forms of iteration, right?
[[beat:q1_mean]] So what does iteration mean, right? Iterations simply means repeats.
So for next repeats, right? While, do, and while repeats. If is a selection. Case is a
selection, right? [[beat:q1_answer]] So the correct answer is C, right? The official
market scheme gives C, right? All right. So iteration equals repetition. Just remember
that, right? It's a quick exam habit. [[beat:families]] Classify structures into three
families. Sequence, one thing after another. Selection, decisions, iteration,
repetition. I'll repeat it, right? Sequence is one thing after another. Selection is
decisions, right? And iteration is repetition. All right, [[beat:q2]] let's move to
question number two, all right? So the next question asks, which data type stores a
single letter, symbol, or digit entered from the keyboard, right? [[beat:q2_char]] So
one characteristic means char, right, c -a -r, c -h -a -r. If I store seven as a
character, that is not the same as the storing the integer 7, okay? [[beat:q2_answer]]
So the answer is B, char, okay? So memory line is one character equals char, all
right? [[beat:q3]] Now question 3A and 3B are for validation, right? So now Cambridge
starts testing terminology. [[beat:presence]] If a field must not be left blank, that
is a presence check, okay? [[beat:checkdigit]] If an additional calculated digit is
added to a number to detect errors, that's a checked digit, right? Those are the two
answers in that market scheme, right? [[beat:format]] Then a format checks whether
data follows the required pattern or structure. For example, suppose a date must look
like dd slash mm slash yyy, right? So a format check can check whether the input
follows that pattern. I want you to notice something important, right?
[[beat:format_trap]] Format does not necessarily mean correct, okay? Like 99 slash 99
slash 2036 may fit the shape of a date while not being a sensible date, right? Because
they're not, they're not 99 months in a year, they're not 99 days in a month, right?
So that distinction matters, okay? The marking guidance expects the idea of a required
patronage structure and an appropriate example such as date format. All right, so
[[beat:q3c]] the question 3C is a validation algorithm, right? Now we have to write
pseudocode. So we need to collect 15 valid whole numbers. The keyword is valid, right?
If somebody gives us a bad value, that must not consume one of our 15 array positions,
right? [[beat:valid_first]] So validate first, store second. [[beat:two_loops]] So I
need two different kinds of repetition. The outside loop counts the 15 accepted rules.
The inside loop keeps asking until the current value is valid. So [[beat:q3c_code]]
this is the pseudocode we are going to write. So for counter plus 1 to 15, repeat
output, enter a whole number. Input is a value. right? If mod value one, right? The
zero then, output is invalid input, okay? Now, let me explain this, right?
[[beat:mod_why]] Why use mod value comma one? A whole number divided by one leaves
remainder zero, okay? And notice where we store the value after it passes validation.
[[beat:q3c_marks]] The marker scheme awards marks for the 15 input loop, input integer
test, repeated input, correct storage, and appropriate message. Then connect the
short, right? And [[beat:and_or]] whenever the question is about a valid range,
remember the short about inside equals and outside equals or. All right so [[beat:q4]]
question number four is coding and testing right this question is worth six marks So
one vague sentence is not enough. Let's split it into coding and testing, right? What
is coding? [[beat:coding]] Coding equals means build, right? So during coding, the
programmer converts the design into program code. They may use pseudocode, flowcharts,
or structured diagrams from the design stage. They may create procedures and
functions, and they can add comments so the code is understandable and maintainable,
right? And they may test small sections as they're developed. Then testing, right?
What does actually mean? [[beat:testing]] That means testing means try to break it.
So, during the testing, we test the finished program using data for which we know the
expected result. We can use normal, abnormal, binary, or extreme tests, right? We
compare actual results with expected results. If something goes wrong, we debug it and
test again. So [[beat:q4_marks]] Cambridge rewards up to three marks for coding and
three for testing, right? So including code creation, comments, routines, development
tools, test data and debugging. So here is what I want you to remember, okay?
[[beat:q4_rule]] Coding builds it, testing tries to break it. All right, so let's go
on to [[beat:q5]] question number five, which is debugging, searching and flight,
right? So now we hit one of the most useful questions in this paper, okay?
[[beat:q5_task]] The program should search a two dimensional array using an account ID
and display the matching customer name. But four lines are wrong. Here's a
[[beat:ple]] debugging rule, right? Purpose, line, effect. First, understand what the
program is supposed to do. Then read each line and ask, does this instruction actually
help achieve that purpose? So [[beat:err1]] in the example error one, the account ID
contains letters and numbers, but it has been described as an integer, right? So it
should be declare account ID colon string, right? Now, [[beat:err2]] this error number
two is we need to receive the account ID from the user, right? Not display it. So
input account ID, that's the error number two. [[beat:err3]] Now the error number
three, we're testing one Boolean condition. So use if, not case, right? So if account
ID equals accounts row one then, right? [[beat:err4]] Now error number four, right?
And this one catches the students of God, right? So algorithm displays the name from
row one. even if the match occurred on row 427. So use the current row, right? So
output accounts, row 2, right? So those are the four corrections in the official
marking guidance, right? Then what we do? [[beat:linear]] Then what search algorithm
is this? Row 1, row 2, row 3, one after another, right? So it's a linear search. It's
also called sequential. All right. So [[beat:q5c]] question C is now imagine we reach
the entire array and find nothing. The computer needs to remember whether a match ever
happened, right? [[beat:flag]] That is what a Boolean flag is for. Okay. Found false
true, right? Check. [[beat:flag_code]] So before the search, nothing has been found.
So inside match, right? Found is true if that is true. So after the loop, we'll have
it found false, then I'll put account note found. So the [[beat:flag_marks]] mark
scheme explicitly rewards initializing the flag before the loop, setting it when the
record is fine and checking it after the loop. Remember, a flag remembers whether
something happened. Once it becomes true, it stays true unless another instruction
changes it, okay? [[beat:rule_p]] That is a step up rule P, they preserve variables.
[[beat:q6]] Question number six is trace table. This is the question that catches the
students who try to trace algorithm inside their heads, don't. The thing is that
[[beat:rerm]] you have to read, execute, record, and move. The algorithm takes us word
and compares one character with the next character. [[beat:numletter]] Num letter is
not the letter. right? It is the position number. [[beat:post]] For post position one,
P versus O not equal, right? The counter state is zero. Position number two, O versus
S is still zero. Position number three is S versus T is still zero, right? So output
is zero, then choice Y. Okay. [[beat:committee]] So we process another word,
committee, right? So CO doesn't match, right? No. OM, no, right? mm, yes. So count
becomes one. Mi, no. [[beat:no_change]] Does the count return to zero? No, right? No
instruction changes it. And it is still one. Tt is a match, right? So now count goes
to two, right? Te is still two, right? But ee is a match, so output would be, so count
three, so output would be three, right? So the published The stress gives zero for
post and three for committee. After the second choice is end processing stops, right?
So bookkeeper is never processed, okay? So [[beat:purpose]] what is the purpose of the
algorithm? It counts pairs of identical consecutive letters. That is the accepted
purpose. No assignment equals no change. All right, let's go to [[beat:q7]] question
number seven, file handling. Ask yourself, why do, why store data in a file, right?
Because we often need the data to remain available after the program stops or machine
is switched off, right? [[beat:why_file]] Files provide persistent, non -volatile
stories. So the mark scheme also accepts letter reuse, backup and sharing transport,
right? To read one name from a text file, [[beat:file_seq]] remember our simple
sequence, declare, open, read, and close. Okay, so for example, right, declare name is
string, open file name .txt for read okay open file names that txt name right close
file names that txt so those are the four elements Cambridge awards marks for all
right [[beat:q8]] now questionnaire is a Boolean logic here is where students make a
very predictable mistake [[beat:one_jump]] they try to solve the entire Boolean
expression expression in one mental jump. Okay, so don't do that. Step up rule U,
[[beat:intermediates]] use intermediate results. So first you'll do, you know, what
you'll do is you'll create plane x1, not c, right? x2, b, or x1. x3, not x2. x4, a, n,
c. z, x3, xor, x4. And one operation at a time. One truth table at a time, right?
[[beat:circuit]] For the circuit, C first passes through NOT. The result B, the result
and B enter OR, right? The OR output is inverted, right? Separately A and C enter NAND
and finally those two branch outputs enter XOR. Okay, so the truth table final output
is this, what I'm showing you, right? Those eight outputs match the published market
scheme. If you're getting Boolean questions wrong, [[beat:mechanical]] stop trying to
be clever, right? Be mechanical. One gate, one result. All right, so the [[beat:q9]]
question number nine is about database and SQL. It gives us a car parts database,
right? It started by choosing data types based on what the value actually represents.
[[beat:datatypes]] So field part ID, data type would be text. Part name, data type
would be text, right? Car type could be an integer or text. Price would be real,
right? Size of the text, color, it's character, number in a stock is integer, right?
In a stock is a Boolean. It's either true or false, right? So the market scheme except
those types, including either integer or text for car type and several representations
for in a stock, right? Okay, [[beat:sql_three]] I teach SQL with three questions. What
do I want? Where is it? Which records, right? So here, as you can look at the SQL
code, [[beat:sql_code]] Select part ID, car type, number in stock. Okay? Where am I
selecting it from car parts? Right? Where, part name, and the name of the brake pads,
for example. Right? That is the required SQL structure. Why don't we really need, I
mean, why don't we really need in a stock? Right? [[beat:redundant]] Because number in
a stock already tells us. Zero means out of stock, a positive quantity means in stock.
right? So storing both repeats the same fact and creates an opportunity for
inconsistency. Okay? So Cambridge rewards the two marks for identifying number in a
stock as an alternative source and explaining how its value determines the stock
status, right? So here's what I want you to remember. [[beat:sql_rule]] Select what,
from where, from which. All right? Cool with that? Very good. So, [[beat:q10]] this is
the set up for the 15 marker, all right? Now [[beat:fear]] we read the question most
students fear, 15 marks. Your instinct is to immediately start writing through the
code, like a code monkey, okay? But it's not. [[beat:plan_first]] The first thing we
write is not code. Plan before you code, okay? Cambridge asks us to
[[beat:requirements]] process a year of rainfall using an array. We need
initialization, input, totals, an average, number of dry days, longest consecutive dry
spell, and a draw decision, right? [[beat:tear_down]] This is not one problem, right?
Let's tear it down, okay? So on store 365 values is array, okay? Start array values,
initialize, then get values, input plus loop. Animal rainfall is accumulator, right?
Mean is a calculation. Dry days is a counter. Longest dry period, current is 3 plus
maximum. Drawed is if, and results is outcome. [[beat:patterns]] The 15 mark question
has disappeared now, right? Now what we have, what remains are programming patterns we
already know. So the marking itself separates the task into declarations, input
calculations counting max, and output draw decision, with up to nine AO2 marks and six
AO3 marks. All right, so first what we'll do, [[beat:blocks]] we'll break it down into
blocks, all right? The first block that we'll do is declare initialize, all right? So
here what we're gonna do, [[beat:declare]] declare rainfall array one to 365 of real,
right? Declare day would be an integer, declare total rain is real, declare total cm
is real and declare average rain is real, declare no rain days, that's an integer,
right? Declare current dry run, that's an integer, declare longest dry run, that's an
integer. I mean, use meaningful variable names, right? That actually matters in the
quality of a long programming solution, right? All right. Then what we do is, then now
we're going to a plain text for day one to 365 rainfall day, greater than zero. All
right. So, and then next day. And what we do is total rain, no rainfalls, current dry
run, and longest run. So that's a [[beat:init]] step up rule E, establish initial
values, never assume a counter or total magically starts at zero, right? The mark
scheme explicitly includes initialization and meaningful and appropriate program
structure. The next plot that we're going to hit [[beat:input_block]] would be input
data. So for day 1, 2, 3, 6, 5, right? Output is enter rainfall in mm. Remember, non
-centimeters and millimeters for day, right? Today, input rainfall. Day gives us both
the repetition and the array position. Okay. Now, [[beat:total_avg]] we'll go into the
total and average. All right. So for day one to 365, total rain, total rain plus
rainfall day, then what we'll do is we'll do average rain. All right. So what are we
doing here? Average rain, total rain. divided by 365, right? So total cm, that's in
centimeter, right? Round, total rain. [[beat:accumulator]] Notice the accumulator,
total rain, total rain plus, okay? We add the existing value, we do not replace it. So
[[beat:rounding]] Cambridge requires total rain in centimeters rounded to two decimal
places and the mean in millimeters rounded to four decimal places, right? So, now,
this is what some people consider. Some people want to, you know, consider the hard
part, right? [[beat:dry_days]] The consecutive dry days. But it's not, right? It's
important. It's an important, most important idea in this entire marker, right? So use
this, you know, for example, 505 centimeters and 0 ,0800, right? Now, rain, we're
going to show rain, current dry run, longest dry run. All right, so we're going to
record that. Rain occurs, right? The current dry street dies, but the record does not
disappear. Okay? So for example, if there are five dry days and then rain occurs,
right? I mean the current dry streak, the current dry streak dies, but the record does
not appear, right? Why? Because [[beat:resets]] the current resets, but the record
survives, right? [[beat:dry_code]] So here's what we do. For day one to 365 total
rain, total rain plus rainfall day, right? If rainfall is equal to zero, then no
rainfall, no rain days, no rain days plus one. So that's how you're going to count
your dry spell. If current dry run is larger than longest dry run, is its current
right run right else current right run zero the next day right so this one block
contains that is [[beat:three_patterns]] three classic paper two patterns right
counter consecutive counter and maximum now let's go like [[beat:output_block]] look
at the other other block output and draw okay so output total rainfall whatever that
is total cm right and then mean daily rainfall and then days with no rainfall right or
largest dry period these are our outputs okay then [[beat:drought]] if longest dry run
is greater than or equal to 15 output there was a drought right else output there was
no drought [[beat:why_ge]] why greater than or equal to 15 rather than 15, right?
Because 15 is self -qualifies, okay? Alright? The source coefficient defines draw at
15 or more consecutive no -ring days. What Cambridge is really rewarding, right? Here
is something important about the 15 marker. Cambridge is not merely checking whether
whether you've reproduced one perfect model solution. The [[beat:bestfit]] published
marker scheme uses a best fit approach, okay? [[beat:marks_split]] It gives us up to
nine marks for applying appropriate programming techniques and data structures, and up
to six more for quality, logic, naming, comments, and completeness of the solution. So
even if your solution is not identical to someone else's, a logical solution that
covers the requirements can earn substantial marks, right? Meaningful identifiers,
comments, and logical ordering matters too, right? So [[beat:syntax]] minor syntax
error do not automatically destroy an otherwise sound solution. So [[beat:close]] let
me close with the six rules, all right? We just completed an entire 75 mark paper too.
But I do not want you leaving this video remembering 75 answers, right?
[[beat:six_habits]] I want you remembering six tables, six habits. Step up. Step
through one instruction at a time, right? Trace tables, read, execute, record, and
move. Here, big problems, it is small requirements, especially the 15 marker, okay? E
is for establish initial values, counters, totals, flags, and maximum need starting
states. P is for preserve value variables, values until an instruction changes them.
No assignments means no change, okay? U is for use intermediate results, especially
Boolean logic. And B is, of course, planned before you go. So if you have an all
-level computer science exam coming up, [[beat:cta]] save this video and work through
the paper yourself without watching me, okay? Every time you get stuck, ask which step
-up rule applies. [[beat:signoff]] I am Ibrahim, the digital tutor. If you want more
Cambridge all -level computer science exam preparation, subscribe, and I'll see you in
the next session.
