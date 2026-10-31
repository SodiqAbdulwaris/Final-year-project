# DistServe: disaggregating prefill and decoding for goodput (Zhong et al., 2024)

| Field | Value |
|---|---|
| Topic (home) | 05 Latency and speed |
| Also relevant to | 03 Load balancing, 08 System design gateway |
| Paper type | system |
| Venue and status | peer-reviewed (18th USENIX OSDI, July 2024) |
| Source read | full text (https://arxiv.org/pdf/2401.09670, v3) |
| Verified on | 2026-10-31, against the USENIX OSDI '24 page and arXiv 2401.09670 |
| Relevance to project | High |

## APA 7 reference
Zhong, Y., Liu, S., Chen, J., Hu, J., Zhu, Y., Liu, X., Jin, X., & Zhang, H. (2024). DistServe: Disaggregating prefill and decoding for goodput-optimized large language model serving. In *Proceedings of the 18th USENIX Symposium on Operating Systems Design and Implementation (OSDI 24)* (pp. 193–210). USENIX Association. https://www.usenix.org/conference/osdi24/presentation/zhong-yinmin (no DOI issued by USENIX; preprint DOI: https://doi.org/10.48550/arXiv.2401.09670)

## In-text citation forms
(Zhong et al., 2024) · Zhong et al. (2024)

## 1. What it is about
DistServe runs the prefill phase (processing the prompt, which sets time to first token, TTFT) and the decoding phase (generating tokens, which sets time per output token, TPOT) on different GPUs. It chooses how many GPUs and which parallelism each phase gets from the application's TTFT and TPOT targets, and measures success as *goodput*.

## 2. The problem
Colocating both phases makes them interfere: one prefill added to a batch of decodes slows every decode (higher TPOT), and decodes added to a prefill-bound GPU slow the prefill (higher TTFT). Under strict targets, colocated systems must over-provision. Their resource and parallelism plans are also coupled.

## 3. Proposed solution
- **Goodput.** The maximum request rate per GPU that keeps SLO attainment (fraction of requests meeting both TTFT and TPOT targets) at a goal such as 90%. It is the paper's central metric and is dominated by whichever of the two targets is stricter.
- **Placement search.** Given workload, targets and cluster bandwidth, an algorithm picks the number of prefill and decoding instances and their parallelism, keeping KV transfers on fast links.
- **Queueing model.** With disaggregation, a prefill instance behaves like an M/D/1 queue (Poisson arrivals, constant service time D). For arrival rate R with RD < 1 the average TTFT is D + R·D² / (2(1 − R·D)): execution time plus queueing delay (Eq. 1). Near RD → 1 the queueing term explodes.
- **Runtime.** A central controller sends each request to the prefill instance with the shortest queue and then to the least-loaded decoding instance, FCFS. Decoding instances pull KV caches, using prefill GPU memory as a buffer. A profiler watches mean lengths and arrival rate and triggers replanning when the pattern shifts.

## 4. Data, models and tools
- OPT-13B/66B/175B on 4 nodes × 8 A100-80GB. Workloads: chatbot (ShareGPT; OPT-13B targets TTFT 0.25 s and TPOT 0.1 s), code completion (HumanEval, strict targets) and summarisation (LongBench, loose TTFT, strict TPOT). Poisson arrivals.
- Baselines: vLLM and DeepSpeed-MII (with chunked prefill).

## 5. Key results
- Abstract: serves up to 7.4× more requests or meets 12.6× tighter SLOs than state-of-the-art, with more than 90% of requests within both latency limits.
- Motivating example (Fig. 1): on one A100, colocated goodput is about 1.6 req/s; a prefill-only GPU reaches 5.6 and a decode-only GPU 10 req/s, so 2 prefill + 1 decode GPU gives 3.3 req/s per GPU, 2.1× higher.
- Chatbot on ShareGPT: 2.0×–4.6× higher sustainable rate than vLLM and 1.6×–7.4× than DeepSpeed-MII (Section 6.2).

## 6. Limitations
- *Stated by authors:* no preemption (FCFS allows a convoy effect: long prompts block short ones) and no fault tolerance; poorly suited to offline throughput work and to one or few GPUs.
- *My observations:* SLO values are the authors' own choices; OPT models only; needs fast interconnects; one cluster, Poisson arrivals; a router would not control placement.

## 7. Relevance to the AI Request Router
- **Metric definitions:** TTFT, TPOT, SLO attainment at a percentile goal, and per-GPU goodput. These can define the router's "can this backend meet this latency budget" test and its benchmark reporting.
- **Predicting a latency budget:** Eq. 1 gives a closed-form, per-backend TTFT estimate from only an arrival rate and a service time, and shows why TTFT is nonlinear in load: queueing dominates as utilisation approaches 1. This suits a gateway that knows each backend's recent request rate and prefill time.
- **Related:** [Sarathi-Serve](agrawal-2024-sarathi-serve.md), [Splitwise](patel-2024-splitwise.md), [SLOs-Serve](../03-load-balancing/chen-2025-slos-serve.md).
- **Not covered:** hosted APIs or routing between models.

## 8. How to use it in the report
- Section on latency metrics (goodput, SLO attainment) and on why tail latency rises sharply at high utilisation.
- Synthesis sentence: "DistServe (Zhong et al., 2024) shows that goodput under joint TTFT and TPOT targets, not raw throughput, determines cost, and models prefill queueing as M/D/1, so TTFT grows sharply as utilisation approaches one."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Zhong et al. (2024) | Maximise per-GPU goodput under TTFT and TPOT targets | Prefill/decode disaggregation; placement search; M/D/1 analysis | OPT 13B–175B, A100 cluster, ShareGPT/HumanEval/LongBench | Up to 7.4× more requests or 12.6× tighter SLO than vLLM-class systems | No preemption or fault tolerance; own SLOs |
