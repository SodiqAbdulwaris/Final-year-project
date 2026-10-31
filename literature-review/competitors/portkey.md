# Portkey AI Gateway (grey literature: vendor documentation)

| Field | Value |
|---|---|
| Type | commercial AI gateway with an open-source gateway component; grey literature (vendor documentation) |
| Pages read | load balancing, fallbacks, conditional routing, circuit breaker, automatic retries; GitHub repository page |
| Fetched | 2026-10-31 |
| Relevance to project | Medium (named in the plan; strong on reliability, no model-quality routing) |

## APA 7 references
Portkey. (n.d.-a). *Load balancing*. Retrieved October 31, 2026, from https://portkey.ai/docs/product/ai-gateway/load-balancing

Portkey. (n.d.-b). *Fallbacks*. Retrieved October 31, 2026, from https://portkey.ai/docs/product/ai-gateway/fallbacks

Portkey. (n.d.-c). *Conditional routing*. Retrieved October 31, 2026, from https://portkey.ai/docs/product/ai-gateway/conditional-routing

Portkey. (n.d.-d). *Circuit breaker*. Retrieved October 31, 2026, from https://portkey.ai/docs/product/ai-gateway/circuit-breaker

Portkey. (n.d.-e). *Automatic retries*. Retrieved October 31, 2026, from https://portkey.ai/docs/product/ai-gateway/automatic-retries

In-text: (Portkey, n.d.-a)

## 1. What it is
A gateway that applies *configs* (JSON) to requests. The docs site now carries the title "Prisma AIRS AI Gateway", and pages state "Portkey is now PRISMA AIRS AI Gateway", so the product has been renamed under a security vendor; I kept the name Portkey used by the plan.

## 2. How routing, fallback and load balancing work
A config has a `strategy` with a `mode` and a list of `targets`:
- **`loadbalance`:** each target has a `weight` (default 1, minimum 0); weights are normalised to percentages; each request picks a target by those probabilities. Optional sticky load balancing by identifier. The docs list use cases: spread across providers or API keys, cost optimisation (for example 80% cheap model, 20% premium), gradual migration.
- **`fallback`:** a prioritised list; the next target is tried on failure. By default any non-2xx status triggers it; `on_status_codes` narrows this (for example `[429, 503]`). Strategies nest, so a fallback target can itself be a load balancer.
- **`conditional`:** targets chosen by rules on request metadata, request parameters (`model`, `temperature`, `max_tokens`) or URL path, evaluated "on the edge" (docs wording). Examples: paid-plan users to a fine-tuned model; model alias `fastest` to a small model.
- **Retries:** `retry` with `attempts` and `on_status_codes` (defaults include 429, 500, 502, 503, 504, 529), exponential backoff, optional `use_retry_after_headers`.
- **Circuit breaker:** `cb_config` with `failure_threshold`, `failure_threshold_percentage`, `minimum_requests`, `cooldown_interval` (minimum 30 seconds) and `failure_status_codes`; unhealthy targets are removed from routing; if all are open the breaker is bypassed; conditional strategies are not evaluated by it.

## 3. Feature checklist
| Question | Finding |
|---|---|
| Per-prompt model choice | By hand-written rules on metadata and parameters, not on prompt content or difficulty |
| Predicts difficulty or quality | No |
| Live load signals | No load signal in the pages read; weights are static; the circuit breaker reacts to failures only |
| Latency budget per request | Not documented in the pages read |
| Fallback and failover | Yes, with retries and a circuit breaker |
| Self-hosted GPU backends | Self-hosting of the gateway itself is documented (hybrid and private-cloud deployments in the docs navigation); support for self-hosted model servers as targets is not stated on the pages read |
| Openness | An open-source gateway repository exists on GitHub; licence and which features are open versus paid not checked |
| Pricing | The pages read say these features are "available on all Portkey plans"; plan prices not documented there |

## 4. Limitations (for our purposes)
Routing is rule-based and static; no model-quality prediction and no load-aware selection; reliability tooling is mature (circuit breaker, retries) but acts on errors after they happen.

## 5. Comparison with the AI Request Router
Portkey is a reliability and governance layer, and its `fallback` and `cb_config` patterns are a good reference design for the router's failover and circuit breaker. It does not choose a model from the prompt or from backend load; the project does.
