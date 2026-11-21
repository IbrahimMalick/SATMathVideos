---
scene: cs.software
---

<!-- Cambridge O Level 2210 Chapter 4: Software. Captions in English; every beat anchored to the recording as delivered. -->

All right guys, [[beat:open]] welcome to chapter 4 of Cambridge O -Level Computer
Science syllabus 2210. Our topic today is software, okay? So [[beat:hardware]] a
computer contains physical components, you know, we discussed a processor, memory
storage and input and output devices. [[beat:needs_instructions]] But hardware alone
cannot perform useful tasks, right? It needs instructions and [[beat:provided_by]]
those instructions are provided by the software. [[beat:switch_on]] Think about
switching on a computer. Before you know, [[beat:before_browser]] before you can open
a browser, write a document or play a game, [[beat:must_start]] the computer must
start up and organize its resources. [[beat:makes_possible]] Software makes that
possible. So in this lesson, [[beat:agenda_sysapp]] we will distinguish system or a
system software from the application software, [[beat:agenda_os]] explore the
operating system, and they start a process, and then [[beat:agenda_interrupt]] follow
what happens when an interrupt occurs. And then we will [[beat:agenda_lang]] compare
programming languages, translators, and the tools inside an integrated development
environment. As you listen, [[beat:focus]] focus on the purpose of each type of
software and how the different parts work together. So, [[beat:two_categories]]
software is commonly divided into two categories, okay? System software and
application software. [[beat:sys_defn]] System software provides services required by
the computer. [[beat:sys_helps]] It helps the computer operate, manages resources, and
support the programs. You know, [[beat:sys_examples]] for example, operating system,
right? Device drivers and utility programs. [[beat:app_defn]] Applications software
provides services to the user. A word processor, for example, [[beat:app_word]]
Microsoft Word helps you create documents, right? [[beat:app_browser]] A web browser,
Google Chrome, Firefox, whatever you use lets you access websites. [[beat:app_db]] A
database application stores and organizes information, right? [[beat:app_game]] A game
provides entertainment. So [[beat:purpose_not_person]] the distinction is based on
purpose, not simply on whether a person interacts with the program. For example,
[[beat:utility_case]] a user may open a utility program to backup files or scan the
malware. [[beat:even_though]] Even though the user opens it directly, its purpose is
to maintain or protect the computer. [[beat:therefore_system]] Therefore, it is a
system software. [[beat:exam_rule_1]] When answering an exam question, explain what
the software does. Like system software supports the computer, application software
helps the user perform a task. [[beat:os_central]] The operating system is the central
part of the system software. [[beat:os_link]] It acts as a link between application
programs and the computer's hardware. [[beat:suppose_save]] Suppose a word processor
needs to save a document. [[beat:app_requests]] The application requests a service
from the operating system. the operating [[beat:os_manages]] system manages the
request and uses the appropriate hardware and driver to store the document. This
arrangement is useful because applications do [[beat:no_direct]] not need to control
every hardware directly, right? Every hardware device directly, right? A word
processor can request that data be saved [[beat:no_tech_detail]] without needing to
know the technical details of the storage device, right? The [[beat:coordinates]]
operating system also coordinates the processor, memory, files, and connected devices.
So [[beat:appear_same_time]] several programs may appear to run at the same time, even
if the processor is sharing its time among them. [[beat:resource_manager]] Think of
operating system as a resource manager. It controls how software and users access the
computer's resources. [[beat:functions_open]] Let's examine the operating systems main
function, okay. [[beat:fn_file]] First, file management. The operating system creates
and organizes files and folders. [[beat:file_detail]] It assigns names, stores files,
you know, retrieves them when needed and [[beat:file_access]] control who is allowed
to access them. [[beat:fn_memory]] Second is memory management, right? The operating
system [[beat:ram_alloc]] allocates a space in random access memory or RAM to programs
and data. [[beat:virtual_memory]] It also manages virtual memory. This allows the
computer to [[beat:vm_detail]] use part of secondary storage when RAM is not
sufficient for the current workload. [[beat:fn_multitask]] Third is multitasking. The
operating system shares [[beat:mt_detail]] processor time and other resources among
processes, right? [[beat:mt_switch]] It switches between tasks so that users can work
with several programs. And then [[beat:fn_peripheral]] fourth, peripheral management.
The operating system controls input and output [[beat:drivers_help]] devices usually
with the help of device drivers, right? [[beat:driver_defn]] A driver provides
instructions that allow operating system to communicate with a particular device. The
[[beat:and_more]] operating system also provides a user interface that you know
manages user accounts and permissions protect system resources handles you know
interrupts and other services that applications can use so when you're for an exam
answer right [[beat:exam_rule_2]] avoid writing only the operating system manages the
computer that's not sufficient right name of function and [[beat:name_a_function]]
explain what it manages okay now let's [[beat:startup_open]] let's trace what happens
when a computer starts. [[beat:base_hardware]] At the base of system is the physical
hardware, the processor, memory, storage, and devices. When the computer is switched
off, [[beat:firmware_first]] firmware stored in the non -volatile memory runs first.
[[beat:firmware_defn]] Firmware software stored in hardware, [[beat:firmware_tasks]]
it performs a startup task, tests, and initializes the hardware and
[[beat:begins_boot]] then begins the boot process. [[beat:starts_bootloader]] The
firmware starts the boot loader. The boot loader's [[beat:bootloader_job]] job is to
locate and load the operating system from the secondary storage [[beat:into_ram]] or
into RAM. [[beat:os_takes_control]] Once loaded, the operating system takes control.
It manages the computer's resources and provides services to applications. And
finally, [[beat:app_can_run]] an application can run, right?
[[beat:app_uses_services]] It uses operating system services to require access to
files, memory, and devices. [[beat:order_matters]] Look, this order matters, okay?
[[beat:order_recap]] Firmware starts the system, bootloader loads the operating
system. The operating system supports the application. [[beat:request_down]] An
application will usually request a device service through the operating system, right?
The operating system [[beat:driver_to_hw]] can then use a driver to communicate with
the hardware. Make sense? Alright, [[beat:interrupt_open]] so what is an interrupt?
[[beat:interrupt_defn]] An interrupt is a signal or event that requires the
processor's attention. You know, [[beat:why_needed]] what do computers need interest
for, right? [[beat:polling]] Imagine if the processor had to repeatedly ask every
device, do you have something for me now? [[beat:waste]] That constant checking would
waste processor time, right? [[beat:instead_signal]] Instead, a device or a program
can generate an interrupt when it needs attention. [[beat:deal_with_event]] The
processor can then deal with the event. [[beat:hw_interrupt]] A hardware interrupt
comes from a hardware device, okay? [[beat:hw_examples]] like a key press, a mouse
movement, [[beat:hw_more]] data arriving through a network connection, or a printer
finishing a task could generate one, okay? [[beat:sw_interrupt]] A software interrupt
is generated by software. For example, [[beat:sw_error]] a program might cause an
error such as division by zero, or [[beat:sw_request]] it might request a service from
the operating system. The processor [[beat:isr_intro]] responds by running a suitable
interrupt service routine, ISR, it's called interrupt service routine. Usually
everybody calls it ISR. [[beat:isr_contains]] The routine contains instruction for
dealing with that particular interrupt. [[beat:steps_open]] Let's follow the steps in
interrupt handling. [[beat:step_generated]] First, an interrupt is generated.
[[beat:step_finish]] The processor finishes the instruction. It is currently
executing. [[beat:not_abandon]] It does not normally abandon an instruction halfway
through. Next, [[beat:step_save]] the processor saves the state of the current
process. [[beat:state_contains]] This state includes information needed to continue
the program later, such as the [[beat:state_detail]] current position in the program
and the relevant processor data. data. [[beat:priorities]] If more than one interrupt
is waiting, the operating system or processor can use priorities to decide which one
to handle first. The processor then hands [[beat:step_isr]] loads and executes the
appropriate interrupt service routine. [[beat:isr_deals]] The routine deals with the
event. For example, it might process data received from a device. After the cause has
been handled, [[beat:cleared]] the interrupt is cleared. [[beat:step_restore]] The
saved state of the original process is restored and [[beat:step_resume]] the processor
resumes the interrupted program. [[beat:sequence_open]] Remember the sequence, okay?
[[beat:seq_1]] Finish the instructions, right? Whatever you're doing. [[beat:seq_2]]
Save the state. [[beat:seq_3]] Handle the interrupt. [[beat:seq_4]] Restore the state.
[[beat:seq_5]] Resume the program. [[beat:not_discarded]] The original program is not
discarded. Saving its state [[beat:correct_point]] allows it to continue from the
content point, from the correct point. So [[beat:lang_open]] programmers use
programming languages to write instructions. [[beat:how_close]] These languages differ
in how close they are to the human language or to the machine instructions used by a
processor. [[beat:high_level]] A high level language, uses the statements and
structures that are easier for people to understand. This generally, you know,
[[beat:high_easy]] makes programs easy to write, debug and maintain. High -level
[[beat:high_portable]] programs are usually more portable between different, you know,
processor types, although [[beat:still_translated]] they still need to be translated
before a processor can execute them, right? [[beat:low_level]] A low language program
is closer to the instructions understood by the processor. It can offer precise
control to the instructions understood by the processor. It can [[beat:low_control]]
offer precise controls over hardware and [[beat:low_timing]] can be useful when timing
or efficiency is important. [[beat:low_harder]] However, low level code is often
harder to write and more difficult to maintain. [[beat:low_dependent]] It is also more
processor dependent. [[beat:choose_open]] If a question asks you to choose a language,
connect your choice to the situation. A high level language [[beat:choose_high]] may
be suitable when readability, portability and faster development matter. right? A low
language [[beat:choose_low]] may be suitable when direct hardware control or precise
timing is required. [[beat:machine_open]] Let's talk about machine code.
[[beat:machine_defn]] Machine code consists of binary instructions that a processor
can execute directly. [[beat:binary_hard]] Writing a complete program as binary would
be difficult. I mean, or for a programmer to read and remember, right?
[[beat:assembly_easier]] Assembly language makes this easier by using minomics, yeah?
[[beat:mnemonic_defn]] A minomic is a short word or code that represents an operation,
[[beat:mnemonic_eg]] such as an instruction to add or move data. [[beat:symbolic]]
Assembly language can also use symbolic addresses instead of requiring the programmer
to [[beat:not_raw]] write every address as a raw number. But [[beat:not_executed]] the
processor does not directly execute this assembly language man is Minovics.
[[beat:must_translate]] They must first be translated into machine code.
[[beat:assembler]] An assembler performs this translation, okay?
[[beat:assembler_detail]] It converts assembly language instructions into machine code
for a particular processor. That last detail matters, okay? For
[[beat:processor_specific]] the resulting machine code is processor -specific, an
[[beat:not_portable]] assembler does not turn assembly language into a portable high
-level program, okay? [[beat:compiler_open]] Let's talk about compiler, okay?
[[beat:compiler_defn]] A compiler translates a whole program before that program is
executed. [[beat:writes_source]] The programmer writes source code,
[[beat:checks_translates]] The compiler checks and translates the code, usually
producing object code or an executable program, right? [[beat:errors_found]] If errors
are found during the compilation, the programmer can correct the source code and
complete it again. After successful compilation, [[beat:run_without]] the program can
be run without translating every line again. So [[beat:execute_quickly]] this is one
reason compiler programs can execute quickly. [[beat:compiler_useful]] Compilers are
useful when a program is finished and needs to be run repeatedly or distributed to
users. However, [[beat:cannot_guarantee]] a compiler cannot guarantee that the program
solves the right problem. [[beat:syntax_errors]] It can detect syntax errors and some
other some often errors, but [[beat:logic_wrong]] a program might still run
incorrectly because its algorithm or logic is wrong. I'll give you an example. Our
program may follow all the rules of the programming language, but
[[beat:wrong_formula]] calculate a total using the wrong formula. So
[[beat:wont_reveal]] compilation alone will not necessarily reveal that mistake.
[[beat:interp_open]] An interpreter translates and executes a program one line or a
statement at a time. [[beat:reads_translates]] It reads the statement, translates it,
and executes it. [[beat:next_statement]] Then it moves to the next statement.
[[beat:stops_at_error]] If it reaches an error, it stops at that point and reports the
problem. So [[beat:no_executable]] an interpreter normally does not produce a separate
executable file containing the fully translated program. [[beat:as_it_runs]]
Translation happens as the program runs. [[beat:useful_dev]] This can be useful when
you are developing and testing a program. If the interpreter finds an error,
[[beat:change_and_test]] the programmer can make a change and test the code again.
This trade -off [[beat:tradeoff]] is that the translation happens during execution. As
a result, [[beat:slower]] an interpreted program may run more slowly than an
equivalent program that has already been compiled. Use scenario and the question to
guide your answer. [[beat:scenario_interp]] If it describes interactive development
and quick testing and interpreting may be suitable. [[beat:scenario_compile]] If it
describes a completed program that will run repeatedly, compilation may be more
suitable. [[beat:compare_open]] Let's compare compilers and interpreters directly.
[[beat:cmp_when]] Compiler translates the whole program before execution.
[[beat:cmp_when_i]] An interpreter translator translates and executes the program one
line at a time. [[beat:cmp_output]] A compiler usually produces an executable file and
[[beat:cmp_output_i]] interpreter normally does not produce a separate executable in
the same way. [[beat:cmp_errors]] A compiler reports errors after attempting to
compile the program. And [[beat:cmp_errors_i]] interpreter stops when it reaches an
error during the execution. So [[beat:cmp_speed]] complied code run quickly because,
you know, translation has already taken place. [[beat:cmp_speed_i]] Interpreted code
may run more slowly because translation happens as it turns, as it runs. So
[[beat:cmp_use_i]] interpreters are often useful during development and testing.
[[beat:cmp_use_c]] Compilers are often useful when a completed program needs to be
distributed or run many times. So, in a comparison question, [[beat:exam_compare]] do
not describe one method and leave the other unestated. [[beat:same_feature]] Compare
the same feature on both sides. For example, a compiler translates the whole program
before running it, whereas an interpreter translates and executes one line at a time.
Now, [[beat:ide_open]] let's talk about an integrated development environment or IDE,
right? IDE [[beat:ide_combines]] combines tools that help a programmer create and test
software, you know, [[beat:ide_editor]] a code editor is used, you know, to use to
write and change source code. [[beat:ide_highlight]] Many editors also highlight, you
know, keywords or arrange code so that it is easier to read. [[beat:ide_translator]]
The IDE may include a translator, such as a compiler or interpreter.
[[beat:ide_runtime]] It may also exclude a runtime environment where the programmer
can execute the program and test how it behaves. [[beat:ide_diagnostics]] Error
diagnostics identify errors and can point to the location where a program was found.
And [[beat:ide_helps]] this helps a programmer investigate and correct faults.
[[beat:ide_autocomplete]] Auto -completion suggests, you know, identifiers or paths of
a statement while the programmer types and [[beat:ide_autocorrect]] auto -correction
can fix common syntax or formatting mistakes. [[beat:ide_pretty]] Pretty printing
improves the appearance of code by applying consistent indentation and formatting.
[[beat:ide_colour]] Some systems use color to distinguish parts of code.
[[beat:exam_ide]] When explaining an IDE feature in an exam, name the feature that
describes how it helps. For example, the [[beat:too_general]] IDE makes programming
easier, you know, it's too general to earn full credit, okay? All right,
[[beat:together_open]] let's bring these ideas together, okay? [[beat:sensor_scene]]
Imagine a programmer creating an application for a device that measures temperature
with a sensor. What the programmer is developing the program, right? And
[[beat:ide_provides]] IDE provides a code editor, a translator, and a run environment
for testing. [[beat:interp_linebyline]] If an interpreter is used, the programmer can
work through the code line -by -line and investigate errors as they as they they're
reached, right? Each [[beat:diag_help]] error diagnostic can help identify where a
problem occurred. [[beat:needs_timing]] If the device needs precise timing or direct
control of the sensor? No, [[beat:choose_low2]] the programmer might choose a low
-level language. [[beat:assembler2]] If assembly language is used, an assembler
translates the mnemonic into machine code. When the completed application runs,
[[beat:not_alone]] it does not usually control the sensor on its own.
[[beat:through_os]] It requires access through the operating system. The operating
system manages resources and [[beat:driver_sensor]] uses the appropriate device driver
to communicate with the sensor. And [[beat:connects_all]] this example connects, you
know, language -wise, translation, the IDE, the operating system and the device
driver. All right, [[beat:recap_open]] let's recap, okay? What we talked about.
Because [[beat:recap_sys]] a system software provides services required by the
computer. [[beat:recap_app]] Application software provides services for the user.
[[beat:recap_os]] The operating system manages files, memory, processor time,
peripheral security accounts, interfaces and interrupts. [[beat:recap_services]] It
also provides services that application can request. At a startup, you know,
[[beat:recap_boot]] firmware initializes the hardware and starts the bootloader.
[[beat:recap_loader]] The bootloader loads the operating system into RAM, okay?
[[beat:recap_os_runs]] The operating system that manages resources and supports
applications. And [[beat:recap_interrupt]] interrupt signals that the processor needs
to respond to an event, right? [[beat:recap_steps]] The processor finishes its current
instruction, saves the process state, runs the appropriate interrupt service routine,
[[beat:recap_restore]] restores the saved state, and resumes the original program. So
[[beat:recap_high]] high -level languages are generally easy to read, write, and
maintain. A low -level [[beat:recap_low]] languages work closer to the hardware,
right? [[beat:recap_assembler]] An assembler translates assembly language into machine
code, and [[beat:recap_compiler]] a compiler translates the whole program before
execution. We talked about interpreter and [[beat:recap_interp]] interpreter
translates and executes code one line at a time, And then [[beat:recap_ide]] IDE
combines tools such as code editor, translator, runtime environment and error
diagnostics. So [[beat:pause]] pause here and try to explain each comparison in your
own words. [[beat:close]] Clear definition and precise comparisons are the key to the
strong answer in this chapter. If you're reading the book, try to attempt all the
questions in the end and then [[beat:see_you]] I'll see you in chapter 5. Thank you.
