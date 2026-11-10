"""Statistics and Probability generators (blueprint category SP)."""
import math
from math import comb, perm

from common import (F, M, Skip, comma, gen, mc, ms, num, pct, svg_curve_shape,
                    svg_plot, table)


def dec(x, d=2):
    s = f"{x:.{d}f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s


# ===================================================== A2.S.ID.A.1
SHAPE_CTX = {
    "right": ["household incomes in a city", "prices of homes in a county", "number of texts students send per day",
              "wait times at a clinic", "ages of people at a children's museum"],
    "left": ["scores on an easy quiz", "ages of people at a retirement celebration", "life spans of a well-made light bulb",
             "percent of homework completed by students in a class"],
    "symmetric": ["heights of adult women", "weights of apples from one orchard", "SAT-style test scores", "lengths of a species of fish"],
}


@gen("A2.S.ID.A.1", 10)
def id1_shape_center(rng):
    shape = rng.choice(["right", "left", "symmetric"])
    ctx = rng.choice(SHAPE_CTX[shape])
    curve = svg_curve_shape(shape)
    ask = rng.choice(["center", "compare"])
    words = {"right": "skewed right", "left": "skewed left", "symmetric": "symmetric"}
    if ask == "center":
        stem = f"The density curve shows the distribution of the {ctx}.{curve}Which measure of center best describes a typical value?"
        if shape == "symmetric":
            ans = "the mean, because the distribution is symmetric"
            ds = [("the median, because the distribution is skewed", "This distribution is symmetric, so the mean works well."),
                  ("the range, because it uses every value", "The range measures spread, not center."),
                  ("the mode, because it is always the most accurate", "The mode is not always the best summary.")]
        else:
            ans = f"the median, because the distribution is {words[shape]}"
            ds = [("the mean, because it uses every value", f"In a {words[shape]} distribution, extreme values pull the mean toward the tail."),
                  ("the standard deviation, because the data vary", "Standard deviation measures spread, not center."),
                  ("the mean, because the distribution is symmetric", f"The distribution is {words[shape]}, not symmetric.")]
        expl = ("For a symmetric distribution the mean and median are about equal and the mean is a good summary."
                if shape == "symmetric" else f"The tail pulls the mean, so the median better represents a typical value in a {words[shape]} distribution.")
    else:
        if shape == "symmetric":
            raise Skip
        stem = f"The density curve shows the distribution of the {ctx}.{curve}Which statement about the mean and median is most likely true?"
        ans = ("The mean is greater than the median." if shape == "right" else "The mean is less than the median.")
        ds = [("The mean is less than the median." if shape == "right" else "The mean is greater than the median.",
               "The mean is pulled toward the long tail."),
              ("The mean and the median are equal.", "That happens for symmetric distributions."),
              ("The median is always greater than the mean.", "Which is greater depends on the direction of the skew.")]
        expl = f"In a distribution {words[shape]}, the long tail is on the {'right' if shape == 'right' else 'left'}, pulling the mean that way."
    return mc("A2.S.ID.A.1", 2, "Y", stem, ans, ds, expl, rng)


@gen("A2.S.ID.A.1", 10)
def id1_compare_spread(rng):
    ctx, unit = rng.choice([("test scores in two classes", "points"), ("daily high temperatures in two cities", "°F"),
                            ("commute times for two bus routes", "minutes"), ("weights of bags from two machines", "grams"),
                            ("heights of two basketball teams", "inches")])
    m1 = rng.choice([45, 60, 72, 80, 85, 500])
    m2 = m1 + rng.choice([0, 0, 3, -3, 5])
    s1 = rng.choice([2, 3, 4, 5, 6])
    s2 = s1 + rng.choice([3, 4, 5, 6, 8])
    flip = rng.random() < 0.5
    A, B = ("A", "B")
    data = [(m1, s1), (m2, s2)]
    if flip:
        data.reverse()
    tbl = table(["Group", "Mean", "Standard deviation"], [["A", data[0][0], data[0][1]], ["B", data[1][0], data[1][1]]], row_head=True)
    more = "A" if data[0][1] > data[1][1] else "B"
    less = "B" if more == "A" else "A"
    stem = f"The table summarizes the {ctx}, in {unit}. Both distributions are roughly symmetric.{tbl}Which statement is best supported?"
    ans = f"The values in group {more} are more spread out than the values in group {less}."
    ds = [(f"The values in group {less} are more spread out than the values in group {more}.", "A larger standard deviation means more spread."),
          (f"Group {more} has a greater mean because its standard deviation is larger.", "Standard deviation measures spread, not center."),
          ("The two groups have the same spread because the means are close.", "Close means say nothing about spread.")]
    if data[0][0] != data[1][0]:
        hi = "A" if data[0][0] > data[1][0] else "B"
    return mc("A2.S.ID.A.1", 2, "Y", stem, ans, ds,
              f"Group {more} has the larger standard deviation ({max(s1, s2)} vs {min(s1, s2)}), so its values vary more from the mean.", rng)


# ===================================================== A2.S.ID.A.2
@gen("A2.S.ID.A.2", 20)
def id2_empirical(rng):
    ctx, unit = rng.choice([("heights of adult men", "inches"), ("weights of newborn babies", "pounds"), ("scores on a state test", "points"),
                            ("battery life of a phone model", "hours"), ("lengths of trout in a stream", "centimeters"),
                            ("times to run a mile", "minutes"), ("amounts of cereal in a box", "ounces")])
    mu = rng.choice([7, 9, 12, 30, 45, 50, 70, 72, 100, 250, 500])
    sd = rng.choice([s for s in [0.5, 1, 1.5, 2, 3, 4, 5, 8, 10, 25] if s * 3 < mu])
    lo, hi = rng.choice([(-1, 1), (-2, 2), (-3, 3), (-1, 2), (-2, 1), (0, 1), (0, 2), (-1, 0), (1, 2), (-2, -1), (2, 3), (1, 10), (-10, -1), (2, 10), (-10, 1)])
    band = {(-3, -2): 2.35, (-2, -1): 13.5, (-1, 0): 34, (0, 1): 34, (1, 2): 13.5, (2, 3): 2.35}
    def area(a, b):
        if a == -10:
            return 50 - area(b, 0) if b <= 0 else 50 + area(0, b)
        if b == 10:
            return 50 - area(0, a) if a >= 0 else 50 + area(a, 0)
        total = 0
        for k in range(a, b):
            total += band[(k, k + 1)]
        return total
    p = area(lo, hi)
    if p in (0, 50, 100):
        raise Skip
    v = lambda z: dec(mu + z * sd, 2)
    if lo == -10:
        q = f"less than {v(hi)} {unit}"
    elif hi == 10:
        q = f"greater than {v(lo)} {unit}"
    else:
        q = f"between {v(lo)} and {v(hi)} {unit}"
    stem = (f"The {ctx} are approximately normally distributed with a mean of {dec(mu)} {unit} and a standard deviation of {dec(sd)} {unit}. "
            f"About what percent are {q}?")
    cands = [68, 95, 99.7, 34, 47.5, 81.5, 13.5, 16, 84, 2.5, 97.5, 50, 49.85, 83.85, 15.85, 2.35]
    rng.shuffle(cands)
    ds = []
    for c in cands:
        if abs(c - p) < 0.01:
            continue
        ds.append((f"{dec(c)}%", "Count the standard deviations from the mean and add the Empirical Rule pieces: 34%, 13.5%, 2.35%, and 0.15% on each side."))
    ds.sort(key=lambda t: abs(float(t[0][:-1]) - p))
    ds = ds[:6]
    rng.shuffle(ds)
    zs = lambda z: f"{z:+d}".replace("+", "+") if abs(z) < 10 else ("−∞" if z < 0 else "+∞")
    expl = (f"Convert to standard deviations from the mean: "
            + (f"{v(lo)} is {lo} SD and " if lo != -10 else "")
            + (f"{v(hi)} is {hi} SD" if hi != 10 else "")
            + f". Using 34%, 13.5%, 2.35% (and 50% for each half), the percent is about {dec(p)}%.").replace(" and .", ".")
    return mc("A2.S.ID.A.2", 2, "Y", stem, f"{dec(p)}%", ds, expl, rng)


@gen("A2.S.ID.A.2", 10)
def id2_count(rng):
    N = rng.choice([200, 400, 500, 800, 1000, 1200, 2000, 5000])
    mu = rng.choice([50, 64, 70, 80, 100])
    sd = rng.choice([2, 4, 5, 8, 10])
    k = rng.choice([1, 2])
    above = rng.random() < 0.5
    p = (16 if k == 1 else 2.5) / 100
    count = N * p
    if count != int(count):
        raise Skip
    val = mu + k * sd if above else mu - k * sd
    ctx = rng.choice(["students took a test", "eggs were weighed", "plants were measured", "runners were timed"])
    stem = (f"{comma(N)} {ctx}. The results are approximately normal with a mean of {mu} and a standard deviation of {sd}. "
            f"About how many results are {'greater' if above else 'less'} than {val}?")
    p_other = (2.5 if k == 1 else 16) / 100
    ds = [(comma(round(N * 0.34 if k == 1 else N * 0.135)), "That is only the band next to the mean."),
          (comma(round(N * (0.68 if k == 1 else 0.95))), "That is the number within the interval, not beyond it."),
          (comma(round(N * p_other)), f"{val} is {k} standard deviation{'s' if k > 1 else ''} from the mean."),
          (comma(round(N * (0.32 if k == 1 else 0.05))), "That counts both tails; only one side is asked.")]
    return mc("A2.S.ID.A.2", 2, "Y", stem, comma(int(count)), ds,
              f"{val} is {k} standard deviation{'s' if k > 1 else ''} {'above' if above else 'below'} the mean. About {pct(p, 1)} of values are beyond it: "
              f"{pct(p, 1)} of {comma(N)} ≈ {comma(int(count))}.", rng)


# ===================================================== A2.S.ID.A.3
NAMES = ["Ava", "Malik", "Sofia", "Ethan", "Zara", "Diego", "Mei", "Andre", "Nia", "Omar", "Jada", "Liam"]


@gen("A2.S.ID.A.3", 10)
def id3_compute(rng):
    mu = rng.choice([50, 60, 65, 70, 72, 75, 80, 100, 500])
    sd = rng.choice([2, 4, 5, 6, 8, 10, 20, 50])
    z = rng.choice([-2.5, -2, -1.5, -1.25, -1, -0.5, 0.5, 0.75, 1, 1.25, 1.5, 2, 2.5])
    x = mu + z * sd
    if x != int(x) or x <= 0:
        raise Skip
    x = int(x)
    name = rng.choice(NAMES)
    ctx = rng.choice(["scored", "ran a time of", "measured", "earned"])
    stem = (f"Scores on a test have a mean of {mu} and a standard deviation of {sd}. {name} scored {x}. What is {name}'s z-score?")
    ds = [(dec(x - mu), "That is the difference from the mean; divide by the standard deviation."),
          (dec(-z), "Subtract the mean from the score, not the score from the mean."),
          (dec((x - mu) / sd * 2) if z * 2 != z else dec(z + 1), "Arithmetic error dividing by the standard deviation."),
          (dec(x / sd), "Subtract the mean before dividing.")]
    return mc("A2.S.ID.A.3", 1, "Y", stem, dec(z), ds,
              f"{M(f'z = \\frac{{{x} - {mu}}}{{{sd}}} = {dec(z)}')}.", rng)


@gen("A2.S.ID.A.3", 8)
def id3_compare(rng):
    n1, n2 = rng.sample(NAMES, 2)
    s1, s2 = rng.sample(["math test", "history test", "science test", "English test"], 2)
    mu1, sd1 = rng.choice([(70, 8), (75, 5), (80, 4), (65, 10), (72, 6)])
    mu2, sd2 = rng.choice([(68, 12), (82, 3), (60, 8), (78, 6), (85, 5)])
    z1 = rng.choice([0.5, 1, 1.25, 1.5, 2, -0.5, -1])
    z2 = rng.choice([0.5, 1, 1.5, 2, 2.5, -1, 0.75])
    if z1 == z2:
        raise Skip
    x1, x2 = mu1 + z1 * sd1, mu2 + z2 * sd2
    if x1 != int(x1) or x2 != int(x2):
        raise Skip
    x1, x2 = int(x1), int(x2)
    better = n1 if z1 > z2 else n2
    worse = n2 if better == n1 else n1
    bz, wz = max(z1, z2), min(z1, z2)
    stem = (f"{n1} scored {x1} on a {s1} with a mean of {mu1} and a standard deviation of {sd1}. {n2} scored {x2} on a {s2} with a mean of "
            f"{mu2} and a standard deviation of {sd2}. Who performed better relative to the others who took the same test?")
    ans = f"{better}, with a z-score of {dec(bz)} compared with {dec(wz)}"
    raw_better = n1 if x1 > x2 else n2
    ds = [(f"{worse}, with a z-score of {dec(bz)} compared with {dec(wz)}", "The z-scores are matched to the wrong students."),
          (f"{raw_better}, because the raw score is higher" if x1 != x2 else f"{n1}, because both scores are equal", "Raw scores on different tests cannot be compared directly."),
          ("They performed equally well relative to their classes.", f"The z-scores are {dec(z1)} and {dec(z2)}.")]
    if raw_better == better:
        ds[1] = (f"{worse}, because that test was harder", "Compare z-scores, not test difficulty.")
    return mc("A2.S.ID.A.3", 2, "Y", stem, ans, ds,
              f"{n1}: {M(f'z = \\frac{{{x1} - {mu1}}}{{{sd1}}} = {dec(z1)}')}. {n2}: {M(f'z = \\frac{{{x2} - {mu2}}}{{{sd2}}} = {dec(z2)}')}. "
              f"The higher z-score is farther above that test's mean.", rng)


@gen("A2.S.ID.A.3", 7)
def id3_find_value(rng):
    mu = rng.choice([20, 50, 64, 70, 100, 150])
    sd = rng.choice([2, 3, 4, 5, 10, 12])
    z = rng.choice([-2, -1.5, -1, 1, 1.5, 2, 2.5])
    x = mu + z * sd
    if x != int(x) or x <= 0:
        raise Skip
    ctx, unit = rng.choice([("the lengths of bolts", "millimeters"), ("customer wait times", "minutes"), ("the masses of packages", "kilograms"),
                            ("the speeds of cars on a highway", "miles per hour")])
    stem = (f"{ctx.capitalize()} are normally distributed with a mean of {mu} {unit} and a standard deviation of {sd} {unit}. "
            f"What value has a z-score of {dec(z)}?")
    ds = [(f"{dec(mu + z)} {unit}", "Multiply the z-score by the standard deviation before adding."),
          (f"{dec(mu - z * sd)} {unit}", "Sign error: a positive z-score is above the mean." if z > 0 else "Sign error: a negative z-score is below the mean."),
          (f"{dec(z * sd)} {unit}", "Add the mean to z times the standard deviation."),
          (f"{dec(mu * z)} {unit}", "Multiply the z-score by the standard deviation, not the mean.")]
    return mc("A2.S.ID.A.3", 2, "Y", stem, f"{dec(x)} {unit}", ds,
              f"{M(f'x = \\mu + z\\sigma = {mu} + ({dec(z)})({sd}) = {dec(x)}')}.", rng)


# ===================================================== A2.S.ID.B.4
@gen("A2.S.ID.B.4", 10)
def idb4_model_type(rng):
    kind = rng.choice(["linear", "quadratic", "exponential", "exp_decay"])
    pts = []
    for x in range(0, 11):
        noise = rng.uniform(-0.6, 0.6)
        if kind == "linear":
            y = 1 + 1.1 * x + noise
        elif kind == "quadratic":
            y = 14 - 0.5 * (x - 5) ** 2 + noise * 0.8
        elif kind == "exponential":
            y = 0.6 * 1.35 ** x + noise * 0.3
        else:
            y = 14 * 0.72 ** x + noise * 0.3
        pts.append((x, max(0.2, y)))
    ctx = rng.choice({"linear": [("Hours worked", "Earnings (tens of $)", "a student's earnings"), ("Gallons used", "Miles (tens)", "miles driven"),
                                 ("Minutes", "Water in tank (gal)", "water pumped into a tank")],
                      "quadratic": [("Time (s)", "Height (m)", "the height of a kicked ball"), ("Price ($)", "Profit (hundreds of $)", "profit at different prices"),
                                    ("Hour after 6 a.m.", "Temperature (°C)", "temperature during a day")],
                      "exponential": [("Week", "Followers (hundreds)", "followers of a new account"), ("Day", "Bacteria (thousands)", "bacteria in a culture"),
                                      ("Year", "Value (hundreds of $)", "the value of a collectible")],
                      "exp_decay": [("Hour", "Medicine (mg)", "medicine in a patient's blood"), ("Minute", "Temp. above room (°C)", "a cooling drink"),
                                    ("Year", "Value (thousands of $)", "the value of a car")]}[kind])
    g = svg_plot([], xr=(0, 10), yr=(0, 16), ystep=2, points=pts, xlabel=ctx[0], ylabel=ctx[1], label_every=1)
    stem = f"The scatter plot shows data about {ctx[2]}.{g}Which type of function best models the data?"
    names = {"linear": "linear", "quadratic": "quadratic", "exponential": "exponential growth", "exp_decay": "exponential decay"}
    whys = {"linear": "The points rise at a roughly constant rate.", "quadratic": "The points rise and then fall, with a maximum.",
            "exponential": "The points rise slowly, then faster and faster.", "exp_decay": "The points fall quickly, then level off."}
    ds = [(names[k].capitalize(), "The pattern does not match: " + whys[k].lower().replace("the points", "these points would")) for k in names if k != kind]
    return mc("A2.S.ID.B.4", 2, "Y", stem, names[kind].capitalize(), ds, whys[kind] + f" That matches {'an' if names[kind][0] in 'aeiou' else 'a'} {names[kind]} model.", rng)


@gen("A2.S.ID.B.4", 10)
def idb4_predict(rng):
    kind = rng.choice(["linear", "exp", "quad"])
    if kind == "linear":
        m = rng.choice([1.5, 2.4, 3.2, 4.5, 12.5])
        b = rng.choice([5, 8, 12, 20, 40])
        x0 = rng.randint(6, 20)
        val = m * x0 + b
        expr = f"y = {dec(m)}x + {b}"
        ctx = ("y is the cost in dollars and x is the number of hours", "dollars")
    elif kind == "exp":
        a = rng.choice([150, 200, 500, 1200])
        r = rng.choice([1.08, 1.12, 1.15, 1.2])
        x0 = rng.randint(3, 10)
        val = a * r ** x0
        expr = f"y = {comma(a).replace(',', '{,}')}({r})^{{x}}"
        ctx = ("y is the number of app downloads and x is the number of weeks since launch", "downloads")
    else:
        a = rng.choice([-4.9, -5])
        v = rng.choice([20, 24, 30])
        c = rng.choice([1.5, 2, 3])
        x0 = rng.choice([1, 2, 3])
        val = a * x0 * x0 + v * x0 + c
        expr = f"y = {dec(a)}x^{{2}} + {v}x + {dec(c)}"
        ctx = ("y is the height of a ball in meters and x is the time in seconds", "meters")
    stem = f"A function fitted to a set of data is {M(expr)}, where {ctx[0]}. Use the model to predict {M('y')} when {M(f'x = {x0}')}. Round to the nearest whole number."
    ans = comma(round(val))
    if kind == "linear":
        ds = [(comma(round(m * x0)), "Forgot to add the y-intercept."), (comma(round((x0 - b) / m)) if x0 > b else comma(round(m + b + x0)), "Solved for x instead of evaluating."),
              (comma(round(m * (x0 + b))), "Multiplied before adding incorrectly.")]
    elif kind == "exp":
        ds = [(comma(round(a * r * x0)), "Multiplied by the base times x instead of raising to the power."), (comma(round(a + r ** x0)), "Added instead of multiplying."),
              (comma(round(a * r ** (x0 - 1))), "Used one fewer week.")]
    else:
        ds = [(comma(round(a * x0 + v * x0 + c)), "Forgot to square x."), (comma(round(-a * x0 * x0 + v * x0 + c)), "Sign error on the squared term."),
              (comma(round(v * x0 + c)), "Left out the squared term.")]
    return mc("A2.S.ID.B.4.a" if False else "A2.S.ID.B.4", 2, "Y", stem, ans, ds,
              f"Substitute {M(f'x = {x0}')}: {M('y \\approx ' + comma(round(val)).replace(',', '{,}'))}.", rng)


@gen("A2.S.ID.B.4", 5)
def idb4_describe(rng):
    kind = rng.choice(["pos", "neg", "none", "pos_nonlin", "neg_nonlin"])
    pts = []
    for x in range(1, 13):
        e = rng.uniform(-1.2, 1.2)
        y = {"pos": 2 + 0.9 * x + e, "neg": 13 - 0.9 * x + e, "none": 7 + rng.uniform(-5, 5),
             "pos_nonlin": 1 + 0.08 * x * x + e * 0.5, "neg_nonlin": 14 * 0.8 ** x + e * 0.4}[kind]
        pts.append((x, max(0.3, min(15.5, y))))
    g = svg_plot([], xr=(0, 13), yr=(0, 16), ystep=2, points=pts, label_every=2)
    words = {"pos": "a positive linear association", "neg": "a negative linear association", "none": "no clear association",
             "pos_nonlin": "a positive nonlinear association", "neg_nonlin": "a negative nonlinear association"}
    ctx = rng.choice({"pos": ["hours studied and test score", "practice time and free throws made", "height and arm span"],
                      "neg": ["outdoor temperature and hot drinks sold", "weekly exercise time and resting heart rate", "price of a ticket and tickets sold"],
                      "none": ["shoe size and number of siblings", "birth month and test score", "phone number digits and height"],
                      "pos_nonlin": ["weeks since launch and app downloads", "years invested and account balance", "days and bacteria count"],
                      "neg_nonlin": ["age of a car and its value", "hours after a dose and medicine level", "minutes and temperature of cooling soup"]}[kind])
    stem = f"The scatter plot shows {ctx}.{g}Which statement best describes the relationship shown?"
    ds = [(f"The data show {w}.", "Look at whether y tends to rise or fall as x increases, and whether the pattern is straight or curved.")
          for k, w in words.items() if k != kind]
    return mc("A2.S.ID.B.4", 1, "Y", stem, f"The data show {words[kind]}.", ds,
              f"As x increases, the points show {words[kind]}.", rng)


# ===================================================== A2.S.IC.A.1
STUDY = [
    ("A researcher randomly assigns 80 volunteers to drink either green tea or water daily for a month and compares their blood pressure.", "experiment"),
    ("A school asks a random sample of 150 students which lunch option they prefer.", "survey"),
    ("A scientist records how many hours students sleep and their grades, without changing anything.", "observational"),
    ("A farmer plants a new fertilizer on 20 randomly chosen plots and the old fertilizer on 20 others, then compares yields.", "experiment"),
    ("A city mails a questionnaire to 500 randomly chosen households asking about a new park.", "survey"),
    ("A doctor reviews medical records to see whether people who exercise more have fewer colds.", "observational"),
    ("A teacher randomly assigns half of her classes to use flashcards and half to use a video, then compares test scores.", "experiment"),
    ("A news station asks a random sample of voters which candidate they support.", "survey"),
    ("A biologist counts how many birds visit feeders in different parks over a season.", "observational"),
    ("A company randomly gives half of its stores a new layout and compares sales with the other half.", "experiment"),
    ("A student asks 60 randomly chosen classmates how many hours of TV they watch per week.", "survey"),
    ("A researcher compares the test scores of students who chose to join a study group with those who did not.", "observational"),
    ("Plants are randomly assigned to grow under red, blue, or white light, and their heights are measured after 3 weeks.", "experiment"),
    ("An app developer asks a random sample of users to rate a new feature from 1 to 5.", "survey"),
    ("A traffic engineer records the speeds of cars passing a school zone at different times of day.", "observational"),
    ("Volunteers are randomly assigned to take a new allergy medicine or a placebo, and their symptoms are compared.", "experiment"),
    ("A library asks a random sample of visitors how often they borrow e-books.", "survey"),
    ("A researcher looks at existing data on whether teens who play sports have higher GPAs.", "observational"),
    ("A coach randomly assigns runners to two different warm-up routines and compares their race times.", "experiment"),
    ("A store gives a short questionnaire to every 10th customer about checkout wait times.", "survey"),
]


@gen("A2.S.IC.A.1", 14)
def ic1_type(rng):
    text, kind = rng.choice(STUDY)
    names = {"experiment": "an experiment", "survey": "a sample survey", "observational": "an observational study"}
    why = {"experiment": "a treatment is imposed on randomly assigned groups", "survey": "people are asked questions to estimate something about a population",
           "observational": "data are recorded without assigning any treatment"}
    ds = [(names[k].capitalize() + ", because " + why[k] + ".", f"In this study, {why[kind]}.") for k in names if k != kind]
    ds.append(("A census, because every member of the population is studied.", "Only a sample is studied, not every member."))
    return mc("A2.S.IC.A.1", 2, "Y", f"{text} Which type of study is this?", names[kind].capitalize() + ", because " + why[kind] + ".", ds,
              f"This is {names[kind]}: {why[kind]}.", rng)


@gen("A2.S.IC.A.1", 6)
def ic1_randomization(rng):
    q, ans, ds = rng.choice([
        ("In an experiment, why are subjects randomly assigned to treatment groups?",
         "to make the groups similar so differences in results can be attributed to the treatment",
         [("to make sure every subject gets the treatment", "Random assignment splits subjects; not everyone gets the treatment."),
          ("to make the sample larger", "Randomization does not change the sample size."), ("to guarantee the treatment works", "Randomization cannot guarantee a result.")]),
        ("Why does a sample survey use a random sample?",
         "so the sample is likely to represent the population",
         [("so the results are guaranteed to be exact", "Random samples still have sampling variability."), ("so fewer people need to be asked", "Randomness is about selection, not size."),
          ("so the researcher can choose the most helpful people", "That would introduce bias.")]),
        ("Why can an observational study not show that one variable causes another?",
         "because other variables that were not controlled might explain the relationship",
         [("because observational studies never use real data", "They use real data, just without assigning treatments."), ("because the sample is always too small", "Size is not the main issue."),
          ("because observational studies use random assignment", "They do not assign treatments at all.")]),
        ("A researcher wants to know whether a new study app causes higher test scores. Which design would best answer this question?",
         "randomly assign students to use the app or not, then compare scores",
         [("survey students about whether they like the app", "Opinions do not show cause and effect."), ("compare scores of students who chose to use the app with those who did not", "Students who choose the app may differ in other ways."),
          ("ask teachers to predict which students will improve", "Predictions are not measurements of the effect.")]),
        ("A company wants to estimate the percent of its customers who are satisfied. Which method is most appropriate?",
         "a sample survey of randomly selected customers",
         [("an experiment that assigns customers to two stores", "No treatment is needed to estimate a percent."), ("an observational study of how long customers stay", "Time in a store does not measure satisfaction."),
          ("asking the five most frequent customers", "That sample is not random and may be biased.")]),
        ("A scientist wants to know whether a fertilizer increases tomato yield. Which design would best answer this question?",
         "randomly assign plants to get the fertilizer or not, then compare yields",
         [("ask farmers whether they think the fertilizer works", "Opinions do not show cause and effect."), ("record yields of farms that already use it", "Those farms may differ in soil or weather."),
          ("measure one plant before and after using it", "One plant cannot separate the effect from other changes.")]),
    ])
    return mc("A2.S.IC.A.1", 2, "Y", q, ans[0].upper() + ans[1:] + ".", [(t[0].upper() + t[1:] + ".", w) for t, w in ds],
              ans[0].upper() + ans[1:] + ".", rng)


# ===================================================== A2.S.IC.A.2
BIAS = [
    ("A survey asks, “Don't you agree that the school day is too long?”", "leading question", "The wording pushes respondents toward agreeing."),
    ("To learn how residents feel about a new gym, a researcher surveys people leaving a fitness center.", "sampling bias", "People at a fitness center are more likely to support a gym."),
    ("A website posts a poll and anyone who visits can vote as many times as they want.", "voluntary response", "People with strong opinions choose to respond, and some respond more than once."),
    ("A survey about internet use is done only by phone calls to landlines.", "undercoverage", "People without landlines are left out."),
    ("Surveys are mailed to 1,000 homes, but only 90 are returned.", "nonresponse", "The people who did not respond may differ from those who did."),
    ("A study concludes a new diet works after testing it on 4 people.", "small sample size", "Four people are too few to support a general conclusion."),
    ("A survey asks, “Should the city waste money on a new stadium?”", "leading question", "The word “waste” pushes respondents toward saying no."),
    ("To estimate the average height of students, a researcher measures only the basketball team.", "sampling bias", "Basketball players tend to be taller than other students."),
    ("A TV show asks viewers to text in their opinion on a new law.", "voluntary response", "Only viewers who care strongly tend to respond."),
    ("A school surveys students about after-school programs by asking only students in the library after school.", "sampling bias", "Students in the library after school may use programs differently from others."),
    ("A survey about a later school start time is given only to seniors.", "undercoverage", "Students in other grades are left out of the sample."),
    ("A researcher calls homes between 10 a.m. and 2 p.m. on weekdays to ask about job satisfaction.", "undercoverage", "People who work during those hours are unlikely to be reached."),
    ("An online review site shows that 95% of reviewers loved a restaurant.", "voluntary response", "Only customers who choose to write reviews are counted."),
    ("A survey asks, “Do you support the reckless plan to cut library hours?”", "leading question", "The word “reckless” influences the response."),
    ("A company emails a survey to all customers, and 6% reply.", "nonresponse", "With so few replies, the respondents may not represent all customers."),
    ("A teacher concludes that a study method works because 3 students' grades went up.", "small sample size", "Three students are too few, and there is no comparison group."),
    ("A mall surveys shoppers on a Tuesday morning to estimate how many county residents shop online.", "sampling bias", "Weekday-morning mall shoppers are not representative of all residents."),
    ("A poll about a city bus route is taken only among people who ride that route.", "sampling bias", "Riders of that route are not representative of all residents."),
    ("A question asks, “Most experts agree that homework helps. Do you agree?”", "leading question", "Mentioning experts pressures respondents to agree."),
    ("A survey of 2,000 people about phone use is posted only on a gaming website.", "undercoverage", "People who do not visit the site are left out."),
    ("A cafeteria puts out a suggestion box and gets 12 notes, all complaints.", "voluntary response", "People who are unhappy are more likely to leave notes."),
]


@gen("A2.S.IC.A.2", 20)
def ic2_bias(rng):
    text, kind, why = rng.choice(BIAS)
    names = ["leading question", "sampling bias", "voluntary response", "undercoverage", "nonresponse", "small sample size"]
    others = [n for n in names if n != kind]
    rng.shuffle(others)
    ds = [(o.capitalize(), f"The main problem is {kind}: {why[0].lower() + why[1:]}") for o in others]
    return mc("A2.S.IC.A.2", 2, "Y", f"{text} What is the main source of bias?", kind.capitalize(), ds, why, rng)


# ===================================================== A2.S.IC.A.3
@gen("A2.S.IC.A.3", 8)
def ic3_stat_param(rng):
    pop, n, what = rng.choice([("all students at a high school", rng.choice([50, 80, 120]), "the mean number of hours of sleep"),
                               ("all registered voters in a county", rng.choice([400, 600, 900]), "the percent who support a new tax"),
                               ("all phones made in a factory last month", rng.choice([200, 300]), "the percent that are defective"),
                               ("all adults in a state", rng.choice([1000, 1500]), "the mean amount spent on groceries each week")])
    val = rng.choice(["7.2 hours", "54%", "3%", "$142"]) if False else None
    ask = rng.choice(["stat", "param"])
    stem = (f"A researcher wants to know {what} for {pop}. She selects a random sample of {n} and finds the value for the sample. ")
    if ask == "stat":
        stem += "Which describes the value she found?"
        ans = "a statistic, because it describes the sample"
        ds = [("a parameter, because it describes the sample", "A parameter describes the whole population."),
              ("a parameter, because it describes the population", "She measured only the sample."),
              ("a statistic, because it describes the population", "A statistic describes a sample.")]
    else:
        stem += f"Which describes {what} for {pop}?"
        ans = "a parameter, because it describes the population"
        ds = [("a statistic, because it describes the population", "A statistic describes a sample."),
              ("a statistic, because it describes the sample", "This value is for the whole population."),
              ("a parameter, because it describes the sample", "A parameter describes the population.")]
    return mc("A2.S.IC.A.3", 1, "Y", stem, ans[0].upper() + ans[1:] + ".", [(t[0].upper() + t[1:] + ".", w) for t, w in ds],
              "A statistic summarizes a sample; a parameter summarizes the whole population.", rng)


EVAL = [
    ("A study finds that cities with more ice cream sales have more sunburns. A report concludes that ice cream causes sunburns.",
     "The conclusion is not justified; hot, sunny weather could explain both.",
     ["The conclusion is justified because the data show a strong relationship.", "The conclusion is justified because the study used real sales data.",
      "The conclusion is not justified because ice cream sales cannot be measured."]),
    ("In a randomized experiment, students assigned to a tutoring program scored higher than students not assigned. A report concludes the program likely improved scores.",
     "The conclusion is reasonable because random assignment makes the groups comparable.",
     ["The conclusion is not justified because it is an experiment.", "The conclusion is not justified because tutoring cannot be measured.",
      "The conclusion proves every student will improve with tutoring."]),
    ("A random sample of 1,000 adults found 62% support a policy. A report says exactly 62% of all adults support it.",
     "The report overstates the result; 62% is an estimate with sampling variability.",
     ["The report is correct because the sample was random.", "The report is correct because 1,000 is a large number.",
      "The report should say 38% support the policy."]),
    ("Students who eat breakfast have higher grades, according to school records. A report claims eating breakfast causes higher grades.",
     "The conclusion is not justified because this is observational data and other factors could be involved.",
     ["The conclusion is justified because school records are accurate.", "The conclusion is justified because the relationship is positive.",
      "The conclusion is not justified because grades are not numerical."]),
    ("A random sample of 40 students at one school shows that 70% walk to school. A report says 70% of students in the whole state walk to school.",
     "The conclusion is not justified because one school does not represent the whole state.",
     ["The conclusion is justified because the sample was random.", "The conclusion is justified because 70% is a majority.",
      "The conclusion is not justified because 40 is an even number."]),
    ("An experiment randomly assigned 200 patients to a new drug or a placebo. The drug group recovered faster. A report claims the drug cures everyone.",
     "The report overstates the result; the drug group recovered faster on average, not every patient.",
     ["The report is correct because it was an experiment.", "The report is correct because 200 patients is a large sample.",
      "The report is wrong because placebos always work better."]),
    ("A survey of 25 volunteers at a car show finds 90% want more electric cars. A report says 90% of drivers want more electric cars.",
     "The conclusion is not justified because the volunteers at a car show are not a random sample of drivers.",
     ["The conclusion is justified because 90% is very high.", "The conclusion is justified because the people surveyed own cars.",
      "The conclusion is not justified because 25 is an odd number."]),
]


@gen("A2.S.IC.A.3", 7)
def ic3_evaluate(rng):
    text, ans, wrong = rng.choice(EVAL)
    ds = [(w, "Consider how the data were collected and what kind of conclusion the design supports.") for w in wrong]
    return mc("A2.S.IC.A.3", 3, "Y", f"{text} Which statement best evaluates the report?", ans, ds, ans, rng)


# ===================================================== A2.S.CP.A.1
EVERYDAY = [
    ("flipping a coin and getting heads, then rolling a number cube and getting 6", True, "The coin does not affect the number cube."),
    ("drawing a red card from a deck, then drawing another red card without putting the first one back", False, "Removing a card changes what is left."),
    ("it raining today and a soccer game being canceled today", False, "Rain makes a cancellation more likely."),
    ("choosing a student at random who is left-handed and the same student having a birthday in May", True, "Handedness has no connection to birth month."),
    ("a student studying for a test and the student passing the test", False, "Studying changes the chance of passing."),
    ("spinning a spinner and landing on blue, then spinning again and landing on blue", True, "Each spin starts fresh."),
    ("picking a marble from a bag and keeping it, then picking a second marble from the same bag", False, "The first draw changes what remains in the bag."),
    ("a car running out of gas and the driver being late to work", False, "Running out of gas makes being late more likely."),
    ("rolling two different number cubes and getting a 3 on each", True, "One cube does not affect the other."),
    ("the temperature outside being below freezing and a lake being frozen", False, "Cold weather makes a frozen lake more likely."),
    ("a randomly chosen person's favorite color being green and the person's shoe size being 9", True, "Favorite color has no connection to shoe size."),
    ("forgetting an umbrella and getting wet on a rainy day", False, "Not having an umbrella makes getting wet more likely."),
    ("choosing a card from a deck, replacing it, and choosing again", True, "Replacing the card keeps the deck the same."),
    ("a phone's battery being low and the phone shutting off during a call", False, "A low battery makes shutting off more likely."),
    ("tossing a coin twice and getting tails both times", True, "The first toss does not affect the second."),
]


@gen("A2.S.CP.A.1", 9)
def cpa1_everyday(rng):
    text, indep, why = rng.choice(EVERYDAY)
    ans = "independent" if indep else "dependent"
    other = "dependent" if indep else "independent"
    stem = f"Consider the events: {text}. Are these events independent or dependent?"
    ds = [(f"{other.capitalize()}, because " + ("the outcome of one changes the probability of the other." if other == "dependent" else "the outcome of one does not change the probability of the other."), why),
          (f"{ans.capitalize()}, because both events can happen at the same time.", "Whether events can happen together is not the test for independence."),
          ("Neither, because only one of the events can happen.", "Both events can occur.")]
    full = f"{ans.capitalize()}, because " + ("the outcome of one does not change the probability of the other." if indep else "the outcome of one changes the probability of the other.")
    return mc("A2.S.CP.A.1", 2, "Y", stem, full, ds, why, rng)


@gen("A2.S.CP.A.1", 6)
def cpa1_table(rng):
    cats = rng.choice([(("Plays an instrument", "Does not"), ("Grade 10", "Grade 11")), (("Has a pet", "No pet"), ("Lives in town", "Lives outside town")),
                       (("Prefers mornings", "Prefers evenings"), ("Athlete", "Not an athlete"))])
    indep = rng.random() < 0.5
    if indep:
        a = rng.choice([10, 12, 15, 20, 30])
        k = rng.choice([2, 3])
        m = rng.choice([2, 3, 4])
        A = [[a, a * k], [a * m, a * k * m]]
    else:
        A = [[rng.randint(10, 40) for _ in range(2)] for _ in range(2)]
        if A[0][0] * A[1][1] == A[0][1] * A[1][0] or abs(A[0][0] / (A[0][0] + A[1][0]) - A[0][1] / (A[0][1] + A[1][1])) < 0.08:
            raise Skip
    (c1, c2), (r1, r2) = cats
    tbl = table(["", c1, c2], [[r1, A[0][0], A[0][1]], [r2, A[1][0], A[1][1]]], row_head=True)
    tot = sum(map(sum, A))
    pA = F(A[0][0] + A[1][0], tot)
    pAgB = F(A[0][0], A[0][0] + A[0][1])
    stem = f"A survey of {tot} students is summarized in the table.{tbl}Are the events “{c1.lower()}” and “{r1.lower()}” independent?"
    if indep:
        ans = f"Yes, because P({c1.lower()} | {r1.lower()}) = P({c1.lower()}) = {num(pA)}."
        ds = [(f"No, because P({c1.lower()} | {r1.lower()}) ≠ P({c1.lower()}).", f"Both probabilities equal {num(pA)}."),
              (f"No, because the counts in the table are different.", "Independence compares probabilities, not raw counts."),
              (f"Yes, because both events can happen to the same student.", "That is not the test for independence.")]
    else:
        ans = f"No, because P({c1.lower()} | {r1.lower()}) = {num(pAgB)} but P({c1.lower()}) = {num(pA)}."
        ds = [(f"Yes, because P({c1.lower()} | {r1.lower()}) = P({c1.lower()}).", f"{num(pAgB)} ≠ {num(pA)}."),
              (f"Yes, because the events can happen at the same time.", "That is not the test for independence."),
              (f"No, because the table has more than 50 students.", "The total does not determine independence.")]
    return mc("A2.S.CP.A.1", 3, "Y", stem, ans, ds,
              f"{M(f'P(\\text{{A}}) = {num(pA)}')} and {M(f'P(\\text{{A}} \\mid \\text{{B}}) = {num(pAgB)}')}. "
              f"Events are independent when these are equal.", rng)


# ===================================================== A2.S.CP.B.2
@gen("A2.S.CP.B.2", 8)
def cpb2_fcp(rng):
    kind = rng.choice(["outfit", "code", "menu", "plate"])
    if kind == "outfit":
        a, b, c = rng.randint(3, 7), rng.randint(2, 6), rng.randint(2, 4)
        stem = f"A student has {a} shirts, {b} pairs of pants, and {c} pairs of shoes. How many different outfits of one shirt, one pair of pants, and one pair of shoes are possible?"
        ans = a * b * c
        ds = [(str(a + b + c), "Added the choices; multiply them instead."), (str(a * b), "Left out the shoes."), (str(comb(a + b + c, 3)), "Order and category matter here; use the counting principle.")]
        expl = f"{a} × {b} × {c} = {ans}."
    elif kind == "code":
        n = rng.choice([3, 4])
        rep = rng.random() < 0.5
        ans = 10 ** n if rep else perm(10, n)
        stem = f"A lock code uses {n} digits from 0 to 9{'; digits may repeat' if rep else ', and no digit can repeat'}. How many codes are possible?"
        ds = [(comma(perm(10, n) if rep else 10 ** n), "Check whether digits can repeat."), (comma(10 * n), "Multiplied 10 by the number of digits."),
              (comma(comb(10, n)), "In a code, order matters.")]
        expl = f"{' × '.join(['10'] * n) if rep else ' × '.join(str(10 - i) for i in range(n))} = {comma(ans)}."
        return mc("A2.S.CP.B.2.a", 2, "Y", stem, comma(ans), ds, expl, rng)
    elif kind == "menu":
        a, b, c = rng.randint(2, 6), rng.randint(3, 8), rng.randint(2, 5)
        stem = f"A lunch special includes one of {a} soups, one of {b} sandwiches, and one of {c} drinks. How many different lunch specials are possible?"
        ans = a * b * c
        ds = [(str(a + b + c), "Added the choices; multiply them instead."), (str(a * b + c), "Multiply all three counts."), (str(a * b * c * 3), "Each meal is counted once.")]
        expl = f"{a} × {b} × {c} = {ans}."
    else:
        L, D = rng.choice([(2, 3), (3, 3), (3, 2), (2, 4)])
        ans = 26 ** L * 10 ** D
        stem = f"A license plate has {L} letters (A–Z) followed by {D} digits (0–9). Letters and digits may repeat. How many plates are possible?"
        ds = [(comma(26 * L + 10 * D), "Multiply the choices for each position."), (comma(perm(26, L) * perm(10, D)), "Letters and digits may repeat."),
              (comma(26 ** L + 10 ** D), "Multiply the letter count and the digit count.")]
        expl = f"{M(f'26^{{{L}}} \\times 10^{{{D}}} = {comma(ans).replace(',', '{,}')}')}."
        return mc("A2.S.CP.B.2.a", 2, "Y", stem, comma(ans), ds, expl, rng)
    return mc("A2.S.CP.B.2.a", 1, "Y", stem, str(ans), ds, expl, rng)


@gen("A2.S.CP.B.2", 8)
def cpb2_perm_comb(rng):
    n = rng.randint(6, 15)
    r = rng.randint(2, 4)
    order = rng.random() < 0.5
    group = rng.choice(["club members", "students", "runners", "volunteers"])
    if order:
        roles = ["president", "vice president", "secretary", "treasurer"][:r]
        stem = f"From {n} {group}, a {', '.join(roles[:-1])}{',' if r > 2 else ''} and {roles[-1]} will be chosen. How many ways can these positions be filled?"
        if group == "runners":
            stem = f"In a race with {n} runners, how many ways can the first {r} places be awarded?"
        ans = perm(n, r)
        ds = [(comma(comb(n, r)), "The positions are different, so order matters."), (comma(n ** r), "A person cannot hold two positions."), (comma(n * r), "Multiply n · (n − 1) · ...")]
        expl = f"Order matters: {M(f'{{}}_{{{n}}}P_{{{r}}} = ' + ' \\cdot '.join(str(n - i) for i in range(r)) + f' = {comma(ans)}'.replace(',', '{,}'))}."
        std = "A2.S.CP.B.2.b"
    else:
        stem = f"A committee of {r} will be chosen from {n} {group}. How many different committees are possible?"
        ans = comb(n, r)
        ds = [(comma(perm(n, r)), "A committee has no order, so divide by the arrangements."), (comma(n ** r), "A person cannot be chosen twice, and order does not matter."),
              (comma(n * r), "Use combinations, not n times r.")]
        expl = f"Order does not matter: {M(f'{{}}_{{{n}}}C_{{{r}}} = {ans}')}."
        std = "A2.S.CP.B.2.b"
    return mc(std, 2, "Y", stem, comma(ans), ds, expl, rng)


@gen("A2.S.CP.B.2", 9)
def cpb2_probability(rng):
    a = rng.randint(3, 8)
    b = rng.randint(3, 8)
    r = rng.choice([2, 3])
    if r > a:
        raise Skip
    na, nb = rng.choice([("girls", "boys"), ("juniors", "seniors"), ("red marbles", "blue marbles"), ("teachers", "students")])
    stem = f"A group has {a} {na} and {b} {nb}. {r} are chosen at random. What is the probability that all {r} are {na}?"
    p = F(comb(a, r), comb(a + b, r))
    ds = [(M(num(F(a, a + b))), f"That is the probability for one choice only."),
          (M(num(F(a, a + b) ** r)), "This assumes replacement; without replacement the probability changes after each pick."),
          (M(num(F(r, a + b))), "Divide the number of favorable groups by the number of possible groups."),
          (M(num(F(perm(a, r), comb(a + b, r)))) if F(perm(a, r), comb(a + b, r)) < 1 else M(num(F(comb(a, r), perm(a + b, r)))), "Mixed permutations and combinations.")]
    return mc("A2.S.CP.B.2.b", 2, "Y", stem, M(num(p)), ds,
              f"{M(f'\\frac{{{{}}_{{{a}}}C_{{{r}}}}}{{{{}}_{{{a + b}}}C_{{{r}}}}} = \\frac{{{comb(a, r)}}}{{{comb(a + b, r)}}} = {num(p)}')}.", rng)


# ===================================================== A2.S.CP.B.3
LLN = [
    ("A basketball player makes 3 of her first 4 free throws and claims she is a 75% shooter.",
     "Four shots are too few; over many more shots her percentage will better reflect her true skill."),
    ("A student rolls a number cube 12 times and gets a 6 four times. He claims the cube is unfair.",
     "Twelve rolls are too few to judge; over many rolls a fair cube's proportion of 6s should approach 1/6."),
    ("A coin is flipped 8 times and lands on heads 6 times. A student says the next flip is more likely to be tails.",
     "Each flip is independent; the long-run proportion approaches 0.5, but a single flip is still 50-50."),
    ("A new restaurant has 5 online reviews, all 5 stars. The owner claims it is the best restaurant in town.",
     "Five reviews are too few to support the claim; more data would give a more reliable rating."),
    ("A spinner with 4 equal sections lands on red 2 times in 5 spins. A student says P(red) is 40%.",
     "Five spins are too few; with many more spins the proportion should approach 25%."),
    ("A game app says players win 1 in 10 games. After 10 games, a player has not won and says the app is wrong.",
     "Ten games are too few; the 1-in-10 rate describes the long run over many games."),
    ("A weather station recorded rain on 3 of the first 4 days of a month and predicts 75% of days will be rainy.",
     "Four days are too few to estimate the rate; more days of data are needed."),
    ("A student draws a card from a deck, replaces it, and gets a heart 4 times in 6 draws. She says hearts are most likely.",
     "Six draws are too few; over many draws the proportion of hearts should approach 1/4."),
]


@gen("A2.S.CP.B.3", 8)
def cpb3_lln(rng):
    text, ans = rng.choice(LLN)
    ds = [("The claim is correct because the results came from real trials.", "A small number of trials can vary a lot from the true probability."),
          ("The claim is correct because the results are already more than half.", "Short-run results do not reliably show long-run probability."),
          ("The claim cannot be tested with more trials.", "More trials give a better estimate of the true probability.")]
    return mc("A2.S.CP.B.3", 2, "Y", f"{text} Which statement best evaluates the claim?", ans, ds,
              "By the Law of Large Numbers, the proportion in many trials gets close to the true probability; a few trials can be misleading.", rng)


# ===================================================== A2.S.CP.C.4
@gen("A2.S.CP.C.4", 8)
def cpc4_table(rng):
    (c1, c2), (r1, r2), who = rng.choice([
        (("Bus", "Car"), ("Juniors", "Seniors"), "students"), (("Cats", "Dogs"), ("Own a pet", "Want a pet"), "students"),
        (("Yes", "No"), ("Freshmen", "Sophomores"), "students asked whether they play a sport"),
        (("Chocolate", "Vanilla"), ("Adults", "Children"), "people asked about ice cream")])
    A = [[rng.randint(8, 45) for _ in range(2)] for _ in range(2)]
    tot = sum(map(sum, A))
    tbl = table(["", c1, c2, "Total"], [[r1, A[0][0], A[0][1], sum(A[0])], [r2, A[1][0], A[1][1], sum(A[1])],
                                         ["Total", A[0][0] + A[1][0], A[0][1] + A[1][1], tot]], row_head=True)
    i, j = rng.randrange(2), rng.randrange(2)
    rows, cols = [r1, r2], [c1, c2]
    given_row = rng.random() < 0.5
    cell = A[i][j]
    T = lambda w: "\\text{" + w + "}"
    if given_row:
        den = sum(A[i])
        q = f"what is {M(f'P({T(cols[j])} \\mid {T(rows[i])})')}, the probability that the person is in the {cols[j]} column given that the person is in the {rows[i]} row?"
    else:
        den = A[0][j] + A[1][j]
        q = f"what is {M(f'P({T(rows[i])} \\mid {T(cols[j])})')}, the probability that the person is in the {rows[i]} row given that the person is in the {cols[j]} column?"
    ans = F(cell, den)
    other_den = (A[0][j] + A[1][j]) if given_row else sum(A[i])
    ds = [(M(num(F(cell, tot))), "That is the joint probability; for a conditional probability divide by the total of the given group."),
          (M(num(F(cell, other_den))) if F(cell, other_den) != ans else M(num(F(den, tot))), "Divided by the wrong total; use the given condition's total."),
          (M(num(F(den, tot))), "That is the probability of the condition itself."),
          (M(num(F(den - cell, den))), "That is the complement within the given group.")]
    stem = f"The table shows the responses of {tot} {who}.{tbl}If one person is chosen at random, {q}"
    return mc("A2.S.CP.C.4", 2, "Y", stem, M(num(ans)), ds,
              f"Restrict to the given group ({den} people). Of those, {cell} are in the other category: {M(f'\\frac{{{cell}}}{{{den}}}' + ('' if ans == F(cell, den) and ans.numerator == cell else f' = {num(ans)}'))}.", rng)


@gen("A2.S.CP.C.4", 7)
def cpc4_percent(rng):
    pB = rng.choice([0.4, 0.5, 0.6, 0.75, 0.8])
    pAB = rng.choice([0.1, 0.15, 0.2, 0.24, 0.3, 0.36])
    if pAB >= pB:
        raise Skip
    ans = pAB / pB
    if abs(ans * 100 - round(ans * 100)) > 1e-9:
        raise Skip
    ctx = rng.choice([("passed the first quiz", "passed both quizzes", "who passed the first quiz also passed the second"),
                      ("own a bike", "own a bike and a skateboard", "who own a bike also own a skateboard"),
                      ("take Spanish", "take Spanish and band", "who take Spanish are also in band"),
                      ("play a sport", "play a sport and an instrument", "who play a sport also play an instrument")])
    stem = f"At a school, {pct(pB, 0)} of students {ctx[0]} and {pct(pAB, 0)} {ctx[1]}. What percent of the students {ctx[2]}?"
    ds = [(pct(pAB * pB, 1), "Multiplied instead of dividing."), (pct(pB - pAB, 0), "Subtracted instead of dividing."),
          (pct(pAB, 0), "That is the “and” probability, not the conditional probability."), (pct(pB / (pB + pAB), 0), "Divided by the wrong total.")]
    return mc("A2.S.CP.C.4", 2, "Y", stem, pct(ans, 1), ds,
              f"{M(f'P(\\text{{B}} \\mid \\text{{A}}) = \\frac{{P(\\text{{A and B}})}}{{P(\\text{{A}})}} = \\frac{{{dec(pAB)}}}{{{dec(pB)}}} = {dec(ans)}')}, or {pct(ans, 1)}.", rng)
