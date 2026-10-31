# SpotServe: serving LLMs on preemptible instances (Miao et al., 2024)

| Field | Value |
|---|---|
| Topic (home) | 06 Error handling and fallback |
| Also relevant to | 04 Cost reduction, 05 Serving systems |
| Paper type | system |
| Venue and status | peer-reviewed (ASPLOS 2024, per the arXiv comment field) |
| Source read | full text, arXiv v1 (https://arxiv.org/pdf/2311.15566); the final ACM DOI could not be verified (the PDF shows a template placeholder) |
| Verified on | 2026-10-31, against the arXiv abstract page |
| Relevance to project | Medium |

## APA 7 reference
Miao, X., Shi, C., Duan, J., Xi, X., Lin, D., Cui, B., & Jia, Z. (2024). SpotServe: Serving generative large language models on preemptible instances. In *Proceedings of the 29th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, Volume 2*. ACM. https://doi.org/10.48550/arXiv.2311.15566

*Preprint DOI shown; replace with the ACM DOI once confirmed.*

## In-text citation forms
(Miao et al., 2024) · Miao et al. (2024)

## 1. What it is about
A distributed LLM serving system that runs on cheap cloud "spot" GPU instances that the provider can reclaim at any time. When instances disappear or appear, it re-plans how the model is split across GPUs, moves cached state instead of reloading, and keeps partial progress of in-flight requests.

## 2. The problem
Spot GPUs cost up to 90% less than on-demand ones, but a preemption stops an entire model-parallel pipeline, so a lost instance hangs its peers. Earlier spot-serving systems (MArk, Cocktail) targeted small models that fit one instance and handled loss by rerouting requests or redundant computation. For LLMs, restarting is expensive: loading a 120-billion-parameter model from storage takes over two minutes on AWS, and interrupted requests restart from scratch.

## 3. Proposed solution
1. **Dynamic reparallelization.** A controller chooses data, pipeline and tensor parallel degrees for the current instance count and arrival rate, minimising latency when capacity suffices and maximising throughput otherwise; it can also acquire on-demand instances.
2. **Cheap migration.** Mapping surviving GPUs to the new device mesh is a bipartite matching solved with the Kuhn-Munkres algorithm so that the most model parameters and KV cache stay in place; migration is overlapped with pipeline execution.
3. **Stateful inference recovery.** Using the cloud's grace period (30 s on AWS) the engine commits progress per token and migrates the KV cache of finished tokens, so interrupted requests resume rather than restart.

**How cost is modelled.** Dollar cost per hour of instances and cost per token; the optimiser trades throughput, latency and monetary cost. For GPT-20B the paper compares spot at 1.9 USD/h with on-demand at 3.9 USD/h. The intro also states that serving GPT-3 on AWS takes over 16 A100-40GB GPUs, costing more than $66 per hour per pipeline.

## 4. Data, models and tools
- OPT-6.7B, GPT-20B, LLaMA-30B on AWS g4dn.12xlarge (4 × T4 GPUs); a real 12-hour spot availability trace, two 20-minute segments, plus traces mixing on-demand instances; arrivals 1.5, 0.35 and 0.2 requests/s, Gamma process with CV 6; a Microsoft production trace for fluctuating load.
- Baselines built on FasterTransformer: *Rerouting* (drop the broken pipeline, reroute requests) and *Reparallelization* (restart with a new configuration, Varuna style). Code: https://github.com/Hsword/SpotServe.

## 5. Key results
- P99 tail latency 2.4 to 9.1 times lower than the baselines (abstract). On LLaMA-30B: 1.34 to 2.43 times better than Reparallelization and 2.14 to 9.13 times better than Rerouting.
- Up to 54% monetary saving versus on-demand-only serving, at under 18% higher average latency and under 90% higher P99 (Figure 7, GPT-20B).
- Rerouting overloads once an instance is lost because it drops a whole pipeline; the ablation (Figure 9) shows that removing the parallelization controller changes tail latency by 179% (the text's wording is ambiguous, so I do not rely on the direction).

## 6. Limitations
*Stated by the authors:* only latency minimisation is the optimisation target; strict SLOs or throughput targets and newer architectures such as mixture-of-experts are future work.

*My observations:* a single model per cluster in one region; it relies on the grace-period warning, so sudden failures are not handled (DéjàVu makes the same point). Evaluation uses small T4 GPUs. SkyServe (Mao et al., 2025) later reports SpotServe failing 2.0 to 75.9% of requests depending on region when spot capacity is unavailable, because it does no provisioning or placement.

## 7. Relevance to the AI Request Router
- Quantifies why **backend loss is costly for self-hosted LLMs** (minutes to reload, restart from scratch) and why the router should avoid sending traffic to a backend that is about to be reclaimed. A preemption warning is a health signal the circuit breaker could consume.
- Shows the cost-availability trade-off the scoring function faces when spot or cheap capacity is mixed with on-demand.
- **Reuse:** grace-period handling, on-demand fallback, token-level progress as a concept (a router can resend the prompt plus partial output to a different backend). **Avoid:** re-implementing parallelism logic; it is out of scope. **Not covered:** hosted APIs, gateway-level failover.

## 8. How to use it in the report
Section 2.5 (recovery in self-hosted serving) and a pointer to topic 05. "Miao et al. (2024) show that preemption-aware serving cuts P99 latency 2.4 to 9.1 times and cost 54%, but only for failures with warning inside a single deployment."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Miao et al. (2024) | Serve LLMs cheaply on preemptible GPUs | Dynamic reparallelization; matching-based migration; token-level stateful recovery | OPT-6.7B, GPT-20B, LLaMA-30B; AWS spot trace; FasterTransformer | P99 2.4 to 9.1x lower; 54% cheaper | Needs grace period; one deployment; latency-only objective |
