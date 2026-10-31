# CHAPTER THREE: METHODOLOGY, SYSTEM ANALYSIS AND DESIGN (draft)

**Drafting notes (delete before pasting)**

- Tense: future (proposal). Facts from `00-source-facts.md`; fact IDs in square brackets are for the team.
- Numeric targets are **not set** in the proposal [E-01]. Every target below is written as `TODO-confirm-with-supervisor` with the unit and form of the measure, never with an invented number.
- Items the drafter chose are marked `ASSUMPTION:`. The template numbers the first three Chapter 3 tables as 3.1 to 3.3; extra tables here continue from 3.4 in the order they appear. Renumber with Word's caption tool when assembling.
- Template target length 15 to 25 pages. Diagrams (use case, class, sequence, activity, deployment) must be drawn; this file gives their content as lists and tables.

---

This chapter describes how the AI Request Router will be researched, specified, designed and evaluated. It sets out the methodology, how requirements will be gathered, an analysis of the existing way of working, the proposed system, the requirements, the design including the routing algorithm, the data to be used, the tools, the evaluation plan, and the ethical considerations. The aim is that someone with similar skills can reproduce the work from this chapter alone.

## 3.1 Research and Development Methodology

**Research design: Design Science Research (DSR).** The project builds an artefact, the router, to close a stated gap, and evaluates it against stated criteria. That is the pattern of design science [CITE: Design Science Research methodology; candidate sources from the drafter's knowledge, verify before citing: Hevner et al. (2004) and Peffers et al. (2007)]. Experiments on public benchmarks supply the evidence, so the evaluation is also experimental (Wohlin et al., 2012, cited in the course module). ASSUMPTION: the proposal does not name a methodology; DSR plus iterative development is the drafter's choice. TODO-confirm-with-supervisor.

**Development model: iterative and incremental, three iterations that follow the proposal's phases** [SC-01 to SC-03; order "to be confirmed with the team"].

| Iteration | Phase [proposal] | Build | Evaluate and review | Objective |
|---|---|---|---|---|
| 1 | Phase 1: gateway and classifier | FastAPI endpoint; hosted, Ollama and vLLM adapters; classifier; first scoring function | Functional tests; classifier routing accuracy on at least two model pairs; router overhead | O1 to O3 |
| 2 | Phase 2: resilience and load awareness | Prometheus signals from vLLM into Redis; load terms in the score; retry and circuit breaker | Load-aware versus load-blind under load; success rate under injected failure | O4, O5 |
| 3 | Phase 3: benchmarking | Benchmark harness; baselines; Grafana dashboards | Cost, quality, p95 versus always-strong and always-weak on RouterBench and MT-Bench | O6 |

Each iteration ends with a review with the supervisor. TODO: iteration length, number of sprints, meeting cadence, calendar dates (feeds the "time-bound" part of the SMART objectives and Appendix F).

**Figure 3.1: Methodology diagram** (draw; content below).

```
 Problem identification         Define objectives         Design and development        Demonstration            Evaluation              Communication
 (gaps G1-G7, Table 2.4)  ───►  (O1-O6, SMART)      ───►  (iterations 1, 2, 3)     ───►  (router runs on    ───►   (metrics, baselines,  ───►  (report, replication
                                                                ▲                         benchmark prompts)       hypotheses H0/H1)          package, dashboards)
                                                                └──────────────── feedback to next iteration ◄────────────────┘
```

## 3.2 Requirements Elicitation

The template asks who was asked, how many, and how they were selected. For this project the planned sources are documents, not participants:

1. **Review of existing solutions.** The proposal already analyses OpenRouter, LiteLLM Router and Auto Router, RouteLLM, FrugalGPT-style cascades and commercial routers, and records what each does and does not cover [S-01 to S-05]. Their documentation will be re-read, with access dates, before the requirements are frozen [R-04].
2. **Literature review** (Chapter Two): the gaps G1 to G7 become requirement drivers.
3. **Supervisor consultation**, to agree the numeric targets before testing [E-01]. TODO: date of the agreement.

Main findings so far (from the proposal): the router must decide per prompt, use live load, honour a latency budget, work with hosted and self-hosted backends, recover from failure and be measurable against baselines [D-01 to D-07].

TODO-confirm-with-supervisor: whether the department expects interviews or a questionnaire with the target users (developers and organisations running more than one LLM [P-07]). **No human participants are planned in the proposal.** If interviews are added, consent forms and the interview guide go in Appendix C and Section 3.10 changes.

## 3.3 Analysis of the Existing System

### 3.3.1 Description of the Existing System

"Existing system" here means how teams send LLM requests today [P-01, P-04]:

1. **Hard-coded single model.** The application calls one model's API for every request. There is no per-prompt choice, no awareness of backend load and no failover. This is the baseline situation.
2. **Gateways and routers.** Some teams put OpenRouter or LiteLLM in front of their models. These add provider choice, load balancing across copies of a named model, fallbacks, or complexity tiers, each covering one slice [S-01, S-02].

Figure (draw): flowchart or activity diagram of the hard-coded path, Client application, then one model API, then response, with "error returned to client" on failure. TODO: draw.

### 3.3.2 Limitations of the Existing System

Source for each row: the proposal's section 2 [S-01 to S-05]. All third-party statements are VERIFY until re-checked.

**Table 3.4: Limitations of the existing system**

| ID | Limitation | Evidence | Gap in Table 2.4 |
|---|---|---|---|
| L1 | Easy and hard prompts go to the same model | Hard-coded setups; LiteLLM core Router [S-02] | G1 |
| L2 | Live load is seen late or not at all | OpenRouter rolling 5-minute statistics [S-01]; LiteLLM Auto Router docs do not mention load [S-02] | G2 |
| L3 | Self-hosted GPU servers are not covered together with hosted APIs | OpenRouter routing docs [S-01]; commercial routers closed [S-05] | G3 |
| L4 | Decisions are price-only or quality-only | OpenRouter defaults [S-01]; RouteLLM two models only [S-03] | G4 |
| L5 | Failure handling is absent in hard-coded setups and not tied to per-prompt choice in research routers | Proposal section 1 [P-04]; RouteLLM [S-03] | G5 |
| L6 | Cascades pay the latency of every failed attempt | FrugalGPT-style cascades [S-04] | G6 |
| L7 | Savings are unproven without comparison to single-model baselines | Proposal section 3 [D-07] | G7 |

## 3.4 The Proposed System

### 3.4.1 Description of the Proposed System

The AI Request Router is a gateway: one OpenAI-compatible endpoint that receives every client request, scores the prompt for difficulty and task type, weighs predicted quality, cost and the live load of each backend against an optional per-request latency budget, and sends the request to the best backend, hosted or self-hosted, retrying on the next-best backend on failure [M-05, D-01 to D-06].

- **Users:** developers and organisations running more than one LLM [P-07]. In design terms the actors are the client application, the operator who configures backends, the backends themselves, and Prometheus.
- **Main modules:** gateway (FastAPI); prompt classifier; scoring engine; backend adapters (hosted APIs, Ollama, vLLM); live-state store (Redis) with the Prometheus metrics collector; resilience (retry and circuit breaker); benchmark harness and dashboards (Grafana).

### 3.4.2 Justification for the Proposed System

**Table 3.5: How the proposed system addresses each limitation** (from proposal section 3 [D-01 to D-07])

| Limitation (Table 3.4) | What the router does | Built with | Requirements |
|---|---|---|---|
| L1 | Scores each prompt for difficulty and task type before choosing a model | sentence-transformers, scikit-learn logistic regression | FR-03, FR-04 |
| L2 | Reads live queue length, GPU use and tokens per second and avoids busy servers | vLLM, Prometheus | FR-09, FR-10 |
| L3 | Puts hosted APIs and own GPU servers behind one OpenAI-compatible endpoint | vLLM, Ollama, FastAPI | FR-01, FR-06, FR-07, FR-08 |
| L4 | Combines predicted quality, cost and latency into one score; honours a latency budget | Custom scoring function in Python | FR-02, FR-04, FR-05 |
| L5 | Retries on the next-best backend; pauses traffic to a repeatedly failing one | Redis, circuit-breaker pattern | FR-11, FR-12 |
| L6 | Decides before calling, in one hop | Same classifier run before the request is sent | FR-03 |
| L7 | Plots cost against quality and p95 latency against always-strong and always-weak baselines | RouterBench, MT-Bench, Grafana | FR-14, FR-15 |

## 3.5 Requirements Specification

### 3.5.1 Functional Requirements

MoSCoW priorities are the drafter's reading of the proposal (ASSUMPTION): features the proposal builds in a named phase are Must; supporting features are Should or Could; building or training models is Won't [SC-04]. TODO-confirm-with-supervisor. Use the IDs again in the Chapter 4 test cases.

**Table 3.1: Functional requirements**

| ID | Requirement | Actor | Priority |
|---|---|---|---|
| FR-01 | The system shall expose one OpenAI-compatible endpoint that accepts chat requests from any client. (ASSUMPTION: the chat-completions style of request; exact paths fixed in design.) | Client application | Must |
| FR-02 | The system shall accept an optional per-request latency budget. (TODO: whether it is sent as a header or a body field.) | Client application | Must |
| FR-03 | The system shall classify each prompt for difficulty and task type before a backend is chosen, once per request. | System | Must |
| FR-04 | The system shall compute a score for each eligible backend from predicted quality, cost and latency, and select the highest-scoring backend. | System | Must |
| FR-05 | The system shall exclude, or rank lower, a backend whose predicted latency exceeds the request's latency budget. | System | Must |
| FR-06 | The system shall route to hosted API backends. | System | Must |
| FR-07 | The system shall route to self-hosted vLLM backends. | System | Must |
| FR-08 | The system shall route to Ollama backends. | System | Should |
| FR-09 | The system shall obtain queue length, GPU use and tokens per second for each vLLM backend through Prometheus. | System | Must |
| FR-10 | The system shall use the live load values in the score so that busy backends are avoided. | System | Must |
| FR-11 | The system shall retry a failed request on the next-best backend. | System | Must |
| FR-12 | The system shall temporarily stop sending traffic to a backend that keeps failing, and shall keep that health state in Redis. | System | Must |
| FR-13 | The system shall record, for every request, the chosen backend, the scores, the attempts, the latency, the tokens and the cost. (ASSUMPTION: needed to compute the evaluation metrics; not stated in the proposal.) | System | Must |
| FR-14 | The system shall provide a benchmark harness that replays RouterBench and MT-Bench prompts through the router and through the always-strong and always-weak baselines. | Evaluator | Must |
| FR-15 | The system shall show cost against quality and p95 latency per strategy on Grafana dashboards. | Evaluator | Should |
| FR-16 | The system shall let an operator configure backends, prices and scoring weights without code changes. (ASSUMPTION.) | Operator | Should |
| FR-17 | The system shall authenticate client calls with API keys. (ASSUMPTION: usual for an OpenAI-compatible gateway; not in the proposal.) | Client application | Should |
| FR-18 | The system shall support streamed responses. (ASSUMPTION: not in the proposal.) | Client application | Could |
| FR-19 | The system shall build or train the language models it routes between. | n/a | Won't (out of scope [SC-04]) |

### 3.5.2 Non-Functional Requirements

The proposal sets no numeric targets [E-01]. Each row states the measure, the unit and how it is measured. The target cell stays `TODO-confirm-with-supervisor` unless the requirement can be pass or fail without a number.

**Table 3.2: Non-functional requirements**

| ID | Category | Requirement | Measure / target |
|---|---|---|---|
| NFR-01 | Performance | Router decision overhead (classification plus scoring), added to the call | p95 overhead in ms per request under a stated load. Target: TODO-confirm-with-supervisor |
| NFR-02 | Performance | End-to-end latency compared with always-strong | p95 latency in ms per strategy and load level. Target: TODO-confirm-with-supervisor [E-03] |
| NFR-03 | Cost | Cost per request compared with always-strong | Mean cost per request, and percent reduction. Target: TODO-confirm-with-supervisor [E-02] |
| NFR-04 | Quality | Answer quality compared with always-strong | Mean benchmark quality score, with the allowed drop δ. Target: TODO-confirm-with-supervisor [E-02] |
| NFR-05 | Accuracy | Routing accuracy of the classifier | Proportion of prompts routed to the right model, with 95% confidence interval, on at least two model pairs. "Right model" definition and target: TODO-confirm-with-supervisor [E-04, R-01] |
| NFR-06 | Reliability | Request success rate when one backend fails | Success rate with and without fallback under injected failure. Target: TODO-confirm-with-supervisor |
| NFR-07 | Reliability | Circuit breaker behaviour | Opens after a configured number of failures and recovers after a probe. Parameter values: TODO-confirm-with-supervisor. Pass or fail on the behaviour |
| NFR-08 | Compatibility | Works with a standard OpenAI client library without changing client code | Pass or fail test with an unmodified client (ASSUMPTION: library choice TODO) |
| NFR-09 | Scalability | Number of concurrent requests the gateway sustains | Concurrent requests at which p95 overhead stays within NFR-01. Target and hardware: TODO |
| NFR-10 | Security | Provider keys and client keys are not stored in code or logs | Pass or fail review; secrets read from the environment (ASSUMPTION) |
| NFR-11 | Privacy | Raw prompt text is not written to logs by default | Pass or fail review; prompts logged as hashes (ASSUMPTION) |
| NFR-12 | Observability | Every request and every backend exposes metrics | Prometheus metrics present for each backend; decision log per request (FR-13) |
| NFR-13 | Maintainability | Scoring weights and prices change without code changes | Change by configuration only (FR-16) |
| NFR-14 | Reproducibility | Anyone can repeat the benchmark runs | Replication package with versions, seeds and scripts; results reproduced within reported confidence intervals (ASSUMPTION: module rule on replicability) |

### 3.5.3 Use Case Model

**Actors.** Client application (developer's software that calls the endpoint); Operator (configures backends, prices, weights); Evaluator (the team, runs benchmarks); external systems: hosted API providers, Ollama server, vLLM server, Prometheus.

**Use cases** (draw the diagram from this list):

| ID | Use case | Actor | Requirements |
|---|---|---|---|
| UC-01 | Route a request to the best backend | Client application | FR-01 to FR-07, FR-13 |
| UC-02 | Recover from a backend failure | System (client sees a normal answer) | FR-11, FR-12 |
| UC-03 | Observe live backend load | Prometheus, system | FR-09, FR-10 |
| UC-04 | Configure backends, prices and weights | Operator | FR-16, FR-17 |
| UC-05 | Run a benchmark comparison | Evaluator | FR-14, FR-15 |

**UC-01: Route a request to the best backend**

| Field | Content |
|---|---|
| Actor | Client application |
| Preconditions | At least one backend is configured and not in an open-circuit state. Client holds a valid key (FR-17). |
| Main flow | 1. Client sends an OpenAI-style request with an optional latency budget. 2. Gateway validates it. 3. Classifier returns difficulty and task type. 4. Scoring engine reads live state for each backend. 5. Engine drops backends with an open circuit or predicted latency above the budget. 6. Engine scores the rest and ranks them. 7. Gateway calls the top backend. 8. Gateway returns the response in the OpenAI format. 9. Gateway records the decision, latency, tokens and cost. |
| Alternative flows | A. No latency budget given: latency is scored but no backend is excluded on budget. B. No backend meets the budget: TODO design decision (relax the budget and choose the lowest predicted latency, or return an error). C. Backend call fails: go to UC-02. D. Invalid key or request: return an error without calling any backend. |
| Postconditions | The client holds a response or an error; a decision record exists. |

**UC-02: Recover from a backend failure**

| Field | Content |
|---|---|
| Actor | System (triggered by UC-01) |
| Preconditions | A backend call has failed or timed out. |
| Main flow | 1. Gateway records the failure against that backend in Redis. 2. If the failure count reaches the threshold, the circuit opens and the backend receives no traffic for a cool-down period. 3. Gateway retries on the next-best backend from the ranked list. 4. Gateway returns the first successful response. |
| Alternative flows | A. Every ranked backend fails: return an error to the client. B. Cool-down ends: the circuit half-opens and a single probe request decides whether it closes. |
| Postconditions | Health state is updated; the attempt sequence is logged. Thresholds, cool-down and maximum attempts: TODO-confirm-with-supervisor. |

**UC-05: Run a benchmark comparison**

| Field | Content |
|---|---|
| Actor | Evaluator |
| Preconditions | Benchmark prompts and prices loaded; strategies configured (always-strong, always-weak, load-blind router, load-aware router). |
| Main flow | 1. Evaluator selects a benchmark, model pair and load level. 2. Harness replays the same prompts through each strategy. 3. Harness records cost, quality, latency and success per request. 4. Harness computes means, p95 and confidence intervals. 5. Results appear on dashboards and in result files. |
| Alternative flows | A. A backend is unavailable: the run is marked and the cause logged. |
| Postconditions | A result set exists that the Chapter 4 tables are filled from. |

## 3.6 System Design

### 3.6.1 System Architecture

The design follows the proposal's Figure 1. Style: ASSUMPTION: a layered request pipeline inside one asynchronous gateway service, with a shared state store and external backends. It is chosen because every request must pass the classifier and scoring engine once, in order [F-01], and because shared health state must be visible to every gateway instance [D-05]. TODO: justify further against the alternatives from Section 2.3.

**Request flow** [F-02 to F-04]

1. **Client request**: OpenAI-style call with an optional latency budget.
2. **Gateway (FastAPI)**: single endpoint for every client.
3. **Prompt classifier**: scores difficulty and task type.
4. **Scoring engine**: weighs quality, cost and latency; reads **live state (Redis)**: queue length, GPU use, tokens per second (collected by Prometheus), health and failure counts.
5. **Backend**: one of hosted APIs (pay-per-token providers), Ollama (local models) or vLLM (self-hosted GPU server).
6. **On failure**: retry on the next-best backend and pause traffic to the failing one.
7. vLLM servers report their metrics, which flow into the live state.

**Open design question** [F-05]: how metrics get from Prometheus into Redis. ASSUMPTION: a small collector in the gateway periodically queries Prometheus (or scrapes the vLLM metrics endpoint) and writes the latest values into Redis with a short expiry, so a stale value is not trusted. TODO-confirm-with-supervisor: polling interval and expiry.

**Deployment diagram (draw).** Nodes: client machine; gateway host (FastAPI, classifier loaded in memory); Redis; Prometheus and Grafana; one or more GPU hosts running vLLM; a host running Ollama; external hosted API providers. TODO: actual hardware, network layout and where each runs.

Figure 3.2: reuse the image of proposal Figure 1 as a starting point and redraw it as a UML deployment diagram.

### 3.6.2 Structural Design (Class Diagram)

ASSUMPTION: candidate classes, to confirm during Iteration 1.

| Class | Responsibility | Key attributes and methods |
|---|---|---|
| `Gateway` | HTTP endpoint, validation, auth | `handle_request(req)` |
| `PromptClassifier` | Embed the prompt; return difficulty and task type | `embed(text)`, `difficulty(e)`, `task_type(e)` |
| `ScoringEngine` | Rank eligible backends | `score(backend, d, t, live, budget)`, `rank(...)` |
| `Backend` (abstract) | Common interface | `price_in`, `price_out`, `call(req)` |
| `HostedBackend`, `OllamaBackend`, `VllmBackend` | Concrete adapters | provider-specific `call` |
| `LiveStateStore` | Read and write live metrics and health in Redis | `get(backend)`, `put(backend, metrics)` |
| `MetricsCollector` | Pull queue, GPU use and tokens per second from Prometheus | `poll()` |
| `CircuitBreaker` | Closed, open, half-open state per backend | `allow()`, `record_success()`, `record_failure()` |
| `Router` | Orchestrate classify, score, call, retry | `route(req)` |
| `DecisionLogger` | Persist the decision record | `log(record)` |
| `BenchmarkHarness` | Replay prompts through strategies | `run(strategy, dataset, load)` |

### 3.6.3 Behavioural Design (Sequence and Activity Diagrams)

Draw: (a) sequence diagram for UC-01 with lifelines Client, Gateway, Classifier, ScoringEngine, LiveStateStore, Backend; (b) sequence diagram for UC-02 with CircuitBreaker and two Backends; (c) activity diagram of the routing algorithm in Section 3.6.5; (d) state diagram of the circuit breaker (closed, open, half-open).

### 3.6.4 Database Design

The proposal names no relational database [D-05]. Shared state lives in Redis; decision logs need a durable store (FR-13). TODO-confirm-with-supervisor: whether the department expects an ERD and 3NF schema for this project, and which store holds the logs.

**Redis keys (ASSUMPTION: names are draft).**

| Key pattern | Content | Written by |
|---|---|---|
| `backend:{id}:queue_len` | Current queue length | MetricsCollector |
| `backend:{id}:gpu_util` | Current GPU use | MetricsCollector |
| `backend:{id}:tps` | Current tokens per second | MetricsCollector |
| `backend:{id}:failures` | Recent failure count | CircuitBreaker |
| `backend:{id}:breaker` | closed, open or half-open, with reopen time | CircuitBreaker |

**Decision-log schema (ASSUMPTION), in at least 3NF if stored relationally.**

| Table | Columns | Notes |
|---|---|---|
| `backend` | `backend_id` (PK), `name`, `kind` (hosted, ollama, vllm), `price_in`, `price_out` | One row per configured backend |
| `request` | `request_id` (PK), `received_at`, `prompt_hash`, `difficulty`, `task_type`, `latency_budget_ms`, `strategy`, `final_backend_id` (FK), `outcome` | No raw prompt text (NFR-11) |
| `attempt` | `attempt_id` (PK), `request_id` (FK), `backend_id` (FK), `seq`, `score`, `status`, `latency_ms`, `tokens_in`, `tokens_out`, `cost` | One row per backend call, so retries are visible |

Provide a data dictionary (type, constraint, description) for each table when the schema is final.

### 3.6.5 Algorithm and Model Design

**Pipeline** (each request passes the classifier and scoring engine once [F-01]).

1. Embed the prompt with sentence-transformers.
2. Classifier outputs a difficulty score d in [0, 1] and a task type t [D-01]. ASSUMPTION: difficulty is the estimated probability that the weak model's answer would be unacceptable, learned by logistic regression from benchmark labels; task type is a second classifier. The labels and their definition: TODO-confirm-with-supervisor [E-04, R-02].
3. For each eligible backend i, the scoring engine computes predicted quality, expected cost and expected latency (below), then the score.
4. The highest-scoring backend is called; on failure the next ranked one is tried (Section 3.6.5, resilience).

**Predicted quality.** ASSUMPTION: q̂ᵢ(x) = (1 − d) · qᵢ,easy(t) + d · qᵢ,hard(t), where qᵢ,easy(t) and qᵢ,hard(t) are the mean benchmark quality of model i on easy and hard prompts of task type t in the training split. This is the simplest form that uses both outputs of the classifier. Alternatives (one logistic regression per model predicting acceptable quality) are compared in Chapter Two.

**Expected cost.** ĉᵢ(x) = pᵢ,in · nᵢₙ(x) + pᵢ,out · n̂ₒᵤₜ(t), with per-token prices pᵢ,in and pᵢ,out from configuration, input token count nᵢₙ(x) and an estimated output length n̂ₒᵤₜ(t) by task type. Hosted prices come from the provider. TODO-confirm-with-supervisor: how a self-hosted token is priced (for example amortised GPU cost); the proposal does not say.

**Expected latency.** ASSUMPTION: l̂ᵢ(x) = l₀ᵢ + n̂ₒᵤₜ(t) / TPSᵢ + Qᵢ · sᵢ, where l₀ᵢ is base latency, TPSᵢ is tokens per second, Qᵢ is queue length and sᵢ is the average service time per queued request, for self-hosted servers from live state [D-02]. For hosted APIs, a rolling average of recent latency stands in. The form is to be validated against measurements in Iteration 2.

**Score.** For each backend i not blocked by the circuit breaker and, when a budget B is given, with l̂ᵢ ≤ B:

> Sᵢ(x) = w_q · q̂ᵢ(x) − w_c · ĉᵢ(x) / c_ref − w_l · l̂ᵢ(x) / L_ref

with w_q + w_c + w_l = 1; c_ref = the largest ĉ among eligible backends; L_ref = B if a budget is given, otherwise the largest l̂ among eligible backends. The router picks argmaxᵢ Sᵢ. Weights are tuned on a validation split (ASSUMPTION: grid search) and reported; the values are TODO.

**Worked example (ILLUSTRATIVE VALUES ONLY: these are invented to show how the formula behaves, not measurements, and must not appear in results).**

Setup: weights w_q = 0.6, w_c = 0.2, w_l = 0.2. Latency budget B = 3 s, so L_ref = 3 s. Two backends: Strong (hosted API) and Weak (vLLM). Cost is normalised by the larger cost, so Strong has ĉ/c_ref = 1.0 and Weak has 0.05.

| Case | Backend | q̂ | ĉ / c_ref | l̂ (s) | l̂ / L_ref | Computation | S |
|---|---|---|---|---|---|---|---|
| 1. Easy prompt, Weak idle | Strong | 0.95 | 1.00 | 1.2 | 0.40 | 0.6·0.95 − 0.2·1.00 − 0.2·0.40 = 0.570 − 0.200 − 0.080 | **0.290** |
| | Weak | 0.90 | 0.05 | 0.6 | 0.20 | 0.6·0.90 − 0.2·0.05 − 0.2·0.20 = 0.540 − 0.010 − 0.040 | **0.490** (chosen) |
| 2. Hard prompt, Weak idle | Strong | 0.92 | 1.00 | 1.2 | 0.40 | 0.552 − 0.200 − 0.080 | **0.272** (chosen) |
| | Weak | 0.40 | 0.05 | 0.6 | 0.20 | 0.240 − 0.010 − 0.040 | **0.190** |
| 3. Easy prompt, Weak busy (queue pushes l̂ to 3.4 s) | Weak | 0.90 | 0.05 | 3.4 | n/a | l̂ = 3.4 s > B = 3 s, so Weak is excluded before scoring | excluded |
| | Strong | 0.95 | 1.00 | 1.2 | 0.40 | 0.290 as in case 1 | **0.290** (chosen) |

What the example shows: the same weights send the easy prompt to the cheap model and the hard prompt to the strong model (gap G1); when the cheap model's live load makes it miss the latency budget, traffic moves to the other backend (gap G2). The numbers 0.95, 0.90, 0.92, 0.40, the latencies and the weights are placeholders. Real values come from the benchmark data and measurements.

**Routing pseudocode.**

```
function ROUTE(request):
    B  ← request.latency_budget            # may be none
    e  ← EMBED(request.prompt)
    d  ← DIFFICULTY(e);  t ← TASK_TYPE(e)
    ranked ← []
    for each backend i in REGISTRY:
        if BREAKER[i].state = OPEN: continue
        q ← PREDICT_QUALITY(i, d, t)
        c ← EXPECTED_COST(i, request, t)
        l ← EXPECTED_LATENCY(i, t, LIVE_STATE[i])
        if B is set and l > B: continue
        ranked.append(i, SCORE(q, c, l, B))
    if ranked is empty:                    # TODO design decision: relax budget or return error
        return HANDLE_NO_CANDIDATE(request)
    sort ranked by score, highest first
    for (i, score) in first K of ranked:   # K = maximum attempts, TODO
        response ← CALL(i, request, timeout)    # timeout value TODO
        if response is success:
            BREAKER[i].RECORD_SUCCESS();  LOG(request, ranked, i);  return response
        BREAKER[i].RECORD_FAILURE()
    return ERROR(503)
```

**Resilience.** Circuit breaker per backend with three states [D-05]: closed (normal), open (no traffic during a cool-down), half-open (one probe decides). Opens after a number of failures; closes after a successful probe. State is shared in Redis so every gateway instance sees it. Parameters (failure threshold, window, cool-down, maximum attempts K, timeout) are TODO-confirm-with-supervisor.

**Design choices to justify in the final report.** Why logistic regression (small, fast, one pass before the call, so no cascade latency [D-01, D-06]); why a linear score (inspectable weights, unlike closed commercial routers [S-05]); why a hard budget constraint instead of only a penalty (a budget is a promise to the caller).

### 3.6.6 User Interface Design

The router has no end-user interface in the proposal. The visible parts are the HTTP API (error format and response fields in the OpenAI style) and Grafana dashboards [D-07]. ASSUMPTION: planned dashboard panels: cost versus quality per strategy; p95 latency per strategy; per-backend queue length, GPU use and tokens per second; breaker state; request success rate. TODO: wireframes of the dashboards; whether any operator interface beyond configuration files is wanted.

### 3.6.7 Security and Privacy Design

- Client authentication by API keys (FR-17, ASSUMPTION). Provider keys held as environment secrets, never in code or logs (NFR-10).
- Input validation on every request before any backend is called; request size limit (TODO value).
- Raw prompts are not logged by default; the log stores a hash (NFR-11, ASSUMPTION). Benchmark prompts are public, but prompts sent by a real user may contain personal data, so the Nigeria Data Protection Act 2023 applies in that case [CITE: Nigeria Data Protection Act 2023].
- Transport security between client and gateway and between gateway and backends: TODO (depends on deployment).
- Sending prompts to a hosted provider shares them with that provider. The operator must be able to restrict sensitive prompts to self-hosted backends. ASSUMPTION: a configuration flag per backend; not in the proposal.

## 3.7 Data Collection and Preparation

The project uses public benchmarks, not collected data [D-07]. Everything about the datasets beyond their names is **TODO: confirm from the benchmark papers before writing**.

| Item | Content |
|---|---|
| Datasets | RouterBench and MT-Bench [D-07]. Chatbot Arena is named in the proposal's literature base [SRC-07]; whether it is used as a data source is TODO. |
| Source, size, features, licence, date | TODO for each: from the benchmark papers and repositories. Do not estimate. |
| Whether per-prompt, per-model quality scores and costs are provided | TODO. This decides whether routing decisions can be replayed offline without calling every model, or whether live calls are needed. ASSUMPTION: offline replay for classifier and cost-versus-quality results; live calls for latency, load and failure experiments. |
| Quality labels | Preference-based labels are noisy [R-02]. Report uncertainty as confidence intervals, not a single number. |
| Cleaning and preprocessing | TODO: de-duplicate prompts; remove prompts that overflow a model's context; fix text encoding. |
| Features | Prompt embedding from sentence-transformers; token counts; task type [D-01]. |
| Split | ASSUMPTION: train, validation and test split by prompt with a fixed seed; weights tuned on validation only; test touched once. |
| Generalisation test | Train on one model pair and test on another, for at least two pairs [R-01]. Which pairs: TODO. |
| Class balance | TODO: report the share of "easy" and "hard" labels; handle imbalance if material. |

## 3.8 Tools and Technologies

Names and purposes are from the proposal [D-01 to D-07]. Versions are TODO until the environment is fixed (replication needs them: NFR-14).

**Table 3.3: Tools and technologies**

| Tool / technology | Purpose | Justification |
|---|---|---|
| Python | Implementation language for the gateway, classifier and scoring function | The scoring function is custom Python [D-04]; ecosystem for the classifier |
| FastAPI | Asynchronous gateway exposing one OpenAI-compatible endpoint | Async Python framework suited to many concurrent calls [D-03] |
| sentence-transformers | Turns the prompt text into vectors | Cheap features computed before the call [D-01] |
| scikit-learn (logistic regression) | Difficulty and task-type classifier | Small, fast classifier, adds little latency [D-01] |
| vLLM | Self-hosted GPU model serving; source of queue, GPU and throughput signals | Runs open models efficiently; exposes the metrics the router reads [D-02, D-03] |
| Ollama | Local model serving | Simple local backend [D-03] |
| Hosted LLM APIs | Pay-per-token backends | Strong models without own hardware [Figure 1]. TODO: providers |
| Prometheus | Collects live metrics from vLLM | Standard metrics collector [D-02] |
| Redis | Shared live state and health counts | Fast in-memory store shared by gateway instances [D-05] |
| Grafana | Dashboards for cost, quality, latency | Visual comparison against baselines [D-07] |
| RouterBench, MT-Bench | Public benchmarks | Common ground for comparing routers and answer quality [D-07] |
| Circuit-breaker pattern | Pause traffic to repeatedly failing backends | Standard resilience pattern [D-05] |

Tools not yet chosen (TODO): load generator for concurrent requests; unit and integration test framework; container and orchestration setup; version control hosting and CI; reference manager (the template suggests Zotero or Mendeley); GPU hardware and hosted-API budget.

## 3.9 Evaluation Plan

**Strategies compared** (same prompts, same hardware, same time window where possible):

| Code | Strategy | Purpose |
|---|---|---|
| S1 | Always-strong | Quality and cost reference [D-07] |
| S2 | Always-weak | Cost floor and quality floor [D-07] |
| S3 | Load-blind router: classifier and score without live load | Isolates the effect of live load [R-03] |
| S4 | Load-aware router: the full design | The proposed system |
| S5 (optional) | Cascade (cheap first, then escalate) | Tests gap G6. TODO-confirm-with-supervisor; not in the proposal's plan |

**Testing strategy** (template 3.9): unit tests for classifier, scoring and circuit breaker; integration tests with real and mocked backends; system tests of the full flow; failure-injection and load tests; acceptance against Table 3.1 and Table 3.2 with the test IDs in Table 4.2. TODO-confirm-with-supervisor: the proposal has no user study, and the template's usability section (System Usability Scale, at least 20 participants) is aimed at user-facing systems. Decide whether a small developer-usability check of the API and dashboards is required or marked not applicable.

**Table 3.6: Evaluation plan by objective**

| Objective | Question | Metric (scale) | Data and setting | Baseline | Hypothesis | Reported in |
|---|---|---|---|---|---|---|
| O1 | RQ1 | Requirement coverage; traceability of tests to FR IDs | Tables 3.1, 3.2 | n/a | none | 4.5.3, Table 4.2 |
| O2 | RQ2 | Functional test pass rate (ratio); p95 router overhead, ms (ratio) | Unit, integration, system tests; load test | Direct call to a backend | none | 4.5, 4.6.5 |
| O3 | RQ3 | Routing accuracy (ratio) with 95% CI per model pair | RouterBench, held-out and cross-pair | Best constant policy | H0/H1 of RQ3 | 4.6.1 |
| O4 | RQ4 | p95 latency, ms (ratio); also mean latency | Load generator at low and high concurrency against vLLM | S3 load-blind | H0/H1 of RQ4 | 4.6.3 |
| O5 | RQ5 | Request success rate (ratio); added latency, ms | Failure injection: stop or slow a backend for a period | Router without fallback | H0/H1 of RQ5 | 4.6.4 |
| O6 | RQ6 | Mean cost per request (ratio); mean quality score; p95 latency | RouterBench and MT-Bench | S1, S2 (and S3) | H0a/H1a, H0b/H1b of RQ6 | 4.6.2 |

**Variables (course module).**

| Role | Variable | Scale |
|---|---|---|
| Independent | Routing strategy (S1 to S4) | Nominal |
| Dependent | Cost per request | Ratio (currency unit TODO) |
| Dependent | Answer quality score | ASSUMPTION: treated as continuous; depends on how each benchmark scores (TODO verify) |
| Dependent | p95 latency | Ratio (ms) |
| Dependent | Request success rate | Ratio (proportion) |
| Dependent | Routing accuracy | Ratio (proportion) |
| Moderating | Load level (low, high; or concurrency) | Ordinal, or ratio if concurrency |
| Extraneous | Provider variability and time of day; prompt length; hardware differences | Controlled by running strategies on the same prompts and hardware in the same window and by fixing seeds |

**Statistics (ASSUMPTION).** Significance level 0.05. Uncertainty reported with 95% bootstrap confidence intervals, in line with the proposal's wish to report uncertainty rather than a single number [R-02]; paired comparisons on the same prompts. Number of repeated runs: TODO. Random seeds fixed and recorded. Multiple-comparison handling for the two hypotheses in RQ6: TODO-confirm-with-supervisor.

**Numeric targets.** Not set [E-01]. TODO-confirm-with-supervisor, before any test is run: targets for NFR-01 to NFR-06 and the margin δ. Recording the agreement date protects against changing targets after seeing results.

### 3.9.1 Anticipated risks and threats to validity

Carried forward to Section 4.8.

| Threat or risk | Type | Handling |
|---|---|---|
| Classifier trained on one model pair generalises poorly [R-01] | External validity | Test on more than one model pair before trusting it |
| Noisy preference-based quality labels [R-02] | Construct validity | Public benchmarks; report confidence intervals |
| Little prior work on live-load routing [R-03] | Gap not confirmed by literature | Compare directly with the load-blind variant S3; state honestly if Chapter Two finds more prior work |
| Competitors change [R-04] | Relevance of the gap | Re-check LiteLLM and OpenRouter docs before submission |
| Benchmarks are not production traffic (ASSUMPTION) | External validity | State the limit; do not claim production savings |
| Hosted-API latency varies with provider load and time (ASSUMPTION) | Internal validity | Interleave strategies in time; repeat runs; report spread |
| Quality scoring of MT-Bench may rely on a model as judge (ASSUMPTION: verify how it is scored) | Construct validity | Read the benchmark paper; discuss judge bias if applicable |
| Small GPU capacity limits load tests (ASSUMPTION) | Conclusion validity | Record hardware; state the load range tested |
| Overfitting weights to the test data | Conclusion validity | Tune on validation only; touch test once |

## 3.10 Ethical Considerations

- **Human participants:** none planned [proposal]. Consent forms are not needed unless interviews or a user study are added (see 3.2 and 3.9). TODO-confirm-with-supervisor: whether department ethical approval is still required for a project without human participants.
- **Data:** public benchmark data only; check each licence and cite it [D-07]. No personal data is collected. If real prompts are ever used, apply the Nigeria Data Protection Act 2023, store hashes not text, and anonymise [CITE: Nigeria Data Protection Act 2023].
- **Third-party services:** sending benchmark prompts to hosted providers must follow each provider's terms of use (ASSUMPTION: to check). Provider keys are kept secret (NFR-10).
- **Research integrity:** targets agreed before testing; results reported as measured, including failures; replication package shared (module: replicability and objectivity).
- **Generative AI:** any use is declared in the front matter table.

## 3.11 Chapter Summary

TODO: one or two paragraphs once the chapter is final. Content to cover: Design Science Research with three iterations tied to the three phases; requirements from the existing-solutions review; a pipeline of classifier, scoring engine, live state, backends and resilience; a linear scoring function with hard latency budget and circuit breaker; public benchmarks with always-strong, always-weak and load-blind baselines; and an evaluation plan with hypotheses and uncertainty reporting.
