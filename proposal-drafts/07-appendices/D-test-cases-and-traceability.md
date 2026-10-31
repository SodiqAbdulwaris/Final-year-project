Status: DRAFT
Depends on: D01–D12; Chapter 3 protocol
Sources: _meta/hybrid-design.md; _meta/history/ch4-ch5-skeletons.md
Open items: See _meta/placeholders.md

# Appendix D: Test Cases and Traceability

All cases below will be planned tests, not passing evidence. Actual outcomes and build identifiers will be filled after implementation.

## Requirements-to-test matrix

| Requirement(s) | Planned test IDs | Evidence to collect |
|---|---|---|
| FR-01–FR-02 | T01 | Valid/invalid request and authentication responses. |
| FR-03–FR-04 | T02 | Registry and capability/context/privacy/availability exclusions. |
| FR-05–FR-07 | T03 | Feature and prediction outputs; no-retrieval ablation. |
| FR-08–FR-09 | T04 | Cheapest-feasible and infeasible-policy decisions. |
| FR-10; NFR-05 | T05 | Concurrent reservations, usage reconciliation and uncertain charges. |
| FR-11 | T06 | Hosted/local adapter contract checks. |
| FR-12–FR-14; NFR-04 | T07–T09 | Breaker state transitions, bounded attempts and partial-stream failure. |
| FR-15; NFR-07 | T10 | Redaction, access and authorised-endpoint negative tests. |
| FR-16; NFR-01–NFR-03; NFR-06; NFR-09 | T11 | Frozen replay/live reports, calibration and rerun evidence. |
| FR-17; NFR-10 | T12 | Labelled keyboard-accessible dashboard/export walkthrough. |
| FR-18 | T13 | Optional cascade trigger and all-call accounting, only if enabled. |
| FR-19 | T14 | Scope/configuration review: no live RL/POMDP or response fusion. |
| NFR-08 | T15 | Requirement coverage and test/coverage report. |

## Unit cases

| ID | Input/scenario | Expected behaviour | Observed/evidence |
|---|---|---|---|
| T01 | Missing auth, invalid payload and valid request. | Reject unauthorised/invalid calls; accept valid contract. | [PLACEHOLDER: test evidence] |
| T02 | Candidate violates each hard restriction. | Candidate excluded with reason; no provider call. | [PLACEHOLDER: test evidence] |
| T03 | Evaluated request and restricted historical index. | No evaluated outcome used; feature configuration recorded. | [PLACEHOLDER: test evidence] |
| T04 | Feasible set, equal-cost tie and empty set. | Deterministic cheapest-feasible choice or explicit infeasibility. | [PLACEHOLDER: test evidence] |

## Integration and fault cases

| ID | Scenario | Expected behaviour | Observed/evidence |
|---|---|---|---|
| T05 | Concurrent calls and a timeout with uncertain usage. | Reservations prevent unauthorised spend; uncertainty remains encumbered. | [PLACEHOLDER: test evidence] |
| T06 | Same request through local/hosted adapters. | Declared contract and usage/error mapping preserved. | [PLACEHOLDER: test evidence] |
| T07 | Repeated eligible failures and recovery probe. | Closed/open/half-open transitions under frozen thresholds. | [PLACEHOLDER: test evidence] |
| T08 | 429, connection error and slow response. | Bounded eligible fallback only while resources remain. | [PLACEHOLDER: test evidence] |
| T09 | Mid-stream disconnect or uncertain side effect. | Explicit failure; no silent splice/unsafe repeated action. | [PLACEHOLDER: test evidence] |
| T10 | Forbidden endpoint and sensitive log content. | Block unauthorised destination and redact secrets/content. | [PLACEHOLDER: test evidence] |

## Code-review log

| Date | Revision | Reviewer | Scope | Finding | Disposition/evidence |
|---|---|---|---|---|---|

Implementation and review results will remain absent until performed. This proposal task will not create a router or claim test execution.
