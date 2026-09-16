---
scene: cs.number_systems_p1
---

[[beat:open]] Assalam-o-Alaikum everyone, and welcome to The Digital Tutor.
Let me start with a question. [[beat:common]] What does a photograph have in
common with a song? What does a YouTube video have in common with a Word
document? And what does your name have in common with a video game? They
look completely different to us. But inside a computer, all of them
eventually have something very important in common: they have to be
represented as data using binary. Zeros and ones. That's it.
[[beat:not_human]] Your computer doesn't look at a photograph and say: what
a beautiful sunset. It doesn't listen to a song and say: I like that guitar.
At the lowest level, the computer is dealing with patterns of binary digits.
And that's what we're going to understand today. [[beat:objectives]] By the
end of this lesson, you should be able to explain and work with: binary,
denary, hexadecimal, number conversion, binary addition, overflow, logical
shifts, and two's complement. Some of those terms may sound intimidating
right now. That's okay. We're going to build them one at a time. And
throughout the lesson I'm going to give you challenges. When I do, pause the
video and actually solve them. Don't turn mathematics into a spectator
sport. [[beat:workbook]] I've also prepared a workbook containing practice
questions for this lesson. You can download it from The Digital Tutor
website. Keep it beside you while we work. Let's begin with the most
important question.

[[beat:switch]] Part one. Why do computers use binary? Imagine an ordinary
light switch. How many basic states does it have? Two. ON and OFF. We could
decide to represent those two states like this: ON equals one. OFF equals
zero. And now we have a very simple system for recording two possible
states. [[beat:hardware]] Computer hardware is built from enormous numbers
of electronic components that can operate using distinguishable states. So
rather than trying to represent ten different states reliably at the
fundamental level, digital computers work naturally with two states. We
represent those states using zero and one. This is the binary number system.
[[beat:bit]] And each individual zero or one is called a bit. That's short
for binary digit. So if I write one, that's one bit. If I write one zero one
one, that's four bits. If I write one one zero zero one zero one zero,
that's eight bits. [[beat:byte]] Eight bits together are commonly called a
byte. [[beat:base2]] Here is an important distinction. Binary isn't simply a
bunch of zeros and ones. It is a base-two positional number system. That's
important, because once you understand what base two means, binary becomes
much easier.

[[beat:denary]] Part two. Let's start with the number system you already
know. Before learning binary, let's examine something you already
understand. Suppose I write five thousand two hundred and seventy four. You
immediately recognize that as five thousand, two hundred and seventy-four.
But why? Because the position of each digit gives it a value. Let's break it
apart. [[beat:place_value]] Thousands, hundreds, tens and units. One
thousand, one hundred, ten, one. Five, two, seven, four. [[beat:expand]] So
five thousand two hundred and seventy four actually means: five times one
thousand, two times one hundred, seven times ten, and four times one. Which
gives five thousand plus two hundred plus seventy plus four, equals five
thousand two hundred and seventy four. [[beat:powers10]] Those column values
are powers of ten. Ten cubed is one thousand. Ten squared is one hundred.
Ten to the one is ten. Ten to the zero is one. That's why our everyday
number system is called base ten, or denary. You may also hear the term
decimal. We have ten available digits: zero through nine.

[[beat:powers2]] Part three. Binary is the same idea with a different base.
Binary works using exactly the same positional principle. But instead of
powers of ten, we use powers of two. Let's build the columns from right to
left. Two to the zero is one. Two to the one is two. Two squared is four.
Two cubed is eight. Two to the four is sixteen. Two to the five is thirty
two. Two to the six is sixty four. Two to the seven is one hundred and
twenty eight. [[beat:columns]] So for an eight-bit unsigned binary number,
our columns are: one hundred and twenty eight, sixty four, thirty two,
sixteen, eight, four, two, one. [[beat:doubling]] I want you to notice
something. Move one position to the left. What happens? One becomes two. Two
becomes four. Four becomes eight. Eight becomes sixteen. Every column is
double the column immediately to its right. This gives you an easy way to
reconstruct the headings if you forget them. Start at one and keep doubling:
one, two, four, eight, sixteen, thirty two, sixty four, one hundred and
twenty eight. When we normally write the table, we reverse that order: one
hundred and twenty eight, sixty four, thirty two, sixteen, eight, four, two,
one. Memorize that sequence eventually. But more importantly, understand
where it comes from.

[[beat:convert_intro]] Part four. Converting binary to denary. Let's convert
one zero one one zero one zero one into denary. First, put the binary digits
underneath our column headings. [[beat:rule]] Now here's the rule. When you
see a one, use the column value. When you see a zero, don't use the column
value. [[beat:walk]] Let's go from left to right. One hundred and twenty
eight has a one, so include one hundred and twenty eight. Sixty four has a
zero. Ignore it. Thirty two has a one. Add thirty two. Sixteen has a one.
Add sixteen. Eight has a zero. Ignore it. Four has a one. Add four. Two has
a zero. Ignore it. One has a one. Add one. [[beat:sum]] So one hundred and
twenty eight plus thirty two plus sixteen plus four plus one. Let's
calculate. One hundred and twenty eight plus thirty two is one hundred and
sixty. One hundred and sixty plus sixteen is one hundred and seventy six.
One hundred and seventy six plus four is one hundred and eighty. One hundred
and eighty plus one is one hundred and eighty one. [[beat:total]] Therefore
one zero one one zero one zero one in binary represents one hundred and
eighty one in denary. That's all binary-to-denary conversion is. You're
asking: which powers of two have been switched on?

[[beat:challenge1]] Challenge one. Pause and try. Convert zero one one zero
one zero one zero into denary. Don't wait for me. Pause the video. Write one
hundred and twenty eight, sixty four, thirty two, sixteen, eight, four, two,
one above the bits. Then add the active columns. [[beat:challenge1_answer]]
Let's check. Which columns are active? So sixty four plus thirty two plus
eight plus two. That is ninety six plus eight plus two, which is one hundred
and four plus two, which is one hundred and six. If you got one hundred and
six, excellent.

[[beat:denary_to_binary]] Part five. Converting denary to binary. Now let's
reverse the problem. Suppose I give you ninety three and ask you to
represent it as an eight-bit unsigned binary number. Write our headings.
[[beat:subtract_walk]] We're going to work from left to right. Ask: can I
subtract one hundred and twenty eight from ninety three without going
negative? No. So put zero under one hundred and twenty eight. Next: can I
use sixty four? Yes. Ninety three minus sixty four is twenty nine. Put one
under sixty four. We have twenty nine remaining. Can we use thirty two? No.
Put zero. Can we use sixteen? Yes. Twenty nine minus sixteen is thirteen.
Put one. Can we use eight? Yes. Thirteen minus eight is five. Put one. Can
we use four? Yes. Five minus four is one. Put one. Can we use two? No. Put
zero. Can we use one? Yes. Put one. [[beat:result93]] Our answer is zero one
zero one one one zero one. Let's verify it. Sixty four plus sixteen plus
eight plus four plus one equals ninety three. Correct.

[[beat:division]] Part six. The division-by-two method. There's another way
to convert denary to binary. Let's use a smaller number: twenty six. Divide
repeatedly by two and record the remainder. Twenty six divided by two is
thirteen remainder zero. Thirteen divided by two is six remainder one. Six
divided by two is three remainder zero. Three divided by two is one
remainder one. One divided by two is zero remainder one. [[beat:read_up]]
Now here's the important part. Read the remainders from bottom to top. That
gives one one zero one zero. If we need an eight-bit representation, add
leading zeros: zero zero zero one one zero one zero. Let's check. Sixteen
plus eight plus two is twenty six. Correct. [[beat:two_methods]] So there
are two useful methods. You can use the powers-of-two column method, or you
can use successive division by two. Know both.

[[beat:range_min]] Part seven. How large can an unsigned binary number be?
Let's think about an eight-bit unsigned number. The smallest possible
pattern is zero zero zero zero zero zero zero zero. That's zero.
[[beat:range_max]] The largest is one one one one one one one one. Every
column is active. One hundred and twenty eight plus sixty four plus thirty
two plus sixteen plus eight plus four plus two plus one equals two hundred
and fifty five. So an unsigned eight-bit integer can represent zero to two
hundred and fifty five. [[beat:formula]] There's also a useful formula. With
n bits, the number of possible patterns is two to the n. Eight bits gives
two to the eight, which is two hundred and fifty six different patterns.
Since one of those represents zero, the largest unsigned value is two to the
eight minus one, which is two hundred and fifty five. [[beat:overflow_tease]]
Keep this idea in mind. It will become very important when we discuss
overflow.
