# Learning to route LLMs with confidence tokens (Chuang et al., 2025)

| Field | Value |
|---|---|
| Topic (home) | 02 Prompt difficulty prediction |
| Also relevant to | 01 Routing algorithms, 04 Cost reduction, 06 Fallback and reliability |
| Paper type | method |
| Venue and status | peer-reviewed (ICML 2025, PMLR 267:10859–10878); an earlier arXiv version appeared as a NeurIPS 2024 ENLSP workshop paper |
| Source read | full text (https://arxiv.org/pdf/2410.13284v3, the ICML-era version) |
| Verified on | 2026-10-31, against arXiv and the PMLR page (proceedings.mlr.press/v267/chuang25b.html) |
| Relevance to project | Medium |

## APA 7 reference
Chuang, Y.-N., Sarma, P. K., Gopalan, P., Boccio, J., Bolouki, S., Hu, X., & Zhou, H. (2025). Learning to route LLMs with confidence tokens. In *Proceedings of the 42nd International Conference on Machine Learning* (Vol. 267, pp. 10859–10878). PMLR. https://proceedings.mlr.press/v267/chuang25b.html

(No DOI is issued for PMLR volumes; the arXiv DOI is https://doi.org/10.48550/arXiv.2410.13284.)

## In-text citation forms
(Chuang et al., 2025) · Chuang et al. (2025)

## 1. What it is about
Self-REF fine-tunes a small local LLM to append a "confident" or "unconfident" token after its answer. The probability of the confident token is used as a correctness score: when it is low, the query is sent on to a larger, costlier model or the system abstains.

## 2. The problem
Systems that want to escalate hard queries need a trustworthy confidence signal. Token probabilities are poorly calibrated, verbalised confidence ("I am 80% sure") is unstable across prompts and datasets, and sampling-consistency methods cost several generations and are not aligned with correctness. The authors want a cheap, learned signal that is tied to whether the answer is right.

## 3. Proposed solution
Self-REF has three steps (Figure 1).

1. **Annotation.** Run the base LLM on the training set. Append `<CN>` to the instance if its answer is correct and `<UN>` if it is wrong. These labels come from the model's own outcomes, so no human difficulty labelling is needed.
2. **Fine-tuning.** Fine-tune the base model on the augmented data so that a confidence token is generated after its answer (the two tokens have trainable embeddings; an ablation studies gradient masking).
3. **Score extraction.** Confidence = P(`<CN>`) / (P(`<CN>`) + P(`<UN>`)).

For routing, queries whose score falls below a threshold go to a larger LLM; the threshold sets the routing rate. For rejection learning, a low score means the system declines to answer.

## 4. Data, models and tools
- Datasets: MMLU, OpenbookQA, GSM8K, MedQA (rejection tests on MMLU and OpenbookQA).
- Local models: Llama3-8B-Instruct and Mistral-7B-v0.3-Instruct; escalation target: Llama3-70B-Instruct (not fine-tuned).
- Baselines: verbalised yes/no confidence (Tian et al., 2023), token-probability and fine-tuned-logit variants, evaluated with calibration metrics and routing rate.
- Cost measured as GPU hours and per-token latency, excluding network time between machines.

## 5. Key results
- Routing (Figure 2): with Llama3-8B, routing 39% of MMLU queries reaches accuracy comparable to using Llama3-70B alone; the routing rates needed for parity are 49%, 65% and 40% on OpenbookQA, GSM8K and MedQA. For Mistral-7B the rates are 70%, 50%, 75% and 70% on MMLU, OpenbookQA, GSM8K and MedQA.
- Latency (Table 1): per-token latency drops from 0.292 s for Llama3-70B alone to 0.145 s for the Self-REF/Llama3-8B system on MMLU (2.03× faster) at the same accuracy (0.739); other combinations give 1.2× to 2.0×.
- Self-REF gives the best accuracy-versus-routing-rate curve on all four datasets and both local models, and the best or near-best calibration in Table 2, according to the authors. The fine-tuned-logit baseline is usually second.
- The authors note that the routed system can beat the 70B model alone because the fine-tuned small model learns some knowledge the 70B model lacks and the two models make different errors.

## 6. Limitations
Stated by the authors: network transmission costs between machines are excluded and could change the savings; the right balance between routing/abstention and risk is application specific.

Identified by me: the confidence is produced *after* generating an answer, so the small model must run first on every query (the cost of a failed attempt is paid before escalating). It needs task-specific fine-tuning per base model and per domain, so generalisation to unseen task mixes is unclear. The routing target is a single larger model of the same family; there is no multi-model choice, no per-query price model and no live load. Latency numbers are per token from the authors' setup, not under concurrent traffic.

## 7. Relevance to the AI Request Router
- Supports a confidence/escalation path and the calibration discussion: it compares learned confidence against verbalised and token-probability confidence and reports calibration metrics alongside routing rate.
- Reuse: correctness-derived labels (no human annotation), routing-rate-versus-accuracy curves, parity routing rate as a headline metric.
- Avoid: copying the "generate first, then decide" pattern as the primary router; for the project's pre-call prediction it is a fallback or cascade layer instead.
- Not covered: pre-call prediction, multiple backends, load, latency budgets.

## 8. How to use it in the report
- Section 2.4 contrast between pre-call predictors (embedding classifiers) and post-generation confidence (cascade-style), and 2.5 on calibration.
- Sentence: "Chuang et al. (2025) learn a confidence token inside a small model, which routes well but only after the small model has already answered, unlike pre-call classifiers."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Chuang et al. (2025) | Reliable confidence for routing or abstaining | Self-REF: fine-tune with correctness-based confidence tokens, route on P(confident) | MMLU, OpenbookQA, GSM8K, MedQA; Llama3-8B, Mistral-7B, Llama3-70B | 39% of MMLU queries routed matches 70B accuracy; up to 2.03× lower per-token latency | Post-generation, per-task fine-tuning, one escalation target, no load |
