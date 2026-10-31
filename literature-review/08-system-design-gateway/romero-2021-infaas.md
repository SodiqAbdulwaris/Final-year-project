Status: DRAFT
Depends on: D08; D12
Sources: Primary URLs in source table and proposal-audit section
Open items: Scoped numerical/final-version checks recorded below

# INFaaS: model-less inference serving with per-query variant selection (Romero et al., 2021)

| Field | Value |
|---|---|
| Topic (home) | 08 System design and gateway |
| Also relevant to | 03 Load balancing, 04 Cost reduction |
| Paper type | system |
| Venue and status | peer-reviewed (USENIX Annual Technical Conference, July 2021; listed on the USENIX page as a best-paper award winner by a web search result, not re-checked on the page itself) |
| Source read | full text (https://www.usenix.org/system/files/atc21-romero.pdf); sections 1 to 9 read, appendix material not present in this PDF |
| Verified on | 2026-10-31, against the USENIX ATC '21 presentation page (via search result) and the PDF's own front page and page numbers (pp. 397 to 411) |
| Relevance to project | High (as a design pattern; it serves image models, not LLMs) |

## APA 7 reference
Romero, F., Li, Q., Yadwadkar, N. J., & Kozyrakis, C. (2021). INFaaS: Automated model-less inference serving. In *Proceedings of the 2021 USENIX Annual Technical Conference* (pp. 397–411). USENIX Association. https://www.usenix.org/conference/atc21/presentation/romero (USENIX issues no DOI; an earlier preprint with a different title is arXiv:1905.13348 and is not the cited version)

## In-text citation forms
(Romero et al., 2021) · Romero et al. (2021)

## 1. What it is about
INFaaS lets an application say what it needs (latency, accuracy, cost) for each inference query instead of naming a model. The system then picks which "model-variant" (a version of a trained model on a given framework, optimiser and hardware) serves that query, and scales variants up and down as load changes.

## 2. The problem
Developers must search thousands of variants that differ in accuracy, latency, cost and hardware, then usually fix one and replicate it as load grows. The authors argue this wastes money because the best variant changes with load, hardware availability and each query's requirements. Existing serving systems (Clipper, TensorFlow Serving, SageMaker and others) leave this choice to the developer.

## 3. Proposed solution
- **Model-less API.** `register_model` stores a model; `inference_query` takes the input, an application ID and requirements such as latency and accuracy (the paper's example is 200 ms and above 70% accuracy).
- **Variant generation and profiling.** Variants are generated from registered models with graph optimisers (TensorRT, Neuron) and profiled once, with results stored in a Metadata Store.
- **Per-query selection (Algorithm 1).** The dispatcher first looks for an already loaded ("Active") variant that meets the requirements and sends the query to the least-loaded worker. If none, it considers unloaded variants, and otherwise suggests the closest variant.
- **Dynamic state machine.** Each variant instance is tracked as Inactive, Active, Overloaded or Interfered (slower than profiled because of co-location). The authors state that static profiles alone are not enough for selection.
- **Autoscaling.** VM-level scaling is combined with model-level scaling, including "model-vertical" scaling (switching to a differently optimised variant). An integer linear program and a heuristic choose the cheapest combination of variants.

## 4. Data, models and tools
- 175 variants generated from 22 model architectures (the motivation section counts 166 variants from 21 models) on AWS EC2 (CPU, V100 GPU, AWS Inferentia). Controller on m5.2xlarge; workers on inf1.2xlarge, p3.2xlarge and m5.2xlarge.
- Baselines: "Clipper+" and "SM+", the authors' improved versions of Clipper-style and SageMaker-style serving, because the originals could not use variants or sharing.
- Workloads from published application patterns and traces, 10 to 1,000 queries per second; one experiment used 113,420 batch-1 queries.
- The Metadata Store is built on Redis, with hash maps and sorted sets. The implementation builds on Triton Inference Server (GPUs) and the Neuron SDK (Inferentia). Code availability is not checked here.

## 5. Key results
- Abstract and introduction: 1.3 times higher throughput, 1.6 times fewer latency-objective violations, cost saving of up to 21.6 times (8.5 times on average in the abstract; the text of section 6.2 says 10 times on average in one place) compared with state-of-the-art systems on AWS EC2.
- Versus Clipper+: 1.23 times lower cost, 1.6 times fewer violations and 2.8 times higher resource utilisation; at low load, 21.6 times cheaper than Clipper+ and 21.3 times cheaper than SM+ when those use GPUs.
- Decision overhead (Table 7, section 6.4): median 1.0 ms or less when the model is named, 3.5 ms when the chosen variant is not loaded and 2.2 ms when it is loaded, up to 44 times faster than brute-force search (35.5 times on average); unchanged when variants grow from 10 to 166 because the store uses constant-time structures.
- Failure handling (section 7): worker failures are detected by heartbeats and a replacement starts from state in the Metadata Store; the controller is replicated and queries move to a standby controller.

## 6. Limitations
- **Authors:** query fairness (different users may get different variants and accuracy, though requirements are always met); controlling the runtime may limit generality across hardware.
- **Mine:** serves image classification style DNNs, not autoregressive LLMs; accuracy is a fixed property of a variant, not predicted per prompt; no cost of hosted pay-per-token APIs; evaluated on AWS only; some figures in the text are inconsistent (8.5 times versus 10 times average cost saving), so quote the abstract.

## 7. Relevance to the AI Request Router
- **Supports:** the scoring engine (D-04) and gateway design. It is the closest published precedent for "the caller states requirements, the system chooses the backend per query", including a latency requirement analogous to the router's per-request latency budget.
- **Reuse:** (a) prefer variants already warm and healthy, then fall back; (b) track dynamic state, not just static profiles, which mirrors the router's live-load signals; (c) keep the decision on a constant-time store; the 2 to 4 ms decision overhead is a useful order of magnitude to compare against the router's own overhead target (NFR-01); (d) Redis as shared state store and a replicated controller for failure.
- **Not covered:** LLM-specific signals (queue length, tokens per second, KV cache), hosted APIs, prompt difficulty, circuit breaker.

## 8. How to use it in the report
- Chapter 2, section 2.4.8 (gateway design) and 2.3 (justify Redis for shared state).
- Suggested synthesis sentence: "Unlike INFaaS (Romero et al., 2021), which selects among variants of image models from stated latency and accuracy requirements, the proposed router selects among language models using predicted prompt difficulty and live LLM-serving load."
- Chapter 3, section 3.6.1 and 3.6.5: cite for the Active, Overloaded and Interfered state idea; for NFR-01 as a point of comparison only.

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Romero et al. (2021) | Remove the need for developers to pick model-variants and hardware per query | Model-less API; per-query variant selection with a dynamic state machine; model-vertical autoscaling with ILP and heuristic | 175 variants of 22 architectures on AWS CPU, GPU and Inferentia; Redis metadata store | 1.3x throughput, 1.6x fewer SLO violations, up to 21.6x lower cost; 2.2 to 3.5 ms median selection overhead | Image DNNs only; no LLM load signals, hosted APIs or prompt-level quality prediction |


## 2026-10-31 proposal audit

- Source attempted: https://www.usenix.org/system/files/atc21-romero.pdf.
- Scope: Source retrieval did not yield a usable abstract/metadata parse; no fresh detailed claim verification. Historical claims remain unverified.
- Historical Source read above records the earlier session, not a claim of a fresh full reading.
