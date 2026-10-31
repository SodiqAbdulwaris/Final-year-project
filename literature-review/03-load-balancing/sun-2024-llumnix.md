Status: DRAFT
Depends on: D08; D12
Sources: Primary URLs in source table and proposal-audit section
Open items: Scoped numerical/final-version checks recorded below

# Llumnix: dynamic rescheduling of LLM requests across instances (Sun et al., 2024)

| Field | Value |
|---|---|
| Topic (home) | 03 LLM load balancing |
| Also relevant to | 05 Serving engines, 08 Serving frameworks |
| Paper type | system |
| Venue and status | peer-reviewed (18th USENIX OSDI, July 2024) |
| Source read | full text (https://www.usenix.org/system/files/osdi24-sun-biao.pdf; arXiv v1 also checked) |
| Verified on | 2026-10-30, against USENIX OSDI '24 page and arXiv 2406.03243 |
| Relevance to project | High |

## APA 7 reference
Sun, B., Huang, Z., Zhao, H., Xiao, W., Zhang, X., Li, Y., & Lin, W. (2024). Llumnix: Dynamic scheduling for large language model serving. In *Proceedings of the 18th USENIX Symposium on Operating Systems Design and Implementation (OSDI 24)* (pp. 173–191). USENIX Association. https://www.usenix.org/conference/osdi24/presentation/sun-biao (no DOI issued by USENIX; preprint DOI: https://doi.org/10.48550/arXiv.2406.03243)

## In-text citation forms
(Sun et al., 2024) · Sun et al. (2024)

## 1. What it is about
Llumnix is an Alibaba multi-instance LLM serving layer that, besides picking a replica, moves running requests with their KV cache between instances. One load metric, "freeness", drives dispatch, migration and auto-scaling.

## 2. The problem
Prompt lengths vary and output length is unknown in advance, so even load-aware dispatch leaves instances unbalanced, with preemptions, queuing delays and fragmented memory. Existing schedulers use round-robin or one-time placement and cannot differentiate priorities.

## 3. Proposed solution
- **Live migration.** The KV cache only grows by appending, so computed blocks are copied while the source keeps decoding; only the last iteration's blocks are copied during a short pause, giving near-constant downtime.
- **Two-level scheduling.** A global scheduler sees only instance-level load reported periodically by per-instance "llumlets". It dispatches, pairs instances for migration and triggers scaling; llumlets pick and move the requests.
- **Virtual usage and freeness.** A request's virtual memory usage is its real usage, its full demand if head of a queue (queuing counts as load), extra headroom if high priority, or infinite on a draining instance. Freeness F = (M − ΣV) / B (M memory, V virtual usages, B batch size) estimates how many more decode steps the batch can run. Requests go to the highest-freeness instance; thresholds drive migration; scaling keeps average freeness in a range (default [10, 60]).

## 4. Data, models and tools
- vLLM backend, about 3,300 lines of Python, Ray; code at https://github.com/AlibabaPAI/llumnix.
- 16 A10 GPUs; LLaMA-7B and LLaMA-30B; 10,000-request Poisson or Gamma traces with ShareGPT, BurstGPT and generated lengths.
- Baselines: round-robin, INFaaS++ (memory-load dispatch counting queued demand) and Llumnix-base (no priorities).

## 5. Key results
All from Section 6.
- Migration downtime about 20–30 ms regardless of length; alternatives up to 111× worse (Fig. 10).
- Versus round-robin (ShareGPT, BurstGPT): prefill up to 26.6× (mean) and 34.4× (P99) better, end-to-end up to 2× and 2.9×, preemption loss down 84%.
- Versus INFaaS++: P99 prefill up to 5.5× better on real traces, 14.8× on generated ones.
- High-priority mean latency 1.2–1.5× better; normal requests slowed by at most 4.5%.
- Up to 36% cost saving at similar P99 (abstract).

## 6. Limitations
- *Stated by authors:* the interplay with preemptive/fair local scheduling and support for multiple model types are future work (Section 7). The implementation scope is narrower than the design: it implements two priority classes, though the design generalises to more through headroom sizes (Section 4.4), and it supports vLLM as backend, though the architecture is described as non-intrusive and extensible to other backends (Section 5).
- *My observations:* one model per cluster; synthetic arrivals, small A10 testbed; staleness of periodic load reports not measured; migration needs engine internals, unavailable to a gateway in front of Ollama or hosted APIs.

## 7. Relevance to the AI Request Router
- **Live-load signals:** strong evidence that round-robin is a poor baseline for variable-length traffic and that queued demand must count as load.
- **Reuse:** freeness (free capacity over consumption rate) can be approximated from vLLM Prometheus metrics (KV-cache usage, running and waiting requests); reporting instance-level metrics only keeps a gateway scalable; priority headroom suggests reserving capacity for latency budgets.
- **Not covered:** live migration is impossible from a gateway; no model choice, cost or quality.

## 8. How to use it in the report
- Section 2.x on load-aware dispatching and the case against round-robin; also in the justification for a live-load term in the scoring function.
- Synthesis sentence: "Unlike round-robin dispatch (the default in many serving stacks), Llumnix (Sun et al., 2024) balances on a queue-aware memory metric and migrates running requests, but it assumes one model and engine-level access, which a model-selecting gateway lacks."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Sun et al. (2024) | Balance load, fragmentation, priorities and scaling across LLM instances | Live KV-cache migration; virtual-usage "freeness" metric; global scheduler plus per-instance llumlets | vLLM, 16×A10, LLaMA-7B/30B, ShareGPT, BurstGPT, synthetic lengths | Up to 26.6× better mean prefill than round-robin, 5.5× better P99 prefill than INFaaS++, up to 36% cost saving | Single model; needs engine internals; report staleness not studied |


## 2026-10-31 proposal audit

- Source attempted: https://www.usenix.org/system/files/osdi24-sun-biao.pdf;.
- Scope: Current source fetch failed; earlier venue/details remain unverified in this session. HTTP Error 404: Not Found
- Historical Source read above records the earlier session, not a claim of a fresh full reading.
