# CHAPTER TWO: LITERATURE REVIEW (skeleton)

**Drafting notes (delete before pasting)**

- This file is a section skeleton and theme plan. It deliberately contains **no paper summaries and no citations to unverified work**. The supervisor fills the paper tables (Tables 2.3 and 2.4 evidence columns) from the verified notes in `literature-review/`, which other workers are writing.
- Template minimum standard: at least 25 related works reviewed in depth, at least 70 percent from the last five years, at least 40 references in total, mainly peer-reviewed. Target length 15 to 25 pages. Wikipedia, blogs and unpublished student projects are not acceptable as primary sources.
- Vendor documentation (OpenRouter, LiteLLM, Martian) is grey literature. It is used in Section 2.5 and cited as such, not counted toward the 25 papers.
- Marker meanings: `TODO:` (to fill), `[CITE: ...]` (needs a verified citation), `ASSUMPTION:` (drafter's choice), `[F-xx]` etc. (fact IDs from `00-source-facts.md`; delete when pasting).

---

Opening paragraph (write last, 3 to 5 lines): State that the chapter reviews the literature on routing LLM requests across models. It is organised into the search method (2.1), the concepts behind the project (2.2), the enabling techniques and technologies (2.3), related works by theme (2.4), existing systems (2.5), a summary table (2.6), the research gap (2.7) and a chapter summary (2.8). TODO: finalise once the content exists.

## 2.1 Review Methodology

The review will follow a documented search so that another person can repeat it. Table 2.1 is partly filled from the project documents; the rest is completed when the searches are run.

**Table 2.1: Literature search strategy**

| Item | Description |
|---|---|
| Databases | Planned in `PLAN.md`: Google Scholar, arXiv, ACL Anthology, ACM Digital Library, IEEE Xplore, Semantic Scholar. TODO: confirm which were actually searched and add Scopus if used. |
| Search strings | ASSUMPTION: draft strings, one block per theme; refine when run. See the list under the table. |
| Period covered | 2020 to 2026 (rule in `PLAN.md`: papers from 2020 onward; the template wants at least 70 percent from the last five years). TODO: the exact search date. |
| Inclusion criteria | Peer-reviewed version preferred over a preprint (`PLAN.md`); published 2020 or later; directly relevant to one of the eight themes; full text read where obtainable. ASSUMPTION: written in English. |
| Exclusion criteria | Published before 2020; unverifiable or unreachable papers (dropped and replaced, `PLAN.md`); Wikipedia, blogs and unpublished student projects (template). Vendor documentation is kept separately as grey literature. |
| Studies retrieved / screened / included | TODO: fill from the search log (for example "N / N / N"). Do not estimate. |

Draft search strings (ASSUMPTION), to be combined with AND across concept groups:

- Routing: ("LLM routing" OR "model routing" OR "model selection" OR "LLM cascade") AND (cost OR quality)
- Prompt difficulty: ("query difficulty" OR "prompt complexity" OR "difficulty estimation") AND ("language model" OR LLM)
- Load balancing: ("load balancing" OR "request scheduling") AND (LLM OR "language model serving")
- Cost: ("cost reduction" OR "cost-aware" OR "inference cost") AND (LLM OR "language model")
- Latency: (latency OR "tail latency" OR "time to first token") AND ("LLM serving" OR inference)
- Fallback: (fallback OR failover OR "circuit breaker" OR resilience) AND (LLM OR "model serving")
- Benchmarking: (benchmark OR "evaluation") AND ("LLM routing" OR "LLM-as-a-judge" OR "chat assistant")
- Gateway design: ("LLM gateway" OR "inference gateway" OR "serving system") AND (architecture OR orchestration)

Figure 2.1 (PRISMA-style flow of identification, screening, eligibility and inclusion): TODO, draw from the search log. ASSUMPTION: the template uses "Figure 2.1" for both this flow and the conceptual framework; here the flow is 2.1 and the framework is 2.2.

## 2.2 Conceptual and Theoretical Framework

The template asks for the key concepts and the relations among the main components or variables, with a framework diagram. Draft content from the proposal and the evaluation plan:

**Concepts to define (cite each):** model routing; prompt difficulty and task type; predicted quality; cost per request; latency, p95 and tail latency; load awareness (queue length, GPU use, tokens per second); fallback and circuit breaker; benchmarking with preference data. [CITE: one standard source per concept, from the literature-review notes]

**Conceptual framework (Figure 2.2), proposed relations:**

```
  INPUTS                          ROUTER (artefact)                    OUTCOMES (dependent variables)
  ------                          -----------------                    ------------------------------
  Prompt (text)  ───────────────► Prompt classifier ─┐
  Latency budget ───────────────►                    ├► Scoring ─► Backend ─► Cost per request
  Live backend load ────────────►                    │   engine    choice     Answer quality
  (queue, GPU use, tokens/s,                         │                        p95 latency
   health, failure counts)                           │                        Request success rate
  Price table, weights ─────────────────────────────┘      ▲
                                                           │ failure ► retry next-best, circuit breaker
  Independent variable: routing strategy (always-strong, always-weak, difficulty-only, load-aware)
  Extraneous variable:  backend load and provider variability at test time
```

ASSUMPTION: the framework is the drafter's reading of the proposal's Figure 1 and evaluation plan. Redraw it as a proper figure. TODO-confirm-with-supervisor: whether a formal theory is expected (for example a decision-theory view of the scoring function), since the template's examples (TAM, security models) do not fit a systems project. If none, say so and rely on the conceptual framework.

## 2.3 Enabling Technologies and Techniques

Compare alternatives on clear criteria and use the comparison to justify Chapter Three. The proposal's choices are already fixed, so each sub-section must explain why that choice over the alternatives, using sources, not assertion.

| Area | Proposal's choice [D-xx] | Alternatives to review | Criteria for comparison | Sources |
|---|---|---|---|---|
| Text representation for the classifier | sentence-transformers [D-01] | TF-IDF; token-count features; fine-tuned encoder | Accuracy, speed per prompt, CPU suitability | [CITE: sentence embeddings] TODO |
| Classifier | scikit-learn logistic regression [D-01] | Gradient boosting; small neural classifier; matrix-factorisation or similarity-based routers from the routing literature | Training data needed, inference time, interpretability | [CITE: routing-method papers] TODO |
| Self-hosted serving | vLLM, Ollama [D-02, D-03] | Other inference servers | Throughput, exposed metrics, ease of setup | [CITE: LLM serving systems] TODO |
| Metrics collection | Prometheus [D-02] | Application-level polling; other monitoring stacks | Standard exporter support, scrape interval, overhead | [CITE: vLLM and Prometheus documentation, grey literature] TODO |
| Gateway framework | FastAPI [D-03] | Other asynchronous web frameworks | Async support, OpenAI-compatible schemas | TODO |
| Shared state | Redis [D-05] | In-process state; relational database | Shared across gateway instances, read speed | TODO |
| Resilience pattern | Circuit breaker, retry on next-best [D-05] | Hedged requests; retry with backoff; cascades [S-04] | Added latency, success rate, complexity | [CITE: resilience patterns; fallback in LLM serving] TODO |
| Evaluation | RouterBench, MT-Bench, Chatbot Arena [D-07, SRC-07] | Other quality benchmarks | Coverage of model pairs, cost data, quality labels | [CITE: each benchmark paper] TODO |

## 2.4 Review of Related Works

Organise by theme, not by paper. The eight themes map one-to-one to the reading-list topics and to the notes folders. For each theme the supervisor writes: what the studies did, the method, data or setting, the main results with figures, their limitations, a comparison across studies ("Unlike X (year), Y (year) ..."), and the link to this project. **No studies are named here as findings.** Names given below are only the anchors listed in the proposal [SRC-05, SRC-07] and are still to be verified.

| Section | Theme (reading-list topic) | Notes folder | Project feature or risk it supports | Questions the theme must answer | Anchors named in the proposal (verify first) |
|---|---|---|---|---|---|
| 2.4.1 | Routing algorithms | `01-routing-algorithms/` | Scoring engine [D-04]; gap G1; risk R-01 | Which routing approaches exist (learned, cascade, similarity-based)? What do they optimise, on which model sets, and how well do they transfer to unseen models? | RouteLLM, Hybrid LLM, FrugalGPT |
| 2.4.2 | Prompt difficulty | `02-prompt-difficulty/` | Prompt classifier [D-01]; gap G1; risk R-02 | How is prompt or query difficulty estimated? What features and labels are used and how noisy are they? | TODO from notes |
| 2.4.3 | Load balancing | `03-load-balancing/` | Live load awareness [D-02]; gap G2; risk R-03 | How is request scheduling and load balancing done for LLM serving? Which runtime signals (queue length, GPU use, throughput) are used? Is routing across different models load-aware anywhere? | TODO from notes |
| 2.4.4 | Cost reduction | `04-cost-reduction/` | Cost term in the score [D-04]; gap G4, G7 | How much cost is saved by cascades, routers and caching, at what quality loss, and how are savings measured? | FrugalGPT, Hybrid LLM |
| 2.4.5 | Latency and speed | `05-latency-and-speed/` | Latency budget; p95; gap G6 | What drives LLM latency and tail latency? What does a cascade add? What does a pre-call decision cost? | TODO from notes |
| 2.4.6 | Error handling and fallback | `06-error-handling-fallback/` | Retry and circuit breaker [D-05]; gap G5 | What failover and resilience mechanisms exist for model serving? What evidence supports retry on next-best and circuit breakers? | TODO from notes |
| 2.4.7 | Testing and benchmarking | `07-testing-and-benchmarking/` | Evaluation plan [D-07]; gap G7; risk R-02 | How are routers and chat models benchmarked? How are quality labels produced and how reliable are they? | RouterBench, MT-Bench, Chatbot Arena |
| 2.4.8 | System design and gateway | `08-system-design-gateway/` | Gateway architecture [D-03] | How are LLM gateways and serving orchestrators designed? Which design choices (API compatibility, state sharing, observability) recur? | TODO from notes |

Writing rule for each sub-section (template): start with a two- or three-sentence synthesis, then compare studies with synthesis language, and end by stating the limitation that leads to the gap. TODO: fill each from the matching notes folder.

## 2.5 Review of Existing Systems

The template asks for three to five existing products compared with the proposed system. The proposal analyses the following. Cells marked **TBD** are not stated in the proposal. All entries remain **VERIFY** until the vendor documentation is re-read (the proposal's own risk R-04 asks for this before submission). The `literature-review/competitors/` folder is intended to supply the re-checked facts and access dates.

Brief entries (from the proposal; to be rewritten after re-checking):

1. **OpenRouter** [S-01]: one API to many hosted providers, with fallbacks and uptime-aware balancing. Chooses between providers of the model the caller names, not between models. Latency and throughput come from rolling five-minute statistics. Setting a sort order turns load balancing off. Routing docs cover listed providers and the user's own provider keys, not self-hosted GPUs.
2. **LiteLLM Router and Auto Router** [S-02]: the Router balances across the user's own deployments of a named model with latency-based, least-busy and cost-based strategies, plus fallbacks. The Auto Router (beta, 2026) sorts a request into a complexity tier and maps tiers to models. The reviewed Auto Router docs do not mention live load, queue depth, GPU use or per-request latency budgets.
3. **RouteLLM** [S-03]: a research framework that learns to pick between one strong and one weak model from preference data. Two models only; no live load, latency budget or failover.
4. **Commercial routers, for example Martian** [S-05]: managed, closed; as far as the team knows the rules cannot be inspected and it cannot run on the user's infrastructure.

FrugalGPT-style cascades [S-04] are a technique rather than a product and are discussed in 2.4.1 and 2.4.4. If the supervisor wants a fifth product, TODO: add one from the competitors notes.

**Table 2.2: Feature comparison of existing systems and the proposed system**

Legend: ✓ stated in the proposal; ✗ stated as absent or not covered in the documents reviewed; partial = stated as limited; TBD = not stated. "Proposed" column describes the plan, not an achieved result.

| Feature | OpenRouter | LiteLLM Router | LiteLLM Auto Router | RouteLLM | Martian (commercial) | Proposed router |
|---|---|---|---|---|---|---|
| Chooses the model per prompt (not only the provider) | ✗ | ✗ | ✓ (complexity tiers) | ✓ (strong vs weak) | TBD | ✓ (planned) |
| Predicts difficulty or quality before the call | ✗ | ✗ | ✓ (tier) | ✓ (learned) | TBD | ✓ (planned) |
| Uses live load (queue, GPU, throughput) | partial (rolling 5-min stats, late) | partial (latency-based, least-busy; usage-based not recommended for production) | ✗ (not mentioned in docs reviewed) | ✗ | TBD | ✓ (planned) |
| Honours a per-request latency budget | TBD | TBD | ✗ (not mentioned in docs reviewed) | ✗ | TBD | ✓ (planned) |
| Works with self-hosted GPU backends | ✗ (not covered in routing docs) | ✓ (own deployments) | TBD | TBD | ✗ (as far as the team knows) | ✓ (planned) |
| Works with hosted APIs | ✓ | TBD | TBD | TBD | TBD | ✓ (planned) |
| Fallback and failover | ✓ | ✓ | TBD | ✗ | TBD | ✓ (planned) |
| Routing rules inspectable | TBD | TBD | TBD | TBD | ✗ (as far as the team knows) | ✓ (planned, own code) |
| Number of models it can choose between | many (by named model's providers) | many deployments of a named model | tiers mapped to models | two | TBD | any configured set |

## 2.6 Summary of Reviewed Works

One row per work from Section 2.4, in chronological order or by theme. Placeholders only; the supervisor fills this from the paper notes. Minimum 25 works in depth.

**Table 2.3: Summary of related works**

| S/N | Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|---|
| 1 | TODO | TODO | TODO | TODO | TODO | TODO |
| 2 | TODO | TODO | TODO | TODO | TODO | TODO |
| 3 | TODO | TODO | TODO | TODO | TODO | TODO |
| … | … | … | … | … | … | … |
| 25+ | TODO | TODO | TODO | TODO | TODO | TODO |

## 2.7 Research Gap and Justification of the Study

The gaps below are the proposal's **claims**, not yet findings. Each stays a hypothesis until Section 2.4 supplies evidence for it, and the supervisor must drop or reword any gap the literature does not support. In particular R-03 says runtime-aware routing is "thin in the literature"; this must be checked, not assumed. Module rule: identify at least three to five gaps and show how the study addresses each.

**Table 2.4: Mapping of research gaps to project objectives**

| Gap ID | Gap identified (proposal's claim) | Evidence (studies) | Objective that addresses it |
|---|---|---|---|
| G1 | The same model serves easy and hard prompts in many gateways [D-01, S-01, S-02] | TODO: studies from 2.4.1 and 2.4.2; vendor docs as grey literature | O3 |
| G2 | Live load is seen late or not at all in routing [D-02, S-01, S-02] | TODO: studies from 2.4.3 | O4 |
| G3 | No single router covers hosted APIs and self-hosted GPU backends [D-03, S-01, S-02, S-05] | TODO: studies from 2.4.8 and the competitors notes | O2 |
| G4 | Decisions are price-only or quality-only, without a combined score and latency budget [D-04, S-03] | TODO: studies from 2.4.4 and 2.4.5 | O4 |
| G5 | Failure and slow-provider handling is not combined with per-prompt model choice [D-05, S-03] | TODO: studies from 2.4.6 | O5 |
| G6 | Cascades pay the latency of failed attempts; a pre-call decision avoids this [D-06, S-04] | TODO: studies from 2.4.5. A direct cascade baseline is not in the proposal's evaluation plan. TODO-confirm-with-supervisor: add a cascade baseline or limit the claim to a literature argument. | O6 |
| G7 | Savings of routers are unproven or hard to compare [D-07] | TODO: studies from 2.4.7 | O6 |

Closing sentences for the section (template): state which of these the project addresses and how, and state which are left to future work.

## 2.8 Chapter Summary

TODO: one or two paragraphs. Summarise the main findings of the review and restate the gap the project addresses. Write after 2.4 to 2.7 are filled.

---

### Scaffold: reference list rules (delete before pasting)

APA 7th, alphabetical by first author's surname, hanging indent, DOI wherever one exists. Every in-text citation must be in the list and vice versa. Until the notes folders are verified, no reference is entered here. Candidate sources already named by the proposal and verified by nobody yet: FrugalGPT, RouteLLM, Hybrid LLM, RouterBench, MT-Bench, Chatbot Arena [SRC-05, SRC-07]; vendor pages [SRC-01 to SRC-04] listed as grey literature with access dates.

Course-module sources that can already be cited for methodology wording in Chapters 1 and 3 (they are printed in the module): Fraenkel and Wallen (2008); Nachmias and Nachmias (1992); Ogula (2005); Wohlin et al. (2012); Kitchenham and Charters (2007). Full details are on the module's reference slide.
