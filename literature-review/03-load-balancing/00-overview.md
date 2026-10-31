# 03 LLM load balancing: overview

## 1. Topic definition and why it matters to the router
Load balancing here means choosing which backend instance (replica, GPU or region) serves each LLM request so that latency, throughput and cost stay within targets while the load on instances changes second by second. LLM requests are unusually uneven: prompt lengths vary widely, output length is unknown until generation ends, and memory in the KV cache (the stored attention state of a request) grows during decoding. Classic policies such as round-robin or "fewest connections" therefore leave some instances overloaded while others idle. The AI Request Router adds a live-load term next to difficulty, quality and cost, so this topic decides which signals to read from vLLM/Prometheus (queue length, KV-cache use, tokens per second), how stale they may be, and which routing rule beats round-robin or least-busy.

## 2. Comparison of papers
| Paper | Year | Type | Venue | Problem | Method | Key result | Limitation |
|---|---|---|---|---|---|---|---|
| [Sun et al. (Llumnix)](sun-2024-llumnix.md) | 2024 | system | OSDI 2024 | Imbalance, fragmentation and priorities across LLM instances | Live KV migration; queue-aware "freeness" load metric; global plus per-instance schedulers | Prefill up to 26.6× (mean) and 34.4× (P99) better than round-robin; up to 36% cost saving | One model; needs engine internals; report staleness not studied |
| [Jain et al.](jain-2024-intelligent-router.md) | 2024 | method | preprint | Route among identical replicas | Output-length predictor, mixing penalty, RL router | 11.43% lower latency than round-robin; join-shortest-queue only 0.46% | Same-model replicas; RL training; modest gains |
| [Kossmann et al.](kossmann-2024-gpu-half-empty.md) | 2024 | empirical + method | preprint | Practical balancer and queue scheduler | SAL: queued tokens + free memory, polled 10 Hz | 1.0–1.5× lower p50 TTFT than next-best balancer | Small margin over P2C; replayed traces |
| [Srivatsa et al. (Preble)](srivatsa-2025-preble.md) | 2025 | system | ICLR 2025 | Prefix reuse vs balance across GPUs | E2 policy: windowed token load + eviction + prefill cost | 1.5×–14.5× lower mean latency than round-robin SGLang | Needs high prompt sharing |
| [Qin et al. (Mooncake)](qin-2025-mooncake.md) | 2025 | system | FAST 2025 | SLO-bound chatbot at scale | Cache-aware prefill scheduling; reject if SLO unreachable; early rejection with load prediction | Mean TTFT 3.07 s vs 19.65 s random; 59%–498% more effective capacity | Infrastructure-heavy; manual thresholds |
| [Chen et al. (SLOs-Serve)](chen-2025-slos-serve.md) | 2025 | system | preprint | Per-stage SLOs and bursts | DP token scheduler; admission control; SLO-based replica hopping | 2.2× per-GPU capacity; 4.61× on 4 replicas (ChatBot) | Needs profiling per GPU; ≤4 replicas |
| [Yuan et al. (L4/CascadeInfer)](yuan-2025-l4-cascadeinfer.md) | 2025 | system | preprint | Length heterogeneity in batches | Length-staged replica pipeline; decentralised bid-ask migration | Up to 67% lower latency; 1.71× throughput vs Llumnix (heavy load) | Long-context only; engine access |
| [Xia et al. (SkyWalker)](xia-2026-skywalker.md) | 2026 | system | EuroSys 2026 | Cross-region cost and cache locality | Regional balancers; selective pushing on pending requests (100 ms probes) | 1.12–2.06× throughput; 25% cost saving | Homogeneous replicas; GDPR |
| [Toniolo et al. (GORGO)](toniolo-2026-gorgo.md) | 2026 | method | preprint | Cross-region cost model | RTT + proxy queue tokens + uncached prefill; weights tuned online | 6.9–15.5% better p95 TTFT than session affinity (held-out) | One model; synthetic trace |
| [Vestrum et al.](vestrum-2026-multi-tier-sla.md) | 2026 | method (simulated) | preprint | More than two SLA tiers | Per-tier headroom in Llumnix freeness | 4 tiers best; up to 3.1× E2E P99 vs simulated INFaaS | Simulation; own baselines |
| [Da & Kalyvianaki (RouteBalance)](da-2026-routebalance.md) *(added)* | 2026 | system | preprint | Model choice and load together | Quality–latency–cost score; KNN estimator; dead-reckoned load | 2.6–4.1× faster than enhanced BEST-Route at high load | One family; offline quality labels |

## 3. Themes and trends
**What the papers read as "load".** Request counts are the weakest signal. Jain et al. found join-shortest-queue only 0.46% better than round-robin, and SkyWalker showed a fixed cap on outstanding requests performs worse than a check for a waiting request because one replica held 20 to 50 requests depending on request size. The stronger signals are memory-based and token-based:
- Llumnix: virtual KV memory including queued demand, divided by batch size.
- Kossmann: queued prefill tokens and free memory; Yuan and Preble: token counts and sequence lengths.
- SkyWalker: whether a replica has a pending (not yet admitted) request.
- Mooncake, SLOs-Serve: a predicted finish time compared with an SLO.
- GORGO: network RTT plus proxy-tracked in-flight tokens plus uncached prefill.
- RouteBalance: queue depth, pending decode work, KV pressure and service rate.

**How stale the signals are.** Almost no paper measures staleness; they only state their refresh rates: 10 Hz polling (Kossmann), 100 ms probes (SkyWalker), 30 s Prometheus scrapes and 30 s RTT probes (GORGO), a 3-minute window of scheduler-side token counts (Preble), periodic reports of unstated period (Llumnix). Three papers handle staleness by design rather than by faster polling: optimistic local updates between polls (Kossmann), dead reckoning (RouteBalance, GORGO's proxy-tracked tokens) and decentralised exchange (Yuan). Mooncake's extended study gives the one clear failure example: acting on lagged decode load made prefill and decode load oscillate until load was predicted.

**What beats round-robin or least-busy.** Everything memory- or token-aware beats round-robin, by 11% (Jain, RL router) to more than 20× on prefill latency (Llumnix, on bursty variable-length traces). Against smarter baselines such as P2C or session affinity, margins shrink to roughly 1.0–1.5× (Kossmann) or 7–31% (GORGO). Gains depend on workload: prefix-aware policies help only with heavy prompt sharing (Preble, SkyWalker, GORGO), and Jain et al. saw gains fall from about 11% to 7.8% on a production trace where prompts dominate.

**Three generations.** (1) Dispatch-time balancing on memory (Llumnix, Kossmann); (2) cache-aware and SLO-aware routing with predicted times (Preble, Mooncake, SLOs-Serve, GORGO); (3) joint decisions with other objectives, namely cross-region cost (SkyWalker) and model choice (RouteBalance). Rescheduling by migration (Llumnix, Yuan, Vestrum) is powerful but sits inside the engine, so it is out of reach for an external gateway.

## 4. Strongest three papers for the proposal
1. **Kossmann et al. (2024)**: gives a gateway-implementable recipe (poll queued tokens and free memory, correct between polls, route on estimated wait) and compares it with random and power-of-two-choices baselines (random stands in for round-robin) under production-style traces; Llumnix is surveyed, not evaluated. Preprint, so cite with that note.
2. **Sun et al. (2024), Llumnix**: the peer-reviewed anchor showing round-robin fails for variable-length traffic and that queued demand must count as load; its freeness idea maps onto vLLM metrics.
3. **Toniolo et al. (2026), GORGO**: the clearest worked example of a weighted cost over Prometheus-scraped metrics and proxy-side counters, with the scrape interval stated and online weight tuning. Also a preprint.

Must-cite for the gap statement (not on the supervisor's list): **Da & Kalyvianaki (2026), RouteBalance**, the closest prior art to the "model choice plus live load" claim.

## 5. Gaps visible in this topic
- **Model choice and load are almost never combined.** All ten assigned papers balance replicas of one model; the only exception is RouteBalance (added), which covers self-hosted Qwen sizes on one cluster. None covers hosted APIs together with self-hosted backends. Evidence: Sun, Jain, Kossmann, Srivatsa, Qin, Chen, Yuan, Xia, Toniolo, Vestrum.
- **Engine-level methods are unusable for a gateway.** Migration (Sun, Yuan, Vestrum), performance models of the batch (Chen) and disaggregated KV stores (Qin) need engine access that a gateway in front of Ollama, vLLM or an API does not have.
- **Signal staleness and polling cost are not studied.** Only refresh rates are stated (10 Hz, 100 ms, 30 s); no paper varies the scrape interval and reports its effect on routing quality, except Mooncake's qualitative oscillation finding.
- **Latency budgets are per-stage or per-tier, not per-request and per-prompt.** SLOs-Serve and Mooncake use SLO checks and rejection; Vestrum adds tiers; none ties the budget to a predicted prompt difficulty.
- **Failure and failover are barely evaluated.** SkyWalker recovers from a balancer failure and RouteBalance removes a tier, but none tests backend errors, timeouts or circuit breaking under load.
- **Evidence quality.** Seven of the eleven are preprints without a peer-reviewed venue found (Jain, Kossmann, Chen, Yuan, Toniolo, Vestrum, Da); only Sun, Srivatsa, Qin and Xia are peer reviewed. Vestrum is simulation only, and most results rely on replayed or synthetic traces.

## 6. Paper files in this folder
- [sun-2024-llumnix.md](sun-2024-llumnix.md)
- [jain-2024-intelligent-router.md](jain-2024-intelligent-router.md)
- [kossmann-2024-gpu-half-empty.md](kossmann-2024-gpu-half-empty.md)
- [srivatsa-2025-preble.md](srivatsa-2025-preble.md)
- [qin-2025-mooncake.md](qin-2025-mooncake.md)
- [chen-2025-slos-serve.md](chen-2025-slos-serve.md)
- [yuan-2025-l4-cascadeinfer.md](yuan-2025-l4-cascadeinfer.md)
- [xia-2026-skywalker.md](xia-2026-skywalker.md)
- [toniolo-2026-gorgo.md](toniolo-2026-gorgo.md)
- [vestrum-2026-multi-tier-sla.md](vestrum-2026-multi-tier-sla.md)
- [da-2026-routebalance.md](da-2026-routebalance.md) (added, not on the original list)

### Related papers documented elsewhere
- 01 Routing algorithms: [RouteLLM](../01-routing-algorithms/ong-2025-routellm.md), [FrugalGPT](../01-routing-algorithms/chen-2024-frugalgpt.md), [Hybrid LLM](../01-routing-algorithms/ding-2024-hybrid-llm.md), [AutoMix](../01-routing-algorithms/aggarwal-2024-automix.md), [RouterDC](../01-routing-algorithms/chen-2024-routerdc.md), [benchmark routing (Shnitzer)](../01-routing-algorithms/shnitzer-2023-benchmark-routing.md), [routing survey (Varangot-Reille)](../01-routing-algorithms/varangot-reille-2026-routing-survey.md)
- 04 Cost reduction: [cascade routing (Dekoninck)](../04-cost-reduction/dekoninck-2025-cascade-routing.md)
- 05 Latency and speed (files not yet written when I checked): vLLM/PagedAttention, Orca, Sarathi-Serve, DistServe, Splitwise, Vidur, Etalon, Niyama; see [folder](../05-latency-and-speed/)
- 06 Error handling and fallback: SpotServe, DéjàVu (pending); see [folder](../06-error-handling-fallback/)
- 07 Testing and benchmarking: RouterBench, MT-Bench; see [folder](../07-testing-and-benchmarking/)
- 08 System design gateway: SGLang, AIBrix (pending); see [folder](../08-system-design-gateway/)

## 7. Search log
| Item | Detail |
|---|---|
| Dates | 2026-10-30 to 2026-10-31 |
| Databases and sources | arXiv API and abstract pages; USENIX pages (OSDI '24, FAST '25); ICLR 2025 proceedings; Crossref (DOIs and venues); web search for venue checks |
| Title searches | One arXiv title query per assigned paper (10 queries); all 10 found with unique matches |
| Discovery queries (arXiv, relevance order) | `all:"load balancing" AND all:LLM AND all:serving` (47 hits); `all:"request routing" AND all:"LLM inference" AND all:replicas` (1); `all:router AND all:"LLM serving" AND all:"load-aware"` (1); `all:"prefix cache" AND all:routing AND all:"LLM serving"` (11); `all:"multi-SLO" AND all:LLM AND all:serving` (6) |
| Counts | 66 hits across the five queries (with overlap); titles screened: top 8 per query (about 25 distinct); full text read: 11; included: 11 (10 assigned + RouteBalance) |
| Dropped | None. All ten assigned papers were reachable and verified; 2026 papers (GORGO, SkyWalker EuroSys, Multi-tier SLA) all exist on arXiv |
| Added | RouteBalance (arXiv 2606.17949): closest prior art to the project's gap |
| Verification notes | L4 (arXiv v1 title "L4: Low-latency and load-balanced LLM serving via length-aware scheduling") was retitled CascadeInfer in v3; GORGO's title changed between versions; Mooncake has a FAST '25 paper (different title and authors) and an extended ACM TOS version (DOI 10.1145/3773772), both read; Preble's arXiv v2 header says ICLR 2024 but the ICLR proceedings are 2025, which I used. Llumnix, Mooncake (FAST) and Preble have no DOI at USENIX/ICLR, so URLs are given and arXiv DOIs noted where relevant |
| Seen but not read (possible additions) | DualMap (2602.06502), CacheRoute (2608.19677), PolyServe (2507.17769), HFX (2508.15919), AdaServe (2501.12162), BanaServe (2510.13223), "A Year in LLM Serving" (2608.13573), a data-parallel load-balancing paper (2605.06113) |
| Caveat | Venue status was checked only on the arXiv, publisher and Crossref pages above; absence of a venue means none was found, not that none exists |
