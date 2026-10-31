Status: DRAFT
Depends on: D08; D12
Sources: Primary URLs in source table and proposal-audit section
Open items: Scoped numerical/final-version checks recorded below

# RouteBalance: fusing model routing and load balancing (Da & Kalyvianaki, 2026)

| Field | Value |
|---|---|
| Topic (home) | 03 LLM load balancing (added by me; not on the assigned list) |
| Also relevant to | 01 Routing algorithms, 04 Cost reduction, competitors |
| Paper type | system |
| Venue and status | preprint only (arXiv v1, 16 Jun 2026, University of Cambridge; ACM template with placeholder venue, so not yet published) |
| Source read | full text (https://arxiv.org/pdf/2606.17949) |
| Verified on | 2026-10-30, against arXiv listing 2606.17949 |
| Relevance to project | High (closest prior art found in this topic) |

## APA 7 reference
Da, W., & Kalyvianaki, E. (2026). *RouteBalance: Fused model routing and load balancing for heterogeneous LLM serving*. arXiv. https://doi.org/10.48550/arXiv.2606.17949

## In-text citation forms
(Da & Kalyvianaki, 2026) · Da and Kalyvianaki (2026)

## 1. What it is about
RouteBalance picks, for each request, a concrete model instance (a specific model on a specific GPU) using one score that trades off predicted answer quality, latency and cost. It joins what are usually two separate layers: a model router that ignores load, and a load balancer that ignores quality.

## 2. The problem
Model routers (FrugalGPT, RouteLLM, BEST-Route, Avengers-Pro) choose by quality and cost and treat capacity as static, so they can saturate the best model. Under a quality-only router the authors saw mean latency rise from 2.3 s to over 60 s at 30 requests/s. Load balancers handle queues but ignore quality.

## 3. Proposed solution
- **Batch assignment.** Waiting requests are scheduled in batches. Requests are sorted by predicted output length, longest first (the longest-processing-time rule), and each is greedily assigned to the instance with the best score; a replay found the greedy result differs negligibly from a Hungarian matching in realised quality.
- **Score.** A weighted sum of predicted quality, latency and cost, with weights on a simplex that act as one knob (named presets: Quality, Latency, Cost).
- **Estimators.** Quality and expected output length come from a MiniLM sentence embedding plus a k = 10 nearest-neighbour lookup over 14,919 labelled prompts. Latency uses per-tier gradient-boosted heads.
- **Live load by dead reckoning.** Each vLLM worker exposes a non-blocking telemetry endpoint (queue depth, pending decode work, active sequences, KV-cache pressure, recent service rate) from a cached value. The scheduler seeds its state from it and updates its own copy after every dispatch within the batch to avoid herding on stale readings.

## 4. Data, models and tools
- 13 instances on 28 GPUs (CloudLab), Qwen2.5 3B to 72B on A30, V100 and A100; code at https://github.com/AKafakA/route-balance.
- 18,608 prompts from seven public datasets; quality scored by DeepEval G-Eval with a Llama-3.1-8B judge.
- Baselines: Avengers-Pro, BEST-Route, vLLM Semantic Router, each with round-robin, shortest-queue or random dispatch; 442 configurations, about 1.5 million requests.

## 5. Key results
- Abstract: highest routing-decision quality (DeepEval 0.419, +0.013 over BEST-Route, 95% CI [+0.005, +0.022]); the balanced preset serves at 2.8 s at 30 requests/s, 2.6–4.1× ahead of enhanced BEST-Route.
- The joint decision costs about 32 ms per request at 12 requests/s on the CPU; router baselines run as published (one scoring call per request) collapsed 23× under load.
- A four-arm isolation attributes the gain to pricing latency at model-selection time; within a tier, reactive queue depth was sufficient and the learned predictors mainly add calibration (Section 6.3).
- Predictor accuracy (Section 6.8): the quality estimator picks the best model on 34.8% of held-out prompts (random 25%); on one math dataset (gsm8k) it fell to 0.23, below chance.
- Removing the 72B tier caused zero failed requests; the quality cell fell from 0.419 to 0.372.

## 6. Limitations
- *Stated by authors:* a second model family and topology, production-trace arrivals and an SLO-driven weight controller are future work; nearest-neighbour estimation can fail on novel domains.
- *My observations:* one model family and one cluster; quality is an offline judge score looked up per (prompt, model), not measured at serve time; Poisson-style replayed arrivals; preprint; failure handling is evaluated only as loss of a whole tier.

## 7. Relevance to the AI Request Router
- **Live-load signals:** the closest published match to the project's concept: per-prompt model choice plus live load together. Uses queue depth and KV pressure from vLLM telemetry, dead-reckoned between readings, and shows load-blind routing collapses at high rate.
- **Reuse:** the quality–latency–cost weight simplex; sentence-embedding plus KNN estimator (a simpler alternative to the planned classifier); dead reckoning to handle stale metrics; batched, off-GPU decision path.
- **Gap check:** it narrows the project's claimed gap; state differences clearly (latency budgets, hosted plus self-hosted backends, failover, benchmark evaluation).

## 8. How to use it in the report
- Gap statement, competitor comparison and staleness discussion.
- Synthesis sentence: "Da and Kalyvianaki (2026) fuse model routing and load balancing for self-hosted clusters, but do not cover hosted backends, per-request latency budgets or failover."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Da & Kalyvianaki (2026) | Jointly choose model and instance under load | Weighted quality–latency–cost score; KNN quality estimator; dead-reckoned load; LPT-greedy batches | 13 instances/28 GPUs, Qwen2.5 3B–72B, 18,608 prompts | Quality 0.419; 2.6–4.1× faster than enhanced BEST-Route at high load | One family; offline quality labels; preprint |


## 2026-10-31 proposal audit

- Source attempted: https://arxiv.org/abs/2606.17949.
- Scope: Abstract/metadata check only in this session; detailed numerical results remain unchecked.
- Historical Source read above records the earlier session, not a claim of a fresh full reading.
- arXiv title matched: RouteBalance: Fused Model Routing and Load Balancing for Heterogeneous LLM Serving. Latest listed version: v1; arXiv DOI identifies the preprint, not peer review. A missing journal reference does not prove that no published version exists.
