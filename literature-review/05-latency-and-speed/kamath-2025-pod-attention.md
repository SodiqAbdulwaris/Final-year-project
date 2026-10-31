Status: DRAFT
Depends on: D08; D12
Sources: Primary URLs in source table and proposal-audit section
Open items: Scoped numerical/final-version checks recorded below

# POD-Attention: overlapping prefill and decode in one kernel (Kamath et al., 2025)

| Field | Value |
|---|---|
| Topic (home) | 05 Latency and speed |
| Also relevant to | 08 System design gateway (engine behaviour under load) |
| Paper type | system (GPU kernel) |
| Venue and status | peer-reviewed (ASPLOS '25, March 2025); first posted on arXiv October 2024 |
| Source read | full text (https://arxiv.org/pdf/2410.18038, v2) |
| Verified on | 2026-10-31, against Crossref record for DOI 10.1145/3676641.3715996 and arXiv 2410.18038 |
| Relevance to project | Medium |

## APA 7 reference
Kamath, A. K., Prabhu, R., Mohan, J., Peter, S., Ramjee, R., & Panwar, A. (2025). POD-Attention: Unlocking full prefill-decode overlap for faster LLM inference. In *Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, Volume 2* (pp. 897–912). ACM. https://doi.org/10.1145/3676641.3715996

## In-text citation forms
(Kamath et al., 2025) · Kamath et al. (2025)

## 1. What it is about
Modern engines use hybrid batching, which puts prefill chunks and decode tokens from different requests in the same batch. POD-Attention is a GPU kernel that computes attention for such mixed batches by running prefill and decode work at the same time on each streaming multiprocessor, instead of using two separate kernels one after the other.

## 2. The problem
Hybrid batching makes linear layers efficient, but attention kernels are still specialised: the prefill kernel is compute-bound and the decode kernel is memory-bandwidth-bound, and they run one after another. Each leaves the other resource idle, so attention in hybrid batches wastes GPU capacity.

## 3. Proposed solution
- **SM-aware scheduling.** The kernel decides at run time, per streaming multiprocessor, whether the next work item is a prefill or a decode tile, so both kinds co-reside and keep compute and memory bandwidth busy together.
- **Fusion and tuning.** Prefill and decode are fused in one kernel using FlashAttention-based code, with tuned tile sizes, thread blocks per multiprocessor, and a limit on how many pieces a prefill is split into.
- Integrated into the Sarathi-Serve scheduler ([Agrawal et al., 2024b](agrawal-2024-sarathi-serve.md)) on vLLM for end-to-end tests.

## 4. Data, models and tools
- Yi-6B (one A100), Llama-2-7B and Llama-3-8B (two A100s, tensor parallel); A100-80GB.
- Workloads of 2K requests with 4K–32K-token contexts: an internal enterprise trace (mean context 10.5K tokens) and arXiv-Summarization (mean 9.5K).
- Baselines: original vLLM scheduler (prefill-prioritising) and Sarathi-Serve, both with FlashAttention 2.6.1.

## 5. Key results
- Attention computation up to 59% faster (mean 28%) than independently optimised kernels (abstract).
- Offline throughput: 22%, 20% and 19% higher than Sarathi, and 27%, 13% and 12% higher than vLLM for the three models (Fig. 12).
- Online latency near capacity (Tables 5–6, Llama-3-8B, seconds): on the internal workload at 1.2 queries/s, vLLM's median TTFT is 0.94 and P99 TBT 1.76, but with 99.6% of requests seeing a stall above 500 ms; Sarathi has median TTFT 25.44 and P99 TBT 0.16; Sarathi+POD gives 7.49 and 0.15.
- Sarathi+POD cut P99 TTFT by up to 4.3× versus Sarathi and P99 request latency by up to 42% versus vLLM on the internal workload (106.8 s vs 151.8 s).
- Chunk size shifts the balance: 2K tokens lowered median TTFT from 6.3 s to 1.6 s while raising P99 TBT from 0.11 s to 0.18 s (Table 7).

## 6. Limitations
- *Stated by authors:* an inherent tradeoff exists among TTFT, TBT and throughput, and optimising one can compromise the others.
- *My observations:* kernel-level and tied to A100 and FlashAttention; three small models; one of two traces is proprietary; no routing or multi-replica analysis.

## 7. Relevance to the AI Request Router
- **Why queueing dominates the tail:** the tables show the same hardware moving from a median TTFT under 1 s to 25–46 s when load nears capacity with a stall-free scheduler. Median TTFT can grow by an order of magnitude with queueing while TBT stays flat, so a backend's *queue wait* is the signal to watch for TTFT budgets, and TBT/TPOT is a separate signal.
- **Scheduler differences change what the router sees:** vLLM's default favours TTFT and causes decode stalls (95+% of requests with at least one 200 ms stall); a Sarathi-style scheduler does the reverse. The router should measure TTFT and TPOT per backend instead of assuming them, because engine configuration shifts the tradeoff.
- **Not covered:** routing, SLO attainment across replicas, hosted models.

## 8. How to use it in the report
- Background on the TTFT/TBT/throughput tradeoff and why percentiles must be reported separately.
- Synthesis sentence: "POD-Attention (Kamath et al., 2025) lowers P99 TTFT by up to 4.3× over Sarathi-Serve near capacity, a reminder that the same engine can give very different TTFT and TBT depending on scheduler and load."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Kamath et al. (2025) | Efficient attention for hybrid prefill/decode batches | SM-aware fused kernel running prefill and decode concurrently | Yi-6B, Llama-2-7B, Llama-3-8B, A100; enterprise and arXiv traces | Attention up to 59% faster; throughput +12–27%; P99 TTFT up to 4.3× lower than Sarathi | Hardware-specific; proprietary trace |


## 2026-10-31 proposal audit

- Source attempted: https://arxiv.org/abs/2410.18038.
- Scope: Abstract/metadata check only in this session; detailed numerical results remain unchecked.
- Historical Source read above records the earlier session, not a claim of a fresh full reading.
- arXiv title matched: POD-Attention: Unlocking Full Prefill-Decode Overlap for Faster LLM Inference. Latest listed version: v2; arXiv DOI identifies the preprint, not peer review. A missing journal reference does not prove that no published version exists.
