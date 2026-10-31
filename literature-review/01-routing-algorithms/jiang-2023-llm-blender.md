Status: DRAFT
Depends on: D08; D12
Sources: Primary URLs in source table and proposal-audit section
Open items: Scoped numerical/final-version checks recorded below

# LLM-Blender: pairwise ranking and generative fusion (Jiang et al., 2023)

| Field | Value |
|---|---|
| Topic (home) | 01 Routing algorithms |
| Also relevant to | 07 Benchmarks (MixInstruct), 04 Cost reduction (expensive baseline) |
| Paper type | method (ensembling) plus dataset |
| Venue and status | peer-reviewed (ACL 2023, long paper) |
| Source read | full text of arXiv v3 (https://arxiv.org/pdf/2306.02561) |
| Verified on | 2026-10-31, against the ACL Anthology (2023.acl-long.792) |
| Relevance to project | Medium |

## APA 7 reference
Jiang, D., Ren, X., & Lin, B. Y. (2023). LLM-Blender: Ensembling large language models with pairwise ranking and generative fusion. In *Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)* (pp. 14165–14178). Association for Computational Linguistics. https://doi.org/10.18653/v1/2023.acl-long.792

## In-text citation forms
(Jiang et al., 2023) · Jiang et al. (2023)

## 1. What it is about
LLM-Blender queries many open LLMs for every input, ranks their answers with a pairwise model (PairRanker) and merges the top few into a new answer (GenFuser). It is an ensemble, not a router, and later routers use it as the "call everything" reference and reuse its MixInstruct data.

## 2. The problem
No open LLM is best everywhere: in Figure 1 the first-ranked model changes by example (Vicuna first on 21.22%, no other model above about 13%). Earlier rerankers score each candidate alone and, the authors argue, miss subtle differences between strong, similar answers.

## 3. Proposed solution
1. Run N = 11 models to get candidates.
2. **PairRanker** (DeBERTa, 400M) reads the input with two candidates in one cross-attention encoder and says which is better. All N(N-1)/2 pairs (55) give a matrix; aggregation by MaxLogits (default), MaxWins or one bubble-sort pass (O(N) comparisons).
3. **GenFuser** (Flan-T5-XL, 3B) takes the input and the top K = 3 candidates and writes the final answer.

PairRanker trains on BARTScore-derived pairwise labels (best correlated with ChatGPT ranking, Table 3), 5 sampled pairs per input, with candidate order shuffled.

## 4. Data, models and tools
**MixInstruct:** 110K instructions (Alpaca-GPT4, Dolly-15K, GPT4All-LAION, ShareGPT), split 100K/5K/5K, outputs from 11 open LLMs, ChatGPT pairwise judgments as oracle. Metrics: BERTScore, BARTScore, BLEURT, GPT-Rank. Baselines: single LLMs, random, MLM-Scoring, SimCLS, SummaReranker, oracles. Code: https://github.com/yuchenlin/LLM-Blender (link live).

## 5. Key results (Table 2 unless stated)
- Best single LLM, Open Assistant: GPT-Rank 3.90, BARTScore -3.45.
- PairRanker alone: GPT-Rank 3.20, BARTScore -3.14; matches or beats Vicuna on 54.76% and Open Assistant on 57.79% of examples.
- Full LLM-Blender: GPT-Rank 3.01, BARTScore -3.02, BERTScore 79.09; matches or beats Vicuna on 70.73% and Open Assistant on 77.72%; top 3 on 68.59% of examples (Vicuna alone 52.88%).
- Table 3: PairRanker has the highest correlation with GPT-based ranking (Pearson 46.98, Spearman 44.98).
- Oracle top-1 selection by GPT-Rank scores BARTScore -3.33, better than the best single model, so selection has real headroom.

## 6. Limitations
**Authors:** O(N^2) ranker calls (bubble sort and parallelism help); no large-scale human evaluation, ChatGPT judges instead.
**Mine:** all 11 models run on every input, so cost and GPU load scale with N, which defeats cost-aware routing; latency is the slowest model plus ranker plus fuser; quality is similarity metrics and ChatGPT judging on instruction data, not task correctness; 2023 open chat models only; no failure handling.

## 7. Relevance to the AI Request Router
- Supports the *premise* of per-prompt model choice (Figure 1 and oracle numbers).
- Reuse: MixInstruct as instructions with multi-model candidates; pairwise comparison as an offline labelling idea; parallel candidates as an optional quality mode.
- Avoid: calling all models in the hot path.
- Not covered: cost, latency, load.

## 8. How to use it in the report
- Chapter 2, ensembling versus routing versus cascading.
- "LLM-Blender (Jiang et al., 2023) shows no single open model dominates but pays for every model per query; Hybrid LLM (Ding et al., 2024) and RouteLLM (Ong et al., 2025) pursue the same diversity with one call."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Jiang et al. (2023) | Exploit per-input differences between open LLMs | Pairwise ranker picks top-K; Flan-T5-XL fuses | MixInstruct (110K, 11 LLMs); ChatGPT ranking | GPT-Rank 3.01 vs 3.90 best single; top 3 on 68.59% | All N models run per query; ChatGPT-judged only |


## 2026-10-31 proposal audit

- Source attempted: https://arxiv.org/abs/2306.02561.
- Scope: Abstract/metadata check only in this session; detailed numerical results remain unchecked.
- Historical Source read above records the earlier session, not a claim of a fresh full reading.
- arXiv title matched: LLM-Blender: Ensembling Large Language Models with Pairwise Ranking and Generative Fusion. Latest listed version: v3; arXiv DOI identifies the preprint, not peer review. A missing journal reference does not prove that no published version exists.
