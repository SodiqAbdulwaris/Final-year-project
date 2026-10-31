# EcoAssistant: cheaper and more accurate LLM assistants (Zhang et al., 2023)

| Field | Value |
|---|---|
| Topic (home) | 04 Cost reduction |
| Also relevant to | 01 Routing algorithms, 06 Fallback |
| Paper type | system (empirical) |
| Venue and status | preprint on arXiv (October 2023); a workshop version appears in the ICLR 2024 LLM Agents workshop listing; no archival proceedings version found |
| Source read | full text, arXiv v1 (https://arxiv.org/pdf/2310.03046) |
| Verified on | 2026-10-31, against the arXiv abstract page and the ICLR 2024 virtual-site / mlanthology workshop listing |
| Relevance to project | Medium |

## APA 7 reference
Zhang, J., Krishna, R., Awadallah, A. H., & Wang, C. (2023). *EcoAssistant: Using LLM assistant more affordably and accurately* [Preprint]. arXiv. https://doi.org/10.48550/arXiv.2310.03046

## In-text citation forms
(Zhang et al., 2023) · Zhang et al. (2023)

## 1. What it is about
A system for answering "code-driven" questions (weather, stock prices, nearby places) where the LLM must write code that calls an external API. It combines three ideas: let the LLM debug its code against an executor, try cheap models before expensive ones, and reuse past successful solutions as in-context examples.

## 2. The problem
LLMs rarely write correct API code on the first attempt, and serving high query volumes through a paid API is expensive. Prior cost work (quantisation, prompt compression, FrugalGPT) targeted single-turn generation rather than multi-turn agent conversations with code execution.

## 3. Proposed solution
1. **Executor loop.** An assistant agent (LLM) and a code-executor agent talk automatically, built on AutoGen. The conversation ends on a "TERMINATE" token, a context-window overflow, or after 5 turns.
2. **Assistant hierarchy.** Start with the cheapest assistant. If the conversation ends without success, restart with the next more expensive one. Success is judged by user feedback (a human, or a GPT-4 evaluator in the autonomous variant).
3. **Solution demonstration.** Store each successful (query, code) pair in a Chroma vector database. A new query retrieves its most similar stored query (multi-qa-mpnet-base-dot-v1 embeddings, cosine similarity) and shows it as an in-context example.

The two techniques interact: solutions written by GPT-4 become demonstrations for the cheaper model on later queries, so the cheap tier succeeds more often and the expensive tier is called less. No offline training is required.

**How cost is modelled.** Actual dollar cost from the API prices of GPT-3.5-turbo and GPT-4 (the paper says GPT-3.5-turbo is "an order of magnitude cheaper" than GPT-4). The self-hosted Llama-2-13B-chat is assumed to cost $0 because it "can be hosted with a reasonable amount of computing resources". Average model calls per query are also reported. In the autonomous variant the GPT-4 evaluator's cost is added to the system cost.

## 4. Data, models and tools
- Three ToolBench domains (Places, Weather, Stock), 100 random queries each, plus mixed sets of 300 queries in three orders; a 100-query human-evaluated subset, Mixed-100.
- Models: Llama-2-13B-chat, GPT-3.5-turbo, GPT-4; hierarchies "Hier-G" (GPT-3.5 then GPT-4) and "Hier-L" (Llama then GPT-3.5 then GPT-4). Code: https://github.com/JieyuZ2/EcoAssistant.

## 5. Key results
- Table 3 (Mixed-100, human evaluation; success rate, dollar cost): GPT-3.5-turbo 25%, $0.36; GPT-3.5 plus solution demonstration 45%, $0.48; GPT-4 59%, $13.77; GPT-4 plus demonstration 78%, $10.27; Hier-G 63%, $11.84; **EcoAssistant (Hier-G plus demonstration) 80%, $5.90**.
- EcoAssistant calls GPT-4 on average 1.25 times per query, against 2.57 for GPT-4 with demonstration (Table 3).
- Table 2, Places: GPT-4 85.00% at $12.58, versus Hier-G with demonstration 96.67% at $3.73.
- Without a human in the loop (Table 4, GPT-4 evaluator), EcoAssistant still beats GPT-4 by more than 10 points at over 50% lower cost (I read 72% success, but the table layout was ambiguous), though success falls about 8 points versus the human-in-the-loop run. The headline claim in the abstract is "10 points of success rate with less than 50% of GPT-4's cost".
- Order of arriving queries had little effect (Mixed-1/2/3 curves are consistent).

## 6. Limitations
*Stated by the authors:* the autonomous variant's evaluator sometimes distrusts GPT-3.5 and skips GPT-4, lowering success. I found no dedicated limitations section.

*My observations:* three API domains and 300 queries; GPT-4 acts as both judge and system component; success depends on a feedback signal that a general gateway may not have. Hier-G has the longest run time because it often tries both models in sequence. Treating a local model's cost as $0 hides GPU, energy and load. Only a non-archival workshop version is confirmed.

## 7. Relevance to the AI Request Router
- Strong real-dollar evidence that **cheap-first plus a success-feedback loop** halves cost, plus a **query-to-solution cache** (embedding retrieval) that improves the cheap tier over time. Both map to Redis/semantic-cache and failover design.
- **Reuse:** per-call dollar accounting; reporting average calls per tier; retrieval of past successes. **Avoid:** $0 for self-hosted models. **Not covered:** live load, multi-user fairness, difficulty prediction before the first call, latency budgets.

## 8. How to use it in the report
Section 2.4 (cheap-first strategies and caching of successes). Synthesis sentence: "Unlike FrugalGPT's single-turn cascades, Zhang et al. (2023) combine a model hierarchy with retrieval of past solutions in a streaming setting, cutting cost to roughly 43% of GPT-4 while raising success."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Zhang et al. (2023) | Cheaper, more accurate LLM assistants for code-driven QA | Executor loop, cheap-to-expensive assistant hierarchy, retrieval of past successful solutions | ToolBench (Places, Weather, Stock); Llama-2-13B, GPT-3.5, GPT-4; AutoGen, Chroma | 80% success at $5.90 vs GPT-4 59% at $13.77 (Mixed-100) | Preprint or workshop only; small dataset; needs success feedback; local model costed at $0 |
