"""Functions generators (blueprint category FN)."""
import math

from common import (F, M, Skip, coef_term, comma, factor, gen, lin, mc, money,
                    ms, num, pct, poly, pt, signed, svg_plot, table, xy_table)

FN = ["f", "g", "h", "p", "k"]


def r2(x):
    return round(x, 2)


def dec(x, d=2):
    s = f"{x:.{d}f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s


# ===================================================== A2.F.IF.A.1
@gen("A2.F.IF.A.1", 14)
def ifa1_projectile(rng):
    p = rng.choice([0.5, 1, 1.5, 2, 2.5])
    d = rng.choice([1.5, 2, 2.5, 3, 3.5])
    if d <= p:
        raise Skip
    q = 16 * d * d
    h0 = 16 * (d * d - p * p)
    land = p + d
    f = lambda t: -16 * (t - p) ** 2 + q if 0 <= t <= land + 1e-9 else None
    top = math.ceil(q / 20) * 20 + 20
    ystep = 10 if top <= 120 else 20
    g = svg_plot([f], xr=(0, math.ceil(land) + 1), yr=(0, top), xstep=0.5, ystep=ystep, label_every=2,
                 xlabel="Time (seconds)", ylabel="Height (feet)", points=[(p, q), (0, h0), (land, 0)])
    obj = rng.choice(["ball", "rock", "water balloon", "softball", "beanbag"])
    stem = f"The graph shows the height of a {obj}, in feet, {M('t')} seconds after it is thrown upward.{g}"
    ask = rng.choice(["max", "tmax", "land", "h0", "inc"])
    if ask == "max":
        stem += "What is the maximum height of the " + obj + "?"
        ans = f"{dec(q)} feet"
        ds = [(f"{dec(p)} feet", f"{dec(p)} is the time of the maximum, not the height."),
              (f"{dec(h0)} feet", "That is the starting height."),
              (f"{dec(land)} feet", "That is the time it lands, not a height.")]
        expl = f"The highest point on the graph is {M(pt(dec(p), dec(q)))}, so the maximum height is {dec(q)} feet."
    elif ask == "tmax":
        stem += "How many seconds after it is thrown does the " + obj + " reach its maximum height?"
        ans = f"{dec(p)} seconds"
        ds = [(f"{dec(q)} seconds", "That is the maximum height, not the time."), (f"{dec(land)} seconds", "That is when it lands."),
              (f"{dec(land / 2 + 0.5)} seconds" if land / 2 + 0.5 != p else f"{dec(p + 1)} seconds", "Read the x-coordinate of the highest point.")]
        expl = f"The vertex is at {M(pt(dec(p), dec(q)))}; it reaches the top after {dec(p)} seconds."
    elif ask == "land":
        stem += "When does the " + obj + " hit the ground?"
        ans = f"after {dec(land)} seconds"
        ds = [(f"after {dec(p)} seconds", "That is when it reaches its maximum height."),
              (f"after {dec(2 * p)} seconds" if 2 * p != land else f"after {dec(land + 1)} seconds", "The graph is not symmetric about the start because it begins above the ground."),
              (f"after {dec(h0)} seconds", "That is the starting height in feet.")]
        expl = f"The height is 0 when the graph meets the t-axis, at {M(f't = {dec(land)}')}."
    elif ask == "h0":
        stem += f"What does the {M('h')}-intercept, {M(pt(0, dec(h0)))}, represent?"
        ans = f"The {obj} was thrown from a height of {dec(h0)} feet."
        ds = [(f"The {obj} reaches a maximum height of {dec(h0)} feet.", f"The maximum height is {dec(q)} feet."),
              (f"The {obj} lands after {dec(h0)} seconds.", "The intercept is a height when t = 0."),
              (f"The {obj} rises {dec(h0)} feet each second.", "The intercept is not a rate.")]
        expl = f"At {M('t = 0')}, when it is thrown, the height is {dec(h0)} feet."
    else:
        stem += "Over which interval is the height increasing?"
        ans = M(f"0 < t < {dec(p)}")
        ds = [(M(f"{dec(p)} < t < {dec(land)}"), "On this interval the height is decreasing."),
              (M(f"0 < t < {dec(land)}"), "The height increases only until the maximum."),
              (M(f"0 < t < {dec(q)}"), f"{dec(q)} is a height, not a time.")]
        expl = f"The graph rises from {M('t = 0')} to the maximum at {M(f't = {dec(p)}')}."
    return mc("A2.F.IF.A.1", 2, "Y", stem, ans, ds, expl, rng)


@gen("A2.F.IF.A.1", 8)
def ifa1_sketch(rng):
    start = rng.choice([8, 10, 12, 15])
    level = rng.choice([2, 3, 4, 5])
    if level >= start - 3:
        raise Skip
    rise = rng.random() < 0.5
    if rise:
        what = rng.choice(["height of a growing plant, in inches,", "number of people who have heard a rumor, in hundreds,",
                           "temperature of a pizza warming in an oven, in hundreds of degrees,"])
        a, b = level, start
        desc = (f"starts at {a}, increases quickly at first, and then increases more and more slowly, approaching but never "
                f"reaching {b}")
        correct = lambda x: b - (b - a) * 0.55 ** x
        w1 = lambda x: a + (b - a) * x / 8 if x <= 8 else None
        w2 = lambda x: a * 1.25 ** x
        w3 = lambda x: b - (b - a) * 0.55 ** x if x <= 3 else b - (b - a) * 0.55 ** 3 - (x - 3) * 0.9
        whys = ["This increases at a constant rate.", "This keeps growing faster with no limit.", "This eventually decreases."]
    else:
        what = rng.choice(["water level in a draining tank, in feet,", "temperature of a cooling cup of coffee, in tens of degrees,",
                           "amount of medicine in the blood, in tens of milligrams,"])
        a, b = start, level
        desc = (f"starts at {a}, decreases quickly at first, and then decreases more and more slowly, approaching but never "
                f"reaching {b}")
        correct = lambda x: b + (a - b) * 0.55 ** x
        w1 = lambda x: a - (a - b) * x / 8 if x <= 8 else None
        w2 = lambda x: a * 0.6 ** x
        w3 = lambda x: a - 0.1 * x * x
        whys = ["This decreases at a constant rate and reaches the level.", f"This approaches 0, not {b}.",
                "This decreases more and more quickly."]
    G = lambda fn: svg_plot([fn], xr=(0, 10), yr=(0, 16), xstep=1, ystep=2, label_every=2, width=170, height=140)
    stem = f"The {what} {desc}. Which graph could represent this situation? (Time is on the horizontal axis.)"
    ds = [(G(w1), whys[0]), (G(w2), whys[1]), (G(w3), whys[2])]
    return mc("A2.F.IF.A.1", 2, "Y", stem, G(correct), ds,
              f"The correct graph starts at {a}, changes quickly at first, then levels off toward a horizontal asymptote at {b}.", rng)


@gen("A2.F.IF.A.1", 8)
def ifa1_asymptote_context(rng):
    room = rng.choice([18, 20, 21, 22, 24, 68, 70, 72])
    diff = rng.choice([50, 60, 70, 75, 80, 140, 150])
    b = rng.choice([0.85, 0.88, 0.9, 0.92, 0.95])
    hot = room + diff
    expr = f"T(t) = {room} + {diff}({b})^{{t}}"
    unit = "°C" if room < 30 else "°F"
    stem = (f"The temperature of a cup of soup, in {unit}, {M('t')} minutes after it is served is {M(expr)}. "
            f"As {M('t')} increases, the graph approaches a horizontal asymptote. What does the asymptote represent?")
    ans = f"The soup cools toward the room temperature, {room}{unit}."
    ds = [(f"The soup starts at {room}{unit}.", f"The starting temperature is {M(f'T(0) = {hot}')}{unit}."),
          (f"The soup cools by {diff}{unit} each minute.", f"The temperature is multiplied, not reduced by a fixed amount, and {diff} is the starting difference."),
          (f"The soup cools to 0{unit}.", f"The term {M(f'{diff}({b})^t')} approaches 0, so T approaches {room}, not 0."),
          (f"The soup cools to {hot}{unit}.", f"{hot}{unit} is the starting temperature.")]
    return mc("A2.F.IF.A.1", 2, "Y", stem, ans, ds,
              f"As {M('t')} grows, {M(f'({b})^t')} approaches 0, so {M('T(t)')} approaches {room}: the soup cools toward room temperature.", rng)


# ===================================================== A2.F.IF.A.2
@gen("A2.F.IF.A.2", 12)
def ifa2_formula(rng):
    kind = rng.choice(["exp", "quad", "cubic"])
    f = rng.choice(FN)
    if kind == "exp":
        a, b = rng.choice([2, 3, 4, 5, 10]), rng.choice([2, 3])
        x1 = rng.randint(0, 2)
        x2 = x1 + rng.randint(2, 3)
        F_ = lambda x: a * b ** x
        expr = f"{a}({b})^{{x}}"
    elif kind == "quad":
        a, bb, c = rng.choice([1, 2, -1, 3]), rng.randint(-6, 6), rng.randint(-9, 9)
        F_ = lambda x: a * x * x + bb * x + c
        expr = poly([a, bb, c])
        x1 = rng.randint(-3, 2)
        x2 = x1 + rng.randint(2, 4)
    else:
        a, c = rng.choice([1, -1, 2]), rng.randint(-8, 8)
        F_ = lambda x: a * x ** 3 + c
        expr = poly([a, 0, 0, c])
        x1 = rng.randint(-2, 1)
        x2 = x1 + rng.randint(2, 3)
    y1, y2 = F_(x1), F_(x2)
    rate = F(y2 - y1, x2 - x1)
    ds = [(M(num(F(y2 - y1))), "That is the change in the function's value; divide by the change in x."),
          (M(num(F(y2, x2) if x2 else F(y2))), f"Divided {M(f'{f}({x2})')} by {x2} instead of using both endpoints."),
          (M(num(F(x2 - x1, y2 - y1) if y2 != y1 else F(1, 2))), "The fraction is upside down: change in output over change in input."),
          (M(num(F(y2 + y1, x2 - x1))), "Added the outputs instead of subtracting.")]
    return mc("A2.F.IF.A.2", 2, "Y", f"What is the average rate of change of {M(f'{f}(x) = {expr}')} from {M(f'x = {x1}')} to {M(f'x = {x2}')}?",
              M(num(rate)), ds,
              f"{M(f'{f}({x1}) = {y1}')} and {M(f'{f}({x2}) = {y2}')}, so the rate is {M(f'\\frac{{{y2} - ({y1})}}{{{x2} - ({x1})}} = {num(rate)}')}.", rng)


@gen("A2.F.IF.A.2", 10)
def ifa2_table(rng):
    ctx = rng.choice([("Day", "Visitors", "visitors per day"), ("Year", "Value ($)", "dollars per year"),
                      ("Hour", "Bacteria", "bacteria per hour"), ("Month", "Members", "members per month"),
                      ("Minute", "Temperature (°F)", "degrees per minute")])
    xs = list(range(rng.randint(0, 2), 0, 1)) or []
    x0 = rng.randint(0, 3)
    xs = [x0 + i * rng.choice([1, 2]) for i in range(5)] if False else [x0 + i for i in range(5)]
    a = rng.choice([100, 200, 250, 400, 800])
    b = rng.choice([0.5, 0.8] if "Temperature" in ctx[1] or "Value" in ctx[1] else [1.5, 2, 0.5, 1.2, 0.8])
    ys = [round(a * b ** (x - x0)) for x in xs]
    i, j = sorted(rng.sample(range(5), 2))
    if j - i < 2:
        raise Skip
    rate = F(ys[j] - ys[i], xs[j] - xs[i])
    if rate.denominator not in (1, 2, 4):
        raise Skip
    tbl = xy_table(xs, ys, ctx[0], ctx[1])
    stem = (f"The table shows values of a function.{tbl}What is the average rate of change from {ctx[0].lower()} {xs[i]} to "
            f"{ctx[0].lower()} {xs[j]}?")
    ds = [(f"{num(F(ys[j] - ys[i]))} {ctx[2]}", f"That is the total change; divide by {xs[j] - xs[i]}."),
          (f"{num(F(ys[i + 1] - ys[i]))} {ctx[2]}", "That is the rate over only the first step of the interval."),
          (f"{num(F(ys[j], xs[j]) if xs[j] else F(ys[j]))} {ctx[2]}", "Used only one point; rate of change needs two."),
          (f"{dec(float(rate) * -1)} {ctx[2]}", "Subtracted in the wrong order.")]
    return mc("A2.F.IF.A.2", 2, "Y", stem, f"{dec(float(rate))} {ctx[2]}", ds,
              f"{M(f'\\frac{{{ys[j]} - {ys[i]}}}{{{xs[j]} - {xs[i]}}} = {num(rate)}')} {ctx[2]}.", rng)


@gen("A2.F.IF.A.2", 8)
def ifa2_graph(rng):
    a = rng.choice([-1, -2, 1, 2])
    h = rng.randint(-2, 2)
    k = rng.randint(-3, 3)
    f = lambda x: 0.5 * a * (x - h) ** 2 + k if a else None
    xs = [x for x in range(-5, 6) if abs(f(x)) <= 8 and float(f(x)).is_integer()]
    if len(xs) < 4:
        raise Skip
    x1, x2 = sorted(rng.sample(xs, 2))
    if x2 - x1 < 2:
        raise Skip
    y1, y2 = f(x1), f(x2)
    rate = F(int(y2 - y1), x2 - x1)
    g = svg_plot([f], xr=(-6, 6), yr=(-9, 9), points=[(x1, y1), (x2, y2)], label_every=2)
    stem = f"The graph of {M('y = f(x)')} is shown.{g}What is the average rate of change of {M('f')} from {M(f'x = {x1}')} to {M(f'x = {x2}')}?"
    ds = [(M(num(F(int(y2 - y1)))), "That is the change in y; divide by the change in x."),
          (M(num(-rate)) if rate != 0 else M("1"), "Subtracted in the wrong order for one of the coordinates."),
          (M(num(F(x2 - x1, int(y2 - y1)))) if y2 != y1 else M(num(F(x2 - x1))), "The fraction is upside down."),
          (M(num(rate + 1)), "Misread a point on the graph.")]
    return mc("A2.F.IF.A.2", 2, "Y", stem, M(num(rate)), ds,
              f"The points are {M(pt(x1, int(y1)))} and {M(pt(x2, int(y2)))}. Rate {M(f'= \\frac{{{int(y2)} - ({int(y1)})}}{{{x2} - ({x1})}} = {num(rate)}')}.", rng)


# ===================================================== A2.F.IF.A.3
@gen("A2.F.IF.A.3", 6)
def ifa3_scale(rng):
    shape, formula, var, power = rng.choice([
        ("square", "A(s) = s^{2}", "side length", 2), ("circle", "A(r) = \\pi r^{2}", "radius", 2),
        ("cube", "V(s) = s^{3}", "edge length", 3), ("sphere", "V(r) = \\frac{4}{3}\\pi r^{3}", "radius", 3),
        ("cube", "S(s) = 6s^{2}", "edge length", 2), ("sphere", "S(r) = 4\\pi r^{2}", "radius", 2)])
    k = rng.choice([2, 3, 4, 5, 10])
    what = {"A": "area", "V": "volume", "S": "surface area"}[formula[0]]
    word = {2: "doubled", 3: "tripled", 4: "multiplied by 4", 5: "multiplied by 5", 10: "multiplied by 10"}[k]
    stem = f"The {what} of a {shape} is given by {M(formula)}. If the {var} is {word}, what happens to the {what}?"
    ans = f"It is multiplied by {k ** power}."
    ds = [(f"It is multiplied by {k}.", f"The {what} depends on the {var} raised to the power {power}."),
          (f"It is multiplied by {k * power}.", f"Multiplied {k} by the exponent instead of raising {k} to it."),
          (f"It is multiplied by {k ** (5 - power)}.", f"The exponent on the {var} is {power}."),
          (f"It increases by {k}.", "Scaling a length multiplies the measure; it does not add.")]
    return mc("A2.F.IF.A.3", 2, "Y", stem, ans, ds,
              f"Replacing the {var} with {k} times itself multiplies the {what} by {M(f'{k}^{{{power}}} = {k ** power}')}.", rng)


@gen("A2.F.IF.A.3", 6)
def ifa3_rewrite(rng):
    choice = rng.choice([
        ("the area of a circle", "diameter", "d", "A(d) = \\frac{\\pi d^{2}}{4}",
         [("A(d) = \\pi d^{2}", "The radius is d/2, not d."), ("A(d) = \\frac{\\pi d^{2}}{2}", "(d/2)² = d²/4."), ("A(d) = 2\\pi d", "That is not an area formula.")]),
        ("the area of a square", "perimeter", "P", "A(P) = \\frac{P^{2}}{16}",
         [("A(P) = \\frac{P^{2}}{4}", "The side is P/4, so the area is (P/4)²."), ("A(P) = 4P", "Area is the side squared."), ("A(P) = \\frac{P}{4}", "That is the side length.")]),
        ("the volume of a cube", "surface area", "S", "V(S) = \\left(\\frac{S}{6}\\right)^{\\frac{3}{2}}",
         [("V(S) = \\frac{S^{3}}{6}", "The edge is √(S/6), then cube it."), ("V(S) = \\left(\\frac{S}{6}\\right)^{3}", "S/6 is the edge squared, not the edge."), ("V(S) = \\frac{S}{6}", "That is the area of one face.")]),
        ("the area of an equilateral triangle", "perimeter", "P", "A(P) = \\frac{\\sqrt{3}}{36}P^{2}",
         [("A(P) = \\frac{\\sqrt{3}}{4}P^{2}", "The side is P/3, so square P/3."), ("A(P) = \\frac{\\sqrt{3}}{12}P^{2}", "(P/3)² = P²/9."), ("A(P) = \\frac{P^{2}}{9}", "Left out the √3/4 factor.")]),
        ("the circumference of a circle", "area", "A", "C(A) = 2\\sqrt{\\pi A}",
         [("C(A) = 2\\pi A", "First find r = √(A/π)."), ("C(A) = \\sqrt{\\frac{A}{\\pi}}", "That is the radius."), ("C(A) = \\frac{2A}{\\pi}", "Use r = √(A/π), then C = 2πr.")]),
        ("the area of a circle", "circumference", "C", "A(C) = \\frac{C^{2}}{4\\pi}",
         [("A(C) = \\frac{C^{2}}{2\\pi}", "r = C/(2π), so r² = C²/(4π²)."), ("A(C) = \\pi C^{2}", "C is not the radius."), ("A(C) = \\frac{C}{2}", "Area is not half the circumference.")]),
    ])
    what, by, v, ans, ds = choice
    stem = f"Which function gives {what} in terms of its {by}, {M(v)}?"
    return mc("A2.F.IF.A.3", 2, "Y", stem, M(ans), [(M(t), w) for t, w in ds],
              f"Write the usual formula, then replace the length with an expression in {M(v)}: {M(ans)}.", rng)


# ===================================================== A2.F.IF.B.4
@gen("A2.F.IF.B.4", 10)
def ifb4_exp_features(rng):
    a = rng.choice([1, 2, 3, 4, -1, -2])
    b = rng.choice([2, 3, F(1, 2), F(1, 3)])
    k = rng.randint(-5, 5)
    f = rng.choice(FN)
    expr = f"{'' if a == 1 else ('-' if a == -1 else a)}({num(b)})^{{x}} {signed(k) if k else ''}".strip()
    ask = rng.choice(["asym", "yint", "range"])
    if ask == "asym":
        stem = f"What is the horizontal asymptote of the graph of {M(f'{f}(x) = {expr}')}?"
        ans = M(f"y = {k}")
        ds = [(M(f"y = {a + k}"), "That is the y-intercept."), (M(f"y = {a}"), "The coefficient stretches the graph; it does not set the asymptote."),
              (M(f"y = {-k}"), "Sign error on the vertical shift."), (M("y = 0") if k else M("y = 1"), "The graph is shifted vertically, so the asymptote moves too.")]
        expl = f"{M(f'({num(b)})^x')} approaches 0 at one end, so {M(f'{f}(x)')} approaches {k}."
    elif ask == "yint":
        stem = f"What is the y-intercept of the graph of {M(f'{f}(x) = {expr}')}?"
        ans = M(pt(0, a + k))
        ds = [(M(pt(0, k)), "That is the asymptote's height. At x = 0 the power equals 1."),
              (M(pt(0, a)), f"Forgot to add the shift {k}." if k else "Check the power at x = 0."),
              (M(pt(0, a * b + k)), "At x = 0 the power is 1, not the base."),
              (M(pt(a + k, 0)), "A y-intercept has x-coordinate 0.")]
        expl = f"{M(f'{f}(0) = {a}({num(b)})^0 {signed(k)} = {a + k}')}." if k else f"{M(f'{f}(0) = {a}')}."
    else:
        stem = f"What is the range of {M(f'{f}(x) = {expr}')}?"
        ans = M(f"y > {k}") if a > 0 else M(f"y < {k}")
        ds = [(M(f"y < {k}") if a > 0 else M(f"y > {k}"), "A positive coefficient keeps the graph above the asymptote; a negative one flips it below."),
              (M("\\text{all real numbers}"), "An exponential graph never crosses its horizontal asymptote."),
              (M(f"y \\ge {k}") if a > 0 else M(f"y \\le {k}"), f"The graph never reaches {k}."),
              (M(f"y > {a + k}"), "The y-intercept is not the boundary of the range.")]
        expl = f"The asymptote is {M(f'y = {k}')}, and the graph is {'above' if a > 0 else 'below'} it."
    return mc("A2.F.IF.B.4", 2, "N", stem, ans, ds, expl, rng)


@gen("A2.F.IF.B.4", 10)
def ifb4_domain_range(rng):
    kind = rng.choice(["sqrt", "log", "cbrt", "sqrt_neg"])
    h = rng.randint(-6, 6)
    k = rng.randint(-5, 5)
    f = rng.choice(FN)
    if kind == "sqrt":
        expr = f"\\sqrt{{{lin(1, -h)}}} {signed(k) if k else ''}"
        ask = rng.choice(["domain", "range"])
        if ask == "domain":
            ans = M(f"x \\ge {h}")
            ds = [(M(f"x \\ge {-h}"), "Sign error: solve x − h ≥ 0."), (M(f"x > {h}"), f"x = {h} is allowed; the square root of 0 is 0."),
                  (M(f"x \\ge {k}"), "The vertical shift does not affect the domain."), (M("\\text{all real numbers}"), "The radicand must be at least 0.")]
            expl = f"The radicand must be nonnegative: {M(f'{lin(1, -h)} \\ge 0')}, so {M(f'x \\ge {h}')}."
        else:
            ans = M(f"y \\ge {k}")
            ds = [(M(f"y \\ge {h}"), "The horizontal shift affects the domain, not the range."), (M(f"y > {k}"), f"The value {k} is reached at x = {h}."),
                  (M(f"y \\le {k}"), "A square root is at least 0, so the outputs are at least the shift."), (M(f"y \\ge {-k}"), "Sign error on the vertical shift.")]
            expl = f"{M(f'\\sqrt{{{lin(1, -h)}}} \\ge 0')}, so {M(f'{f}(x) \\ge {k}')}."
    elif kind == "sqrt_neg":
        expr = f"\\sqrt{{{lin(-1, h)}}} {signed(k) if k else ''}"
        ans = M(f"x \\le {h}")
        ds = [(M(f"x \\ge {h}"), f"Solve {M(f'{lin(-1, h)} \\ge 0')}; dividing by −1 flips the inequality."), (M(f"x \\ge {-h}"), "Sign errors when solving the inequality."),
              (M(f"x < {h}"), f"x = {h} is allowed."), (M(f"x \\le {-h}"), "Sign error on the constant.")]
        expl = f"{M(f'{lin(-1, h)} \\ge 0')} gives {M(f'x \\le {h}')}."
        ask = "domain"
    elif kind == "log":
        base = rng.choice([2, 3, 10])
        expr = f"\\log_{{{base}}}({lin(1, -h)}) {signed(k) if k else ''}"
        ans = M(f"x > {h}")
        ds = [(M(f"x \\ge {h}"), "The log of 0 is undefined, so the inequality is strict."), (M(f"x > {-h}"), "Sign error: solve x − h > 0."),
              (M(f"x > {k}"), "The vertical shift does not affect the domain."), (M("x > 0"), "The graph is shifted horizontally.")]
        expl = f"The argument must be positive: {M(f'{lin(1, -h)} > 0')}, so {M(f'x > {h}')}."
        ask = "domain"
    else:
        expr = f"\\sqrt[3]{{{lin(1, -h)}}} {signed(k) if k else ''}"
        ans = M("\\text{all real numbers}")
        ds = [(M(f"x \\ge {h}"), "Cube roots of negative numbers are defined."), (M(f"x > {h}"), "Cube roots are defined for every real number."),
              (M(f"x \\ge {k}"), "Cube roots are defined for every real number."), (M("x \\ge 0"), "Cube roots of negative numbers are real.")]
        expl = "Every real number has a real cube root, so the domain is all real numbers."
        ask = "domain"
    stem = f"What is the {ask} of {M(f'{f}(x) = {expr}'.strip())}?"
    return mc("A2.F.IF.B.4", 2, "N", stem, ans, ds, expl, rng)


@gen("A2.F.IF.B.4", 10)
def ifb4_abs_vertex(rng):
    a = rng.choice([1, 2, 3, -1, -2, F(1, 2)])
    h = rng.randint(-6, 6)
    k = rng.randint(-6, 6)
    f = rng.choice(FN)
    lead = "" if a == 1 else ("-" if a == -1 else num(a))
    inside = lin(1, -h) if h else "x"
    expr = f"{lead}|{inside}| {signed(k) if k else ''}".strip()
    ask = rng.choice(["vertex", "range", "inc"])
    if ask == "vertex":
        ans = M(pt(h, k))
        ds = [(M(pt(-h, k)), "Sign error: |x − h| has its vertex at x = h."), (M(pt(k, h)), "Coordinates are switched."),
              (M(pt(h, -k)), "Sign error on the vertical shift."), (M(pt(-h, -k)), "Sign errors on both shifts.")]
        q = "What is the vertex of the graph of"
        expl = f"The graph of {M(f'a|x - h| + k')} has its vertex at {M('(h, k)')} = {M(pt(h, k))}."
    elif ask == "range":
        ans = M(f"y \\ge {k}") if a > 0 else M(f"y \\le {k}")
        ds = [(M(f"y \\le {k}") if a > 0 else M(f"y \\ge {k}"), "The graph opens " + ("up" if a > 0 else "down") + "."),
              (M(f"y \\ge {h}") if a > 0 else M(f"y \\le {h}"), "The range depends on the vertical shift."),
              (M("\\text{all real numbers}"), "An absolute value graph has a minimum or maximum."),
              (M(f"y > {k}") if a > 0 else M(f"y < {k}"), f"The vertex value {k} is included.")]
        q = "What is the range of"
        expl = f"The vertex is {M(pt(h, k))} and the graph opens {'up' if a > 0 else 'down'}."
    else:
        ans = M(f"x > {h}") if a > 0 else M(f"x < {h}")
        ds = [(M(f"x < {h}") if a > 0 else M(f"x > {h}"), "That is where the graph decreases."), (M(f"x > {-h}") if a > 0 else M(f"x < {-h}"), "Sign error on the vertex."),
              (M(f"x > {k}") if a > 0 else M(f"x < {k}"), "Use the x-coordinate of the vertex."), (M("\\text{all real numbers}"), "The graph changes direction at the vertex.")]
        q = "Over which interval is the function increasing for"
        expl = f"The vertex is at {M(f'x = {h}')}. The graph opens {'up, so it increases to the right' if a > 0 else 'down, so it increases to the left'} of the vertex."
    return mc("A2.F.IF.B.4", 2, "N", f"{q} {M(f'{f}(x) = {expr}')}?", ans, ds, expl, rng)


# ===================================================== A2.F.IF.B.5
@gen("A2.F.IF.B.5", 14)
def ifb5_vertex_form(rng):
    a = rng.choice([1, 1, 2, -1, -2, 3])
    h = rng.randint(-6, 6)
    k = rng.randint(-12, 12)
    if h == 0:
        raise Skip
    f = rng.choice(FN)
    std = poly([a, -2 * a * h, a * h * h + k])
    vform = f"{'' if a == 1 else ('-' if a == -1 else a)}{factor(h)}^{{2}} {signed(k) if k else ''}".strip()
    ask = rng.choice(["form", "extreme"])
    if ask == "form":
        stem = f"Which form of {M(f'{f}(x) = {std}')} shows the {'minimum' if a > 0 else 'maximum'} value of the function?"
        ans = M(f"{f}(x) = {vform}")
        bad1 = f"{'' if a == 1 else ('-' if a == -1 else a)}{factor(-h)}^{{2}} {signed(k)}".strip()
        bad2 = f"{'' if a == 1 else ('-' if a == -1 else a)}{factor(h)}^{{2}} {signed(k + a * h * h)}".strip()
        bad3 = f"{'' if a == 1 else ('-' if a == -1 else a)}{factor(h)}^{{2}} {signed(-k)}".strip()
        ds = [(M(f"{f}(x) = {bad1}"), "Sign error inside the square."), (M(f"{f}(x) = {bad2}"), "When completing the square, subtract the added term back out."),
              (M(f"{f}(x) = {bad3}"), "Sign error on the constant.")]
        expl = f"Completing the square gives {M(vform)}. The {'minimum' if a > 0 else 'maximum'} value is {k}, at {M(f'x = {h}')}."
    else:
        stem = f"The function {M(f'{f}(x) = {std}')} can be written as {M(f'{f}(x) = {vform}')}. What is the {'minimum' if a > 0 else 'maximum'} value of {M(f)}?"
        ans = M(str(k))
        ds = [(M(str(h)), "That is the x-value where it occurs."), (M(str(a * h * h + k)), "That is the y-intercept."),
              (M(str(-k)), "Sign error."), (M(str(-h)), "That is the opposite of the x-value of the vertex.")]
        expl = f"In vertex form, the {'minimum' if a > 0 else 'maximum'} value is the constant {k}, reached at {M(f'x = {h}')}."
    return mc("A2.F.IF.B.5.a", 2, "N", stem, ans, ds, expl, rng)


@gen("A2.F.IF.B.5", 14)
def ifb5_exponential(rng):
    kind = rng.choice(["shift", "shift", "monthly", "halflife"])
    if kind == "shift":
        a = rng.choice([2, 3, 4, 5, 10])
        b = rng.choice([2, 3])
        s = rng.choice([1, 2, 3])
        if b ** s > 30:
            raise Skip
        newc = F(a) * F(b) ** s
        expr = f"{a}({b})^{{t {signed(s)}}}"
        ctx = rng.choice(["bacteria in a sample", "views of a video, in thousands,", "fish in a pond"])
        stem = f"The number of {ctx} after {M('t')} days is modeled by {M(f'N(t) = {expr}')}. Which equivalent function shows the initial amount?"
        ans = M(f"N(t) = {num(newc)}({b})^{{t}}")
        ds = [(M(f"N(t) = {a * b * s}({b})^{{t}}"), f"Multiplied by {b} × {s} instead of by {M(f'{b}^{{{s}}}')}." if s > 1 else "Check the power."),
              (M(f"N(t) = {a}({b})^{{t}} + {s}"), "Exponent rules turn the shift into a factor, not a sum."),
              (M(f"N(t) = {a + b ** s}({b})^{{t}}"), f"Added {M(f'{b}^{{{s}}}')} instead of multiplying by it."),
              (M(f"N(t) = {num(F(a) / F(b) ** s)}({b})^{{t}}"), "Sign error on the exponent; adding to the exponent multiplies.")]
        expl = f"{M(f'{b}^{{t {signed(s)}}} = {b}^{{t}} \\cdot {b}^{{{s}}}')}, so {M(f'N(t) = {a} \\cdot {num(F(b) ** s)} \\cdot {b}^t = {num(newc)}({b})^t')}. The initial amount is {num(newc)}."
        return mc("A2.F.IF.B.5.b", 2, "N", stem, ans, ds, expl, rng)
    if kind == "monthly":
        r = rng.choice([0.06, 0.08, 0.1, 0.12, 0.15, 0.2])
        b = 1 + r
        m = b ** (1 / 12)
        P = rng.choice([500, 1000, 2500, 5000])
        stem = (f"An account balance is modeled by {M(f'A(t) = {comma(P).replace(',', '{,}')}({dec(b)})^{{t}}')}, where {M('t')} is in years. "
                f"Which expression is equivalent and shows the approximate monthly growth rate?")
        ans = M(f"{comma(P).replace(',', '{,}')}({dec(m, 4)})^{{12t}}")
        ds = [(M(f"{comma(P).replace(',', '{,}')}({dec(1 + r / 12, 4)})^{{t}}"), "Dividing the annual rate by 12 ignores compounding, and the exponent must be 12t."),
              (M(f"{comma(P).replace(',', '{,}')}({dec(b ** 12, 2)})^{{\\frac{{t}}{{12}}}}"), "Raised the base to the 12th power instead of the 1/12 power."),
              (M(f"{comma(P).replace(',', '{,}')}({dec(m, 4)})^{{t}}"), "With a monthly factor, the exponent counts months: 12t.")]
        expl = (f"{M(f'({dec(b)})^t = \\left(({dec(b)})^{{1/12}}\\right)^{{12t}} \\approx ({dec(m, 4)})^{{12t}}')}, so the balance grows about "
                f"{pct(m - 1, 2)} each month.")
        return mc("A2.F.IF.B.5.b", 2, "Y", stem, ans, ds, expl, rng)
    hl = rng.choice([2, 3, 4, 5, 6, 8])
    A0 = rng.choice([80, 100, 200, 400, 640])
    stem = (f"The amount of a substance, in milligrams, after {M('t')} hours is {M(f'A(t) = {A0}\\left(\\frac{{1}}{{2}}\\right)^{{\\frac{{t}}{{{hl}}}}}')}. "
            f"What does the {hl} represent?")
    ans = f"The amount is cut in half every {hl} hours."
    ds = [(f"The amount decreases by {hl} milligrams each hour.", "The model is exponential, not linear."),
          (f"The amount is cut in half every hour.", f"The exponent is t/{hl}, so one halving takes {hl} hours."),
          (f"There are {hl} milligrams left after {hl} hours.", f"After {hl} hours there are {num(F(A0, 2))} milligrams."),
          (f"The amount is divided by {hl} every hour.", "The base 1/2 means halving; the denominator sets the time it takes.")]
    return mc("A2.F.IF.B.5.b", 2, "Y", stem, ans, ds,
              f"When {M(f't = {hl}')}, the exponent is 1 and the amount is {M(f'{A0} \\cdot \\frac{{1}}{{2}}')}. Every {hl} hours the amount halves.", rng)


# ===================================================== A2.F.IF.B.6
@gen("A2.F.IF.B.6", 12)
def ifb6_compare(rng):
    a = rng.choice([-1, 1, 2, -2])
    h = rng.randint(-3, 3)
    k = rng.randint(-6, 6)
    fexpr = f"{'' if a == 1 else ('-' if a == -1 else a)}{factor(h)}^{{2}} {signed(k) if k else ''}".strip()
    xs = list(range(-2, 3))
    g = lambda x: 2 ** x * rng_c + d
    rng_c = rng.choice([1, 2, 3])
    d = rng.randint(-5, 5)
    ys = [num(F(rng_c) * F(2) ** x + d) for x in xs]
    tbl = xy_table(xs, ys, "x", "g(x)")
    ask = rng.choice(["yint", "rate"])
    fy0 = a * h * h + k
    gy0 = rng_c + d
    if ask == "yint" and fy0 != gy0:
        stem = f"Function {M('f')} is defined by {M(f'f(x) = {fexpr}')}. Function {M('g')} is shown in the table.{tbl}Which statement is true?"
        big = "f" if fy0 > gy0 else "g"
        small = "g" if big == "f" else "f"
        ans = f"{M(big)} has the greater y-intercept."
        ds = [(f"{M(small)} has the greater y-intercept.", f"{M(f'f(0) = {fy0}')} and {M(f'g(0) = {gy0}')}."),
              ("They have the same y-intercept.", f"{M(f'f(0) = {fy0}')} and {M(f'g(0) = {gy0}')}."),
              (f"The y-intercept of {M('f')} is {k}.", f"Substitute x = 0: {M(f'f(0) = {fy0}')}." if fy0 != k else "Check both functions at x = 0.")]
        expl = f"{M(f'f(0) = {fy0}')} and from the table {M(f'g(0) = {gy0}')}."
    else:
        fr = F((a * (2 - h) ** 2 + k) - (a * (0 - h) ** 2 + k), 2)
        gr = F(F(rng_c) * 4 + d - (rng_c + d), 2)
        if fr == gr:
            raise Skip
        stem = (f"Function {M('f')} is defined by {M(f'f(x) = {fexpr}')}. Function {M('g')} is shown in the table.{tbl}"
                f"Which statement compares the average rates of change from {M('x = 0')} to {M('x = 2')}?")
        big = "f" if fr > gr else "g"
        small = "g" if big == "f" else "f"
        ans = f"{M(big)} has the greater rate: {num(max(fr, gr))} compared with {num(min(fr, gr))}."
        ds = [(f"{M(small)} has the greater rate: {num(max(fr, gr))} compared with {num(min(fr, gr))}.", "The rates are matched to the wrong functions."),
              ("The rates are equal.", f"The rates are {num(fr)} for f and {num(gr)} for g."),
              (f"{M(big)} has the greater rate: {num(max(fr, gr) * 2)} compared with {num(min(fr, gr) * 2)}.", "Divide the change in y by the change in x, 2.")]
        expl = f"For {M('f')}: {M(f'\\frac{{f(2) - f(0)}}{{2}} = {num(fr)}')}. For {M('g')}: {M(f'\\frac{{g(2) - g(0)}}{{2}} = {num(gr)}')}."
    return mc("A2.F.IF.B.6.a", 2, "Y", stem, ans, ds, expl, rng)


@gen("A2.F.IF.B.6", 8)
def ifb6_intervals(rng):
    kind = rng.choice(["quad", "cubic"])
    if kind == "quad":
        a = rng.choice([1, -1, 2])
        h = rng.randint(-2, 3)
        k = rng.randint(-5, 5)
        f = lambda x: a * (x - h) ** 2 + k
        expr = f"{'' if a == 1 else ('-' if a == -1 else a)}{factor(h)}^{{2}} {signed(k) if k else ''}".strip()
    else:
        c = rng.randint(-5, 5)
        f = lambda x: x ** 3 - 3 * x + c
        expr = poly([1, 0, -3, c])
    x1 = rng.randint(-3, 0)
    I1 = (x1, x1 + 2)
    I2 = (x1 + 2, x1 + 4)
    r1 = F(f(I1[1]) - f(I1[0]), 2)
    r2_ = F(f(I2[1]) - f(I2[0]), 2)
    if r1 == r2_:
        raise Skip
    stem = (f"For {M(f'f(x) = {expr}')}, compare the average rate of change on {M(f'[{I1[0]}, {I1[1]}]')} with the average rate of "
            f"change on {M(f'[{I2[0]}, {I2[1]}]')}. Which statement is true?")
    if r1 > r2_:
        ans = f"The rate on {M(f'[{I1[0]}, {I1[1]}]')} is greater."
        wrong = f"The rate on {M(f'[{I2[0]}, {I2[1]}]')} is greater."
    else:
        ans = f"The rate on {M(f'[{I2[0]}, {I2[1]}]')} is greater."
        wrong = f"The rate on {M(f'[{I1[0]}, {I1[1]}]')} is greater."
    ds = [(wrong, f"The rates are {num(r1)} and {num(r2_)}."), ("The rates are equal.", "A nonlinear function does not change at a constant rate."),
          ("The rates cannot be compared without a graph.", "Each rate can be found from the equation.")]
    return mc("A2.F.IF.B.6.b", 2, "Y", stem, ans, ds,
              f"On {M(f'[{I1[0]}, {I1[1]}]')}: {M(f'\\frac{{{f(I1[1])} - ({f(I1[0])})}}{{2}} = {num(r1)}')}. On {M(f'[{I2[0]}, {I2[1]}]')}: "
              f"{M(f'\\frac{{{f(I2[1])} - ({f(I2[0])})}}{{2}} = {num(r2_)}')}.", rng)


# ===================================================== A2.F.BF.A.1
@gen("A2.F.BF.A.1", 12)
def bfa1_profit(rng):
    item = rng.choice(["candles", "bracelets", "T-shirts", "phone cases", "mugs", "posters"])
    price = rng.choice([8, 10, 12, 15, 18, 20, 25])
    fixed = rng.choice([150, 200, 300, 450, 600, 800])
    unit = rng.choice([2, 3, 4, 5, 6])
    if unit >= price:
        raise Skip
    mode = rng.choice(["profit", "profit", "avgcost"])
    if mode == "profit":
        stem = (f"A student sells {item}. The revenue is {M(f'R(x) = {price}x')} and the cost is {M(f'C(x) = {fixed} + {unit}x')}, "
                f"where {M('x')} is the number of {item}. Which function gives the profit, {M('P(x)')}?")
        ans = M(f"P(x) = {price - unit}x - {fixed}")
        ds = [(M(f"P(x) = {price + unit}x + {fixed}"), "Profit is revenue minus cost, not their sum."),
              (M(f"P(x) = {price - unit}x + {fixed}"), "Subtract all of the cost, including the fixed cost."),
              (M(f"P(x) = {fixed} - {price - unit}x"), "That is cost minus revenue."),
              (M(f"P(x) = {price}x - {unit}x"), f"The fixed cost of {fixed} is missing.")]
        expl = f"{M(f'P(x) = R(x) - C(x) = {price}x - ({fixed} + {unit}x) = {price - unit}x - {fixed}')}."
    else:
        stem = (f"The cost to make {M('x')} {item} is {M(f'C(x) = {fixed} + {unit}x')}. Which function gives the average cost per item, {M('A(x)')}?")
        ans = M(f"A(x) = \\frac{{{fixed} + {unit}x}}{{x}}")
        ds = [(M(f"A(x) = \\frac{{{fixed}}}{{x}} + {unit}x"), f"Divide every term of C(x) by x; {M(f'{unit}x')} ÷ x = {unit}."),
              (M(f"A(x) = {fixed} + \\frac{{{unit}}}{{x}}"), "Divide the fixed cost by x as well."),
              (M(f"A(x) = x({fixed} + {unit}x)"), "Average cost divides by the number of items.")]
        expl = f"Average cost = total cost ÷ number of items = {M(f'\\frac{{{fixed} + {unit}x}}{{x}}')}."
    return mc("A2.F.BF.A.1.a", 2, "Y", stem, ans, ds, expl, rng)


@gen("A2.F.BF.A.1", 13)
def bfa1_compose(rng):
    kind = rng.choice(["discount_tax", "coupon_pct", "units", "evaluate"])
    if kind == "discount_tax":
        off = rng.choice([5, 10, 15, 20])
        tax = rng.choice([0.05, 0.07, 0.08, 0.0925, 0.1])
        stem = (f"An item with original price {M('x')} dollars is on sale for {money(off)} off: {M(f'g(x) = x - {off}')}. Sales tax of "
                f"{pct(tax, 2)} is then added: {M(f'f(x) = {dec(1 + tax, 4)}x')}. Which function gives the final price?")
        ans = M(f"f(g(x)) = {dec(1 + tax, 4)}(x - {off})")
        ds = [(M(f"g(f(x)) = {dec(1 + tax, 4)}x - {off}"), "This takes the discount after tax; the discount comes first."),
              (M(f"f(g(x)) = {dec(1 + tax, 4)}x - {off}"), f"The tax applies to the discounted price, so multiply all of {M(f'x - {off}')}."),
              (M(f"f(g(x)) = {dec(tax, 4)}(x - {off})"), "That is only the tax amount.")]
        expl = f"Apply {M('g')} first, then {M('f')}: {M(f'f(g(x)) = {dec(1 + tax, 4)}(x - {off})')}."
    elif kind == "coupon_pct":
        p = rng.choice([0.1, 0.15, 0.2, 0.25, 0.3])
        ship = rng.choice([4, 5, 6, 8, 10])
        stem = (f"A store takes {pct(p, 0)} off the price {M('x')} and then adds {money(ship)} shipping. Let {M(f'd(x) = {dec(1 - p)}x')} and "
                f"{M(f's(x) = x + {ship}')}. Which expression gives the total cost?")
        ans = M(f"s(d(x)) = {dec(1 - p)}x + {ship}")
        ds = [(M(f"d(s(x)) = {dec(1 - p)}(x + {ship})"), "This discounts the shipping too; the discount is taken first."),
              (M(f"s(d(x)) = {dec(p)}x + {ship}"), f"The customer pays {pct(1 - p, 0)} of the price, not {pct(p, 0)}."),
              (M(f"s(x) + d(x) = {dec(2 - p)}x + {ship}"), "Adding the functions counts the price twice.")]
        expl = f"Discount first, then shipping: {M(f's(d(x)) = {dec(1 - p)}x + {ship}')}."
    elif kind == "units":
        stem_opts = [("A recipe uses {M('c(n) = 0.75n')} cups of flour for {M('n')} servings. One cup is 16 tablespoons: {M('t(c) = 16c')}.",
                      "t(c(n)) = 12n", "tablespoons of flour for n servings",
                      [("c(t(n)) = 12n", "Convert servings to cups first, then cups to tablespoons: t(c(n))."), ("t(c(n)) = 16.75n", "Composition multiplies here; it does not add."),
                       ("t(c(n)) = \\frac{0.75n}{16}", "Multiply by 16 to convert cups to tablespoons.")]),
                     ("A car uses {M('g(m) = \\frac{m}{30}')} gallons of gas to drive {M('m')} miles. Gas costs \\$3.50 per gallon: {M('C(g) = 3.5g')}.",
                      "C(g(m)) = \\frac{3.5m}{30}", "cost to drive m miles",
                      [("g(C(m)) = \\frac{3.5m}{30}", "Find gallons first, then cost: C(g(m))."), ("C(g(m)) = \\frac{30m}{3.5}", "Gallons are m/30; multiply by 3.5."),
                       ("C(g(m)) = 3.5m + \\frac{m}{30}", "Composition substitutes; it does not add.")])]
        text, ansx, what, ds = rng.choice(stem_opts)
        text = text.replace("{M('c(n) = 0.75n')}", M("c(n) = 0.75n")).replace("{M('n')}", M("n")).replace("{M('t(c) = 16c')}", M("t(c) = 16c"))
        text = text.replace("{M('g(m) = \\frac{m}{30}')}", M("g(m) = \\frac{m}{30}")).replace("{M('m')}", M("m")).replace("{M('C(g) = 3.5g')}", M("C(g) = 3.5g"))
        stem = f"{text} Which function gives the {what}?"
        ans = M(ansx)
        ds = [(M(t), w) for t, w in ds]
        expl = f"Substitute the first function into the second: {M(ansx)}."
    else:
        a, b = rng.choice([1, 2, 3, -1, -2]), rng.randint(-5, 5)
        c = rng.randint(-4, 4)
        x0 = rng.randint(-3, 3)
        fS = f"f(x) = {poly([1, 0, c])}"
        gS = f"g(x) = {lin(a, b)}"
        fg = (a * x0 + b) ** 2 + c
        gf = a * (x0 * x0 + c) + b
        if fg == gf:
            raise Skip
        stem = f"Given {M(fS)} and {M(gS)}, what is {M(f'f(g({x0}))')}?"
        ans = M(str(fg))
        ds = [(M(str(gf)), "That is g(f(" + str(x0) + ")); evaluate g first."),
              (M(str((x0 * x0 + c) * (a * x0 + b))), "Multiplied f and g instead of composing."),
              (M(str(a * x0 + b)), f"Stopped after finding g({x0})."),
              (M(str((a * x0 + b) * 2 + c)), "Doubled instead of squaring.")]
        expl = f"{M(f'g({x0}) = {a * x0 + b}')}, then {M(f'f({a * x0 + b}) = {fg}')}."
    return mc("A2.F.BF.A.1.b", 2, "Y", stem, ans, ds, expl, rng)


# ===================================================== A2.F.BF.A.2
@gen("A2.F.BF.A.2", 10)
def bfa2_arith(rng):
    a1 = rng.randint(-20, 30)
    d = rng.choice([k for k in range(-9, 13) if k not in (0, 1)])
    terms = [a1 + d * i for i in range(4)]
    ask = rng.choice(["explicit", "recursive", "term"])
    seq = ", ".join(str(t) for t in terms) + ", ..."
    if ask == "explicit":
        stem = f"Which formula gives the {M('n')}th term of the arithmetic sequence {seq}?"
        ans = M(f"a_n = {a1} {signed(d)}(n - 1)")
        ds = [(M(f"a_n = {a1} {signed(d)}n"), "With n = 1 this gives the second term; use (n − 1)."),
              (M(f"a_n = {d} {signed(a1)}(n - 1)"), "The first term and the common difference are switched."),
              (M(f"a_n = {a1}({d})^{{n - 1}}"), "That is a geometric formula; this sequence adds a constant.")]
        expl = f"The first term is {a1} and the common difference is {d}, so {M(f'a_n = {a1} {signed(d)}(n - 1)')}."
    elif ask == "recursive":
        stem = f"Which recursive formula defines the arithmetic sequence {seq}?"
        ans = M(f"a_1 = {a1};\\ a_n = a_{{n-1}} {signed(d)}")
        ds = [(M(f"a_1 = {d};\\ a_n = a_{{n-1}} {signed(a1)}"), "The first term and the difference are switched."),
              (M(f"a_1 = {a1};\\ a_n = {d}a_{{n-1}}"), "Arithmetic sequences add the difference; they do not multiply."),
              (M(f"a_1 = {a1};\\ a_n = a_{{n-1}} {signed(-d)}"), "Sign error on the common difference.")]
        expl = f"Start at {a1} and add {d} each time."
    else:
        n = rng.randint(15, 60)
        val = a1 + d * (n - 1)
        stem = f"What is the {n}th term of the arithmetic sequence {seq}?"
        ans = M(str(val))
        ds = [(M(str(a1 + d * n)), "Used n instead of n − 1."), (M(str(a1 * d * (n - 1))), "Multiplied the first term by the change."),
              (M(str(d * (n - 1))), "Forgot to add the first term.")]
        expl = f"{M(f'a_{{{n}}} = {a1} {signed(d)}({n} - 1) = {val}')}."
    return mc("A2.F.BF.A.2", 2, "Y", stem, ans, ds, expl, rng)


@gen("A2.F.BF.A.2", 10)
def bfa2_geom(rng):
    a1 = rng.choice([1, 2, 3, 4, 5, 6, 64, 81, 128, 243, -2, -3])
    r = rng.choice([2, 3, -2, F(1, 2), F(1, 3), 4])
    if (isinstance(r, F) and abs(a1) not in (64, 81, 128, 243)) or (not isinstance(r, F) and abs(a1) > 10):
        raise Skip
    if r == F(1, 3) and abs(a1) not in (81, 243):
        raise Skip
    if r == F(1, 2) and abs(a1) not in (64, 128):
        raise Skip
    terms = [F(a1) * F(r) ** i for i in range(4)]
    seq = ", ".join(num(t) for t in terms) + ", ..."
    ask = rng.choice(["explicit", "recursive", "term"])
    rs = f"\\left({num(r)}\\right)" if (isinstance(r, F) and r.denominator != 1) or r < 0 else num(r)
    if ask == "explicit":
        stem = f"Which formula gives the {M('n')}th term of the geometric sequence {seq}?"
        ans = M(f"a_n = {a1}{rs}^{{n - 1}}")
        ds = [(M(f"a_n = {a1}{rs}^{{n}}"), "With n = 1 this gives the second term."),
              (M(f"a_n = {num(r)}({a1})^{{n - 1}}"), "The first term and the ratio are switched."),
              (M(f"a_n = {a1} + {num(r)}(n - 1)" if r > 0 else f"a_n = {a1} - {num(-r)}(n - 1)"), "That is an arithmetic formula; this sequence multiplies.")]
        expl = f"The first term is {a1} and the common ratio is {num(r)}."
    elif ask == "recursive":
        stem = f"Which recursive formula defines the geometric sequence {seq}?"
        ans = M(f"a_1 = {a1};\\ a_n = {num(r)} \\cdot a_{{n-1}}")
        ds = [(M(f"a_1 = {a1};\\ a_n = a_{{n-1}} + {num(r)}"), "Geometric sequences multiply by the ratio."),
              (M(f"a_1 = {num(r)};\\ a_n = {a1} \\cdot a_{{n-1}}"), "The first term and the ratio are switched."),
              (M(f"a_1 = {a1};\\ a_n = {num(1 / F(r))} \\cdot a_{{n-1}}"), "Used the reciprocal of the ratio.")]
        expl = f"Start at {a1} and multiply by {num(r)} each time."
    else:
        n = rng.randint(6, 9)
        val = F(a1) * F(r) ** (n - 1)
        if abs(val) > 10 ** 6 or (val.denominator > 1000):
            raise Skip
        stem = f"What is the {n}th term of the geometric sequence {seq}?"
        ans = M(num(val))
        ds = [(M(num(F(a1) * F(r) ** n)), "Used n instead of n − 1."), (M(num(F(a1) * F(r) ** (n - 2))), "That is the term before."),
              (M(num(F(a1) * F(r) * (n - 1))), "Multiplied by the ratio times (n − 1) instead of raising it to that power.")]
        expl = f"{M(f'a_{{{n}}} = {a1}{rs}^{{{n - 1}}} = {num(val)}')}."
    return mc("A2.F.BF.A.2", 2, "Y", stem, ans, ds, expl, rng)


@gen("A2.F.BF.A.2", 10)
def bfa2_context(rng):
    kind = rng.choice(["seats", "savings", "bounce", "pushups", "tree"])
    if kind == "seats":
        a1, d = rng.randint(12, 30), rng.randint(2, 5)
        n = rng.randint(10, 30)
        stem = f"The first row of a theater has {a1} seats, and each row after that has {d} more seats than the row in front of it. How many seats are in row {n}?"
        val = a1 + d * (n - 1)
        ds = [(str(a1 + d * n), "Used n instead of n − 1."), (str(a1 * n), "Each row adds seats; it does not multiply."), (str(d * n), "Forgot the first row's seats.")]
        expl = f"{M(f'a_n = {a1} + {d}(n - 1)')}, so row {n} has {M(f'{a1} + {d}({n - 1}) = {val}')} seats."
    elif kind == "savings":
        a1, d = rng.choice([20, 25, 40, 50]), rng.choice([5, 10, 15])
        n = rng.randint(8, 30)
        stem = f"In week 1 a student saves {money(a1)}. Each week the student saves {money(d)} more than the week before. How much does the student save in week {n}?"
        val = a1 + d * (n - 1)
        ds = [(money(a1 + d * n), "Used n instead of n − 1."), (money(a1 * n), "That multiplies the first week's savings."), (money(d * (n - 1)), "Forgot the first week's amount.")]
        expl = f"{money(a1)} + {money(d)}({n - 1}) = {money(val)}."
        return mc("A2.F.BF.A.2", 2, "Y", stem, money(val), ds, expl, rng)
    elif kind == "bounce":
        h = rng.choice([8, 10, 12, 16, 20, 25])
        r = rng.choice([0.5, 0.6, 0.75, 0.8])
        n = rng.randint(3, 6)
        stem = (f"A ball is dropped and its first bounce reaches {h} feet. Each bounce reaches {pct(r, 0)} of the height of the previous bounce. "
                f"About how high does bounce {n} reach? Round to the nearest tenth of a foot.")
        val = round(h * r ** (n - 1), 1)
        ds = [(dec(round(h * r ** n, 1)), "Used n instead of n − 1."), (dec(round(h - h * (1 - r) * (n - 1), 1)), "Subtracted a constant amount; each bounce is a percent of the last."),
              (dec(round(h * r * (n - 1), 1)), "Multiplied by the rate times (n − 1).")]
        ans = dec(val)
        return mc("A2.F.BF.A.2", 2, "Y", stem, f"{ans} feet", [(f"{t} feet", w) for t, w in ds],
                  f"{M(f'a_n = {h}({r})^{{n - 1}}')}, so {M(f'a_{{{n}}} = {h}({r})^{{{n - 1}}} \\approx {ans}')} feet.", rng)
    elif kind == "pushups":
        a1, d = rng.randint(5, 15), rng.randint(2, 4)
        target = a1 + d * rng.randint(8, 20)
        n = (target - a1) // d + 1
        stem = f"A student does {a1} push-ups on day 1 and adds {d} push-ups each day. On which day will the student do {target} push-ups?"
        val = n
        ds = [(str(n - 1), "Forgot that day 1 already has the first term."), (str((target) // d), "Divided the target by the increase without accounting for day 1."),
              (str(n + 1), "Off by one.")]
        expl = f"Solve {M(f'{a1} + {d}(n - 1) = {target}')}: {M(f'n - 1 = {(target - a1) // d}')}, so {M(f'n = {n}')}."
    else:
        h0 = rng.choice([2, 3, 4, 5])
        g_ = rng.choice([1.5, 2, 2.5])
        n = rng.randint(5, 12)
        stem = f"A tree is {h0} feet tall when planted (year 1) and grows {dec(g_)} feet each year. Which recursive formula gives its height {M('h_n')} in year {M('n')}?"
        ans_ = M(f"h_1 = {h0};\\ h_n = h_{{n-1}} + {dec(g_)}")
        ds = [(M(f"h_1 = {dec(g_)};\\ h_n = h_{{n-1}} + {h0}"), "The starting height and the growth are switched."),
              (M(f"h_1 = {h0};\\ h_n = {dec(g_)}h_{{n-1}}"), "Constant growth is added, not multiplied."),
              (M(f"h_1 = {h0};\\ h_n = h_{{n-1}} + {dec(g_)}n"), "The same amount is added every year.")]
        return mc("A2.F.BF.A.2", 2, "Y", stem, ans_, ds, f"Start at {h0} and add {dec(g_)} each year.", rng)
    return mc("A2.F.BF.A.2", 2, "Y", stem, str(val), ds, expl, rng)


# ===================================================== A2.F.BF.B.3
PARENTS = [
    ("x^{2}", lambda x: x * x, "{a}(x {h})^{{2}} {k}"),
    ("|x|", abs, "{a}|x {h}| {k}"),
    ("\\sqrt{x}", lambda x: math.sqrt(x) if x >= 0 else None, "{a}\\sqrt{{x {h}}} {k}"),
    ("\\sqrt[3]{x}", lambda x: math.copysign(abs(x) ** (1 / 3), x), "{a}\\sqrt[3]{{x {h}}} {k}"),
    ("x^{3}", lambda x: x ** 3, "{a}(x {h})^{{3}} {k}"),
    ("2^{x}", lambda x: 2 ** x, "{a}2^{{x {h}}} {k}"),
]


def tform(tpl, a, h, k):
    A = "" if a == 1 else ("-" if a == -1 else num(a))
    H = signed(h) if h else ""
    K = signed(k) if k else ""
    s = tpl.format(a=A, h=H, k=K)
    return s.replace("(x )", "x").replace("{x }", "{x}").replace("|x |", "|x|").replace("^{x }", "^{x}").strip()


@gen("A2.F.BF.B.3", 12)
def bfb3_describe(rng):
    name, fn, tpl = rng.choice(PARENTS)
    refl = rng.random() < 0.4
    h = rng.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
    k = rng.choice([-6, -4, -3, -2, 2, 3, 5, 7])
    a = -1 if refl else 1
    lines = []
    if refl:
        lines.append("a reflection over the x-axis")
    lines.append(f"a horizontal translation {abs(h)} unit{'s' if abs(h) != 1 else ''} to the {'left' if h > 0 else 'right'}")
    lines.append(f"a vertical translation {abs(k)} units {'up' if k > 0 else 'down'}")
    stem = (f"The graph of {M('g(x)')} is the graph of {M(f'f(x) = {name}')} after these transformations:<ul>"
            + "".join(f"<li>{l}</li>" for l in lines) + f"</ul>Which equation represents {M('g(x)')}?")
    ans = M("g(x) = " + tform(tpl, a, h, k))
    ds = [(M("g(x) = " + tform(tpl, a, -h, k)), "Sign error: shifting left replaces x with x + h."),
          (M("g(x) = " + tform(tpl, a, k, h)), "Horizontal and vertical shifts are swapped."),
          (M("g(x) = " + tform(tpl, -a, h, k)), "Check the reflection." if refl else "There is no reflection."),
          (M("g(x) = " + tform(tpl, a, h, -k)), "Sign error on the vertical shift.")]
    return mc("A2.F.BF.B.3", 2, "N", stem, ans, ds,
              f"{'Reflect: multiply by −1. ' if refl else ''}Left/right shifts change the input ({M(f'x {signed(h)}')}); up/down shifts add to the output ({M(signed(k))}).", rng)


@gen("A2.F.BF.B.3", 10)
def bfb3_find_k(rng):
    name, fn, tpl = rng.choice(PARENTS[:2] + PARENTS[4:5])
    kind = rng.choice(["vert", "horiz", "vert", "stretch"])
    k = rng.choice([-4, -3, -2, 2, 3, 4])
    if kind == "vert":
        g = lambda x: fn(x) + k
        expr, ans = "f(x) + k", k
    elif kind == "horiz":
        g = lambda x: fn(x + k)
        expr, ans = "f(x + k)", k
    else:
        k = rng.choice([2, 3, -1, -2])
        g = lambda x: k * fn(x)
        expr, ans = "k \\cdot f(x)", k
    graph = svg_plot([fn, g], xr=(-7, 7), yr=(-8, 8), label_every=2, styles=[("#245b47", None), ("#a8442f", "7 5")])
    stem = (f"The graphs of {M(f'f(x) = {name}')} (solid green) and {M(f'g(x) = {expr}')} (dashed red) are shown."
            f"{graph}What is the value of {M('k')}?")
    ds = [(M(str(-ans)), "Sign error: f(x + k) with k > 0 shifts left." if kind == "horiz" else "Check the direction of the change."),
          (M(str(ans + 1)), "Read the graph carefully."), (M(str(ans - 1 if ans - 1 != 0 else ans + 2)), "Read the graph carefully.")]
    if kind == "stretch":
        ds.append((M(num(F(1, ans))), "A factor greater than 1 makes the graph steeper."))
    expl = {"vert": f"The graph of g is {abs(k)} units {'above' if k > 0 else 'below'} f, so {M(f'k = {k}')}.",
            "horiz": f"The graph of g is {abs(k)} units to the {'left' if k > 0 else 'right'} of f. {M('f(x + k)')} moves left when k > 0, so {M(f'k = {k}')}.",
            "stretch": f"Each y-value of g is {k} times the y-value of f, so {M(f'k = {k}')}."}[kind]
    return mc("A2.F.BF.B.3", 2, "Y", stem, M(str(ans)), ds, expl, rng)


@gen("A2.F.BF.B.3", 8)
def bfb3_effect(rng):
    k = rng.choice([2, 3, 4, 5, -2, -3])
    kind = rng.choice(["fx+k", "f(x+k)", "kf", "fkx"])
    expr = {"fx+k": f"f(x) {signed(k)}", "f(x+k)": f"f(x {signed(k)})", "kf": f"{k}f(x)", "fkx": f"f({k}x)"}[kind]
    descs = {
        "fx+k": f"a vertical translation {abs(k)} units {'up' if k > 0 else 'down'}",
        "f(x+k)": f"a horizontal translation {abs(k)} units to the {'left' if k > 0 else 'right'}",
        "kf": f"a vertical stretch by a factor of {abs(k)}" + (" and a reflection over the x-axis" if k < 0 else ""),
        "fkx": f"a horizontal compression by a factor of {num(F(1, abs(k)))}" + (" and a reflection over the y-axis" if k < 0 else ""),
    }
    ans = descs[kind]
    alt = {
        "fx+k": [f"a horizontal translation {abs(k)} units to the {'right' if k > 0 else 'left'}", f"a vertical translation {abs(k)} units {'down' if k > 0 else 'up'}", f"a vertical stretch by a factor of {abs(k)}"],
        "f(x+k)": [f"a horizontal translation {abs(k)} units to the {'right' if k > 0 else 'left'}", f"a vertical translation {abs(k)} units {'up' if k > 0 else 'down'}", f"a horizontal stretch by a factor of {abs(k)}"],
        "kf": [f"a horizontal stretch by a factor of {abs(k)}", f"a vertical translation {abs(k)} units up", f"a vertical compression by a factor of {num(F(1, abs(k)))}"],
        "fkx": [f"a horizontal stretch by a factor of {abs(k)}", f"a vertical stretch by a factor of {abs(k)}", f"a horizontal translation {abs(k)} units to the left"],
    }[kind]
    whys = ["Inside changes affect x in the opposite direction; outside changes affect y directly.",
            "Check whether the change is inside or outside the function.", "Adding shifts; multiplying stretches or compresses."]
    stem = f"How does the graph of {M(f'g(x) = {expr}')} compare with the graph of {M('f(x)')}?"
    return mc("A2.F.BF.B.3", 2, "N", stem, ans.capitalize() + ".", [(t.capitalize() + ".", w) for t, w in zip(alt, whys)],
              f"{M(f'g(x) = {expr}')} is {ans} of {M('f')}.", rng)


# ===================================================== A2.F.BF.B.4
@gen("A2.F.BF.B.4", 12)
def bfb4_inverse(rng):
    kind = rng.choice(["linear", "cubic", "exp", "log", "sqrt"])
    f = rng.choice(["f", "g", "h"])
    if kind == "linear":
        a, b = rng.choice([2, 3, 4, 5, -2, -3]), rng.randint(-9, 9)
        if b == 0:
            raise Skip
        expr = lin(a, b)
        ans = f"\\frac{{x {signed(-b)}}}{{{a}}}"
        ds = [f"\\frac{{x {signed(b)}}}{{{a}}}", f"\\frac{{x}}{{{a}}} {signed(-b)}", f"{lin(-a, b)}"]
        whys = ["Undo adding by subtracting.", "Subtract before dividing.", "The inverse is not the opposite function."]
    elif kind == "cubic":
        a, b = rng.choice([1, 2, 3]), rng.randint(-8, 8)
        if b == 0:
            raise Skip
        expr = poly([a, 0, 0, b])
        ans = f"\\sqrt[3]{{\\frac{{x {signed(-b)}}}{{{a}}}}}" if a != 1 else f"\\sqrt[3]{{x {signed(-b)}}}"
        ds = [f"\\sqrt[3]{{x}} {signed(-b)}" if a == 1 else f"\\frac{{\\sqrt[3]{{x}} {signed(-b)}}}{{{a}}}",
              (f"\\left(\\frac{{x {signed(-b)}}}{{{a}}}\\right)^{{3}}" if a != 1 else f"(x {signed(-b)})^{{3}}"),
              f"\\sqrt[3]{{\\frac{{x {signed(b)}}}{{{a}}}}}" if a != 1 else f"\\sqrt[3]{{x {signed(b)}}}"]
        whys = ["Undo the steps in reverse order: subtract, then divide, then take the cube root.", "Undo cubing with a cube root.", "Sign error."]
    elif kind == "exp":
        b = rng.choice([2, 3, 5, 10])
        k = rng.randint(-5, 5)
        if k == 0:
            raise Skip
        expr = f"{b}^{{x}} {signed(k)}"
        ans = f"\\log_{{{b}}}(x {signed(-k)})"
        ds = [f"\\log_{{{b}}}(x) {signed(-k)}", f"\\log_{{{b}}}(x {signed(k)})", f"(x {signed(-k)})^{{{b}}}"]
        whys = ["Subtract the shift before taking the log.", "Sign error.", "The inverse of an exponential is a logarithm."]
    elif kind == "log":
        b = rng.choice([2, 3, 10])
        k = rng.randint(-5, 5)
        if k == 0:
            raise Skip
        expr = f"\\log_{{{b}}}(x) {signed(k)}"
        ans = f"{b}^{{x {signed(-k)}}}"
        ds = [f"{b}^{{x}} {signed(-k)}", f"{b}^{{x {signed(k)}}}", f"(x {signed(-k)})^{{{b}}}"]
        whys = ["Subtract the shift before rewriting in exponential form.", "Sign error.", "The base of the log becomes the base of the power."]
    else:
        h = rng.randint(1, 6)
        expr = f"\\sqrt{{x - {h}}}"
        ans = f"x^{{2}} + {h},\\ x \\ge 0"
        ds = [f"x^{{2}} - {h},\\ x \\ge 0", f"\\sqrt{{x + {h}}}", f"x^{{2}} + {h},\\ x \\ge {h}"]
        whys = ["Sign error: add h back.", "The inverse of a square root is a square.", f"The domain of the inverse is the range of {M(f)}, which is y ≥ 0."]
    stem = f"What is the inverse of {M(f'{f}(x) = {expr}')}?"
    return mc("A2.F.BF.B.4.b", 2, "N", stem, M(f"{f}^{{-1}}(x) = {ans}"), [(M(f"{f}^{{-1}}(x) = {t}"), w) for t, w in zip(ds, whys)],
              f"Swap x and y in {M(f'y = {expr}')} and solve for y: {M(f'{f}^{{-1}}(x) = {ans}')}.", rng)


@gen("A2.F.BF.B.4", 6, by_choices=True)
def bfb4_one_to_one(rng):
    pool_yes = [("f(x) = x^{3} + 2", "Each output comes from exactly one input."), ("f(x) = 2^{x}", "An exponential function always increases or always decreases."),
                ("f(x) = \\sqrt{x - 1}", "A square root function always increases."), ("f(x) = 4x - 7", "A nonhorizontal line passes the horizontal line test."),
                ("f(x) = \\log_{3} x", "A log function always increases."), ("f(x) = \\sqrt[3]{x} + 5", "A cube root function always increases."),
                ("f(x) = -\\frac{1}{2}x + 3", "A nonhorizontal line passes the horizontal line test."), ("f(x) = (0.5)^{x}", "An exponential function always decreases here.")]
    pool_no = [("f(x) = x^{2} - 4", "f(2) = f(−2), so it fails the horizontal line test."), ("f(x) = |x| + 1", "f(3) = f(−3)."),
               ("f(x) = (x - 3)^{2}", "f(2) = f(4)."), ("f(x) = x^{3} - 9x", "f(0) = f(3) = 0."), ("f(x) = 5", "Every input gives the same output.")]
    ask_yes = rng.random() < 0.5
    if ask_yes:
        cor = rng.sample(pool_yes, 2)
        wr = rng.sample(pool_no, 3)
        stem = "Which functions are one-to-one?"
    else:
        cor = rng.sample(pool_no, 2)
        wr = rng.sample(pool_yes, 3)
        stem = "Which functions are <b>not</b> one-to-one?"
    return ms("A2.F.BF.B.4.a", 2, "Y", stem, [(M(t), "Correct: " + w) for t, w in cor], [(M(t), w) for t, w in wr],
              "A function is one-to-one when no horizontal line meets its graph more than once.", rng)


@gen("A2.F.BF.B.4", 7)
def bfb4_inverse_domain(rng):
    kind = rng.choice(["sqrt", "exp", "log", "quad"])
    h = rng.randint(-5, 5)
    k = rng.randint(-5, 5)
    if kind == "sqrt":
        expr = f"\\sqrt{{{lin(1, -h)}}} {signed(k) if k else ''}"
        ans = M(f"x \\ge {k}")
        ds = [(M(f"x \\ge {h}"), "That is the domain of f; the inverse's domain is f's range."), (M("\\text{all real numbers}"), "The range of f is limited."),
              (M(f"x \\ge {-k}"), "Sign error on the vertical shift.")]
    elif kind == "exp":
        b = rng.choice([2, 3, 10])
        expr = f"{b}^{{x}} {signed(k) if k else ''}"
        ans = M(f"x > {k}")
        ds = [(M("\\text{all real numbers}"), "That is the domain of f."), (M(f"x \\ge {k}"), f"f never equals {k}."), (M("x > 0"), "The graph is shifted vertically.") if k else (M("x \\ge 1"), "Use the range of f.")]
    elif kind == "log":
        b = rng.choice([2, 3, 10])
        expr = f"\\log_{{{b}}}({lin(1, -h)})"
        ans = M("\\text{all real numbers}")
        ds = [(M(f"x > {h}"), "That is the domain of f, not of its inverse."), (M("x > 0"), "The range of a log function is all real numbers."),
              (M(f"x \\ge {h}"), "The domain of the inverse is the range of f.")]
    else:
        expr = f"{factor(h)}^{{2}} {signed(k) if k else ''},\\ x \\ge {h}"
        ans = M(f"x \\ge {k}")
        ds = [(M(f"x \\ge {h}"), "That is the restricted domain of f."), (M("\\text{all real numbers}"), "f has a minimum value."), (M(f"x \\le {k}"), "f opens up, so its outputs are at least k.")]
    stem = f"The function {M(f'f(x) = {expr}'.strip())} is invertible. What is the domain of {M('f^{-1}(x)')}?"
    return mc("A2.F.BF.B.4.c", 2, "N", stem, ans, ds, "The domain of the inverse is the range of the original function.", rng)


# ===================================================== A2.F.LE.A.1
@gen("A2.F.LE.A.1", 10)
def lea1_solve_log(rng):
    a = rng.choice([2, 3, 4, 5, 10])
    b = rng.choice([2, 10, "e"])
    c = rng.choice([1, 2, 3, 4])
    d_mult = rng.choice([3, 5, 6, 7, 8, 12, 20, 50])
    d = a * d_mult
    base = "e" if b == "e" else str(b)
    log = "\\ln" if b == "e" else ("\\log" if b == 10 else f"\\log_{{{b}}}")
    expr = f"{a} \\cdot {base}^{{{'' if c == 1 else c}t}} = {d}"
    ans = M(f"t = \\frac{{{log} {d_mult}}}{{{c}}}" if c != 1 else f"t = {log} {d_mult}")
    ds = [(M(f"t = \\frac{{{log} {d}}}{{{c}}}" if c != 1 else f"t = {log} {d}"), f"Divide both sides by {a} before taking the log."),
          (M(f"t = \\frac{{{log} {d - a}}}{{{c}}}" if c != 1 else f"t = {log} {d - a}"), f"{a} multiplies the power; divide by it instead of subtracting."),
          (M(f"t = {c}{log} {d_mult}" if c != 1 else f"t = \\frac{{{log} {d_mult}}}{{2}}"), "Divide by the coefficient of t; do not multiply.") if c != 1 else (M(f"t = {log} {d_mult * a}"), "Divide by " + str(a) + "."),
          (M(f"t = \\frac{{{log} {d_mult}}}{{{a * c}}}"), f"Divided by {a} twice.")]
    val = math.log(d_mult) / (1 if b == "e" else math.log(b)) / c
    return mc("A2.F.LE.A.1.b", 2, "Y", f"Which expression gives the solution to {M(expr)}?", ans, ds,
              f"Divide by {a}: {M(f'{base}^{{{'' if c == 1 else c}t}} = {d_mult}')}. Take {'the natural log' if b == 'e' else f'the base-{b} log'}: "
              f"{M(f'{'' if c == 1 else c}t = {log} {d_mult}')}, so {ans} ≈ {dec(val, 3)}.", rng)


@gen("A2.F.LE.A.1", 6)
def lea1_forms(rng):
    b = rng.choice([2, 3, 4, 5, 10])
    e = rng.randint(2, 4)
    v = b ** e
    to_log = rng.random() < 0.5
    if to_log:
        stem = f"Which equation is equivalent to {M(f'{b}^{{{e}}} = {v}')}?"
        ans = M(f"\\log_{{{b}}} {v} = {e}")
        ds = [(M(f"\\log_{{{e}}} {v} = {b}"), "The base of the power becomes the base of the log."), (M(f"\\log_{{{b}}} {e} = {v}"), "The log equals the exponent."),
              (M(f"\\log_{{{v}}} {b} = {e}"), "The log's argument is the result of the power.")]
    else:
        stem = f"Which equation is equivalent to {M(f'\\log_{{{b}}} {v} = {e}')}?"
        ans = M(f"{b}^{{{e}}} = {v}")
        ds = [(M(f"{e}^{{{b}}} = {v}"), "The base of the log is the base of the power."), (M(f"{b}^{{{v}}} = {e}"), "The log is the exponent."),
              (M(f"{v}^{{{e}}} = {b}"), "The argument of the log is the result of the power.")]
    return mc("A2.F.LE.A.1", 1, "N", stem, ans, ds, f"{M(f'\\log_{{{b}}} {v} = {e}')} means {M(f'{b}^{{{e}}} = {v}')}.", rng)


@gen("A2.F.LE.A.1", 6)
def lea1_context(rng):
    P = rng.choice([1500, 2000, 2500, 4000, 5000])
    r = rng.choice([0.03, 0.04, 0.05, 0.06, 0.07])
    mult = rng.choice([1.5, 2, 3])
    T = P * mult
    t = math.log(mult) / math.log(1 + r)
    stem = (f"An investment of {money(P)} grows according to {M(f'A(t) = {comma(P).replace(',', '{,}')}({dec(1 + r)})^{{t}}')}, where {M('t')} is in years. "
            f"About how many years will it take to reach {money(T)}? Round to the nearest tenth.")
    ans = dec(round(t, 1), 1)
    ds = [(dec(round(math.log(T) / math.log(1 + r), 1), 1), f"Divide by {comma(P)} before taking the log."),
          (dec(round((mult - 1) / r, 1), 1), "Used simple (linear) growth instead of exponential growth."),
          (dec(round(math.log(mult) / r, 1), 1), f"Divided by the rate {num(r)} instead of by {M(f'\\log {dec(1 + r)}')}.")]
    return mc("A2.F.LE.A.1.c", 2, "Y", stem, f"{ans} years", [(f"{d_} years", w) for d_, w in ds],
              f"{M(f'({dec(1 + r)})^t = {dec(mult)}')}, so {M(f't = \\frac{{\\log {dec(mult)}}}{{\\log {dec(1 + r)}}} \\approx {ans}')}.", rng)


# ===================================================== A2.F.LE.A.2
@gen("A2.F.LE.A.2", 10)
def lea2_exceeds(rng):
    b = rng.choice([1.5, 2, 3, 1.2, 1.1])
    kind = rng.choice(["linear", "quad", "cubic"])
    if kind == "linear":
        m = rng.choice([50, 100, 200, 500])
        g = lambda x: m * x
        gexpr = f"{m}x"
    elif kind == "quad":
        c = rng.choice([10, 20, 50])
        g = lambda x: c * x * x
        gexpr = f"{c}x^{{2}}"
    else:
        c = rng.choice([2, 4, 5])
        g = lambda x: c * x ** 3
        gexpr = f"{c}x^{{3}}"
    f = lambda x: b ** x
    x = 1
    while not (f(x) > g(x) and all(f(y) > g(y) for y in range(x, x + 30))):
        x += 1
        if x > 400:
            raise Skip
    stem = f"Compare {M(f'f(x) = ({dec(b)})^{{x}}')} and {M(f'g(x) = {gexpr}')} for {M('x > 0')}. Which statement is true?"
    ans = f"{M('f(x)')} eventually exceeds {M('g(x)')} and stays greater."
    ds = [(f"{M('g(x)')} is always greater than {M('f(x)')}.", f"An increasing exponential eventually exceeds any polynomial. Here f is greater for x ≥ {x}."),
          (f"{M('f(x)')} is always greater than {M('g(x)')}.", f"At small x, such as x = {max(1, x // 2)}, g is greater."),
          (f"The two functions never intersect.", "Their graphs cross, because f starts below g and ends above it.")]
    return mc("A2.F.LE.A.2", 2, "Y", stem, ans, ds,
              f"A quantity growing by a constant factor eventually passes any linear, quadratic, or cubic quantity. Here {M('f(x) > g(x)')} for every whole number {M(f'x \\ge {x}')}.", rng)
