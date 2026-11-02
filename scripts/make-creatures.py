#!/usr/bin/env python3
"""Make the made-up creature data for Unit 2 (Lessons 2.4 to 2.6).

The recipe is the point: the book knows the real rule, so students can compare
what a network learns with the truth (Explore More, Unit 2).

  Type     Strength  Magic   Size
  Fighter  high      low     medium
  Wizard   low       high    medium
  Giant    very high very high  big
  Mini     very low  very low   small

Strength and Magic: normal, spread 12, kept between 5 and 100.
Speed and Toughness: the same for every type (noise).
Height: Giant about 3 m, Mini about 0.5 m, Fighter and Wizard about 1.5 m.
Weight: about 30 x height^2, give or take.
Home: Forest, Mountain or Lake, at random. It has nothing to do with anything.

Writes data/creatures.json. scripts/embed-creatures.py puts it in the widgets.
"""
import json, os, numpy as np

SEED = 2
COUNTS = dict(fighter=70, wizard=70, giant=60, mini=100)
MEANS = dict(fighter=(66, 40), wizard=(40, 66), giant=(82, 82), mini=(24, 24))
SPREAD = 12

# real words to skip (and anything else that reads badly)
COMMON = set("villa villas sevas domba toga tomb bomb gun kill dead poop butt boob bum sex pee "
             "dork dumb fat ugly stupid nazi gay sin lube".split())

def names(n, rng, banned):
    start = "b d f g k l m n p r s t v z br dr gr kr pl sk sn tr gl fl".split()
    vow = "a e i o u a o i".split()
    mid = "b d g k l m n p r s t v z ll rr nd nk mb sh".split()
    end = ["", "", "", "x", "k", "n", "r", "l", "s", "m"]
    out, seen = [], set(banned)
    while len(out) < n:
        k = 2 if rng.random() < 0.75 else 3
        w = rng.choice(start) + rng.choice(vow)
        for _ in range(k - 1):
            w += rng.choice(mid) + rng.choice(vow)
        w += rng.choice(end)
        if len(w) > 7 or w in seen or w in COMMON: continue
        seen.add(w); out.append(w.capitalize())
    return out

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    rng = np.random.default_rng(SEED)
    rows = []
    for t, n in COUNTS.items():
        for _ in range(n):
            s, m = (int(round(np.clip(rng.normal(MEANS[t][k], SPREAD), 5, 100))) for k in range(2))
            h = {"giant": rng.normal(3.0, 0.5), "mini": rng.normal(0.5, 0.12)}.get(t, rng.normal(1.5, 0.3))
            h = max(0.2, float(h))
            w = max(1.0, 30 * h * h * float(rng.lognormal(0, 0.25)))
            spd = int(round(np.clip(rng.normal(50, 15), 5, 100)))
            tough = int(round(np.clip(rng.normal(50, 15), 5, 100)))
            home = str(rng.choice(["forest", "mountain", "lake"]))
            rows.append([t, s, m, spd, tough, round(h, 1), int(round(w)), home])
    banned = set()
    pk = os.path.join(here, "pokemon-names.txt")   # optional: names to avoid
    if os.path.exists(pk):
        banned = {l.strip().lower() for l in open(pk) if l.strip()}
    nm = names(len(rows), rng, banned)
    order = rng.permutation(len(rows))
    data = [[nm[i]] + rows[j] for i, j in enumerate(order)]
    json.dump({"fields": ["name", "type", "strength", "magic", "speed", "toughness", "height", "weight", "home"],
               "rows": data}, open(os.path.join(here, "..", "data", "creatures.json"), "w"), separators=(",", ":"))
    print(len(data), "creatures")

if __name__ == "__main__":
    main()
