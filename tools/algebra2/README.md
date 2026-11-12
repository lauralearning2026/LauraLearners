# Algebra II question bank tools

These scripts build `public/courses/algebra-2/bank.json`, the 1,000-item practice bank used by `/courses/algebra-2`.

- `so.py`, `ei.py`, `fn.py`, `sp.py`: generators for the four TCAP reporting categories. Each generator picks random numbers, computes the answer, and builds distractors from common student errors.
- `handwritten.json`: the original hand-written items, kept alongside the generated ones.
- `build.py`: builds the bank (fixed seed, so the same items every time) and prints the blueprint balance.
- `check.py`: checks the built bank for structural problems, formatting glitches, duplicates, and distractors equal to the key.
- `review.py OUTPUT_DIR`: writes a printable review book (HTML) and a review tracker (CSV).
- `ids.json`: locked question IDs. An item keeps its ID across rebuilds (keyed by generator and position), and IDs are never reused.

The build also writes `practice-app/lib/bank-data.ts` for the practice app, and tags each wrong choice with an error type (`errorTypes` in the bank) so the app can spot repeated mistakes.

To rebuild after editing a generator:

```
cd tools/algebra2
python3 build.py && python3 check.py
```
