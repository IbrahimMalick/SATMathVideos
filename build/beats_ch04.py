"""Beat placement for Chapter 4, Software — Cambridge O Level 2210.

Run from the repo root:

    python build/beats_ch04.py

The audio the pipeline reads is made from the upload by one command. The
recorder was running for twenty-three seconds before the lecture started
and for seven after it ended:

    ffmpeg -ss 22.7 -to 1430.5 -i audio/CH04-software-raw.m4a \\
        -c:a aac -b:a 96k audio/CH04-software.m4a

    python build/transcribe.py audio/CH04-software-raw.m4a \\
        --model small --language en

Transcribed before the trim, then every timestamp shifted by the 22.7
seconds the trim removed. That is exact rather than a shortcut: the
trimmed audio is the same samples moved along the clock, so subtracting a
constant is the whole of the correction. It saves re-running the model on
the same twenty-four minutes.

This transcript came back clean -- ``build/repair_loops.find_loops``
reports no loops at all, where the Urdu chapter had eleven. English
narration at a steady pace is simply a much easier thing to decode, and
no repair step was needed here.

One stretch looks like a loop and is not. At 660-672 the transcript has

    "A low language program is closer to the instructions understood by
     the processor. It can offer precise control to the instructions
     understood by the processor. It can offer precise controls over
     hardware ..."

Re-transcribing those thirty seconds on their own gives back the same
repeat, so this is the lecturer restarting a sentence, not the decoder
sticking. The check matters because the two are indistinguishable in the
transcript and opposite in what they require: a loop must be repaired
before a single anchor is placed, and a stumble must be left exactly
alone. ``low_control`` therefore anchors on the second, finished version
of the sentence, so the figure lights as he says the words he meant.

Anchors are copied from the transcript as it came out, mis-hearings and
all, never from the written script: "minomics" is mnemonics, "exclude a
runtime environment" is include, "switched off" is switched on, and
"compiler programs" is compiled programs. A phrase corrected to the
script would not be in the audio, and would either fail to match or --
far worse -- match somewhere else.
"""

from mkbeats import build

BEATS = [
    # ------------------------------------------------------- 1. opening
    ("open", "welcome to chapter 4 of Cambridge"),
    ("hardware", "a computer contains physical components"),
    ("needs_instructions", "But hardware alone cannot perform useful tasks"),
    ("provided_by", "those instructions are provided by the software"),
    ("switch_on", "Think about switching on a computer"),
    ("before_browser", "before you can open a browser, write a document or play"),
    ("must_start", "the computer must start up and organize"),
    ("makes_possible", "Software makes that possible"),
    ("agenda_sysapp", "we will distinguish system or a system software"),
    ("agenda_os", "explore the operating system"),
    ("agenda_interrupt", "follow what happens when an interrupt occurs"),
    ("agenda_lang", "compare programming languages, translators, and the tools"),
    ("focus", "focus on the purpose of each type"),

    # -------------------------------- 2. system against application software
    ("two_categories", "software is commonly divided into two categories"),
    ("sys_defn", "System software provides services required by the computer"),
    ("sys_helps", "It helps the computer operate, manages resources"),
    ("sys_examples", "for example, operating system, right? Device drivers"),
    ("app_defn", "Applications software provides services to the user"),
    ("app_word", "Microsoft Word helps you create documents"),
    ("app_browser", "A web browser, Google Chrome, Firefox"),
    ("app_db", "A database application stores and organizes information"),
    ("app_game", "A game provides entertainment"),
    ("purpose_not_person", "the distinction is based on purpose, not simply"),
    ("utility_case", "a user may open a utility program to backup files"),
    ("even_though", "Even though the user opens it directly"),
    ("therefore_system", "Therefore, it is a system software"),
    ("exam_rule_1", "When answering an exam question, explain what the software does"),

    # ------------------------------------------- 3. the operating system as link
    ("os_central", "The operating system is the central part"),
    ("os_link", "It acts as a link between application programs"),
    ("suppose_save", "Suppose a word processor needs to save a document"),
    ("app_requests", "The application requests a service from the operating system"),
    ("os_manages", "system manages the request and uses the appropriate hardware"),
    ("no_direct", "not need to control every hardware directly"),
    ("no_tech_detail", "without needing to know the technical details"),
    ("coordinates", "operating system also coordinates the processor, memory, files"),
    ("appear_same_time", "several programs may appear to run at the same time"),
    ("resource_manager", "Think of operating system as a resource manager"),

    # ------------------------------------- 4. the functions, one at a time
    ("functions_open", "Let's examine the operating systems main function"),
    ("fn_file", "First, file management"),
    ("file_detail", "It assigns names, stores files"),
    ("file_access", "control who is allowed to access them"),
    ("fn_memory", "Second is memory management"),
    ("ram_alloc", "allocates a space in random access memory or RAM"),
    ("virtual_memory", "It also manages virtual memory"),
    ("vm_detail", "use part of secondary storage when RAM is not sufficient"),
    ("fn_multitask", "Third is multitasking"),
    ("mt_detail", "processor time and other resources among processes"),
    ("mt_switch", "It switches between tasks so that users can work"),
    ("fn_peripheral", "fourth, peripheral management"),
    ("drivers_help", "devices usually with the help of device drivers"),
    ("driver_defn", "A driver provides"),
    ("and_more", "operating system also provides a user interface"),
    ("exam_rule_2", "avoid writing only the operating system manages the computer"),
    ("name_a_function", "explain what it manages"),

    # ----------------------------------------------- 5. what happens at start-up
    ("startup_open", "let's trace what happens when a computer starts"),
    ("base_hardware", "At the base of system is the"),
    ("firmware_first", "firmware stored in the non -volatile memory runs"),
    ("firmware_defn", "Firmware software stored in hardware"),
    ("firmware_tasks", "it performs a startup task, tests, and initializes the hardware"),
    ("begins_boot", "then begins the boot process"),
    ("starts_bootloader", "The firmware starts the boot loader"),
    ("bootloader_job", "job is to locate and load the operating system"),
    ("into_ram", "or into RAM"),
    ("os_takes_control", "Once loaded, the operating system takes control"),
    ("app_can_run", "an application can run"),
    ("app_uses_services", "It uses operating system services to require access"),
    ("order_matters", "Look, this order matters"),
    ("order_recap", "Firmware starts the system, bootloader loads the operating system"),
    ("request_down", "An application will usually request a device service"),
    ("driver_to_hw", "can then use a driver to communicate with the hardware"),

    # ---------------------------------------------------- 6. what an interrupt is
    ("interrupt_open", "so what is an interrupt"),
    ("interrupt_defn", "An interrupt is a signal or event that requires"),
    ("why_needed", "what do computers need interest for"),
    ("polling", "Imagine if the processor had to repeatedly ask every device"),
    ("waste", "That constant checking would waste processor time"),
    ("instead_signal", "Instead, a device or a program can generate an interrupt"),
    ("deal_with_event", "The processor can then deal with the event"),
    ("hw_interrupt", "A hardware interrupt comes from a hardware device"),
    ("hw_examples", "like a key press, a"),
    ("hw_more", "data arriving through a network connection, or a printer finishing"),
    ("sw_interrupt", "A software interrupt is"),
    ("sw_error", "a program might cause an error such as division by zero"),
    ("sw_request", "it might request a service"),
    ("isr_intro", "responds by running a suitable interrupt service routine"),
    ("isr_contains", "The routine contains instruction for dealing with that particular"),

    # ----------------------------------------- 7. the five steps, in order
    ("steps_open", "Let's follow the steps in interrupt handling"),
    ("step_generated", "First, an"),
    ("step_finish", "The processor finishes the instruction"),
    ("not_abandon", "It does not normally abandon an instruction halfway through"),
    ("step_save", "the processor saves the state of the current process"),
    ("state_contains", "This state includes information needed to continue the program later"),
    ("state_detail", "current position in the program and the relevant processor data"),
    ("priorities", "If more than one interrupt is waiting"),
    ("step_isr", "loads and executes the appropriate interrupt service"),
    ("isr_deals", "The routine deals with the event"),
    ("cleared", "the interrupt is cleared"),
    ("step_restore", "The saved state of the original process is restored"),
    ("step_resume", "the processor resumes the interrupted program"),
    ("sequence_open", "Remember the sequence"),
    ("seq_1", "Finish the instructions"),
    ("seq_2", "Save the state"),
    ("seq_3", "Handle the interrupt"),
    ("seq_4", "Restore the state"),
    ("seq_5", "Resume the program"),
    ("not_discarded", "The original program is not discarded"),
    ("correct_point", "allows it to continue from the content point"),

    # ------------------------------------------- 8. high level against low level
    ("lang_open", "programmers use programming languages to write instructions"),
    ("how_close", "These languages differ in how close they are"),
    ("high_level", "A high level language, uses the statements and structures"),
    ("high_easy", "makes programs easy to write, debug and maintain"),
    ("high_portable", "programs are usually more portable between different"),
    ("still_translated", "they still need to be translated before a processor can execute"),
    ("low_level", "A low language program is closer to the instructions"),
    # The second, finished version of the restarted sentence -- see the
    # note at the top of this file.
    ("low_control", "offer precise controls over hardware"),
    ("low_timing", "can be useful when timing or efficiency is important"),
    ("low_harder", "However, low level code is often harder"),
    ("low_dependent", "It is also more processor dependent"),
    ("choose_open", "If a question asks you to choose a language"),
    ("choose_high", "may be suitable when readability, portability and faster development"),
    ("choose_low", "may be suitable when direct hardware control or precise timing"),

    # --------------------------------- 9. machine code, assembly, the assembler
    ("machine_open", "Let's talk about machine code"),
    ("machine_defn", "Machine code consists of binary instructions"),
    ("binary_hard", "Writing a complete program as binary would be difficult"),
    ("assembly_easier", "Assembly language makes this easier by using minomics"),
    ("mnemonic_defn", "A minomic is a short word"),
    ("mnemonic_eg", "such as an instruction to add or move data"),
    ("symbolic", "Assembly language can also use symbolic addresses"),
    ("not_raw", "write every address as a raw number"),
    ("not_executed", "the processor does not directly execute this assembly"),
    ("must_translate", "They must first be translated into machine code"),
    ("assembler", "An assembler performs this translation"),
    ("assembler_detail", "It converts assembly language instructions into machine code"),
    ("processor_specific", "the resulting machine code is processor -specific"),
    ("not_portable", "assembler does not turn assembly language into a portable"),

    # ----------------------------------------------------------- 10. the compiler
    ("compiler_open", "Let's talk about compiler"),
    ("compiler_defn", "A compiler translates a"),
    ("writes_source", "The programmer writes source code"),
    ("checks_translates", "The compiler checks and translates the code"),
    ("errors_found", "If errors are found during the compilation"),
    ("run_without", "the program can be run without translating every line again"),
    ("execute_quickly", "this is one reason compiler programs"),
    ("compiler_useful", "Compilers are useful when a program is finished"),
    ("cannot_guarantee", "a compiler cannot guarantee that the program solves the right problem"),
    ("syntax_errors", "It can detect syntax errors"),
    ("logic_wrong", "a program might still run incorrectly because its algorithm"),
    ("wrong_formula", "calculate a total using the wrong formula"),
    ("wont_reveal", "compilation alone will not necessarily"),

    # -------------------------------------------------------- 11. the interpreter
    ("interp_open", "An interpreter translates and executes a program one line"),
    ("reads_translates", "It reads the statement, translates it, and executes it"),
    ("next_statement", "Then it moves to the next statement"),
    ("stops_at_error", "If it reaches an error, it stops at that point"),
    ("no_executable", "an interpreter normally does not produce a separate executable file"),
    ("as_it_runs", "Translation happens"),
    ("useful_dev", "This can be useful when you are developing and testing"),
    ("change_and_test", "the programmer can make a change and test the code again"),
    ("tradeoff", "is that the translation happens during execution"),
    ("slower", "an interpreted program may run more slowly"),
    ("scenario_interp", "If it describes interactive development and quick testing"),
    ("scenario_compile", "If it describes a"),

    # ------------------------------------------- 12. the comparison, side by side
    ("compare_open", "Let's compare compilers and interpreters directly"),
    ("cmp_when", "Compiler translates the whole program before execution"),
    ("cmp_when_i", "An interpreter translator translates and executes the program one line"),
    ("cmp_output", "A compiler usually produces an executable file"),
    ("cmp_output_i", "interpreter normally does not produce a separate executable in the same"),
    ("cmp_errors", "A compiler reports errors after attempting to compile"),
    ("cmp_errors_i", "interpreter stops when it reaches an error during the execution"),
    ("cmp_speed", "complied code run quickly because"),
    ("cmp_speed_i", "Interpreted code may run more slowly because translation happens"),
    ("cmp_use_i", "interpreters are often useful during development and testing"),
    ("cmp_use_c", "Compilers are often useful when a completed program needs to be distributed"),
    ("exam_compare", "do not describe one method and leave the other"),
    ("same_feature", "Compare the same feature on both sides"),

    # ------------------------------------------------------------------- 13. IDE
    ("ide_open", "let's talk about an integrated development environment"),
    ("ide_combines", "combines tools that help a programmer create and test software"),
    ("ide_editor", "a code editor is used"),
    ("ide_highlight", "Many editors also highlight"),
    ("ide_translator", "The IDE may include a translator"),
    ("ide_runtime", "It may also exclude a runtime environment"),
    ("ide_diagnostics", "Error diagnostics identify errors and can point to the location"),
    ("ide_helps", "this helps a programmer investigate and correct faults"),
    ("ide_autocomplete", "Auto -completion suggests"),
    ("ide_autocorrect", "auto -correction can fix common syntax"),
    ("ide_pretty", "Pretty printing improves the appearance of code"),
    ("ide_colour", "Some systems use color to distinguish"),
    ("exam_ide", "When explaining an IDE feature in an exam"),
    ("too_general", "IDE makes programming easier"),

    # ------------------------------------------------ 14. one example, all of it
    ("together_open", "let's bring these ideas together"),
    ("sensor_scene", "Imagine a programmer creating an application for a device"),
    ("ide_provides", "IDE provides a code editor, a translator, and a run environment"),
    ("interp_linebyline", "If an interpreter is used, the programmer"),
    ("diag_help", "error diagnostic can"),
    ("needs_timing", "If the device needs precise timing or direct control"),
    ("choose_low2", "the programmer might"),
    ("assembler2", "If assembly language is used, an assembler translates the mnemonic"),
    ("not_alone", "it does not usually control the sensor on its own"),
    ("through_os", "It requires access through the operating system"),
    ("driver_sensor", "uses the appropriate device driver to communicate with the sensor"),
    ("connects_all", "this example connects"),

    # ---------------------------------------------------------------- 15. recap
    ("recap_open", "let's recap"),
    ("recap_sys", "a system software provides"),
    ("recap_app", "Application software provides services for the user"),
    ("recap_os", "The operating system manages files, memory, processor time"),
    ("recap_services", "It also provides services that application can request"),
    ("recap_boot", "firmware initializes the hardware and"),
    ("recap_loader", "The bootloader loads the operating system into RAM"),
    ("recap_os_runs", "The operating system that manages resources and supports applications"),
    ("recap_interrupt", "interrupt signals that the processor needs to respond to an event"),
    ("recap_steps", "The processor finishes its current instruction, saves the process state"),
    ("recap_restore", "restores the saved state, and resumes the original program"),
    ("recap_high", "high -level languages are generally easy"),
    ("recap_low", "languages work closer to the hardware"),
    ("recap_assembler", "An assembler translates assembly language into machine"),
    ("recap_compiler", "a compiler translates the whole program before execution"),
    ("recap_interp", "interpreter translates and executes code one line"),
    ("recap_ide", "IDE combines tools such as code editor, translator, runtime environment"),
    ("pause", "pause here and try to explain each comparison"),
    ("close", "Clear definition and precise comparisons are the key"),
    ("see_you", "I'll see you in"),
]

if __name__ == "__main__":
    build("CH04-software", "cs.software", BEATS, "CH04-software",
          "Cambridge O Level 2210 Chapter 4: Software. Captions in English; "
          "every beat anchored to the recording as delivered.")
