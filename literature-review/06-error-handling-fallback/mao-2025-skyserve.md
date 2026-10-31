# SkyServe: serving AI models across regions and clouds with spot instances (Mao et al., 2025)

| Field | Value |
|---|---|
| Topic (home) | 06 Error handling and fallback |
| Also relevant to | 03 Load balancing, 04 Cost reduction |
| Paper type | system (policy and implementation) |
| Venue and status | peer-reviewed (EuroSys 2025) |
| Source read | full text, arXiv v2 (https://arxiv.org/pdf/2411.01438) |
| Verified on | 2026-10-31, against the arXiv PDF header (ACM DOI as printed there) and a search listing for the venue |
| Relevance to project | Medium |

## APA 7 reference
Mao, Z., Xia, T., Wu, Z., Chiang, W.-L., Griggs, T., Bhardwaj, R., Yang, Z., Shenker, S., & Stoica, I. (2025). SkyServe: Serving AI models across regions and clouds with spot instances. In *Proceedings of the Twentieth European Conference on Computer Systems* (EuroSys '25). ACM. https://doi.org/10.1145/3689031.3717459

## In-text citation forms
(Mao et al., 2025) · Mao et al. (2025)

## 1. What it is about
A policy, *SpotHedge*, and a system, SkyServe, for hosting model replicas on cheap spot GPU instances spread across regions and clouds, with on-demand replicas as a fallback. The aim is to cut cost and still stay available when spot capacity is preempted or simply unavailable.

## 2. The problem
Spot GPUs cost 8 to 50% of on-demand (Table 1, prices pulled 23 October 2024), but preemptions are frequent, correlated within a region, and recovery takes minutes (finding capacity, provisioning, loading a model), longer than the 2-minute AWS or 30-second GCP and Azure warnings. Single-region systems fail when spot capacity vanishes: in one AWS trace all zones of a region lacked spot GPUs 33.1% of the time.

## 3. Proposed solution
SpotHedge (1) spreads spot replicas across failure domains (regions and clouds) to decorrelate preemptions, (2) over-provisions cheap spot replicas as insurance, and (3) dynamically falls back to on-demand replicas when spot replicas become unavailable. SkyServe wraps this with a load balancer and autoscaler on top of existing inference servers (vLLM, TGI, Triton), built in the SkyPilot ecosystem.

**How cost is modelled.** Dollars per instance-hour: spot versus on-demand price ratio per GPU type and cloud; for one example an on-demand replica costs $16.3 per hour against $4.9 for spot. Cost is traded against availability and latency; the "hedge" is the extra spot replicas that cost less than one on-demand replica.

## 4. Data, models and tools
Real deployments on AWS and GCP with live preemptions, and replays of real spot traces from AWS and GCP; real AI workloads on LLM and other models; compared with research and production systems (including SpotServe and an AWS autoscaling group) and with on-demand-only serving. Open source: https://github.com/skypilot-org/skypilot.

## 5. Key results
- Cost 43% lower on average than on-demand-only serving while keeping high availability (abstract).
- P50, P90 and P99 latency improved by 2.3, 2.1 and 2.1 times on average over other systems (abstract; a later technical report quotes larger figures, so cite the version you read).
- A pure-spot AWS autoscaling group had 49.4% of requests fail or time out; SpotServe's failure rate was 2.0 to 75.9% depending on region.
- Spreading across more regions raises availability (Figure 5).

## 6. Limitations
*Stated by the authors:* I did not find a dedicated limitations section; the paper positions the policy as simple, with no formal optimality claim.

*My observations:* it manages whole model replicas, not individual requests; it treats a replica as up or down and does not examine partial degradation. Spot price ratios and availability change over time and by provider. Latency comparisons depend on the baselines' configuration, and the evaluation is on a few services.

## 7. Relevance to the AI Request Router
- Direct precedent for **tiered fallback by price**: cheap pool first, on-demand pool when the cheap one fails, then return. The router's "self-hosted first, hosted API as fallback" is the same shape across providers.
- Supports **spreading across failure domains** (do not put all fallbacks behind one provider or region) and **over-provisioning** as a hedge.
- **Reuse:** the fallback-with-recovery loop, cost ratios as inputs to the cost term. **Avoid:** provisioning logic (out of scope). **Not covered:** per-request quality, hosted APIs with rate limits.

## 8. How to use it in the report
Section 2.5 and the design rationale for the fallback chain. "Mao et al. (2025) show that mixing cheap and reliable replicas across failure domains cut cost by 43% while preserving availability, an infrastructure-level analogue of cost-ordered failover."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Mao et al. (2025) | Serve AI models cheaply and available on spot GPUs | SpotHedge: cross-region spread, over-provisioned spot, on-demand fallback | AWS and GCP deployments and traces; vLLM and other servers | 43% cheaper; P99 2.1x better; pure spot fails 49.4% | Replica-level only; prices time-varying; few workloads |
