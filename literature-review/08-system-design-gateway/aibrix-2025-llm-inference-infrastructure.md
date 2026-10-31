Status: DRAFT
Depends on: D08; D12
Sources: Primary URLs in source table and proposal-audit section
Open items: Scoped numerical/final-version checks recorded below

# AIBrix: cloud-native LLM-aware gateway and inference infrastructure (AIBrix Team, 2025)

| Field | Value |
|---|---|
| Topic (home) | 08 System design and gateway |
| Also relevant to | 03 Load balancing, 04 Cost reduction, 06 Fallback |
| Paper type | system (technical report) |
| Venue and status | preprint only (arXiv); not peer-reviewed. Project code is open source under the vLLM project organisation. |
| Source read | full text (https://arxiv.org/pdf/2504.03648, v1, 10 pages plus references) |
| Verified on | 2026-10-31, against the arXiv abstract page and the PDF |
| Relevance to project | High for architecture; evidence is thin and self-reported |

## APA 7 reference
Shan, J., Gupta, V., Xu, L., Shi, H., Zhang, J., Wang, N., Xu, L., Kang, R., Liu, T., Zhang, Y., Zhu, Y., Jin, S., Lim, G., Chen, B., Chen, Z., Liu, X., Chen, X., Yin, K., Chung, C.-P., . . . Xie, L. (2025). *AIBrix: Towards scalable, cost-effective large language model inference infrastructure* [Preprint]. arXiv. https://doi.org/10.48550/arXiv.2504.03648

(The PDF credits "The AIBrix Team" as author. The arXiv page lists 26 individuals; the list above follows APA 7's 19 plus last-author rule. Discrepancy to resolve: the arXiv identifier 2504 suggests April 2025, but the PDF and the arXiv page both show 22 February 2025.)

## In-text citation forms
(Shan et al., 2025) · Shan et al. (2025)

## 1. What it is about
AIBrix is an open-source Kubernetes-based layer around inference engines such as vLLM. It covers an LLM-aware API gateway and routing, autoscaling, adapter (LoRA) management, a distributed KV cache, multi-node orchestration, a GPU optimiser and failure diagnosis tools.

## 2. The problem
The authors argue that model and engine optimisations are not enough: real-world cost and scalability depend on the system layer that does scheduling, autoscaling and request routing. They say generic microservice stacks (Knative, Istio) and general ML serving frameworks (KServe, Ray Serve) lack LLM-specific features such as token-based rate limiting, KV-cache-aware routing and heterogeneous GPU use.

## 3. Proposed solution
- **Control plane and data plane.** The control plane registers model metadata, runs controllers (LoRA adapter, multi-node) and an LLM-specific autoscaler. The data plane holds the API gateway, serving units (engine plus a lightweight "AI Runtime" sidecar) and the distributed KV cache.
- **LLM-aware gateway.** It extends Envoy Gateway. It enforces fairness, request and token rate limits (RPM and TPM) and workload isolation, and routes using token patterns, prefix-cache availability and GPU load.
- **Routing policies in the current version:** random, throughput (lowest tokens per second), least-request, least-kv-cache, least-latency (queuing plus serving latency) and prefix-cache-aware.
- **Unified AI Runtime.** A sidecar abstracts engines (vLLM, SGLang, TensorRT-LLM), exposes metrics and manages model artefacts.
- **GPU optimiser.** An off-path component, based on an integer linear program inspired by Mélange, picks GPU mixes under SLOs. Distributed KV cache and hybrid Kubernetes and Ray orchestration are the other components.

## 4. Data, models and tools
Kubernetes, Envoy Gateway, Ray, vLLM; Bird-SQL benchmark on 4 NVIDIA A10 GPUs for the KV cache; ShareGPT and an internal Text2SQL workload on A10 and L20 GPUs for the GPU optimiser. Model sizes for these tests are not stated in the text I read. Code: https://github.com/vllm-project/aibrix.

## 5. Key results
All figures are self-reported by the authors.
- Routing: "reduce mean latency by 19.2% and P99 latency by 79%" (section 3.2.2). The paper gives no table or figure for this, and the conclusion says some experiments do not fully evaluate routing strategies.
- Autoscaling: latency down 11.5%, token throughput up 11.4% and scaling oscillations down 33% against native Kubernetes HPA.
- Distributed KV cache (Table 1, Bird-SQL, 4 A10 GPUs): with prefix caching, peak throughput up 51.64%, average and P99 time to first token down 65.06% and 77.26%.
- Heterogeneous GPUs (A10 plus L20) against L20 only: latency up to 20% higher within the SLO, cost down about 10%.

## 6. Limitations
- **Authors:** routing strategies and heterogeneous serving are not fully evaluated under non-ideal workloads; autoscaling and GPU optimisation rely on offline profiling.
- **Mine:** preprint and technical report; the routing claim has no visible experiment; routing is between instances of the same model, not between different models; no prompt difficulty, no hosted APIs, no fallback or circuit-breaker evidence. The paper criticises Knative's circuit-breaker-based rate limiting as incompatible with token-based limits, but does not describe a circuit breaker of its own.

## 7. Relevance to the AI Request Router
- **Supports:** the gateway architecture and live-load routing (gap G2, D-02). It names the same signals the router plans to read (throughput, queue and latency, KV cache use) and shows a gateway in front of vLLM instances.
- **Reuse:** the separation of gateway, runtime sidecar and metrics; the list of simple routing policies as load-aware baselines for the evaluation (least-request, least-latency); token-based limits.
- **Not covered:** per-prompt model choice, hosted APIs, Ollama, Prometheus or Redis (not mentioned in the paper), circuit breaker. It runs on Kubernetes and Envoy, heavier than the proposed FastAPI gateway. The reference to the Gateway API Inference Extension project signals a standards direction (the paper cites the repository, not a paper).

## 8. How to use it in the report
- Chapter 2, section 2.4.8 (gateway design) and 2.4.3 (load-aware routing between instances).
- Suggested synthesis sentence: "AIBrix (Shan et al., 2025) routes among instances of one model using cache and load signals, whereas the proposed router chooses between different models and combines load with predicted prompt difficulty."
- Chapter 3, section 3.6.1: cite as precedent for a gateway reading engine metrics; flag as preprint.

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Shan et al. (2025) | Cost-effective, scalable LLM serving infrastructure beyond the engine | LLM-aware Envoy-based gateway with load- and prefix-aware routing; autoscaler; distributed KV cache; GPU optimiser | Kubernetes, Ray, vLLM; Bird-SQL, ShareGPT, Text2SQL on A10 and L20 | Self-reported: mean latency down 19.2%, P99 down 79% from routing; KV cache about 50% more throughput | Preprint; routing not fully evaluated; same-model instances only; no per-prompt model choice or fallback evidence |


## 2026-10-31 proposal audit

- Source attempted: https://arxiv.org/abs/2504.03648.
- Scope: Abstract/metadata check only in this session; detailed numerical results remain unchecked.
- Historical Source read above records the earlier session, not a claim of a fresh full reading.
- arXiv title matched: AIBrix: Towards Scalable, Cost-Effective Large Language Model Inference Infrastructure. Latest listed version: v1; arXiv DOI identifies the preprint, not peer review. A missing journal reference does not prove that no published version exists.
