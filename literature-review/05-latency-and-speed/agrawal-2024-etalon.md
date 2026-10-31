Status: DRAFT
Depends on: D08; D12
Sources: Primary URLs in source table and proposal-audit section
Open items: Scoped numerical/final-version checks recorded below

# Etalon: a fluidity-based evaluation framework for LLM serving (Agrawal et al., 2024a)

| Field | Value |
|---|---|
| Topic (home) | 05 Latency and speed |
| Also relevant to | 07 Testing and benchmarking, 08 System design gateway |
| Paper type | benchmark / evaluation framework |
| Venue and status | preprint only (arXiv v2, 30 Aug 2024; no venue listed on the arXiv page) |
| Source read | full text (https://arxiv.org/pdf/2407.07000) |
| Verified on | 2026-10-31, against arXiv abs 2407.07000 |
| Relevance to project | High |

## APA 7 reference
Agrawal, A., Agarwal, A., Kedia, N., Mohan, J., Kundu, S., Kwatra, N., Ramjee, R., & Tumanov, A. (2024a). *Etalon: Holistic performance evaluation framework for LLM inference systems*. arXiv. https://doi.org/10.48550/arXiv.2407.07000

## In-text citation forms
(Agrawal et al., 2024a) · Agrawal et al. (2024a). Suffix "a" because three 2024 papers share first author and "et al." (Sarathi-Serve 2024b, Vidur 2024c).

## 1. What it is about
Etalon argues that the usual latency metrics for LLM serving give a misleading picture of what a streaming user experiences, and proposes a *fluidity-index*: the share of output tokens that arrive before a per-token deadline, with slack carried forward. It then benchmarks open-source engines and three commercial API providers using black-box measurements.

## 2. The problem
- **TTFT** (time to first token, including scheduling delay and prompt processing) grows with prompt length (the paper says quadratically), so one static TTFT target is unfair; dividing by prompt length hides scheduling delay.
- **TPOT** (average time per output token) and **normalised latency** (end-to-end time divided by decode tokens) hide stalls: a 10 s generation stall barely moves the average.
- **TBT** (time between tokens) tails capture stalls but cannot describe overall token throughput, and treat each token independently.

## 3. Proposed solution
- **Metric definitions (Section 2.2):** TTFT, TBT, TPOT, normalised latency, and *capacity* (the maximum queries per second sustained while meeting latency targets).
- **Fluidity-index.** Token i has deadline D_i = D_p + i · D_d, where D_p is the first-token target (a function of prompt length) and D_d the per-token target. Early tokens bank slack; on a miss, deadlines reset from the late token so that one stall counts once. The index is the fraction of deadlines met.
- **Choosing targets.** D_p comes from profiling a reference engine at several prompt lengths and fitting a curve; D_d has three levels: 25 ms (interactive chat), 50 ms (medium) and 100 ms (low priority).
- **Fluid token generation rate.** The inverse of the smallest D_d for which 99% of requests have a fluidity-index of at least 0.9.

## 4. Data, models and tools
- Black-box tests of Anyscale, Groq and Fireworks APIs with Llama3-70B and Mixtral-8x7B, prompts of 256–8k tokens, up to 256 output tokens, repeated hourly over 24 hours to cover traffic variation.
- Open source: vLLM and Sarathi-Serve (via vLLM chunked prefill) on Llama3-8B with one H100, using ShareGPT and Arxiv-Summarization requests.
- Code: https://github.com/project-etalon/etalon.

## 5. Key results
- At high load, vLLM's tail-TBT-based throughput is 3× worse than Sarathi-Serve's while TPOT-based throughput shows them on par (Section 3.1), so the choice of metric changes the ranking.
- Under a strict 25 ms TBT target, a P99-TBT SLO makes Sarathi-Serve's capacity 2× lower than vLLM's, while the fluidity-index capacity of the two is equal at 0.6 queries/s in the Arxiv-Summarization setting (Section 5.2).
- The API comparison (Fig. 5) contrasts TPOT-, tail-TBT- and fluidity-based throughput per provider; values appear only in figures, so none are quoted.

## 6. Limitations
- *Stated by authors:* the first-token target is hard to set for proprietary systems (observed prefill includes unknown scheduling delay); scheduling slack is empirical; engine knobs are not tuned.
- *My observations:* preprint; one model size in the open-source tests; API results are a 24-hour snapshot that will drift; fluidity-index is not a standard, so report standard metrics alongside.

## 7. Relevance to the AI Request Router
- **Defining and measuring latency:** this is the best single source in the topic for metric definitions, for the pitfalls of averaged metrics, and for black-box measurement of hosted APIs, which is exactly how the router can observe latency of remote backends it does not control. Report TTFT with prompt length, TBT percentiles, and a deadline-based score.
- **Latency budget per backend:** fitting a prefill-time curve against prompt length from a few isolated requests (Section 4.1) is a cheap way to predict a backend's TTFT floor; scheduling delay is then the difference between observed and predicted TTFT, which separates queueing from compute.
- **Not covered:** routing decisions, cost, or quality.
- **Related:** [Sarathi-Serve](agrawal-2024-sarathi-serve.md), [Vidur](agrawal-2024-vidur.md), [DistServe](zhong-2024-distserve.md).

## 8. How to use it in the report
- Latency-metrics subsection (definitions) and the benchmark design in Chapter 3.
- Synthesis sentence: "Etalon (Agrawal et al., 2024a) shows that average TPOT can rank two engines as equal while one stalls for seconds, so the router's evaluation should include tail TBT and deadline-based measures."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Agrawal et al. (2024a) | Better user-facing latency evaluation for LLM serving | Fluidity-index with per-token deadlines; black-box API probing | vLLM, Sarathi-Serve, Anyscale, Groq, Fireworks; ShareGPT, Arxiv-Summarization | Tail-TBT throughput of vLLM 3× worse than Sarathi while TPOT shows parity | Preprint; targets chosen empirically |


## 2026-10-31 proposal audit

- Source attempted: https://arxiv.org/abs/2407.07000.
- Scope: Abstract/metadata check only in this session; detailed numerical results remain unchecked.
- Historical Source read above records the earlier session, not a claim of a fresh full reading.
- arXiv title matched: Etalon: Holistic Performance Evaluation Framework for LLM Inference Systems. Latest listed version: v2; arXiv DOI identifies the preprint, not peer review. A missing journal reference does not prove that no published version exists.
