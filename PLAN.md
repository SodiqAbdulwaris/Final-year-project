# Work Plan: AI Request Router Literature Review and Proposal Drafts

Status: **draft, waiting for confirmation**. Nothing below has been started except reading your files.

## 1. What I found in your files

| File | What it tells me |
|---|---|
| Final-year template (.docx) | Chapters 1–5 structure. Ch. 2 needs **≥25 related works in depth, ≥70% from the last 5 years, ≥40 references, APA 7th with DOIs**, Table 2.1 (search strategy), Table 2.3 (summary of works), Table 2.4 (gap → objective). Proposal uses future tense. Aim + 4–6 SMART objectives, one RQ per objective. |
| Scopus manuscript template | Optional later. Same content re-cut as a journal paper (Related Work, Methods, RQs, Declarations). |
| Research Methodology pptx (Module 1) | Problem-driven, not topic-driven. Problem = gap between *what is* and *what ought to be*. SMART objectives, H0/H1, replicability. I will word problem statement and objectives to match this. |
| Reading list PDF | 8 topics, ~60 distinct papers, tagged ✓ (confirmed) or † (unverified). |
| `My Research/` | Your Topic 1 notes (`AI Model Routing Algorithms.md`, **88 KB**, 10 papers), plus two reference files. I will mine these for content and ideas, then split and clean. |
| Other folders (`Rejected/`, `Research Review/`, `Team Briefs/`, `.qodo/`) | Not part of this task. **I will not touch them.** |

## 2. Rules for every paper

1. Published **2020 or later** (anything older is dropped).
2. **≥8 papers per topic, each with its own fully documented file.** A paper that belongs to several topics is documented once, in its home topic. Other topics link to it, and link-only entries do **not** count toward the 8.
3. Unreachable, unverifiable or too-old papers are dropped and replaced with better ones found by search (Google Scholar, arXiv, ACL Anthology, ACM, IEEE, Semantic Scholar).
4. Prefer the **peer-reviewed version** (venue, DOI) over the arXiv preprint. Each file states which: *peer-reviewed* / *preprint only*. This matters because the template asks for mainly peer-reviewed sources.
5. **Full text read** wherever obtainable. Each file says `full text` or `abstract only`. Abstract-only papers are used only when nothing better exists.
6. **APA 7th** citation in every paper file, with DOI (arXiv DOI `10.48550/arXiv.<id>` if no venue DOI). Every number quoted in a file is checked against the paper.
7. No blogs or Wikipedia as sources. Vendor docs (OpenRouter, LiteLLM, Portkey, TrueFoundry, Martian) go in a separate `competitors/` folder, labelled grey literature.

## 3. Folder layout (in `Final year project/`)

```
literature-review/
├── README.md                 master index, paper table, how to use
├── 00-project-context.md     proposal in brief + the questions papers must help answer
├── cross-reference.md        paper × topic matrix
├── gaps-and-synthesis.md     what the literature shows, gaps, mapped to objectives
├── references.md             master APA 7 list, alphabetical, DOIs
├── _templates/paper-template.md
├── 01-routing-algorithms/    00-overview.md + one file per paper
├── 02-prompt-difficulty/
├── 03-load-balancing/
├── 04-cost-reduction/
├── 05-latency-and-speed/
├── 06-error-handling-fallback/
├── 07-testing-and-benchmarking/
├── 08-system-design-gateway/
└── competitors/              OpenRouter, LiteLLM, Martian, Portkey, TrueFoundry (feeds Table 2.2)

proposal-drafts/
├── 00-source-facts.md        every fact already in your proposal, with what is still TBD
├── front-matter.md           title, declarations, AI-use table, abbreviations (names/IDs left as TODO)
├── ch1-introduction.md       1.1–1.11, problem statement as what-is / ought-to-be / gap
├── ch2-literature-review.md  2.1 search strategy (Table 2.1), 2.3 techniques, 2.4 themes, 2.6–2.8 tables
├── ch3-methodology-design.md requirements (FR/NFR tables), architecture, algorithm design, tools, evaluation plan, ethics
├── ch4-ch5-skeletons.md      evaluation plan carried forward, empty result tables to fill later
└── manuscript-outline.md     OPTIONAL Scopus-style outline (only if you want it)
```

Each **paper file** (~600–900 words, columns match template Table 2.3):
citation (APA) and verification status · what it is about · problem · proposed solution · data/tools · key results (with numbers) · limitations · relevance to the router (which proposal feature or risk it supports) · how to cite it in Ch. 2 · open questions.

Each **topic overview**: how the topic fits the project, comparison table of the papers, themes and trends, strongest papers for the proposal, links to files, and one-line pointers to related papers living in other topics.

## 4. Who does what

I stay the **supervisor**. Workers are separate sessions I can message; each reports back briefly, and the findings live in files, not in chat. Workers run in this same folder (it is not a git repo). Each writes only to its own folder, so nothing collides.

| Wave | Session | Owns | Notes |
|---|---|---|---|
| A | T1 Routing algorithms | `01-…/` | Starts from your existing notes. Verify against sources, upgrade to published citations, split into per-paper files. |
| A | T2 Prompt difficulty | `02-…/` | Reading list has ~9 usable. Drops pre-2020 or vague entries (e.g. Zotos) and replaces if needed. |
| A | T3 Load balancing | `03-…/` | |
| A | T4 Cost reduction | `04-…/` | Only ~5 papers are exclusive to it. Finds ≥3 more. |
| A | P Proposal drafts | `proposal-drafts/` | Uses the proposal, templates and pptx. Ch. 2 filled in at the end. |
| B | T5 Latency | `05-…/` | |
| B | T6 Fallback | `06-…/` | Sparse area. Finds extras (failover, circuit breaker, retry research). |
| B | T7 Benchmarking | `07-…/` | |
| B | T8 Gateway design | `08-…/` | Finds extras (inference-gateway and serving-orchestration papers). |
| B | C Competitors | `competitors/` | Re-checks LiteLLM and OpenRouter docs, as your proposal's risk table asks. |

Waves limit parallel load. If limits allow, B starts while A is still finishing.

Phases: **0** scaffold + template + ownership table (me) → **1** wave A → **2** wave B → **3** my review → **4** my synthesis → **5** cleanup.

## 5. My review (before anything is called done)

- Count files per topic (≥8 owned), check year ≥2020, APA format, DOI present.
- Spot-check ≥2 papers per topic against the actual source (numbers, limitations).
- Reject and send back anything thin, abstract-only without reason, or suspicious. Workers get a second pass via message.
- Failures are reported honestly in the final summary (anything I could not verify is flagged, not hidden).

## 6. Synthesis files (written by me last)

`README.md`, `cross-reference.md`, `references.md` (merged, deduplicated, alphabetical APA), `gaps-and-synthesis.md` (gaps from the proposal: runtime-aware routing, generalisation, label noise, competitors — checked against what the papers actually say, mapped to objectives), then the Ch. 2 tables in `proposal-drafts/`.

## 7. Cleanup of `My Research/`

1. Extract anything useful from `AI Model Routing Algorithms.md` and the two `Ref …` files into the new paper files and references.
2. Move the originals to `My Research/_archive/` (nothing is deleted).
3. Leave `My Research/` pointing to `literature-review/` with a short `README.md`.
4. You can delete `_archive/` yourself when satisfied.

## 8. What I will not do

- Invent team names, student IDs, supervisor, numeric targets, or results. These stay as `TODO` in the drafts.
- Treat unread papers as read. Abstract-only is labelled.
- Change your proposal `.docx` or the templates.
- Touch other folders or push anything anywhere.

## 9. Things that can go wrong while you are away

- A worker hits a permission prompt and stalls. I will check on sessions and reply or restart.
- Site blocks or paywalls: I drop and replace the paper, not guess.
- Some 2026 preprints may be unreadable or revised. They are replaced or flagged.

## 10. Expected output

~64+ paper files, 8 topic overviews, competitors folder (5 files), 7 proposal-draft files, and the 5 synthesis files. Every section meets the ≥8 target, or I tell you exactly which does not and why.
