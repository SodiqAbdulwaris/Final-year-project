# TrueFoundry AI Gateway (grey literature: vendor documentation)

| Field | Value |
|---|---|
| Type | commercial AI gateway ("virtual models"); grey literature (vendor documentation) |
| Pages read | Virtual models / load balancing overview |
| Fetched | 2026-10-31 |
| Relevance to project | Medium to High (the only gateway read with SLA cutoffs on token latency) |

## APA 7 reference
TrueFoundry. (n.d.). *Virtual models*. Retrieved October 31, 2026, from https://www.truefoundry.com/docs/gateway/load-balancing-overview

In-text: (TrueFoundry, n.d.)

## 1. What it is
A *virtual model* is a named entry in the gateway that applications call like any model. Behind it, one routing strategy distributes requests over several real target models. The gateway handles load balancing, health-aware routing, retries and fallbacks. Virtual models do not apply to the Batch API.

## 2. How routing, fallback and load balancing work
Three strategies (`type` field):
- **`weight-based-routing`:** traffic by `weight` (0 to 100, summing to 100); optional `sticky_routing` with `ttl_seconds` and `session_identifiers`.
- **`priority-based-routing`:** the healthy target with the lowest `priority` number is used; failure falls to the next. It supports **`sla_cutoff`** with `time_per_output_token_ms` and `time_to_first_token_ms`. The gateway monitors a rolling average over a 3-minute window (up to 10 samples, at least 3 required) and marks a target unhealthy, moving it to the end of the list, if a threshold is exceeded. SLA cutoff is available only for priority-based routing.
- **`latency-based-routing`:** no weights; the gateway measures each target's time per output token over the last 20 minutes and picks a target per caller, deterministically, sticky for a 10-minute epoch; lower-latency targets are more likely, but every healthy target keeps some share.

Retries and fallback: `retry_config` with `on_status_codes` (default `["429","500","502","503"]`) and `fallback_status_codes` for trying a different target.

## 3. Feature checklist
| Question | Finding |
|---|---|
| Per-prompt model choice | No: strategies choose among targets of one virtual model by weight, priority or latency, not by prompt content |
| Predicts difficulty or quality | No |
| Live load signals | Observed latency (TPOT, TTFT) over minutes; no queue depth or GPU utilisation documented |
| Latency budget per request | A per-target SLA threshold, not a per-request budget |
| Fallback and failover | Yes |
| Self-hosted GPU backends | Not documented on the page read |
| Openness | Not documented on the page read |
| Pricing | Not documented on the page read |

## 4. Limitations (for our purposes)
Targets are assumed to be interchangeable; latency data is minutes old by design (3 to 20 minute windows); no content-aware selection.

## 5. Comparison with the AI Request Router
The SLA-cutoff idea (mark a backend unhealthy when its TPOT or TTFT crosses a threshold) is a useful reference for the project's health signal. The project differs by selecting between non-equivalent models per prompt and by using shorter-horizon signals such as queue depth from Prometheus.
