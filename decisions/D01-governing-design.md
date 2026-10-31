# D01: Which design governs: 16 Oct proposal or 26 Oct team guide?

| | |
|---|---|
| Status | **OPEN, needs your decision** |
| Who decides | You, the team, and the supervisor (the proposal may already have been submitted) |
| Blocks | Chapter 1 aim, objectives and RQs; Chapter 3 requirements and design; Chapter 4 experiments; the gap statement |
| Default used meanwhile | The 26 Oct guide governs; proposal elements it does not contradict are kept; conflicts are marked `DECISION-NEEDED` in `proposal-drafts/design-reconciliation.md` |

## The question
The proposal (16 Oct) plans a sentence-embedding + logistic-regression difficulty classifier, live queue/GPU signals via vLLM + Prometheus, Redis health state, and a per-request latency budget. The team guide (26 Oct, Rev 2) plans k-NN competence estimation over past outcomes, cost budget bands, session hysteresis, a context policy, five experiments (E1-E5), and a simple one-process architecture. They are two different projects in emphasis.

## What I found
- The guide is later and states the team's own decisions (`Research Review/Research Paper Review.docx`; summary in `proposal-drafts/team-design-guide-notes.md`).
- Literature check: the proposal's live-load gap is narrower than claimed (RouteBalance, vLLM Semantic Router, several 2026 preprints; see `literature-review/gaps-and-synthesis.md`). k-NN retrieval routing is supported by Varangot-Reille et al. (2026, EACL SRW) and LLMRouterBench finds simple baselines often competitive.
- The guide makes failover, TTFT measurement and local-backend integration part of E4/E5, so the proposal's resilience goals are mostly preserved. The parts dropped from the MVP are Prometheus/Redis live-load routing and the learned difficulty classifier.
- The guide's own synthetic simulation found k-NN no better than rules (80.5% vs 81.7%): invented numbers, not evidence, but a reminder that RQ1 may come out negative (the guide accepts that).

## Options
| Option | What it means | For | Against |
|---|---|---|---|
| A. Guide governs, live load as optional extension | Core = eligibility filter, k-NN competence, budget bands, hysteresis, context policy, E1-E5. Live-load routing is a stretch objective | Matches the team's latest thinking; smaller, testable scope; fits the SE assessment criteria | Weakens the proposal's headline novelty; needs supervisor sign-off if the proposal was submitted |
| B. Proposal governs | Keep the classifier + live load + Redis/Prometheus core; add guide ideas later | Matches what was submitted; live load is still a real (if narrower) gap | Competes with RouteBalance/vLLM-SR; heavier infrastructure; ignores the team's later decisions |
| C. Hybrid with two clear tracks | Track 1 = guide's k-NN/budget/switching core; Track 2 = live-load signals + failover from the proposal, evaluated on p95 | Keeps both novelty angles | Largest scope; risk of doing both thinly |

## Recommendation
**Option A**, with the proposal's failover/circuit-breaker and p95 measurement kept inside E4/E5, and live-load signals written as a clearly labelled optional objective (O-extension) that you build only if the core is stable. Reason: the evidence shows live-load routing is no longer a clean gap, the guide gives a testable plan with honest negative-result handling, and scope is already large. Confirm with the supervisor in writing before relying on it.

## Consequences and things to watch
- If the proposal was already approved, changes to objectives usually need supervisor/department approval.
- Do not delete the proposal's facts: `proposal-drafts/00-source-facts.md` keeps them.
- Whichever option is picked, update the gap statement (D04) to match.

## Where this shows up in the files
`proposal-drafts/team-design-guide-notes.md`, `proposal-drafts/design-reconciliation.md`, `proposal-drafts/ch1-introduction.md`, `ch3-methodology-design.md`, `literature-review/gaps-and-synthesis.md`
