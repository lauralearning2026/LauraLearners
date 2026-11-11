"""Equations and Inequalities generators (blueprint category EI)."""
import math

from common import (F, M, Skip, augmented, coef_term, comma, factor, gen, lin, mc, money,
                    ms, num, pct, poly, pt, signed)


def eq2(a, b, c, x="x", y="y"):
    """ax + by = c as LaTeX."""
    return coef_term(a, 1, x, first=True) + coef_term(b, 1, y, first=(a == 0)) + f" = {c}"


# ================================================== A2.N.M.A.3 augmented
@gen("A2.N.M.A.3", 12)
def aug_from_system(rng):
    a, b, c, d = [rng.choice([k for k in range(-6, 7) if k != 0]) for _ in range(4)]
    x0, y0 = rng.randint(-5, 6), rng.randint(-5, 6)
    if a * d - b * c == 0 or (a, b) == (c, d) or len({a, b, c, d}) < 3:
        raise Skip
    e, f = a * x0 + b * y0, c * x0 + d * y0
    s1, s2 = eq2(a, b, e), eq2(c, d, f)
    stem = f"Which augmented matrix represents this system of equations?<p>{M(s1)}<br>{M(s2)}</p>"
    ans = augmented([[a, b, e], [c, d, f]])
    ds = [(augmented([[a, c, e], [b, d, f]]), "Wrote the coefficients by column instead of by equation."),
          (augmented([[e, b, a], [f, d, c]]), "The constants belong in the last column, after the bar."),
          (augmented([[a, -b, e], [c, d, f]]), "Lost a negative sign or changed a sign on a coefficient."),
          (augmented([[a, b, -e], [c, d, -f]]), "The constants keep their signs when the equation is in the form ax + by = c.")]
    return mc("A2.N.M.A.3", 1, "N", stem, M(ans), [(M(t), w) for t, w in ds],
              "Each row is one equation: the x-coefficient, the y-coefficient, then the constant after the bar.", rng)


@gen("A2.N.M.A.3", 8)
def aug_interpret(rng):
    (n1, n2), (p1, p2), unit = rng.choice([
        (("adult tickets", "student tickets"), (12, 7), "tickets"),
        (("large pizzas", "small pizzas"), (15, 9), "pizzas"),
        (("hardcover books", "paperback books"), (18, 8), "books"),
        (("bags of mulch", "bags of soil"), (6, 4), "bags")])
    x0, y0 = rng.randint(12, 60), rng.randint(12, 60)
    if x0 == y0:
        raise Skip
    total, money_ = x0 + y0, p1 * x0 + p2 * y0
    stem = (f"A store sold {total} {unit}: {n1} for {money(p1)} each and {n2} for {money(p2)} each, for a total of {money(money_)}. "
            f"Let {M('x')} be the number of {n1} and {M('y')} the number of {n2}. The augmented matrix for the system reduces to "
            f"{M(augmented([[1, 0, x0], [0, 1, y0]]))}. What does this mean?")
    ans = f"The store sold {x0} {n1} and {y0} {n2}."
    ds = [(f"The store sold {y0} {n1} and {x0} {n2}.", "The first column is x, the second is y."),
          (f"The store sold {x0} {n1} for {money(y0)} each.", "The last column gives the values of x and y, not prices."),
          (f"The system has no solution.", "A row of the form [1 0 | a] gives a solution."),
          (f"The store sold {x0 + y0} {n1}.", f"{x0 + y0} is the total of both kinds.")]
    return mc("A2.N.M.A.3", 2, "Y", stem, ans, ds,
              f"Row 1 says {M(f'x = {x0}')} and row 2 says {M(f'y = {y0}')}. Check: {x0} + {y0} = {total} and "
              f"{p1}({x0}) + {p2}({y0}) = {comma(money_)}.", rng)


# ===================================================== A2.A.CED.A.1
GROW = [("population of a town", "people", "years"), ("number of members in a club", "members", "months"),
        ("number of visitors to a website each day", "visitors", "weeks"), ("value of a rare coin", "dollars", "years"),
        ("balance in an account", "dollars", "years")]
DECAY = [("value of a truck", "dollars", "years"), ("amount of a medicine in the body", "milligrams", "hours"),
         ("number of fish in a lake", "fish", "years"), ("charge in a phone battery", "percent", "hours")]


@gen("A2.A.CED.A.1", 12)
def ced_exp_inequality(rng):
    grow = rng.random() < 0.55
    what, unit, tu = rng.choice(GROW if grow else DECAY)
    a = rng.choice([400, 800, 1500, 2400, 5000, 12000, 25000] if unit != "percent" else [100])
    r = rng.choice([0.03, 0.04, 0.05, 0.06, 0.08, 0.1, 0.12, 0.15])
    b = round(1 + r if grow else 1 - r, 2)
    target = round(a * (rng.choice([1.5, 2, 3]) if grow else rng.choice([0.5, 0.4, 0.25])))
    sym = ">" if grow else "<"
    word = "more than" if grow else "less than"
    stem = (f"The {what} is {comma(a)} {unit} and {'increases' if grow else 'decreases'} by {pct(r, 0)} each {tu[:-1]}. "
            f"Which inequality can be used to find the number of {tu}, {M('t')}, until the {what} is {word} {comma(target)}?")
    A = comma(a).replace(",", "{,}")
    T = comma(target).replace(",", "{,}")
    ans = f"{A}({b})^{{t}} {sym} {T}"
    wb = round(1 - r if grow else 1 + r, 2)
    ds = [(f"{A}({num(r)})^{{t}} {sym} {T}", f"The base must be {M(f'1 {'+' if grow else '-'} {num(r)}')}, not the rate alone."),
          (f"{A}({wb})^{{t}} {sym} {T}", f"{'An increase' if grow else 'A decrease'} of {pct(r, 0)} uses the factor {b}."),
          (f"{A} {'+' if grow else '-'} {num(r)}t {sym} {T}", "This is a linear model; a percent change each period is exponential."),
          (f"{A}({b})^{{t}} {'<' if grow else '>'} {T}", "The inequality symbol points the wrong way.")]
    return mc("A2.A.CED.A.1", 2, "Y", stem, M(ans), [(M(t), w) for t, w in ds],
              f"A {pct(r, 0)} {'increase' if grow else 'decrease'} multiplies the amount by {b} each {tu[:-1]}, so the amount is "
              f"{M(f'{A}({b})^{{t}}')}. We want it {word} {comma(target)}.", rng)


@gen("A2.A.CED.A.1", 8)
def ced_exp_solve(rng):
    grow = rng.random() < 0.5
    what, unit, tu = rng.choice(GROW if grow else DECAY)
    a = rng.choice([500, 1200, 2000, 8000, 15000, 30000] if unit != "percent" else [100])
    r = rng.choice([0.05, 0.06, 0.08, 0.1, 0.12, 0.15, 0.2])
    b = 1 + r if grow else 1 - r
    target = a * (rng.choice([2, 3]) if grow else rng.choice([0.5, 0.25]))
    n = 0
    v = a
    while (v <= target if grow else v >= target):
        n += 1
        v *= b
        if n > 60:
            raise Skip
    lin_n = math.ceil(abs(target - a) / (a * r))
    word = "more than" if grow else "less than"
    stem = (f"The {what} starts at {comma(a)} {unit} and {'increases' if grow else 'decreases'} by {pct(r, 0)} each {tu[:-1]}. "
            f"After how many whole {tu} will it first be {word} {comma(round(target))} {unit}?")
    ds = [(str(n - 1), f"After {n - 1} {tu} the amount is about {comma(round(a * b ** (n - 1)))}, which is not yet {word} {comma(round(target))}."),
          (str(lin_n) if lin_n != n else str(n + 2), f"Used a linear model, changing by {pct(r, 0)} of the starting amount each {tu[:-1]}."),
          (str(n + 1), "One more than needed."),
          (str(round(1 / r)), "Divided 1 by the rate; that does not account for compounding.")]
    return mc("A2.A.CED.A.1", 2, "Y", stem, str(n), ds,
              f"Solve {M(f'{comma(a)}({num(round(b, 2))})^{{t}} {">" if grow else "<"} {comma(round(target))}')}. "
              f"After {n} {tu} the amount is about {comma(round(a * b ** n))}, and after {n - 1} it is about {comma(round(a * b ** (n - 1)))}.", rng)


@gen("A2.A.CED.A.1", 10)
def ced_quadratic_create(rng):
    kind = rng.choice(["rect", "rect", "border", "consecutive"])
    if kind == "rect":
        w = rng.randint(4, 20)
        k = rng.randint(2, 9)
        mode = rng.choice(["more", "less2"])
        if mode == "more":
            L = w + k
            stem = f"The length of a rectangular garden is {k} feet more than its width, {M('w')}. The area is {w * L} square feet. Which equation can be used to find {M('w')}?"
            ans = f"w(w + {k}) = {w * L}"
            ds = [(f"w + (w + {k}) = {w * L}", "Added the sides; area is length times width."),
                  (f"2w + 2(w + {k}) = {w * L}", "That is the perimeter, not the area."),
                  (f"w(w - {k}) = {w * L}", f"The length is {k} feet more, so add {k}."),
                  (f"{k}w = {w * L}", "The length is not k times the width.")]
            expl = f"Area = width × length = {M(f'w(w + {k})')}, which must equal {w * L}. (The width is {w} feet.)"
        else:
            L = 2 * w - k
            if L <= 0:
                raise Skip
            stem = f"The length of a rectangular poster is {k} inches less than twice its width, {M('w')}. The area is {w * L} square inches. Which equation can be used to find {M('w')}?"
            ans = f"w(2w - {k}) = {w * L}"
            ds = [(f"w(2 - {k}w) = {w * L}", "Translate “twice the width” as 2w."),
                  (f"w({k} - 2w) = {w * L}", f"“{k} less than twice the width” is {M(f'2w - {k}')}."),
                  (f"2w(w - {k}) = {w * L}", f"The length is {M(f'2w - {k}')}, not {M(f'2(w - {k})')}."),
                  (f"2w + 2(2w - {k}) = {w * L}", "That is the perimeter, not the area.")]
            expl = f"The length is {M(f'2w - {k}')}, so area = {M(f'w(2w - {k})')}. (The width is {w} inches.)"
    elif kind == "border":
        L, W = rng.choice([(10, 8), (12, 9), (20, 15), (16, 12), (24, 18)])
        x = rng.randint(1, 4)
        A = (L + 2 * x) * (W + 2 * x)
        stem = (f"A {L}-foot by {W}-foot pool is surrounded by a deck of uniform width {M('x')} feet. The pool and deck together cover "
                f"{A} square feet. Which equation can be used to find {M('x')}?")
        ans = f"({L} + 2x)({W} + 2x) = {A}"
        ds = [(f"({L} + x)({W} + x) = {A}", "The deck adds x on both sides, so each dimension grows by 2x."),
              (f"({L} - 2x)({W} - 2x) = {A}", "The deck is outside the pool, so the dimensions increase."),
              (f"{L}({W}) + 2x = {A}", "The deck area is not just 2x."),
              (f"2({L} + 2x) + 2({W} + 2x) = {A}", "That is the outside perimeter, not the area.")]
        expl = f"Each dimension increases by {M('2x')}: {M(f'({L} + 2x)({W} + 2x) = {A}')}. (The deck is {x} feet wide.)"
    else:
        n = rng.randint(3, 25)
        par = rng.choice(["consecutive", "consecutive even", "consecutive odd"])
        step = 1 if par == "consecutive" else 2
        if par == "consecutive even" and n % 2:
            n += 1
        if par == "consecutive odd" and n % 2 == 0:
            n += 1
        P = n * (n + step)
        stem = f"The product of two positive {par} integers is {P}. If {M('n')} is the smaller integer, which equation can be used to find {M('n')}?"
        ans = f"n(n + {step}) = {P}"
        wrong = 1 if step == 2 else 2
        ds = [(f"n(n + {wrong}) = {P}", f"{par.capitalize()} integers differ by {step}."),
              (f"n + (n + {step}) = {P}", "That is the sum, not the product."),
              (f"n^{{2}} = {P}", "The two integers are different, so the product is not a square."),
              (f"n^{{2}} + {step} = {P}", f"{M(f'n(n + {step})')} expands to {M(f'n^{{2}} + {step}n')}, not {M(f'n^{{2}} + {step}')}.")]
        expl = f"The integers are {M('n')} and {M(f'n + {step}')}, so {M(f'n(n + {step}) = {P}')}. (They are {n} and {n + step}.)"
    return mc("A2.A.CED.A.1", 2, "Y", stem, M(ans), [(M(t), w) for t, w in ds], expl, rng)


# ===================================================== A2.A.CED.A.2
@gen("A2.A.CED.A.2", 10)
def ced2_exp_model(rng):
    grow = rng.random() < 0.5
    what, unit, tu = rng.choice(GROW if grow else DECAY)
    a = rng.choice([300, 600, 1500, 4000, 9000, 20000] if unit != "percent" else [100])
    r = rng.choice([0.02, 0.04, 0.05, 0.07, 0.09, 0.11, 0.18, 0.25])
    b = round(1 + r if grow else 1 - r, 2)
    A = comma(a).replace(",", "{,}")
    stem = (f"The {what} is {comma(a)} {unit} now and {'grows' if grow else 'decreases'} by {pct(r, 0)} each {tu[:-1]}. "
            f"Which equation models the {what}, {M('y')}, after {M('x')} {tu}?")
    ans = f"y = {A}({b})^{{x}}"
    ds = [(f"y = {A}({round(1 - r if grow else 1 + r, 2)})^{{x}}", f"{'Growth' if grow else 'Decay'} of {pct(r, 0)} uses {b}."),
          (f"y = {A}({num(r)})^{{x}}", f"The base is {M(f'1 {'+' if grow else '-'} {num(r)}')}."),
          (f"y = {A} {'+' if grow else '-'} {num(r)}x", "A constant percent change is exponential, not linear."),
          (f"y = {num(b)}({A})^{{x}}", "The starting amount is the coefficient and the growth factor is the base.")]
    return mc("A2.A.CED.A.2", 2, "Y", stem, M(ans), [(M(t), w) for t, w in ds],
              f"Start at {comma(a)} and multiply by {b} each {tu[:-1]}: {M(ans)}.", rng)


@gen("A2.A.CED.A.2", 10)
def ced2_budget(rng):
    (n1, p1), (n2, p2) = rng.sample([("sandwiches", 6), ("salads", 8), ("drinks", 2), ("snacks", 3), ("tickets", 12),
                                      ("posters", 5), ("pens", 2), ("notebooks", 4), ("plants", 9), ("pots", 7)], 2)
    if p1 == p2:
        raise Skip
    B = p1 * p2 * rng.randint(2, 5)
    stem = (f"A club can spend at most {money(B)} on {n1} that cost {money(p1)} each and {n2} that cost {money(p2)} each. "
            f"Let {M('x')} be the number of {n1} and {M('y')} the number of {n2}. ")
    mode = rng.choice(["which_ineq", "which_point"])
    if mode == "which_ineq":
        stem += "Which inequality represents this situation?"
        ans = M(f"{p1}x + {p2}y \\le {B}")
        ds = [(M(f"{p1}x + {p2}y \\ge {B}"), "“At most” means less than or equal to."),
              (M(f"{p2}x + {p1}y \\le {B}"), f"The price of {n1} goes with {M('x')}."),
              (M(f"x + y \\le {B}"), "Each item must be multiplied by its price."),
              (M(f"{p1}x + {p2}y < {B}"), "Spending exactly the budget is allowed, so use ≤.")]
        expl = f"Cost = {M(f'{p1}x + {p2}y')}, and it can be at most {B}: {M(f'{p1}x + {p2}y \\le {B}')}."
        return mc("A2.A.CED.A.2", 2, "Y", stem, ans, ds, expl, rng)
    good = []
    bad = []
    for x in range(0, B // p1 + 3):
        for y in range(0, B // p2 + 3):
            if x == 1 or y == 1:
                continue
            (good if p1 * x + p2 * y <= B else bad).append((x, y))
    edge = [(x, y) for (x, y) in good if p1 * x + p2 * y > B - min(p1, p2)]
    if not edge:
        raise Skip
    ans_pt = rng.choice(edge)
    over = [(x, y) for (x, y) in bad if p1 * x + p2 * y <= B + max(p1, p2) * 2]
    if len(over) < 3:
        raise Skip
    rng.shuffle(over)
    stem += f"Which combination can the club buy?"
    ds = [(f"{x} {n1} and {y} {n2}", f"That costs {money(p1 * x + p2 * y)}, which is more than {money(B)}.") for x, y in over[:3]]
    ax, ay = ans_pt
    return mc("A2.A.CED.A.2", 2, "Y", stem, f"{ax} {n1} and {ay} {n2}", ds,
              f"Check {M(f'{p1}x + {p2}y \\le {B}')}: {p1}({ax}) + {p2}({ay}) = {p1 * ax + p2 * ay}, which is at most {B}.", rng)


# ===================================================== A2.A.CED.A.3
FORMULAS = [
    ("the area of a circle", "A = \\pi r^{2}", "r", "r = \\sqrt{\\frac{A}{\\pi}}",
     [("r = \\frac{A}{2\\pi}", "Divided by 2 instead of taking the square root."), ("r = \\sqrt{A\\pi}", "Multiply by π? No: divide both sides by π."),
      ("r = \\frac{\\sqrt{A}}{\\pi^{2}}", "Squared π instead of leaving it under the root.")]),
    ("the volume of a cube", "V = s^{3}", "s", "s = \\sqrt[3]{V}",
     [("s = \\frac{V}{3}", "Divided by 3 instead of taking the cube root."), ("s = \\sqrt{V}", "The inverse of cubing is the cube root."), ("s = V^{3}", "Cubed instead of taking the cube root.")]),
    ("the volume of a sphere", "V = \\frac{4}{3}\\pi r^{3}", "r", "r = \\sqrt[3]{\\frac{3V}{4\\pi}}",
     [("r = \\sqrt[3]{\\frac{4V}{3\\pi}}", "Multiplied by 4/3 instead of by its reciprocal, 3/4."), ("r = \\frac{3V}{4\\pi}", "Forgot the cube root."),
      ("r = \\sqrt{\\frac{3V}{4\\pi}}", "Used a square root; r is cubed.")]),
    ("the volume of a cylinder", "V = \\pi r^{2}h", "r", "r = \\sqrt{\\frac{V}{\\pi h}}",
     [("r = \\frac{V}{2\\pi h}", "Divided by 2 instead of taking the square root."), ("r = \\sqrt{V\\pi h}", "Divide by πh; do not multiply."),
      ("r = \\sqrt{\\frac{V}{\\pi}} - h", "h multiplies; it must be divided out, not subtracted.")]),
    ("the volume of a cylinder", "V = \\pi r^{2}h", "h", "h = \\frac{V}{\\pi r^{2}}",
     [("h = V - \\pi r^{2}", "πr² multiplies h; divide instead of subtracting."), ("h = \\frac{\\pi r^{2}}{V}", "The fraction is upside down."),
      ("h = \\frac{V}{2\\pi r}", "r is squared, not doubled.")]),
    ("kinetic energy", "K = \\frac{1}{2}mv^{2}", "v", "v = \\sqrt{\\frac{2K}{m}}",
     [("v = \\sqrt{\\frac{K}{2m}}", "Dividing by 1/2 is multiplying by 2."), ("v = \\frac{2K}{m}", "Forgot the square root."),
      ("v = \\sqrt{2Km}", "Divide by m; do not multiply.")]),
    ("kinetic energy", "K = \\frac{1}{2}mv^{2}", "m", "m = \\frac{2K}{v^{2}}",
     [("m = \\frac{K}{2v^{2}}", "Dividing by 1/2 is multiplying by 2."), ("m = 2Kv^{2}", "Divide by v²; do not multiply."),
      ("m = \\frac{2K}{v}", "v is squared.")]),
    ("the Pythagorean Theorem", "a^{2} + b^{2} = c^{2}", "b", "b = \\sqrt{c^{2} - a^{2}}",
     [("b = c - a", "Square roots do not distribute over subtraction."), ("b = \\sqrt{c^{2} + a^{2}}", "Subtract a² from both sides."),
      ("b = c^{2} - a^{2}", "Forgot the square root.")]),
    ("the surface area of a cube", "S = 6s^{2}", "s", "s = \\sqrt{\\frac{S}{6}}",
     [("s = \\frac{\\sqrt{S}}{36}", "Took the square root of 36 instead of dividing by 6 first."), ("s = \\frac{S}{12}", "Divided by 2 instead of taking the square root."),
      ("s = \\sqrt{6S}", "Divide by 6; do not multiply.")]),
    ("the distance an object falls", "d = \\frac{1}{2}gt^{2}", "t", "t = \\sqrt{\\frac{2d}{g}}",
     [("t = \\sqrt{\\frac{d}{2g}}", "Dividing by 1/2 is multiplying by 2."), ("t = \\frac{2d}{g}", "Forgot the square root."),
      ("t = \\sqrt{2dg}", "Divide by g; do not multiply.")]),
    ("the period of a pendulum", "T = 2\\pi\\sqrt{\\frac{L}{g}}", "L", "L = g\\left(\\frac{T}{2\\pi}\\right)^{2}",
     [("L = \\frac{gT}{2\\pi}", "Undo the square root by squaring."), ("L = \\frac{1}{g}\\left(\\frac{T}{2\\pi}\\right)^{2}", "Multiply by g; do not divide."),
      ("L = g\\left(\\frac{2\\pi}{T}\\right)^{2}", "The fraction is upside down.")]),
    ("compound interest", "A = P(1 + r)^{t}", "P", "P = \\frac{A}{(1 + r)^{t}}",
     [("P = A - (1 + r)^{t}", "The factor multiplies P, so divide instead of subtracting."), ("P = \\frac{A}{1 + rt}", "The exponent applies to (1 + r)."),
      ("P = A(1 + r)^{t}", "Divide by the growth factor; do not multiply.")]),
    ("compound interest", "A = P(1 + r)^{t}", "r", "r = \\left(\\frac{A}{P}\\right)^{\\frac{1}{t}} - 1",
     [("r = \\frac{A}{Pt} - 1", "Undo the exponent t with a root, not by dividing by t."), ("r = \\left(\\frac{A}{P}\\right)^{t} - 1", "Undo the power t with the exponent 1/t."),
      ("r = \\left(\\frac{A}{P} - 1\\right)^{\\frac{1}{t}}", "Take the root before subtracting 1.")]),
    ("continuous growth", "A = Pe^{rt}", "t", "t = \\frac{\\ln\\left(\\frac{A}{P}\\right)}{r}",
     [("t = \\frac{\\ln A - P}{r}", "Divide by P before taking the natural log."), ("t = \\ln\\left(\\frac{A}{P}\\right) - r", "r multiplies t, so divide by r."),
      ("t = \\frac{A}{Pre}", "Use the natural log to undo e.")]),
    ("the pH of a solution", "\\text{pH} = -\\log H", "H", "H = 10^{-\\text{pH}}",
     [("H = -10^{\\text{pH}}", "The negative belongs in the exponent."), ("H = \\frac{-\\text{pH}}{\\log}", "log is a function, not a factor."),
      ("H = 10^{\\text{pH}}", "Lost the negative sign.")]),
    ("sound level in decibels", "L = 10\\log\\left(\\frac{I}{I_0}\\right)", "I", "I = I_0 \\cdot 10^{\\frac{L}{10}}",
     [("I = I_0 \\cdot 10^{10L}", "Divide L by 10 before using it as an exponent."), ("I = \\frac{10^{L/10}}{I_0}", "Multiply by I₀; do not divide."),
      ("I = I_0 + 10^{\\frac{L}{10}}", "I₀ divides I, so multiply to undo it.")]),
    ("the vertex form of a parabola", "y = a(x - h)^{2} + k", "x", "x = h \\pm \\sqrt{\\frac{y - k}{a}}",
     [("x = h + \\frac{y - k}{2a}", "Undo the square with a square root."), ("x = \\pm\\sqrt{\\frac{y - k}{a}} - h", "Add h; it is subtracted from x."),
      ("x = h \\pm \\sqrt{\\frac{y}{a}} - k", "Subtract k before dividing by a.")]),
    ("the area of a square", "A = s^{2}", "s", "s = \\sqrt{A}",
     [("s = \\frac{A}{2}", "Squaring is undone with a square root, not by dividing by 2."), ("s = A^{2}", "Squared again instead of taking the root."),
      ("s = \\frac{A}{4}", "That divides by the number of sides.")]),
    ("the volume of a cone", "V = \\frac{1}{3}\\pi r^{2}h", "h", "h = \\frac{3V}{\\pi r^{2}}",
     [("h = \\frac{V}{3\\pi r^{2}}", "Dividing by 1/3 is multiplying by 3."), ("h = 3V - \\pi r^{2}", "πr² multiplies h; divide instead."),
      ("h = \\frac{3V}{2\\pi r}", "r is squared, not doubled.")]),
    ("the volume of a cone", "V = \\frac{1}{3}\\pi r^{2}h", "r", "r = \\sqrt{\\frac{3V}{\\pi h}}",
     [("r = \\sqrt{\\frac{V}{3\\pi h}}", "Dividing by 1/3 is multiplying by 3."), ("r = \\frac{3V}{\\pi h}", "Forgot the square root."),
      ("r = \\frac{\\sqrt{3V}}{\\pi h}", "The square root applies to the whole fraction.")]),
    ("gravitational force", "F = \\frac{Gm_1m_2}{d^{2}}", "d", "d = \\sqrt{\\frac{Gm_1m_2}{F}}",
     [("d = \\frac{Gm_1m_2}{2F}", "Undo the square with a square root."), ("d = \\sqrt{\\frac{F}{Gm_1m_2}}", "The fraction is upside down."),
      ("d = \\sqrt{FGm_1m_2}", "Multiply both sides by d² first, then divide by F.")]),
    ("an exponential model", "y = ab^{x}", "b", "b = \\left(\\frac{y}{a}\\right)^{\\frac{1}{x}}",
     [("b = \\frac{y}{ax}", "Undo the exponent with a root, not division."), ("b = \\frac{y^{1/x}}{a}", "Divide by a before taking the root."),
      ("b = \\left(\\frac{y}{a}\\right)^{x}", "Use the exponent 1/x to undo the power x.")]),
    ("a cube root function", "y = \\sqrt[3]{x - h} + k", "x", "x = (y - k)^{3} + h",
     [("x = (y + k)^{3} + h", "Subtract k first."), ("x = (y - k)^{3} - h", "Add h at the end."), ("x = \\sqrt[3]{y - k} + h", "Undo a cube root by cubing.")]),
    ("a square root function", "y = a\\sqrt{x} + k", "x", "x = \\left(\\frac{y - k}{a}\\right)^{2}",
     [("x = \\frac{(y - k)^{2}}{a}", "Divide by a before squaring."), ("x = \\sqrt{\\frac{y - k}{a}}", "Undo a square root by squaring."),
      ("x = \\left(\\frac{y}{a}\\right)^{2} - k", "Subtract k before dividing by a.")]),
    ("the logarithm definition", "y = \\log_{b} x", "x", "x = b^{y}",
     [("x = y^{b}", "The base of the log becomes the base of the power."), ("x = \\frac{y}{\\log b}", "Rewrite in exponential form."),
      ("x = by", "A log is an exponent, not a factor.")]),
    ("the logarithm definition", "y = \\log_{2}(x + 5)", "x", "x = 2^{y} - 5",
     [("x = 2^{y} + 5", "Subtract 5 after rewriting."), ("x = y^{2} - 5", "The base is 2, so x + 5 = 2^y."), ("x = 2^{y - 5}", "Subtract 5 from 2^y, not from the exponent.")]),
    ("Ohm's law for power", "P = \\frac{V^{2}}{R}", "V", "V = \\sqrt{PR}",
     [("V = \\sqrt{\\frac{P}{R}}", "Multiply both sides by R."), ("V = \\frac{PR}{2}", "Undo the square with a square root."),
      ("V = PR^{2}", "Multiply by R and then take a square root.")]),
    ("the area of an equilateral triangle", "A = \\frac{\\sqrt{3}}{4}s^{2}", "s", "s = \\sqrt{\\frac{4A}{\\sqrt{3}}}",
     [("s = \\sqrt{\\frac{\\sqrt{3}A}{4}}", "Multiply by the reciprocal of √3/4."), ("s = \\frac{4A}{\\sqrt{3}}", "Forgot the square root."),
      ("s = \\frac{2\\sqrt{A}}{3}", "√3 does not become 3 under the root this way.")]),
    ("centripetal acceleration", "a = \\frac{v^{2}}{r}", "v", "v = \\sqrt{ar}",
     [("v = \\sqrt{\\frac{a}{r}}", "Multiply both sides by r."), ("v = \\frac{ar}{2}", "Undo the square with a square root."), ("v = a^{2}r", "Take the square root after multiplying by r.")]),
]


@gen("A2.A.CED.A.3", 29)
def ced3_rearrange(rng):
    name, formula, var, ans, ds = rng.choice(FORMULAS)
    if not ds:
        raise Skip
    stem = f"The formula for {name} is {M(formula)}. Which equation is solved for {M(var)}?"
    if var in ("r", "s", "v", "d", "t") and "\\sqrt" in ans and "\\pm" not in ans:
        stem = f"The formula for {name} is {M(formula)}. Which equation gives {M(var)}, a positive length or quantity, in terms of the other variables?"
    return mc("A2.A.CED.A.3", 2, "Y", stem, M(ans), [(M(t), w) for t, w in ds],
              f"Undo the operations on {M(var)} in reverse order. The result is {M(ans)}.", rng)


# ===================================================== A2.A.REI.A.1
@gen("A2.A.REI.A.1", 12)
def rei_find_error(rng):
    a = rng.choice([2, 3, 4, 5])
    h = rng.choice([-5, -4, -3, -2, 2, 3, 4, 5, 6])
    k = rng.choice([-9, -7, -5, -3, 2, 4, 6, 8])
    s = rng.choice([2, 3, 4, 5, 6])
    c = a * s * s + k
    name = rng.choice(["Maria", "Devon", "Aisha", "Luis", "Kenji", "Tamika", "Jordan", "Priya"])
    steps_ok = [f"{a}{factor(h)}^{{2}} {signed(k)} = {c}",
                f"{a}{factor(h)}^{{2}} = {c - k}",
                f"{factor(h)}^{{2}} = {s * s}",
                f"x {'-' if h > 0 else '+'} {abs(h)} = \\pm {s}",
                f"x = {h} \\pm {s}"]
    err = rng.choice(["move_k", "divide", "plusminus", "sign_h"])
    steps = list(steps_ok)
    if err == "move_k":
        steps[1] = f"{a}{factor(h)}^{{2}} = {c + k}"
        bad = 2
        why = f"Step 2: to undo {M(signed(k))}, {'subtract' if k > 0 else 'add'} {abs(k)} on both sides; {c} {signed(-k)} = {c - k}."
        if (c + k) % a:
            steps[2] = f"{factor(h)}^{{2}} = {num(F(c + k, a))}"
        else:
            steps[2] = f"{factor(h)}^{{2}} = {(c + k) // a}"
        steps[3] = steps[4] = None
    elif err == "divide":
        steps[2] = f"{factor(h)}^{{2}} = {c - k - a}"
        bad = 3
        why = f"Step 3: undo multiplying by {a} by dividing by {a}, not subtracting {a}."
        steps[3] = steps[4] = None
    elif err == "plusminus":
        steps[3] = f"x {'-' if h > 0 else '+'} {abs(h)} = {s}"
        steps[4] = f"x = {h + s}"
        bad = 4
        why = f"Step 4: a square equal to {s * s} has two square roots, {M(f'\\pm {s}')}."
    else:
        steps[4] = f"x = {-h} \\pm {s}"
        bad = 5
        why = f"Step 5: {M(f'x {'-' if h > 0 else '+'} {abs(h)}')} means {'add' if h > 0 else 'subtract'} {abs(h)} to isolate x."
    shown = [t for t in steps if t is not None]
    lines = "".join(f"<li>{M(t)}</li>" for t in shown)
    stem = f"{name} solved an equation. The work is shown.<ol>{lines}</ol>In which step did {name} make the first error?"
    opts = [f"Step {i}" for i in range(2, len(shown) + 1)]
    ans = f"Step {bad}"
    ds = [(o, "This step follows correctly from the step before it.") for o in opts if o != ans]
    ds.append(("There is no error.", why))
    return mc("A2.A.REI.A.1", 3, "N", stem, ans, ds, why, rng)


@gen("A2.A.REI.A.1", 8)
def rei_justify(rng):
    kind = rng.choice(["sqrt", "exp", "radical", "log"])
    if kind == "sqrt":
        a = rng.choice([2, 3, 4])
        k = rng.randint(2, 9)
        s = rng.randint(2, 7)
        top = f"{a}x^{{2}} = {a * s * s}"
        bot = f"x^{{2}} = {s * s}"
        ans = "Division property of equality"
        ds = [("Subtraction property of equality", f"The {a} multiplies, so both sides are divided by {a}."),
              ("Square root property", "The square root is taken in the next step, not this one."),
              ("Distributive property", "Nothing is being distributed.")]
        expl = f"Both sides were divided by {a}."
    elif kind == "exp":
        b = rng.choice([2, 3, 5])
        n = rng.randint(2, 5)
        top = f"{b}^{{x + 1}} = {b}^{{{n}}}"
        bot = f"x + 1 = {n}"
        ans = "If two powers with the same base are equal, their exponents are equal."
        ds = [("Divide both sides by the base.", f"Dividing by {b} would change each exponent by 1, not remove the base."),
              ("Take the square root of both sides.", "No square roots are involved."),
              ("Subtract the base from both sides.", "Subtracting does not remove a base.")]
        expl = f"Since {M(f'{b}^{{x}}')} is one-to-one, equal powers of {b} have equal exponents."
    elif kind == "radical":
        c = rng.randint(2, 8)
        top = f"\\sqrt{{x + {c}}} = x - {c}"
        bot = f"x + {c} = (x - {c})^{{2}}"
        ans = "Square both sides; any solutions found must be checked."
        ds = [("Take the square root of both sides.", "Squaring, not a square root, removes the radical."),
              ("Subtract the radical from both sides.", "That would not remove the radical."),
              ("Square both sides; checking is not needed.", "Squaring can create extraneous solutions, so check every answer.")]
        expl = "Squaring both sides removes the radical, but it can introduce extraneous solutions."
    else:
        b = rng.choice([2, 3, 10])
        n = rng.randint(2, 4)
        top = f"\\log_{{{b}}}(x - 1) = {n}"
        bot = f"x - 1 = {b}^{{{n}}}"
        ans = "Rewrite the logarithmic equation in exponential form."
        ds = [("Multiply both sides by the base.", f"A log is an exponent: {M(f'\\log_{{{b}}} y = {n}')} means {M(f'{b}^{{{n}}} = y')}."),
              ("Divide both sides by log.", "log is a function, not a factor."),
              ("Raise both sides to the power n.", "The base is raised to the value of the log.")]
        expl = f"{M(f'\\log_{{{b}}} y = {n}')} means {M(f'y = {b}^{{{n}}}')}."
    stem = f"A student wrote these two lines while solving an equation.<p>{M(top)}<br>{M(bot)}</p>Which reason justifies going from the first line to the second?"
    return mc("A2.A.REI.A.1", 2, "N", stem, ans, ds, expl, rng)


# ===================================================== A2.A.REI.A.2
@gen("A2.A.REI.A.2", 16)
def rei_radical_extraneous(rng):
    c = rng.randint(-6, 6)
    case = rng.choice(["one", "one", "one", "both", "none"])
    if case == "one":
        x1 = rng.randint(-c + 1, -c + 9)
        x2 = rng.randint(-c - 9, -c - 1)
    elif case == "both":
        x1, x2 = rng.randint(-c + 1, -c + 9), rng.randint(-c, -c + 9)
    else:
        x1, x2 = rng.randint(-c - 9, -c - 1), rng.randint(-c - 9, -c - 1)
    if x1 == x2:
        raise Skip
    a = 2 * c + x1 + x2
    b = c * c - x1 * x2
    if a == 0 or abs(a) > 20 or abs(b) > 80:
        raise Skip
    rad = lin(a, b)
    rhs = lin(1, c) if c else "x"
    valid = sorted([x for x in (x1, x2) if x + c >= 0])
    allr = sorted([x1, x2])
    fmt = lambda L: "no solution" if not L else ("x = " + " and x = ".join(str(v) for v in L))
    fmtM = lambda L: "no solution" if not L else " and ".join(M(f"x = {v}") for v in L)
    ans = fmtM(valid)
    opts = [allr, [allr[0]], [allr[1]], []]
    ds = []
    for o in opts:
        if o == valid:
            continue
        if o == allr:
            why = "Both values solve the squared equation, but each must be checked in the original. " + \
                  "; ".join(f"x = {v} gives {M(f'\\sqrt{{{a * v + b}}} = {v + c}')}" for v in allr if v + c < 0) + "."
        elif not o:
            why = f"{M(f'x = {valid[0]}')} does check: {M(f'\\sqrt{{{a * valid[0] + b}}} = {valid[0] + c}')}." if valid else "Check each value."
        else:
            v = o[0]
            why = (f"{M(f'x = {v}')} is extraneous: the square root cannot equal {v + c}." if v + c < 0
                   else f"Missed a valid solution; check both values from the squared equation.")
        ds.append((fmtM(o), why))
    sq = poly([1, 2 * c - a, c * c - b])
    expl = (f"Square both sides: {M(f'{rad} = ({rhs})^{{2}}')}, so {M(sq + ' = 0')} and {M(f'x = {allr[0]}')} or {M(f'x = {allr[1]}')}. "
            + " ".join(f"Check {M(f'x = {v}')}: {M(f'\\sqrt{{{a * v + b}}} = {abs(v + c)}')} and the right side is {v + c}, so it "
                       f"{'works' if v + c >= 0 else 'is extraneous'}." for v in allr))
    return mc("A2.A.REI.A.2", 2, "Y", f"What is the solution set of {M(f'\\sqrt{{{rad}}} = {rhs}')}?", ans, ds, expl, rng)


@gen("A2.A.REI.A.2", 8)
def rei_radical_simple(rng):
    a = rng.choice([1, 2, 3, 4, 5])
    b = rng.randint(-12, 12)
    neg = rng.random() < 0.3
    s = rng.randint(2, 9)
    k = rng.randint(0, 6)
    rhs = s - k if not neg else -s - k
    # sqrt(ax + b) + k = rhs+k ... present as sqrt(ax+b) + k = R
    R = rhs + k
    if neg:
        stem = f"What is the solution to {M(f'\\sqrt{{{lin(a, b)}}}' + (f' {signed(k)}' if k else '') + f' = {R}')}?"
        val = F(s * s - b, a)
        ans = "no solution"
        ds = [(M(f"x = {num(val)}"), f"Squaring hides the problem: a square root cannot equal {-s}."),
              (M(f"x = {num(F(-s - b, a))}"), "Did not square, and a square root cannot be negative."),
              (M(f"x = {num(F(s * s + b, a))}"), "Sign error when isolating x, and the equation has no solution.")]
        expl = f"Isolate the radical: {M(f'\\sqrt{{{lin(a, b)}}} = {-s}')}. A principal square root is never negative, so there is no solution."
    else:
        val = F(s * s - b, a)
        stem = f"What is the solution to {M(f'\\sqrt{{{lin(a, b)}}}' + (f' {signed(k)}' if k else '') + f' = {R}')}?"
        ans = M(f"x = {num(val)}")
        ds = [(M(f"x = {num(F(R * R - b, a))}"), f"Isolate the radical first: subtract {k} before squaring." if k else "Arithmetic error."),
              (M(f"x = {num(F(s - b, a))}"), "Forgot to square both sides."),
              (M(f"x = {num(F(s * s + b, a))}"), f"Sign error: {'subtract' if b > 0 else 'add'} {abs(b)}."),
              ("no solution", f"{M(f'x = {num(val)}')} checks in the original equation.")]
        expl = f"{M(f'\\sqrt{{{lin(a, b)}}} = {s}')}, so {M(f'{lin(a, b)} = {s * s}')} and {M(f'x = {num(val)}')}. It checks."
    return mc("A2.A.REI.A.2", 2, "Y", stem, ans, ds, expl, rng)


@gen("A2.A.REI.A.2", 7)
def rei_cube_root(rng):
    a = rng.choice([1, 2, 3, 4])
    b = rng.randint(-10, 10)
    s = rng.choice([-4, -3, -2, 2, 3, 4])
    val = F(s ** 3 - b, a)
    stem = f"What is the solution to {M(f'\\sqrt[3]{{{lin(a, b)}}} = {s}')}?"
    ds = [(M(f"x = {num(F(s * s - b, a))}"), "Squared instead of cubing."),
          (M(f"x = {num(F(3 * s - b, a))}"), "Multiplied by 3 instead of cubing."),
          (M(f"x = {num(F(-s ** 3 - b, a))}"), "Sign error when cubing."),
          ("no solution", "A cube root can be negative, so there is a solution.")]
    return mc("A2.A.REI.A.2", 2, "Y", stem, M(f"x = {num(val)}"), ds,
              f"Cube both sides: {M(f'{lin(a, b)} = {s ** 3}')}, so {M(f'x = {num(val)}')}.", rng)


# ===================================================== A2.A.REI.B.3
NAMES = ["Ava", "Malik", "Sofia", "Ethan", "Zara", "Diego", "Mei", "Andre", "Nia", "Omar"]


@gen("A2.A.REI.B.3", 18)
def rei_system_context(rng):
    kind = rng.choice(["tickets", "plans", "mix", "coins", "items"])
    if kind == "tickets":
        p1, p2 = rng.sample([4, 5, 6, 7, 8, 10, 12, 15], 2)
        x, y = rng.randint(20, 150), rng.randint(20, 150)
        ask = rng.choice(["x", "y"])
        n1, n2 = rng.choice([("adult", "student"), ("general", "reserved"), ("child", "adult")])
        if (n1 == "adult") != (p1 > p2):
            p1, p2 = p2, p1
        stem = (f"A theater sold {x + y} tickets for {money(p1 * x + p2 * y)}. {n1.capitalize()} tickets cost {money(p1)} and "
                f"{n2} tickets cost {money(p2)}. How many {n1 if ask == 'x' else n2} tickets were sold?")
        ans = x if ask == "x" else y
        other = y if ask == "x" else x
        ds = [(str(other), f"That is the number of {n2 if ask == 'x' else n1} tickets."),
              (str(round((p1 * x + p2 * y) / (p1 + p2))), "Divided the total by the sum of the prices."),
              (str(ans + rng.choice([-10, 10, 5])), "Arithmetic error when solving the system.")]
        expl = (f"Let {M('a')} = {n1} and {M('s')} = {n2} tickets: {M(f'a + s = {x + y}')} and {M(f'{p1}a + {p2}s = {p1 * x + p2 * y}')}. "
                f"Solving gives {M(f'a = {x}')} and {M(f's = {y}')}.")
    elif kind == "plans":
        f1, r1 = rng.choice([(20, 3), (15, 4), (40, 2), (30, 5), (25, 6), (10, 8)])
        f2, r2 = rng.choice([(60, 1), (50, 2), (80, 1), (75, 3), (45, 4), (100, 2)])
        if r1 <= r2 or f1 >= f2 or (f2 - f1) % (r1 - r2):
            raise Skip
        n = (f2 - f1) // (r1 - r2)
        thing, unit = rng.choice([("gym", "visit"), ("streaming service", "movie rental"), ("phone plan", "gigabyte of data"),
                                  ("car rental", "mile driven")])
        stem = (f"{thing.capitalize()} A charges {money(f1)} plus {money(r1)} per {unit}. {thing.capitalize()} B charges {money(f2)} plus "
                f"{money(r2)} per {unit}. For how many {unit}s do the two cost the same?")
        if unit == "mile driven":
            stem = stem.replace("mile drivens", "miles")
        ans = n
        ds = [(str(f1 + r1 * n), "That is the cost at that point, not the number of units."),
              (str(round((f2 + f1) / (r1 + r2))), "Added the fees and the rates instead of setting the costs equal."),
              (str(n + 1 if (f2 - f1) / (r1 + r2) == n + 1 else round((f2 - f1) / (r1 + r2)) or n + 2), "Sign error when combining the rates.")]
        expl = f"Set {M(f'{f1} + {r1}x = {f2} + {r2}x')}: {M(f'{r1 - r2}x = {f2 - f1}')}, so {M(f'x = {n}')}."
    elif kind == "mix":
        p1, p2 = rng.choice([(4, 10), (3, 8), (5, 9), (6, 12), (2, 7)])
        x, y = rng.randint(2, 15), rng.randint(2, 15)
        total = x + y
        cost = p1 * x + p2 * y
        what1, what2 = rng.choice([("peanuts", "cashews"), ("regular coffee", "premium coffee"), ("oats", "dried fruit")])
        stem = (f"A store mixes {what1} that cost {money(p1)} per pound with {what2} that cost {money(p2)} per pound to make "
                f"{total} pounds of a mix worth {money(cost)} in all. How many pounds of {what2} are in the mix?")
        ans = y
        ds = [(str(x), f"That is the amount of {what1}."), (str(total // 2), "Split the total evenly; the prices are different."),
              (str(round(cost / p2)), f"Divided the total value by the price of {what2} alone.")]
        expl = f"{M(f'a + b = {total}')} and {M(f'{p1}a + {p2}b = {cost}')}. Solving gives {M(f'a = {x}')} and {M(f'b = {y}')}."
    elif kind == "coins":
        x, y = rng.randint(5, 40), rng.randint(5, 40)
        name = rng.choice(NAMES)
        v = 10 * x + 25 * y
        stem = (f"{name} has {x + y} coins, all dimes and quarters, worth {money(v / 100, True)}. How many quarters does {name} have?")
        ans = y
        ds = [(str(x), "That is the number of dimes."), (str(round(v / 25)), "Assumed all the coins were quarters."),
              (str(y + 5), "Arithmetic error when solving the system.")]
        expl = f"{M(f'd + q = {x + y}')} and {M(f'0.10d + 0.25q = {num(v / 100)}')}. Solving gives {M(f'q = {y}')} and {M(f'd = {x}')}."
    else:
        p1, p2 = rng.sample([2, 3, 4, 5, 6, 8, 9], 2)
        x, y = rng.randint(3, 25), rng.randint(3, 25)
        n1, n2 = rng.choice([("notebooks", "folders"), ("muffins", "cookies"), ("hats", "scarves"), ("small candles", "large candles")])
        name = rng.choice(NAMES)
        stem = (f"{name} bought {x + y} items: {n1} for {money(p1)} each and {n2} for {money(p2)} each. "
                f"{name} spent {money(p1 * x + p2 * y)}. How many {n1} did {name} buy?")
        ans = x
        ds = [(str(y), f"That is the number of {n2}."), (str((x + y) // 2), "Split the items evenly; the prices are different."),
              (str(round((p1 * x + p2 * y) / p1)), f"Divided the total by the price of {n1} alone.")]
        expl = f"{M(f'a + b = {x + y}')} and {M(f'{p1}a + {p2}b = {p1 * x + p2 * y}')}. Solving gives {M(f'a = {x}')} and {M(f'b = {y}')}."
    return mc("A2.A.REI.B.3", 2, "Y", stem, str(ans), ds, expl, rng)


@gen("A2.A.REI.B.3", 7)
def rei_system_three(rng):
    p = sorted(rng.sample([3, 4, 5, 6, 8, 10, 12, 15], 3))
    x, y, z = rng.randint(5, 40), rng.randint(5, 40), rng.randint(5, 40)
    k = rng.randint(2, 15)
    if len({x, y, z}) < 3:
        raise Skip
    names = rng.choice([("small", "medium", "large"), ("bronze", "silver", "gold"), ("lawn", "upper deck", "box")])
    thing = rng.choice(["drinks", "tickets", "pizzas"])
    if names[2] == "box" or names[0] == "lawn":
        thing = "seats"
    total = x + y + z
    cost = p[0] * x + p[1] * y + p[2] * z
    stem = (f"A vendor sold {total} {thing} in three sizes: {names[0]} for {money(p[0])}, {names[1]} for {money(p[1])}, and "
            f"{names[2]} for {money(p[2])}. The sales totaled {money(cost)}, and {k} more {names[1]} than {names[0]} {thing} were sold "
            f". How many {names[2]} {thing} were sold?").replace(" .", ".")
    y = x + k
    total = x + y + z
    cost = p[0] * x + p[1] * y + p[2] * z
    stem = (f"A vendor sold {total} {thing}: {names[0]} for {money(p[0])} each, {names[1]} for {money(p[1])} each, and "
            f"{names[2]} for {money(p[2])} each. Sales totaled {money(cost)}, and the vendor sold {k} more {names[1]} {thing} than "
            f"{names[0]} {thing}. Use technology to solve the system. How many {names[2]} {thing} were sold?")
    ds = [(str(x), f"That is the number of {names[0]} {thing}."), (str(y), f"That is the number of {names[1]} {thing}."),
          (str(total // 3), "Split the total evenly; the system must be solved.")]
    return mc("A2.A.REI.B.3", 3, "Y", stem, str(z), ds,
              f"Let {M('a, b, c')} be the {names[0]}, {names[1]}, and {names[2]} counts: {M(f'a + b + c = {total}')}, "
              f"{M(f'{p[0]}a + {p[1]}b + {p[2]}c = {cost}')}, and {M(f'b = a + {k}')}. Solving gives {M(f'a = {x}, b = {y}, c = {z}')}.", rng)


# ===================================================== A2.A.REI.B.4
@gen("A2.A.REI.B.4", 12)
def rei_lin_quad(rng):
    x1, x2 = rng.sample(range(-6, 7), 2)
    m = rng.choice([-3, -2, -1, 1, 2, 3])
    c = rng.randint(-8, 8)
    lead = rng.choice([1, 1, 1, -1])
    # lead*x^2 + p x + q = m x + c  -> lead(x - x1)(x - x2) = 0
    p = m - lead * (x1 + x2)
    q = c + lead * x1 * x2
    quad = poly([lead, p, q])
    line = lin(m, c) if c else lin(m, 0).replace(" + 0", "")
    P = lambda x: (x, m * x + c)
    s1, s2 = P(x1), P(x2)
    corr = [(M(pt(*s1)), "Correct: it is on both graphs."), (M(pt(*s2)), "Correct: it is on both graphs.")]
    cands = []
    for x in range(-7, 8):
        yl, yq = m * x + c, lead * x * x + p * x + q
        if x in (x1, x2):
            cands.append(((s1[1], x1) if x == x1 else (s2[1], x2), "Coordinates are switched."))
            continue
        cands.append(((x, yl), "This point is on the line but not on the parabola."))
        cands.append(((x, yq), "This point is on the parabola but not on the line."))
    rng.shuffle(cands)
    wrongs = []
    for (a, b), why in cands:
        if (a, b) in (s1, s2):
            continue
        if b == m * a + c and b == lead * a * a + p * a + q:
            continue
        wrongs.append((M(pt(a, b)), why))
    stem = f"Which ordered pairs are solutions to this system?<p>{M('y = ' + quad)}<br>{M('y = ' + line)}</p>"
    sx = sorted([x1, x2])
    return ms("A2.A.REI.B.4", 2, "Y", stem, corr, wrongs, rng=rng,
              explanation=f"Set the expressions equal: {M(quad + ' = ' + line)}, so {M(poly([lead, p - m, q - c]) + ' = 0')}. "
                          f"The x-values are {sx[0]} and {sx[1]}; substitute into the line to get {M(pt(*P(sx[0])))} and {M(pt(*P(sx[1])))}.")


@gen("A2.A.REI.B.4", 8)
def rei_count_solutions(rng):
    m = rng.choice([-2, -1, 1, 2, 3])
    c = rng.randint(-6, 6)
    kind = rng.choice([0, 1, 2])
    # x^2 + bx + q - (m x + c) = x^2 + (b - m)x + (q - c); choose discriminant sign
    B = rng.choice([-6, -4, -2, 0, 2, 4, 6])
    if kind == 1:
        C = (B // 2) ** 2
    elif kind == 2:
        C = (B // 2) ** 2 - rng.choice([1, 4, 9, 16])
    else:
        C = (B // 2) ** 2 + rng.choice([1, 3, 5, 8])
    b, q = B + m, C + c
    quad = poly([1, b, q])
    line = lin(m, c) if c else lin(m, 0).replace(" + 0", "")
    disc = B * B - 4 * C
    words = {0: "no real solutions", 1: "exactly one solution", 2: "exactly two solutions"}
    ds = [(w.capitalize() + ".", f"The discriminant of {M(poly([1, B, C]) + ' = 0')} is {disc}.") for k, w in words.items() if k != kind]
    ds.append(("Infinitely many solutions.", "A line and a parabola cannot overlap everywhere."))
    return mc("A2.A.REI.B.4", 2, "Y", f"How many solutions does this system have?<p>{M('y = ' + quad)}<br>{M('y = ' + line)}</p>",
              words[kind].capitalize() + ".", ds,
              f"Set the expressions equal: {M(poly([1, B, C]) + ' = 0')}. The discriminant is {M(f'{B}^{{2}} - 4(1)({C}) = {disc}')}, "
              f"which is {'negative' if disc < 0 else ('zero' if disc == 0 else 'positive')}, so the system has {words[kind]}.", rng)
