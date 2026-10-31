Status: DRAFT
Depends on: Owner proposal-building instructions, 31 October 2026
Sources: proposal-drafts/_meta/decisions-applied.md
Open items: Only residual implementation/evidence details stated in current register

# D03 current outcome

No numeric targets invented. Use [PROVISIONAL: revise after pilot]; justify/freeze quality margin before test inspection.

The owner has supplied this decision; do not re-ask the historical question below. [Applied register](../proposal-drafts/_meta/decisions-applied.md).

## Historical question and recommendation (superseded)

# D03: Numeric targets and the non-inferiority margin

| | |
|---|---|
| Status | **OPEN, needs your decision** |
| Who decides | You and the supervisor (the proposal says targets "will be agreed with the supervisor before testing") |
| Blocks | Template Table 3.2 (non-functional requirements), Chapter 4 pass/fail, E1/E2 claims |
| Default used meanwhile | All targets marked `TODO-confirm-with-supervisor`; only the guide/template numbers (>=80% line coverage, SUS benchmark 68, >=5 interviews, >=8 usability participants) are used as given |

## The question
What are the measurable targets for gateway overhead, success rate under injected failures, routing quality, and the quality loss you will accept (non-inferiority margin)?

## What I found
- The guide says its example margin of 3 percentage points is "only a placeholder, not a recommendation" and must be justified by user tolerance and approved.
- Reference points from the literature (not targets to copy): router decision cost about 32 ms/request at 12 req/s (RouteBalance, preprint); vLLM Semantic Router quotes a <100 ms tail budget for its own signal extraction (preprint); ContinuityBench reports 99.2% context preservation across 750 failovers (preprint, one provider pair).
- The template's example NFR is "<=2 s at the 95th percentile" for search, a web-app norm, not an LLM routing norm.

## Options
| Target | Option 1 (cautious) | Option 2 (ambitious) |
|---|---|---|
| Added gateway latency (p95, measured against direct call) | <= 100 ms | <= 50 ms |
| Success rate with one backend failing | >= 99% of requests complete via fallback | >= 99.5% |
| Quality vs always-strong baseline | non-inferior within a margin fixed after the pilot | same, narrower margin |
| Non-inferiority margin | choose after pilot variance (guide: not a guess) | n/a |
| Line coverage | >= 80% (guide) | >= 85% on budget/routing modules |
| SUS | mean >= 68 (template benchmark) | >= 75 |
| Usability sample | >= 8 | >= 12 |

## Recommendation
Take Option 1 as provisional wording in the drafts, label every number `provisional`, and fix the final values (especially the margin) only after the E1/E2 pilot and with supervisor approval, as the guide requires. Record the date they were fixed before test data are examined.

## Consequences and things to watch
Changing a target after seeing results is a validity threat; write the date and version of the targets into the report.

## Where this shows up in the files
`proposal-drafts/03-methodology-design/00-overview.md` (Table 3.2), `ch4-ch5-skeletons.md`
