Status: DRAFT
Depends on: Owner proposal-building instructions, 31 October 2026
Sources: proposal-drafts/_meta/decisions-applied.md
Open items: Only residual implementation/evidence details stated in current register

# D05 current outcome

Three to four benchmark-covered models spanning cheap/small, mid-tier and frontier. Exact identities pending aligned coverage; recommendations in decisions-applied.

The owner has supplied this decision; do not re-ask the historical question below. [Applied register](../proposal-drafts/_meta/decisions-applied.md).

## Historical question and recommendation (superseded)

# D05: Which 3-4 models to route between

| | |
|---|---|
| Status | **OPEN, needs your decision** |
| Who decides | You and the team (hardware and API budget decide) |
| Blocks | E1 (data must exist for the models), E2, E4, E5, cost estimates |
| Default used meanwhile | Not chosen; no model named in the drafts beyond examples |

## The question
Which 3-4 differentiated models/deployments (local and hosted) will the router choose between?

## What I found
- The guide says: only compare models that have outcomes in RouterBench/LLMRouterBench, or run the missing ones on a small controlled set; do not substitute unrelated benchmark scores. Model IDs must stay fixed during experiments.
- RouterBench data is 2023-24 models and prices (see `literature-review/07-testing-and-benchmarking/hu-2024-routerbench.md`), so recent models may be absent; LLMRouterBench (2026) is newer (`li-2026-llmrouterbench.md`).
- Local models need to fit your hardware (guide example: 8 GB GPU, one small model at a time).

## Options
| Option | Pool |
|---|---|
| A. All from benchmark data | Pick 3-4 models present in both RouterBench/LLMRouterBench. Easiest for E1 but some may not be runnable locally |
| B. Mixed | 1-2 benchmark-covered hosted models + 1-2 small local open-weight models (Ollama), run the local ones over your scored task set yourself |
| C. All own-evaluated | Evaluate everything yourself on a small set; fully controlled, most work |

## Recommendation
**Option B**: one strong hosted model, one cheap hosted model, and one or two small local open-weight models, all of which appear in LLMRouterBench's pool or that you score yourselves. Check the pool lists in the topic 07 files before choosing. Freeze IDs and versions before E1.

## Consequences and things to watch
Provider updates change model behaviour; record version and date. API cost for scoring tasks is a real budget line.

## Where this shows up in the files
`literature-review/07-testing-and-benchmarking/`, `proposal-drafts/03-methodology-design/00-overview.md` (3.7)
