# vLLM Semantic Router (grey literature: open-source project, release blog and preprint)

| Field | Value |
|---|---|
| Type | open-source (Apache-2.0) per-request model router from the vLLM ecosystem; sources are the GitHub README, a release blog and an arXiv preprint (grey literature) |
| Pages read | GitHub README, v0.3 "Themis" release blog (5 June 2026), arXiv 2603.04444 v4 (3 June 2026; full extracted text searched for load, latency, budget, SLO and deadline terms; not every section read in detail) |
| Fetched | 2026-10-31 |
| Relevance to project | **High: the closest open competitor found, and it sits in the same vLLM ecosystem the project plans to use** |

## APA 7 references
vLLM Semantic Router Team. (n.d.). *vLLM Semantic Router: An open, programmable decision layer for models and compute* [Computer software]. GitHub. Retrieved October 31, 2026, from https://github.com/vllm-project/semantic-router

vLLM Semantic Router Team. (2026, June 5). *vLLM Semantic Router v0.3 Themis: From signals to stateful production routing*. vLLM Blog. Retrieved October 31, 2026, from https://vllm.ai/blog/2026-06-05-v0.3-vllm-sr-themis-release

Liu, X., Chen, H., Lu, S., Ovadia, Y., Wen, G., Wu, H., Tan, Z., Zhang, J., Zedan, S., Kerido, Y., Weiss, L., Zhang, H., Yu, B., Balum, A., Limoy, N., Samara, A., Fan, B., Salisbury, B., Cook, R., . . . He, B. (2026). *vLLM Semantic Router: Signal driven decision routing for mixture-of-modality models* (arXiv:2603.04444). arXiv. https://doi.org/10.48550/arXiv.2603.04444

In-text: (vLLM Semantic Router Team, n.d.) · (Liu et al., 2026)

## 1. What it is
A router that sits in front of many models and "selects or combines models for each call, guided by your policy" (README wording, paraphrased). Backends may be local vLLM servers or cloud endpoints. A public model ID such as `vllm-sr/auto` is called by the client; the router chooses the backend.

## 2. How routing, fallback and load balancing work
- **Signals:** thirteen signal types (for example domain, estimated context-window demand, language, modality, safety, user identity) extracted from the request by heuristics and small neural classifiers.
- **Decision engine:** Boolean rules over signals define *decisions* (policies); matched decisions pick a **selection algorithm** from thirteen in the preprint, described as rating-based, contrastive, cascading, classical machine learning, reinforcement learning and latency-aware. RouterDC (Chen et al., 2024; see topic 01) and a `session_aware` selector (v0.3: switch economics, prefix locality, hard locks around tool loops) are among them. CLI example: `vllm-sr serve --algorithm latency_aware`.
- **`latency_aware`:** "selects the model with the best observed latency" using percentile TPOT and TTFT statistics "collected at runtime" (Equation 43), so it "responds to real-time backend performance degradation" (preprint wording, quoted fragments under 15 words).
- **Endpoints and failover:** a deployment may expose several endpoints with weighted load distribution; the multi-cloud scenario uses "latency-aware model selection with weighted failover".
- Other features: plugin chains for safety (hallucination detection, PII), semantic caching and episodic memory.

## 3. Feature checklist
| Question | Finding |
|---|---|
| Per-prompt model choice | **Yes**: signals plus decision rules and selection algorithms |
| Predicts difficulty or quality | Complexity and domain signals; some selectors are learned (contrastive, rating-based, reinforcement learning); no single documented quality predictor was read in detail |
| Live load signals | Runtime TPOT/TTFT percentiles for `latency_aware`; weighted multi-endpoint distribution. Queue depth and GPU or KV-cache utilisation are **not documented** in the sources read; a third-party listing mentions a `multi_factor` selector balancing quality, latency, cost and load, which I could not verify |
| Latency budget per request | **Not documented as a mechanism.** The problem formulation (Section 2.1) says the router selects a model "respecting cost and latency constraints", and Section 11.1 sets a <100 ms tail-latency budget for the router's own signal extraction. A search of the full preprint text for "budget", "SLO" and "deadline" found no per-request latency budget, SLO or deadline mechanism for model selection |
| Fallback and failover | Yes (weighted multi-endpoint failover per the preprint) |
| Self-hosted GPU backends | **Yes**, local vLLM instances alongside cloud endpoints; AMD ROCm validated, NVIDIA via Docker (release blog) |
| Openness | Apache-2.0, public GitHub repository |
| Pricing | Free software; infrastructure costs are the user's |

## 4. Limitations (for our purposes)
A large configuration surface (a Boolean decision DSL) rather than a single trained scoring function; latency signals are observed percentiles, not queue state; the preprint reports mostly system design and deployment scenarios, and I did not find a benchmark of cost-quality-load routing against baselines in the sections read. RouteBalance (Da & Kalyvianaki, 2026) used this project as a baseline and reports that router baselines run as published degrade under load.

## 5. Comparison with the AI Request Router
This is the product the proposal's novelty claim must be argued against. It already does per-prompt selection, self-hosted vLLM backends, runtime latency statistics and failover. What the project can still show: a learned quality-cost-load scoring function with measured benchmarks (RouterBench, MT-Bench), queue-depth and GPU signals from Prometheus rather than percentile history, explicit latency budgets, and a head-to-head comparison against it as a baseline. The "none of the products reviewed" wording in the proposal should not be reused without this system in the list.
