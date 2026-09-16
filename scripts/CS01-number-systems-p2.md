---
scene: cs.number_systems_p2
---

[[beat:hex_intro]] Part eight. Enter hexadecimal. Now suppose I give you one
one zero one zero one one zero one zero one one one one one zero. It's
perfectly valid binary. But it's not particularly pleasant for a human to
read. Did I type that, or did I type something slightly different? Long
binary sequences are easy for humans to misread. [[beat:hex_symbols]] So
computer science frequently uses another number system: hexadecimal. Usually
shortened to hex. Hexadecimal is base sixteen. That means it needs sixteen
symbols. But our normal digits only give us zero through nine. That's ten
symbols. We need six more. So hexadecimal uses letters.
[[beat:memorize]] Zero is zero, one is one, all the way to nine is nine.
Then A is ten. B is eleven. C is twelve. D is thirteen. E is fourteen. F is
fifteen. I recommend memorizing A B C D E F as ten, eleven, twelve,
thirteen, fourteen, fifteen.

[[beat:four_bits]] Part nine. Why binary and hex fit together so
beautifully. Here's the key relationship. Hexadecimal has sixteen
possibilities per digit. And sixteen is two to the power four. That means
one hex digit equals four binary bits. Four binary bits can represent zero
zero zero zero through one one one one, which means zero through fifteen.
Exactly the values represented by zero through F in hexadecimal.
[[beat:full_table]] Let's build the complete relationship. Zero zero zero
zero is zero is zero. Zero zero zero one is one. And so on, up to one one
one one, which is fifteen, which is F. [[beat:fallback]] Eventually you'll
recognize these quickly. But don't depend entirely on memorization. If you
forget one, use eight, four, two, one. Let me show you.

[[beat:group_intro]] Part ten. Binary to hexadecimal, step by step. Convert
one one zero one zero one one zero one zero one one into hexadecimal. Step
one: divide into groups of four. Always start grouping from the right. So we
get one one zero one, zero one one zero, one zero one one. Why groups of
four? Because one hexadecimal digit corresponds to four binary bits. Now
we're going to convert each group individually. [[beat:group1]] Group one is
one one zero one. Put our four-bit headings above it: eight, four, two, one.
A one means use the column. A zero means don't. So eight plus four plus zero
plus one is thirteen. But hexadecimal uses a single symbol for thirteen. Ten
is A, eleven is B, twelve is C, thirteen is D. Therefore one one zero one is
D. [[beat:group2]] Group two is zero one one zero. Again: eight, four, two,
one. Calculate: zero plus four plus two plus zero is six. Six is already
represented by the digit six in hexadecimal. Therefore zero one one zero is
six. [[beat:group3]] Group three is one zero one one. Eight, four, two, one.
Calculate: eight plus zero plus two plus one is eleven. What's eleven in
hexadecimal? A is ten. B is eleven. Therefore one zero one one is B.
[[beat:assemble]] Now put our answers together. One one zero one is D. Zero
one one zero is six. One zero one one is B. Therefore our binary number is D
six B in hexadecimal. That's the complete process.

[[beat:challenge2]] Challenge two. Binary to hex. Convert one zero one zero,
one one one one, zero one zero one. Pause the video.
[[beat:challenge2_answer]] First group: one zero one zero. Eight plus two is
ten. Ten in hex is A. Second: one one one one. Eight plus four plus two plus
one is fifteen. Fifteen is F. Third: zero one zero one. Four plus one is
five. Therefore A F five.

[[beat:padding]] Part eleven. What if there aren't four bits in every group?
Consider one zero one one zero one zero one one zero. Start grouping from
the right. The group on the left only has two bits. We need four. So add
zeros to the left. Now convert. Zero zero one zero is two. One one zero one
is thirteen, which is D. Zero one one zero is six. Therefore two D six.
[[beat:padding_warning]] Be careful. We added zeros on the left. Why?
Because leading zeros do not change the value. One zero and zero zero one
zero both represent two. But adding zeros on the other side can change the
positional value. So don't randomly add zeros.

[[beat:hex_to_binary]] Part twelve. Hexadecimal to binary. Now let's go
backwards. Convert seven A C into binary. This is actually easier. Every
hexadecimal digit becomes exactly four bits. Start with seven. Seven in
four-bit binary is zero one one one. Why? Four plus two plus one is seven.
Now A. A is ten. Ten is eight plus two. So one zero one zero. Now C. C is
twelve. Twelve is eight plus four. So one one zero zero. Put the groups
together. [[beat:hex_binary_note]] Notice something important. When
converting hex to binary, never drop the zeros inside the four-bit groups.
Each hexadecimal digit maps to four bits.

[[beat:hex_to_denary]] Part thirteen. Hexadecimal to denary. Now let's
convert three B seven into denary. Remember how denary had place values
based on powers of ten? And binary had powers of two? Hexadecimal has powers
of sixteen. For three hexadecimal digits, our columns are sixteen squared,
sixteen to the one, and sixteen to the zero, which gives two hundred and
fifty six, sixteen, and one. Put three B seven underneath.
[[beat:hex_denary_calc]] But we can't calculate with B until we remember B
is eleven. So: three times two hundred and fifty six. Eleven times sixteen.
Seven times one. Let's calculate. Three times two hundred and fifty six is
seven hundred and sixty eight. Eleven times sixteen is one hundred and
seventy six. Seven times one is seven. Now add: seven hundred and sixty
eight plus one hundred and seventy six is nine hundred and forty four. Nine
hundred and forty four plus seven is nine hundred and fifty one. Therefore
three B seven hexadecimal is nine hundred and fifty one in denary.

[[beat:denary_to_hex]] Part fourteen. Denary to hexadecimal. Let's convert
six hundred and eighty four to hexadecimal. We can repeatedly divide by
sixteen. Six hundred and eighty four divided by sixteen is forty two
remainder twelve. Forty two divided by sixteen is two remainder ten. Two
divided by sixteen is zero remainder two. [[beat:denary_hex_read]] Now
translate the remainders. Twelve is C. Ten is A. Two is two. And just as
with the division-by-two method, read the remainders from bottom to top.
That gives two A C. Let's verify it. Two times two hundred and fifty six is
five hundred and twelve. A means ten, so ten times sixteen is one hundred
and sixty. C means twelve, so twelve times one is twelve. Five hundred and
twelve plus one hundred and sixty plus twelve. Correct.

[[beat:why_hex]] Part fifteen. Why do we actually use hexadecimal? This is
where the subject becomes more practical. Hexadecimal gives humans a compact
representation of binary data. For example, hexadecimal is commonly
encountered in MAC addresses, IPv6 addresses, colour codes, and various
low-level values, diagnostics and error codes. [[beat:colours]] Let's look
at colours. You may have seen something like hash F F zero zero zero zero.
The six hexadecimal digits can be interpreted as three pairs. These
represent red, green and blue, or RGB. Each pair ranges from zero zero
hexadecimal to F F hexadecimal. [[beat:ff_value]] Let's find F F. F is
fifteen. So fifteen times sixteen plus fifteen is two hundred and forty plus
fifteen, which is two hundred and fifty five. Therefore each RGB component
can have a value from zero to two hundred and fifty five.
[[beat:colour_examples]] So hash F F zero zero zero zero means red is two
hundred and fifty five, green is zero, blue is zero. So we get bright red.
What would hash zero zero F F zero zero give us? Green. What about hash zero
zero zero zero F F? Blue. And hash F F F F F F has maximum red, maximum
green and maximum blue. That's white. Hexadecimal suddenly feels much less
abstract.

[[beat:mac]] Part sixteen. MAC and IP addresses. You'll also encounter
hexadecimal in networking. A traditional MAC address is commonly represented
as six groups of two hexadecimal digits, for example three C, five two,
eight two, seven A, nine one, F zero. That's much easier for a human to work
with than writing the equivalent forty-eight-bit binary sequence. IPv6
addresses also use hexadecimal notation. [[beat:why_summary]] The important
conceptual point isn't to memorize a particular address. It's to understand
that hexadecimal is often used because it provides a shorter, more
manageable representation of binary values. That's an excellent explanation
whenever you're asked why hex is useful.
