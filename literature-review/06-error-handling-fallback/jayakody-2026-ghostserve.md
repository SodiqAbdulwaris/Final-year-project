Status: DRAFT
Depends on: D08; D12
Sources: Primary URLs in source table and proposal-audit section
Open items: Scoped numerical/final-version checks recorded below

# GhostServe: erasure-coded checkpointing for fault-tolerant LLM serving (Jayakody et al., 2026)

| Field | Value |
|---|---|
| Topic (home) | 06 Error handling and fallback |
| Also relevant to | 05 Serving systems |
| Paper type | system |
| Venue and status | peer-reviewed (MLSys 2026, oral); also on arXiv |
| Source read | full text, arXiv v1 (https://arxiv.org/pdf/2605.00831), headed "Proceedings of the 9th MLSys Conference, Bellevue, WA, USA, 2026" |
| Verified on | 2026-10-31, against the MLSys 2026 conference page and the arXiv PDF |
| Relevance to project | Low to Medium |

## APA 7 reference
Jayakody, S., Zhao, Y., Nehate, C. D., & Wang, J. (2026). GhostServe: A lightweight checkpointing system in the shadow for fault-tolerant LLM serving. In *Proceedings of the 9th Conference on Machine Learning and Systems*. https://doi.org/10.48550/arXiv.2605.00831

*Preprint DOI shown; the proceedings page range and publisher record were not found.*

## In-text citation forms
(Jayakody et al., 2026) · Jayakody et al. (2026)

## 1. What it is about
A way to protect the KV cache of long-running LLM requests (million-token agent tasks) against GPU failure without copying the whole cache. It stores small erasure-code parity shards in host memory and, after a failure, rebuilds the lost cache from parity plus surviving data, optionally recomputing the first part in parallel.

## 2. The problem
Most engines recover by recomputing the whole KV cache, which for long contexts can take tens of minutes. Replicating the whole cache (DéjàVu) uses large host memory and works poorly with intra-node tensor parallelism in engines such as SGLang. Training-style checkpointing to SSD is too slow for serving.

## 3. Proposed solution
- Chunk-level erasure coding: tokens are grouped into chunks, N data shards produce K parity shards (XOR, row-diagonal parity or Reed-Solomon implemented as GPU kernels working on an integer view of the cache), and a rotating "parity worker" balances the encoding load.
- **Hybrid recovery:** recompute an early part of the cache while reconstructing the rest from parity.
- Implemented on SGLang. Ablation of parity ratio, batch size and tensor-parallel degree.

**How cost is modelled.** Overheads, not dollars: checkpointing latency, host-memory footprint (the introduction reports 75% less host memory and 73% lower checkpointing latency), effective-inference-time ratio (EITR, the share of runtime spent on real inference) and mean time to recover (MTTR).

## 4. Data, models and tools
8 × H200 GPUs on NVLink with 1 TB host memory; LLaMA-3 8B and 70B, GPT-OSS 20B and 120B, DeepSeek-R1 32B in FP16; synthetic traces from the Medha generator with sequence lengths 4K to 1M tokens and batch sizes 4 to 64; failures simulated by flushing worker memory at random points at a 5% to 15% failure rate. Baselines: SGLang recompute, SGLang plus SSD checkpoint (PCCheck style), SGLang plus CPU replication (DéjàVu style).

## 5. Key results
- Abstract: up to 2.7 times lower checkpointing latency, 2.1 times lower recovery latency for a single batch, and 1.2 times better median response latency under failures. *The conclusion states the 2.1 and 2.7 figures the other way round*, so quote the abstract with care.
- LLaMA-3-70B with 64K input tokens recovers in under 5 seconds versus close to 2 minutes for SSD checkpointing.
- Under failures, EITR above 90% and about 23% better than replication on average; CPU replication falls behind plain recomputation for 70B and 120B models.
- Under 6% overhead against the baseline at up to 1M tokens; hybrid recovery gives up to 42.9% faster recovery.

## 6. Limitations
*Stated by the authors:* single-node (intra-node) only, cross-node needs topology-aware parity placement; benefit disappears at tensor-parallel size 2; prefill/decode disaggregated deployments are an open question.

*My observations:* failures are simulated memory flushes, not real hardware faults; synthetic traces; the baselines are re-implementations. Focused on long-context agent workloads rather than ordinary chat.

## 7. Relevance to the AI Request Router
Mostly **background** that clarifies the layering: engine-level recovery makes a backend come back faster, but the router still needs a fallback while it recovers. Useful numbers for a **recovery-time assumption** (seconds with good protection, minutes without) when choosing circuit-breaker open and half-open timers.
- **Reuse:** MTTR and EITR as vocabulary for backend recovery metrics. **Avoid:** implementing KV checkpointing. **Not covered:** gateway failover, API outages, rate limits.

## 8. How to use it in the report
Section 2.5, a sentence situating engine-internal recovery below the gateway. "GhostServe (Jayakody et al., 2026) reports recovery of a 70B model's 64K-token context in under 5 s versus about 2 min with SSD checkpointing, so backend recovery time depends strongly on the engine."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Jayakody et al. (2026) | Cheap, fast KV-cache fault tolerance for long contexts | Chunk-level erasure coding with GPU kernels; hybrid recompute and reconstruct | LLaMA-3, GPT-OSS, DeepSeek-R1 on 8 H200 GPUs; SGLang | Up to 2.7x faster checkpointing; 2.1x faster recovery | Single node; simulated faults; synthetic traces |


## 2026-10-31 proposal audit

- Source attempted: https://arxiv.org/abs/2605.00831.
- Scope: Abstract/metadata check only in this session; detailed numerical results remain unchecked.
- Historical Source read above records the earlier session, not a claim of a fresh full reading.
- arXiv title matched: GhostServe: A Lightweight Checkpointing System in the Shadow for Fault-Tolerant LLM Serving. Latest listed version: v1; arXiv DOI identifies the preprint, not peer review. A missing journal reference does not prove that no published version exists.
