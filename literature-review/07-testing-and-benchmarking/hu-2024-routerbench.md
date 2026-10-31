# RouterBench: cost-quality benchmark for multi-LLM routing (Hu et al., 2024)

| Field | Value |
|---|---|
| Topic (home) | 07 Testing and benchmarking |
| Also relevant to | 01 Routing algorithms, 02 Prompt difficulty prediction, 04 Cost reduction |
| Paper type | benchmark |
| Venue and status | arXiv preprint (v2, March 2024); presented as a poster at the Agentic Markets Workshop at ICML 2024 (workshop, not the main conference; workshop review process and archival status not verified; OpenReview forum IVXmV8Uxwh blocked by a bot check) |
| Source read | full text (https://arxiv.org/pdf/2403.12031v2) |
| Verified on | 2026-10-31, against arXiv and the ICML 2024 virtual page (icml.cc/virtual/2024/39041, which lists session type "Poster" and event "Agentic Markets Workshop") |
| Relevance to project | High |

## APA 7 reference
Hu, Q. J., Bieker, J., Li, X., Jiang, N., Keigwin, B., Ranganath, G., Keutzer, K., & Upadhyay, S. K. (2024). *RouterBench: A benchmark for multi-LLM routing system* [Poster presentation]. Agentic Markets Workshop, International Conference on Machine Learning (ICML 2024). arXiv:2403.12031. https://doi.org/10.48550/arXiv.2403.12031

## In-text citation forms
(Hu et al., 2024) · Hu et al. (2024)

## 1. What it is about
RouterBench is a dataset of pre-computed LLM responses plus an evaluation framework, so that routers can be trained and compared without calling any model. It records each model's answer, correctness score and dollar cost for every prompt, and compares routers on a cost-quality plane with a single summary number, AIQ.

## 2. The problem
Many routing methods existed (FrugalGPT, benchmark-based routers, meta-models) but no shared benchmark let researchers compare them. Evaluating a router normally requires re-running every candidate LLM, which is expensive and not reproducible as prices and models change.

## 3. Proposed solution
**Data.** Seven existing datasets (Hellaswag, Winogrande, ARC-Challenge, MMLU, MT-Bench, GSM8K, MBPP) plus a RAG set of 800 user queries from a Martian client, each run through 11 LLMs (open: Llama-70B, Mixtral 8x7B, Yi-34B, Code Llama-34B, Mistral-7B, WizardLM-13B; proprietary: GPT-4, GPT-3.5, Claude v1/v2/instant). The paper says inference was run on 14 models in total, 3 specific to RAG, but reports 405,467 samples over 11 models, "8 datasets" and 64 tasks. The paper says eight in several places (Figure 1, Sections 4.2–4.3), but its own list and Table 1 give seven datasets plus the RAG set, so I count seven plus RAG. Each row has: sample_id, model_name, eval_name, prompt, model_response, performance, cost and true_label (Appendix A.3).

**Evaluation framework.** Each router is a point in the (cost, quality) plane. Routers can be mixed by interpolation: send a prompt to router A with probability t and B otherwise, giving any point on the line between them. Taking all points and the model points, build the non-decreasing convex hull. The Zero router is the hull of the individual LLMs and acts as a baseline: a router matters only if it beats it. AIQ (Average Improvement in Quality) is the area under a router's hull normalised over the cost range [c_min, c_max].

**Routers tested.** Predictive: KNN and MLP regressors that predict each model's performance, with the decision rule max of (willingness-to-pay λ × predicted performance − cost). Non-predictive: a cascade with a judge that has error rate ε, and overgenerate-and-rerank.

## 4. Data, models and tools
- Cost: API price for proprietary models; Together AI price as reference for open models (Appendix A.3).
- Quality labels: exact match for MMLU, Hellaswag, GSM8K, ARC and Winogrande; GPT-4 as evaluator for MBPP, MT-Bench and RAG; ratings normalised to [0, 1] (Appendix A.4). Shots: 5-shot for the exact-match sets, 0-shot for the others.
- Split: 70% train / 30% test per dataset; MT-Bench excluded from router training because it is too small.
- Code and data: https://github.com/withmartian/routerbench.

## 5. Key results
- Oracle router (always the cheapest model that is right): near-optimal quality at low cost; GPT-4 is rarely selected, and cheap models like Mistral-7B and WizardLM-13B are chosen often (Figure 3).
- KNN and MLP routers reach the quality of the best single LLMs at lower or similar cost but do not significantly beat the Zero router; AIQ differences are small (for example MMLU: Zero 0.763, KNN 0.773, MLP 0.769; MBPP: Zero 0.660, KNN 0.644, MLP 0.642, Figure 4). These values are printed as labels inside the figure panels, not in a table; I re-checked them on 2026-10-31 against the label text of each panel (each "eval:" name follows its AIQ block and the cost axes fit the datasets), but treat them as read from a figure.
- Cascading with a perfect judge beats Zero (MMLU AIQ 0.901 vs 0.763; MBPP 0.862 vs 0.660; GSM8K 0.680 vs 0.628, Figure 5). Performance degrades quickly once judge error exceeds about 0.1–0.2.
- Costs for comparable quality vary by 2–5× across models.

## 6. Limitations
Stated by the authors: only quality and monetary cost are measured; latency and throughput should be added; many models and tasks are missing; the cascade results are a simulated upper bound with a synthetic judge.

Identified by me: the schema holds one cost number per response with no timing, queue or load fields, so p95 latency and load-aware routing cannot be evaluated. Quality for three datasets comes from a GPT-4 judge, which has known biases (see Zheng et al., 2023). Only about 11 models from API-era 2023, no self-hosted serving, and predictive routers are simple. Results also show that on most tasks learned routers barely beat the Zero baseline, so the benchmark is hard to improve on.

## 7. Relevance to the AI Request Router
- The proposal names RouterBench as a benchmark, so the project should adopt its schema (one row per prompt/model pair) and its AIQ and Zero-router baselines.
- Reuse: cost-quality curve with convex hull and interpolation (turns a routing threshold sweep into one number), Zero-router baseline, per-dataset 70/30 split, oracle router as upper bound.
- Does not cover: latency, p95, live load, failover, multiple model pairs with self-hosted serving. The project should extend each row with measured latency, queue or load snapshot, and the backend that served it.
- Links to topic 02: its KNN/MLP routers follow [Šakota et al. (2024)](../02-prompt-difficulty/sakota-2024-fly-swat-or-cannon.md); the performance-prediction labels are of the same kind as those in [Routoo](../02-prompt-difficulty/mohammadshahi-2024-routoo.md).

## 8. How to use it in the report
- Section 2.7 (benchmarks) and Chapter 3 evaluation design (metrics: AIQ, cost-quality curve, oracle and Zero baselines).
- Sentence: "RouterBench (Hu et al., 2024) fixes a schema of pre-computed responses with quality and dollar cost and a convex-hull AIQ metric, but records no latency or load, which this project's evaluation adds."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Hu et al. (2024) | Standard benchmark for comparing LLM routers | Pre-computed responses; cost-quality plane; convex hull and AIQ; KNN, MLP, cascade routers | 405k samples, 11 LLMs, seven datasets plus a RAG set (paper says eight in places) | Oracle far above any single model; learned routers barely beat Zero router | Cost-only, no latency or load, GPT-4 judge for part of labels, workshop/preprint |
