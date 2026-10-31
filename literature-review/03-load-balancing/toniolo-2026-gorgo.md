Status: DRAFT
Depends on: D08; D12
Sources: Primary URLs in source table and proposal-audit section
Open items: Scoped numerical/final-version checks recorded below

# GORGO: tuned cost-model routing across regions (Toniolo et al., 2026)

| Field | Value |
|---|---|
| Topic (home) | 03 LLM load balancing |
| Also relevant to | 08 Serving frameworks (SGLang, AIBrix baselines) |
| Paper type | method plus released dataset |
| Venue and status | preprint only (arXiv v3, 29 Jul 2026; first posted 12 Feb 2026; title changed between versions) |
| Source read | full text of v3 (https://arxiv.org/pdf/2602.11688) |
| Verified on | 2026-10-30, against arXiv listing 2602.11688 |
| Relevance to project | High |

## APA 7 reference
Toniolo, A. R., Thorstenson, R., & Dinesh, A. (2026). *GORGO: Online tuning for cross-region network-aware LLM serving*. arXiv. https://doi.org/10.48550/arXiv.2602.11688

## In-text citation forms
(Toniolo et al., 2026) · Toniolo et al. (2026)

## 1. What it is about
GORGO is a proxy that routes each request to one of several globally spread inference engines by adding three estimated first-token costs: network round trip, queueing delay and the prefill time left after prefix-cache reuse. Two weights are tuned online by a simple evolutionary search to minimise 95th-percentile time to first token (p95 TTFT).

## 2. The problem
Existing balancers consider replica load (least-load, least-request) or KV-cache locality (session affinity, prefix cache), some both, but none consider cross-region network latency, which the paper measures at roughly 10 ms to 1 s. Pure affinity can overload a warm replica. Public chat datasets (LMSYS-Chat-1M, WildChat-4.8M) lack long-context, high-reuse traffic.

## 3. Proposed solution
- **Cost model.** TTFT ≈ W_rtt·T_network + W_queue·T_queue + T_prefill(tokens not cached on the replica); the prefill weight is fixed to 1 since only ratios matter.
- **Signals.** T_network is an exponentially weighted moving average (EWMA) of a ping RTT measured every 30 s. T_queue is the total tokens of requests the proxy dispatched to that replica and has not seen complete, tracked on the proxy. Prefill cost uses a proxy-side prefix trie.
- **Online tuning.** A (1+1) evolution strategy perturbs the weights multiplicatively and keeps the better, judged by p95 TTFT over a rolling 128-request window; start 0.5 and 0.1, hand-set ranges.
- **Dataset.** ART-Chat-2.5M, synthetic from a week of production metadata: 2,525,215 requests, average input 17,964 tokens, 89.4% intra-user prefix reuse (Table 1). Code and data: https://github.com/atoniolo76/GORGO.

## 4. Data, models and tools
- SGLang engines in Ashburn, Frankfurt and Seoul, two L40S GPUs each, Qwen3.5-35B-A3B FP8.
- Baselines: least-load, least-request, prefix-cache (AIBrix-style trie), simple session affinity. SGLang metrics are scraped from the Prometheus `/metrics` endpoint every 30 s.
- Three 30-minute windows: weights tuned on the first, frozen for two held-out ones. Extra: WildChat (appendix), BFCL multi-turn replay.

## 5. Key results
- Held-out windows versus session affinity: p95 TTFT better by 6.9–15.5% and p95 end-to-end (E2E) latency by 14.3–30.9% (Table 2); I recomputed these from the table.
- On the tuning window GORGO's p95 TTFT (2,514 ms) was slightly worse than session affinity (2,428 ms); weights converged after 672 samples (w_rtt = 0.276, w_queue = 0.5).
- Prefix-cache routing had the worst p95 E2E (22.6 s on the tuning window).
- BFCL replay: p95 TTFT down 7.6% and p95 E2E down 7.9% (Table 3).
- Setting the queue weight to 0 gave 17% better p95 TTFT but collapsed E2E latency (Appendix D).

## 6. Limitations
- *Stated by authors:* weights are specific to a saturation level, so sweep the time scale first; the TTFT objective can be gamed through continuous batching at the cost of E2E latency.
- *My observations:* one model, three regions, one proxy; synthetic trace; 30-minute windows over three days; hand-picked weight ranges; no replica failures; effect of the 30 s scrape not isolated; preprint revised several times.

## 7. Relevance to the AI Request Router
- **Live-load signals:** the best example for a gateway reading Prometheus: proxy-side in-flight bookkeeping combined with scraped engine metrics, with 30 s staleness explicit. Per-backend network latency also suits hosted versus local backends.
- **Reuse:** weighted linear cost with a unit weight; EWMA of latency probes; proxy-side counters between scrapes; tuning on rolling p95.
- **Not covered:** one model only; no difficulty, quality or cost term; tuning can overfit one load regime.

## 8. How to use it in the report
- Section on cost-model routing and on signal staleness; Chapter 3 design of the live-load term and tuning of its weights.
- Synthesis sentence: "Toniolo et al. (2026) combine network round trip, proxy-tracked queue tokens and uncached prefill into one first-token cost whose weights are tuned online, but only across replicas of one model."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Toniolo et al. (2026) | Route across regions using cache, load and network latency | Linear TTFT cost model; (1+1)-ES tuning of two weights on p95 TTFT | SGLang, 3 regions, Qwen3.5-35B-A3B, ART-Chat-2.5M | 6.9–15.5% better p95 TTFT, 14.3–30.9% better p95 E2E than session affinity on held-out windows | Single model; synthetic trace; regime-specific weights; preprint |


## 2026-10-31 proposal audit

- Source attempted: https://arxiv.org/abs/2602.11688.
- Scope: Abstract/metadata check only in this session; detailed numerical results remain unchecked.
- Historical Source read above records the earlier session, not a claim of a fresh full reading.
- arXiv title matched: GORGO: Online Tuning for Cross-Region Network-Aware LLM Serving. Latest listed version: v3; arXiv DOI identifies the preprint, not peer review. A missing journal reference does not prove that no published version exists.
