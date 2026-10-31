# DéjàVu: KV-cache streaming for fault-tolerant LLM serving (Strati et al., 2024)

| Field | Value |
|---|---|
| Topic (home) | 06 Error handling and fallback |
| Also relevant to | 05 Serving systems |
| Paper type | system |
| Venue and status | peer-reviewed (ICML 2024 poster, PMLR volume 235) |
| Source read | full text, arXiv v1 (https://arxiv.org/pdf/2403.01876) |
| Verified on | 2026-10-31, against the arXiv abstract page and the ICML 2024 poster page (the arXiv page lists no venue); PMLR page numbers come from a secondary listing |
| Relevance to project | Medium |

## APA 7 reference
Strati, F., McAllister, S., Phanishayee, A., Tarnawski, J., & Klimovic, A. (2024). DéjàVu: KV-cache streaming for fast, fault-tolerant generative LLM serving. In *Proceedings of the 41st International Conference on Machine Learning* (Vol. 235, pp. 46745–46771). PMLR. https://proceedings.mlr.press/v235/strati24a.html (preprint DOI: https://doi.org/10.48550/arXiv.2403.01876)

## In-text citation forms
(Strati et al., 2024) · Strati et al. (2024)

## 1. What it is about
A pipeline-parallel LLM serving system whose core is a library that streams the attention key-value (KV) cache between GPUs, CPUs and machines. The same primitive is used for three goals: separating prompt processing from token generation to reduce idle "bubbles", swapping per-microbatch caches to CPU to fit larger batches, and replicating the cache so a failed worker can be repaired without restarting requests.

## 2. The problem
Large models need many GPUs, and the KV cache makes generation stateful. When any pipeline stage fails, current systems stall all in-flight requests and recompute from the prompt. The authors cite studies of training clusters (for example 50% of Meta jobs failing within about 16 minutes) to argue failures are routine at scale, and show that a failure halfway through a 1,000-token request nearly doubles its latency.

## 3. Proposed solution
- **DéjàVuLib:** buffered copies and layer-by-layer streaming of cache tensors to local SSD, remote CPU memory or other GPUs.
- **Fault tolerance:** each worker streams its cache incrementally to the next worker in the pipeline, asynchronously with computation. Workers send heartbeats to a central controller; on a missed heartbeat the controller stops the pipeline, restores the failed worker's cache from its neighbour's replica, re-copies the neighbour's own cache, finds the latest microbatch and step that were not fully replicated, and resumes from there.
- **Prompt-token disaggregation** (a planner splits machines between the two phases) and **microbatch swapping** make up the performance half.

**How cost is modelled.** Not in dollars. Cost is lost work: recomputed tokens and extra latency. A planner and simulator estimate makespan and cost for a trace in an appendix.

## 4. Data, models and tools
- VMs with 2 × A100-80GB (40 Gbps links) and V100-16GB VMs (32 Gbps); GPT2-1.5B, OPT-13B, OPT-66B, BLOOM-176B on a FasterTransformer base; request lengths from the LMSys dataset.
- Failure test: OPT-66B, 4-stage pipeline, 500-token prompts, 1,000 generated tokens, one stage failure at step 1200.

## 5. Key results
- Without failures: up to 1.88x (OPT-66B) and 2x (BLOOM-176B) higher throughput than FasterTransformer; microbatch swapping adds up to 1.8x.
- Streaming overhead: within 2% for local SSD and remote CPU memory.
- With one failure (Figure 14): the baseline's microbatch latency rises 1.91x, DéjàVu's 1.24x, which is the 1.54x reduction cited in the abstract; across several injected failures (Figure 15) DéjàVu's runtime is 1.16x shorter.
- A toy GPT2-1.5B request restarted after a failure at token 250 of 500 takes 1.89x longer end to end (Figure 4).

## 6. Limitations
*Stated by the authors:* iteration-level scheduling is not yet integrated.

*My observations:* only pipeline-parallel deployments; tests use a single failure at a time and a few machines; recovery relies on a central controller and heartbeat timeouts (a single point of failure not discussed). GhostServe (Jayakody et al., 2026) reports it works poorly with intra-node tensor parallelism in SGLang and that replicating the whole KV cache costs large host memory. It treats a node failure inside one model deployment, not outages of a provider.

## 7. Relevance to the AI Request Router
- Defines what "a backend recovers" means for self-hosted engines: the router should expect a degraded period (replay or repair) rather than instant return, so a **half-open circuit breaker** should probe gently.
- Gives the cost of **no state protection**: restart from scratch. That is the same cost the router pays when it re-sends a long prompt to another backend after a mid-generation failure.
- **Reuse:** heartbeat-based failure detection as a model for backend health checks. **Avoid:** implementing KV replication (out of scope; use the engine's features). **Not covered:** API providers, rate limits, cross-model failover.

## 8. How to use it in the report
Section 2.5, in the paragraph separating engine-internal fault tolerance from gateway-level failover. "Strati et al. (2024) cut the latency penalty of a stage failure from 1.91x to 1.24x by replicating the KV cache, but protect only a single pipeline, not the path between a client and several providers."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Strati et al. (2024) | Fast recovery of pipeline LLM serving after failures | KV-cache streaming and replication; heartbeats; disaggregation; swapping | OPT-66B, BLOOM-176B; A100/V100 VMs; LMSys | Failure latency 1.24x vs 1.91x; up to 2x throughput | Pipeline parallel only; central controller; single failures |
