# Worker brief (read fully before starting)

You are a worker for the supervisor session on a literature review for a final-year project, the **AI Request Router** (Nile University of Nigeria, Software Engineering). The supervisor reviews your output and may message you for fixes.

## The project in brief
A gateway that scores each LLM request for difficulty, weighs predicted quality, cost and **live load** on every backend, and routes it to the best model (hosted or self-hosted), with failover. Planned stack: sentence-transformers + scikit-learn classifier, vLLM/Ollama, FastAPI, Prometheus, Redis, circuit breaker, benchmarks RouterBench and MT-Bench. Out of scope: training LLMs. Gaps the project claims: per-prompt model choice + live load + latency budgets + self-hosted serving together. Full text: `../../AI_Request_Router_Proposal.docx` (extract text with python zipfile if needed) and `../../PLAN.md`.

## Hard rules
1. **Published 2020 or later.** Drop anything older.
2. **At least 8 papers with their own complete file in your topic folder.** Cross-listed papers owned by another topic do not count; link to them instead (ownership table below).
3. If a listed paper is unreachable, unverifiable, too old or too thin, **drop it and find a replacement** (arXiv, ACL Anthology, ACM DL, IEEE Xplore, Semantic Scholar, Google Scholar, publisher pages). Prefer peer-reviewed venues. Record dropped papers and why in your overview file.
4. **Read the full text** where obtainable (arXiv PDF/HTML; pypdf is installed: `python -I -c "import pypdf"`; download PDFs into your own new folder in the scratchpad or `%TEMP%`, never into the project). If only the abstract is readable, say so in the file and prefer a replacement.
5. Verify title, authors, year, venue and DOI from the publisher or arXiv page. Never copy metadata from memory. Every number in a file must be checked against the paper. Do not invent results. If unsure, write "not stated" or "could not verify".
6. **APA 7th** reference in every file, with DOI (arXiv: `https://doi.org/10.48550/arXiv.<id>`; use the published venue's DOI when the paper has been published). Sentence case titles, journal/proceedings in italics.
7. Use `../_templates/paper-template.md` exactly. 600–900 words per paper file. No padding, no copied paragraphs from the papers (paraphrase; at most one short quote under 15 words per file).
8. File names: `<firstauthor>-<year>-<keyword>.md`, lowercase, hyphens.
9. Write only inside your own folder. Do not edit shared files or other folders. Do not touch anything outside `literature-review/<your folder>/` (or `proposal-drafts/` if that is your job).
10. If blocked (a site refuses, a tool prompts), try an alternative source. Browser tools (`mcp__Claude_Browser__*`, Claude in Chrome) are available. If still blocked, message the supervisor (name `supervisor`, use SendMessage to the session that started you) with the exact problem; do not stall silently.

## Topic overview file (`00-overview.md`) must contain
- Topic definition and why it matters to the router (3–6 sentences).
- Comparison table of all papers (year, type, venue, problem, method, key result, limitation).
- Themes/trends and how papers relate (synthesis, not summary).
- Strongest 3 papers for the proposal and why.
- Gaps visible in this topic (feeds the project gap statement) with paper evidence.
- Link list to every paper file (relative links), plus a "Related papers documented elsewhere" list with links.
- Search log: databases, search strings, date, counts found/screened/included, dropped papers with reason (this feeds Table 2.1).

## Ownership of papers shared between topics
Home topic gets the full file. Others link to it.
- FrugalGPT, RouteLLM, Hybrid LLM, AutoMix, LLM-Blender, Zooter, RouterDC, Shnitzer (benchmark routing), Varangot-Reille survey, Moslem & Kelleher survey → **01**
- Routoo, Chuang confidence tokens, Zhu hidden-state difficulty, Zhao difficulty prediction, Q-DAPS, FamiCom, MoPPS, Zotos, Kadavath → **02**
- Llumnix, Jain Microsoft intelligent router, Kossmann, L4, SLOs-Serve, GORGO, SkyWalker, Mooncake, Multi-tier SLA, Preble → **03**
- Dekoninck unified routing/cascading, Yue cascades, Gupta cascades, EcoAssistant, LLMLingua → **04**
- vLLM/PagedAttention, Orca, Sarathi-Serve, DistServe, Splitwise, POD-Attention, Vidur, Etalon, Niyama, speculative decoding → **05**
- ContinuityBench, SpotServe, DéjàVu (+ extras) → **06**
- RouterBench, RouterEval, LLMRouterBench, RouterArena, EmbedLLM, FusionFactory, MT-Bench/Chatbot Arena, HELM → **07**
- SGLang, Miao serving survey, AIBrix (+ extras) → **08**

Drop any paper dated before 2020 (the list is mostly 2022+).

## Report back
When finished, send the supervisor a **short** message: files written, count of full files, papers dropped/added, anything unverified, anything you need. Details live in the files.
