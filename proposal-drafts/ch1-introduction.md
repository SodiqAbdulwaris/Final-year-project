# CHAPTER ONE: INTRODUCTION (draft, reworked to follow the 26 Oct team guide)

**Drafting notes (delete before pasting into the template)**

- **Governing design.** This draft follows the 26 Oct 2026 team guide where it conflicts with the 16 Oct proposal (supervisor decision, user to confirm). See `design-reconciliation.md`. Unresolved conflicts are marked `DECISION-NEEDED`. The proposal's verified facts are still recorded in `00-source-facts.md` (IDs such as [P-01] below refer to it); the guide's content is cited as "the team guide" and is not in the fact file.
- Tense: future (proposal stage). Switch to past tense for the final report (template rule).
- Citations are APA 7 author-date and every one has an entry in `literature-review/references.md`. `[CITE: topic]` marks a claim with no verified source yet (for example statistics about LLM usage, or Nigeria). `[CITE-09: ...]` and `[CITE-10: ...]` mark work from the literature-review topics 09 (retrieval, k-NN and multi-turn routing) and 10 (context and memory), whose overviews and `references.md` entries were not available when this draft was written. Where two first authors share a surname, initials are added (APA 7): L. Chen, S. Chen, D. Jiang, H. Jiang, H. Li, K. Lu, Y. Lu, Z. Huang, L. Huang, Z. Li, B. Li. The survey by Varangot-Reille et al. is cited as 2026a because a second 2026 paper by the same first author is in topic 09.
- `TODO:` is information only the team or supervisor can supply. `ASSUMPTION:` is a choice made by the drafter. Numeric margins and targets stay unset (the guide says a margin must be justified and approved before test data are examined).
- Template target length: 6 to 10 pages.

---

This chapter introduces the AI Request Router project. It sets out the background, states the problem as the gap between how requests for large language models are handled today and how they ought to be handled, gives the aim, six objectives, research questions and hypotheses, summarises the methodology, and describes the significance, scope, limitations and contributions. It ends with an outline of the report and the definition of the operational terms.

## 1.1 Background of the Study

**Paragraph 1: the broad domain.** Large language models (LLMs) are now used as services that software teams call through an application programming interface, and many teams use more than one of them [CITE: growth and adoption of LLM services; pricing and model diversity]. The models differ in price, answer quality and speed, and they can be run in two ways: on a provider's servers with pay-per-token pricing, or on the team's own hardware with serving software. Serving LLMs is expensive because of heavy computation and memory use (Miao et al., 2025), and the cost of self-hosting depends on which GPUs are used and how requests are shaped (Griggs et al., 2024). Public benchmarks record both quality and price for many models, which shows how widely they differ (Hu et al., 2024), and crowd-sourced platforms rank models by human preference (Chiang et al., 2024). [P-07]

**Paragraph 2: what teams do today.** Teams often hard-code one model into their application [P-01]. This is simple, but sending every request to one large model wastes money, sending everything to a small one lowers quality, and a single hard-coded model gives no way to carry on when that model is slow or fails [P-02 to P-04]. Evidence from the provider side shows that the failures that matter are often degradations rather than outages: degraded latency was the largest incident category in one study of production incidents in generative-AI cloud services (Yan et al., 2025).

**Paragraph 3: routing as a response.** One response is request routing, where a layer in front of the models decides which model should answer each request. Research has proposed learned routers that choose between a strong and a weak model with an adjustable threshold (Ding et al., 2024; Ong et al., 2025), cascades that try a cheap model first and escalate (L. Chen et al., 2024), and surveys that organise the field (Moslem & Kelleher, 2026; Varangot-Reille et al., 2026a). Benchmarks make the approaches comparable, and they also show a sobering pattern: simple baselines are hard to beat. RouterBench found its k-nearest-neighbour and neural routers barely above a trivial one (Hu et al., 2024), and LLMRouterBench found many routers, including commercial ones, not reliably better than the best single model (H. Li et al., 2026). A line of work estimates a model's competence on a new request from the outcomes of similar past requests, which needs no router training and accepts new models without retraining [CITE-09: Varangot-Reille et al., 2026 (EACL 2026 Student Research Workshop); Tang et al., 2026 (preprint)]. In multi-turn use, routing each turn separately can switch models often; work on turn-level routing for agent tasks reports cost savings from switching selectively [CITE-09: Zhang et al., 2026 (MTRouter)].

**Paragraph 4: gateways.** In industry, gateway products and open-source projects already provide one interface to many models, with authentication, budgets, fallbacks, retries and load balancing; some now route automatically by prompt complexity or learned preference (vendor documentation reviewed in Section 2.5). Implementing these features alone is therefore not a novelty claim (team guide). What remains less clear is how well a *simple, inspectable* competence estimate, controlled model switching and a bounded context policy perform together when budgets are enforced and local models are first-class backends, and how such a gateway should be engineered and verified as software.

**Paragraph 5: the setting (Nigeria and Nile University).** TODO: write this paragraph only if evidence is found, otherwise delete it. The template asks the background to narrow to the specific setting, but neither the proposal nor the team guide contains Nigerian or Nile University facts and none are invented here. A possible angle, to be tested against sources before use, is whether cost and the ability to use local models matter more for teams in the project's setting [CITE: Nigerian software and AI adoption, for example from NITDA or a peer-reviewed study]. ASSUMPTION: this angle is the drafter's idea.

**Paragraph 6: the exact issue.** The project addresses the integration and evaluation of these ideas in one budget-aware gateway for hosted and locally served models: eligibility filtering, a validated competence estimate with an uncertainty margin, budget enforcement before dispatch, controlled switching, and failover. The solution itself is described in Chapter Three.

## 1.2 Statement of the Problem

**What is.** Applications that use more than one LLM usually fix the model choice in code [P-01, P-07]. Requests of very different difficulty then go to the same model, so money is wasted on easy requests or quality is lost on hard ones [P-02, P-03], and traffic does not adapt when a backend is slow or fails [P-04]. Published routers are evaluated mostly offline, on replayed benchmark outputs, and the reviewed work reports competence estimates without checking whether they are calibrated, and does not describe a rule for deciding when evidence is too thin to trust [CITE-09; Hu et al., 2024; H. Li et al., 2026]. The literature on routing under budgets, switching between turns of one session, and carrying conversation context across a switch is thin, and most of it is very recent [CITE-09; CITE-10]. Gateway features such as budgets and fallbacks exist in products but are documented as engineering practice, and the evidence that they hold under concurrent requests and failures is not published in the reviewed papers (vendor documentation; see Chapter Two). TODO: add measured evidence for the local setting (for example price and latency figures for a hard-coded setup, or a small pilot). Neither the proposal nor the guide has any, and the module rules say every figure must come from a cited, verifiable source.

**What ought to be.** Each request ought to be answered by the cheapest, lowest-latency model deployment that is *eligible* (it has the needed capabilities, fits the context, is healthy, is allowed by privacy policy and is affordable) and whose estimated chance of success, with an allowance for uncertainty, meets an agreed quality target. A router ought never to silently violate a guaranteed quality threshold, ought to enforce spending limits before a request is sent (even under concurrent load), ought to switch models inside a conversation only when the expected benefit justifies it, and ought to preserve the context a follow-up needs. It ought to work across hosted APIs and locally served models through one OpenAI-compatible interface, and it ought to be built and verified as dependable software. (team guide, sections 3, 5 and 9)

**The gap and its consequences.** To our knowledge, no peer-reviewed system and none of the products reviewed in Chapter Two combines a learned per-prompt quality estimate, live queue and GPU signals from self-hosted servers, per-request latency budgets, failover, and hosted-plus-self-hosted backends in one OpenAI-compatible gateway. Recent preprints and open-source routers cover parts of this combination, notably RouteBalance (Da & Kalyvianaki, 2026) and the vLLM Semantic Router (vendor documentation). The project therefore does not claim to be first. Its gap is narrower: it is unclear, on evidence, whether a simple k-NN competence estimate with an uncertainty lower bound beats simple rules at the same budget, whether controlled session switching saves cost without material quality loss, how much history a new model needs after a switch, whether budgets hold under concurrency and failure, and whether such a gateway is dependable and usable for developers. Developers and organisations running more than one LLM, hosted or local, bear the consequences: avoidable spending, lower quality on hard requests, unpredictable latency and outages with no fallback [P-04, P-07]. Live backend load as a routing input, the project's earlier main idea, is now a secondary, optional extension (`design-reconciliation.md`, item 3).

This project therefore seeks to design, implement and evaluate a budget-aware request router for hosted and locally served LLMs and to determine, with controlled experiments, whether k-NN competence estimation, controlled model switching and a bounded context policy improve the cost–quality–latency trade-off, reporting negative results as readily as positive ones.

> **Problem-statement check (course module).** The problem is the measurable gap above, not the topic "LLM routers". Independent variables: routing method (static cheapest eligible, domain-average rule, k-NN; optionally a classifier), switching policy (locked, free per turn, hysteresis) and context policy (full replay, bounded, retrieval). Dependent variables: success at a given cost, total cost, calibration of success estimates, session cost and switches, p50 and p95 time to first token, context accuracy and evidence recall, budget overshoot, and gateway overhead. Extraneous variables: provider caching, cold starts, prices at test time. See Section 3.9 for the variable table.

## 1.3 Aim and Objectives

**Aim.** To design, implement and evaluate a budget-aware request router, exposed as one OpenAI-compatible gateway, that selects among three to four candidate hosted or local LLM deployments using hard eligibility filtering, k-NN competence estimates with an uncertainty lower bound, cost budget bands and session-aware switching, with bounded retries and a circuit breaker, for developers who call hosted or local LLM APIs.

**Objectives.** The numbering follows the team guide's research questions (RQ1 to RQ3) and experiments (E1 to E5). "Time-bound" uses the guide's nine-step build order (Section 3.1 of Chapter 3) because no dates are set. TODO: replace each "(TODO date)".

| No. | Objective | Experiment | Build step | Measure of success |
|---|---|---|---|---|
| O1 | To determine whether k-NN competence estimation over past per-model outcomes gives a better cost–quality trade-off than rule-based routing at the same budgets, on held-out tasks from RouterBench and LLMRouterBench, and whether its success estimates are calibrated, by step 6 (TODO date). | E1 | 5 to 6 | Success at matched cost (or cost at matched success), with 95% paired intervals and raw counts; reliability table and Brier score; share of requests with insufficient evidence. Primary metric and margin: `DECISION-NEEDED`. |
| O2 | To determine whether session-aware hysteresis reduces session cost and model switches without material quality loss compared with locked and per-turn routing on scripted multi-turn sessions, by step 7 (TODO date). | E2 | 7 | Mean cost per completed session, switch count, success, p50 and p95 TTFT, as paired differences with bootstrap intervals; non-inferiority margin δ (TODO-confirm-with-supervisor). |
| O3 | To determine how much conversation history a model needs after a switch by comparing full replay, bounded history and text or vector retrieval (and, only if simpler methods fall short, a graph), by step 7 (TODO date). | E3 | 7 | Context accuracy, evidence recall, temporal correctness, tokens and total cost against the same context-token allowance. |
| O4 | To implement cost budget bands with atomic reservation and reconciliation, and verify that spending limits hold under concurrent requests and backend failures, by step 8 (TODO date). | E4 | 3 to 4, 8 | Zero requests exceeding the declared reservation limits in the pass/fail assertions; measured overshoot; rejected requests; reconciliation failures. |
| O5 | To implement hosted and local OpenAI-compatible adapters with bounded retries and a circuit breaker, and measure gateway overhead and behaviour under injected faults, by step 8 (TODO date). | E5 | 2, 8 | Proxy overhead (gateway minus direct TTFT), p95 latency and completion rate; timeout, circuit-breaker and fallback rules verified under slow response, 429, connection failure, malformed output and mid-stream disconnect. |
| O6 | To elicit requirements from at least five developers, specify them with MoSCoW priorities and a traceability matrix by step 1 (TODO date), and evaluate software quality (ISO/IEC 25010 table, at least 80% line coverage) and usability (System Usability Scale, preferably at least eight participants) by step 9 (TODO date). | none (SE evaluation) | 1, 8, 9 | Requirements with IDs and acceptance criteria; every Must requirement has a passing test or experiment; quality table with targets fixed before measurement; SUS mean with an interval and task measures. |

**Optional extension X1 (not an objective).** If time allows, feed registry-level health, latency and queue estimates, and vLLM `/metrics` when a server exposes it, into the router and compare with a load-blind variant. `DECISION-NEEDED`: whether X1 is a stated goal or dropped (design-reconciliation item 3).

**SMART check (for the supervisor; delete before submission)**

| Objective | Specific | Measurable | Achievable | Relevant | Time-bound |
|---|---|---|---|---|---|
| O1 | One comparison, two datasets | Success at matched cost, intervals | Public data with per-model outcomes (licences to check) | RQ1, the main research question | step 6, TODO date |
| O2 | One policy comparison | Cost, switches, success, TTFT | Scripted sessions; pilot first | RQ2 | step 7, TODO date |
| O3 | Three or four context builders | Accuracy, recall, tokens | Small controlled corpus | RQ3; graph arms conditional | step 7, TODO date |
| O4 | One ledger design | Pass/fail assertions, overshoot | Mock provider | Spending correctness is a stated risk | step 8, TODO date |
| O5 | One gateway, two engine types | Overhead, completion under faults | ASSUMPTION: needs one local engine and a hosted key (TODO hardware, budget) | Local models are first class | step 8, TODO date |
| O6 | Requirements, quality, usability | Interviews at least 5; coverage at least 80%; SUS | Needs participants and consent (TODO) | Project is assessed as software engineering | steps 1, 8, 9, TODO dates |

**Traceability (template requires it).** Chapter 3 and Chapter 4 section numbers are as in the drafts.

| Objective | Chapter 3 section | Chapter 4 section | Research question | Gap in Table 2.4 |
|---|---|---|---|---|
| O1 | 3.6.5 (competence estimate, selection rule), 3.7, 3.9.2 (E1) | 4.6.1 | RQ1 | R1, L3, L6 |
| O2 | 3.6.5 (hysteresis), 3.9.3 (E2) | 4.6.2 | RQ2 | R2 |
| O3 | 3.6.5 (context policies), 3.9.4 (E3) | 4.6.3 | RQ3 | R3 |
| O4 | 3.6.5 (budget ledger), 3.9.5 (E4) | 4.6.4 | RQ4 | R4 |
| O5 | 3.6.1, 3.6.5 (failover), 3.9.6 (E5) | 4.6.5 | RQ5 | R5, L7 |
| O6 | 3.2, 3.5, 3.9.7 | 4.5 | RQ6 | R6 |

## 1.4 Research Questions

One question per objective, phrased as what, how or to what extent. Hypotheses are the guide's H1 to H3; E4 and E5 are descriptive verification and have none. All margins are TODO until the supervisor approves them, and the guide's rule applies: declare the primary metric, comparison and margin before examining results.

**RQ1 (O1, E1).** Does k-NN model-competence estimation produce a better cost–quality trade-off than simple rules under the same budgets? (Guide wording; recast for the template as "To what extent does k-NN competence estimation improve the cost–quality trade-off over simple rules at the same budget?")
- H0: At comparable total cost on held-out tasks, k-NN routing with the uncertainty lower bound does not achieve higher success than the domain-average rule.
- H1: k-NN routing achieves higher success at a comparable spending level on held-out, representative tasks.
- Secondary (exploratory, labelled as such): calibration of the success estimates, share of insufficient evidence, behaviour with 10%, 25%, 50% and 100% of the training records, and an optional classifier comparator.

**RQ2 (O2, E2).** To what extent does controlled session switching reduce cost and latency without material quality loss?
- H0: Hysteresis does not reduce session cost and model switches relative to per-turn routing, or its session success is lower by the margin δ or more.
- H1: Hysteresis uses fewer switches and less session cost than per-turn routing while meeting the predeclared non-inferiority margin δ on success.
- TODO-confirm-with-supervisor: δ (the guide gives 3 percentage points only as a placeholder).

**RQ3 (O3, E3).** How much conversation history is necessary after model switching?
- H0: A bounded, explicit context policy does not reduce tokens relative to full replay, or loses required facts or task success by more than the agreed margin.
- H1: A bounded, explicit context policy reduces tokens while preserving required facts and task success within the agreed margin.
- Graph retrieval arms are optional and exploratory.

**RQ4 (O4, E4).** To what extent do budget bands and atomic reservation keep spending within declared limits under concurrent requests and backend failures? Descriptive: no hypothesis; assertions and measured overshoot.

**RQ5 (O5, E5).** What overhead does the gateway add to hosted and local backends, and how does it behave under injected faults? Descriptive: no hypothesis; repeated measurements with intervals.

**RQ6 (O6).** What requirements do developers who call hosted or local LLM APIs place on a budget-aware gateway, and to what extent does the implemented system meet its quality targets and usability expectations? Descriptive.

Evaluation rules (guide section 5): keep validation and test data separate; compare methods on the same tasks or sessions; report 95% intervals with raw counts; separate meaningful, small and inconclusive findings; claim non-inferiority only when the lower bound of the quality difference lies above the negative margin; confirmatory tests are limited to H1 to H3; a rejected hypothesis is a valid outcome. Section 3.9 gives the experiments.

## 1.5 Methodology Overview

The project will use Design Science Research with an iterative, incremental build following the guide's nine-step order, and will evaluate the artefact with five experiments. ASSUMPTION: the guide names no methodology; Design Science plus iterative development is the drafter's choice, to be confirmed with the supervisor [CITE: Design Science Research methodology]. The router will be one modular FastAPI application with a relational database, generic OpenAI-compatible adapters for hosted APIs and local engines (Ollama, LM Studio, llama.cpp server, vLLM), and no Redis, graph database or microservices until a measured need appears (team guide, section 10). Routing combines hard eligibility filters, k-NN competence estimates built from public per-model outcome records (RouterBench, LLMRouterBench), a lower-bound rule, budget bands with atomic reservation, and session-aware hysteresis. Evaluation uses offline replay for selection decisions (E1, E2, E3) and live tests on controlled local and hosted endpoints for latency, streaming, budgets and failures (E4, E5), plus requirements interviews, an ISO/IEC 25010 quality table, automated tests and a System Usability Scale study. Full details are in Chapter Three.

## 1.6 Significance of the Study

**Practical significance.** The project will give developers and organisations that run more than one LLM a way to spend less on easy requests, protect quality on hard ones, enforce spending limits, and keep working when a backend is slow or down, with local models treated as first-class backends. It will also give students and the University a documented, reproducible reference design with a traceability matrix and a usability study. TODO: add a University or Nigeria-specific benefit only if it is supported by evidence.

**Academic significance.** The project will test, on real model outcomes and with paired intervals, whether a simple past-performance estimate with an uncertainty margin is competitive with simple rules, whether hysteresis helps in multi-turn sessions, and how much context a switch requires. These questions are open in the reviewed literature (Chapter Two), but no result is assumed. The project's contribution is architectural integration and controlled evaluation, not a new routing method, and negative results are reported as findings.

## 1.7 Scope of the Study

**Included.**
- One OpenAI-compatible gateway (`/v1/chat/completions`, text chat and server-sent-event streaming first) over hosted APIs and local engines.
- Model and deployment registry; hard eligibility filtering; rule-based and k-NN routers; budget bands with atomic reservation; bounded retries and a circuit breaker; decision logs.
- Session-aware hysteresis; optional router-managed sessions; context policies C0 to C2 (graph arms C3a and C3b conditional).
- Experiments E1 to E5, a requirements study, a quality and testing evaluation and a usability study.
- Three or four candidate models or deployments (TODO: which).
- Target users: developers and organisations that call hosted or local LLM APIs.

**Excluded (team guide, section 10).**
- Training or fine-tuning foundation models.
- Portable KV-cache transfer across different models.
- Distributed GPU scheduling and managing inference-engine installation.
- Online reinforcement learning or bandit exploration.
- A general-purpose agent framework.
- Automatic LLM-generated temporal graphs on every live request.

**Optional or deferred.** Live-load signals (X1), a learned difficulty classifier as an E1 comparator, graph memory (E3 arms C3a and C3b), tool calling and structured output (only if needed and verified).

**Platform, setting and time frame.** Server-side Python service. TODO: institutional setting, duration, hardware (the guide warns against loading several models on an 8 GB GPU), hosted-API budget.

## 1.8 Limitations of the Study

| Limitation | Why it matters | Planned mitigation |
|---|---|---|
| k-NN success averages may be miscalibrated, and neighbours are not independent trials | An uncalibrated estimate can break a quality guarantee | Reliability table and Brier score on validation data; uncertainty margin that shrinks with effective neighbours; recalibrate only if needed (E1) |
| Thin evidence in sparse regions of the task space, and no history for a new model | Estimates are noisy or absent | Minimum-evidence rule; unknown is never treated as good; new models are marked unvalidated until scored (E1 new-model test) |
| Benchmark labels contain flaws, and routers are evaluated on replayed outputs [CITE-09] | The "right model" label is uncertain and offline results do not capture live behaviour | Use public data with objective checks where possible, blinded adjudication where feasible; run E4 and E5 live |
| Provider caching, cold starts and pricing change over time | Cost and latency results may not repeat | Record versions, pricing snapshots and conditions; test warm and cold cases; report as measured |
| Live sessions are not perfectly counterfactual | Model-generated outputs change later turns | Use scripted sessions and recorded outputs first; analyse live runs separately (E2) |
| The guide's synthetic simulation is not evidence | Its probabilities are invented | Not used as results; real experiments only |
| Small samples for the pilot and usability study | Intervals may be wide | Size from observed variability; report inconclusive results as inconclusive; usability is formative |
| ASSUMPTION: limited GPU capacity and hosted-API budget | Number of models and test volume are capped | TODO: record real hardware and budget; design tests that fit them |
| Competitors change quickly (proposal risk R-04) | The comparison in Chapter Two may date | Re-fetch vendor documentation before submission |

## 1.9 Contributions of the Project

These match the objectives.

1. A calibrated-estimate evaluation of k-NN competence routing against simple rules, on public per-model outcome data, with paired intervals and an honest negative-result route (O1).
2. A measured test of session-aware hysteresis against locked and per-turn switching (O2).
3. A measured comparison of context policies after a model switch, with graph retrieval tested only if simpler methods fall short (O3).
4. A budget ledger with atomic reservation and reconciliation, verified under concurrency and failure (O4).
5. A working OpenAI-compatible gateway over hosted and local backends with bounded retries, a circuit breaker and fault-injection results (O5).
6. A requirements specification with traceability, a quality table, an automated test suite and a usability study, and a replication package of code, configuration and experiment scripts (O6). ASSUMPTION: the team will publish the replication package; confirm.

## 1.10 Organisation of the Report

Chapter One introduces the study. Chapter Two reviews the literature in ten themes: routing algorithms, prompt difficulty, load balancing, cost reduction, latency, fallback, benchmarking, system and gateway design, retrieval and multi-turn routing, and conversation context and memory. It also compares existing systems and states the research gap. Chapter Three describes the methodology, requirements, system design, the algorithms, the tools, the five experiments and the software-engineering evaluation, and the ethical considerations. Chapter Four will report implementation, testing and results. Chapter Five will summarise the project, state how far each objective was achieved, and give conclusions, limitations, recommendations and future work.

## 1.11 Definition of Operational Terms

Alphabetical. Definitions are as used in this project. Where the guide or proposal defines a term it is used (marked [G] guide, [P] proposal); other entries are the drafter's wording (ASSUMPTION) and should be checked.

| Term | Meaning in this project |
|---|---|
| Ablation | Comparing a complete method with versions missing one feature to see whether that feature helps [G]. |
| Always-strong and always-weak baselines | Policies that send every request to one fixed large or one fixed small model, used as quality and cost references [P]. |
| Atomic reservation | Reserving the maximum estimated spend in the budget ledger in one indivisible step before a request is sent, so concurrent requests cannot jointly exceed a cap [G]. |
| Backend, deployment | A deployment is a specific running copy or API endpoint serving a model. The same model can have several deployments with different speed and availability [G]. |
| Budget band | One of three configurable policy presets (Economy, Balanced, Quality) with request, session and project caps. The numeric caps are configuration, not the meaning of the band [G]. |
| Calibration | Whether predicted success rates match observed ones: among tasks predicted at about 0.8, roughly 80% succeed [G]. |
| Circuit breaker | A pattern that temporarily stops sending traffic to a backend that keeps failing and tries it again later [P]. |
| Competence estimate | An estimate of whether a specific model can succeed on a specific task, used instead of a global difficulty label [G]. |
| Context | Relevant earlier messages, instructions and tool results needed to answer a follow-up. It is not the model's internal attention cache [G]. |
| Eligibility filter | Hard requirements a deployment must pass before ranking: capabilities, context fit, health, privacy and data-location policy, and affordable upper cost [G]. |
| Gateway | The single service that receives every client request and applies routing, budget and session policy [P, G]. |
| Hysteresis | A rule that prevents changing models for a tiny apparent benefit: the expected improvement must exceed a threshold, with exceptions for hard failure or capability change [G]. |
| k-NN (k-nearest neighbours) | Finding the k most similar previously scored tasks and using their per-model outcomes to estimate a model's success on a new task [G]. |
| Lower bound (success lower bound) | The competence estimate minus an uncertainty margin that grows when evidence is thin; compared with the quality target instead of the raw average [G]. |
| Minimum-evidence rule | Requiring at least a tuned number of sufficiently similar scored neighbours before an estimate is trusted; below it the estimate is unknown [G]. |
| Non-inferiority margin | The largest quality loss accepted in exchange for lower cost or latency, fixed and justified before looking at results [G]. |
| OpenAI-compatible endpoint | An HTTP interface that accepts the same request format as the OpenAI chat API, so existing client code works unchanged [P]. |
| p95 latency | The response time that 95 percent of requests beat [P]. |
| Request router | The layer that sends each incoming LLM request to a backend by cost, quality and latency [P]. |
| Session affinity | A preference for staying on the same model during a conversation [G]. |
| SUS (System Usability Scale) | A standard 10-question usability questionnaire scored 0 to 100 [G]. |
| TTFT | Time to first token: how long before the first generated token arrives; end-to-end latency is the time until the response completes [G]. |
