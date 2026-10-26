---
scene: concept.data_transmission
---

<!-- Chapter 2 Data Transmission. Beats placed by anchor phrase from the recording; see build/beats_ch02.py. -->

Alright guys, [[beat:open]] welcome to chapter 2 of Cambridge O -Level Computer
Science 2210 Data Transmission. [[beat:hook]] Imagine sending a large video to a
friend. The video has to travel through a network, pass through different devices, and
arrive in a form your friend's computer can use. [[beat:hook_q]] So what happens if
the data takes different routes? What if some of it's changed along the way? right?
And how can private information stay unreadable if someone intercepts it? [[beat:map]]
In this lesson, we'll follow the data from sender to receiver. We'll learn about
packets, transmission methods, USB, error detection, automatic repeat and request, and
encryption. [[beat:exam_note]] As we go, listen to the precise comparisons and
sequences that help you earn marks in the examination. [[beat:part1]] All right, so
let's begin with packets. [[beat:packet_def]] A packet is a small unit of transmitted
data. [[beat:packet_why]] A large file is divided into packets so that network links
can be shared by many users. [[beat:packet_routes]] If one route is busy or
unavailable, packets may be sent along other routes. [[beat:three_parts]] So a packet
has three main sections, a header, a payload, and a trailer. [[beat:header]] The
header contains control information. [[beat:header_list]] This may include the
destination address, the originator address, and a packet number. [[beat:payload]] The
payload contains part of the original message or file. It is the useful, you know,
data being carried. [[beat:trailer]] And the trailer contains information used for
error checking and may include an end marker. So here is an important examination
point, okay? [[beat:exam_point]] The destination address and packet number belong in
the header. they are control information. [[beat:exam_point2]] The payload carries the
useful data. [[beat:switching]] So now let's follow a message through packet
switching. [[beat:ps_divide]] First, the sender's computer divides the original data
into packets. [[beat:ps_add]] Next, each packet is given a header, a payload and a
trailer. [[beat:ps_route]] Routers examine the destination address in each packet and
select a route. [[beat:ps_differ]] So different packets from same message may take
different routes. [[beat:ps_arrive]] Because those routes may differ, packets can
arrive at different times or out of order. [[beat:ps_reorder]] So the receiver uses
the packet numbers to put them back into the correct order. [[beat:ps_missing]] If a
packet is missing or damaged, the receiver may request that it is not for it to be
sent again. [[beat:ps_reconstruct]] And once the packets have been received and
arranged correctly, the original data can be re -constructed. [[beat:ps_sequence]] So
remember the sequence, divide the data, add packet information, route the packets,
reorder them, and reconstruct the original message. [[beat:ps_trap]] Do not write that
packets choose their own routes. Routers make routing decisions. [[beat:ps_why]] So
why is packet switching useful? It allows many users to share network capacity. It can
also help data, you know, avoid congestion or a failed link. [[beat:ps_limits]] But
packet switching does not guarantee that every packet will take the shortest route or
that every packet will arrive in order, right? [[beat:part2]] So now let's compare
serial and parallel transmission, okay? [[beat:serial]] Serial transmission sends one
bit at a time along one communication channel. [[beat:parallel]] And parallel
transmission sends several bits at the same time along multiple channels.
[[beat:wires]] Because parallel transmission uses multiple channels, it usually
requires more wires. It can transfer several bits simultaneously,
[[beat:not_same_time]] but the bits may not arrive at exactly the same time.
[[beat:skew]] So this timing problem is called this Q. [[beat:skew_group]] If bits
sent together arrive at different times, the receiver may group bits incorrectly.
[[beat:skew_distance]] So a skew becomes more significant over longer distances or at
high speeds. [[beat:serial_wins]] So serial transmission sends bits one after another
so it avoids this type of skew. It uses fewer wires and is generally more suitable for
longer distance lengths. [[beat:recommend]] A common examination question asks you to
recommend serial or parallel transmission in a scenario. [[beat:recommend_why]] Do not
stop after naming a method, explain why it fits the situation. [[beat:recommend_eg]]
For a long link between two buildings, serial transmission may be more suitable
because it chooses fewer wires and avoids timing skew between multiple channels.
signals. [[beat:recommend_marks]] The marks usually come from connecting the technical
reason to the scenario. [[beat:direction]] So next we need to understand the direction
of transmission. [[beat:simplex]] Simplex communications sends data in one direction
only. [[beat:simplex_eg]] For example, a sensor may send reading to a control center
without receiving information back over that connection. [[beat:half]] Half duplex
communication allows data to travel in both directions, but not at the same time. So
the devices to take turns. [[beat:half_eg]] A push to talk, you know, walkie -talkie
is a familiar example. [[beat:full]] Full duplex communication allows data to travel
in both directions at the same time. [[beat:full_eg]] Telephone conversation is an
example because both people can speak here and here simultaneously, right?
[[beat:memory]] So here's a quick memory check. [[beat:mem_simplex]] Remember this,
simplex means one way, half [[beat:mem_half]] Half duplex means two -way, but taking
turns, [[beat:mem_full]] full duplex means two -way at the same time.
[[beat:dir_trap]] Do not describe half duplex as one -way communication, both sides
can transmit. They simply cannot transmit simultaneously. [[beat:dir_method]] So when
a question asks you to recommend a direction mode, first decide whether communication
is needed in one direction or both. If both directions are needed, ask whether both
sides must send data at the same time, right? Then name the mode and explain your
choice using details from the scenario. [[beat:part3]] All right, let's move to USB,
right? We just stands for Universal Serial Bus. [[beat:usb_def]] USB is a standard
serial interface. You use it. I mean, everybody uses it. You know, [[beat:usb_seq]]
the host computer detects when you plug in your device, right? The host computer
detects it to [[beat:usb_driver]] operating system loads an appropriate driver if
required and when required. [[beat:usb_proto]] And the host and device then
communicate using the USB protocol. And data is transferred serially. And error
checking can be used during the transfer, right? [[beat:usb_benefits]] USB has several
benefits, OK? It's widely supported standard. [[beat:usb_pnp]] It often plug -and
-play detection. So a user connect a device without manually configuring every detail.
[[beat:usb_power]] It can carry both power and data. [[beat:usb_hot]] So devices can
normally be connected or disconnected while the computer is running.
[[beat:usb_limits]] There are also limitations though. Performance depends on the USB
version. Cable length is limited. [[beat:usb_bandwidth]] Devices sharing a hub may
share available bandwidth. right? And different connected types may require adapters.
And a malicious USB device can also create a secure reader. What important point?
[[beat:usb_serial]] USB is a serial interface. Do not describe data traveling through
USB as parallel transmission. Okay? That's an important point. You may see it in the
exam. [[beat:part4]] Now let's look at why transmission errors occur. [[beat:causes]]
Data may be corrupted by by electrical noise, electromagnetic interference, a weak
signal or damaged transmissions media, okay? [[beat:bit_change]] A bit may change, for
example, a zero may arrive as a one, right? Data may be lost, right?
[[beat:data_lost]] So a bit or group of bits does not arrive [[beat:data_extra]] or
extra data may appear. [[beat:need_check]] The receiver, therefore, needs a way to
check whether the received data differs from what was said, okay? So,
[[beat:detect_vs_correct]] error detection and error correction and error correction
are not the same thing. An error detection method can indicate that data is probably
wrong. [[beat:detect_note]] It does not necessarily repair the data. The system may
need retransmission or another recovery method. [[beat:parity]] So let's start with
parity checks. [[beat:parity_def]] Parity is added so that the total number of ones
follows an agreed rule. [[beat:even]] With even parity, the total number of ones must
be even. [[beat:odd]] With odd parity, the total number of ones must be odd.
[[beat:example]] Suppose we have the data bits 1, 0, 1, 0, 1, 1, 0.
[[beat:count_ones]] So there are four ones. [[beat:even_bit]] If we use even parity,
the parity bit is 0 because the total remains 4, which is even. [[beat:odd_bit]] If we
use odd parity, the parity is 1. The total then becomes 5, which is odd.
[[beat:receiver_counts]] At the receiving end, the system counts the ones again. If
the total does not match the agreed parity rule, an error is detected.
[[beat:parity_limit]] So one thing to remember, parity has a limitation. It can detect
an odd number of change bits, but an even number of change bits may leave the parity
apparently correct. [[beat:two_bits]] For example, if two bits change, the total
number of ones might remain even. The receiver could then fail to detect the error.
[[beat:block]] A parity block check uses two -dimensional parity. [[beat:block_rows]]
Data is arranged in rows, a parity is added to each row, and parity is also checked
down the columns. [[beat:block_single]] If a single bit changes, one row check check
and one column check may both fail. If a single bit changes, one row check and one
column check may both fail. [[beat:block_locate]] The row and column intersect at
likely location of the change bit. So this can help the system locate a single bit
error. [[beat:four]] Now let's compare four error detection methods. Okay, parity,
checksum, echo check, and check digit. All right. Parity, checksum, echo check, and
check digit. [[beat:checksum]] A checksum is calculated from a block of data by the
sender. The checksum is transmitted with the data, with the data.
[[beat:checksum_recv]] The receiver repeats the same calculation, you know, and
compares the result. If the values differ, the data may have change.
[[beat:checksum_limit]] So a checksum provides a stronger error checking than a simple
parity bit. But a matching checksum does not prove with absolute certainty that no
error occurred. So different corruptions can sometimes produce the same checksum.
[[beat:echo]] With an echo check, the receiver sends the received data back to the
sender. [[beat:echo_compare]] The sender compares the return copy with the original.
[[beat:echo_retx]] If the copies differ, the sender can retransmit the data. But
there's a drawback for it. [[beat:echo_cost]] The drawback is that the data is sent
twice, right, which increases transmission time and uses more bandwidth, right? So the
echo data could also be corrupted though, okay? [[beat:digit]] A check digit is used
to detect errors when entering a scanning or an identifier, right, such as an ISBN or
a barcode. The check data is calculated it from the other digits. [[beat:digit_calc]]
When the number is entered, the calculation is repeated. If the result does not match
the check digit, the system detects a likely data error. [[beat:digit_trap]] So, keep
the users distinct. A check data is mainly used to check identifiers and data entry.
[[beat:digit_not]] It is not encryption and it does not prove what entered the data.
[[beat:part5]] Now come the automatic repeat request, right? Usually you'll see it
abbreviated to ARL, automatic repeat request, okay? [[beat:arq_def]] Automatic repeat
request combines error detection with acknowledgments and a timeout. Its purpose is to
help ensure that data is received correctly. [[beat:arq_send]] So first the sender
transmits a data block that includes error detection information. [[beat:arq_timer]]
The sender starts a timer. [[beat:arq_check]] The receiver checks the block.
[[beat:arq_ack]] If the block is correct, the receiver sends a positive
acknowledgment. [[beat:arq_nak]] And if the receiver detects an error, some systems
send a negative acknowledgment. Remember, some systems send a negative acknowledgment
of it. [[beat:arq_retx]] If a negative acknowledgment arrives, the sender retransmits
the block. The sender also checks the timer. [[beat:arq_timeout]] If no positive
acknowledgment arrives before the timeout, the sender retransmits the block.
[[beat:arq_repeat]] So the process repeats until the block is successfully received or
until the system reaches a defined limit. [[beat:arq_why]] Why is the timeout
important? The data block might be lost. The acknowledgement might also be lost.
[[beat:arq_forever]] Without a timeout, the sender could wait forever, right?
[[beat:arq_answer]] So for an examination answer, describe the sequence clearly, okay?
Send the block, check it, acknowledge successful receipt, and restrustment after an
error or timeout. Remember that, okay? I'm going to repeat it. Describe the sequence
in this way. Send the block, check it, acknowledge successful receipt, and transmit
after an error or timeout. Alright, [[beat:part6]] so now let's finish with
encryption, okay? [[beat:enc_def]] Encryption converts readable data called plain text
into unreadable data called ciphertext, okay? And there are a lot of games where you
actually go and you know check the numbers and you can ciphertext, right? You can play
those games on your phone as well. [[beat:enc_key]] A key is a value used by an
encryption or decryption algorithm. [[beat:enc_conf]] So encryption protects
confidentiality. If encrypted data is intercepted, an attacker should not be able to
understand it without the correct key. This is how the spies used to communicate. It
goes back to, I think, World War II. There are a bunch of documentaries on it as well.
[[beat:enc_not]] So encryption does not stop from being intercepted. It does not
automatically prevent data from being deleted or damaged. [[beat:enc_diff]] That is
why encryption and error detection solve different problems, okay? They're not solving
the same problem. Systematic [[beat:sym]] encryption uses the same secret key to
encrypt and decrypt data. [[beat:sym_fast]] It is generally fast and suitable to
decrypt the data, right? [[beat:asym]] Asymmetric encryption uses a related pair of
keys, a public key and a private key. [[beat:asym_public]] The public key can be
shared. The private key must remain secret. [[beat:asym_use]] To send confidential
data to someone, the sender encrypts the data using the recipient's public key.
[[beat:asym_decrypt]] The recipient uses their private key to decrypt it.
[[beat:asym_slow]] Asymmetric encryption helps with key distribution. What is
generally slower than symmetric encryption. [[beat:hybrid]] So many real systems
combine both methods. This is called hybrid encryption. [[beat:hybrid_how]] The
asymmetric method is used to protect the exchange of a temporary symmetric key. Then
the faster symmetric method encrypts the main data. [[beat:hybrid_why]] So this
approach combines the secure key exchange of asymmetric encryption with the speed of
symmetric encryption. [[beat:enc_remember]] So remember, if confidential data is
encrypted using the recipient's public key, the recipient's correspondent private key
is used to decrypt it. [[beat:review]] All right, let's review the chapter, okay?
Let's recap. [[beat:r_packet]] A packet has a header, a payload and a trailer. Packet
switching device into packets, a device data into packets. [[beat:r_switching]]
Routers direct the packets, packet numbers help the receiver put them back in order.
[[beat:r_serial]] Serial transmission stands one bit at a time. Pedal transmission
stands several bits simultaneously, but can be affected by skew. [[beat:r_duplex]] So
simplex is one way. Half duplex is two -way, taking turns. Full duplex is
simultaneous, two -way communication. [[beat:r_usb]] USB is a standard serial
interface that can carry both data and power. Parity, checksims, eco -check,
[[beat:r_errors]] and check digits detect different kinds of errors. Error detection
does not always correct the data, right? [[beat:r_arq]] automatic repeat request, uses
acknowledgments, and timeout to trigger retransmission. [[beat:r_enc]] Symmetric
encryption uses one shared secret key. Asymmetric encryption uses a public and private
key. Hybrid encryption combines both approaches. [[beat:practise]] So as you practice,
focus on order, Comparison and application. [[beat:pr_order]] In a sequence question,
give the events in the correct order. In a comparison, describe both methods. In a
scenario, use details from the scenario to justify your choice. [[beat:pause]] Pause
the video after each question in your workbook and try it before checking the answer
section. [[beat:diagnostic]] Then use the chapter 2 diagnostic at the academy
.digitaltearer .net to find any topics that need more practice. [[beat:ai]] You can
also upload a photograph of your written answer and ask the digital tutor to check
whether your explanation is accurate. Identify missing points and give you a harder
follow -up questions. [[beat:close]] You've now completed chapter 2, data
transmission, keep practicing the sequences and comparisons and you'll be ready to
apply these you know these ideas confidently in unfamiliar environment and unfamiliar
examination questions as well. Good luck. I'll see you on chapter 3.
