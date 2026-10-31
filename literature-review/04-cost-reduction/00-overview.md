# 04 LLM routing cost reduction: overview

## 1. Topic definition and why it matters to the router
Cost reduction covers every technique that lowers the price (and often the latency) of an LLM answer without a matching drop in quality: choosing a cheaper model per request (routing), trying cheap models first and escalating (cascading), sending fewer input tokens (prompt compression), and skipping the model call entirely (semantic caching). The AI Request Router's scoring function weighs predicted quality, cost and live load, so it needs (a) a defensible **cost term** and (b) evidence for which cost levers actually work. These papers supply the cost formulas (per-token price, per-call or deferral-rate, latency), the empirical size of the savings, and the failure modes (weak quality estimators, false cache hits, compression losses). What they mostly lack is any notion of live load or self-hosted GPU cost, which is exactly where the project claims novelty.

## 2. Comparison of papers
| Paper | Year | Type | Venue | Problem | Method | Key result | Limitation |
|---|---|---|---|---|---|---|---|
| Dekoninck et al. | 2025 | method | ICML 2025 | When do routing and cascading help; can they be unified? | Optimal routing, cascading and cascade routing as a cost-constrained linear programme | Up to 8% (RouterBench) and 14% (SWE-Bench) AUC gain over baselines | Simulated noise; static cost; needs quality estimators |
| Yue et al. | 2024 | method | ICLR 2024 | Cheap, reliable cascade for reasoning | Answer-consistency voting over CoT and PoT samples from GPT-3.5, escalate to GPT-4 | 0.929 vs 0.931 accuracy at about 40% of GPT-4 cost | Verifiable tasks only; many samples; latency |
| Gupta et al. | 2024 | method | ICLR 2024 | How should small LMs defer on generative tasks? | Quantile token-level uncertainty and a learned post-hoc deferral rule | Learned rule most consistent; sum score can be worse than random (TriviaQA −13.09%) | FLAN-T5 only; needs logprobs |
| Zhang et al. | 2023 | system | preprint (ICLR 2024 workshop listing) | Cheaper LLM assistants for code-driven QA | Executor loop, cheap-to-expensive hierarchy, solution retrieval | 80% success at $5.90 vs GPT-4 59% at $13.77 (Mixed-100) | Small data; $0 for local model |
| Jiang et al. | 2023 | method | EMNLP 2023 | Long prompts are costly | Coarse-to-fine perplexity-based prompt compression | 20x compression, 77.33 vs 78.85 EM on GSM8K | Needs 7B compressor; 25x+ degrades |
| Jiang et al. | 2024 | method | ACL 2024 | Long-context cost, noise, position bias | Question-aware compression, reordering | 52.6% to 94.0% API cost saved per 1,000 samples | Per-question recompression |
| Narasimhan et al. | 2025 | method | ICLR 2025 (oral) | Cascades are sequential; speculative decoding is rigid | Speculative execution of cascade deferral rules | Up to 2.61x latency reduction at large-model quality | Two co-served models; batch size 1 |
| Ding et al. | 2025 | method | ICML 2025 | Routers overuse the large model | Router picks (model, n samples); proxy-reward best-of-n | 60% cost cut, 0.8% quality drop vs GPT-4o | One judge; static prices |
| Bang | 2023 | system | NLP-OSS 2023 (workshop) | Repeated or paraphrased queries cost tokens | Embedding-based semantic cache | 0.17 to 0.3 s hit latency vs about 3 s; about 95% of hits correct | Synthetic evaluation; no dollar data |
| Gill et al. | 2025 | system | IEEE IPDPS 2025 | Privacy, false hits and context in semantic caches | Client-side cache, federated embeddings, context chain | Precision 0.72 vs 0.52; false hits 89 vs 233 | Client-side; one baseline |

## 3. How each paper models cost (input for the router's cost term)
| Paper | Unit of cost | Concrete numbers reported |
|---|---|---|
| Dekoninck et al. (2025) | Monetary (tokens × price) or latency; estimated per query | No prices; SWE-Bench cost = completion time |
| Yue et al. (2024) | C = C_w + C_d + 1[reject]·C_s, from token counts and prices | GPT-4 output about 30 times GPT-3.5-turbo (2023 list) |
| Gupta et al. (2024) | Abstract per-model cost; average cost = c1 + D·c2 | None |
| Zhang et al. (2023) | Dollars per query batch; local model assumed $0 | GPT-4 $13.77 vs EcoAssistant $5.90 per 100 queries |
| Jiang et al. (2023) | Prompt tokens; compute ratio of small LM to LLM | 7B vs 175B gives about 1/25 per token; 2,366 → 117 tokens |
| Jiang et al. (2024) | Dollars per 1,000 samples (GPT-3.5-Turbo) | $93.6 → $5.6 on LooGLE |
| Narasimhan et al. (2025) | Large-model call rate and wall-clock latency | 2.61x at best |
| Ding et al. (2025) | n × avg output length × output price + input length × input price | Table of 8 models in $ per 1M tokens (GPT-4o 5 / 15; Llama-3.1-8B 0.3 / 0.61) |
| Bang (2023) | Avoided requests and tokens; hit costs zero tokens | None (latency only) |
| Gill et al. (2025) | Avoided calls, false hits, storage, search time | None in dollars |

**Reading across:** per-token pricing is the common currency for hosted APIs. Nobody models GPU-hour or load-dependent cost for self-hosted models; Zhang et al. set it to zero and Ding et al. use API prices for open models. A candidate router cost term (my synthesis, not from one paper) is cost_i(x) = p_in,i · n_in(x) + p_out,i · E[n_out,i | x], with the per-token price for self-hosted models derived from GPU cost divided by measured throughput at current utilisation.

## 4. Themes and trends
1. **From heuristic to principled selection.** FrugalGPT (documented in topic 01) introduced learned cascades; Yue et al. replace the learned scorer with sampled-answer consistency, Gupta et al. with token-level uncertainty, and Dekoninck et al. show both are special cases of one cost-constrained optimisation in which estimator quality dominates.
2. **Spending test-time compute where it pays.** Ding et al. extend routing from "which model" to "which model and how many samples", and Narasimhan et al. fuse cascading with speculative decoding. Both treat cost as a continuous knob, not a binary choice.
3. **Cheaper inputs.** The LLMLingua pair attack the other side of the price formula (input tokens). They are orthogonal to routing but change the numbers a router sees.
4. **Avoiding the call.** EcoAssistant (solution reuse), GPTCache and MeanCache show a progression from "cache works" to precision-weighted, context-aware evaluation; false hits are the key risk.
5. **Trend:** two-model setups (2023 to 2024) give way to many-model pools (Dekoninck 11 models, Ding 8) and to publication at top venues in 2025; evidence still rests on offline accuracy and 2023 to 2024 API list prices.

## 5. Strongest three papers for the proposal
1. **Dekoninck et al. (2025):** a formal basis for the scoring function (maximise quality minus λ × cost under a budget) and a clear statement that the classifier's accuracy is the critical component, which justifies the project's evaluation focus.
2. **Ding et al. (2025):** the nearest published system to the planned architecture (a BERT-style predictor feeding a cost-aware selector over many models), with an explicit, reusable cost formula and price table.
3. **Gill et al. (2025):** the most rigorous treatment of semantic caching (precision-weighted metric, context handling, compression), backing the Redis cache layer and its evaluation. Bang (2023) is the practical baseline it improves on.

## 6. Gaps visible in this topic (for the gap statement)
- **No live load.** None of the ten papers includes queueing, utilisation or contention in the selection rule. Evidence: Dekoninck et al. use static per-model cost; Ding et al. report only router overhead; Narasimhan et al. measure latency at batch size 1.
- **Self-hosted cost is missing or wrong.** Zhang et al. cost the local Llama-2 model at $0; Ding et al. price open models by API; Jiang et al. (2023) only give a parameter-ratio estimate.
- **Latency is a side effect, not a budget.** Cascades and best-of-n add calls and delay (Yue et al., Appendix K; Narasimhan et al., higher total compute; Zhang et al., Hier-G has the longest run time) yet no objective includes a latency budget.
- **Quality signals are assumed.** Cascade gains depend on a post-hoc quality signal (Dekoninck et al.), logprobs (Gupta et al.) or checkable answers (Yue et al.); free-form chat has none.
- **Levers are studied in isolation.** Compression changes the prompt and can break cache keys (Jiang et al., 2024, limitation on caching), semantic caches ignore routing, and routers ignore both. No paper evaluates cache, compress, route and fail over together.
- **Caching risk is under-measured.** False hits are reported on small or synthetic sets (Bang: 39 of 876 hits wrong; Gill et al.: 89 false hits per 700 unique queries); the effect on end-to-end answer quality is not.
- **Stale or narrow evidence.** Prices and models are 2023 to 2024 vintage and mostly OpenAI, Mistral, Phi and T5/Gemma pairs.

## 7. Paper files (this topic)
- [Dekoninck et al. (2025), cascade routing](dekoninck-2025-cascade-routing.md)
- [Yue et al. (2024), mixture-of-thought cascades](yue-2024-mot-cascades.md)
- [Gupta et al. (2024), token-level uncertainty cascades](gupta-2024-token-uncertainty-cascades.md)
- [Zhang et al. (2023), EcoAssistant](zhang-2023-ecoassistant.md)
- [Jiang et al. (2023), LLMLingua](jiang-2023-llmlingua.md)
- [Jiang et al. (2024), LongLLMLingua](jiang-2024-longllmlingua.md)
- [Narasimhan et al. (2025), speculative cascades](narasimhan-2025-speculative-cascades.md)
- [Ding et al. (2025), BEST-Route](ding-2025-best-route.md)
- [Bang (2023), GPTCache](bang-2023-gptcache.md)
- [Gill et al. (2025), MeanCache](gill-2025-meancache.md)

## 8. Related papers documented elsewhere
Topic 01 (routing algorithms; links checked against the files on disk):
- FrugalGPT (Chen et al.): [../01-routing-algorithms/chen-2024-frugalgpt.md](../01-routing-algorithms/chen-2024-frugalgpt.md)
- RouteLLM (Ong et al.): [../01-routing-algorithms/ong-2025-routellm.md](../01-routing-algorithms/ong-2025-routellm.md)
- Hybrid LLM (Ding et al., 2024): [../01-routing-algorithms/ding-2024-hybrid-llm.md](../01-routing-algorithms/ding-2024-hybrid-llm.md)
- AutoMix (Aggarwal et al., 2024): [../01-routing-algorithms/aggarwal-2024-automix.md](../01-routing-algorithms/aggarwal-2024-automix.md)
- Varangot-Reille et al. survey: [../01-routing-algorithms/varangot-reille-2026-routing-survey.md](../01-routing-algorithms/varangot-reille-2026-routing-survey.md)

Other topics (no link, by ownership table): Chuang et al. confidence tokens and Kadavath et al. (02, both cited by the papers above); speculative decoding (Leviathan et al.) and vLLM prefix and engine optimisations (05); RouterBench (Hu et al., used by Dekoninck et al.) (07).

## 9. Search log
Searches ran on 2026-10-30 and 2026-10-31. Counts are title-level screening; I did not keep numeric result counts from each web search.

| Source | Search string or action | Use |
|---|---|---|
| arXiv abstract pages | the five assigned papers by arXiv ID; then the extra candidates | metadata (title, authors, dates, DOI, comments) |
| General web search (US) | "Dekoninck Unified Approach to Routing and Cascading ICML 2025"; "Gupta Narasimhan Language Model Cascades token-level uncertainty ICLR 2024"; "EcoAssistant ... published venue"; "speculative cascades ICLR 2025"; "GPTCache semantic cache NLP-OSS 2023"; "LongLLMLingua ACL 2024 DOI"; "BEST-Route ICML 2025"; "MeanCache IPDPS 2025 DOI"; "Large Language Model Cascades with Mixture of Thoughts ... ICLR 2024" | venue and publication-status checks, candidate discovery |
| ACL Anthology | EMNLP 2023 (LLMLingua), NLP-OSS 2023 (GPTCache), ACL 2024 (LongLLMLingua) pages and BibTeX | DOI, pages, authors |
| PMLR, ICLR proceedings | ICML 2025 pages for Dekoninck and Ding; ICLR 2024 and 2025 listings | venue, pages |
| IEEE Xplore | DOI redirect for MeanCache; page content not readable by the fetch tool | DOI existence only |
| OpenReview | forum page for Gupta et al. returned a verification screen | not read; ID taken from Dekoninck et al.'s reference list |

**Counts:** screened 14 candidate titles (5 assigned, 5 added after search, 4 noted from search results or reference lists); included 10 full files (5 assigned, 5 added). Full text read for all 10 (PDF text extracted with pdftotext, and key tables checked against page images where the extraction was scrambled).

**Added papers:** Narasimhan et al. (2025), Ding et al. (2025), Bang (2023), Gill et al. (2025), Jiang et al. (2024). All 2020 or later; four peer-reviewed at main venues, one workshop paper (Bang).

**Dropped or not included:** none of the five assigned papers was dropped. Not included, with reason:
- GPT Semantic Cache (arXiv 2411.05276): preprint, seen only in search results, redundant with GPTCache and MeanCache.
- Selective Context (Li, 2023): cited as a baseline in LLMLingua; not retrieved.
- FORC (Sakota et al., 2024) and Tryage (Hari & Thomson, 2023): routing papers cited in the files above; belong to topics 01 and 02, not retrieved.

**Corrections and caveats for the supervisor:**
- Yue et al.'s arXiv title differs from the brief; the ICLR proceedings title is used ("...mixture of thought representations for cost-efficient reasoning").
- Gupta et al. (ICLR 2024) and EcoAssistant have no archival DOI; arXiv DOIs are given. EcoAssistant is a preprint with only a workshop listing found.
- ICML/PMLR papers (Dekoninck, Ding) have no DOI on their proceedings pages; the arXiv DOI is given alongside the PMLR URL.
- GPTCache: the ACL Anthology lists author "Bang, Fu" only, but the PDF byline reads "Bang Fu, Di Feng". The MeanCache page range comes from a secondary listing.
