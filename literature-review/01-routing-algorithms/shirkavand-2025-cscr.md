# CSCR: cost-aware contrastive routing for LLMs (Shirkavand et al., 2025)

| Field | Value |
|---|---|
| Topic (home) | 01 Routing algorithms (added in the discovery search) |
| Also relevant to | 02 Capability prediction, 07 Benchmarks (EmbedLLM, RouterBench) |
| Paper type | method |
| Venue and status | peer-reviewed (NeurIPS 2025) |
| Source read | full text of the NeurIPS proceedings PDF; appendix skimmed |
| Verified on | 2026-10-31, against the NeurIPS 2025 proceedings page and PDF header ("39th Conference on Neural Information Processing Systems") |
| Relevance to project | High |

## APA 7 reference
Shirkavand, R., Gao, S., Yu, P., & Huang, H. (2025). Cost-aware contrastive routing for LLMs. *Advances in Neural Information Processing Systems, 38*. https://proceedings.neurips.cc/paper_files/paper/2025/hash/e46eb6403af68506331f941282d838aa-Abstract-Conference.html. NeurIPS has no DOI; editors, volume and arXiv DOI not checked (the arXiv API was rate-limited).

## In-text citation forms
(Shirkavand et al., 2025) · Shirkavand et al. (2025)

## 1. What it is about
Cost-Spectrum Contrastive Routing (CSCR) embeds prompts and candidate LLMs in one vector space so that routing becomes a single nearest-neighbour lookup. The training loss itself favours the cheapest model that is still accurate, rather than applying cost only at test time. New models can be added without retraining.

## 2. The problem
The authors say existing routers ignore prompt context, need costly model profiling, assume a fixed pool, or learn by trial and error. Softmax classifiers optimise top-1 accuracy with no cost term and default to expensive models; non-parametric and bandit methods are cost-agnostic in training and rebuild footprints when the pool changes.

## 3. Proposed solution
- **Expert descriptors:** a *logit footprint* (average next-token probabilities over about 192 probe prompts, fewer than 10 forward passes) for open-weight models, and a *perplexity fingerprint* (a small GPT-2 scoring each API's answers) for black-box APIs. Both live on the unit sphere, so open and API models can be mixed.
- **Router:** a frozen sentence encoder (all-MiniLM-L6-v2) plus a two-layer MLP maps the prompt into the descriptor space.
- **Cost-Spectrum InfoNCE:** positives are chosen within K = 5 adaptive cost bands, each band has its own temperature, and negatives are down-weighted by cost. This stops the router collapsing onto the cheapest models that happen to be right on easy prompts.
- **Inference:** a FAISS k-NN lookup returns the most cost-effective experts; a routing penalty λ traces a deferral curve.

## 4. Data, models and tools
Datasets: EmbedLLM, MixInstruct, RouterBench. Cost is parameter count for EmbedLLM and MixInstruct (a proxy for compute and latency) and actual USD API cost for RouterBench. Metrics: area under the deferral curve (AUDC), peak accuracy and query-normalised cost (QNC). Baselines: UMR, Thompson sampling, Pareto-random, softmax and Soft-MoE gating, random, oracle. Code release not confirmed in the text read.

## 5. Key results
- Abstract: up to 25% better accuracy-cost trade-off, robust to unseen LLMs and out-of-distribution prompts, microsecond routing latency.
- Table 1, AUDC: EmbedLLM 0.541 (UMR 0.515); RouterBench 0.7110 (parametric 0.691, Thompson 0.622, UMR 0.568); MixInstruct 0.051 (UMR 0.049, oracle 0.079).
- Out-of-distribution prompts (STEM held out, Table 3): AUDC 0.5146 against 0.4863 for the next-best baseline (Section 4.2.2).
- New LLMs unseen at training (Table 2): reported more robust than baselines; I did not verify the cells because the table text was garbled in extraction.
- Ablations (Section 4.3): cost-aware training lifts EmbedLLM AUDC from 0.342 to 0.495 and peak accuracy from about 36% to 54% over plain InfoNCE, at a higher QNC (Table 5); perplexity descriptors lift MixInstruct AUDC only slightly (0.0461 to 0.0467) and need at least 2x more time (Table 4).

## 6. Limitations
**Authors:** very large model pools were not tested because of resources; difficulty awareness as a function of router size is left open.
**Mine:** cost is parameter count or API price, never live load or queue state; quality is correctness on benchmark tasks; descriptor probes must be recomputed when a model is fine-tuned or updated; latency stated "microsecond" refers to the lookup only; no failover.

## 7. Relevance to the AI Request Router
- Directly matches the planned stack: sentence-transformers embeddings, a lightweight learned head and a FAISS or k-NN lookup.
- Supports the scoring function: cost enters training, not just a test-time threshold; and the "add a model without retraining" requirement.
- Reuse: cost-banded contrastive loss, perplexity fingerprints for black-box APIs, AUDC/QNC metrics.
- Not covered: live load, latency budgets, failover, self-hosted serving signals.

## 8. How to use it in the report
- Chapter 2 embedding-based routing and generalisation to new models; chapter 3 router design.
- "Shirkavand et al. (2025) put cost inside the contrastive training objective and route by nearest-neighbour search, yet cost remains a static property of each model."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Shirkavand et al. (2025) | Cost-aware routing over dynamic model pools | Contrastive router, cost-banded InfoNCE, logit and perplexity fingerprints, FAISS k-NN | EmbedLLM, MixInstruct, RouterBench | Highest AUDC on all three; robust to unseen models and OOD prompts | Static cost; no live load or failover |
