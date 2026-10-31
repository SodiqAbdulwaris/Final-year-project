# D04: How to word the research gap and the novelty claim

| | |
|---|---|
| Status | **OPEN, needs your decision** |
| Who decides | You and the supervisor |
| Blocks | Proposal section 2, Chapter 1.2, Chapter 2.7, abstract |
| Default used meanwhile | Reworded gap from `literature-review/gaps-and-synthesis.md` section 2 |

## The question
The proposal says no existing tool picks the model per prompt, watches live load, and runs on your own GPUs. That is no longer safe. What can you claim?

## What I found
- vLLM Semantic Router (open source; arXiv 2603.04444): per-prompt selection, self-hosted vLLM, runtime TPOT/TTFT-based selection, weighted failover. It does not document a per-request latency budget mechanism (checked against the preprint text).
- RouteBalance (arXiv preprint, 2026): per-request model-instance choice with vLLM queue/KV signals and a quality-latency-cost score. One model family, one cluster, no hosted backends, no failover beyond losing a tier.
- OpenRouter now has an Auto Router that picks a model per prompt; LiteLLM Auto Router v2 (13 Jul 2026) routes by complexity tier; Not Diamond sells per-prompt selection (closed, hosted, no documented failover/load).
- Competitor claims the proposal made about OpenRouter/LiteLLM were checked in `literature-review/competitors/00-overview.md` section 3: most hold, but "providers not models" for OpenRouter is outdated.

## Options
| Option | Wording |
|---|---|
| 1. Combination claim | "To our knowledge no peer-reviewed system or reviewed product combines [learned per-prompt estimate, live signals, budgets, failover, hosted + self-hosted] in one gateway; recent preprints and open-source routers cover parts." |
| 2. Evaluation claim | "Prior routers are evaluated offline on quality/price; we add a measured comparison of budget-aware routing and switching under load and failure." |
| 3. Engineering claim | "An open, tested, budget-enforcing gateway for mixed local/hosted LLMs; we do not claim algorithmic novelty" (the guide's own stance) |

## Recommendation
Use **Option 3 as the main claim with Option 2 as the contribution**, and keep Option 1 only as a hedged sentence in the literature review. This matches the guide's honest positioning and survives a reviewer finding RouteBalance or vLLM Semantic Router. Re-check the competitor docs before submission (the proposal's risk table already asks for this).

## Consequences and things to watch
Never claim to be first. Several supporting sources are preprints (see L02).

## Where this shows up in the files
`literature-review/gaps-and-synthesis.md`, `competitors/00-overview.md`, `proposal-drafts/ch1-introduction.md`, `ch2-literature-review.md` (2.7)
