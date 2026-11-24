---
scene: cs.algorithms
---

<!-- Cambridge O Level 2210 Chapter 7: Algorithm Design and Problem Solving. Anchors copied from the transcript, mis-hearings and all. -->

[[beat:open]] Welcome to Chapter 7 of Cambridge O -Level Computer Science.
[[beat:turning]] This chapter is about turning a problem into a clear solution that
can be tested. [[beat:cycle_promise]] We'll work through the program development
lifecycle, break large problems into smaller parts, and [[beat:represent]] represent
algorithms using structured diagrams, flowcharts, and pseudocode.
[[beat:also_testing]] We'll also practice standard algorithm methods, testing,
validation, and verification, trace tables, and error correction. [[beat:precision]]
The main habit to develop is precision. An algorithm must be clear enough that
[[beat:without_guessing]] another person or a computer can follow each step without
guessing. [[beat:pdlc_open]] Let's begin with the program development lifecycle.
cycle. [[beat:four_stages]] The four main stages are analysis, design, coding, and
testing. [[beat:analysis]] During analysis, the programmer identifies the problem and
works out what the system needs to do. [[beat:analysis_ipos]] This includes
identifying the inputs, processes, outputs, and any data that must be stored.
[[beat:requirements]] The result of analysis is a clear set of requirements.
[[beat:design]] During design, the programmer plans a solution. [[beat:design_tools]]
They might use a structure diagram, a flow chart, pseudo code, and a test plan.
[[beat:design_detail]] The design should be detailed enough to guide the coding stage.
[[beat:coding]] During coding, the programmer translates the design into a programming
language. [[beat:code_checked]] The code is then developed and checked.
[[beat:testing]] During testing, the program is run using planned test data.
[[beat:compare_results]] The programmer compares the actual results with the expected
results and corrects any errors. [[beat:connected]] These stages are connected.
[[beat:not_wait]] Testing does not have to wait until every line of code is finished.
[[beat:test_parts]] A programmer can test parts of a program while coding then carry
out more complete testing once the solution is ready. [[beat:iterative]] This is
called iterative development. Designing coding and testing can happen repeatedly as
the solution improves. [[beat:break_open]] Before designing a solution it helps to
make a difficult problem more manageable. [[beat:two_techniques]] Two important
techniques are abstraction and decomposition. [[beat:abstraction_is]] Abstraction
means removing details that do not affect the solution. [[beat:library_image]] Imagine
designing a school library system. If you are working on the process for issuing a
book, [[beat:walls]] the color of the library walls is irrelevant. You can leave that
detail out and [[beat:keep_these]] focus on information such as the book, the
borrower, and the issue date. [[beat:decomposition_is]] Decomposition means breaking a
system or problem into smaller parts. [[beat:four_parts]] A library system could be
divided into member management, book management, fine processing, and reporting.
[[beat:divided_again]] Each part can then be divided into smaller tasks. For example,
[[beat:book_tasks]] book management might include adding a book, searching the
catalog, issuing a book, and recording a return. [[beat:easier]] Decomposition makes a
large problem easier to understand, design and test. [[beat:different_people]]
Different people may be able to work on different parts, [[beat:must_fit]] but the
parts must fit together. For example, [[beat:overdue]] the book management module and
the fine processing module must agree on how an overdue return is recorded.
[[beat:ipos_open]] Another useful way to analyze a problem is to identify its inputs,
processes, outputs and storage. [[beat:payroll]] Let's use a payroll system.
[[beat:inputs]] Inputs might include an employee's identification number, hours
worked, and hourly rate. [[beat:processes]] Processes might include calculating gross
pay and working out deductions. [[beat:outputs]] Outputs might include a pay slip and
a payment amount. [[beat:storage]] Storage could include employee details and previous
payment records. [[beat:four_questions]] Ask for questions. What data enters the
system? What [[beat:what_does]] What does the system do with it? [[beat:comes_out]]
What information comes out? [[beat:kept]] What information must be kept for later?
[[beat:define_first]] This method helps you define the problem before writing an
algorithm. [[beat:algo_open]] An algorithm is a finite, precise sequence of steps that
solves a problem. [[beat:finite]] Finite means the algorithm will eventually stop.
[[beat:precise_means]] Precise means each step has one clear meaning.
[[beat:describes_how]] A good algorithm describes how to produce the required result.
[[beat:not_repeat]] It does not simply repeat the question in different words. For
example, [[beat:grade_example]] suppose a program must decide whether a student earns
grade day when a mark is at least 80. [[beat:needs_to]] The algorithm needs to receive
the mark, compare it with 80, assign the correct grade and output the result.
[[beat:specific]] The condition must be specific. [[beat:not_precise]] Writing check
if the mark is high is not precise. [[beat:exact]] Writing if mark is greater than or
equal to 80 gives an exact condition. [[beat:ways_open]] Algorithms can be represented
in different ways. [[beat:structure_is]] A structured diagram shows how a problem is
divided into a hierarchy of smaller tasks. [[beat:structure_use]] It is useful for
showing the main modules of a system and how they are organized.
[[beat:structure_not]] It does not usually show the detailed order of decisions and
loops. [[beat:flow_is]] A flow chart represents the flow of control, visually
[[beat:flow_shows]] it can show sequence decisions, loops, input, output, and
subroutines. A flow chart is useful for seeing how an algorithm moves from one step to
another, [[beat:flow_limit]] although a large flow chart can become difficult to edit.
[[beat:pseudo_is]] PseudoCode describes a logic in precise written steps. It is not
tied to one programming language, but [[beat:pseudo_conventions]] it uses conventions
that must be followed consistently. [[beat:pseudo_useful]] Suda code is useful because
it is more detailed than a structured diagram, while remaining easier to read than
many programming languages. [[beat:symbols_open]] Let's review the main flowchart
symbols. [[beat:terminator]] A terminator represents the start or stop of an
algorithm. [[beat:process]] A process symbol represents an action, calculation or
assignment. [[beat:io]] An input or output symbol represents data entering or leaving
the system. [[beat:decision]] A decision symbol represents a condition with different
possible outcomes such as yes and no. [[beat:subroutine]] A subroutine symbol
represents a call to a separately defined process. [[beat:flowlines]] Flow lines show
the direction in which the algorithm proceeds. [[beat:correct_symbol]] Use the correct
symbol for each action. [[beat:connect]] Connect symbols with directional arrows so
that the route through the algorithm is clear. [[beat:precise_open]] pseudocode must
be written precisely too. [[beat:suppose]] Suppose a program receives a mark and
decides whether it is at least 80. [[beat:read_mark]] The algorithm can read the mark.
[[beat:test_mark]] Then it can test whether the mark is greater than or equal to 80.
[[beat:assign_a]] If the condition is true, it assigns the grade A. [[beat:otherwise]]
Otherwise, it assigns a different result. [[beat:output_grade]] Finally, it outputs
the grade. [[beat:notice]] Notice that the condition uses an exact comparison. A
[[beat:not_enough]] A phrase such as the mark is high is not enough.
[[beat:unambiguous]] A computer needs an unambiguous condition that can be evaluated
as true or false. [[beat:both]] This is true for both selection and repetition.
[[beat:search_open]] Now let's study some standard methods that appear in algorithms.
First, linear search. [[beat:search_is]] Linear search checks items one at a time in
order until it finds the target or reaches the end of the list. For example,
[[beat:names_example]] imagine searching a list of student names for Amina.
[[beat:start_first]] Start with the first name, compare it with the target.
[[beat:if_matches]] If it matches, the search has found the name. [[beat:if_not]] If
it does not match, move to the next name and repeat the comparison. [[beat:stops]] The
search stops when the target is found or when there are no more items to check.
[[beat:unsorted]] Linear search can be used on unsorted data. [[beat:limitation]] Its
limitation is that it may have to check every item. [[beat:found_var]] In pseudocode,
a search often uses a Boolean variable called found. [[beat:found_false]] At the
beginning, found is set to false. [[beat:while_loop]] The algorithm checks each item
while the end of the list has not been reached and found is still false.
[[beat:found_true]] When the target is found, found becomes true. [[beat:not_present]]
If the search finishes with found still false, the algorithm reports that the target
is not present. [[beat:order_matters]] The order of the loop condition matters.
[[beat:beyond_end]] If the algorithm checks an array position that is beyond the end
of the list, it may cause an error. [[beat:sort_open]] Another standard method is
bubble sort means [[beat:sort_is]] bubble sort orders data by repeatedly comparing
adjacent values and swapping them when they are in the wrong order. [[beat:lets_sort]]
Let's sort the values 7, 3, 5, and 2 into ascending order. [[beat:seven_three]] Start
with 7 and 3. [[beat:swap1]] 7 is greater than three. So swap them. [[beat:list_now]]
The list is now three. Seven, five, two. [[beat:seven_five]] Compare seven and five.
[[beat:swap2]] Swap them. The list is now three, five, seven, two. [[beat:seven_two]]
Compare seven and two. [[beat:swap3]] Swap them. After this pass, the largest value
has moved to the end. [[beat:after_pass]] The list is three, five, two, seven.
[[beat:next_pass]] Start the next pass? [[beat:three_five]] Compare 3 and 5. They are
already in the correct order. [[beat:five_two]] Compare 5 and 2. Swap them.
[[beat:becomes]] The list becomes 3, 2, 5, 7. [[beat:next_comparison]] The next
comparison leaves 5 and 7 in the correct order. [[beat:continues]] Bubble sort
continues making passes until the values are ordered. [[beat:exam_passes]] In many
exam questions you'll be asked to describe a specific number of passes.
[[beat:show_each]] Do not jump straight to the final sorted list. Show each comparison
and swap in order. [[beat:count_open]] Algorithms often need to count, total, find a
maximum or minimum, or calculate an average. [[beat:counter]] A counter starts at
zero. [[beat:increase]] When an item meets a condition, increase the counter by one.
For example, [[beat:above_fifty]] to count the number of students who scored above 50,
start count at zero. [[beat:check_each]] Check each mark. If a mark is above 50, add
one to count. [[beat:total_zero]] A total also usually starts at zero.
[[beat:add_value]] For each value, add that value to total. [[beat:max_init]] To find
a maximum or minimum, initialize the variable to the first valid value in the data.
[[beat:compare_rest]] Then compare each remaining value. [[beat:replace_max]] If a
value is greater than the current maximum, replace the maximum. [[beat:replace_min]]
If a value is less than the current minimum, replace the minimum. [[beat:not_zero]] Do
not automatically initialize a maximum to zero. [[beat:negatives]] If all valid values
could be negative, zero would not be a correct starting maximum. [[beat:average]] To
calculate an average, keep both a total and a count. [[beat:divide]] After processing
the values, divide the total by the count. [[beat:check_open]] Now let's distinguish
validation and verification. [[beat:validation_is]] Validation checks whether data is
reasonable and follows specified rules. [[beat:not_true]] It does not prove that the
data is true. [[beat:range_check]] A range check test whether a value falls within a
permitted range. For example, [[beat:range_example]] a mark might have to be between 0
and 100. [[beat:length_check]] A length check tests the number of characters.
[[beat:password]] A password might need to contain at least eight characters.
[[beat:type_check]] A type check makes sure the data is the correct type. For example,
a whole number may be required, [[beat:presence_check]] a presence check makes sure a
required field has not been left blank. [[beat:format_check]] A format check makes
sure data follows a particular pattern. [[beat:check_digit]] A check digit can help
detect errors in an identification number. [[beat:verification_is]] Verification
checks whether data has been copied accurately from its source. For example,
[[beat:visual]] a user might visually compare the entered data with the original
document, [[beat:double_entry]] or data might be entered twice with the two versions
compared. [[beat:key_distinction]] Here is the key distinction.
[[beat:validation_asks]] Validation asks, does this data follow the rules?
[[beat:verification_asks]] Verification asks, was this data copied correctly?
[[beat:dob]] A date of birth may pass a format check but still be wrong. For example,
it may use the corrected date format but not match the person's real date of birth.
[[beat:test_open]] Test data is used to check how a program behaves. [[beat:normal]]
Normal test data is an acceptable typical value. [[beat:ages_example]] If a program
accepts ages from 12 to 18, an age of 15 is normal data. [[beat:abnormal]] Abnormal
test data should be rejected. [[beat:outside]] It could be a value outside the
accepted range such as 11 or 19 or data of the wrong type such as text when a number
is required. [[beat:extreme]] Extreme test data is the smallest or largest acceptable
value. For the accepted age range of 12 to 18, [[beat:extreme_values]] the extreme
values are 12 and 18. [[beat:boundary]] Boundary testing checks the limits and the
values just outside them. For the same range, [[beat:boundary_values]] useful boundary
values are 11, 12, 18 and 19. [[beat:accepted_limits]] 12 and 18 are accepted limits.
[[beat:just_outside]] 11 and 19 are just outside the limits and should be rejected.
[[beat:remember_diff]] Remember the difference. [[beat:extreme_acceptable]] Extreme
values are acceptable values at the edge of the range. [[beat:beyond_edges]] Boundary
testing also checks the values just beyond those edges. [[beat:cover_cases]] Good test
data should cover these different cases. [[beat:only_normal]] Using only normal data
may not reveal mistakes at the limit. [[beat:trace_open]] A trace table helps you
follow an algorithm step by step. [[beat:records]] It records the values of variables,
the results of conditions, and any output produced. [[beat:lets_trace]] Let's trace
this simple process. [[beat:total_starts]] Total starts at 0, the algorithm sets x to
2, then 4, then 6. [[beat:each_time]] Each time it adds x to total and outputs the new
total. [[beat:x_two]] When x is 2, total changes from 0 to 2, so the output is 2.
[[beat:x_four]] When x is 4, total changes from 2 to 6, so the output is 6.
[[beat:x_six]] When x is 6, total changes from 6 to 12 so the output is 12.
[[beat:outputs_are]] The outputs are 2, 6 and 12. [[beat:follow_order]] When
completing a trace table follow the algorithm in order. [[beat:only_when]] Update a
variable only when the algorithm changes it. [[beat:record_output]] Record output only
when an output statement is executed. [[beat:not_every_cell]] Do not fill every cell
on every row if the value has not changed. [[beat:errors_open]] Trace tables can also
help you find errors in an algorithm. A [[beat:syntax]] A syntax error breaks the
grammar or notation of a programming language. [[beat:may_not_run]] The program may
not run because an instruction is written incorrectly. [[beat:logic]] A logic error
occurs when the algorithm runs but produces the wrong result. [[beat:boundary_err]] A
boundary error occurs when a loop starts or stops at the wrong value.
[[beat:init_err]] An initialization error happens when a variable begins with an
unsuitable value. [[beat:update_err]] An update error happens when a counter, total,
or index is not changed correctly. [[beat:condition_err]] A condition error happens
when a selection or loop uses the wrong comparison. For example, [[beat:loop_example]]
a loop that should continue while an index is less than or equal to 10 might stop too
early if the condition uses only less than 10. [[beat:that_is]] That is a boundary
error caused by an incorrect condition. [[beat:debugging]] When debugging, trace the
algorithm with carefully chosen data. [[beat:first_step]] The trace may reveal the
first step where the actual result differs from the expected result.
[[beat:recap_open]] Let's bring the chapter together. [[beat:r_pdlc]] The program
development lifecycle moves through analysis, design, coding, and testing.
[[beat:r_analysis]] Analysis identifies the requirements, inputs, processes, outputs,
and storage. [[beat:r_design]] Design plans the solution, coding implements it,
[[beat:r_testing]] testing checks it using planned data and compares actual results
with expected results. [[beat:r_abstraction]] Abstraction removes irrelevant details.
[[beat:r_decomposition]] Decomposition breaks a large problem into manageable parts.
[[beat:r_represent]] Algorithms can be represented by structure diagrams, flow charts
and pseudocode. [[beat:r_methods]] Standard methods include linear search, bubble
sort, counting, totaling, finding maximum and minimum values and calculating averages,
[[beat:r_validation]] validation checks whether data follows rules,
[[beat:r_verification]] verification checks whether data was copied accurately.
[[beat:r_testdata]] Normal, abnormal, extreme and boundary test data check different
situations. [[beat:r_trace]] Trace tables help you follow an algorithm and locate
errors. [[beat:exam_open]] When you answer exam questions in this chapter, be precise
about the process. [[beat:exam_stage]] For development and stage, explain what happens
and what it produces. [[beat:exam_algo]] For an algorithm, follow every instruction in
order. [[beat:exam_test]] For a test data question, identify the accepted range and
select values that test normal cases, errors, and limits. [[beat:exam_valid]] For
validation and verification, state which question each one answers. and
[[beat:exam_trace]] when you trace or debug an algorithm, update values carefully
rather than guessing the final result. [[beat:pause]] Pause here and try a trace table
or a bubble sort question from chapter 7. [[beat:close]] Work through each step in
order and you'll find that even a long algorithm becomes manageable.
