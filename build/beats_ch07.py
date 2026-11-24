"""Beat placement for Chapter 7, Algorithm Design and Problem Solving.

Run from the repo root:

    python build/beats_ch07.py

No edit to the recording at all this time. It is a synthetic reading and
it starts on its first word and stops on its last: the file is 1071.49
seconds, the first word begins at 0.00 and the last ends at 1070.84, so
audio/CH07-algorithms.mp3 is the upload copied, not trimmed.

    python build/transcribe.py audio/CH07-algorithms-raw.mp3 \\
        --model small --language en

``build/repair_loops.find_loops`` reports no loops.

Anchors are copied from the transcript as it came out, mis-hearings and
all, never from the written script. The reading is correct throughout;
the transcriber is what these are matched against, and it heard:
"structured diagram" for structure diagram, "grade day" for grade A,
"Suda code" for pseudocode, "Ask for questions" for ask four questions,
"the corrected date format" for the correct date format, "For
development and stage" for for a development stage, and it doubled a
word in three places ("lifecycle. cycle.", "What What does", "A A
phrase"). A phrase corrected to the script would not be in the audio,
and would either fail to match or -- far worse -- match somewhere else.

Several anchors repeat earlier wording: the grade-A condition is given
twice, once as an example of precision and once as the flowchart, and
the development stages are named in the opening, in section 1 and again
in the recap. Matching runs forward from the previous beat, so each pass
finds its own occurrence, and an anchor that resolved out of order would
fail loudly rather than quietly marking the wrong sentence.
"""

from mkbeats import build

BEATS = [
    # ------------------------------------------------------- 0. opening
    ("open", "Welcome to Chapter 7 of Cambridge"),
    ("turning", "This chapter is about turning a problem into a clear "
                "solution that can be tested"),
    ("cycle_promise", "We'll work through the program development "
                      "lifecycle"),
    ("represent", "represent algorithms using structured diagrams, "
                  "flowcharts, and pseudocode"),
    ("also_testing", "We'll also practice standard algorithm methods, "
                     "testing"),
    ("precision", "The main habit to develop is precision"),
    ("without_guessing", "another person or a computer can follow each "
                         "step without guessing"),

    # --------------------------------------------- 1. the life cycle
    ("pdlc_open", "Let's begin with the program development lifecycle"),
    ("four_stages", "The four main stages are analysis, design, coding, "
                    "and testing"),
    ("analysis", "During analysis, the programmer identifies the problem"),
    ("analysis_ipos", "This includes identifying the inputs, processes, "
                      "outputs, and any data that must be stored"),
    ("requirements", "The result of analysis is a clear set of "
                     "requirements"),
    ("design", "During design, the programmer plans a solution"),
    ("design_tools", "They might use a structure diagram, a flow chart, "
                     "pseudo code, and a test plan"),
    ("design_detail", "The design should be detailed enough to guide the "
                      "coding stage"),
    ("coding", "During coding, the programmer translates the design into "
               "a programming language"),
    ("code_checked", "The code is then developed and checked"),
    ("testing", "During testing, the program is run using planned test "
                "data"),
    ("compare_results", "The programmer compares the actual results with "
                        "the expected results"),
    ("connected", "These stages are connected"),
    ("not_wait", "Testing does not have to wait until every line of code "
                 "is finished"),
    ("test_parts", "A programmer can test parts of a program while coding"),
    ("iterative", "This is called iterative development"),

    # ------------------------------- 2. abstraction and decomposition
    ("break_open", "Before designing a solution it helps to make a "
                   "difficult problem more manageable"),
    ("two_techniques", "Two important techniques are abstraction and "
                       "decomposition"),
    ("abstraction_is", "Abstraction means removing details that do not "
                       "affect the solution"),
    ("library_image", "Imagine designing a school library system"),
    ("walls", "the color of the library walls is irrelevant"),
    ("keep_these", "focus on information such as the book, the borrower, "
                   "and the issue date"),
    ("decomposition_is", "Decomposition means breaking a system or problem "
                         "into smaller parts"),
    ("four_parts", "A library system could be divided into member "
                   "management, book management"),
    ("divided_again", "Each part can then be divided into smaller tasks"),
    ("book_tasks", "book management might include adding a book, searching "
                   "the catalog"),
    ("easier", "Decomposition makes a large problem easier to understand, "
               "design and test"),
    ("different_people", "Different people may be able to work on "
                         "different parts"),
    ("must_fit", "but the parts must fit together"),
    ("overdue", "the book management module and the fine processing module "
                "must agree"),

    # ----------------------------- 3. inputs, processes, outputs, storage
    ("ipos_open", "Another useful way to analyze a problem is to identify "
                  "its inputs, processes, outputs and storage"),
    ("payroll", "Let's use a payroll system"),
    ("inputs", "Inputs might include an employee's identification number, "
               "hours worked"),
    ("processes", "Processes might include calculating gross pay"),
    ("outputs", "Outputs might include a pay slip and a payment amount"),
    ("storage", "Storage could include employee details and previous "
                "payment records"),
    ("four_questions", "Ask for questions. What data enters the system?"),
    ("what_does", "What does the system do with it?"),
    ("comes_out", "What information comes out?"),
    ("kept", "What information must be kept for later?"),
    ("define_first", "This method helps you define the problem before "
                     "writing an algorithm"),

    # ------------------------------------------ 4. what an algorithm is
    ("algo_open", "An algorithm is a finite, precise sequence of steps "
                  "that solves a problem"),
    ("finite", "Finite means the algorithm will eventually stop"),
    ("precise_means", "Precise means each step has one clear meaning"),
    ("describes_how", "A good algorithm describes how to produce the "
                      "required result"),
    ("not_repeat", "It does not simply repeat the question in different "
                   "words"),
    ("grade_example", "suppose a program must decide whether a student "
                      "earns grade day"),
    ("needs_to", "The algorithm needs to receive the mark, compare it "
                 "with 80"),
    ("specific", "The condition must be specific"),
    ("not_precise", "Writing check if the mark is high is not precise"),
    ("exact", "Writing if mark is greater than or equal to 80 gives an "
              "exact condition"),

    # --------------------------------------------- 5. three ways to write
    ("ways_open", "Algorithms can be represented in different ways"),
    ("structure_is", "A structured diagram shows how a problem is divided "
                     "into a hierarchy"),
    ("structure_use", "It is useful for showing the main modules of a "
                      "system"),
    ("structure_not", "It does not usually show the detailed order of "
                      "decisions and loops"),
    ("flow_is", "A flow chart represents the flow of control"),
    ("flow_shows", "it can show sequence decisions, loops, input, output, "
                   "and subroutines"),
    ("flow_limit", "although a large flow chart can become difficult to "
                   "edit"),
    ("pseudo_is", "PseudoCode describes a logic in precise written steps"),
    ("pseudo_conventions", "it uses conventions that must be followed "
                           "consistently"),
    ("pseudo_useful", "Suda code is useful because it is more detailed "
                      "than a structured diagram"),

    # ------------------------------------------- 6. the flowchart symbols
    ("symbols_open", "Let's review the main flowchart symbols"),
    ("terminator", "A terminator represents the start or stop of an "
                   "algorithm"),
    ("process", "A process symbol represents an action, calculation or "
                "assignment"),
    ("io", "An input or output symbol represents data entering or leaving "
           "the system"),
    ("decision", "A decision symbol represents a condition with different "
                 "possible outcomes"),
    ("subroutine", "A subroutine symbol represents a call to a separately "
                   "defined process"),
    ("flowlines", "Flow lines show the direction in which the algorithm "
                  "proceeds"),
    ("correct_symbol", "Use the correct symbol for each action"),
    ("connect", "Connect symbols with directional arrows"),

    # ------------------------------------------ 7. one algorithm, precisely
    ("precise_open", "pseudocode must be written precisely too"),
    ("suppose", "Suppose a program receives a mark and decides whether it "
                "is at least 80"),
    ("read_mark", "The algorithm can read the mark"),
    ("test_mark", "Then it can test whether the mark is greater than or "
                  "equal to 80"),
    ("assign_a", "If the condition is true, it assigns the grade A"),
    ("otherwise", "Otherwise, it assigns a different result"),
    ("output_grade", "Finally, it outputs the grade"),
    ("notice", "Notice that the condition uses an exact comparison"),
    ("not_enough", "A phrase such as the mark is high is not enough"),
    ("unambiguous", "A computer needs an unambiguous condition that can be "
                    "evaluated as true or false"),
    ("both", "This is true for both selection and repetition"),

    # -------------------------------------------------- 8. linear search
    ("search_open", "Now let's study some standard methods that appear in "
                    "algorithms"),
    ("search_is", "Linear search checks items one at a time in order"),
    ("names_example", "imagine searching a list of student names for Amina"),
    ("start_first", "Start with the first name, compare it with the "
                    "target"),
    ("if_matches", "If it matches, the search has found the name"),
    ("if_not", "If it does not match, move to the next name"),
    ("stops", "The search stops when the target is found or when there are "
              "no more items"),
    ("unsorted", "Linear search can be used on unsorted data"),
    ("limitation", "Its limitation is that it may have to check every "
                   "item"),
    ("found_var", "In pseudocode, a search often uses a Boolean variable "
                  "called found"),
    ("found_false", "At the beginning, found is set to false"),
    ("while_loop", "The algorithm checks each item while the end of the "
                   "list has not been reached"),
    ("found_true", "When the target is found, found becomes true"),
    ("not_present", "If the search finishes with found still false"),
    ("order_matters", "The order of the loop condition matters"),
    ("beyond_end", "If the algorithm checks an array position that is "
                   "beyond the end of the list"),

    # ---------------------------------------------------- 9. bubble sort
    ("sort_open", "Another standard method is bubble sort"),
    ("sort_is", "bubble sort orders data by repeatedly comparing adjacent "
                "values"),
    ("lets_sort", "Let's sort the values 7, 3, 5, and 2 into ascending "
                  "order"),
    ("seven_three", "Start with 7 and 3"),
    ("swap1", "7 is greater than three. So swap them"),
    ("list_now", "The list is now three. Seven, five, two"),
    ("seven_five", "Compare seven and five"),
    ("swap2", "Swap them. The list is now three, five, seven, two"),
    ("seven_two", "Compare seven and two"),
    ("swap3", "Swap them. After this pass, the largest value has moved to "
              "the end"),
    ("after_pass", "The list is three, five, two, seven"),
    ("next_pass", "Start the next pass"),
    ("three_five", "Compare 3 and 5. They are already in the correct "
                   "order"),
    ("five_two", "Compare 5 and 2. Swap them"),
    ("becomes", "The list becomes 3, 2, 5, 7"),
    ("next_comparison", "The next comparison leaves 5 and 7 in the correct "
                        "order"),
    ("continues", "Bubble sort continues making passes until the values "
                  "are ordered"),
    ("exam_passes", "In many exam questions you'll be asked to describe a "
                    "specific number of passes"),
    ("show_each", "Do not jump straight to the final sorted list"),

    # ------------------------------ 10. counting, totalling, max, average
    ("count_open", "Algorithms often need to count, total, find a maximum "
                   "or minimum"),
    ("counter", "A counter starts at zero"),
    ("increase", "When an item meets a condition, increase the counter by "
                 "one"),
    ("above_fifty", "to count the number of students who scored above 50"),
    ("check_each", "Check each mark. If a mark is above 50, add one to "
                   "count"),
    ("total_zero", "A total also usually starts at zero"),
    ("add_value", "For each value, add that value to total"),
    ("max_init", "To find a maximum or minimum, initialize the variable to "
                 "the first valid value"),
    ("compare_rest", "Then compare each remaining value"),
    ("replace_max", "If a value is greater than the current maximum, "
                    "replace the maximum"),
    ("replace_min", "If a value is less than the current minimum, replace "
                    "the minimum"),
    ("not_zero", "Do not automatically initialize a maximum to zero"),
    ("negatives", "If all valid values could be negative, zero would not "
                  "be a correct starting maximum"),
    ("average", "To calculate an average, keep both a total and a count"),
    ("divide", "After processing the values, divide the total by the "
               "count"),

    # ------------------------------------- 11. validation and verification
    ("check_open", "Now let's distinguish validation and verification"),
    ("validation_is", "Validation checks whether data is reasonable and "
                      "follows specified rules"),
    ("not_true", "It does not prove that the data is true"),
    ("range_check", "A range check test whether a value falls within a "
                    "permitted range"),
    ("range_example", "a mark might have to be between 0 and 100"),
    ("length_check", "A length check tests the number of characters"),
    ("password", "A password might need to contain at least eight "
                 "characters"),
    ("type_check", "A type check makes sure the data is the correct type"),
    ("presence_check", "a presence check makes sure a required field has "
                       "not been left blank"),
    ("format_check", "A format check makes sure data follows a particular "
                     "pattern"),
    ("check_digit", "A check digit can help detect errors in an "
                    "identification number"),
    ("verification_is", "Verification checks whether data has been copied "
                        "accurately from its source"),
    ("visual", "a user might visually compare the entered data with the "
               "original document"),
    ("double_entry", "or data might be entered twice with the two versions "
                     "compared"),
    ("key_distinction", "Here is the key distinction"),
    ("validation_asks", "Validation asks, does this data follow the "
                        "rules?"),
    ("verification_asks", "Verification asks, was this data copied "
                          "correctly?"),
    ("dob", "A date of birth may pass a format check but still be wrong"),

    # ------------------------------------------------------ 12. test data
    ("test_open", "Test data is used to check how a program behaves"),
    ("normal", "Normal test data is an acceptable typical value"),
    ("ages_example", "If a program accepts ages from 12 to 18, an age of "
                     "15 is normal data"),
    ("abnormal", "Abnormal test data should be rejected"),
    ("outside", "It could be a value outside the accepted range such as 11 "
                "or 19"),
    ("extreme", "Extreme test data is the smallest or largest acceptable "
                "value"),
    ("extreme_values", "the extreme values are 12 and 18"),
    ("boundary", "Boundary testing checks the limits and the values just "
                 "outside them"),
    ("boundary_values", "useful boundary values are 11, 12, 18 and 19"),
    ("accepted_limits", "12 and 18 are accepted limits"),
    ("just_outside", "11 and 19 are just outside the limits and should be "
                     "rejected"),
    ("remember_diff", "Remember the difference"),
    ("extreme_acceptable", "Extreme values are acceptable values at the "
                           "edge of the range"),
    ("beyond_edges", "Boundary testing also checks the values just beyond "
                     "those edges"),
    ("cover_cases", "Good test data should cover these different cases"),
    ("only_normal", "Using only normal data may not reveal mistakes at the "
                    "limit"),

    # ---------------------------------------------------- 13. trace tables
    ("trace_open", "A trace table helps you follow an algorithm step by "
                   "step"),
    ("records", "It records the values of variables, the results of "
                "conditions"),
    ("lets_trace", "Let's trace this simple process"),
    ("total_starts", "Total starts at 0, the algorithm sets x to 2"),
    ("each_time", "Each time it adds x to total and outputs the new total"),
    ("x_two", "When x is 2, total changes from 0 to 2"),
    ("x_four", "When x is 4, total changes from 2 to 6"),
    ("x_six", "When x is 6, total changes from 6 to 12"),
    ("outputs_are", "The outputs are 2, 6 and 12"),
    ("follow_order", "When completing a trace table follow the algorithm "
                     "in order"),
    ("only_when", "Update a variable only when the algorithm changes it"),
    ("record_output", "Record output only when an output statement is "
                      "executed"),
    ("not_every_cell", "Do not fill every cell on every row"),

    # ----------------------------------------- 14. errors, and debugging
    ("errors_open", "Trace tables can also help you find errors in an "
                    "algorithm"),
    ("syntax", "A syntax error breaks the grammar or notation of a "
               "programming language"),
    ("may_not_run", "The program may not run because an instruction is "
                    "written incorrectly"),
    ("logic", "A logic error occurs when the algorithm runs but produces "
              "the wrong result"),
    ("boundary_err", "A boundary error occurs when a loop starts or stops "
                     "at the wrong value"),
    ("init_err", "An initialization error happens when a variable begins "
                 "with an unsuitable value"),
    ("update_err", "An update error happens when a counter, total, or "
                   "index is not changed correctly"),
    ("condition_err", "A condition error happens when a selection or loop "
                      "uses the wrong comparison"),
    ("loop_example", "a loop that should continue while an index is less "
                     "than or equal to 10"),
    ("that_is", "That is a boundary error caused by an incorrect "
                "condition"),
    ("debugging", "When debugging, trace the algorithm with carefully "
                  "chosen data"),
    ("first_step", "The trace may reveal the first step where the actual "
                   "result differs"),

    # ---------------------------------------------------------- 15. recap
    ("recap_open", "Let's bring the chapter together"),
    ("r_pdlc", "The program development lifecycle moves through analysis, "
               "design, coding, and testing"),
    ("r_analysis", "Analysis identifies the requirements, inputs, "
                   "processes, outputs, and storage"),
    ("r_design", "Design plans the solution, coding implements it"),
    ("r_testing", "testing checks it using planned data and compares "
                  "actual results"),
    ("r_abstraction", "Abstraction removes irrelevant details"),
    ("r_decomposition", "Decomposition breaks a large problem into "
                        "manageable parts"),
    ("r_represent", "Algorithms can be represented by structure diagrams, "
                    "flow charts and pseudocode"),
    ("r_methods", "Standard methods include linear search, bubble sort, "
                  "counting"),
    ("r_validation", "validation checks whether data follows rules"),
    ("r_verification", "verification checks whether data was copied "
                       "accurately"),
    ("r_testdata", "Normal, abnormal, extreme and boundary test data check "
                   "different situations"),
    ("r_trace", "Trace tables help you follow an algorithm and locate "
                "errors"),
    ("exam_open", "When you answer exam questions in this chapter, be "
                  "precise about the process"),
    ("exam_stage", "For development and stage, explain what happens and "
                   "what it produces"),
    ("exam_algo", "For an algorithm, follow every instruction in order"),
    ("exam_test", "For a test data question, identify the accepted range"),
    ("exam_valid", "For validation and verification, state which question "
                   "each one answers"),
    ("exam_trace", "when you trace or debug an algorithm, update values "
                   "carefully"),
    ("pause", "Pause here and try a trace table or a bubble sort "
              "question"),
    ("close", "Work through each step in order"),
]

if __name__ == "__main__":
    build("CH07-algorithms", "cs.algorithms", BEATS, "CH07-algorithms",
          "Cambridge O Level 2210 Chapter 7: Algorithm Design and Problem "
          "Solving. Anchors copied from the transcript, mis-hearings and "
          "all.")
