# Top 3 papers per section

24 papers across the original eight literature-review sections, ranked **1–3 within each section** by relevance to the current AI Request Router hybrid design. Selections preserve the order in the [full relevance ranking](relevance-ranking.md).

To match the requested total of 24, this shortlist covers topics 01–08; the supplementary topic 09 (retrieval, k-NN and multi-turn routing) is excluded. Papers stay in their home section and appear once.

## 01. Routing algorithms

| Rank | Paper | Why it is relevant |
|---|---|---|
| 1 | [Hybrid LLM — Ding et al. (2024)](01-routing-algorithms/ding-2024-hybrid-llm.md) | Direct foundation for predicting relative model suitability before generation and tuning the quality–cost trade-off. |
| 2 | [RouteLLM — Ong et al. (2025)](01-routing-algorithms/ong-2025-routellm.md) | Practical learned-routing reference for preference-based suitability prediction, threshold selection and generalisation. |
| 3 | [CSCR — Shirkavand et al. (2025)](01-routing-algorithms/shirkavand-2025-cscr.md) | Connects lightweight prompt embeddings, model representations and cost-aware selection across open and API models. |

## 02. Prompt difficulty and suitability prediction

| Rank | Paper | Why it is relevant |
|---|---|---|
| 1 | [FORC / Fly-swat or cannon — Šakota et al. (2024)](02-prompt-difficulty/sakota-2024-fly-swat-or-cannon.md) | A small prompt-only predictor estimates each model's success, then a budget-aware selector assigns requests: the closest structural match to our predictor-and-selector pipeline. |
| 2 | [Routoo — Mohammadshahi et al. (2024)](02-prompt-difficulty/mohammadshahi-2024-routoo.md) | Very close decomposition into per-model performance prediction and cost-aware multi-model selection. |
| 3 | [LLM uncertainty calibration — Xiong et al. (2024)](02-prompt-difficulty/xiong-2024-llm-uncertainty-calibration.md) | Useful calibration vocabulary and warning against treating confidence as actual success probability. |

## 03. Load balancing

| Rank | Paper | Why it is relevant |
|---|---|---|
| 1 | [RouteBalance — Da et al. (2026)](03-load-balancing/da-2026-routebalance.md) | Closest overlap with joint quality–cost–latency model/instance selection; essential prior art when explaining what our contribution adds. |
| 2 | [SLOs-Serve — Chen et al. (2025)](03-load-balancing/chen-2025-slos-serve.md) | Useful admission principle: accept work only when predicted latency can meet its target. |
| 3 | [GORGO — Toniolo et al. (2026)](03-load-balancing/toniolo-2026-gorgo.md) | Gateway-level latency estimation combines network, queued work and prefill, relevant to local/remote latency modelling. |

## 04. Cost reduction

| Rank | Paper | Why it is relevant |
|---|---|---|
| 1 | [Cascade Routing — Dekoninck et al. (2025)](04-cost-reduction/dekoninck-2025-cascade-routing.md) | Strong theoretical foundation for predicted-quality and predicted-cost selection, validation-tuned trade-offs and distinguishing routing from cascading. |
| 2 | [BEST-Route — Ding et al. (2025)](04-cost-reduction/ding-2025-best-route.md) | Useful predictor-to-selector design, expected-output cost estimation and threshold-sweep evaluation. |
| 3 | [Token-uncertainty cascades — Gupta et al. (2024)](04-cost-reduction/gupta-2024-token-uncertainty-cascades.md) | Useful post-answer deferral features if the optional quality cascade is tested. |

## 05. Latency and speed

| Rank | Paper | Why it is relevant |
|---|---|---|
| 1 | [Etalon — Agrawal et al. (2024)](05-latency-and-speed/agrawal-2024-etalon.md) | Especially useful for black-box hosted-backend timing and separating first-token delay from streaming experience. |
| 2 | [Niyama / QoServe — Goel et al. (2025)](05-latency-and-speed/goel-2025-niyama.md) | Deadline semantics and overload handling help define the latency constraint. |
| 3 | [DistServe — Zhong et al. (2024)](05-latency-and-speed/zhong-2024-distserve.md) | Supporting source for TTFT, TPOT and goodput under latency targets. |

## 06. Error handling and fallback

| Rank | Paper | Why it is relevant |
|---|---|---|
| 1 | [ContinuityBench — Pandey and Singh (2026)](06-error-handling-fallback/pandey-2026-continuitybench.md) | Direct gateway-failover study; useful for continuity tests and timeout, 429 and 5xx scenarios. |
| 2 | [ResilienceBench-Operator — Aderaldo and Mendonça (2026)](06-error-handling-fallback/aderaldo-2026-resiliencebench-operator.md) | Controlled fault-injection approach for choosing bounded retries by their success/latency trade-off. |
| 3 | [FailureAtlas — Pandey and Singh (2026)](06-error-handling-fallback/pandey-2026-failureatlas.md) | Direct gateway failure checklist for concurrency, retries, streaming and apparently successful but invalid responses. |

## 07. Testing and benchmarking

| Rank | Paper | Why it is relevant |
|---|---|---|
| 1 | [EmbedLLM — Zhuang et al. (2025)](07-testing-and-benchmarking/zhuang-2025-embedllm.md) | Strong fit for sentence embeddings plus a small learned suitability head; useful model-by-question correctness representation. |
| 2 | [LLMRouterBench — Li et al. (2026)](07-testing-and-benchmarking/li-2026-llmrouterbench.md) | Major evaluation reference for shared-condition comparisons and checking whether a complex hybrid beats simple baselines. |
| 3 | [RouterBench — Hu et al. (2024)](07-testing-and-benchmarking/hu-2024-routerbench.md) | Stored per-prompt, per-model outcomes and costs support low-budget training, replay and quality–cost curves. |

## 08. System design and gateway

| Rank | Paper | Why it is relevant |
|---|---|---|
| 1 | [INFaaS — Romero et al. (2021)](08-system-design-gateway/romero-2021-infaas.md) | Close architectural precedent for callers specifying accuracy/latency/cost requirements while the service chooses a backend. |
| 2 | [Clockwork — Gujarati et al. (2020)](08-system-design-gateway/gujarati-2020-clockwork.md) | Supports deadline-aware eligibility and explicit latency-prediction error reporting. |
| 3 | [Mélange — Griggs et al. (2024)](08-system-design-gateway/griggs-2024-melange.md) | Helps justify a declared local-inference cost basis and request-size-dependent serving costs. |

Based on the existing paper notes and ranking; original-publication metadata and full texts were not freshly reverified. See the full ranking for paper-specific limitations.
