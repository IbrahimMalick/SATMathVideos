"""Beat placement for the system software and operating system lecture.

Run from the repo root:

    python build/beats_os01.py

The narration is an ElevenLabs read of the written script, not a live
recording, and it opened with a false start: the voice began "Part 1,
system software and" — then stopped, left 1.6 seconds of digital silence,
and read the title again from the top. The audio the pipeline reads is made
from the uploaded file by one command, so the same upload reproduces the
same mp4:

    ffmpeg -ss 4.0 -i audio/OS01-system-software-raw.mp3 \\
        -c:a aac -b:a 192k audio/OS01-system-software.m4a

    python build/transcribe.py audio/OS01-system-software.m4a \\
        --language en --chunk 90

The cut lands at 4.0s, inside the stretch of exact digital zeroes that runs
from 3.45s to 5.02s, so it clips neither take. retake.py cannot do this
one: both takes open with the same words, so an anchor on the real take's
opening phrase also matches the false start, and a drop that runs from the
first to the second swallows the good take along with the bad.

Anchors below are taken from the transcript of the cut audio, mis-hearings
included, never from the written script: "organizers" is organizes, "this
cleanup software" is disk-cleanup software, "and force passwords" is
enforce passwords, "See, security management" is Security management, and
"understand and what" is understand what.
"""

from mkbeats import build

BEATS = [
    # ------------------------------------------------------- what software is
    ("open", "Part 1, system software and application software"),
    ("software_is", "Software is a collection of programs and instructions"),
    ("distinguish", "For Cambridge O -level computer science"),
    ("bins", "you must distinguish between system software and application"),

    # --------------------------------------------------- sorting the two kinds
    ("sys_def", "System software provides services required by the computer"),
    ("sys_eg1", "Examples include operating systems"),
    ("sys_eg2", "utility software, device drivers"),
    ("sys_eg3", "device drivers, Application Software provides"),
    ("app_def", "Application Software provides services required by the user"),
    ("app_eg1", "Examples include Word processors"),
    ("app_eg2", "web browsers, database software"),
    ("app_eg3", "database software, games"),
    ("app_eg4", "games, presentation software"),
    ("app_eg5", "presentation software, video editing"),
    ("app_eg6", "video editing software. Here is the simplest"),

    # ------------------------------------------------------- the rule to hold
    ("simplest", "Here is the simplest way to remember the difference"),
    ("rule_sys", "System software helps the computer operate"),
    ("rule_app", "Application software helps the user complete a task"),

    # --------------------------------------------------- the antivirus test
    ("antivirus", "consider antivirus software"),
    ("can_open", "A user can open it and interact with it"),
    ("still_system", "but it is still classified as system software"),
    ("its_role", "because its main role is to maintain and protect"),

    # ------------------------------------------------------ the common mistake
    ("mistake", "A common mistake is to classify every program"),
    ("incorrect", "That is incorrect software must be classified"),
    ("by_purpose", "according to its purpose"),
    ("not_open", "Not simply according to whether the user can open it"),

    # ------------------------------------------------------------ quick check
    ("quick_check", "Quick check"),
    ("qc_item", "A student uses spreadsheet software to calculate monthly"),
    ("qc_ask", "Is the spreadsheet system software or application software"),
    ("qc_answer", "It is application software because it helps the user"),
    ("qc2", "Now consider this cleanup software"),
    ("qc2_what", "It removes unnecessary files and helps maintain"),
    ("qc2_answer", "This is utility software and is therefore classified"),

    # ------------------------------------------------- part two: the OS itself
    ("part2", "Part 2. The operating system."),
    ("most_important", "The operating system is the most important type"),
    ("manages", "It manages the computer's hardware and software resources"),
    ("platform_intro", "and provides a platform on which application software"),
    ("examples", "Examples include Windows, Mac OS, Linux"),
    ("no_memorise", "You do not need to memorize product names"),
    ("understand", "You need to understand and what an operating system does"),
    ("functions", "Let us examine its major functions"),

    # ------------------------------------------------------- 1. managing files
    ("files", "File management"),
    ("files_verbs", "The operating system creates names, stores, retrieves"),
    ("files_folders", "It also manages folders and keeps track of where data"),
    ("files_save", "When you save a file, the application does not normally"),
    ("files_asks", "It asks the operating system to handle the process"),
    ("files_also", "The operating system can also manage file names"),
    ("files_weak", "In an examination answer, do not write only"),
    ("files_stronger", "For a stronger answer, explain what that means"),
    ("files_strong", "The operating system creates names, organizes, stores"),

    # -------------------------------------------------- 3. providing an interface
    ("ui", "User Interface The operating system provides an interface"),
    ("gui", "A graphical user interface may contain"),
    ("cli", "A command line interface allows the user to type commands"),
    ("ui_converts", "the user interface converts the user's actions"),

    # ------------------------------------------ 4. managing peripherals and drivers
    ("periph", "Peripheral and driver management"),
    ("periph_def", "A peripheral is a hardware device connected to"),
    ("periph_eg", "Examples include printers, keyboards, mice"),
    ("driver_def", "A device driver is software that allows the operating"),
    ("diff_printers", "Different printers may require different drivers"),
    ("not_direct", "An application normally does not communicate directly"),
    ("path", "The typical path is application software"),
    ("path_os", "then the operating system, then the device driver"),
    ("path_driver", "then the device driver, then the hardware device"),
    ("path_hw", "then the hardware device. This separation"),
    ("separation", "This separation makes applications easier to develop"),

    # ------------------------------------------------------ 5. managing memory
    ("memory", "Memory Management The operating system manages the use"),
    ("mem_decides", "It decides which program receives memory"),
    ("mem_how_much", "how much memory is allocated"),
    ("mem_where", "where instructions and data are stored"),
    ("mem_release", "when memory can be released and used by another program"),
    ("mem_protect", "The operating system must also prevent one process"),
    ("virtual", "If there is not enough physical RAM"),
    ("virtual_what", "Virtual memory uses part of secondary storage"),
    ("slower", "However, secondary storage is slower than RAM"),
    ("excessive", "Therefore, excessive use of virtual memory"),
    ("mem_exam", "A strong examination answer should mention allocation"),
    ("mem_weak", "Not simply say that the operating system controls RAM"),

    # ------------------------------------------------- 6. managing multitasking
    ("multi", "Multi -tasking allows more than one process"),
    ("process_def", "A process is a program that is currently being executed"),
    ("single_core", "On a single processor core, the operating system switches"),
    ("allocates", "and it allocates a small amount of processor time"),
    ("impression", "This can create the impression that the programs"),
    ("multi_eg", "For example, you may stream music"),
    ("share", "The operating system must share processor time"),

    # --------------------------------------------- 8. providing system security
    ("security", "security management, the operating system helps protect"),
    ("sec_list", "It can authenticate users and force passwords"),
    ("sec_not_all", "Security does not mean that the operating system prevents"),
    ("sec_mechanisms", "It means that it provides mechanisms for controlling"),

    # ----------------------------------------------- 9. managing user accounts
    ("accounts", "User account management"),
    ("acct_maintain", "The operating system can maintain different user accounts"),
    ("acct_each", "Each account may have its own, user name, password"),
    ("admin", "and administrator account normally has greater control"),
    ("admin_why", "and this prevents every user from changing sensitive"),

    # ------------------------------ 7. providing a platform for running applications
    ("platform", "Application Platform"),
    ("plat_services", "The operating system provides services that applications use"),
    ("plat_list", "Applications may request services for displaying information"),
    ("why_platform", "This is why the operating system is described as a platform"),

    # ------------------------------------------------- 2. handling interrupts
    ("interrupts", "Interrupt handling"),
    ("int_manage", "The operating system also helps manage interrupts"),
    ("int_def", "An interrupt is a signal or event that requires"),
    ("next_time", "We will examine interrupts carefully in a few minutes"),
]

NOTE = ("System software, application software and the operating system. "
        "Cambridge O Level Computer Science 2210, topic 4.1, syllabus for "
        "examination in 2026, 2027 and 2028. ElevenLabs narration; the "
        "false start on the title was cut before transcription, see "
        "build/beats_os01.py.")

if __name__ == "__main__":
    build("OS01-system-software", "cs.system_software", BEATS,
          "OS01-system-software", NOTE)
