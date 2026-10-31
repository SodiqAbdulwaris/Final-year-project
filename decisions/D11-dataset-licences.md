Status: DRAFT
Depends on: Owner proposal-building instructions, 31 October 2026
Sources: proposal-drafts/_meta/decisions-applied.md
Open items: Only residual implementation/evidence details stated in current register

# D11 current outcome

Check data/component terms before use/redistribution. Findings and unresolved gates are in decisions-applied and Appendix B.

The owner has supplied this decision; do not re-ask the historical question below. [Applied register](../proposal-drafts/_meta/decisions-applied.md).

## Historical question and recommendation (superseded)

# D11: Datasets and licences (RouterBench, LLMRouterBench, LongMemEval)

| | |
|---|---|
| Status | **OPEN, needs your decision** |
| Who decides | You |
| Blocks | E1, E3 data use and redistribution |
| Default used meanwhile | Not checked |

## The question
Can you use and redistribute these datasets, and do they cover your chosen models (see D05)?

## What I found
- The guide says to check licences and model coverage before use. I did not verify licences.
- RouterBench (2024) and LLMRouterBench (2026) code/data are public; terms and coverage are in each repository.

## Options
| Option | Notes |
|---|---|
| Use public data, cite licence | Standard |
| Create own scored set for gaps | Needed for models not in the data |

## Recommendation
Open each repository's licence and data card, record the licence and version in Table 3.x, and do not redistribute raw data unless allowed.

## Consequences and things to watch
Judge-based labels are noisy (see topic 07 overview).

## Where this shows up in the files
`literature-review/07-testing-and-benchmarking/`, `proposal-drafts/03-methodology-design/00-overview.md` (3.7)
