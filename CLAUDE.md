# AI and You: Project Context

The book for "AI and You", an AI literacy elective at Frederick Douglass High
School. A 17-week mini-block class: every lesson is **40 minutes** and every
lesson has a hands-on activity. Most students are English learners, many with
little math background. The units and their weeks are the table in
`index.md`, taken from the teacher's syllabus.

Built from the DHS Statistics book (`tinkermeister-42/Statistics`), which was
built from DHS Algebra 1: same theme, callouts, glossary and headings
extensions, TikZ figures, and pdflatex handouts.

**Do not make it easier.** The content is real: how machine learning works,
neural networks, bias, the history. Simplify the sentence, never the idea.
"A chatbot predicts the next word, again and again" is the level to aim for:
plain words, true statement.

## Build & Deploy
- **Handouts:** `./build.sh [1.1 ...]` builds `handouts/Unit_X/<name>.pdf` and
  `<name>_KEY.pdf` from one `.tex` (pdflatex, TikZ). Commit the PDFs
- **Web figures:** `scripts/make-figures.sh [1.1 ...]` turns
  `figures/Unit_X/<name>.tex` into `images/Unit_X/<name>.svg`. Shared colors
  and styles are in `figures/preamble.tex`
- **Logo:** `figures/logo.tex`, built by hand (commands in the file) to
  `images/logo.svg` and `images/logo.png`
- **Render:** `quarto render --to html` (run it twice on a fresh clone: the
  glossary post-render writes `glossary.json` after the copy step)
- **Deploy:** `./deploy.sh` renders, runs `scripts/check-site-assets.py`
  (fails on a missing or stale PDF or SVG), and force-pushes `_book` to
  `gh-pages` (personal site: `tinkermeister-42.github.io/AI_and_You`)
- **Mirror to the work site is manual.** The teacher reviews the personal
  site, then runs "Mirror site to Work Account" from the Actions tab
  (`.github/workflows/sync-to-work.yml`, workflow_dispatch from `main`). It
  force-pushes `gh-pages` to the repo named by the `WORK_OWNER` and
  `WORK_REPO` secrets with `WORK_TOKEN`. Keep workflow files off `gh-pages`
- A shallow clone fetches only `main`, so `deploy.sh` dies with "invalid
  reference: origin/gh-pages". Fix with
  `git config remote.origin.fetch '+refs/heads/*:refs/remotes/origin/*' && git fetch --depth 1 origin gh-pages`
- A container needs quarto >= 1.7 (tarball from the quarto-cli releases into
  `/opt/quarto`), pdflatex, `pdftocairo` (poppler), and a clean tree

## Structure
```
chapters/Unit_1…8/     # Lessons: #.#_Topic.qmd, index.qmd (unit intro)
handouts/Unit_1…8/     # Printable lesson sheets: .tex source, student + _KEY PDFs
figures/Unit_1…8/      # TikZ sources for web figures -> images/Unit_X/*.svg
assets/Unit_1…8/       # Interactive widgets, included with {{< include >}}
scripts/               # JS helpers, glossary build, figure build, asset check
styles/                # Shared CSS from the other books + ai-and-you.css
_extensions/           # glossary, headings
glossary.qmd           # Source -> glossary.json on render
```

## Lesson Page Pattern
1.1 is the model. In order:

1. Title, then a concrete hook (three short paragraphs at most)
2. `.agenda`: "Today's Plan" cards with minutes that add to 40
3. `.objectives`, then `.vocab` holding a `.word-cards` list (emoji, glossary
   link, short meaning). Every vocab word has a glossary entry
4. `.guided-notes-link` to the student PDF
5. `{{< warmup >}}`, `{{< learn >}}` with numbered `### #.#.# -` sections,
   `{{< tryit >}}`, `{{< bigq >}}`, then `{{< watch >}}` and `{{< further >}}`

- **The Big Question runs through every lesson.** "Is AI like a human
  brain?" Each lesson ends with a `.big-question` prompt and `.frames`
  (sentence starters). Unit 8 is the final project built on these answers
- **Lesson, handout and figures are one change.** The handout restates the
  page's activities. Handouts pull shared figures with `\fig{Unit_X/<name>}`
- **Keys are unlisted.** `<name>_KEY.pdf` is served beside the student PDF
  but nothing links to it. The URL is predictable on purpose
- Worksheet directions say "Work with a partner", never "work by yourself"
- Handout tables use ragged-right columns: no hyphenated words for second
  language readers
- **Figure colors mean something:** blue is a person, orange is the computer,
  green is an answer, pink is the human brain

## Callout Types
The Algebra 1 set (`.objectives`, `.vocab`, `.remember`, `.real-world`,
`.you-try`, `.you-try-m`, `.think`, `.gotcha`, `.answer(s)`, `.note`) plus:

| Class | Purpose |
|---|---|
| `.watch` | A video, with a "while you watch" prompt (red) |
| `.steps` | Numbered steps for a hands-on activity (teal) |
| `.frames` | Sentence starters for talking and writing (orange) |
| `.big-question` | The Big Question prompt; `[text]{.bq}` is the large line (pink) |
| `.project` | A Go Further project idea (indigo) |

Syntax: `:::{.callout-type title="Title"} … :::`. New types need an entry in
`scripts/custom-callouts.js` and styles in `styles/ai-and-you.css`.

## Links, Videos and Tools
- **Fetch every link before it goes in.** Tools and videos disappear. A
  dead link in front of a class costs the block
- **Videos:** short, from a source that will keep them up (Code.org's How AI
  Works series is the default). Embed with `{{< video URL title="..." >}}`
  inside a `.watch` callout, and keep the caption/auto-translate tip
- **Tools students open:** prefer ones that need no account (Quick, Draw!,
  Teachable Machine). Anything that needs a student account must be allowed
  under the district's AI Use Plan; Claude.ai and ChatGPT have age limits.
  Teacher-led demos on the projector are the fallback
- **Privacy:** when a tool saves what students make, say so in a `.gotcha`
  next to the activity (see Quick, Draw! in 1.1)
- **Home languages are an asset.** About 14 languages are spoken in the
  school. Activities that test AI in a student's own language make that
  student the expert

## Branches

Keep the repository clean. Dead branches are clutter.

- Work happens on a feature branch. Granular commits there are fine and
  wanted while the feature is still being worked on
- When a feature is finished it goes to `main` as **one squashed commit**
  naming the feature. `main` keeps a history of what was added, not of every
  step it took to get there
- The branch is deleted once it is merged
- **Nothing is merged or deleted without the teacher signing off on it.**
  Propose it, show what would land, and wait

Two things that bite:

- **Deploying is not merging.** `deploy.sh` force-pushes the built `_book` to
  `gh-pages` and touches nothing else, so a change can be live on the site
  while its source exists only on a feature branch. Check
  `git rev-list --count origin/main..HEAD` before assuming work is safe
- **Session credentials may not delete branches.** A 403 on
  `git push origin --delete` is a permission limit; branch removal is the
  teacher's to do

**Checking a squashed branch is safe to delete:** `git diff origin/main
origin/<branch>` (empty output means nothing would be lost). Ancestry checks
report a squash-merged branch as unmerged.

## Writing Style

**Who is reading this.** Most students are not native English speakers. Many
read well below grade level, and some have had little school before. Reading
is the barrier, not the ideas. Every sentence a student has to decode twice
is a sentence that costs them the idea.

- **Short sentences.** One idea each. Split a sentence before adding a clause
- **Common words.** Prefer "use" to "utilize", "shows" to "demonstrates"
- **No colloquialisms or figurative idioms**, where the literal words do not
  give the meaning. Plain phrasal verbs ("show up", "figure out") are fine
- **No dash asides.** The fix is not a different dash character, it is a
  different sentence. Split it in two, use a comma, or put a short aside in
  parentheses. Labels in a list take a colon. Section headings keep the
  spaced hyphen they already use
- **Lead with the concrete.** A picture, a game, or a story first; the idea
  after. The cat rule in 1.1.2 is the pattern to copy
- **Say what is true.** No "AI thinks" or "AI knows" as plain fact. Whether
  AI is like a brain is the question the class is asking, so the book does
  not answer it in passing

## Curriculum Judgment

**Do not propose cutting a lesson or a unit.** The teacher spent fifteen years
in AI and data science before teaching. Scope decisions are his. Report what
you find and let him decide.
