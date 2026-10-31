Status: DRAFT
Depends on: D08; D12
Sources: Primary URLs in source table and proposal-audit section
Open items: Scoped numerical/final-version checks recorded below

# HELM: holistic, multi-metric evaluation of language models (Liang et al., 2023)

| Field | Value |
|---|---|
| Topic (home) | 07 Testing and benchmarking |
| Also relevant to | 05 Latency and speed (efficiency metrics), 02 Prompt difficulty (calibration) |
| Paper type | benchmark / evaluation framework / empirical study |
| Venue and status | peer-reviewed (Transactions on Machine Learning Research, August 2023); the arXiv preprint dates from November 2022, so the supervisor's list year 2022 is the preprint year |
| Source read | full text (arXiv v2, https://arxiv.org/pdf/2211.09110v2, whose header reads "Published in TMLR (08/2023)"); main text, the efficiency section and Section 11 read, appendices not |
| Verified on | 2026-10-31, against the TMLR bib entry (jmlr.org/tmlr/papers/bib/iO4LZibEqW.bib), a TMLR listing found by web search, and the arXiv PDF header |
| Relevance to project | Medium |

## APA 7 reference
Liang, P., Bommasani, R., Lee, T., Tsipras, D., Soylu, D., Yasunaga, M., Zhang, Y., Narayanan, D., Wu, Y., Kumar, A., Newman, B., Yuan, B., Yan, B., Zhang, C., Cosgrove, C., Manning, C. D., Ré, C., Acosta-Navas, D., Hudson, D. A., . . . Koreeda, Y. (2023). Holistic evaluation of language models. *Transactions on Machine Learning Research*. https://openreview.net/forum?id=iO4LZibEqW

(TMLR has no DOI; arXiv DOI: https://doi.org/10.48550/arXiv.2211.09110. The full list has 50 authors; APA 7 shows the first 19, an ellipsis, and the last.)

## In-text citation forms
(Liang et al., 2023) · Liang et al. (2023)

## 1. What it is about
HELM (Holistic Evaluation of Language Models) is a framework and large evaluation that measures 30 language models on 42 scenarios with seven metrics each: accuracy, calibration, robustness, fairness, bias, toxicity and efficiency. All prompts and completions are released so that others can reuse them, and the toolkit is meant to be extended.

## 2. The problem
Before HELM, models were evaluated on different small sets of tasks, so results were not comparable: on average each model had been evaluated on only 17.9% of the core scenarios, and some prominent models shared none. Accuracy was usually the only metric. The authors want transparency across use cases and desiderata, with the trade-offs made visible.

## 3. Proposed solution
**Taxonomy.** Scenarios (task, domain, language, who produced the text) and metrics are organised, then a broad feasible subset is selected, with what is missing stated explicitly.

**Multi-metric measurement.** Seven metrics are measured for each of 16 core scenarios whenever possible (87.5% of the time). Calibration is measured against accuracy; robustness uses perturbations such as typos and fairness uses dialect or demographic changes, both as worst-case accuracy over perturbations; efficiency separates training cost from inference runtime.

**Inference efficiency.** Per-request runtime is not comparable across providers because of different hardware, software and contention, where requests wait in queues. HELM therefore reports a denoised runtime (provider's own setup with performance variation removed) and an idealized runtime (uniform optimised hardware, on A100 GPUs with Megatron), modelled as time to encode the prompt plus a per-token generation time.

**Standardised adaptation.** Models are evaluated with a fixed few-shot prompting protocol, and the seven targeted evaluations cover knowledge, reasoning, memorisation and copyright, disinformation and others.

## 4. Data, models and tools
- 30 models (open, limited-access and closed) on 42 scenarios, 21 of which were not previously used in mainstream LM evaluation; after HELM, coverage of the core scenarios rose from 17.9% to 96.0%.
- Open-source toolkit and all raw prompts and completions released (github.com/stanford-crfm/helm); the project describes itself as a living benchmark. (A web search listing says the repository went into maintenance mode on 1 June 2026; I did not verify this on the repository.)

## 5. Key results
The paper lists 25 top-level findings. Those relevant here:
- Accuracy, robustness and fairness are strongly correlated, but the most accurate model is not always the most robust or fair: for example, on NarrativeQA TNLG v2 (530B) falls from 72.6% to 38.9% accuracy under perturbation.
- Calibration depends on the scenario and adaptation: on HellaSwag improving accuracy worsens calibration, on OpenBookQA it improves it.
- No strong overall accuracy-versus-efficiency trade-off across all 30 models; within a family larger models are more accurate but cost more to train and run, and only some models lie on the accuracy-efficiency Pareto frontier for each scenario.
- A consistent gap between open and non-open models on core scenarios at that time.
- Instruction-tuned models (Anthropic-LM v4-s3 and the larger tested models) do best on accuracy, robustness and fairness.

## 6. Limitations
Stated by the authors (Section 11): relevance for practical use (a poor-scoring model may still suit a specific context); generalisability, since train–test contamination cannot be ruled out; dependence on the prompting adaptation (trends may not hold under fine-tuning); validity and reliability of datasets are assumed, and Goodhart's Law is acknowledged.

Identified by me: HELM models are 2022-era and many scenarios are multiple choice or short generation; there is no routing or per-prompt choice, no live queueing metric (it deliberately removes it), and no multi-turn chat. The seven-metric table is hard to turn into a single number.

## 7. Relevance to the AI Request Router
- Argues for more than accuracy: the project's metrics (quality, cost, latency, p95, robustness, calibration of the difficulty predictor) follow the same multi-metric idea.
- HELM's own explanation of why per-request latency is noisy (hardware, software, queue contention) is evidence for the project's claim that live load matters and that a latency benchmark must record load conditions; its denoised/idealized split offers one method to separate model speed from load.
- Reuse: robustness via typo perturbations (also used by [RouterArena](lu-2026-routerarena.md)), calibration as a reported metric, and per-scenario reporting instead of one aggregate.
- Source of data: Šakota et al. (2024) trained their meta-model on raw HELM runs, see [Šakota et al.](../02-prompt-difficulty/sakota-2024-fly-swat-or-cannon.md).
- Does not cover: routing, cost per request in a gateway, p95 latency under traffic.

## 8. How to use it in the report
- Section 2.7 (benchmarks) and the case for multi-metric evaluation, including why latency needs load context.
- Sentence: "HELM (Liang et al., 2023) shows that per-request runtime depends on hardware and queue contention and therefore reports denoised and idealized runtimes, whereas this project measures latency under controlled load conditions."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Liang et al. (2023) | Standardised, transparent, multi-metric evaluation of LMs | Taxonomy; 7 metrics (incl. calibration, robustness, efficiency); denoised and idealized runtime | 30 models, 42 scenarios; open toolkit and raw outputs | Coverage 17.9% to 96.0%; accuracy not tied to efficiency; calibration varies by scenario | 2022 models, prompting only, contamination, no routing or load |


## 2026-10-31 proposal audit

- Source attempted: https://arxiv.org/abs/2211.09110.
- Scope: Abstract/metadata check only in this session; detailed numerical results remain unchecked.
- Historical Source read above records the earlier session, not a claim of a fresh full reading.
- arXiv title matched: Holistic Evaluation of Language Models. Latest listed version: v2; arXiv DOI identifies the preprint, not peer review. A missing journal reference does not prove that no published version exists.
