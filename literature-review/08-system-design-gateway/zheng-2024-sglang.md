Status: DRAFT
Depends on: D08; D12
Sources: Primary URLs in source table and proposal-audit section
Open items: Scoped numerical/final-version checks recorded below

# SGLang: a language and runtime for efficient LLM programs (Zheng et al., 2024)

| Field | Value |
|---|---|
| Topic (home) | 08 System design and gateway |
| Also relevant to | 05 Latency and speed, 04 Cost reduction |
| Paper type | system |
| Venue and status | peer-reviewed (NeurIPS 2024, *Advances in Neural Information Processing Systems 37*) |
| Source read | full text of the main body (https://arxiv.org/pdf/2312.07104, v2 of 6 June 2024, which still says "Preprint. Under review" on its first page; the NeurIPS version was checked for metadata only, not compared line by line); appendices (A to D) not read |
| Verified on | 2026-10-31, against the NeurIPS 2024 proceedings page and arXiv |
| Relevance to project | Medium (a candidate backend, not a gateway) |

## APA 7 reference
Zheng, L., Yin, L., Xie, Z., Sun, C., Huang, J., Yu, C. H., Cao, S., Kozyrakis, C., Stoica, I., Gonzalez, J. E., Barrett, C., & Sheng, Y. (2024). SGLang: Efficient execution of structured language model programs. In *Advances in Neural Information Processing Systems* (Vol. 37, pp. 62557–62583). Curran Associates. https://doi.org/10.52202/079017-2000

(The DOI is the one the NeurIPS proceedings page shows. The page range comes from an author-site record found by search, not from the NeurIPS page. Preprint DOI: https://doi.org/10.48550/arXiv.2312.07104.)

## In-text citation forms
(Zheng et al., 2024) · Zheng et al. (2024)

## 1. What it is about
SGLang is a Python-embedded language for programs that make many dependent LLM calls, plus a runtime that runs them efficiently. Its main runtime ideas are RadixAttention (reusing the KV cache of shared prompt prefixes), faster constrained decoding for structured outputs, and speculative execution for API-only models.

## 2. The problem
Modern LLM use is often a program (agents, few-shot prompting, tree-of-thought, JSON output) with several calls. Programming this is tedious. Existing engines (vLLM, TGI, TensorRT-LLM) throw away the KV cache after each request and decode constrained output one token at a time, so they redo work.

## 3. Proposed solution
- **Frontend primitives:** `gen`, `select`, `fork`, `join`, `extend`, with an interpreter that runs calls asynchronously and a compiler mode.
- **RadixAttention:** keeps the KV cache of prompts and outputs in a radix tree with LRU eviction and reference counts; the runtime matches new prompts against the tree and reuses cached prefixes.
- **Cache-aware scheduling:** waiting requests are ordered by longest shared prefix first, not first-come-first-served; for the offline case the authors prove this gives an optimal hit rate (Theorem 3.1). They note it can starve some requests.
- **Compressed finite-state machine:** several forced tokens of a regular-expression constraint are decoded in one step.
- **API speculative execution:** for black-box endpoints such as OpenAI, the first call is allowed to generate extra tokens that later calls reuse, saving input-token cost and latency.

## 4. Data, models and tools
Llama-2 7B to 70B, Mixtral-8x7B, LLaVA image and video models, and GPT-3.5 through the API. AWS G5 instances with A10G 24 GB GPUs (some A100 runs). Baselines: Guidance v0.1.8, vLLM v0.2.5, LMQL v0.7.3. Workloads include MMLU, HellaSwag, ReAct and generative-agent traces, tree-of-thought, JSON decoding and multi-turn chat. Code: https://github.com/sgl-project/sglang.

## 5. Key results
- Up to 6.4 times higher throughput and up to 3.7 times lower latency than the baselines on open-weight model workloads (section 6.2; Figures 5 and 6 show Llama-7B).
- Multi-modal: up to 6 times higher throughput (Table 2: LLaVA-v1.5-7B 0.18 to 1.15 image/s).
- Cache hit rates 50% to 99% across benchmarks; cache-aware scheduling reaches about 96% of the optimal hit rate on average.
- Production use in Chatbot Arena for one month: 52.4% hit rate for LLaVA-Next-34B and 74.1% for Vicuna-33B, with 1.7 times lower first-token latency on average for Vicuna-33B.

## 6. Limitations
- **Authors:** extend to other output modalities; use the DRAM and disk hierarchy; fuzzy semantic matching in RadixAttention; fix starvation in cache-aware scheduling; stronger compiler optimisations.
- **Mine:** the baseline vLLM version (0.2.5) is old, and the authors note RadixAttention was later partly added to vLLM, so the gap today may be smaller; the main workloads run on a single worker; no routing between different models; evaluated for throughput and single-program latency, not tail latency under a mixed load; appendix A.4 on multi-worker data parallelism was not read.

## 7. Relevance to the AI Request Router
- **Supports:** the self-hosted backend choice (D-03). SGLang is an alternative to vLLM, and AIBrix lists it as a supported engine. It also shows an API-model backend (OpenAI, Anthropic) behind the same programming interface.
- **Reuse:** the idea that prefix locality matters. If the router sends turns of one conversation to the same backend, that backend's cache is reused. This is a possible extra term for the scoring function, not in the proposal.
- **Not covered:** gateway design, model choice, failover, live metrics. It does not mention Prometheus, Redis or a circuit breaker.

## 8. How to use it in the report
- Chapter 2, section 2.3 (enabling technologies: serving engines) and 2.4.8.
- Suggested synthesis sentence: "SGLang (Zheng et al., 2024) speeds up multi-call programs inside one engine through prefix reuse; it assumes the model is already chosen, which is the decision the proposed router makes."
- Chapter 3, section 3.8: optional alternative to vLLM; if not used, state why.

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Zheng et al. (2024) | Efficient execution of multi-call LLM programs | RadixAttention prefix cache reuse; cache-aware scheduling; compressed FSM decoding; API speculative execution | Llama-2, Mixtral, LLaVA, GPT-3.5; A10G and A100; MMLU, agents, JSON, chat | Up to 6.4x throughput, 3.7x lower latency vs Guidance, vLLM 0.2.5, LMQL; 52.4% to 74.1% cache hit in Chatbot Arena | Engine-level only; old vLLM baseline; no multi-model routing or failover |


## 2026-10-31 proposal audit

- Source attempted: https://arxiv.org/abs/2312.07104.
- Scope: Full-text sample: method and selected numerical/limitation statements checked; see L07.
- Historical Source read above records the earlier session, not a claim of a fresh full reading.
- arXiv title matched: SGLang: Efficient Execution of Structured Language Model Programs. Latest listed version: v2; arXiv DOI identifies the preprint, not peer review. A missing journal reference does not prove that no published version exists.
