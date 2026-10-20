---
scene: concept.five_patterns
---

<!-- Body is the transcript verbatim so the aligner matches exactly. Beats placed by anchor phrase, not by hand-counted word index. -->

[[beat:cold_code]] Suppose a variable called count currently contains the value three.
[[beat:cold_if]] Now the program checks and if a statement, if a is equal to b, then
count gets count plus one, okay? But suppose a is not equal to b. [[beat:cold_ask]]
What is count now? Is it zero? is it four or is it still three? [[beat:cold_answer]]
The answer is three. Why? Because the program never instructed us to change the count,
right? [[beat:cold_cost]] This tiny mistake cost students easy marks and trace it. So
remember this rule, okay? [[beat:cold_rule]] If there is no assignment, there is no
change. [[beat:agenda]] In this lesson, I'm going to show you five patterns that can
make Cambridge all -level computer science paper too much easier. [[beat:agenda_list]]
Trace tables, validation, searching and boolean flags, boolean logic, and the 15 mark
programming question. But I do not want you to memorize my answers, okay?
[[beat:agenda_learn]] I want you to learn the pattern underneath the question because
Cambridge can change the scenario, right? [[beat:agenda_similar]] The programming
patterns remain remarkably similar. [[beat:su_intro]] I use a method call the step up.
[[beat:su_s]] S stands for a step through one instruction at a time. [[beat:su_t]] T
means steer big problems into small requirements. [[beat:su_e]] E is for establish
initial values and [[beat:su_p1]] P means preserve variables until an instruction
changes them and [[beat:su_u]] U means use intermediate results. And [[beat:su_p2]]
the final P means plan before you code. [[beat:su_again]] You're going to see these
habits again and again throughout this lesson. [[beat:p1_title]] So let's begin with
trace tables. [[beat:p1_mistake]] The biggest trace table mistake is trying to run the
entire algorithm inside your head. Don't. Instead, [[beat:p1_rule]] remember read,
execute, record, move. [[beat:p1_rule_detail]] Read the instructions, execute exactly
that instruction, record any value that changes, then move to the next instruction.
Alright, [[beat:p1_code]] let's try an example. We begin with Value gets 2. Count gets
0. [[beat:p1_while]] Then, while value is less than 20, do the following. Value gets
multiplied by 2. Count gets count plus 1. End while, okay? [[beat:p1_notjump]] Do not
jump to the answer. We trace at the beginning. [[beat:p1_start]] Value is 2. Count is
0. Now ask yourself, is 2 less than 20? Yes, right? So [[beat:p1_r1]] execute the
first instruction inside the loop. Value gets 2 multiplied by 2. 2 multiplied by 2
equals 4, right? [[beat:p1_r1b]] So value becomes 4. Next, count gets count plus 1. So
count was 0, right? So 0 plus 1 equals what? 1? So count becomes 1. We now have value
equals four, count equals one. [[beat:p1_r2]] Now, test the condition again. Is four
less than 20? Yes, right? So value gets four multiplied by two, right? So four
multiplied by two, what is what? Equals eight, right? So count gets one plus one. So
one plus one equals two. [[beat:p1_r2b]] Now you have value equals eight, count equals
2 and check again [[beat:p1_r3]] is 8 less than 20 yes right it multiplied by 2 equals
16 so the value becomes 16 2 plus 1 equals 3 so the count becomes 3 [[beat:p1_r4]]
check again is 16 less than 20 yes so 16 multiplied by 2 equals 32 so value becomes
32, 3 plus 1 equals 4, the count becomes 4. Now check for the condition again.
[[beat:p1_stop]] Is 32 less than 20? No. The loop stops. [[beat:p1_final]] Our final
values are value equals 32, count equals 4. [[beat:p1_notice]] Notice what we did,
right? One instruction at a time, read, execute, record, and then move. All right. Now
let me show you the mistake that causes many trace table errors, right?
[[beat:p1_persist_code]] Imagine the program says if character one is equal to
character two then count gets count plus one and if right suppose count currently
equals one [[beat:p1_persist_ask]] the characters are not equal what happens to count
nothing count stays one [[beat:p1_persist_ans]] the if a statement is skipped there's
no instruction saying count gets zero so do not change it. This gives us one of the
most important paper two rules. [[beat:p1_persist_rule]] Variable values persist until
an instruction changes them or even shorter. No assignment means no change.
[[beat:p1_chal]] All right, try this one. Number gets three. Total gets zero. For I
gets one to three. right? [[beat:p1_chal_for]] Total gets total plus number. So the
number gets number plus two. Next i, [[beat:p1_chal_q]] what is the final value of
total? Let's trace it, okay? [[beat:p1_chal_start]] Initially, number equals three,
total equals zero. So first iteration, total gets zero plus three. Zero plus three
equals what? Three, right? [[beat:p1_chal_i1]] So total becomes three. Number gets
three plus two. Three plus two equals five. So number becomes five. So now
[[beat:p1_chal_i2]] let's look at the second iteration. Total gets three plus five.
Three plus five equals what? Eight, right? So number gets five plus two. So five plus
two equals what? Seven, right? [[beat:p1_chal_i3]] Now the third iteration. Total gets
8 plus 7. 8 plus 7 equals 15. Alright, so number gets 7 plus 2. 7 plus 2 equals 9. The
loop ends, right? So [[beat:p1_chal_ans]] the final value of total is 15. Notice that
[[beat:p1_chal_sum]] the value is added to the total with 3, 5, and 7, right? 3 plus
5, 3 plus 7 equals what? 3 plus 5 plus 7 equals 15, right? [[beat:p1_close]] That is a
trace table thinking. Don't guess the answer, okay? Follow the instructions. All
right. [[beat:p2_title]] Now, let's move to validation. Okay. [[beat:p2_range]]
Suppose an age is valid only if it is from 10 to 18 Inclusive, okay.
[[beat:p2_options]] What condition is correct? Age is greater than or equal to 10 or
age is less than or equal to 18 or age is greater than or equal to 10 and age is less
than or equal to 18 [[beat:p2_answer]] The correct answer is and right Why? Because
[[beat:p2_both]] a valid age has to satisfy both boundaries, right? It must be at
least 10 and it must not be more than 18. [[beat:p2_rule]] So remember, inside a valid
range equals AND. Okay? Outside a valid range equals OR. Let's say that again.
[[beat:p2_rule_again]] Inside equals AND. Outside equals OR. Alright, let me show you
why OR is dangerous here. okay [[beat:p2_fifty]] suppose somebody enters age 50
consider this in consider this incorrect condition right age is greater than or equal
to or age is less than or equal to 18 50 [[beat:p2_eval1]] is 50 greater than or equal
to 10 yes right that is true [[beat:p2_eval2]] is 50 less than or equal to 18 no that
is false but with or we have the true, false, right? [[beat:p2_or]] True or false
equals true. Remember that true or false equal true. So [[beat:p2_accepts]] the
program incorrectly accepts 50 as a valid age, right? That is why a valid range uses
and age must be, you know, above the lower boundary and below the upper boundary.
Okay. So for an invalid The condition is [[beat:p2_invalid]] age is less than 10 or
age is greater than 18 because an invalid value can be too low or too high. Now let's
look at the validation group. [[beat:p2_loop]] Now suppose the program must keep
asking until the user gives us a valid mark from 0 to 100. [[beat:p2_loop_code]] A
good pattern is repeat input mark until mark is greater than or equal to 0 and mark is
less than or equal to 100. Read that carefully okay repeat input mark until mark is
greater than or equal to 0 and mark is less than or equal to 100. [[beat:p2_loop_why]]
Why is repeat until useful? Because the input statement runs at least once the
condition is checked after the input. [[beat:p2_three]] Remember the three common
loops right for means we normally know how many reputations are required. while checks
the condition before running the loop. Repeat until performs the the first body and
checks the condition afterwards. All right? All right, so [[beat:p2_chal]] here's the
validation challenge, right? Here's your challenge. [[beat:p2_chal_q]] A valid score
is from 0 to 75 inclusive. What should the until condition be? [[beat:p2_chal_ans]]
The answer is until the score is greater than or equal to zero and score is less than
or equal to 75. [[beat:p2_chal_rule]] So again, inside the valid range equals and
right. So here's [[beat:p3_title]] here's the pattern three for searching and Boolean
flag right now [[beat:p3_data]] imagine a school database has 500 student records.
[[beat:p3_cols]] column 1 contains the student ID, column 2 contains the student name.
We need to search for a particular student ID, okay? But there's another problem.
[[beat:p3_problem]] If you search for 500 records and find nothing, how does the
program remember that? [[beat:p3_flag]] We use a Boolean flag here. So it starts with,
you know, [[beat:p3_false]] found gets false, right? Why false? Because there we
search anything we have not found the student. [[beat:p3_loop]] then for row gets 1 to
500. If search ID is equal to students at row column 1, then output students at row
column 2, right, found gets true and then and if. Now next row, [[beat:p3_after]]
after the loop, if found is equal to false, then output student not found and if. Did
you that? If not, then pause it, rewind it and check read again. So flag memory rule,
right? [[beat:p3_rule]] The pattern is false before the search, true when found,
right? So the check after the search, false, true, check, right? [[beat:p3_memory]] A
Boolean flag is simply a memory, right? It remembers whether something happened and
here is a connection to our trace table rule, okay? [[beat:p3_persist]] Suppose found
comes true on how on row 200 okay then row 200 and one does not match right does found
become false no [[beat:p3_persist_ans]] there is no instructions saying found gets
false so found it stays true again remember no assignment means no change alright
[[beat:p3_trap]] so the matching row trap right there is another important search
mistake suppose you search all 500 rows. [[beat:p3_trap_detail]] You find the correct
student under 247. But you wait until after the loop and then write output its
students at row column 2, right? There's a problem. [[beat:p3_trap_problem]] After the
loop finishes, may no longer refer to row 247. You have lost the position where the
match occurred, right? So there are two safe approaches. [[beat:p3_safe1]] Approach 1
would be output the student's name immediately leave when you find the match and
[[beat:p3_safe2]] approach two would be store the matching row. For example, found row
gets row, okay? Then later you can use found row. The memory rule is [[beat:p3_rule2]]
if you need a value later, store it before you lose it, okay? [[beat:p4_title]] So now
let's look at Boolean logic, okay? the [[beat:p4_expr]] suppose the expression is z
equals not open bracket and a and b closed bracket or open bracket be exclusive or or
c closed bracket right that sounds complicated but [[beat:p4_dont]] the worst thing
you can do is try to solve the entire expression in your head right instead
[[beat:p4_one]] one gate one result one one column let's [[beat:p4_break]] Let's break
it apart, okay? X gets... [[beat:p4_x1]] X1 gets A and B. X2 gets not X1. X3 gets B
exclusive or C. [[beat:p4_z]] Z gets X2 or X3. [[beat:p4_easier]] Now the expression
is much easier, right? [[beat:p4_gates]] So here are the gate rules. Remember the
basic rules. [[beat:p4_and_or]] And produces only when both inputs are one or produces
one when at least one input is one okay [[beat:p4_xor_not]] exclusive or produces one
when the inputs are different not reverse the rules okay not zero becomes one not one
becomes zero for exclusive or [[beat:p4_xor_table]] zero exclusive or zero equals zero
zero, okay? Zero exclusive or one equals one. One exclusive or zero equals one. And
one exclusive or one equals two. One equals zero, sorry. The easiest memory rule for
this exercise or is [[beat:p4_xor_rule]] different equals one, same equals zero. All
right? Let that sink in. If you want, you can pause, rewind, go back and listen to
this section, okay? Okay, so I'm gonna tell you this. [[beat:p4_row]] Work one Boolean
row, okay? Let's calculate one row. [[beat:p4_row_vals]] A equals one, okay? B equals
zero, C equals one. So [[beat:p4_row_x1]] first, X1 gets A and B, one and zero equals
zero, so X1 equals zero, okay? [[beat:p4_row_x2]] Next, x2 gets not x1. Not 0 equals
1, so x2 equals 1. [[beat:p4_row_x3]] Next, x3 gets b exclusive or c. 0 exclusive or 1
equals 1 because the inputs are different, right? So x3 equals 1 and [[beat:p4_row_z]]
finally z gets x or 2 or x3 1 or 1 equals 1 right therefore z equals 1
[[beat:p4_mech]] Notice how mechanical that was that is exactly what we want Boolean
logic becomes easier [[beat:p4_clever]] When you stop trying to be clever right one
gate one result one column all right [[beat:p4_circuit]] now let's look at the Boolean
circuit rule right the same idea works when drawing the circuit [[beat:p4_brackets]]
the brackets tell you what happens first right for not not open bracket a and b close
bracket [[beat:p4_and_gate]] a and b first enter an AND gate okay [[beat:p4_not_gate]]
the output of that AND gate enters a NOT gate [[beat:p4_xor_gate]] separately B
exclusive or C right B and C enter an exclusive or get gate right [[beat:p4_or_gate]]
and finally the output of not gate and output of the exclusive or gate enter an or
gate that gives us Z [[beat:p4_inside_out]] so build the circuit from inside outward
alright inside output okay [[beat:p4_chal]] so here's a Boolean challenge A Exclusive
or B. Close bracket and not C. [[beat:p4_chal_q]] What intermediate results should you
create? [[beat:p4_chal_ans]] First, X1 gets Exclusive or B. Second, X2 gets not C. And
finally, [[beat:p4_chal_y]] Y gets x and x2 that is the method all right
[[beat:p5_title]] so the pattern 5 as I said right we'll do the 15 mark question to
now now we read the question that [[beat:p5_scare]] it scares many students before
they even start but don't be scared the 15 mark question a mark programming question
my first is why it's so simple [[beat:p5_dont]] you do not store start coding not in
the exam when you become a programmer not then right [[beat:p5_dont_again]] do not
start coding let me say that again do not start coding [[beat:p5_break]] first break
the scenario into requirements let's let's use a new example right
[[beat:p5_scenario]] a fitness center records the number of visitors each day for 30
days [[beat:p5_reqs]] the program must store the values calculate the total number of
visitors calculate the average visitors per day. [[beat:p5_reqs2]] Count the number of
quiet days where fewer than 20 people visited. [[beat:p5_reqs3]] Find the longest
consecutive run of quiet days and display a warning if that run is four days or more.
[[beat:p5_large]] That sounds like a large program but let's break it apart.
[[beat:p5_map1]] Store 30 values means array. 30 days means for loop. [[beat:p5_map2]]
Total visitors mean accumulator. Average means calculation. [[beat:p5_map3]] Number of
quiet days means counter. And consecutive quiet days means current streak.
[[beat:p5_map4]] Longest run means maximum or record warning means if a statement
[[beat:p5_gone]] now the giant problem has disappeared right we have several small
programming patterns [[beat:p5_init]] so initialize first before processing anything
establish initial values right [[beat:p5_init_code]] total gets zero quite gets quite
count gets zero current quite can come get zero longest quite gets zero. Why?
[[beat:p5_init_why]] Because the counters and totals do not magically begin at zero,
right? We explicitly initialize them. [[beat:p5_init_e]] That is, the E in the step
up, establish initial values. [[beat:p5_loop]] So now let's move to accumulator right
for day [[beat:p5_loop_code]] for day gets 1 to 30 right input visitors at at position
day [[beat:p5_accum]] then total gets total plus visitors at position day this is an
accumulator [[beat:p5_contrast]] notice the difference between two statements right
total gets visitors at position day [[beat:p5_replace]] that replaces the previous
total but total gets total plus visitors at position day [[beat:p5_adds]] That adds
the new value to the existing state total, okay? [[beat:p5_rule]] So remember
assignment replaces accumulation adds [[beat:p5_quiet]] So now let's count the quite
days, okay? Now suppose a quite day means fewer than 20 visitors
[[beat:p5_quiet_code]] So we write if visitors at position day is less than 20 then
quite count gets quite count plus one This counts every point quite there, right? But
[[beat:p5_streak]] we also need the current consecutive quite streak So current coin
gets current quite plus one. [[beat:p5_record]] Then we ask is current quite greater
than the longest quite? If yes, the longest quite gets quite current quite. That
updates our record. [[beat:p5_reset]] If today is not a quite day, current zero gets
zero, right? Why zero? [[beat:p5_why_reset]] Because the consecutive streak has
broken. But do we reset longest quite? Now, longest quite is towards the best record
we have seen. [[beat:p5_survives]] So remember, current resets, longest survives. All
right? [[beat:p5_three]] Now, count versus current versus longest, right? Count versus
current versus longest, right? This extension is extremely important. What does count
mean, right? [[beat:p5_def_count]] Count means how many qualifying items in total.
[[beat:p5_def_current]] Current means how long is the qualifying streak right now?
[[beat:p5_def_longest]] Longest means what is the best streak we have seen?
[[beat:p5_data]] Let's use six days of visitor numbers. 12, 15, 35, 10, 8, 7. A quiet
day is below 20, right? [[beat:p5_d1]] So day one is 12, which is quiet, right? Quiet
day becomes one. Current quiet day becomes one. Longest quiet day becomes one.
[[beat:p5_d2]] Day two is 15, right? So a quiet count now becomes two. current count
quite becomes 2. Longest quite becomes 2. [[beat:p5_d3]] Day 3 is 55, right? That's
not a quite. So, quite count stays 2. Current quite resets it to 0. Longest quite
stays 2, right? [[beat:p5_d4]] Then day 4 is 10, which is quite, right? So, quite
count becomes three. Current quite count becomes one. Longest quite stays two, right?
And [[beat:p5_d5]] then day five is eight. That's a quite, right? So quite count
becomes four. Current quite count becomes two. Longest quite stays two. All right,
remember that. [[beat:p5_d6]] So day six is seven. So that's quite, right? Quite count
becomes five. Current quite becomes three. [[beat:p5_d6_record]] Now three is greater
than two, right? So the longest quite becomes three. [[beat:p5_totals]] At the end,
total quiet days equals five. Longest consecutive quite run equals three.
[[beat:p5_proves]] This proves why one counter cannot do both jobs. All right.
[[beat:p5_avg]] So average and final decision work after all 30 days have been have
been present process, right? Calculate the average. [[beat:p5_avg_code]] Average gets
total total divided by 30 rounded to 2 decimal points. Say that again average gets
total divided by 30 rounded to 2 decimal places [[beat:p5_output]] then output right
total average quite count longest quite [[beat:p5_warn]] finally check the warning
right if the longest quite is greater than or equal to 4 then Then output low activity
warding. [[beat:p5_warn_else]] Else output activity normal. And if [[beat:p5_why4]]
why greater than or equal to 4? Because the requirement says 4 days or more, right? 4
itself qualifies. [[beat:p5_gt4]] So if we wrote greater than 4, then 4 would
incorrectly fail. [[beat:p5_boundary]] Pay very close attention to boundary words such
as at least more than, less than, no more than and inclusive. They change the
condition. All right. [[beat:p5_lesson]] So the 15 mark lesson, right? The 15 mark
question is usually not 15 marks of completely not new knowledge. Okay.
[[beat:p5_familiar]] It is familiar programming patterns connected together.
[[beat:p5_list]] Accumulator, counter, array, loop, validation, maximum, consecutive
streak, selection, output. [[beat:p5_code_reqs]] So do not code the paragraph. Code
the requirements. Okay. Okay, [[beat:recap_intro]] and let's do a recap of this step
up, right? Let's, [[beat:recap_s]] S is stepped through one instruction at a time.
That is how we handle trade staples, right? [[beat:recap_t]] Then T is to your big
problems into small requirements, and that is how we attack the 15 more quiescent.
[[beat:recap_e]] E establish initial values, encounters, totals, flags, maximums,
right? And then [[beat:recap_p]] P preserves values until an instruction changes them.
No assignments means no change, and [[beat:recap_u]] you use intermediate results,
especially in Boolean logic. [[beat:recap_p2]] And the final P, plan before you code.
[[beat:recap_easier]] Paper 2 becomes much easier when you stop seeing dozens of
unrelated questions and start recognizing recurring patterns. [[beat:check_intro]] So
let's recap it. Before we finish let's do this quickly. [[beat:check_trace]] Trade
stable read execute record move. [[beat:check_persist]] Variable not change keep its
previous value right. [[beat:check_range]] Valid range and outside the range or
[[beat:check_flag]] bullion flag falls before true when found. Check after right.
[[beat:check_bool]] Bullion logic one gate one result one column [[beat:check_total]]
And the running total, total gets value, total plus value, [[beat:check_streak]]
consecutive sequence, current resets, longest survives, right? [[beat:check_15]] 15
marker, plan before you code, alright? [[beat:cta]] Now I want you to know which paper
2 skill costs you the most marks, right? [[beat:cta_words]] In the comments, just
write one word, trace, pseudocode Boolean or 15 mark. [[beat:cta_decide]] I'll use
your comments to decide what I solve next. If you're preparing for Cambridge O level
computer science, [[beat:cta_sub]] subscribe to the digital tutor. My goal is to make
you, not to make you memorize answers, right? My goal is to teach you how to think
through the question, [[beat:outro]] learn the pattern, apply the pattern, and collect
the marks. See you in the next video.
