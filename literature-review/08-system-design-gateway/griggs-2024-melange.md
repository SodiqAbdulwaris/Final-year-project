# Mélange: cost-efficient LLM serving by mixing GPU types (Griggs et al., 2024)

| Field | Value |
|---|---|
| Topic (home) | 08 System design and gateway |
| Also relevant to | 04 Cost reduction |
| Paper type | method / system |
| Venue and status | preprint only. The arXiv page lists no journal reference or comments, and a web search for a published venue (a COLM 2025 listing was tried) found none. Check again before submission. |
| Source read | full text (https://arxiv.org/pdf/2404.14527, v4 of 22 July 2024); appendices A.2 (load balancer) and C not read in full |
| Verified on | 2026-10-31, against the arXiv abstract page (v1 22 April 2024 to v4 22 July 2024) |
| Relevance to project | Medium to high for the cost term of the scoring function when backends are self-hosted |

## APA 7 reference
Griggs, T., Liu, X., Yu, J., Kim, D., Chiang, W.-L., Cheung, A., & Stoica, I. (2024). *Mélange: Cost efficient large language model serving by exploiting GPU heterogeneity* [Preprint]. arXiv. https://doi.org/10.48550/arXiv.2404.14527

## In-text citation forms
(Griggs et al., 2024) · Griggs et al. (2024)

## 1. What it is about
Mélange chooses the cheapest mix of GPU types to serve one LLM at a latency target. The authors show that which GPU is cheapest per token depends on request size, request rate and the latency target, so a mix of GPU types is usually best.

## 2. The problem
LLM serving is expensive, and work on faster engines says little about which GPU type to rent. Higher-priced GPUs are not always better value, but the right choice changes with the workload.

## 3. Proposed solution
- **Cost-efficiency measure:** tokens processed per dollar (T/$), using on-demand cloud prices.
- **Three findings (section 4):** small requests favour cheaper GPUs (A10G up to 2.6 times better T/$ than A100 for small sizes; A100 up to 1.5 times better for large ones); tight latency targets favour high-end GPUs; at low request rates a cheaper GPU saves money, and mixing types scales more finely.
- **Allocation as bin packing:** GPUs are bins and slices of the workload are items; an integer linear program with an off-the-shelf solver finds the minimum-cost allocation that meets the latency target. Workload is bucketed (10 input-length ranges by 6 output-length ranges, 60 buckets, 8 slices each, 480 slices).
- **Load balancer (Appendix A.2):** estimates a new request's output length from past requests and routes by weighted random choice, with weights from each GPU's performance for that size.

## 4. Data, models and tools
Llama-2-7b (and 70b for an H100 versus A100 comparison) with vLLM 0.2.7. GPUs and on-demand prices per hour (Table 1): L4 $0.70, A10G $1.01, A100-80G $3.67, H100 $7.5164. Datasets: Chatbot Arena (short conversations), PubMed (long documents) and an 80/20 mix. Time-per-output-token targets of 40 ms and 120 ms. Baselines are single-GPU-type allocations from the same solver. Code: https://github.com/tyler-griggs/melange-release.

## 5. Key results
- Cost reduction against single-GPU-type allocations: 9 to 77% on short-context, 2 to 33% on long-context and 4 to 51% on mixed workloads (section 1; abstract gives the maxima 77%, 33%, 51%).
- Latency targets met: over 99.95% of requests at the 120 ms target and 99.5% at 40 ms in a 4 requests per second test; 84% of the violations came from bursts or co-location with large requests (section 6.3).
- The solver ran in under 1.2 seconds in all tests (section 6.4).

## 6. Limitations
- **Authors:** it assumes a fixed workload distribution and rate; it does not handle GPU unavailability or autoscaling; it is a component that has to be plugged into a wider serving system.
- **Mine:** cloud on-demand prices only; a single model (Llama-2) evaluated; preprint; it plans GPU rental, not request routing between models.

## 7. Relevance to the AI Request Router
- **Supports:** the cost term in the scoring function (D-04). The proposal does not say how a self-hosted token is priced; tokens per dollar from the GPU's hourly price is one published, simple definition the team could adopt for self-hosted backends (still to be decided by the team).
- **Reuse:** the finding that cost efficiency depends on request size and latency target supports giving the router per-request cost estimates from input and output length. Its output-length estimate from past requests is a model for the router's expected-output-length term.
- **Not covered:** per-prompt model choice, live routing, hosted APIs.

## 8. How to use it in the report
- Chapter 2, section 2.4.4 (cost) and 2.4.8; Chapter 3, section 3.6.5 (expected cost).
- Suggested synthesis sentence: "Mélange (Griggs et al., 2024) minimises cost by choosing GPU types for a fixed workload; the proposed router instead minimises cost per request by choosing a model, given the prices of whatever backends exist."
- Link: AIBrix uses a Mélange-inspired optimiser: [AIBrix](aibrix-2025-llm-inference-infrastructure.md).

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Griggs et al. (2024) | Minimise cost of serving an LLM across GPU types | Tokens-per-dollar analysis; ILP cost-aware bin packing over workload slices | Llama-2-7b/70b, vLLM; L4, A10G, A100, H100; Chatbot Arena, PubMed | Up to 77%, 33%, 51% lower cost by workload type; 99.5% to 99.95% of requests meet latency targets | Fixed workload; no autoscaling; one model; preprint |
