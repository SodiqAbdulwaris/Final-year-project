# Orca: iteration-level scheduling (Yu et al., 2022)

| Field | Value |
|---|---|
| Topic (home) | 05 Latency and speed |
| Also relevant to | 03 Load balancing (queueing delay), 08 System design gateway |
| Paper type | system |
| Venue and status | peer-reviewed (16th USENIX OSDI, July 2022); no arXiv version |
| Source read | full text (https://www.usenix.org/system/files/osdi22-yu.pdf) |
| Verified on | 2026-10-31, against the USENIX OSDI '22 presentation page |
| Relevance to project | Medium |

## APA 7 reference
Yu, G.-I., Jeong, J. S., Kim, G.-W., Kim, S., & Chun, B.-G. (2022). Orca: A distributed serving system for transformer-based generative models. In *Proceedings of the 16th USENIX Symposium on Operating Systems Design and Implementation (OSDI 22)* (pp. 521–538). USENIX Association. https://www.usenix.org/conference/osdi22/presentation/yu (no DOI issued by USENIX)

## In-text citation forms
(Yu et al., 2022) · Yu et al. (2022)

## 1. What it is about
Orca introduced *iteration-level scheduling*, now called continuous batching. A generative model needs many forward passes (iterations), one per output token. Instead of dispatching a fixed batch until all its requests finish, the scheduler re-forms the batch after every iteration.

## 2. The problem
In request-level serving, such as Triton in front of FasterTransformer, a batch is returned only when its slowest request finishes. Requests that finish early wait to return, and requests that arrive after dispatch wait for the whole batch, which inflates latency and queueing time. Naively batching requests at different stages is also hard because their tensor shapes differ.

## 3. Proposed solution
- **Iteration-level scheduling.** The scheduler invokes the engine for one iteration at a time, so a new request waits at most one iteration to join and a finished request returns at once.
- **Selective batching.** Operations that do not depend on sequence length (such as linear layers) run on all tokens of the batch together; attention, which needs per-request shapes, runs per request.
- **Scheduler policy.** First-come-first-served at the iteration level, with a configurable *maximum batch size*. The paper notes that larger batches trade latency for throughput with diminishing returns, so operators tune this knob "to maximize throughput while satisfying one's latency budget" (a paraphrase of Section 4.2).
- Distributed execution with inter- and intra-layer model parallelism, and a pipeline in which the scheduler can inject new requests (Fig. 8).

## 4. Data, models and tools
- GPT-style models of 13B, 101B, 175B and 341B parameters (the 13B and 175B configurations follow GPT-3); fp16; up to four Azure VMs with 8 × A100-40GB each.
- Baseline: NVIDIA FasterTransformer; synthetic request traces. Kwon et al. (2023) describe Orca as not publicly available.

## 5. Key results
- Metric: median end-to-end latency normalised by the number of generated tokens, plotted against throughput (req/s) (Fig. 10).
- For the 175B model at a median normalised latency of 190 ms, Orca delivers 6.81 req/s against 0.185 for FasterTransformer, a 36.9× speedup (Section 6.2, and abstract).
- Orca beat FasterTransformer at every load level for the models using more than one pipeline partition, but lost for the 101B model at low load.
- Raising the maximum batch size increased Orca's throughput without hurting latency in these tests; the authors caution this need not hold in general.

## 6. Limitations
- *Stated by authors:* the maximum batch size must be set carefully against latency and throughput requirements; no guarantee that bigger batches do not raise latency on other hardware, models or workloads.
- *My observations:* FCFS with no notion of prompt length means a long prompt can stall the decoding of others in the batch (the issue [Sarathi-Serve](agrawal-2024-sarathi-serve.md) later targets); memory is reserved per request for the maximum length, which [vLLM](kwon-2023-pagedattention.md) shows wastes capacity; the baseline is a 2022 engine; no TTFT or percentile metrics.

## 7. Relevance to the AI Request Router
- **Why queueing matters:** the paper states the mechanism behind queueing delay: requests wait for the in-flight batch, so latency depends on how many requests are ahead and how long their remaining iterations are. This supports using the waiting-queue size and running-batch size of a backend as a latency predictor.
- **Reuse:** the idea of a per-backend maximum concurrency that is tuned against a latency budget; continuous batching is why a vLLM backend can accept requests while others are decoding, so "busy" is not binary.
- **Not covered:** multiple replicas, routing, SLO attainment or tail percentiles.

## 8. How to use it in the report
- Section 2.x on serving internals: the line from request-level batching (Triton/FasterTransformer) to continuous batching (Orca, vLLM).
- Synthesis sentence: "Orca (Yu et al., 2022) cut queueing by letting requests join and leave the batch each iteration, the basis for the engines (vLLM) the router will call."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Yu et al. (2022) | Cut queueing and early-finish waiting in generative serving | Iteration-level scheduling, selective batching, FCFS with max batch size | GPT 13B–341B, A100 VMs, FasterTransformer | 36.9× throughput at equal median normalised latency (175B) | Long prompts can stall batch; per-request max-length memory; no tail metrics |
