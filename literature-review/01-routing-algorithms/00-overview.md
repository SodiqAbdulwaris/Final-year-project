# Topic 01: AI model routing algorithms (overview)

Verified 2026-10-31. Eleven full paper files (ten seed papers plus one added by the discovery search), all published 2023 or later, all read in full text (survey paradigm sections skimmed, see their files).

## 1. Topic definition and why it matters to the router
Model routing is the choice, for each incoming request, of which LLM (or which cascade of LLMs) should answer, trading quality against cost and sometimes latency. Methods fall into pre-generation routers (a classifier, embedding or preference model picks one model before any generation), cascades (a cheap model answers, a verifier or confidence score decides whether to escalate) and ensembles (query many models and combine). For the AI Request Router this topic supplies the core decision logic: the difficulty/quality predictor, the cost-versus-quality scoring function with a tunable threshold, the evaluation metrics and the known failure modes (out-of-distribution queries, noisy labels, stale model pools). It does not supply what the project adds on top: live backend load, latency budgets, failover and self-hosted serving.

## 2. Comparison table
| Paper | Year | Type | Venue | Problem | Method | Key result | Limitation |
|---|---|---|---|---|---|---|---|
| [FrugalGPT](chen-2024-frugalgpt.md) | 2023 preprint, TMLR Dec 2024 | method / position | TMLR | API cost differs ~100x | Learned cascade with DistilBERT scorer | Up to 98% saving at GPT-4 accuracy (HEADLINES 98.3%) | Sequential latency; in-distribution labels; no load |
| [LLM-Blender](jiang-2023-llm-blender.md) | 2023 | method + dataset | ACL | Best open LLM varies per input | Pairwise ranker plus generative fusion | GPT-Rank 3.01 vs 3.90 best single | Runs all N models per query |
| [Zooter](lu-2024-zooter.md) | 2023 preprint, 2024 | method | NAACL | Ensemble without running all models | Reward distillation to 86M router | MTR 1.94 vs 2.23 best single | Fixed 13B pool; noisy rewards |
| [Shnitzer et al.](shnitzer-2023-benchmark-routing.md) | 2023 | method + study | preprint (workshop version) | Pick LLM for new task from benchmarks | Per-LLM kNN correctness predictors | 0.694 vs 0.688 best-on-average, smaller models; predictors 0.59 OOD | Weak OOD; small gain |
| [Hybrid LLM](ding-2024-hybrid-llm.md) | 2024 | method | ICLR | Small vs large model per query | DeBERTa quality-gap router, three label designs | Up to 40% fewer large calls, no drop | Two models; no OOD |
| [AutoMix](aggarwal-2024-automix.md) | 2024 | method | NeurIPS | Cascade with noisy self-check | Few-shot self-verification plus POMDP | Over 50% cost cut at comparable quality | Context tasks only; sequential calls |
| [RouterDC](chen-2024-routerdc.md) | 2024 | method | NeurIPS | Several models equally good | Dual contrastive losses on LLM embeddings | 58.54% vs 54.56% best single; survives model removal | 7-8B models; accuracy only |
| [RouteLLM](ong-2025-routellm.md) | 2025 | method + framework | ICLR | Strong/weak routing from preferences | Four routers on Arena data plus augmentation | 3.66x fewer GPT-4 calls than random routing at 95% quality (MT-Bench) | Two models; fixed price |
| [CSCR (Shirkavand et al.)](shirkavand-2025-cscr.md) | 2025 | method | NeurIPS | Cost-aware routing over dynamic pools | Cost-banded contrastive router, logit and perplexity fingerprints, k-NN lookup | Highest AUDC on EmbedLLM, MixInstruct, RouterBench; robust to new models | Static cost; no live load |
| [Varangot-Reille et al.](varangot-reille-2026-routing-survey.md) | 2026 (preprint 2025) | survey | JAIR | Unify routing view | Objective / timing / strategy taxonomy | Lightweight pre-generation routers suffice | No live-load view |
| [Moslem & Kelleher](moslem-2026-routing-cascading-survey.md) | 2026 | survey | TMLR | Map routing and cascading | Six paradigms plus when/what/how framework | Evaluations not comparable; four failure modes | No re-evaluation |

## 3. Themes and how the papers relate
**From ensembling to single-call routing.** LLM-Blender (2023) established that the best model changes per input but paid for all models; Zooter, RouterDC and Shnitzer et al. keep the diversity and call one model, with RouterDC measuring about 6x faster inference than voting. Hybrid LLM and RouteLLM narrow this to the strong/weak decision with a threshold.

**Where the quality label comes from.** Each paper answers this differently: benchmark correctness (Shnitzer, RouterDC), BART-score gaps (Hybrid LLM), reward-model scores (Zooter), human preferences plus judge or gold augmentation (RouteLLM), model self-verification (AutoMix), a trained scorer (FrugalGPT). Label noise recurs (Zooter's tag smoothing, Hybrid LLM's soft labels and transformation).

**Generalisation is the weak point.** Shnitzer et al. measure 0.59 predictor accuracy out of distribution; RouteLLM's Arena-only routers sit near random on MMLU and GSM8K until augmented; RouterDC gains only about 1.9 points out of distribution. Few papers test new model pairs (RouteLLM and Hybrid LLM do, partially).

**Routing versus cascading.** FrugalGPT and AutoMix spend extra calls to learn from a first answer, while Hybrid LLM, RouteLLM and RouterDC avoid them. The surveys treat the two as points on one design space, with production systems combining both.

**The field matured into surveys.** Varangot-Reille et al. give the formal budget-constrained definition; Moslem and Kelleher add a design-space view and conclude that evaluations are not comparable across papers.

## 4. Strongest three papers for the proposal
1. **RouteLLM (Ong et al., 2025):** the closest published analogue to the project's classifier router, with a tunable threshold, four router designs (including a cheap embedding-based one), CPT/APGR metrics, an out-of-domain test, measured router overhead and open code.
2. **Moslem & Kelleher (2026):** the current map of the field, with the failure modes (distribution shift, staleness, routing collapse) and the evaluation-comparability problem that justify the project's benchmark design and gap statement.
3. **Hybrid LLM (Ding et al., 2024):** the clearest recipe for quality-gap labels from sampled responses, soft labels for noise, a data transformation for lopsided pairs and threshold calibration on a small validation set.

Honourable mentions: Shnitzer et al. (embeddings plus a simple classifier and leave-one-task-out testing match the planned sentence-transformers and scikit-learn stack, but it is preprint only) and Varangot-Reille et al. (formal definition, standard baselines).

## 5. Gaps visible in this topic (with evidence)
1. **No live system state.** None of the eleven papers uses queue depth, GPU load or backend health as a routing input. Costs are token prices or call counts (RouteLLM Table 6, Hybrid LLM "cost advantage", AutoMix relative units). Moslem and Kelleher list serving metrics only as evaluation metrics. The closest joint work is outside this topic (RouteBalance in topic 03), which should be checked before the "together" claim is worded.
2. **No failover or reliability handling.** FrugalGPT mentions provider unavailability as motivation only; RouterDC's Table 3 simulates losing a model but not timeouts or rate limits. Quality-based escalation (AutoMix, FrugalGPT) is not operational fallback.
3. **Latency budgets are absent.** Latency appears as a cost to minimise (Varangot-Reille et al.) or as router overhead (RouteLLM, Hybrid LLM), never as a per-request constraint.
4. **Mostly two-model, fixed-pool routing.** RouteLLM and Hybrid LLM are binary; Zooter and RouterDC need retraining for a new pool (Moslem and Kelleher's "staleness").
5. **Weak out-of-distribution evidence and non-comparable evaluation** (Shnitzer 0.59; Moslem and Kelleher Section 9.3).
6. **Recent 2026 preprints start to close parts of gaps 1 and 3 (abstract-level reading only, not peer reviewed as far as I could see):** *Robust Batch-Level Query Routing under Cost and Capacity Constraints* (Markovic-Voronov et al., arXiv 2603.26796) routes batches under cost, GPU and concurrency limits; *CEMA-Router* (arXiv 2610.26171) uses node profiles and backlog estimates for cloud-edge batch routing; *RouterWorld* (arXiv 2610.26511) is a latency-aware routing benchmark with hardware latency annotations and finds most routers neglect latency; *You Cannot Pick a Provider From the Price List* (arXiv 2609.37902) routes among live providers using measured latency, availability and a fallback anchor. RouteBalance (topic 03) is the closest joint model-plus-load router, and the open-source vLLM Semantic Router (see `../competitors/vllm-semantic-router.md`) already does per-prompt selection with runtime latency statistics and self-hosted vLLM backends. The gap should therefore be worded as "absent from the peer-reviewed routing literature up to 2025 and only emerging in very recent preprints", not as "nobody has done it".
7. **Self-hosted serving is not considered.** All experiments use API prices or offline outputs; AutoMix notes only that a local 13B model could be nearly free.

## 6. Paper files
- [chen-2024-frugalgpt.md](chen-2024-frugalgpt.md)
- [jiang-2023-llm-blender.md](jiang-2023-llm-blender.md)
- [lu-2024-zooter.md](lu-2024-zooter.md)
- [shnitzer-2023-benchmark-routing.md](shnitzer-2023-benchmark-routing.md)
- [ding-2024-hybrid-llm.md](ding-2024-hybrid-llm.md)
- [aggarwal-2024-automix.md](aggarwal-2024-automix.md)
- [chen-2024-routerdc.md](chen-2024-routerdc.md)
- [ong-2025-routellm.md](ong-2025-routellm.md)
- [shirkavand-2025-cscr.md](shirkavand-2025-cscr.md) (added by discovery search)
- [varangot-reille-2026-routing-survey.md](varangot-reille-2026-routing-survey.md)
- [moslem-2026-routing-cascading-survey.md](moslem-2026-routing-cascading-survey.md)

### Related papers documented elsewhere
- Topic 02: [Routoo](../02-prompt-difficulty/mohammadshahi-2024-routoo.md), [Chuang confidence tokens](../02-prompt-difficulty/chuang-2025-confidence-tokens.md), [Zhu hidden-state difficulty](../02-prompt-difficulty/zhu-2025-llm-already-knows.md), [Zhao difficulty prediction](../02-prompt-difficulty/zhao-2025-reasoning-efficiency-difficulty.md), [Q-DAPS](../02-prompt-difficulty/mozafari-2026-q-daps.md), [FamiCom](../02-prompt-difficulty/li-2024-famicom.md), [Zotos](../02-prompt-difficulty/zotos-2025-model-uncertainty-difficulty.md), [Kadavath](../02-prompt-difficulty/kadavath-2022-know-what-they-know.md)
- Topic 03: [Jain intelligent router](../03-load-balancing/jain-2024-intelligent-router.md), [Llumnix](../03-load-balancing/sun-2024-llumnix.md), [Preble](../03-load-balancing/srivatsa-2025-preble.md), [RouteBalance](../03-load-balancing/da-2026-routebalance.md)
- Topic 04: [Cascade routing (Dekoninck)](../04-cost-reduction/dekoninck-2025-cascade-routing.md), [BEST-Route](../04-cost-reduction/ding-2025-best-route.md), [MoT cascades (Yue)](../04-cost-reduction/yue-2024-mot-cascades.md), [EcoAssistant](../04-cost-reduction/zhang-2023-ecoassistant.md)
- Topic 07 (RouterBench, MT-Bench, EmbedLLM and others) and topic 06: not yet written when this overview was made; link when available.

## 7. Search log (feeds Table 2.1)
Two phases. Phase A (2026-10-30 to 10-31) verified the ten seed papers supplied by the supervisor and the user's notes. Phase B (2026-10-31) was a discovery search, run after the supervisor asked for one.

**Phase B databases, strings and counts**
| Source | String or action | Result |
|---|---|---|
| arXiv search page (abstract field, all dates) | "LLM routing" OR "model routing" OR "query routing" | 327 results; titles of the 38 top-ranked and 37 most recent screened (about 60 unique; relevance order was dominated by September to October 2026 preprints) |
| Web search (standard) | "LLM routing" cost quality router preference data cascade paper arXiv 2025 | RouteLLM only; no new candidate |
| Web search (standard) | RouterBench benchmark multi-LLM routing system Hu et al. ICML | RouterBench (topic 07 owns it) |
| Web search (extended) | "model routing" OR "query routing" cost-aware router 2025 2026 NeurIPS ICLR ACL accepted | CSCR (NeurIPS 2025), MTRouter (ACL 2026), batch-level routing (arXiv 2026), TwinRouterBench, SeqRoute |
| Web search restricted to aclanthology.org | LLM routing cost quality router query model selection | about 10 hits (FLARE and MTRouter at ACL 2026, plus arXiv-linked ones) |
| Web search restricted to openreview.net, dl.acm.org, ieeexplore.ieee.org, mlr.press | "LLM routing" survey OR benchmark OR router cost-aware 2025 | about 10 hits (Causal LLM Routing, Carrot, Dynaroute, LLMRouterBench, RouterEval, surveys); no PMLR hit |
| arXiv API, Semantic Scholar API, dblp, ACL Anthology search page, OpenReview pages | attempted | blocked or rate-limited (429, bot check, JavaScript-only page); not bypassed |
| Google Scholar | not run | no scripted access; the supervisor may run the same string by hand |

**Counts (Phase B):** about 75 distinct titles screened by title, 12 read at abstract level or beyond, 1 included as a full file (CSCR; peer-reviewed NeurIPS 2025, matches the planned embedding-plus-k-NN stack). Phase A plus B overall: 11 included.

**Excluded after screening, with reason**
- Routing preprints relevant to the gap but abstract-only and not peer reviewed at the time of search: Markovic-Voronov et al. 2026 (arXiv 2603.26796), CEMA-Router (2610.26171), RouterWorld (2610.26511), market-aware routing (2609.37902). Kept as pointers in section 5; topic 03 or 07 may want full files.
- Benchmarks owned by topic 07: RouterBench, RouterEval, LLMRouterBench, SPROUT, RouterArena, EmbedLLM.
- Peer-reviewed but not read: MTRouter (ACL 2026, multi-turn routing), FLARE (ACL 2026, length-aware routing); relevant if the report needs multi-turn routing.
- Seen in results, venue not verified: Router-R1 (arXiv 2506.09033), Carrot (2502.03261), Causal LLM Routing (2505.16037, OpenReview), IPR (2509.06274), PickLLM (2412.12170), R2-Router (2602.02823), RerouteGuard (2601.21380, adversarial risks to routers).
- Off topic: image-editing and mixture-of-experts layer routing, agent memory and non-LLM routing results.

**Dropped from the seed list:** none.

**Repeat it:** run the arXiv abstract query above and the same strings on Semantic Scholar and Google Scholar for 2020 to 2026; the field adds many papers per month, so counts will change.

## 8. Corrections to the user's notes and open verification points
- **Year and venue upgrades:** FrugalGPT is TMLR, December 2024; Zooter is NAACL 2024 (DOI 10.18653/v1/2024.naacl-long.109); LLM-Blender is ACL 2023 (DOI 10.18653/v1/2023.acl-long.792); Hybrid LLM is ICLR 2024; RouteLLM is ICLR 2025; RouterDC and AutoMix are NeurIPS 2024; Varangot-Reille et al. is JAIR vol. 86, **2026** (DOI 10.1613/jair.1.19801), not 2025; Moslem and Kelleher is TMLR, August 2026.
- **Shnitzer et al.:** I found only an arXiv preprint and a NeurIPS 2023 DistShift workshop version. OpenReview lists a "COLM" entry, which I could not confirm as an accepted paper.
- **AutoMix author order** in the user's reference list is alphabetical, not the paper's order.
- **RouterDC abstract** says +2.76% in-distribution, but Table 1 gives +3.98 points over the best single LLM and +2.77 over LoraRetriever; the file uses table values.
- **Numbers read from arXiv preprints, not camera-ready versions:** FrugalGPT, Hybrid LLM, Zooter, RouterDC (v1 of each); Varangot-Reille (v3, before the JAIR version). Check against final versions if exact figures are quoted.
- **No DOI exists** for ICLR, NeurIPS or TMLR papers; references give the venue URL plus the arXiv DOI.
- **Not checked:** editor lists for the two NeurIPS references; the independent RouterBench study cited by Varangot-Reille et al. about AutoMix.
