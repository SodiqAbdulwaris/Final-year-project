Status: DRAFT
Depends on: D08; D12
Sources: Primary URLs in source table and proposal-audit section
Open items: Scoped numerical/final-version checks recorded below

# Workload-aware RL router across LLM instances (Jain et al., 2024)

| Field | Value |
|---|---|
| Topic (home) | 03 LLM load balancing |
| Also relevant to | 02 Difficulty estimation (output-length prediction), 01 Routing algorithms |
| Paper type | method (simulation plus vLLM experiments) |
| Venue and status | preprint only (arXiv v2, 7 Jan 2025; no peer-reviewed venue found on the arXiv page) |
| Source read | full text (https://arxiv.org/pdf/2408.13510) |
| Verified on | 2026-10-30, against arXiv abs 2408.13510 |
| Relevance to project | High |

## APA 7 reference
Jain, K., Parayil, A., Mallick, A., Choukse, E., Qin, X., Zhang, J., Goiri, Í., Wang, R., Bansal, C., Rühle, V., Kulkarni, A., Kofsky, S., & Rajmohan, S. (2024). *Intelligent router for LLM workloads: Improving performance through workload-aware load balancing*. arXiv. https://doi.org/10.48550/arXiv.2408.13510

## In-text citation forms
(Jain et al., 2024) · Jain et al. (2024)

## 1. What it is about
A Microsoft team studies how to route each request to one of several identical LLM replicas, arguing routing matters more than tweaks to the batching scheduler inside each replica. The router uses a predicted output length and a hand-built "mixing penalty" to guide a reinforcement-learning (RL) agent.

## 2. The problem
Earlier work optimises scheduling inside one replica or routes between different models. Routing between replicas of the same model was left to round-robin or classic queue heuristics that treat requests as equal jobs. Prefill is compute-bound and decode memory-bound, so mixing long prompts and long generations on one replica causes preemptions and latency spikes.

## 3. Proposed solution
- **Observation study.** Mixing request types lengthens everyone's execution time (Fig. 1a); in an exhaustive 8-request, 2-instance test, random assignment was about 10% slower than the best (29.81 s vs 27.03 s).
- **Output-length predictor.** A fine-tuned DistilBERT predicts an output-length bucket; adding the task type to the prompt raised accuracy from 5.5% to 79.15% on unequal buckets.
- **Workload impact estimator.** Two formulas estimate how much a new request slows its own prefill and the decode of running requests, combined into a "mixing" penalty.
- **RL router.** State: queue length, next request's prompt length and predicted decode bucket, per-instance length histograms, capacity and earliest completion time. Action: send to instance i, or wait. The penalty serves as decaying guidance ("workload-guided RL").

## 4. Data, models and tools
- Five task types (sentiment, entity recognition, in-context and general QnA, translation); a one-hour trace from an unnamed "Cloud provider X" (appendix).
- Four Llama-2-7B instances on V100s with vLLM; repeated on A100 with Llama-3.1-8B.
- Baselines: round-robin, Join Shortest Queue, Maximum Capacity Usage, Min-Min, plain RL. No code link found.

## 5. Key results
- 2,000 requests, 4 instances: workload-guided RL cut mean end-to-end latency by 19.18 s (11.43%) versus round-robin; plain RL 4.35%, workload-aware RL 7.79% (Section 6.1).
- Join Shortest Queue, Maximum Capacity Usage and Min-Min beat round-robin by only 0.46%, 2.60% and 1.50%.
- A100 with Llama-3.1-8B: about 10.81%; eight instances: 11.62% (Section 6.2, Appendix A.11).
- Production trace (mean prompt 5,526.64 tokens, mean decode 112.69): guided RL 7.84% better, plain RL 2.28% (Appendix A.12); gains shrink when prompts dominate decodes.

## 6. Limitations
- *Stated by authors:* the RL router adds overhead versus heuristics; its value is finding good policies per model, hardware and scheduler, usable as a benchmark.
- *My observations:* identical replicas only (no model choice, cost, quality); 8–11% gains are modest; needs per-hardware calibration and retraining; the predictor needs prompt text or task labels; no staleness analysis (router appears to see exact state); preprint.

## 7. Relevance to the AI Request Router
- **Live-load signals:** queue length alone (Join Shortest Queue) barely beats round-robin, because the length mix of queued and running requests matters. Predicted output length is a useful extra signal.
- **Reuse:** delaying dispatch ("wait" action); routing separate from engine scheduling; the task-type hint links to the difficulty classifier; a simplified mixing penalty could be a load-score term.
- **Not covered:** RL training is out of scope; no model choice, hosted APIs or failover.

## 8. How to use it in the report
- Section on load-balancing policies (where queue-length and round-robin baselines are compared) and in motivating a length-aware load term.
- Synthesis sentence: "Jain et al. (2024) found that classic heuristics such as join-shortest-queue improved on round-robin by under 3%, whereas a length-aware learned router reached 11%, which suggests that raw queue counts are an incomplete load signal."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Jain et al. (2024) | Route requests across identical LLM instances to cut latency | Output-length predictor (DistilBERT), mixing-penalty estimator, heuristic-guided RL router | Five-task mix, Cloud provider X trace; Llama-2-7B/Llama-3.1-8B, vLLM, V100/A100 | 11.43% lower mean end-to-end latency than round-robin; JSQ only 0.46% | Same-model replicas only; RL training and calibration; preprint |


## 2026-10-31 proposal audit

- Source attempted: https://arxiv.org/abs/2408.13510.
- Scope: Abstract/metadata check only in this session; detailed numerical results remain unchecked.
- Historical Source read above records the earlier session, not a claim of a fresh full reading.
- arXiv title matched: Intelligent Router for LLM Workloads: Improving Performance Through Workload-Aware Load Balancing. Latest listed version: v2; arXiv DOI identifies the preprint, not peer review. A missing journal reference does not prove that no published version exists.
