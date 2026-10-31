# Zooter: reward-guided routing to expert LLMs (Lu et al., 2024)

| Field | Value |
|---|---|
| Topic (home) | 01 Routing algorithms |
| Also relevant to | 02 Capability prediction, 07 Evaluation |
| Paper type | method |
| Venue and status | peer-reviewed (NAACL 2024, long paper) |
| Source read | full text of arXiv v1 (https://arxiv.org/pdf/2311.08692, marked "work in progress"); NAACL camera-ready not read, numbers may differ |
| Verified on | 2026-10-31, against the ACL Anthology (2024.naacl-long.109) |
| Relevance to project | Medium |

## APA 7 reference
Lu, K., Yuan, H., Lin, R., Lin, J., Yuan, Z., Zhou, C., & Zhou, J. (2024). Routing to the expert: Efficient reward-guided ensemble of large language models. In *Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers)* (pp. 1964–1974). Association for Computational Linguistics. https://doi.org/10.18653/v1/2024.naacl-long.109

## In-text citation forms
(Lu et al., 2024) · Lu et al. (2024)

## 1. What it is about
Zooter trains an 86M-parameter router to predict which of six 13B chat models suits a query. It learns from the scores a reward model gives each candidate's answers on a training set, so at run time only the router and one LLM are used. Tag-based smoothing reduces label noise.

## 2. The problem
Reward-model ranking (as in LLM-Blender) needs every model to generate for every query, which is too costly. Earlier routers used benchmark data with gold answers. The authors want a router that needs only queries and works across diverse alignment tasks.

## 3. Proposed solution
**Reward distillation:** candidates answer a diverse training set; a reward model (QwenRM) scores every answer; a softmax over models becomes the soft target, and the router is trained with KL divergence. **Tag-based label enhancement:** reward scores are noisy (Figure 3: high reward entropy goes with lower MT-Bench scores). Queries get instruction tags, rewards are averaged per tag, and the target blends sample and tag rewards, r' = α·r + (1-α)·r_tag. α = 0.3 was best (Table 2); pure tag-level (α = 0) beat pure sample-level (α = 1). At inference the router's top choice answers.

## 4. Data, models and tools
Candidates (LLaMA-based 13B): WizardLM, WizardCoder, WizardMath, Vicuna, OpenChat, Llama-2-Chat. Training set DivInstruct: 47,986 instructions, 6,270 tags, 13 source datasets, decontaminated by 6-gram overlap. Router: mdeberta-v3-base, 8 A100 GPUs. Benchmarks: AlpacaEval, FLASK, MT-Bench (GPT-4 judge), MMLU, GSM8K, HumanEval; 26 subsets. Metrics: mean task rank (MTR, lower is better) and uplift rate. Baselines: reward-model ranking with five reward models and an oracle, plus GPT-3.5-turbo and GPT-4. Code release not stated in the version read.

## 5. Key results (Table 1 of v1)
- MTR 1.94 overall against 2.23 for the best single model (Llama-2-Chat); top on 44% of subsets against 31%.
- MT-Bench: 0.39 points above the best single model (Section 4.2).
- Against reward-model ranking, which runs six 13B models: better than OAssistRM (MTR 3.42) and LLM-Blender (3.39), close to Auto-J (2.25), behind UltraRM (1.53) and QwenRM (1.58).
- Oracle ranking reaches MTR 1.0; GPT-3.5-turbo (1.78) and GPT-4 (1.0) stay ahead of Zooter.
- Reward-model ranking does not help on MMLU, GSM8K and HumanEval, because reward models judge knowledge, maths and code poorly (authors).

## 6. Limitations
**Authors:** paper is marked work in progress; reward models are uncertain on knowledge, maths and code; a gap to the best reward-model ranking remains.
**Mine:** fixed six-model pool, so adding a model means new rewards and retraining; one reward model and GPT-4 judging; all candidates are same-family 13B models, so no dollar cost or latency is measured; modest gains; no load or failover.

## 7. Relevance to the AI Request Router
- Supports the classifier and the *label-noise* risk: reward scores as silver labels and tag-level smoothing.
- Reuse: soft distribution over models as target, the tag prior, MTR and uplift metrics.
- Avoid: one reward model for code or maths prompts.
- Not covered: price-aware choice, live load, cheap addition of models, failure handling.

## 8. How to use it in the report
- Chapter 2 reward-guided routing; chapter 3 label noise.
- "Zooter (Lu et al., 2024) distils reward scores into a light router so one model runs per query, but for a fixed pool of similar 13B models and without price or load."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Lu et al. (2024) | Ensemble LLMs without running all | Reward distillation into 86M router, tag-based smoothing | DivInstruct; six 13B LLMs; AlpacaEval, FLASK, MT-Bench, MMLU, GSM8K, HumanEval | MTR 1.94 vs 2.23 best single; top on 44% of subsets | Fixed pool; noisy rewards; no cost or load |
