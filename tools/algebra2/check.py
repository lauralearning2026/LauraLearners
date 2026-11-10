"""Independent checks on the built bank. Exit code 1 if anything fails."""
import json
import os
import re
import sys
from collections import Counter, defaultdict
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
BANK = os.path.join(HERE, "..", "..", "public", "courses", "algebra-2", "bank.json")
bank = json.load(open(BANK))
items = bank["items"]
problems = defaultdict(list)


def math_segments(s):
    return re.findall(r"\\\((.*?)\\\)", s, flags=re.S)


def balanced(seg):
    depth = 0
    i = 0
    while i < len(seg):
        ch = seg[i]
        if ch == "\\" and i + 1 < len(seg) and seg[i + 1] in "{}":
            i += 2
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth < 0:
                return False
        i += 1
    return depth == 0


def as_number(text):
    t = re.sub(r"<[^>]+>", "", text)
    t = t.replace("\\(", "").replace("\\)", "").replace("$", "").replace(",", "").replace("{,}", "").strip()
    t = re.sub(r"\s*(%|[a-zA-Z ]+)$", "", t).strip()
    m = re.fullmatch(r"(-?)\\frac\{(\d+)\}\{(\d+)\}", t)
    if m:
        v = Fraction(int(m.group(2)), int(m.group(3)))
        return -v if m.group(1) else v
    try:
        return Fraction(t)
    except (ValueError, ZeroDivisionError):
        return None


ids = Counter(q["id"] for q in items)
for q in items:
    qid = q["id"]
    n = len(q["choices"])
    if len(q["rationales"]) != n:
        problems[qid].append("rationales count")
    if q["type"] == "MC" and len(q["answer"]) != 1:
        problems[qid].append("MC must have one key")
    if q["type"] == "MS" and len(q["answer"]) < 2:
        problems[qid].append("MS needs two or more keys")
    if not all(0 <= a < n for a in q["answer"]):
        problems[qid].append("answer index out of range")
    if n < 4:
        problems[qid].append("fewer than 4 choices")
    norm = ["".join(c.split()).lower() for c in q["choices"]]
    if len(set(norm)) != n:
        problems[qid].append("duplicate choice text")
    texts = [q["stem"], q["explanation"]] + q["choices"] + q["rationales"]
    for t in texts:
        plain = re.sub(r"<svg.*?</svg>", "", t, flags=re.S)
        for word in ("None", "nan", "inf", "NaN"):
            if re.search(rf"\b{word}\b", plain):
                problems[qid].append(f"suspicious word '{word}'")
        for bad in ("{M(", "{num(", "{signed(", "\\\\(", "[]", "+ -", "- -", "+ +"):
            if bad in plain:
                if bad in ("+ -", "- -", "+ +"):
                    segs = math_segments(t)
                    if any(bad in s for s in segs):
                        problems[qid].append(f"sign glitch '{bad}'")
                    continue
                problems[qid].append(f"suspicious text '{bad}'")
        if t.count("\\(") != t.count("\\)"):
            problems[qid].append("unmatched math delimiters")
        for seg in math_segments(t):
            if not balanced(seg):
                problems[qid].append("unbalanced braces in math")
    # numeric distractor equal to the key
    nums = [None if "<svg" in c else as_number(c) for c in q["choices"]]
    for a in q["answer"]:
        if nums[a] is None:
            continue
        for i, v in enumerate(nums):
            if i not in q["answer"] and v is not None and v == nums[a]:
                problems[qid].append(f"distractor {i} equals the key numerically")
    if q["calculator"] not in ("Y", "N") or q["dok"] not in (1, 2, 3):
        problems[qid].append("metadata")

dupe_ids = [k for k, v in ids.items() if v > 1]
stems = Counter("".join(re.sub(r"llc\\d+", "", q["stem"]).split()) + "|" + "|".join(sorted(re.sub(r"llc\\d+", "", c) for c in q["choices"])) for q in items)
dupes = sum(v - 1 for v in stems.values() if v > 1)

print(f"Checked {len(items)} items.")
print(f"Duplicate ids: {len(dupe_ids)}; duplicate questions: {dupes}")
key_pos = Counter(q["answer"][0] for q in items if q["type"] == "MC")
print("MC key position spread:", dict(sorted(key_pos.items())))
print("Types:", dict(Counter(q["type"] for q in items)), " DOK:", dict(sorted(Counter(q["dok"] for q in items).items())),
      " Calculator:", dict(Counter(q["calculator"] for q in items)))
std = Counter(q["standard"].rsplit(".", 1)[0] if q["standard"].count(".") > 4 else q["standard"] for q in items)
print("Standards covered:", len(std))
if problems:
    print(f"\n{len(problems)} items with problems:")
    for k, v in list(problems.items())[:60]:
        print(" ", k, sorted(set(v)))
    sys.exit(1)
print("No problems found.")
