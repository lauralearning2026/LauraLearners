"""Make a printable teacher review book and a review tracker CSV.

Usage: python3 review.py OUTPUT_DIR
"""
import csv
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
bank = json.load(open(os.path.join(HERE, "..", "..", "public", "courses", "algebra-2", "bank.json")))
out = sys.argv[1]
os.makedirs(out, exist_ok=True)
CATS = bank["categories"]
L = "ABCDEF"

parts = []
cur = None
for q in bank["items"]:
    if q["category"] != cur:
        cur = q["category"]
        parts.append(f"<h2>{CATS[cur]}</h2>")
    keys = ", ".join(L[a] for a in q["answer"])
    opts = "".join(
        f"<li class='{'key' if i in q['answer'] else ''}'><b>{L[i]}.</b> <span>{c}</span><div class='why'>{q['rationales'][i]}</div></li>"
        for i, c in enumerate(q["choices"]))
    parts.append(
        f"<article><header><b>{q['id']}</b><span>{q['standard']}</span><span>{q['type']}</span><span>DOK {q['dok']}</span>"
        f"<span>{'No calculator' if q['calculator'] == 'N' else 'Calculator'}</span><span class='key'>Key: {keys}</span></header>"
        f"<div class='stem'>{q['stem']}</div><ol>{opts}</ol><p class='ex'><b>Explanation.</b> {q['explanation']}</p>"
        f"<p class='rev'>Reviewed ☐ &nbsp; Keep ☐ &nbsp; Edit ☐ &nbsp; Remove ☐ &nbsp; Notes: ____________________________</p></article>")

page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Algebra II Question Bank Review</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
 onload="renderMathInElement(document.body,{{delimiters:[{{left:'\\\\(',right:'\\\\)',display:false}}],throwOnError:false}})"></script>
<style>
body{{font:15px/1.5 Arial,Helvetica,sans-serif;color:#17231e;background:#f5f1e8;margin:0}}
main{{max-width:900px;margin:auto;padding:24px 16px 80px}}
h1{{margin:0 0 6px}} h2{{margin:48px 0 12px;padding-bottom:6px;border-bottom:2px solid #245b47;color:#245b47}}
article{{background:#fff;border:1px solid #c9c6bb;padding:18px 20px;margin:14px 0;break-inside:avoid}}
header{{display:flex;flex-wrap:wrap;gap:8px;font-size:12px;margin-bottom:10px}} header span{{background:#f5f1e8;padding:2px 8px;border:1px solid #ddd8cd}}
header .key{{background:#e4eddc;border-color:#245b47;font-weight:700}}
.stem{{font-size:16px;margin-bottom:8px}} ol{{list-style:none;padding:0;margin:0}} li{{padding:6px 8px;border:1px solid #eee;margin:4px 0}}
li.key{{background:#e4eddc;border-color:#245b47}} .why{{font-size:12px;color:#59625e}}
.ex{{font-size:13px;background:#faf8f2;padding:8px}} .rev{{font-size:12px;color:#59625e}}
table.data{{border-collapse:collapse;margin:8px 0}} table.data th,table.data td{{border:1px solid #c9c6bb;padding:4px 10px;text-align:center}}
svg{{max-width:100%;height:auto}} @media print{{body{{background:#fff}} article{{border-color:#999}}}}
</style></head><body><main>
<h1>Algebra II EOC Question Bank: Teacher Review</h1>
<p>{len(bank['items'])} original practice items aligned to the 2023–24 Tennessee Algebra II standards. The key is highlighted in green, and each choice shows why it is right or wrong.</p>
{''.join(parts)}
</main></body></html>"""
open(os.path.join(out, "algebra-2-review-book.html"), "w", encoding="utf-8").write(page)

plain = lambda s: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<svg.*?</svg>", "[graph]", s, flags=re.S)))).replace("\\(", "").replace("\\)", "").strip()
with open(os.path.join(out, "algebra-2-review-tracker.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["ID", "Category", "Standard", "Type", "DOK", "Calculator", "Question", "Key", "Correct answer", "Template", "Reviewed", "Decision", "Notes"])
    for q in bank["items"]:
        w.writerow([q["id"], CATS[q["category"]], q["standard"], q["type"], q["dok"], q["calculator"], plain(q["stem"]),
                    ", ".join(L[a] for a in q["answer"]), " | ".join(plain(q["choices"][a]) for a in q["answer"]), q["template"], "", "", ""])
print("wrote review book and tracker")
