# Topic 07: LLM route testing and benchmarking (overview)

## 1. Topic definition and why it matters to the router
Testing and benchmarking covers how routers and the models behind them are evaluated: datasets of pre-computed model outputs, quality labels (ground truth, LLM judges, human votes), and metrics such as cost-quality curves, oracle gaps, robustness and latency. For the AI Request Router this topic decides what "better" means: the proposal plans to evaluate on RouterBench and MT-Bench, compare against always-strong and always-weak baselines, and report latency. The papers here supply the data schemas, metrics and baselines to copy, show how noisy the quality labels are, and show which of the project's claims (live load, p95 latency, failover) existing benchmarks cannot test.

## 2. Comparison table
| Paper (file) | Year | Type | Venue | Problem | Method / design | Key result | Limitation |
|---|---|---|---|---|---|---|---|
| [Liang et al. (HELM)](liang-2023-helm.md) | 2023 | framework + study | TMLR | Non-comparable, accuracy-only LM evaluation | 7 metrics over 42 scenarios, 30 models; denoised and idealized runtime | Coverage of core scenarios from 17.9% to 96.0%; no strong accuracy-efficiency trade-off | 2022 models, prompting only, no routing |
| [Zheng et al. (MT-Bench)](zheng-2023-mt-bench-llm-judge.md) | 2023 | benchmark + study | NeurIPS 2023 D&B | Can LLM judges replace humans? | 80 multi-turn questions; pairwise/single-answer GPT-4 judging; Arena votes | GPT-4–human agreement 85% vs 81% human–human; position and verbosity bias | Small set, helpfulness only |
| [Hu et al. (RouterBench)](hu-2024-routerbench.md) | 2024 | benchmark | preprint; Agentic Markets Workshop poster at ICML 2024 | No common router benchmark | 405k pre-computed responses; cost-quality hull; AIQ; Zero router | Oracle far above any model; KNN/MLP routers barely beat Zero router | Cost only, no latency or load, GPT-4 labels for part |
| [Chiang et al. (Chatbot Arena)](chiang-2024-chatbot-arena.md) | 2024 | platform | ICML 2024 | Live human-preference evaluation | Anonymous battles; Bradley–Terry with intervals; active sampling | Crowd–expert agreement 72–83% | Hobbyist users, helpfulness only |
| [Zhuang et al. (EmbedLLM)](zhuang-2025-embedllm.md) | 2025 | method + dataset | ICLR 2025 | Reusable model representations | Matrix factorisation on model×question correctness; mpnet embeddings | 3,000 routes in 3.80 s on one A100; beats KNN | 112 models, fixed pool, correctness only |
| [Huang et al. (RouterEval)](huang-2025-routereval.md) | 2025 | benchmark | Findings EMNLP 2025 | Large open pool for routers | m-way selection labels; strong/weak pools; V_R, V_B, entropy | Model-level scaling up; existing routers far below oracle | Performance only, no cost or latency |
| [Lu et al. (RouterArena)](lu-2026-routerarena.md) | 2026 | platform | ICLR 2026 poster (arXiv v3 read) | No router leaderboard | DDC/Bloom dataset; accuracy, cost, optimality, robustness, router latency | No router wins all metrics; some add 250–550 ms | Router overhead only, no load |
| [Feng et al. (FusionFactory)](feng-2026-fusionfactory.md) | 2026 | benchmark + method | TMLR 2026 | Use multi-LLM logs for fusion | Log tuple with cost and judge score; routers; three fusion levels | Routers beat best single LLM by 2–16% | Token-based cost, judge noise, no latency |
| [Li et al. (LLMRouterBench)](li-2026-llmrouterbench.md) | 2026 | benchmark | Findings ACL 2026 | Unfair, fragmented router comparison | 391,645 instances; Gain, Gap@O, CostSave, ParetoDist; ten routers | Routers converge; many do not beat Best Single | Approximate latency, automated labels |

## 3. Themes and trends
**Convergence on a record schema.** From RouterBench (prompt, model, response, performance, cost, true label) through EmbedLLM (a binary model×question matrix), RouterEval (a selection vector per input) to FusionFactory (adding response mode and a judge score) and LLMRouterBench (tokens in and out), the unit is the same: one row per (prompt, model) with a quality score and a cost. None adds timing beyond token counts.

**Metrics grow from one curve to many dimensions.** RouterBench reduces a router to a point on the cost-quality plane and summarises with AIQ. LLMRouterBench adds relative gains (Gain@R, Gain@B), distance to the oracle (Gap@O) and Pareto distance. RouterArena adds routing optimality, typo robustness and the router's own latency. HELM argued earlier for reporting calibration, robustness and efficiency next to accuracy.

**Simple baselines are hard to beat.** RouterBench found KNN and MLP routers barely above its Zero router; LLMRouterBench found many routers, including commercial ones, not reliably better than Best Single and a persistent oracle gap caused by missed correct models; RouterArena found no router best on all metrics and low robustness; RouterEval found routers far below the oracle. This makes always-strong and best-single baselines the essential control.

**Quality labels vary in cleanliness.** Exact match or test-based correctness is cleanest (MMLU, GSM8K, HumanEval). Open-ended chat needs judges or humans: MT-Bench shows GPT-4 agrees with experts 85% of the time but has position and verbosity bias and misgrades maths; Chatbot Arena shows crowd–expert agreement of 72–83%, and expert–expert disagreement of 10–20% on prompts without a ground truth. RouterBench uses GPT-4 for MBPP, MT-Bench and RAG, and FusionFactory adds an insightfulness judge, so router training labels can inherit judge bias.

**Pool and difficulty define the result.** RouterEval shows results depend on pool size and strength; LLMRouterBench shows diminishing returns from large pools and that careful curation matters; EmbedLLM fixes its pool and needs retraining for new models; RouterArena defines difficulty empirically by how many of 42 models answer correctly.

**Latency is the weakest dimension.** RouterBench lists latency as future work; RouterEval ignores it; EmbedLLM and RouterArena measure only the router's own overhead; LLMRouterBench estimates model latency from tokens and one provider's throughput; HELM explains that per-request runtime depends on hardware, software and queue contention, and so reports idealized runtimes instead.

## 4. Strongest three papers for the proposal
1. **RouterBench (Hu et al., 2024).** Already named in the proposal. Its row schema, convex-hull cost-quality curve, AIQ, Zero router and oracle are the most reusable pieces. It is a workshop poster and preprint, so cite it alongside the peer-reviewed benchmarks.
2. **LLMRouterBench (Li et al., 2026).** The most current and best-validated protocol: Best Single, Random and Oracle baselines, Gain/Gap/CostSave/ParetoDist, five-seed averaging, and an explicit statement that no method targets joint cost-latency trade-offs.
3. **RouterArena (Lu et al., 2026).** The best metric checklist (optimality, robustness, router overhead) and an empirical difficulty definition that matches the difficulty labels in topic 02. Treat the leaderboard figures with care (see caveats).
Runner-up for label quality: MT-Bench (Zheng et al., 2023), because it quantifies judge bias.

## 5. Gaps visible in this topic (feeds the project gap statement)
1. **No benchmark measures request latency under load.** RouterBench (cost and quality only), RouterEval (performance only), FusionFactory (token-based cost), EmbedLLM and RouterArena (router overhead only) and LLMRouterBench (latency "indicative rather than definitive") all stop short; HELM explains why per-request runtime is not comparable but removes the queue effect.
2. **Cost is list price or token estimates, not measured serving cost.** RouterBench uses API prices and Together AI prices, FusionFactory estimates tokens with GPT-2, and LLMRouterBench reports API spend. Self-hosted serving with measured GPU cost is not represented.
3. **Quality labels are noisy and their effect on router training is not studied.** MT-Bench and Chatbot Arena quantify judge and crowd noise, yet RouterBench and FusionFactory train and score routers with judge-based labels without a sensitivity analysis.
4. **Static, single-request evaluation.** The benchmarks replay stored outputs, so they cannot test routers that react to backend state, queue depth or outages. Router robustness to typos is tested only in RouterArena and is low.
5. **No failover or fault-injection evaluation.** I found no test of provider errors, timeouts or retries in the sections read of any of the nine papers.
6. **Pools are dated and pair choices narrow.** RouterBench's pool is 2023–24 models and prices; pair-wise routing across more than one model pair is studied systematically only in RouterEval's pool-size experiments.

## 6. What the project should copy and what it needs beyond these benchmarks
This section is my synthesis, not a claim by the papers.

**Dataset schema (copy from RouterBench, extend).** Keep sample_id, model_name, eval_name, prompt, model_response, performance, cost, true_label. Add, as the project's own contribution: request_id, timestamp, backend and provider ID, time to first token, end-to-end latency, tokens in and out, queue depth or GPU utilisation at dispatch, error or timeout flag, retry and failover flag, judge model and version, optional human label, and the classifier's predicted difficulty (cf. FusionFactory's mode and judge fields, LLMRouterBench's token counts).

**Baselines.** Always-strong, always-weak, Random, Best Single, Zero router (RouterBench), cheapest-correct Oracle, and KNN/MLP routers. Report each on more than one model pair (for example one hosted and one self-hosted pair), because RouterEval and LLMRouterBench show that conclusions depend on the pool.

**Metrics.** Accuracy, cost, cost-quality curve with AIQ, Gain@B and Gap@O, CostSave and ParetoDist, optimal-selection ratio, typo robustness and router overhead (RouterArena); plus what none of them provide: p50, p95 and p99 latency at several load levels, SLO attainment, and failover recovery time.

**Quality labels.** Prefer ground truth for maths, code and multiple choice. For chat, use a judge with swapped answer order and reference answers (MT-Bench), check agreement against a small human-labelled subset, and report intervals (Chatbot Arena). Link the difficulty label to topic 02: RouterArena's "number of models that answer correctly" matches [Mozafari et al. (2026)](../02-prompt-difficulty/mozafari-2026-q-daps.md), and soft success rates match [Damani et al. (2025)](../02-prompt-difficulty/damani-2025-learning-how-hard-to-think.md).

## 7. Links to paper files
- [liang-2023-helm.md](liang-2023-helm.md)
- [zheng-2023-mt-bench-llm-judge.md](zheng-2023-mt-bench-llm-judge.md)
- [hu-2024-routerbench.md](hu-2024-routerbench.md)
- [chiang-2024-chatbot-arena.md](chiang-2024-chatbot-arena.md)
- [zhuang-2025-embedllm.md](zhuang-2025-embedllm.md)
- [huang-2025-routereval.md](huang-2025-routereval.md)
- [lu-2026-routerarena.md](lu-2026-routerarena.md)
- [feng-2026-fusionfactory.md](feng-2026-fusionfactory.md)
- [li-2026-llmrouterbench.md](li-2026-llmrouterbench.md)

### Related papers documented elsewhere
- 02 Prompt difficulty prediction: [Šakota et al. (2024)](../02-prompt-difficulty/sakota-2024-fly-swat-or-cannon.md), [Mohammadshahi et al. (Routoo, 2024)](../02-prompt-difficulty/mohammadshahi-2024-routoo.md), [Mozafari et al. (Q-DAPS, 2026)](../02-prompt-difficulty/mozafari-2026-q-daps.md), [Damani et al. (2025)](../02-prompt-difficulty/damani-2025-learning-how-hard-to-think.md), [Zhu et al. (2025)](../02-prompt-difficulty/zhu-2025-llm-already-knows.md), [Zotos et al. (2025)](../02-prompt-difficulty/zotos-2025-model-uncertainty-difficulty.md), [Xiong et al. (2024) on calibration](../02-prompt-difficulty/xiong-2024-llm-uncertainty-calibration.md)
- 01 Routing algorithms: [RouteLLM (Ong et al., 2025)](../01-routing-algorithms/ong-2025-routellm.md), [Hybrid LLM (Ding et al., 2024)](../01-routing-algorithms/ding-2024-hybrid-llm.md), [FrugalGPT (Chen et al., 2024)](../01-routing-algorithms/chen-2024-frugalgpt.md), [Benchmark-dataset routing (Shnitzer et al., 2023)](../01-routing-algorithms/shnitzer-2023-benchmark-routing.md), [RouterDC (Chen et al., 2024)](../01-routing-algorithms/chen-2024-routerdc.md)
- 03 Load balancing (live-load signals the benchmarks lack): [Llumnix (Sun et al., 2024)](../03-load-balancing/sun-2024-llumnix.md), [SLOs-Serve (Chen et al., 2025)](../03-load-balancing/chen-2025-slos-serve.md)

## 8. Search log
All lookups were done on 2026-10-31.

| Source | Search (strings) | Result |
|---|---|---|
| arXiv API | Title queries: "RouterBench", "RouterEval", "LLMRouterBench", "RouterArena", "EmbedLLM", "FusionFactory", "Judging LLM-as-a-Judge", "Chatbot Arena" with "Open Platform", "Holistic Evaluation of Language Models" | All 9 supervisor-listed papers found |
| arXiv abstract pages | Comments and journal-reference fields for all 9 | MT-Bench (NeurIPS 2023 D&B), EmbedLLM and others as hints; most lacked venue |
| ACL Anthology | Entry pages for RouterEval (2025.findings-emnlp.208) and LLMRouterBench (2026.findings-acl.1881) | Venue, pages, DOI confirmed |
| PMLR, ICLR and NeurIPS proceedings; ICLR and ICML virtual sites; TMLR bib files | Chatbot Arena (PMLR v235), EmbedLLM (ICLR 2025), RouterArena (ICLR 2026 poster), MT-Bench (NeurIPS 36), FusionFactory and HELM (TMLR), RouterBench (ICML 2024 Agentic Markets Workshop poster) | Venues confirmed; RouterBench is a workshop poster |
| Web search (standard mode) | Venue and DOI confirmation per paper | Used only as pointers; claims were re-checked on the primary pages above |

Counts: **9 papers found, 9 screened, 9 included as full files, 0 dropped, 0 replaced.** All nine are dated 2020 or later and were read in full text (main text; appendices only skimmed for some). No replacements were needed because every listed paper was reachable and substantial; I did not search for extra papers, because the minimum of 8 was met.

Date and venue corrections to the supervisor's list: HELM is TMLR 2023 (arXiv 2022); FusionFactory is TMLR 2026 (arXiv 2025); RouterArena is an ICLR 2026 poster; LLMRouterBench is Findings of ACL 2026; RouterEval is Findings of EMNLP 2025; EmbedLLM is ICLR 2025; Chatbot Arena is ICML 2024; MT-Bench is NeurIPS 2023.

Unverified or caveats:
- RouterBench: no main-conference venue found; cited as a preprint presented as a poster at the Agentic Markets Workshop at ICML 2024 (confirmed on the ICML virtual page; OpenReview forum IVXmV8Uxwh could not be read because of a bot check, so the workshop's review and archival status are not verified). Its text says 14 models were run (3 RAG-specific) yet reports 11 models.
- MT-Bench: NeurIPS page numbers not confirmed, so none are given.
- HELM: the claim (from a web-search summary) that the repository entered maintenance mode on 1 June 2026 was not verified on the repository.
- RouterArena: read as arXiv v3, labelled "A PREPRINT"; leaderboard numbers differ between Figure 1 and Table 2; the dataset size is given as about 8,000 (introduction) and 8,400 (Section 3); difficulty bands are hard at most 4/42, medium 5–19, easy 20 or more correct models, with shares read from Figure 3 labels (47.5%, 29.1%, 23.4%; label order not certain); the lowest robustness in Figure 9 is vLLM-SR at 35.00% (NIRT-BERT 49.29%).
- EmbedLLM: Table 1 extraction was garbled, so the quoted 0.741 versus 0.715 is my reading and flagged in the file.
- RouterEval: the source of the raw per-model records and the project-page URL were not found in the text read.
- LLMRouterBench: appendix scoring rules for free-form answers not extracted.
- Chatbot Arena, MT-Bench, EmbedLLM, RouterEval, LLMRouterBench: read as arXiv versions, not the proceedings PDFs.
- Word counts: sections 1–8 of each paper file are 743–829 words; full files are longer because of the header table, reference and the Table 2.3 row.
