# 06 Error handling and fallback: overview

## 1. Topic definition and why it matters to the router
Error handling and fallback covers what a gateway does when a backend is slow, rate-limited, wrong or gone: detecting the fault (health checks, timeouts, error rates), containing it (circuit breakers, bounded retries, load shedding), and re-serving the request elsewhere (failover, request migration, tiered fallback) without losing the user's conversation state. For the AI Request Router this is half of the claimed gap: routing is only useful if the chosen model is reachable, so the design needs a failure model, a recovery policy, and tests that show failover keeps both availability and quality. **The direct literature is very thin.** Only two papers (ContinuityBench and FailureAtlas, both 2026 preprints from the same vendor) study multi-provider LLM gateway failover itself. The rest of the evidence is adjacent: fault tolerance inside a serving engine, resilience patterns from microservices, and incident studies. Grey sources (vendor documentation) fill the practice gap and are listed separately in section 8.

## 2. Comparison of papers
| Paper | Year | Type | Venue | Problem | Method | Key result | Limitation |
|---|---|---|---|---|---|---|---|
| Pandey & Singh, ContinuityBench (2026a) | 2026 | benchmark and system | preprint | Failover keeps uptime but loses conversation | CPR and CLO metrics; stateless vs history-forwarding proxy | CPR 99.20% vs 0%; retry storm and race condition found | Synthetic; strawman baseline; vendor preprint |
| Pandey & Singh, FailureAtlas (2026b) | 2026 | taxonomy | preprint | Gateway failures are undocumented | Layer × detectability matrix; five verified entries | Worst failures are silent (HTTP 200) | Five entries; vendor authors |
| Miao et al., SpotServe | 2024 | system | ASPLOS 2024 | Serve LLMs on preemptible GPUs | Reparallelization, matching-based migration, token-level recovery | P99 2.4 to 9.1x lower; 54% cheaper | Needs grace period; one deployment |
| Strati et al., DéjàVu | 2024 | system | ICML 2024 | Pipeline stage failure restarts requests | KV-cache streaming and replication | Failure latency 1.24x vs 1.91x | Pipeline parallel only; single failures |
| Jayakody et al., GhostServe | 2026 | system | MLSys 2026 | Cheap KV-cache protection for long contexts | Erasure-coded checkpoints, hybrid recovery | Up to 2.7x faster checkpointing; 2.1x faster recovery | Single node; simulated faults |
| Fu et al., ServerlessLLM | 2024 | system | OSDI 2024 | Cold start and locality conflicts | Fast loading; token-based live migration | 10 to 200x lower latency | Failure handling not evaluated |
| Mao et al., SkyServe | 2025 | system | EuroSys 2025 | Spot preemption and unavailability | Cross-region spot spread plus on-demand fallback | 43% cheaper; pure spot fails 49.4% | Replica-level only |
| Huang et al., Metastable Failures | 2022 | empirical study | OSDI 2022 | Why retries and overload sustain outages | Incident survey; load-capacity model | Retries sustain over half of 21 incidents | No LLM context |
| Yan et al., GenAI incidents | 2025 | empirical study | preprint | How GenAI cloud services fail | Coded Microsoft incidents | 49.8% degradation; 38.3% human-detected | One provider; preprint |
| Aderaldo & Mendonça, ResilienceBench-Operator | 2026 | benchmark tool | JSERD 2026 | Tuning retry and circuit breaker | Declarative scenarios on Kubernetes | Max attempts drives success; best backoff varies | Retry only; abort faults |

## 3. Themes and how the papers relate
1. **Availability is not the same as correctness.** ContinuityBench and FailureAtlas argue, and Yan et al. show from the provider side, that the failures that matter often return HTTP 200: degraded latency (49.8% of Microsoft's GenAI incidents), invalid output (14.5%), or lost context. Health checks based on status codes are therefore insufficient.
2. **Recovery inside the serving engine is a separate layer.** SpotServe, DéjàVu, GhostServe and ServerlessLLM all keep the *same model* alive by saving or moving the KV cache (replicate to a neighbour, erasure-code to host memory, migrate tokens and recompute). They cut recovery from restart-from-scratch (minutes) to seconds, but none protects against a provider outage or a rate limit. A router sits above them and treats the backend as up, slow or down.
3. **Cheap-first with a reliable fallback.** SkyServe and SpotServe mix preemptible and on-demand capacity; it is the same pattern as self-hosted first with a hosted API behind it, and the cost reduction (43% to 54%) is what pays for the redundancy. This links topic 04 (cost) and topic 06.
4. **Retries cut both ways.** Metastable Failures finds retries sustaining over half of studied outages; ContinuityBench reproduces this against a rate-limited fallback; ResilienceBench-Operator shows retry persistence raises success but the right backoff depends on failure rate. The consistent advice is bounded retries with jittered backoff and load shedding.
5. **Practice leads research.** Gateway features (fallback chains, retries, circuit breakers) exist in products long before any peer-reviewed evaluation, which is why section 8 relies on grey sources for design justification.

## 4. Strongest three papers for the proposal
1. **Pandey & Singh (2026), ContinuityBench:** the only direct study of gateway failover; supplies metrics (CPR, CLO), a fault-injection design and the retry-storm and race-condition lessons. Use with care: preprint, vendor authors, strawman baseline.
2. **Huang et al. (2022), Metastable Failures:** peer-reviewed grounding for bounded retries, backoff, load shedding and for checking the target's headroom before failing over.
3. **Yan et al. (2025), GenAI incidents:** empirical evidence on how hosted LLM services fail (degradation most of all), which justifies latency-aware circuit breakers and output checks. Preprint, but it is the only incident study of GenAI services.

## 5. Gaps visible in this topic (for the gap statement)
- **No peer-reviewed study of multi-provider LLM gateway failover.** Evidence: the two direct papers are preprints from one vendor (Pandey & Singh, 2026a, 2026b); FailureAtlas draws three of its five entries from one gateway's issue tracker.
- **Failover quality is not examined.** ContinuityBench uses one provider pair and a single fact-recall probe; no study compares answer quality before and after failing over to a different model, or lets the router pick the fallback by predicted quality and cost (the project's idea).
- **Failover target selection ignores live load.** SkyServe chooses replicas by price and availability, ContinuityBench walks a fixed chain; Huang et al. show that overloading a fallback sustains outages, yet no paper combines failover with live load signals.
- **Circuit-breaker parameters for LLM calls are unstudied.** ResilienceBench-Operator evaluates retries on millisecond microservice calls; LLM calls last seconds and cost tokens per retry. The circuit-breaker evidence in the authors' earlier paper was available to me only as an abstract.
- **Mid-stream failure is not handled at gateway level.** ContinuityBench excludes streaming; SpotServe, DéjàVu and ServerlessLLM resume inside one engine. A gateway-level resume (re-send prompt plus partial output) is only suggested by ServerlessLLM's token migration.
- **Hedged and duplicate requests:** I found no 2020 or later peer-reviewed work on hedging for LLM serving; the standard reference (Dean & Barroso, 2013) predates the cutoff.
- **Client-side provider reliability data are missing.** Yan et al. give provider-side incident statistics only; no study reports error and latency rates seen by API clients across providers.

## 6. Paper files (this topic)
- [Pandey & Singh (2026), ContinuityBench](pandey-2026-continuitybench.md)
- [Pandey & Singh (2026), FailureAtlas](pandey-2026-failureatlas.md)
- [Miao et al. (2024), SpotServe](miao-2024-spotserve.md)
- [Strati et al. (2024), DéjàVu](strati-2024-dejavu.md)
- [Jayakody et al. (2026), GhostServe](jayakody-2026-ghostserve.md)
- [Fu et al. (2024), ServerlessLLM](fu-2024-serverlessllm.md)
- [Mao et al. (2025), SkyServe](mao-2025-skyserve.md)
- [Huang et al. (2022), Metastable Failures](huang-2022-metastable-failures.md)
- [Yan et al. (2025), GenAI cloud incidents](yan-2025-genai-incidents.md)
- [Aderaldo & Mendonça (2026), ResilienceBench-Operator](aderaldo-2026-resiliencebench-operator.md)

## 7. Related papers documented elsewhere
Topic 04 (written, links valid):
- [Dekoninck et al. (2025), cascade routing](../04-cost-reduction/dekoninck-2025-cascade-routing.md)
- [Gupta et al. (2024), token-level uncertainty cascades](../04-cost-reduction/gupta-2024-token-uncertainty-cascades.md)
- [Yue et al. (2024), mixture-of-thought cascades](../04-cost-reduction/yue-2024-mot-cascades.md)

Topic 03 (files seen on disk):
- [Sun et al. (2024), Llumnix](../03-load-balancing/sun-2024-llumnix.md): live request migration for load balancing.
- [Jain et al. (2024), intelligent router](../03-load-balancing/jain-2024-intelligent-router.md)
- [Kossmann et al. (2024), GPU half empty](../03-load-balancing/kossmann-2024-gpu-half-empty.md)

Topics 01 and 02 (links checked against the files on disk): [FrugalGPT](../01-routing-algorithms/chen-2024-frugalgpt.md) and [AutoMix](../01-routing-algorithms/aggarwal-2024-automix.md) (escalation on a quality signal), [Varangot-Reille survey](../01-routing-algorithms/varangot-reille-2026-routing-survey.md); [Chuang et al., confidence tokens](../02-prompt-difficulty/chuang-2025-confidence-tokens.md). These are cascades triggered by *quality* rather than *failure*; the failover trigger is the project's distinct contribution.

## 8. Grey literature (design justification only; not counted as papers)
All pages fetched on 2026-10-31.
- Portkey. *Fallbacks* (AI Gateway documentation). https://portkey.ai/docs/portkey-features/ai-gateway/fallbacks-on-llms. Describes ordered fallback targets that trigger by default on any non-2xx response, optionally restricted by status code (for example 429 or 503); requests can be traced across the fallback chain. The page says nothing about conversation state, retries or circuit breakers. A separate Portkey feature listing mentions retries with exponential backoff and a circuit breaker (seen in search results, details not read).
- TrueFoundry (Dubey, A.). *What is LLM fallback? Definition, mechanism, and how to implement it* (blog; published 28 July 2026, updated 15 October 2026). https://www.truefoundry.com/blog/what-is-llm-fallback. Lists fallback triggers (429, server errors, network errors, timeouts, failed quality checks), recommends bounded retries with backoff and jitter before rerouting, a circuit breaker to remove unhealthy targets, and warns that the fallback model must support the same prompts, context windows, tool use and formats; cooldown durations are not specified. Vendor marketing content.
- Brooker, M. *Exponential backoff and jitter* (AWS Architecture Blog, 4 March 2015). https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/. Pre-2020; recommends adding randomness to backoff, which the ContinuityBench retry-storm fix relies on.
- Pre-2020 background cited by the papers but not retrieved by me: Dean and Barroso (2013), *The Tail at Scale*; Nygard (2007), *Release It!* (circuit breaker, bulkhead).

## 9. Search log
Searches ran on 2026-10-30 and 2026-10-31. I did not keep numeric hit counts; the counts below are title-level screening.

| Source | Search string or action | Use |
|---|---|---|
| General web search (US) | "ContinuityBench stateful failover multi-provider LLM routing benchmark"; "SpotServe ... ASPLOS 2024 DOI"; "DéjàVu KV-cache Streaming ... ICML 2024"; "fault-tolerant LLM inference serving failure recovery request migration KV cache GPU failure"; "metastable failures retry amplification OSDI 2022"; "empirical study of production incidents generative AI cloud services LLM API outages reliability"; "circuit breaker pattern microservices resilience empirical evaluation peer-reviewed"; "hedged requests tail latency 2020 ... cloud services"; "ServerlessLLM OSDI 2024 ...; SkyServe EuroSys 2025"; "Aderaldo declarative approach ... resiliency patterns"; "GhostServe ... MLSys 2026"; "hedging redundant requests LLM serving tail latency failover SLO-aware"; "request hedging tail latency microservices ... SoCC OR NSDI OR EuroSys 2021 2022 2023"; Portkey and TrueFoundry documentation searches | candidate discovery and venue checks |
| arXiv abstract pages | ContinuityBench, SpotServe, DéjàVu, Yan et al.; PDFs for all included arXiv papers | metadata and full text |
| USENIX OSDI pages | Huang et al. (2022), Fu et al. (2024) | venue, pages |
| ICML and MLSys virtual sites | DéjàVu poster page; GhostServe oral page | venue |
| Journal pages (SBC OJS, UMA portal, Wiley) | Aderaldo & Mendonça (2026) page and PDF; Wiley page for the 2025 SPE paper returned 403 | full text for the 2026 paper; metadata only for 2025 |
| IEEE Xplore, ACM DL, Semantic Scholar, Google Scholar | not queried directly; reached only through web search results | |

**Counts:** screened 17 candidate titles (the grey sources in section 8 are not counted); included 10 full files (3 assigned, 7 added); read in full text: all 10.

**Assigned papers:** ContinuityBench, SpotServe, DéjàVu all retained. None dropped. SpotServe's ACM DOI is unverified (the PDF shows a placeholder), so the arXiv DOI is used.

**Added:** FailureAtlas (preprint), Metastable Failures in the Wild (OSDI 2022), ServerlessLLM (OSDI 2024), SkyServe (EuroSys 2025), Yan et al. incidents (preprint), GhostServe (MLSys 2026), ResilienceBench-Operator (JSERD 2026). Of the ten, six are conference papers (SpotServe, DéjàVu, GhostServe, ServerlessLLM, SkyServe, Metastable Failures), one is a journal article, and three are preprints (ContinuityBench, FailureAtlas, Yan et al.); SpotServe's venue rests on the arXiv comment field and GhostServe's on the MLSys page.

**Screened, not documented (7):**
- Aderaldo et al. (2025), *Software: Practice and Experience* 55(1), 170–192, on Retry and Circuit Breaker experiments: Wiley returned 403 and no open version was found, so only the abstract was seen; cited inside the ResilienceBench-Operator file.
- KevlarFlow (arXiv 2601.22438), AnchorTP (arXiv 2511.11617), LUMEN (arXiv 2606.17787) and an AI-inference incident study (arXiv 2511.07424): preprints seen in search results; KevlarFlow was downloaded but not read, the others not retrieved.
- Dean & Barroso, *The Tail at Scale*: published 2013, excluded by the 2020 rule.
- An InfoQ article on adaptive hedged requests: grey and not peer-reviewed.

**Unverified items and caveats for the supervisor:**
- ContinuityBench and FailureAtlas are by the same two authors at a gateway vendor, and FailureAtlas describes ContinuityBench inconsistently; treat the pair as one source.
- GhostServe's abstract and conclusion swap the 2.1x and 2.7x figures.
- ResilienceBench-Operator's page numbers (179–208) and PDF identifier (14:9) differ; DéjàVu's PMLR page numbers and GhostServe's proceedings details were not confirmed on a publisher page.
- Links to topics 01 and 02 were corrected to the files that now exist on disk.
