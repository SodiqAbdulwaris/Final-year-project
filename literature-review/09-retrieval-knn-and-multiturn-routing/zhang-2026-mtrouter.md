Status: DRAFT
Depends on: D08; D12
Sources: Primary URLs in source table and proposal-audit section
Open items: Scoped numerical/final-version checks recorded below

# MTRouter: cost-aware turn-level routing with history–model embeddings (Zhang et al., 2026)

| Field | Value |
|---|---|
| Topic (home) | 09 Retrieval, k-NN and multi-turn routing |
| Also relevant to | 01 Routing algorithms, 04 Cost reduction |
| Paper type | method |
| Venue and status | peer-reviewed (ACL 2026 long paper, pp. 44206–44226) |
| Source read | full text (arXiv v1, https://arxiv.org/pdf/2604.23530v1); the ACL camera-ready may differ |
| Verified on | 2026-10-31, against the ACL Anthology entry 2026.acl-long.2045 and arXiv |
| Relevance to project | High |

## APA 7 reference
Zhang, Y., Li, H., Wang, Z., Feng, S., Yang, X., Wang, D., Zhang, B., Bai, L., & Hu, S. (2026). MTRouter: Cost-aware multi-turn LLM routing with history–model joint embeddings. In *Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)* (pp. 44206–44226). Association for Computational Linguistics. https://doi.org/10.18653/v1/2026.acl-long.2045

## In-text citation forms
(Zhang et al., 2026) · Zhang et al. (2026)

## 1. What it is about
MTRouter chooses which model to call at each turn of a long, tool-using agent episode, under a fixed cost budget. A small network predicts the final outcome of the episode for each candidate model given the interaction history so far, and the router picks the highest predicted outcome.

## 2. The problem
Single-turn routers pick one model at the start of an episode and keep it, but different steps of an episode vary from planning to routine tool calls, so one fixed model is wasteful or risky. Turn-level routing is harder because a choice now affects an outcome dozens of steps later. Earlier multi-turn work (Router-R1) uses a heavy LLM as the router and switches aggressively after errors.

## 3. Proposed solution
- **History encoding.** The task, past actions and observations are serialised into a fixed template, truncated to 8,192 tokens (oldest context dropped first, task block kept) and encoded by a frozen text encoder.
- **Model encoding.** Each model has an embedding built from structured attributes (context limit, knowledge cut-off, pricing) plus a learned residual that captures behaviour not explained by metadata.
- **Outcome estimator.** An MLP maps the concatenated history and model embeddings to the expected terminal score. The training target is the episode's final score minus a cumulative, severity-weighted error penalty (invalid actions, format violations), with later errors penalised more heavily.
- **Inference.** At each turn, take the model with the highest predicted outcome; the episode stops at the cost budget or turn limit. There is no explicit switching penalty.
- **Training data.** Offline trajectories from a random router (wide coverage) plus single-model runs (anchoring each model's behaviour): 1,291 training instances, 29,693 trajectories, 515,221 turns, at an estimated one-time collection cost of about $1,620.

## 4. Data, models and tools
- Benchmarks: ScienceWorld and Humanity's Last Exam (HLE), with held-out and out-of-distribution test sets; per-episode cost cap of $2.0 for HLE. Each run repeated three times, with ± intervals reported.
- A fixed pool of six models (GPT-5, DeepSeek, MiniMax, Kimi, Gemini, GPT-OSS).
- Baselines: single models, Router-R1, and OpenRouter's routing API, which cannot be given a custom pool and so selects from a much larger one.
- Code: https://github.com/ZhangYiqun018/MTRouter.

## 5. Key results
- ScienceWorld: average score 53.8 versus 48.4 for GPT-5, with total cost reduced by 58.7% (Table 3).
- HLE: competitive accuracy with a 43.4% cost reduction against GPT-5; gains carry over to out-of-distribution tasks.
- Ablations (Table 4, full model 53.8 ± 3.2 on ScienceWorld and 26.0 ± 2.3 on HLE): ridge regression instead of an MLP 49.1 and 23.4; no random-router data 47.2 and 22.6; no error penalties 48.5 and 23.8; no routing history 44.6 and 21.3; a hardcoded model encoder 41.3 and 19.7.
- Switching behaviour (Section 4.3): after an error, MTRouter stays with the same model 90.2% of the time on ScienceWorld and 80.9% on HLE, versus 38.3% and 66.4% for Router-R1, yet recovers more often on the next turn. Model use is structured over time (for example GPT-5 provides 50.8% of early ScienceWorld turns while GPT-OSS rises to 24.3% in the final turns).

## 6. Limitations
Stated by the authors: collecting diverse long trajectories across candidate models is costly, which limited the horizon and benchmark coverage; the other limitation items I read concern scalability of data collection.

Identified by me: the paper only notes, without measuring, that switching models loses prompt or KV-cache reuse and forces the new model to re-process the whole prefix, raising latency and per-turn cost; the router has no explicit switching cost or hysteresis, it simply happens to switch less than Router-R1. Cost is token usage times price, with no cache-hit pricing. The tasks are agentic (ScienceWorld, HLE), not chat sessions, and the pool is six frontier or near-frontier models. The estimator needs expensive logged trajectories, unlike a k-NN lookup over scored tasks.

## 7. Relevance to the AI Request Router
- The nearest published treatment of the guide's RQ2 (does controlled switching save cost without material quality loss). It shows that "switch less, but selectively" can beat reactive switching, and it names the cache and prefix-reprocessing penalty as the reason to be wary of frequent switches.
- Reuse: evaluate with repeated runs and intervals; compare against a "switch after each error" reactive baseline; report stay-versus-switch rates after errors; use a random-router plus single-model data mix to cover the pool when logging data.
- What the project must decide, and this paper does not answer: hysteresis thresholds (how much better the new model's estimate must be, and for how many turns), a cache-aware cost term for switching, and hard-failure exceptions that override stickiness.
- Not covered: k-NN or retrieval of past outcomes, calibration, minimum evidence, local models, live load.
- Related: prefix-sharing in serving is studied in [Preble (Srivatsa et al., 2025)](../03-load-balancing/srivatsa-2025-preble.md); the cache-loss effect of switching is quantified in [Parashar et al. (2026)](parashar-2026-whose-turn-is-it.md).

## 8. How to use it in the report
- Chapter 2 on multi-turn and session routing, and the motivation for session-aware hysteresis in Chapter 3.
- Sentence: "Zhang et al. (2026) show that a turn-level router that switches models less often after errors reaches better score at lower cost than a reactive router, but they leave the prompt-cache cost of switching unmeasured."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Zhang et al. (2026) | Cost-aware model choice at each turn of agent episodes | History–model joint embeddings; MLP outcome estimator trained on logged trajectories | ScienceWorld, HLE; six-model pool; Router-R1, OpenRouter baselines | 53.8 vs 48.4 (GPT-5) at 58.7% lower cost on ScienceWorld; 43.4% cost cut on HLE; stays with same model 90.2% after error | Cache loss on switching not measured, no hysteresis rule, agent tasks, costly trajectory logging |


## 2026-10-31 proposal audit

- Source attempted: https://arxiv.org/abs/2604.23530.
- Scope: Full-text sample: method and selected numerical/limitation statements checked; see L07.
- Historical Source read above records the earlier session, not a claim of a fresh full reading.
- arXiv title matched: MTRouter: Cost-Aware Multi-Turn LLM Routing with History-Model Joint Embeddings. Latest listed version: v1; arXiv DOI identifies the preprint, not peer review. A missing journal reference does not prove that no published version exists.
