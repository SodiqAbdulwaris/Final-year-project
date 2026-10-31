# MeanCache: user-centric semantic caching (Gill et al., 2025)

| Field | Value |
|---|---|
| Topic (home) | 04 Cost reduction |
| Also relevant to | 08 Serving and gateway systems (caching layer) |
| Paper type | system (empirical) |
| Venue and status | peer-reviewed (IEEE IPDPS 2025) |
| Source read | full text, arXiv v4 (https://arxiv.org/pdf/2403.02694), marked "Accepted at 2025 IEEE 39th IPDPS" |
| Verified on | 2026-10-31; DOI resolves to the IEEE Xplore record (the IEEE page itself could not be read, so pages come from a secondary listing) |
| Relevance to project | Medium |

## APA 7 reference
Gill, W., Elidrisi, M., Kalapatapu, P., Ahmed, A., Anwar, A., & Gulzar, M. A. (2025). MeanCache: User-centric semantic caching for LLM web services. In *2025 IEEE International Parallel and Distributed Processing Symposium (IPDPS)* (pp. 1298–1310). IEEE. https://doi.org/10.1109/IPDPS64566.2025.00117

*Pages 1298–1310 come from a university repository listing, not from the IEEE page; check before submission.*

## In-text citation forms
(Gill et al., 2025) · Gill et al. (2025)

## 1. What it is about
A semantic cache that lives on the user's device, not in the provider's server. Similar past queries are found with a small embedding model; a federated-learning loop improves that model without sharing queries. It also checks the conversation context, so a follow-up question is not mistaken for a repeat.

## 2. The problem
Server-side semantic caches such as GPTCache must hold every user's queries (privacy, scale), still bill the user for the round trip, use one embedding model for everyone, sometimes need a large model to embed, and wrongly return a cached answer to context-dependent follow-ups (a similar-looking follow-up that depends on different earlier turns), giving high false-hit rates.

## 3. Proposed solution
- **Local cache** per user: cached query embeddings, responses, parent-query context chain, with LRU eviction.
- **Small embedding models** (MPNet, Albert) trained collaboratively with federated learning (FedAvg) on clients' own query pairs, so the model adapts to each user's wording without uploading data. A **cosine-similarity threshold** is also learned federatedly; the F-score is computed with beta 0.5 so precision counts double, since a false hit hands the user a wrong answer while a false miss only costs one normal LLM call.
- **Context chains:** each cached query stores its parent queries; a match is accepted only if the context also matches (Algorithm 1).
- **Embedding compression:** PCA from 768 dimensions to 64.

**How cost is modelled.** Costs avoided are LLM calls (billing, provider load, energy). The paper reports **no dollar savings**; cost proxies are false-hit counts (each forces a resend), storage, search time and embedding time. The cost of a miss is one extra normal LLM call.

## 4. Data, models and tools
- Dataset from GPTCache's repository (1,000 standalone queries: 700 unique, 300 duplicates) and a new set of 450 contextual queries. Baseline GPTCache (Llama 2 for similarity, threshold 0.7). LLM backend: local Llama 2 service. Implemented with the Flower FL framework; code at https://github.com/SEED-VT/MeanCache.

## 5. Key results
- Standalone queries (Table I, Figure 7): MeanCache with MPNet precision 0.72 versus 0.52 for GPTCache; F-score 0.73 (MPNet) and 0.68 (Albert) versus 0.56. False hits 89 versus 233 among 700 unique queries. GPTCache has higher recall, which the authors consider less important. Abstract: about 17% higher F-score and 20% higher precision.
- Contextual queries (450-query set): MeanCache over 25% higher F-score and accuracy and 32% higher precision; in a 100-query check, 3 false hits against 54 for GPTCache (Figures 8 to 9).
- Compression: 83% less storage and about 11% faster search, with a slight F-score decrease but still above GPTCache (Figure 10).
- Embedding time per query: Llama 2 0.04 s, Albert 0.005 s, MPNet 0.009 s.

## 6. Limitations
*Stated by the authors:* I did not find a dedicated limitations section in the text I read; they acknowledge that compression slightly lowers the F-score and that clients have limited storage.

*My observations:* it is built for client-side caches, whereas a gateway serves many users and would need a shared, access-controlled cache. It is compared only with GPTCache, on GPTCache's own dataset plus the authors' contextual set. It uses small curated datasets and a local Llama 2 backend. No dollar savings or real traffic are shown. Federated training adds operational complexity unnecessary for a single-gateway project.

## 7. Relevance to the AI Request Router
- Supplies the **evaluation viewpoint** for a gateway cache: weight precision above recall (F0.5), count false hits, and treat context-dependent follow-ups as misses. A wrong cached answer is worse than one extra model call.
- **Reuse:** F0.5 metric; context-chain check (store the previous turn's key); embedding compression to cut Redis memory and search time; small embedding models (MPNet matches the planned sentence-transformers). **Avoid:** federated training. **Not covered:** shared multi-tenant caches, TTL and staleness, routing on a miss.

## 8. How to use it in the report
Section 2.4 (semantic caching) as the second, more rigorous cache paper after GPTCache; also the evaluation-metric choice in Section 3.9. Synthesis sentence: "Gill et al. (2025) improve on GPTCache's synthetic evaluation by measuring precision-weighted hit decisions and context-dependent queries, cutting false hits from 233 to 89 per 700 unique queries."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Gill et al. (2025) | Reduce LLM calls with a privacy-preserving semantic cache that handles context | Client-side cache; federated embedding and threshold training; context chain; PCA compression | GPTCache dataset (1,000 queries) plus 450 contextual queries; MPNet, Albert; Llama 2 | Precision 0.72 vs 0.52; false hits 89 vs 233; 83% less storage | Client-side only; one baseline; small data; no dollar savings |
