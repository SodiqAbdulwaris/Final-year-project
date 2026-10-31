Status: DRAFT
Depends on: D08; D12
Sources: Primary URLs in source table and proposal-audit section
Open items: Scoped numerical/final-version checks recorded below

# ICL-Router: onboarding new models through in-context capability profiles (Wang et al., 2026)

| Field | Value |
|---|---|
| Topic (home) | 09 Retrieval, k-NN and multi-turn routing (new-model onboarding) |
| Also relevant to | 01 Routing algorithms, 02 Prompt difficulty prediction |
| Paper type | method |
| Venue and status | peer-reviewed (AAAI 2026, Proceedings of the AAAI Conference on Artificial Intelligence, 40(39), 33413–33421) |
| Source read | full text (arXiv v3, https://arxiv.org/pdf/2510.09719v3); the AAAI version may differ |
| Verified on | 2026-10-31, against the Crossref record for DOI 10.1609/aaai.v40i39.40628 and the arXiv comments field |
| Relevance to project | Medium |

## APA 7 reference
Wang, C., Li, H., Zhang, Y., Chen, L., Chen, J., Jian, P., Ye, P., Zhang, Q., & Hu, S. (2026). ICL-Router: In-context learned model representations for LLM routing. *Proceedings of the AAAI Conference on Artificial Intelligence, 40*(39), 33413–33421. https://doi.org/10.1609/aaai.v40i39.40628

(The author order is taken from the arXiv v3 title page; I did not check it against the AAAI page.)

## In-text citation forms
(Wang et al., 2026) · Wang et al. (2026)

## 1. What it is about
ICL-Router describes each candidate LLM by its pattern of right and wrong answers on a fixed set of hard queries. A router language model reads this profile "in context" together with a new query and predicts whether each model would answer correctly. Adding a new model only needs the model to be run on the profile queries, with no router retraining.

## 2. The problem
Routers such as RouterDC and EmbedLLM learn a fixed embedding per model and must be retrained when the pool changes, which does not fit a world where new models appear constantly. MODEL-SAT avoids retraining with hand-written capability instructions but needs manual design per benchmark.

## 3. Proposed solution
**Stage 1: query reconstruction.** A frozen embedding model (Qwen3-Embedding-8B) encodes each query; a two-layer MLP projector maps it into the router's input space, and the router (Qwen2.5-7B-Instruct) is trained to reconstruct the original query text from the projected vector. This aligns vectors with the router's semantics.

**Stage 2: ICL routing training.** Each model's capability profile is a list of (query vector, correct/incorrect) pairs over a query set chosen to be challenging, meaning that only a few models answer correctly. The projector and router are trained with cross-entropy to answer "yes" or "no" for whether a model will answer a new query correctly, given its profile.

**Inference.** The router outputs the probability of a correct answer for each model and selects the highest. For a new model, build its profile on the same query set and use it directly.

## 4. Data, models and tools
- Ten benchmarks. In-distribution (7:3 train/test): OlympiadBench, BBH, LogicBench, MMLU-Pro, MBPP. Out-of-distribution, test only: AIME, HumanEval, KORBench, AGIEval and MMLU-CF.
- Pool: eight open models around 7–9B (for example DeepSeek-R1-Distill-Qwen-7B, Llama-3.1-8B-Instruct, Qwen2.5-7B-Instruct, Gemma-2-9B-IT, GLM-4-9B-Chat); further models (AceReason-Nemotron-1.1-7B among them) are added in the new-model test.
- Baselines: random, an LLM router, Max Expert (best model per dataset), RouterDC, EmbedLLM, MODEL-SAT. Code: https://github.com/lalalamdbf/ICL-Router.
- Training: one epoch for the projector (learning rate 2e-5) then two epochs joint (5e-6).

## 5. Key results
- In-distribution average accuracy (Table 1): ICL-Router 76.30, EmbedLLM 74.16, RouterDC 72.32, MODEL-SAT 71.72, Max Expert 73.19, random router 57.91 (Table 1 values as printed).
- It beats Max Expert on MMLU-Pro (+8.69), BBH (+4.9), LogicBench (+1) and MBPP (+1.32), according to the text.
- Out-of-distribution: ICL-Router leads EmbedLLM by 3.65% and MODEL-SAT by 3.48% on average.
- Adding models without retraining (Figures 2–3): in-distribution accuracy rises from 76.3% to 79.9% as more models are integrated, with a similar trend out of distribution; gains were not always monotonic ("fluctuate").
- No ablation numbers were extracted.

## 6. Limitations
Stated by the authors (Appendix A.5): computing resources and the time needed to collect data for larger models limited the scale of the experiments (the pool is 7–9B open models).

Identified by me: the router is a 7B LLM plus an 8B embedder, which is heavy and slow compared with a lookup; the profile query set must be re-run for every new model (cost grows with the set size, which I did not see quantified); one run per setting, no intervals or paired tests in the text I read; benchmarks are multiple-choice, math and code with automatic correctness, so label noise from chat judging is out of scope; no calibration of the yes/no probability; no latency or session logic.

## 7. Relevance to the AI Request Router
- Shows the cold-start recipe that the guide's retrieval design shares: evaluate a new model on a stored set of scored tasks, then route. For the project's k-NN estimator this means new models must be run on the history set before they can be selected, and a minimum-evidence rule should keep them out of the pool until enough neighbours have scores.
- Reuse: choose the onboarding set to be informative (hard, discriminating queries), report in- and out-of-distribution results separately, and test adding models one at a time.
- Avoid: an LLM-based router at request time; [Varangot-Reille et al. (2026)](varangot-reille-2026-contextualrouter.md) report that plain k-NN does as well without it.
- Not covered: cost, latency, sessions, calibrated probabilities with intervals.

## 8. How to use it in the report
- Chapter 2 on new-model onboarding and cold start; Chapter 3 for the onboarding procedure of a new backend.
- Sentence: "Wang et al. (2026) onboard new models by evaluating them on a fixed query set and reading their right/wrong profile in context, avoiding router retraining, but their router is a 7B language model."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Wang et al. (2026) | Route without retraining when models are added | Query-reconstruction pre-training, then LLM router reading in-context (query, correct?) profiles | 10 benchmarks, eight 7–9B open models; Qwen3-Embedding-8B, Qwen2.5-7B | 76.30 vs EmbedLLM 74.16 average in-distribution; +3.65% OOD; new models need no retraining | 7B router, small pool, no calibration, no cost or latency |


## 2026-10-31 proposal audit

- Source attempted: https://arxiv.org/abs/2510.09719.
- Scope: Abstract/metadata check only in this session; detailed numerical results remain unchecked.
- Historical Source read above records the earlier session, not a claim of a fresh full reading.
- arXiv title matched: ICL-Router: In-Context Learned Model Representations for LLM Routing. Latest listed version: v3; arXiv DOI identifies the preprint, not peer review. A missing journal reference does not prove that no published version exists.
