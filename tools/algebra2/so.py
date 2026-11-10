"""Structure and Operations generators (blueprint category SO)."""
from math import gcd

from common import (F, M, Skip, article, augmented, bmatrix, coef_term, comma, factor, gen, mc, ordinal,
                    money, ms, num, pct, poly, signed, table)

VARS = ["x", "a", "m", "n", "y", "b", "t"]


def frac_exp(p, q):
    f = F(p, q)
    if f.denominator == 1:
        return num(f)
    return num(f)


# ===================================================== A2.N.RN.A.1.c
@gen("A2.N.RN.A.1", 15)
def rn_radical_to_exponent(rng):
    v = rng.choice(VARS)
    n = rng.randint(2, 6)
    m = rng.randint(2, 7)
    if gcd(m, n) != 1 or m == n:
        raise Skip
    a = rng.choice([1, 1, 2, 3, 5, 6, 7, 10])
    base = f"{a if a != 1 else ''}{v}"
    root = r"\sqrt" + ("" if n == 2 else f"[{n}]") + "{" + base + "}"
    mode = rng.choice(["outer", "inner"])
    expr = rf"\left({root}\right)^{{{m}}}" if mode == "outer" else (r"\sqrt" + ("" if n == 2 else f"[{n}]") + "{" + (f"({base})^{{{m}}}" if a != 1 else f"{v}^{{{m}}}") + "}")
    wrapped = f"({base})" if a != 1 else base
    ans = f"{wrapped}^{{{num(F(m, n))}}}"
    d = [
        (f"{wrapped}^{{{num(F(n, m))}}}", "The root index goes in the denominator and the power in the numerator; these are switched."),
        (f"{wrapped}^{{{m * n}}}", "Multiplied the power and the index. A root divides the exponent."),
    ]
    if a != 1:
        d.append((f"{a}{v}^{{{num(F(m, n))}}}", f"The exponent applies to the whole base {M(base)}, including the {a}."))
        d.append((f"{a ** m}{v}^{{{num(F(1, n))}}}", f"Raised {a} to the power {m} but left {M(v)} with only the root."))
    d.append((f"{wrapped}^{{{m - n}}}" if m - n not in (0, 1) else f"{wrapped}^{{{m + n}}}", "Subtracted or added the index and the power instead of dividing."))
    stem = f"Which expression is equivalent to {M(expr)}{' for ' + M(v + r' \ge 0') if n % 2 == 0 else ''}?"
    return mc("A2.N.RN.A.1.c", 1 if a == 1 else 2, "N", stem, M(ans), [(M(t), w) for t, w in d],
              f"{article(ordinal(n)).capitalize()} root is the exponent {M(num(F(1, n)))}, and raising to the power {m} multiplies the exponent by {m}: "
              f"{M(expr + ' = ' + ans)}.", rng)


@gen("A2.N.RN.A.1", 12)
def rn_exponent_to_radical(rng):
    v = rng.choice(VARS)
    n = rng.randint(3, 6)
    m = rng.randint(2, 7)
    if gcd(m, n) != 1 or m == n:
        raise Skip
    rt = lambda idx, inside: r"\sqrt" + ("" if idx == 2 else f"[{idx}]") + "{" + inside + "}"
    expr = f"{v}^{{{num(F(m, n))}}}"
    corrects = [(M(rt(n, f"{v}^{{{m}}}")), "Correct: the denominator is the index and the numerator is the power."),
                (M(rf"\left({rt(n, v)}\right)^{{{m}}}"), "Correct: take the root first, then raise to the power.")]
    wrongs = [(M(rt(m, f"{v}^{{{n}}}")), "Index and power are switched."),
              (M(rf"\left({rt(m, v)}\right)^{{{n}}}"), "Index and power are switched."),
              (M(rf"\frac{{{v}^{{{m}}}}}{{{n}}}"), "A fractional exponent is not division by the denominator."),
              (M(f"{m}" + rt(n, v)), "The power was written as a coefficient.")]
    rng.shuffle(wrongs)
    return ms("A2.N.RN.A.1.c", 2, "N", f"Which expressions are equivalent to {M(expr)}?",
              corrects, wrongs, rng=rng,
              explanation=f"{M(rf'{v}^{{\frac{{{m}}}{{{n}}}}} = \left({v}^{{\frac{{1}}{{{n}}}}}\right)^{{{m}}}')} so it is the {ordinal(n)} root of {M(v)}, raised to the {ordinal(m)} power. "
                          f"The order does not matter: {M(rt(n, f'{v}^{{{m}}}') + ' = ' + rf'\left({rt(n, v)}\right)^{{{m}}}')}.")


@gen("A2.N.RN.A.1", 14)
def rn_evaluate(rng):
    b = rng.randint(2, 5)
    n = rng.randint(2, 4)
    m = rng.choice([2, 3, 4, 5, -1, -2])
    if gcd(abs(m), n) != 1 or abs(m) == n:
        raise Skip
    a = b ** n
    if a > 700:
        raise Skip
    val = F(b) ** m
    expr = f"{a}^{{{num(F(m, n))}}}"
    d = []
    prod = F(a * m, n)
    d.append((num(prod), f"Multiplied {a} by the exponent instead of using it as a power."))
    d.append((num(F(b * m)) if m > 0 else num(F(-b ** abs(m))), "Took the root, then multiplied by the power instead of raising to it." if m > 0 else "A negative exponent means a reciprocal, not a negative number."))
    if m < 0:
        d.append((num(F(b) ** abs(m)), "Ignored the negative sign in the exponent; it means reciprocal."))
    d.append((num(F(a) ** abs(m)) if abs(m) <= 2 and a ** abs(m) < 10 ** 6 else num(F(b ** (n + 1))), "Did not take the root."))
    d.append((num(F(b) ** (abs(m) + 1)), "Arithmetic error when raising to the power."))
    stem = f"What is the value of {M(expr)}?"
    root = r"\sqrt" + ("" if n == 2 else f"[{n}]") + f"{{{a}}}"
    expl = (f"{M(root + ' = ' + str(b))}, so {M(expr + ' = ' + f'{b}^{{{m}}}' + ' = ' + num(val))}.")
    return mc("A2.N.RN.A.1.c", 2, "N", stem, M(num(val)), [(M(t), w) for t, w in d], expl, rng)


@gen("A2.N.RN.A.1", 14)
def rn_exponent_rules(rng):
    v = rng.choice(VARS)
    kind = rng.choice(["product", "quotient", "power"])
    p = F(rng.randint(1, 5), rng.randint(2, 6))
    q = F(rng.randint(1, 5), rng.randint(2, 6))
    if p.denominator == 1 or q.denominator == 1 or p == q:
        raise Skip
    E = lambda e: f"{v}^{{{num(e)}}}"
    if kind == "product":
        expr, ans = rf"{E(p)} \cdot {E(q)}", p + q
        d = [(E(p * q), "Multiplied the exponents; when multiplying like bases you add them."),
             (E(F(p.numerator + q.numerator, p.denominator + q.denominator)), "Added numerators and denominators separately instead of finding a common denominator."),
             (E(p - q) if p - q != 0 else E(p * 2), "Subtracted the exponents; that is the rule for dividing.")]
        rule = "add the exponents"
    elif kind == "quotient":
        if p <= q:
            p, q = q, p
        expr, ans = rf"\frac{{{E(p)}}}{{{E(q)}}}", p - q
        d = [(E(p / q), "Divided the exponents; when dividing like bases you subtract them."),
             (E(p + q), "Added the exponents; that is the rule for multiplying."),
             (E(F(abs(p.numerator - q.numerator) or 1, abs(p.denominator - q.denominator) or 1)), "Subtracted numerators and denominators separately.")]
        rule = "subtract the exponents"
    else:
        k = rng.choice([2, 3, 4, 6])
        expr, ans = rf"\left({E(p)}\right)^{{{k}}}", p * k
        d = [(E(p + k), "Added the outer power; a power of a power multiplies exponents."),
             (E(F(p.numerator, p.denominator * k)), "Divided by the outer power instead of multiplying."),
             (E(F(p.numerator * k, p.denominator * k)) if F(p.numerator * k, p.denominator * k) != ans else E(p ** 2), "Multiplied both numerator and denominator by the power.")]
        rule = "multiply the exponents"
    if ans == 0 or ans.denominator == 1 and kind != "power":
        raise Skip
    expl = f"With the same base, {rule}: {M(expr + ' = ' + E(ans))}."
    return mc("A2.N.RN.A.1.c", 2, "N", f"Which expression is equivalent to {M(expr)}{', for ' + M(v + ' > 0') }?",
              M(E(ans)), [(M(t), w) for t, w in d], expl, rng)


@gen("A2.N.RN.A.1", 14)
def rn_why_definition(rng):
    b = rng.choice([2, 3, 5, 6, 7, 10, 11, 12, 13, 15, 17, 19, 20])
    n = rng.randint(2, 5)
    name = {2: "square", 3: "cube", 4: "fourth", 5: "fifth"}[n]
    rt = r"\sqrt" + ("" if n == 2 else f"[{n}]") + f"{{{b}}}"
    e = num(F(1, n))
    ans = rf"\left({b}^{{{e}}}\right)^{{{n}}} = {b}^{{{e} \cdot {n}}} = {b}^{{1}} = {b}"
    d = [(rf"{b}^{{{e}}} \cdot {n} = {b}", "Multiplying by the index is not the same as raising to a power."),
         (rf"\left({b}^{{{e}}}\right)^{{{n}}} = {b}^{{{e} + {n}}}", "A power of a power multiplies exponents; it does not add them."),
         (rf"{b}^{{{e}}} = \frac{{{b}}}{{{n}}}", "A fractional exponent is not division of the base."),
         (rf"\left({b}^{{{n}}}\right)^{{{e}}} = {b}^{{{n}}}", "The exponents should multiply to 1, giving the base itself.")]
    stem = (f"Which equation best explains why {M(f'{b}^{{{e}}}')} is defined as the {name} root of {b}, {M(rt)}?")
    return mc("A2.N.RN.A.1.b", 2, "N", stem, M(ans), [(M(t), w) for t, w in d],
              f"Keeping the power-of-a-power rule for rational exponents means {M(ans)}. "
              f"So {M(f'{b}^{{{e}}}')} is a number whose {name} power is {b}, which is the definition of {M(rt)}.", rng)


# ============================================================ A2.N.Q.A.1
@gen("A2.N.Q.A.1", 12)
def nq_rate_conversion(rng):
    ctx = rng.choice(["drive", "pump", "price", "run", "download"])
    if ctx == "drive":
        t = rng.choice([12, 15, 20, 24, 30, 36, 40, 45])
        rate = rng.choice([40, 45, 48, 50, 54, 55, 60, 64, 65, 70])
        d = F(rate * t, 60)
        if d.denominator != 1:
            raise Skip
        stem = f"A car travels {num(d)} miles in {t} minutes at a constant speed. What is its speed in miles per hour?"
        ans = rate
        ds = [(num(F(d) / t), "That is miles per minute, not miles per hour."),
              (num(d * t / 60) if (d * t) % 60 == 0 else num(F(rate * 2)), "Multiplied by the time instead of dividing by it."),
              (num(d + 60 - t) if d + 60 - t != rate else num(rate + 10), "Added minutes to miles; units must be converted, not combined."),
              (num(F(d * 60, t) / 2), "Converted the time incorrectly.")]
        unit = "miles per hour"
        expl = f"{M(rf'\frac{{{num(d)}\text{{ mi}}}}{{{t}\text{{ min}}}} \cdot \frac{{60\text{{ min}}}}{{1\text{{ h}}}} = {ans}')} miles per hour."
    elif ctx == "pump":
        rate = rng.choice([3, 4, 5, 6, 8, 9, 12])
        hours = rng.choice([2, 3, 4, 5])
        stem = f"A pump moves water at {rate} gallons per minute. How many gallons does it move in {hours} hours?"
        ans = rate * 60 * hours
        ds = [(num(rate * hours), "Did not convert hours to minutes."),
              (num(F(rate * hours, 60)) if (rate * hours) % 60 == 0 else num(rate * 60), "Divided by 60 instead of multiplying, or forgot the number of hours."),
              (num(rate * 60 + hours), "Added the hours instead of multiplying."),
              (num(rate * 24 * hours), "Used 24 as the conversion factor; there are 60 minutes in an hour.")]
        unit = "gallons"
        expl = f"{M(rf'{rate}\,\tfrac{{\text{{gal}}}}{{\text{{min}}}} \cdot 60\,\tfrac{{\text{{min}}}}{{\text{{h}}}} \cdot {hours}\text{{ h}} = {comma(ans)}')} gallons."
    elif ctx == "price":
        per_lb = rng.choice([4.80, 5.60, 6.40, 7.20, 8.00, 9.60, 11.20])
        oz = rng.choice([4, 8, 12])
        cost = round(per_lb * oz / 16, 2)
        stem = f"A {oz}-ounce bag of trail mix costs {money(cost, True)}. At this rate, what is the price per pound? (1 pound = 16 ounces)"
        ans = per_lb
        ds = [(money(cost / oz, True), "That is the price per ounce."),
              (money(cost * oz, True), "Multiplied by the ounces in the bag instead of converting to a pound."),
              (money(cost * 16, True), "Multiplied the bag price by 16; first find the price of one ounce."),
              (money(cost + 16 - oz, True), "Added units instead of using a rate.")]
        unit = None
        expl = f"Price per ounce is {money(cost, True)} ÷ {oz} = {money(cost / oz, True) if abs(cost/oz*100 - round(cost/oz*100))<1e-9 else '$' + format(cost/oz, '.4f').rstrip('0')}. Multiply by 16 ounces: {money(per_lb, True)} per pound."
        return mc("A2.N.Q.A.1.b", 2, "Y", stem, money(ans, True), ds, expl, rng)
    elif ctx == "run":
        km = rng.choice([5, 8, 10, 12, 15])
        minutes = rng.choice([25, 30, 40, 45, 50, 60, 75])
        ans = F(km * 1000, minutes * 60)
        if ans.denominator > 10 or ans.denominator not in (1, 2, 3, 9, 4, 5, 6):
            raise Skip
        stem = f"A runner completes a {km}-kilometer race in {minutes} minutes. What is the runner's average speed in meters per second?"
        val = round(km * 1000 / (minutes * 60), 2)
        ds = [(f"{round(km / minutes, 3)}", "That is kilometers per minute."),
              (f"{round(km * 1000 / minutes, 1)}", "Converted kilometers to meters but not minutes to seconds."),
              (f"{round(km * 60 / minutes, 2)}", "That is kilometers per hour."),
              (f"{round(km * 100 / (minutes * 60), 2)}", "Used 100 meters per kilometer instead of 1,000.")]
        unit = "meters per second"
        expl = f"{km} km = {comma(km*1000)} m and {minutes} min = {comma(minutes*60)} s, so the speed is {comma(km*1000)} ÷ {comma(minutes*60)} ≈ {val} meters per second."
        return mc("A2.N.Q.A.1.b", 2, "Y", stem + " Round to the nearest hundredth.", f"{val} {unit}", [(f"{t} {unit}", w) for t, w in ds], expl, rng)
    else:
        mb = rng.choice([150, 240, 300, 360, 450, 600, 720, 900])
        s = rng.choice([20, 30, 40, 45, 60])
        if mb % s:
            raise Skip
        stem = f"A file of {mb} megabytes downloads in {s} seconds. At this rate, how many megabytes download per minute?"
        ans = mb // s * 60
        ds = [(num(mb // s), "That is megabytes per second."),
              (num(F(mb * s, 60)) if (mb * s) % 60 == 0 else num(mb * 2), "Multiplied by the seconds instead of dividing."),
              (num(mb + 60), "Added 60 instead of converting the rate."),
              (num(F(mb, 60)) if mb % 60 == 0 else num(mb * 60), "Divided by 60 instead of finding the per-second rate first.")]
        unit = "megabytes"
        expl = f"{mb} ÷ {s} = {mb // s} megabytes per second, and {mb // s} × 60 = {comma(ans)} megabytes per minute."
    return mc("A2.N.Q.A.1.b", 2, "Y", stem, f"{comma(ans) if isinstance(ans, int) else num(ans)} {unit}",
              [(f"{t} {unit}", w) for t, w in ds], expl, rng)


@gen("A2.N.Q.A.1", 10)
def nq_reasonable_answer(rng):
    ctx = rng.choice(["bus", "boxes", "paint", "tables", "vans", "rope"])
    if ctx == "bus":
        people, cap, thing, who = rng.randint(180, 520), rng.choice([44, 48, 52, 56, 60]), "buses", "students on a field trip"
    elif ctx == "boxes":
        people, cap, thing, who = rng.randint(130, 400), rng.choice([12, 16, 18, 24]), "boxes", "books to pack, with each box holding"
    elif ctx == "paint":
        people, cap, thing, who = rng.randint(500, 1300), rng.choice([150, 200, 250, 350, 400]), "cans of paint", "square feet of wall to paint, with each can covering"
    elif ctx == "tables":
        people, cap, thing, who = rng.randint(70, 260), rng.choice([6, 8, 10, 12]), "tables", "guests at a banquet, with each table seating"
    elif ctx == "vans":
        people, cap, thing, who = rng.randint(30, 110), rng.choice([7, 8, 12, 15]), "vans", "team members traveling, with each van holding"
    else:
        people, cap, thing, who = rng.randint(40, 190), rng.choice([6, 8, 9, 15]), "pieces of rope", "feet of rope needed, cut from pieces that are each"
    if people % cap == 0 or (people / cap) % 1 > 0.85 or (people / cap) % 1 < 0.15:
        raise Skip
    exact = people / cap
    up = -(-people // cap)
    if ctx == "bus":
        stem = f"There are {people} students on a field trip. Each bus holds {cap} students. A calculator shows {people} ÷ {cap} ≈ {exact:.4f}. How many buses are needed?"
    elif ctx == "rope":
        stem = f"A project needs {people} feet of rope, sold only in {cap}-foot pieces. A calculator shows {people} ÷ {cap} ≈ {exact:.4f}. How many pieces must be bought?"
    else:
        unit = {"boxes": "books", "paint": "square feet", "tables": "guests", "vans": "people"}[ctx]
        stem = f"There are {people} {who} {cap} {unit}. A calculator shows {people} ÷ {cap} ≈ {exact:.4f}. How many {thing} are needed?"
    one = {"buses": "bus", "boxes": "box", "cans of paint": "can of paint", "tables": "table", "vans": "van", "pieces of rope": "piece of rope"}[thing]
    short = "not everything would fit" if ctx != "rope" else "there would not be enough rope"
    ds = [(str(up - 1), f"Rounded down, so {short}."),
          (f"{exact:.2f}", f"You cannot have part of a {one}; the answer must be a whole number."),
          (f"{exact:.4f}", f"Reported more precision than the situation allows; {thing} come in whole numbers."),
          (str(up + 1), "One more than needed.")]
    return mc("A2.N.Q.A.1.d", 2, "Y", stem, str(up), ds,
              f"{thing.capitalize()} must be whole numbers, and rounding down to {up - 1} would not be enough, so round up to {up}.", rng)


@gen("A2.N.Q.A.1", 8)
def nq_axis_scale(rng):
    top = rng.choice([180, 240, 360, 450, 640, 760, 900, 1150, 1400, 2300, 3700, 4800])
    squares = 10
    scales = [5, 10, 20, 25, 50, 100, 200, 250, 500, 1000]
    good = [s for s in scales if s * squares >= top]
    if not good:
        raise Skip
    best = good[0]
    i = scales.index(best)
    small = scales[i - 1] if i > 0 else None
    big = [s for s in scales if s > best]
    if small is None or len(big) < 2:
        raise Skip
    lo = rng.randint(1, 4) * (top // 20)
    stem = (f"A student is graphing data values that range from {comma(lo)} to {comma(top)}. The vertical axis starts at 0 and has "
            f"{squares} grid squares. Which scale for each grid square shows all the data while using as much of the graph as possible?")
    ds = [(comma(small), f"With {comma(small)} per square the axis only reaches {comma(small * squares)}, so {comma(top)} would not fit."),
          (comma(big[0]), "This fits, but the data would use only a small part of the graph."),
          (comma(big[1]), "This fits, but the data would be squeezed into a small part of the graph.")]
    return mc("A2.N.Q.A.1.a", 2, "Y", stem, comma(best), ds,
              f"The axis must reach at least {comma(top)}. {comma(best)} × {squares} = {comma(best * squares)} is enough, and a smaller common scale ({comma(small)}) is not.", rng)


# ============================================================ A2.A.SSE.A.1
CONTEXTS_EXP = [
    ("population of a town", "people", "years", True, [1200, 4800, 8500, 15000, 24000, 32000], [0.02, 0.03, 0.04, 0.05, 0.06]),
    ("value of a car", "dollars", "years", False, [18000, 22000, 26000, 32000, 41000], [0.08, 0.1, 0.12, 0.15, 0.2]),
    ("number of bacteria in a sample", "bacteria", "hours", True, [120, 250, 400, 850, 1500], [0.1, 0.12, 0.15, 0.2, 0.25]),
    ("amount of medicine in a patient's body, in milligrams,", "milligrams", "hours", False, [200, 250, 400, 500, 800], [0.1, 0.12, 0.15, 0.2, 0.25]),
    ("balance in a savings account", "dollars", "years", True, [500, 1200, 2500, 4000, 7500], [0.02, 0.03, 0.04, 0.05, 0.06]),
    ("number of followers on a social media account", "followers", "months", True, [250, 850, 1200, 3600], [0.05, 0.08, 0.1, 0.12, 0.15]),
    ("value of a laptop", "dollars", "years", False, [900, 1200, 1500, 2000], [0.1, 0.15, 0.2, 0.25]),
    ("temperature difference, in degrees, between a cup of tea and the room", "degrees", "minutes", False, [50, 60, 70, 80], [0.03, 0.04, 0.05, 0.06, 0.08]),
]


@gen("A2.A.SSE.A.1", 18)
def sse_exponential_parts(rng):
    what, unit, tunit, grow, avals, rvals = rng.choice(CONTEXTS_EXP)
    a = rng.choice(avals)
    r = rng.choice(rvals)
    b = round(1 + r if grow else 1 - r, 2)
    t = "t"
    expr = f"{comma(a).replace(',', '{,}')}({b})^{{{t}}}"
    ask = rng.choice(["a", "b", "rate"])
    stem = f"The {what} after {M(t)} {tunit} is modeled by {M('f(t) = ' + expr)}. "
    word = "increases" if grow else "decreases"
    if ask == "a":
        stem += f"What does {comma(a)} represent?"
        ans = f"the starting {what.split(' of ')[0] if ' of ' in what else what} when {M('t = 0')}"
        ans = f"the starting value, when {M('t = 0')}"
        ds = [(f"the value after one {tunit[:-1]}", f"After one {tunit[:-1]} the amount is {comma(a)} × {b}, not {comma(a)}."),
              (f"the amount it {word} by each {tunit[:-1]}", "The change each period depends on the base, not the starting value."),
              (f"the greatest possible value", "The model does not give a maximum." if grow else "The start is the greatest value here, but that is not what the number means in the model."),
              (f"the value after {M(t)} {tunit}", "That is the whole expression, not the coefficient.")]
        expl = f"When {M('t = 0')}, {M(f'({b})^0 = 1')}, so {M(f'f(0) = {comma(a)}')}. The coefficient is the initial amount."
    elif ask == "b":
        stem += f"What does {b} represent?"
        ans = f"the value is multiplied by {b} each {tunit[:-1]}"
        ds = [(f"the value {word} by {b} {unit} each {tunit[:-1]}", "The base is a growth factor that multiplies; it is not an amount added or subtracted."),
              (f"the value {word} by {b}% each {tunit[:-1]}", f"The percent change is {pct(r, 0)}, not {b}%."),
              (f"the starting value", f"The starting amount is the coefficient, {comma(a)}."),
              (f"the number of {tunit} that have passed", f"The number of {tunit} is {M('t')}.")]
        expl = f"Each time {M('t')} increases by 1, the value is multiplied by {b}. That is a {pct(r, 0)} {'increase' if grow else 'decrease'} each {tunit[:-1]}."
    else:
        stem += f"By what percent does the value change each {tunit[:-1]}?"
        ans = f"It {word} by {pct(r, 0)}."
        other = "decreases" if grow else "increases"
        ds = [(f"It {word} by {pct(b, 0)}.", f"{b} is the growth factor; the percent change is {M(f'{b} - 1')}" if grow else f"{b} is the decay factor; the percent change is {M(f'1 - {b}')}."),
              (f"It {other} by {pct(r, 0)}.", f"A base {'greater' if grow else 'less'} than 1 means the amount {word}."),
              (f"It {word} by {num(r)}%.", f"{num(r)} as a percent is {pct(r, 0)}."),
              (f"It {word} by {pct(1 - r if grow else 1 + r, 0)}.", "Used the wrong comparison with 1.")]
        expl = f"The base is {b} = {'1 + ' if grow else '1 - '}{num(r)}, so the value {word} by {pct(r, 0)} each {tunit[:-1]}."
    return mc("A2.A.SSE.A.1.a", 2, "Y", stem, ans, ds, expl, rng)


@gen("A2.A.SSE.A.1", 15)
def sse_revenue_factors(rng):
    item, store = rng.choice([("tickets", "theater"), ("T-shirts", "club"), ("cupcakes", "bakery"), ("smoothies", "café"),
                              ("phone cases", "kiosk"), ("candles", "craft fair booth")])
    n0 = rng.choice([120, 150, 180, 200, 240, 300, 400, 500])
    k = rng.choice([3, 4, 5, 6, 8, 10])
    p0 = rng.choice([4, 5, 6, 8, 10, 12, 15, 18, 20])
    inc = rng.choice([0.25, 0.5, 1, 2])
    inc_s = money(inc, inc < 1)
    expr = f"R(x) = ({n0} - {k}x)({p0} + {num(inc)}x)"
    ask = rng.choice(["first", "second", "k", "inc"])
    stem = (f"A {store} sells {item}. Its revenue, in dollars, is modeled by {M(expr)}, where {M('x')} is the number of "
            f"{inc_s} price increases. ")
    if ask == "first":
        stem += f"What does {M(f'{n0} - {k}x')} represent?"
        ans = f"the number of {item} sold"
        ds = [(f"the price of one of the {item}", f"The price is the other factor, {M(f'{p0} + {num(inc)}x')}."),
              ("the total revenue", "Revenue is the product of both factors."),
              (f"the number of {item} the {store} has in stock", f"It decreases as the price goes up, so it is how many are sold."),
              (f"the profit from each sale", "Revenue does not account for costs, and this factor counts items.")]
        expl = f"Revenue = (number sold)(price). The price factor is {M(f'{p0} + {num(inc)}x')}, so {M(f'{n0} - {k}x')} is the number sold."
    elif ask == "second":
        stem += f"What does {M(f'{p0} + {num(inc)}x')} represent?"
        ans = f"the price of one of the {item}"
        ds = [(f"the number of {item} sold", f"That is the factor {M(f'{n0} - {k}x')}."),
              ("the total revenue", "Revenue is the product of both factors."),
              ("the number of price increases", f"That is {M('x')}."),
              (f"the change in price for each increase", f"Each increase is {inc_s}, the coefficient of {M('x')}.")]
        expl = f"The price starts at {money(p0)} and goes up {inc_s} for each increase, so {M(f'{p0} + {num(inc)}x')} is the price per item."
    elif ask == "k":
        stem += f"What does the {k} represent?"
        ans = f"the number of fewer {item} sold for each price increase"
        ds = [(f"the number of {item} sold at the original price", f"That is {n0}."),
              (f"the amount the price goes up each time", f"The price goes up {inc_s} each time."),
              (f"the number of price increases", f"That is {M('x')}."),
              (f"the original price", f"The original price is {money(p0)}.")]
        expl = f"Each increase lowers the number sold, {M(f'{n0} - {k}x')}, by {k}."
    else:
        stem += f"What does {M(f'{p0} + {num(inc)}x')} equal when {M('x = 0')}, and what does that value mean?"
        ans = f"{money(p0)}, the original price"
        ds = [(f"{n0}, the original number sold", f"That is the other factor when {M('x = 0')}."),
              (f"{money(p0 * n0)}, the original price", f"{money(p0 * n0)} is the original revenue."),
              (f"{money(p0 + inc, inc < 1)}, the original price", f"With {M('x = 0')} there is no increase yet."),
              (f"{money(p0)}, the original revenue", f"{money(p0)} is a price per item, not revenue.")]
        expl = f"With no increases, the price is {money(p0)}."
    return mc("A2.A.SSE.A.1.b", 2, "Y", stem, ans, ds, expl, rng)


@gen("A2.A.SSE.A.1", 15)
def sse_geometry_parts(rng):
    kind = rng.choice(["box", "box", "frame", "garden"])
    if kind == "box":
        L, W = rng.choice([(30, 20), (24, 18), (40, 30), (36, 24), (100, 30), (50, 40), (28, 22)])
        expr = f"V(x) = x({L} - 2x)({W} - 2x)"
        ask = rng.choice(["L", "W", "x", "2x"])
        stem = (f"An open box is made from a {L}-inch by {W}-inch sheet of cardboard by cutting an {M('x')}-inch by {M('x')}-inch "
                f"square from each corner and folding up the sides. The volume is {M(expr)}. ")
        if ask == "L":
            stem += f"What does {M(f'{L} - 2x')} represent?"
            ans, ds = "the length of the base of the box", [
                ("the height of the box", f"The height is {M('x')}, the size of the cut."),
                ("the width of the base of the box", f"The width is {M(f'{W} - 2x')}."),
                ("the area of the base of the box", "Area is the product of the length and width."),
                ("the amount cut from the length", f"The amount cut is {M('2x')}.")]
            expl = f"A square of side {M('x')} is cut from both ends of the {L}-inch side, leaving {M(f'{L} - 2x')} for the base."
        elif ask == "W":
            stem += f"What does {M(f'{W} - 2x')} represent?"
            ans, ds = "the width of the base of the box", [
                ("the height of the box", f"The height is {M('x')}."),
                ("the length of the base of the box", f"The length is {M(f'{L} - 2x')}."),
                ("the volume of the box", "Volume is the product of all three factors."),
                ("the amount cut from the width", f"The amount cut is {M('2x')}.")]
            expl = f"Cutting {M('x')} from each end of the {W}-inch side leaves {M(f'{W} - 2x')}."
        elif ask == "x":
            stem += f"In the expression, what does the factor {M('x')} represent?"
            ans, ds = "the height of the box", [
                ("the length of the base", f"That is {M(f'{L} - 2x')}."),
                ("the number of corners cut", "There are always 4 corners; the factor is a length."),
                ("the volume of the box", "Volume is the whole product."),
                ("the area of one cut-out square", f"That area is {M('x^2')}.")]
            expl = f"When the sides fold up, their height is the side of the cut square, {M('x')}."
        else:
            stem += f"Why does the expression subtract {M('2x')} from {L} and from {W}?"
            ans, ds = "A square is cut from both ends of each side.", [
                ("The box has two equal sides.", "The 2 comes from cutting at both ends, not from equal sides."),
                ("The height is doubled when the sides fold up.", f"The height is {M('x')}, not {M('2x')}."),
                ("Two squares are cut in total.", "Four squares are cut, one from each corner."),
                ("The volume formula multiplies by 2.", "Volume is length × width × height with no extra factor.")]
            expl = f"Each side loses {M('x')} at each end, so it loses {M('2x')} in all."
        return mc("A2.A.SSE.A.1.b", 2, "Y", stem, ans, ds, expl, rng)
    if kind == "frame":
        L, W = rng.choice([(8, 10), (5, 7), (11, 14), (16, 20), (12, 18)])
        expr = f"A(x) = ({L} + 2x)({W} + 2x)"
        stem = (f"A {L}-inch by {W}-inch photo is placed in a frame of uniform width {M('x')} inches. The total area is {M(expr)}. "
                f"What does {M(f'{L} + 2x')} represent?")
        ans, ds = "the outside length of one side of the frame", [
            ("the width of the frame", f"The frame width is {M('x')}."),
            ("the area of the frame only", "The expression gives total area, including the photo."),
            ("the length of the photo", f"The photo side is {L} inches."),
            ("the perimeter of the photo", "Perimeter adds all four sides.")]
        expl = f"The frame adds {M('x')} on each side, so a {L}-inch side becomes {M(f'{L} + 2x')} inches."
        return mc("A2.A.SSE.A.1.b", 2, "Y", stem, ans, ds, expl, rng)
    L, W = rng.choice([(20, 30), (15, 25), (12, 16), (24, 40), (18, 30)])
    expr = f"A(x) = ({L} - 2x)({W} - 2x)"
    stem = (f"A {L}-foot by {W}-foot yard has a walkway of width {M('x')} feet along all four edges. The area of grass inside the "
            f"walkway is {M(expr)}. What does {M(f'{W} - 2x')} represent?")
    ans, ds = "one side length of the grass region", [
        ("the width of the walkway", f"The walkway width is {M('x')}."),
        ("the area of the walkway", "The expression is the grass area."),
        ("the total length of the yard", f"The yard side is {W} feet."),
        ("the perimeter of the grass region", "Perimeter adds all four sides.")]
    expl = f"The walkway takes {M('x')} from each end of the {W}-foot side, leaving {M(f'{W} - 2x')} feet of grass."
    return mc("A2.A.SSE.A.1.b", 2, "Y", stem, ans, ds, expl, rng)


# ======================================================= A2.A.APR.A.1/2
def cubic_from_roots(r1, r2, r3, a=1):
    s1 = r1 + r2 + r3
    s2 = r1 * r2 + r1 * r3 + r2 * r3
    s3 = r1 * r2 * r3
    return [a, -a * s1, a * s2, -a * s3]


def peval(c, x):
    v = 0
    for k in c:
        v = v * x + k
    return v


FN = ["p", "f", "g", "h", "q"]


@gen("A2.A.APR.A.1", 14)
def apr_which_factor(rng):
    roots = rng.sample([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5], 3)
    c = cubic_from_roots(*roots)
    if max(abs(k) for k in c) > 70:
        raise Skip
    r = roots[0]
    f = rng.choice(FN)
    cands = [-r] + [s for s in range(-6, 7) if s != 0 and peval(c, s) != 0 and s != -r]
    wrong_roots = []
    if peval(c, -r) != 0:
        wrong_roots.append((-r, "sign"))
    for s in rng.sample(cands[1:], len(cands) - 1):
        if len(wrong_roots) >= 4:
            break
        if all(s != w for w, _ in wrong_roots):
            wrong_roots.append((s, "other"))
    ds = []
    for s, kind in wrong_roots:
        if peval(c, s) == 0:
            continue
        why = (f"Sign error: {M(factor(s))} is a factor only if {M(f'{f}({s}) = 0')}, and {M(f'{f}({s}) = {peval(c, s)}')}."
               if kind == "sign" else f"{M(f'{f}({s}) = {peval(c, s)}')}, which is not 0.")
        ds.append((M(factor(s)), why))
    stem = f"Which binomial is a factor of {M(f'{f}(x) = ' + poly(c))}?"
    return mc("A2.A.APR.A.1", 2, "N", stem, M(factor(r)), ds,
              f"By the Factor Theorem, {M(factor(r))} is a factor exactly when {M(f'{f}({r}) = 0')}. "
              f"Substituting gives {M(f'{f}({r}) = 0')}.", rng)


@gen("A2.A.APR.A.1", 12)
def apr_find_k(rng):
    a = rng.choice([-3, -2, -1, 1, 2, 3])
    b = rng.randint(-5, 5)
    k_true = rng.randint(-12, 12)
    # p(x) = x^3 + b x^2 + k x + c, choose c so p(a) = 0
    c = -(a ** 3 + b * a * a + k_true * a)
    if c == 0 or abs(c) > 60 or k_true == 0:
        raise Skip
    f = rng.choice(FN)
    expr = f"{f}(x) = " + coef_term(1, 3, first=True) + coef_term(b, 2) + " + kx " + signed(c)
    # k if student used x = -a
    ka = (-a) ** 3 + b * a * a + c
    k_sign = F(-((-a) ** 3 + b * (-a) ** 2 + c), -a)
    k_drop = F(-(a ** 3 + b * a * a), a)
    ds = []
    if k_sign.denominator == 1 and k_sign != k_true:
        ds.append((M(num(k_sign)), f"Used {M(f'x = {-a}')} instead of {M(f'x = {a}')}. The factor {M(factor(a))} means {M(f'{f}({a}) = 0')}."))
    if k_drop != k_true and k_drop.denominator == 1:
        ds.append((M(num(k_drop)), "Left out the constant term when substituting."))
    ds += [(M(num(-k_true)), "Sign error when solving for k."), (M(num(k_true + 2 * a)), "Arithmetic error when solving for k."),
           (M(num(c)), "That is the constant term, not k.")]
    stem = f"For what value of {M('k')} is {M(factor(a))} a factor of {M(expr)}?"
    work = f"{f}({a}) = {num(a**3)} {signed(b * a * a)} {signed(a)}k {signed(c)} = 0"
    work = work.replace("+ 1k", "+ k").replace("- 1k", "- k")
    return mc("A2.A.APR.A.1", 2, "N", stem, M(num(k_true)), ds,
              f"By the Factor Theorem, {M(f'{f}({a}) = 0')}: {M(work)}, so {M(f'k = {k_true}')}.", rng)


@gen("A2.A.APR.A.1", 12)
def apr_must_be_true(rng):
    f = rng.choice(FN)
    a = rng.choice([-6, -5, -4, -3, -2, 2, 3, 4, 5, 6, 7])
    b = rng.choice([s for s in range(-7, 8) if s not in (0, a, -a)])
    v = rng.choice([s for s in range(-9, 10) if s != 0])
    stem = (f"For a polynomial function {M(f'{f}(x)')}, {M(f'{f}({a}) = 0')} and {M(f'{f}({b}) = {v}')}. Which statement must be true?")
    ans = f"{M(factor(a))} is a factor of {M(f'{f}(x)')}."
    ds = [(f"{M(factor(-a))} is a factor of {M(f'{f}(x)')}.", f"{M(factor(-a))} is a factor when {M(f'{f}({-a}) = 0')}; that is not given."),
          (f"{M(factor(b))} is a factor of {M(f'{f}(x)')}.", f"{M(f'{f}({b}) = {v}')}, which is not 0, so {M(factor(b))} is not a factor."),
          (f"{M(f'{f}(x)')} has exactly one zero.", "Other zeros are possible; nothing limits the number of zeros."),
          (f"{M(factor(v))} is a factor of {M(f'{f}(x)')}.", f"The output {v} does not create a factor.")]
    return mc("A2.A.APR.A.1", 2, "Y", stem, ans, ds,
              f"The Factor Theorem says {M(f'{f}({a}) = 0')} if and only if {M(factor(a))} is a factor.", rng)


@gen("A2.A.APR.A.2", 12)
def apr_zeros_factored(rng):
    a = rng.choice([1, 1, 2, -1, 3])
    roots = sorted(rng.sample([-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6], 3))
    r_lin = None
    f = rng.choice(FN)
    use_lin = rng.random() < 0.35
    parts = []
    zeros = list(roots)
    if use_lin:
        p, q = rng.choice([(2, 1), (2, 3), (3, 1), (3, 2), (2, -1), (3, -4)])
        zeros = roots[:2] + [F(q, p)]
        parts = [factor(roots[0]), factor(roots[1]), f"({p}x {'-' if q > 0 else '+'} {abs(q)})"]
    else:
        parts = [factor(r) for r in roots]
    lead = "" if a == 1 else ("-" if a == -1 else str(a))
    expr = f"{f}(x) = {lead}" + "".join(parts)
    zs = sorted(zeros)
    fmt = lambda L: ", ".join(M(num(F(z))) for z in L)
    ans = fmt(zs)
    flip = sorted(-F(z) for z in zeros)
    ds = [(fmt(flip), "Sign error: the zero of (x − r) is r, not −r."),
          (fmt(sorted(set(zs[:-1] + [F(a)]))) if a not in zs and abs(a) != 1 else fmt(sorted(zs[:-1])), "Missed a zero or treated the leading coefficient as a zero."),
          ]
    for idx in (1, 0, 2):
        trial = list(zs)
        trial[idx] = -F(trial[idx])
        if trial[idx] != zs[idx] and len(set(trial)) == 3:
            ds.append((fmt(sorted(trial)), "Sign error on one factor."))
            break
    if use_lin:
        p_, q_ = parts[2].strip("()").split("x")[0], None
        ds.append((fmt(sorted(roots[:2] + [F(q, 1)])), "For a factor like (px − q), solve px − q = 0; the zero is q/p."))
    stem = f"What are the zeros of {M(expr)}?"
    return mc("A2.A.APR.A.2", 2, "N", stem, ans, ds,
              f"Set each factor equal to 0. The zeros are {ans}.", rng)


@gen("A2.A.APR.A.2", 12)
def apr_zeros_grouping(rng):
    p = rng.choice([-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6])
    q = rng.choice([1, 2, 3, 4, 5, 6])
    if abs(p) == q:
        raise Skip
    lead = rng.choice([1, 1, 1, 2])
    # (lead x - lead p)?? keep lead 1 for clean grouping, or lead 2: 2(x-p)(x^2-q^2)
    c = [1, -p, -q * q, p * q * q]
    c = [lead * k for k in c]
    f = rng.choice(FN)
    zs = sorted([F(p), F(q), F(-q)])
    fmt = lambda L: ", ".join(M(num(z)) for z in L)
    ds = [(fmt(sorted([F(-p), F(q), F(-q)])), f"Sign error in the factor {M(factor(p))}."),
          (fmt(sorted({F(p), F(q * q)})), f"Stopped at {M(f'x^2 - {q*q}')} and used {q*q} instead of solving {M(f'x^2 = {q*q}')}."),
          (fmt(sorted([F(p), F(q)])), f"Missed the negative square root: {M(f'x^2 = {q*q}')} gives {M(f'x = \\pm {q}')}."),
          (fmt(sorted([F(-p), F(q * q)])), "Several sign and square-root errors.")]
    stem = f"What are the zeros of {M(f'{f}(x) = ' + poly(c))}?"
    g = f"x^{{2}}({lin(1, -p)}) - {q*q}({lin(1, -p)})"
    expl = (f"Group: {M(('' if lead == 1 else str(lead)) + g if lead == 1 else f'{lead}[{g}]')}, so "
            f"{M(('' if lead == 1 else str(lead)) + f'({lin(1, -p)})(x^{{2}} - {q*q})')} "
            f"{M('= ' + ('' if lead == 1 else str(lead)) + factor(p) + factor(q) + factor(-q))}. The zeros are {fmt(zs)}.")
    return mc("A2.A.APR.A.2", 2, "N", stem, fmt(zs), ds, expl, rng)


def lin(a, b, var="x"):
    return poly([a, b], var)


@gen("A2.A.APR.A.2", 10)
def apr_graph_description(rng):
    roots = sorted(rng.sample([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5], 3))
    a = rng.choice([1, -1, 2, -2])
    f = rng.choice(FN)
    lead = {1: "", -1: "-", 2: "2", -2: "-2"}[a]
    expr = f"{f}(x) = {lead}" + "".join(factor(r) for r in roots)
    zs = ", ".join(str(r) for r in roots)
    negs = sorted(-r for r in roots)
    if set(negs) == set(roots):
        raise Skip
    neg = ", ".join(str(r) for r in negs)
    up = "falls to the left and rises to the right"
    down = "rises to the left and falls to the right"
    end_ok = up if a > 0 else down
    end_bad = down if a > 0 else up
    ans = f"It crosses the x-axis at {zs} and {end_ok}."
    ds = [(f"It crosses the x-axis at {neg} and {end_ok}.", "Sign error: the zero of (x − r) is r."),
          (f"It crosses the x-axis at {zs} and {end_bad}.", f"A cubic with a {'positive' if a > 0 else 'negative'} leading coefficient {end_ok}."),
          (f"It crosses the x-axis at {neg} and {end_bad}.", "Both the zeros and the end behavior are reversed."),
          (f"It crosses the x-axis at {zs} and rises on both ends.", "That end behavior describes an even-degree function, not a cubic.")]
    return mc("A2.A.APR.A.2", 2, "Y", f"Which statement describes the graph of {M(expr)}?", ans, ds,
              f"The zeros are {zs}. The leading term is {M(('' if a == 1 else ('-' if a == -1 else str(a))) + 'x^{3}')}, so the graph {end_ok}.", rng)


@gen("A2.A.APR.A.2", 10)
def apr_select_zeros(rng):
    k = rng.choice([1, 2, 3, 4, 5, 6, 7])
    a = rng.choice([1, 2, 3, -1])
    f = rng.choice(FN)
    c = [a, 0, -a * k * k, 0]
    cor = [(M(f"x = {r}"), "Correct.") for r in (0, k, -k)]
    wr = [(M(f"x = {k*k}"), f"Used {k*k} instead of its square roots."), (M(f"x = {-k*k}"), "Did not take the square root."),
          (M(f"x = {a}"), "The leading coefficient is not a zero.") if abs(a) != 1 and a not in (k, -k) else (M(f"x = {k + 1}"), "Not a zero; substitute to check."),
          (M(f"x = {2 * k}"), "Not a zero; substitute to check.")]
    rng.shuffle(wr)
    gcf = ("" if a == 1 else ("-" if a == -1 else str(a))) + "x"
    return ms("A2.A.APR.A.2", 2, "N", f"Which values are zeros of {M(f'{f}(x) = ' + poly(c))}?", cor, wr,
              f"Factor out {M(gcf)}: {M(gcf + f'(x^{{2}} - {k*k}) = ' + gcf + factor(k) + factor(-k))}. The zeros are 0, {k}, and {-k}.", rng,
              total=6, tell_count=False)


# ================================================================ Matrices
MAT_CTX = [
    (["Store A", "Store B"], ["Small", "Medium", "Large"], "T-shirts sold"),
    (["Monday", "Tuesday", "Wednesday"], ["Pizza", "Salad"], "orders"),
    (["Team 1", "Team 2", "Team 3"], ["Wins", "Losses", "Ties"], "games"),
    (["Grade 9", "Grade 10", "Grade 11", "Grade 12"], ["Band", "Choir"], "students"),
    (["Week 1", "Week 2"], ["Apples", "Oranges", "Pears", "Bananas"], "pounds of fruit sold"),
    (["Plant 1", "Plant 2", "Plant 3"], ["Chairs", "Desks"], "items made"),
]


@gen("A2.N.M.A.1", 15)
def m_dimensions(rng):
    rows, cols, what = rng.choice(MAT_CTX)
    data = [[rng.randint(4, 60) for _ in cols] for _ in rows]
    i, j = rng.randrange(len(rows)), rng.randrange(len(cols))
    if len(rows) == len(cols):
        raise Skip
    tbl = table([""] + cols, [[r] + [str(v) for v in data[k]] for k, r in enumerate(rows)], row_head=True)
    mode = rng.choice(["dims", "entry", "find"])
    R, C = len(rows), len(cols)
    if mode == "dims":
        stem = f"The matrix shows the number of {what}.{tbl}What are the dimensions of the matrix?"
        ans = f"{R} × {C}"
        ds = [(f"{C} × {R}", "Dimensions are listed as rows × columns."), (f"{R * C} × 1", "Counted entries instead of rows and columns."),
              (f"{R + 1} × {C + 1}", "Counted the labels as rows and columns.")]
        expl = f"There are {R} rows ({', '.join(rows)}) and {C} columns, so the matrix is {R} × {C}."
    elif mode == "entry":
        stem = f"The matrix shows the number of {what}.{tbl}What does the entry in row {i + 1}, column {j + 1} represent?"
        ans = f"{data[i][j]} {what}, {rows[i]}, {cols[j]}"
        ans = f"{data[i][j]}, the number of {what} for {rows[i]} and {cols[j]}"
        alt = [(j, i)] if j < R and i < C else []
        ds = []
        if j < R and i < C:
            ds.append((f"{data[j][i]}, the number of {what} for {rows[j]} and {cols[i]}", "Row and column are switched."))
        oi, oj = (i + 1) % R, (j + 1) % C
        ds += [(f"{data[oi][j]}, the number of {what} for {rows[oi]} and {cols[j]}", f"Row {i + 1} is {rows[i]}."),
               (f"{data[i][oj]}, the number of {what} for {rows[i]} and {cols[oj]}", f"Column {j + 1} is {cols[j]}."),
               (f"{sum(data[i])}, the total number of {what} for {rows[i]}", "An entry is one value, not a row total.")]
        expl = f"Row {i + 1} is {rows[i]} and column {j + 1} is {cols[j]}, so the entry is {data[i][j]}."
    else:
        stem = f"The matrix shows the number of {what}.{tbl}Which entry gives the number of {what} for {rows[i]} and {cols[j]}?"
        ans = f"row {i + 1}, column {j + 1}"
        ds = [(f"row {j + 1}, column {i + 1}", "Rows and columns are switched."),
              (f"row {i + 1}, column {(j + 1) % C + 1}", f"{cols[j]} is column {j + 1}."),
              (f"row {(i + 1) % R + 1}, column {j + 1}", f"{rows[i]} is row {i + 1}.")]
        if j + 1 > R:
            ds[0] = (f"row {(i + 2) % R + 1}, column {(j + 2) % C + 1}", "Find the row label first, then the column label.")
        expl = f"{rows[i]} is row {i + 1} and {cols[j]} is column {j + 1}."
    return mc("A2.N.M.A.1", 1, "Y", stem, ans, ds, expl, rng)


@gen("A2.N.M.A.2", 8)
def m_scalar(rng):
    R, C = rng.choice([(2, 2), (2, 3), (3, 2)])
    prices = [[rng.choice([4, 5, 6, 8, 10, 12, 15, 20, 25, 30]) for _ in range(C)] for _ in range(R)]
    r = rng.choice([0.1, 0.2, 0.25, 0.5])
    up = rng.random() < 0.6
    k = 1 + r if up else 1 - r
    new = [[round(v * k, 2) for v in row] for row in prices]
    fmt = lambda Mx: M(bmatrix([[F(str(v)) if isinstance(v, float) else v for v in row] for row in Mx]))
    def dec(v):
        return F(str(v)).limit_denominator(100)
    show = lambda Mx: M(r"\begin{bmatrix} " + r" \\ ".join(" & ".join(num(float(v)) for v in row) for row in Mx) + r" \end{bmatrix}")
    P = show(prices)
    stem = (f"Matrix {M('P')} shows prices, in dollars, at a shop: {P}. All prices are {'increased' if up else 'decreased'} by "
            f"{pct(r, 0)}. Which matrix shows the new prices?")
    add = [[round(v + (r if up else -r), 2) for v in row] for row in prices]
    only = [[round(v * r, 2) for v in row] for row in prices]
    wrongk = [[round(v * (1 - r if up else 1 + r), 2) for v in row] for row in prices]
    ds = [(show(only), f"That is only the amount of the {'increase' if up else 'decrease'}, {M(num(r) + 'P')}."),
          (show(add), f"{'Added' if up else 'Subtracted'} {num(r)} {'to' if up else 'from'} each price instead of multiplying by {num(k)}."),
          (show(wrongk), f"Used the factor for {'a decrease' if up else 'an increase'}.")]
    return mc("A2.N.M.A.2.a", 2, "Y", stem, show(new), ds,
              f"A {pct(r, 0)} {'increase' if up else 'decrease'} multiplies each price by {num(k)}: {M(num(k) + 'P')}.", rng)


@gen("A2.N.M.A.2", 8)
def m_add_sub(rng):
    rows, cols, what = rng.choice(MAT_CTX[:3] + MAT_CTX[5:])
    R, C = len(rows), len(cols)
    A = [[rng.randint(10, 60) for _ in range(C)] for _ in range(R)]
    B = [[rng.randint(5, 50) for _ in range(C)] for _ in range(R)]
    op = rng.choice(["sum", "diff"])
    if op == "diff":
        B = [[min(B[i][j], A[i][j] - 1) for j in range(C)] for i in range(R)]
        if any(v <= 0 for row in B for v in row):
            raise Skip
    res = [[A[i][j] + B[i][j] if op == "sum" else A[i][j] - B[i][j] for j in range(C)] for i in range(R)]
    mA, mB = M("J = " + bmatrix(A)), M("K = " + bmatrix(B))
    if op == "sum":
        stem = (f"Matrix {M('J')} shows {what} in January and matrix {M('K')} shows {what} in February. Rows are "
                f"{', '.join(rows)}; columns are {', '.join(cols)}.<p>{mA} &nbsp; {mB}</p>Which matrix shows the total for both months?")
    else:
        stem = (f"Matrix {M('J')} shows {what} this year and matrix {M('K')} shows {what} last year. Rows are "
                f"{', '.join(rows)}; columns are {', '.join(cols)}.<p>{mA} &nbsp; {mB}</p>Which matrix shows how many more there were this year than last year?")
    swap = [[res[i][j] for j in range(C)] for i in range(R)]
    wrong1 = [[A[i][j] - B[i][j] if op == "sum" else A[i][j] + B[i][j] for j in range(C)] for i in range(R)]
    wrong2 = [row[:] for row in res]
    wrong2[0][0] += 10
    wrong3 = [[res[i][j] for j in range(C)] for i in range(R)]
    wrong3[-1] = list(reversed(wrong3[-1]))
    if wrong3 == res:
        wrong3[0][-1] -= 10
    ds = [(M(bmatrix(wrong1)), "Used the wrong operation."), (M(bmatrix(wrong2)), "Arithmetic error in the first entry."),
          (M(bmatrix(wrong3)), "Entries were not matched by position.")]
    return mc("A2.N.M.A.2.b", 1, "Y", stem, M(bmatrix(res)), ds,
              f"{'Add' if op == 'sum' else 'Subtract'} entries in matching positions: {M(('J + K' if op == 'sum' else 'J - K') + ' = ' + bmatrix(res))}.", rng)


@gen("A2.N.M.A.2", 7)
def m_multiply(rng):
    rows, items, unit = rng.choice([
        (["Monday", "Tuesday"], ["pizzas", "salads"], "orders"),
        (["Order 1", "Order 2"], ["notebooks", "pens"], "school supplies"),
        (["Saturday", "Sunday"], ["adult tickets", "child tickets"], "tickets"),
        (["Booth A", "Booth B"], ["hats", "scarves"], "items"),
        (["Week 1", "Week 2"], ["bags of rice", "bags of beans"], "bags")])
    Q = [[rng.randint(1, 9) for _ in range(2)] for _ in range(2)]
    C = [[rng.choice([2, 3, 4, 5, 6, 8, 10, 12])] for _ in range(2)]
    if C[0][0] == C[1][0] or Q[0] == Q[1]:
        raise Skip
    res = [[Q[i][0] * C[0][0] + Q[i][1] * C[1][0]] for i in range(2)]
    colwise = [[Q[0][i] * C[0][0] + Q[1][i] * C[1][0]] for i in range(2)]
    entry = [[Q[i][j] * C[j][0] for j in range(2)] for i in range(2)]
    tot = [[sum(Q[i]) * (C[0][0] + C[1][0])] for i in range(2)]
    stem = (f"Matrix {M('Q')} shows how many {items[0]} and {items[1]} were bought ({', '.join(rows)} in the rows). Matrix "
            f"{M('C')} shows the price of each item in dollars.<p>{M('Q = ' + bmatrix(Q))} &nbsp; {M('C = ' + bmatrix(C))}</p>"
            f"Which matrix gives the total cost for each row, {M('QC')}?")
    ds = [(M(bmatrix(colwise)), f"Multiplied columns of {M('Q')} by {M('C')} instead of rows."),
          (M(bmatrix(entry)), "Multiplied entry by entry, without adding the products in each row."),
          (M(bmatrix(tot)), "Added the quantities and the prices before multiplying.")]
    return mc("A2.N.M.A.2.c", 2, "N", stem, M(bmatrix(res)), ds,
              f"Each row of {M('Q')} times the column of {M('C')}: {M(f'{Q[0][0]}({C[0][0]}) + {Q[0][1]}({C[1][0]}) = {res[0][0]}')} and "
              f"{M(f'{Q[1][0]}({C[0][0]}) + {Q[1][1]}({C[1][0]}) = {res[1][0]}')}.", rng)
