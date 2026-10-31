Status: DRAFT
Depends on: D08; D12
Sources: Primary URLs in source table and proposal-audit section
Open items: Scoped numerical/final-version checks recorded below

# SLOs-Serve: admission control and SLO-driven routing for multi-SLO LLMs (Chen et al., 2025)

| Field | Value |
|---|---|
| Topic (home) | 03 LLM load balancing |
| Also relevant to | 05 Serving engines (chunked prefill, speculative decoding), 06 Fallback |
| Paper type | system |
| Venue and status | preprint only (arXiv v1, 5 Apr 2025; no later venue found) |
| Source read | full text (https://arxiv.org/pdf/2504.08784) |
| Verified on | 2026-10-30, against arXiv abs 2504.08784 |
| Relevance to project | High |

## APA 7 reference
Chen, S., Jia, Z., Khan, S., Krishnamurthy, A., & Gibbons, P. B. (2025). *SLOs-Serve: Optimized serving of multi-SLO LLMs*. arXiv. https://doi.org/10.48550/arXiv.2504.08784

## In-text citation forms
(Chen et al., 2025) · Chen et al. (2025)

## 1. What it is about
SLOs-Serve serves LLM requests that carry their own latency targets (service level objectives, SLOs) per stage: prefill, tool-call loops, "thinking", decode. It plans token allocation per batch so admitted requests meet their SLOs, and uses the same check to decide when to route a request to another replica.

## 2. The problem
Applications want different SLO shapes: a summariser needs fast prefill, a code assistant fast decode, a chatbot is relaxed on both. Greedy engine schedulers (vLLM prioritises prefill, Sarathi-Serve uses a fixed chunk size) violate SLOs in bursts, and violations cascade. Disaggregated systems are rigid when the length mix shifts.

## 3. Proposed solution
- **Performance model.** A profiling-based model predicts batch execution time per GPU family.
- **Dynamic-programming scheduler.** Over a few planned batches it chooses tokens per request, exploring chunked-prefill sizes, batch size and optional speculative decoding. Requests with unattainable SLOs are not admitted ("soft admission control") and go to a best-effort tier that uses leftover capacity and is preempted by SLO traffic.
- **Multi-replica routing.** A central controller "virtualises" each replica with the performance model. A one-shot round-robin dispatcher picks a replica; its scheduler checks whether the SLO is attainable; if not, the request moves to the next replica, up to a hop limit, then a backup policy declines it or offloads it to lower-tier resources. The authors contrast this with balancers using indirect metrics such as device load and memory.

## 4. Data, models and tools
- vLLM backend, Ray; about 10K lines of Python plus 1.5K lines of C++.
- 4× A100-40GB; six scenarios (ChatBot, Coder, Summarizer, ToolLLM, Mixed, Reasoning) using ShareGPT, HumanEval, arXiv summaries, ToolBench, OPT models and Azure arrival traces.
- Baselines: vLLM, Sarathi-Serve, DistServe. Capacity = maximum per-GPU request rate at 90% SLO attainment. No code link found.

## 5. Key results
- Abstract and Fig. 1: 2.2× average (geometric mean) per-GPU capacity versus prior systems; the introduction gives 2.2× against the best of Sarathi-Serve and vLLM and 2.4× against DistServe.
- Section 6.1 gives per-baseline gains of 1.76× (vLLM), 1.94× (Sarathi) and 2.6× (DistServe), which differ from the introduction's wording; quote the abstract figure.
- Multi-replica (Section 6.2, Fig. 13, OPT-7B): ChatBot capacity 2.18×, 3.36× and 4.61× with 2, 3 and 4 replicas; up to 6.2× on four replicas under bursty arrivals, which the authors call super-linear.
- Ablation (Section 6.3): request routing alone adds 1.19× on average (1.92× on the bursty Coder scenario); speculative decoding 1.66×; burst-resilient scheduling 1.34×.
- Scheduling overhead stays under 10 ms per call, mostly under 2 ms; performance-model R² between 0.82 and 0.93.

## 6. Limitations
- *Stated by authors:* sequential routing is one of several possible policies; accuracy depends on profiling each GPU family.
- *My observations:* up to four replicas on one machine; SLOs set per scenario, not per user; needs a performance model per GPU, model and engine, which hosted APIs do not allow; round-robin plus retry can add latency when most replicas are full; preprint.

## 7. Relevance to the AI Request Router
- **Live-load signals:** routing on "can this replica still meet this request's deadline?" rather than raw queue length or GPU use maps directly to the project's latency budgets.
- **Reuse:** admission control with a best-effort or fallback tier; trying replicas in order up to a hop limit (like a failover chain); deferring unattainable requests during bursts.
- **Not covered:** the DP token scheduler and speculative decoding are engine-level; no model choice or cost.

## 8. How to use it in the report
- Section on SLO-aware balancing and latency budgets; also in the failover and degradation discussion.
- Synthesis sentence: "Whereas Llumnix balances on memory-based freeness, SLOs-Serve (Chen et al., 2025) routes on whether a request's own latency target can still be met, and demotes unattainable requests to a best-effort tier."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Chen et al. (2025) | Meet per-stage SLOs for mixed LLM applications, including across replicas | DP token-budget scheduler, soft admission control, SLO-attainability routing | vLLM, 4×A100, ShareGPT, HumanEval, ToolBench, Azure traces | 2.2× per-GPU capacity vs SOTA; 4.61× ChatBot capacity on 4 replicas | Needs per-GPU profiling; ≤4 replicas; preprint |


## 2026-10-31 proposal audit

- Source attempted: https://arxiv.org/abs/2504.08784.
- Scope: Abstract/metadata check only in this session; detailed numerical results remain unchecked.
- Historical Source read above records the earlier session, not a claim of a fresh full reading.
- arXiv title matched: SLOs-Serve: Optimized Serving of Multi-SLO LLMs. Latest listed version: v1; arXiv DOI identifies the preprint, not peer review. A missing journal reference does not prove that no published version exists.
