Status: DRAFT
Depends on: D08; D12
Sources: Primary URLs in source table and proposal-audit section
Open items: Scoped numerical/final-version checks recorded below

# LongLLMLingua: question-aware compression for long contexts (Jiang et al., 2024)

| Field | Value |
|---|---|
| Topic (home) | 04 Cost reduction |
| Also relevant to | none beyond this topic (extends Jiang et al., 2023 LLMLingua) |
| Paper type | method (empirical) |
| Venue and status | peer-reviewed (ACL 2024, main conference, long paper) |
| Source read | full text, arXiv v2 (https://arxiv.org/pdf/2310.06839) |
| Verified on | 2026-10-31, against the ACL Anthology page |
| Relevance to project | Medium |

## APA 7 reference
Jiang, H., Wu, Q., Luo, X., Li, D., Lin, C.-Y., Yang, Y., & Qiu, L. (2024). LongLLMLingua: Accelerating and enhancing LLMs in long context scenarios via prompt compression. In *Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)* (pp. 1658–1677). Association for Computational Linguistics. https://doi.org/10.18653/v1/2024.acl-long.91

## In-text citation forms
(Jiang et al., 2024) · Jiang et al. (2024)

## 1. What it is about
An extension of LLMLingua to long prompts such as retrieved documents. Compression is conditioned on the user's question so that the parts relevant to it survive, and the surviving documents are reordered to avoid the "lost in the middle" effect. On several benchmarks the compressed prompt gave *better* answers than the full prompt at a fraction of the cost.

## 2. The problem
Long prompts bring three problems: higher cost and latency, lower accuracy because irrelevant text dilutes the useful part, and position bias, where answer-bearing text in the middle is used less. LLMLingua and Selective-Context compress by token predictability alone, ignoring the question, so in long contexts they keep much question-irrelevant noise.

## 3. Proposed solution
Four mechanisms on top of LLMLingua (small LM LLaMA-2-7B-Chat as compressor):
1. **Question-aware coarse compression:** rank documents by the small LM's perplexity of the question given each document (lower means more relevant) and keep the top ones.
2. **Document reordering:** place the highest-ranked documents at the start of the prompt.
3. **Dynamic compression ratio and question-aware fine compression:** more relevant documents are compressed less, and token selection uses *contrastive perplexity* (how much the question lowers a token's perplexity).
4. **Subsequence recovery:** after the LLM answers, map compressed fragments in the answer back to the original text, so entities and numbers are intact.

**How cost is modelled.** Input and output tokens at GPT-3.5-Turbo API prices (Appendix D, Table 9), per 1,000 samples, plus end-to-end latency including compression time on a V100-32GB. The paper does not state per-token prices in dollars within the text I read; it cites the OpenAI pricing page.

## 4. Data, models and tools
- NaturalQuestions multi-document QA (20 documents), LongBench, ZeroSCROLLS, MuSiQue, LooGLE. Target models: GPT-3.5-Turbo-0613 (16k for longer prompts) and LongChat-13B-16k, greedy decoding.
- Baselines: BM25, Gzip, SentenceBERT, OpenAI embeddings (retrieval), Selective-Context, LLMLingua. Code: https://aka.ms/LongLLMLingua.

## 5. Key results
- Abstract: on NaturalQuestions with the answer at the 10th position, accuracy rises by up to 21.4% with about 4x fewer tokens to GPT-3.5-Turbo; compressing ~10k-token prompts at 2x to 6x speeds up end-to-end latency by 1.4x to 2.6x.
- LooGLE (Table 8): original prompt 30,546 tokens scores 22.6 on average; LongLLMLingua uses 3,121 tokens (10x) and scores 32.1. LLMLingua at 3,404 tokens scores 17.3.
- **Dollar cost per 1,000 samples with GPT-3.5-Turbo (Table 9):** multi-document QA 4.6 → 1.3 (71.7% saved); LongBench 31.5 → 3.0 (90.5%); ZeroSCROLLS 30.6 → 3.2 (89.5%); MuSiQue 3.8 → 1.8 (52.6%); LooGLE 93.6 → 5.6 (94.0%).
- Going from 2x to 4x compression, the method even gains slightly, whereas retrieval baselines decline as compression increases (Section 5.2).
- Using GPT-2-small as compressor still beat the original prompt by 2.6 points on MuSiQue (Table 7).

## 6. Limitations
*Stated by the authors:* the method is question-aware, so the same context must be recompressed for every new question and cannot be cached; it needs about twice the computation of LLMLingua. Evaluated mainly on QA and summarisation, with greater loss on retrieval tasks in very long contexts for compression-based baselines.

*My observations:* it needs a 7B compressor on a GPU; only two target LLMs (one API, one open); savings are specific to long-context workloads and say little about short chat prompts; the dollar figures depend on one provider's price list (collection date not stated).

## 7. Relevance to the AI Request Router
- Relevant to **RAG-style or document-heavy requests**, where input tokens dominate cost. Cost per request is mainly input tokens × price, so the router's cost term benefits when long prompts are compressed before dispatch.
- **Reuse:** per-1,000-samples cost reporting; relevance-first reordering as a cheap alternative to full compression. **Avoid:** adding a GPU compressor to the hot path unless prompts are long. **Not covered:** interaction with difficulty prediction, caching of compressed contexts, live load.

## 8. How to use it in the report
Section 2.4 (prompt compression), directly after Jiang et al. (2023). Synthesis sentence: "Jiang et al. (2024) show that conditioning compression on the question both improves accuracy and cuts API cost by 52.6% to 94.0% per 1,000 samples on long-context benchmarks, at the price of non-cacheable, per-question compression."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Jiang et al. (2024) | Cut cost and position bias in long-context prompts | Question-aware coarse-to-fine compression, reordering, subsequence recovery | NaturalQuestions, LongBench, ZeroSCROLLS, MuSiQue, LooGLE; GPT-3.5-Turbo, LongChat-13B | Up to 21.4% accuracy gain at 4x fewer tokens; 52.6% to 94.0% cost saved per 1,000 samples | Per-question recompression; 7B compressor; two target models |


## 2026-10-31 proposal audit

- Source attempted: https://arxiv.org/abs/2310.06839.
- Scope: Abstract/metadata check only in this session; detailed numerical results remain unchecked.
- Historical Source read above records the earlier session, not a claim of a fresh full reading.
- arXiv title matched: LongLLMLingua: Accelerating and Enhancing LLMs in Long Context Scenarios via Prompt Compression. Latest listed version: v2; arXiv DOI identifies the preprint, not peer review. A missing journal reference does not prove that no published version exists.
