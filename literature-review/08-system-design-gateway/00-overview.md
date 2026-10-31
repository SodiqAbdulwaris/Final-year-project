# Topic 08: System design and gateway (overview)

Verified 2026-10-31. Written by the proposal-drafts session for the supervisor. Nine full paper files are in this folder.

## 1. Topic definition and why it matters

This topic covers the software layers around and above an LLM inference engine: gateways and request routers, multi-model serving, cluster schedulers, admission control, shared state and failure handling. For the AI Request Router it is the evidence base for Chapter 3 section 3.6.1 (architecture): a FastAPI asynchronous gateway in front of vLLM, Ollama and hosted APIs, with an OpenAI-compatible interface, Prometheus metrics, Redis shared health state and a circuit breaker.

**Honest summary of the evidence.** Peer-reviewed work in this area is about *serving systems* (how to run models well), not about *gateways that choose between models*. Nearly every paper here assumes the caller already names the model. Gateway design, OpenAI-compatible proxies, Prometheus and Redis practice and circuit breakers are documented mostly in engineering documentation and vendor or open-source projects, which are grey literature and belong in `../competitors/`. Across the nine papers in this folder (full text searched), "gateway" appears only in AIBrix, "circuit breaker" only in AIBrix (as a criticism of another tool), "Prometheus" and "Ollama" in none, and Redis is used by INFaaS alone as a store. The chapter should therefore present gateway design as an engineering synthesis supported by these papers for individual components, not as an established research area.

## 2. Papers in this topic (comparison)

| Paper | Year | Type | Venue | Problem | Method | Key result (as reported) | Limitation |
|---|---|---|---|---|---|---|---|
| [Romero et al. (INFaaS)](romero-2021-infaas.md) | 2021 | system | USENIX ATC | Developers pick model-variants and hardware by hand | Model-less API; per-query variant selection from latency and accuracy needs; dynamic state machine; Redis metadata store | 1.3x throughput, 1.6x fewer SLO violations, up to 21.6x lower cost; 2.2 to 3.5 ms selection overhead | Image DNNs, not LLMs; no hosted APIs |
| [Li et al. (AlpaServe)](li-2023-alpaserve.md) | 2023 | system | USENIX OSDI | Bursty traffic over many large models | Model-parallel placement; shortest-queue dispatch with SLO check | 10x rate or 6x burstiness at 99% SLO attainment | Non-autoregressive models; controller is a single point of failure |
| [Duan et al. (MuxServe)](duan-2024-muxserve.md) | 2024 | system | ICML | Uneven popularity of many LLMs wastes GPUs | Popularity-aware colocation; prefill and decode multiplexing | Up to 1.8x throughput; 2.9x more requests within 99% SLO | Model already named; known rates needed |
| [Sheng et al. (S-LoRA)](sheng-2024-slora.md) | 2024 | system | MLSys | Serve thousands of LoRA variants | Unified paging; batching kernels; early-abort admission | Up to 4x vs vLLM-packed, 30x vs PEFT | LoRA and one base model only |
| [Zheng et al. (SGLang)](zheng-2024-sglang.md) | 2024 | system | NeurIPS | Multi-call LLM programs redo work | RadixAttention; cache-aware scheduling; compressed FSM | Up to 6.4x throughput, 3.7x lower latency | Engine-level; old vLLM baseline |
| [Gujarati et al. (Clockwork)](gujarati-2020-clockwork.md) | 2020 | system | USENIX OSDI | Tail latency of DNN serving is unpredictable | Central controller predicts durations and runs a request only if it can meet its deadline | 100 ms target met for 99.9999% of requests with thousands of models | Deterministic DNNs only; no fault tolerance |
| [Griggs et al. (Mélange)](griggs-2024-melange.md) | 2024 | method | preprint | Which GPU types are cheapest for a service | Tokens-per-dollar; ILP bin packing | Up to 77% lower cost (chat), 33% (documents), 51% (mixed) | Fixed workload; preprint |
| [Miao et al. (survey)](miao-2025-llm-serving-survey.md) | 2025 | survey | ACM Computing Surveys | Map of efficient LLM serving | Taxonomy; framework comparison | No fair serving benchmark yet | Stops below the gateway layer |
| [AIBrix Team (Shan et al.)](aibrix-2025-llm-inference-infrastructure.md) | 2025 | system (report) | preprint | LLM-aware cloud infrastructure beyond the engine | Envoy-based gateway with load- and prefix-aware routing; autoscaler; KV cache; GPU optimiser | Self-reported: mean latency down 19.2%, P99 down 79% from routing | Preprint; routing not fully evaluated; same-model instances only |

## 3. Themes and trends (synthesis)

1. **Three layers, rarely joined.** SGLang and the survey describe the *engine* layer. AlpaServe, MuxServe, S-LoRA and Clockwork describe the *multi-model cluster* layer, mostly deciding where models live. INFaaS and AIBrix come closest to the *request-routing* layer. No paper joins all three with a choice between different language models per prompt, which is the router's position.
2. **The caller names the model.** In AlpaServe, MuxServe, S-LoRA and Clockwork, each request is addressed to a particular model, and the system decides placement and scheduling. Only INFaaS lets the system choose by stated requirements, and it does so for image models with a fixed per-variant accuracy.
3. **SLO attainment is the common yardstick.** AlpaServe, MuxServe, S-LoRA, Clockwork and Mélange report the share of requests meeting a latency target, usually as a multiple of single-device latency or a fixed first-token or per-token limit. This supports using p95 latency and a latency budget as the router's measures, and adding SLO attainment as a companion metric.
4. **Shared state and failure are handled as engineering details.** INFaaS keeps metadata in Redis and replicates the controller; AlpaServe says plainly that its controller is a single point of failure and has no fault tolerance, and Clockwork likewise leaves fault tolerance of its central scheduler as future work; ServerlessLLM (documented in [topic 06](../06-error-handling-fallback/fu-2024-serverlessllm.md)) persists server status in a reliable key-value store; AIBrix ships GPU failure diagnosis and failure mock-up tools. None evaluates a circuit breaker.
5. **Cost-aware selection exists, but at the infrastructure level.** INFaaS and Mélange choose variants or GPU types by cost and a latency target. Mélange's tokens-per-dollar offers a way to price self-hosted tokens (see the gap list).
6. **Evidence quality is uneven.** Six of the nine are peer-reviewed systems papers from major venues; a seventh, the survey, is peer-reviewed too; the two newest, practical gateway sources (AIBrix, Mélange) are preprints with self-reported numbers.

## 4. Strongest three papers for the proposal

1. **INFaaS (Romero et al., 2021).** Peer-reviewed and the closest published precedent for "choose the backend per query from stated requirements using live state", with a measured decision overhead of 2.2 to 3.5 ms, a Redis store and a replicated controller. Limitation: not LLMs.
2. **AIBrix (Shan et al., 2025).** The only paper here with an LLM-aware gateway in front of vLLM instances and a list of load-aware routing policies (least-request, least-latency and others) that can serve as load-aware baselines. Use with care: it is a preprint and its routing numbers have no visible experiment.
3. **Miao et al. (2025) survey.** A peer-reviewed map of the engine and scheduler layer, useful to justify engine choices and to state the evaluation caveat that routing or scheduling overhead is hard to separate from model latency (relevant to NFR-01).

Runner-up for the cost term: Mélange (preprint). Runner-up for failure design: the explicit single-point-of-failure remarks in AlpaServe and Clockwork, and ServerlessLLM's recovery design (topic 06). Runner-up for the latency-budget rule: Clockwork (run a request only if it is predicted to meet its deadline).

## 5. Gaps visible in this topic (feeds the project gap statement)

Each gap names the evidence in this folder. They remain claims until the other topics and the competitor re-check confirm them.

| ID | Gap | Evidence |
|---|---|---|
| T8-G1 | No reviewed peer-reviewed system selects between *different LLMs per prompt* as part of a gateway; selection by requirements exists only for image-model variants | INFaaS (image DNNs, static accuracy); AlpaServe, MuxServe, S-LoRA, Clockwork address named models; AIBrix routes among instances of one model |
| T8-G2 | Health-based traffic pausing (circuit breaker) is not evaluated in these papers | AlpaServe: no fault tolerance, controller single point of failure; Clockwork: fault tolerance of the central scheduler left as future work; AIBrix mentions a circuit breaker only to say Knative's is incompatible with token-based limits; ServerlessLLM (topic 06) and INFaaS handle recovery of state, not traffic pausing |
| T8-G3 | Hosted pay-per-token APIs and self-hosted GPU servers are not routed together | Only SGLang has an API-model backend (OpenAI, Anthropic) and only for program execution; all others assume GPUs under the operator's control |
| T8-G4 | Router or gateway overhead is rarely measured | INFaaS reports 2.2 to 3.5 ms; the survey says separating scheduling overhead from inference latency is hard; AIBrix reports none |
| T8-G5 | No agreed cost basis for self-hosted tokens next to hosted prices | Mélange defines tokens per dollar from on-demand GPU price; no paper compares it to provider price lists |
| T8-G6 | Prometheus-style live metrics feeding routing are practice, not literature | None of the nine mentions Prometheus; AIBrix exposes metrics through its runtime sidecar |

## 6. Reference-architecture pointers for Chapter 3 (by component)

| Router component | Supporting evidence in this folder | What is missing (needs grey literature or own justification) |
|---|---|---|
| Gateway with one endpoint for all clients | AIBrix (LLM-aware gateway, rate limits); INFaaS (model-less API) | OpenAI-compatible interface: only a de-facto standard; SGLang's baseline text says vLLM is used through its default API server. Cite the vLLM and OpenAI API documentation as grey literature (not fetched in this session) |
| Per-request decision from live state | INFaaS (state machine, Algorithm 1); AIBrix (routing policies); AlpaServe (shortest queue) | Combining quality prediction with load is the project's contribution |
| Shared health state | INFaaS (Redis metadata store, replicated controller); ServerlessLLM (key-value store recovery; documented in topic 06) | Redis in the router's own role needs Redis documentation |
| Failure handling | AlpaServe (single point of failure admitted); Clockwork (workers reject actions that miss their window); AIBrix (failure mock-up tools); ServerlessLLM (migration failure handling, topic 06) | Circuit-breaker pattern itself: engineering literature, see topic 06 |
| Admission and latency budget | S-LoRA (early abort against a first-token SLO); AlpaServe (reject if SLO cannot be met) | Per-request budgets from callers |
| Self-hosted engine choice | Miao et al. (framework comparison); SGLang | Ollama is not covered by any paper here |
| Cost term | Mélange (tokens per dollar); INFaaS | Hosted-API pricing: provider documentation |

## 7. Links to every paper file in this topic

- [romero-2021-infaas.md](romero-2021-infaas.md)
- [li-2023-alpaserve.md](li-2023-alpaserve.md)
- [duan-2024-muxserve.md](duan-2024-muxserve.md)
- [sheng-2024-slora.md](sheng-2024-slora.md)
- [zheng-2024-sglang.md](zheng-2024-sglang.md)
- [gujarati-2020-clockwork.md](gujarati-2020-clockwork.md)
- [griggs-2024-melange.md](griggs-2024-melange.md)
- [miao-2025-llm-serving-survey.md](miao-2025-llm-serving-survey.md)
- [aibrix-2025-llm-inference-infrastructure.md](aibrix-2025-llm-inference-infrastructure.md)

## 8. Related papers documented elsewhere (links only; not counted toward this topic)

These were assigned to other topics. I did not read them for this overview and make no claims about their content beyond their topic assignment.

- Intelligent router, Jain et al. (03): [jain-2024-intelligent-router.md](../03-load-balancing/jain-2024-intelligent-router.md)
- Llumnix, Sun et al. (03): [sun-2024-llumnix.md](../03-load-balancing/sun-2024-llumnix.md). Its file records that Llumnix compared against an "INFaaS++" baseline, which makes it a follow-up to the dispatch idea in INFaaS.
- Mooncake, Qin et al. (03): [qin-2025-mooncake.md](../03-load-balancing/qin-2025-mooncake.md)
- SkyWalker, Xia et al. (03): [xia-2026-skywalker.md](../03-load-balancing/xia-2026-skywalker.md)
- Kossmann et al. (03): [kossmann-2024-gpu-half-empty.md](../03-load-balancing/kossmann-2024-gpu-half-empty.md)
- ContinuityBench, Pandey et al. (06): [pandey-2026-continuitybench.md](../06-error-handling-fallback/pandey-2026-continuitybench.md)
- Routing survey, Varangot-Reille et al. (01): [varangot-reille-2026-routing-survey.md](../01-routing-algorithms/varangot-reille-2026-routing-survey.md)
- ServerlessLLM, Fu et al. (06, owns the paper): [fu-2024-serverlessllm.md](../06-error-handling-fallback/fu-2024-serverlessllm.md). Relevant here for its key-value-store recovery design and its startup-time-aware scheduler.
- Home-topic serving engines referenced from these papers: [PagedAttention](../05-latency-and-speed/kwon-2023-pagedattention.md), [Orca](../05-latency-and-speed/yu-2022-orca.md), [DistServe](../05-latency-and-speed/zhong-2024-distserve.md)

## 9. Search log (feeds Table 2.1)

**Scope note.** This was targeted retrieval of named candidates, not a systematic search. Do not use these counts as a PRISMA-style flow for the whole review; use them only as this topic's contribution, and say so.

| Item | Detail |
|---|---|
| Date | 2026-10-31 |
| Sources used | arXiv (abstract pages and PDFs); USENIX, NeurIPS, PMLR and MLSys proceedings pages; Crossref API (DOI, volume, pages for the survey); web search (general). The ACM Digital Library page returned HTTP 403 and was not read. Not searched directly: IEEE Xplore, Semantic Scholar, Google Scholar. |
| Queries run (web search) | (1) `SGLang: Efficient Execution of Structured Language Model Programs NeurIPS 2024 proceedings papers.nips.cc` (metadata check). (2) `LLM inference gateway architecture paper arXiv OpenAI-compatible API gateway routing multiple model backends semantic router vLLM` (discovery: returned only open-source projects and a blog, no peer-reviewed paper). (3) `INFaaS: Automated Model-less Inference Serving USENIX ATC 2021 Romero` (metadata check). (4) `Mélange: Cost Efficient Large Language Model Serving by Exploiting GPU Heterogeneity Griggs published venue COLM 2025` (venue check; none found). (5) Crossref bibliographic query for the S-LoRA proceedings title (no matching record). |
| Candidates identified | 10: SGLang, Miao survey, AIBrix (assigned); AlpaServe, MuxServe, S-LoRA (named in the brief); INFaaS, Mélange, ServerlessLLM, Clockwork (added during retrieval). ServerlessLLM was then swapped out (see below), so 9 remain. |
| Screened | 10 |
| Included with full file | 9 |
| Period | all included papers 2020 to 2025 (all 2020 or later) |
| Peer-reviewed / preprint only | 7 peer-reviewed; 2 preprint only (Mélange, AIBrix). Peer-reviewed list: INFaaS, AlpaServe, MuxServe, S-LoRA, SGLang, Clockwork, Miao survey. |

**Dropped or not documented**

| Paper | Reason |
|---|---|
| Fu et al., *ServerlessLLM* (OSDI 2024) | **Swapped out on the supervisor's instruction.** I had written a full file for it in this folder, but topic 06 already owns the same paper ([fu-2024-serverlessllm.md](../06-error-handling-fallback/fu-2024-serverlessllm.md)). The 08 copy was deleted. It is cited here only by link to the 06 file. |
| Gujarati et al., *Serving DNNs like Clockwork* (OSDI 2020) | Not dropped: it **replaced ServerlessLLM** as the ninth owned paper ([gujarati-2020-clockwork.md](gujarati-2020-clockwork.md)); full text read, metadata verified on the USENIX OSDI '20 page and arXiv. A check of all topic folders found no other file on it. |
| Open-source gateways found by general search (for example an inference gateway in Rust, an OpenAI-compatible Go proxy, a Go round-robin gateway) | Not peer-reviewed; grey literature. Pass to `../competitors/` if wanted; not verified. |
| Ray (Moritz et al., 2018) | Cited by AIBrix; published before 2020, dropped by the 2020 rule. KServe is cited by AIBrix only by project URL (no paper). |
| Peer-reviewed OpenAI-compatible proxy or gateway architecture papers | None found in the single discovery query. This is a finding about this search, not proof that none exist. A further search (ACM, IEEE, Semantic Scholar) would test it. |

## 10. Open items for the supervisor

1. Decide whether to run a second discovery pass (IEEE Xplore, ACM, Semantic Scholar) for gateway and proxy architecture papers, since the first returned none. Further candidate, not yet read: Shepherd (NSDI 2023, cited in AlpaServe) and Nexus (SOSP 2019, pre-2020, would be dropped).
2. The S-LoRA proceedings listing shows a different title from its printed title (see the paper file); decide which to cite.
3. AIBrix: arXiv identifier 2504 against a 22 February 2025 date, and a corporate author versus the 26 individual authors; the paper file uses the individual list.
4. The Clockwork file reports a prediction-error figure whose unit symbol was lost in text extraction (see its section 5); check the PDF before quoting it.
5. Per-file word counts run slightly above 900 once the field table and Table 2.3 row are included; body text alone is about 700 to 900 words.
