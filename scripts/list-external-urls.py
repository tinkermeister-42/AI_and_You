#!/usr/bin/env python3
"""list-external-urls.py [--json]: every outside web address the book uses.
Kinds: "link" (students click it), "video" (embedded), "page" (loaded by every
page: scripts, fonts). Used by the teacher guide and for the school firewall check."""
import re, glob, json, sys, pathlib
from urllib.parse import urlparse

def where(path):
    m = re.search(r"(\d\.\d)_", path)
    if m: return m.group(1)
    if "explore-unit-" in path: return "Explore " + re.search(r"explore-unit-(\d)", path).group(1)
    return pathlib.Path(path).stem

found = {}
def add(url, kind, src):
    url = url.rstrip(".,;)")
    if "localhost" in url or url.startswith("https://www.openstreetmap.org/?mlat=$"): pass
    e = found.setdefault(url, {"url": url, "domain": urlparse(url).netloc.removeprefix("www."), "kind": kind, "where": set()})
    if kind == "video": e["kind"] = "video"
    e["where"].add(src)

for f in sorted(glob.glob("chapters/**/*.qmd", recursive=True)) + ["index.md", "syllabus.qmd", "course-map.qmd", "glossary.qmd"]:
    s = open(f).read()
    for u in re.findall(r"\{\{<\s*video\s+(https?://\S+)", s): add(u, "video", where(f))
    for v in re.findall(r"\{\{<\s*ytvideo\s+([\w-]+)", s): add("https://www.youtube-nocookie.com/embed/" + v, "video", where(f))
    for u in re.findall(r"\]\((https?://[^)\s]+)\)", s): add(u, "link", where(f))
    for u in re.findall(r'href="(https?://[^"]+)"', s): add(u, "link", where(f))
for f in sorted(glob.glob("assets/**/*.html", recursive=True)):
    s = open(f).read()
    for u in re.findall(r'(https?://[a-zA-Z0-9.-]+\.[a-z]{2,}[^\s"\'`<>)]*)', s):
        if "${" in u:  # a template, like the map link built from a photo's location
            u = u.split("?")[0]
        add(u, "link", where(f))
for f in sorted(glob.glob("handouts/**/*.tex", recursive=True)):
    for u in re.findall(r"\\url\{(https?://[^}]+)\}|\\href\{(https?://[^}]+)\}", open(f).read()):
        add(u[0] or u[1], "link", where(f))
# what every page loads from outside (fonts, math, search)
for f in glob.glob("_book/**/*.html", recursive=True):
    s = open(f).read()
    for u in re.findall(r'<(?:script|link|iframe)[^>]+(?:src|href)="(https?://[^"]+)"', s):
        kind = "video" if "youtube" in u else "page"
        add(u, kind, "every page" if kind == "page" else where(f))

rows = sorted(found.values(), key=lambda e: ({"link": 0, "video": 1, "page": 2}[e["kind"]], e["domain"], e["url"]))
for r in rows: r["where"] = sorted(r["where"])
if "--json" in sys.argv: print(json.dumps(rows, indent=1))
else:
    for r in rows: print(f'{r["kind"]:6} {r["domain"]:32} {r["url"]}   [{", ".join(r["where"])}]')
