# RouteProfile: profiling a new LLM from public signals only (Xu et al., 2026)

| Field | Value |
|---|---|
| Topic (home) | 09 Retrieval, k-NN and multi-turn routing (cold start and new-model onboarding) |
| Also relevant to | 01 Routing algorithms |
| Paper type | method / empirical study |
| Venue and status | preprint only (arXiv v2, May 2026); no peer-reviewed venue found on the arXiv page |
| Source read | full text (https://arxiv.org/pdf/2605.00180v2); appendices skimmed |
| Verified on | 2026-10-31, against the arXiv abstract page and PDF |
| Relevance to project | Medium |

## APA 7 reference
Xu, J., Pu, H., Feng, T., Zhang, H., You, J., & Liu, G. (2026). *RouteProfile: Graph-based profiling for cold-start LLM routing* (arXiv:2605.00180). arXiv. https://doi.org/10.48550/arXiv.2605.00180

## In-text citation forms
(Xu et al., 2026) · Xu et al. (2026)

## 1. What it is about
When a new LLM is released there is no history of how it performed on past queries, so a router has nothing to learn from. RouteProfile builds a profile for the new model from information that is public on release (model family, description, reported benchmark scores and benchmark domains), arranged as a graph, and tests whether routing with such profiles works without any query–response data.

## 2. The problem
Cold-start routing means routing to a model for which no query–response–reward data exist. Existing profile styles have drawbacks: LLM-written descriptions are coarse and interaction-based embeddings are costly because they need large-scale inference on the new model. The authors ask whether sparse and heterogeneous public signals are enough.

## 3. Proposed solution
- **Graph of public signals.** Nodes for models, families, benchmark domains and benchmarks, with edges for relations such as family membership and reported scores. Text descriptions and numbers are attached to nodes (generated with tailored prompts).
- **Four design dimensions.** Organisational form (flat text versus structured graph), representation type (text versus embedding), aggregation depth (1–4 hops of graph propagation) and learning configuration (training-free versus trainable).
- **Two settings.** (1) Training-free cold-start routing with SimRouter, which picks the model whose profile is most similar to the query representation. (2) New-LLM integration: a router (MLPRouter or GraphRouter) is trained on seven existing LLMs and frozen; the new model (Mistral-Small-24B-Instruct-2501) is added as a node initialised from public information only.
- **New metric.** New-LLM Correct Integration Rate (NCIR): the share of all queries that were both routed to the new LLM and answered correctly by it.

## 4. Data, models and tools
- Candidate pool of seven existing LLMs plus one held-out new LLM; benchmark-style query sets with query–response–reward records for the existing models.
- Baselines: Oracle, Single-Best, Random Selection, PlainText (flat concatenation of signals).
- Code and data: github.com/ulab-uiuc/RouteProfile and a Hugging Face collection (linked on the paper's first page).

## 5. Key results
- Training-free cold start (Table 1): Oracle 0.679; PlainText 0.532; TextGNN-4hop 0.580 and EmbGNN-4hop 0.577; one-hop graph profiles give little or no gain over PlainText (0.526 and 0.531). The text says PlainText is below Single-Best at 0.547, while Table 1 as extracted shows Single-Best at 0.508, an inconsistency I could not resolve.
- Trainable profiles (TrainGNN) reach 0.613 at 1 or 2 hops, closer to Oracle, but fall to 0.600 at 3 hops and 0.555 at 4 hops, consistent with over-smoothing.
- Model family metadata helps consistently; benchmark-domain information is less reliable (Table 2, Section 6.3).
- New-LLM integration (Table 3): PlainText gives NCIR = 0.000 for both routers; text-based structured profiles are near zero (at most 0.007). Embedding-based profiles are needed to route any queries to the new model correctly, so the authors conclude that profile and router must be designed together.

## 6. Limitations
Stated by the authors: public signals are incomplete and inconsistent across models (different evaluation protocols, benchmark coverage and reporting granularity), which may introduce reporting bias; the experiments cover representative profile designs and router architectures but not all possibilities.

Identified by me: one new model was held out (a 24B instruct model), so conclusions about new-model integration rest on a single case; the benchmark-derived queries and rewards are not chat traffic; a single run with no intervals in the text read; no latency, cost or session aspects; preprint.

## 7. Relevance to the AI Request Router
- A sober result for onboarding a new backend (including a new local model): metadata alone gave a near-zero rate of correctly routed queries to the new model. For the guide's rule "unknown ≠ good", this supports a minimum-evidence rule: until the new model has scored neighbours from real traffic or an onboarding run, treat it as unknown, not as competent, and probe it with a controlled share of traffic or an onboarding set.
- Reuse: NCIR as an onboarding metric (share of queries that are routed to the new model and answered correctly), and reporting a cold-start result separately from steady-state results.
- Contrast: [ICL-Router](wang-2026-icl-router.md) onboards a new model by running it on a stored query set; RouteProfile shows what is lost when this step is skipped.
- Not covered: retrieval over past outcomes, calibration, sessions, hysteresis.

## 8. How to use it in the report
- Chapter 2 on cold start; Chapter 3 on how a new backend enters the pool.
- Sentence: "Xu et al. (2026) found that profiles built only from public model-card information routed almost no queries correctly to a newly released model, which supports requiring observed outcomes before a new backend is trusted."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Xu et al. (2026) | Route to a new LLM with no interaction data | Graph of public signals; text or embedding profiles; 1–4 hop aggregation; NCIR metric | Seven existing LLMs plus Mistral-Small-24B as new model; SimRouter, MLPRouter, GraphRouter | Structured profiles 0.580 vs PlainText 0.532 (oracle 0.679); NCIR near 0 for text profiles | One new model, inconsistent Single-Best figure, public-signal bias, preprint |
