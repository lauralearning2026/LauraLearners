"""Build the Algebra II practice bank.

Usage (from this folder):  python3 build.py
Writes public/courses/algebra-2/bank.json for the site and prints a
blueprint summary. Re-running gives the same items (fixed seed).
"""
import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))
import common  # noqa: E402
import so, ei, fn, sp  # noqa: E402,F401  (registers generators)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(ROOT, "public", "courses", "algebra-2", "bank.json")
ORDER = ["SO", "EI", "FN", "SP"]
TARGET = {"SO": 0.275, "EI": 0.20, "FN": 0.30, "SP": 0.225}
BLUEPRINT = {"SO": (25, 30), "EI": (17, 23), "FN": (27, 33), "SP": (20, 28)}


def main():
    generated, report = common.run(seed=2026)
    hand = json.load(open(os.path.join(HERE, "handwritten.json")))
    seen = {common.stem_key(q) for q in generated}
    items = generated + [q for q in hand if common.stem_key(q) not in seen]
    items.sort(key=lambda q: (ORDER.index(q["category"]), q["standard"], q["template"]))
    for i, q in enumerate(items, 1):
        q["id"] = f"A2-{i:04d}"
    bank = {
        "course": "Algebra II",
        "exam": "TCAP Algebra II EOC (Tennessee)",
        "standards": "2023-24 Tennessee Academic Standards for Mathematics, Algebra II",
        "note": "Original practice items. Not official TCAP items. Answer keys are computed by the generators in tools/algebra2.",
        "categories": {"SO": "Structure and Operations", "EI": "Equations and Inequalities",
                       "FN": "Functions", "SP": "Statistics and Probability"},
        "items": [{k: q[k] for k in ("id", "category", "standard", "type", "dok", "calculator", "stem", "choices",
                                     "answer", "explanation", "rationales", "template")} for q in items],
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(bank, f, ensure_ascii=False, separators=(",", ":"))
    short = [(n, s, q, g) for n, s, q, g in report if g < q]
    c = Counter(q["category"] for q in items)
    n = len(items)
    print(f"{n} items -> {os.path.relpath(OUT, ROOT)} ({os.path.getsize(OUT) // 1024} KB)")
    for k in ORDER:
        lo, hi = BLUEPRINT[k]
        share = 100 * c[k] / n
        print(f"  {k}: {c[k]:4d} ({share:.1f}%)  blueprint {lo}-{hi}%  {'OK' if lo <= share <= hi else 'OUT OF RANGE'}")
    if short:
        print("Generators short of quota:", short)


if __name__ == "__main__":
    main()
