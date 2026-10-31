# FrugalGPT: LLM cascades to cut API cost (Chen et al., 2024)

| Field | Value |
|---|---|
| Topic (home) | 01 Routing algorithms |
| Also relevant to | 04 Cost reduction and cascades, 06 Fallback |
| Paper type | method / position (strategies plus one instantiation) |
| Venue and status | peer-reviewed (*Transactions on Machine Learning Research*, December 2024); preprint May 2023 |
| Source read | full text of arXiv v1 (https://arxiv.org/pdf/2305.05176); TMLR version not read (OpenReview blocks automated access), so numbers may differ slightly |
| Verified on | 2026-10-31, against arXiv and the TMLR paper list (id cSimKw5p6R) |
| Relevance to project | High |

## APA 7 reference
Chen, L., Zaharia, M., & Zou, J. (2024). FrugalGPT: How to use large language models while reducing cost and improving performance. *Transactions on Machine Learning Research*. https://openreview.net/forum?id=cSimKw5p6R (preprint: https://doi.org/10.48550/arXiv.2305.05176). TMLR has no DOI; the early-version form is (Chen et al., 2023).

## In-text citation forms
(Chen et al., 2024) · Chen et al. (2024)

## 1. What it is about
The paper outlines three ways to cut LLM API cost (prompt adaptation, LLM approximation, LLM cascade) and builds FrugalGPT, a learned cascade that calls cheap models first and escalates only when an answer looks unreliable.

## 2. The problem
API prices differ by about two orders of magnitude (Table 1, 12 APIs from 5 providers, March 2023 prices: 10M input tokens cost USD 30 on GPT-4 against 0.2 on GPT-J). Prices have input, output and sometimes per-request parts, so the cheapest model depends on the task. Earlier cascades assumed classification with known labels, and depending on one provider is risky if it becomes unavailable.

## 3. Proposed solution
Prompt adaptation shortens or batches prompts; approximation uses a cache or a cheaper fine-tuned model; a **cascade** queries a list of APIs in order and stops at the first reliable answer. FrugalGPT has two parts: a **scoring function** g(q, answer) in [0,1] (a DistilBERT regressor judging correctness) and a **router** that picks the ordered list (length 3) and a threshold per model. The choice maximises expected accuracy under an average-cost budget; because the problem is mixed-integer, a specialised optimiser prunes lists whose models rarely disagree and interpolates the objective from few samples.

## 4. Data, models and tools
12 APIs (OpenAI GPT-4, ChatGPT, GPT-3, GPT-Curie; AI21 J1; Cohere; Textsynth GPT-J, FAIRSEQ, GPT-Neo; ForeFrontAI). Datasets (Table 2): HEADLINES (finance, 10,000), OVERRULING (law, 2,400), COQA (7,982), randomly split into training and test. Code: github.com/stanford-futuredata/FrugalGPT (link live, not checked against the paper).

## 5. Key results
- Abstract: matches the best single LLM with up to 98% cost reduction, or beats GPT-4 by 4% at equal cost (the Figure 5 caption says "up to 5%").
- Case study, HEADLINES (Figure 3): budget USD 6.5, one fifth of GPT-4; cascade GPT-J, J1-L, GPT-4 with thresholds 0.96 and 0.37 cuts cost 80% and gains 1.5% accuracy.
- Table 3, cost to match the best single model: HEADLINES USD 33.1 to 0.6 (98.3% saving); OVERRULING 9.7 to 2.6 (73.3%); COQA 72.5 to 29.6 (59.2%).
- Figure 4: on about 6% of HEADLINES queries GPT-4 errs where cheaper models are right; on COQA 13% where GPT-3 is right. This diversity lets a cascade beat its best member.

## 6. Limitations
**Authors:** needs labelled examples resembling test data; learning the cascade costs resources; not comprehensive; latency, fairness, privacy and environment are future work; some queries still run the whole chain.
**Mine:** three narrow tasks and 2023 models; cost is price per API, not load; sequential calls add latency; a wrong "reliable" score ends the cascade; scorer needs retraining when models or prices change; failover is motivation only.

## 7. Relevance to the AI Request Router
- Supports the cost term (input, output and fixed fee formula) and a learned reliability score.
- Reuse: the cost model, MPI diversity analysis as motivation, a cascade as an optional second line when confidence is low.
- Avoid: sequential calls on the latency-critical path; single-dataset training.
- Not covered: live load, queueing, self-hosted GPUs, failover, latency budgets.

## 8. How to use it in the report
- Chapter 2 cost-aware routing and cascading (with topic 04); chapter 3 cost model.
- "FrugalGPT (Chen et al., 2024) pays for cheap models first and escalates on a learned score, whereas Hybrid LLM (Ding et al., 2024) and RouteLLM (Ong et al., 2025) decide before generating."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Chen et al. (2024) | Cut LLM API cost, keep accuracy | Learned cascade (DistilBERT scorer, thresholds, budget optimiser) | HEADLINES, OVERRULING, COQA; 12 APIs | Up to 98% saving at GPT-4 accuracy | Sequential latency; needs in-distribution labels; no load or failover |
