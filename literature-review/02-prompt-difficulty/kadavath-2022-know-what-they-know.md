Status: DRAFT
Depends on: D08; D12
Sources: Primary URLs in source table and proposal-audit section
Open items: Scoped numerical/final-version checks recorded below

# Language models (mostly) know what they know (Kadavath et al., 2022)

| Field | Value |
|---|---|
| Topic (home) | 02 Prompt difficulty prediction |
| Also relevant to | 01 Routing algorithms, 06 Fallback and reliability |
| Paper type | empirical study (with a training method for P(IK)) |
| Venue and status | preprint only (arXiv v4, Nov 2022, Anthropic); no peer-reviewed venue found |
| Source read | full text (https://arxiv.org/pdf/2207.05221v4) |
| Verified on | 2026-10-31, against arXiv abstract page and PDF |
| Relevance to project | Medium |

## APA 7 reference
Kadavath, S., Conerly, T., Askell, A., Henighan, T., Drain, D., Perez, E., Schiefer, N., Hatfield-Dodds, Z., DasSarma, N., Tran-Johnson, E., Johnston, S., El-Showk, S., Jones, A., Elhage, N., Hume, T., Chen, A., Bai, Y., Bowman, S., Fort, S., . . . Kaplan, J. (2022). *Language models (mostly) know what they know* (arXiv:2207.05221). arXiv. https://doi.org/10.48550/arXiv.2207.05221

## In-text citation forms
(Kadavath et al., 2022) · Kadavath et al. (2022)

## 1. What it is about
The paper asks whether a language model can tell when it is right. It shows that large models are well calibrated on multiple-choice questions when formatted well, that they can judge their own sampled answers (P(True)), and that a model can be trained to predict, from the question alone, the probability P(IK) that it will answer correctly.

## 2. The problem
If systems are to act on a model's confidence (abstain, escalate, ask for help), the confidence must match reality. Earlier calibration work covered mostly classification or token probabilities. The authors want to know whether this extends to open-ended generation and whether a model can predict its own success *before* answering.

## 3. Proposed solution
Three layers of evidence.

1. **Calibration on multiple choice.** Plot predicted probability against observed accuracy across BIG-Bench multiple-choice tasks, MMLU, TruthfulQA, LogiQA and QuALITY. Larger models and few-shot prompts improve calibration. Replacing an option with "none of the above" hurts both accuracy and calibration, and RLHF-tuned policies are miscalibrated but can be fixed with temperature tuning.
2. **P(True), self-evaluation.** The model proposes an answer, then is asked whether it is correct. Showing the model several of its own samples before asking improves self-evaluation.
3. **P(IK), "I know".** A binary value head is added to the language model and the whole model is fine-tuned to predict P(IK) from the question only. Ground-truth P(IK) for training is the fraction of 30 temperature-1 samples that are correct. The score is read at the last token of the question, so it is available before any answer is generated.

## 4. Data, models and tools
- Models: a family of 800M, 3B, 12B and 52B parameter language models, pretrained on 850B tokens, with architecture like Bai et al. (2022). Not released.
- Sampling tasks: TriviaQA, Lambada, GSM8K, Codex HumanEval, arithmetic and scraped Python function synthesis problems.
- P(IK) trained on TriviaQA (10-shot prompts) and tested out of distribution on the others; also trained directly on Lambada, arithmetic and function synthesis.
- Metrics: calibration charts with equal-count bins, expected calibration error (10 bins), RMS error, AUROC.
- No public code in the text I read.

## 5. Key results
- Larger models are well calibrated on diverse multiple-choice tasks, and calibration improves with size and few-shot prompting (Section 2).
- A P(IK) classifier trained on TriviaQA separates questions the model answers correctly from those it gets wrong and is very well calibrated on TriviaQA (Figure 12).
- Out of distribution it keeps useful discrimination on maths, Lambada and code questions but is poorly calibrated there (Figures 12–13, Section 1.1), so generalisation is partial.
- P(IK) rises when relevant source material or correct hints are added to the context and falls with distracting hints (Figures 18–19).
- Two models of similar capability but different pretraining data are "somewhat better" at predicting their own P(IK) than the other model's (Figure 20).
- The paper does not report a single headline accuracy figure for P(IK); results are in figures.

## 6. Limitations
Stated by the authors: focus on pretrained models (RLHF policies are less well calibrated); the work does not separate "the truth" from "what humans say"; deception is not addressed; only five sampling datasets were studied, so conclusions on scale trends and generalisation are limited in power and scope.

Identified by me: the authors themselves note a confound that P(IK) may reflect "how hard is this question in general" rather than "does this model know it" (footnote 2, partly examined in Section 5.5). Models are Anthropic-internal and the data is 2022-era, with no instruction-tuned chat models or modern multi-model pools. The predictor is the full LM fine-tuned with a value head, so it costs a forward pass of the large model.

## 7. Relevance to the AI Request Router
- Foundational evidence for the project's central assumption: a model can estimate a question's difficulty (its own success rate) from the prompt alone, before generating, and this estimate can be calibrated.
- Reuse: training labels as the fraction of correct samples (a soft label without human annotation), calibration charts and ECE for evaluating the router's probability output, and the warning that calibration degrades out of distribution.
- Avoid: assuming a fine-tuned giant model is needed for the predictor; the project will use a small encoder.
- Not covered: routing across models, cost, latency, live load.

## 8. How to use it in the report
- Section 2.4 (difficulty as predicted success probability) and the calibration discussion.
- Sentence: "Kadavath et al. (2022) showed that a language model can predict, before answering, the probability that it will answer correctly, but this estimate was poorly calibrated outside its training distribution."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Kadavath et al. (2022) | Can an LM predict whether it will answer correctly? | Calibration study, P(True) self-evaluation, P(IK) value head trained on sampled correctness | BIG-Bench, MMLU, TriviaQA, GSM8K, HumanEval; 800M–52B models | Calibrated on MC; P(IK) discriminates and generalises partially but is miscalibrated OOD | Preprint, 2022 pretrained models, difficulty confound, no routing or cost |


## 2026-10-31 proposal audit

- Source attempted: https://arxiv.org/abs/2207.05221.
- Scope: Abstract/metadata check only in this session; detailed numerical results remain unchecked.
- Historical Source read above records the earlier session, not a claim of a fresh full reading.
- arXiv title matched: Language Models (Mostly) Know What They Know. Latest listed version: v4; arXiv DOI identifies the preprint, not peer review. A missing journal reference does not prove that no published version exists.
