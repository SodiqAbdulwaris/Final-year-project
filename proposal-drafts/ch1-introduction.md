# CHAPTER ONE: INTRODUCTION (draft)

**Drafting notes (delete before pasting into the template)**

- Tense: future, because this is the proposal stage. Switch to past tense for the final report (template rule).
- Facts come only from `00-source-facts.md` (IDs in square brackets, for example [P-01], are for the team; delete them when pasting).
- `[CITE: topic]` marks a claim that needs a verified citation. The literature-review notes in `literature-review/` will supply them. No statistic is stated in this chapter because none is available yet.
- `TODO:` is information only the team or supervisor can supply. `ASSUMPTION:` is a choice made by the drafter.
- Template target length: 6 to 10 pages. This draft is a skeleton with full wording where the facts allow it.

---

This chapter introduces the AI Request Router project. It sets out the background of the study, states the problem as the gap between how large language model requests are handled today and how they ought to be handled, gives the aim, objectives and research questions, summarises the methodology, and describes the significance, scope, limitations and contributions of the project. It ends with an outline of the report and the definition of the operational terms.

## 1.1 Background of the Study

**Paragraph 1: the broad domain (general).** Large language models (LLMs) are now offered as services that software teams call through an application programming interface, and many organisations use more than one of them [CITE: growth and adoption of LLM services; pricing and model diversity]. The available models differ widely in price, answer quality and speed, and they can be run in two ways: on a provider's servers with pay-per-token pricing, or on the organisation's own graphics processing units (GPUs) with serving software [CITE: hosted versus self-hosted LLM serving]. [P-07, D-03]

**Paragraph 2: what teams do today (narrowing).** In practice, teams often hard-code one model into their application [P-01]. This is simple, but it has costs. Sending every request to one large model wastes money, because easy requests do not need that capacity [P-02]. Sending every request to one small model saves money but lowers answer quality on hard requests [P-03]. A single hard-coded model also gives the application latency spikes when that model is busy, and no way to carry on when it fails [P-04]. [CITE: evidence that cost, latency and availability differ across LLM providers and models]

**Paragraph 3: routing as a response.** One response is request routing, where a layer in front of the models decides which model should answer each request. Research has proposed learned routers that choose between a strong and a weak model, cascades that try a cheap model first and escalate, and benchmarks to compare them [CITE: FrugalGPT; RouteLLM; Hybrid LLM; RouterBench; MT-Bench; Chatbot Arena. Names only in the proposal, authors and years to be verified] [SRC-05, SRC-07]. In industry, gateway products offer one interface to many models, with fallbacks and load balancing [CITE: OpenRouter provider-routing documentation; LiteLLM routing and load-balancing documentation; Martian] [SRC-01, SRC-02, SRC-06]. These vendor documents are grey literature and will be cited as such.

**Paragraph 4: the setting (Nigeria and Nile University).** TODO: write this paragraph only if evidence is found, otherwise delete it. The template asks the background to narrow to the specific setting, but the proposal contains no Nigerian or Nile University facts and none are invented here. A possible angle, to be tested against sources before use, is whether cost and the ability to use self-hosted GPUs matter more for teams in the project's setting [CITE: Nigerian software and AI adoption, for example from NITDA or a peer-reviewed study]. ASSUMPTION: this angle is the drafter's idea, not the proposal's.

**Paragraph 5: the exact issue.** Within this landscape, the documentation reviewed by the team shows each tool solving one slice of the problem. In the proposal's reading, none chooses the model per prompt, watches the live load of the backends, and also runs on the user's own GPUs [S-01 to S-05; the claim stays VERIFY until the documents are re-read]. The project addresses that combination. The solution itself is described in Chapter Three, not here.

## 1.2 Statement of the Problem

**What is.** Applications that use more than one LLM usually fix the model choice in code [P-01, P-07]. As a result, requests of very different difficulty are sent to the same model, so money is wasted on easy requests or quality is lost on hard ones [P-02, P-03], and traffic does not react to how busy a backend is or to a backend failing [P-04]. The tools that could help each cover part of the need. One gateway chooses between providers of a model the caller has already named. Another spreads load across copies of a named model, and its newer complexity-based router, by the documents reviewed, does not mention live load, queue depth, GPU use or per-request latency budgets. A research router picks between two models only, with no live load, latency budget or failover. Cascades pay the latency of every failed attempt. Commercial routers are closed [S-01 to S-05]. TODO: add measured evidence (for example price and latency figures for a hard-coded setup, or a small pilot). The proposal has none, and the module rules say every figure must come from a cited, verifiable source.

**What ought to be.** Each request ought to be answered by the model that gives the quality it needs at the lowest cost, within the latency the caller can accept, with the decision adapting to how busy each backend is right now, with the request moving to another backend when one fails, and with the router able to work across both hosted services and the organisation's own GPU servers [P-04, D-01 to D-06].

**The gap and its consequences.** The gap is the absence of a single, inspectable routing layer that decides per prompt, uses live backend load, respects a latency budget, handles failure, and runs on self-hosted infrastructure, together [P-06; R-03]. Developers and organisations running more than one LLM bear the consequences: avoidable spending, lower quality on hard requests, latency spikes under load and outages with no fallback [P-04, P-07]. The proposal also notes that runtime-aware routing is thin in the literature [R-03], a point Chapter Two will test against the reviewed papers and may or may not confirm.

This project therefore seeks to design, implement and evaluate a request router that scores each prompt for difficulty, weighs predicted quality, cost and live backend load, and sends the request to the best hosted or self-hosted model with failover.

> **Problem-statement check (course module):** the problem is the measurable gap above, not the topic "LLM routers". Independent variable: routing strategy (single fixed model, difficulty-only routing, load-aware routing). Dependent variables: cost per request, answer quality, p95 latency, request success rate. Extraneous variable: backend load at test time. All four dependent variables are on a ratio scale. See Section 3.9 for the full variable table.

## 1.3 Aim and Objectives

**Aim.** To design, implement and evaluate an AI Request Router that selects the most suitable hosted or self-hosted large language model for each request, using prompt difficulty, predicted quality, cost, live backend load and a latency budget, with failover, for developers and organisations running more than one LLM.

**Objectives.** Each objective begins with an action verb and maps to a project phase [SC-01 to SC-03]. "Time-bound" uses the phase end, because the proposal sets no dates. TODO: replace each "(TODO date)" once the team confirms the schedule.

| No. | Objective | Phase | Measure of success |
|---|---|---|---|
| O1 | To specify the functional and non-functional requirements of the router, and design its architecture and scoring algorithm using UML models, before implementation starts (TODO date). | Start of Phase 1 | Requirement tables with IDs and priorities (Tables 3.1, 3.2) agreed with the supervisor; numeric targets agreed [E-01]. |
| O2 | To implement a FastAPI gateway that exposes one OpenAI-compatible endpoint over hosted APIs, Ollama and vLLM backends, by the end of Phase 1 (TODO date). | Phase 1 | All Must-priority functional requirements for the gateway pass their test cases; the added latency of the decision step is measured and reported (p95, in ms). |
| O3 | To develop a prompt classifier from sentence embeddings and logistic regression that scores difficulty and task type, and to determine its routing accuracy on at least two model pairs from RouterBench, by the end of Phase 1 (TODO date). | Phase 1 | Routing accuracy with a 95% confidence interval per model pair; target TODO-confirm-with-supervisor [E-01, E-04, R-01]. |
| O4 | To implement a scoring function that combines predicted quality, cost and latency with live queue length, GPU use and tokens per second, and to compare load-aware with load-blind routing on p95 latency, by the end of Phase 2 (TODO date). | Phase 2 | p95 latency of load-aware versus load-blind routing under the same load; target TODO-confirm-with-supervisor [R-03]. |
| O5 | To implement retry on the next-best backend with a circuit breaker, and to evaluate request success rate under injected backend failures, by the end of Phase 2 (TODO date). | Phase 2 | Success rate and added latency with and without fallback; target TODO-confirm-with-supervisor. |
| O6 | To compare the router against always-strong and always-weak baselines on cost, quality and p95 latency using RouterBench and MT-Bench, by the end of Phase 3 (TODO date). | Phase 3 | Cost-versus-quality and p95 latency results with uncertainty; targets TODO-confirm-with-supervisor [E-02, E-03, D-07]. |

**SMART check (for the supervisor; delete before submission)**

| Objective | Specific | Measurable | Achievable | Relevant | Time-bound |
|---|---|---|---|---|---|
| O1 | One document set | Tables signed off | Documents only | Feeds all others | TODO date |
| O2 | One endpoint, three backend types | Test pass rate; p95 overhead | ASSUMPTION: feasible if a GPU server is available (TODO hardware) | Phase 1 of the proposal | TODO date |
| O3 | One classifier | Routing accuracy with CI | Public benchmark data | Answers the "easy vs hard prompt" gap | TODO date |
| O4 | One scoring function, one comparison | p95 latency | Needs a load generator (TODO tool) | Core difference from existing routers | TODO date |
| O5 | One fallback mechanism | Success rate | Failures can be injected | Gap "failures and slow providers" | TODO date |
| O6 | Two baselines, two benchmarks | Cost, quality, p95 | Public benchmarks | Gap "unproven savings" | TODO date |

**Traceability (template requires it).**

| Objective | Chapter 3 section | Chapter 4 section | Research question | Gap in Table 2.4 |
|---|---|---|---|---|
| O1 | 3.2, 3.5, 3.6 | 4.5.3 (Table 4.2 links tests to FR IDs) | RQ1 | all |
| O2 | 3.4, 3.6.1 | 4.2, 4.4, 4.6.5 | RQ2 | G3 |
| O3 | 3.6.5, 3.7 | 4.6.1 | RQ3 | G1 |
| O4 | 3.6.5, 3.9 | 4.6.3 | RQ4 | G2, G4 |
| O5 | 3.6.1, 3.6.5 | 4.6.4 | RQ5 | G5 |
| O6 | 3.9 | 4.6.2 | RQ6 | G6, G7 |

## 1.4 Research Questions

One question per objective, phrased as what, how or to what extent. Hypotheses are stated where the objective makes a testable claim. Numeric margins are TODO until the supervisor agrees the targets [E-01].

**RQ1 (O1).** What functional and non-functional requirements must a request router meet to serve hosted and self-hosted LLM backends from one endpoint?
No hypothesis (descriptive).

**RQ2 (O2).** How can hosted APIs, Ollama and vLLM servers be placed behind one OpenAI-compatible endpoint, and to what extent does the routing decision add to end-to-end latency?
No hypothesis. The overhead is reported against the target in Table 3.2 (TODO).

**RQ3 (O3).** To what extent can a sentence-embedding and logistic-regression classifier predict the right model for a prompt, and how well does it hold up on a model pair it was not trained on?
- H0: The classifier's routing accuracy is no higher than that of the best constant policy (always-strong or always-weak) on held-out data.
- H1: The classifier's routing accuracy is higher than that of the best constant policy on held-out data.
- ASSUMPTION: "right model" is defined as the cheapest model whose benchmark quality score on the prompt is within a tolerance of the best model's score. The proposal does not define it [E-04]. TODO-confirm-with-supervisor: definition and tolerance.

**RQ4 (O4).** To what extent does adding live load signals to the scoring function reduce p95 latency compared with load-blind routing under the same load?
- H0: The p95 latency of load-aware routing is not lower than that of load-blind routing.
- H1: The p95 latency of load-aware routing is lower than that of load-blind routing.

**RQ5 (O5).** How does retry on the next-best backend with a circuit breaker change the request success rate and latency when a backend fails?
- H0: Request success rate under injected backend failure is the same with and without fallback.
- H1: Request success rate under injected backend failure is higher with fallback.

**RQ6 (O6).** To what extent does the router lower cost relative to always-strong routing while keeping quality close to it, and raise quality relative to always-weak routing, on RouterBench and MT-Bench?
- H0a: Mean cost per request of the router is not lower than that of always-strong routing.
- H1a: Mean cost per request of the router is lower than that of always-strong routing.
- H0b: Mean quality of the router is lower than that of always-strong routing by δ or more.
- H1b: Mean quality of the router is lower than that of always-strong routing by less than δ.
- TODO-confirm-with-supervisor: the margin δ and how quality is scored on each benchmark.

Significance level and tests are in Section 3.9 (ASSUMPTION: 0.05, with bootstrap confidence intervals, because the proposal asks for uncertainty to be reported and sets no level).

## 1.5 Methodology Overview

The project will use Design Science Research as the research approach, because it builds an artefact (the router) and evaluates it against stated criteria, with an iterative, incremental development model across the three phases: gateway and classifier, resilience and load awareness, and benchmarking [SC-01 to SC-03]. ASSUMPTION: the proposal names no methodology; this is the drafter's choice, to be confirmed with the supervisor [CITE: Design Science Research methodology]. The router will be built in Python with FastAPI, sentence-transformers and scikit-learn for the classifier, vLLM and Ollama for self-hosted serving, Prometheus and Redis for live state and health, and Grafana for dashboards [D-01 to D-07]. It will be evaluated on the public benchmarks RouterBench and MT-Bench against always-strong and always-weak baselines and a load-blind variant, using cost, quality, p95 latency, routing accuracy and request success rate, reporting uncertainty rather than single numbers [E-02 to E-04, R-02, D-07]. Full details are in Chapter Three.

## 1.6 Significance of the Study

**Practical significance.** The router will help developers and organisations that run more than one LLM spend less on easy requests, protect quality on hard ones, and keep the application running when a backend is slow or down [P-07, D-01 to D-05]. Because it is planned to run on the user's own GPUs as well as hosted APIs, it also gives teams that self-host a way to use that capacity before paying a provider [D-03]. For students and the University, it gives a documented, reproducible reference implementation. TODO: add a University or Nigeria-specific benefit only if it is supported by evidence.

**Academic significance.** The project will measure, directly and against a load-blind baseline, whether live load signals improve routing, which the proposal describes as thin in the literature [R-03]. It will also test whether a classifier-based router generalises across more than one model pair [R-01]. Neither claim is assumed here: Chapter Two checks the first against the literature, and Chapter Four reports what the measurements show. No result is promised.

## 1.7 Scope of the Study

**Included.**
- One OpenAI-compatible gateway endpoint over hosted APIs, Ollama and vLLM backends [SC-01].
- A prompt classifier for difficulty and task type, and a scoring function over predicted quality, cost and latency, with a per-request latency budget [SC-01, D-01, D-04].
- Fallback with a circuit breaker, and live queue, GPU and throughput signals from vLLM through Prometheus [SC-02].
- Benchmark comparison with always-strong and always-weak baselines on RouterBench and MT-Bench [SC-03].
- Target users: developers and organisations running more than one LLM [P-07].

**Excluded.**
- Building or training the language models. The router only chooses between existing ones [SC-04].
- ASSUMPTION: text chat requests only (no image, audio or other modalities); the proposal does not say.
- ASSUMPTION: no end-user graphical interface. The proposal lists a gateway and Grafana dashboards only.
- ASSUMPTION: no production deployment for real customers during the project.

**Platform, setting and time frame.** Server-side service in Python. TODO: institutional setting and duration. TODO: which hosted providers, which self-hosted models and what GPU hardware, because these set the real boundary of the evaluation [see 00-source-facts, TBD 7 and 8].

## 1.8 Limitations of the Study

| Limitation | Why it matters | Planned mitigation |
|---|---|---|
| Routers trained on one model pair may generalise poorly [R-01] | Results on one pair may not hold for others | Test the classifier on more than one model pair from RouterBench before trusting it |
| Quality labels from preference data are noisy [R-02] | The "right model" label is uncertain, which limits routing accuracy | Use public benchmarks and preference data; report uncertainty (confidence intervals), not one number |
| Little prior work on live-load routing [R-03] | Fewer papers to compare against | Treat it as the project's gap and measure it directly against load-blind routing |
| Competitors are changing quickly [R-04] | LiteLLM's Auto Router now routes by complexity, so the claimed difference may narrow | Re-check the LiteLLM and OpenRouter documentation before submission |
| ASSUMPTION: benchmark prompts are not real production traffic | External validity | State this in Section 4.8; do not claim production-level savings |
| ASSUMPTION: limited GPU capacity and API budget | Number of backends and test volume are capped | TODO: record the real hardware and budget; design tests that fit them |

## 1.9 Contributions of the Project

These match the objectives (template rule).

1. A written requirements and design specification for a load-aware LLM request router (O1).
2. A working OpenAI-compatible gateway over hosted, Ollama and vLLM backends (O2).
3. A prompt classifier for difficulty and task type, with measured routing accuracy across more than one model pair (O3).
4. A scoring function that combines predicted quality, cost and latency with live load and a latency budget, with a direct load-aware versus load-blind comparison (O4).
5. A fallback and circuit-breaker mechanism with measured effect on success rate (O5).
6. A comparative evaluation against always-strong and always-weak baselines on RouterBench and MT-Bench, with a replication package (code, configuration, benchmark scripts) for reproducibility (O6). ASSUMPTION: the team will publish the replication package; confirm.

## 1.10 Organisation of the Report

Chapter One introduces the study. Chapter Two reviews the literature on routing algorithms, prompt difficulty, load balancing, cost reduction, latency, fallback, benchmarking and gateway design, compares existing systems, and states the research gap. Chapter Three describes the research and development methodology, the requirements, the system design including the scoring algorithm, the tools, the evaluation plan and the ethical considerations. Chapter Four will report the implementation, testing and results, and discuss them against the objectives. Chapter Five will summarise the project, state how far each objective was achieved, and give conclusions, limitations, recommendations and future work.

## 1.11 Definition of Operational Terms

Alphabetical. Definitions are as used in this project. Where the proposal gives a definition it is used; other entries are the drafter's wording (ASSUMPTION) and should be checked.

| Term | Meaning in this project |
|---|---|
| Always-strong baseline | A policy that sends every request to one fixed large, high-quality model. Used as the quality and cost reference [D-07]. |
| Always-weak baseline | A policy that sends every request to one fixed small, cheap model. Used as the other reference [D-07]. |
| Backend | Any model endpoint the router can call: a hosted API, an Ollama server or a vLLM server. |
| Circuit breaker | A pattern that temporarily stops sending traffic to a backend that keeps failing, and tries it again later [D-05]. |
| Difficulty score | The classifier's estimate of how hard a prompt is, used to predict which models can answer it well [D-01]. |
| Fallback (failover) | Retrying a failed request on the next-best backend [D-05, F-04]. |
| Gateway | The single service that receives every client request and applies routing [D-03]. |
| Hosted API | A model provider's service billed per token [Figure 1]. |
| Large language model (LLM) | A neural language model that generates text from a prompt. [CITE: standard definition] |
| Latency budget | An optional maximum acceptable response time that the caller attaches to a request [Figure 1, D-04]. |
| Live load | The current queue length, GPU use and tokens per second of a self-hosted server, plus health and failure counts [D-02, F-03]. |
| Load-aware routing / load-blind routing | Routing that does / does not use live load when scoring backends. |
| OpenAI-compatible endpoint | An HTTP interface that accepts the same request format as the OpenAI chat API, so existing client code can use it without change [D-03]. ASSUMPTION: the exact endpoints supported are fixed in Chapter Three. |
| p95 latency | The response time that 95 percent of requests beat [D-07]. |
| Prompt classifier | The model that turns a prompt into a difficulty score and task type before a backend is chosen [D-01]. |
| Quality (predicted) | The expected answer quality of a model on a given prompt, estimated before the call. Measured quality uses benchmark scores. |
| Request router | The layer that sends each incoming LLM request to the best backend by cost, quality and latency [M-06]. |
| Routing accuracy | How often the classifier picks the right model [E-04]. Operational definition is TODO-confirm-with-supervisor (see RQ3). |
| Scoring function | The function that combines predicted quality, cost and latency (and live load) into one score per backend [D-04]. |
| Self-hosted model | A model run on the organisation's own hardware with vLLM or Ollama. |

Tool terms from the proposal, for reference: sentence-transformers turns text into numbers; scikit-learn logistic regression is a small, fast classifier; vLLM is a server that runs open models efficiently; Prometheus collects metrics; Ollama runs models locally; FastAPI is a Python framework for the asynchronous gateway; Redis is a fast in-memory store for shared health state [D-01 to D-05].
