Status: DRAFT
Depends on: Original proposal record; decisions-applied.md
Sources: AI_Request_Router_Proposal.docx, historical extraction
Open items: Historical record only; current decisions supersede older unknowns; not independently re-extracted in this session

# 00 Source facts: AI Request Router

Every fact in `AI_Request_Router_Proposal.docx` (draft of 16 October 2026), tagged by how far it can be trusted. All other draft files in this folder may use only what is listed here. Anything not listed is either marked `ASSUMPTION:` where it is used or left as `TODO`.

**Legend**

| Tag | Meaning |
|---|---|
| KNOWN | The proposal states it as the project plan or design. Safe to build on. |
| VERIFY | A claim about a third party (a product, a paper, a benchmark). It comes from the proposal, but the proposal itself says exact details still need checking. Do not cite it as fact until the source is re-read. |
| TBD | The proposal says it is not decided, or does not say. Left as `TODO` in the drafts. |

Other markers used across the drafts: `TODO:` (team must supply), `TODO-confirm-with-supervisor:` (needs a supervisor decision), `[CITE: topic]` (citation needed, source not yet verified), `ASSUMPTION:` (a choice made by the drafter, not stated in any source document).

---

## 1. Document metadata

| ID | Fact | Tag |
|---|---|---|
| M-01 | Document: "PROJECT PROPOSAL (SHORT FORM)", title "AI Request Router". | KNOWN |
| M-02 | Institution: Nile University of Nigeria, Department of Software Engineering. | KNOWN |
| M-03 | Draft dated 16 October 2026. Footer reads "Final Year Project, Proposal". | KNOWN |
| M-04 | Team and supervisor: "to be confirmed". No names, student IDs or supervisor named anywhere. | TBD |
| M-05 | One-sentence summary: a gateway that scores each request for difficulty, weighs predicted quality, cost and the live load on every backend, and sends it to the best model, hosted or self-hosted, with failover. | KNOWN |
| M-06 | A boxed "working assumption": the router is a layer that sends each incoming LLM request to the best model by cost, quality and latency, with the note "Adjust if the project is something else." So the project identity itself is a working assumption, not a confirmed topic. | TBD |
| M-07 | A "Review: Adaptive LMS and AI Request Router (project document, October 2026)" is cited as a literature source. That document was not among the files given for this task. | TBD |

## 2. The problem (proposal section 1)

| ID | Fact | Tag |
|---|---|---|
| P-01 | Teams often hard-code a single model. | KNOWN |
| P-02 | Sending every request to one large model wastes money. | KNOWN |
| P-03 | Sending everything to a small model hurts quality. | KNOWN |
| P-04 | Hard-coding also brings latency spikes and no failover. | KNOWN |
| P-05 | Existing routers mostly optimise cost and quality offline. | VERIFY |
| P-06 | Few existing routers handle live load, latency budgets and self-hosted model serving together. | VERIFY |
| P-07 | Target users: developers and organisations running more than one LLM. | KNOWN |
| P-08 | No quantified evidence (costs, latency figures, survey results, Nigerian-context statistics) is given anywhere in the proposal. | TBD |

## 3. Existing solutions and their drawbacks (proposal section 2)

General claim (VERIFY): "In the documentation we reviewed, none picks the model per prompt, watches live load, and also runs on your own GPUs." Each tool "solves one slice".

| ID | Solution | Does well (as stated) | Drawback (as stated) | Tag |
|---|---|---|---|---|
| S-01 | OpenRouter | One API to many hosted providers, with fallbacks and uptime-aware balancing. | Chooses between providers of the model you name, not between models. By default avoids providers with recent outages, then favours lower price. Latency and throughput come from rolling 5-minute statistics, so a sudden queue build-up shows up late. Setting a sort order turns load balancing off. Routing docs cover listed providers and your own provider keys, not self-hosted GPUs. | VERIFY |
| S-02 | LiteLLM Router and Auto Router | Router balances across your own deployments with latency-based, least-busy and cost-based strategies, plus fallbacks. Auto Router (beta, 2026) sorts each request into a complexity tier and maps tiers to models. | Core Router spreads traffic across copies of the model the caller names, so easy and hard questions go to the same model. Its usage-based strategy adds latency from Redis tracking and is "not recommended for production". The Auto Router docs reviewed do not mention live load, queue depth, GPU use or per-request latency budgets. | VERIFY |
| S-03 | RouteLLM | Learns to pick between one strong and one weak model from preference data. | A research framework: two models only, no live load, latency budget or failover. | VERIFY |
| S-04 | FrugalGPT-style cascades | Try the cheap model first and escalate if the answer looks weak. | A hard question pays the latency of every failed attempt before the right model answers. | VERIFY |
| S-05 | Commercial routers (for example Martian) | Managed routing without running your own. | Closed. "As far as we know" the routing rules cannot be inspected and the router cannot run on your own infrastructure. | VERIFY |

## 4. The planned solution (proposal section 3)

Each feature answers one gap. Tools are exactly as named in the proposal.

| ID | Gap (what is missing) | What the team builds | Built with | Tag |
|---|---|---|---|---|
| D-01 | Same model for easy and hard prompts | Scores each prompt for difficulty and task type before choosing a model. | sentence-transformers (text to vectors) and scikit-learn logistic regression (small, fast classifier) | KNOWN |
| D-02 | Load seen late or not at all | Reads live queue length, GPU use and tokens per second from each self-hosted server and avoids busy ones. | vLLM and Prometheus | KNOWN |
| D-03 | No self-hosted backends | Puts hosted APIs and own GPU servers behind one OpenAI-compatible endpoint. | vLLM, Ollama, FastAPI (async gateway) | KNOWN |
| D-04 | Price-only or quality-only decisions | Combines predicted quality, cost and latency into one score and honours a per-request latency budget. | Custom scoring function in Python | KNOWN |
| D-05 | Failures and slow providers | Retries on the next-best backend and temporarily stops sending traffic to one that keeps failing. | Redis (shared health state) and a circuit-breaker pattern | KNOWN |
| D-06 | Cascade latency | Decides before calling, in one hop, instead of trying models in sequence. | The same classifier, run before the request is sent | KNOWN |
| D-07 | Unproven savings | Plots cost against quality and p95 latency (the time 95% of requests beat) versus always-strong and always-weak baselines. | RouterBench and MT-Bench (public benchmarks), Grafana (dashboards) | KNOWN |

### Figure 1 (request flow), read from the image and its alt text

| ID | Fact | Tag |
|---|---|---|
| F-01 | Title: "Each request is scored against live backend load before it is sent". Caption: every request passes the classifier and scoring engine once; live load from the self-hosted servers feeds the score before a backend is chosen. | KNOWN |
| F-02 | Flow, top to bottom: Client request (OpenAI-style call, optional latency budget) to Gateway (FastAPI, single endpoint for every client) to Prompt classifier (scores difficulty and task type) to Scoring engine (weighs quality, cost and latency) to one of three backends: Hosted APIs (pay-per-token providers), Ollama (local models), vLLM (self-hosted GPU server). | KNOWN |
| F-03 | Live state (Redis) holds queue length, GPU use, tokens/s (collected by Prometheus) and health and failure counts. It feeds the Scoring engine. An arrow runs from the vLLM box up to Live state. | KNOWN |
| F-04 | Footnote: if a backend fails, the router retries on the next-best one and pauses traffic to the failing one. | KNOWN |
| F-05 | How metrics get from Prometheus into Redis (a poller? the gateway?) is not stated. | TBD |

## 5. Scope and phasing (proposal section 4)

The proposal calls this "proposed order ... to be confirmed with the team".

| ID | Fact | Tag |
|---|---|---|
| SC-01 | Phase 1, gateway and classifier: one OpenAI-compatible endpoint over hosted and self-hosted backends, the prompt classifier, and the cost, quality and latency score. | KNOWN (order TBD) |
| SC-02 | Phase 2, resilience and load awareness: fallback with a circuit breaker, and live queue, GPU and throughput signals from vLLM through Prometheus. | KNOWN (order TBD) |
| SC-03 | Phase 3, benchmarking: compare against always-strong and always-weak baselines on RouterBench and MT-Bench. | KNOWN (order TBD) |
| SC-04 | Out of scope: building or training the language models. The router only chooses between existing ones. | KNOWN |
| SC-05 | Dates, durations, team allocation of phases. | TBD |

## 6. How success will be judged (proposal section 5)

| ID | Fact | Tag |
|---|---|---|
| E-01 | Numeric targets are not set. They will be agreed with the supervisor before testing. | TBD |
| E-02 | Measures: cost versus quality, against single-model baselines. | KNOWN |
| E-03 | Measures: latency, including p95. | KNOWN |
| E-04 | Measures: routing accuracy, "how often the classifier picks the right model". The meaning of "right model" is not defined. | TBD |

## 7. Risks and mitigations (proposal section 6)

| ID | Risk | Mitigation as stated | Tag |
|---|---|---|---|
| R-01 | Poor generalisation | Routers trained on one model pair generalise poorly. Test the classifier on more than one model pair using RouterBench before trusting it. | KNOWN (claim VERIFY) |
| R-02 | Noisy quality labels | Quality labels from preference data are noisy. Use public benchmarks and preference data; report uncertainty rather than a single number. | KNOWN (claim VERIFY) |
| R-03 | Little prior work on live-load routing | Runtime-aware routing is thin in the literature. Treat it as the project's gap and measure it directly against load-blind routing. | KNOWN (claim VERIFY) |
| R-04 | Competitors are moving | LiteLLM's Auto Router now routes by complexity, so the difference is the combination of live load, latency budgets and self-hosted serving. Re-check the LiteLLM and OpenRouter docs before submission. | KNOWN |

## 8. Sources named in the proposal

| ID | Source | Tag |
|---|---|---|
| SRC-01 | OpenRouter, provider routing | VERIFY (URL, access date missing) |
| SRC-02 | LiteLLM, routing and load balancing | VERIFY |
| SRC-03 | LiteLLM, Auto Router v2 (13 July 2026) | VERIFY |
| SRC-04 | LiteLLM, Auto Routing (beta) | VERIFY |
| SRC-05 | Methods (names only): FrugalGPT, RouteLLM, Hybrid LLM | VERIFY (authors, years, links "still need to be checked before citing") |
| SRC-06 | Systems (names only): OpenRouter, LiteLLM, Martian | VERIFY |
| SRC-07 | Benchmarks (names only): RouterBench, MT-Bench, Chatbot Arena | VERIFY |
| SRC-08 | Review: Adaptive LMS and AI Request Router (project document, October 2026) | TBD (not provided) |

## 9. Consolidated TBD register

Nothing in the drafts fills these in. They need an answer from the team or the supervisor.

| # | Unknown | Needed for |
|---|---|---|
| 1 | Team member names, student IDs, group leader, roles | Front matter, contributions table |
| 2 | Supervisor full name and title (template shows only "Dr. Supervisor") | Front matter |
| 3 | Is "AI Request Router" the confirmed topic (proposal calls it a working assumption)? | Everything |
| 4 | Academic session, submission month, phase dates | Front matter, SMART "time-bound" |
| 5 | Numeric targets for cost saving, quality loss, p95 latency, routing accuracy, overhead, availability | NFR table, hypotheses, Chapter 4 |
| 6 | Definition of "right model" for routing accuracy | Objective 3, Chapter 4 |
| 7 | Which models (the "strong" and "weak"), which hosted providers, which self-hosted models, how many model pairs | Design, evaluation |
| 8 | GPU hardware, budget for hosted API calls | Development environment |
| 9 | How live metrics flow from Prometheus to Redis | Architecture |
| 10 | RouterBench and MT-Bench details (size, models covered, licence, how quality is scored) | Section 3.7 |
| 11 | Authors, years, venues of FrugalGPT, RouteLLM, Hybrid LLM, RouterBench, MT-Bench, Chatbot Arena | Chapters 1 and 2 |
| 12 | Whether a user or usability study (template 4.5.5, SUS) is required for a gateway with no user interface | Evaluation plan |
| 13 | Whether department ethics approval is needed (no human participants are planned) | Section 3.10 |
| 14 | University AI-use policy wording for the generative-AI declaration | Front matter |
| 15 | Quantified evidence for the problem (price or latency measurements, a pilot, Nigerian-context data) | Section 1.1, 1.2 |
| 16 | Content of the "Adaptive LMS and AI Request Router" review document | Chapter 2 |

## 10. Rules from the other source documents that shape the drafts

| Source | Rule |
|---|---|
| Template | Follow the body numbering of each chapter (see section 11 below for a mismatch with its own contents list). Body text: Times New Roman 12 pt, 1.5 spacing, justified, first-line indent 0.5 inch. Future tense in the proposal; past tense in the final report. |
| Template, Ch. 1 | 6 to 10 pages. Problem statement in three parts (what is; what ought to be; gap and consequences), ending with "This project therefore seeks to ...". Aim plus four to six SMART objectives, each starting with an action verb and traceable to Chapter 3 or 4 and an evaluation result. One research question per objective, never yes/no. H0 and H1 in 1.4 or 3.9. |
| Template, Ch. 2 | 15 to 25 pages. At least 25 related works in depth, at least 70 percent from the last five years, at least 40 references, mainly peer-reviewed. Organise by theme, not paper by paper. Tables 2.1 to 2.4. APA 7th with DOIs. |
| Template, Ch. 3 | 15 to 25 pages. Requirements with IDs and MoSCoW; non-functional requirements measurable; algorithm with pseudocode, flowchart or equations; evaluation plan states metrics, baselines and hypotheses. |
| Template, Ch. 4 and 5 | Tables 4.1, 4.2, 5.1 as given. Report results in 4.6, interpret them only in 4.7. Do not introduce new results in Chapter 5. |
| Course module 1 | A research problem is the gap between what is and what ought to be. A topic or a technology is not a problem. Problem statement: social need (cited facts), knowledge gap, then "the problem of this study is to ...". Never invent statistics. SMART objectives with measurable verbs (determine, compare, investigate, establish, examine); avoid show, prove, confirm, verify, demonstrate, validate. One research question per objective (what / to what extent / how). Hypotheses: H0 (no relationship), H1 (non-directional or directional). Name IV, DV, extraneous or moderating variable, and the scale of measurement of each. Replicability: share code and data. |
| PLAN.md | Literature rules: papers from 2020 onward, peer-reviewed version preferred, APA 7th with DOI, vendor docs kept as grey literature in `competitors/`. Drafts must not invent team names, IDs, supervisor, numeric targets or results. |

## 11. Inconsistencies found in the source documents

1. The template's own contents list (front pages) uses older section numbers (for example 1.1 to 1.7 in Chapter 1; "3.1 System Analysis" in Chapter 3; Chapter 4 ends at 4.5). The body headings are fuller (1.1 to 1.11; 3.1 to 3.11; 4.1 to 4.9). **The drafts follow the body headings.**
2. The template uses "Figure 2.1" for both the PRISMA-style flow diagram (Section 2.1) and the conceptual framework (list of figures). The drafts call the PRISMA flow Figure 2.1 and the conceptual framework Figure 2.2. Confirm which numbering the department wants.
3. The template's SMART wording is Achievable and Relevant; the course module says Attainable and Realistic. The drafts use the template's.
4. The template's example objectives use "evaluate", which the course module does not list as an avoid-verb. Kept.
5. The proposal refers to "Adaptive LMS and AI Request Router" as one review document. Whether Adaptive LMS is a competing or sibling topic is unknown.
6. Folders `Team Briefs/` and `Research Review/` exist beside the proposal but were outside this task's source list and were not read. They may hold team names or the review document.
