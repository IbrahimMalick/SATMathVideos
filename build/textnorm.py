"""One word-folding rule, shared by the aligner and the beat placer.

Both used to fold a word with ``re.sub(r"[^a-z0-9]", "", word.lower())``.
That is fine for English and silently catastrophic for anything else: every
Urdu word folds to the empty string, so every word compares equal to every
other word, the aligner matches nothing in particular, and an anchor phrase
"matches" at the first position it is offered. It fails by appearing to
succeed, which is the worst way for this pipeline to fail.

So folding keeps letters and digits in whatever script they are written in
and drops everything else. On ASCII input it agrees with the old rule, bar
accented Latin, which now folds to its unaccented form.
"""

import unicodedata

# Urdu is written with several code points that mean the same letter, and a
# transcriber picks between them inconsistently from one word to the next.
# Folding those together is the difference between an anchor matching and an
# anchor being silently absent.
#
# Only the pairs a transcriber really does interchange are folded. Barree
# yeh and heh doachashmee are left alone: they are distinct Urdu letters,
# not spellings of another one, and folding them would make کے and کی the
# same word, and بھی and بہی the same word.
LETTER_FOLD = {
    "ي": "ی",   # Arabic yeh   -> Farsi yeh
    "ى": "ی",   # alef maksura -> Farsi yeh
    "ك": "ک",   # Arabic kaf   -> keheh
    "ه": "ہ",   # Arabic heh   -> heh goal
    "ة": "ہ",   # teh marbuta  -> heh goal
    "ۃ": "ہ",   # teh marbuta goal
}

# Joiners carry no sound and appear or vanish depending on the transcriber.
INVISIBLE = {"​", "‌", "‍", "⁠", "﻿"}


def normalize(word):
    """Fold a word to a comparison key, in any script."""
    out = []
    for ch in unicodedata.normalize("NFKD", word).casefold():
        if ch in INVISIBLE or unicodedata.combining(ch):
            continue          # Urdu diacritics are optional; ignore them
        ch = LETTER_FOLD.get(ch, ch)
        decimal = unicodedata.decimal(ch, None)
        if decimal is not None:
            out.append(str(decimal))   # Arabic-Indic digits fold to ASCII
        elif ch.isalnum():
            out.append(ch)
    return "".join(out)
