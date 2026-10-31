Status: DRAFT
Depends on: D08; D12
Sources: Primary URLs in source table and proposal-audit section
Open items: Scoped numerical/final-version checks recorded below

# Splitwise: phase splitting for LLM inference (Patel et al., 2024)

| Field | Value |
|---|---|
| Topic (home) | 05 Latency and speed |
| Also relevant to | 04 Cost reduction (cost and power), 03 Load balancing |
| Paper type | system plus characterisation study |
| Venue and status | peer-reviewed (51st ACM/IEEE ISCA, June 2024) |
| Source read | full text (https://arxiv.org/pdf/2311.18677, v2) |
| Verified on | 2026-10-31, against Crossref record for DOI 10.1109/ISCA59077.2024.00019 and arXiv 2311.18677 |
| Relevance to project | Medium |

## APA 7 reference
Patel, P., Choukse, E., Zhang, C., Shah, A., Goiri, Í., Maleki, S., & Bianchini, R. (2024). Splitwise: Efficient generative LLM inference using phase splitting. In *Proceedings of the 51st Annual International Symposium on Computer Architecture (ISCA 2024)* (pp. 118–132). IEEE. https://doi.org/10.1109/ISCA59077.2024.00019

## In-text citation forms
(Patel et al., 2024) · Patel et al. (2024)

## 1. What it is about
Splitwise, from Microsoft, characterises production-style LLM traces and shows that the prompt phase and the token-generation phase behave very differently. It then runs them on separate machine pools, possibly with different GPU types, to raise throughput per cost and per watt.

## 2. The problem
Even with continuous batching, token generation under-uses GPU compute and does not need the newest, most power-hungry GPUs, while prompt computation does. Colocating the phases on identical machines wastes money and power, and mixed batching raises the tail of time between tokens (TBT).

## 3. Proposed solution
- **Characterisation.** Production traces for a coding and a conversation service (Azure) with BLOOM-176B and Llama2-70B on vLLM. Findings include: TTFT grows almost linearly with prompt length (Fig. 5a); 60–70% of conversation time runs 20 or fewer batched tokens; token-phase batching raises TBT only about 2× at batch 64 (Fig. 5b); most end-to-end (E2E) time is spent in the token phase (Insight III).
- **Cluster design.** A cluster-level scheduler (CLS) assigns a prompt machine and a token machine to each request together, so KV-cache transfer overlaps prompt computation; transfer uses optimised network libraries over InfiniBand. A third *mixed* pool absorbs load imbalance.
- **Routing.** The CLS uses Join-the-Shortest-Queue, where queue length is the number of *pending tokens*, not requests. Machines report capacity and queue changes periodically, not at every iteration. If a pool's queue exceeds a threshold, the request goes to the mixed pool, then to a machine borrowed from the other pool.

## 4. Data, models and tools
- Real hardware: a vLLM-based KV-transfer implementation on two DGX-A100 and two DGX-H100 VMs (open source per the paper). Cluster designs evaluated in a simulator driven by a piece-wise linear performance model.
- Baselines: all-A100 and all-H100 clusters with mixed continuous batching.

## 5. Key results
- Abstract: up to 1.4× higher throughput at 20% lower cost than current designs, or 2.35× more throughput at the same power and cost.
- **Metrics (Table II, Section V):** E2E latency, TTFT, TBT and throughput (requests/s). SLOs are written as slowdowns versus a request running alone on a DGX-A100: P50/P90/P99 of 2×/3×/6× for TTFT and 1.25×/1.5×/5× for TBT and E2E (Table VI). All nine must hold for a throughput figure to count.
- The performance model has a mean absolute percentage error under 3% on an 80:20 train/test split, and the simulator was checked against hardware and a production load of over 50,000 iterations.
- For BLOOM-176B, prompt computation of 1,500 input tokens takes as long as generating about 6 output tokens.

## 6. Limitations
- *Stated by authors:* the approach relies on the two-phase autoregressive structure; at high load Splitwise "devolves" toward an all-mixed cluster (Section VI).
- *My observations:* cluster-level results come from simulation with synthetic Poisson arrivals; two models; requires fast interconnects; the design is for a provider operating its own fleet, not a gateway calling third-party backends.

## 7. Relevance to the AI Request Router
- **Defining and predicting latency:** the slowdown-versus-uncontended SLO form is a practical way for the router to express per-backend latency budgets, with P50/P90/P99 targets. A piece-wise linear model from profiled batches gave under 3% error, so a per-backend latency model fitted from a short calibration run is plausible. TTFT being near-linear in prompt length lets the router estimate prefill time from the prompt token count it already computes.
- **Load signal:** pending *tokens*, not request count, as queue length (compare [Kossmann et al.](../03-load-balancing/kossmann-2024-gpu-half-empty.md) and [Llumnix](../03-load-balancing/sun-2024-llumnix.md)).
- **Not covered:** hosted APIs, routing across different models.

## 8. How to use it in the report
- Metrics and "why decode dominates end-to-end time" in the latency background; also links to [DistServe](zhong-2024-distserve.md) as the parallel disaggregation proposal.
- Synthesis sentence: "Splitwise (Patel et al., 2024) shows TTFT scales near-linearly with prompt length while most end-to-end time is spent generating tokens, so a latency budget must account for expected output length as well as prompt length."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Patel et al. (2024) | Cut cost and power of LLM serving | Phase splitting across machine pools; JSQ on pending tokens; mixed pool | Azure traces, BLOOM-176B, Llama2-70B, A100/H100, vLLM | 1.4× throughput at 20% lower cost, or 2.35× at same power and cost | Simulated clusters; fleet-operator view |


## 2026-10-31 proposal audit

- Source attempted: https://arxiv.org/abs/2311.18677.
- Scope: Abstract/metadata check only in this session; detailed numerical results remain unchecked.
- Historical Source read above records the earlier session, not a claim of a fresh full reading.
- arXiv title matched: Splitwise: Efficient generative LLM inference using phase splitting. Latest listed version: v2; arXiv DOI identifies the preprint, not peer review. A missing journal reference does not prove that no published version exists.
