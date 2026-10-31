# CHAPTERS FOUR AND FIVE: SKELETONS (reworked to follow the 26 Oct team guide)

**Rules for this file**

- Empty shells carried forward from the evaluation plan (`ch3-methodology-design.md`, Section 3.9). **Do not fill a result cell until the measurement exists.** `—` means "not yet measured". No number in this file is a result.
- Section numbers follow the template body (4.1 to 4.9; 5.1 to 5.7). Tables 4.1, 4.2 and 5.1 are the template's; the others are added and numbered in order of appearance. Renumber with Word's caption tool.
- Results are reported in 4.6 and interpreted only in 4.7. Chapter 5 introduces no new results (template rule). Past tense in the final report.
- Targets and margins come from Chapter 3 and stay `TODO-confirm-with-supervisor` until approved **before** test data are examined (guide section 5). Confirmatory tests are limited to H1 to H3; everything else is exploratory or descriptive and must be labelled so.
- For every experiment record: configuration version, dataset source and version, model ID and version, backend version, seed, date, machine specification, pricing snapshot and raw outputs. Never label synthetic assumptions as observed results.
- `DECISION-NEEDED` marks items the team must settle (see `design-reconciliation.md`).
- Citations are placeholders to fill from `literature-review/references.md`; none is invented here.

---

# CHAPTER FOUR: IMPLEMENTATION, TESTING AND RESULTS

Opening paragraph (3 to 5 lines): what was built and tested, and where the evidence that each objective (O1 to O6) was met is found. Target length 15 to 25 pages.

## 4.1 Development Environment

**Table 4.1: Hardware and software requirements**

| Category | Development | Deployment / minimum |
|---|---|---|
| Processor | — | — |
| Memory (RAM) | — | — |
| GPU (model, memory) for local inference | — | — |
| Operating system | — | — |
| Software and runtime (Python, FastAPI, database, scikit-learn, embedding model, local engines, test and coverage tools: exact versions) | — | — |
| Local engines and models used (engine, model, quantisation) | — | — |
| Hosted APIs and models used | — | — |

## 4.2 Implementation of System Modules

For each module: what was implemented, a captioned screenshot where useful, a code snippet of at most 15 lines, and the requirement IDs implemented. Full code goes in the repository (link in Appendix A).

| Module | Requirements | Build step | Status | Evidence |
|---|---|---|---|---|
| Gateway (OpenAI-compatible endpoint, auth, validation) | FR-01, FR-02 | 2 | — | — |
| Registry (models and deployments) | FR-03 | 3 | — | — |
| Context estimator and eligibility filter | FR-04, FR-05 | 3 | — | — |
| Rule-based routers | FR-06 | 5 | — | — |
| k-NN estimator, minimum-evidence rule, lower bound, calibration report | FR-07, FR-08, FR-09 | 6 | — | — |
| Budget bands and atomic ledger | FR-10, FR-11 | 4 | — | — |
| Adapters (local and hosted) | FR-12 | 2 | — | — |
| Fallback executor and circuit breaker | FR-13, FR-14 | 8 | — | — |
| Decision logging | FR-15 | 5 | — | — |
| Sessions, hysteresis, context builders | FR-16 to FR-19 | 7 | — | — |
| Evaluation harness and report export | FR-21, FR-26 | 8 | — | — |
| Optional: latency budget, vLLM metrics, classifier, graph arms | FR-20, FR-23 to FR-25 | — | — | — |

## 4.3 Database Implementation

Show how the schema (Section 3.6.4) was implemented: tables, relationships and constraints, with DDL or screenshots, and how the atomic reservation was implemented. TODO after implementation.

## 4.4 Integration and Deployment

How the components were integrated and deployed: process layout, local engines, hosted providers, version control, CI. TODO after implementation.

## 4.5 System Testing

### 4.5.1 Testing Strategy

Levels and types of tests and tools (from Section 3.9.7): unit, integration, concurrency, fault injection, performance. TODO: tool names.

### 4.5.2 Unit and Integration Testing

**Table 4.3: Unit and integration test summary and coverage**

| Module | Tests | Passed | Pass rate | Line coverage |
|---|---|---|---|---|
| Eligibility filter | — | — | — | — |
| Budget arithmetic and ledger | — | — | — | — |
| Rule-based routers | — | — | — | — |
| k-NN estimator | — | — | — | — |
| Adapters (with mocks) | — | — | — | — |
| Fallback and circuit breaker | — | — | — | — |
| Gateway | — | — | — | — |
| **Overall (target: at least 80%)** | — | — | — | — |

### 4.5.3 Functional Testing and Traceability

Each test links to a requirement ID; every Must requirement must have at least one passing test or experiment. Full set in Appendix D. TODO: write the concrete inputs.

**Table 4.2: Functional test cases**

| Test ID | Req. ID | Description | Input / steps | Expected result | Actual result | Status |
|---|---|---|---|---|---|---|
| TC-01 | FR-01 | Unmodified OpenAI client works, non-streamed and streamed | TODO | Valid response in the OpenAI format | | |
| TC-02 | FR-02 | Invalid key or payload rejected | TODO | Error; no backend called | | |
| TC-03 | FR-05 | Ineligible deployments excluded | TODO: lacking capability, context overflow, unhealthy, forbidden, unaffordable | None of them selected | | |
| TC-04 | FR-06 | Rule baselines deterministic | TODO | Same input, same choice | | |
| TC-05 | FR-07 | Insufficient evidence handled | TODO: sparse neighbours | Domain average, then unknown; unknown never treated as good | | |
| TC-06 | FR-08 | Lower bound applied | TODO: two models with equal averages and different evidence | The one with the higher lower bound is chosen; below-target outcome labelled | | |
| TC-07 | FR-10 | Budget bands apply caps | TODO | Request, session and project caps enforced | | |
| TC-08 | FR-11 | Atomic reservation under concurrency | TODO: 10 and 100 concurrent requests | No cap exceeded; unaffordable requests rejected before dispatch | | |
| TC-09 | FR-12 | Local and hosted adapters | TODO | Same request through both | | |
| TC-10 | FR-13 | Bounded retries; no stream continuation on another model | TODO: mid-stream failure | Explicit error, no silent continuation | | |
| TC-11 | FR-14 | Circuit breaker opens and recovers | TODO | Traffic paused, then resumed after a successful probe | | |
| TC-12 | FR-15 | Decision logged without raw sensitive prompt | TODO | Record complete; prompt not stored by default | | |
| TC-13 | FR-16, FR-19 | Stateless default; no silent truncation | TODO | Supplied messages unchanged; explicit context-too-large error | | |
| TC-14 | FR-18 | Hysteresis and exceptions | TODO | No switch below threshold; switch on capability change or failure | | |
| TC-15 | FR-21 | Harness saves run metadata | TODO | Config, versions, seed, pricing snapshot saved | | |

**Traceability matrix (start at step 1, update each step).**

| Requirement | Design module | Implementation | Test case(s) | Experiment |
|---|---|---|---|---|
| FR-01 | Gateway | — | TC-01 | E5 |
| FR-05 | EligibilityFilter | — | TC-03 | E4 |
| FR-07, FR-08 | KnnEstimator, SelectionPolicy | — | TC-05, TC-06 | E1 |
| FR-10, FR-11 | BudgetLedger | — | TC-07, TC-08 | E4 |
| FR-13, FR-14 | FallbackExecutor, CircuitBreaker | — | TC-10, TC-11 | E4, E5 |
| FR-18 | SelectionPolicy | — | TC-14 | E2 |
| FR-19 | ContextBuilder | — | TC-13 | E3 |
| … | … | … | … | … |

### 4.5.4 Non-Functional Testing (ISO/IEC 25010 quality table)

State the edition of the standard cited. Targets are fixed before measurement and justified by a requirement or a measured baseline.

**Table 4.4: Quality table**

| Characteristic | Indicator | Target | Justification | Measured result | Met? |
|---|---|---|---|---|---|
| Performance efficiency | Proxy overhead (gateway minus direct TTFT), p95 | TODO-confirm-with-supervisor | NFR-01; measured direct baseline | — | — |
| Performance efficiency | Throughput at stated concurrency | TODO | NFR-02 | — | — |
| Reliability | Completion under injected faults | TODO-confirm-with-supervisor | NFR-03 | — | — |
| Reliability | Circuit-breaker and fallback rules | Pass or fail | NFR-04 | — | — |
| Reliability (budget) | No reservation limit exceeded at 10 and 100 concurrent requests | Pass or fail | NFR-05 | — | — |
| Security | Authentication, secret hygiene, allow-listing, SSRF controls | Pass or fail | NFR-06 | — | — |
| Security (privacy) | No raw sensitive prompts stored by default; retention and deletion | Pass or fail | NFR-07 | — | — |
| Maintainability | Line coverage; effort to add an adapter | at least 80%; TODO | NFR-08, NFR-09 | — | — |
| Estimate quality | Brier score and reliability table | TODO-confirm-with-supervisor | NFR-13 | — | — |

### 4.5.5 Usability Evaluation and User Acceptance Testing

Preferably at least 8 developers. Tasks: point an existing OpenAI-compatible client at the gateway; choose a budget band; register a local deployment; read a routing decision log. Then the System Usability Scale. Formative evidence, not statistical proof.

**Table 4.5: Usability results**

| Participant | Task 1 done (Y/N, time) | Task 2 | Task 3 | Task 4 | Errors | Help requests | SUS score |
|---|---|---|---|---|---|---|---|
| P1 | — | — | — | — | — | — | — |
| … | … | … | … | … | … | … | … |
| **Mean and 95% interval** | — | — | — | — | — | — | — |

Also list usability issues fixed or deferred. `DECISION-NEEDED`: consent approach; number of participants.

## 4.6 Results and Performance Evaluation

Report the results for each objective in turn; interpret them in 4.7. Declare the primary metric, comparison and margin **before** reporting (state the date they were declared and who approved them).

### 4.6.1 E1: k-NN competence estimation against rules (O1, RQ1, H1)

**Table 4.6: E1 setup record**

| Item | Value |
|---|---|
| Datasets and versions; licences | — |
| Models (3 to 4) and domains (3 to 5) | — |
| Split (training, validation, test) and counts | — |
| Primary metric; comparison; declared margin; date declared | TODO-confirm-with-supervisor |
| k, thresholds, minimum-evidence rule (tuned on validation) | — |

**Table 4.7: E1 results on held-out test tasks at matched budgets**

| Method | Band | Total cost | Success | Completion rate | Routing decision time (ms) | Success at matched cost: difference vs rule B (95% interval) |
|---|---|---|---|---|---|---|
| A Static cheapest eligible | Economy / Balanced / Quality | — | — | — | — | — |
| B Domain-average rule | … | — | — | — | — | reference |
| C k-NN, raw average | … | — | — | — | — | — |
| C k-NN, lower bound | … | — | — | — | — | — |
| Optional classifier comparator | … | — | — | — | — | — |
| Always-strong | n/a | — | — | — | — | — |
| Always-weak | n/a | — | — | — | — | — |

**Table 4.8: E1 calibration and evidence**

| Quantity | Value |
|---|---|
| Brier score (raw neighbour average; lower bound; after recalibration if used) | — |
| Reliability table (predicted bin, observed success, count) | — |
| Share of requests with insufficient evidence; how they were routed | — |
| Achieved success when the lower bound met the target | — |

**Table 4.9: E1 sparsity and new-model checks (exploratory)**

| Training records used | k-NN success at matched cost | Interval |
|---|---|---|
| 10% / 25% / 50% / 100% | — | — |
| New-model records added (0 / 20 / 50 / 100 per domain) | — | — |
| Held-out domain (if run) | — | — |

Figure 4.x: cost–quality curve across bands for each method. Hypothesis decision for H1, labelled meaningful, small or inconclusive.

### 4.6.2 E2: controlled switching (O2, RQ2, H2)

**Table 4.10: E2 results (paired differences across test sessions)**

| Policy | Mean cost per completed session | Switches per session | Success | p50 TTFT | p95 TTFT | Fallbacks | Completion rate | Difference vs per-turn routing (95% interval) |
|---|---|---|---|---|---|---|---|---|
| Free (per turn) | — | — | — | — | — | — | — | reference |
| Locked | — | — | — | — | — | — | — | — |
| Hysteresis, threshold 1 | — | — | — | — | — | — | — | — |
| Hysteresis, threshold 2 | — | — | — | — | — | — | — | — |

Cache conditions (warm repeated prefix, cold new prefix; loaded and cold-loading local models): — . Number of pilot sessions and number of separate test sessions: —. Non-inferiority margin δ: TODO-confirm-with-supervisor. Hypothesis decision for H2; live sessions reported separately.

### 4.6.3 E3: context policies after switching (O3, RQ3, H3)

**Table 4.11: E3 results at the same context-token allowance**

| Condition | Context accuracy | Evidence recall | Temporal correctness | False memories | Abstention correctness | Tokens | Indexing tokens and latency | Retrieval latency | Total cost |
|---|---|---|---|---|---|---|---|---|---|
| C0 Full replay | — | — | — | — | — | — | — | — | — |
| C1 Bounded | — | — | — | — | — | — | — | — | — |
| C2 Text or vector retrieval | — | — | — | — | — | — | — | — | — |
| C3a Graph, manual (optional) | — | — | — | — | — | — | — | — | — |
| C3b Graph, automatic (optional) | — | — | — | — | — | — | — | — | — |

Cold and amortised indexing: —. Break-even calculation for the graph (avoided context inference cost against creation, update, retrieval and verification costs): —. Stop rules applied: —. Hypothesis decision for H3. [CITE-10]

### 4.6.4 E4: budget correctness (O4, RQ4)

**Table 4.12: E4 budget assertions**

| Scenario | Concurrency | Requests | Admitted | Rejected before dispatch | Reserved total | Actual total | Cap overshoot | Reconciliation failures | Assertion passed? |
|---|---|---|---|---|---|---|---|---|---|
| Economy | 1 / 10 / 100 | — | — | — | — | — | — | — | — |
| Balanced | 1 / 10 / 100 | — | — | — | — | — | — | — | — |
| Quality | 1 / 10 / 100 | — | — | — | — | — | — | — | — |
| With 429, timeout, partial stream, retry | — | — | — | — | — | — | — | — | — |
| Local fallback bypass check | — | — | — | — | — | — | — | — | — |

Estimated against provider-reported billing: —. p95 gateway overhead: —.

### 4.6.5 E5: local backend, overhead and fault injection (O5, RQ5)

**Table 4.13: E5 overhead**

| Engine and model | Condition (warm / cold; concurrency) | Direct TTFT | Gateway TTFT | Overhead (95% interval) | Full request time | Runs |
|---|---|---|---|---|---|---|
| TODO engine 1 | — | — | — | — | — | — |
| TODO engine 2 (if run) | — | — | — | — | — | — |
| Hosted API | — | — | — | — | — | — |

**Table 4.14: E5 fault injection**

| Fault | Expected rule | Observed behaviour | Completion rate | Passed? |
|---|---|---|---|---|
| Slow response | Timeout, then fallback | — | — | — |
| HTTP 429 | Bounded retry or fallback | — | — | — |
| Connection failure | Fallback; circuit opens | — | — | — |
| Malformed output | Detect; retry or error | — | — | — |
| Mid-stream disconnect | No transparent continuation on another model | — | — | — |

Record hardware, engine versions, quantisation, loaded state, batch size, power settings and concurrency.

### 4.6.6 Optional extension X1: live-load signals

Only if run (`DECISION-NEEDED`): load-aware against load-blind p95 TTFT under concurrent load; scrape-interval sensitivity. **Table 4.15** — rows: variant, concurrency, p95 TTFT, interval; —.

## 4.7 Discussion of Findings

Interpret the results: what they mean, whether each objective was achieved, how they compare with the related works and existing systems in Chapter Two, and how the project addresses the gap in Section 2.7. Answer each research question here first. Say plainly where a hypothesis was not supported; that is a valid outcome.

| RQ | Finding in one sentence | Evidence | Compared with literature (section in Ch. 2) |
|---|---|---|---|
| RQ1 | — | Tables 4.7 to 4.9 | 2.4.1, 2.4.2, 2.4.9 |
| RQ2 | — | Table 4.10 | 2.4.9 |
| RQ3 | — | Table 4.11 | 2.4.10 |
| RQ4 | — | Table 4.12 | 2.4.4, 2.4.8 |
| RQ5 | — | Tables 4.13, 4.14 | 2.4.5, 2.4.6, 2.4.8 |
| RQ6 | — | Tables 4.4, 4.5 and the requirements | 2.4.8 |

## 4.8 Threats to Validity

Start from the anticipated list in Section 3.9.8 and update it with what happened.

| Threat | Type | Mitigation applied | Remaining effect |
|---|---|---|---|
| Miscalibrated k-NN estimates | Construct | — | — |
| Noisy or flawed benchmark labels | Construct | — | — |
| Replay versus live behaviour | External | — | — |
| Caching, cold starts, price changes | Internal | — | — |
| Pilot and test sessions mixed | Conclusion | — | — |
| Refusal flattering a router | Construct | — | — |
| Small usability sample | Conclusion | — | — |

## 4.9 Chapter Summary

TODO: one or two paragraphs on the implementation and the main results. Write last.

---

# CHAPTER FIVE: SUMMARY, CONCLUSION AND RECOMMENDATIONS

Opening paragraph: what the chapter covers. Target length 3 to 6 pages. No new results.

## 5.1 Summary of the Project

About one page: the problem (Section 1.2), the approach (Chapter 3) and the main results (Chapter 4). TODO.

## 5.2 Achievement of Objectives

**Table 5.1: Achievement of objectives**

| Objective | How it was achieved | Evidence (section, table or figure) |
|---|---|---|
| O1: k-NN competence estimation against rules (E1) | — | Tables 4.6 to 4.9 |
| O2: session-aware hysteresis (E2) | — | Table 4.10 |
| O3: context after switching (E3) | — | Table 4.11 |
| O4: budget bands and atomic reservation (E4) | — | Table 4.12 |
| O5: adapters, retries, circuit breaker, overhead (E5) | — | Tables 4.13, 4.14 |
| O6: requirements, quality, usability | — | Tables 3.1, 3.2, 4.2 to 4.5 |

## 5.3 Contributions to Knowledge and Practice

Restate the contributions in Section 1.9, each supported by a result. TODO.

## 5.4 Conclusion

Answer each research question from Section 1.4 briefly and evidence-based; state which of H1 to H3 were supported, not supported or inconclusive.

| RQ | Answer |
|---|---|
| RQ1 | — |
| RQ2 | — |
| RQ3 | — |
| RQ4 | — |
| RQ5 | — |
| RQ6 | — |

## 5.5 Limitations

Summarise the limitations of the final system and of the evaluation (Sections 1.8 and 4.8). TODO.

## 5.6 Recommendations

Practical recommendations to specific stakeholders (developers and organisations running hosted or local LLMs, the University, researchers), based only on the findings. TODO.

## 5.7 Future Work

Specific extensions. Candidate list from the guide (ASSUMPTION: for the team to keep or drop after the results): live-load signals as a routing input (X1); a learned difficulty classifier; graph memory if E3 justifies it; richer budget learning; more local engines; tool calling and structured output; real production traffic; online learning (out of scope now).

---

# REFERENCES

APA 7th with DOIs, from `references-apa.md` (generated from `literature-review/references.md`).

# APPENDICES (as in the template)

- Appendix A: Source code repository link and key code listings
- Appendix B: User manual and installation guide (gateway configuration, registering deployments, budget bands)
- Appendix C: Interview guide, consent forms, usability task script and SUS questionnaire
- Appendix D: Full test cases and test results; traceability matrix
- Appendix E: Similarity (plagiarism) report summary
- Appendix F: Project schedule (Gantt chart) and record of group meetings with the supervisor
