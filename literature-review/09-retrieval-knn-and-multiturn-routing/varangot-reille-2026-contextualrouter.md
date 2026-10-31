# Past-performance retrieval and a few-shot k-NN router (Varangot-Reille et al., 2026)

| Field | Value |
|---|---|
| Topic (home) | 09 Retrieval, k-NN and multi-turn routing |
| Also relevant to | 01 Routing algorithms, 07 Testing and benchmarking |
| Paper type | method / empirical study |
| Venue and status | peer-reviewed (EACL 2026 Student Research Workshop, pp. 304–319); not the JAIR survey by the same first author, which is homed in topic 01 |
| Source read | full text (ACL Anthology PDF, https://aclanthology.org/2026.eacl-srw.22.pdf); appendices only skimmed |
| Verified on | 2026-10-31, against the ACL Anthology entry 2026.eacl-srw.22 |
| Relevance to project | High |

## APA 7 reference
Varangot-Reille, C., Bouvard, C., & Gourru, A. (2026). Generalising LLM routing using past performance retrieval: A few-shot router is sufficient. In *Proceedings of the 19th Conference of the European Chapter of the Association for Computational Linguistics (Volume 4: Student Research Workshop)* (pp. 304–319). Association for Computational Linguistics. https://doi.org/10.18653/v1/2026.eacl-srw.22

## In-text citation forms
(Varangot-Reille et al., 2026) · Varangot-Reille et al. (2026)

## 1. What it is about
The paper tests whether a router needs complex learned representations to handle new candidate models. Its ContextualRouter estimates each model's score on a new query from the scores of similar past queries, and a plain k-NN average over the same neighbours does as well or better. Both work with as little as 1% of the historical data and accept new models without retraining.

## 2. The problem
Most routers are trained for a fixed model pool and must be retrained whenever a model is added or removed. Representation-based methods (graph networks, learned model embeddings) avoid retraining but add architectural complexity. The authors ask whether that sophistication is necessary.

## 3. Proposed solution
**Routing rule.** Choose the model that maximises estimated performance minus a cost penalty: argmax over models of (p̂_ij − λ·c_i). The penalty λ is set at deployment and is not learned, so the same estimator serves several budgets.

**Context extraction.** Embed the query, take the cosine-similarity top-k neighbours from a corpus of past queries (k = 40 by default) and build a similarity vector s and a neighbour performance matrix P (models × k). The estimator sees only these meta-features, never a model identity, which is what lets it generalise to unseen models.

**ContextualRouter.** Project s and P into a shared space, compute an attention matrix that re-weights each model's neighbour scores (distant neighbours get less weight), and feed the weighted scores through a two-layer feed-forward head with a clamp to [0, 1]. The loss is mean squared error plus an NDCG ranking loss.

**k-NN baseline.** For each model, average its observed score over the k neighbours without any distance weighting.

## 4. Data, models and tools
- Benchmarks: SPROUT, RouterBench (Chinese subsets removed), LiveBench, BigGenBench and EmbedLLM; low-data and generalisation tests use FusionBench. Scores come from an LLM judge in these benchmarks.
- Embeddings: snowflake-arctic-embed-m-v2.0 (768 dimensions) by default; potion-multilingual-128M (256) and OpenAI text-embedding-3-large (3072) as alternatives.
- Baselines: random, oracle, best-training, most expensive, cheapest model, the Universal Model Router (UMR), and k-NN.
- Metrics: peak performance, weighted distance to the oracle (DTOw, with weights 0.25 cost and 0.75 performance), relative cost to reach 95% or 100% of best-model performance (RelDiff), MSE of the performance estimate, and NDCG over the model ranking.

## 5. Key results
- k-NN averaging matches or beats ContextualRouter on performance estimation and ranking (Table 2); both match UMR's cost-quality trade-off.
- Number of neighbours: k from 10 to 80 was tested; going beyond k = 40 gave no significant gain. Smaller k gave better cost-performance (lower DTOw) while larger k raised peak performance, because larger, expensive models dominate a wide neighbourhood and hide the local strengths of small models.
- Embedding size barely matters: even the 256-dimension static model nearly matched the best one.
- Low data: with only 1% of the FusionBench training split (53 samples) the retrieval routers reached the same performance as with 10% (535 samples), while UMR degraded at 1% because its clusters were small and noisy. Adding models at inference time worked without retraining.
- Retrieval degradation: after paraphrasing 3,000 queries per benchmark with gpt-4o-mini, changes were small (peak performance −0.3 to +2.0, DTOw −3.0 to +1.1).

## 6. Limitations
Stated by the authors: benchmark labels contain flaws (unanswerable questions, several valid answers, wrong ground truth; SPROUT examples in Appendix B), which corrupt both training and the historical performance data used for retrieval; the share of the gap to the oracle that is simply unpredictable has not been measured; a query corpus with performance records has to be kept at inference time (though only a small one).

Identified by me: benchmark questions share formats, which makes retrieval easy (the authors acknowledge this as a confounder for k); no reported intervals, paired tests or repeated seeds in the main text I read; scores are LLM-judge or exact match, so the "past performance" is noisy; no minimum-evidence rule, calibration of the estimates or uncertainty on them is described; single-turn queries only; latency and load are not modelled, only cost.

## 7. Relevance to the AI Request Router
- This is the closest published support for the guide's choice of k-NN over past per-model outcomes as the competence estimate (RQ1) and for treating a learned classifier as optional.
- Reuse: k around 40 as a starting point with a sweep over about 10–80; cosine similarity over sentence embeddings; routing by estimate minus a cost penalty; evaluation with cost-quality curves and an oracle; the 1%-data and paraphrase stress tests as a template for a cold-start and robustness check; the point that new models need only to be run on the stored history.
- What the project must decide that this paper leaves open: similarity weighting (the paper's plain k-NN uses none, ContextualRouter learns weights), a minimum-evidence rule (how many sufficiently similar neighbours before an estimate is trusted), calibration (reliability table, Brier score) of the estimates, and a lower-bound rule.
- Not covered: multi-turn sessions, switching, budget enforcement, latency or live load.
- Links: [RouterBench](../07-testing-and-benchmarking/hu-2024-routerbench.md) and [EmbedLLM](../07-testing-and-benchmarking/zhuang-2025-embedllm.md) supply the data; [Šakota et al. (2024)](../02-prompt-difficulty/sakota-2024-fly-swat-or-cannon.md) is the trained-predictor alternative.

## 8. How to use it in the report
- Chapter 2 on competence estimation (retrieval versus trained predictors) and the design rationale for k-NN in Chapter 3.
- Sentence: "Varangot-Reille et al. (2026) found that a plain k-NN average over similar past queries performs as well as learned retrieval-based routers and stays effective with 1% of the history, which supports a retrieval-based competence estimate that needs no retraining for new models."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Varangot-Reille et al. (2026) | Generalisable routing to new models without retraining | ContextualRouter (attention over k nearest past queries) versus plain k-NN; cost penalty λ | SPROUT, RouterBench, LiveBench, BigGenBench, EmbedLLM, FusionBench | k-NN as good as learned routers; works with 1% history; k > 40 no gain; embedding size irrelevant | Flawed labels, easy retrieval on benchmarks, no calibration or intervals, single turn |
