# LLM routing learned from benchmark datasets (Shnitzer et al., 2023)

| Field | Value |
|---|---|
| Topic (home) | 01 Routing algorithms |
| Also relevant to | 07 Benchmarks, 02 Capability prediction |
| Paper type | method with empirical study |
| Venue and status | preprint (arXiv, one version). A shorter version, "LLM Routing with Benchmark Datasets", was at the NeurIPS 2023 DistShift workshop; no main-conference publication found |
| Source read | full text (https://arxiv.org/pdf/2309.15789) |
| Verified on | 2026-10-31, against arXiv and the ML Anthology workshop listing (OpenReview k9EfAJhFZc) |
| Relevance to project | Medium |

## APA 7 reference
Shnitzer, T., Ou, A., Silva, M., Soule, K., Sun, Y., Solomon, J., Thompson, N., & Yurochkin, M. (2023). *Large language model routing with benchmark datasets* (arXiv:2309.15789). arXiv. https://doi.org/10.48550/arXiv.2309.15789

## In-text citation forms
(Shnitzer et al., 2023) · Shnitzer et al. (2023)

## 1. What it is about
Per-question results from public benchmarks (HELM, MixInstruct) become training data for a router. For each LLM a binary classifier predicts whether it will answer a given input correctly, and the model with the best predicted correctness is recommended for a new task. Only the chosen LLM generates.

## 2. The problem
No LLM wins everywhere, and ranking methods (LLM-Blender, reward reranking) need outputs from every candidate, which does not scale to thousands of open models. Benchmarks report an average and discard the per-sample information that reveals each model's strengths.

## 3. Proposed solution
**Correctness predictors:** for each model m, g_m(x) estimates P(correct | x), trained on benchmark inputs with 0/1 labels; deliberately simple: sentence-transformer embeddings with k-nearest neighbours (k = 5). **Three scores** pick a model for a new task: S1, mean predicted probability; S2, share of inputs above a threshold (robust to poor calibration); S3, S2 corrected by the predictor's own estimated accuracy on the new task, p(d, m), predicted by kernel smoothing from a "distance to other tasks" descriptor, falling back to the best model on average unless 0.6 confident of a better one. A meta-learning argument (Lemma 4.1) says S3 has lower expected risk than S2.

## 4. Data, models and tools
HELM: 29 datasets, 18 open models (3B to 70B), leave-one-task-out. MixInstruct: 100K train, 5K test, 11 LLMs, compared with Jiang et al.'s rankers and log-likelihood. Baselines: best model on average (BMA, Llama-2-70B), log-likelihood scoring, oracle. Code release not stated.

## 5. Key results
- HELM (Table 1): S3 selects models with average accuracy 0.694 against 0.688 for BMA (oracle 0.773), at 49.8B average parameters against 70B. S3 with the true predictor accuracy reaches 0.735 at 33.8B, so estimating p(d, m) is the main lever.
- Predictors are weak out of distribution: average accuracy 0.59 (Section 5.1).
- With min(n_d, 50) in-domain labelled samples moved into training, predictor accuracy rises to 0.65 and all scores improve (Figures 2 and 6b).
- Routing among 13B models can match Llama-2-70B with about 2 to 40 labelled samples (Figure 4).
- MixInstruct (Table 2): one model call instead of N; does not consistently beat the compared methods.
- Figure 3: the router approaches the oracle on inputs close to training data.

## 6. Limitations
**Authors:** low out-of-distribution accuracy; depends on benchmark coverage; simple S3 correction; large variance from sampling in-domain points.
**Mine:** only kNN on frozen embeddings; open-ended chat judged by similarity metrics; no price, latency or load; S3 gain over BMA is only 0.006 accuracy on average; 2023 open models; selection is per task rather than per live request.

## 7. Relevance to the AI Request Router
- Supports the classifier design and the *generalisation risk*: it quantifies weak out-of-distribution predictors and the value of a few in-domain labels.
- Reuse: embeddings plus a lightweight classifier as a baseline; one correctness classifier per model (adding a model means one more classifier); leave-one-task-out evaluation; about 50 in-domain labels for calibration.
- Avoid: judging routers on averages only.
- Not covered: price beyond model size, live signals, failover.

## 8. How to use it in the report
- Chapter 2 classifier-based routing and generalisation; chapter 3 out-of-distribution evaluation protocol.
- "Shnitzer et al. (2023) route with per-model kNN correctness predictors but report weak out-of-distribution accuracy (0.59); RouteLLM (Ong et al., 2025) later closed part of that gap with augmentation."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Shnitzer et al. (2023) | Pick the best LLM for a new task from benchmark data | Per-LLM kNN correctness predictors; three scores, S3 corrects OOD error | HELM (29 datasets, 18 models), MixInstruct | Accuracy 0.694 vs 0.688 best on average, with smaller models; predictors 0.59 OOD | Task-level; small gain; no price, load; preprint/workshop only |
