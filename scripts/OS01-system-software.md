---
scene: cs.system_software
---

<!-- System software, application software and the operating system. Cambridge O Level Computer Science 2210, topic 4.1, syllabus for examination in 2026, 2027 and 2028. ElevenLabs narration; the false start on the title was cut before transcription, see build/beats_os01.py. -->

[[beat:open]] Part 1, system software and application software. [[beat:software_is]]
Software is a collection of programs and instructions that tell a computer what to do.
[[beat:distinguish]] For Cambridge O -level computer science, [[beat:bins]] you must
distinguish between system software and application software. [[beat:sys_def]] System
software provides services required by the computer system. [[beat:sys_eg1]] Examples
include operating systems, [[beat:sys_eg2]] utility software, [[beat:sys_eg3]] device
drivers, [[beat:app_def]] Application Software provides services required by the user.
[[beat:app_eg1]] Examples include Word processors, [[beat:app_eg2]] web browsers,
[[beat:app_eg3]] database software, [[beat:app_eg4]] games, [[beat:app_eg5]]
presentation software, [[beat:app_eg6]] video editing software. [[beat:simplest]] Here
is the simplest way to remember the difference. [[beat:rule_sys]] System software
helps the computer operate. [[beat:rule_app]] Application software helps the user
complete a task, [[beat:antivirus]] consider antivirus software. [[beat:can_open]] A
user can open it and interact with it, [[beat:still_system]] but it is still
classified as system software [[beat:its_role]] because its main role is to maintain
and protect the computer system. [[beat:mistake]] A common mistake is to classify
every program with a visible user interface as application software.
[[beat:incorrect]] That is incorrect software must be classified [[beat:by_purpose]]
according to its purpose, [[beat:not_open]] Not simply according to whether the user
can open it. [[beat:quick_check]] Quick check. [[beat:qc_item]] A student uses
spreadsheet software to calculate monthly expenses. [[beat:qc_ask]] Is the spreadsheet
system software or application software? [[beat:qc_answer]] It is application software
because it helps the user complete a specific task. [[beat:qc2]] Now consider this
cleanup software. [[beat:qc2_what]] It removes unnecessary files and helps maintain
the computer. [[beat:qc2_answer]] This is utility software and is therefore classified
as system software. [[beat:part2]] Part 2. The operating system.
[[beat:most_important]] The operating system is the most important type of system
software. [[beat:manages]] It manages the computer's hardware and software resources
[[beat:platform_intro]] and provides a platform on which application software can run.
[[beat:examples]] Examples include Windows, Mac OS, Linux, Android and iOS.
[[beat:no_memorise]] You do not need to memorize product names for the examination.
[[beat:understand]] You need to understand and what an operating system does.
[[beat:functions]] Let us examine its major functions. [[beat:files]] File management.
[[beat:files_verbs]] The operating system creates names, stores, retrieves, organizers
and protects files. [[beat:files_folders]] It also manages folders and keeps track of
where data is stored. [[beat:files_save]] When you save a file, the application does
not normally decide the exact physical location on the storage device.
[[beat:files_asks]] It asks the operating system to handle the process.
[[beat:files_also]] The operating system can also manage file names, file types, file
permissions, folder structures, access rights. [[beat:files_weak]] In an examination
answer, do not write only the operating system manages files. [[beat:files_stronger]]
For a stronger answer, explain what that means. [[beat:files_strong]] The operating
system creates names, organizes, stores, retrieves, and protects files. [[beat:ui]]
User Interface The operating system provides an interface through which the user can
interact with the computer. [[beat:gui]] A graphical user interface may contain
Windows, icons, menus, buttons, pointers. [[beat:cli]] A command line interface allows
the user to type commands, [[beat:ui_converts]] the user interface converts the user's
actions into instructions that the computer can process. [[beat:periph]] Peripheral
and driver management. [[beat:periph_def]] A peripheral is a hardware device connected
to or used with a computer. [[beat:periph_eg]] Examples include printers, keyboards,
mice, scanners, speakers, storage devices. [[beat:driver_def]] A device driver is
software that allows the operating system to communicate with a particular hardware
device. [[beat:diff_printers]] Different printers may require different drivers
because their internal commands is can be different. [[beat:not_direct]] An
application normally does not communicate directly with the hardware. [[beat:path]]
The typical path is application software, [[beat:path_os]] then the operating system,
[[beat:path_driver]] then the device driver, [[beat:path_hw]] then the hardware
device. [[beat:separation]] This separation makes applications easier to develop
because the application does not need to contain instructions for every possible
hardware model. [[beat:memory]] Memory Management The operating system manages the use
of random access memory or RAM. [[beat:mem_decides]] It decides which program receives
memory, [[beat:mem_how_much]] how much memory is allocated [[beat:mem_where]] where
instructions and data are stored [[beat:mem_release]] when memory can be released and
used by another program. [[beat:mem_protect]] The operating system must also prevent
one process from incorrectly accessing memory allocated to another process.
[[beat:virtual]] If there is not enough physical RAM, the operating system may use
virtual memory. [[beat:virtual_what]] Virtual memory uses part of secondary storage as
if it were additional RAM. [[beat:slower]] However, secondary storage is slower than
RAM. [[beat:excessive]] Therefore, excessive use of virtual memory can reduce
performance. [[beat:mem_exam]] A strong examination answer should mention allocation,
protection or virtual memory. [[beat:mem_weak]] Not simply say that the operating
system controls RAM multitasking. [[beat:multi]] Multi -tasking allows more than one
process to appear to run at the same time. [[beat:process_def]] A process is a program
that is currently being executed. [[beat:single_core]] On a single processor core, the
operating system switches rapidly between processes [[beat:allocates]] and it
allocates a small amount of processor time to each process. [[beat:impression]] This
can create the impression that the programs are running simultaneously.
[[beat:multi_eg]] For example, you may stream music, download a file, edit a document,
receive notifications. [[beat:share]] The operating system must share processor time,
memory and other resources between these processes. See, [[beat:security]] security
management, the operating system helps protect the computer and its resources.
[[beat:sec_list]] It can authenticate users and force passwords, control access
permissions, restrict access to files, protect system resources, maintain separate
user accounts. [[beat:sec_not_all]] Security does not mean that the operating system
prevents every possible attack. [[beat:sec_mechanisms]] It means that it provides
mechanisms for controlling and protecting access. [[beat:accounts]] User account
management. [[beat:acct_maintain]] The operating system can maintain different user
accounts. [[beat:acct_each]] Each account may have its own, user name, password,
permissions, files, settings, preferences, [[beat:admin]] and administrator account
normally has greater control than a standard user account. [[beat:admin_why]] and this
prevents every user from changing sensitive system settings. [[beat:platform]]
Application Platform. [[beat:plat_services]] The operating system provides services
that applications use. [[beat:plat_list]] Applications may request services for
displaying information, reading keyboard input, saving files, using memory, accessing
the network, printing documents. [[beat:why_platform]] This is why the operating
system is described as a platform for application software. [[beat:interrupts]]
Interrupt handling. [[beat:int_manage]] The operating system also helps manage
interrupts. [[beat:int_def]] An interrupt is a signal or event that requires the
processor's attention. [[beat:next_time]] We will examine interrupts carefully in a
few minutes.
