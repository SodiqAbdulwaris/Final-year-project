# Topic 02: Prompt difficulty prediction (overview)

## 1. Topic definition and why it matters to the router
Prompt difficulty prediction estimates, before a request is sent to a model, how likely a given LLM is to answer it well, or how much extra computation it needs. In the literature this appears under several names: difficulty estimation, performance prediction, success-probability (P(IK)) prediction, compute allocation and confidence estimation. For the AI Request Router, this is the "score each request" step: the classifier (sentence embeddings plus a scikit-learn model) must turn a prompt into a predicted quality per backend, which the scoring function then trades against cost and live load. The papers below show which signals work (text, hidden states, post-answer confidence), how labels can be obtained without human annotation, and how reliable and transferable the predictions are, which is the main risk for the project.

## 2. Comparison table
| Paper (file) | Year | Type | Venue | Problem | Method | Key result | Limitation |
|---|---|---|---|---|---|---|---|
| [Kadavath et al.](kadavath-2022-know-what-they-know.md) | 2022 | empirical study + method | preprint (arXiv) | Can an LM know whether it will answer correctly? | Calibration study, P(True), P(IK) value head from question only | MC calibration good; P(IK) discriminates and partly transfers, poorly calibrated OOD | 2022 Anthropic models, difficulty confound, preprint |
| [Šakota et al.](sakota-2024-fly-swat-or-cannon.md) | 2024 | method | WSDM '24 | Choose cheapest adequate LM per query | DistilBERT meta-model for per-LM success + ILP assignment | About 63% cost cut at the largest model's accuracy; calibrated | Old single-vendor pool; price-only cost; no latency or load |
| [Mohammadshahi et al.](mohammadshahi-2024-routoo.md) | 2024 | system | preprint (arXiv) | Route among many LLMs under budget | 7B-LLM correctness predictor + greedy cost-aware selector | 75.87% MMLU vs Mixtral 70.6% at equal cost; near GPT-4 at about half cost | One benchmark; heavy predictor; average cost only |
| [Xiong et al.](xiong-2024-llm-uncertainty-calibration.md) | 2024 | empirical study | ICLR 2024 | Is black-box verbalised confidence reliable? | Prompting, sampling, aggregation; ECE and AUROC | Overconfident; consistency helps; white-box gap narrow | Post-answer, unique-answer QA, weak AUROC |
| [Li et al. (FamiCom)](li-2024-famicom.md) | 2024 | method | preprint (arXiv) | Label-free prompt performance estimate | Familiarity (perplexity) × inverse complexity (steps) | Spearman 0.848 vs 0.426 (familiarity only) | MC tasks, needs logits, small validation |
| [Zotos et al.](zotos-2025-model-uncertainty-difficulty.md) | 2025 | method | EDM 2025 | MCQ difficulty without student field tests | Random Forest on TF-IDF/BERT + uncertainty of nine LLMs | RMSE 0.1365 vs 0.1498 text-only (Biopsychology); beats prior bests | Exam MCQs, many LLM calls |
| [Chuang et al.](chuang-2025-confidence-tokens.md) | 2025 | method | ICML 2025 | Reliable confidence for routing/abstaining | Self-REF confidence tokens by fine-tuning | 39% of MMLU queries routed matches 70B accuracy | Post-generation, per-task fine-tuning |
| [Damani et al.](damani-2025-learning-how-hard-to-think.md) | 2025 | method | ICLR 2025 | Allocate compute per query | Probe on hidden state predicts marginal reward; greedy allocation | Up to 50% less compute on math/code; 72–84% easy/hard accuracy | Two-option routing, sample-count cost |
| [Zhu et al.](zhu-2025-llm-already-knows.md) | 2025 | method | EMNLP 2025 | LLM-perceived difficulty without generation | Value function on initial hidden state (TD learning) | ROC-AUC 93.09 on ScienceQA; near-chance cross-model transfer | Needs hidden states; per-model probe |
| [Zhao et al.](zhao-2025-reasoning-efficiency-difficulty.md) | 2025 | method (workshop) | NeurIPS 2025 workshop | Route reasoning problems by difficulty | MLP probes on s1.1-32B activations | About equal to s1.1-32B at about two-thirds of compute | Math only, 32B features, very short |
| [Mozafari et al. (Q-DAPS)](mozafari-2026-q-daps.md) | 2026 | method | ACL 2026 | LLM-oriented question difficulty | Entropy of debiased plausibility of generated wrong answers | Listwise ρ −0.61 to −0.96 with model-success count | Multi-call, needs gold answer, factoid QA |

## 3. Themes and trends
**Where the signal comes from.** Four families appear, ordered by when they can be computed:
1. *From the prompt text or a small encoder, before any model runs.* Šakota et al. (2024) use a 66M-parameter DistilBERT per-model success predictor, Zotos et al. (2025) use TF-IDF or BERT features in a Random Forest, and Routoo uses a 7B decoder as encoder. This family fits the project's plan best.
2. *From the target model's own hidden states after reading the prompt but before generating.* Kadavath et al. (2022), Zhu et al. (2025), Damani et al. (2025) and Zhao et al. (2025) do this, with probes ranging from two-layer MLPs to a fully fine-tuned model. They are accurate but require the model internals, so they suit self-hosted backends only.
3. *From the model's confidence after it has answered.* Chuang et al. (2025) and Xiong et al. (2024) belong here. These behave like cascades, since the first attempt is paid for before the decision.
4. *Offline difficulty measures needing several model calls or a gold answer.* Q-DAPS and FamiCom are useful for labelling or analysis, not for the request path.

**Labels without human annotation.** Almost all the router-relevant papers derive training labels from observed correctness of models: per-model right/wrong (Šakota, Routoo, Zhao, Chuang), the fraction of sampled answers that are correct (Kadavath, Damani), "all three rollouts correct" (Zhu), or the number of LLMs that answer correctly (Mozafari). Human-derived difficulty appears only for exam items (Zotos) and MATH levels (Zhao). Soft labels (success probability or marginal reward) are used by Kadavath and Damani and avoid forcing a hard easy/hard split.

**Difficulty is model-specific, not absolute.** Zhu et al. report near-chance ROC-AUC (47.29 and 49.74) when a probe trained on one LLM is applied to another, Kadavath et al. show weak calibration outside the training distribution, and Kadavath's own footnote concedes P(IK) may partly reflect general question difficulty. This explains why the strongest router designs predict per-model success rather than a single global difficulty number.

**From difficulty to decision.** The 2023–2024 papers pair a predictor with an explicit selection rule (ILP in Šakota, greedy ratio in Routoo, matroid-greedy in Damani); the 2025 papers extend to reasoning models and test-time compute (Zhao, Damani, Zhu). Calibration (Kadavath, Xiong, Chuang, Šakota's calibration plots) is treated as a quality measure of the predictor, not just accuracy.

## 4. Strongest three papers for the proposal
1. **Šakota et al. (2024).** The closest published match to the proposed architecture: a small encoder-based predictor of per-model success feeding a cost-aware assignment, peer-reviewed, with calibration, a leave-one-dataset-out test, an oracle comparison and public code. It also states the gap the project fills, since cost is price only.
2. **Damani et al. (2025).** Gives the cleanest recipe for label construction by repeated sampling, soft targets, an offline binning policy so each request is routed independently, and evaluation against uniform and oracle baselines. Peer-reviewed at ICLR.
3. **Kadavath et al. (2022).** The foundational evidence that success probability can be predicted from the prompt alone and calibrated, with the honest finding that it degrades out of distribution. Preprint only, but it is cited by two other papers in this folder (Xiong et al., Damani et al.). Routoo and Zotos et al. are the next most useful for the classifier design.

## 5. Gaps visible in this topic (feeds the project gap statement)
1. **No live load or latency in the predictor-to-decision step.** Cost is list price and average output length (Šakota et al., 2024), average model price (Mohammadshahi et al., 2024), sample counts (Damani et al., 2025) or average seconds per question (Zhao et al., 2025). None conditions on queue length, GPU utilisation or latency budgets.
2. **Predictors are tied to a fixed model pool and need retraining when it changes.** Cross-model transfer was near chance in Zhu et al. (2025); Routoo and Šakota train for specific pools; Kadavath et al. found partial, poorly calibrated transfer. The project's registry of changing backends is not addressed.
3. **Strong predictors need access to a large model's internals.** Zhu, Zhao, Damani and Kadavath use hidden states of 7B to 52B models (Zhu et al. state closed APIs do not expose them), and Routoo uses a 7B encoder. Only Šakota (DistilBERT) and Zotos (BERT/TF-IDF) test small encoders, and predictor latency is rarely reported.
4. **Benchmark-style evaluation.** Tasks are mostly MCQ, math, code or factoid QA with exact-match scoring; real mixed traffic, multi-turn chat and open-ended quality are largely untested (Zhu et al. note single-turn only; Šakota et al. restrict to binary-scored tasks), so label noise and distribution shift are open risks.
5. **Calibration under shift is weak.** Kadavath et al. report poor calibration out of distribution and Xiong et al. report AUROC around 0.5–0.6 for several black-box signals, so thresholds chosen on one benchmark may not hold in deployment.
6. **No failover coupling.** Confidence-based escalation (Chuang et al.) happens after an answer is produced and does not consider provider outages or error handling.

## 6. Links to paper files
- [kadavath-2022-know-what-they-know.md](kadavath-2022-know-what-they-know.md)
- [sakota-2024-fly-swat-or-cannon.md](sakota-2024-fly-swat-or-cannon.md)
- [mohammadshahi-2024-routoo.md](mohammadshahi-2024-routoo.md)
- [xiong-2024-llm-uncertainty-calibration.md](xiong-2024-llm-uncertainty-calibration.md)
- [li-2024-famicom.md](li-2024-famicom.md)
- [zotos-2025-model-uncertainty-difficulty.md](zotos-2025-model-uncertainty-difficulty.md)
- [chuang-2025-confidence-tokens.md](chuang-2025-confidence-tokens.md)
- [damani-2025-learning-how-hard-to-think.md](damani-2025-learning-how-hard-to-think.md)
- [zhu-2025-llm-already-knows.md](zhu-2025-llm-already-knows.md)
- [zhao-2025-reasoning-efficiency-difficulty.md](zhao-2025-reasoning-efficiency-difficulty.md)
- [mozafari-2026-q-daps.md](mozafari-2026-q-daps.md)

### Related papers documented elsewhere
- 01 Routing algorithms: [Hybrid LLM (Ding et al., 2024)](../01-routing-algorithms/ding-2024-hybrid-llm.md), [RouteLLM (Ong et al., 2025)](../01-routing-algorithms/ong-2025-routellm.md), [FrugalGPT (Chen et al., 2024)](../01-routing-algorithms/chen-2024-frugalgpt.md), [AutoMix (Aggarwal et al., 2024)](../01-routing-algorithms/aggarwal-2024-automix.md), [Benchmark-dataset routing (Shnitzer et al., 2023)](../01-routing-algorithms/shnitzer-2023-benchmark-routing.md), [RouterDC (Chen et al., 2024)](../01-routing-algorithms/chen-2024-routerdc.md), [Zooter (Lu et al., 2024)](../01-routing-algorithms/lu-2024-zooter.md)
- 04 Cost reduction: [Token-uncertainty cascades (Gupta et al., 2024)](../04-cost-reduction/gupta-2024-token-uncertainty-cascades.md), [BEST-Route (Ding et al., 2025)](../04-cost-reduction/ding-2025-best-route.md), [Cascade routing (Dekoninck et al., 2025)](../04-cost-reduction/dekoninck-2025-cascade-routing.md)
- 07 Benchmarking (folder not yet populated when this was written): RouterBench, RouterEval and similar benchmarks are owned there.

## 7. Search log
All lookups were done on 2026-10-30 and 2026-10-31.

| Source | Search (strings) | Result |
|---|---|---|
| arXiv API (title and keyword queries) | Title or phrase of each supervisor-listed paper: "Q-DAPS", "FamiCom", "Model Predictive Prompt Selection", "Confidence Tokens" with "route", "Zotos difficulty uncertainty", "Mostly Know What They Know"; then "Learning How Hard to Think", "Fly-Swat or Cannon", "Can LLMs Express Their Uncertainty", "Adaptive Inference-Time Compute", "Confident or Seek Stronger" | Found all 9 listed papers on arXiv (Routoo, Zhu and Zhao by ID from the user's notes) plus 5 replacement candidates |
| arXiv abstract pages | Comments and journal-reference fields for all 14 papers | Venue hints for Q-DAPS (ACL 2026), Zhao (workshop), Zotos COLING precursor, Xiong (ICLR 2024) |
| ACL Anthology, PMLR, ICLR proceedings, EDM proceedings, arXiv PDF headers | Entry pages for Zhu (EMNLP 2025), Q-DAPS (ACL 2026), Chuang (ICML 2025), Damani (ICLR 2025), Zotos (EDM 2025) | Venue, pages and DOI checked where one exists |
| Web search (standard mode) | Venue and DOI confirmation for each paper with its title plus the venue or "doi" | Confirmed Šakota (WSDM '24 and DOI) and Routoo (no venue found); MoPPS KDD 2026 |
| Crossref API | Title queries | Unusable (no matches or rate-limited); not relied on |
| Semantic Scholar API | Metadata by arXiv ID | Rate-limited (HTTP 429); not relied on |

Counts: **14 papers found** (9 supervisor-listed, 5 added by me), **14 screened**, **11 included as full files** (8 supervisor-listed + 3 added replacements), **1 dropped**, **2 found but not reviewed**.

Papers found but not included:
- *Can prompt difficulty be online predicted for accelerating RL finetuning of reasoning models?* (Qu et al., MoPPS, KDD 2026, arXiv:2507.04632): **dropped**. It estimates prompt difficulty to choose training prompts for reinforcement-learning fine-tuning, which is outside the project (training LLMs is out of scope) and has no routing or inference-time use. Venue and DOI (10.1145/3770854.3780263) are noted in the PDF header if wanted for a footnote.
- *Adaptive inference-time compute: LLMs can predict if they can do better, even mid-generation* (Manvi et al., arXiv:2410.02725): identified, not read; a possible extra for adaptive computation.
- *Confident or seek stronger: uncertainty-based on-device LLM routing* (Chuang et al., arXiv:2502.04428): identified, not read; a possible extra for uncertainty routing.
- Zotos et al.'s COLING 2025 paper (*Can model uncertainty function as a proxy for multiple-choice question item difficulty?*): not given its own file because it is the correlation-only precursor of the EDM 2025 paper that has its own file. It is verified as ACL Anthology 2025.coling-main.749, pp. 11304–11316.

Replacements added: Šakota et al. (WSDM '24; small-encoder per-model success predictor, matches the project's classifier), Damani et al. (ICLR 2025; labels by repeated sampling and per-query compute allocation), Xiong et al. (ICLR 2024; calibration protocol).

Unverified or caveats:
- Šakota et al.: the ACM page could not be opened by my tool; the DOI and venue come from the arXiv v3 PDF's own ACM reference block and web-search listings, and the page range 606–615 from a listing. The abstract says a 63% cost cut while the conclusion says 62.79% and Section 4.2 says 62.1% for one strategy.
- Xiong et al.: the OpenReview URL comes from a web search listing and was not opened; ICLR 2024 acceptance is confirmed by the PDF header and arXiv comment.
- Zotos et al.: read as arXiv v2; I did not diff it against the EDM camera-ready.
- Zhu et al.: read as arXiv v1; Table 1 extraction was garbled, so only numbers stated in the text are used; no code link found.
- Zhao et al.: results are only in figures; no per-threshold numbers are quoted.
- Q-DAPS: Table 2 extraction was unreliable, so only Table 1 values are quoted.
- Damani et al., Chuang et al.: read as arXiv versions, not the proceedings PDFs.
- Word counts: sections 1–8 of each paper file are 628–880 words; the full files are longer because they include the header table, reference and Table 2.3 row.
