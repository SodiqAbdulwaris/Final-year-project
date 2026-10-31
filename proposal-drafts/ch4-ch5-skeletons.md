# CHAPTERS FOUR AND FIVE: SKELETONS

**Rules for this file**

- These are empty shells carried forward from the evaluation plan (`ch3-methodology-design.md`, Section 3.9). **Do not fill a result cell until the measurement exists.** `—` means "not yet measured". No number in this file is a result.
- Section numbers follow the template body (4.1 to 4.9; 5.1 to 5.7). Tables 4.1, 4.2 and 5.1 are the template's; the others (4.3 onward) are added from the evaluation plan and numbered in order of appearance. Renumber with Word's caption tool.
- Report results in 4.6 and interpret them only in 4.7. Chapter 5 introduces no new results (template rule).
- Use past tense in the final report. The shells below describe what each section will hold.
- `TODO-confirm-with-supervisor` targets in the "Target" columns come from Table 3.2 and stay unset until the supervisor agrees them (proposal: targets "not set yet" [E-01]).

---

# CHAPTER FOUR: IMPLEMENTATION, TESTING AND RESULTS

Opening paragraph (3 to 5 lines): what was built and tested, and where the evidence that each objective was met is found. Target length 15 to 25 pages.

## 4.1 Development Environment

**Table 4.1: Hardware and software requirements**

| Category | Development | Deployment / minimum |
|---|---|---|
| Processor | — | — |
| Memory (RAM) | — | — |
| GPU (model, memory) for vLLM | — | — |
| Operating system | — | — |
| Software / runtime (Python, FastAPI, vLLM, Ollama, Redis, Prometheus, Grafana, scikit-learn, sentence-transformers: exact versions) | — | — |
| Hosted API providers and models used | — | — |

## 4.2 Implementation of System Modules

For each module: what was implemented, a captioned screenshot where useful, a code snippet of at most 15 lines, and the requirement IDs implemented. Full code goes in the repository, link in Appendix A.

| Module | Requirements | Status | Evidence (figure, listing) |
|---|---|---|---|
| Gateway (FastAPI endpoint) | FR-01, FR-02, FR-17 | — | — |
| Prompt classifier | FR-03 | — | — |
| Scoring engine | FR-04, FR-05, FR-10 | — | — |
| Backend adapters (hosted, Ollama, vLLM) | FR-06, FR-07, FR-08 | — | — |
| Metrics collector and live state | FR-09, FR-12 | — | — |
| Resilience (retry, circuit breaker) | FR-11, FR-12 | — | — |
| Decision logging | FR-13 | — | — |
| Benchmark harness and dashboards | FR-14, FR-15 | — | — |
| Configuration | FR-16 | — | — |

## 4.3 Database Implementation

Show how the log store and the Redis keys were implemented: tables or keys created, relationships and constraints, with DDL or screenshots. TODO: write only if a relational store is used (see 3.6.4); otherwise state that Redis holds state and give the log format.

## 4.4 Integration and Deployment

How the components were joined and deployed: hosting, containers, version control, CI/CD, where each service ran, how the Prometheus-to-Redis path was implemented. TODO after implementation.

## 4.5 System Testing

### 4.5.1 Testing Strategy

Levels and types of tests and the tools used (from Section 3.9). TODO: tool names.

### 4.5.2 Unit and Integration Testing

**Table 4.3: Unit and integration test summary**

| Component | Tests | Passed | Pass rate | Coverage (if measured) |
|---|---|---|---|---|
| Classifier | — | — | — | — |
| Scoring engine | — | — | — | — |
| Circuit breaker | — | — | — | — |
| Backend adapters | — | — | — | — |
| Gateway | — | — | — | — |

### 4.5.3 Functional Testing

Each test is linked to a requirement ID. Expected results below are taken from the requirement text; "Actual result" and "Status" stay empty until the test is run. Full set in Appendix D. TODO: write the concrete inputs.

**Table 4.2: Functional test cases**

| Test ID | Req. ID | Description | Input / steps | Expected result | Actual result | Status |
|---|---|---|---|---|---|---|
| TC-01 | FR-01 | Single OpenAI-compatible endpoint | TODO: request from an unmodified OpenAI client | Valid response in the OpenAI format | | |
| TC-02 | FR-02 | Latency budget accepted | TODO: request with a budget | Request accepted; budget used in routing | | |
| TC-03 | FR-03 | Prompt classified before routing | TODO: easy and hard prompt | Difficulty and task type produced once per request | | |
| TC-04 | FR-04 | Highest-scoring backend selected | TODO: two backends with known scores | The higher-scoring backend is called | | |
| TC-05 | FR-05 | Budget exceeded excludes a backend | TODO: backend with predicted latency above budget | That backend is not chosen | | |
| TC-06 | FR-06 | Hosted backend reached | TODO | Response from the hosted API | | |
| TC-07 | FR-07 | vLLM backend reached | TODO | Response from the vLLM server | | |
| TC-08 | FR-08 | Ollama backend reached | TODO | Response from Ollama | | |
| TC-09 | FR-09 | Live metrics read | TODO | Queue, GPU use and tokens per second in live state | | |
| TC-10 | FR-10 | Busy backend avoided | TODO: raise one backend's queue | Traffic moves to another backend | | |
| TC-11 | FR-11 | Retry on next-best | TODO: make the top backend fail | Request succeeds on the next-best backend | | |
| TC-12 | FR-12 | Circuit opens and recovers | TODO: repeated failures, then recovery | Traffic paused, then resumed after a successful probe | | |
| TC-13 | FR-13 | Decision logged | TODO | Record with backend, scores, attempts, latency, tokens, cost | | |
| TC-14 | FR-14 | Benchmark replay | TODO | Same prompts run through S1 to S4 | | |
| TC-15 | FR-15 | Dashboard shows results | TODO | Cost versus quality and p95 panels populated | | |
| TC-16 | FR-16 | Configuration without code change | TODO: change a weight | Routing changes after reload | | |
| TC-17 | FR-17 | Invalid API key rejected | TODO | Error; no backend called | | |

### 4.5.4 Non-Functional Testing

Report measured values against the targets in Table 3.2.

**Table 4.4: Non-functional results against targets**

| ID | Measure | Target | Measured | Met? |
|---|---|---|---|---|
| NFR-01 | p95 router overhead (ms) | TODO-confirm-with-supervisor | — | — |
| NFR-02 | p95 end-to-end latency versus always-strong | TODO-confirm-with-supervisor | — | — |
| NFR-03 | Cost reduction versus always-strong | TODO-confirm-with-supervisor | — | — |
| NFR-04 | Quality drop versus always-strong | TODO-confirm-with-supervisor | — | — |
| NFR-05 | Routing accuracy | TODO-confirm-with-supervisor | — | — |
| NFR-06 | Success rate with one backend down | TODO-confirm-with-supervisor | — | — |
| NFR-07 | Circuit breaker opens and recovers | Pass or fail | — | — |
| NFR-08 | Unmodified OpenAI client works | Pass or fail | — | — |
| NFR-09 | Concurrent requests sustained | TODO | — | — |
| NFR-10 | No secrets in code or logs | Pass or fail | — | — |
| NFR-11 | No raw prompts in logs | Pass or fail | — | — |
| NFR-12 | Metrics exposed per backend | Pass or fail | — | — |
| NFR-13 | Weights and prices configurable | Pass or fail | — | — |
| NFR-14 | Results reproducible from the package | Pass or fail | — | — |

### 4.5.5 Usability Evaluation and User Acceptance Testing

TODO-confirm-with-supervisor: required or not applicable for a gateway with no end-user interface (see 3.9). If required: participants (at least 20 recommended by the template), tasks, instrument (for example the 10-item System Usability Scale), results with mean and standard deviation against the benchmark of 68. If not applicable, write one sentence saying so and why.

## 4.6 Results and Performance Evaluation

Present results for each objective in turn. For machine-learning parts the template asks for accuracy, precision, recall, F1-score, a confusion matrix and cross-validation, compared with at least one baseline. Report only; interpret in 4.7.

### 4.6.1 Classifier results (O3, RQ3)

**Table 4.5: Routing accuracy by model pair**

| Model pair (strong / weak) | Train pair | Test pair | Routing accuracy | 95% CI | Best constant policy accuracy | Precision | Recall | F1 |
|---|---|---|---|---|---|---|---|---|
| TODO pair A | A | A (held out) | — | — | — | — | — | — |
| TODO pair B | A | B (unseen pair) | — | — | — | — | — | — |
| TODO pair C (if used) | — | — | — | — | — | — | — | — |

Also include: confusion matrix (Figure 4.x); cross-validation results (mean and standard deviation); hypothesis decision for RQ3 (H0 rejected or not, test and p-value).

### 4.6.2 Cost versus quality (O6, RQ6)

**Table 4.6: Cost and quality by strategy on RouterBench**

| Strategy | Mean cost per request | 95% CI | Mean quality | 95% CI | Cost change vs S1 | Quality change vs S1 |
|---|---|---|---|---|---|---|
| S1 Always-strong | — | — | — | — | n/a | n/a |
| S2 Always-weak | — | — | — | — | — | — |
| S3 Load-blind router | — | — | — | — | — | — |
| S4 Load-aware router | — | — | — | — | — | — |

**Table 4.7: Quality on MT-Bench by strategy**

| Strategy | Mean quality score | 95% CI | Notes (how scored) |
|---|---|---|---|
| S1 | — | — | — |
| S2 | — | — | — |
| S3 | — | — | — |
| S4 | — | — | — |

Figure 4.x: cost against quality scatter or curve, one point per strategy with intervals. Hypothesis decisions for H0a/H1a and H0b/H1b (margin δ: TODO-confirm-with-supervisor).

### 4.6.3 Latency and load awareness (O4, RQ4)

**Table 4.8: Latency by strategy and load level**

| Load level (concurrency: TODO) | Strategy | Mean (ms) | p50 (ms) | p95 (ms) | p95 95% CI | Runs |
|---|---|---|---|---|---|---|
| Low | S1 | — | — | — | — | — |
| Low | S3 | — | — | — | — | — |
| Low | S4 | — | — | — | — | — |
| High | S1 | — | — | — | — | — |
| High | S3 | — | — | — | — | — |
| High | S4 | — | — | — | — | — |

Figure 4.x: latency distribution per strategy; per-backend queue length over time from Grafana. Hypothesis decision for RQ4.

### 4.6.4 Resilience under failure (O5, RQ5)

**Table 4.9: Success rate with injected backend failure**

| Failure scenario (TODO: which backend, how long, how injected) | Fallback on? | Requests | Successes | Success rate | Added latency p95 (ms) |
|---|---|---|---|---|---|
| Backend down | No | — | — | — | — |
| Backend down | Yes | — | — | — | — |
| Backend slow | No | — | — | — | — |
| Backend slow | Yes | — | — | — | — |

Also include: time for the circuit to open and to recover; hypothesis decision for RQ5.

### 4.6.5 Router overhead and gateway behaviour (O2, RQ2)

**Table 4.10: Decision overhead**

| Concurrency | Classifier time p95 (ms) | Scoring time p95 (ms) | Total overhead p95 (ms) | Target (NFR-01) |
|---|---|---|---|---|
| TODO | — | — | — | TODO-confirm-with-supervisor |

## 4.7 Discussion of Findings

Interpret the results: what they mean, whether each objective was achieved, how they compare with the related works and existing systems in Chapter Two, and how the project addresses the gap in Section 2.7. Answer each research question here first. Say plainly where a hypothesis was not supported.

| RQ | Finding in one sentence | Evidence | Compared with literature (section in Ch. 2) |
|---|---|---|---|
| RQ1 | — | Tables 3.1, 3.2, 4.2 | — |
| RQ2 | — | Table 4.10 | — |
| RQ3 | — | Table 4.5 | — |
| RQ4 | — | Table 4.8 | — |
| RQ5 | — | Table 4.9 | — |
| RQ6 | — | Tables 4.6, 4.7 | — |

## 4.8 Threats to Validity

Start from the anticipated list in Section 3.9.1 and update it with what actually happened. Columns: threat, type (internal, external, construct, conclusion), what was done, what remains.

| Threat | Type | Mitigation applied | Remaining effect |
|---|---|---|---|
| Single or few model pairs | External | — | — |
| Noisy quality labels | Construct | — | — |
| Benchmarks differ from production traffic | External | — | — |
| Hosted-provider variability | Internal | — | — |
| Limited GPU capacity | Conclusion | — | — |
| Weights tuned on test data | Conclusion | — | — |

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
| O1: specify requirements and design the router | — | Section 3.5, 3.6; Tables 3.1, 3.2 |
| O2: implement the gateway over hosted, Ollama and vLLM backends | — | Section 4.2, 4.5; Table 4.2, Table 4.10 |
| O3: develop the classifier and determine routing accuracy | — | Table 4.5 |
| O4: implement the scoring function and compare load-aware with load-blind routing | — | Table 4.8 |
| O5: implement fallback with circuit breaker and evaluate success rate | — | Table 4.9 |
| O6: compare against always-strong and always-weak baselines | — | Tables 4.6, 4.7 |

## 5.3 Contributions to Knowledge and Practice

Restate the contributions listed in Section 1.9, each supported by a result. TODO.

## 5.4 Conclusion

Answer each research question from Section 1.4 briefly, evidence-based.

| RQ | Answer |
|---|---|
| RQ1 | — |
| RQ2 | — |
| RQ3 | — |
| RQ4 | — |
| RQ5 | — |
| RQ6 | — |

## 5.5 Limitations

Summarise the limitations of the final system and of the evaluation (from Sections 1.8 and 4.8). TODO.

## 5.6 Recommendations

Practical recommendations to specific stakeholders (developers and organisations running more than one LLM, the University, researchers), based only on the findings. TODO.

## 5.7 Future Work

Specific extensions. Candidate list from the proposal's scope boundary and plan (ASSUMPTION: for the team to keep or drop after the results): more than two models per request; other model families; routing with real production traffic; comparison against a cascade baseline; learning the scoring weights online; training or fine-tuning models (out of scope now [SC-04]).

---

# REFERENCES

Use APA 7th with DOIs, from the verified master list in `literature-review/references.md` when it exists. No entry is added here until the source has been read.

# APPENDICES (as in the template)

- Appendix A: Source code repository link and key code listings
- Appendix B: User manual and installation guide (here: gateway configuration and operation guide)
- Appendix C: Questionnaires, interview guides and consent forms (only if interviews are added; see 3.2)
- Appendix D: Full test cases and test results
- Appendix E: Similarity (plagiarism) report summary
- Appendix F: Project schedule (Gantt chart) and record of group meetings with the supervisor
