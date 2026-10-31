# D08: How much to rely on preprints and 2026 papers

| | |
|---|---|
| Status | **OPEN, needs your decision** |
| Who decides | You and the supervisor |
| Blocks | Chapter 2 reference quality, template minimums |
| Default used meanwhile | All papers listed with a peer-reviewed/preprint label; both used |

## The question
The template wants mainly peer-reviewed sources (>=25 works in depth, >=70% from the last five years, >=40 references). About 16 of 89 paper files are not peer-reviewed. Do you cite them?

## What I found
- Non-peer-reviewed files at the 2026-10-31 snapshot are listed in `limitations/L02-preprint-share.md`. Many are exactly the closest prior art (RouteBalance, ContinuityBench, SLOs-Serve).
- The template excludes Wikipedia, blogs and unpublished student projects as primary sources, but preprints on arXiv are not named as excluded; vendor docs are grey literature.
- All papers are 2020 or later, so the five-year share is met.

## Options
| Option | Notes |
|---|---|
| Cite all, label preprints in text and in a column | Honest, uses the best evidence |
| Cite preprints only where no peer-reviewed alternative exists | Safest for marking |
| Exclude preprints | Loses the closest prior art, weakens the gap argument |

## Recommendation
Second option: build the argument on peer-reviewed papers and cite preprints only where nothing peer-reviewed covers the point (live-load routing, failover, 2026 benchmarks), always labelled as preprints. Re-check each preprint's status before submission.

## Consequences and things to watch
Some preprints get revised or published; update citations.

## Where this shows up in the files
`literature-review/_paper-index.md`, `references.md`
