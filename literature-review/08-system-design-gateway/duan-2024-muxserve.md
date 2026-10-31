Status: DRAFT
Depends on: D08; D12
Sources: Primary URLs in source table and proposal-audit section
Open items: Scoped numerical/final-version checks recorded below

# MuxServe: spatial-temporal multiplexing for serving multiple LLMs (Duan et al., 2024)

| Field | Value |
|---|---|
| Topic (home) | 08 System design and gateway |
| Also relevant to | 03 Load balancing, 04 Cost reduction |
| Paper type | system |
| Venue and status | peer-reviewed (41st International Conference on Machine Learning, PMLR vol. 235, 2024, pp. 11905–11917) |
| Source read | full text of sections 1 to 6 (https://arxiv.org/pdf/2404.02015, v2 of 13 June 2024); appendix not read |
| Verified on | 2026-10-31, against the PMLR proceedings page and arXiv |
| Relevance to project | Medium |

## APA 7 reference
Duan, J., Lu, R., Duanmu, H., Li, X., Zhang, X., Lin, D., Stoica, I., & Zhang, H. (2024). MuxServe: Flexible spatial-temporal multiplexing for multiple LLM serving. In *Proceedings of the 41st International Conference on Machine Learning* (Proceedings of Machine Learning Research, Vol. 235, pp. 11905–11917). PMLR. https://proceedings.mlr.press/v235/duan24a.html (no DOI shown; preprint DOI: https://doi.org/10.48550/arXiv.2404.02015)

## In-text citation forms
(Duan et al., 2024) · Duan et al. (2024)

## 1. What it is about
MuxServe serves several LLMs of different sizes and popularity on one GPU cluster by sharing GPUs between them. It places LLMs together according to how popular each is and overlaps the compute-heavy prompt phase of one model with the decoding phase of another.

## 2. The problem
Endpoint providers serve many LLMs, and request rates differ widely between them (the paper shows a 20-day trace from a provider). Giving each LLM its own GPUs (spatial partitioning) leaves GPUs of unpopular models idle and overloads those of popular ones. Time-sharing whole models (as in AlpaServe) ignores that decoding often leaves a GPU underused.

## 3. Proposed solution
- **Formal problem:** choose LLM colocations and a batching and scheduling strategy to maximise utilisation.
- **Placement:** an enumeration-based greedy algorithm that prioritises LLMs with high computation demand (a function of size and arrival rate) and colocates popular with unpopular models.
- **Adaptive batch scheduling (ADBS):** shares KV-cache memory fairly according to arrival rates.
- **Unified resource manager:** separates prefill and decoding into different jobs, uses NVIDIA multi-process service to partition GPU compute and a shared KV cache to multiplex memory.

## 4. Data, models and tools
Llama-family models from 4B to 70B, with 12, 4, 2 and 1 models per size bucket in the synthetic setting. Cluster of 4 nodes with 8 NVIDIA A100 80 GB GPUs. Synthetic workloads: request rates from a power law, Poisson arrivals, requests sampled from ShareGPT. Real workload: a ChatLMSYS trace with 16 LLMs on 32 GPUs, where 20% of the LLMs receive 50% of the traffic. Baselines: spatial partitioning (one vLLM per LLM) and a temporal-multiplexing baseline the authors implemented, similar to AlpaServe. Code: https://github.com/hao-ai-lab/MuxServe.

## 5. Key results
- Up to 1.8 times higher throughput and up to 2.9 times more requests served within 99% SLO attainment (abstract; section 4.2).
- Real trace: up to 1.38 times and 1.46 times higher throughput than spatial and temporal baselines at SLO scale 8 (section 4.3).
- Ablations: the placement algorithm gives 1.3 times the throughput of a greedy baseline (Figure 8); ADBS gives 1.43 times over round-robin and 1.85 times over first-come-first-served (Figure 9); the unified resource manager adds 1.7 times then 1.2 times throughput and 3.6 times SLO attainment (Figure 10).
- With evenly spread rates, colocation interference lowers SLO attainment slightly at tight SLO scales.

## 6. Limitations
- **Authors:** the paper has no separate limitations section; it notes the colocation interference overhead.
- **Mine:** placement needs request rates known in advance and a fixed LLM set; each request already names its LLM, so it does not decide which model should answer; throughput-centred; one cluster type (A100); no failover or health tracking.

## 7. Relevance to the AI Request Router
- **Supports:** the self-hosted multi-model backend (D-03) and the observation that demand across models is highly uneven, which motivates load-aware routing (gap G2). The paper's real trace shows 20% of models taking 50% of traffic, a pattern the router's live-load term should handle.
- **Reuse:** SLO attainment with an "SLO scale" (a multiple of single-device latency) as a way to express latency targets in Chapter 4.
- **Not covered:** the model-choice decision, hosted APIs, gateway, Prometheus, Redis, circuit breaker.

## 8. How to use it in the report
- Chapter 2, section 2.4.8 (multi-model serving) and 2.4.3.
- Suggested synthesis sentence: "Whereas AlpaServe (Li et al., 2023) time-shares models of a cluster, MuxServe (Duan et al., 2024) shares GPUs between LLMs by popularity and by prefill and decode phase; both assume the caller has already named the model."
- Link: [AlpaServe](li-2023-alpaserve.md); [Llumnix](../03-load-balancing/sun-2024-llumnix.md) for load-based rescheduling.

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Duan et al. (2024) | Efficiently serve multiple LLMs with uneven popularity | Popularity-aware colocation; prefill and decode multiplexing; adaptive batch scheduling; unified resource manager | Llama 4B to 70B; 32 A100 GPUs; ShareGPT; ChatLMSYS trace | Up to 1.8x throughput; 2.9x more requests within 99% SLO | Needs known rates; model already named; no failover |


## 2026-10-31 proposal audit

- Source attempted: https://arxiv.org/abs/2404.02015.
- Scope: Full-text sample: method and selected numerical/limitation statements checked; see L07.
- Historical Source read above records the earlier session, not a claim of a fresh full reading.
- arXiv title matched: MuxServe: Flexible Spatial-Temporal Multiplexing for Multiple LLM Serving. Latest listed version: v2; arXiv DOI identifies the preprint, not peer review. A missing journal reference does not prove that no published version exists.
