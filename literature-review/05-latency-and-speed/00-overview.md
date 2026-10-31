# 05 LLM response speed and latency: overview

## 1. Topic definition and why it matters to the router
This topic covers how LLM serving engines produce tokens, how their speed is defined and measured (time to first token, time between tokens, percentiles, goodput), and why latency rises sharply once a backend nears capacity. The AI Request Router must keep a latency budget per request, so it needs three things from this literature: precise metric definitions to report and test against, the metrics a vLLM backend exports to Prometheus, and a way to predict each backend's likely latency before sending a request. The papers show that the average hides the problem: queueing and prefill-decode interference dominate the tail, and the same engine can look fine or poor depending on the metric chosen.

## 2. Comparison of papers
| Paper | Year | Type | Venue | Problem | Method | Key result | Limitation |
|---|---|---|---|---|---|---|---|
| [Yu et al. (Orca)](yu-2022-orca.md) | 2022 | system | OSDI 2022 | Request-level batching makes requests wait for the slowest in the batch | Iteration-level scheduling (continuous batching), selective batching | 36.9× throughput at equal median normalised latency (GPT-3 175B vs FasterTransformer) | FCFS, no TTFT/tail metrics |
| [Kwon et al. (vLLM)](kwon-2023-pagedattention.md) | 2023 | system | SOSP 2023 | KV-cache waste limits batch size | PagedAttention, block tables, preemption | 2–4× throughput vs Orca and FasterTransformer at similar latency | Normalised latency only |
| [Leviathan et al.](leviathan-2023-speculative-decoding.md) | 2023 | method | ICML 2023 | Serial decoding is slow | Draft with small model, verify in parallel | 2–3× faster, identical outputs (T5-XXL) | Batch size 1; extra compute |
| [Agrawal et al. (Sarathi-Serve)](agrawal-2024-sarathi-serve.md) | 2024 | system | OSDI 2024 | Prefill stalls decodes | Chunked prefill, stall-free batching, token budget | 2.6× (Mistral-7B) to 5.6× (Falcon-180B) capacity vs vLLM at P99 TBT targets | Single replica |
| [Zhong et al. (DistServe)](zhong-2024-distserve.md) | 2024 | system | OSDI 2024 | Prefill/decode interference | Disaggregation; goodput-optimised placement; M/D/1 model | Up to 7.4× more requests or 12.6× tighter SLO | No preemption or fault tolerance |
| [Patel et al. (Splitwise)](patel-2024-splitwise.md) | 2024 | system + study | ISCA 2024 | Cost and power of colocated phases | Phase-split pools, JSQ on pending tokens | 1.4× throughput at 20% less cost | Simulated clusters |
| [Agrawal et al. (Vidur)](agrawal-2024-vidur.md) | 2024 | simulator | MLSys 2024 | Expensive deployment tuning | Operator profiling, RF regression, search | Under 9% latency error; about 1 hour on a 96-core CPU machine ($9.93/h) vs 42K GPU-hours | Error grows near capacity |
| [Agrawal et al. (Etalon)](agrawal-2024-etalon.md) | 2024 | benchmark | preprint | Metrics hide stalls | Fluidity-index; black-box API probing | Tail-TBT throughput 3× different while TPOT equal | Preprint; empirical targets |
| [Kamath et al. (POD-Attention)](kamath-2025-pod-attention.md) | 2025 | system (kernel) | ASPLOS 2025 | Hybrid batches waste GPU in attention | Fused prefill/decode attention kernel | Up to 59% faster attention; P99 TTFT up to 4.3× lower than Sarathi | Hardware-specific |
| [Goel et al. (Niyama/QoServe)](goel-2025-niyama.md) | 2025 | system | preprint; ASPLOS 2026 as QoServe | Siloed interactive/batch clusters | Deadline-based dynamic chunking, hybrid priority, relegation | 32% more capacity; 13–32% fewer GPUs | Small models |

## 3. Themes and trends

### 3.1 How the papers define and measure latency
| Metric | Definition (as used in the papers) | Where defined |
|---|---|---|
| TTFT (time to first token) | From request arrival to the first output token; includes scheduling delay and prompt processing | Sarathi-Serve Section 2.4; Etalon Section 2.2 |
| TBT (time between tokens) | Interval between consecutive output tokens of one request; reported as a tail percentile (P99) because every token produces a value | Sarathi-Serve, Splitwise, Etalon |
| TPOT (time per output token) | Average per-token decode time of a request, so it hides stalls | DistServe, Etalon |
| Normalised latency | End-to-end latency divided by output length, plotted against request rate | Orca, vLLM, Vidur |
| Scheduling delay | Time waiting before processing starts; Vidur caps P99 scheduling delay at 5 s, Sarathi-Serve caps median at 2 s, to call a load sustainable | Vidur Section 6; Sarathi-Serve Section 5.1 |
| Capacity | Highest request rate meeting latency targets while the queue stays bounded | Sarathi-Serve, Vidur, Etalon |
| Goodput | Highest per-GPU request rate at which a target share (for example 90%) of requests meet both TTFT and TPOT targets | DistServe |
| SLO attainment | Share of requests meeting all targets; Splitwise requires P50, P90 and P99 of TTFT, TBT and E2E all met | DistServe, Splitwise |
| Fluidity-index | Share of tokens meeting a per-token deadline with carried slack | Etalon |

Practical rule drawn from the set (my synthesis): report median TTFT with prompt length, P95/P99 TBT or inter-token latency, and attainment against a stated target, and never rely on average TPOT or normalised latency alone.

### 3.2 Metrics a vLLM backend exposes to Prometheus
Checked against the vLLM design page for metrics (https://docs.vllm.ai/en/latest/design/metrics.html, read 2026-10-31). Names change between versions, so check the deployed version's `/metrics` output.
| Router need | Metric (v1 engine) | Type |
|---|---|---|
| Queue length | `vllm:num_requests_waiting` | gauge |
| Running batch | `vllm:num_requests_running` | gauge |
| KV-cache pressure | `vllm:kv_cache_usage_perc` | gauge |
| TTFT | `vllm:time_to_first_token_seconds` | histogram |
| Inter-token latency (TBT) | `vllm:inter_token_latency_seconds` | histogram |
| Per-request TPOT | `vllm:request_time_per_output_token_seconds` | histogram |
| End-to-end latency | `vllm:e2e_request_latency_seconds` | histogram |
| Queue time | `vllm:request_queue_time_seconds` | listed without a stated type |
| Prefill and decode time | `vllm:request_prefill_time_seconds`, `vllm:request_decode_time_seconds` | histograms |
| Throughput | `vllm:prompt_tokens_total`, `vllm:generation_tokens_total` | counters |
| Prompt and output size | `vllm:request_prompt_tokens`, `vllm:request_generation_tokens` | histograms |
| Rejections | `vllm:admission_rejections_total` | counter |
| Prefix cache | `vllm:prefix_cache_queries`, `vllm:prefix_cache_hits` | counters |
The document also says swap-related metrics (`vllm:num_requests_swapped`, `vllm:cpu_cache_usage_perc`) no longer apply in v1 and lists no preemption metric. Percentiles must be estimated from histogram buckets (for example with `histogram_quantile` in Prometheus), which is coarser than the exact P99 values in the papers.

### 3.3 Why queueing dominates the tail
- Mechanism: in request-level batching, arrivals wait for the in-flight batch (Orca); with continuous batching, new prompts still wait for memory and for the prefill-prioritising scheduler (vLLM, Sarathi-Serve).
- Closed form: for a prefill instance with Poisson arrivals at rate R and execution time D, average TTFT is D + R·D² / (2(1 − R·D)), so queueing delay diverges as R·D approaches 1 (DistServe, Eq. 1).
- Evidence near capacity: with the Sarathi stall-free scheduler, median TTFT on the internal workload rose from 2.2 s to 25.4 s when load went from 1.1 to 1.2 queries/s (POD-Attention, Table 5); Vidur notes "tipping point" behaviour at capacity; Niyama shows median latency growing by orders of magnitude without relegation.
- Prefill-decode interference is the second cause: one added prefill raises TPOT of all running decodes (DistServe, Fig. 2); vLLM's default scheduler produced decode stalls for over 95% of requests (POD-Attention).
- The routing papers in [topic 03](../03-load-balancing/00-overview.md) use the same lesson, treating a waiting request or queued tokens as a sign a backend is full ([Xia et al.](../03-load-balancing/xia-2026-skywalker.md), [Kossmann et al.](../03-load-balancing/kossmann-2024-gpu-half-empty.md)).

### 3.4 Predicting a latency budget per backend (synthesis for the proposal)
No paper gives a ready recipe for a gateway, but the pieces combine into one:
1. **Prefill floor.** Fit prefill time against prompt tokens from a few isolated requests (Etalon Section 4.1; TTFT is near-linear in prompt length, Splitwise Fig. 5a; Vidur uses random-forest regression).
2. **Queue wait.** Estimate from queue size and recent service rate, or with the M/D/1 formula above (DistServe); for pending work, use tokens, not requests (Splitwise).
3. **Decode time.** Expected output tokens times measured TPOT; for unknown output length use the historical mean plus two standard deviations (Niyama) or a per-task estimate; allow for batch-size effects on TBT (Splitwise: about 2× at batch 64).
4. **Safety margin.** Predictions are accurate up to about 85% of capacity and unreliable beyond (Vidur Section 7.2); treat a backend above that load as unable to meet tight budgets.
5. **Deadline form.** Express budgets as arrival + TTFT target + (n − 1) × TBT target (Niyama, Etalon).
6. **Engine-dependent behaviour.** TTFT and TBT trade off by scheduler and chunk size (POD-Attention Table 7; Sarathi-Serve), and speculative decoding changes TPOT with acceptance rate (Leviathan), so calibrate per backend.

## 4. Strongest three papers for the proposal
1. **Sarathi-Serve (Agrawal et al., 2024b)**: the clearest peer-reviewed definitions of TTFT, TBT and capacity with an explicit stability condition and percentile choices.
2. **DistServe (Zhong et al., 2024)**: defines goodput and SLO attainment and supplies the M/D/1 closed form that links load to TTFT, directly usable in a latency-budget predictor.
3. **Etalon (Agrawal et al., 2024a)**: shows why averages mislead, and measures hosted APIs from the outside, the router's situation for remote backends. It is a preprint, so pair it with the first two.
Next best: Niyama/QoServe for deadline-based budgets and overload handling.

## 5. Gaps visible in this topic
- **Nothing is designed for a gateway.** Every paper optimises inside an engine or cluster it controls; none predicts a third-party backend's latency from client-side signals alone, except Etalon's black-box measurements, which only characterise it.
- **Metric fragmentation.** Orca/vLLM use normalised latency, Sarathi-Serve P99 TBT, DistServe goodput at 90% attainment, Splitwise slowdown ratios, Etalon fluidity; results are not comparable across papers (Etalon shows rankings flip with the metric).
- **Prometheus histograms versus paper percentiles.** The papers use exact per-request or per-token percentiles; a Prometheus-based router sees bucketed histograms and 15–30 s scrape intervals, an accuracy cost none of them discusses.
- **Accuracy near saturation.** Vidur is the only paper to quantify prediction error against load, and it degrades near capacity, exactly where routing matters.
- **Engine-specific effects.** Results depend on scheduler (vLLM versus Sarathi-style), chunk size and hardware, and speculative decoding is evaluated at batch size 1 only.
- **Evidence quality.** Eight of ten are peer reviewed (Etalon and Niyama's preprint are not, though Niyama has a published ASPLOS 2026 version I did not read). Most results are on A100/H100 clusters with Poisson arrivals and small open models.

## 6. Paper files in this folder
- [yu-2022-orca.md](yu-2022-orca.md)
- [kwon-2023-pagedattention.md](kwon-2023-pagedattention.md)
- [leviathan-2023-speculative-decoding.md](leviathan-2023-speculative-decoding.md)
- [agrawal-2024-sarathi-serve.md](agrawal-2024-sarathi-serve.md)
- [zhong-2024-distserve.md](zhong-2024-distserve.md)
- [patel-2024-splitwise.md](patel-2024-splitwise.md)
- [agrawal-2024-vidur.md](agrawal-2024-vidur.md)
- [agrawal-2024-etalon.md](agrawal-2024-etalon.md)
- [kamath-2025-pod-attention.md](kamath-2025-pod-attention.md)
- [goel-2025-niyama.md](goel-2025-niyama.md)

APA note: three 2024 papers share the first author and "et al.", so they carry suffixes a, b, c: Etalon 2024a, Sarathi-Serve 2024b, Vidur 2024c.

### Related papers documented elsewhere
- 03 Load balancing (all read in full): [Llumnix](../03-load-balancing/sun-2024-llumnix.md), [Kossmann et al.](../03-load-balancing/kossmann-2024-gpu-half-empty.md), [SLOs-Serve](../03-load-balancing/chen-2025-slos-serve.md), [Mooncake](../03-load-balancing/qin-2025-mooncake.md), [SkyWalker](../03-load-balancing/xia-2026-skywalker.md), [GORGO](../03-load-balancing/toniolo-2026-gorgo.md), [RouteBalance](../03-load-balancing/da-2026-routebalance.md)
- 04 Cost reduction: [cascade routing (Dekoninck)](../04-cost-reduction/dekoninck-2025-cascade-routing.md)
- 07 Testing and benchmarking: RouterBench, MT-Bench (pending); see [folder](../07-testing-and-benchmarking/)
- 08 System design gateway: SGLang, AIBrix (pending); see [folder](../08-system-design-gateway/)

## 7. Search log
| Item | Detail |
|---|---|
| Dates | 2026-10-31 |
| Databases and sources | arXiv API and abstract pages; USENIX pages (OSDI '22, OSDI '24); PMLR volume 202; MLSys 2024 proceedings; Crossref (DOIs, pages, venues); vLLM documentation (metrics) |
| Title searches | One arXiv title query per assigned paper (10 queries); 9 matched uniquely (Splitwise returned three unrelated titles besides the target; Etalon needed a second query; Orca is not on arXiv and was taken from USENIX) |
| Discovery queries (arXiv, relevance order) | `all:"time to first token" AND all:"LLM serving" AND all:latency` (51 hits); `all:goodput AND all:"LLM serving" AND all:SLO` (24); `all:"tail latency" AND all:"LLM inference" AND all:queueing` (6); `all:"latency prediction" AND all:"LLM inference" AND all:scheduling` (1); `all:"performance metrics" AND all:"LLM inference" AND all:benchmark AND all:TPOT` (1) |
| Counts | 83 hits across five queries (with overlap); titles screened: top 8 per query (about 30 distinct); full text read: 10; included: 10 (all assigned) |
| Dropped | None. All ten were reachable and verified, and all are 2020 or later (earliest: Orca, 2022) |
| Changes | Niyama (arXiv title) was published as QoServe at ASPLOS 2026; the arXiv v1 text was read, the published version was not. Mooncake and other topic-03 items were not repeated here |
| Verification notes | Vidur and Speculative decoding have no DOI at the venue (MLSys, PMLR); Orca, Sarathi-Serve and DistServe have none at USENIX. Their references give venue URLs, with arXiv DOIs where useful. PagedAttention, Splitwise, POD-Attention and QoServe DOIs were confirmed in Crossref |
| Seen but not read (possible additions) | Scorpio (2505.23022), AdaServe (2501.12162), JITServe (2504.20068), "Cascade: exploiting SLO-aware latency budget" (2608.06557), Ascendra (2504.20828), GAUSS simulator (2610.37989), "Latency Prediction for LLM Inference on NPU Systems" (2606.18042) |
| Caveat | Absence of a venue means none was found on the pages above, not that none exists |
