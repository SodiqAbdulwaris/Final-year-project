Status: DRAFT
Depends on: D08; D12
Sources: Primary URLs in source table and proposal-audit section
Open items: Scoped numerical/final-version checks recorded below

# Speculative decoding (Leviathan et al., 2023)

| Field | Value |
|---|---|
| Topic (home) | 05 Latency and speed |
| Also relevant to | 04 Cost reduction (smaller-model drafts), 01 Routing (small-model/large-model pairing) |
| Paper type | method |
| Venue and status | peer-reviewed (40th ICML, PMLR 202, 2023); first on arXiv in November 2022 |
| Source read | full text (https://arxiv.org/pdf/2211.17192, v2) |
| Verified on | 2026-10-31, against the PMLR volume 202 page and arXiv 2211.17192 |
| Relevance to project | Medium |

## APA 7 reference
Leviathan, Y., Kalman, M., & Matias, Y. (2023). Fast inference from transformers via speculative decoding. In *Proceedings of the 40th International Conference on Machine Learning* (Vol. 202, pp. 19274–19286). PMLR. https://proceedings.mlr.press/v202/leviathan23a.html (no DOI issued by PMLR; preprint DOI: https://doi.org/10.48550/arXiv.2211.17192)

## In-text citation forms
(Leviathan et al., 2023) · Leviathan et al. (2023)

## 1. What it is about
Speculative decoding speeds up generation from a large language model without changing its output distribution. A small, fast "approximation" model guesses several next tokens; the large "target" model checks all guesses in one parallel pass and keeps those it would have produced itself.

## 2. The problem
Producing K tokens takes K serial passes of the model, and each pass is slow for large models. Most steps are memory-bandwidth-bound, so compute sits unused. Earlier speed-ups changed the architecture, needed retraining or altered the outputs.

## 3. Proposed solution
- **Algorithm.** Draft γ tokens with the small model Mq, run the target Mp once on all of them in parallel, accept the longest prefix that passes a *speculative sampling* test, and take one extra token from Mp. At least one token is produced per target pass.
- **Acceptance rate α.** The average probability that a guessed token is accepted; α = 1 − E[divergence between the two models' distributions] (Corollary 3.6). The expected number of tokens per target pass is (1 − α^(γ+1)) / (1 − α) (Eq. 1).
- **Speed-up formula.** With c the cost of a draft step relative to a target step, the expected wall-time improvement is (1 − α^(γ+1)) / ((1 − α)(γc + 1)) (Theorem 3.8). A gain exists whenever α > c, and is at least (1 + α) / (1 + c) at γ = 1 (Corollary 3.9).
- **Trade-off.** More parallel verification raises the total arithmetic work (Table 1: for example α = 0.8, γ = 5 gives 3.69× speed with 1.63× operations, if c = 0), which is acceptable only with spare compute.

## 4. Data, models and tools
- T5-XXL (11B) as target for English–German translation and CNN/DM summarisation, with T5-small, base and large as approximation models; single TPU-v4, batch size 1, with both argmax (temperature 0) and standard sampling.
- Acceptance rates also measured for a GPT-like 97M decoder on lm1b and for LaMDA 137B on dialogue.

## 5. Key results
- Abstract: 2×–3× faster than the standard T5X implementation with identical outputs.
- Table 2: T5-small as drafter is best, giving 3.4× (translation, temperature 0), 2.6× (temperature 1), 3.1× and 2.3× (summarisation). Using T5-large as drafter gave only 1.4×–2.2×, because it is costlier (higher c).
- Table 3: drafters about two orders of magnitude smaller than the target give α between about 0.5 and 0.9; trivial unigram and bigram drafters give α of 0.03–0.23. Acceptance is higher at temperature 0 than at 1.

## 6. Limitations
- *Stated by authors:* the extra arithmetic matters when compute is scarce; the oracle-γ gain is left to future work.
- *My observations:* measured at batch size 1 on TPUs with T5, so benefit under a busy multi-request GPU server (large batches, little spare compute) is not shown here; speed-up depends on how well the drafter fits the task; no queueing or multi-user effects.

## 7. Relevance to the AI Request Router
- **Predicting per-backend latency:** time per output token (TPOT) is not fixed per model. A backend using speculative decoding has TPOT that varies with acceptance rate, which depends on the task and sampling temperature, so the router should measure TPOT empirically (and per task type) rather than assume a model-level constant. The vLLM metrics design document lists speculative-decoding acceptance-rate and efficiency gauges (marked legacy); I did not check them on a running server.
- **Design echo:** a small model drafting for a large one is the same pairing logic as the router's small-versus-large model choice, though here the large model always verifies, so quality is unchanged. Compare [Dekoninck et al.](../04-cost-reduction/dekoninck-2025-cascade-routing.md) for cascades where quality can change.
- **Not covered:** serving under load, queueing, routing.

## 8. How to use it in the report
- Background on decode-latency optimisations; a short note that latency measured at the router depends on such backend features.
- Synthesis sentence: "Speculative decoding (Leviathan et al., 2023) reduces decode latency 2–3× without changing outputs, but the gain depends on acceptance rate, so per-backend TPOT should be measured, not assumed."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Leviathan et al. (2023) | Faster autoregressive decoding without changing outputs | Draft with small model, verify in parallel, speculative sampling | T5-XXL, T5-small/base/large, LaMDA, TPU-v4 | 2×–3× speed-up, identical outputs | Batch size 1; compute overhead; task-dependent acceptance |


## 2026-10-31 proposal audit

- Source attempted: https://arxiv.org/abs/2211.17192.
- Scope: Abstract/metadata check only in this session; detailed numerical results remain unchecked.
- Historical Source read above records the earlier session, not a claim of a fresh full reading.
- arXiv title matched: Fast Inference from Transformers via Speculative Decoding. Latest listed version: v2; arXiv DOI identifies the preprint, not peer review. A missing journal reference does not prove that no published version exists.
