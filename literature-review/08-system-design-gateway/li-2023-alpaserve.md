# AlpaServe: serving many models with model parallelism and statistical multiplexing (Li et al., 2023)

| Field | Value |
|---|---|
| Topic (home) | 08 System design and gateway |
| Also relevant to | 03 Load balancing, 06 Fallback |
| Paper type | system |
| Venue and status | peer-reviewed (17th USENIX OSDI, July 2023, pp. 663–679) |
| Source read | full text of sections 1 to 9 (https://arxiv.org/pdf/2302.11665, v2 of 19 July 2023); appendices not read |
| Verified on | 2026-10-31, against the USENIX OSDI '23 presentation page and arXiv |
| Relevance to project | Medium (design ideas for the dispatcher and for burst handling; models are not generative LLMs) |

## APA 7 reference
Li, Z., Zheng, L., Zhong, Y., Liu, V., Sheng, Y., Jin, X., Huang, Y., Chen, Z., Zhang, H., Gonzalez, J. E., & Stoica, I. (2023). AlpaServe: Statistical multiplexing with model parallelism for deep learning serving. In *Proceedings of the 17th USENIX Symposium on Operating Systems Design and Implementation (OSDI 23)* (pp. 663–679). USENIX Association. https://www.usenix.org/conference/osdi23/presentation/li-zhouhan (USENIX issues no DOI; preprint DOI: https://doi.org/10.48550/arXiv.2302.11665)

## In-text citation forms
(Li et al., 2023) · Li et al. (2023)

## 1. What it is about
AlpaServe studies how to place and parallelise several large models on a GPU cluster so that bursty requests for different models share the same devices. Its finding is that model parallelism, normally used for models too big for one GPU, also helps serving by pooling devices across models.

## 2. The problem
Serving large models is costly and request rates are bursty, with spikes up to 50 times the average in the traces the authors cite. Giving each model its own GPUs means provisioning for each model's peak and leaving devices idle. Existing systems (Clockwork, Shepherd, Nexus and others) do not reason about how co-located models interact.

## 3. Proposed solution
- **Trade-off analysis:** model parallelism adds communication overhead but lets bursts for one model use more devices. Memory per GPU, arrival pattern and latency target decide which wins.
- **Placement algorithms:** a simulator-guided greedy placement of models onto device groups, plus a search over how to partition the cluster into groups and parallel configurations, bucketing models by size.
- **Runtime:** all requests go to a centralised controller that sends each to the group with the shortest queue. Each group serves first-come-first-served and rejects a request it predicts cannot meet its latency target, using execution times known from profiling.
- Batching, swapping and preemption are discussed as complementary and mostly left out of the main experiments.

## 4. Data, models and tools
BERT and GShard mixture-of-experts Transformers (1.3B to 104B parameters); footnote 4 says the work targets non-autoregressive models and could extend to GPT-style ones. 64 V100 16 GB GPUs on 8 AWS p3.16xlarge nodes. Workloads are the Microsoft Azure function traces MAF1 and MAF2, used as a proxy because no open production ML inference trace exists. A discrete-event simulator (error below 2% on SLO attainment against the real system, Table 2). About 4,000 lines of Python built on Alpa. Code: https://github.com/alpa-projects/mms. Baselines: Selective Replication and a Clockwork++ variant.

## 5. Key results
- With the metric "SLO attainment" (share of requests finished within the latency target), at 99% attainment AlpaServe handles up to 10 times higher request rates, 6 times more burstiness or 2.5 times tighter latency targets, or saves up to 2.3 times the devices (abstract and section 6).
- Two-model case study: mean latency 0.70 s with one model per GPU versus 0.55 s with model-parallel placement (1.3 times); with a request-variance coefficient of 3 the gain is 1.9 times (section 3.1).
- Both placement and group partitioning are needed: group partitioning raises the sustainable rate 1.5 times and the burstiness tolerated 1.3 times in an ablation (Figure 17).

## 6. Limitations
- **Authors:** fault tolerance is not a focus; a single GPU failure can take down a whole model-parallel group, and the centralised controller is a single point of failure; no swapping; placement refreshed periodically (for example every 24 hours).
- **Mine:** not autoregressive generation; execution time is assumed predictable, which does not hold for LLMs with variable output length; Azure function traces are a proxy; each request names its model, so there is no model choice.

## 7. Relevance to the AI Request Router
- **Supports:** the load-aware dispatch step and the failover requirement (gap G5). The shortest-queue dispatch with an admission check is a simple baseline for the router's live-load term, and the authors' admission of a single point of failure in the controller is direct evidence for keeping health state in a shared store such as Redis.
- **Reuse:** SLO attainment as a metric next to p95 latency; a simulator to test routing policies before using real GPUs (a possible way to save GPU time in Chapter 4).
- **Not covered:** circuit breaker, hosted APIs, per-prompt choice, LLM-specific signals.

## 8. How to use it in the report
- Chapter 2, section 2.4.8 and 2.4.3; Chapter 3, section 3.9 (metric choice).
- Suggested synthesis sentence: "Unlike AlpaServe (Li et al., 2023), whose controller dispatches to the shortest queue and whose authors flag it as a single point of failure, the proposed router keeps health state in a shared store and retries on the next-best backend."
- Link: [MuxServe](duan-2024-muxserve.md) extends this idea to LLMs.

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Li et al. (2023) | Serve many large models with bursty traffic efficiently | Model-parallel placement with simulator-guided search; shortest-queue dispatch with SLO check | BERT, GShard MoE; 64 V100 GPUs; Azure function traces; simulator | 10x rate, 6x burstiness or 2.5x tighter SLO at 99% attainment; up to 2.3x fewer devices | Non-autoregressive models; no fault tolerance; controller single point of failure |
