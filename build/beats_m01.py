"""Beat placement for Matrices — beyond a table of numbers.

Run from the repo root:

    python build/beats_m01.py

The narration is Urdu, so the anchors are Urdu — and they are copied from
the transcript rather than from the written plan, mis-hearings included.
The transcriber renders English loanwords phonetically and inconsistently
("students" comes out as اسٹوڑنٹس, اسٹورینس and اسٹریلز in three different
places), so an anchor written the way the word *should* be spelled would
not match the audio at all.

This only works because the word-folding rule understands more than ASCII.
The one it replaced mapped every Urdu word to the empty string, which made
every anchor match at the first position it was offered.
"""

from mkbeats import build

BEATS = [
    # ----------------------------------------------------------- opening
    ("title", "آپ کو شاید لگتا ہو کہ ان کے میٹرسز"),
    ("misconception", "بس نمبر کی مشکل تھی ٹیوز ہوتی ہیں"),
    ("not_true", "لیکن یہ بات بالکل دروست نہیں ہے"),
    ("tournament", "آج جو ہے نا ہم اسکول کی کرکٹ ٹیم کی ایک مثال"),

    # ------------------------------------------------------- first count
    ("students_come", "اچھا آپ ایمینڈ کرو کہ ٹورنامنٹ کے لئے تین سٹوڑنٹس"),
    ("two_each", "ہر اسٹوڑنٹ کے لئے آپ کو ڈو سموسے رکھنے"),
    ("multiply", "ٹین کو ڈو سے ملڈپلائی کریں جواب ہے"),

    # ------------------------------------------------------ three groups
    ("not_only", "لیکن ٹورنامنٹ میں صرف اسٹوڑنٹ نہیں ہے"),
    ("also", "تیچرز اور کریگٹ کے پلیئرز بھی ہیں"),
    ("headcount", "تو مثال کے طور پر ہم نے ہمارے پاس تین اسٹوڑن سے دو ٹیچرز"),
    ("needs_differ", "ہر شخص کی ضرورت ایک جیسی نہیں"),
    ("per_person", "ایک اسٹوڑن کے لئے ڈو سموسہ ایک ٹیچر کے لئے"),
    ("calc_students", "تو اسٹوڈرز کیلئے 3 گناہ دو یعنی"),
    ("calc_teachers", "ٹیچرز کے لئے 2 گناہ 1 یعنی"),
    ("calc_players", "اور پلائرس کے لئے کیا 4 گناہ 3"),
    ("total", "اب انہیں جما کرتے ہیں چھے پلس دو پلز بارہ"),

    # ------------------------------------------------------ the matrix
    ("more_items", "اب اسی طریقے سے پانی کی بوطلیں بھی چاہیئے"),
    ("arrange", "یہ سب ضروریات ایک جگہ لکھنے کے بجائے"),
    ("matrix_named", "اس ریکٹانگلر ٹیول آف نومبرز کو میٹرکس کہتے ہیں"),
    ("columns", "اس میٹریس کا ہر کولم ایک گروپ کو دکھاتا ہے"),
    ("rows", "ہر رو ایک آئٹم کو دکھاتی ہے"),
    ("each_number", "ہر نمبر بتاتا ہے کہ اس گروب کی ایک شخص کے لیے"),
    ("entry_eg", "اگر ہر پلائر کے لیے ڈو بوتل پانی چاہیے"),

    # ------------------------------------------------------- the vector
    ("vector", "اب ایک چھوٹا سا کالم ویکتر لکھتے ہیں"),
    ("vector_meaning", "یہ ویکتر بتاتا ہے کہ کتنے اسٹورینس ہیں"),

    # ------------------------------------------------------ the product
    ("how", "اب ہر گروپ کی ضروریات کو اس گروپ کے لوگوں کی تعداد"),
    ("water_row", "تو پانی کی بوتلیں ہوں گی تین پلس ڈو پلس آٹھ"),
    ("samosa_row", "سموسیں ہم پہلے ہی نکال چکے ہیں"),
    ("banana_row", "بناننز ہوں گے تین پلس دو پلس جار کل نو"),
    ("output", "تو میتمیٹقلی ہمیں میٹریکس کو لوگوں کی ویکتر سے ملٹیپلائے"),
    ("mathematically", "یہ آف پوڈ بتاتا ہے کہ ٹورنامنٹ کے لئے ہر ایٹم"),
    ("idea_simple", "یہ کالکولیشن لکھی ہوئی دیکھیں مشکل لگ سکتی ہے"),

    # -------------------------------------------------------- the order
    ("order", "یہاں ایک بہت ضروری بات ہے کالومز کا ارڈر"),
    ("order_match", "اگر پہلا کالوم اسٹریلز کا ہے تو ویکتر کا پہلا نمبر"),
    ("order_wrong", "اورڈل غلط ہوئے اساس بھی غلط ہو سکتا ہے"),

    # ----------------------------------------------------- as a function
    ("function", "تو اب اس پورے پروسس کو ایک فنکشن سمجھتے ہیں"),
    ("three_three", "کیونکہ لوگوں کی تین کٹی گریز ہے نا"),

    # --------------------------------------------------------- scaling
    ("scaling", "تو اس فنکشن کے پہلی خاصیت یہ ہے"),
    ("scaling_eg", "اگر ٹورنامنٹ کے لئے 13 بوطل چاہیئے تھیں"),
    ("scaling_name", "انپٹ کو کسی نمبر سے ملٹپلائے کریں"),

    # ------------------------------------------------------- additivity
    ("additivity", "یاد رکھنا یہ دوسری خاصیت ہے"),
    ("additivity_two_ways", "ہم دونوں گروپس کی تعداد جماع کر سکتے ہیں"),
    ("additivity_same", "دوروں طریقوں سے وہ ہی جواب ملے گا"),
    ("linear", "جس فنکشن میں اس کیلنگ اور اڈیٹوئی ٹی دونوں ہو"),

    # ---------------------------------------------------------- geometry
    ("geometry", "میٹریسز صرف event پلاننگ میں کام نہیں آتی"),
    ("shapes", "ان سے شیپس کو"),
    # "stretch" and "rotate" are said in one breath, 0.7s apart, so both
    # transformations belong to this beat; splitting them would give the
    # stretch less than a second to happen in.
    ("transform", "سٹرچ روٹیٹ"),
    ("dimensions", "دو ڈیمنٹشنز میں بھی ہوتے ہیں"),

    # ----------------------------------------------------------- closing
    ("not_just", "اگلی بار میٹریکز دیکھیں تو اس سے صرف نومبر کی ٹیبل"),
    ("three_uses", "یہ معلومات کو ارہنچ کرنے"),
    ("maths_interesting", "جب ہم فارملو کے ساتھ یہ بھی سمجھتے ہیں"),
    ("cta", "اگر یہ اسپلیریشن آپ کے لئے مدد مفید تھی"),
]

NOTE = ("Matrices, narrated in Urdu with English slides. Take 2 of the "
        "recording; take 1 is cut by build/segment.py. Beats placed by "
        "anchor phrase from the transcript; see build/beats_m01.py.")

if __name__ == "__main__":
    build("M01-matrices", "concept.matrices", BEATS, "M01-matrices", NOTE)
