Status: DRAFT
Depends on: D08; D12
Sources: Primary URLs in source table and proposal-audit section
Open items: Scoped numerical/final-version checks recorded below

# LLM cascades with mixture of thought representations (Yue et al., 2024)

| Field | Value |
|---|---|
| Topic (home) | 04 Cost reduction |
| Also relevant to | 01 Routing algorithms, 02 Difficulty prediction, 06 Fallback |
| Paper type | method (empirical) |
| Venue and status | peer-reviewed (ICLR 2024) |
| Source read | full text, arXiv v3 (https://arxiv.org/pdf/2310.03094), which carries the "Published as a conference paper at ICLR 2024" header |
| Verified on | 2026-10-31, against the arXiv abstract page and the ICLR 2024 proceedings listing |
| Relevance to project | Medium |

## APA 7 reference
Yue, M., Zhao, J., Zhang, M., Du, L., & Yao, Z. (2024). Large language model cascades with mixture of thought representations for cost-efficient reasoning. In *The Twelfth International Conference on Learning Representations*. https://proceedings.iclr.cc/paper_files/paper/2024/hash/5de11e930c1bbfda5d4fc9d2b0924032-Abstract-Conference.html (preprint DOI: https://doi.org/10.48550/arXiv.2310.03094)

*Note:* the arXiv title reads "...Mixture of Thoughts Representations..."; the proceedings title is used above.

## In-text citation forms
(Yue et al., 2024) · Yue et al. (2024)

## 1. What it is about
A two-LLM cascade for reasoning questions. GPT-3.5-turbo answers first; if its answers are not consistent across several samples, the question goes to GPT-4. Consistency is checked across a mixture of chain-of-thought (CoT) and program-of-thought (PoT) prompts, and the cascade reaches near-GPT-4 accuracy at about 40% of the cost.

## 2. The problem
Earlier cascades (FrugalGPT; Chen et al., 2023) train a small scorer on the question and the weak model's answer. On multi-step reasoning, the authors found that judging difficulty or correctness from the text alone is unreliable, since errors are subtle even when the reasoning looks plausible.

## 3. Proposed solution
The decision maker uses *answer consistency* of the weaker model as a difficulty signal. Total cost per query is C = C_w + C_d + 1[reject]·C_s: weak-model call, decision overhead, plus the strong model only when rejected (Eq. 1).

Two decision rules:
- **Vote-based:** sample K answers; accept the majority answer if the agreement share s ≥ threshold τ. τ can be tuned to a cost constraint.
- **Verification-based:** take the majority answer from two different prompt settings and accept only if they agree (no threshold needed).

Answers can be sampled from one demonstration set (1D), two sets (2D), or a mixture of thought representations: CoT and PoT (MoT). CoT mistakes tend to repeat across demonstration sets, whereas PoT errs differently, so disagreement across representations separates hard from easy questions better. That gives 10 variants (6 vote, 4 verify).

**Cost model.** Dollar cost from API token prices. Table 1 of the paper writes each variant's weaker-model cost from the input price per token, output price per token, the number of demonstrations M and tokens per demonstration; sample counts are tuned so variants have comparable weak-model cost. The paper counts actual tokens with tiktoken and reports cost *relative to GPT-4 with CoT self-consistency*. It notes GPT-4 output tokens were about 30 times the price of GPT-3.5-turbo at the time (OpenAI pricing page, 2023).

## 4. Data, models and tools
- Six datasets: GSM8k, ASDiv, TabMWP (math), DATE and Navigate (BIG-Bench Hard symbolic), CREPE (causal).
- Weak LLM GPT-3.5-turbo (K = 20 samples), strong LLM GPT-4 with CoT self-consistency (K = 3), temperature 0.4, 8-shot demonstrations. Each approach run twice and averaged. Additional test with Llama-2-13B as the weak model.
- Baselines: fine-tuned RoBERTa-base verifiers (question only, question plus answer) and prompted GPT-3.5 verifiers.
- Code: https://github.com/MurongYue/LLM_MoT_cascade.

## 5. Key results
- Figure 3 (average over six datasets): the four MoT variants reach 0.929 accuracy against 0.931 for GPT-4-CoT-SC at about 40% of its cost.
- CREPE: MoT variants 0.885 vs 0.871 for GPT-4-CoT-SC at 47% of the cost.
- CoT-2D-Vote: 0.924 average accuracy at 57% relative cost. Two demonstration sets beat one by 1.4 points at 0.4 relative cost.
- A useful vote threshold typically falls between 0.5 and 0.6; raising it further wastes cost on hallucinated outliers.
- External verifiers (Section 3.5, Figure 6): on GSM8k the best reached 0.892, versus 0.958 for GPT-4-CoT-SC and 0.951 for the proposed approach.
- With Llama-2-13B as the weak model, the cascade works on DATE but not on GSM8k or CREPE: too weak to be consistent.
- Weak-model hints do not help GPT-4 (they hurt on GSM8k and CREPE).

## 6. Limitations
*Stated by the authors (Appendix K):* applies to tasks with clear, checkable answers; latency rises when the strong model is needed; assumes steps can be expressed in different representations; fails if the weak model is confidently wrong.

*My observations:* the 40% figure is relative to an already expensive GPT-4 self-consistency baseline, so savings against a single GPT-4 call would be smaller. The cascade draws 20 samples per query from the weak model, which is cheap through an API but not free on a loaded self-hosted GPU. The evaluation uses two OpenAI models and 2023 prices, with no concurrency, queueing or load.

## 7. Relevance to the AI Request Router
- Supports a **fallback/escalation path** for tasks with verifiable answers (maths, code, structured output): the router can try the cheap model first and escalate on disagreement.
- The vote threshold τ is a tunable cost-quality knob, similar in role to λ in Dekoninck et al. (2025).
- **Reuse:** consistency as a post-hoc quality signal; relative-cost reporting. **Avoid:** multi-sample cascades for free-form chat, where agreement cannot be scored. **Not covered:** live load, self-hosted models as the strong tier, latency budgets.

## 8. How to use it in the report
Section 2.4 (cascading as cost reduction) and as a contrast to classifier-based routing in 2.3. Synthesis sentence: "Where FrugalGPT (2023) learns a scorer on the answer text, Yue et al. (2024) show that agreement across sampled answers from diverse prompting styles identifies hard reasoning questions better and halves cost at near-GPT-4 accuracy."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Yue et al. (2024) | Cut GPT-4 cost on reasoning without losing accuracy | Two-LLM cascade; vote or verification over answer consistency, sampling CoT and PoT | GSM8k, ASDiv, TabMWP, DATE, Navigate, CREPE; GPT-3.5-turbo and GPT-4 | 0.929 vs 0.931 accuracy at about 40% of GPT-4 self-consistency cost | Verifiable-answer tasks only; many weak-model samples; two API models; no load or latency model |


## 2026-10-31 proposal audit

- Source attempted: https://arxiv.org/abs/2310.03094.
- Scope: Abstract/metadata check only in this session; detailed numerical results remain unchecked.
- Historical Source read above records the earlier session, not a claim of a fresh full reading.
- arXiv title matched: Large Language Model Cascades with Mixture of Thoughts Representations for Cost-efficient Reasoning. Latest listed version: v3; arXiv DOI identifies the preprint, not peer review. A missing journal reference does not prove that no published version exists.
