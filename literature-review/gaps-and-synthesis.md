# Gaps and synthesis (supervisor)

Built from the eight topic overviews and the competitors review. Every gap names its evidence. Where a source is a preprint or grey literature, the gap statement says so. Objectives O1–O6 are the drafts in `../proposal-drafts/ch1-introduction.md`.

## 1. What the literature shows

1. **Routing quality is well studied; routing under load is not.** Routers learn to pick a model from preference or benchmark data (RouteLLM, Hybrid LLM, RouterDC, Zooter, Routoo) and to cascade (FrugalGPT, AutoMix, Dekoninck et al.). Cost is a token price or call count. No peer-reviewed method in topics 01, 02 or 04 uses queue depth, GPU use or backend health as a routing input.
2. **Load balancing is well studied only inside one engine or one model.** Llumnix, Preble, Mooncake and the L4/SLOs-Serve/Sky* papers balance replicas of a model with engine-level access (migration, KV caches, batch models). A gateway in front of vLLM, Ollama or a hosted API has none of that access.
3. **Difficulty prediction works but is tied to a model pool.** Hidden-state and embedding predictors (Zhu et al., Šakota et al., Zhao et al., Damani et al.) predict well in-pool; cross-model transfer is near chance and calibration degrades out of distribution (Kadavath et al., Xiong et al.). Small-encoder predictors are the only ones cheap enough for a gateway.
4. **Latency is defined carefully in serving papers and ignored in routing papers.** TTFT, TPOT, goodput and tail latency are well defined (DistServe, Sarathi-Serve, Etalon); routing papers treat latency as a cost or overhead, never a per-request budget.
5. **Failover literature is thin.** Direct gateway-failover evidence is two vendor preprints (ContinuityBench, FailureAtlas); the rest is engine-level recovery (SpotServe, DéjàVu, ServerlessLLM) and microservice resilience patterns.
6. **Benchmarks stop at quality and price.** RouterBench, RouterEval, FusionFactory and LLMRouterBench replay stored outputs; none measures latency under load or injects failures. Judge and crowd label noise is quantified (MT-Bench, Chatbot Arena) but not propagated into router evaluation.
7. **Gateway design is practice, not literature.** Peer-reviewed system work is INFaaS, AlpaServe, MuxServe, S-LoRA, SGLang and AIBrix-style infrastructure; hosted-plus-self-hosted routing and Prometheus-fed routing are not covered.

## 2. The closest prior art (must be addressed head-on)

| Work | Status | What it already does | What it does not cover |
|---|---|---|---|
| RouteBalance (Da & Kalyvianaki, 2026) | arXiv preprint | Per-request model-instance choice from predicted quality, latency, cost, with vLLM queue and KV signals, dead reckoning | Hosted backends, per-request latency budgets, failover, one model family, preprint |
| vLLM Semantic Router (arXiv 2603.04444; Apache-2.0) | open source, preprint | Per-prompt selection, self-hosted vLLM, runtime TPOT/TTFT-based selection, weighted failover | Queue/GPU signals, learned quality estimate with latency budget (to confirm) |
| 2026 preprints named in `01-routing-algorithms/00-overview.md` (batch routing under capacity, CEMA-Router, RouterWorld, provider-selection from measured latency) | preprints, abstract-level reading | Parts of capacity-aware and latency-aware routing | Full combination; not yet read in full |
| LiteLLM, OpenRouter, Portkey, TrueFoundry, Kong | vendor docs (grey) | Target-level load/latency strategies, fallbacks | Learned per-prompt quality estimate with load and latency budget (see `competitors/00-overview.md`) |

**Consequence for the proposal.** The sentence "none picks the model per prompt, watches live load, and also runs on your own GPUs" is no longer safe. Reword (suggested):

> To our knowledge, no peer-reviewed system and none of the products reviewed combines a learned per-prompt quality estimate, live queue and GPU signals from self-hosted servers, per-request latency budgets, failover, and hosted-plus-self-hosted backends in one OpenAI-compatible gateway. Recent preprints and open-source routers cover parts of this combination.

The contribution is then the **combination plus a measured comparison against load-blind routing**, not being first.

## 3. Gaps mapped to objectives

| ID | Gap | Evidence (folder, paper) | Objective |
|---|---|---|---|
| L1 | Routers ignore live backend state; serving papers ignore model choice | 01 overview gap 1; 02 gap 1; 03 gap 1; 04 first bullet; 03 RouteBalance only partial | O4 |
| L2 | Latency is a metric or overhead, never a per-request budget tied to prompt difficulty | 01 gap 3; 03 latency-budget bullet; 04 latency bullet; 05 gaps | O4 |
| L3 | Difficulty predictors tied to a model pool; need cheap, retrainable gateway-side predictors; calibration under shift | 02 gaps 2, 3, 5; 01 gap 4 | O3 |
| L4 | Failover target chosen by predicted quality, cost and load is unstudied; circuit-breaker settings for LLM calls untested; no peer-reviewed evidence | 06 gaps; 01 gap 2; 03 failure bullet; 08 T8-G2 | O5 |
| L5 | Hosted APIs and self-hosted GPU servers are not routed together; no agreed cost basis for self-hosted tokens | 01 gap 7; 03 gap 1; 04 self-hosted bullet; 08 T8-G3, T8-G5 | O2, O4 |
| L6 | Evaluation does not measure latency under load, failures or label-noise sensitivity; pools are dated | 07 gaps 1–6; 05 metric fragmentation | O6 |
| L7 | Gateway overhead and Prometheus-scrape staleness unmeasured | 08 T8-G4, T8-G6; 03 staleness bullet; 05 histogram bullet | O2, O4 |

## 4. Risks the literature confirms

| Proposal risk | Literature evidence |
|---|---|
| Poor generalisation across model pairs | Zhu et al. cross-model transfer near chance; Shnitzer et al. out-of-distribution results; Moslem & Kelleher "staleness" |
| Noisy quality labels | MT-Bench/Chatbot Arena judge and crowd noise; RouterBench and FusionFactory judge-based labels without sensitivity analysis |
| Little prior work on live-load routing | True for peer-reviewed work; now **partly false** given RouteBalance, vLLM Semantic Router and 2026 preprints. Reword as "emerging, mostly preprints" |
| Competitors are moving | Confirmed: OpenRouter Auto Router, LiteLLM Auto Router v2 (13 Jul 2026), vLLM Semantic Router. Re-check docs before submission (see `competitors/00-overview.md` section 3) |

## 5. Design decisions the literature supports (for Chapter 3)

- **Classifier:** frozen sentence embedding plus a light head is the only family cheap enough for a gateway (Šakota et al., Zotos et al., RouteBalance's k-NN). Hidden-state predictors need a large model's internals.
- **Score:** weighted sum of predicted quality, cost and latency with a simplex of weights as one knob (RouteBalance; Hybrid LLM threshold tradeoff; RouteLLM cost-quality curve).
- **Live signals:** queue depth, pending decode work and KV-cache pressure matter; dead reckoning between scrapes avoids herding on stale metrics (RouteBalance; Mooncake oscillation finding). Report scrape-interval sensitivity, which no paper does.
- **Latency budget:** define TTFT/TPOT per Etalon and DistServe; predict budget feasibility per backend from recent histogram quantiles (Vidur is the only error-vs-load study).
- **Failover:** exponential backoff with jitter and a circuit breaker (ContinuityBench, grey Portkey/TrueFoundry docs), choosing the fallback by the same score; test with fault injection.
- **Evaluation:** RouterBench for cost-quality, MT-Bench for quality, plus own load generator and fault injection for p95 and success rate; report confidence intervals; test on more than one model pair (RouterEval pool-size method).

## 6. Evidence quality caveats

- Several 2026 items are preprints (RouteBalance, ContinuityBench, FailureAtlas, LLMRouterBench, RouterArena, GORGO, Vestrum). Cite them as preprints, and check status before submission.
- Some numbers come from arXiv v1 rather than the camera-ready (see each file's verification block and the corrections lists in topic overviews).
- Competitors are grey literature fetched 2026-10-31 and must be re-fetched before submission.
