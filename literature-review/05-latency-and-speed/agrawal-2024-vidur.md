# Vidur: simulating LLM inference performance (Agrawal et al., 2024c)

| Field | Value |
|---|---|
| Topic (home) | 05 Latency and speed |
| Also relevant to | 07 Testing and benchmarking, 03 Load balancing |
| Paper type | system (simulator) plus configuration search |
| Venue and status | peer-reviewed (7th MLSys Conference, 2024) |
| Source read | full text (https://arxiv.org/pdf/2405.05465, v2) |
| Verified on | 2026-10-31, against the MLSys 2024 proceedings page and arXiv 2405.05465 |
| Relevance to project | Medium to high |

## APA 7 reference
Agrawal, A., Kedia, N., Mohan, J., Panwar, A., Kwatra, N., Gulavani, B. S., Ramjee, R., & Tumanov, A. (2024c). Vidur: A large-scale simulation framework for LLM inference. *Proceedings of Machine Learning and Systems, 6*. https://proceedings.mlsys.org/paper_files/paper/2024/hash/b74a8de47d2b3c928360e0a011f48351-Abstract-Conference.html (no DOI issued by MLSys; preprint DOI: https://doi.org/10.48550/arXiv.2405.05465)

## In-text citation forms
(Agrawal et al., 2024c) · Agrawal et al. (2024c). Suffix "c" because three 2024 papers share first author and "et al." (Etalon 2024a, Sarathi-Serve 2024b).

## 1. What it is about
Vidur predicts how an LLM deployment will perform without running it on GPUs. It profiles each operator once, predicts operator run times, and simulates a replica and a cluster scheduler. Its search tool, Vidur-Search, finds the cheapest configuration that meets latency constraints.

## 2. The problem
Choosing parallelism, batching algorithm (Orca, vLLM, Sarathi-Serve), batch size and chunk size multiplies into thousands of combinations. Testing each on real GPUs is slow and costly (the paper estimates 42K GPU hours, about $218K, for LLaMA2-70B). Simulating inference is hard because small errors in a batch's predicted time change which requests are batched next and cascade.

## 3. Proposed solution
- **Operator-level profiling and prediction.** Operators are classified (token-level, sequence-level, communication); token-level ones are profiled by number of tokens, attention by batch composition, and a random-forest-style regressor fills in untested sizes.
- **Hierarchical scheduler.** A global scheduler routes requests to replicas (round-robin, least outstanding requests, and stateful policies) and a replica scheduler models memory planning and batching for vLLM, Orca, Sarathi-Serve and others.
- **Vidur-Bench.** Workloads from LMSys-Chat-1M, Arxiv-Summarization and Bilingual-Web-Book, and metrics at operator, request (scheduling delay, TTFT, TBT), replica and hardware (utilisation) level.
- **Capacity definition (Section 6).** The maximum queries per second a configuration supports "without the queuing delay blowing up", operationalised as P99 scheduling delay under 5 s and found by binary search on QPS.

## 4. Data, models and tools
- Models: LLaMA2-7B/70B, InternLM-20B, Qwen-72B, on A100 and H100 GPUs.
- Open source: https://github.com/microsoft/vidur.

## 5. Key results
- Fidelity: end-to-end latency predicted with under 9% error (abstract); P95 tail latency of static workloads within 3.33%; under 5% error in almost all dynamic scenarios at 85% of capacity (Section 7.2, Figs. 3–4).
- The authors warn that near capacity small prediction deltas blow up, because the system is at "a tipping point" where a slight increase in arrival rate or processing time causes a sharp rise in latency from uncontrolled queue delay.
- Vidur-Search finds the best LLaMA2-70B configuration in about one hour on a 96-core CPU machine (about $9.93 per hour on Azure), versus 42K GPU hours (about $218K) on hardware (abstract and introduction).

## 6. Limitations
- *Stated by authors:* accuracy degrades near and beyond capacity; production systems are provisioned with buffer; energy modelling is planned.
- *My observations:* needs per-model, per-GPU profiling; models only the engine, not network or API latency; fidelity numbers come from the authors' own workloads and vLLM defaults; it models routing only with simple global policies; not designed to predict a live third-party backend.

## 7. Relevance to the AI Request Router
- **Predicting a latency budget per backend:** Vidur's recipe is profile once, predict a request's TTFT and TBT from batch composition, then find the capacity point by searching for the arrival rate at which scheduling delay stops being bounded. A router can reuse the idea in a lighter form: estimate each backend's capacity from load tests, and keep it below about 85% of that point where predictions stay accurate.
- **Reuse:** the P99-scheduling-delay definition of capacity; the request-level metric set (scheduling delay, TTFT, TBT); the simulator itself for offline testing of routing policies (the project's benchmarking chapter) because it supports stateful global scheduling policies.
- **Related:** [Etalon](agrawal-2024-etalon.md), [Sarathi-Serve](agrawal-2024-sarathi-serve.md), [Niyama/QoServe](goel-2025-niyama.md).
- **Not covered:** live telemetry, hosted APIs.

## 8. How to use it in the report
- Evaluation methodology (simulation before live testing) and the definition of capacity.
- Synthesis sentence: "Vidur (Agrawal et al., 2024c) predicts request latency to within 9% and defines capacity as the highest request rate with bounded scheduling delay, but its accuracy falls near saturation."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Agrawal et al. (2024c) | Predict and search LLM deployment performance without GPUs | Operator profiling, regression, hierarchical scheduler, Vidur-Search | LMSys-Chat-1M, Arxiv, BWB; LLaMA2, Qwen, InternLM | Under 9% latency error; best config in about 1 hour on a 96-core CPU machine ($9.93/h) vs 42K GPU-hours | Accuracy falls near capacity; engine-only model |
