# AutoMix: self-verification and POMDP routing (Aggarwal et al., 2024)

| Field | Value |
|---|---|
| Topic (home) | 01 Routing algorithms |
| Also relevant to | 04 Cost reduction and cascades, 02 Confidence estimation |
| Paper type | method (cascade with learned meta-verifier) |
| Venue and status | peer-reviewed (NeurIPS 2024) |
| Source read | full text of arXiv v5 (https://arxiv.org/pdf/2310.12963v5, NeurIPS 2024 header) |
| Verified on | 2026-10-31, against the NeurIPS 2024 proceedings page and arXiv |
| Relevance to project | Medium |

## APA 7 reference
Aggarwal, P., Madaan, A., Anand, A., Potharaju, S. P., Mishra, S., Zhou, P., Gupta, A., Rajagopal, D., Kappaganthu, K., Yang, Y., Upadhyay, S., Faruqui, M., & Mausam. (2024). AutoMix: Automatically mixing language models. In A. Globerson, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. Tomczak, & C. Zhang (Eds.), *Advances in Neural Information Processing Systems* (Vol. 37). Curran Associates. https://proceedings.neurips.cc/paper_files/paper/2024/hash/ecda225cb187b40ea8edc1f46b03ffda-Abstract-Conference.html (preprint: https://doi.org/10.48550/arXiv.2310.12963). No DOI; editor list not checked. Author order follows the paper (the user's notes list them alphabetically).

## In-text citation forms
(Aggarwal et al., 2024) · Aggarwal et al. (2024)

## 1. What it is about
A small model answers first, then the same model checks its own answer against the context, and the query goes to a larger model only if the check is unconvincing. A POMDP router decides how far to trust the noisy self-check. It needs only black-box API access and few training examples.

## 2. The problem
FrugalGPT and Hybrid LLM train a verifier or router per task with lots of in-domain data, which is hard with closed APIs. A bare confidence threshold cannot separate "fixable by a bigger model" from "unsolvable for every model".

## 3. Proposed solution
(1) The small LM answers. (2) **Few-shot self-verification** frames checking as entailment of the answer against context and question, sampled k times to get a probability v of correctness (one 4-shot prompt, no training). (3) **Routing:** either a **threshold** on v, or a **POMDP router** whose hidden state is the current model plus its unobserved performance, with v as a noisy observation estimated by kernel density from a small training set; reward is performance minus λ·cost, solved with the AdaOps particle-filter solver. It implicitly separates easy, hard-but-solvable and unsolvable queries. The paper also proposes **IBC** (incremental benefit per cost), the gain per extra cost over always using the large model.

## 4. Data, models and tools
Small models: Mistral-7B, Llama-2-13B, GPT-3.5; large: GPT-4 (Llama-2-70B as middle model in a three-model test). Datasets: QASPER, QuALITY, CoQA, MuTual, DIPLOMAT. Relative cost: 1 for the small model and 60, 100, 200 for GPT-4 against GPT-3.5, Llama-2-13B and Mistral-7B, from public prices; verification costs the small model's price. Baselines: FrugalGPT and Hybrid LLM (free routers), random mixing. Code: github.com/automix-llm/automix (as stated).

## 5. Key results
- Abstract: over 50% lower cost at comparable performance (introduction: more than 2x).
- Figure 4 and Table 1: the POMDP router is the only method with positive IBC in every setting; best on DIPLOMAT, averaging 122% across the three small models (Section 5.3).
- With 50 training examples AutoMix keeps about 15% IBC and beats both baselines by over 20 points (Figure 5 left).
- Gains appear from a cost ratio as low as 1:10 on many datasets (Figure 5 right).
- POMDP overhead under 1 ms per query (Section 5.4).
- Three-model setting (Figure 6): beats FrugalGPT, chained AutoMix and union AutoMix.

## 6. Limitations
**Authors:** gains vary by model and dataset; designed for context-grounded and dialogue reasoning, not factual QA or commonsense; generation tasks with subjective quality are future work.
**Mine:** a cascade, so escalated queries pay for a small-model answer, k verifications and a large-model answer (latency and tokens); costs are relative units, not measured GPU load; needs a context in the prompt; no failure or queue handling. An independent study cited by Varangot-Reille et al. (2026, Section 4.4.5) reports AutoMix did not beat random routing on RouterBench (not checked by me).

## 7. Relevance to the AI Request Router
- Supports quality estimation *after* a cheap attempt: an optional "escalate if unsure" policy and the escalation path of failover.
- Reuse: IBC against random mixing; treating confidence as a noisy signal; cost as a ratio re-set per deployment (a self-hosted 13B model can be nearly free, GPT-4 is not).
- Avoid: self-verification for non-context tasks without testing; verifier cost on every request.
- Not covered: pre-generation routing, live load, availability failures.

## 8. How to use it in the report
- Chapter 2 cascading and uncertainty-based routing (with topic 04 and 02); chapter 3 escalation policy and IBC.
- "AutoMix (Aggarwal et al., 2024) learns how far to trust a small model's self-check with a POMDP, but only for context-grounded tasks and with sequential calls."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Aggarwal et al. (2024) | Mix small and large LMs via black-box APIs with little data | Few-shot self-verification plus POMDP or threshold router; IBC | QASPER, QuALITY, CoQA, MuTual, DIPLOMAT; Mistral, Llama-2, GPT-3.5/4 | Over 50% cost reduction at comparable performance; works with 50 examples | Context tasks only; sequential latency; no load or failover |
