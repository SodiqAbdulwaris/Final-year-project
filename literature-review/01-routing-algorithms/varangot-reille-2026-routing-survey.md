# Routing strategies for resource optimisation: a survey (Varangot-Reille et al., 2026)

| Field | Value |
|---|---|
| Topic (home) | 01 Routing algorithms |
| Also relevant to | 04 Cost reduction, 07 Benchmarks |
| Paper type | survey |
| Venue and status | peer-reviewed (*Journal of Artificial Intelligence Research*, vol. 86, published 30 June 2026); arXiv Feb 2025 (v3 21 Jul 2025) |
| Source read | full text of arXiv v3 (https://arxiv.org/pdf/2502.00409v3); JAIR final version not read, details may differ |
| Verified on | 2026-10-31, against the JAIR page (article/view/19801), Crossref and arXiv |
| Relevance to project | High |

## APA 7 reference
Varangot-Reille, C., Bouvard, C., Ciancone, M., Gourru, A., Schaeffer, M., & Jacquenet, F. (2026). Doing more with less: A survey on routing strategies for resource optimisation in large language model-based systems. *Journal of Artificial Intelligence Research, 86*. https://doi.org/10.1613/jair.1.19801. The brief and user notes say 2025 (the arXiv year); the journal is 2026. Author order follows JAIR (arXiv v3 lists Gourru before Ciancone). Article number not shown on the JAIR page.

## In-text citation forms
(Varangot-Reille et al., 2026) · Varangot-Reille et al. (2026)

## 1. What it is about
A survey of routing in LLM-based systems as a performance-versus-cost optimisation: why (objectives), when (before or after generation) and how (similarity, supervised, reinforcement learning, generative). Candidates may also be prompts, tools, data sources or pipeline stages.

## 2. The problem
LLM-based systems such as chatbots usually send every query to one general model, so easy queries use financial, energy and compute resources they do not need. Routing literature was scattered, without a common definition, objective or protocol.

## 3. Proposed solution (survey structure)
- **Definition (Eq. 1):** a router picks the model M in a pool that maximises a score s(q, M) subject to cost C_M(q) ≤ B. Unlike mixture-of-experts gating it is external to the model, budget-constrained and may route to non-neural components.
- **Why (Section 2):** metrics (human evaluation, exact match, similarity, LLM-as-judge, preferences) and costs (price per token, latency, compute, energy, carbon).
- **When (Section 3):** pre-generation (estimate complexity or domain; no added latency) versus post-generation or cascade (evaluate an answer, escalate; usually costlier).
- **How (Section 4):** similarity-based (query, clustering, preference), supervised (recommender-style, domain classification, knowledge graphs, answer confidence), reinforcement learning (stateless, state-based, reward-based) and generative (token or sequence probability, prompting, fine-tuning, repeated calls, code execution).

## 4. Data, models and tools
No experiments. Table 2 lists surveyed works. RouterBench, MixInstruct, EmbedLLM and SPROUT are named as datasets for comparing routers; Ecologits, CodeCarbon, MLCO2 and Boavizta for carbon cost.

## 5. Key findings
- Most strategies are pre-generation and frugal; post-generation ones are usually more resource-intensive (Section 5).
- Routing can be solved with low-resource methods that keep generalisation.
- Industry practice is simple: conditional rules, similarity or prompt-based classification, sometimes a small classifier trained on LLM-generated data (Section 5.1).
- Five challenges (Section 5.2): costs beyond money; no standard evaluation (proposed baselines: random, oracle, best stand-alone LLM, other routers); complementary rather than redundant candidates; routing every pipeline stage; adaptive routers that add candidates without retraining.
- Caution (Section 4.4.5): AutoMix beat HybridLLM and FrugalGPT in its own paper, but a cited independent study found it did not beat random routing on RouterBench (not checked by me).

## 6. Limitations
**Authors:** focus on conversational and RAG-style systems; standardisation, non-financial cost and adaptivity left open.
**Mine:** descriptive, no meta-analysis of reported numbers; 2025 to 2026 work after its cut-off is covered better by Moslem and Kelleher (2026); latency is a cost to minimise, not a per-request budget; little on live load, queueing, failover or self-hosted serving.

## 7. Relevance to the AI Request Router
- Supports the problem framing: Eq. 1 is almost the project's "quality subject to cost and latency" decision.
- Supports the benchmark plan: its four baselines can be adopted unchanged.
- Gap evidence: non-financial costs and adaptive routing named as open, backing latency and live-load inputs.
- Reuse: pre-/post-generation distinction; lightweight embedding-plus-classifier routers as competitive.
- Not covered: live system state, failover, circuit breakers, serving engines.

## 8. How to use it in the report
- Chapter 2 definition and taxonomy (2.4); chapter 3 baselines.
- "Varangot-Reille et al. (2026) formalise routing as budget-constrained selection and call for non-financial costs and adaptivity, but ignore live backend state; this study adds load-aware signals."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Varangot-Reille et al. (2026) | Survey routing as performance-cost optimisation | Taxonomy by objective, timing and strategy | Reviews RouterBench, MixInstruct, EmbedLLM, SPROUT | Lightweight pre-generation routers suffice; needs standard baselines, non-financial costs, adaptivity | Descriptive; no live load or failover view |
