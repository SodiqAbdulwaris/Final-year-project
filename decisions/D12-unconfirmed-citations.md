# D12: Citations to confirm before submission (DOIs, venues, versions)

| | |
|---|---|
| Status | **OPEN, needs your decision** |
| Who decides | You (a quick check per item) |
| Blocks | Reference list accuracy |
| Default used meanwhile | Marked "unconfirmed" or "not checked" in the files |

## The question
Which reference details could not be confirmed and need a manual look?

## What I found
- LLMRouterBench: Findings of ACL 2026 DOI `10.18653/v1/2026.findings-acl.1881` was reported on the Anthology record by the team guide but not confirmed independently.
- SpotServe: ACM DOI `10.1145/3620665.3640411` could not be confirmed (ACM blocked); a Crossref check was requested.
- RouteLLM and Hybrid LLM: OpenReview pages were behind a bot check; ICLR venue rests on the PDF header and arXiv comment.
- RouterBench: venue is an ICML 2024 workshop poster; archival status not verified.
- NeurIPS/ICLR/TMLR papers have no DOI; editor lists and volumes were not all checked (several references say so).
- Numbers for FrugalGPT, Hybrid LLM, Zooter and RouterDC come from arXiv v1, not camera-ready versions.

## Options
| Option | Notes |
|---|---|
| Check each before citing | 15-30 min total |
| Cite arXiv versions with "preprint" label | Always valid |

## Recommendation
Check each item when you read the paper (D09); the full list with sources is in `limitations/L03-unconfirmed-citations.md`.

## Consequences and things to watch
Wrong DOIs are easy for examiners to spot.

## Where this shows up in the files
`limitations/L03-unconfirmed-citations.md`, `literature-review/references.md`
