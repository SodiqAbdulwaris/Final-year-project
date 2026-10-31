Status: DRAFT
Depends on: D08; D12
Sources: Primary URLs in source table and proposal-audit section
Open items: Scoped numerical/final-version checks recorded below

# Fly-swat or cannon: a small meta-model predicts which LM will succeed (Šakota et al., 2024)

| Field | Value |
|---|---|
| Topic (home) | 02 Prompt difficulty prediction (added replacement paper) |
| Also relevant to | 01 Routing algorithms, 04 Cost reduction |
| Paper type | method / framework |
| Venue and status | peer-reviewed (WSDM '24, 17th ACM International Conference on Web Search and Data Mining, pp. 606–615) |
| Source read | full text (arXiv v3, https://arxiv.org/pdf/2308.06077v3, which is in the ACM WSDM format) |
| Verified on | 2026-10-31, against the arXiv PDF header (ACM reference format and DOI) and a web search listing of the ACM DOI; the ACM page itself could not be opened by my fetch tool |
| Relevance to project | High |

## APA 7 reference
Šakota, M., Peyrard, M., & West, R. (2024). Fly-swat or cannon? Cost-effective language model choice via meta-modeling. In *Proceedings of the 17th ACM International Conference on Web Search and Data Mining* (pp. 606–615). Association for Computing Machinery. https://doi.org/10.1145/3616855.3635825

(Page numbers come from a web-search summary of the ACM and DBLP records and from a reference in another paper; the arXiv copy states "10 pages".)

## In-text citation forms
(Šakota et al., 2024) · Šakota et al. (2024)

## 1. What it is about
FORC ("fly-swat or cannon") predicts, from the text of a query alone, whether each of several candidate language models will answer it correctly. An assignment step then sends every query to the model that best trades predicted success against API price, within a user budget.

## 2. The problem
Bigger LMs cost much more (the authors compare GPT-4 8K with GPT-3.5 4K at about 20× the price), yet many queries do not need them. In the authors' data, 33% of samples are solved by both the biggest model and at least one smaller one, and 11% are solved only by smaller models. The difficulty is knowing in advance who will succeed without running every model. Cascades (FrugalGPT) run models in sequence and pay for failed attempts.

## 3. Proposed solution
1. **Meta-model.** A fine-tuned DistilBERT (66M parameters) reads the query with an appended token naming the target LM (for example "[LM_k]") and outputs the probability that this LM solves it. It is trained on existing query/outcome pairs. At inference it needs only the query, not the dataset or task name.
2. **Cost estimation.** Cost per query is computed from API prices and the average output length of each model (taken from the HELM runs), since real output length is unknown beforehand.
3. **Assignment strategies.** (a) Cost-oriented integer linear program: maximise total predicted performance within a budget. (b) Performance-oriented ILP: minimise cost subject to a minimum performance. (c) A greedy strategy that walks through queries until the budget runs out, and cost-insensitive options (performance maximisation, thresholding on the predicted probability). A query can be left unassigned. ILPs are solved with PuLP and the CBC solver in a fraction of a second.

## 4. Data, models and tools
- Data: raw HELM runs (Liang et al.) on 14 datasets covering five tasks, restricted to tasks with a binary right/wrong score (exact match, quasi-exact match, or mathematical equivalence).
- Candidate LMs: OpenAI text-ada-001, text-babbage-001, text-curie-001 and text-davinci-002, priced at $0.0004, $0.0005, $0.002 and $0.02 per 1k tokens.
- Meta-model training: 3,000 steps, batch size 16, learning rate 3×10⁻⁵, one Tesla T4 GPU, about 2 hours.
- Baselines: single models, an oracle assignment, and a dummy majority-class classifier that is given the dataset label. Code: https://github.com/epfl-dlab/forc.

## 5. Key results
- Meta-model (Table 3): overall meta-accuracy 81.57% versus 79.60% for the dummy classifier that knows the dataset. The gap is small because classes are imbalanced, but the dummy cannot be used in practice. The meta-model is well calibrated (Figure 2a).
- Leave-one-dataset-out retraining gives somewhat lower scores but the meta-model still generalises (Table 4).
- It is harder to predict outcomes for bigger LMs and for complex reasoning tasks (stratified results).
- Oracle assignment: 84.46% cheaper than always using text-davinci-002 and 10.74% more accurate (Figure 3). The cheapest model, text-ada-001, is 98.05% cheaper but 18.18% (absolute) less accurate.
- Framework: matches the largest LM's performance while cutting cost by about 63% (abstract; 62.79% in the conclusion, and 62.1% for the thresholding strategy in Section 4.2, so check which one you cite).

## 6. Limitations
Stated by the authors: I found no dedicated limitations section; the paper restricts itself to tasks with clear right/wrong answers.

Identified by me: the pool is four old OpenAI models from one family, so heterogeneity and modern open models are not tested. Cost uses average output length and list price, with no latency or load, and queries are assumed to be processed in a batch for the ILP. The meta-model must be retrained when models change. Evaluation uses HELM-era benchmark prompts rather than real traffic; exact-match scoring undervalues open-ended answers.

## 7. Relevance to the AI Request Router
- This is the nearest published match to the project's planned design: a small encoder-based classifier over the prompt, trained on per-model correctness, feeding a cost-aware assignment. It supports the choice of a small pre-call predictor and shows that per-model outcome labels can be harvested from existing evaluation runs without human annotation.
- Reuse: appending the target model name as a token (one predictor for all models), calibration plots, leave-one-dataset-out generalisation test, ILP or greedy assignment, and cost-versus-accuracy curves with an oracle.
- Avoid: using list price and average output length as the only cost signals; the project adds measured latency and load.
- Not covered: live load, latency budgets, self-hosted serving, failover.

## 8. How to use it in the report
- Sections 2.3 and 2.4 (small pre-call predictors) and the design rationale for the classifier.
- Sentence: "Šakota et al. (2024) showed that a 66M-parameter DistilBERT meta-model can predict per-model success from the query text and, with a cost-aware assignment, cut cost by about 63% at the accuracy of the largest model, but without any latency or load signal."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Šakota et al. (2024) | Cheapest LM that solves each query, chosen before running | DistilBERT meta-model for per-LM success + ILP/greedy assignment under budget | 14 HELM datasets, 4 OpenAI models; PuLP | About 63% cost cut at largest-model accuracy; meta-accuracy 81.57%; calibrated | Old single-vendor pool, price-only cost, no latency or load |


## 2026-10-31 proposal audit

- Source attempted: https://arxiv.org/abs/2308.06077.
- Scope: Full-text sample: method and selected numerical/limitation statements checked; see L07.
- Historical Source read above records the earlier session, not a claim of a fresh full reading.
- arXiv title matched: Fly-Swat or Cannon? Cost-Effective Language Model Choice via Meta-Modeling. Latest listed version: v3; arXiv DOI identifies the preprint, not peer review. A missing journal reference does not prove that no published version exists.
