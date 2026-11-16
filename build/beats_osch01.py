"""Beat placement for the Operating System chapter, Roman Urdu delivery.

Run from the repo root:

    python build/beats_osch01.py

The lecture is delivered in Roman Urdu and every caption on screen is in
English, as asked. That split is only safe because build/textnorm.py
folds words in whatever script they are written in: the rule it replaced
stripped every non-ASCII character, so every Urdu word folded to the
empty string, every word compared equal to every other, and an anchor
"matched" at the first position it was offered. It failed by appearing to
succeed, which is the one way this pipeline must never fail.

The audio the pipeline reads is made from the upload by one command,
because the recorder was running for three and a half minutes before the
lecture started:

    ffmpeg -ss 206 -to 1487 -i audio/OS-CH01-operating-system-raw.m4a \\
        -c:a aac -b:a 96k audio/OS-CH01-operating-system.m4a

    python build/transcribe.py audio/OS-CH01-operating-system.m4a \\
        --language ur --chunk 90 --no-vad --repetition-penalty 1.25
    python build/repair_loops.py audio/OS-CH01-operating-system.words.json \\
        --audio audio/OS-CH01-operating-system.m4a --language ur

That last step is not optional here. Even with VAD off and a repetition
penalty, the transcriber looped eleven times and filled 167 seconds with
repeated words and phrases -- including the hardware list, the device
drivers, the whole FCFS definition and the threads section. Anchors
written against that transcript would have been placed inside speech
that was never said.

Anchors are copied from the repaired transcript as it came out,
mis-hearings and all, never from the written script: "اوپرڈیکсیستن" is
operating system, "ارعیفز" is arrival, "زیکیشن" is execution, "افس" is
FCFS. Where the delivery drops into English the English is used, because
it is the most reliable thing in the file.
"""

from mkbeats import build

BEATS = [
    # ----------------------------------------------------------- opening
    ("open", "آپ کم پیر پر اپنا کام پھولتے ہیں براوزہ چلاتے ہیں"),
    ("behind", "آپ کی ہر رکوش کے پیچھے آپریگٹنگ سیستم کام کرتے ہیں"),
    ("agenda", "ہم کارنل, شل, عویس لیرز، یوزر ایک کاؤنز، پروسسز"),
    ("fcfs_promise", "پھر FCFS نی فرس کم فرس سرب اس کےجلن کا ایک سوال"),

    # ------------------------------------------- 1. what an OS actually does
    ("definition", "اوپرڈیکсیستن ایک سیستن صفر ہے جو کمپیٹروں کے حاردویر"),
    ("gives_access", "اور اوپرڈیکشت کو ان ریسورسز کے ساتھ کام کرنے کا"),
    ("hardware", "سیپیو ریم، سٹوریج ڈرائیو کیبورڈ سکرین اور نیٹورک کارڈ"),
    ("apps", "اپلیکیشن میں آپ کا پراوزر ہو گیا گیمز ہو گئے ورڈ پروسسرز"),
    ("double_click", "اپنے ماؤس سے فائل پر ڈبل کلک کرتے ہیں یہ یوزر ایکشن"),
    ("request_travels", "فائل کھولنے کی ریکویسٹ اپلیکیشن اور آپریٹنگ سسٹم تک جاتی ہے"),
    ("os_decides", "دیدہ میمگری میں رکنایا اور اس کین پر دیکھانا ہے"),
    ("no_detail", "تو user کو Hardware کے Hard Technical Detail کو سیدھا"),
    ("waiter", "آپ رسٹرین میں ویٹر کو آر دیتے ہیں ویٹر آپ کی ریکوز"),
    ("os_examples", "وینڈوز لینیکس میکوز اینڈرویڈ"),

    # -------------------------------------------------- 2. user accounts
    ("many_users", "ایک کمپیٹر کو کئی لوگ استعمال کر سکتے ہیں"),
    ("account_has", "اپنا اوزر نیم ہوتا ہے سیٹنگز اور فیلس"),
    ("login_check", "لگن کے وقت اوزر کی پیشان چیک کرتے اور پرمیشنز"),
    ("admin", "آپ کے واعلان کم یہ کونوں ہو سکتے جو کی an Administrator"),
    ("siblings", "اگر ایک ایک نئے اگر بھائی نگر اکسز کی ہے"),
    ("accounts_recap", "OS Accounts کو مینج کرتا ہے Users کی پیشان چیک"),

    # ------------------------------------------------- 3. kernel and shell
    ("kernel_shell", "اب بات کرتے گرنلورشیل کیا Operate System"),
    ("kernel", "OS کا سنترلص ہے یہ CPU میموری اور دوائز"),
    ("kernel_time", "یہ پروگرامس کو CPU کا وقت دینے"),
    ("shell", "شل جو ہے نا وہ ایوزر اور آپریڈing system کے درمیان انٹرافیس"),
    ("gui", "گرافقل شل ہوتا ہے اس میں وینڈوز ایکونز"),
    ("cli", "کمان لائن شل اس میں آپ کمان ٹیپ کرتے ہیں"),
    ("one_line", "شل یوزر سے رکس لیٹھا ہے کرنل ریسورٹسیز اور ہارڈویر"),

    # ------------------------------------- 4. layers, libraries and drivers
    ("layers", "بات کرتے ہیں OS LAYERS & LIBRIRES OR DRYVERS"),
    ("upper", "اپر Layer User & Application کی قریب ہوتی ہے"),
    ("middle", "middle layer وہ Operating System کی services اور resources"),
    ("lower", "پھر لوڑڈ لیر جنا محادویر کے قریب ہوتی ہے یہاں پہ کرنل"),
    ("print_example", "جب آپ دکمین پرنڈ کرتے ہیں تو اپلکیشن پرنٹ رکوست OS کو"),
    ("printer_driver", "پرنٹر درائیور اسے پرنٹر کے سمجھنے"),
    ("libraries", "سسٹم لائبریریز میں پہلے سے تیار فوجنشنز یا کوڑ"),
    ("driver_def", "دوائز ڈرائیور جو ہوتے ہیں وہ آپریٹنگ سسٹم اور کسی ہارڈوئر"),
    ("driver_eg", "جیسے پرنٹر ڈرائیور ہوتا ہے، ساؤنڈ ڈرائیور ہوتا ہے"),

    # --------------------------------------------- 5. process and lifecycle
    ("process", "موونگ آنٹو پروسس اور پروسس کا رائیف سائیکل"),
    ("process_def", "جب پروگرام چلنا شروع اسے پر اسے پرسس کہتے"),
    ("browser_example", "براوزر کا پر گیاں اس طورج میں ہوتا ہے"),
    ("lifecycle", "پرسس کی جو لیسائکل کنہ ٹین مرائل ہوتے نمبر"),
    ("termination", "اپنا کام ختم کرتا ہے یا بند کر دیا جاتا ہے"),
    ("resources_back", "او ایس کے استعمال شدہ ریسورسز واپس لے دی جاتے ہیں"),
    ("calculator", "جیسے کلکلیٹر کھولنا ہے کھولنا جو ہے نا میں کلک کیا"),
    ("calc_three", "اس کے اندر اس کی ایک زیقیشن ہے"),

    # --------------------------------------------------- 6. FCFS scheduling
    ("fcfs", "ایف سی ایف ایس کیا ہوتا ہے فرس کم فرس سیف اسکیجولنگ"),
    ("waiting_cpu", "جب کئی پروسیس سی پی او کا انتظار کر رہے ہونا"),
    ("scheduling", "اسی لیے پروسیس اسکیجولنگ کرنی پڑتی ہے"),
    ("first_come", "فرس کم فرس سیف میں جو پروسیس پہلے آتا ہے پہلے"),
    ("bakery", "آپ کو بیکری کی لائن میں لگے میں آپ اپنی بے باریکن"),
    ("the_table", "سیپیو برنس فور سیکن سیکنہ پیٹھو ارعیفز"),
    ("order", "سیس کے مطابق ایک زیکیشن ارعیوگا p1 p2 p3 ہوگا"),
    ("p1_runs", "تو p1 پہ 0 start ہوگا اور 4 پر complete ہوگا"),
    ("p2_runs", "p2 ہے 4 پر اسٹارت ہوگا اور 7"),
    ("p3_runs", "پر اسٹارت ہوگا اور 8 پیٹھو گا"),
    ("formula", "ویٹنگ time equals start time minus arrival"),
    ("p1_wait", "دیکھیں P1 0 -0 2nds"),
    ("p23_wait", "3 seconds and p3 7 – 2 it's 5 sec"),
    ("average", "So averaged waiting time gap was zero plus three"),
    ("exam_order", "so exam they tell execution order"),
    ("exam_rest", "اُس کے بہت ویٹنگ ٹائم اور آخر میں ایوریج ویٹنگ ٹائم"),

    # -------------------------------------- 7. multitasking and concurrency
    ("multitasking", "ملٹی ٹیسکنگ اور کونکرنسی کس کو بولتے ہیں"),
    ("multi_eg", "جیسے آپ نا میوزک بھی سن رہے ہیں آپ براوزنگ بھی کر رہے ہیں"),
    ("concurrency", "اب کو کرنسی کا کیا بطلب ہوتا ہے؟"),
    ("switching", "سی پیو تجی سے تاس کے درمیاں سوچ کرتا"),
    ("chef", "ایک شف دال پکنے کے لئے رکھتا ایک روٹی تیار کرتے"),

    # ------------------------------------------ 8. RAM and virtual memory
    ("ram", "اب وہ بھاں بات کرتے ہیں ریم اور ورچور میمری کی"),
    ("ram_def", "ریم جہنا وہ پرائمری این رینڈم ایکس میمری جہاں چلے والے پرگرامز"),
    ("ram_fast", "وہ ریم سے دیٹا جلدی ایکسنس کر سکتے ہیں"),
    ("virtual", "جب رہم بھڑھنے لگے ایک اس کا ایوز بڑھنے لگے"),
    ("virtual_slow", "لیکن سٹورتج درائف رہم سے سوستوثتی ہے"),

    # ------------------------------------- 9. process, thread, multithreading
    ("thread_def", "thread جو ہے وہ process کے اندر execution کا چھوٹا unit"),
    ("thread_share", "ایک process کے thread اسی process کی memory اور کچھ resources"),
    ("word_threads", "ایک ٹرڈ جائے وہ تائپنک کو حندل کر سکتا ہے"),
    ("autosave", "اور دوسرا جو ہے داکومن کو auto safe کرتے ہیں"),
    ("office", "اسے ایک آفیس سمجھے تکنا جیسے پرسس جیم آفیس ہے"),
    ("multithreading", "ملکی ٹریکن سے اپلکیشن کے کام ایک ہی پروسس کے اندر چل سکتے"),
    ("responsive", "آرٹو سیف چلتے ہوئے بھی آپ ٹائپنگ جاری رکھ سکتے"),

    # -------------------------------------------------- 10. system calls
    ("syscalls", "اب ہم آتےSystems call کے پر نا"),
    ("syscall_def", "سستم کال وہ طریق ہے جسے پرگرام اپرارٹیک سستم سے صرفیس"),
    ("syscall_when", "فائل کھولنی ہو، دیتہ پرنا ہو، دیتہ لکنا ہوں"),
    ("sc_process", "پرسیز مینجنگ دو گیا ہے نا پرسیز بنانے یا ختم کرنا"),
    ("sc_file", "فائل مینجمن جہا ہے فائل کھولنا پڑنا یا لکنا"),
    ("sc_device", "دیوائز مینجمن کہیں ایک پرنتر"),
    ("sc_comm", "اب کمیніکیشن یا پرگرامس یا کمپیٹریز کے در میں"),
    ("fork_note", "فورک جہنا وہ یونکس لینکس سیستم میں نیاں پروسس بنانے کی مصال"),

    # ------------------------------- 11. file system, folders and metadata
    ("filesystem", "اب بات کرتے فائر سیسٹرم کے بر فائر سیسٹرم اور میٹھیں دیٹھا"),
    ("fs_def", "فائر سیسٹرم جو ہے وہ اس طورج میں دیٹھا کو ارغنائز"),
    ("file", "تو فائر میں دیتا ہوتا ہے جیسے دکمین یا تصویر"),
    ("folder", "اف فولڑر جو یا نا وہ فائرز اور فولڑرز کو گروب"),
    ("metadata", "میٹر دیتا جو یا نا وہ فائر کے بارے میں ملومات"),
    ("papers", "اب سوچئے آپ کے پاس جو ہے نا ہزاروں پیپرز ہیں"),
    ("labelled", "اگر وہ لیبل فولڈرز میں رکھے ہوں تو ڈھونڈنا آسان"),

    # -------------------------------------- 12. the journey to a server
    ("journey", "جب آپ براوزر میں Website کا نام لکھنے تو رکس جے نا وہ کیسے سفر"),
    ("you_type", "آپ کی بورد سے Website کا نام تیب کرتے ہیں براوزر"),
    ("network_card", "نٹورک کارڈ رکوز کو انٹرنت کے ذریعے سرورک"),
    ("server_replies", "سرورک جو نا وہ جواب واپس بھیجتے ہیں"),
    ("back_to_browser", "اوپریڈنگ سسٹم اس دیتا کو مینچ کرتے ہیں اور براوزر کو دیتے"),
    ("on_screen", "پر براوزر ویب پیچ کو اسکرید پر دیکھا تا ہے"),

    # ------------------------------------------------------------- recap
    ("recap", "تو آج ہم نس کیا سکے کہ اوپرینک سیستم ہارڈویر ریسورٹز مینج"),
    ("recap_kernel", "ترنال جہ ہے وہ اوپرینک سیستم کا قور ہے شل جہاں وہ user interface"),
    ("recap_layers", "user layers milkar application request کو hardware تک"),
    ("recap_accounts", "user accounts, you know alloc settings"),
    ("recap_process", "چلتا وہ program جوحناس کا بروسس کہتے ہیں"),
    ("recap_fcfs", "افس کی افسی سف میں جہے میں پہلے آنے والا پروسس پہلے جلتا"),
    ("recap_multi", "ملٹی تاسک کی تاسک کو مختلف دپرنیہ نا سیورل ٹاسک"),
    ("recap_threads", "پھر Threads جو ہے نا وہ پر آسس کے اندر کام کرتے"),
    ("recap_syscalls", "بات کی تھی سیسٹم کسیسٹم کسیسٹم جہنا وہ پروگرائم کو اویس"),
    ("recap_files", "فائل سسٹرمس اور فولڈرس کو ارغنائز کرتے ہیں میٹرڑیتا"),

    # ------------------------------------------------------ self-check
    ("pause", "اب آپ ویڈیوں پوز کر لئے جس ہوتے گے نا اور خود"),
    ("q1", "عبرڈیگ سسٹرمس سے ایوزر کی رکوز کو حاردویر تک کیسے"),
    ("q2", "نمبرٹل، ملکطپو ایوزر ایکانس اور پرمیشن کا کیا فائد ہے"),
    ("q3", "نموطری قرنل اور شلپ شل میں کیا فرق ہوتا ہے"),
    ("q4", "افس سوال میں ویٹنگ تائم کیسے نکالتے ہیں"),
    ("q5", "پروسس اور تھرد میں کیا فرق ہے"),
    ("q6", "and then 6th, Systems call it 3 types"),
    ("q7", "file system & meta data ke ka kya"),
    ("close", "اگر آپ ان سوالوں کو جواب اپنے عالفاظ میں دے سکتے ہیں"),
]

NOTE = ("Operating System, Chapter 1. Roman Urdu delivery, English slides. "
        "Recorder ran 206s before the lecture; audio cut with ffmpeg, "
        "transcribed --language ur --chunk 90 --no-vad "
        "--repetition-penalty 1.25, then repaired with "
        "build/repair_loops.py, which replaced eleven transcription loops "
        "covering 167s. Beats placed by anchor phrase, see "
        "build/beats_osch01.py.")

if __name__ == "__main__":
    build("OS-CH01-operating-system", "cs.os_chapter1", BEATS,
          "OS-CH01-operating-system", NOTE)
