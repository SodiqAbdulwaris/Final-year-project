Status: DRAFT
Depends on: D08; D12
Sources: Primary URLs in source table and proposal-audit section
Open items: Scoped numerical/final-version checks recorded below

# Routoo: predicting each model's correctness per prompt (Mohammadshahi et al., 2024)

| Field | Value |
|---|---|
| Topic (home) | 02 Prompt difficulty prediction |
| Also relevant to | 01 Routing algorithms, 04 Cost reduction |
| Paper type | method / system |
| Venue and status | preprint only (arXiv v1 Jan 2024, v3 Oct 2024); no peer-reviewed venue found on arXiv or by web search |
| Source read | full text (https://arxiv.org/pdf/2401.13979v3) |
| Verified on | 2026-10-31, against arXiv abstract page and PDF |
| Relevance to project | High |

## APA 7 reference
Mohammadshahi, A., Shaikh, A. R., & Yazdani, M. (2024). *Routoo: Learning to route to large language models effectively* (arXiv:2401.13979). arXiv. https://doi.org/10.48550/arXiv.2401.13979

## In-text citation forms
(Mohammadshahi et al., 2024) · Mohammadshahi et al. (2024)

## 1. What it is about
Routoo is an architecture that decides, before any model runs, which LLM from a pool should answer a prompt. A learned performance predictor estimates whether each candidate model will answer correctly, and a cost-aware selector then picks a model within a budget. It is evaluated on MMLU with open-source models and with GPT-4 added to the pool.

## 2. The problem
Bigger LLMs answer better but cost more, while many prompts can be handled by smaller models. Earlier selection work either ran several models and picked an output (ensembling, reranking, cascades) or handled only a strong/weak pair. The authors want to pick among many models without executing them and with explicit control over the cost–quality trade-off.

## 3. Proposed solution
Routoo has three parts (Figure 1 of the paper).

- **Performance predictor.** A decoder-only LLM encodes the prompt and the last-token embedding is taken as the prompt representation. Each candidate model has its own learned embedding. The predictor subtracts the model embedding from the prompt embedding and passes the result through a linear layer that outputs a correctness level (0 to K−1; K = 2 on MMLU, so correct/incorrect). It is trained with cross-entropy over all (model, prompt) pairs.
- **Cost-aware selector.** The problem is posed as maximising total predicted correctness under a total budget B. A greedy rule scores each model by predicted correctness divided by its cost (with an exponent that controls how strongly cost is emphasised), sorts models per prompt, and assigns the best one that still fits the budget. Costs are the average cost per model, not per-request cost.
- **Universe constructor.** From a large pool of models it greedily picks a small complementary subset (the objective is the mean of the per-prompt best score in the subset), because only a limited number of models can be served.

## 4. Data, models and tools
- Pool: top 1,000 models of the Open LLM Leaderboard fed to the universe constructor, with 56 models used for routing; "open-source" variant uses 7B, 13B and 34B models, and "mix" adds GPT-4.
- Query encoder: Mistral 7B v0.1 fine-tuned with LoRA (r = 1024).
- Training data (about 75,000 prompts): 55,645 prompts from ARC, MC-TEST, OBQA, RACE and TruthfulQA (45,645 on which SOLAR-10.7B scored 0, plus 10,000 random easier ones) and 20,000 prompts generated with GPT-4. Labels come from whether each model answers correctly, so no human difficulty annotation is needed.
- Evaluation: MMLU (57 domains) with the Eleuther harness. Baselines are LLaMA-2 7B/13B/70B, Mistral 7B, Mixtral 8x7B, GPT-3.5 and GPT-4. No public router baseline was found by the authors.
- Code: models announced as to be released; I did not verify a repository.

## 5. Key results
- Routoo (open-source) reaches 75.87% on MMLU at about $0.6 per million tokens, against Mixtral 8x7B at 70.6% for the same $0.6 (Table 1), a gain of 5.27 points at equal cost. It matches Mixtral's accuracy at roughly 33% lower cost (Figure 2).
- It beats LLaMA-2 70B by about 6 points at 33% lower cost and is competitive with GPT-3.5 at 73.3% lower cost.
- Routoo (mix) scores 84.9% at $10.2 versus GPT-4 at 86.4% and $20 (Table 1), nearly half the cost. At a different budget it reaches 86.64% versus GPT-4's 86.40% with about 25% lower cost (Figure 2).
- The authors state that choosing the best open-source model per MMLU question would give 97.5% accuracy (an oracle upper bound, Appendix A).

## 6. Limitations
Stated by the authors: none discussed in a dedicated section that I could find.

Identified by me:
- Single benchmark (MMLU, multiple choice, likelihood-scored), so the claim that it generalises to open-ended generation is untested. Training data is synthetic because MMLU has no training split.
- The predictor is a 7B LLM, so prediction itself is not cheap or fast, and its latency is not reported.
- Cost is an average per model; there is no latency measurement and no live load or queueing signal.
- Costs are API list prices at writing time and will drift.
- Preprint, not peer reviewed.

## 7. Relevance to the AI Request Router
- Directly supports the scoring function: predicted quality per model, combined with cost under a budget, then a per-prompt choice among many models rather than a weak/strong pair.
- Reuse: the "prompt embedding minus model embedding" predictor, correctness labels obtained by running models on training prompts, and the greedy selector with a cost-emphasis parameter.
- Avoid: using a 7B encoder in the request path. The project plans sentence-transformers plus scikit-learn, which is much cheaper; Routoo gives no evidence on whether that is enough.
- Not covered: live load, latency budgets, self-hosted serving state, failover.

## 8. How to use it in the report
- Section on per-prompt performance prediction (2.4) and the scoring-function design (Chapter 3).
- Sentence: "Unlike binary strong/weak routers (Ding et al., 2024), Routoo (Mohammadshahi et al., 2024) predicts correctness for every model in a pool and selects under a budget, but it ignores latency and live load."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Mohammadshahi et al. (2024) | Pick the cheapest adequate LLM per prompt from a large pool without running it | LLM-based correctness predictor + greedy cost-aware selector + universe constructor | MMLU; Mistral 7B encoder (LoRA); about 75k training prompts; LLaMA-2, Mixtral, GPT-3.5/4 baselines | 75.87% vs Mixtral 70.6% at equal cost; near GPT-4 accuracy at about half the cost | One benchmark, heavy predictor, average (not live) cost, no latency or load, preprint |


## 2026-10-31 proposal audit

- Source attempted: https://arxiv.org/abs/2401.13979.
- Scope: Abstract/metadata check only in this session; detailed numerical results remain unchecked.
- Historical Source read above records the earlier session, not a claim of a fresh full reading.
- arXiv title matched: Routoo: Learning to Route to Large Language Models Effectively. Latest listed version: v3; arXiv DOI identifies the preprint, not peer review. A missing journal reference does not prove that no published version exists.
