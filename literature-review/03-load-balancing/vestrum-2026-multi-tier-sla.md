# Multi-tier SLA scheduling as an extension of Llumnix (Vestrum et al., 2026)

| Field | Value |
|---|---|
| Topic (home) | 03 LLM load balancing |
| Also relevant to | 05 Serving engines and simulators (Vidur) |
| Paper type | method evaluated in simulation |
| Venue and status | preprint only (arXiv v1, 17 Aug 2026, UC Berkeley EECS authors; no peer-reviewed venue found; low evidential weight) |
| Source read | full text (https://arxiv.org/pdf/2608.16336) |
| Verified on | 2026-10-30, against arXiv listing 2608.16336 |
| Relevance to project | Low to medium |

## APA 7 reference
Vestrum, A., Raeesi, A., & Roed, H. (2026). *Beyond binary priorities: Multi-tier SLA scheduling for large language model serving*. arXiv. https://doi.org/10.48550/arXiv.2608.16336

## In-text citation forms
(Vestrum et al., 2026) · Vestrum et al. (2026)

## 1. What it is about
Llumnix supports only two request priorities (high and normal). This paper generalises it to any number of tiers, each with reserved memory headroom, and asks how many tiers are worth having. It is tested in the Vidur simulator, not on real GPUs.

## 2. The problem
The authors state that production LLM services commonly sell three to five service tiers (not a cited survey). Round-robin or FCFS dispatch cannot isolate them, Llumnix's binary model is too coarse, and it is unclear how headroom should be split or whether more tiers cost performance.

## 3. Proposed solution
- Keep Llumnix's freeness F = (M − ΣV) / B and migration, but give tier p headroom H_p = M · h_max · e^(−λp) (example h_max = 0.20, λ = 1.0: tier 0 reserves 20% of KV capacity, about 31.1% in total for four tiers).
- A tier's full budget is charged whenever any of its requests is on the replica, so one critical request pushes normal traffic away.
- The dispatcher serves tier 0 first (FCFS within a tier) to the highest-freeness non-draining replica; migration runs every 50 ms or when the freeness gap exceeds 0.3.
- Two freeness values per replica: one with headroom for dispatch and migration, one without for auto-scaling (out below −0.5, in above 1.5).
- The INFaaS-style baseline scores queue depth, EWMA service time and a state penalty.

## 4. Data, models and tools
- Fork of the Vidur simulator (https://github.com/andersvestrum/llumnix_sim); baselines INFaaS+vLLM, Orca, Sarathi-Serve.
- Synthetic lengths of 64–512 tokens; three priority mixes (uniform, Gaussian, "enterprise"); 4 replicas; 10K and 15K requests; main sweeps at 1,250 QPS, scheduler comparison at 10 QPS. Model and GPU type not stated in the sections I read.

## 5. Key results
- Abstract and Table 2 (uniform distribution, 10K requests): prefill mean speedup up to 8.3× and end-to-end P99 speedup up to 3.1× over INFaaS, cost-per-latency improvements of 46–68% over the two scales.
- Four tiers gave the best result in all three distributions (peak P99 speedup and cost-per-latency); at 15K requests the gains fall (uniform distribution, prefill P99 2.72–3.16× versus 4.16–4.87× at 10K).
- Up to 10 tiers did not collapse tail latency at moderate load; the overhead shows mainly in prefill (Section 5.2).
- At 10 QPS all four schedulers have near-identical aggregate latency (P99 about 1.58–1.63 s at K = 1), so that test shows only overhead parity, not tier benefits.

## 6. Limitations
- *Stated by authors:* static headroom (adaptive headroom, MLFQ-style promotion, Vidur-Search tuning left for future work); simulator results are not directly comparable with Llumnix's hardware results; the scheduler comparison runs below saturation.
- *My observations:* all results come from the authors' own re-implementations in a simulator; synthetic lengths; speedups exceed Llumnix's reported numbers, explained but untested; 1,250 QPS on four replicas is unexplained; no sign of peer review, so treat as indicative; priorities are random, not from real tenants.

## 7. Relevance to the AI Request Router
- **Live-load signals:** separating dispatch freeness from scaling freeness keeps priority reservations out of capacity-planning signals.
- **Reuse:** 3–4 tiers (interactive, standard, batch) are a sensible default for latency budgets; geometric headroom decay is a simple per-tier reservation rule.
- **Not covered:** do not cite its speedups as router evidence; it needs migration-capable engines, ignores model choice, and has no real hardware.

## 8. How to use it in the report
- Brief mention in the section on priority and SLA differentiation, after Llumnix (Sun et al., 2024), flagged as a simulation-only preprint.
- Synthesis sentence: "Vestrum et al. (2026) extend Llumnix's two priority levels to K tiers in simulation and find four tiers to be the best trade-off, though the finding awaits validation on real GPUs."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Vestrum et al. (2026) | Support more than two SLA tiers in a migration-based LLM scheduler | Per-tier exponentially decaying headroom in Llumnix freeness; tier-aware dispatch | Vidur simulator, synthetic lengths, 3 priority mixes, 4 replicas | 4 tiers best; up to 8.3× prefill mean and 3.1× E2E P99 speedup over simulated INFaaS | Simulation only; own baselines; unreviewed preprint |
