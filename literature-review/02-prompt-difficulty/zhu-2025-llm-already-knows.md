# The LLM already knows: difficulty from hidden states (Zhu et al., 2025)

| Field | Value |
|---|---|
| Topic (home) | 02 Prompt difficulty prediction |
| Also relevant to | 04 Cost reduction (adaptive inference) |
| Paper type | method |
| Venue and status | peer-reviewed (EMNLP 2025 main conference, pp. 1160–1176) |
| Source read | full text (arXiv HTML v1, https://arxiv.org/html/2509.12886v1); the EMNLP camera-ready may differ slightly |
| Verified on | 2026-10-31, against ACL Anthology (2025.emnlp-main.61) and arXiv |
| Relevance to project | Medium |

## APA 7 reference
Zhu, Y., Liu, D., Lin, Z., Tong, W., Zhong, S., & Shao, J. (2025). The LLM already knows: Estimating LLM-perceived question difficulty via hidden representations. In *Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing* (pp. 1160–1176). Association for Computational Linguistics. https://doi.org/10.18653/v1/2025.emnlp-main.61

## In-text citation forms
(Zhu et al., 2025) · Zhu et al. (2025)

## 1. What it is about
The paper estimates how hard a question is for a specific LLM using only that model's hidden state after reading the question, with no tokens generated. The difficulty estimate then decides how much repeated sampling (self-consistency, best-of-N, self-refine) to spend per question.

## 2. The problem
Difficulty-aware inference needs a per-question difficulty signal. Existing signals either need repeated sampling (answer consistency), an auxiliary judge LLM, or fine-tuning the target model. The authors argue these are costly, can miss what the *target* model finds hard, or can damage the model's general abilities.

## 3. Proposed solution
Generation is modelled as a Markov chain whose state is the sequence of hidden representations plus generated tokens. A reward is given only at the end-of-sequence token (an outcome score for the final answer), and a value function V(s) gives the expected final reward from a state. Difficulty is defined as V(s0) at the initial state, which depends only on the question; the question is "difficult" if V(s0) is below a threshold τ chosen on a validation split.

The value function is a small two-layer fully connected network on the last-layer hidden state, trained with a temporal-difference loss (squared TD error over the sampled responses). Training data is the target model's own sampled responses scored by reward. For the application, difficult questions receive the expensive strategy (K sampled paths, N candidates or refinement rounds) while easy questions get a single sample.

## 4. Data, models and tools
- Datasets: MMBench, ScienceQA, MathVista (multimodal) and StrategyQA, GSM8K, CommonsenseQA (text); random 50/45/5 train/test/validation splits for MMBench and MathVista, official splits for ScienceQA and CommonsenseQA.
- Models: Qwen2.5-VL-7B-Instruct and InternVL3-8B; scaling tests on Qwen2.5-VL 3B/7B/32B/72B; a cross-model test on Qwen2.5-7B-Instruct and LLaMA-3.1-8B-Instruct.
- Ground truth: a question is easy if the model answers correctly in all three independent attempts, otherwise hard. This needs no human difficulty labels.
- Baselines: self-prompting, answer-consistency (AG), auxiliary-LLM ranking, and two fine-tuned HaluSearch variants.
- Metrics: ROC-AUC and macro-F1 for difficulty, accuracy and total output tokens for adaptive sampling. One A100 GPU, temperature 0.5. I did not find a code link in the text.

## 5. Key results
- Difficulty estimation (Table 1): on ScienceQA the method reaches ROC-AUC 93.09% and macro-F1 79.48%, and the text says it beats all baselines on nearly every metric. Note: Table 4 (model-size study, same ScienceQA setup) prints 93.04 and 79.48, an inconsistency in the paper; 93.09 is kept here as given in the text and Table 1.
- Adaptive sampling (Figures 3–4, budgets K = 10 for SC/BoN and 5 for SR): highest accuracy at fewer or comparable output tokens. Exact token savings are only shown in figures, so I do not quote them.
- Training time (Table 6): about 1.56 and 1.85 minutes (MMBench, ScienceQA), against 5.32/5.20 for HaluSearch-Gen and 10.23/9.15 for HaluSearch-Critic.
- Cross-model transfer (Table 5): a probe trained on Qwen2.5-7B-Instruct and tested on LLaMA-3.1-8B-Instruct gives ROC-AUC 47.29 (CommonsenseQA) and 49.74 (StrategyQA), close to chance, so one value function per target model is needed.
- Cross-dataset transfer (Table 3) is reported as "strong" but I did not extract figures.

## 6. Limitations
Stated by the authors: needs token-level hidden states, which closed-source APIs do not expose; single-turn inputs only; generalisation to unseen domains and tasks is future work.

Identified by me: difficulty is model-specific (labels depend on one model and three rollouts), so the probe must be retrained per model, as the near-chance transfer result shows. Models are mostly 7–8B (Qwen2.5-VL-7B, InternVL3-8B), with a scaling test on Qwen2.5-VL 3B, 7B, 32B and 72B (Table 4) and tasks that are multiple-choice or short-answer, so open-ended chat prompts are mostly untested (a Section 6.1 open-ended test exists but I did not extract its numbers). No serving-cost or latency measurement under load: the paper reports training time (Table 6) and, in Figure 2 only, a test-time comparison of estimation time over 400 questions per dataset on Qwen2.5-VL-7B-Instruct, whose values I did not extract.

## 7. Relevance to the AI Request Router
- Supports the difficulty classifier and the label-noise/generalisation risk: it shows that a small probe can predict "will this model fail" and that probes do not transfer across models.
- Reuse: label rule (all-correct over several rollouts = easy), threshold chosen on a validation split, AUC/F1 evaluation.
- Avoid: requiring the target model's hidden states. In the router, a hosted backend cannot expose them and running a 7B model first adds cost; a small proxy encoder would be the practical substitute, but this paper does not test that.
- Not covered: multi-model choice, cost, latency, live load.

## 8. How to use it in the report
- Section 2.4 theme "internal-state probes versus external embeddings" and the generalisation-risk discussion.
- Sentence: "Zhu et al. (2025) estimate difficulty from the target model's own hidden state, but the probe failed to transfer between models, which supports training a per-backend predictor."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Zhu et al. (2025) | Estimate LLM-perceived question difficulty without generating tokens | Value function on initial hidden state, trained by TD learning; drives adaptive SC/BoN/SR | MMBench, ScienceQA, MathVista, GSM8K and others; Qwen2.5-VL, InternVL3 | ROC-AUC 93.09 on ScienceQA; fewer tokens at higher accuracy; near-chance cross-model transfer | Needs hidden states, per-model training, single-turn, no cost or load |
