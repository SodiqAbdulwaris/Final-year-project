# BEST-Route: adaptive routing with best-of-n sampling (Ding et al., 2025)

| Field | Value |
|---|---|
| Topic (home) | 04 Cost reduction |
| Also relevant to | 01 Routing algorithms, 02 Difficulty prediction |
| Paper type | method (empirical) |
| Venue and status | peer-reviewed (ICML 2025, PMLR 267) |
| Source read | full text, arXiv v1 (https://arxiv.org/pdf/2506.22716) |
| Verified on | 2026-10-31, against the PMLR proceedings page and the arXiv page |
| Relevance to project | High |

## APA 7 reference
Ding, D., Mallick, A., Zhang, S., Wang, C., Madrigal, D., Garcia, M. D. C. H., Xia, M., Lakshmanan, L. V. S., Wu, Q., & Rühle, V. (2025). BEST-Route: Adaptive LLM routing with test-time optimal compute. In *Proceedings of the 42nd International Conference on Machine Learning* (Vol. 267, pp. 13870–13884). PMLR. https://proceedings.mlr.press/v267/ding25d.html (preprint DOI: https://doi.org/10.48550/arXiv.2506.22716)

## In-text citation forms
(Ding et al., 2025) · Ding et al. (2025)

## 1. What it is about
A router that picks not only *which* model answers but *how many responses* to sample from it: a cheap model once for easy queries, several times (best-of-n) for medium ones, and GPT-4o only for the hardest. A small proxy reward model picks the best sample.

## 2. The problem
Earlier routers (Hybrid LLM, RouteLLM, multi-model routers) take one response from one model. One small-model answer rarely beats a large-model answer, so most traffic still goes to the large model and savings are small.

## 3. Proposed solution
1. **Proxy reward model** (DeBERTa-v3-large, 300M), trained with a pairwise ranking loss on worst, median and best responses per query (scored by armoRM), so best-of-n selection is cheap.
2. **Multi-head router** (DeBERTa-v3-small, 44M shared encoder, K × N sigmoid heads). Head (k, n) predicts the *match probability* that the best of n samples from small model k is at least as good as one GPT-4o answer.
3. **Selection (Algorithm 1).** Keep (model, n) pairs whose match probability ≥ threshold t, choose the cheapest, and fall back to one GPT-4o call if none qualifies.

**How cost is modelled (the most reusable part).** Dollar cost per query = n × (average output length of the model) × (output price) + (input length) × (input price). Input tokens are charged once for n samples, since APIs can return several completions per prompt. Output length is unknown at routing time, so the per-model training-set average is used; the average estimation error is under $0.003 per query for all eight models (about $0.0001 for three).

Prices (Table 6, input / output, $ per 1M tokens): GPT-4o 5 / 15; GPT-3.5-turbo 3 / 6; Llama-3.1-8B 0.3 / 0.61; Mistral-7B 0.25 / 0.25; Mistral-8x7B 0.7 / 0.7; Phi-3-mini 0.3 / 0.9; Phi-3-medium 0.5 / 1.5; Codestral-22B 1 / 3.

## 4. Data, models and tools
- New 10K-instruction dataset (QA, coding, safety; 8K / 1K / 1K split); 20 responses per example from each of 8 LLMs; out-of-distribution test on MT-Bench; quality by armoRM scores.
- Baselines: N-class, N-label and clustering-based routers. The main text says all three come from prior work of Srivatsa et al. (2024), but the appendix attributes only N-label and clustering to Srivatsa et al. (2024) and gives no citation for N-class, so the origin of N-class is ambiguous. Model cascades (appendix, Appendix B.2) follow Yue et al., which the paper's own reference list dates 2023 (the ICLR version is 2024). One A100 GPU. Code: https://github.com/microsoft/best-route-llm.

## 5. Key results
- Table 1 (quality drop vs always using GPT-4o at 10 / 20 / 40 / 60% cost reduction): BEST-Route 0.19 / 0.21 / 0.47 / 0.80%; N-label 0.63 / 1.17 / 3.26 / 5.08%. N-class and clustering almost always pick GPT-4o (0.07% and 0% saving).
- MT-Bench out of distribution (Table 3): at 60% cost reduction BEST-Route loses 1.59% against 5.89% for N-label.
- Adding a coding specialist, Codestral-22B, redirects coding traffic and gives gains over GPT-4o at 10 and 20% savings (Table 2: −0.10% and −0.50% drops).
- Overhead (Section 5.4): at n = 20, match-probability prediction takes 0.04 s and best-of-n scoring 0.58 s, about 18.7 times faster than the fastest LLM; n = 1 to 20 raises generation latency by only 30% to 59%.
- Cascade baselines cost more for equal quality; BEST-Route is up to 6.46% better at 60% saving.

## 6. Limitations
*Stated by the authors:* depends on proxy reward model accuracy; not tested with very large model pools (hundreds of LLMs).

*My observations:* quality is relative to one reference model (GPT-4o) judged by one reward model, so judge noise flows into the router. Prices are static API list prices (date not stated); costs are API-based, not GPU-hour. Best-of-n multiplies output tokens, i.e. extra load on a self-hosted GPU that the formula cannot see. No live load, latency SLOs or failover.

## 7. Relevance to the AI Request Router
- The closest published match to the router's design: a **BERT-style predictor feeding a cost-aware selector** over many models with a tunable threshold. The cost formula is directly reusable as the monetary term of the scoring function.
- **Reuse:** cost formula, price table, per-model average-output-length estimator, threshold sweep for cost-quality curves. **Avoid:** costing self-hosted models with API prices only. **Not covered:** live load, queueing, circuit breaking, GPU-hour pricing.

## 8. How to use it in the report
Section 2.4 (test-time compute as a cost lever); scoring function in Chapter 3. "Unlike Hybrid LLM and RouteLLM, Ding et al. (2025) also route the number of samples, reaching 60% cost saving with 0.8% quality loss against GPT-4o."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Ding et al. (2025) | Route across many LLMs without over-using the largest | DeBERTa multi-head router over (model, n); proxy-reward best-of-n; cheapest valid option | 10K instructions, 8 LLMs, MT-Bench; armoRM | 60% cost cut, 0.8% quality drop vs GPT-4o | One judge; static prices; no load |
