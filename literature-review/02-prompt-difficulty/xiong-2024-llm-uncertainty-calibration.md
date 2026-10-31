Status: DRAFT
Depends on: D08; D12
Sources: Primary URLs in source table and proposal-audit section
Open items: Scoped numerical/final-version checks recorded below

# Can LLMs express their uncertainty? Black-box confidence calibration (Xiong et al., 2024)

| Field | Value |
|---|---|
| Topic (home) | 02 Prompt difficulty prediction (added replacement paper, covers calibration) |
| Also relevant to | 06 Fallback and reliability |
| Paper type | empirical study / benchmark of methods |
| Venue and status | peer-reviewed (ICLR 2024; the PDF header reads "Published as a conference paper at ICLR 2024") |
| Source read | full text (https://arxiv.org/pdf/2306.13063v2) |
| Verified on | 2026-10-31, against the arXiv abstract page (comments field: accepted by ICLR 2024) and PDF; OpenReview URL taken from a web-search listing, not opened |
| Relevance to project | Medium |

## APA 7 reference
Xiong, M., Hu, Z., Lu, X., Li, Y., Fu, J., He, J., & Hooi, B. (2024). Can LLMs express their uncertainty? An empirical evaluation of confidence elicitation in LLMs. *The Twelfth International Conference on Learning Representations*. https://openreview.net/forum?id=gjeQKFxFpZ

(ICLR papers carry no DOI; arXiv DOI: https://doi.org/10.48550/arXiv.2306.13063.)

## In-text citation forms
(Xiong et al., 2024) · Xiong et al. (2024)

## 1. What it is about
The paper evaluates how well LLMs can report how likely their own answers are to be correct when only black-box access is available (no logits, no fine-tuning). It organises the methods into prompting, sampling and aggregation, and tests them for calibration and for predicting failures.

## 2. The problem
Systems that trust or escalate on a model's confidence need that confidence to be meaningful. White-box methods (token probabilities, hidden states) do not work for closed APIs, and the literature on black-box confidence was thin. The authors ask how reliable verbalised confidence and sampling consistency are.

## 3. Proposed solution
A three-part framework.

1. **Prompting.** How to ask for confidence: vanilla verbalised confidence, chain-of-thought, multi-step, Top-K (give K guesses with probabilities) and "human-inspired" variants.
2. **Sampling.** How to get multiple answers: self-random sampling (temperature), prompt variation, or misleading hints.
3. **Aggregation.** How to combine them: average confidence, consistency (agreement) between samples, and rank-based pairwise aggregation. Verbalised confidence can be folded into the consistency vote.

Evaluation uses two tasks. Calibration: expected calibration error (ECE) tests whether 80% confidence means 80% accuracy. Failure prediction: AUROC, plus AUPRC-positive and AUPRC-negative, tests whether confidence separates correct from incorrect answers.

## 4. Data, models and tools
- Datasets (eight, five types): commonsense (Sports Understanding, StrategyQA), arithmetic (GSM8K, SVAMP), symbolic (Date Understanding, Object Counting), professional knowledge (Professional Law from MMLU) and ethics (Business Ethics from MMLU).
- Models: Vicuna 13B, GPT-3 (175B), GPT-3.5-turbo, GPT-4 and LLaMA 2 70B.
- Code: https://github.com/MiaoXiong2320/llm-uncertainty.

## 5. Key results
- Verbalised confidence is overconfident: values cluster between 80% and 100%, often as multiples of 5, and accuracy within each confidence bin is far lower (Figure 2, GSM8K).
- Larger, more capable models are better calibrated and better at failure prediction, but still far from ideal.
- CoT and Self-Probing style prompts reduce overconfidence somewhat; sampling consistency and better aggregators (including adding verbalised confidence to the vote) improve failure prediction, especially on arithmetic.
- Best algorithms reach ECE as low as 0.028 (Table 4) but still struggle to detect wrong answers on professional-knowledge tasks such as Professional Law.
- White-box methods are better but the gap is narrow, "0.522 to 0.605 in AUROC" (abstract and Section 6).
- Practitioner recommendation: Top-K prompt plus self-random sampling plus average-confidence or pair-rank aggregation.

## 6. Limitations
Stated by the authors: focus on question answering with a unique ground-truth answer (no summarisation or open-ended QA); black-box methods remain suboptimal compared with white-box ones; combining them with limited white-box information is future work.

Identified by me: all methods are post-answer, so they need at least one generation (often several samples) per query, which defeats cost savings if used as the primary router; evaluated on 2023-era models and benchmark-style tasks; AUROC values near 0.5–0.6 mean the signals are weak in absolute terms.

## 7. Relevance to the AI Request Router
- Provides the evaluation vocabulary and cautions for the router's own difficulty or success-probability output: report ECE and AUROC, plot reliability diagrams, and do not trust a model's self-stated confidence without checking calibration.
- Supports the design choice of learning confidence from observed correctness (as in Kadavath et al., 2022; Chuang et al., 2025) rather than asking the LLM how sure it is.
- Reuse: ECE/AUROC/AUPRC protocol; sample-consistency as an optional offline label-quality check.
- Avoid: multi-sample consistency in the request path (cost and latency).
- Not covered: routing, cost, latency, load.

## 8. How to use it in the report
- A calibration subsection in 2.4 and the evaluation metrics subsection of Chapter 3 (why ECE and AUROC accompany accuracy).
- Sentence: "Xiong et al. (2024) found that LLMs state overly high confidence and that sampling consistency helps failure prediction, which motivates calibrating the router's predictor against observed outcomes."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Xiong et al. (2024) | Benchmark black-box confidence elicitation in LLMs | Prompting, sampling and aggregation strategies; ECE and AUROC evaluation | Eight QA/reasoning datasets; GPT-3/3.5/4, Vicuna 13B, LLaMA 2 70B | Overconfident verbalised scores; consistency and aggregation help; white-box only slightly better | Needs generation per query, unique-answer QA only, weak AUROC in hard domains |


## 2026-10-31 proposal audit

- Source attempted: https://arxiv.org/abs/2306.13063.
- Scope: Full-text sample: method and selected numerical/limitation statements checked; see L07.
- Historical Source read above records the earlier session, not a claim of a fresh full reading.
- arXiv title matched: Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs. Latest listed version: v2; arXiv DOI identifies the preprint, not peer review. A missing journal reference does not prove that no published version exists.
