Status: DRAFT
Depends on: D08; D12
Sources: Primary URLs in source table and proposal-audit section
Open items: Scoped numerical/final-version checks recorded below

# Niyama / QoServe: QoS-aware co-scheduling (Goel et al., 2025)

| Field | Value |
|---|---|
| Topic (home) | 05 Latency and speed |
| Also relevant to | 03 Load balancing (SLO tiers), 06 Fallback (graceful degradation) |
| Paper type | system (scheduler) |
| Venue and status | peer-reviewed successor QoServe, ASPLOS 2026, DOI 10.1145/3779212.3790206 (Crossref confirmed); earlier Niyama preprint remains the version read |
| Source read | full text of the arXiv v1 preprint (https://arxiv.org/pdf/2503.22562). I did not read the published QoServe version, so numbers are cited to the preprint |
| Verified on | 2026-10-31, against arXiv abs 2503.22562 and the Crossref record of the ASPLOS paper |
| Relevance to project | High |

## APA 7 reference
Goel, K., Mohan, J., Kwatra, N., Anupindi, R. S., & Ramjee, R. (2026). QoServe: Breaking the silos of LLM inference serving. In *Proceedings of the 31st ACM International Conference on Architectural Support for Programming Languages and Operating Systems, Volume 2* (pp. 1492–1507). Association for Computing Machinery. https://doi.org/10.1145/3779212.3790206

## In-text citation forms
(Goel et al., 2025) · Goel et al. (2025). Switch to Goel et al. (2026) if the published text is used.

## 1. What it is about
Niyama (renamed QoServe) serves requests of different latency classes on one cluster instead of separate "interactive" and "batch" clusters. Each request gets a deadline from its class, which drives chunk sizes, ordering and the dropping of hopeless requests in overload.

## 2. The problem
Providers keep interactive traffic (tight TTFT and TBT) and batch traffic in separate silos, which over-provisions GPUs and copes badly with surges. Co-scheduling is hard because the strictest class forces small prefill chunks.

## 3. Proposed solution
- **QoS classes and deadlines (Section 3.2).** Interactive requests have a TTFT and TBT target; the first-token deadline is arrival + SLO_TTFT and token n's deadline is arrival + SLO_TTFT + (n − 1) · SLO_TBT. Non-interactive requests have one total-latency (TTLT) deadline.
- **Dynamic chunking.** Compute each decoding request's slack (next-token deadline minus now) and pick the largest prefill chunk that breaks no deadline.
- **Hybrid prioritisation.** Priority = deadline + α · remaining prefill time: Earliest-Deadline-First (EDF) behaviour at low load, shortest-remaining-prefill-first (SRPF) behaviour near overload. Unknown decode length of batch requests is over-approximated from history by two standard deviations.
- **Eager relegation.** A request that has missed or is about to miss its deadline moves to a relegated queue, low-priority (for example free-tier) requests first, so the rest keep their SLOs.
- **Selective preemption.** Only requests still in prefill are preempted, and only if their deadline survives.

## 4. Data, models and tools
- Llama3-8B on one A100-80GB and Qwen-7B on two A100s; ShareGPT and Azure code and conversation traces with Poisson arrivals; three equal QoS buckets: one interactive (TTFT 6 s, TBT 50 ms) and two non-interactive (TTLT 600 s and 1,800 s).
- Built on Sarathi-Serve/vLLM; baselines Sarathi-Silo, Sarathi-FCFS, Sarathi-EDF, Sarathi-SRPF.

## 5. Key results
- Abstract: 32% more serving capacity than siloed deployments while keeping QoS, and an order of magnitude fewer SLO violations under extreme load.
- To serve 50 queries/s, Niyama needs 13–32% fewer A100 GPUs than the siloed baseline across three datasets (Section 4.1.1; a replica's capacity is the load at which at most 1% of requests violate QoS).
- Goodput (requests/s meeting P99 targets, at most 1% violations) is 1.5×–2.4× that of Sarathi-FCFS and 20–40% above Sarathi-EDF on Azure-Code (Section 4.1.2).
- Fig. 5: without relegation, median latency grows through a cascade of violations as load rises; relegating about 5% of requests keeps it within SLO. EDF alone nears 100% violations past a load threshold (Fig. 2).

## 6. Limitations
- *Stated by authors:* the decode-length over-approximation is a simple heuristic.
- *My observations:* small models, at most two A100s per replica; QoS buckets and SLOs are the authors' constructions; relegation delays real requests; preprint and published versions may differ; a single-engine scheduler, not a router.

## 7. Relevance to the AI Request Router
- **Latency budgets:** a clear per-request deadline model (arrival + TTFT target + (n − 1) × TBT target, or one total-latency deadline for batch work) that maps to the router's latency-budget parameter.
- **Queueing and the tail:** the cascade of violations past capacity (Fig. 5, median latency up by orders of magnitude) justifies redirecting work before a backend reaches its knee.
- **Reuse:** a relegated or fallback class (compare the best-effort tier in [SLOs-Serve](../03-load-balancing/chen-2025-slos-serve.md)); free-versus-paid tiering; historical mean plus two standard deviations for unknown output length.
- **Not covered:** routing across backends or models.

## 8. How to use it in the report
- Subsection on latency budgets and graceful degradation under overload.
- Synthesis sentence: "Niyama (Goel et al., 2025) assigns each request a deadline from its QoS class and relegates a small share of doomed requests under overload, which kept latency within SLO where deadline-first scheduling alone collapsed."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Goel et al. (2025) | Co-schedule mixed-latency classes on shared GPUs | Deadlines per QoS class; dynamic chunking; EDF/SRPF hybrid; eager relegation | Llama3-8B, Qwen-7B, A100; Azure traces, ShareGPT | 32% more capacity than silos; 13–32% fewer GPUs; 1.5–2.4× goodput vs FCFS | Small models; own SLO buckets; preprint vs published versions |


## 2026-10-31 proposal audit

- Source attempted: https://arxiv.org/abs/2503.22562.
- Scope: Abstract/metadata check only in this session; detailed numerical results remain unchecked.
- Historical Source read above records the earlier session, not a claim of a fresh full reading.
- arXiv title matched: Niyama : Breaking the Silos of LLM Inference Serving. Latest listed version: v1; arXiv DOI identifies the preprint, not peer review. A missing journal reference does not prove that no published version exists.
- Crossref confirms the published successor QoServe at ASPLOS 2026, DOI https://doi.org/10.1145/3779212.3790206. Published text not read; do not transfer Niyama numbers to QoServe without comparison.


## Published-version preference

Canonical metadata will use QoServe (2026), confirmed through Crossref. The Niyama preprint remains the only full text read in the earlier summary; all numerical findings above remain attached to that preprint and must not be transferred to the final version without checking. Historical filename retained for links.
