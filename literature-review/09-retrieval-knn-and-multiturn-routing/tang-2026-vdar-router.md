# VDAR-Router: retrieving past performance by verbalised difficulty (Tang et al., 2026)

| Field | Value |
|---|---|
| Topic (home) | 09 Retrieval, k-NN and multi-turn routing |
| Also relevant to | 02 Prompt difficulty prediction, 07 Testing and benchmarking |
| Paper type | method |
| Venue and status | arXiv preprint (v2, Aug 2026); the arXiv comment says "Accepted by EMNLP 2026 Findings", but I could not find a proceedings entry, so cite it as a preprint until one exists |
| Source read | full text (https://arxiv.org/pdf/2607.18098v2); appendices skimmed |
| Verified on | 2026-10-31, against the arXiv abstract page and PDF |
| Relevance to project | Medium |

## APA 7 reference
Tang, Y.-C., Hung, J.-C., Peng, W.-C., & Yen, A.-Z. (2026). *VDAR-Router: Adaptive LLMs routing via verbalized query difficulty analysis retrieval* (arXiv:2607.18098). arXiv. https://doi.org/10.48550/arXiv.2607.18098

## In-text citation forms
(Tang et al., 2026) · Tang et al. (2026)

## 1. What it is about
VDAR-Router is a training-free router that, for each incoming query, first has a small LLM write a short "difficulty analysis" (which capabilities are needed and at what level). It then retrieves past queries whose analyses are similar and picks the model with the best reward (quality minus cost) on those neighbours. It reports better cost-performance trade-offs than several baselines on three datasets.

## 2. The problem
Retrieval routers compare the raw query embedding with past queries, but two queries can look alike on the surface and need different capabilities (a personal website versus an e-shop), or look unrelated and be equally easy (two one-step arithmetic questions). Surface similarity therefore picks the wrong neighbours as evidence of model competence.

## 3. Proposed solution
1. **Difficulty analysis.** A "Difficulty Analyst" LLM scores the query along seven capability dimensions: reasoning, comprehension, instruction following, agentic ability, knowledge retrieval, coding and multilingual ability. This is done offline for all training queries, embedded and stored in a vector database (FAISS).
2. **Retrieval at request time.** The incoming query gets the same analysis, which is embedded and used to retrieve the top-k most similar analyses (k = 30).
3. **Reward ranking.** For each candidate model, average over the k neighbours: R(m | q) = α·performance − β·cost, with α + β = 1 and both normalised to [0, 1]. The router selects the model with the highest R, which stops it from always choosing the strongest, most expensive model.

The method needs no training, only a stored history of per-model performance and cost.

## 4. Data, models and tools
- RouterBench (10,000 queries, 11 models sampled) and LLMRouterBench (12,732 queries, 11 models) with an 80/20 train/test split; ArenaExpert5K (2,678 queries, 105 models) which has only pairwise human preferences, so it is scored with pairwise accuracy and Spearman correlation against an Elo ranking.
- Difficulty Analyst: Gemma4-31B (and Qwen3.5-4B on ArenaExpert5K), and a small Qwen3.5-2B for the deployment test; embeddings from Qwen3-Embedding-0.6B.
- Baselines: KNN (Stripelis et al., 2024), RouteLLM (MLP variant), RouterDC, IRT-Router, ICL-Router, plus always-smallest and always-largest models.
- Seed 42, temperature 0, one run per setting; two RTX A6000 GPUs. Code: https://github.com/NYCU-NLP-Lab/VDAR-Router.

## 5. Key results
- On RouterBench and LLMRouterBench it reaches the best combined reward under both (α, β) settings of (0.8, 0.2) and (0.6, 0.4), without having the highest raw performance; it cuts cost sharply compared with the highest-performing baselines (RouterDC, ICL-Router). The text says the advantage holds with the 2B analyst. I did not extract exact table values because the extracted table was garbled.
- On ArenaExpert5K it beats the baselines in pairwise accuracy and rank correlation; with a 50:50 split IRT-Router is competitive but VDAR-Router still leads.
- k and weights (Figure 3): k from 5 to 30 and α from 0.3 to 0.9 were swept; a larger α (more weight on quality) generally improves performance and pairwise accuracy.
- Retrieval quality (Section 5.4): retrieved neighbours are closer in Rasch difficulty to the query than random or query-embedding neighbours.
- Overhead (Table 5, Qwen3.5-2B analyst): mean routing latency 1.46 s per query, of which difficulty analysis generation takes 1.43 s, embedding 0.021 s, FAISS retrieval 0.004 s and reward ranking 0.0001 s.

## 6. Limitations
Stated by the authors: the method depends on the accuracy of the generated difficulty analysis, and generating it at test time adds latency; mitigation (a small model producing latent analysis tokens) is future work.

Identified by me: a single seed and a single split, with no intervals or paired tests reported; the expensive step (an LLM call per request) is the opposite of the cheap pre-call classifier the project wants, and 1.46 s is large relative to the response time of a small model; results rely on benchmark labels (judge or exact match) and on a sampled subset of RouterBench; no calibration of the reward estimates, no minimum-evidence rule and no session or switching logic.

## 7. Relevance to the AI Request Router
- Evidence that what is retrieved matters: neighbours chosen by similarity of the *task profile* can give better routing than neighbours chosen by raw text similarity, which bears on the guide's similarity-weight decision for k-NN. It is a candidate comparator for E1, not an MVP dependency.
- Reuse: the reward form (α·quality − β·cost over retrieved neighbours); the latency breakdown showing that embedding plus FAISS retrieval costs about 25 ms while an LLM analyst costs over a second, which is a useful number for the gateway-overhead experiment (E5); paired sweeps over k and α.
- Avoid: an LLM call per request on the hot path unless it is shown to pay for itself.
- What the project must decide that this paper leaves open: k (here 30, versus about 40 in [Varangot-Reille et al., 2026](varangot-reille-2026-contextualrouter.md)), the minimum evidence before trusting an estimate, and calibration of the neighbour-averaged score.
- Datasets: it uses [RouterBench](../07-testing-and-benchmarking/hu-2024-routerbench.md) and [LLMRouterBench](../07-testing-and-benchmarking/li-2026-llmrouterbench.md), the same two datasets the guide proposes for E1.
- Link to topic 02: difficulty analysis as a retrieval key is the verbalised cousin of the difficulty classifiers in [Zhu et al. (2025)](../02-prompt-difficulty/zhu-2025-llm-already-knows.md).

## 8. How to use it in the report
- Chapter 2 on retrieval-based competence estimation, as the "difficulty-aware retrieval" variant, and the E1 comparator discussion.
- Sentence: "Tang et al. (2026) retrieve past outcomes by the similarity of a generated difficulty analysis rather than the raw query, but the extra LLM call adds about 1.4 seconds per request, which a cheap embedding lookup avoids."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Tang et al. (2026) | Better neighbours for retrieval-based routing | LLM-written difficulty analysis as retrieval key; neighbour reward α·perf − β·cost | RouterBench, LLMRouterBench, ArenaExpert5K; Qwen3-Embedding, FAISS | Best reward on both benchmark datasets; analysis step is 1.43 of 1.46 s routing latency | Preprint, one seed, LLM call per request, no calibration or evidence rule |
