# Cascade routing: a unified approach to routing and cascading (Dekoninck et al., 2025)

| Field | Value |
|---|---|
| Topic (home) | 04 Cost reduction |
| Also relevant to | 01 Routing, 02 Difficulty, 07 Benchmarks |
| Paper type | method (with theory and empirical evaluation) |
| Venue and status | peer-reviewed (ICML 2025, PMLR 267); first posted on arXiv October 2024 |
| Source read | full text, arXiv v5 (https://arxiv.org/pdf/2410.10347) |
| Verified on | 2026-10-31, against the arXiv abstract page and the PMLR proceedings page |
| Relevance to project | High |

## APA 7 reference
Dekoninck, J., Baader, M., & Vechev, M. (2025). A unified approach to routing and cascading for LLMs. In *Proceedings of the 42nd International Conference on Machine Learning* (Vol. 267, pp. 12987–13010). PMLR. https://proceedings.mlr.press/v267/dekoninck25a.html (preprint DOI: https://doi.org/10.48550/arXiv.2410.10347)

## In-text citation forms
(Dekoninck et al., 2025) · Dekoninck et al. (2025)

## 1. What it is about
Model selection is framed as one optimisation problem: maximise expected answer quality under an expected-cost budget. The paper derives the optimal routing rule, the optimal cascading rule, and a hybrid, *cascade routing*, that can start with any model and keep re-routing after each answer.

## 2. The problem
Routing (one model per query) and cascading (cheap to expensive until an answer looks good) were studied separately, with heuristics instead of optimality proofs. It was unclear when each helps or how to combine them.

## 3. Proposed solution
Quality and cost of model i on query x are unknown, so estimators q̂_i(x) and ĉ_i(x) are used. Routing is a linear programme whose optimal rule picks the model maximising q̂_i(x) − λ·ĉ_i(x), with λ set from the budget on a validation set; ties mix the cheapest and dearest tied model, so the rule can be stochastic (Theorem 1).

Cascading becomes a sequence of routing problems over "supermodels" (ordered sequences of models). After each answer the estimates are updated and the cascade stops if the computed supermodel has the best trade-off (Theorem 2). The usual "continue if quality < threshold" cascade is optimal only under restrictive conditions (Corollary 1). Cascade routing lets each step choose among all supermodels extending what has already run, so the order is not fixed (Theorem 3); the 2^k supermodel space is pruned with a negative-marginal-gain lemma.

**How cost is modelled.** Cost "could measure either monetary costs or latency": tokenised input plus the model's average output length, times API per-token prices, or execution time as a proxy. A supermodel's cost is the sum of its members' costs. Cost estimation was found easier and less critical than quality estimation.

## 4. Data, models and tools
- RouterBench (seven benchmarks, 11 models from GPT-4 to Mistral-7B) with 3, 5 and 11 models; estimates simulated as the true value plus Gaussian noise (low, medium, high), before and after generation.
- SWE-Bench (cost = completion time), Qwen-2.5 on Minerva Math and LiveCodeBench, and Llama and Gemma families with log-probability estimators (after Gupta et al., 2024).
- Metric: area under the quality-cost curve (AUC). Code: https://github.com/eth-sri/cascade-routing.

## 5. Key results
- RouterBench zero-shot (Table 1), AUC %: with 11 models at low noise, routing 83.25, baseline cascade 84.48, their cascade 84.47, cascade routing 87.24 (linear interpolation 70.51). At high noise with 11 models, cascade routing 74.40 vs routing 72.67 and baseline cascade 69.79.
- The gap widens with more models and shrinks as noise grows; the paper reports gains of up to 8% on RouterBench and 14% on SWE-Bench.
- SWE-Bench, 10 models (Table 2): routing 40.47, baseline cascade 38.52, their cascade 53.20, cascade routing 54.12 (post-hoc quality is accurate because tests can be run).
- Qwen models on Minerva Math plus LiveCodeBench: routing and cascade routing tie at 58.20; baseline cascade 47.03 (ex-ante estimation is good, post-hoc poor).
- With real log-probability estimators (Table 2, right) the gain is at most 1.2%. Selection overhead stays within 1 s for up to 40 models (appendix).

## 6. Limitations
*Stated by the authors:* gains shrink when quality estimators are poor; the supermodel count grows exponentially, so pruning is needed.

*My observations:* most evidence uses simulated noise on RouterBench rather than trained predictors. Cascading needs a post-hoc quality signal, which open-ended chat lacks. Costs are static per model: no queueing or GPU contention, and sequential re-routing adds latency the cost term ignores. I read arXiv v5, which may differ slightly from the camera-ready.

## 7. Relevance to the AI Request Router
- **Scoring function.** argmax_i [q̂_i(x) − λ·ĉ_i(x)] is a theoretically backed form of the router's quality-versus-cost score. A live-load penalty could be added to ĉ_i (my extension, not in the paper).
- **Classifier.** Supports the claim that predicted-quality accuracy is the critical component.
- **Reuse:** λ tuned on validation data; cost = tokens × price or latency. **Avoid:** assuming accurate post-hoc scores for chat. **Not covered:** live load, failover, self-hosted GPU cost.

## 8. How to use it in the report
Section 2.4 (cost-aware selection); scoring-function design in Chapter 3. "Unlike heuristic cascades (Chen et al., 2023), Dekoninck et al. (2025) derive optimal routing, cascading and combined strategies and show that estimator accuracy dominates the trade-off."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Dekoninck et al. (2025) | Unify routing and cascading with optimality guarantees | Linear-programme view; cascade routing with quality and cost estimators | RouterBench, SWE-Bench, Minerva Math, LiveCodeBench | Beats both baselines (up to 8% and 14% AUC gain); estimator quality decisive | Simulated noise; static costs; no live load |
