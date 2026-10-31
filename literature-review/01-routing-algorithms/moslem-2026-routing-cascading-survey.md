# Dynamic model routing and cascading: a survey (Moslem & Kelleher, 2026)

| Field | Value |
|---|---|
| Topic (home) | 01 Routing algorithms |
| Also relevant to | 04 Cost reduction, 07 Benchmarks, 02 Difficulty prediction |
| Paper type | survey |
| Venue and status | peer-reviewed (*Transactions on Machine Learning Research*, August 2026); arXiv v1 Feb 2026, v3 30 Aug 2026 |
| Source read | full text of the published version (https://arxiv.org/pdf/2603.04445v3, "Published in TMLR (08/2026)"); sections 1, 9, 10, 11 in detail, paradigm sections skimmed |
| Verified on | 2026-10-31, against arXiv and the TMLR paper list (id ypRg1TvQaM) |
| Relevance to project | High |

## APA 7 reference
Moslem, Y., & Kelleher, J. D. (2026). Dynamic model routing and cascading for efficient LLM inference: A survey. *Transactions on Machine Learning Research*. https://openreview.net/forum?id=ypRg1TvQaM (preprint: https://doi.org/10.48550/arXiv.2603.04445). TMLR has no DOI. Companion list: https://github.com/ymoslem/awesome-llm-routing-cascading.

## In-text citation forms
(Moslem & Kelleher, 2026) · Moslem and Kelleher (2026)

## 1. What it is about
A survey of methods that pick among several independently trained LLMs at inference time, by routing (one decision per query) or cascading (try a cheap model, escalate if the answer looks poor). Mixture-of-experts routing inside one model is excluded.

## 2. The problem
Static deployment wastes money on easy queries and underserves hard ones. Routing and cascading work grew fast in 2024 to 2026 and needed one current map, plus a way to compare systems that differ in what they use and when they decide.

## 3. Proposed solution (survey structure)
**Six paradigms:** difficulty-aware, human-preference-aligned (for example RouteLLM), clustering-based, reinforcement-learning (policy optimisation and bandits), uncertainty-based, and cascading (for example FrugalGPT, AutoMix); plus multimodal routing and evaluation. **Design-space framework (Section 1.4):** each system is described by *when* it decides (pre-generation, post-generation, multi-stage), *what information* it uses (query, model metadata such as cost and latency, response signals, feedback) and *how* it decides (heuristic, supervised, bandit, reinforcement learning). Section 10 views production routing as a three-stage pipeline: cheap pre-router, post-generation verifier, escalation policy.

## 4. Data, models and tools
No experiments; it collects reported results. Tables 2 to 4 gather published results on RouterBench (over 405,000 precomputed outputs, 11 LLMs, 7 tasks), MT-Bench and MixInstruct.

## 5. Key findings
- Evaluation is not comparable (Section 9.3): on one dataset, methods use different metrics (AUC, AIQ, accuracy at a cost point, deferral-curve area, quality-drop percentage, calls to a target), model pools and cost bases.
- Four failure modes (Section 9.4): distribution shift (rarely tested), router staleness when the pool changes (some methods avoid retraining, Zooter-style fixed pools do not), asymmetric cost of router errors, and "routing collapse" (scalar-score routers over-select the strongest model as budget grows; Lai & Ye, 2026, as cited).
- Gaps from the design-space matrix (Section 10): no method pairs response-level signals with online adaptation; RL is little used in cascades; few methods optimise quality, cost and latency jointly.
- Conclusion: good routers can beat the strongest single model; most work is one-stage routing; retraining-free generalisation and shared evaluation are open.
- Serving metrics (TTFT, throughput, goodput) appear only as evaluation metrics; queueing appears only in one contextual queueing-bandit method. Live load, failover and self-hosted serving are not treated as routing signals.

## 6. Limitations
**Authors:** methods span several paradigms, so classification is approximate; cost-minimising routers send more users to weaker models by design (ethical statement).
**Mine:** reported numbers only, no re-evaluation under a shared protocol; coverage of 2025 to 2026 depends on the authors' selection; serving aspects out of scope; I read the paradigm sections only briefly.

## 7. Relevance to the AI Request Router
- Supports the framing: the most current taxonomy, placing the project as a pre-generation classifier router with optional escalation.
- Gap evidence: no shared metrics, thin distribution-shift testing, staleness, routing collapse, few multi-objective systems, matching proposal risks.
- Reuse: the when/what/how framework to describe the project; the failure modes as test cases; the three-stage pipeline as a template for failover and quality fallback.
- Not covered: load and latency as routing inputs, self-hosted serving, circuit breakers.

## 8. How to use it in the report
- Chapter 2 introduction and taxonomy; chapter 2 gap analysis; chapter 3 positioning.
- "As Moslem and Kelleher (2026) note, methods on the same benchmark rarely share a metric, model pool or cost basis, and none treats live backend load as a routing signal."
- Pair with Varangot-Reille et al. (2026).

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Moslem & Kelleher (2026) | Map multi-LLM routing and cascading | Survey; six paradigms plus when/what/how framework | Reported results on RouterBench, MT-Bench, MixInstruct | Evaluations not comparable; four failure modes; no method joins response signals with online adaptation | No re-evaluation; load and failover out of scope |
