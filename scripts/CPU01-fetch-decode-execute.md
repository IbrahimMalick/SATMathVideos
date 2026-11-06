---
scene: concept.cpu_cycle
---

<!-- Shared O Level 2210 / AS Level 9618 lesson on the fetch-decode-execute cycle. The take starts at the plan's 0:45 and ends on the shared recap; beats placed by anchor phrase, see build/beats_cpu01.py. -->

[[beat:open]] All right, so let's start with a simple question, okay?
[[beat:question]] When you click run, how does the computer turn a program into
actions, all right? [[beat:think]] Think about that, right? When you run, when you
click run, how does the computer turn a program into actions, all right? And so
[[beat:not_magic]] the processor does not read a whole program, right? And understand
it all at once and then magically produces the result. It doesn't, that's not how
computer works, right? [[beat:sequence]] It works through instructions in an organized
sequences. [[beat:for_each]] For each instruction, the processor finds it in memory,
brings it into the CPU, works out what it means and carries it out, right?
[[beat:then_next]] Then it moves it to the next instruction. [[beat:named]] That
repeating process is called the fetch decode execute cycle, right? [[beat:alias]] Some
books call it the fetch execute cycle, but the idea is the same. Okay, fetch an
instruction decoded and executed. [[beat:today]] So today we'll make that process
visible. [[beat:agenda]] We'll name the important CPU components, trace the
instruction through the registers, and see how the buses connect the processors can
memory. [[beat:stored]] So to understand the cycle, we need one key idea. the stored
program concept, a stored program concept, [[beat:program_is]] a program consists of
instructions. [[beat:in_memory]] Those instructions are stored in memory along with
the data the program uses. [[beat:retrieves]] The processor retrieves instructions
from memory as it needs them. [[beat:von_neumann]] So in the one Newman model
instructions and data share the same main memory. [[beat:buses_intro]] The processor
communicates with memory and input output devices through the buses. [[beat:system]]
So let's draw the basic system. [[beat:inside]] Inside the CPU, we'll focus on the
control unit, the arithmetic logic unit, and instead of a small fastest storage
location squad registers. [[beat:cu]] The control unit or CU coordinates the CPU's
activity. [[beat:cu_role]] It interprets instructions and sends control signals.
[[beat:alu]] The arithmetic logic unit, or ALU, performs arithmetic operations such as
addition [[beat:alu_logic]] and logical operations, such as AND or comparations, all
right? [[beat:regs_role]] Registers, hold the addresses, instructions, and the data,
and data the CPU is currently working with. [[beat:regs_small]] There are much smaller
than main memory, right? [[beat:regs_direct]] but they are directly available to the
processor. [[beat:four_regs]] So now let's meet four registers that are central to the
cycle. [[beat:pc]] First is the program controller or PC [[beat:pc_role]] the PC
stores the address of next instruction the processor should fetch It's only a storing
the Address, right [[beat:pc_bookmark]] think of it as a process is bookmark in the
program [[beat:mar]] Next is the memory address register or more right the more
[[beat:mar_role]] Stores the address of the memory location currently being accessed
[[beat:mar_example]] So if the CPU wants to read an instruction from, say, address
1000, right, that address is placed in the more. [[beat:mdr]] Then we have memory data
register or MDR. [[beat:mdr_role]] This is where we hold the data or instruction being
transferred to or or from memory. [[beat:mdr_repeat]] So MDR is where the data or
instruction is held, right? Mar is where the address of the memory location correctly
being used. And in the MDR holds the data or instruction being transferred from the
memory. [[beat:cir]] Finally, the current instruction register or CIR holds the
instruction that the processor is currently decoding or executing. [[beat:mix_up]] So,
let's separate the two registers. There are students often mix up, Mar and MDR.
[[beat:mar_holds]] The Mar holds an address, the MDR holds a data or instruction that
is transferred. [[beat:trick]] So a quick memory trick, A in more for address, D in
MDR is for data, okay? So keep the distinction in mind. [[beat:exam_note]] It will
help you explain the cycle accurately in an exam, all right? [[beat:follow]] Now,
let's follow an instruction from memory into the PCPU. [[beat:pc_1000]] Suppose the PC
contains the address 1000. [[beat:mem_1000]] That means the next instruction is a
stored at memory location 1000. [[beat:copy_mar]] The processor begins the fetch stage
by copying the address and the PC into the more into the more right. [[beat:brackets]]
So the brackets mean the contents off okay the contents off. [[beat:mar_receives]] So
more receives the address currently story in the PC. [[beat:address_bus]] The
processor then sends the address 1000 along with the address address bus to memory it
also sends a you know [[beat:read_signal]] a read signal to the control of us.
[[beat:memory_finds]] Memory uses that address to find the instruction is stored at
location 1000, right? [[beat:data_bus]] So the instruction is transferred back to the
processor, along with the data bus and placed in the MDR. [[beat:double_brackets]] So
the double bracket means go to the address in the more, then read the contents of that
memory location. So in our example, [[beat:mdr_gets]] the MDR receives instruction
from address 2040, Okay, [[beat:to_cir]] the instruction is then copied from from the
MDR to the CIR. [[beat:pc_update]] And then the PC is also updated, and so it points
to the next instruction. It is simplified example, right? [[beat:pc_increment]] We
will increase it from 1 ,000 to 1 ,000, 1 ,000. [[beat:pc_note]] The next exact amount
added to the PC depends on how the computer represents instruction addresses.
[[beat:convention]] For this trace, we are using the simple one step convention shown
in the book, right? [[beat:fetch_done]] So our fetch page stage has brought the
instruction from memory into the CIR, and the PC is ready to point to the next
instruction. [[beat:once_more]] So let's say the sequence once more, right?
[[beat:s_pc]] The PC holds the address of the next instruction, [[beat:s_mar]] then
address is copied to the more. [[beat:s_mdr]] The instruction at the memory address is
transferred to the MDR. [[beat:s_cir]] The instruction is copied from MDR to the CIR.
[[beat:s_update]] The PC is updated. Now the control unit can decode the instruction.
[[beat:cir_holds]] So our CIR now holds address 2040, right? [[beat:cu_decodes]] The
control unit decodes it. That means it identifies the operation and information needed
to perform it. [[beat:operation]] Here the operation is add, okay? [[beat:operand]]
The operation is associated with address 2040, okay? [[beat:get_value]] The processor
must now get the values stored at address 2040. [[beat:mar_2040]] So the added to 040
is placed in the more. Making sense? Yeah. [[beat:read_again]] So the processor sends
that address to memory with a read signal [[beat:mdr_7]] and the value of that
location is transferred into the DR. Excuse me. [[beat:alu_adds]] The ALU performs the
addition, okay. [[beat:acc_result]] The result is placed in a register such as the
accumulator. [[beat:two_accesses]] The important point is that fetching the
instruction and fetching is data can involve separate memory access.
[[beat:first_access]] So the first access retrieves the instruction.
[[beat:second_access]] Another access may retrieve the data that the instruction
needs. [[beat:who_does]] The control unit coordinates these steps. Now and the LLU
performs the arithmetic. [[beat:regs_hold]] The registers hold the value as they move
through the processor. [[beat:example]] All right, let's trace the whole example,
okay, with actual values. [[beat:assume]] Assume the PC starts at 1000.
[[beat:given_mem]] Memory location 1000 contains add 2040. [[beat:given_7]] Memory
location 2040 contains the value 7, all right. [[beat:given_acc]] The accumulator or
ACC contains 12. [[beat:means]] So the instruction means add the value stay stored at
address 2040 to the content value in the accumulator. [[beat:ex_fetch]] Okay, first
fetch the instruction, right? [[beat:ex_mar]] The address 1000 is copied from PC to
the more. [[beat:ex_pc]] The PC is updated to 1000. One memory [[beat:ex_mdr]] returns
the instruction and add 2040 to the MDR. [[beat:ex_cir]] It is then copied into the
CIR. [[beat:ex_decode]] Next, the control unit decodes the instruction.
[[beat:ex_identify]] It determines and as the operation and 2040 as the address of
the, you know, as the address of the operator. Okay, [[beat:ex_read]] so the processor
needs memory location 2040. [[beat:ex_7]] The value is seven is placed in the empty R.
[[beat:ex_add]] The ALU has the value to the accumulator which currently contains 12,
okay. [[beat:ex_sum]] 12 plus 7 is 90. [[beat:ex_store]] The result is stored back in
the accumulator, okay. [[beat:ex_after]] So, after this instruction is executed,
[[beat:ex_state]] The accumulator contains 19 and the PC points to the next
instruction at 1 ,001. [[beat:one_complete]] That is one complete instruction passing
through the processor. [[beat:buses]] Okay, so how do the buses help, right? We have
talked about addresses, instructions, data and control signals moving between CPU and
memory. [[beat:buses_routes]] The buses provide the routes for those transfers. So the
data, [[beat:addr_bus]] the address bus carries an address from the processor to a
memory or another component. [[beat:addr_oneway]] It is normally one way from the
processor when the processor is requesting a location, okay? [[beat:data_bus_role]]
The data bus carries instructions and data [[beat:data_bidir]] It is bidirectional
because information can move to the processor or away from it, right?
[[beat:ctrl_bus]] And the control bus carries control signals [[beat:ctrl_examples]]
Example include like read, write, clock, and interrupt signals [[beat:in_example]] So
in our example, the address bus carried 1000 to memory, right? [[beat:ctrl_read]] the
control bus carried the read signal, right? [[beat:data_back]] The data bus carried
the instruction back to the CPU. [[beat:operand_trip]] For the operand the address bus
carried to 040, okay, the control bus again indicated a read and the data bus carried
the value 7 back to the processor, right? [[beat:roles]] Keep the roles listed, okay,
[[beat:where_what]] address bus, where to access and data bus what is being
transferred. [[beat:ctrl_what]] Control bus, what action should happen. Okay.
[[beat:as_level]] For AS level, you may encounter additional registers and more
detailed registered transfer notation. Okay. [[beat:acc]] The accumulator or ACC
stores intermediate results from arithmetic and logic operations. We used it in our
addition example. Okay. [[beat:ix]] The index register or Ix can hold an offset used
when accessing data in an array or sequence. [[beat:status]] A status register holds
flags about the result of an operation. [[beat:flags]] For example, a zero flag may
indicate that the result is zero right while carry on overflow flags record the
conditions [[beat:no_change]] These registers do not change the basic cycle. Okay,
[[beat:more_places]] they give the processor more places to hold Okay, the values
needed to carry out instructions right [[beat:rtn]] now when you see register transfer
notation follow the movement one step at a time don't skip directly to the final
result. [[beat:rtn_1]] For example, more to PC means copy the contents of the PC into
the more, right? [[beat:rtn_2]] More to more in double brackets means read the
contents of the memory location where address is stored in the more, then place that
data into the MDR. [[beat:rtn_3]] CIR to MDR means copy the instruction from MDR into
the CIR. Okay, [[beat:rtn_vary]] that exact notation can vary between questions. Okay,
so follow the convention used in that question in your course. All right, you're
trying. [[beat:challenge]] Okay, pause the video after I show you the starting stage,
[[beat:ch_predict]] then try to predict the accumulator after the instruction
executes. All right, [[beat:ch_given]] the PC contains 300. [[beat:ch_mem]] memory
location 300 condense add 700 [[beat:ch_700]] memory location 700 condense 6
[[beat:ch_acc]] so the accumulator restarts at night [[beat:ch_pause]] Now pause, now,
and work it through. I hear back. Okay. [[beat:ch_answer]] So the instruction at
address 300 is fetched into the CLR. [[beat:ch_pc]] The BC is updated to 301 in our
simplified example. [[beat:ch_decode]] The control unit decodes add 700.
[[beat:ch_read]] The processor reads the value at address 700, which is 6.
[[beat:ch_add]] The ALU adds 6 to the original accumulator value. of 9, [[beat:ch_15]]
the result is 15. So the accumulator now contains 15. [[beat:ch_check]] If you got 15,
you follow the instruction correctly. [[beat:ch_else]] If not, you know, replay the
trace and keep the rolls of the PC, more MDR and CIR are separate. [[beat:mistakes]]
All right, here are some of the mistakes to avoid, okay? Before we finish here, right
there. [[beat:three_common]] Here there are three common mistakes or what and I see
that is see that happen all the time. Very small [[beat:all_the_time]] students make
these these mistakes all the time right so don't don't don't be disappointed if you're
making them. [[beat:m1]] First don't say that more in stores instruction
[[beat:m1_right]] is it stores the address being access, okay? [[beat:m2]] Second,
don't say that the MDR stores the address, [[beat:m2_right]] it stores the data or
instruction being transferred. [[beat:m3]] Third, don't skip the decode stage array.
[[beat:m3_right]] The control unit must interpret the instruction before the processor
can carry it out. [[beat:recap]] Here's how the whole cycle and one quick recap, okay?
[[beat:r_pc]] The PC stores the address of the next instruction. [[beat:r_mar]] That
address is copied to the more. [[beat:r_mdr]] The instruction is read from memory into
the MDR then copied into the CER. [[beat:r_pc_up]] The PC is updated. The control unit
decodes the instruction. [[beat:r_execute]] the CP executes, executes it using the ALU
and registers as needed, right? [[beat:r_repeat]] The processor repeats the cycle for
the next instruction.
