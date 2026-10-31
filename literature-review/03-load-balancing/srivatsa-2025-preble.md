# Preble: prompt-sharing-aware distributed scheduling (Srivatsa et al., 2025)

| Field | Value |
|---|---|
| Topic (home) | 03 LLM load balancing |
| Also relevant to | 05 Serving engines (prefix caching), 08 Serving frameworks |
| Paper type | system |
| Venue and status | peer-reviewed (ICLR 2025); arXiv first posted 2024 as 2407.00023 |
| Source read | full text of the ICLR 2025 proceedings PDF (https://proceedings.iclr.cc/paper_files/paper/2025/file/5bc342f48de8264779952fac378f96dc-Paper-Conference.pdf) |
| Verified on | 2026-10-30, against ICLR proceedings page and arXiv 2407.00023 |
| Relevance to project | Medium |

## APA 7 reference
Srivatsa, V., He, Z., Abhyankar, R., Li, D., & Zhang, Y. (2025). Preble: Efficient distributed prompt scheduling for LLM serving. In *Proceedings of the International Conference on Learning Representations (ICLR 2025)*. https://proceedings.iclr.cc/paper_files/paper/2025/hash/5bc342f48de8264779952fac378f96dc-Abstract-Conference.html (no DOI issued by the proceedings; preprint DOI: https://doi.org/10.48550/arXiv.2407.00023)

## In-text citation forms
(Srivatsa et al., 2025) · Srivatsa et al. (2025)

## 1. What it is about
Preble is a cluster-level scheduler for LLM prompts that share long prefixes (tool descriptions, long documents, few-shot examples). A global scheduler above per-GPU local schedulers chooses the GPU for each request so that reuse of cached KV state and load balance are optimised together.

## 2. The problem
Prefix caching worked only inside one GPU. In a cluster, round-robin scatters requests with the same prefix and recomputes it everywhere, while always sending a prefix to its caching GPU overloads that GPU when a prompt family is popular. The authors' study of five workloads found prompts far longer than outputs (ratio from 4× for Azure chat to 2,494× for video QA) and heavy sharing.

## 3. Proposed solution
- **Global prefix trees.** Radix trees of seen prompts record which GPUs cache each node and how many recent requests used it.
- **E2 (exploit/explore) policy.** If the cached prefix is longer than the uncached remainder, exploit: send to the GPU with the longest match (lightest load on ties). Otherwise explore: pick the GPU with the lowest sum of three costs in estimated GPU time: recent load over a window (default 3 min), cost of evicting cache to make room, and prefill of the missed tokens. Times come from offline regression per GPU type on token counts, not live engine metrics; output length is the recent average.
- **Corrections.** If the busiest GPU's load exceeds the lightest by a set factor, future requests are redirected; a very hot prefix is replicated (when average queue time doubles over the window). A GPU busy with decode-like requests is preferred for prefill-like ones.
- **Local scheduler.** Priority groups by cached percentage, picked proportionally, to avoid starvation.

## 4. Data, models and tools
- Five workloads (tool use, embodied agent, program generation, video QA, long-document QA) plus Azure-trace arrivals.
- Mistral 7B on A6000s and Llama-3 70B on 8 H100s; baselines SGLang and vLLM behind round-robin; vLLM and SGLang backends. Code availability not checked.

## 5. Key results
- Abstract: 1.5×–14.5× lower average latency and 2×–10× lower p99 latency than state-of-the-art serving (SGLang with round-robin).
- Mixed Tool+Video workload with Azure arrivals on 4 A6000s: 6.02× average and 4.61× p99 improvement (Fig. 4).
- Ablation (Fig. 5): each component helps; the priority queue improves p99 but not average latency, as intended.
- The global scheduler handled 245 requests/s (ToolBench) to 2,931 requests/s (VideoQA).

## 6. Limitations
- *Stated by authors:* no separate limitations section in the text I read; thresholds are configurable and set by profiling.
- *My observations:* gains depend on heavy prompt sharing; offline profiling per GPU type; short-output workloads only; a central scheduler is a possible single point of failure; baselines are round-robin rather than other load-aware routers; load comes from its own token counts, not live engine metrics.

## 7. Relevance to the AI Request Router
- **Live-load signals:** load can be tracked at the gateway from token counts of requests already sent (no polling), smoothed over a window, since an instant reading ignores the longer-term effect of placement.
- **Reuse:** recent-load-plus-new-request cost; exploit/explore split; hot-prefix replication; redirect on imbalance. Relevant if the router pins a session to one backend.
- **Not covered:** engine-specific radix-tree matching; no model selection, quality or failover.

## 8. How to use it in the report
- Section on cache-aware routing as the third family beside queue-based and memory-based policies; also supports session-affinity design in Chapter 3.
- Synthesis sentence: "Preble (Srivatsa et al., 2025) routes by recent token load plus prefix reuse and reports up to 14.5× lower mean latency than round-robin over SGLang, but only for workloads with heavy prompt sharing."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Srivatsa et al. (2025) | Co-optimise KV-prefix reuse and load balance across GPUs | E2 policy over global radix trees with windowed token-based load cost; rebalancing; local priority queue | Five prompt-sharing workloads, Azure arrivals, Mistral 7B, Llama-3 70B, SGLang/vLLM | 1.5×–14.5× lower mean latency, 2×–10× lower p99 vs round-robin SGLang | Needs high prompt sharing; offline profiling; one model |
