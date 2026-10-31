Status: DRAFT
Depends on: D08; D12
Sources: Primary URLs in source table and proposal-audit section
Open items: Scoped numerical/final-version checks recorded below

# ResilienceBench-Operator: benchmarking retry and circuit-breaker patterns (Aderaldo & Mendonça, 2026)

| Field | Value |
|---|---|
| Topic (home) | 06 Error handling and fallback |
| Also relevant to | 03 Load balancing |
| Paper type | benchmark tool with a controlled experiment |
| Venue and status | peer-reviewed journal (*Journal of Software Engineering Research and Development*, 2026, open access, CC BY 4.0) |
| Source read | full text (https://journals-sol.sbc.org.br/index.php/jserd/article/view/6965) |
| Verified on | 2026-10-31, against the journal's article page |
| Relevance to project | Medium |

## APA 7 reference
Aderaldo, C. M., & Mendonça, N. C. (2026). ResilienceBench-Operator: A Kubernetes extension for systematic evaluation of microservice resilience patterns. *Journal of Software Engineering Research and Development, 14*, 179–208. https://doi.org/10.5753/jserd.2026.6965

*The PDF header gives the article identifier "14:9"; the journal page gives pages 179–208 and issue 1. Check which form the university requires.*

## In-text citation forms
(Aderaldo & Mendonça, 2026) · Aderaldo and Mendonça (2026)

## 1. What it is about
A Kubernetes-native tool that generates and runs hundreds of controlled experiments on the **Retry** and **Circuit Breaker** patterns in a real microservice application, injecting faults and measuring the reliability and latency trade-offs. The paper extends the authors' earlier ResilienceBench (Aderaldo et al., 2025, *Software: Practice and Experience*, 55(1), 170–192) from a single client-server pair to an application with many services.

## 2. The problem
Retry and circuit breaker are standard resilience patterns, but wrong settings can increase tail latency, reduce throughput, or amplify failure. Tools to test them under controlled, reproducible failure and load, on realistic multi-service deployments, were lacking.

## 3. Proposed solution
A declarative "evaluation space" (patterns, parameters, workloads, fault rates, libraries) is expanded into scenarios; Kubernetes custom resources and controllers reconfigure the service, inject faults through a proxy, run a k6 load script and collect metrics, one scenario at a time. Analysis uses Pareto frontiers (success versus P95 time) and per-scenario Spearman correlations.

**How cost is modelled.** Latency is the cost of resilience: 95th-percentile session time, min-max normalised within each scenario group, traded against success rate.

## 4. Data, models and tools
Experiment on the Online Boutique application (extended with gRPC retry support), retry policy on the checkout-to-payment connector; failure rates 25%, 50%, 75% (abort of requests), 300 or 500 virtual users, retry parameters: maximum attempts, initial backoff (0.5 to 1.5 s), backoff multiplier (1.0 to 2.0); 222 scenarios in total; one control-plane and three worker nodes on one physical host. Scripts: https://github.com/cmendesce/resilience-bench-operator-k8s-env.

## 5. Key results
- Retries help a lot: at 25% failure, Pareto-optimal retry settings reach checkout success of about 0.70 to 0.75 versus about 0.55 without retries; at 50% failure 0.40 to 0.50 versus under 0.25; at 75% 0.15 to 0.20 versus near zero.
- Maximum attempts dominates reliability (Spearman correlation with success 0.72 to 0.94 across scenarios); initial backoff and multiplier correlate weakly and inconsistently with success and mainly shape latency.
- At high failure rates optimal strategies split into "five fast attempts" and "few attempts with long backoff"; there is no single best setting.
- Circuit breaker results appear only in the authors' earlier paper, whose abstract states that retry and circuit breaker both reduced load on the target service with little impact on performance at low to moderate failure rates (abstract only; not read in full).

## 6. Limitations
*Stated by the authors:* one connector, one application, modified source code, results apply to that setting; Kubernetes noise between scenarios; hundreds of scenarios still cover a small space.

*My observations:* faults are uniform aborts rather than slowdowns or rate limits; the study examines retries, not circuit breaker thresholds, so the evidence for breaker parameters here is indirect. Traditional microservices (milliseconds) differ from LLM calls (seconds, expensive per retry).

## 7. Relevance to the AI Request Router
- Peer-reviewed support for treating **retry parameters as tunable and workload-dependent** and for using Pareto analysis when choosing them; the planned FastAPI gateway can reuse the approach to tune max attempts and backoff against success and P95.
- Shows that more attempts raise success but cost latency, which in LLM calls also costs tokens.
- **Reuse:** the scenario-grid method and metrics for resilience tests. **Not covered:** circuit-breaker thresholds, LLM-specific costs, rate limits.

## 8. How to use it in the report
Section 2.5 (resilience patterns) and the test design in 3.9. "Aderaldo and Mendonça (2026) show on Online Boutique that retry persistence drives success at every failure rate tested but the best backoff differs by failure rate, which argues for measured rather than default retry settings."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Aderaldo & Mendonça (2026) | Systematic evaluation of retry and circuit breaker | Declarative scenarios on Kubernetes; fault injection; Pareto and correlation analysis | Online Boutique; 222 scenarios; k6 | Max attempts drives success; best backoff varies by failure rate | One connector; abort faults; no breaker data here |


## 2026-10-31 proposal audit

- Source attempted: No machine-selected URL; manual check still needed.
- Scope: Current source fetch failed; earlier venue/details remain unverified in this session. unknown url type: 'None'
- Historical Source read above records the earlier session, not a claim of a fresh full reading.
