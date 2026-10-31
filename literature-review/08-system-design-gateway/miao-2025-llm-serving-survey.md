# Survey of efficient generative LLM serving (Miao et al., 2025)

| Field | Value |
|---|---|
| Topic (home) | 08 System design and gateway |
| Also relevant to | 05 Latency and speed, 07 Benchmarking |
| Paper type | survey |
| Venue and status | peer-reviewed (*ACM Computing Surveys*, vol. 58, issue 1; published online 4 September 2025, print date 31 January 2026 per Crossref). First preprint December 2023; the arXiv v2 (23 July 2025) is the version read. |
| Source read | full text for sections 1, 3.2.4 (request scheduling), 4 (frameworks), 5 (benchmarks), 6, 7 and 8, plus Table 2; the algorithm and kernel sections (3.1, 3.2.1 to 3.2.3, 3.2.5) were skimmed only (https://arxiv.org/pdf/2312.15234, v2) |
| Verified on | 2026-10-31, against the arXiv abstract page (v1 and v2 listed) and Crossref for DOI 10.1145/3754448. The ACM page itself returned HTTP 403, so volume and pages come from Crossref. |
| Relevance to project | Medium (background map of the serving layer below the gateway) |

## APA 7 reference
Miao, X., Oliaro, G., Zhang, Z., Cheng, X., Jin, H., Chen, T., & Jia, Z. (2025). Towards efficient generative large language model serving: A survey from algorithms to systems. *ACM Computing Surveys, 58*(1), 1–37. https://doi.org/10.1145/3754448

## In-text citation forms
(Miao et al., 2025) · Miao et al. (2025)

## 1. What it is about
A survey of how to serve generative LLMs efficiently, split into algorithmic innovations (decoding algorithms, architecture design, model compression) and system optimisations (low-bit quantisation, parallel computation, memory management, request scheduling, kernel optimisation). It also compares open-source serving frameworks and discusses benchmarks and future directions.

## 2. The problem
LLMs need heavy compute and memory to serve, which makes low latency and high throughput hard. The literature on fixes is spread across machine-learning and systems venues, and the authors want one organised map for researchers and practitioners.

## 3. Proposed solution
A taxonomy rather than a method. For this project the most relevant parts are:
- **Request scheduling (3.2.4):** request-level scheduling in early systems; iteration-level scheduling from Orca; continuous batching in vLLM; preemption (FastServe); prefill and decode disaggregation (Splitwise, DistServe); length prediction (S3); mixed-workload interference (TetriInfer); quality-of-experience scheduling (Andes); and Llumnix for rescheduling across instances by load. The survey lists "model selection" and "load balancing" among aspects LLM serving shares with earlier ML serving.
- **Software frameworks (4, Table 2):** compares FasterTransformer, FlexFlow-Serve, vLLM, FlexGen, TGI, DeepSpeed-Inference, ZeRO-Inference, LightLLM, MLC-LLM and TensorRT-LLM on parallelism, scheduling, kernels and main features. It states that low latency and high throughput are dual, often conflicting targets, and splits latency into time to first token plus time per output token times output length.
- **Benchmarks (5):** no convincing benchmark covers all influencing factors; most work replays public traces; measuring inference latency while excluding scheduling and network overhead is hard; fair tests need aligned model outputs.
- **Future directions (7):** deployment in complex environments (edge, hybrid, decentralised, spot instances with fault tolerance), long context, new architectures, hardware and automatic adaptation to application needs.

## 4. Data, models and tools
Not applicable (literature survey). The survey excludes hardware-specific stacks and deployment layers built on other engines (for example RayLLM and Ray Serve on vLLM, OpenLLM and Xinference), stating they are outside Table 2.

## 5. Key results
No experimental results. Counts I verified: Table 2 lists ten GPU-based serving frameworks; the DOI, volume and 37-page length come from Crossref.

## 6. Limitations
- **Authors:** the benchmark section says a fair, comprehensive serving benchmark does not yet exist; the survey scopes out accuracy and quality evaluation of the LLMs themselves.
- **Mine:** it stays below the application layer. The words "gateway" and "circuit breaker" do not appear in the text, and "router" appears once (LLM microserving's request-level programmable router). It does not cover Ollama, Prometheus-based monitoring, or routing between different models. Cutoff is early 2025, so 2025 to 2026 gateway work (for example AIBrix, see `aibrix-2025-llm-inference-infrastructure.md`) is absent.

## 7. Relevance to the AI Request Router
- **Supports:** the choice of serving engines (D-02, D-03) and the latency vocabulary for evaluation (time to first token, time per output token, p95), and the benchmark caveats for the evaluation plan (Section 3.9).
- **Reuse:** cite for "latency and throughput trade off" and for the point that routing or scheduling overhead is hard to separate from model latency, which the proposed evaluation of router overhead (NFR-01) must handle explicitly.
- **Not covered:** the model-selection and gateway layers the project builds.

## 8. How to use it in the report
- Chapter 2, section 2.3 (enabling technologies) and 2.4.8 (opening paragraph: serving surveys cover engines, not multi-model gateways).
- Suggested synthesis sentence: "Surveys of LLM serving (Miao et al., 2025) catalogue engines and schedulers that run a chosen model well; the choice of which model should receive a prompt is outside their scope."
- Link to home-topic papers: [Llumnix](../03-load-balancing/sun-2024-llumnix.md), [Orca](../05-latency-and-speed/yu-2022-orca.md), [PagedAttention](../05-latency-and-speed/kwon-2023-pagedattention.md), [DistServe](../05-latency-and-speed/zhong-2024-distserve.md).

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Miao et al. (2025) | Organise the field of efficient generative LLM serving | Survey with taxonomy of algorithmic and system optimisations; framework comparison | Literature; ten open-source GPU serving frameworks compared | No fair, comprehensive serving benchmark yet; latency and throughput conflict | No gateway, multi-model routing or failover coverage; cutoff early 2025 |
