---
scene: cs.number_systems_p4
---

[[beat:where_negatives]] Part twenty five. So far, where are the negative
numbers? We've been treating our eight-bit patterns as unsigned numbers.
That gives zero through two hundred and fifty five. But computers obviously
need to represent minus one, minus twenty five, minus one hundred, and so
on. How do we represent a minus sign using bits? [[beat:name]] One widely
used solution is two's complement. This is where students sometimes get
nervous. Don't. There's one major change to understand.
[[beat:negative_column]] For an eight-bit two's-complement number, our
columns are minus one hundred and twenty eight, sixty four, thirty two,
sixteen, eight, four, two, one. Look carefully. In ordinary unsigned
eight-bit binary, the leftmost column was plus one hundred and twenty eight.
In eight-bit two's complement, the leftmost column has weight minus one
hundred and twenty eight. Everything else remains the same: sixty four,
thirty two, sixteen, eight, four, two, one.

[[beat:sign_clue]] Part twenty six. The sign clue. This gives us a very
useful clue. In an eight-bit two's-complement number, if the MSB is zero,
the number is non-negative. If the MSB is one, the number is negative.
[[beat:sign_examples]] For example, zero zero one one zero one one zero
starts with zero. Non-negative. But one zero one one zero one one zero
starts with one. Negative. [[beat:sign_warning]] But be careful. The first
bit isn't a separate minus-sign character. It has positional weight minus
one hundred and twenty eight in the eight-bit interpretation.

[[beat:largest]] Part twenty seven. The two's-complement range. What is the
largest positive eight-bit two's-complement number? We must keep the MSB at
zero. So zero one one one one one one one. That's sixty four plus thirty two
plus sixteen plus eight plus four plus two plus one, which is plus one
hundred and twenty seven. [[beat:most_negative]] What's the most negative
value? One zero zero zero zero zero zero zero. That's simply minus one
hundred and twenty eight. [[beat:range]] Therefore the range is minus one
hundred and twenty eight to plus one hundred and twenty seven. Notice that
this is different from unsigned eight-bit binary. Unsigned is zero to two
hundred and fifty five. Two's complement is minus one hundred and twenty
eight to plus one hundred and twenty seven. [[beat:same_bits]] Same eight
bits. Different interpretation.
