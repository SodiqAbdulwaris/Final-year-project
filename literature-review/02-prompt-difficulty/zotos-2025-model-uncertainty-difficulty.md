Status: DRAFT
Depends on: D08; D12
Sources: Primary URLs in source table and proposal-audit section
Open items: Scoped numerical/final-version checks recorded below

# Model uncertainty plus text embeddings for item difficulty (Zotos et al., 2025)

| Field | Value |
|---|---|
| Topic (home) | 02 Prompt difficulty prediction |
| Also relevant to | 07 Benchmarks and evaluation (difficulty labels) |
| Paper type | method / empirical study |
| Venue and status | peer-reviewed (18th International Conference on Educational Data Mining, EDM 2025, long paper, pp. 77–89) |
| Source read | full text (arXiv v2, https://arxiv.org/pdf/2412.11831v2, same title and abstract as the EDM paper; I did not diff the two versions) |
| Verified on | 2026-10-31, against the EDM 2025 proceedings page and bib record (educationaldatamining.org) and arXiv |
| Relevance to project | Medium |

## APA 7 reference
Zotos, L., van Rijn, H., & Nissim, M. (2025). Are you doubtful? Oh, it might be difficult then! Exploring the use of model uncertainty for question difficulty estimation. In C. Mills, G. Alexandron, D. Taibi, G. Lo Bosco, & L. Paquette (Eds.), *Proceedings of the 18th International Conference on Educational Data Mining* (pp. 77–89). International Educational Data Mining Society. https://doi.org/10.5281/zenodo.15870153

## In-text citation forms
(Zotos et al., 2025) · Zotos et al. (2025)

Note: the supervisor's list described this paper vaguely ("Zotos et al. 2025"). It is the right paper; the same first author also has a COLING 2025 paper, "Can model uncertainty function as a proxy for multiple-choice question item difficulty?", which is the weaker correlation-only precursor and is not given its own file.

## 1. What it is about
The paper predicts how hard multiple-choice exam questions are for students, using a small Random Forest regressor over two kinds of features: a vector representation of the question and the uncertainty that several LLMs show when they answer it. The uncertainty features clearly improve over text alone.

## 2. The problem
Knowing an exam item's difficulty normally needs a field test with real students, which is slow and costly, and teachers estimate it poorly. Earlier automatic work used syntactic or semantic features with mixed success; at the BEA 2024 shared task, most systems barely beat simple baselines. The authors test whether LLM uncertainty is a usable proxy.

## 3. Proposed solution
Figure 1 shows the pipeline. Each question (stem plus choices) is encoded as TF-IDF unigrams and bigrams (up to 1,000 features) or as 768-dimensional BERT embeddings. Uncertainty is measured per LLM in two ways: the average probability the model gives to the correct choice's first token over ten random orderings of the choices, and "choice order sensitivity", the share of orderings in which the correct choice is picked. The per-model scores are concatenated with the text vector and fed to a scikit-learn Random Forest regressor with default settings. Optional extras are 17 linguistic features and the average cosine similarity between distractors and the correct answer (sentence-transformers). SHAP is used to explain which features matter.

## 4. Data, models and tools
- Datasets (difficulty = proportion of students answering correctly, or Rasch IRT difficulty for one set): Biopsychology (819 questions, private, 573 train/246 test), USMLE from the BEA 2024 shared task (667, 466/201), CMCQRD reading comprehension (793, 552/241).
- Nine open-source decoder-only instruction-tuned LLMs of different sizes and families, in default precision and 4-bit quantised form. Two A100 GPUs. Code is on GitHub (Leonidas Zotos / Are-You-Doubtful-Oh-It-Might-Be-Difficult-Then).
- Metric: RMSE on the test set, averaged over ten repetitions.

## 5. Key results (Table 3, RMSE, lower is better)
- Biopsychology: dummy baseline 0.1667; BERT text only 0.1498; both uncertainty features only 0.1460; BERT plus both uncertainty features 0.1365 (TF-IDF version 0.1359).
- USMLE: dummy 0.3110; best previous literature 0.291; BERT plus both uncertainty features 0.2864.
- CMCQRD (IRT metric): dummy 9.7568; best previous literature 8.5; BERT plus first-token probability 8.2763.
- First-token probability is a more useful signal than choice order sensitivity; combining both gives the best results. Text-only differences between methods are small, as in the shared task, but adding uncertainty consistently lowers RMSE and beats earlier published results on USMLE and CMCQRD (Section 5.1).
- Extra linguistic and similarity features help further except on Biopsychology (Section 5.2).

## 6. Limitations
Stated by the authors: uncertainty only helps when the LLM can answer the question without being overconfident, so strong models and easy (e.g. primary-school) questions are a problem; small LLMs are fragile to phrasing and choice order; only three exams were tested, and it is unknown whether it works for mathematical reasoning.

Identified by me: difficulty here means human student difficulty on factual MCQs, not model-to-model difficulty; running nine LLMs on every question is far too slow and costly to do per request in a gateway; improvements in RMSE are small in absolute terms; one dataset is private so it cannot be reproduced.

## 7. Relevance to the AI Request Router
- Directly relevant to the planned design: a text embedding fed to a classical scikit-learn model, plus a calibrated "how sure are LLMs about this" signal. It shows embedding-only features give small gains and model-confidence features give larger ones.
- Reuse idea: for the router, the uncertainty features could be pre-computed offline for training prompts and the cheap embedding classifier trained to predict them (distillation), keeping the request path light.
- Avoid: running multiple LLMs at request time to get uncertainty.
- Not covered: routing, cost, latency, general chat prompts, live load.

## 8. How to use it in the report
- Section 2.4, on feature choices for cheap difficulty estimators, and the label-source discussion (human student statistics versus model signals).
- Sentence: "Zotos et al. (2025) combined sentence embeddings with LLM uncertainty in a Random Forest, showing that model confidence adds information beyond text features, though only for exam questions."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Zotos et al. (2025) | Estimate MCQ difficulty without student field tests | Random Forest on TF-IDF/BERT features plus uncertainty from nine LLMs | Biopsychology, USMLE, CMCQRD; scikit-learn, SHAP | RMSE 0.1365 vs text-only 0.1498 (Biopsychology); beats prior bests on USMLE and CMCQRD | Exam MCQs only, many LLM calls, overconfident models weaken signal |


## 2026-10-31 proposal audit

- Source attempted: https://arxiv.org/abs/2412.11831.
- Scope: Abstract/metadata check only in this session; detailed numerical results remain unchecked.
- Historical Source read above records the earlier session, not a claim of a fresh full reading.
- arXiv title matched: Are You Doubtful? Oh, It Might Be Difficult Then! Exploring the Use of Model Uncertainty for Question Difficulty Estimation. Latest listed version: v2; arXiv DOI identifies the preprint, not peer review. A missing journal reference does not prove that no published version exists.
