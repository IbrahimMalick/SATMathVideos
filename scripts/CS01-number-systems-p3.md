---
scene: cs.number_systems_p3
---

[[beat:add_rules]] Part seventeen. Binary addition. Now we're going to add
binary numbers. Don't worry. There are fewer basic combinations to learn than
in denary arithmetic. Start with zero plus zero. Obviously zero. Next, zero
plus one. That's one. And one plus zero, also one. Now one plus one. We have
a problem. Binary doesn't have a digit two. So the result is one zero.
[[beat:carry_analogy]] Think of this like denary arithmetic. In denary, nine
plus one is ten. We write zero and carry one. In binary, one plus one is one
zero. We write zero and carry one. So memorize: zero plus zero is zero. Zero
plus one is one. One plus zero is one. One plus one is one zero.
[[beat:triple]] And if we already have a carry: one plus one plus one is one
one, because that's three in denary, and three is one one in binary. So the
result bit is one and the carry is one.

[[beat:add_setup]] Part eighteen. A complete binary addition. Let's add zero
zero one one zero one zero one and zero zero one zero one one one zero.
Before we calculate, let's convert them mentally. The first is thirty two
plus sixteen plus four plus one, which is fifty three. The second is thirty
two plus eight plus four plus two, which is forty six. So we already know
our answer should represent fifty three plus forty six, which is ninety
nine. [[beat:add_columns]] Now perform the binary addition. Work from the
right. One plus zero is one. Zero plus one is one. One plus one is zero
carry one. Zero plus one plus the carry is zero carry one. One plus zero
plus the carry is zero carry one. One plus one plus the carry is one carry
one. Zero plus zero plus the carry is one. And zero plus zero is zero.
[[beat:add_verify]] Let's verify the answer. Zero one one zero zero zero one
one is sixty four plus thirty two plus two plus one, which is ninety nine.
Excellent. [[beat:why_verify]] Why should you verify? Because conversion
gives you a quick way to catch an arithmetic mistake. If your binary result
represents one hundred and three but you know the denary values should total
ninety nine, something went wrong.

[[beat:overflow_intro]] Part nineteen. Overflow. Now let's imagine our
computer has space for exactly eight bits. For an unsigned number, the
largest value we can store is one one one one one one one one, which is two
hundred and fifty five. [[beat:overflow_def]] Now imagine we add two numbers
and mathematically the result is three hundred. Can three hundred be
represented in eight unsigned bits? No. Why? Because the maximum is two
hundred and fifty five. We would need an additional bit. This situation is
called overflow. [[beat:overflow_wording]] Overflow occurs when the result
of an operation cannot be represented using the available number of bits.
That's the definition I want you to understand. Not: overflow is when the
number gets really big. That's too vague. Say: the result is outside the
range representable by the available number of bits.
[[beat:overflow_carry]] For unsigned eight-bit addition, a carry beyond the
eighth bit is a clear sign that the complete result cannot be held in the
eight-bit register.

[[beat:shift_left]] Part twenty. Logical binary shifts. Now we're going to
make binary do something surprisingly useful. Take zero zero zero zero one
one zero one. Let's convert it. Eight plus four plus one is thirteen. Now
move every bit one position to the left. Empty space on the right is filled
with zero. Now calculate the new value. Sixteen plus eight plus two is
twenty six. [[beat:shift_left2]] We started with thirteen. We now have
twenty six. What happened? We multiplied by two. Shift left again. That's
thirty two plus sixteen plus four, which is fifty two. So thirteen becomes
twenty six becomes fifty two. Every valid left shift multiplies the unsigned
value by two.

[[beat:shift_n]] Part twenty one. Shifting more than one place. Suppose we
shift left by two positions. That's equivalent to multiplying by two times
two, which is four, or two squared. Shift left three positions? Multiply by
two cubed, which is eight. Four positions? Two to the four, which is
sixteen. So in general, a logical left shift by n positions corresponds to
multiplication by two to the n. [[beat:shift_caveat]] Provided significant
bits are not lost. That last part matters. We'll come back to it.

[[beat:shift_right]] Part twenty two. Logical right shifts. Now take zero
one one zero zero zero zero zero. Convert it: sixty four plus thirty two is
ninety six. Shift everything one position to the right. That's thirty two
plus sixteen, which is forty eight. Ninety six became forty eight. We
divided by two. [[beat:shift_right2]] Shift right again. That's sixteen plus
eight, which is twenty four. So ninety six becomes forty eight becomes
twenty four. [[beat:shift_right_n]] Therefore a logical right shift by one
position divides an unsigned value by two. Two positions: divide by two
squared, which is four. Three: divide by two cubed, which is eight.

[[beat:bits_lost]] Part twenty three. Bits can fall off. Here's the catch.
Take an eight-bit register. If we shift left and a one moves beyond the
left-hand boundary, that bit is lost. Similarly, during a logical right
shift, a bit moving beyond the right-hand boundary is lost. Once bits are
discarded, the simple multiplication or division interpretation may no
longer give the full mathematical result. [[beat:precise_statement]] So the
precise statement is: a logical left shift by n places corresponds to
multiplication by two to the n, provided no significant bits are lost from
the available representation. And logical right shifts can discard low-order
bits, which means integer information can be lost.

[[beat:msb_lsb]] Part twenty four. MSB and LSB. Two terms you should know.
Look at one zero one one zero one one zero. The bit furthest to the left is
called the most significant bit, or MSB. The bit furthest to the right is
called the least significant bit, or LSB. [[beat:msb_why]] Why most
significant? Because in a positional representation it occupies the
highest-value position. And the least significant bit occupies the
lowest-value position. So: left is MSB, right is LSB.
