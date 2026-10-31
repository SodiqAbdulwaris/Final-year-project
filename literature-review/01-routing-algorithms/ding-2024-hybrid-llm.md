# Hybrid LLM: quality-aware query routing (Ding et al., 2024)

| Field | Value |
|---|---|
| Topic (home) | 01 Routing algorithms |
| Also relevant to | 02 Difficulty prediction, 04 Cost reduction |
| Paper type | method |
| Venue and status | peer-reviewed (ICLR 2024, poster) |
| Source read | full text of arXiv v1 (https://arxiv.org/pdf/2404.14618); ICLR camera-ready not read, numbers are from v1 |
| Verified on | 2026-10-31, against arXiv ("Accepted to ICLR 2024") and OpenReview (forum 02f3mUtqnM) |
| Relevance to project | High |

## APA 7 reference
Ding, D., Mallick, A., Wang, C., Sim, R., Mukherjee, S., Rühle, V., Lakshmanan, L. V. S., & Awadallah, A. H. (2024). Hybrid LLM: Cost-efficient and quality-aware query routing. In *Proceedings of the Twelfth International Conference on Learning Representations (ICLR 2024)*. https://openreview.net/forum?id=02f3mUtqnM (preprint: https://doi.org/10.48550/arXiv.2404.14618). ICLR has no DOI; the arXiv DOI is the same work.

## In-text citation forms
(Ding et al., 2024) · Ding et al. (2024)

## 1. What it is about
A DeBERTa-v3-large router predicts whether a small model will answer about as well as a large one. Easy queries go to the small model, the rest to the large one, and one threshold set at test time trades quality for cost. Each query is answered by exactly one model.

## 2. The problem
Large models need costly cloud serving, small ones lag in quality, yet for some queries the small model matches the large one (Figure 1b: Llama-2 13B equals or beats GPT-3.5-turbo on about 20% of queries). Earlier hybrid inference covered image classification with deterministic models; LLM output is random, and ensembles or cascades call several models per query.

## 3. Proposed solution
The router outputs a score in [0,1]; queries above the threshold go to the small model. It is trained with binary cross-entropy on three label designs. The quality gap H(x) is the small model's BART score minus the large model's.
- **r_det:** hard label from one sample per model.
- **r_prob:** soft label Pr[H(x) ≥ 0] estimated from 10 samples per model, capturing randomness.
- **r_trans:** relaxed label Pr[H(x) ≥ -t], with t found by grid search, for when the large model is much stronger (about 90% of labels were 0 for FLAN-T5 800M versus Llama-2 13B).

Cost advantage is the share of queries sent to the small model; quality is BART score, so no LLM judge is needed.

## 4. Data, models and tools
MixInstruct (10K training queries, 10 responses per model; 5K validation and test). Pairs: Llama-2 7B/13B, Llama-2 13B vs GPT-3.5-turbo, FLAN-T5 800M vs Llama-2 13B. One A100. Baselines: all-at-large, all-at-small, random. Code: https://github.com/m365-core/hybrid_llm_routing (as stated in the paper).

## 5. Key results
- Abstract: up to 40% fewer large-model calls with no drop in quality.
- Table 1, drop at 40% cost advantage: Llama-2 7B/13B 0.2% (r_det), 0.1% (r_prob), 0.0% (r_trans); Llama-2 13B vs GPT-3.5 3.5%, 3.4%, 2.9%; FLAN-T5 vs Llama-2 13B 13.8%, 13.1%, 10.3%. Only r_trans clearly beats random for the large gap.
- The router is nearly 10x faster than the fastest LLM (Section 4.4).
- Table 3: a threshold tuned on 500 validation samples for a 1% drop carried over to test data.
- With GPT-4 scores as metric, 20% cost advantage cost up to 1% when BART and GPT-4 gaps correlated (r = 0.46; Figure 7a). On unseen model pairs, routers held up only when the quality-gap correlation with the training pair exceeded 0.7 (Figure 8a).

## 6. Limitations
**Authors:** query text only, no task labels; two models; model pair and data fixed between training and test, so out-of-distribution generalisation is open; better metrics needed.
**Mine:** BART score correlates weakly with GPT-4 in some pairs (r = 0.26, Figure 7c); one dataset; cost counted in calls, not price, queueing or GPU load (load balancing is listed as future work); no failure handling.

## 7. Relevance to the AI Request Router
- Supports the difficulty/quality-gap classifier and a tunable threshold.
- Reuse: soft labels from several samples (label-noise handling), the data transformation for lopsided pairs, threshold calibration on a small validation set, and the quality-gap-correlation test before reusing a router on a new pair.
- Avoid: BART score as the only quality signal.
- Not covered: N-way routing, live load, failover, latency budgets.

## 8. How to use it in the report
- Chapter 2 classifier-based routing; chapter 3 label noise.
- "Hybrid LLM (Ding et al., 2024) predicts the small-large quality gap with a tunable threshold; RouteLLM (Ong et al., 2025) learns the same decision from human preferences and tests it out of domain."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Ding et al. (2024) | Cut large-model calls, keep quality | DeBERTa router on quality-gap labels (deterministic, probabilistic, transformed); threshold | MixInstruct; Llama-2, FLAN-T5, GPT-3.5; BART score | Up to 40% fewer large calls, no drop for close pairs | Two models, one dataset, no OOD, load or failover |
