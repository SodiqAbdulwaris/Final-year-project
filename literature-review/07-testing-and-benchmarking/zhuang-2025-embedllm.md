# EmbedLLM: compact model embeddings, a correctness dataset and a fast router (Zhuang et al., 2025)

| Field | Value |
|---|---|
| Topic (home) | 07 Testing and benchmarking |
| Also relevant to | 01 Routing algorithms, 02 Prompt difficulty prediction |
| Paper type | method + dataset |
| Venue and status | peer-reviewed (ICLR 2025) |
| Source read | full text (arXiv v2, https://arxiv.org/pdf/2410.02223v2) |
| Verified on | 2026-10-31, against the ICLR 2025 proceedings page and arXiv |
| Relevance to project | Medium |

## APA 7 reference
Zhuang, R., Wu, T., Wen, Z., Li, A., Jiao, J., & Ramchandran, K. (2025). EmbedLLM: Learning compact representations of large language models. *The Thirteenth International Conference on Learning Representations*. https://proceedings.iclr.cc/paper_files/paper/2025/hash/bf5e4b85d203481d6e37bd32d9600162-Abstract-Conference.html

(ICLR papers carry no DOI; the arXiv DOI is https://doi.org/10.48550/arXiv.2410.02223.)

## In-text citation forms
(Zhuang et al., 2025) · Zhuang et al. (2025)

## 1. What it is about
EmbedLLM learns one short vector for each LLM by training on a matrix of right/wrong results (which model answered which question correctly). The model vectors are combined with sentence-transformer question embeddings to predict correctness for new questions, to route queries and to predict benchmark accuracy.

## 2. The problem
Comparing and choosing among hundreds of thousands of models usually means learning a fresh representation of each model for every downstream task, which repeats compute. The authors want a single reusable representation of each model that supports routing, performance forecasting and benchmark analysis without re-running models.

## 3. Proposed solution
A matrix-factorisation-style encoder–decoder. Question text is embedded once with the sentence transformer all-mpnet-base-v2 (768 dimensions) and projected to the model-embedding size. Each model has a learnable vector. The decoder is a linear classifier on the element-wise product of model and question vectors, giving the probability that the model answers correctly, trained with binary cross-entropy to reconstruct the correctness matrix.

Three evaluation tasks: (1) correctness forecasting on unseen questions; (2) routing: score all models for a question and pick the highest, measuring the share of questions where the chosen model is correct; (3) benchmark accuracy prediction: regress a model's accuracy on a held-out benchmark from its embedding, tested with Kendall's tau over 100 random model splits. Probing shows that models with similar characteristics lie close in the embedding space.

## 4. Data, models and tools
- Dataset: 112 open-source models answering 36,054 test questions from MMLU, TruthfulQA, SocialQA, PIQA, MedMCQA, MathQA, LogiQA, GSM8K, GPQA and ASDiv. Binary correctness labels come from lm-evaluation-harness. Split 80/10/10 over questions.
- Baselines: KNN for correctness; single-best-model router and a random router with the same selection frequencies; the causal-LLM router of RouteLLM for speed.
- Code and data: https://github.com/richardzhuang0412/EmbedLLM.

## 5. Key results
- Correctness forecasting (Table 1): matrix factorisation beats KNN at every training size and improves with data; on the full roughly 29K training questions the two rows read about 0.741 versus 0.715 (my reading of the extracted table; the extraction was messy, so check the paper before quoting).
- Routing (Figure 4): the MF router beats both the single-best and random baselines overall and approaches the single-best model per benchmark.
- Speed: 3.80 seconds on average to route 3,000 questions on one A100 80GB GPU, more than 750 selections per second, which the authors compare with under 50 requests per second for the RouteLLM causal-LLM router (15× faster) over 112 candidate models versus 2. Training needs under 1GB of GPU memory.
- Benchmark prediction: significant rank correlation on 7 of the 10 benchmarks (for example 100 of 100 splits on MathQA, LogiQA and MedMCQA, 93 on GSM8K).

## 6. Limitations
Stated by the authors: the dataset is small, with only 112 models so embeddings are moderately sparse; the embeddings depend on a fixed pool, and new models require retraining the factorisation; only correctness-based data are used.

Identified by me: all tasks are multiple-choice or short-answer with exact-match style labels; no cost or latency enters the routing score; "router accuracy" counts a hit if any correct model is chosen regardless of price; the single-best baseline is on the same benchmarks the router trained on; no human preference data.

## 7. Relevance to the AI Request Router
- Closest published design to the planned stack: it uses a sentence-transformer question embedding plus a very small learned head, and shows the whole router is cheap (under 1GB GPU, thousands of routes per second).
- Dataset schema to copy: a model × question binary correctness matrix with a fixed question-embedding table. It is a minimal schema for the classifier's training data.
- Evaluation to copy: single-best and weighted-random baselines, plus per-benchmark breakdown. The weighted random router is a good control for whether the classifier uses model strengths rather than just a selection mix.
- Does not cover: cost, latency, load, quality noise from judges, adding a new backend without retraining (limitation listed by the authors).
- Links to topic 02: the same per-model correctness label used by [Šakota et al. (2024)](../02-prompt-difficulty/sakota-2024-fly-swat-or-cannon.md) and [Routoo](../02-prompt-difficulty/mohammadshahi-2024-routoo.md); [LLMRouterBench](li-2026-llmrouterbench.md) later finds that EmbedLLM is among the top routers and that embedding choice matters little.

## 8. How to use it in the report
- Section 2.7 and the design justification for a sentence-transformer + light classifier.
- Sentence: "EmbedLLM (Zhuang et al., 2025) shows that sentence-transformer question embeddings with a lightweight learned head can route among 112 models at over 750 selections per second, but its pool is fixed and ignores cost."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Zhuang et al. (2025) | Reusable compact LLM embeddings for routing and forecasting | Matrix-factorisation encoder–decoder on model×question correctness; all-mpnet-base-v2 question embeddings | 112 open models × 36,054 questions from 10 benchmarks | Beats KNN and single-best; 3,000 routes in 3.80 s on one A100; predicts 7 of 10 benchmark rankings | Fixed pool, retraining for new models, correctness-only, no cost or latency |
