# RouteLLM: learning to route with preference data (Ong et al., 2025)

| Field | Value |
|---|---|
| Topic (home) | 01 Routing algorithms |
| Also relevant to | 04 Cost reduction, 07 Benchmarks |
| Paper type | method (with open-source framework) |
| Venue and status | peer-reviewed (ICLR 2025 poster) |
| Source read | full text (https://arxiv.org/pdf/2406.18665v4) |
| Verified on | 2026-10-31, against arXiv and the PDF header ("Published as a conference paper at ICLR 2025"); the arXiv page shows no venue comment, and the OpenReview listing (forum 8sSqNntaMr, ICLR 2025 poster) was seen only in a search result, so it is unconfirmed (the page itself was bot-blocked) |
| Relevance to project | High |

## APA 7 reference
Ong, I., Almahairi, A., Wu, V., Chiang, W.-L., Wu, T., Gonzalez, J. E., Kadous, M. W., & Stoica, I. (2025). RouteLLM: Learning to route LLMs with preference data. In *Proceedings of the Thirteenth International Conference on Learning Representations (ICLR 2025)*. https://openreview.net/forum?id=8sSqNntaMr (preprint: https://doi.org/10.48550/arXiv.2406.18665). ICLR has no DOI; the arXiv DOI is the same work.

## In-text citation forms
(Ong et al., 2025) · Ong et al. (2025)

## 1. What it is about
RouteLLM trains routers that decide, per query, whether a strong, costly LLM or a weak, cheap one should answer. Routers learn from human preference votes (Chatbot Arena) plus cheap data augmentation. An open-source framework for training, serving and evaluating routers is released.

## 2. The problem
Strong models can cost over 50x more per output token than weak ones, yet sending everything to the strong model wastes money. Earlier approaches call several models per query (LLM-Blender, FrugalGPT, AutoMix), adding latency, or were tested on one dataset (Hybrid LLM). The authors want a single-call router that generalises out of domain and across model pairs.

## 3. Proposed solution
Binary routing. A **win-prediction model** estimates P(strong beats weak | query) from preference labels; a **threshold α** turns it into a decision (below α: weak model). Four predictors are compared: similarity-weighted Bradley-Terry ranking, matrix factorisation, a BERT classifier and a Llama 3 8B classifier. Sparse Arena labels are handled by grouping models into tiers, and training is augmented with about 1,500 MMLU golden-label questions or about 120K GPT-4-judged Nectar queries (about USD 700). Metrics: PGR (share of the strong-weak gap recovered), APGR (average PGR over cost levels) and CPT(x%) (fewest strong calls needed for PGR of x%).

## 4. Data, models and tools
Training: Chatbot Arena (65K comparisons across 64 models after filtering). Evaluation: MMLU, MT-Bench, GSM8K, decontaminated. Main pair: GPT-4-1106-preview and Mixtral-8x7B; transfer pairs Claude 3 Opus/Sonnet and Llama 3.1 70B/8B. Baseline: random router. Code: https://github.com/lm-sys/RouteLLM (link live; the paper only says "open source").

## 5. Key results
- Abstract: over 2x cost reduction without quality loss.
- MT-Bench (Table 1, Arena + judge data): matrix factorisation CPT(50%) = 13.40% against 49.03% for random.
- Table 6 (Section 5.4), cost saving ratio against a random-routing baseline at the same quality, taken as the inverse of the ratio of GPT-4 calls (best router at CPT(50%) versus random): 3.66x on MT-Bench (95% of GPT-4 quality), 1.41x on MMLU (92%), 1.49x on GSM8K (87%). It is not a saving against sending every query to GPT-4.
- Arena-only routers sit near random on MMLU and GSM8K; golden-label augmentation lifts MMLU APGR by 14 to 21% over random (Table 2).
- New model pairs without retraining (Table 4): SW ranking CPT(50%) of 23.27% (Claude pair) and 21.18% (Llama pair).
- Overhead (Table 7): at most 0.4% of GPT-4 generation cost; 155 requests/s for matrix factorisation on one L4 GPU.
- Appendix E: up to 40% fewer GPT-4 calls than Unify AI and Martian at equal quality.

## 6. Limitations
**Authors:** real-world distributions may differ; only two models; performance of different routers trained on the same data can vary widely on the same benchmark without a clear explanation (Section 6).
**Mine:** quality proxies (Arena votes, GPT-4 judge); cost is a fixed token price, with no load or latency; needs strong/weak tiers fixed in advance; out-of-domain performance depends on augmentation data; commercial comparison rests on one benchmark.

## 7. Relevance to the AI Request Router
- Supports the classifier, the cost/quality score and the threshold knob (α behaves like a quality-versus-cost weight).
- Reuse: CPT and APGR metrics, cheap embedding-based routers, the augmentation recipe, and the benchmark-similarity score (Table 5) as a generalisation check.
- Avoid: binary-only routing and static price as the only cost signal.
- Not covered: live load, failover, latency budgets, self-hosted serving, N-way routing.

## 8. How to use it in the report
- Chapter 2 preference-based routing; chapter 3 evaluation metrics.
- "Unlike Hybrid LLM (Ding et al., 2024), RouteLLM (Ong et al., 2025) compared four router families trained on human preferences, but still treated cost as a fixed price."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Ong et al. (2025) | Cut LLM cost by routing between strong and weak model | Win-probability router with cost threshold; data augmentation | Chatbot Arena; MMLU, MT-Bench, GSM8K; GPT-4 vs Mixtral | Needs 3.66x fewer GPT-4 calls than random routing at 95% of GPT-4 quality (MT-Bench); transfers to new pairs | Two models; fixed price; no load or failover |
