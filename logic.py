"""Project core: letter indexing, Quine-McCluskey minimization, Karnaugh map.

The Boolean function has 4 variables (A, B, C, D), A being the most significant bit.
An implicant is a 4-character string over {'0', '1', '-'}; for example '000-'
means A'B'C' (variable D has been eliminated).
"""
from itertools import combinations

# Official Romanian alphabet (31 letters)
RO_ALPHABET = list("AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ")
N_ALPHABET = len(RO_ALPHABET)
VARS = "ABCD"

_CEDILLA = {"Ş": "Ș", "Ţ": "Ț"}  # cedilla variants are treated as ș / ț


def letter_index(ch):
    """Position of the letter in the Romanian alphabet (A=1 ... Z=31), or None."""
    ch = _CEDILLA.get(ch.upper(), ch.upper())
    return RO_ALPHABET.index(ch) + 1 if ch in RO_ALPHABET else None


def text_to_rows(text, bits=4):
    """For each letter: (letter, index, index mod 2**bits, hex, binary, minterm)."""
    rows = []
    for ch in text:
        idx = letter_index(ch)
        if idx is None:  # spaces, hyphens etc. are ignored
            continue
        m = idx % (2 ** bits)
        rows.append((_CEDILLA.get(ch.upper(), ch.upper()), idx, m,
                     format(m, "X"), format(m, f"0{bits}b"), m))
    return rows


def minterms_from_text(text, bits=4):
    return sorted({r[5] for r in text_to_rows(text, bits)})


# ------------------------------------------------------------------ Quine-McCluskey
def _merge(a, b):
    diff = [i for i in range(len(a)) if a[i] != b[i]]
    if len(diff) == 1 and a[diff[0]] != "-" and b[diff[0]] != "-":
        i = diff[0]
        return a[:i] + "-" + a[i + 1:]
    return None


def covers(imp):
    """Set of minterms covered by an implicant."""
    out = [""]
    for c in imp:
        out = [p + x for p in out for x in ("01" if c == "-" else c)]
    return {int(s, 2) for s in out}


def prime_implicants(minterms, n=4):
    current = {format(m, f"0{n}b") for m in minterms}
    primes = set()
    while current:
        used, nxt = set(), set()
        for a, b in combinations(sorted(current), 2):
            m = _merge(a, b)
            if m:
                nxt.add(m)
                used.update((a, b))
        primes |= current - used
        current = nxt
    return sorted(primes)


def literals(imp):
    return sum(c != "-" for c in imp)


def minimal_covers(minterms, n=4):
    """All minimal covers (fewest terms first, then fewest literals)."""
    if not minterms:
        return []
    primes = prime_implicants(minterms, n)
    target = set(minterms)
    for size in range(1, len(primes) + 1):
        found = [c for c in combinations(primes, size)
                 if set().union(*(covers(p) for p in c)) == target]
        if found:
            best = min(sum(literals(p) for p in c) for c in found)
            found = [c for c in found if sum(literals(p) for p in c) == best]
            # deterministic order: by the minterms covered by each group
            found.sort(key=lambda c: sorted(sorted(covers(p)) for p in c))
            return [sorted(c, key=lambda p: sorted(covers(p))) for c in found]
    return []


def implicant_to_str(imp, names=VARS):
    s = "".join(names[i] + ("'" if c == "0" else "") for i, c in enumerate(imp) if c != "-")
    return s or "1"


def expression(cover, names=VARS):
    return " + ".join(implicant_to_str(p, names) for p in cover) if cover else "0"


def evaluate(cover, m, n=4):
    bits = format(m, f"0{n}b")
    return any(all(c == "-" or c == b for c, b in zip(p, bits)) for p in cover)


# ------------------------------------------------------------------ Karnaugh
GRAY = [0, 1, 3, 2]  # 00 01 11 10


def kmap_text(minterms):
    """Karnaugh map as text: AB horizontal, CD vertical (same layout as the report)."""
    ms = set(minterms)
    head = "CD\\AB |  00    01    11    10"
    lines = [head, "-" * len(head)]
    for cd in GRAY:
        cells = []
        for ab in GRAY:
            m = ab * 4 + cd
            cells.append(f"{int(m in ms)}(p{m})".ljust(6))
        lines.append(f" {cd:02b}   | " + " ".join(cells))
    return "\n".join(lines)
