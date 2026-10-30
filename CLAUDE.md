# AI and You: Project Context

The book for "AI and You", an AI literacy elective at Frederick Douglass High
School. A one-semester mini-block class. Most students are English learners,
many with little math background. The six units and every lesson are in
`course-map.qmd`; the unit table is in `index.md`.

## Pacing
- The block is 45 minutes and meets daily, but the school uses it for
  college visits, field trips and assemblies, so the class meets about 3/4
  of the days (about 64 meetings)
- **38 lessons.** Each lesson is a 40-minute core (the "Today's Plan" minutes
  add to 40) plus a **Go Further** that can fill a second day. Behind
  schedule means skipping Go Further, never squeezing the core
- **Budget at twice the time.** Every activity takes these students about
  twice as long as a typical estimate: they need a lot of guidance through
  language barriers and learning gaps. Plan a core with about half of what
  would fill 40 minutes in a typical class (one main activity, not two).
  What does not fit goes in Go Further
- **Core, Go Further, Explore More.** A lesson's core is the warm-up, the
  essential idea, one main activity, and Talk About It. A second class
  activity goes first in Go Further as a "Day 2" project; its sheet section
  moves to the end of the sheet under "Go Further". Extra explanation,
  history, and extra widgets go to the unit's Explore More page
  (`chapters/Explore/explore-unit-N.qmd`, section id `#explore-N-M`), which
  is for students working on their own. Each lesson that has one ends with an
  `.explore-link` div pointing there. Never cut an acted-out experiment or a
  teacher favorite (Klingon Room, human network, live build, Rule 30) from a
  core to make room
- The teacher thinks 38 is already plenty. Do not add lessons to the map
  without asking
- Students miss days, so every lesson stands alone and the page is the
  catch-up path: a student who was out reads it and does the Try It

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
- **Deploy in batches:** once per finished unit or at the end of a working
  session, not after every lesson. Each push to `gh-pages` runs a Pages
  build, and the teacher's GitHub Actions allotment is limited
- **The teacher can only view the work site** (school network). A deploy is
  not visible to him until he runs the mirror, which this session is not
  allowed to trigger. Tell him when a batch is ready to mirror
- **Mirror to the work site is manual.** The teacher reviews the personal
  site, then runs "Mirror site to Work Account" from the Actions tab
  (`.github/workflows/sync-to-work.yml`, workflow_dispatch from `main`). It
  force-pushes `gh-pages` to `andyrosscps/DHS-AI_and_You` branch `gh-pages` (its
  Pages source, live at `andyrosscps.github.io/DHS-AI_and_You`), named by the
  `WORK_OWNER` and `WORK_REPO` secrets, with `WORK_TOKEN`. The workflow only
  appears in the Actions tab once it is on `main`. Keep workflow files off
  `gh-pages`: a workflow file there would also need the Workflows
  permission on the token
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

## Demos First
The teacher wants kids' hands on real things in every lesson.

- **The book carries the demos.** Prefer an interactive widget built into the
  page (`assets/Unit_X/*.html`) that students can change and watch: edit a
  chatbot's rules, turn a game bot's rules off, train a model in the browser.
  Widgets need no account, send nothing anywhere, and work on a Chromebook
- **No-login tools next** (Quick, Draw!, Teachable Machine, TensorFlow
  Playground, Google Translate), then physical activities
- **No platform dependency.** The school will likely give students only
  MagicSchool. When a lesson needs a chatbot, the page says "your class AI
  tool" and the activity works with any chatbot. Never write steps for one
  product's menus
- **The class AI tool is Raina, in MagicSchool.** Raina's own list of what it
  can do (October 2026; the teacher still has to confirm in class): text
  chat (write, rewrite, summarize, translate, explain, math help), image
  generation and graphs (one shared usage limit, so plan pairs or staggered
  turns), web search with cited sources, documents and slides. It cannot
  make audio, video, or voice clones; students cannot switch models or
  settings; no memory between chats. Photo upload is unconfirmed: never make
  it required. Every activity that uses Raina needs a fallback: Mr. Ross runs
  it on the projector, or an unplugged version. Raina is the only AI tool
  students may use with an account. District rule for any other site: it is
  allowed if it needs no login, is not blocked on the school network, and
  collects no student data (its concern is personal information tied to a
  login, so students never log in or type personal information). The
  teacher checks the network block; list any new outside tool for him
- **Students see AI built, but do not build it.** The teacher builds AI
  professionally. In Unit 2 he trains a real model live (his Pokémon stats
  demo: the CSV from his old Algebra site, a neural network instead of the
  regression he used then), and the class first trains a **physical**
  neural network on the same kind of data, so they can see how a simple
  network makes decisions. Students watch, test, and change things; they do
  not write code
- A widget that shows an idea with made-up numbers says so on the page
  ("This shows the idea. A real ... uses ...")

## Lesson Page Pattern
1.1 is the model. In order:

1. Title, then a concrete hook (three short paragraphs at most)
2. `.agenda`: "Today's Plan" cards with minutes that add to 40
3. `.objectives`, then `.vocab` holding a `.word-cards` list (emoji, glossary
   link, short meaning). Every vocab word has a glossary entry
4. `.guided-notes-link` to the student PDF
5. `{{< warmup >}}`, `{{< learn >}}` with numbered `### #.#.# -` sections,
   `{{< tryit >}}`, `{{< talk >}}` (a `.frames` list of sentence starters on
   the lesson's own topic), then `{{< further >}}`. A `{{< watch >}}` section
   only for a video that passes the video rule (Links, Videos and Tools)

- **The Big Question is a bookend, not a theme.** "Is AI like a human
  brain?" is asked in 1.1 (students write an answer Mr. Ross keeps) and asked
  again in 6.6, the last lesson. Nothing in between is organized around it;
  no unit is devoted to it, and lessons do not end with it. The brain
  comparison comes up only where the content raises it (Unit 2).
  `{{< bigq >}}` and `.big-question` belong to 1.1 and 6.6 only
- **Ethics and possible futures matter to these students.** Each Talk About
  It can raise the ethics of its own topic. Unit 6 holds the hidden costs,
  the rules, and possible futures. Present real disagreement among experts
  evenhandedly, without doom and without hype, and end on what a student
  can do
- **Labs scale from 4 to 18 students.** Class size swings day to day. Give
  every group activity a size range ("groups of 3 or 4"), say how roles
  double up when the class is tiny (4 students may be one group), and how a
  big class splits (several groups, or two teams that race). A physical
  activity that needs N people must work with 4 and say what extra people do. Class-size notes go in a `.teacher` block (see Reader first)
- **Famous experiments, acted out.** The teacher wants classic experiments
  and thought experiments folded in where they fit, in a `.experiment`
  callout, with the class physically acting them out when possible: the
  Turing test (1.2), the Chinese Room (1.3, acted out in Klingon as "the Klingon Room": the teacher does not want a real language playing the unreadable one), Pavlov (2.3), Rule 30 and the Game of Life (2.1, the teacher worked at Wolfram
  Research), Clever Hans and the husky that was really a snow detector (4.2), the trolley problem and
  the Moral Machine (6.4), the paperclip maximizer (6.5), replacing a brain
  one neuron at a time (6.6)
- **Dated facts go in a box.** Anything that will go out of date (a model
  name, a law, a number of users) goes in a `.note` titled "Right now (fall
  2026)" so it is easy to find and update. History before 2026 does not need
  one
- **Course map and unit intro change with the lesson.** Writing a lesson
  means linking it in `course-map.qmd`, adding it under "Topics in This
  Unit" in its unit `index.qmd`, and adding it to `_quarto.yml`
- **The syllabus is part of the book** (`syllabus.qmd`, after the home page).
  Keep it current in the same change: unit names, weeks, lesson counts, what
  each unit does, tools, and the privacy and honesty rules. When this
  session can reach the claude.ai project, also refresh the project's copy
  (`claude/AI_and_You_syllabus.md`)
- **Sheet snippets live in `handouts/Unit_X/parts/`.** A `.tex` that a sheet
  `\input`s (a generated grid, say) must not sit next to the sheets: the
  build and the asset check treat every `handouts/Unit_X/*.tex` as a sheet
- **Unit 1 builds a class timeline.** Each history lesson's sheet ends with
  timeline cards to cut out and post on the wall
- **Lesson, handout and figures are one change.** The handout restates the
  page's activities. Handouts pull shared figures with `\fig{Unit_X/<name>}`
- **Keys are unlisted.** `<name>_KEY.pdf` is served beside the student PDF
  but nothing links to it. The URL is predictable on purpose
- **Reader first: teacher material stays off student pages.** Anything for
  the teacher (class-size logistics, prep, answers) goes in a
  `:::{.teacher title="..."}` block in the lesson source, with no nested
  divs inside. `scripts/strip-teacher.lua` removes it from student pages and
  the site search. `scripts/make-teacher-guide.py` (post-render) builds the
  unlisted guide at `/teacher/`: every lesson's teacher notes, sheets and
  keys, the dated boxes, and the outside websites. Nothing links to it
- **Blocked for students on the school network** (checked October 2026):
  youtube.com, youtube-nocookie.com, ytimg.com, lens.google.com, tineye.com.
  yout-ube.com is not blocked and needs no login, so students watch videos
  there at school. Embed every video with `{{< ytvideo VIDEO_ID title="..." >}}`
  (`_extensions/ytvideo`): it shows the privacy-mode player for home and an
  "At school" link to yout-ube.com. Quarto's own `{{< video >}}` rewrites
  YouTube addresses to youtube.com: never use it. Link single videos only,
  never a YouTube home or channel page (the district does not want students
  browsing YouTube). If yout-ube.com is ever blocked, videos become a
  projector demo. No student step may need a blocked site
- **Outside websites:** `scripts/list-external-urls.py` lists every one. When
  links change, republish the firewall checklist artifact
  (https://claude.ai/artifact/6zYejQfNhQbDTe8d6tQovi) from that list
- **Home-language parts of a sheet carry `\ELL`**, plus what a student whose
  first language is English does instead (skip it, or use a partner's
  language)
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
| `.big-question` | The bookend question, 1.1 and 6.6 only; `[text]{.bq}` is the large line (pink) |
| `.project` | A Go Further project idea (indigo) |
| `.experiment` | A famous experiment or thought experiment, acted out when possible (brown) |

Syntax: `:::{.callout-type title="Title"} … :::`. New types need an entry in
`scripts/custom-callouts.js` and styles in `styles/ai-and-you.css`.

## Links, Videos and Tools
- **Fetch every link before it goes in.** Tools and videos disappear. A
  dead link in front of a class costs the block
- **Videos: skip them in most lessons.** A video that says what AI can or
  cannot do goes out of date fast, and nobody can edit it (the TED-Ed Turing
  test video said chatbots cannot fool people). Use one only when it cannot go
  stale: history told by the people who were there, with its year on the page
  (Conway in 2.1, Fei-Fei Li's 2015 talk in 1.5); how AI worked at a date,
  with that year in the title and a line that details may have changed
  (3Blue1Brown's 2024 chatbot video in 2.9); or a skill that does not depend
  on AI (lateral reading in 3.4). Embed with
  `{{< ytvideo VIDEO_ID title="..." >}}` inside a `.watch` callout, and keep
  the caption/auto-translate tip
- **Tools students open:** prefer ones that need no account (Quick, Draw!,
  Teachable Machine). Anything that needs a student account must be allowed
  under the district's AI Use Plan; Claude.ai and ChatGPT have age limits.
  "Your class AI tool" covers whatever students have (likely MagicSchool)
- **Privacy:** when a tool saves what students make, say so in a `.gotcha`
  next to the activity (see Quick, Draw! in 1.1)
- **No personal information in any AI tool, ever.** Never ask or let a
  student type or upload names (their own, classmates', family's,
  teachers'), pictures or recordings of themselves or other people,
  addresses, phone numbers, birthdays, student numbers, or private family or
  health details. Prompts use stand-ins ("my grandmother", "Student Name").
  Camera activities show hands and objects, never faces. Writing that goes
  into a tool is about a topic, not about the student
- **No phones in class.** Missouri law bans phones in the classroom. Any
  step that uses a phone says to try it at home ("Try it at home: ..."). In
  class, students use Chromebooks
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
- **First draft (fall 2026): squash each finished unit into `main` without
  asking.** The teacher reads the lessons on the site anyway. Deleting
  branches is still his

Things that bite:

- **Deploying is not merging.** `deploy.sh` force-pushes the built `_book` to
  `gh-pages` and touches nothing else, so a change can be live on the site
  while its source exists only on a feature branch. Check
  `git rev-list --count origin/main..HEAD` before assuming work is safe
- **A squash or checkout makes built files look stale.** Git rewrites the
  files with new timestamps, so `check-site-assets.py` may call a PDF or SVG
  stale when it is not. If the sources did not change since the build,
  `touch handouts/Unit_*/*.pdf images/Unit_*/*.svg`; otherwise rebuild
- **An interrupted deploy leaves a worktree behind.** The next `deploy.sh`
  dies with "'gh-pages' is already used by worktree". Fix with
  `git worktree list`, then `git worktree remove --force <path>`
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
- **Talk to the reader.** The book is written to the student, as "you".
  Never "for students who ..." or "students should ..." when the reader is
  meant ("Read it on your own, if you want to learn more"). Third person is
  fine for roles in a group activity ("one student is the robot")
- **Lead with the concrete.** A picture, a game, or a story first; the idea
  after. The cat rule in 1.1.2 is the pattern to copy
- **Say what is true.** No "AI thinks" or "AI knows" as plain fact. Whether
  AI is like a brain is the question the class is asking, so the book does
  not answer it in passing

## Curriculum Judgment

**Scope decisions are the teacher's.** He spent fifteen years in AI and data
science before teaching. He removed the original first and last units (the
brain question as whole units) and cut the plan from 60 lessons to 37, then added 2.1 (simple rules, complex behavior). Do
not propose cutting or adding lessons; report what you find and let him
decide.
