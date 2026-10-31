# RouterEval: routing LLMs and model-level scaling up (Huang et al., 2025)

| Field | Value |
|---|---|
| Topic (home) | 07 Testing and benchmarking |
| Also relevant to | 01 Routing algorithms, 02 Prompt difficulty prediction |
| Paper type | benchmark / empirical study |
| Venue and status | peer-reviewed (Findings of EMNLP 2025, pp. 3860–3887) |
| Source read | full text (https://arxiv.org/pdf/2503.10657v2); main text and tables read, appendices only skimmed |
| Verified on | 2026-10-31, against ACL Anthology (2025.findings-emnlp.208) and arXiv |
| Relevance to project | Medium |

## APA 7 reference
Huang, Z., Ling, G., Lin, Y., Chen, Y., Zhong, S., Wu, H., & Lin, L. (2025). RouterEval: A comprehensive benchmark for routing LLMs to explore model-level scaling up in LLMs. In *Findings of the Association for Computational Linguistics: EMNLP 2025* (pp. 3860–3887). Association for Computational Linguistics. https://doi.org/10.18653/v1/2025.findings-emnlp.208

## In-text citation forms
(Huang et al., 2025) · Huang et al. (2025)

## 1. What it is about
RouterEval is a large collection of per-input performance records of more than 8,500 LLMs on 12 evaluations, organised so that routers can be trained as multi-class classifiers. The authors also report a "model-level scaling up" effect: a good router's accuracy grows rapidly as more candidate models are added, even beating the best single model.

## 2. The problem
Existing router benchmarks have few candidate models, little evaluation diversity, or closed performance records. Without a large open pool, it is hard to study how routers behave as the candidate set grows, or to build strong routers that need much training data.

## 3. Proposed solution
**Formulation.** A pool of m LLMs and n inputs. For each input the label is a binary "selection vector" over the m models marking those that are best (all models that answer correctly count for correctness metrics; for continuous scores, any model within 95% of the best). A router is an m-way classifier over an input representation produced by an encoder (the paper provides features from Sentence-BERT, RoBERTa, last-layer RoBERTa and Longformer; RoBERTa is used in the experiments).

**Scaling study.** A synthetic router r_o(p) behaves like the oracle with probability p and picks uniformly otherwise. Sampling candidate subsets of size m (100 random subsets per m) shows that for p of about 0.5 or higher performance climbs quickly with m and can pass strong reference models such as GPT-4, and that pools of mostly weak models can still be promising.

**Candidate groups.** For m = 3 or 5 ("easy") and 10, 100, 1000 ("hard"), three pool types are built: all-strong (top 20% of models), all-weak (bottom 20%) and a strong-to-weak mix. The reported number is the average over them.

**Metrics.** μ_o (raw performance of the routed choices), V_R (μ_o divided by a reference strong model, such as GPT-4), V_B (μ_o divided by the best single model in the pool) and E_p (entropy of the router's selection distribution, to detect routers that always pick the same model).

## 4. Data, models and tools
- 12 evaluations: ARC, HellaSwag, MMLU, TruthfulQA, Winogrande, GSM8K, IFEval, BBH, GPQA, MUSR, MATH Lvl 5 and MMLU-PRO.
- More than 200,000,000 performance records from more than 8,500 LLMs; train/validation/test split 8:1:1; 4 pre-computed encoders.
- Router baselines: LinearR, MLPR, C-RoBERTa, MLC, PRknn, plus Random and oracle.
- Where the raw per-model scores came from is not stated in the main text I read. Code and data are on a project page (footnote 1), which I did not open.

## 5. Key results
- Scaling-up effect (Figure 2): routers with p ≥ about 0.5 improve fast with the number of candidates and can exceed the best single model.
- Table 1 (m = 3 and 5): existing routers have some classification ability above Random but fall behind the oracle and the best single model, and no router wins on every benchmark. For example on ARC with m = 3, the oracle scores 0.80, MLPR 0.61, C-RoBERTa 0.62 and Random 0.54. Some routers have low selection entropy, showing collapse onto a few models.
- Oracle performance with weak models is high: on MMLU with m = 10, each all-weak model is at most 0.3 accurate but the oracle reaches 0.95 (Section 4.2).
- Ranges V_R and V_B are mostly below or around 1 for learned routers.

## 6. Limitations
Stated by the authors: many candidates make deployment harder, although the best cost-effectiveness is with about 3–10 models; current data is still too small to train an excellent router, and most benchmark performance records are not open-source and are expensive to collect.

Identified by me: cost and latency are explicitly not modelled (Section 2 says performance only, with computational cost left to future work); labels are correctness on standard benchmarks (mostly multiple choice), so noise in free-form chat quality is not covered; the "oracle" labels assume independent correctness per model; pool composition (strong/weak groups) is synthetic; no live serving.

## 7. Relevance to the AI Request Router
- Useful for generalisation and failure-mode testing: it shows that routers collapse to a few models (entropy metric), that no router wins everywhere, and that results depend on pool strength. The project should test routing accuracy on more than one model pair, not only one strong/weak pair.
- Reuse: the m-way selection-vector label, oracle/random/best-single baselines, the V_B ratio, and the entropy-of-selection check.
- Does not cover: cost-quality curves, latency, load. It complements RouterBench ([Hu et al., 2024](hu-2024-routerbench.md)), which has cost but fewer models.
- Links to topic 02: the m-way classifier labels are the per-model correctness targets used by [Šakota et al. (2024)](../02-prompt-difficulty/sakota-2024-fly-swat-or-cannon.md) and [Routoo](../02-prompt-difficulty/mohammadshahi-2024-routoo.md).

## 8. How to use it in the report
- Section 2.7 (benchmarks) and the evaluation-design discussion of oracle upper bounds and pool-size sensitivity.
- Sentence: "RouterEval (Huang et al., 2025) shows that candidate-pool size and composition strongly affect router results, and that learned routers often collapse onto a few models, but it ignores cost and latency."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Huang et al. (2025) | Large open benchmark for routers and study of pool-size effects | m-way classification labels; pool groups of varying strength; μ_o, V_R, V_B, entropy | 12 evaluations, 8,500+ LLMs, 200M+ records; RoBERTa and other encoders | Model-level scaling up with capable routers; existing routers far below oracle | Performance-only, no cost or latency, benchmark-style tasks |
