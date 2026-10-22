---
scene: concept.data_representation
---

<!-- Body is the transcript verbatim so the aligner matches exactly. Beats placed by anchor phrase, not by hand-counted word index. Covers slides 1-20 of the companion deck; the recording stops after storage units. -->

[[beat:open_title]] Welcome to chapter one, data representation for Cambridge O -Level
Computer Science, syllabus 2210. So [[beat:open_book]] open chapter one in your book
and keep a pen nearby, right? So in this lesson, [[beat:open_scope]] we will connect
every major idea in that in the chapter. Number systems, binary arithmetic, shifts,
two complement, text sound, text, sound images, storage units and compression.
[[beat:open_goal]] The goal is more than remembering definitions, okay?
[[beat:open_by_end]] By the end, you should be able to explain each idea using precise
examination language. Carry out the calculations accurately and recognize the common
traps that cost more marks. So [[beat:open_pause]] pause the video whenever you see a
stop and check slide. So attempt the question before I reveal the method. So let's
begin. [[beat:why_display]] A computer may display photographs, play music, text and
video, but its circuits do not understand those forms directly, right? So at the
lowest level, [[beat:why_states]] an electronic circuit distinguishes between two
stable states. [[beat:why_switch]] A voltage may be high or low, right? A switch may
be on or off. [[beat:why_bit]] We label those states as one and zero. So one binary
digit is called the bit, right? [[beat:why_reliable]] 2 states make digital systems
reliable because small electrical variations can still be interpreted as the intended
high or low state. So this leads to the examiner quality explanation.
[[beat:why_answer]] Data is converted into binary so that it can be processed by logic
gates and stored in registers. What's saying only that computers understand 0 and 1,
[[beat:why_vague]] that statement is too vague. Name the hardware reason. Two stable
electronic states. [[beat:map_intro]] So the chapter becomes much easier, right? So
when you see a structure, [[beat:map_1]] first we learn how numbers are represented
using binary, denary, and hexadecimal. We then use those ideas for binary addition,
overflow, logical shifts, and two's complement. [[beat:map_2]] Second, we examine how
character sets, sampling and pixels represent text, sound and images. [[beat:map_3]]
Third, we calculate file sizes and convert storage units. [[beat:map_4]] Finally, we
compare lossless and lossy compression and apply run length encoding.
[[beat:map_connected]] So these topics are connected. For example, a sound sample
becomes a binary number and the number of bits per sample, right? affects the file
size. So keep asking one question throughout the lesson. [[beat:map_question]] What
exactly is being encoded and how many bits are needed? [[beat:pv_base]] So a number
system has a base. The base determines the available digit symbols, how place values
grow from right to left. [[beat:pv_denary]] Denry is base 10, so its columns are of 1s
to 10s, right, 1s, 10s, 100s, and 1000s, right. [[beat:pv_binary]] Binary is base 2.
So its columns are powers of 2. [[beat:pv_row]] For an 8 -bit pattern, the place
values from left to right, 128. 64, 32, 16, 8, 4, 2, and 1. [[beat:pv_contrib]] A bit
containing 1 contributes its place value. A bit containing 0 contributes nothing.
[[beat:pv_learn]] So learn this row until you can write it from memory. It supports
binary conversion, unsigned ranges, shifts, and twos complement. So I would want you
to, you know, just get this in your head, what this what the slide is doing for you,
right? [[beat:b2d_intro]] So let us convert binary 1, 0, 1, 0, 1, 0 to denry. Okay.
[[beat:b2d_write]] So write the eight places values above the bits. [[beat:b2d_ones]]
We have ones under 128. 32, 16, 4, and 2. [[beat:b2d_add]] Add only those values,
right? [[beat:b2d_result]] 128 plus 32 plus 16 plus 4 plus 2 equals 182, right?
Therefore, the binary 101010 equals denry 182. [[beat:b2d_show]] So in the
examination, show the selected place values or the addition when working is requested,
right? This gives you a quick check, right? [[beat:b2d_check]] An unsigned 8 -bit
numbers must be between 0 and 255. That's the key thing to remember. So with me, all
right. [[beat:d2b_intro]] So now connect denry 157 to 8 -bit denry. [[beat:d2b_128]]
Let's start with the largest place value 128 fits. So you know we're going to write 1
and subtract it. The remainder is 29, right? [[beat:d2b_6432]] So 64 and 32 do not
fit, right? So write 0 in both columns. [[beat:d2b_rest]] 16 fits leaving 13, right?
And then 8 fits leaving 5. 4 fits leaving 1. 2 does not fit and 1 fits, right? The
result is 1, 0, 1, 1, 0, 1. [[beat:d2b_result]] Notice that every column receives a
digit, right? When And [[beat:d2b_leading]] a question asked for eight bits include,
include leading zeros, right? [[beat:d2b_13]] And denry 13, for example, is 0, 0, 0,
0, 1, 1, 0, 1, right? Okay. [[beat:hex_base]] Hexadecimal is base 16. It uses a symbol
0 to 9, followed by A, B, C, D, and F for the values 1 to 15, okay?
[[beat:hex_nibble]] So one hexadecimal digit maps exactly the four binary bits. And
it's called a Nibble, N -I -B -B -L -E, right? [[beat:hex_shorter]] This makes long
binary patterns shorter and easier for people to read. [[beat:hex_example]] For
example, binary 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1 becomes hexadecimal B6B, okay?
[[beat:hex_reverse]] So in the other direction, hexadecimal 7A3 becomes binary 0, 1,
1, 1, 0, 1, 0, 0, 0, 0, 1, 1. Okay, [[beat:hex_where]] and hexadecimal appears in
memory addresses, right? Machine code, media access, control addresses, internet
protocol version six addresses, and color codes. [[beat:hex_storage]] It does not
reduce the storage used inside the computer, right? So underlying data remains binary,
all right? So the underlying data remains one and zero, okay? [[beat:hp_two]] So for 2
hexadecimal number, the left digit represents 16s and the right digit represents 1.
[[beat:hp_4d]] Hexadecimal 4D means 4 multiplied by 16 plus 13, right? Because D
stands for 13, right? That gives what [[beat:hp_77]] that gives 77 right to convert
denry 206 to decimal to hexadecimal divide by 16 did you get it [[beat:hp_206]] so to
convert denry 206 to hexadecimal divide by 16 right [[beat:hp_quotient]] so the cotton
is 12 and the remainder is 14. [[beat:hp_ce]] 12 is C and 14 is E. So answer is C E.
[[beat:hp_check]] A useful checking routine is to convert your result back right. C
multiplied by 16 is 192. Add E which is 14 and you turn to 206. Okay.
[[beat:add_rules]] Now, the binary addition follows four small rules. [[beat:add_r1]]
Zero plus zero gives zero. Zero plus one gives one. Okay. [[beat:add_r2]] One plus one
gives binary one, zero. So write zero and carry one. Okay. [[beat:add_r3]] One plus
one, a carried one gives binary one. One, one. Okay. So write one and carry one.
[[beat:add_dir]] right work from right to left exactly as you do in denry addition
[[beat:add_example]] right in the examples 0 1 1 0 1 1 0 1 plus 0 0 1 1 0 1 1 gives
you 1 0 0 0 1 0 0 and in denry [[beat:add_check]] 109 plus 55 equals 164, right, which
confirms the answer. [[beat:add_carry]] Show carries clearly right a carry is a part
of the calculation. It's not automatically overflow, okay [[beat:ov_range]] So for
positive 8 -bit integers the available range is 0 255 [[beat:ov_def]] Overflow occurs
when the true result is greater than 255 and therefore needs more than 8 bits
[[beat:ov_example]] so consider binary 1 1 0 0 1 0 1 0, 1, 0 plus 0, 1, 0, 1, 1, 1, 0,
1. [[beat:ov_values]] The denry values are 202 and 93. [[beat:ov_sum]] The sum is 295.
[[beat:ov_ninth]] The 9th bit falls outside the bit register. So unsigned overflow
occurs here, right? So it straight both parts in an explanation. [[beat:ov_explain]]
The result is outside the average range and and it cannot fit in the register.
[[beat:ov_notcarry]] Do not describe every carry as overflow, all right?
[[beat:sh_intro]] Now let's look at logical shifts, right? [[beat:sh_def]] A logical
shift moves every bit left to right, left to right, okay? [[beat:sh_lost]] Bits
published beyond the register are lost and zeros enter at the opposite end.
[[beat:sh_mult]] If no significant bit is lost, shifting left by one place multiplies
the unsigned value by two. [[beat:sh_div]] And shifting right by one place divides the
unsigned value by two and discards any remainder. [[beat:sh_example]] For example, 0,
0, 1, 1, 0, 1, 1, 1 shifted left by two places becomes 1, 1, 0, 1, 1, 1, 0, 0.
[[beat:sh_result]] So, the original value 55 becomes 225, [[beat:sh_inspect]] but
always inspect the bits that leave the register. If a 1 is discarded, the simple
multiplication or division relationship no longer preserves the original value.
[[beat:tc_intro]] Let's talk about 2's complement now. [[beat:tc_def]] 2's complement
represents positive and negative integers using a fixed number of bits. In an 8 -bit
value, [[beat:tc_msb]] the most significant bit has a place value of negative 128.
[[beat:tc_rest]] The remaining columns keep their positive values, 64, 32, 16, 8, 4,
2, and 1. [[beat:tc_range]] This produces a range from negative 128 to positive 127.
[[beat:tc_leading]] A leading zero indicates a non -negative value. Always remember
that. And a leading one indicates a negative value. To read 11, 0, 1, 0, 1, 1,
[[beat:tc_read]] add the sign -place values, right? negative 128 plus 64 plus 32 plus
8 plus 2 plus 1. [[beat:tc_result]] So what is the result? The result is negative 21,
right? Yeah. Alright, let's talk about the negative value now, right?
[[beat:ia_intro]] To represent negative 37, [[beat:ia_write]] first write positive 37
as 8 -bit binary 0 0 1 0 0 1 0 1. [[beat:ia_invert]] Invert every bit to convert 1 1 0
1 1 0 1 0. [[beat:ia_add]] Then add 1 giving 1 0 and 1 1 0 1 1, right?
[[beat:ia_check]] Check the result using you know using sign place values. negative
128 plus 64 plus 16 plus 8 plus 2 equals plus plus 1 equals negative 37.
[[beat:ia_never]] Never place a minus sign in front of a binary pattern okay. The
pattern itself encodes the sign. [[beat:ia_limit]] Also remember that the positive
limit is 127 because one bit is used as the negative place value. Alright,
[[beat:sc_intro]] now moving on to the number system check point, right? Pause the
video now, right? [[beat:sc_pause]] I want you to pause the video and answer these
four questions. [[beat:sc_q1]] First, convert binary 0, 1, 1, 0, 1, 0, 1, 1 to denry.
Okay? [[beat:sc_q2]] Second, write denry 45 as an 8 -bit binary integer.
[[beat:sc_q3]] Third task is to convert binary 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1,
0 to hexadecimal. So that's your third task. [[beat:sc_q4]] And the fourth is write
negative 54 as 8 -bit 2's complement. After you've done this four, then resume, right?
Don't start looking at the answer right away. [[beat:sc_resume]] Resume when you have
shown you're working, right? [[beat:sc_answers]] The answers are, you know, the
answers are 107, 001, 001, and 01. 1, hexadecimal bca, and 1, 0, 0, 1, 0, 1, 0.
[[beat:sc_differs]] If an answer differs, identify the first step where your method
changed. Correct this step before continuing, all right? You need to get it right
before you move on. All right, [[beat:tx_intro]] so a character set assigns a
numerical code to every character. [[beat:tx_stored]] The code is then stored in
binary. [[beat:tx_examples]] A capital letter, a digit, a punctuation mark, and even a
control character each have a defined code, right? ASCII, pronounced ASCII, right?
[[beat:tx_ascii]] Includes common English letters, digits, punctuation and control
characters. [[beat:tx_unicode]] Unicode supports a much larger range of writing system
symbols and emoji right. So an examination comparison should make the relationship
clear. [[beat:tx_compare]] Unicode can represent a greater range of characters than
ASCII, but it may require more bits per character. I was saying that text is stored as
letters, right? [[beat:tx_avoid]] The computer stores the binary codes assigned by the
character set, okay? [[beat:sn_intro]] So now let's look at the sampling conversions,
right? So begins, right? [[beat:sn_wave]] As a continuously challenging, changing
analog wave. An analog to digital converts, [[beat:sn_adc]] a converter measures the
amplitude at regular time intervals. [[beat:sn_sample]] Each measurement is a sample,
right? is stored as a binary value. [[beat:sn_rate]] So sample rate is the number of
samples taken per second measured in hertz. [[beat:sn_44k]] So a sample rate of 44
,000 hertz means study means 44 ,000 samples every second. [[beat:sn_res]] Sample
resolution sometimes called bit depth is the number of bits used to store each sample.
So, remember that, right? Sample rate is the number of samples taken per second,
measured in hertz, right? A sample rate of 44 ,000 hertz means 44 ,000 samples every
second, right? Sample resolution, on the other hand, which is also called bit depth,
is the number of bits used to storey sample. [[beat:sn_increase]] So, increasing the
sample rate captures the wave more frequently, right? Increasing the sample resolution
provides more, you know, more possible amplitude values, right? Either change usually
improves accuracy, but it also increases the file size, right? [[beat:sn_separate]]
Keep those two terms separate, samples per second versus bits per sample.
[[beat:sf_intro]] Let's talk about sound rate. For uncompressed sound,
[[beat:sf_formula]] the file size in bits equals sample rate multiplied by sample
resolution, multiplied by duration in seconds, multiplied by the number of channels.
[[beat:sf_again]] Let me say it again. For uncompressed sound, file size in bits
equals samples rate multiplied by sample resolution, multiplied by duration in
seconds, multiplied by the number of channels. [[beat:sf_example]] So consider a mono
recording, right? Mono recording sample at 44 ,000 Hz using 16 bits per sample for 30
seconds. [[beat:sf_mono]] So mono has only one channel, right? That's what, so
multiply by 4 ,000 by 16 by 31. [[beat:sf_calc]] The result is 21 ,120 ,000 bits.
[[beat:sf_bytes]] Then you can divide by bit to obtain 2 ,640 ,000 bytes.
[[beat:sf_units]] So keep units visible at every step. A value in bits is not the same
as a value in bytes. For the stereo type, multiply by two channels. So mono, you don't
need a channel, but [[beat:sf_stereo]] if the exam question asks for a stereo sound,
multiply it by two channels. [[beat:im_intro]] So let's think about how the bitmap
stores color value. [[beat:im_grid]] So a bitmap image is a grid of pixels. It's
basically a grid of pixel. [[beat:im_pixel]] Each pixel has a binary color value.
[[beat:im_res]] Image resolution is the number of pixels, often written as width
multiplied by height. We'll talk about pixels. [[beat:im_phone]] My phone has 4k
pixels or 1080 pixels. What does that actually mean? right? [[beat:im_detail]] More
pixels can preserve finer spatial detail. [[beat:im_depth]] More bits per pixel
provide a larger range of possible colors, right? And if you have both, both increase
the uncompressed file size, okay? [[beat:im_meta]] So metadata such as dimensions,
creation date, or camera settings may also be short. But basic examination
calculations normally use only the pixel count and color depth unless a metadata size
is given. If it's given, then yeah, include it. If not, then don't, don't bother.
[[beat:if_formula]] So the uncompressed size of bit of an image in this equal width
multiplied by a height, right multiplied by color depth. [[beat:if_example]] So for an
image that is 1 ,920 pixels wide and 1 ,080 pixels high multiply with 24 -bit color,
[[beat:if_calc]] multiply 1 ,920 by 1 ,080 by 24. [[beat:if_bits]] The result is a 49
,766 ,400 -bit. right? [[beat:if_bytes]] Now divide by 8 to obtain 6 million, right?
220 ,800 bytes. [[beat:if_errors]] So the most common errors are forgetting the color
depth or changing from bits to bytes without dividing by 8, right? So I see that
happen a lot. [[beat:st_intro]] So now let's talk about storage, right? Because the
largest size, the better image, it takes more and more storage, right?
[[beat:st_binary]] So in this syllabus, storage units are binary multiples, okay?
[[beat:st_ladder]] Eight bits make one byte. 1 ,024 bytes make one kilobyte, okay?
[[beat:st_1024]] 1 ,024 kilobytes make one megabyte, right? it, 1 ,024 megabytes make
one gigabyte. [[beat:st_direction]] So moving from a smaller unit to a larger unit
means divide. Okay. Moving from a larger unit to a smaller unit means multiply.
[[beat:st_example]] For example, 2 ,764 ,800 bytes divided by 1 ,024 equals 2 ,000,
right? Equals divided by 1 ,024 would equal 2 ,700 kilobytes. [[beat:st_unit]] Write
the unit after every answer, right? Correct? are arithmetic with the wrong unit going
to still lose marks.
