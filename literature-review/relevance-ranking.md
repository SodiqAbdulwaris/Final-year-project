# Papers ranked by relevance to the AI Request Router

Prepared: **1 November 2026**. Coverage: **90 papers across nine topics**, ranked once each.

This is a project-specific reading and citation priority, not a ranking of scientific quality or demonstrated performance. A paper can be excellent research and still address a different problem from ours.

## Basis for the ranking

The governing scope is the [owner-approved hybrid design](../proposal-drafts/_meta/hybrid-design.md), confirmed by [D01](../decisions/D01-governing-design.md), and the [current evaluation plan](../proposal-drafts/03-methodology-design/3.9-evaluation-plan.md). Some older topic notes recommend a different design; those recommendations do not override the hybrid decision.

Our project combines lightweight task/capability classification and embedding-derived historical-performance features to estimate **model-specific suitability**. It then selects an eligible model under quality, cost and latency constraints. Provider-health checks and bounded operational fallback form a separate reliability controller. The evaluation must compare against simpler baselines and isolate each hybrid component's contribution.

I prioritised:

1. Direct overlap with the predictor, constrained selector or operational fallback.
2. Usefulness for required experiments: baselines, ablations, calibration, quality–cost curves, measured latency and injected failures.
3. Practical fit for two RTX 4070 machines and a minimal API budget.
4. Breadth of relevant coverage and how little adaptation an idea needs.

These are qualitative judgements, not measured scores. The tiers matter more than small differences between neighbouring ranks. Benchmark and resilience papers rank highly where they support essential project work. Relevance and evidence strength are separate: a directly relevant preprint can still need more verification than a less directly relevant established study.

**Review basis:** the local paper records' descriptions, methods, relevance and limitations, with closer inspection of selected records and the current project documents. This pass does not claim a fresh full-text reading of all 90 original publications or fresh verification of their metadata. Each paper link leads to its local research record, which contains the original-source references and earlier verification notes. Existing [citation](../limitations/L03-unconfirmed-citations.md), [partial-reading](../limitations/L06-partial-reading.md) and [fact-check](../limitations/L07-fact-check-sample.md) limitations remain applicable. Historical improvement figures are not adopted as project results.

Vendor/competitor documents, topic overviews and papers merely mentioned as search leads are outside this numbered paper ranking.

## Tier A — Essential: ranks 1–15

Start here. Together these cover the main algorithm, closest overlapping work, affordable evaluation, live timing and operational recovery.

| Rank | Paper | Relevance to our project | Main boundary or caution |
|---|---|---|---|
| 1 | [FORC / Fly-swat or cannon — Šakota et al. (2024)](02-prompt-difficulty/sakota-2024-fly-swat-or-cannon.md) | A small prompt-only predictor estimates each model's success, then a budget-aware selector assigns requests: the closest structural match to our predictor-and-selector pipeline. | Batch assignment and older same-family models; does not establish online deadline or fallback behaviour. |
| 2 | [Hybrid LLM — Ding et al. (2024)](01-routing-algorithms/ding-2024-hybrid-llm.md) | Direct foundation for predicting relative model suitability before generation and tuning the quality–cost trade-off. | Two-model routing; not a complete multi-model, latency-constrained solution. |
| 3 | [RouteLLM — Ong et al. (2025)](01-routing-algorithms/ong-2025-routellm.md) | Practical learned-routing reference for preference-based suitability prediction, threshold selection and generalisation. | Binary strong/weak routing; preference is not identical to factual correctness. |
| 4 | [Past-performance retrieval / ContextualRouter — Varangot-Reille et al. (2026)](09-retrieval-knn-and-multiturn-routing/varangot-reille-2026-contextualrouter.md) | Direct support for retrieving similar historical requests and their scored model outcomes; makes plain k-NN an essential comparator for the embedding component. | Benchmark-label and distribution-shift limitations; does not make classification optional in our approved design. |
| 5 | [Cascade Routing — Dekoninck et al. (2025)](04-cost-reduction/dekoninck-2025-cascade-routing.md) | Strong theoretical foundation for predicted-quality and predicted-cost selection, validation-tuned trade-offs and distinguishing routing from cascading. | Expected-cost optimisation does not guarantee a hard per-request cap or deadline; cascade machinery is optional here. |
| 6 | [RouteBalance — Da et al. (2026)](03-load-balancing/da-2026-routebalance.md) | Closest overlap with joint quality–cost–latency model/instance selection; essential prior art when explaining what our contribution adds. | Local-cluster/load-aware setting and a preprint in the local record; GPU telemetry is not an established core requirement for us. |
| 7 | [CSCR — Shirkavand et al. (2025)](01-routing-algorithms/shirkavand-2025-cscr.md) | Connects lightweight prompt embeddings, model representations and cost-aware selection across open and API models. | Contrastive training/descriptors add work; no operational fallback or deadline guarantees. |
| 8 | [RouterDC — Chen et al. (2024)](01-routing-algorithms/chen-2024-routerdc.md) | Direct inspiration for embedding-based suitability and recognising several acceptable models rather than one winner label. | Quality-only training and fixed pool; reproducing full dual-contrastive training is not required for the MVP. |
| 9 | [PORT — Wu and Silwal (2025)](09-retrieval-knn-and-multiturn-routing/wu-2025-port-online-routing.md) | Combines neighbour-based quality/cost estimates with budget-aware selection; close comparator for retrieval plus optimisation. | Total token budgets differ from per-request monetary/deadline constraints; no operational-state model. |
| 10 | [EmbedLLM — Zhuang et al. (2025)](07-testing-and-benchmarking/zhuang-2025-embedllm.md) | Strong fit for sentence embeddings plus a small learned suitability head; useful model-by-question correctness representation. | Correctness-focused, fixed pool; quality–cost–latency selection must be added separately. |
| 11 | [LLMRouterBench — Li et al. (2026)](07-testing-and-benchmarking/li-2026-llmrouterbench.md) | Major evaluation reference for shared-condition comparisons and checking whether a complex hybrid beats simple baselines. | Approximate latency cannot replace our live timing; verify usable model coverage and licences. |
| 12 | [RouterBench — Hu et al. (2024)](07-testing-and-benchmarking/hu-2024-routerbench.md) | Stored per-prompt, per-model outcomes and costs support low-budget training, replay and quality–cost curves. | Historical model prices/pools; no measured current latency or fault behaviour. |
| 13 | [ContinuityBench — Pandey and Singh (2026)](06-error-handling-fallback/pandey-2026-continuitybench.md) | Direct gateway-failover study; useful for continuity tests and timeout, 429 and 5xx scenarios. | Limited provider pair and synthetic conversations; no streaming recovery. Preserving supplied context does not require a managed-memory subsystem. |
| 14 | [Etalon — Agrawal et al. (2024)](05-latency-and-speed/agrawal-2024-etalon.md) | Especially useful for black-box hosted-backend timing and separating first-token delay from streaming experience. | Measurement framework rather than selection policy; report standard timing metrics alongside its proposed metric. |
| 15 | [ResilienceBench-Operator — Aderaldo and Mendonça (2026)](06-error-handling-fallback/aderaldo-2026-resiliencebench-operator.md) | Controlled fault-injection approach for choosing bounded retries by their success/latency trade-off. | Microservice study, not LLM routing; does not establish universal circuit-breaker thresholds. |

## Tier B — Strong relevance: ranks 16–35

Use these to develop the literature argument, select comparators and make the design/evaluation defensible.

| Rank | Paper | Relevance to our project | Main boundary or caution |
|---|---|---|---|
| 16 | [FrugalGPT — Chen et al. (2024)](01-routing-algorithms/chen-2024-frugalgpt.md) | Foundational cost-aware multi-LLM work; informs cost accounting and the optional cheap-first quality-cascade comparison. | Post-generation answer scoring; quality escalation is different from operational failover. |
| 17 | [Benchmark-dataset routing — Shnitzer et al. (2023)](01-routing-algorithms/shnitzer-2023-benchmark-routing.md) | Simple embedding/k-NN per-model correctness predictors support an affordable baseline and held-out-task generalisation tests. | Task-level emphasis and weak distribution transfer; no joint cost/latency control. |
| 18 | [Routoo — Mohammadshahi et al. (2024)](02-prompt-difficulty/mohammadshahi-2024-routoo.md) | Very close decomposition into per-model performance prediction and cost-aware multi-model selection. | Heavy router and narrow benchmark; borrow the decomposition rather than the request-time encoder. |
| 19 | [BEST-Route — Ding et al. (2025)](04-cost-reduction/ding-2025-best-route.md) | Useful predictor-to-selector design, expected-output cost estimation and threshold-sweep evaluation. | Best-of-n sampling adds calls and a reward model; sampling allocation is outside the core build. |
| 20 | [Avengers-Pro — Zhang et al. (2025)](09-retrieval-knn-and-multiturn-routing/zhang-2025-avengers-pro.md) | Cheap embedding/cluster score lookup is a practical retrieval-only comparator and quality–cost policy reference. | Cluster-relative scores are not calibrated success probabilities; no latency constraints. |
| 21 | [FusionFactory — Feng et al. (2026)](07-testing-and-benchmarking/feng-2026-fusionfactory.md) | Links multi-model outcome logs to lightweight routing predictors and explicit quality/cost objectives. | Logging is not online learning; our records also need timing and operational outcomes. |
| 22 | [FailureAtlas — Pandey and Singh (2026)](06-error-handling-fallback/pandey-2026-failureatlas.md) | Direct gateway failure checklist for concurrency, retries, streaming and apparently successful but invalid responses. | Small catalogue in a preprint; test ideas, not evidence of failure prevalence. |
| 23 | [Metastable Failures — Huang et al. (2022)](06-error-handling-fallback/huang-2022-metastable-failures.md) | Strong systems rationale for bounded retries, backoff and avoiding fallback-induced overload. | Not LLM-specific; cannot supply our retry counts or breaker timers. |
| 24 | [GenAI production incidents — Yan et al. (2025)](06-error-handling-fallback/yan-2025-genai-incidents.md) | Production incident evidence motivates testing slowdowns and malformed successes alongside outright outages. | One provider's incident population; percentages are not client request failure rates. |
| 25 | [LLM uncertainty calibration — Xiong et al. (2024)](02-prompt-difficulty/xiong-2024-llm-uncertainty-calibration.md) | Useful calibration vocabulary and warning against treating confidence as actual success probability. | Studies post-answer model confidence; our pre-call predictor needs separate calibration measurement. |
| 26 | [Routing and cascading survey — Moslem and Kelleher (2026)](01-routing-algorithms/moslem-2026-routing-cascading-survey.md) | Broad framing for pre-generation routing, optional cascading and routing failure modes. | Survey synthesis, not independent evidence that our hybrid will improve results. |
| 27 | [Routing strategies survey — Varangot-Reille et al. (2026)](01-routing-algorithms/varangot-reille-2026-routing-survey.md) | Formal framing of external, budget-constrained routing and distinctions between objectives and techniques. | Descriptive survey; does not establish novelty or implement resilience. |
| 28 | [RouterArena — Lu et al. (2026)](07-testing-and-benchmarking/lu-2026-routerarena.md) | Evaluation template for routing overhead, difficulty breakdowns and robustness to wording changes. | Router overhead differs from total backend latency and outage recovery. |
| 29 | [Learning how hard to think — Damani et al. (2025)](02-prompt-difficulty/damani-2025-learning-how-hard-to-think.md) | Supports query-specific benefit prediction and comparison against uniform/oracle allocation policies. | Compute allocation and target-model features differ from our independent lightweight encoder. |
| 30 | [HELM — Liang et al. (2023)](07-testing-and-benchmarking/liang-2023-helm.md) | Foundational support for multi-metric, per-domain evaluation including calibration, robustness and efficiency. | General model evaluation, not a complete gateway experiment. |
| 31 | [MT-Bench / LLM-as-judge — Zheng et al. (2023)](07-testing-and-benchmarking/zheng-2023-mt-bench-llm-judge.md) | Essential caution about judge-scored training/evaluation labels; informs bias checks and paired judging. | Small chat benchmark and judge biases; scores are not ground-truth correctness. |
| 32 | [INFaaS — Romero et al. (2021)](08-system-design-gateway/romero-2021-infaas.md) | Close architectural precedent for callers specifying accuracy/latency/cost requirements while the service chooses a backend. | DNN variant selection uses static accuracy, not prompt-specific LLM suitability. |
| 33 | [Clockwork — Gujarati et al. (2020)](08-system-design-gateway/gujarati-2020-clockwork.md) | Supports deadline-aware eligibility and explicit latency-prediction error reporting. | Predictable DNN inference with runtime control differs from variable-length hosted LLM calls. |
| 34 | [SLOs-Serve — Chen et al. (2025)](03-load-balancing/chen-2025-slos-serve.md) | Useful admission principle: accept work only when predicted latency can meet its target. | Engine scheduling and same-model replicas; cannot directly govern opaque hosted APIs. |
| 35 | [GORGO — Toniolo et al. (2026)](03-load-balancing/toniolo-2026-gorgo.md) | Gateway-level latency estimation combines network, queued work and prefill, relevant to local/remote latency modelling. | Single-model replica selection; online weight adaptation is not approved core scope. |

## Tier C — Supporting relevance: ranks 36–60

Read selectively for predictor features, calibration, latency estimation or a clearly labelled optional extension.

| Rank | Paper | Relevance to our project | Main boundary or caution |
|---|---|---|---|
| 36 | [Models know what they know — Kadavath et al. (2022)](02-prompt-difficulty/kadavath-2022-know-what-they-know.md) | Conceptual basis for model-specific pre-answer success prediction, soft outcome labels and calibration under shift. | Large-model confidence evidence does not prove a small external predictor will behave similarly. |
| 37 | [The LLM already knows — Zhu et al. (2025)](02-prompt-difficulty/zhu-2025-llm-already-knows.md) | Reinforces model-dependent difficulty and validation-based prediction thresholds. | Requires target-model hidden states, unavailable from our hosted backends. |
| 38 | [Reasoning efficiency and difficulty — Zhao et al. (2025)](02-prompt-difficulty/zhao-2025-reasoning-efficiency-difficulty.md) | Helps distinguish generic difficulty classes from more useful per-model success estimates. | Math-only and large-model activation features; weak practical fit for a cheap general gateway. |
| 39 | [FamiCom — Li et al. (2024)](02-prompt-difficulty/li-2024-famicom.md) | Separates task complexity from model familiarity, motivating complementary prompt features. | Not multi-model routing; perplexity and reasoning-analysis features add access/cost requirements. |
| 40 | [Zooter — Lu et al. (2024)](01-routing-algorithms/lu-2024-zooter.md) | Suitability-learning comparison and warning that training labels can be noisy across task categories. | Reward-guided training is deferred; fixed models and no cost/latency objective. |
| 41 | [RouterEval — Huang et al. (2025)](07-testing-and-benchmarking/huang-2025-routereval.md) | Supports pool-size, domain and selection-collapse analyses beyond one strong/weak pair. | No joint cost/latency evaluation; huge candidate pools exceed immediate scope. |
| 42 | [Chatbot Arena — Chiang et al. (2024)](07-testing-and-benchmarking/chiang-2024-chatbot-arena.md) | Context for preference labels, uncertainty intervals and domain variation in model comparisons. | Aggregate preference rankings do not identify the best model for each prompt. |
| 43 | [RouteProfile — Xu et al. (2026)](09-retrieval-knn-and-multiturn-routing/xu-2026-routeprofile.md) | Useful negative cold-start evidence: public metadata alone is insufficient evidence of routing competence. | Narrow study; onboarding need not become a separate research track. |
| 44 | [VDAR-Router — Tang et al. (2026)](09-retrieval-knn-and-multiturn-routing/tang-2026-vdar-router.md) | Connects task/difficulty analysis to retrieval of historical outcomes, useful for feature-design comparison. | Generating an analysis per request adds substantial overhead; different from our lightweight classification. |
| 45 | [ICL-Router — Wang et al. (2026)](09-retrieval-knn-and-multiturn-routing/wang-2026-icl-router.md) | Precedent for profiling a candidate with scored tasks rather than advertised capabilities. | Large router/embedder and profile preparation costs; secondary to the main hybrid test. |
| 46 | [GPU half-empty / SAL — Kossmann et al. (2024)](03-load-balancing/kossmann-2024-gpu-half-empty.md) | Practical estimated-wait signal and simple load-aware baselines if local telemetry is included. | Same-model replica balancing; live KV/queue integration remains conditional scope. |
| 47 | [Niyama / QoServe — Goel et al. (2025)](05-latency-and-speed/goel-2025-niyama.md) | Deadline semantics and overload handling help define the latency constraint. | Single-engine scheduling and differing versions; priority service classes are not core requirements. |
| 48 | [DistServe — Zhong et al. (2024)](05-latency-and-speed/zhong-2024-distserve.md) | Supporting source for TTFT, TPOT and goodput under latency targets. | Prefill/decode disaggregation is below the gateway and beyond the MVP. |
| 49 | [Sarathi-Serve — Agrawal et al. (2024)](05-latency-and-speed/agrawal-2024-sarathi-serve.md) | Explains batching/queueing effects and why first-token and inter-token metrics must be separate. | Single-replica scheduler; use measurement concepts rather than reimplementing scheduling. |
| 50 | [Vidur — Agrawal et al. (2024)](05-latency-and-speed/agrawal-2024-vidur.md) | Profiling/simulation reference for offline latency estimates and capacity experiments. | Hardware profiling and opaque API/network gaps; simulation cannot establish our live results. |
| 51 | [Mélange — Griggs et al. (2024)](08-system-design-gateway/griggs-2024-melange.md) | Helps justify a declared local-inference cost basis and request-size-dependent serving costs. | GPU provisioning for one model; rental economics do not directly price our owned machines. |
| 52 | [AIBrix — AIBrix Team (2025)](08-system-design-gateway/aibrix-2025-llm-inference-infrastructure.md) | Useful separation of gateway, runtime and metrics responsibilities around LLM backends. | Heavy Kubernetes stack and limited routing evidence; not a required deployment architecture. |
| 53 | [SkyServe — Mao et al. (2025)](06-error-handling-fallback/mao-2025-skyserve.md) | Precedent for cheap capacity with a more expensive fallback and recovery across failure domains. | Spot-replica provisioning rather than per-request quality-aware API selection. |
| 54 | [MTRouter — Zhang et al. (2026)](09-retrieval-knn-and-multiturn-routing/zhang-2026-mtrouter.md) | Relevant if multi-turn selection is added; history and switching frequency can affect outcome/cost. | Agent episodes and session control are not established core requirements. |
| 55 | [Whose turn is it? — Parashar et al. (2026)](09-retrieval-knn-and-multiturn-routing/parashar-2026-whose-turn-is-it.md) | Useful for accounting for prompt-cache savings lost when switching models across turns. | Narrow session setting; does not make hysteresis or managed session memory mandatory. |
| 56 | [Conformal Cascade — Dou et al. (2026)](09-retrieval-knn-and-multiturn-routing/dou-2026-conformal-cascade.md) | Optional-cascade calibration reference and example of stating an error guarantee precisely. | Finite answer sets, marginal guarantee and exchangeability; no hard per-request quality guarantee for our router. |
| 57 | [Token-uncertainty cascades — Gupta et al. (2024)](04-cost-reduction/gupta-2024-token-uncertainty-cascades.md) | Useful post-answer deferral features if the optional quality cascade is tested. | Requires token probabilities and initial generation; not the primary pre-call predictor. |
| 58 | [AutoMix — Aggarwal et al. (2024)](01-routing-algorithms/aggarwal-2024-automix.md) | Optional self-verification cascade comparison and warning that confidence is noisy. | POMDP control is excluded initially; verification and extra generation add overhead. |
| 59 | [Confidence tokens / Self-REF — Chuang et al. (2025)](02-prompt-difficulty/chuang-2025-confidence-tokens.md) | Supports calibration-aware quality escalation using correctness-labelled confidence. | LLM fine-tuning and an answer before deferral; outside the core lightweight predictor. |
| 60 | [Mixture-of-thought cascades — Yue et al. (2024)](04-cost-reduction/yue-2024-mot-cascades.md) | Optional reasoning-cascade cost accounting, including decision overhead and escalation. | Multiple samples, checkable answers and confidently wrong outputs limit general use. |

## Tier D — Peripheral or conditional: ranks 61–90

Useful background, but generally a different implementation layer or an extension outside the approved core. Low rank means lower project reading priority, not poor research.

| Rank | Paper | Relevance to our project | Main boundary or caution |
|---|---|---|---|
| 61 | [Llumnix — Sun et al. (2024)](03-load-balancing/sun-2024-llumnix.md) | Explains capacity-aware routing and queued demand for local backends. | Request/KV migration is below the gateway; no cross-model suitability selection. |
| 62 | [Mooncake — Qin et al. (2025)](03-load-balancing/qin-2025-mooncake.md) | Background on estimated TTFT, admission rejection and cache/load interactions. | Large disaggregated single-model infrastructure; no need to build its KV store. |
| 63 | [Intelligent router — Jain et al. (2024)](03-load-balancing/jain-2024-intelligent-router.md) | Supports output-length prediction as a possible latency feature. | Reinforcement-learning replica routing is outside initial scope. |
| 64 | [Preble — Srivatsa et al. (2025)](03-load-balancing/srivatsa-2025-preble.md) | Useful if prefix-cache affinity matters for repeated/session requests. | Cluster scheduling needs backend cache state; conditional scope. |
| 65 | [SkyWalker — Xia et al. (2026)](03-load-balancing/xia-2026-skywalker.md) | Illustrates avoiding overloaded replicas and spilling to available capacity. | Multi-region single-model infrastructure; no need for regional balancers. |
| 66 | [PagedAttention / vLLM — Kwon et al. (2023)](05-latency-and-speed/kwon-2023-pagedattention.md) | Important background for vLLM batching and KV-memory pressure. | Memory management does not answer our algorithmic model-choice question. |
| 67 | [LLM serving survey — Miao et al. (2025)](08-system-design-gateway/miao-2025-llm-serving-survey.md) | Broad engine-layer orientation and latency/throughput terminology. | Mostly below our selection and reliability layers. |
| 68 | [Splitwise — Patel et al. (2024)](05-latency-and-speed/patel-2024-splitwise.md) | Supporting source for prompt/decode differences and profiling by length. | Disaggregated hardware pools exceed the two-machine gateway experiment. |
| 69 | [Orca — Yu et al. (2022)](05-latency-and-speed/yu-2022-orca.md) | Foundational continuous-batching and concurrency-latency explanation. | Engine scheduling background rather than routing-algorithm evidence. |
| 70 | [SGLang — Zheng et al. (2024)](08-system-design-gateway/zheng-2024-sglang.md) | Alternative-backend reference and explanation of prefix-cache effects. | Runtime/programming framework; no direct model-selection/failover policy. |
| 71 | [EcoAssistant — Zhang et al. (2023)](04-cost-reduction/zhang-2023-ecoassistant.md) | Cheap-first execution with success feedback and retrieval of successful solutions. | Code-execution agents and quality escalation are narrower than a general gateway. |
| 72 | [ServerlessLLM — Fu et al. (2024)](06-error-handling-fallback/fu-2024-serverlessllm.md) | Background on cold starts and token-based continuation when moving inference. | Not verified cross-provider streaming recovery; cross-model continuation needs its own contract. |
| 73 | [DéjàVu — Strati et al. (2024)](06-error-handling-fallback/strati-2024-dejavu.md) | Explains recovery delays and preserving partial backend computation. | KV replication and pipeline recovery are engine responsibilities. |
| 74 | [SpotServe — Miao et al. (2024)](06-error-handling-fallback/miao-2024-spotserve.md) | Illustrates availability–cost trade-offs and expensive restarts. | Spot-GPU scheduling/reconfiguration is outside our owned-hardware gateway. |
| 75 | [MuxServe — Duan et al. (2024)](08-system-design-gateway/duan-2024-muxserve.md) | Background on contention when local LLMs share compute. | Allocates resources after a model is named; does not select by prompt suitability. |
| 76 | [AlpaServe — Li et al. (2023)](08-system-design-gateway/li-2023-alpaserve.md) | Background on sharing resources across served models. | Placement and parallelism are below the gateway. |
| 77 | [GPTCache — Bang (2023)](04-cost-reduction/bang-2023-gptcache.md) | Explains semantic answer reuse and false cache hits. | Answer caching differs from historical-outcome retrieval; not approved core scope. |
| 78 | [MeanCache — Gill et al. (2025)](04-cost-reduction/gill-2025-meancache.md) | False-hit and context cautions if answer caching is later added. | Client-side caching and federated training are outside this design. |
| 79 | [LLMLingua — Jiang et al. (2023)](04-cost-reduction/jiang-2023-llmlingua.md) | Alternative cost reduction through input-token compression. | Changes the request; needs its own quality/overhead study rather than being added to routing. |
| 80 | [LongLLMLingua — Jiang et al. (2024)](04-cost-reduction/jiang-2024-longllmlingua.md) | Relevant to a separate long-context/RAG compression experiment. | Adds compute and can alter suitability features; not core routing. |
| 81 | [Q-DAPS — Mozafari et al. (2026)](02-prompt-difficulty/mozafari-2026-q-daps.md) | Possible offline inspiration for auditing difficulty labels. | Several model calls/external lookup and restricted answers; not a lightweight request-path predictor. |
| 82 | [Uncertainty-based question difficulty — Zotos et al. (2025)](02-prompt-difficulty/zotos-2025-model-uncertainty-difficulty.md) | Illustrates combining text and uncertainty in a classical predictor. | Student exam difficulty differs from backend suitability; features require repeated model evaluation. |
| 83 | [LLM-Blender — Jiang et al. (2023)](01-routing-algorithms/jiang-2023-llm-blender.md) | Useful premise and offline pairwise-labelling context for model strengths. | Calls many models and fuses answers; generative ensembling is excluded initially. |
| 84 | [L4 / CascadeInfer — Yuan et al. (2025)](03-load-balancing/yuan-2025-l4-cascadeinfer.md) | Background on sequence length and serving capacity. | Replica stages and KV migration do not implement model selection/API fallback. |
| 85 | [Multi-tier SLA scheduling — Vestrum et al. (2026)](03-load-balancing/vestrum-2026-multi-tier-sla.md) | Conditional background for local priority reservations. | Simulation-only migration policy; service tiers are not established core scope. |
| 86 | [Speculative decoding — Leviathan et al. (2023)](05-latency-and-speed/leviathan-2023-speculative-decoding.md) | Backend acceleration context; token latency depends on decoding strategy. | Token drafting/verification is below request-level model selection. |
| 87 | [Speculative cascades — Narasimhan et al. (2025)](04-cost-reduction/narasimhan-2025-speculative-cascades.md) | Distinguishes token-level speculation from request-level routing. | Tightly coupled models/logits; not cascading across independent endpoints. |
| 88 | [POD-Attention — Kamath et al. (2025)](05-latency-and-speed/kamath-2025-pod-attention.md) | Background on backend-dependent TTFT/TPOT trade-offs. | GPU kernel optimisation; no model-selection or gateway-recovery mechanism. |
| 89 | [S-LoRA — Sheng et al. (2024)](08-system-design-gateway/sheng-2024-slora.md) | Relevant if candidates become adapters sharing a base model. | The approved project does not require adapter multiplexing. |
| 90 | [GhostServe — Jayakody et al. (2026)](06-error-handling-fallback/jayakody-2026-ghostserve.md) | Clarifies engine recovery versus gateway fallback. | KV erasure coding targets a different layer/workload; not a feature this project needs. |

## How to use the highest-ranked papers

| Project responsibility | First papers to use | What to take from them |
|---|---|---|
| Prompt classification and suitability | FORC (#1), Hybrid LLM (#2), RouteLLM (#3), RouterDC (#8), EmbedLLM (#10) | Small predictors, per-model outcome labels and feature ablations. A universal easy/hard label is not enough. |
| Historical-performance evidence | Past-performance retrieval (#4), PORT (#9), Shnitzer et al. (#17), Avengers-Pro (#20) | Retrieval-only baselines, low-data tests and held-out-domain checks. Keep evaluated outcomes out of retrieval history. |
| Constrained selection and closest prior art | Cascade Routing (#5), RouteBalance (#6), CSCR (#7), FORC (#1) | Formalise constraints and compare against simple utility/threshold policies. Average budgets are not hard per-request guarantees. |
| Affordable evaluation | LLMRouterBench (#11), RouterBench (#12), RouterArena (#28), HELM (#30) | Licensed stored outcomes, common splits, simple baselines, ablations and uncertainty. Replay cannot establish current provider latency. |
| Latency prediction/measurement | Etalon (#14), INFaaS (#32), Clockwork (#33), SLOs-Serve (#34), GORGO (#35) | Define deadline semantics; separate overhead, TTFT and completion time; measure prediction error and actual violations. |
| Operational recovery | ContinuityBench (#13), ResilienceBench-Operator (#15), FailureAtlas (#22), Metastable Failures (#23), GenAI incidents (#24) | Bound attempts, preserve supplied context, account for consumed cost/time and inject slow, failed and malformed responses. |
| Optional quality cascade | FrugalGPT (#16), Conformal Cascade (#56), token-uncertainty cascades (#57), AutoMix (#58) | Study after the core; charge all generation and verifier calls. Report separately from operational failover. |

**Suggested reading sequence:** FORC → Hybrid LLM → RouteLLM → past-performance retrieval → Cascade Routing → RouteBalance. Next, read RouterBench and LLMRouterBench before fixing the data plan, and Etalon, ContinuityBench and ResilienceBench-Operator before fixing timing/fault experiments. CSCR, RouterDC, PORT and EmbedLLM complete the essential set.

## Implications for our literature review

- The main story should be **predict suitability → enforce constraints → select → execute with bounded recovery**, rather than a catalogue of GPU optimisations.
- FrugalGPT remains foundational, but its completed-answer cascade is optional in our current scope. It is not the sole justification for operational fallback.
- Discuss RouteBalance explicitly because joint quality–cost–latency selection overlaps our problem. Neither this ranking nor a survey establishes that our combination is novel or will outperform simple alternatives.
- Multi-turn hysteresis, semantic answer caching, GPU telemetry and custom scheduling do not become mandatory because older notes recommend them. Retrieving scored historical examples is also different from returning cached answers.
- No single paper supplies the whole system. The contribution remains the decision policy, integration and empirical evaluation, including a negative or inconclusive hybrid result.

## Coverage check

All 90 individual paper records in topics 01–09 are included exactly once. Topic counts: 01 = 11; 02 = 11; 03 = 11; 04 = 10; 05 = 10; 06 = 10; 07 = 9; 08 = 9; 09 = 9. Original research material and individual paper records remain unchanged.
