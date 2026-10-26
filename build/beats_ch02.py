"""Beat placement for Chapter 2 — Data Transmission.

Run from the repo root:

    python build/beats_ch02.py

Each anchor is a phrase from the recording, not from the written plan,
because the two differ: the plan's "A USB connection can also supply
electrical power" is never said at that point (it arrives later, as a
benefit), and the plan's "the challenge is sharing the secret key
securely" is never said at all. Anchoring on the plan would have put two
reveals on sentences that do not exist.

mkbeats resolves these left to right and fails loudly on a poor match, so
a phrase that drifted out of the recording stops the build rather than
quietly marking the wrong word.
"""

from mkbeats import build

BEATS = [
    # ---------------------------------------------------------- opening
    ("open", "welcome to chapter 2 of Cambridge O Level Computer Science"),
    ("hook", "Imagine sending a large video to a friend"),
    ("hook_q", "So what happens if the data takes different routes"),
    ("map", "In this lesson we'll follow the data from sender to receiver"),
    ("exam_note", "As we go listen to the precise comparisons and sequences"),

    # ---------------------------------------------------------- packets
    ("part1", "All right so let's begin with packets"),
    ("packet_def", "A packet is a small unit of transmitted data"),
    ("packet_why", "A large file is divided into packets so that network links"),
    ("packet_routes", "If one route is busy or unavailable"),
    ("three_parts", "So a packet has three main sections"),
    ("header", "The header contains control information"),
    ("header_list", "This may include the destination address"),
    ("payload", "The payload contains part of the original message or file"),
    ("trailer", "And the trailer contains information used for error checking"),
    ("exam_point", "The destination address and packet number belong in the header"),
    ("exam_point2", "The payload carries the useful data"),

    # ------------------------------------------------- packet switching
    ("switching", "So now let's follow a message through packet switching"),
    ("ps_divide", "First the sender's computer divides the original data into packets"),
    ("ps_add", "Next each packet is given a header a payload and a trailer"),
    ("ps_route", "Routers examine the destination address in each packet"),
    ("ps_differ", "So different packets from same message may take different routes"),
    ("ps_arrive", "Because those routes may differ packets can arrive at different times"),
    ("ps_reorder", "So the receiver uses the packet numbers to put them back"),
    ("ps_missing", "If a packet is missing or damaged"),
    ("ps_reconstruct", "And once the packets have been received and arranged correctly"),
    ("ps_sequence", "So remember the sequence divide the data add packet information"),
    ("ps_trap", "Do not write that packets choose their own routes"),
    ("ps_why", "So why is packet switching useful"),
    ("ps_limits", "But packet switching does not guarantee that every packet"),

    # ----------------------------------------------- serial & parallel
    ("part2", "So now let's compare serial and parallel transmission"),
    ("serial", "Serial transmission sends one bit at a time along one communication channel"),
    ("parallel", "And parallel transmission sends several bits at the same time"),
    ("wires", "Because parallel transmission uses multiple channels it usually requires more wires"),
    ("not_same_time", "but the bits may not arrive at exactly the same time"),
    # "called this Q" is the transcriber on "called skew".
    ("skew", "So this timing problem is called"),
    ("skew_group", "If bits sent together arrive at different times"),
    ("skew_distance", "So a skew becomes more significant over longer distances"),
    ("serial_wins", "So serial transmission sends bits one after another"),
    ("recommend", "A common examination question asks you to recommend serial or parallel"),
    ("recommend_why", "Do not stop after naming a method"),
    ("recommend_eg", "For a long link between two buildings"),
    ("recommend_marks", "The marks usually come from connecting the technical reason"),

    # --------------------------------------------------------- direction
    ("direction", "So next we need to understand the direction of transmission"),
    ("simplex", "Simplex communications sends data in one direction only"),
    ("simplex_eg", "For example a sensor may send reading to a control center"),
    ("half", "Half duplex communication allows data to travel in both directions"),
    ("half_eg", "A push to talk you know walkie talkie is a familiar example"),
    ("full", "Full duplex communication allows data to travel in both directions at the same time"),
    ("full_eg", "Telephone conversation is an example because both people can speak"),
    ("memory", "So here's a quick memory check"),
    ("mem_simplex", "Remember this simplex means one way"),
    ("mem_half", "Half duplex means two way but taking turns"),
    ("mem_full", "full duplex means two way at the same time"),
    ("dir_trap", "Do not describe half duplex as one way communication"),
    ("dir_method", "So when a question asks you to recommend a direction mode"),

    # --------------------------------------------------------------- USB
    ("part3", "All right let's move to USB"),
    ("usb_def", "USB is a standard serial interface"),
    ("usb_seq", "the host computer detects when you plug in your device"),
    ("usb_driver", "operating system loads an appropriate driver"),
    ("usb_proto", "And the host and device then communicate using the USB protocol"),
    ("usb_benefits", "USB has several benefits"),
    ("usb_pnp", "It often plug and play detection"),
    ("usb_power", "It can carry both power and data"),
    ("usb_hot", "So devices can normally be connected or disconnected while the computer is running"),
    ("usb_limits", "There are also limitations though"),
    ("usb_bandwidth", "Devices sharing a hub may share available bandwidth"),
    ("usb_serial", "USB is a serial interface"),

    # ------------------------------------------------------- why errors
    ("part4", "Now let's look at why transmission errors occur"),
    ("causes", "Data may be corrupted by by electrical noise"),
    ("bit_change", "A bit may change for example a zero may arrive as a one"),
    ("data_lost", "So a bit or group of bits does not arrive"),
    ("data_extra", "or extra data may appear"),
    ("need_check", "The receiver therefore needs a way to check"),
    ("detect_vs_correct", "error detection and error correction and error correction are not the same"),
    ("detect_note", "It does not necessarily repair the data"),

    # ------------------------------------------------------------ parity
    ("parity", "So let's start with parity checks"),
    ("parity_def", "Parity is added so that the total number of ones follows an agreed rule"),
    ("even", "With even parity the total number of ones must be even"),
    ("odd", "With odd parity the total number of ones must be odd"),
    ("example", "Suppose we have the data bits 1 0 1 0 1 1 0"),
    ("count_ones", "So there are four ones"),
    ("even_bit", "If we use even parity the parity bit is 0"),
    ("odd_bit", "If we use odd parity the parity is 1"),
    ("receiver_counts", "At the receiving end the system counts the ones again"),
    ("parity_limit", "So one thing to remember parity has a limitation"),
    ("two_bits", "For example if two bits change the total number of ones might remain even"),
    ("block", "A parity block check uses two dimensional parity"),
    ("block_rows", "Data is arranged in rows a parity is added to each row"),
    ("block_single", "If a single bit changes one row check check and one column check"),
    ("block_locate", "The row and column intersect at likely location"),

    # ----------------------------------------------------- four methods
    ("four", "Now let's compare four error detection methods"),
    ("checksum", "A checksum is calculated from a block of data by the sender"),
    ("checksum_recv", "The receiver repeats the same calculation you know and compares the result"),
    ("checksum_limit", "So a checksum provides a stronger error checking than a simple parity bit"),
    ("echo", "With an echo check the receiver sends the received data back to the sender"),
    ("echo_compare", "The sender compares the return copy with the original"),
    ("echo_retx", "If the copies differ the sender can retransmit the data"),
    ("echo_cost", "The drawback is that the data is sent twice"),
    ("digit", "A check digit is used to detect errors when entering a scanning"),
    ("digit_calc", "When the number is entered the calculation is repeated"),
    ("digit_trap", "So keep the users distinct"),
    ("digit_not", "It is not encryption and it does not prove what entered the data"),

    # --------------------------------------------------------------- ARQ
    ("part5", "Now come the automatic repeat request"),
    ("arq_def", "Automatic repeat request combines error detection with acknowledgments"),
    ("arq_send", "So first the sender transmits a data block that includes error detection"),
    ("arq_timer", "The sender starts a timer"),
    ("arq_check", "The receiver checks the block"),
    ("arq_ack", "If the block is correct the receiver sends a positive acknowledgment"),
    ("arq_nak", "And if the receiver detects an error some systems send a negative"),
    ("arq_retx", "If a negative acknowledgment arrives the sender retransmits the block"),
    ("arq_timeout", "If no positive acknowledgment arrives before the timeout"),
    ("arq_repeat", "So the process repeats until the block is successfully received"),
    ("arq_why", "Why is the timeout important"),
    ("arq_forever", "Without a timeout the sender could wait forever"),
    ("arq_answer", "So for an examination answer describe the sequence clearly"),

    # -------------------------------------------------------- encryption
    ("part6", "so now let's finish with encryption"),
    ("enc_def", "Encryption converts readable data called plain text into unreadable data"),
    ("enc_key", "A key is a value used by an encryption or decryption algorithm"),
    ("enc_conf", "So encryption protects confidentiality"),
    ("enc_not", "So encryption does not stop from being intercepted"),
    ("enc_diff", "That is why encryption and error detection solve different problems"),
    # "Systematic" here is a misspeak for symmetric; the screen says symmetric.
    ("sym", "encryption uses the same secret key to encrypt and decrypt data"),
    ("sym_fast", "It is generally fast and suitable"),
    ("asym", "Asymmetric encryption uses a related pair of keys"),
    ("asym_public", "The public key can be shared"),
    ("asym_use", "To send confidential data to someone the sender encrypts the data"),
    ("asym_decrypt", "The recipient uses their private key to decrypt it"),
    ("asym_slow", "Asymmetric encryption helps with key distribution"),
    ("hybrid", "So many real systems combine both methods"),
    ("hybrid_how", "The asymmetric method is used to protect the exchange of a temporary"),
    ("hybrid_why", "So this approach combines the secure key exchange"),
    ("enc_remember", "So remember if confidential data is encrypted using the recipient's public key"),

    # ------------------------------------------------------------ review
    ("review", "All right let's review the chapter"),
    ("r_packet", "A packet has a header a payload and a trailer"),
    ("r_switching", "Routers direct the packets packet numbers help the receiver"),
    ("r_serial", "Serial transmission stands one bit at a time"),
    ("r_duplex", "So simplex is one way"),
    ("r_usb", "USB is a standard serial interface that can carry both data and power"),
    ("r_errors", "and check digits detect different kinds of errors"),
    ("r_arq", "automatic repeat request uses acknowledgments and timeout"),
    ("r_enc", "Symmetric encryption uses one shared secret key"),

    # ---------------------------------------------------------- practice
    ("practise", "So as you practice focus on order"),
    ("pr_order", "In a sequence question give the events in the correct order"),
    ("pause", "Pause the video after each question in your workbook"),
    ("diagnostic", "Then use the chapter 2 diagnostic at the academy"),
    ("ai", "You can also upload a photograph of your written answer"),
    ("close", "You've now completed chapter 2 data transmission"),
]

NOTE = ("Chapter 2 Data Transmission. Beats placed by anchor phrase from "
        "the recording; see build/beats_ch02.py.")

if __name__ == "__main__":
    build("CH02-data-transmission", "concept.data_transmission", BEATS,
          "CH02-data-transmission", NOTE)
