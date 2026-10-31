# Design reconciliation: 16 Oct proposal versus 26 Oct team guide

**31 October 2026 update:** The owner selected a hybrid, constraint-aware design under D01. See [hybrid-design-direction.md](hybrid-design-direction.md) for the complete direction and decision status. It supersedes the earlier guide-governs assumption. Detailed sections below await reconciliation after D04, D05, D03 and D02; they must not be treated as the final agreed design.

**Status: DECISION-NEEDED (user and team to confirm).** The supervisor session decided, in the user's absence, that the later team document governs where the two conflict. The drafts in this folder follow that decision.

| Document | Date | Where it is kept | Role in the drafts |
|---|---|---|---|
| `AI_Request_Router_Proposal.docx` ("the proposal") | 16 Oct 2026, short form | `../AI_Request_Router_Proposal.docx` | Record of the old plan. Its verified facts stay in `00-source-facts.md` unchanged. Elements the guide does not contradict are kept. |
| "LLM Router FYP: Architecture, Research Decisions and Experiment Guide", Rev 2 ("the guide") | 26 Oct 2026 | `../Research Review/Research Paper Review.docx`, summarised in `team-design-guide-notes.md` | **Governs** the design, objectives, research questions, experiments and evaluation. |

**Rule used in the drafts.** (1) Where the guide and the proposal conflict, follow the guide. (2) Keep proposal elements the guide does not contradict: an OpenAI-compatible gateway, hosted plus self-hosted backends, failover with a circuit breaker, p95 latency reporting, RouterBench, and the always-strong and always-weak baselines. (3) Mark every unresolved conflict `DECISION-NEEDED`. (4) Carry live-load signals as an **optional extension** (registry health, latency and queue estimates; vLLM `/metrics` only when exposed), not a core dependency.

Marker for unresolved items in the drafts: `DECISION-NEEDED: <short question>`.

## 1. Conflict table

| # | Item | 16 Oct proposal | 26 Oct guide | What the drafts follow | Question for the team |
|---|---|---|---|---|---|
| 1 | Framing and contribution | Router that picks the best model by cost, quality and latency; the difference from existing tools is the combination of per-prompt choice, live load, self-hosted serving and failover | A budget-constrained, load- and budget-aware gateway for hosted and local models. The contribution is architectural integration plus controlled evaluation, not a new routing method. Negative results are valid. | **Guide.** The proposal's sentence that no tool combines per-prompt choice, live load and self-hosted serving is dropped (the literature review found it is no longer safe). | `DECISION-NEEDED`: confirm the framing and that rejecting a hypothesis is an acceptable outcome for the supervisor. |
| 2 | Quality prediction | sentence-transformers features with a scikit-learn logistic-regression classifier for difficulty and task type | k-NN over past per-model outcomes of scored tasks (competence estimate); a learned difficulty classifier is an optional comparator, not an MVP dependency | **Guide.** The classifier appears only as an optional comparator arm in E1. ASSUMPTION: the k-NN embeddings come from a sentence-transformers model (the proposal's tool). | `DECISION-NEEDED`: which embedding model; keep the optional classifier arm or drop it. |
| 3 | Live load | Core feature: queue length, GPU use and tokens per second from vLLM through Prometheus into the score | Health, latency and queue **estimates** kept in the registry; vLLM `/metrics` used only when a server exposes it; no Prometheus in the MVP | **Guide.** Live load is an optional extension (objective-free, tested only if time allows). The "load-aware versus load-blind" comparison from the proposal moves to the extension. | `DECISION-NEEDED`: is the live-load extension still wanted as a stated goal, or dropped? It changes the title and the headline contribution. |
| 4 | Stack: Redis, Prometheus, Grafana | FastAPI, Redis for shared health state, Prometheus for metrics, Grafana for dashboards | One modular FastAPI application and a relational database; no Redis, graph database or microservices until a measured need | **Guide.** Health state lives in the application and database. Dashboards become CSV or a basic export. | `DECISION-NEEDED`: SQLite or a server database; whether any dashboard is a deliverable. |
| 5 | Failover | Retry on the next-best backend plus a circuit breaker with shared health state in Redis | Bounded retries and a circuit breaker, tested by fault injection (E4, E5); never continue a started stream on another model; never bypass privacy rules by falling back to a free local model | **Guide for state and rules; proposal for the pattern.** | `DECISION-NEEDED`: circuit-breaker thresholds, cool-down and maximum attempts (still unset). |
| 6 | Budget | Optional per-request latency budget in the score | Three cost budget bands (Economy, Balanced, Quality) with request, session and project caps; atomic reservation before dispatch; reconciliation with provider usage. TTFT is measured, not a request parameter. | **Guide for cost budgets (core).** The proposal's per-request latency budget is kept only as a Could requirement (FR-23) because the guide does not contradict it. | `DECISION-NEEDED`: keep or drop the per-request latency budget. |
| 7 | Benchmarks | RouterBench and MT-Bench | RouterBench and LLMRouterBench for E1; LongMemEval for E3 | **Guide.** MT-Bench is kept only as an optional quality check for open-ended outputs in E2 (ASSUMPTION). | `DECISION-NEEDED`: is MT-Bench still used? Which dataset licences and model coverage apply? |
| 8 | Baselines | Always-strong, always-weak; load-blind router | Static cheapest eligible; domain-average rule; k-NN; optional classifier; fixed, per-turn and hysteresis switching policies; full replay, bounded, retrieval and graph context builders | **Union.** Always-strong and always-weak are kept as references in E1. | None; confirm that always-strong and always-weak are worth keeping next to the rule baselines. |
| 9 | Phases and order | Three phases: gateway and classifier; resilience and load awareness; benchmarking | Nine-step build order (requirements first; proxy and adapters; registry and filters; budget ledger; rule router; k-NN router; managed sessions and hysteresis; reliability and quality evaluation; usability evaluation) | **Guide.** Phase dates stay TODO. | `DECISION-NEEDED`: calendar dates for the nine steps. |
| 10 | Candidate models | Not specified | 3 to 4 differentiated models or deployments | **Guide.** Which models stay TODO. | TODO: the actual three or four models, with versions and evaluation labels fixed. |
| 11 | Success measures | Cost versus quality against single-model baselines; latency including p95; routing accuracy; numeric targets "not set yet" | Declare the primary metric and a non-inferiority margin before looking at results; paired comparisons with 95% intervals; calibration (reliability table, Brier score); budget correctness; gateway overhead; ISO/IEC 25010 targets set from requirements | **Guide.** "Routing accuracy" is replaced by success at matched cost and calibration; p95 and TTFT are kept (E2, E5). Margins and targets remain TODO. | `DECISION-NEEDED`: primary metric and margin for E1 and E2 (the guide says a 3-point figure is only a placeholder); supervisor approval. |
| 12 | Software-engineering evaluation | Not in the proposal. The template's usability section was an open question. | Requirements from at least 5 developer interviews or surveys; MoSCoW and a traceability matrix; ISO/IEC 25010 quality table (four characteristics); at least 80% line coverage; SUS with preferably at least 8 participants | **Guide.** This resolves the earlier open question: a usability study is required. | `DECISION-NEEDED`: consent approach and whether department ethics approval is needed for interviews and the SUS study; which edition of ISO/IEC 25010. |
| 13 | Conversation context and switching | Absent | Session-aware hysteresis (E2); client owns context by default, optional router-managed sessions; context policies C0 to C3b (E3); graph memory deferred and optional | **Guide.** Graph arms (C3a, C3b) are optional and conditional. | `DECISION-NEEDED`: go or no-go for the graph arms; whether managed sessions are in the MVP. |
| 14 | Scope exclusions | Out of scope: building or training the language models | Out of scope: training or fine-tuning, KV-cache transfer across models, distributed GPU scheduling, managing engine installation, online RL or bandit exploration, a general agent framework, LLM-built graphs on every live request | **Union.** | None. |
| 15 | Backends | Hosted APIs, Ollama, vLLM | Local models first class through OpenAI-compatible APIs (Ollama, LM Studio, llama.cpp server, vLLM); hosted APIs; a generic adapter | **Guide**, which includes the proposal's backends. | `DECISION-NEEDED`: which local engines the MVP actually supports. |
| 16 | Hypotheses | None stated; numeric targets to be agreed | H1 to H3 (confirmatory), with E4 and E5 descriptive; exploratory ablations labelled as such | **Guide.** | Confirm that only H1 to H3 are confirmatory. |
| 17 | Title | Options centred on live load and failover | Not set. The guide's wording suggests "budget-aware" and "prompt-aware" | **New title options** in `front-matter.md`; the old ones are kept as superseded. | `DECISION-NEEDED`: pick a title. |
| 18 | Risks | R-01 generalisation, R-02 noisy labels, R-03 little prior work on live-load routing, R-04 competitors moving | The guide's risks (calibration of k-NN scores, thin evidence, caching and cold starts, graph extraction cost, extraction errors) | **Both**, re-mapped: R-03 becomes secondary. | None. |
| 19 | Evidence status of cited work | Names only, "exact authors, years and links still need to be checked" | Sources labelled by type; the guide's own relevance and limitation summaries "were not re-read against full texts" | The literature-review files do the checking. Drafts cite the review's verified entries. Three papers new to the guide (EACL past-performance retrieval, MTRouter, VDAR-Router) have review files in topic 09 but are not yet in `references.md`; they are cited as `[CITE-09]`. Topic 10 (memory) does not yet exist; `[CITE-10]`. | Chase when topics 09 and 10 are complete. |
| 20 | Which document governs | The proposal was the main fact source | The guide is later (26 Oct) and says it refines the architecture | **Guide governs** by the supervisor's decision. | `DECISION-NEEDED`: the user confirms this. |

## 2. What stays from the proposal (not contradicted)

- Project identity: an AI request router for LLM requests (it is still a working assumption whether this is the confirmed topic; see `00-source-facts.md` M-06 and the "Adaptive LMS" note).
- One OpenAI-compatible endpoint in front of hosted and self-hosted backends.
- Failover with a circuit breaker.
- p95 latency (now with TTFT) and cost versus quality against single-model baselines.
- Always-strong and always-weak baselines; RouterBench.
- Out of scope: building or training language models.
- Team, supervisor, dates and numeric targets remain unknown.

## 3. How the old plan maps onto the new one

| Proposal phase or feature | Where it sits now |
|---|---|
| Phase 1 gateway and classifier | Build steps 2 to 6 (proxy and adapters, registry and filters, budget ledger, rule router, k-NN router); classifier is an optional comparator |
| Phase 2 resilience and load awareness | Build step 8 (fault injection, E4, E5); live signals are the optional extension |
| Phase 3 benchmarking | E1 (RouterBench, LLMRouterBench), E2, E3 |
| Scoring function over quality, cost, latency | Selection rule: lowest expected cost among eligible models whose competence lower bound meets the target (Section 3.6 of Chapter 3) |
| Circuit breaker and Redis state | Circuit breaker kept; Redis removed until a measured need |
| Grafana dashboards | CSV or basic export (DECISION-NEEDED) |

## 4. Where each decision shows up in the drafts

| Draft | What changed |
|---|---|
| `ch1-introduction.md` | New aim, six objectives, RQ1 to RQ3 plus RQ4 to RQ6, hypotheses H1 to H3, new problem statement and gap wording |
| `ch2-literature-review.md` | Two extra themes (2.4.9, 2.4.10); gaps table re-mapped to the new objectives; live-load gap marked secondary |
| `ch3-methodology-design.md` | Requirements, architecture, eligibility filter, competence estimate with lower bound, budget ledger, hysteresis, experiments E1 to E5, software-engineering evaluation plan |
| `ch4-ch5-skeletons.md` | Empty result tables for E1 to E5 and the software-engineering evaluation |
| `front-matter.md` | New title options, objectives mapping, list of tables |
| `00-source-facts.md` | **Unchanged**: the record of the 16 Oct plan |
