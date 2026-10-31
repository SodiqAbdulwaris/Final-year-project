# Routing reasoning problems by predicted difficulty (Zhao et al., 2025)

| Field | Value |
|---|---|
| Topic (home) | 02 Prompt difficulty prediction |
| Also relevant to | 01 Routing algorithms, 04 Cost reduction |
| Paper type | method (short workshop paper) |
| Venue and status | NeurIPS 2025 Workshop on Efficient Reasoning (workshop paper, not main conference); arXiv preprint |
| Source read | full text (https://arxiv.org/pdf/2511.03808; 4 pages of body text plus appendix) |
| Verified on | 2026-10-31, against arXiv abstract page (comments field names the workshop) |
| Relevance to project | Medium |

## APA 7 reference
Zhao, B., Kapusuzoglu, B., Balasubramaniam, K., Sahu, S., Chakraborty, S., & Winata, G. I. (2025). *Optimizing reasoning efficiency through prompt difficulty prediction* (arXiv:2511.03808). arXiv. https://doi.org/10.48550/arXiv.2511.03808

## In-text citation forms
(Zhao et al., 2025) · Zhao et al. (2025)

## 1. What it is about
The paper trains small neural classifiers on a language model's intermediate activations to predict either a math problem's difficulty level or whether each of several models will answer it correctly. These predictions route each problem to the smallest reasoning model expected to solve it.

## 2. The problem
Reasoning models are accurate but slow and expensive, and many problems do not need them. Earlier routing for reasoning relied on hand-designed, task-specific difficulty measures (the authors cite the number of obstacles in a maze as an example). The paper asks whether a general learned predictor can replace them.

## 3. Proposed solution
Two predictors share the same input: the layer-45 activations (dimension 5120) of the reasoning model s1.1-32B for the prompt.

1. **Difficulty-level predictor.** A 3-layer MLP (hidden sizes 256 and 64, cross-entropy loss) is trained on MATH, which labels 7,500 competition problems from level 1 to 5 (6,000 train / 1,500 validation). Routing sends a problem to the larger model if predicted difficulty exceeds a threshold, otherwise to the smaller one.
2. **Correctness predictor.** A 4-layer MLP (hidden sizes 8192, 2048, 128, binary cross-entropy) predicts for each candidate model whether it answers correctly. Routing sends the problem to the smallest model whose predicted correctness is above a threshold.

Layer choice was explored: middle layers gave the best prediction (Figure 2), so layer 45 was used. Only one model (s1.1-32B) is used to produce the features for all candidates, which assumes its notion of difficulty carries over to the others.

## 4. Data, models and tools
- MathCombined: 3,136 problems from AIME24, AMC23, GSM8K, Minerva, OlympiadBench and TheoremQA, split 1,882 train / 626 validation / 628 router evaluation. It has ground-truth answers but no difficulty labels.
- Models: eight were profiled for the correctness predictor (Mixtral-8x7B-Instruct, OLMo-2-7B-Instruct, Llama-3.1-8B-Instruct, phi-4, Llama-3.1-Nemotron-Nano-8B, Llama-3.3-70B-Instruct, Llama-3.3-Nemotron-Super-49B and s1.1-32B). Appendix B removes Mixtral and Llama-3.1-8B (both non-reasoning) and Nemotron-Nano from the router pool because they were off the accuracy–time trend.
- Baselines: each single model, and random assignment between two models. No code link found in the paper.

## 5. Key results
- Middle layers of s1.1-32B are the most informative for both predictions (Figure 2).
- Difficulty-based routing beats random assignment between two models on the accuracy–time plane for thresholds between 2.1 and 2.9 (Figure 3).
- Correctness-based routing reaches comparable and even slightly better accuracy than s1.1-32B while using about two-thirds of the inference compute (Figure 4, Section 4).
- Appendix C reports similar results when the features come from a smaller model (Llama Nemotron 8B), but I did not extract numbers.
- Exact accuracy values per threshold are only in plots, so none are quoted here.

## 6. Limitations
Stated assumption and future work (the paper has no limitations section): features come from one representative model rather than from each candidate, on the assumption that difficulty patterns generalise across similar architectures; future work should analyse the embedding space, try similarity-based routing, and go beyond a single model.

Identified by me: math-only evaluation; very short paper with results shown mainly in figures and no confidence intervals or repeated runs; inference "cost" is measured as average seconds per question on the authors' own setup, not as money or under concurrent load; the 32B feature extractor is expensive for a gateway; the training set for the correctness predictor is only 1,882 problems; workshop-level evidence, so treat claims cautiously.

## 7. Relevance to the AI Request Router
- Supports the idea of two predictor types for the classifier: "difficulty level" versus "will model X be correct". The second matches the router's per-model quality estimate and avoids needing human difficulty levels.
- Reuse: threshold-based routing, sweeping thresholds to trace a cost–quality curve, and the observation that every model fails on some problems another model solves.
- Avoid: using a 32B model's activations as the router input.
- Not covered: non-math prompts, live load, latency budgets, failover.

## 8. How to use it in the report
- Section 2.4, pairing difficulty prediction with model selection; also useful as a small example of threshold sweeping for the evaluation design.
- Sentence: "Zhao et al. (2025) show that a lightweight classifier on intermediate activations can route math problems among reasoning models, though only in a workshop-scale evaluation."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Zhao et al. (2025) | Route reasoning problems to the smallest capable model | MLP probes on s1.1-32B layer-45 activations predicting difficulty or correctness | MATH (difficulty labels); MathCombined (3,136 problems); eight open models profiled, five in the router pool (Appendix B) | Beats random routing; about equal to s1.1-32B at roughly two-thirds of compute | Math only, 32B features, workshop paper, no live load or money cost |
