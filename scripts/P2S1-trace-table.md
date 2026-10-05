---
scene: shorts.trace_table
---

<!-- Body is the segment transcript verbatim so the aligner matches exactly. Screen renders correct pseudocode: the delivery says 'count one' where the instruction is Count <- Count + 1. -->

[[beat:hook]] Here is one trace table mistake that can cost you easy Cambridge marks.
[[beat:reset]] Resetting a variable when the algorithm never told you to.
[[beat:count0]] Suppose count starts at zero. [[beat:match]] We compare two
neighboring letters. They match. [[beat:increment]] So the instruction says count one.
Count is now one, right? [[beat:next_pair]] The next pair does not match. what happens
to count [[beat:rule]] stays one no assignment equals no change [[beat:example]] all
right now let's take a look at balloon okay [[beat:trace_ba]] ba no match so count
zero [[beat:trace_al]] al is still zero [[beat:trace_ll]] l l match the count becomes
one [[beat:trace_lo]] LO, no match, and counter stays one. And [[beat:trace_oo]] then
OO, match, so count becomes two, right? Do not trace in your head. [[beat:steps]]
Follow four steps. Read, execute, record, move. [[beat:close]] If the program does not
change the variable, neither do you. That is step up rule number one. Step through one
instruction at a time.
