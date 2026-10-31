# vLLM and PagedAttention (Kwon et al., 2023)

| Field | Value |
|---|---|
| Topic (home) | 05 Latency and speed |
| Also relevant to | 08 System design gateway (vLLM is the planned backend), 03 Load balancing |
| Paper type | system |
| Venue and status | peer-reviewed (29th ACM SOSP, 2023) |
| Source read | full text (https://arxiv.org/pdf/2309.06180) |
| Verified on | 2026-10-31, against Crossref record for the ACM DOI and arXiv 2309.06180 |
| Relevance to project | High |

## APA 7 reference
Kwon, W., Li, Z., Zhuang, S., Sheng, Y., Zheng, L., Yu, C. H., Gonzalez, J., Zhang, H., & Stoica, I. (2023). Efficient memory management for large language model serving with PagedAttention. In *Proceedings of the 29th Symposium on Operating Systems Principles* (pp. 611–626). ACM. https://doi.org/10.1145/3600006.3613165

## In-text citation forms
(Kwon et al., 2023) · Kwon et al. (2023)

## 1. What it is about
vLLM is an LLM serving engine built on PagedAttention, which stores each request's key-value (KV) cache in small fixed-size blocks that need not be contiguous, like pages in an operating system. This almost removes wasted GPU memory, so more requests can run in one batch.

## 2. The problem
The KV cache is large and grows with each generated token, and nobody knows output length in advance. Earlier systems reserved a contiguous maximum-length slot per request, causing reserved-but-unused space, fragmentation and no sharing between requests. The authors measured that only 20.4%–38.2% of KV memory held real token state. Small batches mean low throughput.

## 3. Proposed solution
- **Paged KV cache.** A block table maps a request's logical blocks to physical GPU blocks allocated on demand; waste is limited to the last partially filled block.
- **Sharing.** Blocks can be shared across parallel samples, beam search and common prompt prefixes, with copy-on-write.
- **Scheduling and preemption.** Requests are served first-come-first-served. When memory runs out, the most recently arrived sequences are preempted: their blocks are swapped to CPU memory or recomputed later. New requests wait while any preempted sequence is pending.
- Continuous (iteration-level) batching is inherited from Orca ([Yu et al., 2022](yu-2022-orca.md)).

## 4. Data, models and tools
- OPT 13B/66B/175B and LLaMA 13B on A100 GPUs in Google Cloud; synthetic request streams built from ShareGPT and Alpaca length distributions.
- Baselines: FasterTransformer with a custom dynamic batcher, and the authors' own reimplementation of Orca in three variants (Oracle, Pow2, Max) because Orca is not public.
- Code: https://github.com/vllm-project/vllm.

## 5. Key results
- Abstract: 2–4× higher throughput than FasterTransformer and Orca at the same latency level.
- Metric: *normalized latency*, the mean over requests of end-to-end latency divided by output length (s/token), plotted against request rate (Section 6.1). The curve is flat until capacity is reached, then queueing makes latency grow without bound.
- ShareGPT, OPT-13B: sustains 1.7×–2.7× higher request rates than Orca (Oracle), 2.7×–8× than Orca (Max) and up to 22× than FasterTransformer (Section 6.2). It batched 2.2× more requests than Orca (Oracle) at once (Fig. 13a).
- Shared translation prefix (LLaMA-13B): 1.67× throughput over Orca (Oracle) with a one-shot prefix and 3.58× with a five-shot prefix; chatbot workload: 2× higher sustainable rate (Sections 6.4–6.5).

## 6. Limitations
- *Stated by authors:* paging helps only workloads with dynamic memory and memory-bound performance; for compute-bound DNN serving the indirection can hurt.
- *My observations:* the headline metric is normalized latency, which hides time to first token (TTFT) and time between tokens, the targets a router needs; Orca is a reimplementation; FCFS scheduling lets long prompts block later requests (later work such as [Sarathi-Serve](agrawal-2024-sarathi-serve.md) addresses this); a single engine, not a cluster.

## 7. Relevance to the AI Request Router
- **Metrics:** vLLM is the planned self-hosted backend, so its Prometheus metrics (see the overview for names checked against the vLLM docs) come from this engine. KV-cache usage and the waiting queue are the capacity signals; the paper explains why they matter, because batch size is bounded by KV memory and preemption causes sudden stalls.
- **Reuse:** the queue-grows-without-bound shape of the latency-versus-rate curve is the basis for treating a backend as "saturated" past a threshold of cache use or waiting requests, as in [Llumnix](../03-load-balancing/sun-2024-llumnix.md) and [Kossmann et al.](../03-load-balancing/kossmann-2024-gpu-half-empty.md).
- **Not covered:** per-request TTFT/TPOT percentiles or SLO attainment; multiple replicas.

## 8. How to use it in the report
- Section 2.x on serving engines and why memory is the bottleneck; Chapter 3 justification for choosing vLLM.
- Synthesis sentence: "vLLM (Kwon et al., 2023) removes most KV-cache waste, raising sustainable request rates 1.7–2.7× over Orca-style serving, but it reports normalized rather than percentile latency."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Kwon et al. (2023) | Raise LLM serving throughput by cutting KV-cache waste | PagedAttention, block tables, sharing, FCFS with preemption | OPT/LLaMA, A100, ShareGPT/Alpaca traces | 2–4× throughput vs FasterTransformer and Orca | Normalized latency only; single engine |
