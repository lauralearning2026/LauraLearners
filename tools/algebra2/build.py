"""Build the Algebra II practice bank.

Usage (from this folder):  python3 build.py
Writes public/courses/algebra-2/bank.json for the site and prints a
blueprint summary. Re-running gives the same items (fixed seed).
"""
import hashlib
import json
import os
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))
import common  # noqa: E402
import so, ei, fn, sp  # noqa: E402,F401  (registers generators)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(ROOT, "public", "courses", "algebra-2", "bank.json")
APP_OUT = os.path.join(ROOT, "practice-app", "lib", "bank-data.ts")
STD_NAMES = {
    "A2.N.RN.A.1": "Rational exponents", "A2.N.Q.A.1": "Units, scale and precision",
    "A2.A.SSE.A.1": "Interpreting expressions", "A2.A.APR.A.1": "Factor Theorem",
    "A2.A.APR.A.2": "Zeros of polynomials", "A2.N.M.A.1": "Matrix basics",
    "A2.N.M.A.2": "Matrix operations", "A2.N.M.A.3": "Augmented matrices",
    "A2.A.CED.A.1": "Creating equations and inequalities", "A2.A.CED.A.2": "Modeling with equations",
    "A2.A.CED.A.3": "Rearranging formulas", "A2.A.REI.A.1": "Reasoning while solving",
    "A2.A.REI.A.2": "Radical equations", "A2.A.REI.B.3": "Systems in context",
    "A2.A.REI.B.4": "Linear-quadratic systems", "A2.F.IF.A.1": "Key features from graphs",
    "A2.F.IF.A.2": "Average rate of change", "A2.F.IF.A.3": "Rewriting and scaling functions",
    "A2.F.IF.B.4": "Domain, range and asymptotes", "A2.F.IF.B.5": "Equivalent forms",
    "A2.F.IF.B.6": "Comparing functions", "A2.F.BF.A.1": "Building and composing functions",
    "A2.F.BF.A.2": "Sequences", "A2.F.BF.B.3": "Transformations", "A2.F.BF.B.4": "Inverse functions",
    "A2.F.LE.A.1": "Exponential equations and logs", "A2.F.LE.A.2": "Exponential vs. polynomial growth",
    "A2.S.ID.A.1": "Shape, center and spread", "A2.S.ID.A.2": "Normal distributions",
    "A2.S.ID.A.3": "Z-scores", "A2.S.ID.B.4": "Scatter plots and models",
    "A2.S.IC.A.1": "Types of studies", "A2.S.IC.A.2": "Bias in data collection",
    "A2.S.IC.A.3": "Evaluating conclusions", "A2.S.CP.A.1": "Independent events",
    "A2.S.CP.B.2": "Counting and probability", "A2.S.CP.B.3": "Law of Large Numbers",
    "A2.S.CP.C.4": "Conditional probability",
}
ORDER = ["SO", "EI", "FN", "SP"]
TARGET = {"SO": 0.275, "EI": 0.20, "FN": 0.30, "SP": 0.225}
BLUEPRINT = {"SO": (25, 30), "EI": (17, 23), "FN": (27, 33), "SP": (20, 28)}


IDS = os.path.join(HERE, "ids.json")


def signature(text):
    t = re.sub(r"<svg.*?</svg>", "", text, flags=re.S)
    t = re.sub(r"\\\(.*?\\\)", "#", t, flags=re.S)
    t = re.sub(r"<[^>]+>", "", t)
    t = re.sub(r"-?\d[\d,./]*%?", "#", t)
    t = re.sub(r"\$#", "#", t)
    return t.split(". ")[0].strip().rstrip(".")


def tag_errors(items):
    """Give every wrong choice a stable error-type id (template + rationale pattern)."""
    labels, counts = {}, {}
    for q in items:
        errs = []
        for i, r in enumerate(q["rationales"]):
            if i in q["answer"]:
                errs.append(None)
                continue
            sig = signature(r)
            eid = "e" + hashlib.sha1((q["template"] + "|" + sig).encode()).hexdigest()[:8]
            counts[eid] = counts.get(eid, 0) + 1
            if eid not in labels:
                labels[eid] = sig if "#" not in sig else r.split(". ")[0].rstrip(".")
            errs.append(eid)
        q["errors"] = errs
    # Only patterns that recur across items are worth tracking.
    keep = {k: v for k, v in labels.items() if counts[k] >= 4 and len(v) > 12 and not signature(v).startswith("#")}
    for q in items:
        q["errors"] = [e if e in keep else None for e in q["errors"]]
    return keep


def main():
    generated, report = common.run(seed=2026)
    hand = json.load(open(os.path.join(HERE, "handwritten.json")))
    seen = {common.stem_key(q) for q in generated}
    ordinal = {}
    for q in generated:
        k = ordinal.get(q["template"], 0) + 1
        ordinal[q["template"]] = k
        q["key"] = f"{q['template']}#{k}"
    hand = [dict(q, key="handwritten#" + q["id"]) for q in hand if common.stem_key(q) not in seen]
    items = generated + hand

    # IDs are locked: an item keeps its ID across rebuilds, and retired IDs are never reused.
    ids = json.load(open(IDS)) if os.path.exists(IDS) else {}
    nxt = max([int(v.split("-")[1]) for v in ids.values()] + [0]) + 1
    for q in items:
        if q["key"] not in ids:
            ids[q["key"]] = f"A2-{nxt:04d}"
            nxt += 1
        q["id"] = ids[q["key"]]
    with open(IDS, "w") as f:
        json.dump(ids, f, indent=0, sort_keys=True)
    items.sort(key=lambda q: q["id"])
    error_types = tag_errors(items)
    bank = {
        "course": "Algebra II",
        "exam": "TCAP Algebra II EOC (Tennessee)",
        "standards": "2023-24 Tennessee Academic Standards for Mathematics, Algebra II",
        "note": "Original practice items. Not official TCAP items. Answer keys are computed by the generators in tools/algebra2.",
        "categories": {"SO": "Structure and Operations", "EI": "Equations and Inequalities",
                       "FN": "Functions", "SP": "Statistics and Probability"},
        "errorTypes": error_types,
        "items": [{k: q[k] for k in ("id", "category", "standard", "type", "dok", "calculator", "stem", "choices",
                                     "answer", "explanation", "rationales", "errors", "template")} for q in items],
    }
    bases = sorted({".".join(q["standard"].split(".")[:5]) for q in items})
    missing = [b for b in bases if b not in STD_NAMES]
    if missing:
        raise SystemExit(f"Add names for new standards: {missing}")
    cat_of = {}
    for q in items:
        cat_of.setdefault(".".join(q["standard"].split(".")[:5]), q["category"])
    bank["standardList"] = [{"code": b, "name": STD_NAMES[b], "cat": cat_of[b]} for b in bases]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    os.makedirs(os.path.dirname(APP_OUT), exist_ok=True)
    with open(APP_OUT, "w", encoding="utf-8") as f:
        f.write("// Generated by tools/algebra2/build.py. Do not edit by hand.\n")
        f.write("export const BANK_JSON: string = " + json.dumps(json.dumps(bank, ensure_ascii=False, separators=(",", ":"))) + ";\n")
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
