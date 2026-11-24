"""One Word for Your Wi-Fi — entrypoint.

Picks the single word that best describes home Wi-Fi under the
competition brief's five criteria, in the brief's own priority order:

  1. on_subject — describes Wi-Fi as the entrant lives it.
  2. funny      — a real laugh at once, no explaining needed.
  3. true       — feels true to how home Wi-Fi actually behaves.
  4. fresh      — avoids the words everyone reaches for.
  5. instant    — works as one word, understood instantly.

The winner is the candidate whose score tuple is lexicographically
greatest, which mirrors the judge's rule: the first criterion where
two words differ decides, unless a later one differs by much more.
The program writes exactly that one word to entry.txt in the output
directory (MAKEFUN_OUTPUT_DIR, default /output) and prints it.
"""

import os

# Candidate words, each scored 0-5 on the five brief criteria above.
# Scores are this entry's own judgement, written down so the pick is
# reproducible rather than a magic constant.
CANDIDATES = {
    # Wi-Fi that vanishes mid-call, like a bad date who stops replying:
    # on-subject, funny at once, true of every home network, and a fresh
    # angle instead of the usual "slow / laggy / buffering" complaint.
    "Ghosting": (5, 5, 5, 5, 5),
    # True and instant, but "flaky" is the word everyone already reaches for.
    "Flaky": (5, 4, 5, 3, 5),
    # Personifies the router's moods; funny, but less precise than vanishing.
    "Moody": (5, 4, 4, 4, 5),
    # The one-bar-then-nothing tease; good, but softer than disappearing.
    "Teasing": (5, 4, 4, 4, 5),
    # A diva that only works when it feels like it; the joke needs a beat.
    "Diva": (4, 4, 3, 4, 5),
    # Feels cursed some days, but says more about luck than about Wi-Fi.
    "Cursed": (4, 4, 3, 4, 5),
    # The cliche: true, instantly understood — and exactly what criterion 4
    # punishes, because everyone reaches for it first.
    "Buffering": (5, 3, 5, 1, 5),
    # Honest, boring, and the first word in every complaint thread.
    "Laggy": (5, 2, 5, 1, 5),
}


def pick_word(candidates):
    """Return the candidate with the greatest score tuple.

    Ties break toward the shorter word, then the earlier name, so the
    choice is fully deterministic.
    """
    best = None
    for word, scores in candidates.items():
        key = (scores, -len(word), tuple(-ord(c) for c in word))
        if best is None or key > best[0]:
            best = (key, word)
    return best[1]


def check_gate(word):
    """Enforce the sealed scorer's gate before writing anything.

    The entry must be UTF-8 text of 1 to 20 characters, not only
    whitespace, and a single word — anything else scores 0 and takes
    no prize, so refuse to write it rather than submit an invalid entry.
    """
    if not word or len(word) > 20 or not word.strip():
        raise ValueError("entry fails the gate: empty or over 20 chars")
    if len(word.split()) != 1:
        raise ValueError("entry fails the gate: not a single word")
    return word


def main():
    word = check_gate(pick_word(CANDIDATES))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8") as f:
        f.write(word)
    print(word)


if __name__ == "__main__":
    main()
