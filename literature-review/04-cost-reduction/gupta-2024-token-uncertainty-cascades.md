# Language model cascades: token-level uncertainty (Gupta et al., 2024)

| Field | Value |
|---|---|
| Topic (home) | 04 Cost reduction |
| Also relevant to | 02 Difficulty prediction, 01 Routing algorithms |
| Paper type | method (empirical study) |
| Venue and status | peer-reviewed (ICLR 2024 poster); the arXiv page itself lists no venue |
| Source read | full text, arXiv v1 (https://arxiv.org/pdf/2404.10136) |
| Verified on | 2026-10-31, against the arXiv abstract page, the ICLR 2024 poster listing and the citation in Dekoninck et al. (2025) |
| Relevance to project | Medium |

## APA 7 reference
Gupta, N., Narasimhan, H., Jitkrittum, W., Rawat, A. S., Menon, A. K., & Kumar, S. (2024). Language model cascades: Token-level uncertainty and beyond. In *The Twelfth International Conference on Learning Representations*. https://openreview.net/forum?id=KgaBScZ4VI (preprint DOI: https://doi.org/10.48550/arXiv.2404.10136)

## In-text citation forms
(Gupta et al., 2024) · Gupta et al. (2024)

## 1. What it is about
A systematic study of how a small language model should decide to hand an input to a larger one. For classification, the small model's confidence works well. For text generation the output is a sequence of token probabilities, and the way these are summarised changes which queries are deferred.

## 2. The problem
The classic rule defers when the predicted-class probability is low (Chow's rule). Naively carried over to generation, the sum of token log-probabilities (Chow-Sum) is biased against long outputs, and the length-normalised average (Chow-Average) over-corrects and defers short outputs. Both hide a few very uncertain tokens inside many easy ones.

## 3. Proposed solution
- **Chow-Quantile:** take a quantile (for instance the minimum, 0.4, or 0.8) of the per-token log-probabilities as the deferral score. Different quantiles catch different failures: the minimum flags repetition and unknown tokens, the 0.8 quantile flags short, uncertain answers.
- **Post-hoc deferral rule:** since no single quantile wins everywhere, train a small model (5-layer MLP) on the quantile vector plus the sum and average scores to predict whether the large model would do better. Labels come from the large model's correctness (logistic loss) or the BLEURT difference for translation (squared loss).
- **Embeddings:** optionally add the small model's final decoder embedding (Post-Hoc-Embed-1) and an intermediate large-model embedding of the first token (Embed-1+2).

**Cost model.** Two-model cascade with per-example costs c(1) for the small model and c(2) for the large one. A deferred input pays both: cost = c(1) + 1[defer]·c(2), so average cost = c(1) + D·c(2) for deferral rate D (Section 2). The threshold t is chosen to meet the budget. Costs are abstract (the paper mentions latency); no dollar prices or GPU-hour figures are given.

## 4. Data, models and tools
- FLAN-T5 family (Small 80M to XXL 11B), mainly Base → Large, few-shot and greedy decoding.
- 17 task sets in Table 1: ANLI (three rounds), BoolQ, IMDb, Lambada, MNLI, PIQA, SQuAD, TriviaQA, TyDiQA (three languages), Winogrande and three WMT translation pairs.
- Metric: area under the deferral curve (AUC-DF); numbers averaged over 5 runs.

## 5. Key results (Table 1, AUC-DF, with % change over random deferral)
- MNLI: Chow-Sum 0.627 (−2.63%), Chow-Quantile-0.8 0.691 (+7.29%), Post-Hoc-Quantile 0.711 (+10.4%), Post-Hoc-Embed-1+2 0.722 (+12.24%).
- TriviaQA: Chow-Sum 0.073 (−13.09%, worse than random), Post-Hoc-Quantile 0.097 (+15.47%), Embed-1+2 0.100 (+19.56%).
- ANLI-R1: Chow-Sum 0.524 (+4.59%), Embed-1+2 0.563 (+12.51%).
- Sum and average scores are sometimes worse than random deferral; no fixed quantile is best across tasks; the learned rule is the most consistent, and the large-model embedding helps most on classification-style tasks.

## 6. Limitations
*Stated by the authors:* only encoder-decoder FLAN-T5; decoder-only models should be tested; RLHF-tuned models are known to be less calibrated, which may change the findings; extracting intermediate large-model embeddings has a non-trivial cost; a 5-layer MLP was used and sequence-aware models are left for future work.

*My observations:* it needs token log-probabilities from the small model, which hosted APIs may not expose and which the router would have to compute if it runs the small model itself. The deferral rule is trained per task with the large model's outputs as labels, so label generation itself costs large-model calls. Cost is abstract, with no load or dollar figures, and the benchmarks are classic NLP tasks rather than chat.

## 7. Relevance to the AI Request Router
- Gives a concrete, cheap **post-hoc confidence signal** for a self-hosted vLLM/Ollama small model: vLLM can return log-probabilities (my note, not from the paper), so a quantile-style feature vector can feed an escalate-or-stay decision.
- The deferral-rate cost identity (average cost = c1 + D·c2) is a simple budget-planning formula for the cheap-first tier.
- **Reuse:** quantile features; learned deferral on small features. **Avoid:** raw sequence probability as a confidence score. **Not covered:** more than two models, live load, hosted-API models without logprobs.

## 8. How to use it in the report
Section 2.4 (uncertainty-based cascading) and the failover and escalation design in Chapter 3. Synthesis sentence: "Gupta et al. (2024) show that naive sequence-level confidence is length-biased and propose learned deferral on token-level uncertainty, a signal Dekoninck et al. (2025) later adopt as their post-hoc quality estimator."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Gupta et al. (2024) | When should a small LM defer a generative task to a larger one? | Chow-Quantile scores; learned post-hoc deferral on token-probability quantiles and embeddings | FLAN-T5 Small to XXL; 17 NLP task sets (MNLI, TriviaQA, WMT, others) | Sum/average confidence can be worse than random; learned rule most consistent (e.g. MNLI +12.2% over random) | Encoder-decoder only; needs logprobs; abstract cost; two models |
