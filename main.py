"""Minimizing a Boolean function with the Veitch-Karnaugh method, starting from letters.

Examples:
    python main.py SIMION --extra ESCU
    python main.py MOLDOVANU --extra E --schema schema.png
"""
import argparse

import logic


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("name", help="surname (letters of the Romanian alphabet)")
    ap.add_argument("--extra", default="", help="extra letters appended to reach at least 8 unique values")
    ap.add_argument("--schema", default="schema.png", help="file where the logic diagram is saved")
    ap.add_argument("--no-schema", action="store_true", help="do not generate the diagram image")
    args = ap.parse_args()

    text = args.name + args.extra
    rows = logic.text_to_rows(text)
    print(f"Name used: {text.upper()}  (Romanian alphabet, N = {logic.N_ALPHABET})\n")
    print("Letter  Index   Mod16  Hex  Binary(ABCD)  Minterm")
    for ch, idx, m, hx, b, mt in rows:
        print(f"{ch:^6}  {idx:^6}  {m:^5}  {hx:^3}  {b:^12}  p{mt}")

    ms = logic.minterms_from_text(text)
    print(f"\nUnique minterms ({len(ms)}): {ms}")
    if len(ms) < 8:
        print("WARNING: fewer than 8 unique values; add letters with --extra.")

    print("\nKarnaugh map:\n" + logic.kmap_text(ms))

    covers = logic.minimal_covers(ms)
    if not covers:
        print("\nThe function is identically 0.")
        return
    print("\nPrime implicants:", ", ".join(logic.implicant_to_str(p) for p in logic.prime_implicants(ms)))
    print("\nMinimal sum-of-products forms:")
    for i, c in enumerate(covers, 1):
        print(f"  {i}. f = {logic.expression(c)}")
    best = covers[0]
    ok = all(logic.evaluate(best, m) == (m in ms) for m in range(16))
    print(f"\nCheck on all 16 input combinations: {'OK' if ok else 'ERROR'}")

    if not args.no_schema:
        import draw
        draw.draw_schema(best, args.schema)
        print(f"Logic diagram of form 1 saved to: {args.schema}")


if __name__ == "__main__":
    main()
