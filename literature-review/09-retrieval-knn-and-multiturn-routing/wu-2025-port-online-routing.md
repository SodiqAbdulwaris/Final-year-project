# PORT: training-free online routing with approximate nearest neighbours and a token budget (Wu & Silwal, 2025)

| Field | Value |
|---|---|
| Topic (home) | 09 Retrieval, k-NN and multi-turn routing (retrieval-based estimation with budget constraints) |
| Also relevant to | 01 Routing algorithms, 04 Cost reduction, 03 Load balancing |
| Paper type | method with theory |
| Venue and status | peer-reviewed (NeurIPS 2025; the PDF header reads "39th Conference on Neural Information Processing Systems"); I did not find the proceedings page, so the proceedings volume and pages are not given |
| Source read | full text (arXiv v3, https://arxiv.org/pdf/2509.02718v3); proofs skimmed |
| Verified on | 2026-10-31, against the arXiv abstract page (comment "NeurIPS 2025") and the PDF header |
| Relevance to project | High |

## APA 7 reference
Wu, F., & Silwal, S. (2025). Efficient training-free online routing for high-volume multi-LLM serving. In *Proceedings of the 39th Conference on Neural Information Processing Systems (NeurIPS 2025)*. https://doi.org/10.48550/arXiv.2509.02718

(The DOI is the arXiv DOI; replace it with the proceedings URL once located.)

## In-text citation forms
(Wu & Silwal, 2025) · Wu and Silwal (2025)

## 1. What it is about
PORT is a routing algorithm for high-volume serving under a total token budget. It estimates each model's quality and cost for a new query by averaging over approximate nearest neighbours in a historical dataset, then picks the model with the best estimate-minus-weighted-cost, where per-model weights are learned once from a small set of early queries. It needs no training and comes with a competitive-ratio guarantee.

## 2. The problem
Most routers are offline: they assume all queries are known, or they train predictors that must be retrained when deployments change. Exact k-NN is also costly at scale. Online serving needs routing decisions made one query at a time, with a limited token budget, in a stream whose order is unknown.

## 3. Proposed solution
1. **Estimation by ANNS.** A historical dataset stores, for each past query, an embedding and each LLM's performance score and cost. For a new query, an approximate nearest-neighbour index (HNSW or DiskANN) returns a set of neighbours; the estimated performance d̂ and cost ĝ of each model are the neighbour means. HNSW search is O(log |D|) in practice versus O(|D|) for exact k-NN.
2. **Online routing from observed queries.** The global assignment under a token budget is a mixed-integer linear programme that cannot be solved when queries arrive one by one. The dual problem is parameterised by one weight α_i per LLM. The first few queries are routed randomly (for generalisable weights) and the weights are fitted by optimising the dual on them. Later queries are routed with i* = argmax over models of (d̂_ij − g_i·α_i·ĝ_ij), as shown in Algorithm 1.
3. **Guarantee.** Under natural assumptions the algorithm achieves a competitive ratio of 1 − o(1) against the offline optimum.

New deployments only require updating the historical dataset, with no retraining.

## 4. Data, models and tools
- Benchmarks: RouterBench (11 LLMs, 10,000 sampled test queries, the rest as history), SPROUT (13 LLMs; its training set as history), Open LLM Leaderboard v2 (18 LLMs, 10,000 test queries).
- Embeddings: bge-base-en-v1.5 by default; SFR-Embedding-2_R and gte-Qwen2-1.5B-instruct as alternatives. Number of neighbours |R_j| = 5.
- Baselines (eight): random; greedy performance and greedy cost via ANNS; exact KNN performance and cost; BatchSplit (solve a linear programme per mini-batch of 256 queries); two RoBERTa predictors for performance and cost.
- Budget: set to the cost for the cheapest single model to process all queries, varied by a factor of 0.25 to 2, split across models by cost efficiency. Code: https://github.com/fzwark/PORT.

## 5. Key results
- Abstract: average improvement of 3.55× in overall performance, 1.85× in cost efficiency and about 4.25× in throughput across 3 benchmarks and 8 baselines.
- Table 1 (budget equal to the cheapest model's cost): on RouterBench total performance is 2718.6 for PORT versus 1838.05 for BatchSplit, the best baseline, and 84.66% of the offline approximate optimum; the greedy and KNN performance-first routers reach only about 31% because they exhaust budget on a few models.
- Robustness: stays best as query volume rises from 4,000 to 12,000, the gap to BatchSplit reaching about 50% on RouterBench at the highest volume; consistent across 100 random shuffles of arrival order and across three embedding models. Sensitivity to its two hyper-parameters is in the appendix.

## 6. Limitations
Stated by the authors (Section 5): only performance and cost are modelled. Query-intrinsic features can be added as extra constraints, but operational-state features such as traffic or system load are outside the formulation and belong to a related load-balancing problem.

Identified by me: performance scores are benchmark labels; the neighbour count is fixed at 5 and no calibration or minimum-evidence rule is described for the neighbour-averaged estimates; the early random-routing phase sacrifices quality while weights are learned; the budget split across models is a design choice that affects results; it is a stream simulation, not a live deployment.

## 7. Relevance to the AI Request Router
- The most relevant paper for the guide's budget-aware design combined with k-NN estimates: ANN retrieval for fast estimates, a per-model weight learned from a small prefix of traffic, and evaluation under token budgets scaled from 0.25× to 2×. It supports using HNSW if exact k-NN becomes slow, and reports that the estimates tolerate embedding changes.
- Reuse: the budget-scaling experiment, the random-arrival-order stress test (100 shuffles), the performance-per-cost and throughput metrics, and the comparison against greedy and plain KNN baselines.
- What the project must decide: k (5 here, around 40 in [Varangot-Reille et al., 2026](varangot-reille-2026-contextualrouter.md)), how to enforce budgets atomically under concurrency (this paper is a simulation and uses a global dual-weight rule, not reservation), and what to do with operational state, which the authors explicitly exclude.
- Datasets: RouterBench is the common ground with [Hu et al. (2024)](../07-testing-and-benchmarking/hu-2024-routerbench.md).

## 8. How to use it in the report
- Chapter 2 on budget-constrained online routing; Chapter 3 on budget policy and nearest-neighbour search implementation.
- Sentence: "Wu and Silwal (2025) estimate model quality and cost from approximate nearest neighbours and learn per-model budget weights from a short prefix of traffic, but they exclude operational-state signals such as system load."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Wu & Silwal (2025) | Online routing under a token budget at high volume | HNSW nearest-neighbour estimates; dual-weight routing fitted on early queries; 1 − o(1) competitive ratio | RouterBench, SPROUT, Open LLM Leaderboard v2; bge-base-en-v1.5; 8 baselines | 3.55× performance, 1.85× cost efficiency, 4.25× throughput over baselines | Only quality and cost, excludes system load, no calibration, simulation |
