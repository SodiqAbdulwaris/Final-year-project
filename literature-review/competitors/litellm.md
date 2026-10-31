Status: DRAFT
Depends on: L04; L10
Sources: Official vendor documentation linked below
Open items: Pinned release/configuration and feature checks before submission

## 31 October 2026 current-source recheck

Core Router documents deployment balancing, cooldowns, fallbacks, timeouts and retries. Auto Router is separate. No performance claim was independently tested. [Vendor documentation](https://docs.litellm.ai/docs/routing), accessed 31 October 2026. This note supersedes conflicting rows below; the earlier review is retained as history.

# LiteLLM Router and Auto Router (grey literature: vendor documentation)

| Field | Value |
|---|---|
| Type | LLM gateway and Python SDK (proxy server plus Router); grey literature (vendor documentation) |
| Pages read | Router (routing and load balancing), Auto Routing (beta), Auto Router v2 announcement, vLLM provider page |
| Fetched | 2026-10-31 |
| Relevance to project | High (named in the proposal; the Auto Router is the closest per-prompt competitor in a gateway) |

## APA 7 references
LiteLLM. (n.d.-a). *Router: Load balancing*. Retrieved October 31, 2026, from https://docs.litellm.ai/docs/routing

LiteLLM. (n.d.-b). *[Beta] Auto routing*. Retrieved October 31, 2026, from https://docs.litellm.ai/docs/proxy/auto_routing

Dholakia, K. (2026, July 13). *Auto Router v2: One router for complexity, semantic, and adaptive routing*. LiteLLM. Retrieved October 31, 2026, from https://docs.litellm.ai/blog/autorouter-v2

LiteLLM. (n.d.-d). *vLLM*. Retrieved October 31, 2026, from https://docs.litellm.ai/docs/providers/vllm

In-text: (LiteLLM, n.d.-a) · (Dholakia, 2026)

## 1. What it is
An OpenAI-compatible gateway that fronts many providers and self-hosted servers. Its **Router** spreads calls across several *deployments* that share one `model_name`. Its **Auto Router** (beta since v1.94.0, announced as v2 on 13 July 2026) picks a model tier per request.

## 2. How routing, fallback and load balancing work
**Router strategies** (`routing_strategy`, default `simple-shuffle`): weighted pick by `rpm`, `tpm` or `weight` (the docs recommend it for production); `least-busy` (fewest ongoing calls); `latency-based-routing` (lowest response time, with `routing_strategy_args` such as `ttl` and `lowest_latency_buffer`); `usage-based-routing-v2` (lowest TPM usage for the minute, tracked in Redis); and cost-based (lowest cost, using `input_cost_per_token`). `routing_groups` apply a different strategy to different `model_name`s. Optional pre-call checks (`enable_pre_call_checks`) filter by context window and region; `session_affinity` and `deployment_affinity` pin callers.

**Reliability:** `num_retries`, `fallbacks` (to another model group), `context_window_fallbacks`, `max_fallbacks` (default 5), per-deployment `cooldown_time` (default 5 seconds) and `allowed_fails`, and an `order` field for priority failover. When every `max_parallel_requests` slot of a deployment is busy, the request gets a 429 at once; the docs state there is "no wait queue".

**Auto Router** (`auto_router/complexity_router`): each request is classified into tiers `SIMPLE`, `MEDIUM`, `COMPLEX`, `REASONING` by a heuristic scorer (seven dimensions such as token count, code presence, reasoning markers; sub-millisecond), an LLM classifier, an external classifier, keyword rules or a custom plugin. A tier maps to one model, a random pool, or an adaptive pool (`adaptive: true`, Thompson sampling with feedback). After the tier is chosen, "ordinary model-group behavior" applies: deployment selection, cooldowns and context-window checks. The older semantic auto router is deprecated.

## 3. Feature checklist
| Question | Finding |
|---|---|
| Per-prompt model choice | Core Router: no (it spreads traffic over copies of the named model). Auto Router: yes, by complexity tier |
| Predicts difficulty or quality | Complexity tier from heuristics or an LLM classifier; adaptive pools learn from feedback; no trained quality predictor in the docs read |
| Live load signals | Router only: `least-busy` (ongoing calls), `latency-based-routing`, usage-based (Redis), cooldowns. Auto Router classification uses request content, not load; but it composes with the Router strategies for the tier's model |
| Latency budget per request | Not found in routing docs (timeouts exist; no budget-driven model choice) |
| Fallback and failover | Yes (`fallbacks`, `order`, cooldowns, retries) |
| Self-hosted GPU backends | Yes: the vLLM provider page documents the `hosted_vllm/<model>` route with `api_base` for an OpenAI-compatible vLLM server (LiteLLM, n.d.-d) |
| Openness | Self-hostable proxy and SDK; some features (custom classifier definitions) need an Enterprise licence; the source licence is not stated on the pages read |
| Pricing | Not documented on the pages read |

## 4. Limitations (for our purposes)
Live-load strategies operate between deployments of one model, not across models of different quality; the docs call usage-based routing slow in production; Auto Router tiers are rules or LLM classification, not a router trained on measured model quality; Auto Routing is beta and its config keys may change.

## 5. Comparison with the AI Request Router
LiteLLM is the nearest open gateway. It can already combine a complexity tier with latency-aware or least-busy deployment selection by configuration. The project's differences are a learned per-prompt quality predictor, a scoring function that trades quality, cost and live load across *different models* in one decision, explicit latency budgets and Prometheus-driven signals; LiteLLM could be a backend rather than a rival.

## 6. Proposal claims check (proposal section 2)
| Proposal claim | Status on 2026-10-31 |
|---|---|
| Router uses latency-based, least-busy and cost-based strategies plus fallbacks | **Holds** (names above) |
| Auto Router "(beta, 2026)" sorts requests into complexity tiers mapped to models | **Holds**: beta since v1.94.0, v2 post dated 2026-07-13, tiers `SIMPLE` to `REASONING`. Auto Router v2 adds LLM classifiers and adaptive pools, so describe it more fully |
| Core Router sends easy and hard questions to the same model | **Holds** for the Router; not for the Auto Router |
| Usage-based strategy "adds latency from Redis tracking and is not recommended for production" | **Holds**; the docs say usage-based routing "is not recommended for production due to performance impacts" |
| Auto Router docs do not mention live load, queue depth, GPU use or latency budgets | **Holds for classification**, with a caveat: tier selection ignores load, yet the chosen model's deployments are then picked by the Router strategy, which can be `least-busy` or latency-based. Reword to "does not use load to pick the tier" |
| "Competitors are moving" | **Confirmed**: adaptive Thompson-sampled pools are online learning from feedback, still not load |
