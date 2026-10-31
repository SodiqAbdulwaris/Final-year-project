# LLMRouterBench: large benchmark with a unified routing framework (Li et al., 2026)

| Field | Value |
|---|---|
| Topic (home) | 07 Testing and benchmarking |
| Also relevant to | 01 Routing algorithms, 05 Latency and speed |
| Paper type | benchmark / empirical study |
| Venue and status | peer-reviewed (Findings of ACL 2026, pp. 37733–37754) |
| Source read | full text (arXiv v1, https://arxiv.org/pdf/2601.07206v1); appendices skimmed |
| Verified on | 2026-10-31, against ACL Anthology (2026.findings-acl.1881; title, 12 authors, pages 37733–37754, July 2026, ACL ISBN 979-8-89176-395-1 and DOI 10.18653/v1/2026.findings-acl.1881 all confirmed) and arXiv |
| Relevance to project | High |

## APA 7 reference
Li, H., Zhang, Y., Guo, Z., Wang, C., Tang, S., Zhang, Q., Chen, Y., Qi, B., Ye, P., Bai, L., Wang, Z., & Hu, S. (2026). LLMRouterBench: A massive benchmark and unified framework for LLM routing. In *Findings of the Association for Computational Linguistics: ACL 2026* (pp. 37733–37754). Association for Computational Linguistics. https://doi.org/10.18653/v1/2026.findings-acl.1881

## In-text citation forms
(Li et al., 2026) · Li et al. (2026)

## 1. What it is about
LLMRouterBench collects over 400K query–model–answer instances from 21 datasets and 33 recent models, wraps ten published routers in one evaluation framework, and re-tests the field under identical conditions. Its main finding is that many routers perform almost the same, several (including commercial ones) do not reliably beat a trivial baseline, and a large gap to the oracle remains.

## 2. The problem
Router papers use different model pools, datasets and protocols, so results cannot be compared, and building the data is expensive. Earlier benchmarks use older open models or cover few routers. The authors want a timely, reproducible, common ground, including both quality-only and quality-cost settings.

## 3. Proposed solution
**Data.** Two settings. Performance-oriented: 20 lightweight (about 7B) models on 15 datasets. Performance-cost: 13 flagship models on 10 datasets (saturated datasets excluded), including five proprietary models. Together: 23,945 prompts and 391,645 instances, about 1.8B tokens, 1K GPU hours and $2,771.84 of API spend. Each record stores prompt, model, output, extracted answer, label, input and output tokens, and cost.

**Framework.** A Collector (unified API with caching, retries and cost tracking), an Evaluator (dataset-specific scoring) and an Adaptor (converts the data to each router's input format, with consistent seeds and splits).

**Metrics.** AvgAcc; Gain@R and Gain@B (relative gain over a Random router and over the Best Single model); Gap@O (gap to the Oracle that picks the cheapest correct model per query); for cost: PerfGain (best accuracy gain over Best Single), CostSave (largest cost cut with accuracy no worse than Best Single) and ParetoDist (distance to the empirical Pareto frontier).

## 4. Data, models and tools
- Task areas: maths (AIME, Math500, LiveMathBench), code (LiveCodeBench, HumanEval, SWE-Bench), knowledge (HLE, SimpleQA, MMLU-Pro), logical, affective, instruction following, agentic.
- Routers: RouterDC, EmbedLLM, MODEL-SAT, GraphRouter, Avengers (performance setting); HybridLLM, FrugalGPT, RouteLLM, GraphRouter, Avengers-Pro and OpenRouter (cost setting); a top-k selection baseline.
- Code and data: https://github.com/ynulihao/LLMRouterBench. Dataset-specific evaluation rules are in Appendix Table 9; I did not extract how free-form answers are judged.

## 5. Key results
- Complementarity holds: no model wins every domain (Figure 3).
- Leading routers (EmbedLLM, GraphRouter, MODEL-SAT, Avengers) give similar results on AvgAcc, Gain@R, Gain@B and Gap@O (Figure 4), and some of the best need no neural training (clustering-based Avengers).
- A large Oracle gap persists, driven mainly by "model-recall failures": often only one model answers correctly and routers miss it.
- Backbone embedding model has little impact; enlarging the pool shows diminishing returns, while a carefully chosen top-k subset beats random selection.
- Cost setting: HybridLLM and FrugalGPT struggle to save cost without losing Best Single accuracy; the commercial OpenRouter shows a −24.7% performance change against Best Single (Section 4.2.2); Avengers-Pro sits near the Pareto frontier.
- Latency (Figure 9, a benchmark on τ²-Bench): Qwen3-Thinking and GLM-4.6 have similar accuracy and cost but latencies of 262.1 s and 32.4 s.

## 6. Limitations
Stated by the authors: only routers with public implementations are covered; domain-specific, long-context and multimodal tasks are absent; latency is approximate, estimated from token counts and OpenRouter throughput for one provider configuration and "indicative rather than definitive".

Identified by me: quality labels are correctness from automated dataset scorers (no human preference data), so noise from judge or extraction errors is not quantified; latency is not measured per request or under load; no self-hosted serving; results are single-turn with fixed prompts.

## 7. Relevance to the AI Request Router
- Directly shows what the project must go beyond: even the best published benchmark can only approximate latency. The project should log measured TTFT, end-to-end latency (including p95) and queue state per request.
- Reuse: the Best Single, Random and Oracle baselines with Gain/Gap metrics, CostSave/PerfGain/ParetoDist for the cost-quality curve, five-seed averaging, the Collector/Evaluator/Adaptor design, and its warning that an always-strong baseline is hard to beat.
- Evidence for the gap statement: it says no method explicitly targets joint performance-cost-latency trade-offs, which is where the router claims its contribution.
- Link to topic 02: the weak role of embeddings matches the question of whether [Zotos et al. (2025)](../02-prompt-difficulty/zotos-2025-model-uncertainty-difficulty.md) and [Šakota et al. (2024)](../02-prompt-difficulty/sakota-2024-fly-swat-or-cannon.md) predictors actually need larger encoders.

## 8. How to use it in the report
- Section 2.7 (benchmarks), the baseline-choice rationale and the evaluation-design chapter (metrics).
- Sentence: "LLMRouterBench (Li et al., 2026) found that many routers converge to similar accuracy and that none targets joint cost-latency trade-offs, which motivates evaluating this project against always-strong and always-weak baselines with measured p95 latency."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Li et al. (2026) | Unified, current benchmark and framework for LLM routing | Collector/Evaluator/Adaptor; Gain, Gap@O, CostSave, ParetoDist; ten routers | 21 datasets, 33 models, 391,645 instances; 1.8B tokens | Routers converge; many do not beat Best Single; large Oracle gap | Approximate latency, public routers only, automated labels |
