# Avengers-Pro: embed, cluster, score and route (Zhang et al., 2025)

| Field | Value |
|---|---|
| Topic (home) | 09 Retrieval, k-NN and multi-turn routing |
| Also relevant to | 01 Routing algorithms, 04 Cost reduction, 07 Testing and benchmarking |
| Paper type | method |
| Venue and status | peer-reviewed (7th International Conference on Distributed Artificial Intelligence, DAI 2025, pp. 122–129) |
| Source read | full text (arXiv v2, https://arxiv.org/pdf/2508.12631v2) |
| Verified on | 2026-10-31, against the Crossref record for the DOI and the arXiv comments field ("accepted to DAI 2025"); the ACM page itself returned HTTP 403 |
| Relevance to project | Medium |

## APA 7 reference
Zhang, Y., Li, H., Chen, J., Zhang, H., Ye, P., Bai, L., & Hu, S. (2025). Beyond GPT-5: Making LLMs cheaper and better via performance-efficiency optimized routing. In *Proceedings of the 2025 Seventh International Conference on Distributed Artificial Intelligence* (pp. 122–129). Association for Computing Machinery. https://doi.org/10.1145/3772429.3772445

## In-text citation forms
(Zhang et al., 2025) · Zhang et al. (2025)

## 1. What it is about
Avengers-Pro routes each query using only three cheap steps: embed the query, find the nearest k-means clusters of past labelled queries, and pick the model with the best stored performance-efficiency score in those clusters. A single parameter α trades accuracy against cost, and the resulting curve beats every single model it ensembles.

## 2. The problem
Most routers train a neural network and must be retrained for every new model, and the then-new GPT-5 showed commercial interest in test-time routing. The authors want a simple, reproducible router that covers the whole performance-efficiency range and shows that routing can beat the best single proprietary model.

## 3. Proposed solution
**Offline calibration.** Embed a labelled set with Qwen3-Embedding-8B (4,096 dimensions), run k-means with 60 clusters, run every model on the set and store, for each (model, cluster), its accuracy p and its total cost q.

**Score.** For each model and cluster: score = α·p̃ + (1 − α)·(1 − q̃), where p̃ and q̃ are min–max normalised across models within the cluster. α near 1 favours accuracy, α near 0 favours cost.

**Online inference.** Embed the query, take the nearest clusters (the text states top-p = 4 in one place and "these three clusters" in another, an inconsistency in the paper), add up each model's cluster scores and route to the highest total. A new model is added by evaluating it on the stored set; no network is retrained.

This is a coarse, cluster-level cousin of a k-NN estimate: neighbours are replaced by the centroid statistics of the nearest clusters.

## 4. Data, models and tools
- Eight models: GPT-5-chat, GPT-5-medium, Claude-4.1-opus, Claude-4-sonnet, Gemini-2.5-pro, Gemini-2.5-flash, Qwen3-235B-A22B-2507 and its thinking variant, accessed through OpenRouter with the prices it listed.
- Six benchmarks (2,603 questions in total): GPQA-Diamond, Humanity's Last Exam (first 500), ARC-AGI-v1 (first 200), SimpleQA (500 sampled), LiveCodeBench v6 (1,055) and τ²-bench (150). Metric pass@1.
- Random 70% / 30% split of queries: 70% to fit clusters and per-cluster statistics, 30% for routing evaluation.
- Code: https://github.com/ZhangYiqun018/AvengersPro. The method is also one of the routers in [LLMRouterBench](../07-testing-and-benchmarking/li-2026-llmrouterbench.md) (as "Avengers" and "Avengers-Pro").

## 5. Key results
- Strongest single model GPT-5-medium: 62.25% average accuracy at $47.96. Avengers-Pro reaches 66.66% at $47.13 (about +7% accuracy at comparable cost, Table 3 and abstract).
- At α = 0.53 it matches GPT-5-medium's accuracy (62.66%) at $35.05, a 27% cost cut; at α = 0.39 it reaches 90% of that accuracy at 63% lower cost, and the abstract says it forms a Pareto frontier over all single models.
- Behaviour versus α (Figure 3): accuracy saturates around α of 0.6; cost stays near minimum up to about 0.4 then rises steeply; the 95% interval narrows as α grows. Three regimes: efficiency-first (α up to 0.4), a transition band, and performance-first (above 0.6).
- Model use (Figure 4): at low α most queries go to the cheap Qwen3 models; as α rises GPT-5-medium dominates.
- Caveat in the table caption: it says α = 0.1 for the +7% setting, while the body text ties 66.66% to α = 1.0. I could not reconcile this, so check the paper before quoting the α value.

## 6. Limitations
Stated by the authors: I did not find a limitations section in the text.

Identified by me: strong frontier models and hard benchmarks only, with a single random split and no repeated seeds; cost is OpenRouter list price for the evaluation set, not live; a cluster-level average hides local strengths, and the number of clusters (60) and clusters probed are fixed without a sweep reported; it does not model uncertainty or minimum evidence per cluster, and there is no latency, load or session logic; embedding with an 8B model is heavier than a small sentence-transformer.

## 7. Relevance to the AI Request Router
- A concrete, cheap alternative to per-query k-NN: pre-compute per-cluster per-model score tables offline and look up at request time. This helps if the project's k-NN lookup becomes slow, and gives a baseline for E1.
- Reuse: min–max normalised α-blend of accuracy and cost; sweeping α to trace a Pareto curve; three-regime reading of the curve to justify the Economy / Balanced / Quality bands; new models onboarded by evaluating them on the stored set.
- What the project must still decide: k or cluster count, a minimum-evidence rule per cluster, and calibration of the score. Avengers-Pro's score is a relative rank, not a success probability, so it cannot support the guide's lower-bound quality target without a separate calibration step.
- Not covered: sessions, switching, local models, hard eligibility filters.

## 8. How to use it in the report
- Chapter 2 on retrieval and clustering routers; Chapter 3 for the cost-quality trade-off parameter.
- Sentence: "Zhang et al. (2025) show that routing by the nearest query clusters, with no trained network, can exceed the best single model by about 7% accuracy at similar cost, which supports a training-free competence estimate."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Zhang et al. (2025) | Training-free routing across performance-efficiency trade-offs | Embedding, k-means clusters, per-cluster α-weighted score, nearest-cluster vote | 6 benchmarks (2,603 questions), 8 frontier models via OpenRouter | +7% accuracy at similar cost; 27% cheaper at equal accuracy; Pareto frontier over single models | Frontier models only, single split, no calibration or evidence rule, cluster inconsistency |
