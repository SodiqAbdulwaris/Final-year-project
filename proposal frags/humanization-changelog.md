Status: DRAFT
Depends on: Proposal_Working_Draft_v2.docx; Proposal_Working_Draft_v2_Humanized.docx
Sources: Humanizer 12B (Q4_K_M) samples; edits by Claude Sonnet 5.5
Open items: team to read every change before adopting the humanized copy

# Humanization change log

One entry per changed chunk (a chunk is one paragraph, or about 85 words of a longer one). Bold lead-ins, citations, numbers, identifiers and tense were checked programmatically for every entry. Chunks not listed here are unchanged.

## Chunk 119.0 (paragraph 119)

**Before**

Applications that use large language models (LLMs) can reach them through hosted services or locally run models, and these options differ in price, response time, capability and availability. Sending every request to one fixed model ignores these differences, and routing studies that compare methods offline on stored outputs do not show whether a working system enforces budget, capability and privacy limits or recovers when a model fails.

**After**

Applications built on large language models (LLMs) can reach them through hosted services or locally run models, and the two differ in price, response time, capability and availability. Sending every request to one fixed model ignores those differences. Routing studies that compare methods offline on stored outputs also leave open whether a working system enforces budget, capability and privacy limits, or recovers when a model fails.

## Chunk 119.1 (paragraph 119)

**Before**

For Nigerian developers, dollar-priced services and rules on moving personal data abroad make the choice more consequential. This project will design, implement and evaluate a prompt-aware request-routing gateway that selects an eligible hosted or local model for each request under quality, cost, latency and privacy constraints, with bounded fallback, using health tracking and circuit breakers, when a model fails. The work will follow an iterative development approach.

**After**

For Nigerian developers, dollar-priced services and rules on moving personal data abroad make the choice more consequential. This project will design, implement and evaluate a prompt-aware request-routing gateway. For each request, the gateway will select an eligible hosted or local model under quality, cost, latency and privacy constraints. When a model fails, it will fall back in a bounded way, using health tracking and circuit breakers. The work will follow an iterative development approach.

## Chunk 119.2 (paragraph 119)

**Before**

The gateway will first remove models that fail hard requirements, then use lightweight task classification and similarity to previously scored requests to estimate how well each remaining model suits the request, and choose the cheapest model that meets the quality and deadline requirements. Development will reuse public scored benchmark outputs where licences allow, run small local models on two RTX 4070 laptops and cap hosted calls. The hybrid approach will be compared with fixed-model, cheapest-eligible, rule-based and simpler learned routers, with each component tested by ablation.

**After**

The gateway will first remove models that fail hard requirements. It will then use lightweight task classification and similarity to previously scored requests to estimate how well each remaining model suits the request, and choose the cheapest model that meets the quality and deadline requirements. Development will reuse public scored benchmark outputs where licences allow, run small local models on two RTX 4070 laptops and cap hosted calls. The hybrid approach will be compared with fixed-model, cheapest-eligible, rule-based and simpler learned routers, and each component will be tested by ablation.

## Chunk 119.3 (paragraph 119)

**Before**

Evaluation will measure quality, cost, latency, calibration, constraint violations, gateway overhead and request completion under injected failures, with the protocol fixed before the held-out results are examined. At this proposal stage no results exist. The expected outputs are a requirements specification, a deployed gateway, a documented comparison and reproducible evaluation evidence. A simpler router that matches the hybrid will be an acceptable finding, so the study can show when added routing intelligence is worth its overhead.

**After**

Evaluation will measure quality, cost, latency, calibration, constraint violations, gateway overhead and request completion under injected failures, and the protocol will be fixed before the held-out results are examined. No results exist at this proposal stage. The expected outputs are a requirements specification, a deployed gateway, a documented comparison and reproducible evaluation evidence. A simpler router that matches the hybrid will count as an acceptable finding, because the study can then show when added routing intelligence is worth its overhead.

## Chunk 208 (paragraph 208)

**Before**

This chapter introduces the project. It gives the background to the choice of a large language model (LLM) for each request, states the problem the project addresses and sets out the aim, objectives and research questions. It then summarises the methodology, significance, scope, limitations and expected contributions, defines the key terms and describes how the rest of the report is organised.

**After**

This chapter introduces the project. It starts with the background to choosing a large language model (LLM) for each request, then states the problem, the aim, the objectives and the research questions. The remaining sections summarise the methodology, significance, scope, limitations and expected contributions, define the key terms and outline how the report is organised.

## Chunk 210 (paragraph 210)

**Before**

Large language models (LLMs) are increasingly used in applications that answer questions, summarise documents and assist with software development. This use is part of a wider rise in the adoption of artificial intelligence (AI). The 2025 Stanford AI Index reported that 78% of surveyed respondents said their organisations used AI in 2024, compared with 55% in 2023, and that the share reporting generative AI use in at least one business function rose from 33% to 71% over the same period (Stanford Institute for Human-Centered Artificial Intelligence, 2025). These figures describe the organisations in the survey. They do not show what share of all organisations run LLMs in production.

**After**

Large language models (LLMs) now appear in applications that answer questions, summarise documents and help with software development, as part of a wider rise in the adoption of artificial intelligence (AI). The 2025 Stanford AI Index reported that 78% of surveyed respondents said their organisations used AI in 2024, up from 55% in 2023, and that the share reporting generative AI use in at least one business function rose from 33% to 71% over the same period (Stanford Institute for Human-Centered Artificial Intelligence, 2025). Those figures describe the organisations in the survey, so they cannot show what share of all organisations run LLMs in production.

## Chunk 211.0 (paragraph 211)

**Before**

Developers reach LLMs either through hosted application programming interfaces (APIs) or by running models on their own hardware. The models differ in price, response time and capability. One model may perform well on a hard task but cost much more per request, while another may be cheaper and adequate for easy tasks but unreliable on difficult ones. Chen et al. (2024) examined how to choose among LLM APIs that differ in price and performance so as to reduce cost without losing quality.

**After**

Developers reach LLMs either through hosted application programming interfaces (APIs) or by running models on their own hardware, and the models differ in price, response time and capability. One may handle a hard task well but cost much more per request; another may be cheaper and adequate for easy tasks yet unreliable on difficult ones. Chen et al. (2024) examined how to choose among LLM APIs that differ in price and performance so as to reduce cost without losing quality.

## Chunk 211.1 (paragraph 211)

**Before**

Prices also change over time. The AI Index reported that the cost of querying a model that scored at GPT-3.5 level on the Massive Multitask Language Understanding (MMLU) benchmark fell from $20 per million tokens in November 2022 to $0.07 in October 2024 (Stanford Institute for Human-Centered Artificial Intelligence, 2025). That comparison holds at one benchmark score only. It does not mean the cheaper models are equally capable on every task.

**After**

Prices also change over time. The AI Index reported that the cost of querying a model that scored at GPT-3.5 level on the Massive Multitask Language Understanding (MMLU) benchmark fell from $20 per million tokens in November 2022 to $0.07 in October 2024 (Stanford Institute for Human-Centered Artificial Intelligence, 2025). That holds for one benchmark score only, and it does not mean the cheaper models are equally capable on every task.

## Chunk 212.0 (paragraph 212)

**Before**

A common practice is to send every request to one fixed model. This keeps configuration simple, but a short question and a long multi-step task receive the same treatment. Research on routing asks whether the model can instead be chosen for each request. Hybrid LLM routes each query to a smaller or a larger model according to predicted quality (Ding et al., 2024), and RouteLLM uses human preference data to choose between a stronger and a weaker model, aiming to cut cost while keeping response quality acceptable (Ong et al., 2025).

**After**

A common practice is to send every request to one fixed model. That keeps configuration simple, but a short question and a long multi-step task receive the same treatment. Routing research asks whether the model can be chosen for each request instead. Hybrid LLM sends each query to a smaller or a larger model according to predicted quality (Ding et al., 2024), and RouteLLM uses human preference data to choose between a stronger and a weaker model, aiming to cut cost while keeping response quality acceptable (Ong et al., 2025).

## Chunk 212.1 (paragraph 212)

**Before**

Their results show that routing can help under the conditions tested. They do not guarantee a benefit for every application.

**After**

Both results show that routing can help under the conditions tested, but neither guarantees a benefit for every application.

## Chunk 213 (paragraph 213)

**Before**

Response time is another concern. A model that looks suitable on quality and price may be slow or overloaded when a request arrives. Da and Kalyvianaki (2026) studied model selection together with the load on the available model instances in a heterogeneous serving setting. They showed that quality, cost and latency interact, so a choice made without regard to the state of the deployment can cause delays. Their evaluation covers one serving environment and may not transfer to every mix of hosted and local models.

**After**

Response time is another concern. A model that looks suitable on quality and price may still be slow or overloaded when a request arrives. Da and Kalyvianaki (2026) studied model selection together with the load on the available model instances in a heterogeneous serving setting, and showed that quality, cost and latency interact: a choice made without regard to the state of the deployment can cause delays. Their evaluation covers one serving environment, so it may not transfer to every mix of hosted and local models.

## Chunk 214 (paragraph 214)

**Before**

In Nigeria, these choices sit within a national effort to develop and use AI. The National Artificial Intelligence Strategy names AI infrastructure, adoption, responsible development and governance among its priorities (Federal Ministry of Communications, Innovation and Digital Economy, 2025). The strategy sets the policy context. It does not report how much Nigerian software teams spend on LLM services or what difficulties they meet most often.

**After**

In Nigeria, these choices sit within a national effort to develop and use AI. The National Artificial Intelligence Strategy names AI infrastructure, adoption, responsible development and governance among its priorities (Federal Ministry of Communications, Innovation and Digital Economy, 2025). It sets the policy context but does not report how much Nigerian software teams spend on LLM services or what difficulties they meet most often.

## Chunk 215.0 (paragraph 215)

**Before**

Two Nigerian conditions make the choice of model more than a technical detail. The first is the exchange rate. Hosted LLM services are usually priced in US dollars, so a change in the naira–dollar exchange rate changes what a Nigerian team pays in naira even when the provider’s dollar price stays the same. That rate does not stay fixed: the African Development Bank (2026) reported that the naira appreciated by about 5.9% against the US dollar in 2025, so the naira cost of a dollar-priced service changes from year to year.

**After**

Two Nigerian conditions make the choice of model more than a technical detail. The first is the exchange rate. Hosted LLM services are usually priced in US dollars, so a change in the naira–dollar exchange rate changes what a Nigerian team pays in naira even when the provider’s dollar price stays the same. The rate does move: the African Development Bank (2026) reported that the naira appreciated by about 5.9% against the US dollar in 2025, so the naira cost of a dollar-priced service changes from year to year.

## Chunk 215.1 (paragraph 215)

**Before**

How large the effect is for a given application depends on its provider, usage and payment arrangements, and evidence from Nigerian organisations would be needed to measure it. The second condition is privacy. A request sent to a provider outside Nigeria may carry personal data, and sections 41 to 43 of the Nigeria Data Protection Act, 2023 set conditions for transferring such data abroad, including an adequate level of protection or another basis allowed by the Act (Federal Republic of Nigeria, 2023).

**After**

How large the effect is for a given application depends on its provider, usage and payment arrangements, and measuring it would need evidence from Nigerian organisations. The second condition is privacy. A request sent to a provider outside Nigeria may carry personal data, and sections 41 to 43 of the Nigeria Data Protection Act, 2023 set conditions for transferring such data abroad, including an adequate level of protection or another basis allowed by the Act (Federal Republic of Nigeria, 2023).

## Chunk 215.2 (paragraph 215)

**Before**

Whether these sections apply depends on what data is sent, where it is processed and how the transfer is arranged. A local deployment can change where processing happens, but it does not remove the duty to protect personal data.

**After**

Whether these sections apply depends on what data is sent, where it is processed and how the transfer is arranged. A local deployment can change where processing happens, but the duty to protect personal data remains.

## Chunk 216 (paragraph 216)

**Before**

Availability and fit also matter. A hosted endpoint can fail or reject a request, and a local model depends on the hardware that runs it. An application tied to one endpoint cannot complete a request when that endpoint fails. If another deployment takes over, it must still meet the request’s own limits. A substitute chosen only because it is available may break a budget, a capability need or a privacy restriction. These are operating conditions that must be tested alongside quality and cost.

**After**

Availability and fit also matter. A hosted endpoint can fail or reject a request, and a local model depends on the hardware that runs it. An application tied to one endpoint cannot complete a request when that endpoint fails. If another deployment takes over, it must still meet the request’s own limits, because a substitute chosen only for being available may break a budget, a capability need or a privacy restriction. These operating conditions have to be tested alongside quality and cost.

## Chunk 217 (paragraph 217)

**Before**

Existing work supplies methods and benchmarks for parts of this problem. RouterBench stores model outputs and provides a framework for comparing routing strategies on cost and performance (Hu et al., 2024). Offline comparison of this kind lets different policies be tested on the same data. It does not reproduce the network delays, provider outages and failures an application meets in live operation.

**After**

Existing work supplies methods and benchmarks for parts of this problem. RouterBench stores model outputs and provides a framework for comparing routing strategies on cost and performance (Hu et al., 2024). Offline comparison of this kind lets different policies be tested on the same data, but it does not reproduce the network delays, provider outages and failures an application meets in live operation.

## Chunk 218 (paragraph 218)

**Before**

The problem this project addresses is therefore how to choose, for each request, an LLM deployment that is permitted and suitable when quality, cost, latency and privacy requirements must be weighed together, and what should happen when the chosen deployment fails or no permitted alternative remains. The benefit and the overhead of any routing approach need to be measured against simpler choices under defined test conditions. They should not be assumed from the existence of several models.

**After**

The problem this project addresses is therefore how to choose, for each request, an LLM deployment that is permitted and suitable when quality, cost, latency and privacy requirements must be weighed together, and what should happen when the chosen deployment fails or no permitted alternative remains. The benefit and the overhead of any routing approach need to be measured against simpler choices under defined test conditions; neither can be assumed from the mere existence of several models.

## Chunk 220 (paragraph 220)

**Before**

Many applications send every request to one fixed model. A fixed choice is a useful baseline, but it cannot adapt to the request, even though deployments differ in cost, latency, capability and availability (Section 1.1). Learned routing and cascading are already studied (Chen et al., 2024; Ding et al., 2024; Ong et al., 2025), so implementing model selection alone would not be a research contribution. Most comparisons of routing methods are also made offline on stored outputs (Hu et al., 2024), which cannot show whether a working system enforces its constraints and recovers from failures. Nigerian teams meet two further pressures: dollar-priced services and rules on moving personal data abroad.

**After**

Many applications send every request to one fixed model. A fixed choice is a useful baseline, but it cannot adapt to the request, although deployments differ in cost, latency, capability and availability (Section 1.1). Learned routing and cascading are already studied (Chen et al., 2024; Ding et al., 2024; Ong et al., 2025), so implementing model selection alone would not be a research contribution. Most comparisons of routing methods are also made offline on stored outputs (Hu et al., 2024), and those cannot show whether a working system enforces its constraints and recovers from failures. Nigerian teams face two further pressures: dollar-priced services and rules on moving personal data abroad.

## Chunk 221 (paragraph 221)

**Before**

A request should reach a model that can process it, is available and is affordable under the declared policy. Among the feasible candidates, selection should account for estimated quality and latency. Hard capability, budget and privacy restrictions should still apply during recovery. When no permitted action remains, the client should receive an explicit infeasibility or execution error, not an apparently successful response that silently breaks a restriction.

**After**

A request should reach a model that can process it, is available and is affordable under the declared policy. Among the feasible candidates, selection should weigh estimated quality and latency, and the hard capability, budget and privacy restrictions should keep applying during recovery. When no permitted action remains, the client should receive an explicit infeasibility or execution error rather than a response that looks successful but silently breaks a restriction.

## Chunk 222 (paragraph 222)

**Before**

Without a controlled comparison, additional predictor components may add overhead without useful savings, and successful offline routing may hide unreliable execution. The people affected are developers and organisations that integrate several LLM deployments, including Nigerian teams with limited budgets. This project investigates whether combining lightweight classification and embedding-derived suitability features with constrained cost–quality–latency selection improves on simpler routing baselines. Operational fallback is evaluated separately for resilience. The contribution will be the decision policy, its integration into a working gateway and an empirical evaluation. No claim of being the first or a fundamentally new algorithm will be made.

**After**

Without a controlled comparison, extra predictor components may add overhead without useful savings, and successful offline routing may hide unreliable execution. The people affected are developers and organisations that integrate several LLM deployments, including Nigerian teams with limited budgets. This project investigates whether combining lightweight classification and embedding-derived suitability features with constrained cost–quality–latency selection improves on simpler routing baselines, and it evaluates operational fallback separately for resilience. Its contribution will be the decision policy, its integration into a working gateway and an empirical evaluation. It will make no claim to be the first of its kind or a fundamentally new algorithm.

## Chunk 233 (paragraph 233)

**Before**

Each objective yields a specified artefact and a measurable comparison. No objective requires a positive result: a simpler method that matches the hybrid is a reportable outcome. Numeric targets are set in Section 3.9 and may be revised after a pilot only with a recorded reason and before the held-out results are examined.

**After**

Each objective yields a specified artefact and a measurable comparison. None of them requires a positive result: a simpler method that matches the hybrid is a reportable outcome. Numeric targets are set in Section 3.9 and may be revised after a pilot, but only with a recorded reason and before the held-out results are examined.

## Chunk 242 (paragraph 242)

**Before**

The quality comparison will use a margin and scoring protocol fixed before the held-out results are examined. Cost and latency changes will be measured, not assumed. Chapter Three sets out the hypotheses, metrics and sample selection.

**After**

The quality comparison will use a margin and scoring protocol fixed before the held-out results are examined. Cost and latency changes will be measured rather than assumed. Chapter Three sets out the hypotheses, metrics and sample selection.

## Chunk 244 (paragraph 244)

**Before**

The project will follow an iterative artefact-development and controlled-evaluation approach. Requirements will be extracted from the project design, the application scenarios and the reviewed literature. A minimal gateway with validation, a deployment registry and model adapters will be built first. Fixed-model, cheapest-eligible and rule-based policies will give the initial comparisons before the learned components are added. The integrated gateway will then be deployed in a documented environment, and functional, integration and failure-handling tests will check it against its requirements.

**After**

The project will follow an iterative approach that combines artefact development with controlled evaluation. Requirements will be drawn from the project design, the application scenarios and the reviewed literature. A minimal gateway with validation, a deployment registry and model adapters will be built first, and fixed-model, cheapest-eligible and rule-based policies will give the initial comparisons before the learned components are added. The integrated gateway will then be deployed in a documented environment, where functional, integration and failure-handling tests will check it against its requirements.

## Chunk 245.0 (paragraph 245)

**Before**

Already-scored outputs from RouterBench and LLMRouterBench will be considered for offline predictor development and replay evaluation (Hu et al., 2024; Li et al., 2026). Their versions, model coverage, task overlap and licence conditions will be checked before use. Requests will be split into training, validation and test sets, and evaluated outcomes will be kept out of the retrieval index used to route those requests. The hybrid predictor will combine task classification with embedding-derived features, and ablations will isolate the value of each.

**After**

Already-scored outputs from RouterBench and LLMRouterBench will be considered for offline predictor development and replay evaluation (Hu et al., 2024; Li et al., 2026). Their versions, model coverage, task overlap and licence conditions will be checked before use. Requests will be split into training, validation and test sets, and evaluated outcomes will be kept out of the retrieval index used to route those requests. The hybrid predictor will combine task classification with embedding-derived features, and ablations will isolate the value of each.

## Chunk 245.1 (paragraph 245)

**Before**

Deterministic eligibility filtering will come before selection, and the selector will prefer the cheapest feasible model. A capped live pilot and controlled failure injection on local models will measure latency, gateway overhead and fallback behaviour, which replayed outputs cannot show. Results will report quality, cost, latency, calibration, constraint violations and fallback completion with uncertainty intervals where the sample allows, and all tuning will precede the held-out analysis.

**After**

Deterministic eligibility filtering will come before selection, and the selector will prefer the cheapest feasible model. A capped live pilot and controlled failure injection on local models will measure latency, gateway overhead and fallback behaviour, which replayed outputs cannot show. Results will report quality, cost, latency, calibration, constraint violations and fallback completion, with uncertainty intervals where the sample allows. All tuning will precede the held-out analysis.

## Chunk 247 (paragraph 247)

**Before**

For developers, the project will provide a common interface to hosted and local models, with controls over eligibility, budgets and recovery. The gateway will record why a candidate was excluded or chosen and how recovery proceeded, which supports debugging without keeping raw sensitive prompts in routine logs. For Nigerian teams paying in dollars or handling personal data, an explicit policy layer makes cost and data-location choices visible. These benefits depend on implementation and testing, and the project does not assume that every application will save money.

**After**

For developers, the project will provide a common interface to hosted and local models, with controls over eligibility, budgets and recovery. The gateway will record why a candidate was excluded or chosen and how recovery proceeded, which supports debugging without keeping raw sensitive prompts in routine logs. For Nigerian teams paying in dollars or handling personal data, an explicit policy layer makes cost and data-location choices visible. These benefits depend on implementation and testing, and the project does not assume that every application will save money.

## Chunk 248 (paragraph 248)

**Before**

The project will connect requirements, design decisions, tests and experiments for an AI-dependent service, and will evaluate budget accounting, failure handling and privacy restrictions as software behaviours. It will provide a controlled comparison of the hybrid approach against its own simpler components and will report the cost of feature extraction and selection next to any inference savings. A competitive simple baseline or an inconclusive comparison will still show which design is appropriate. The findings will apply to the models, workloads and deployments tested.

**After**

The project will connect requirements, design decisions, tests and experiments for an AI-dependent service, and it will evaluate budget accounting, failure handling and privacy restrictions as software behaviours. It will compare the hybrid approach under control with its own simpler components and report the cost of feature extraction and selection next to any inference savings. If a simple baseline proves competitive or the comparison is inconclusive, that will still show which design is appropriate. The findings will apply to the models, workloads and deployments tested.

## Chunk 250 (paragraph 250)

**Before**

The study covers the requirements, design, implementation, deployment, testing and evaluation of a request-level LLM routing gateway. The target users are developers and organisations that integrate several LLM deployments. The work will be carried out at the Department of Software Engineering, Nile University of Nigeria, within the timeframe of the final-year project.

**After**

The study covers the requirements, design, implementation, deployment, testing and evaluation of a request-level LLM routing gateway. The target users are developers and organisations that integrate several LLM deployments. The work will be carried out at the Department of Software Engineering, Nile University of Nigeria, within the timeframe of the final-year project.

## Chunk 251 (paragraph 251)

**Before**

The core gateway will provide a documented API, request validation, a configurable deployment registry, deterministic capability, context-window, budget and availability filters, lightweight task classification, model-suitability prediction, constrained selection, hosted and local adapters, circuit breakers, bounded operational fallback, and request and decision logging with basic monitoring. The evaluated pool will contain three to four models, chosen from models covered by public scored benchmark data, spanning a small or cheap option, a mid-tier option and a frontier option. Embedding similarity is included as a component whose value will be tested by ablation. Quality-based cascading is an optional experiment, separate from operational fallback.

**After**

The core gateway will provide a documented API, request validation, a configurable deployment registry, deterministic capability, context-window, budget and availability filters, lightweight task classification, model-suitability prediction, constrained selection, hosted and local adapters, circuit breakers, bounded operational fallback, and request and decision logging with basic monitoring. The evaluated pool will contain three to four models chosen from those covered by public scored benchmark data: a small or cheap option, a mid-tier option and a frontier option. Embedding similarity is included as a component whose value will be tested by ablation. Quality-based cascading is an optional experiment, kept separate from operational fallback.

## Chunk 252 (paragraph 252)

**Before**

The evaluation will use offline replay of public scored requests where licences allow, a capped live pilot and controlled local failure tests. Authorised testers will be able to reach the deployment, but public production availability is not assumed.

**After**

The evaluation will use offline replay of public scored requests where licences allow, a capped live pilot and controlled local failure tests. Authorised testers will be able to reach the deployment, but public production availability is not assumed.

## Chunk 253 (paragraph 253)

**Before**

Excluded from the project are training or fine-tuning a foundation model, redesigning an inference engine (a different problem that concerns memory management inside model-serving software, such as in Kwon et al., 2023), reinforcement learning, partially observable Markov decision processes, response fusion, guarantees of compatibility with every provider, and performance claims across all tasks and languages. Live GPU and queue telemetry, session memory and graph-based retrieval are not part of the committed core and would need a separate scope decision.

**After**

The project excludes training or fine-tuning a foundation model, redesigning an inference engine (a different problem that concerns memory management inside model-serving software, such as in Kwon et al., 2023), reinforcement learning, partially observable Markov decision processes, response fusion, guarantees of compatibility with every provider, and performance claims across all tasks and languages. Live GPU and queue telemetry, session memory and graph-based retrieval are not part of the committed core and would need a separate scope decision.

## Chunk 274 (paragraph 274)

**Before**

The report has five chapters. Chapter One introduces the problem, aim, objectives, research questions, methodology, significance, scope, limitations and contributions. Chapter Two reviews routing research, serving and reliability work, and existing gateways, and identifies the research gap. Chapter Three describes the methodology, requirements, system design, data, tools, evaluation plan and ethical considerations. Chapter Four will report the implementation, testing and results, and Chapter Five will summarise the findings, state the conclusions and make recommendations. References and appendices follow.

**After**

The report has five chapters. Chapter One introduces the problem, aim, objectives, research questions, methodology, significance, scope, limitations and contributions. Chapter Two reviews routing research, serving and reliability work, and existing gateways, and ends with the research gap. Chapter Three describes the methodology, requirements, system design, data, tools, evaluation plan and ethical considerations. Chapter Four will report the implementation, testing and results, and Chapter Five will summarise the findings, state the conclusions and make recommendations. References and appendices follow.

## Chunk 294 (paragraph 294)

**Before**

This chapter reviews the research and the existing systems that bear on an LLM request-routing gateway. It first explains how the literature was selected, then sets out the concepts and techniques the project builds on. It reviews 33 studies in eight themes: routing algorithms, suitability prediction, load balancing, cost reduction, latency, failure handling, benchmarking and system design. It then compares three existing gateway products, summarises the studies in a table and states the research gap that the project addresses.

**After**

This chapter reviews the research and the existing systems that bear on an LLM request-routing gateway. It first explains how the literature was selected and then sets out the concepts and techniques the project builds on. The 33 studies are reviewed in eight themes: routing algorithms, suitability prediction, load balancing, cost reduction, latency, failure handling, benchmarking and system design. The chapter then compares three existing gateway products, summarises the studies in a table and states the research gap that the project addresses.

## Chunk 296 (paragraph 296)

**Before**

This is a structured thematic review. It is not a systematic review: the original search and screening totals were not recorded, so no PRISMA-style flow diagram is given and no screening counts are claimed. Table 2.1 reports only what the records support.

**After**

This is a structured thematic review, not a systematic one: the original search and screening totals were not recorded, so no PRISMA-style flow diagram is given and no screening counts are claimed. Table 2.1 reports only what the records support.

## Chunk 299 (paragraph 299)

**Before**

The review covers 33 studies. Of these, 31 (94%) were published in 2022 or later and the other two in 2020 and 2021. Some are preprints and are labelled as such in the reference list; a preprint is evidence of a method, not of peer-reviewed validation. Numerical results are reported only where they were checked against the paper’s abstract or text. Where a figure was not checked, the finding is described without it.

**After**

The review covers 33 studies. Of these, 31 (94%) were published in 2022 or later and the other two in 2020 and 2021. Some are preprints and are labelled as such in the reference list; a preprint is evidence of a method, not of peer-reviewed validation. Numerical results are reported only where they were checked against the paper’s abstract or text, and where a figure was not checked, the finding is described without it.

## Chunk 303 (paragraph 303)

**Before**

Prompt-aware routing chooses a model for a request using information available about the prompt. A rule, a learned score or a model-specific performance estimate can guide the choice. Routing before generation differs from a cascade, which may call another model after inspecting an earlier answer, and that extra call changes both cost and latency. FrugalGPT illustrates cascading, while Hybrid LLM and RouteLLM study selection before generation (L. Chen et al., 2024; Ding et al., 2024; Ong et al., 2025).

**After**

Prompt-aware routing chooses a model for a request using what is known about the prompt. A rule, a learned score or a model-specific performance estimate can guide the choice. Routing before generation differs from a cascade, which may call another model after inspecting an earlier answer, and that extra call changes both cost and latency. FrugalGPT illustrates cascading, while Hybrid LLM and RouteLLM study selection before generation (L. Chen et al., 2024; Ding et al., 2024; Ong et al., 2025).

## Chunk 305 (paragraph 305)

**Before**

The proposed suitability estimator will combine task classification with embedding-derived evidence from previously evaluated requests. CSCR maps prompts and models into a shared representation, whereas EmbedLLM learns representations from model performance on questions (Shirkavand et al., 2025; Zhuang et al., 2025). Neither result proves that the proposed combination is better, so an ablation of each component will test its contribution.

**After**

The proposed suitability estimator will combine task classification with embedding-derived evidence from previously evaluated requests. CSCR maps prompts and models into a shared representation, whereas EmbedLLM learns representations from model performance on questions (Shirkavand et al., 2025; Zhuang et al., 2025). Neither result shows that the proposed combination does better, so an ablation of each component will test what it contributes.

## Chunk 307 (paragraph 307)

**Before**

The selection problem has more than one objective: a response must be useful, but its cost and delay also matter. In the proposed gateway, hard eligibility rules will first exclude deployments that fail capability, privacy, budget or availability requirements. The selector will compare the remaining candidates on estimated quality, cost and latency, and the same restrictions must hold during fallback. Reliability and gateway overhead therefore belong in the evaluation alongside selection quality.

**After**

The selection problem has more than one objective: a response must be useful, but its cost and delay also matter. In the proposed gateway, hard eligibility rules will first exclude deployments that fail capability, privacy, budget or availability requirements. The selector will then compare the remaining candidates on estimated quality, cost and latency, and the same restrictions must still hold during fallback. Reliability and gateway overhead therefore belong in the evaluation alongside selection quality.

## Chunk 308 (paragraph 308)

**Before**

Design science provides a useful research lens: it links the creation of an artefact to its evaluation against a problem and stated requirements (Hevner et al., 2004). Here the artefact is the proposed gateway, and the evaluation will examine both its routing decisions and its operational behaviour. Chapter Three describes the method and acceptance criteria. Figure 2.1 shows the framework.

**After**

Design science offers a useful research lens: it links the creation of an artefact to its evaluation against a problem and stated requirements (Hevner et al., 2004). Here the artefact is the proposed gateway, and the evaluation will examine both its routing decisions and its operational behaviour. Chapter Three describes the method and acceptance criteria, and Figure 2.1 shows the framework.

## Chunk 313 (paragraph 313)

**Before**

Task labels give the router a coarse description of a request, and embeddings can represent its similarity to evaluated examples. CSCR and EmbedLLM use model and prompt representations in different ways (Shirkavand et al., 2025; Zhuang et al., 2025). The proposed system will test classification and embedding-derived evidence together and separately. Retrieval is useful only if similar examples carry information about a candidate model’s performance and the evaluation prevents leakage.

**After**

Task labels give the router a coarse description of a request, and embeddings can represent its similarity to evaluated examples. CSCR and EmbedLLM use model and prompt representations in different ways (Shirkavand et al., 2025; Zhuang et al., 2025). The proposed system will test classification and embedding-derived evidence together and separately. Retrieval helps only if similar examples carry information about a candidate model’s performance and the evaluation prevents leakage.

## Chunk 315 (paragraph 315)

**Before**

A fixed-model policy is easy to implement but cannot adapt to a prompt. A rule-based policy is interpretable, while learned predictors can estimate model-specific success but need suitable training data. FORC and Routoo connect predicted performance to cost-aware selection (Šakota et al., 2024; Mohammadshahi et al., 2024). The proposed gateway will filter candidates against hard constraints and then compare the feasible choices. Fixed-model, cheapest-eligible and rule-based policies remain evaluation baselines, and their performance is not assumed to be worse.

**After**

A fixed-model policy is easy to implement but cannot adapt to a prompt. A rule-based policy is interpretable, while learned predictors can estimate model-specific success but need suitable training data. FORC and Routoo connect predicted performance to cost-aware selection (Šakota et al., 2024; Mohammadshahi et al., 2024). The proposed gateway will filter candidates against hard constraints and then compare the feasible choices. Fixed-model, cheapest-eligible and rule-based policies remain evaluation baselines, and the project does not assume that they perform worse.

## Chunk 317 (paragraph 317)

**Before**

Total latency includes gateway processing, any queueing and the time taken by the selected deployment. Etalon distinguishes delay before the first token from the timing of later tokens, while DistServe studies prefill and decoding in serving infrastructure (Agrawal et al., 2024; Zhong et al., 2024). The project will measure gateway overhead and completion time, and first-token delay where the interface allows. It will not modify the inference engine.

**After**

Total latency includes gateway processing, any queueing and the time taken by the selected deployment. Etalon distinguishes delay before the first token from the timing of later tokens, while DistServe studies prefill and decoding in serving infrastructure (Agrawal et al., 2024; Zhong et al., 2024). The project will measure gateway overhead and completion time, and first-token delay where the interface allows, but it will not modify the inference engine.

## Chunk 319 (paragraph 319)

**Before**

Provider adapters will connect a common request interface to hosted APIs and local model endpoints. The gateway will apply budget rules, record decisions and use bounded fallback, and a monitoring view will show request volumes, routing outcomes, estimated or recorded costs, latency, provider health and fallback events, subject to available data and privacy controls. Existing gateway and serving systems give precedents for parts of this design (LiteLLM, n.d.; OpenRouter, n.d.; Portkey, n.d.).

**After**

Provider adapters will connect a common request interface to hosted APIs and local model endpoints. The gateway will apply budget rules, record decisions and use bounded fallback. A monitoring view will show request volumes, routing outcomes, estimated or recorded costs, latency, provider health and fallback events, subject to available data and privacy controls. Existing gateway and serving systems give precedents for parts of this design (LiteLLM, n.d.; OpenRouter, n.d.; Portkey, n.d.).

## Chunk 323 (paragraph 323)

**Before**

Hybrid LLM predicts the quality gap between a smaller and a larger model and routes by a threshold, reducing calls to the large model by up to 40% in its tested setting (Ding et al., 2024). It uses a limited set of model pairs and says nothing about provider failure or changing load. RouteLLM also chooses between a stronger and a weaker model but learns from preference data and tests transfer to other model pairs; its Table 6 reports a 3.66× cost-saving ratio against GPT-4 at 95% of GPT-4’s MT-Bench quality, an operating-point-specific result (Ong et al., 2025).

**After**

Hybrid LLM predicts the quality gap between a smaller and a larger model and routes by a threshold, reducing calls to the large model by up to 40% in its tested setting (Ding et al., 2024). It uses a limited set of model pairs and says nothing about provider failure or changing load. RouteLLM also chooses between a stronger and a weaker model, but it learns from preference data and tests transfer to other model pairs; its Table 6 reports a 3.66× cost-saving ratio against GPT-4 at 95% of GPT-4’s MT-Bench quality, a result tied to that operating point (Ong et al., 2025).

## Chunk 324.0 (paragraph 324)

**Before**

RouterDC trains query and model representations with dual contrastive objectives and reports gains of 2.76% in distribution and 1.90% out of distribution (S. Chen et al., 2024). CSCR places prompts and models in a shared embedding space with cost-aware training and nearest-neighbour retrieval to cope with changing model pools (Shirkavand et al., 2025), and Shnitzer et al. (2023) show that benchmark correctness labels can train routers.

**After**

RouterDC trains query and model representations with dual contrastive objectives and reports gains of 2.76% in distribution and 1.90% out of distribution (S. Chen et al., 2024). CSCR places prompts and models in a shared embedding space, using cost-aware training and nearest-neighbour retrieval to cope with changing model pools (Shirkavand et al., 2025), and Shnitzer et al. (2023) show that benchmark correctness labels can train routers.

## Chunk 324.1 (paragraph 324)

**Before**

These methods make cost–quality selection a sound starting point, but they do not show that the combination of task classification and embedding evidence proposed here will be better. A fair test must use the same requests and candidate deployments, include a simple baseline and count the cost of the router itself.

**After**

These methods make cost–quality selection a sound starting point, but none of them shows that the combination of task classification and embedding evidence proposed here will do better. A fair test must use the same requests and candidate deployments, include a simple baseline and count the cost of the router itself.

## Chunk 326 (paragraph 326)

**Before**

FORC uses a small meta-model to predict the success of each language model and assigns requests under a budget, reporting about a 63% cost reduction in its setting (Šakota et al., 2024). Routoo likewise separates a performance predictor from a cost-aware selector and evaluates on MMLU (Mohammadshahi et al., 2024). Lu et al. (2024) use reward-model scores to supervise selection of a single model before generation. Varangot-Reille et al. (2026) retrieve past performance for a few-shot router and find that a simple nearest-neighbour approach is competitive, with as little as 1% of history evaluated in one test.

**After**

FORC uses a small meta-model to predict the success of each language model and assigns requests under a budget, reporting about a 63% cost reduction in its setting (Šakota et al., 2024). Routoo likewise separates a performance predictor from a cost-aware selector and evaluates on MMLU (Mohammadshahi et al., 2024). Lu et al. (2024) use reward-model scores to supervise the selection of a single model before generation. Varangot-Reille et al. (2026) retrieve past performance for a few-shot router and find a simple nearest-neighbour approach competitive, with as little as 1% of history evaluated in one test.

## Chunk 327 (paragraph 327)

**Before**

Xiong et al. (2024) study how well language models express uncertainty and find that verbalised confidence tends to be overconfident. Their work concerns generated answers, not a complete gateway, but it shows why a confidence score should not be treated as verified correctness without calibration. The proposed gateway will measure predictive performance and calibration on held-out data and set thresholds there.

**After**

Xiong et al. (2024) study how well language models express uncertainty and find that verbalised confidence tends to be overconfident. Their work concerns generated answers rather than a complete gateway, but it shows why a confidence score should not be treated as verified correctness without calibration. The proposed gateway will measure predictive performance and calibration on held-out data and set thresholds there.

## Chunk 329 (paragraph 329)

**Before**

RouteBalance combines estimated quality, latency and cost with information about available model instances (Da & Kalyvianaki, 2026). Its tests cover one model family and use offline quality labels, which limit how far the result transfers. SLOs-Serve schedules and routes work against service-level objectives across replicas (Chen et al., 2025), and GORGO estimates components of gateway latency and tunes routing weights for cross-region serving (Toniolo et al., 2026), using a single model and a synthetic trace.

**After**

RouteBalance combines estimated quality, latency and cost with information about available model instances (Da & Kalyvianaki, 2026). Its tests cover one model family and use offline quality labels, which limits how far the result transfers. SLOs-Serve schedules and routes work against service-level objectives across replicas (Chen et al., 2025), and GORGO estimates components of gateway latency and tunes routing weights for cross-region serving (Toniolo et al., 2026), using a single model and a synthetic trace.

## Chunk 330 (paragraph 330)

**Before**

These works address queueing and deadlines more directly than a quality-only router, but each assumes a particular view of infrastructure state and uses different workloads and baselines, so their numbers are not comparable. The transferable idea is to use observable backend health and timing in eligibility and selection. Redesigning a scheduler is outside the project’s core scope.

**After**

These works address queueing and deadlines more directly than a quality-only router does, but each assumes a particular view of infrastructure state and uses different workloads and baselines, so their numbers are not comparable. The transferable idea is to use observable backend health and timing in eligibility and selection. Redesigning a scheduler is outside the project’s core scope.

## Chunk 332 (paragraph 332)

**Before**

FrugalGPT cascades queries from cheaper to more expensive models using a learned judgement of answer quality and reports up to 98% cost reduction in its setting (L. Chen et al., 2024). Dekoninck et al. (2025) compare routing and cascading in one optimisation framework and report gains of up to 8% on RouterBench and 14% on SWE-Bench. BEST-Route chooses the model and the amount of test-time computation from predicted rewards (Ding et al., 2025). AutoMix escalates when a model’s own check of its answer is doubtful (Aggarwal et al., 2024), and Gupta et al. (2024) study deferral using token-level uncertainty, which needs token probabilities that hosted providers may not expose.

**After**

FrugalGPT cascades queries from cheaper to more expensive models using a learned judgement of answer quality and reports up to 98% cost reduction in its setting (L. Chen et al., 2024). Dekoninck et al. (2025) compare routing and cascading in one optimisation framework and report gains of up to 8% on RouterBench and 14% on SWE-Bench. BEST-Route chooses the model and the amount of test-time computation from predicted rewards (Ding et al., 2025). AutoMix escalates when a model’s own check of its answer is doubtful (Aggarwal et al., 2024). Gupta et al. (2024) study deferral using token-level uncertainty, which needs token probabilities that hosted providers may not expose.

## Chunk 333 (paragraph 333)

**Before**

A cascade must count the first generation in its cost and delay, so fewer calls to an expensive model do not automatically mean lower total cost or latency. LLM-Blender goes further and fuses several models’ answers (Jiang et al., 2023), which is outside this project’s scope. The evaluation will count every attempt and will test single-model selection separately from operational fallback and from any optional quality cascade.

**After**

A cascade must count the first generation in its cost and delay, so fewer calls to an expensive model do not automatically mean lower total cost or latency. LLM-Blender goes further and fuses several models’ answers (Jiang et al., 2023), which lies outside this project’s scope. The evaluation will count every attempt and will test single-model selection separately from operational fallback and from any optional quality cascade.

## Chunk 335 (paragraph 335)

**Before**

Etalon evaluates the timing of streamed tokens against deadlines and examines both serving systems and hosted APIs (Agrawal et al., 2024). QoServe schedules requests with different quality-of-service targets on shared hardware (Goel et al., 2026), and DistServe separates prefill from decoding to improve goodput under latency targets (Zhong et al., 2024). These mechanisms address different parts of the request path.

**After**

Etalon evaluates the timing of streamed tokens against deadlines and examines both serving systems and hosted APIs (Agrawal et al., 2024). QoServe schedules requests with different quality-of-service targets on shared hardware (Goel et al., 2026), and DistServe separates prefill from decoding to improve goodput under latency targets (Zhong et al., 2024). Each mechanism addresses a different part of the request path.

## Chunk 338 (paragraph 338)

**Before**

ContinuityBench evaluates whether conversational state survives a change of provider, using a history-forwarding proxy, synthetic conversations and fault injection (Pandey & Singh, 2026a). FailureAtlas classifies failures of multi-provider gateways by origin and detectability in a small catalogue of documented entries and finds that the worst are silent (Pandey & Singh, 2026b). The two preprints share authors and are not independent replications. ResilienceBench-Operator tests retry and circuit-breaker patterns in a Kubernetes microservice setting (Aderaldo & Mendonça, 2026), so its findings need to be validated in an LLM gateway.

**After**

ContinuityBench evaluates whether conversational state survives a change of provider, using a history-forwarding proxy, synthetic conversations and fault injection (Pandey & Singh, 2026a). FailureAtlas classifies failures of multi-provider gateways by origin and detectability in a small catalogue of documented entries and finds that the worst are silent (Pandey & Singh, 2026b). The two preprints share authors, so they are not independent replications. ResilienceBench-Operator tests retry and circuit-breaker patterns in a Kubernetes microservice setting (Aderaldo & Mendonça, 2026); its findings need to be validated in an LLM gateway.

## Chunk 339 (paragraph 339)

**Before**

SpotServe reports 2.4 to 9.1 times lower P99 latency and 54% lower cost under its preemption setup (Miao et al., 2024), and DéjàVu streams the KV cache to recover from failures (Strati et al., 2024). Both operate on engine state and cannot show how a gateway should fall back between models. Together these works supply scenarios to test, not proof of the gateway’s reliability. The tests will cover timeouts, rate limits and server errors, measure the added delay and completion, and verify that bounded retries keep the request’s hard constraints.

**After**

SpotServe reports 2.4 to 9.1 times lower P99 latency and 54% lower cost under its preemption setup (Miao et al., 2024), and DéjàVu streams the KV cache to recover from failures (Strati et al., 2024). Both operate on engine state and cannot show how a gateway should fall back between models. Together they supply scenarios to test, not proof of the gateway’s reliability. The tests will cover timeouts, rate limits and server errors, measure the added delay and completion, and verify that bounded retries keep the request’s hard constraints.

## Chunk 341 (paragraph 341)

**Before**

RouterBench supplies over 405,000 stored inference outcomes and a cost–quality framework for comparing routers (Hu et al., 2024). LLMRouterBench covers over 400,000 instances from 21 datasets and 33 models, with ten routing baselines and latency-aware analysis (Li et al., 2026). Both support repeatable offline comparison, but stored outputs cannot establish current provider availability or network latency. EmbedLLM is different in kind: it learns compact model representations from performance on questions and compares them with simpler alternatives (Zhuang et al., 2025), so it is a candidate component to test, not a benchmark.

**After**

RouterBench supplies over 405,000 stored inference outcomes and a cost–quality framework for comparing routers (Hu et al., 2024). LLMRouterBench covers over 400,000 instances from 21 datasets and 33 models, with ten routing baselines and latency-aware analysis (Li et al., 2026). Both support repeatable offline comparison, but stored outputs cannot establish current provider availability or network latency. EmbedLLM is different in kind: it learns compact model representations from performance on questions and compares them with simpler alternatives (Zhuang et al., 2025); it is a candidate component to test rather than a benchmark.

## Chunk 344 (paragraph 344)

**Before**

INFaaS provides a model-less interface and selects among deployed variants for each request (Romero et al., 2021), but it was evaluated on image models. Clockwork uses predicted execution times to schedule inference predictably (Gujarati et al., 2020), without a multi-provider fallback workflow. Mélange studies the placement of LLM serving workloads across GPU types (Griggs et al., 2024), which helps motivate an explicit accounting basis for local inference. None of these alone validates the proposed gateway’s architecture, and none establishes that its combination of adapters, fallback and monitoring is new. Those functions must be built and evaluated in their own right.

**After**

INFaaS provides a model-less interface and selects among deployed variants for each request (Romero et al., 2021), but it was evaluated on image models. Clockwork uses predicted execution times to schedule inference predictably (Gujarati et al., 2020), without a multi-provider fallback workflow. Mélange studies the placement of LLM serving workloads across GPU types (Griggs et al., 2024), which helps motivate an explicit accounting basis for local inference. None of these alone validates the proposed gateway’s architecture, and none establishes that its combination of adapters, fallback and monitoring is new, so those functions must be built and evaluated in their own right.

## Chunk 346 (paragraph 346)

**Before**

Table 2.2 compares three existing gateway products with the proposed system, using their official documentation accessed on 31 October 2026. This is grey literature and not peer-reviewed evidence of performance. A tick means a documented feature, or a planned feature for the proposal; P means a partial or rule-based form; a question mark means the checked pages did not establish the feature, which is not evidence that it is absent. The ticks for the proposed system are planned, not implemented.

**After**

Table 2.2 compares three existing gateway products with the proposed system, using their official documentation accessed on 31 October 2026. This is grey literature, not peer-reviewed evidence of performance. A tick means a documented feature, or a planned feature for the proposal; P means a partial or rule-based form; a question mark means the checked pages did not establish the feature, which is not evidence that it is absent. The ticks for the proposed system are planned, not implemented.

## Chunk 361 (paragraph 361)

**Before**

These are project-specific questions and evidence boundaries. They are not claims that the literature has never studied constraints, calibration, latency or reliability. Live GPU and queue telemetry, session memory and graph-based retrieval are not part of the committed core.

**After**

These are project-specific questions and evidence boundaries, not claims that the literature has never studied constraints, calibration, latency or reliability. Live GPU and queue telemetry, session memory and graph-based retrieval are not part of the committed core.

## Chunk 364 (paragraph 364)

**Before**

The reviewed studies show several ways to predict model suitability and to trade response quality against cost. Serving and resilience studies add constraints that offline routing benchmarks cannot measure, and existing gateways already offer per-prompt routing and fallback. The remaining question is whether the proposed hybrid improves on simpler policies while keeping its operational constraints in the chosen test setting. Chapter Three specifies how the gateway will be built and evaluated.

**After**

The reviewed studies show several ways to predict model suitability and to trade response quality against cost. Serving and resilience studies add constraints that offline routing benchmarks cannot measure, and existing gateways already offer per-prompt routing and fallback. What remains open is whether the proposed hybrid improves on simpler policies while keeping its operational constraints in the chosen test setting. Chapter Three specifies how the gateway will be built and evaluated.

## Chunk 374.0 (paragraph 374)

**Before**

Development model. The team will use Scrum with two-week sprints. This model was chosen for a reason specific to the project: the routing thresholds, features and fallback limits can only be tuned once scored benchmark data and live timing are available, so early working versions are needed and some requirements will change after the first results. The project supervisor, Dr. Emmanuel Aderemi Tunbosun, will act as product owner and approve the backlog priorities.

**After**

Development model. The team will use Scrum with two-week sprints. The choice follows from the project itself: the routing thresholds, features and fallback limits can be tuned only once scored benchmark data and live timing are available, so early working versions are needed and some requirements will change after the first results. The project supervisor, Dr. Emmanuel Aderemi Tunbosun, will act as product owner and approve the backlog priorities.

## Chunk 374.1 (paragraph 374)

**Before**

The team leader will act as Scrum master. The sprint backlog will be kept in GitHub Projects, the code in one GitHub repository with pull-request reviews, and each sprint will end with a review of a working increment against the requirements. Each increment will keep the same external request interface, so that baseline and hybrid policies differ only in the routing mechanism and not in unrelated interface changes.

**After**

The team leader will act as Scrum master. The sprint backlog will be kept in GitHub Projects and the code in one GitHub repository with pull-request reviews, and each sprint will end with a review of a working increment against the requirements. Each increment will keep the same external request interface, so that baseline and hybrid policies differ only in the routing mechanism and not in unrelated interface changes.

## Chunk 387.0 (paragraph 387)

**Before**

Participants are the six team members and the supervisor, and requirements are checked by review with the supervisor in sprint reviews. The instruments are a scenario checklist and the sketches. No questionnaire or interview is planned, because human participation will be minimal or absent, and no result from a population of users will be claimed.

**After**

Participants are the six team members and the supervisor, and requirements are checked by review with the supervisor in sprint reviews. The instruments are a scenario checklist and the sketches. No questionnaire or interview is planned, because human participation will be minimal or absent, and no result from a population of users will be claimed.

## Chunk 387.1 (paragraph 387)

**Before**

Findings will be recorded as requirements with identifiers and MoSCoW priorities (Section 3.5) and, for the main scenarios, as acceptance criteria in the form given, when and then, which become test cases in Chapter Four. If an optional participant exercise is added later, informed consent, anonymous responses and a documented instrument will come first, and the university’s ethics process will be followed (Section 3.10).

**After**

Findings will be recorded as requirements with identifiers and MoSCoW priorities (Section 3.5) and, for the main scenarios, as acceptance criteria in the given, when and then form, which become test cases in Chapter Four. If an optional participant exercise is added later, informed consent, anonymous responses and a documented instrument will come first, and the university’s ethics process will be followed (Section 3.10).

## Chunk 390 (paragraph 390)

**Before**

In the baseline arrangement, a client application calls one predetermined LLM deployment for every request. The project will reproduce this arrangement as a fixed-model reference for comparison. It is not presented as a survey finding about how all developers work. Existing gateways already support routing and recovery in several forms (LiteLLM, n.d.; OpenRouter, n.d.; Portkey, n.d.; Section 2.5), so the comparison also includes current gateway practice.

**After**

In the baseline arrangement, a client application calls one predetermined LLM deployment for every request. The project will reproduce this arrangement as a fixed-model reference for comparison, without presenting it as a survey finding about how all developers work. Existing gateways already support routing and recovery in several forms (LiteLLM, n.d.; OpenRouter, n.d.; Portkey, n.d.; Section 2.5), so the comparison also includes current gateway practice.

## Chunk 391 (paragraph 391)

**Before**

Research comparators include pre-generation routing and cascades. Hybrid LLM uses quality-aware routing, RouteLLM learns from preference data, and FrugalGPT escalates according to the response (Ding et al., 2024; Ong et al., 2025; L. Chen et al., 2024). The study does not assume that any of these features is absent from earlier work.

**After**

Research comparators include pre-generation routing and cascades. Hybrid LLM uses quality-aware routing, RouteLLM learns from preference data, and FrugalGPT escalates according to the response (Ding et al., 2024; Ong et al., 2025; L. Chen et al., 2024). The study does not assume that any of these features is absent from earlier work.

## Chunk 401 (paragraph 401)

**Before**

The proposed system is a gateway that gives client applications one request interface over a registered pool of hosted and local model deployments. For each request it will validate the input, filter out deployments that break mandatory constraints, analyse the task and its capability needs, retrieve permitted historical evidence, predict how well each remaining model suits the request, and select the cheapest feasible candidate. Execution goes through provider adapters. A separate controller owns health state, circuit breakers, bounded attempts and outcome accounting.

**After**

The proposed system is a gateway that gives client applications one request interface over a registered pool of hosted and local model deployments. For each request it will validate the input and filter out deployments that break mandatory constraints. It will then analyse the task and its capability needs, retrieve permitted historical evidence, predict how well each remaining model suits the request, and select the cheapest feasible candidate. Execution goes through provider adapters. A separate controller owns health state, circuit breakers, bounded attempts and outcome accounting.

## Chunk 402 (paragraph 402)

**Before**

A model describes a capability and a version. A deployment is a runnable endpoint with its current health, price profile and latency history. Keeping the two apart lets the evaluation distinguish model quality from deployment conditions. The users are client applications that send requests and administrators who register models, set policies and inspect behaviour. Monitoring will record selection reasons, exclusions, predicted values and observed outcomes without routinely keeping raw prompts.

**After**

A model describes a capability and a version. A deployment is a runnable endpoint with its current health, price profile and latency history. Keeping the two apart lets the evaluation distinguish model quality from deployment conditions. The users are client applications that send requests and administrators who register models, set policies and inspect behaviour. Monitoring will record selection reasons, exclusions, predicted values and observed outcomes without routinely keeping raw prompts.

## Chunk 411 (paragraph 411)

**Before**

The system will be built as one modular application at first. This is a provisional engineering choice that keeps the first version small; it is not a claim that separate services or other tools could not be added later.

**After**

The system will be built as one modular application at first. This is a provisional engineering choice that keeps the first version small, and it does not rule out adding separate services or other tools later.

## Chunk 419 (paragraph 419)

**Before**

Table 3.2 states each quality requirement with a measure and a target. Targets are fixed now, before any results exist. They may be revised after a pilot only with a recorded reason and before the test results are examined. No target allows a hard restriction to be ignored.

**After**

Table 3.2 states each quality requirement with a measure and a target. Targets are fixed now, before any results exist, and may be revised after a pilot only with a recorded reason and before the test results are examined. No target allows a hard restriction to be ignored.

## Chunk 424 (paragraph 424)

**Before**

Figure 3.2 shows the actors and use cases. The client application provides the request and policy, the administrator configures and inspects routing, and the provider or model backend executes model calls. Calibration uses permitted validation evidence and not uncontrolled updates from test outcomes.

**After**

Figure 3.2 shows the actors and use cases. The client application provides the request and policy, the administrator configures and inspects routing, and the provider or model backend executes model calls. Calibration uses permitted validation evidence rather than uncontrolled updates from test outcomes.

## Chunk 434 (paragraph 434)

**Before**

The gateway will be one application made of logical modules, not separate services. Preprocessing validates the declared requirements and classifies the task and capability needs. The retrieval path uses embeddings and a k-nearest-neighbour (k-NN) index built only from permitted historical records. The suitability predictor estimates quality, the selector assesses feasibility and ranks candidates, and the execution controller owns attempts and recovery. A modular layout was chosen because it keeps the first version simple and lets each component be switched off for ablation tests.

**After**

The gateway will be one application made of logical modules rather than separate services. Preprocessing validates the declared requirements and classifies the task and capability needs. The retrieval path uses embeddings and a k-nearest-neighbour (k-NN) index built only from permitted historical records. The suitability predictor estimates quality, the selector assesses feasibility and ranks candidates, and the execution controller owns attempts and recovery. A modular layout keeps the first version simple and lets each component be switched off for ablation tests.

## Chunk 437 (paragraph 437)

**Before**

Figure 3.4 shows the planned development and evaluation deployment on the two laptops. The allocation is provisional until the machines are profiled, and it does not assume that models are loaded at the same time or that the two laptops have equal graphics memory. Memory contention between embeddings and local inference will be measured.

**After**

Figure 3.4 shows the planned development and evaluation deployment on the two laptops. The allocation is provisional until the machines are profiled; it does not assume that models are loaded at the same time or that the two laptops have equal graphics memory. Memory contention between embeddings and local inference will be measured.

## Chunk 455 (paragraph 455)

**Before**

The relational schema will keep stable model metadata apart from deployments and attempt records. Capabilities are held in a join table, not in a comma-separated field. A versioned price record preserves the rate used for accounting, so current prices never overwrite historical costs. Raw prompt text is not required in the operational request table. Figure 3.9 shows the entities and Table 3.4 gives the relations in third normal form (3NF).

**After**

The relational schema will keep stable model metadata apart from deployments and attempt records. Capabilities are held in a join table rather than a comma-separated field. A versioned price record preserves the rate used for accounting, so current prices never overwrite historical costs. Raw prompt text is not required in the operational request table. Figure 3.9 shows the entities and Table 3.4 gives the relations in third normal form (3NF).

## Chunk 465 (paragraph 465)

**Before**

Classification is lightweight. Mandatory request fields are filtered first, and any capability requirement found during analysis is applied again before selection. The classifier never weakens an explicit client restriction. Difficulty and similarity are predictive features and not independent proof of quality, and similarity features come only from permitted historical outcomes. A score will not be called a probability unless its label definition and calibration justify that.

**After**

Classification is lightweight. Mandatory request fields are filtered first, and any capability requirement found during analysis is applied again before selection. The classifier never weakens an explicit client restriction. Difficulty and similarity are predictive features, not independent proof of quality, and similarity features come only from permitted historical outcomes. A score will not be called a probability unless its label definition and calibration justify that.

## Chunk 475 (paragraph 475)

**Before**

When no candidate is feasible, the first version will reject the request with an explicit error. Relaxing an explicitly soft preference, or asking the caller for permission to exceed a constraint, are possible later options. No path silently relaxes a hard budget, capability or privacy rule. Retry eligibility, attempt count, cooldown and circuit-breaker thresholds will be set after the pilot. After delivery has begun, the gateway reports failure instead of joining another model’s stream to the first, and calls with unsafe or uncertain side effects are not repeated automatically.

**After**

When no candidate is feasible, the first version will reject the request with an explicit error. Later versions may relax an explicitly soft preference or ask the caller for permission to exceed a constraint, but no path will silently relax a hard budget, capability or privacy rule. Retry eligibility, attempt count, cooldown and circuit-breaker thresholds will be set after the pilot. After delivery has begun, the gateway reports failure instead of joining another model’s stream to the first, and calls with unsafe or uncertain side effects are not repeated automatically.

## Chunk 478 (paragraph 478)

**Before**

The client-facing interface is the request API. It returns a response or an explicit validation, infeasibility, budget or execution error, with a correlation identifier. Client applications do not need to know how the predictor works to submit a request. The administrator interface prioritises observation and safe configuration: it shows the active model pool, deployment health and circuit-breaker state, reserved spend, aggregate quality and calibration, and latency. It does not show raw prompts or credentials by default, and configuration changes need administrator rights and leave a versioned record. Figure 3.10 is the planned layout.

**After**

The client-facing interface is the request API. It returns a response or an explicit validation, infeasibility, budget or execution error, with a correlation identifier. Client applications do not need to know how the predictor works to submit a request. The administrator interface prioritises observation and safe configuration: it shows the active model pool, deployment health and circuit-breaker state, reserved spend, aggregate quality and calibration, and latency. By default it does not show raw prompts or credentials, and configuration changes need administrator rights and leave a versioned record. Figure 3.10 is the planned layout.

## Chunk 484.1 (paragraph 484)

**Before**

These are regulatory requirements and not a claim that compliance has been achieved. If personal data is ever processed, the team will document its lawful basis, notices, access and deletion process, recipient restrictions and any cross-border arrangement before collection, and will not infer these from a provider merely offering an API.

**After**

These are regulatory requirements, not a claim that compliance has been achieved. If personal data is ever processed, the team will document its lawful basis, notices, access and deletion process, recipient restrictions and any cross-border arrangement before collection, and will not infer these merely from a provider offering an API.

## Chunk 492 (paragraph 492)

**Before**

RouterBench and LLMRouterBench are the candidate sources of already-scored model outputs (Hu et al., 2024; Li et al., 2026). The team will inspect task identifiers, prompts, model revisions, scores, token counts and cost fields before choosing a shared evaluation subset. The evaluated pool will contain three to four models covering a small local option, a mid-tier option and a frontier option. Names will be fixed once aligned scored outputs for the same requests are confirmed, and public availability of a model in a benchmark does not by itself show that its outcomes line up with the others. Table 3.6 lists the planned controls.

**After**

RouterBench and LLMRouterBench are the candidate sources of already-scored model outputs (Hu et al., 2024; Li et al., 2026). The team will inspect task identifiers, prompts, model revisions, scores, token counts and cost fields before choosing a shared evaluation subset. The evaluated pool will contain three to four models covering a small local option, a mid-tier option and a frontier option. Names will be fixed once aligned scored outputs for the same requests are confirmed, because a model’s public availability in a benchmark does not by itself show that its outcomes line up with the others. Table 3.6 lists the planned controls.

## Chunk 496.0 (paragraph 496)

**Before**

A benchmark’s own split will not automatically become the study protocol. A tuning pilot will be kept separate from the untouched test partition. If aligned outcomes across models are not available, the limitation will be recorded and the gaps will not be filled with unrelated benchmark averages. No raw benchmark data will be redistributed with the report. RouterBench has an MIT code licence, but the inspected data card did not establish a dataset-level redistribution grant, and the MIT badge on LLMRouterBench does not settle its missing data licence text; dataset use will be cleared in Appendix G before data is used.

**After**

A benchmark’s own split will not automatically become the study protocol. A tuning pilot will be kept separate from the untouched test partition. If aligned outcomes across models are not available, the limitation will be recorded rather than filled with unrelated benchmark averages. No raw benchmark data will be redistributed with the report. RouterBench has an MIT code licence, but the inspected data card did not establish a dataset-level redistribution grant, and the MIT badge on LLMRouterBench does not settle its missing data licence text; dataset use will be cleared in Appendix G before data is used.

## Chunk 502 (paragraph 502)

**Before**

Tools such as Redis and Prometheus, and direct live collection of graphics-card and queue data, are not part of the committed core. They could be added later if a separate scope decision is made. The final environment record will state operating systems, driver and runtime versions and package versions, instead of calling a changing “latest” release reproducible.

**After**

Tools such as Redis and Prometheus, and direct live collection of graphics-card and queue data, are not part of the committed core and could be added later only after a separate scope decision. The final environment record will state operating systems, driver and runtime versions and package versions instead of calling a changing “latest” release reproducible.

## Chunk 520 (paragraph 520)

**Before**

Paired differences will use identical requests where possible, and uncertainty intervals will resample groups of related requests and not treat correlated copies as independent. Timeouts and rejected requests stay in the denominators of offered requests. Results will be shown per domain as well as in aggregate. Failed, inconclusive and negative results will be kept, and any retuning after test inspection will be labelled exploratory. Appendix I will hold the fixed analysis plan. Figure 3.11 shows the pipeline.

**After**

Paired differences will use identical requests where possible, and uncertainty intervals will resample groups of related requests rather than treat correlated copies as independent. Timeouts and rejected requests stay in the denominators of offered requests. Results will be shown per domain as well as in aggregate. Failed, inconclusive and negative results will be kept, and any retuning after test inspection will be labelled exploratory. Appendix I will hold the fixed analysis plan. Figure 3.11 shows the pipeline.

## Chunk 524 (paragraph 524)

**Before**

No formal ethical approval is sought for this study because it uses public benchmark data and synthetic or redacted requests and involves no human participants. This statement records the team’s position. It is not an approval certificate or an exemption granted by the university.

**After**

No formal ethical approval is sought for this study because it uses public benchmark data and synthetic or redacted requests and involves no human participants. This statement records the team’s position; it is not an approval certificate or an exemption granted by the university.

## Chunk 525 (paragraph 525)

**Before**

The experiments will use permitted public benchmark material, synthetic requests where suitable and redacted operational records. The team will avoid personal data, preserve anonymity, respect source and dataset rights and report findings honestly. Results will not be invented, selectively left out or presented as evidence of human review that did not happen. If people are later involved, informed consent, voluntary participation and anonymised responses will come before any collection, and the team will check the university’s process before the scope changes.

**After**

The experiments will use permitted public benchmark material, synthetic requests where suitable and redacted operational records. The team will avoid personal data, preserve anonymity, respect source and dataset rights and report findings honestly, without inventing results, selectively omitting them or presenting them as evidence of human review that did not happen. If people are later involved, informed consent, voluntary participation and anonymised responses will come before any collection, and the team will check the university’s process before the scope changes.
