Status: DRAFT
Depends on: D08; D12
Sources: Primary URLs in source table and proposal-audit section
Open items: Scoped numerical/final-version checks recorded below

# Sarathi-Serve: chunked prefills and stall-free scheduling (Agrawal et al., 2024)

| Field | Value |
|---|---|
| Topic (home) | 05 Latency and speed |
| Also relevant to | 03 Load balancing, 08 System design gateway |
| Paper type | system (scheduler) |
| Venue and status | peer-reviewed (18th USENIX OSDI, July 2024) |
| Source read | full text (https://arxiv.org/pdf/2403.02310, v3) |
| Verified on | 2026-10-31, against the USENIX OSDI '24 page and arXiv 2403.02310 |
| Relevance to project | High |

## APA 7 reference
Agrawal, A., Kedia, N., Panwar, A., Mohan, J., Kwatra, N., Gulavani, B. S., Tumanov, A., & Ramjee, R. (2024b). Taming throughput-latency tradeoff in LLM inference with Sarathi-Serve. In *Proceedings of the 18th USENIX Symposium on Operating Systems Design and Implementation (OSDI 24)* (pp. 117–134). USENIX Association. https://www.usenix.org/conference/osdi24/presentation/agrawal (no DOI issued by USENIX; preprint DOI: https://doi.org/10.48550/arXiv.2403.02310)

## In-text citation forms
(Agrawal et al., 2024b) · Agrawal et al. (2024b). The "b" applies because three 2024 papers share the first author and "et al." (Etalon 2024a, Sarathi-Serve 2024b, Vidur 2024c).

## 1. What it is about
Sarathi-Serve is a scheduler for one LLM replica that splits long prompts into chunks and packs them into batches next to ongoing decodes, so that no request's token stream pauses. It also gives the clearest definitions in this topic of time to first token, time between tokens and *capacity*.

## 2. The problem
Prefill (processing the prompt) is compute-heavy and slow per iteration, while decode (one token per request per step) is cheap but memory-bound, which makes batching decodes very effective. Prefill-prioritising schedulers (vLLM, Orca) insert whole prompts into the running batch, causing *generation stalls* for ongoing requests and high tail time-between-tokens. Decode-prioritising schedulers (FasterTransformer) avoid stalls but waste throughput.

## 3. Proposed solution
- **Chunked prefill.** A prompt is split into near-equal chunks processed over several iterations.
- **Stall-free batching.** Each iteration first takes all running decodes, then fills a fixed *token budget* with prefill chunks from waiting requests, so new requests join without pausing decodes.
- **Token budget.** Chosen once by profiling (here using the Vidur simulator, see [Agrawal et al., 2024c](agrawal-2024-vidur.md)) as the largest batch that still meets the time-between-tokens target. Chunk sizes must also avoid GPU tile-quantisation penalties (a chunk of 257 tokens can cost 32% more than 256).
- Uniform batches reduce pipeline bubbles under pipeline parallelism.

## 4. Data, models and tools
- Mistral-7B, Yi-34B, LLaMA2-70B, Falcon-180B on A100 (and A40 for LLaMA2-70B) GPUs; request lengths from openchat_sharegpt4 and arxiv_summarization with Poisson arrivals.
- Baselines: vLLM and Orca-style scheduling. Code: https://github.com/microsoft/sarathi-serve.

## 5. Key results
- **Definitions (Section 2.4):** TTFT is the time from request arrival to the first output token; TBT is the interval between consecutive output tokens; *capacity* is the maximum request rate (queries per second) a system sustains while meeting latency targets.
- **Measurement (Section 5):** the median is reported for TTFT (one value per request) and the 99th percentile (P99) for TBT (one value per token). The SLO on P99 TBT is set to 5× (strict) or 25× (relaxed) the decode-iteration time of an interference-free run; for Mistral-7B this is 0.1 s and 0.5 s (Table 3). A load counts as sustainable only if median scheduling delay stays under 2 s, i.e. the queue does not blow up.
- Capacity gains over vLLM: 2.6× for Mistral-7B on one A100 and up to 3.7× for Yi-34B on two A100s (abstract); up to 5.6× for Falcon-180B with pipeline parallelism.
- Figure 10 annotates gains between 1.69× and 4.00× depending on model, dataset and SLO strictness (comparison baseline per label not checked).

## 6. Limitations
- *Stated by authors:* the token budget trades chunking overhead against latency and depends on SLO, parallelism and hardware, so it needs profiling per deployment.
- *My observations:* single-replica scheduling, not routing; SLOs set per model, not per user; Poisson arrivals; TTFT tails are not emphasised.

## 7. Relevance to the AI Request Router
- **Metrics definitions to adopt:** TTFT, TBT/TPOT, P99, and *capacity under an SLO* with a stability check (queue does not grow), see the overview for the full list.
- **Why queueing dominates tail latency:** under load, "low throughput leads to large scheduling delays and higher TTFT" (Section 2.4 paraphrased); the stability condition on scheduling delay marks where the tail explodes. A backend near capacity should be treated as unusable for latency-bound requests.
- **Reuse:** a per-backend token budget profiled once, and a strict/relaxed SLO pair, could define the router's latency tiers. Related load-balancing work: [Chen et al. (SLOs-Serve)](../03-load-balancing/chen-2025-slos-serve.md).
- **Not covered:** routing across replicas, hosted APIs.

## 8. How to use it in the report
- Section on latency metrics and the throughput–latency tradeoff in Chapter 2; evaluation design (which percentiles to report) in Chapter 3.
- Synthesis sentence: "Sarathi-Serve (Agrawal et al., 2024b) defines capacity as the highest request rate meeting P99 time-between-tokens targets with a bounded queue, the notion of backend headroom the router needs."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Agrawal et al. (2024b) | Meet tail-latency SLOs without losing throughput | Chunked prefill, stall-free batching, token budget | Mistral-7B to Falcon-180B, A100/A40, ShareGPT/arXiv traces | 2.6× to 5.6× higher capacity than vLLM | Single replica; per-deployment profiling |


## 2026-10-31 proposal audit

- Source attempted: https://arxiv.org/abs/2403.02310.
- Scope: Full-text sample: method and selected numerical/limitation statements checked; see L07.
- Historical Source read above records the earlier session, not a claim of a fresh full reading.
- arXiv title matched: Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve. Latest listed version: v3; arXiv DOI identifies the preprint, not peer review. A missing journal reference does not prove that no published version exists.
