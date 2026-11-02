#!/usr/bin/env python3
"""Put data/creatures.json into every widget that has a line starting with
`  const CREATURES = ` (one line, replaced in place)."""
import glob, json, os, re
here = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(here, "..", "data", "creatures.json")))["rows"]
line = "  const CREATURES = " + json.dumps(rows, separators=(",", ":")) + ";  // made by scripts/make-creatures.py"
for f in glob.glob(os.path.join(here, "..", "assets", "Unit_*", "*.html")):
    s = open(f).read()
    if "\n  const CREATURES = " not in s: continue
    s2 = re.sub(r"\n  const CREATURES = .*", lambda m: "\n" + line, s)
    if s2 != s: open(f, "w").write(s2); print("updated", os.path.relpath(f))
