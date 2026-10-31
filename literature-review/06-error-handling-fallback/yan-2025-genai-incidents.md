# Production incidents in generative AI cloud services (Yan et al., 2025)

| Field | Value |
|---|---|
| Topic (home) | 06 Error handling and fallback |
| Also relevant to | 03 Load balancing |
| Paper type | empirical study |
| Venue and status | preprint only (arXiv, v1 April 2025, v2 August 2025); no venue found |
| Source read | full text, arXiv v2 (https://arxiv.org/pdf/2504.08865) |
| Verified on | 2026-10-31, against the arXiv abstract page |
| Relevance to project | Medium to High |

## APA 7 reference
Yan, H., Chen, Y., Ma, M., Wen, M., Lu, S., Zhang, S., Xu, T., Wang, R., Bansal, C., Rajmohan, S., Lin, Q., Zhang, C., & Zhang, D. (2025). *An empirical study of production incidents in generative AI cloud services* [Preprint]. arXiv. https://doi.org/10.48550/arXiv.2504.08865

## In-text citation forms
(Yan et al., 2025) · Yan et al. (2025)

## 1. What it is about
The first study of real production incidents in hosted generative-AI services, drawn from Microsoft's incident system (including Azure OpenAI) over June 2020 to February 2024. It describes how incidents are detected, what they look like, why they happen and how they are mitigated, and compares them with incidents in other cloud services.

## 2. The problem
GenAI cloud services add new reliability issues (huge GPU demand, generated-content quality, privacy) on top of ordinary cloud ones, yet no published study characterised their incidents, so teams building on LLM APIs have no evidence on how and how often providers fail.

## 3. Proposed solution (method)
Two datasets: a general set of mitigated or resolved GenAI-related incidents (matched by service and by GenAI keywords in titles) and an in-depth set of high-severity ones with root-cause write-ups, with a comparison set from other services. Two authors coded symptoms, root causes and mitigations in rounds (40% taxonomy, 20% validation, 40% test), reaching Cohen's kappa 0.921, 0.930 and 0.893. Numbers are normalised because Microsoft does not release absolute counts.

**How cost is modelled.** Not modelled; the paper measures *time to mitigate* (normalised time units) as the cost of an incident.

## 4. Data, models and tools
Incidents from Microsoft's IcM system, covering GPT-3 to GPT-4-era services; absolute counts are withheld by company policy, so only normalised numbers are shown.

## 5. Key results
- **Symptoms:** performance degradation 49.8%, deployment failure 35.7%, invalid inference 14.5% (hallucinated or malformed output).
- **Root causes:** infrastructure 27.2% (including maintenance such as worn GPUs 17.8%, network 4.7%, storage 4.7%); configuration 24.5%; code bugs 21.5%; external usage issues 14.1%; operation errors 12.7%.
- **Detection:** 38.3% of GenAI incidents were reported by humans, versus 13.7% for other services; monitor false alarms 11.0% versus 3.8%.
- **Mitigation:** ad-hoc fixes 22.4%, rollback 15.2%, configuration fixes 13.0%, infrastructure fixes 12.1% (of which scaling 6.3%, restart 3.1%, **traffic failover 2.7%**), code fixes only 7.6%, and 19.7% self-recovered, for example by back-off retry.
- Mean time to mitigate was 1.12 time units versus 0.65 for other incidents (1.83 times longer, as the paper writes it); GenAI incidents needed 2.5 times more infrastructure fixes.

## 6. Limitations
*Stated by the authors:* all data from one company (Microsoft), which may not represent other providers; manual labelling may be subjective, mitigated by kappa checks; absolute numbers are hidden.

*My observations:* the study concerns the provider's side, so it does not give the error and latency rates a *client* sees from an API. Percentages are among incidents, not among requests. No venue and no released data. The "mitigation time unit" is unspecified.

## 7. Relevance to the AI Request Router
- Evidence that **hosted LLM services do fail** in ways clients must handle: performance degradation (slow, not down) is the largest class, so the circuit breaker should trip on **latency as well as errors**.
- Invalid outputs (14.5%) are returned as successes, supporting output sanity checks before accepting a response and a fallback on malformed output.
- Provider-side mitigations include traffic failover and rollback, which take time (above mean 1.12 units); a gateway failover bridges that gap.
- **Reuse:** the symptom taxonomy as test scenarios (slow, down, bad output). **Not covered:** client-side error rates, rate limiting, per-provider comparison.

## 8. How to use it in the report
Section 2.5 (why failover is needed) and the fault-injection scenarios in 3.9. "In Microsoft's GenAI incidents, performance degradation (49.8%) and deployment failure (35.7%) dominate and human detection is nearly three times as common as for other services (Yan et al., 2025), so a gateway should not rely on provider health pages."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Yan et al. (2025) | Characterise incidents in GenAI cloud services | Manual coding of symptoms, causes, mitigations; comparison with non-GenAI incidents | Microsoft IcM incidents, 2020 to 2024 | 49.8% degradation; 38.3% human-detected; infrastructure 27.2% of causes | One provider; preprint; normalised numbers; provider-side only |
