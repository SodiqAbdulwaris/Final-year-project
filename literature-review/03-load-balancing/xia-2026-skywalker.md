# SkyWalker: cross-region load balancing with selective pushing (Xia et al., 2026)

| Field | Value |
|---|---|
| Topic (home) | 03 LLM load balancing |
| Also relevant to | 04 Cost reduction, 06 Fallback and failure recovery |
| Paper type | system |
| Venue and status | peer-reviewed (21st European Conference on Computer Systems, EuroSys '26, April 2026); arXiv first posted May 2025 |
| Source read | full text of arXiv v2 (https://arxiv.org/pdf/2505.24095), which carries the EuroSys '26 reference |
| Verified on | 2026-10-30, against arXiv abs 2505.24095 and Crossref record for DOI 10.1145/3767295.3769353 |
| Relevance to project | High |

## APA 7 reference
Xia, T., Mao, Z., Kerney, J., Jackson, E. J., Li, Z., Xing, J., Shenker, S., & Stoica, I. (2026). SkyWalker: A locality-aware cross-region load balancer for LLM inference. In *Proceedings of the 21st European Conference on Computer Systems (EuroSys '26)*. ACM. https://doi.org/10.1145/3767295.3769353

## In-text citation forms
(Xia et al., 2026) · Xia et al. (2026)

## 1. What it is about
SkyWalker is a set of per-region load balancers that let a provider with reserved GPUs in several regions spill traffic from a busy region to an idle one. It keeps KV-cache reuse through prefix-aware routing and avoids overloading replicas with "selective pushing".

## 2. The problem
Reserved or on-premise GPUs are provisioned per region for its own daily peak, so capacity idles off-peak. One central balancer fixes utilisation but adds up to about 200 ms cross-region latency, a bottleneck and a single point of failure. Round-robin and least-load also fail for LLMs because output length is unpredictable: memory use differed by up to 2.64× between two replicas under round-robin.

## 3. Proposed solution
- **Regional balancers.** DNS sends clients to the nearest balancer, which keeps a first-come-first-served queue. Requests go to an "available" local replica, otherwise to an available remote region with a short queue and the best prefix hit ratio.
- **Selective pushing by pending requests.** A replica is "full" when it has a pending request, one not yet admitted to the continuous batch because memory is exhausted. Replicas are probed every 100 ms (a batching step takes tens of ms) and peer balancers share availability by heartbeat. A fixed cap on outstanding requests fails because one replica held 20 to 50 requests depending on their size (Llama 3.1 8B on an L4).
- **Prefix-aware routing.** Consistent hashing on user and session ID (SkyWalker-CH) or an approximate prefix trie (SkyWalker).
- **Failure handling.** A controller probes health; a failed balancer's replicas go to the nearest balancer.

## 4. Data, models and tools
- About 3,000 lines of Python on SkyServe; any OpenAI-compatible engine (vLLM, SGLang).
- Up to 12 replicas in three regions; ChatBot Arena, WildChat and Tree-of-Thoughts workloads.
- Baselines: GKE Gateway, round-robin, least-load, consistent hashing, SGLang Router.

## 5. Key results
- Abstract: 1.12–2.06× higher throughput, 1.74–6.30× lower latency, 25% lower serving cost than existing balancers.
- Versus single-balancer systems, 1.12–1.2× throughput on the multi-turn chat datasets; versus GKE Gateway 1.43–2.06× (Section 5.1).
- Prefix-cache hit rates: round-robin 10.78–16.57%, least-load 28.29–31.13%, SkyWalker 36.96–46.55% on the chat datasets (Section 5.1).
- Selective pushing by pending requests (Section 5.2, Fig. 9): 1.27× throughput and 18.47× lower P90 TTFT than blind pushing; throughput 1.4× higher than the fixed-outstanding-cap variant at similar TTFT.
- Diurnal test (Fig. 10): 1.07–1.18× throughput over region-local deployment; 9 replicas matched what region-local needed 12 for, a 25% cost cut.
- The prefix-tree variant beat consistent hashing by 1.34–8.21%.

## 6. Limitations
- *Stated by authors:* GDPR may forbid cross-region aggregation; prefix sharing can leak information through side channels; heterogeneous accelerators are open (the pending-request check is hardware-agnostic); prompt length could improve routing.
- *My observations:* homogeneous replicas of one model; research prototype; replayed datasets, up to 12 replicas; gains over single-balancer baselines are modest (about 1.1–1.2×); 100 ms probing assumes cheap queue state.

## 7. Relevance to the AI Request Router
- **Live-load signals:** "does the backend have a waiting request?" is a cheap binary saturation signal that adapts to request sizes, unlike a fixed concurrency cap (my mapping: vLLM's waiting-requests gauge). Holding requests in the gateway queue beats pushing blindly.
- **Reuse:** gateway queue plus availability check; probe interval tied to batching step time; local-first routing with spillover; health probes.
- **Not covered:** multi-region DNS and cross-region prefix tries are beyond the project; no model selection, quality or cost.

## 8. How to use it in the report
- Section on live-load signals (queue-based saturation versus outstanding-request counts) and on failover.
- Synthesis sentence: "Xia et al. (2026) show that gating dispatch on whether a replica has a waiting request outperforms a fixed outstanding-request limit by 1.4× in throughput, because LLM request sizes vary too much for a static threshold."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Xia et al. (2026) | Cut cost via cross-region load balancing without losing KV-cache locality | Regional balancers, selective pushing on pending requests (100 ms probes), prefix-aware routing | SkyServe, vLLM/SGLang, ChatBot Arena, WildChat, up to 12 replicas | 1.12–2.06× throughput, 1.74–6.30× lower latency, 25% cost saving | Homogeneous replicas; GDPR and cache side-channel concerns |
