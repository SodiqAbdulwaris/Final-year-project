Status: DRAFT
Depends on: D08; D12
Sources: Primary URLs in source table and proposal-audit section
Open items: Scoped numerical/final-version checks recorded below

# FamiCom: familiarity and complexity for label-free performance estimation (Li et al., 2024)

| Field | Value |
|---|---|
| Topic (home) | 02 Prompt difficulty prediction |
| Also relevant to | none strong; background for prompt-level performance prediction |
| Paper type | method / empirical study |
| Venue and status | preprint only (arXiv v1, June 2024); no peer-reviewed venue found on the arXiv page or by web search |
| Source read | full text (https://arxiv.org/pdf/2406.11243v1) |
| Verified on | 2026-10-31, against arXiv abstract page and PDF |
| Relevance to project | Low |

## APA 7 reference
Li, B., Zhou, B., Fu, X., Wang, F., Roth, D., & Chen, M. (2024). *FamiCom: Further demystifying prompts for language models with task-agnostic performance estimation* (arXiv:2406.11243). arXiv. https://doi.org/10.48550/arXiv.2406.11243

## In-text citation forms
(Li et al., 2024) · Li et al. (2024)

## 1. What it is about
FamiCom is a score computed from a prompt alone, with no labels, that predicts how well a language model will do on it. It multiplies how *familiar* the prompt is to the model (perplexity and key-word similarity) by an inverse measure of how *complex* the underlying task is (the estimated number of reasoning steps). It is applied to choosing prompts and in-context examples.

## 2. The problem
Earlier work found that prompts with lower perplexity, which the model finds more familiar, tend to perform better. The authors show this link weakens for tasks that need more reasoning steps and across tasks or domains. Familiarity alone therefore cannot say whether a given question will be answered correctly.

## 3. Proposed solution
FamiCom has two factors.

- **Complexity.** Approximated by the number of steps needed to solve the problem, obtained in three ways: asking the model "how many steps does it take" (direct), the same with human-written step examples (guided), or counting operations in a RASP-L program (operational, which does not scale because each prompt needs its own program). The guided version worked best.
- **Familiarity.** Two variants: prompt perplexity, and the mutual similarity among the "key" tokens (the top-K highest-perplexity tokens, K = 20 in the reported run).

The final score uses familiarity times inverse complexity (coefficients fixed to f¹ · c⁻¹ after a hyper-parameter search). For applications, FamiCom ranks candidate instructions or retrieves demonstrations from other tasks ("indirect in-context learning") instead of using nearest-neighbour similarity.

## 4. Data, models and tools
- Validation: 28 multiple-choice tasks sampled from MMLU, BIG-Bench, StrategyQA and CommonsenseQA, each paired with three random chain-of-thought demonstrations from Chain-of-Thought Hub; majority vote over five runs; temperature 0.8.
- Models: Phi-3-mini-128k, Mistral-7B-Instruct-v0.2 and Llama-2-13b-chat, tested on 8 NVIDIA RTX 6000 Ada GPUs. The correlation validation used only Mistral-7B.
- Baselines: perplexity ranking, SPELL, k-nearest-neighbour retrieval. No code link found in the paper text.

## 5. Key results
- Spearman correlation with accuracy (Table 1): familiarity 0.426, complexity 0.695, FamiCom 0.848, which matches the abstract's 0.85 versus 0.43.
- Prompt selection (Table 2): FamiCom improves Mistral-7B accuracy by 4.6% on average across tasks, versus 3.3% for SPELL, and is best on most tasks except CoLA.
- Indirect in-context learning (Table 3): FamiCom beats nearest-neighbour retrieval on the tasks shown. The abstract claims gains of more than 7.0% over existing methods; I did not reconstruct that figure from the tables.

## 6. Limitations
Stated by the authors: the validation was run only on Mistral-7B because of data volume; the indirect in-context-learning study is a small pilot with a limited range of demonstrations and tasks.

Identified by me: all experiments are multiple choice; the score needs token perplexities, so it cannot be applied to closed API models (the authors say so for complexity prompting cost); complexity comes from the model's own step-count guess, which is noisy and costs an LLM call; the unit of analysis is a (task, demonstration) setup rather than an individual user prompt; no cost, latency or routing evaluation.

## 7. Relevance to the AI Request Router
- Mostly background. It supports the idea that "how hard the task is" and "how familiar the model is with it" are two separate signals, and that predicted performance can be measured without labels.
- Possible cheap analogues for the classifier: prompt length, number of requested steps or sub-questions as complexity features, and embedding-based similarity to known solved prompts as a familiarity feature.
- Avoid: perplexity-based features that need the target model's logits at routing time.
- Not covered: routing, multiple models, cost, load.

## 8. How to use it in the report
- Section 2.4, in the paragraph on separating "complexity" from "familiarity" when engineering difficulty features.
- Sentence: "Li et al. (2024) showed that familiarity (perplexity) alone fails to predict accuracy on reasoning-heavy tasks and added an estimate of task complexity, reaching a 0.85 Spearman correlation with accuracy on multiple-choice tasks."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Li et al. (2024) | Label-free estimate of prompt-level LLM performance | Familiarity (perplexity, key-token similarity) combined with LLM-estimated complexity | 28 MC tasks from MMLU/BIG-Bench/etc.; Mistral-7B, Phi-3-mini, Llama-2-13b | Spearman 0.848 vs 0.426 familiarity-only; +4.6% prompt-selection accuracy | Preprint, MC tasks, needs logits, not a routing study |


## 2026-10-31 proposal audit

- Source attempted: https://arxiv.org/abs/2406.11243.
- Scope: Abstract/metadata check only in this session; detailed numerical results remain unchecked.
- Historical Source read above records the earlier session, not a claim of a fresh full reading.
- arXiv title matched: FamiCom: Further Demystifying Prompts for Language Models with Task-Agnostic Performance Estimation. Latest listed version: v1; arXiv DOI identifies the preprint, not peer review. A missing journal reference does not prove that no published version exists.
