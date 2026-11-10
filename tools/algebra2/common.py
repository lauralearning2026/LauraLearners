"""Shared helpers for generating Algebra II practice items.

Every generator computes its own answer key from randomly chosen
parameters, so answers are never typed by hand. Distractors are built
from named student errors, and each one carries a short rationale.
"""
from __future__ import annotations

import math
import random
import re
from fractions import Fraction as F

CATEGORY = {
    "A2.N.RN": "SO", "A2.N.Q": "SO", "A2.A.SSE": "SO", "A2.A.APR": "SO",
    "A2.N.M.A.1": "SO", "A2.N.M.A.2": "SO", "A2.N.M.A.3": "EI",
    "A2.A.CED": "EI", "A2.A.REI": "EI",
    "A2.F.": "FN",
    "A2.S.": "SP",
}


def category_of(std: str) -> str:
    best = ""
    for prefix in CATEGORY:
        if std.startswith(prefix) and len(prefix) > len(best):
            best = prefix
    if not best:
        raise ValueError(f"no category for {std}")
    return CATEGORY[best]


class Skip(Exception):
    """Raised when random parameters give an unusable item."""


# ----------------------------------------------------------------- formatting

def M(s: str) -> str:
    """Wrap LaTeX for inline rendering."""
    return r"\(" + s + r"\)"


def num(x) -> str:
    """LaTeX for an int, Fraction or float."""
    if isinstance(x, F):
        if x.denominator == 1:
            return str(x.numerator)
        sign = "-" if x < 0 else ""
        return rf"{sign}\frac{{{abs(x.numerator)}}}{{{x.denominator}}}"
    if isinstance(x, float):
        if abs(x - round(x)) < 1e-9:
            return str(int(round(x)))
        s = f"{x:.6f}".rstrip("0").rstrip(".")
        return s
    return str(x)


def money(x: float, cents: bool | None = None) -> str:
    if cents is None:
        cents = abs(x - round(x)) > 1e-9
    s = f"{x:,.2f}" if cents else f"{round(x):,}"
    return "$" + s


def comma(n: int) -> str:
    return f"{n:,}"


def coef_term(c, power: int, var: str = "x", first: bool = False) -> str:
    """One polynomial term with sign handling. Returns '' for c == 0."""
    if c == 0:
        return ""
    neg = c < 0
    a = abs(c)
    if power == 0:
        body = num(a)
    else:
        coef = "" if a == 1 else num(a)
        body = coef + (var if power == 1 else f"{var}^{{{power}}}")
    if first:
        return ("-" if neg else "") + body
    return (" - " if neg else " + ") + body


def poly(coeffs, var: str = "x") -> str:
    """coeffs listed from highest power to the constant."""
    n = len(coeffs) - 1
    out = ""
    for i, c in enumerate(coeffs):
        t = coef_term(c, n - i, var, first=(out == ""))
        out += t
    return out or "0"


def lin(a, b, var: str = "x") -> str:
    return poly([a, b], var)


def factor(r, var: str = "x") -> str:
    """(x - r) written cleanly."""
    if r == 0:
        return var
    return f"({var} {'-' if r > 0 else '+'} {num(abs(r))})"


def signed(n) -> str:
    """'+ 3' or '- 3' for appending to an expression."""
    return ("- " if n < 0 else "+ ") + num(abs(n))


def pt(x, y) -> str:
    return f"({num(x)}, {num(y)})"


def pct(p: float, digits: int = 1) -> str:
    v = round(p * 100, digits)
    s = f"{v:.{digits}f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s + "%"


def ordinal(n: int) -> str:
    if 10 <= n % 100 <= 20:
        suf = "th"
    else:
        suf = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suf}"


def article(word: str) -> str:
    return ("an " if word[:1].lower() in "aeiou8" else "a ") + word


# ------------------------------------------------------------------ assembly

def _norm(s: str) -> str:
    s = re.sub(r"llc\d+", "llc", s)
    return "".join(s.split()).lower()


def mc(std, dok, calc, stem, correct, distractors, explanation, rng,
       correct_why="Correct."):
    """Multiple choice with one key and three distractors.

    distractors: list of (text, why). Extra ones are dropped; duplicates
    of the key or of each other are removed first.
    """
    seen = {_norm(correct)}
    picked = []
    for text, why in distractors:
        k = _norm(text)
        if k in seen:
            continue
        seen.add(k)
        picked.append((text, why))
        if len(picked) == 3:
            break
    if len(picked) < 3:
        raise Skip("not enough distinct distractors")
    opts = [(correct, correct_why, True)] + [(t, w, False) for t, w in picked]
    rng.shuffle(opts)
    return {
        "category": category_of(std), "standard": std, "type": "MC",
        "dok": dok, "calculator": calc, "stem": stem,
        "choices": [o[0] for o in opts],
        "answer": [i for i, o in enumerate(opts) if o[2]],
        "explanation": explanation,
        "rationales": [o[1] for o in opts],
    }


def ms(std, dok, calc, stem, corrects, wrongs, explanation, rng, total=5,
       tell_count=True):
    """Multiple select. corrects/wrongs: lists of (text, why)."""
    seen = set()
    keep_c, keep_w = [], []
    for t, w in corrects:
        k = _norm(t)
        if k in seen:
            raise Skip("duplicate correct option")
        seen.add(k)
        keep_c.append((t, w))
    for t, w in wrongs:
        k = _norm(t)
        if k in seen:
            continue
        seen.add(k)
        keep_w.append((t, w))
        if len(keep_c) + len(keep_w) == total:
            break
    if len(keep_c) + len(keep_w) < total or len(keep_c) < 2:
        raise Skip("not enough options")
    opts = [(t, w, True) for t, w in keep_c] + [(t, w, False) for t, w in keep_w]
    rng.shuffle(opts)
    words = {2: "two", 3: "three", 4: "four"}
    note = (f" Select the <b>{words[len(keep_c)]}</b> correct answers."
            if tell_count else " Select <b>all</b> that apply.")
    return {
        "category": category_of(std), "standard": std, "type": "MS",
        "dok": dok, "calculator": calc, "stem": stem + note,
        "choices": [o[0] for o in opts],
        "answer": [i for i, o in enumerate(opts) if o[2]],
        "explanation": explanation,
        "rationales": [o[1] for o in opts],
    }


def table(header, rows, row_head=False) -> str:
    h = "".join(f"<th>{c}</th>" for c in header)
    body = ""
    for r in rows:
        cells = ""
        for j, c in enumerate(r):
            tag = "th" if (row_head and j == 0) else "td"
            cells += f"<{tag}>{c}</{tag}>"
        body += f"<tr>{cells}</tr>"
    return f"<table class='data'><tr>{h}</tr>{body}</table>"


def xy_table(xs, ys, xname="x", yname="y") -> str:
    """Horizontal input-output table."""
    r1 = f"<tr><th>{xname}</th>" + "".join(f"<td>{num(x)}</td>" for x in xs) + "</tr>"
    r2 = f"<tr><th>{yname}</th>" + "".join(f"<td>{num(y)}</td>" for y in ys) + "</tr>"
    return f"<table class='data'>{r1}{r2}</table>"


def bmatrix(rows) -> str:
    inner = r" \\ ".join(" & ".join(num(v) for v in r) for r in rows)
    return r"\begin{bmatrix} " + inner + r" \end{bmatrix}"


def augmented(rows) -> str:
    n = len(rows[0]) - 1
    spec = "c" * n + "|c"
    inner = r" \\ ".join(" & ".join(num(v) for v in r) for r in rows)
    return r"\left[\begin{array}{" + spec + "} " + inner + r" \end{array}\right]"


# ---------------------------------------------------------------------- SVG

_CLIP = 0
INK = "#17231e"
GRID = "#ddd8cd"
GREEN = "#245b47"
RED = "#a8442f"


def _fmt_tick(v):
    if abs(v - round(v)) < 1e-9:
        return str(int(round(v)))
    return f"{v:g}"


def svg_plot(funcs=(), xr=(-6, 6), yr=(-6, 6), xstep=1, ystep=1,
             points=(), open_points=(), width=300, height=300,
             xlabel=None, ylabel=None, label_every=None, dashed=(),
             axes_at_zero=True, title=None, styles=None):
    """Small coordinate-plane graph as inline SVG.

    funcs: callables f(x) -> float or None. Pieces break where None or
    outside the window. dashed: list of ('v', x) or ('h', y) asymptotes.
    """
    padL, padB, padT, padR = (46 if ylabel else 30), (40 if xlabel else 26), (26 if title else 10), 12
    W, H = width + padL + padR, height + padB + padT
    x0, x1 = xr
    y0, y1 = yr

    def X(x):
        return padL + (x - x0) / (x1 - x0) * width

    def Y(y):
        return padT + (y1 - y) / (y1 - y0) * height

    global _CLIP
    _CLIP += 1
    cid = f"llc{_CLIP}"
    parts = [f"<svg viewBox='0 0 {W:.0f} {H:.0f}' width='{W:.0f}' height='{H:.0f}' "
             f"role='img' xmlns='http://www.w3.org/2000/svg' style='max-width:100%;height:auto;display:block;margin:12px 0' "
             f"font-family='Arial, sans-serif' font-size='11'>"]
    if title:
        parts.append(f"<text x='{W/2:.1f}' y='16' text-anchor='middle' font-weight='700' font-size='12' fill='{INK}'>{title}</text>")
    # grid
    def steps(a, b, s):
        k = math.ceil(a / s - 1e-9)
        v = k * s
        out = []
        while v <= b + 1e-9:
            out.append(round(v, 10))
            v += s
        return out

    xs, ys = steps(x0, x1, xstep), steps(y0, y1, ystep)
    for v in xs:
        parts.append(f"<line x1='{X(v):.1f}' y1='{Y(y0):.1f}' x2='{X(v):.1f}' y2='{Y(y1):.1f}' stroke='{GRID}' stroke-width='1'/>")
    for v in ys:
        parts.append(f"<line x1='{X(x0):.1f}' y1='{Y(v):.1f}' x2='{X(x1):.1f}' y2='{Y(v):.1f}' stroke='{GRID}' stroke-width='1'/>")
    # axes
    ax_y = 0 if (axes_at_zero and y0 <= 0 <= y1) else y0
    ax_x = 0 if (axes_at_zero and x0 <= 0 <= x1) else x0
    parts.append(f"<line x1='{X(x0):.1f}' y1='{Y(ax_y):.1f}' x2='{X(x1):.1f}' y2='{Y(ax_y):.1f}' stroke='{INK}' stroke-width='1.6'/>")
    parts.append(f"<line x1='{X(ax_x):.1f}' y1='{Y(y0):.1f}' x2='{X(ax_x):.1f}' y2='{Y(y1):.1f}' stroke='{INK}' stroke-width='1.6'/>")
    le_x = label_every or max(1, round(len(xs) / 7))
    le_y = label_every or max(1, round(len(ys) / 7))
    for i, v in enumerate(xs):
        if i % le_x == 0 and not (abs(v - ax_x) < 1e-9 and ax_y == 0 and ax_x == 0 and v == 0 and False):
            parts.append(f"<text x='{X(v):.1f}' y='{Y(ax_y) + 13:.1f}' text-anchor='middle' fill='{INK}'>{_fmt_tick(v)}</text>")
    for i, v in enumerate(ys):
        if i % le_y == 0 and abs(v - ax_y) > 1e-9:
            parts.append(f"<text x='{X(ax_x) - 4:.1f}' y='{Y(v) + 4:.1f}' text-anchor='end' fill='{INK}'>{_fmt_tick(v)}</text>")
    if xlabel:
        parts.append(f"<text x='{padL + width/2:.1f}' y='{H - 6:.1f}' text-anchor='middle' fill='{INK}' font-weight='700'>{xlabel}</text>")
    if ylabel:
        parts.append(f"<text x='12' y='{padT + height/2:.1f}' text-anchor='middle' fill='{INK}' font-weight='700' transform='rotate(-90 12 {padT + height/2:.1f})'>{ylabel}</text>")
    for kind, v in dashed:
        if kind == "v":
            parts.append(f"<line x1='{X(v):.1f}' y1='{Y(y0):.1f}' x2='{X(v):.1f}' y2='{Y(y1):.1f}' stroke='{RED}' stroke-dasharray='5 4' stroke-width='1.4'/>")
        else:
            parts.append(f"<line x1='{X(x0):.1f}' y1='{Y(v):.1f}' x2='{X(x1):.1f}' y2='{Y(v):.1f}' stroke='{RED}' stroke-dasharray='5 4' stroke-width='1.4'/>")
    # curves
    for fi, f in enumerate(funcs):
        color, dash = (styles[fi] if styles and fi < len(styles) else (GREEN, None))
        n = 400
        seg = []
        segs = []
        prev = None
        for i in range(n + 1):
            x = x0 + (x1 - x0) * i / n
            try:
                y = f(x)
            except (ValueError, ZeroDivisionError, OverflowError):
                y = None
            if y is None or isinstance(y, complex) or not math.isfinite(y) or y < y0 - (y1 - y0) or y > y1 + (y1 - y0):
                if len(seg) > 1:
                    segs.append(seg)
                seg = []
                prev = None
                continue
            if prev is not None and abs(y - prev) > (y1 - y0) * 0.6:
                if len(seg) > 1:
                    segs.append(seg)
                seg = []
            seg.append((x, y))
            prev = y
        if len(seg) > 1:
            segs.append(seg)
        for s in segs:
            d = "M" + " L".join(f"{X(x):.1f},{Y(max(min(y, y1 + 1e3), y0 - 1e3)):.1f}" for x, y in s)
            dash_attr = f" stroke-dasharray='{dash}'" if dash else ""
            parts.append(f"<path d='{d}' fill='none' stroke='{color}' stroke-width='2.4'{dash_attr} clip-path='url(#{cid})'/>")
    for (px, py) in points:
        parts.append(f"<circle cx='{X(px):.1f}' cy='{Y(py):.1f}' r='3.6' fill='{GREEN}'/>")
    for (px, py) in open_points:
        parts.append(f"<circle cx='{X(px):.1f}' cy='{Y(py):.1f}' r='3.6' fill='white' stroke='{GREEN}' stroke-width='2'/>")
    parts.insert(1, f"<defs><clipPath id='{cid}'><rect x='{padL}' y='{padT}' width='{width}' height='{height}'/></clipPath></defs>")
    parts.append("</svg>")
    return "".join(parts)


def svg_curve_shape(kind: str, width=260, height=110) -> str:
    """Density curve sketch: 'symmetric', 'right', 'left', 'uniform'."""
    pts = []
    for i in range(101):
        t = i / 100
        if kind == "symmetric":
            y = math.exp(-((t - 0.5) ** 2) / 0.02)
        elif kind == "right":
            y = (t ** 1.2) * math.exp(-t * 7) * 9.5
        elif kind == "left":
            u = 1 - t
            y = (u ** 1.2) * math.exp(-u * 7) * 9.5
        else:
            y = 0.6 if 0.05 <= t <= 0.95 else 0
        pts.append((t, y))
    peak = max(p[1] for p in pts) or 1
    pad = 10
    d = "M" + " L".join(f"{pad + t * (width - 2 * pad):.1f},{height - pad - y / peak * (height - 2 * pad) * 0.92:.1f}" for t, y in pts)
    return (f"<svg viewBox='0 0 {width} {height}' width='{width}' height='{height}' xmlns='http://www.w3.org/2000/svg' "
            f"style='max-width:100%;height:auto;display:block;margin:10px 0' role='img'>"
            f"<line x1='{pad}' y1='{height - pad}' x2='{width - pad}' y2='{height - pad}' stroke='{INK}' stroke-width='1.4'/>"
            f"<path d='{d}' fill='rgba(36,91,71,.12)' stroke='{GREEN}' stroke-width='2.2'/></svg>")


# ------------------------------------------------------------------- runner

REGISTRY: list[tuple[str, int, callable, bool]] = []


def gen(std: str, quota: int, by_choices: bool = False):
    """Register a generator for a standard with a target number of items.

    by_choices: treat items with the same stem but different option sets
    as different (for fixed-stem select-all items).
    """
    def wrap(fn):
        REGISTRY.append((std, quota, fn, by_choices))
        return fn
    return wrap


def item_key(item) -> str:
    return _norm(item["stem"]) + "|" + "|".join(sorted(_norm(c) for c in item["choices"]))


def stem_key(item) -> str:
    return _norm(item["stem"])


def run(seed: int = 2026):
    """Run every registered generator up to its quota. Returns item list."""
    out = []
    seen = set()
    report = []
    for std, quota, fn, by_choices in REGISTRY:
        rng = random.Random(f"{seed}-{fn.__name__}")
        got = 0
        tries = 0
        while got < quota and tries < quota * 80:
            tries += 1
            try:
                item = fn(rng)
            except Skip:
                continue
            k = item_key(item) if by_choices else stem_key(item)
            if k in seen:
                continue
            assert item["standard"].startswith(std), (fn.__name__, item["standard"], std)
            seen.add(k)
            item["template"] = fn.__name__
            out.append(item)
            got += 1
        report.append((fn.__name__, std, quota, got))
    return out, report
