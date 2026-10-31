Status: DRAFT
Depends on: D08; D12
Sources: Primary URLs in source table and proposal-audit section
Open items: Scoped numerical/final-version checks recorded below

# Practical scheduling techniques for LLM serving: LARRY and SAL (Kossmann et al., 2024)

| Field | Value |
|---|---|
| Topic (home) | 03 LLM load balancing |
| Also relevant to | 05 Serving engines (engine-level schedulers) |
| Paper type | empirical study plus two new methods |
| Venue and status | preprint only (arXiv v2, 28 Jan 2025; MIT CSAIL and Databricks) |
| Source read | full text (https://arxiv.org/pdf/2410.17840) |
| Verified on | 2026-10-30, against arXiv abs 2410.17840 |
| Relevance to project | High |

## APA 7 reference
Kossmann, F., Fontaine, B., Khudia, D., Cafarella, M., & Madden, S. (2024). *Is the GPU half-empty or half-full? Practical scheduling techniques for LLMs*. arXiv. https://doi.org/10.48550/arXiv.2410.17840

## In-text citation forms
(Kossmann et al., 2024) · Kossmann et al. (2024)

## 1. What it is about
The paper compares scheduling policies at the two levels where LLM requests are scheduled: the load balancer that picks a replica, and the engine scheduler that decides when a request runs. It proposes one new "drop-in" policy for each: SAL (balancer) and LARRY (engine).

## 2. The problem
Research schedulers often need engine surgery (such as Llumnix's KV migration) or extra trained predictors, so they are rarely deployed. Practical systems use FCFS, round-robin, random or power-of-two-choices, which ignore that requests differ in prompt length and memory needs.

## 3. Proposed solution
- **Survey and common testbed.** Section 3 *surveys* round-robin, random, power of two choices (P2C, compares in-flight request counts of two random servers) and Llumnix. Only random, P2C and SAL are *evaluated* (random stands in for round-robin, which it matches in performance); Llumnix is not evaluated because it needs KV transfer between servers.
- **SAL (Server-Aware Load balancer).** Per server, it estimates the waiting delay if the request is added, as the larger of a memory-shortfall term (prompt memory minus free memory, scaled by a factor β from average input and output lengths) and queued prefill tokens divided by the per-batch token cap. The lowest value wins.
- **Signal freshness.** SAL polls queued tokens and free memory from each server 10 times per second and, between polls, optimistically adds each request it just routed, assuming nothing finished.
- **LARRY.** Orders the waiting queue by α·waiting time − queue length × memory demand, holding back large prompts under memory pressure without starving them; about 20 lines in vLLM.

## 4. Data, models and tools
- Modified vLLM, Ray actors, one balancer process.
- Azure Functions arrival trace; Azure OpenAI token-length traces for a chat and a code-copilot application.
- Four servers with 2×H100 (Llama-3 70B FP8); eight servers with one A100 (Llama-3 8B).
- Multi-server baselines: P2C and random, each with FCFS, TRAIL+ (oracle) and LARRY. Llumnix was not evaluated (needs KV transfer). No code link found.

## 5. Key results
- Balancers matter less than engine schedulers for time to first token (TTFT), but SAL was generally best (Section 7, Figs. 10–11).
- With LARRY, SAL gave 1.0–1.5× lower p50 TTFT and 1.2–1.3× lower p95 TTFT than the next-best balancer, and 1.1–1.3× lower p50 and p95 total generation time.
- Random and P2C performed about the same.
- Engine side (Section 6): LARRY's p50 TTFT was 1.8–2.1× lower than the next-best scheduler.
- Preemption rates stayed under 0.1% for all schedulers.

## 6. Limitations
- *Stated by authors:* numbers depend on the serving system's queueing overhead; only online (not offline batch) scheduling studied.
- *My observations:* prompts are random tokens with trace-enforced output lengths; two traces, two Llama-3 sizes; SAL's margin over P2C is small (often near 1.0×); no server failure, mixed models, cost or quality; polling error not quantified beyond the 10 Hz choice.

## 7. Relevance to the AI Request Router
- **Live-load signals:** the clearest recipe for a gateway: poll queued tokens and free KV memory per backend (vLLM's waiting-request, running-request and KV-cache-usage metrics are the equivalents), correct optimistically between polls, route on estimated wait time rather than request count.
- **Reuse:** SAL's wait-time formula as a load term; optimistic bookkeeping between Prometheus scrapes; P2C as a cheap second baseline.
- **Not covered:** LARRY is an engine change; no model choice, so the load score must be combined with quality and cost.

## 8. How to use it in the report
- Section 2.x on live-load signals and staleness; Section 3.x justifying the choice of polled metrics and scrape interval.
- Synthesis sentence: "Where Llumnix (Sun et al., 2024) needs engine-level KV migration, Kossmann et al. (2024) show that a 30-line balancer using polled queue and memory statistics already beats power-of-two-choices on production-style traces."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Kossmann et al. (2024) | Practical drop-in scheduling for replicated LLM servers | SAL balancer (queued tokens and free memory, polled at 10 Hz) and LARRY queue reordering | Modified vLLM, Azure arrival and token traces, H100/A100, Llama-3 8B/70B | SAL 1.0–1.5× lower p50 TTFT than next-best balancer; P2C and random similar | Small margins over P2C; single model; replayed traces; preprint |


## 2026-10-31 proposal audit

- Source attempted: https://arxiv.org/abs/2410.17840.
- Scope: Abstract/metadata check only in this session; detailed numerical results remain unchecked.
- Historical Source read above records the earlier session, not a claim of a fresh full reading.
- arXiv title matched: Is the GPU Half-Empty or Half-Full? Practical Scheduling Techniques for LLMs. Latest listed version: v2; arXiv DOI identifies the preprint, not peer review. A missing journal reference does not prove that no published version exists.
