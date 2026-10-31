# Topic 09: past-performance retrieval, k-NN routing, multi-turn and session routing (overview)

## 1. Topic definition and why it matters to the router
This topic covers routers that estimate a model's chance of success on a new request by looking up how models performed on similar past requests (nearest neighbours, clusters, retrieval), and routers that decide across the turns of a session, where switching models changes cost and context. The team design guide (26 Oct 2026, summarised in `proposal-drafts/team-design-guide-notes.md`) makes k-NN over past per-model outcomes the competence estimate, treats the learned difficulty classifier as optional, and adds session-aware hysteresis, calibration checks and a minimum-evidence rule. The papers below show how simple retrieval compares with learned routers, how new models can enter the pool, what switching costs when prompt caches are lost, and how much of the evaluation (intervals, calibration) the literature actually provides.

## 2. Comparison table
| Paper (file) | Year | Type | Venue | Problem | Method | Key result | Limitation |
|---|---|---|---|---|---|---|---|
| [Varangot-Reille et al.](varangot-reille-2026-contextualrouter.md) | 2026 | method / study | EACL 2026 SRW | Generalise to new models without retraining | Retrieve k = 40 similar queries; attention-weighted ContextualRouter vs plain k-NN | k-NN as good as learned router; works with 1% history; k > 40 no gain | Flawed labels, easy retrieval, no calibration or intervals |
| [Wu & Silwal (PORT)](wu-2025-port-online-routing.md) | 2025 | method + theory | NeurIPS 2025 | Online routing under token budget | HNSW neighbour means (k = 5); dual weights from early queries | 3.55× performance, 1.85× cost efficiency over baselines | Quality and cost only, excludes system load |
| [Zhang et al. (Avengers-Pro)](zhang-2025-avengers-pro.md) | 2025 | method | DAI 2025 | Training-free cost-quality routing | Embed, 60 k-means clusters, α-weighted score, nearest clusters | +7% accuracy at similar cost; 27% cheaper at equal accuracy | Frontier models, single split, no calibration |
| [Wang et al. (ICL-Router)](wang-2026-icl-router.md) | 2026 | method | AAAI 2026 | Add models without retraining | LLM router reads (query, correct?) profiles in context | 76.30 vs EmbedLLM 74.16 avg | 7B router, small pool |
| [Xu et al. (RouteProfile)](xu-2026-routeprofile.md) | 2026 | method / study | preprint | Cold start with no interaction data | Graph of public model-card signals | Text profiles route almost no queries correctly to a new model | One new model |
| [Tang et al. (VDAR-Router)](tang-2026-vdar-router.md) | 2026 | method | preprint (EMNLP 2026 Findings accepted) | Better neighbours for retrieval routing | LLM-written difficulty analysis as retrieval key | Best reward on RouterBench and LLMRouterBench | 1.46 s per query; one seed |
| [Dou et al. (Conformal Cascade)](dou-2026-conformal-cascade.md) | 2026 | method + theory | preprint | Error guarantee for cascades | Conformal prediction sets decide deferral | Beats best heuristic in 49 of 72 pairs | Marginal guarantee, MC only, post-generation |
| [Zhang et al. (MTRouter)](zhang-2026-mtrouter.md) | 2026 | method | ACL 2026 | Turn-level model choice in agent episodes | History–model embeddings, outcome estimator | 58.7% lower cost than GPT-5 on ScienceWorld | Cache loss unmeasured, no hysteresis |
| [Parashar et al.](parashar-2026-whose-turn-is-it.md) | 2026 | study + cost model | preprint | Session routing and switch cost | Zero-shot per-turn routers; cache break-even formula | History +3.3 points; down-switch repays in about 1.25 calls | One domain, two models |

## 3. Themes and trends
**Retrieval is a strong baseline.** Varangot-Reille et al. (2026) find a plain k-NN average matches a learned attention router and works with 1% of the history; Avengers-Pro (Zhang et al., 2025) and PORT (Wu & Silwal, 2025) also use no trained network, and both beat trained or exact-search baselines on their benchmarks. VDAR-Router (Tang et al., 2026) goes the other way and beats a k-NN baseline by changing what is retrieved (an LLM-written difficulty analysis), at about 1.4 s of extra latency per request.

**Neighbourhood size varies and is rarely justified.** Reported choices are k = 40 (EACL, no gain beyond it, smaller k better for cost-performance and larger k better for peak performance), k = 30 (VDAR), k = 5 (PORT) and 60 clusters with the nearest few clusters used (Avengers-Pro). Embedding model size matters little in the EACL and PORT experiments.

**Cold start is a spectrum.** With no data at all (RouteProfile, Xu et al., 2026) public model-card information routes almost no queries correctly to a new model. Running the new model on a stored set (ICL-Router, the EACL paper, PORT, Avengers-Pro) works with little data and no retraining. This is the practical basis for a minimum-evidence rule.

**Guarantees exist, but only in cascades.** Conformal Cascade (Dou et al., 2026) gives a distribution-free error bound under exchangeability; no paper applies calibration (Platt or isotonic scaling, reliability tables, Brier scores) to the neighbour-averaged success estimate that a k-NN router produces. The calibration literature in topic 02 ([Kadavath et al., 2022](../02-prompt-difficulty/kadavath-2022-know-what-they-know.md); [Xiong et al., 2024](../02-prompt-difficulty/xiong-2024-llm-uncertainty-calibration.md)) concerns model confidence, not retrieval-based estimates.

**Sessions change the problem.** MTRouter (Zhang et al., 2026) shows that stable use of a model with fewer switches beats a reactive router, and notes that switching loses prompt-cache reuse; Parashar et al. (2026) quantify it: session history improves routing at equal offload, a downward switch repays within about one turn, and a late upward switch does not. Evidence is limited to agent tasks with two to six models and short sessions.

**Evaluation reporting is thin.** Most papers use one seed and one split (EACL, VDAR, Avengers-Pro, ICL-Router); MTRouter reports three runs with ± intervals; Dou et al. tune on the test set and could not compute bootstrap intervals. Paired comparisons with intervals are not reported.

## 4. Strongest three papers for the proposal
1. **Varangot-Reille et al. (2026).** The only paper that tests k-NN retrieval against learned routers across five benchmarks, with sweeps over k, embedding size, history size and paraphrase degradation. It directly supports RQ1 and the optional-classifier decision. Peer-reviewed (EACL SRW, a student workshop).
2. **Parashar et al. (2026).** The only quantitative treatment of switching cost with prompt caching, with a break-even formula and the asymmetry between down- and up-switches. It supports the hysteresis design (RQ2). Preprint.
3. **Wu & Silwal (2025).** Combines nearest-neighbour estimates with token-budget enforcement and tests robustness to query volume, arrival order and embedding choice. Peer-reviewed at NeurIPS. Note that it explicitly leaves system load outside its model.
Runner-up: MTRouter (peer-reviewed at ACL 2026) for turn-level routing with intervals.

## 5. What the project must decide (my synthesis from the evidence above, not claims by the papers)
| Decision | What the papers give | Open point for the project |
|---|---|---|
| k | 40 (EACL; no gain above, smaller k cheaper), 30 (VDAR), 5 (PORT), 60 clusters (Avengers-Pro) | Sweep roughly 5–80 on a held-out split and report the cost-quality curve; choose by validation, not by the test set |
| Similarity weights | EACL learns attention weights but plain unweighted k-NN did as well; none test distance-weighted k-NN directly | Compare unweighted, similarity-weighted and thresholded neighbours; keep the simplest if the difference is within the interval |
| Minimum-evidence rule | None; RouteProfile shows unknown models are not routed well | Require a minimum number of neighbours above a similarity cutoff per model before trusting an estimate; otherwise treat the model as "unknown", not "good" |
| Calibration check | Conformal calibration (Dou et al.) for cascades only; confidence calibration in topic 02 | Reliability table and Brier score on a validation split; isotonic or Platt recalibration only if needed; conformal lower bound as an option |
| Hysteresis thresholds | Parashar (asymmetric switch cost, sticky switching); MTRouter (fewer switches helps) | Required estimate margin and number of turns before switching; free downward switches early; hard-failure and capability exceptions |
| Cache effects of switching | Break-even k = 1.25 calls in one price configuration; local servers not studied | Measure prefix-cache reuse on the chosen local backends and API providers, then reuse the formula with measured numbers |
| Evaluation | Rarely paired; intervals in MTRouter only | Declare the primary metric and non-inferiority margin first; paired differences with 95% intervals on the same queries; separate validation and test; hold out whole datasets to avoid easy-retrieval inflation |

## 6. Gaps visible in this topic (feeds the project gap statement)
1. **No minimum-evidence or abstention rule in retrieval routers.** The EACL paper, PORT, Avengers-Pro and VDAR-Router average neighbours without stating when evidence is too thin; RouteProfile shows that a model with no data is routed poorly.
2. **Neighbour-averaged success estimates are not calibrated or evaluated for calibration.** The EACL paper reports MSE and NDCG, PORT and Avengers-Pro report totals or relative scores; Conformal Cascade provides guarantees only for cascades under exchangeability and states that covariate shift needs recalibration.
3. **Switching cost is modelled in one paper only.** Parashar et al. (two-model pools, spreadsheet agents) give a formula; MTRouter acknowledges the loss without measuring it; no study covers local servers, hysteresis thresholds or hard-failure exceptions.
4. **Live load is explicitly out of scope in the retrieval work.** PORT states that operational-state features such as traffic or system load fall outside its formulation; no paper combines retrieval-based competence with live backend state.
5. **Single-turn benchmarks dominate the retrieval evidence.** The k-NN results come from RouterBench, SPROUT, LiveBench, BigGenBench and similar sets; session routing is evaluated on agent tasks. Chat sessions with a mix of turns are not covered.
6. **Statistical reporting is weak.** Single seeds and no paired intervals in most papers, test-set tuning in Conformal Cascade; benchmark labels are flawed (acknowledged in the EACL paper) and judge-based in places.
7. **No routing-specific calibration paper found.** My arXiv searches for Platt, isotonic or reliability-table calibration of LLM routing success probabilities returned no matching paper; this is a possible contribution or a possible search miss (see the search log).

## 7. Which topic-07 datasets the k-NN experiment (E1) can use
- **[RouterBench](../07-testing-and-benchmarking/hu-2024-routerbench.md):** 405,467 pre-computed samples, 11 models, 8 datasets plus a RAG set, with prompt, response, performance, cost and true label per row, and a ready cost-quality metric (AIQ) and baselines. It is already used by the EACL paper, PORT and VDAR-Router, so results are comparable. Cautions: GPT-4-judged labels for MBPP, MT-Bench and RAG; MT-Bench has only 80 questions so is excluded from training in the original paper; cost is API price; its 11-model pool is dated.
- **[LLMRouterBench](../07-testing-and-benchmarking/li-2026-llmrouterbench.md):** 391,645 instances, 21 datasets, 33 models, with two settings (20 lightweight roughly 7B models on 15 datasets, and 13 flagship models on 10 datasets) and metrics Gain, Gap@O, CostSave and ParetoDist. The lightweight setting is the closer stand-in for local models, the flagship setting for hosted ones. VDAR-Router and Avengers-Pro use it.
- **Also usable:** [EmbedLLM's dataset](../07-testing-and-benchmarking/zhuang-2025-embedllm.md) (112 models × 36,054 questions, binary correctness, already embedded with all-mpnet-base-v2) and [RouterEval](../07-testing-and-benchmarking/huang-2025-routereval.md) (large pools).
- **Cautions for any of them:** benchmark questions share formats, which makes retrieval look easier than real traffic (acknowledged in the EACL paper), so hold out entire datasets and add a paraphrase test; none records latency or load, so E2, E4 and E5 need the project's own logs; the guide's three to four candidate models would be a sampled subset of these pools.

## 8. Links to paper files
- [varangot-reille-2026-contextualrouter.md](varangot-reille-2026-contextualrouter.md): the EACL 2026 SRW paper "Generalising LLM Routing using Past Performance Retrieval: A Few-Shot Router is Sufficient" (DOI 10.18653/v1/2026.eacl-srw.22). Title, authors, venue, pages and DOI match the ACL Anthology entry; the file name uses the paper's method name (ContextualRouter) and is not the JAIR survey.
- [zhang-2026-mtrouter.md](zhang-2026-mtrouter.md)
- [tang-2026-vdar-router.md](tang-2026-vdar-router.md)
- [wu-2025-port-online-routing.md](wu-2025-port-online-routing.md)
- [zhang-2025-avengers-pro.md](zhang-2025-avengers-pro.md)
- [wang-2026-icl-router.md](wang-2026-icl-router.md)
- [xu-2026-routeprofile.md](xu-2026-routeprofile.md)
- [dou-2026-conformal-cascade.md](dou-2026-conformal-cascade.md)
- [parashar-2026-whose-turn-is-it.md](parashar-2026-whose-turn-is-it.md)

### Related papers documented elsewhere
- 01 Routing algorithms: [Hybrid LLM](../01-routing-algorithms/ding-2024-hybrid-llm.md), [RouteLLM](../01-routing-algorithms/ong-2025-routellm.md), [Benchmark-dataset routing with k-NN (Shnitzer et al.)](../01-routing-algorithms/shnitzer-2023-benchmark-routing.md), [RouterDC](../01-routing-algorithms/chen-2024-routerdc.md), [FrugalGPT](../01-routing-algorithms/chen-2024-frugalgpt.md), [AutoMix](../01-routing-algorithms/aggarwal-2024-automix.md); the JAIR routing survey by Varangot-Reille et al. is homed there.
- 02 Prompt difficulty: [Šakota et al. (2024)](../02-prompt-difficulty/sakota-2024-fly-swat-or-cannon.md), [Routoo](../02-prompt-difficulty/mohammadshahi-2024-routoo.md), [Kadavath et al. (2022)](../02-prompt-difficulty/kadavath-2022-know-what-they-know.md), [Xiong et al. (2024)](../02-prompt-difficulty/xiong-2024-llm-uncertainty-calibration.md), [Zhu et al. (2025)](../02-prompt-difficulty/zhu-2025-llm-already-knows.md)
- 03 Load balancing: [Preble](../03-load-balancing/srivatsa-2025-preble.md) (prefix sharing on the serving side)
- 04 Cost reduction: [Token-uncertainty cascades](../04-cost-reduction/gupta-2024-token-uncertainty-cascades.md), [Cascade routing](../04-cost-reduction/dekoninck-2025-cascade-routing.md)
- 07 Testing and benchmarking: [RouterBench](../07-testing-and-benchmarking/hu-2024-routerbench.md), [LLMRouterBench](../07-testing-and-benchmarking/li-2026-llmrouterbench.md), [EmbedLLM](../07-testing-and-benchmarking/zhuang-2025-embedllm.md), [RouterEval](../07-testing-and-benchmarking/huang-2025-routereval.md)
- Topic 10 (conversation memory: LongMemEval, Zep) is handled elsewhere.

## 9. Search log
All lookups were done on 2026-10-31.

| Source | Search (strings) | Result |
|---|---|---|
| ACL Anthology | Entry pages for 2026.eacl-srw.22 and 2026.acl-long.2045 | Titles, authors, pages and DOIs of the two named papers confirmed |
| arXiv API | `id:2607.18098`; title or keyword queries: "Past Performance Retrieval", "MTRouter", multi-turn + routing + session, model switching + KV cache + routing, "Avengers" + routing, "performance-efficiency optimized routing", nearest neighbor + routing + LLM, "few-shot router", "conformal" + routing + LLM, calibration + LLM routing + success probability, "cold-start" + router + LLM, new model + routing + without retraining, session + routing + prefix cache | MTRouter and VDAR-Router found; the EACL paper is not on arXiv under that title; several candidate papers found; the calibration and "few-shot router" queries returned nothing |
| arXiv abstract pages | Comments and journal-reference fields for 12 candidate papers | Venue hints: VDAR (EMNLP 2026 Findings), MTRouter (ACL 2026), Avengers-Pro (DAI 2025), PORT (NeurIPS 2025), ICL-Router (AAAI 2026), RouteNLP (ACL 2026 Industry), Task-aware cold start (ACL 2026 Main) |
| Crossref API | DOI lookups for Avengers-Pro (10.1145/3772429.3772445) and ICL-Router (10.1609/aaai.v40i39.40628) | Venue, pages and year confirmed for both; the ACM page itself returned HTTP 403 |

Counts: **14 papers found, 14 screened, 9 included as full files, 0 dropped, 5 found but not reviewed in full.** The three must-include papers (EACL, MTRouter, VDAR-Router) are included. All nine are dated 2020 or later and were read in full text (appendices skimmed).

Found but not included (screened by title and arXiv listing only; candidate extras):
- RouteNLP: closed-loop routing with conformal cascading (arXiv:2604.23577, ACL 2026 Industry Track): a second conformal paper, with industry framing.
- Task-aware LLM routing with profile-guided data synthesis for cold-start scenarios (arXiv:2604.09377, ACL 2026 Main): another cold-start paper.
- SeqRoute: global budget-aware sequential routing via offline reinforcement learning (arXiv:2605.25424): budgeted sequential routing; reinforcement learning is outside the guide's scope.
- Context Is Not Free: carbon-aware routing for multi-turn services (arXiv:2610.35230): multi-turn context costs in a different objective (carbon).
- IRT-Router (arXiv:2506.01048): item-response-theory routing with a cold-start angle; it is also a baseline in VDAR-Router.

Caveats and unverified items:
- VDAR-Router: the arXiv comment says "Accepted by EMNLP 2026 Findings" but no proceedings entry was found, so it is cited as a preprint. Its main results table extracted badly, so I quote only text statements and the latency table.
- MTRouter and PORT, ICL-Router, Avengers-Pro were read as arXiv versions, not the proceedings PDFs. PORT's proceedings page and volume were not located.
- Avengers-Pro: its text says both top-4 and "three" clusters, and its caption and text give different α values for the +7% result; both are flagged in the file.
- RouteProfile: the text says Single-Best is 0.547 while Table 1 as extracted shows 0.508; flagged in the file.
- ICL-Router: author order is from arXiv v3, not checked against the AAAI page.
- Parashar et al.: model names in the paper are pseudonyms; only the Opus pair has exact routed costs.
- Word counts: sections 1–8 of the nine paper files are 750–924 words; four exceed the 900-word target slightly (EACL 924, VDAR 917, Parashar 906, Dou et al. 902).
