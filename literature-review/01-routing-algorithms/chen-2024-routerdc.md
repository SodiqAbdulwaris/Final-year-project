# RouterDC: dual contrastive learning for query-based routing (Chen et al., 2024)

| Field | Value |
|---|---|
| Topic (home) | 01 Routing algorithms |
| Also relevant to | 06 Fallback (robustness to losing a model), 07 Benchmarks |
| Paper type | method |
| Venue and status | peer-reviewed (NeurIPS 2024, poster) |
| Source read | full text of arXiv v1 (https://arxiv.org/pdf/2409.19886); camera-ready not read separately, numbers from v1 |
| Verified on | 2026-10-31, against the NeurIPS 2024 proceedings page and arXiv ("Accepted by NeurIPS 2024") |
| Relevance to project | High |

## APA 7 reference
Chen, S., Jiang, W., Lin, B., Kwok, J. T., & Zhang, Y. (2024). RouterDC: Query-based router by dual contrastive learning for assembling large language models. In A. Globerson, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. Tomczak, & C. Zhang (Eds.), *Advances in Neural Information Processing Systems* (Vol. 37). Curran Associates. https://proceedings.neurips.cc/paper_files/paper/2024/hash/7a641b8ec86162fc875fb9f6456a542f-Abstract-Conference.html (preprint: https://doi.org/10.48550/arXiv.2409.19886). No DOI; editor list not checked against the front matter.

## In-text citation forms
(Chen et al., 2024) · Chen et al. (2024)

## 1. What it is about
Each candidate LLM gets a learnable vector and each query an embedding from a small encoder; the query goes to the LLM with the most similar vector. Two contrastive losses train the router to treat several good LLMs as equally acceptable.

## 2. The problem
Zooter matches the score distribution with a KL loss. The authors show (Figures 3 and 4) that top models often score almost equally, so softmax targets become nearly uniform and weak. A router trained only on "which LLM is best" is also unstable because similar queries may get dissimilar embeddings.

## 3. Proposed solution
mDeBERTa-v3-base (86M) encodes the query; routing probability is a softmax over cosine similarities to 768-dimensional LLM embeddings; inference picks the arg max, LLMs stay frozen. An LLM's training score is accuracy over 10 samples (open-ended tasks) or normalised option probability (multiple choice). The **sample-LLM loss** pulls the query towards the top K+ = 3 LLMs and away from the bottom K- = 3 with score below 0.5. The **sample-sample loss** clusters training queries (t-SNE, then k-means, N = 5) and pulls same-cluster queries together, stabilising training. Combined with weight 1.

## 4. Data, models and tools
Seven 7B/8B LLMs (Mistral-7B, MetaMath-Mistral, zephyr, Chinese-Mistral, two dolphin models, Llama-3-8B). In-distribution: MMLU, GSM8K, CMMLU, ARC-C, HumanEval; out-of-distribution: PreAlgebra, MBPP, C-EVAL. Baselines: single LLMs, Voting, CosineClassifier, Zooter, LoraRetriever. 1,000 steps, A100. Code: https://github.com/shuhao02/RouterDC (stated in the paper).

## 5. Key results
- In-distribution (Table 1): average 58.54% against 54.56% for the best single LLM (+3.98 points); Zooter 53.97%, CosineClassifier 54.22%, LoraRetriever 55.77%, Voting 54.37%.
- Out-of-distribution (Table 2): 45.85% against 43.95% (+1.90 points); per task roughly equal to the best single model.
- Inference time 7.97 minutes against 46.59 for Voting (about 6x faster); router training 28.3 minutes.
- Robustness (Table 3): removing one candidate LLM at inference, without retraining, leaves the average between 57.40 and 58.66 (58.54 with all).
- Ablation (Figure 8): K+ = 1 performs worst, supporting multiple positives.
- The abstract's "+2.76%" in-distribution does not match the 3.98-point table gap (it is near the +2.77 over LoraRetriever); I use table values.

## 6. Limitations
**Authors:** only small 7B/8B candidates because of compute; extension to chat context left for future work.
**Mine:** accuracy-only objective with no price differences between models; fixed model set (new model, new training); small gains outside training tasks; no variance reported; no latency, queue or load signal.

## 7. Relevance to the AI Request Router
- Supports the embedding-based router and the "several models are good enough" case, where cost or load can break ties.
- Reuse: top-K positives instead of one label; clustering for stability; Table 3 as evidence a router can survive a backend disappearing.
- Avoid: fixed model set; quality-only objective.
- Not covered: cost-aware choice, live load, request-time failures such as timeouts.

## 8. How to use it in the report
- Chapter 2 embedding and contrastive routing; chapter 3 "multiple acceptable models" labels.
- "RouterDC (Chen et al., 2024) replaces Zooter's score matching with contrastive training on several top models, but optimises accuracy over a fixed pool with no cost or load term."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Chen et al. (2024) | Route queries among several good LLMs | Encoder plus learnable LLM embeddings; two contrastive losses | MMLU, GSM8K, CMMLU, ARC-C, HumanEval; OOD PreAlgebra, MBPP, C-EVAL; seven 7-8B LLMs | 58.54% vs 54.56% best single; +1.90 OOD; about 6x faster than voting | Small models; accuracy only; fixed pool; no cost or load |
