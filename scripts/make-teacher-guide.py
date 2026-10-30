#!/usr/bin/env python3
"""make-teacher-guide.py: build the unlisted teacher guide at _book/teacher/index.html.

Runs as a post-render step (see _quarto.yml), so it is never out of date. It is
built with pandoc, outside the book, so it is not in the menus or the site
search. Nothing links to it: the teacher bookmarks /teacher/.

It collects, from the sources:
  - every :::{.teacher title="..."} block in a lesson (strip-teacher.lua removes
    these from the student pages), shown under its lesson
  - each lesson's student sheet and _KEY
  - every "Right now (fall 2026)" box, to review each term
  - every outside website, for the school network check
"""
import glob, json, os, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "_book") / "teacher"
os.chdir(ROOT)

UNITS = {}
for idx in sorted(glob.glob("chapters/Unit_*/index.qmd")):
    n = re.search(r"Unit_(\d)", idx).group(1)
    m = re.search(r"\*\*Unit \d: ([^*]+)\*\*", open(idx).read())
    UNITS[n] = m.group(1) if m else f"Unit {n}"

def plain(md):
    """Quarto shortcodes mean nothing to pandoc: keep their text."""
    md = re.sub(r'\{\{<\s*glink\s+slug="[^"]+"\s+text="([^"]+)"\s*>\}\}', r"\1", md)
    md = re.sub(r'\{\{<\s*glink\s+"([^"]+)"\s*>\}\}', r"\1", md)
    md = re.sub(r"\{\{<\s*glink\s+([^\s>]+)\s*>\}\}", r"\1", md)
    return re.sub(r"\{\{<[^>]*>\}\}", "", md)

TEACHER = re.compile(r'^:::\s*\{\.teacher title="([^"]+)"\}\s*\n(.*?)^:::\s*$', re.M | re.S)
DATED = re.compile(r'^:::\s*\{\.note title="Right now \(fall 2026\)"\}\s*\n(.*?)^:::\s*$', re.M | re.S)

lessons = []
for f in sorted(glob.glob("chapters/Unit_*/[0-9]*.qmd")):
    s = open(f).read()
    num, title = re.match(r"#\s+(\d\.\d)\s+-\s+(.+?)\s+\{", s).groups()
    stem = pathlib.Path(f).stem
    sheets = sorted(pathlib.Path(p).stem for p in glob.glob(f"handouts/Unit_{num[0]}/{num}_*.tex"))
    lessons.append({"num": num, "title": title, "unit": num[0], "page": f"../chapters/Unit_{num[0]}/{stem}.html",
                    "sheets": sheets, "notes": TEACHER.findall(s), "dated": DATED.findall(s)})

dated_explore = []
for f in sorted(glob.glob("chapters/Explore/explore-unit-*.qmd")):
    for d in DATED.findall(open(f).read()):
        dated_explore.append((f"Explore More, Unit {re.search(r'unit-(\d)', f).group(1)}",
                              f"../chapters/Explore/{pathlib.Path(f).stem}.html", d))

urls = json.loads(subprocess.run([sys.executable, "scripts/list-external-urls.py", "--json"], capture_output=True, text=True, check=True).stdout)

def first_sentence(md):
    t = re.sub(r"\s+", " ", plain(md)).strip().lstrip("- ")
    m = re.match(r"(.+?[.!?])(\s|$)", t)
    return (m.group(1) if m else t)[:220]

md = [f"""---
title: "AI and You: Teacher Guide"
---

This page is for Mr. Ross. Nothing in the book links here, and it is not in the site search. Bookmark this address.

It is rebuilt every time the book is rendered, so it always matches the lessons.

## How the Lessons Fit the Calendar

- **38 lessons, about 64 meetings.** Each lesson has a 40-minute core. The core is planned at twice the usual time, for language support. **Go Further** fills a second day when there is time. When you are behind, skip Go Further; never squeeze a core.
- **Explore More** pages are for students working on their own. They are never needed for a core.
- **Raina** (MagicSchool) is the only AI tool students use with an account. Every Raina activity has a fallback: you run it on the projector, or an unplugged version. Images share a usage limit, so plan pairs or turns.
- **No personal information** goes into any AI tool: no names, pictures of people, addresses, phone numbers, birthdays, or student numbers.
- **Answer keys** sit beside each student sheet: `handouts/Unit_X/<name>_KEY.pdf`. Nothing links to them.

## Lessons
"""]
for n, name in UNITS.items():
    md.append(f"\n### Unit {n}: {name}\n")
    for L in (l for l in lessons if l["unit"] == n):
        sheets = " · ".join(f"[{s.split('_', 1)[1].replace('_', ' ')}](../handouts/Unit_{n}/{s}.pdf) ([key](../handouts/Unit_{n}/{s}_KEY.pdf))" for s in L["sheets"])
        md.append(f"\n#### [{L['num']} - {L['title']}]({L['page']})\n\n**Sheets:** {sheets or 'none'}\n")
        for t, body in L["notes"]:
            md.append(f"\n**{t}.** {plain(body).strip()}\n")

md.append("\n## Dated Boxes to Review Each Term\n\nThese \"Right now (fall 2026)\" boxes go out of date. Check each one before you teach that lesson.\n")
for L in lessons:
    for d in L["dated"]:
        md.append(f"- [{L['num']} - {L['title']}]({L['page']}): {first_sentence(d)}")
for where, page, d in dated_explore:
    md.append(f"- [{where}]({page}): {first_sentence(d)}")

md.append("\n## Outside Websites\n\nCheck these on the school network. A site is allowed if it needs no login, is not blocked, and collects no student data.\n")
for r in urls:
    kind = {"link": "students open", "video": "video", "page": "every page loads"}[r["kind"]]
    md.append(f"- `{r['domain']}`: <{r['url']}> ({kind}; {', '.join(r['where'])})")

OUT.mkdir(parents=True, exist_ok=True)
src = OUT / "index.md"
src.write_text("\n".join(md) + "\n")
head = OUT / "head.html"
head.write_text("""<meta name="robots" content="noindex, nofollow">
<style>
:root { --bg: #fbfcfd; --fg: #1f2d36; --muted: #5b6b76; --line: #d9e1e8; --accent: #0f6e78; }
@media (prefers-color-scheme: dark) { :root { --bg: #131b20; --fg: #e3eaee; --muted: #9aaab4; --line: #2c3a43; --accent: #5cc3cc; color-scheme: dark; } }
body { background: var(--bg); color: var(--fg); font: 16px/1.6 system-ui, -apple-system, "Segoe UI", sans-serif; max-width: 860px; margin: 0 auto; padding: 24px 16px 64px; }
h1 { font-size: 1.7rem; } h2 { border-bottom: 2px solid var(--line); padding-bottom: 4px; margin-top: 2.2rem; }
h4 { margin: 1.4rem 0 0.3rem; } a { color: var(--accent); } code { font-size: 0.9em; }
header p.subtitle, header p.author { color: var(--muted); }
</style>
""")
subprocess.run(["quarto", "pandoc", str(src), "-s", "-o", str(OUT / "index.html"), "-H", str(head),
                "--metadata", "lang=en", "--toc", "--toc-depth=3"], check=True)
src.unlink(); head.unlink()
print(f"teacher guide: {OUT / 'index.html'} ({sum(len(l['notes']) for l in lessons)} teacher notes, {len(lessons)} lessons)")
