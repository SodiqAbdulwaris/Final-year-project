Status: DRAFT
Depends on: D08; D12
Sources: Primary URLs in source table and proposal-audit section
Open items: Scoped numerical/final-version checks recorded below

# RouterArena: open leaderboard for comparing LLM routers (Lu et al., 2026)

| Field | Value |
|---|---|
| Topic (home) | 07 Testing and benchmarking |
| Also relevant to | 01 Routing algorithms, 02 Prompt difficulty prediction, 05 Latency and speed |
| Paper type | benchmark / platform |
| Venue and status | peer-reviewed (poster at ICLR 2026); read as arXiv v3 (Nov 2025, marked "A PREPRINT") |
| Source read | full text (https://arxiv.org/pdf/2510.00202v3) |
| Verified on | 2026-10-31, against arXiv and the ICLR 2026 virtual poster page (iclr.cc/virtual/2026/poster/10011126) |
| Relevance to project | High |

## APA 7 reference
Lu, Y., Liu, R., Yuan, J., Cui, X., Zhang, S., Liu, H., & Xing, J. (2026). RouterArena: An open platform for comprehensive comparison of LLM routers. *The Fourteenth International Conference on Learning Representations*. https://iclr.cc/virtual/2026/poster/10011126

(ICLR papers carry no DOI; the arXiv DOI is https://doi.org/10.48550/arXiv.2510.00202. Cite the arXiv version if the proceedings entry cannot be found.)

## In-text citation forms
(Lu et al., 2026) · Lu et al. (2026)

## 1. What it is about
RouterArena is an evaluation platform for routers, modelled on model leaderboards. It supplies a new dataset of about 8,000 queries (8,400 in Section 3) with difficulty levels, five groups of metrics (including router overhead latency and robustness to typos), an automated pipeline for adding routers, and a live leaderboard covering open-source, academic and commercial routers.

## 2. The problem
By the authors' comparison (Table 1), RouterBench, RouterEval, FusionBench and EmbedLLM cover 24–27 categories, give no difficulty analysis (FusionBench uses an LLM-judge analysis) and rely on a deferral curve or accuracy alone, none include commercial routers, and none provide a router ranking. So users cannot tell which router to choose.

## 3. Proposed solution
**Dataset.** Domains follow the Dewey Decimal Classification (all but religion), and question skill levels follow Bloom's taxonomy. From 62,000 raw queries (two existing benchmarks plus 21 domain datasets, capped at about 1,000 per source, then de-duplicated by embedding similarity) the authors build the final set over 9 domains and 44 categories. The size is stated two ways: the introduction says about 8,000 queries, while Section 3 says 8,400 queries sampled from 23 source datasets (Appendix E: 420 examples, 5% of the set, were used for the typo test, which agrees with 8,400). I use 8,400 as the exact figure. Difficulty is defined empirically: the number of the 42 LLMs that answer a query correctly gives three bands, hard (at most 4 of 42), medium (5–19) and easy (20 or more) (Section 3, Figure 3). Figure 3's labels show shares of 47.5%, 29.1% and 23.4% for easy, medium and hard; the order of the labels in the extracted figure text is not certain, but it fits the text saying easy and medium queries are more frequent than hard ones.

**Metrics.** (1) Accuracy. (2) Cost from actual tokens times official API prices (self-hosted models priced with comparable hosted tiers). (3) Routing optimality: optimal-selection ratio (cheapest correct model chosen), optimal-accuracy ratio, optimal-cost ratio. (4) Robustness: share of queries for which the chosen model stays the same under paraphrase, grammar, synonym or typo changes. (5) Routing latency: extra time-to-first-token and end-to-end delay added by the router.

**Arena score.** A weighted harmonic mean of accuracy and a log₂-normalised cost score between a cheapest-model cost (0.0044 per 1k queries) and an expensive ceiling (200), with cost weight β = 0.1 by default.

**Framework.** A router exposes an endpoint; the platform sends queries, records the chosen model and timing, reuses cached model answers where pools overlap, and updates the leaderboard.

## 4. Data, models and tools
- Routers: 12, including commercial (Not Diamond, Azure Model Router, GPT-5's internal router) and academic (RouterBench KNN and MLP, GraphRouter, K-means universal router, CARROT, RouterDC, IRT-Router variants, RouteLLM, vLLM Semantic Router). Router overhead is measured on one A100 GPU.
- Extra check: LongBench-v2 (Appendix C).
- Code: https://github.com/RouteWorks/RouterArena; leaderboard on routeworks.github.io.

## 5. Key results
- No router leads on all metrics, and commercial routers are not automatically better; GPT-5 achieves the highest accuracy at every difficulty level but at much higher cost (Section 6.3, 6.5).
- Most routers exceed 89% accuracy on easy queries but accuracy falls sharply on medium and hard ones, often below 10% on hard (Table 6).
- Some routers spend much more on hard than easy queries, others show flat cost, suggesting room for difficulty-aware routing.
- Robustness (1 minus the share of changed selections under perturbed queries) is described as uniformly low, but Figure 9 shows a wide spread: vLLM-SR is lowest at 35.00%, then NIRT-BERT 49.29%, Azure-Router 54.07%, NotDiamond 55.91% and MIRT-BERT 61.19%, up to RouteLLM at 100.00%. The authors attribute the weakness of the academic routers to BERT encoders' sensitivity to surface perturbations. (So "uniformly low" is the authors' wording; the figure itself does not support it for every router.)
- Router latency (Figure 9): vLLM-SR 546.8 and RouteLLM 259.0 (ms) because they call an embedding API over the network, while the rest are mostly under 100 ms. The authors warn that routers add non-negligible overhead that may threaten service-level objectives.
- Leaderboard figures differ slightly between Figure 1 and Table 2 (ranking by arena score versus an average over six ranks), so cite the version you use.

## 6. Limitations
Stated by the authors: I did not find a dedicated limitations section; they note that some commercial routers hide their model choice, so some metrics cannot be computed for them.

Identified by me: labels are automatic correctness checks, and "difficulty" depends on the 42-model pool; latency is router overhead only (not backend queueing or generation time); the platform measures a single-request path, so load behaviour is not tested; pools differ across routers, which complicates fair comparison; the v3 PDF is labelled preprint.

## 7. Relevance to the AI Request Router
- The best template for the project's metrics set: accuracy, cost, optimal-selection, robustness to typos and router overhead latency. The project should add per-request backend latency (including p95) and behaviour under load, which RouterArena does not measure.
- Reuse: empirical difficulty from the number of models that answer correctly (a label with no human annotation, the same idea as in Q-DAPS) and the easy/medium/hard breakdown to test whether the classifier spends more on hard prompts.
- Reuse: the typo/paraphrase consistency test for the embedding classifier, and the measurement of router overhead against an SLO budget.
- Links to topic 02: [Mozafari et al. (2026)](../02-prompt-difficulty/mozafari-2026-q-daps.md) uses the same model-agreement notion of difficulty; [Damani et al. (2025)](../02-prompt-difficulty/damani-2025-learning-how-hard-to-think.md) uses sampled success rates.

## 8. How to use it in the report
- Section 2.7 (benchmarks), the metric-selection argument in Chapter 3, and the robustness and overhead tests.
- Sentence: "RouterArena (Lu et al., 2026) adds router-overhead latency and typo robustness to accuracy-cost metrics, but it does not measure backend latency or behaviour under load, which this project adds."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Lu et al. (2026) | Open platform and leaderboard for comparing routers | DDC/Bloom dataset with empirical difficulty; accuracy, cost, optimality, robustness, router latency; arena score | about 8,000 (8,400) queries, 44 categories, 42 LLMs; 12 routers incl. commercial | No router wins all metrics; commercial not better; low robustness; some routers add 250–550 ms | Router overhead only, no backend load, automatic labels |


## 2026-10-31 proposal audit

- Source attempted: https://arxiv.org/abs/2510.00202.
- Scope: Abstract/metadata check only in this session; detailed numerical results remain unchecked.
- Historical Source read above records the earlier session, not a claim of a fresh full reading.
- arXiv title matched: RouterArena: An Open Platform for Comprehensive Comparison of LLM Routers. Latest listed version: v3; arXiv DOI identifies the preprint, not peer review. A missing journal reference does not prove that no published version exists.
