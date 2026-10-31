Status: DRAFT
Depends on: D08; D12
Sources: Primary URLs in source table and proposal-audit section
Open items: Scoped numerical/final-version checks recorded below

# Mooncake: KVCache-centric scheduling for the Kimi service (Qin et al., 2025)

| Field | Value |
|---|---|
| Topic (home) | 03 LLM load balancing |
| Also relevant to | 05 Serving engines (prefill/decode disaggregation), 06 Fallback and overload handling |
| Paper type | system (production deployment) |
| Venue and status | peer-reviewed (23rd USENIX FAST, Feb 2025, Best Paper); extended version in *ACM Transactions on Storage* (2026) |
| Source read | full text of the FAST '25 paper (https://www.usenix.org/system/files/fast25-qin.pdf) and of arXiv v5 of the extended version (https://arxiv.org/pdf/2407.00079) |
| Verified on | 2026-10-30, against the USENIX FAST '25 page, arXiv 2407.00079 and Crossref (DOI 10.1145/3773772) |
| Relevance to project | High |

## APA 7 reference
Qin, R., Li, Z., He, W., Cui, J., Ren, F., Zhang, M., Wu, Y., Zheng, W., & Xu, X. (2025). Mooncake: Trading more storage for less computation: A KVCache-centric architecture for serving LLM chatbot. In *Proceedings of the 23rd USENIX Conference on File and Storage Technologies (FAST 25)* (pp. 155–170). USENIX Association. https://www.usenix.org/conference/fast25/presentation/qin (no DOI issued by USENIX)

Extended version: Qin, R., Li, Z., He, W., et al. (2026). Mooncake: A KVCache-centric disaggregated architecture for LLM serving. *ACM Transactions on Storage*. https://doi.org/10.1145/3773772 (volume details not checked)

## In-text citation forms
(Qin et al., 2025) · Qin et al. (2025)

## 1. What it is about
Mooncake is the serving platform behind Moonshot AI's Kimi chatbot. It splits prefill and decode onto separate GPU pools and uses spare cluster CPU, DRAM and SSD as a shared KV-cache store. A global scheduler, "Conductor", sends each request to the prefill node with the lowest predicted first-token time and rejects requests that cannot meet their latency targets.

## 2. The problem
In a large chat service long prompts often repeat earlier context. Routing to the node holding the cached prefix saves compute, but that node may be busy; balancing on request counts ignores cache hits, and chasing hits alone overloads hot nodes. First-token (TTFT) and inter-token (TBT) targets must hold, including under overload.

## 3. Proposed solution
- **Cache-aware prefill scheduling.** Per prefill node, estimate queue time (sum of predicted prefill times of queued requests) + prefill time (offline polynomial regression on request length and cached prefix) + any KV transfer time. The lowest total wins; if it exceeds the TTFT target, or the decode node would miss the TBT target, the request is rejected (HTTP 429).
- **Cache load balancing.** If the best-cache node is too busy, the request goes elsewhere and that node copies the KV blocks when transfer beats recomputation, spreading hot blocks; the threshold is hand-set.
- **Overload handling (extended version).** Load is predicted TTFT/TBT versus the SLOs. "Early rejection" checks decode load before prefill starts, but observing decode load with a time lag makes prefill and decode load oscillate; predicting decode load at system level reduces this.

## 4. Data, models and tools
- Production-derived traces: conversation (12,031 requests, mean input 12,035 tokens), tool and agent, synthetic.
- Nodes with 8× A800-80GB and 200 Gbps RDMA (16 nodes); baseline vLLM v0.5.1 with and without prefix caching and chunked prefill. Code availability not checked.

## 5. Key results
- Abstract: effective request capacity (TTFT ≤ 30 s and TBT of 100–300 ms) 59%–498% higher than baselines; Kimi handles 115% more requests on A800 and 107% more on H800 clusters.
- Prefill scheduling (Fig. 5, 16 nodes): mean TTFT 3.07 s global cache-aware, 3.58 s local cache-aware, 5.27 s load-balancing only, 19.65 s random.
- Tool/agent workload: 42% more effective capacity than vLLM with prefix caching at 200 ms TBT.
- Overload test (extended version, 2× replay of 23,000 requests): rejections fell from 4,183 to 3,771 (early rejection) to 3,589 (with prediction).

## 6. Limitations
- *Stated by authors:* cache-balancing threshold tuned manually; request-level output-length prediction is future work.
- *My observations:* one long-context chatbot, single model, RDMA clusters; baselines are vLLM variants; the two versions differ in title, authors and content, so cite numbers to the right one; small overload experiment.

## 7. Relevance to the AI Request Router
- **Live-load signals:** the "estimated finish time" pattern (queue + execution + transfer versus an SLO) and the lesson that lagged load readings cause oscillation, so a gateway polling Prometheus should smooth or predict load.
- **Reuse:** predicted-time scoring per backend; reject or fall back when a latency budget cannot be met; early admission checks.
- **Not covered:** the disaggregated KV store is out of scope; no model choice.

## 8. How to use it in the report
- Section on SLO-driven admission and overload, and on staleness of load signals.
- Synthesis sentence: "Qin et al. (2025) rank prefill nodes by predicted queue plus compute time and reject requests that cannot meet the first-token target; their extended study shows lagged decode load makes load oscillate."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Qin et al. (2025) | Maximise SLO-compliant throughput of a long-context chatbot | KVCache-centric disaggregation; Conductor scoring by queue + prefill + transfer time; early rejection with load prediction | Kimi traces, 16×8 A800, vLLM baselines | 59%–498% higher effective capacity; global cache-aware mean TTFT 3.07 s vs 19.65 s random | Single model; manual thresholds; infrastructure heavy |


## 2026-10-31 proposal audit

- Source attempted: https://arxiv.org/abs/2407.00079.
- Scope: Full-text sample: method and selected numerical/limitation statements checked; see L07.
- Historical Source read above records the earlier session, not a claim of a fresh full reading.
- arXiv title matched: Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving. Latest listed version: v5; arXiv DOI identifies the preprint, not peer review. A missing journal reference does not prove that no published version exists.
