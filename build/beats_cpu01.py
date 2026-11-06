"""Beat placement for the fetch-decode-execute lesson.

Run from the repo root:

    python build/beats_cpu01.py

The recording is the shared O Level 2210 / AS Level 9618 lesson, and it
starts where the plan's timeline says "0:45 - the question we're
answering": there is no opening on this take, and no O Level or AS Level
recap after the shared one, so neither has a beat. A card the narration
never earns is the one thing this pipeline exists to prevent.

Anchors are copied from the transcript as it came out, mis-hearings
included — "the more" for MAR, "the DR" for MDR, "12 plus 7 is 90" for
nineteen, "restarts at night" for starts at nine. Matching the delivery is
the whole job; matching the written script would place the markers against
words that were never said.

Transcribed with build/transcribe.py --chunk 90, then trimmed with
build/segment.py --pad 1.0 to drop ten seconds of lead-in and twenty of
room noise at the end.
"""

from mkbeats import build

BEATS = [
    # ------------------------------------------------- the question we answer
    ("open", "All right, so let's start with a simple question"),
    ("question", "When you click run, how does the computer turn a program into actions"),
    ("think", "Think about that"),
    ("not_magic", "the processor does not read a whole program"),
    ("sequence", "It works through instructions in an organized sequences"),
    ("for_each", "For each instruction"),
    ("then_next", "Then it moves it to the next instruction"),
    ("named", "That repeating process is called the fetch decode execute cycle"),
    ("alias", "Some books call it"),
    ("today", "So today we'll make that process visible"),
    ("agenda", "We'll name the important CPU components"),

    # ------------------------------------------------- the stored-program idea
    ("stored", "So to understand the cycle, we need one key idea"),
    ("program_is", "a program consists of instructions"),
    ("in_memory", "Those instructions are stored in memory along with the data"),
    ("retrieves", "The processor retrieves instructions from memory as it needs them"),
    ("von_neumann", "So in the one Newman model instructions and data share the same main memory"),
    ("buses_intro", "The processor communicates with memory and input output"),
    ("system", "So let's draw the basic system"),

    # ----------------------------------------------------------- inside the CPU
    ("inside", "Inside the CPU, we'll focus on the control unit"),
    ("cu", "The control unit or CU coordinates the CPU's activity"),
    ("cu_role", "It interprets instructions and sends control signals"),
    ("alu", "The arithmetic logic unit, or ALU, performs arithmetic operations"),
    ("alu_logic", "and logical operations, such"),
    ("regs_role", "Registers, hold the addresses, instructions, and the data"),
    ("regs_small", "There are much smaller than main memory"),
    ("regs_direct", "but they are directly available to the processor"),

    # --------------------------------------------------------- four registers
    ("four_regs", "So now let's meet four registers that are central to the cycle"),
    # He says "program controller"; it is the program COUNTER, and the
    # screen says so.
    ("pc", "First is the program controller or PC"),
    ("pc_role", "the PC stores the address of next instruction"),
    ("pc_bookmark", "think of it as a process is bookmark"),
    ("mar", "Next is the memory address register"),
    ("mar_role", "Stores the address of the memory location currently being accessed"),
    ("mar_example", "So if the CPU wants to read an instruction from, say, address 1000"),
    ("mdr", "Then we have memory data register or MDR"),
    ("mdr_role", "This is where we hold the data or instruction being transferred"),
    ("mdr_repeat", "So MDR is where the data or instruction is held"),
    ("cir", "Finally, the current instruction register or CIR"),
    ("mix_up", "So, let's separate the two registers"),
    ("mar_holds", "The Mar holds an address"),
    ("trick", "So a quick memory trick"),
    ("exam_note", "It will help you explain the cycle accurately in an exam"),

    # ------------------------------------------------------- the fetch stage
    ("follow", "Now, let's follow an instruction from memory into the PCPU"),
    ("pc_1000", "Suppose the PC contains the address 1000"),
    ("mem_1000", "That means the next instruction is a stored at memory location 1000"),
    ("copy_mar", "The processor begins the fetch stage by copying the address and the PC into"),
    ("brackets", "So the brackets mean the contents off"),
    ("mar_receives", "So more receives the address currently story in the PC"),
    ("address_bus", "The processor then sends the address 1000 along with the address"),
    ("read_signal", "a read signal to the control"),
    ("memory_finds", "Memory uses that address to find the instruction"),
    ("data_bus", "So the instruction is transferred back to the processor, along with the data bus"),
    ("double_brackets", "So the double bracket means go to the address in the more"),
    # "receives instruction from address 2040" — the instruction ADD 2040
    # came from address 1000. The screen shows where it came from.
    ("mdr_gets", "the MDR receives instruction from address 2040"),
    ("to_cir", "the instruction is then copied from from the MDR to the CIR"),
    ("pc_update", "And then the PC is also updated"),
    ("pc_increment", "We will increase it from"),
    ("pc_note", "The next exact amount added to the PC depends"),
    ("convention", "For this trace, we are using the simple one step convention"),
    ("fetch_done", "So our fetch page stage has brought the instruction from memory into the CIR"),

    # --------------------------------------------------- the sequence once more
    ("once_more", "So let's say the sequence once more"),
    ("s_pc", "The PC holds the address of the next"),
    ("s_mar", "then address is copied to the more"),
    ("s_mdr", "The instruction at the memory address is transferred to the MDR"),
    ("s_cir", "The instruction is copied from MDR to the CIR"),
    ("s_update", "The PC is updated. Now the control unit"),

    # ------------------------------------------------------ decode and execute
    # "CIR now holds address 2040" — it holds the instruction ADD 2040.
    ("cir_holds", "So our CIR now holds address 2040"),
    ("cu_decodes", "The control unit decodes it. That means it identifies the operation"),
    ("operation", "Here the operation is add"),
    # "the operation is associated with address 2040" — it is the OPERAND
    # that is at 2040. He says operand correctly later.
    ("operand", "The operation is associated with address 2040"),
    ("get_value", "The processor must now get the values stored at address"),
    ("mar_2040", "So the added to 040 is placed in the more"),
    ("read_again", "So the processor sends that address to memory with a read signal"),
    ("mdr_7", "and the value of that location is transferred into the DR"),
    ("alu_adds", "The ALU performs the addition"),
    ("acc_result", "The result is placed in a register such as the accumulator"),
    ("two_accesses", "The important point is that fetching the instruction and fetching is data"),
    ("first_access", "So the first access retrieves the instruction"),
    ("second_access", "Another access may retrieve the data that the instruction needs"),
    ("who_does", "The control unit coordinates these steps"),
    ("regs_hold", "The registers hold the value as they move through the processor"),

    # ------------------------------------------------- the example with values
    ("example", "All right, let's trace the whole example"),
    ("assume", "Assume the PC starts"),
    ("given_mem", "Memory location 1000 contains add 2040"),
    ("given_7", "Memory location 2040 contains the value 7"),
    ("given_acc", "The accumulator or ACC contains 12"),
    ("means", "So the instruction means add the value"),
    ("ex_fetch", "Okay, first fetch the instruction"),
    ("ex_mar", "The address 1000 is copied from PC to the more"),
    ("ex_pc", "The PC is updated to 1000"),
    ("ex_mdr", "returns the instruction and add 2040"),
    ("ex_cir", "It is then copied into the CIR"),
    ("ex_decode", "Next, the control unit decodes the instruction"),
    ("ex_identify", "It determines and as the operation and 2040 as the"),
    ("ex_read", "so the processor needs memory location 2040"),
    ("ex_7", "The value is seven is placed in the empty R"),
    ("ex_add", "The ALU has the value to the accumulator which currently contains 12"),
    # "12 plus 7 is 90" in the first transcript; a second pass with a larger
    # model hears nineteen, which is also what he says next. 19 it is.
    ("ex_sum", "12 plus 7 is 90"),
    ("ex_store", "The result is stored back in the accumulator"),
    ("ex_after", "So, after this instruction is executed"),
    ("ex_state", "The accumulator contains 19 and the PC points to the next instruction"),
    ("one_complete", "That is one complete instruction passing through the processor"),

    # ------------------------------------------------------------- the buses
    ("buses", "Okay, so how do the buses help"),
    ("buses_routes", "The buses provide the routes for those transfers"),
    ("addr_bus", "the address bus carries an address from the processor"),
    ("addr_oneway", "It is normally one way from the processor"),
    ("data_bus_role", "The data bus carries instructions and data"),
    ("data_bidir", "It is bidirectional because information can move to the processor"),
    ("ctrl_bus", "And the control bus carries control signals"),
    ("ctrl_examples", "Example include like read, write, clock, and interrupt signals"),
    ("in_example", "So in our example, the address bus carried 1000 to memory"),
    ("ctrl_read", "the control bus carried the read signal"),
    ("data_back", "The data bus carried the instruction back to the"),
    ("operand_trip", "For the operand the address bus carried to 040"),
    ("roles", "Keep the roles listed"),
    ("where_what", "address bus, where to access and data bus what is being transferred"),
    ("ctrl_what", "Control bus, what action should happen"),

    # --------------------------------------------------- AS Level: more registers
    ("as_level", "For AS level, you may encounter additional registers"),
    ("acc", "The accumulator or ACC stores intermediate results"),
    ("ix", "The index register or Ix can hold an offset"),
    ("status", "A status register holds flags about the result of an operation"),
    ("flags", "For example, a zero flag may indicate that the result is zero"),
    ("no_change", "These registers do not change"),
    ("more_places", "they give the processor more places to hold"),

    # ------------------------------------------- register-transfer notation
    ("rtn", "now when you see register transfer notation follow the movement one step at a time"),
    ("rtn_1", "For example, more to PC means copy the contents of the PC"),
    ("rtn_2", "More to more in double brackets means read the contents of the memory location"),
    ("rtn_3", "CIR to MDR means copy the instruction from MDR into the CIR"),
    ("rtn_vary", "that exact notation can vary between questions"),

    # ----------------------------------------------------- student challenge
    ("challenge", "Okay, pause the video after I show you the starting stage"),
    ("ch_predict", "then try to predict the accumulator after the instruction executes"),
    ("ch_given", "the PC contains 300"),
    ("ch_mem", "memory location 300 condense add 700"),
    ("ch_700", "memory location 700 condense"),
    # "the accumulator restarts at night" — it starts at nine, which the
    # answer of fifteen requires.
    ("ch_acc", "so the accumulator restarts at night"),
    ("ch_pause", "Now pause, now, and work it through"),
    ("ch_answer", "So the instruction at address 300 is fetched into the CLR"),
    ("ch_pc", "The BC is updated to 301"),
    ("ch_decode", "The control unit decodes add 700"),
    ("ch_read", "The processor reads the value at address 700, which is 6"),
    ("ch_add", "The ALU adds 6 to the original accumulator value"),
    ("ch_15", "the result is 15"),
    ("ch_check", "If you got 15, you follow the instruction correctly"),
    ("ch_else", "If not, you know, replay the trace"),

    # ------------------------------------------------- mistakes, then the recap
    ("mistakes", "All right, here are some of the mistakes"),
    ("three_common", "Here there are three common mistakes"),
    ("all_the_time", "students make these these mistakes all the time"),
    ("m1", "First don't say that more in stores instruction"),
    ("m1_right", "is it stores the address being access"),
    ("m2", "Second, don't say that the MDR stores the address"),
    ("m2_right", "it stores the data or instruction being transferred"),
    ("m3", "Third, don't skip the decode stage"),
    ("m3_right", "The control unit must interpret the instruction before the processor"),
    ("recap", "Here's how the whole cycle and one quick recap"),
    ("r_pc", "The PC stores the address of the next instruction"),
    ("r_mar", "That address is copied to the more"),
    ("r_mdr", "The instruction is read from memory into the MDR"),
    ("r_pc_up", "The PC is updated. The control unit decodes the instruction"),
    ("r_execute", "the CP executes, executes it using the ALU and registers as needed"),
    ("r_repeat", "The processor repeats the cycle"),
]

NOTE = ("Shared O Level 2210 / AS Level 9618 lesson on the "
        "fetch-decode-execute cycle. The take starts at the plan's 0:45 "
        "and ends on the shared recap; beats placed by anchor phrase, see "
        "build/beats_cpu01.py.")

if __name__ == "__main__":
    build("CPU01-fetch-decode-execute", "concept.cpu_cycle", BEATS,
          "CPU01-fetch-decode-execute", NOTE)
