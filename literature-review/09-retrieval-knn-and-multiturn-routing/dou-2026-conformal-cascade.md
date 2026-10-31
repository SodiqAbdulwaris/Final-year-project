Status: DRAFT
Depends on: D08; D12
Sources: Primary URLs in source table and proposal-audit section
Open items: Scoped numerical/final-version checks recorded below

# Conformal Cascade: distribution-free accuracy guarantees for multi-tier inference (Dou et al., 2026)

| Field | Value |
|---|---|
| Topic (home) | 09 Retrieval, k-NN and multi-turn routing (calibration and uncertainty of success estimates) |
| Also relevant to | 01 Routing algorithms, 04 Cost reduction, 02 Prompt difficulty prediction |
| Paper type | method with a theoretical guarantee |
| Venue and status | preprint only (arXiv v3, July 2026); no peer-reviewed venue found on the arXiv page |
| Source read | full text (https://arxiv.org/pdf/2607.25018v3); proofs and appendices skimmed |
| Verified on | 2026-10-31, against the arXiv abstract page and PDF |
| Relevance to project | Medium |

## APA 7 reference
Dou, Y., Lian, S., & Li, S. (2026). *Conformal Cascade: Distribution-free accuracy guarantees for multi-tier LLM inference* (arXiv:2607.25018). arXiv. https://doi.org/10.48550/arXiv.2607.25018

## In-text citation forms
(Dou et al., 2026) · Dou et al. (2026)

## 1. What it is about
Conformal Cascade (CC) decides whether to accept a small model's answer or escalate to a bigger one by using split conformal prediction. The small model's answer set is accepted only if the calibrated prediction set shrinks to one answer. This gives a finite-sample, distribution-free bound on the error rate that a user can set as an error budget, instead of tuning a confidence threshold.

## 2. The problem
Cascades defer on a confidence threshold, but LLM confidence is miscalibrated (the paper cites Kadavath et al., 2022 and Xiong et al., 2024), thresholds must be tuned for each model pair and domain, and no setting gives a formal bound on cascade accuracy. A practitioner cannot say what threshold corresponds to "at most 5% wrong answers".

## 3. Proposed solution
1. **Score.** For each tier, sample N answers per query and define a nonconformity score for each candidate answer from the sampling frequencies.
2. **Calibration.** On a held-out labelled calibration set, take the ⌈(1 − α)(n + 1)⌉-th smallest score as the threshold q̂. The prediction set for a new query is all answers scoring at or below q̂. Under exchangeability, the set contains the true answer with probability at least 1 − α.
3. **Cascade rule.** Accept at the first tier whose set is a single answer; otherwise escalate. By a per-tier union bound the accepting tier's set covers the true answer with probability at least 1 − Kα (K = number of tiers), and under a "selection-preservation" condition the bound tightens to 1 − α. Expected cost is an explicit function of α and the calibration-set acceptance rate.

Needs only black-box access and no training; works for multiple-choice questions with a finite answer set (open-ended answers need a clustering step the authors leave for future work).

## 4. Data, models and tools
- Two-tier cascades (K = 2) from four open families: Llama, Gemma, Ministral, Phi; tier 1 is the smallest instruction-tuned checkpoint, tier 2 a much larger one from the same family. Served with vLLM, N = 16 samples per tier at temperature 0.7; costs fixed at c₁ = 1 and c₂ = 2.7.
- 18 multiple-choice benchmarks (science, medicine, commonsense, standardized exams, maths, multilingual reading), each split 30% calibration / 70% test with seed 42, giving 72 family–benchmark pairs.
- Baselines: always-weak, always-strong, agreement cascade (five thresholds), entropy cascade (four), random deferral (three). Learned routers (RouteLLM, Shnitzer, Hybrid LLM) are discussed but not run.

## 5. Key results
- Accuracy (Table 1): CC wins against the best heuristic cascade in 49 of the 72 pairs, with the largest gains on reasoning-heavy benchmarks (GPQA-Diamond, MathQA, MMLU-Pro, MMLU, TruthfulQA, MedMCQA, MedQA); on easy benchmarks the cascade commits most queries to the small model at no accuracy cost. Both methods are tuned by taking the argmax on the test set (CC grid of 15 settings, heuristic grid of 12), so gaps are at oracle-tuned operating points, not tuned on held-out data.
- Coverage (Table 2): at α = 0.10 on the Llama cascade, six of eight benchmarks meet the target within a ±0.02 band; MedMCQA (0.130) and ARC-Challenge (0.124) overshoot but stay inside the worst-case Kα bound of 0.20. Every reported cell satisfies the union bound; the empirical regime is between α and Kα, closer to α.

## 6. Limitations
Stated by the authors: the guarantee is marginal, not conditional on query difficulty or subgroup; it relies on calibration–test exchangeability from within-benchmark splitting, so covariate shift needs online recalibration; it needs a finite answer set; aggregate-only logs prevented bootstrap intervals, so differences under 0.5 percentage points on GPQA-Diamond (139 test items) are point estimates.

Identified by me: the method is post-generation (16 samples at each tier), so it is a cascade, not a pre-call router, and its cost per query is high; results use oracle-tuned operating points on the test set; only two tiers and multiple-choice tasks were tested; no latency, load or session behaviour; preprint.

## 7. Relevance to the AI Request Router
- Supplies the formal way to meet the guide's rule "never silently violate a guaranteed threshold": conformal calibration on a held-out scored set turns an error budget α into a threshold with a stated guarantee, and the guarantee is explicitly marginal and breaks under distribution shift. This is the closest model for a lower-bound rule on top of the k-NN estimate.
- Reuse (adaptations are mine): the split calibration protocol (hold out a calibration set separate from the retrieval history and from the test set), a coverage table at several α, and the practice of reporting empirical coverage with a finite-sample band.
- Cautions: the guarantee needs exchangeability, which fails if production prompts differ from the benchmark history; the project should recalibrate on logged traffic and report coverage per task type, not only overall.
- Not covered: retrieval, sessions, switching, local-model health.
- Links: complements the calibration findings in [Kadavath et al. (2022)](../02-prompt-difficulty/kadavath-2022-know-what-they-know.md) and [Xiong et al. (2024)](../02-prompt-difficulty/xiong-2024-llm-uncertainty-calibration.md), and the cascade methods in topic 04 ([Gupta et al., 2024](../04-cost-reduction/gupta-2024-token-uncertainty-cascades.md)).

## 8. How to use it in the report
- Chapter 2 on calibration and uncertainty of success estimates; Chapter 3 on the lower-bound quality rule and the calibration check.
- Sentence: "Dou et al. (2026) replace confidence thresholds with conformal prediction sets to obtain a finite-sample bound on cascade error, but the bound is marginal and assumes calibration and test data are exchangeable."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Dou et al. (2026) | Accuracy guarantee for LLM cascades | Split conformal prediction sets; accept when set is a single answer | 18 MC benchmarks, four open families, two tiers; 16 samples per tier | Beats best heuristic cascade in 49 of 72 pairs; coverage at α = 0.10 within ±0.02 in 6 of 8 Llama benchmarks | Marginal guarantee, exchangeability, MC only, test-tuned grids, preprint |


## 2026-10-31 proposal audit

- Source attempted: https://arxiv.org/abs/2607.25018.
- Scope: Abstract/metadata check only in this session; detailed numerical results remain unchecked.
- Historical Source read above records the earlier session, not a claim of a fresh full reading.
- arXiv title matched: Conformal Cascade: Distribution-Free Accuracy Guarantees for Multi-Tier LLM Inference. Latest listed version: v3; arXiv DOI identifies the preprint, not peer review. A missing journal reference does not prove that no published version exists.
