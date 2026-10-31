# GPTCache: an open-source semantic cache for LLM applications (Bang, 2023)

| Field | Value |
|---|---|
| Topic (home) | 04 Cost reduction |
| Also relevant to | 08 Serving and gateway systems (caching layer) |
| Paper type | system (tool description with a small evaluation) |
| Venue and status | peer-reviewed workshop paper (NLP-OSS 2023, ACL; 7 pages) |
| Source read | full text (https://aclanthology.org/2023.nlposs-1.24.pdf) |
| Verified on | 2026-10-31, against the ACL Anthology page and its BibTeX record |
| Relevance to project | Medium to High |

## APA 7 reference
Bang, F. (2023). GPTCache: An open-source semantic cache for LLM applications enabling faster answers and cost savings. In L. Tan, D. Milajevs, G. Chauhan, J. Gwinnup, & E. Rippeth (Eds.), *Proceedings of the 3rd Workshop for Natural Language Processing Open Source Software (NLP-OSS 2023)* (pp. 212–218). Association for Computational Linguistics. https://doi.org/10.18653/v1/2023.nlposs-1.24

*Author note:* the Anthology record lists one author ("Bang, Fu"); the PDF byline reads "Bang Fu, Di Feng" (Zilliz Inc.). I followed the Anthology record. Confirm the form of the name before final submission.

## In-text citation forms
(Bang, 2023) · Bang (2023)

## 1. What it is about
GPTCache is an open-source library that sits in front of an LLM API. It converts each query to an embedding, looks for a semantically similar earlier query in a vector store, and, on a hit, returns the stored answer without calling the LLM. The paper describes its architecture and reports a small test of hit quality and latency.

## 2. The problem
LLM API calls are billed per token, rate-limited, and slow at peak. Traditional caches (Redis-style exact keys) miss paraphrases such as "which app lets you watch live football for free" versus "how can I watch a football match on my phone". Larger models or more compute raise cost and slow development.

## 3. Proposed solution
Six modular components in a standard cache-aside flow:
- **Adapter:** wraps OpenAI or LangChain calls, so integration needs no application change.
- **Pre-processor:** builds the cache key, e.g. strips template text, keeps the last turn of a conversation, trims long input.
- **Embedding generator:** cloud API or a local model (ONNX).
- **Cache manager:** scalar cache storage, vector storage (e.g. Milvus), and eviction (LRU or FIFO, with asynchronous index clean-up).
- **Similarity evaluator:** retrieves the top-k candidates and decides whether the best one really matches; a fine-tuned ALBERT model was adopted, with cohere rerank and SBERT cross-encoder also supported.
- **Post-processor:** returns the cached answer, or varies it with the request's temperature; on a miss the LLM answer is stored.

**How cost is modelled.** A hit consumes no LLM tokens ("no tokens are consumed when hitting the cache"), so savings equal the avoided per-request and per-token charge times the hit rate. The paper gives **no dollar figures**; it argues qualitatively that providers bill on requests and tokens, and reports latency only.

## 4. Data, models and tools
- Synthetic evaluation: web text plus ChatGPT-generated similar, opposite and unrelated sentence pairs; ChatGPT scores similarity (threshold 0.7) to label positive and negative hits.
- Embedding model paraphrase-albert-small-v2 on ONNX, local Mac (i7, 4 CPU, 32 GB). Code: https://github.com/zilliztech/GPTCache.

## 5. Key results
- Hit latency about 0.3 s on the local machine versus an average 3 s for a ChatGPT call; with other embedding models the end-to-end time is still "about 3 to 4 times faster". The abstract's "2 to 10 times" speed-up applies to cache hits.
- Table 1: 30,000 positive pairs cached, 1,000 queries sent: 876 hits, 124 misses; 837 positive hits, 39 negative (wrong) hits; hit latency 0.20 s. By my arithmetic 837 / 876 ≈ 95.5% of hits were correct.
- Table 2: 1,160 queries (half related, half unrelated): 570 hits, 590 misses; 549 positive, 21 negative hits; latency 0.17 s (about 96.3% correct by my arithmetic).
- Similarity threshold 0.7 gave a workable balance of hit ratio and correctness. Pairs with opposite meaning but high similarity did not hit the cache once the evaluator was fine-tuned.
- Best hit rates with current embeddings did not exceed 90%.

## 6. Limitations
*Stated by the authors:* more rigorous evaluation on larger and more diverse datasets is planned; the similarity threshold needs tuning to balance hits against false positives; embedding models made for search do not separate "opposite" queries well; long inputs and summarisation pre-processing make caching unstable; positive-hit rates near 99% are not yet reachable without cutting the hit rate.

*My observations:* labels and data come from ChatGPT, not humans; no multi-turn or user-specific queries; no dollar savings or real traffic hit-rate; a single-author workshop description of a product, so evidence is thin. A wrong cache hit returns a confident but incorrect answer, which a router would count as a quality failure.

## 7. Relevance to the AI Request Router
- A ready-made design for the **Redis plus embedding semantic cache** in the plan: cache before routing, so a hit has zero token cost and near-zero model load.
- **Reuse:** component split (key builder, embedder, similarity check, eviction); threshold 0.7 as a starting point; the hit / miss / positive-hit / negative-hit metrics. **Avoid:** accepting an embedding-only match without a second check. **Not covered:** multi-user privacy, cache staleness, quality-aware routing on a miss.

## 8. How to use it in the report
Section 2.4 (semantic caching) and the architecture chapter for the cache layer. Pair with Gill et al. (2025) for a precision-focused evaluation. Synthesis sentence: "GPTCache (Bang, 2023) moved caching from exact keys to embedding similarity but evaluated only on synthetic pairs, leaving false hits as an open problem."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Bang (2023) | Cut LLM API cost and latency for repeated or paraphrased queries | Embedding-based semantic cache with vector store, similarity evaluator and eviction | ChatGPT-generated sentence pairs; ALBERT embeddings; Milvus | Hit latency 0.17 to 0.3 s vs about 3 s; about 95% of hits correct in tests | Synthetic data; no dollar figures; false hits; 7-page workshop paper |
