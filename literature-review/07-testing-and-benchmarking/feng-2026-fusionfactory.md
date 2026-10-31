# FusionFactory: multi-LLM log data for routing, prompting and distillation (Feng et al., 2026)

| Field | Value |
|---|---|
| Topic (home) | 07 Testing and benchmarking |
| Also relevant to | 01 Routing algorithms, 04 Cost reduction |
| Paper type | benchmark + method |
| Venue and status | peer-reviewed (Transactions on Machine Learning Research, July 2026; first arXiv version July 2025 was titled "Fusing LLM capabilities with routing data") |
| Source read | full text (arXiv v3, https://arxiv.org/pdf/2507.10540v3, whose header reads "Published in TMLR (07/2026)") |
| Verified on | 2026-10-31, against the TMLR bib entry (jmlr.org/tmlr/papers/bib/N951scS3yE.bib) and arXiv |
| Relevance to project | Medium |

## APA 7 reference
Feng, T., Zhang, H., Lei, Z., Han, P., Patwary, M., Shoeybi, M., Catanzaro, B., & You, J. (2026). FusionFactory: Fusing LLM capabilities with multi-LLM log data. *Transactions on Machine Learning Research*. https://openreview.net/forum?id=N951scS3yE

(TMLR has no DOI; arXiv DOI: https://doi.org/10.48550/arXiv.2507.10540. The supervisor's list dated this paper 2025 from the arXiv preprint; the published year is 2026.)

## In-text citation forms
(Feng et al., 2026) · Feng et al. (2026)

## 1. What it is about
The paper treats the logs that accumulate when many LLMs are called (query, model, response, cost, quality) as a training resource. It builds LLMFusionBench from such logs and tests three ways to use them: choosing a model per query (routing), retrieving reasoning templates, and distilling the best responses into one model.

## 2. The problem
Methods that combine LLMs usually study a single stage (routing, or distillation, or ensembling) in isolation and often need logits that API-hosted models do not expose. The authors ask how the same text-only log data should best be used across stages.

## 3. Proposed solution
**Data format.** Each log entry is (query q, task t, model m, response mode s, response r, cost c, performance y, LLM-judge score j). Response mode is direct or reasoning-augmented prompting, so a router chooses a (model, mode) pair. In the released DataFrame each row has task, query, LLM, response, performance, cost and judge score.

**Benchmark.** Up to 500 training and 50 test queries per task from 14 tasks in six domains, answered by 20 open-source LLMs from 8B to 671B parameters, 103M tokens in total. Cost is estimated from token counts (GPT-2 tokenizer) and Together AI prices.

**Quality labels.** Task-specific metrics, plus an LLM judge scoring how insightful correct answers are, because task metrics can favour short, low-information answers.

**Three fusion levels.** Query-level: a learned router maximises a reward α·Performance − β·Cost + γ·JudgeScore, with four scenarios (Performance First, Balance, Cost First, LLM Judge) set by (α, β, γ) = (1,0,0), (0.5,0.5,0), (0.2,0.8,0) and (0,0,1). Thought-level: retrieve and summarise abstract reasoning templates. Model-level: fine-tune a model on the judge's top-ranked responses.

## 4. Data, models and tools
- Routers compared at query level: RouterKNN, RouterSVM, RouterMLP, RouterBERT and GraphRouter, with Best LLM, LLM-Mean and Largest LLM as static baselines.
- Metrics: Performance (task accuracy), Cost, Reward, LLMScore.
- Code and data: github.com/ulab-uiuc/FusionFactory and a Hugging Face collection (linked in the paper).

## 5. Key results
- Query-level routers beat the best single LLM in all four scenarios, by at least 2% and up to 16% in performance or reward (Section 4.3, Table 4).
- Example (Performance First): Best LLM scores 0.546 at average cost 0.1850, RouterMLP 0.561 at 0.0652 and GraphRouter 0.602 at 0.0184. RouterBERT is worst (0.528 at cost 0.1030).
- GraphRouter, using fused small models, beats both the best single and the largest model (Figure 5), since larger LLMs do not always do best under the 1024-token limit.
- Cross-level (Section 7): thought-level fusion gives the strongest gains, query-level the best accuracy-cost trade-off, and model-level fusion lags because of generalisation limits.
- The abstract states FusionFactory beats the best individual LLM on all 14 benchmarks, with the best configuration varying by benchmark.

## 6. Limitations
Stated by the authors (Appendix A): quality of logs affects every stage and noisy, biased or wrongly scored logs can propagate into routing; richer production signals (time order, user feedback, error patterns, multi-turn history) are not covered; privacy risks of logs; reliability and transparency risks of API-based fusion.

Identified by me: the cost estimate is token-based with list prices, not measured; there is no latency or load field; LLM-judge scoring adds judge bias that is not quantified here (see [Zheng et al., 2023](zheng-2023-mt-bench-llm-judge.md)); the query set is small (500 training queries per task); the paper was revised substantially between v1 and v3, so cite the TMLR version.

## 7. Relevance to the AI Request Router
- Closest published description of the "serving log" the router will itself produce. The log tuple (query, task, model, mode, response, cost, performance, judge score) is a good starting schema, to which the project should add measured latency, queue state and backend ID.
- Reuse: the reward formulation α·quality − β·cost with named scenarios (a template for the router's scoring function and its presets); comparison of KNN, SVM, MLP and BERT routers; using logs to train the classifier without logits.
- Avoid: relying on an LLM judge as the only quality label.
- Not covered: latency, load, failover, real traffic.
- Link to topic 02: the routers trained here are the same family as in [Šakota et al. (2024)](../02-prompt-difficulty/sakota-2024-fly-swat-or-cannon.md); its warning about low-quality logs echoes label-noise concerns in [Zhu et al. (2025)](../02-prompt-difficulty/zhu-2025-llm-already-knows.md).

## 8. How to use it in the report
- Section 2.7 (benchmarks and data), and the data-collection plan in Chapter 3 (what the router logs).
- Sentence: "Feng et al. (2026) formalise multi-LLM serving logs as (query, model, mode, cost, performance, judge-score) records and show that routers trained on them beat the best single model, but their logs carry no latency or load fields."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Feng et al. (2026) | Use multi-LLM logs to fuse model strengths | LLMFusionBench; query-, thought- and model-level fusion; reward α·P − β·C + γ·J | 14 tasks, 20 LLMs (8B–671B), 103M tokens | Routers beat best single LLM by 2–16%; GraphRouter 0.602 at cost 0.0184 vs 0.546 at 0.1850 | Token-based cost, no latency or load, judge scores and log noise |
