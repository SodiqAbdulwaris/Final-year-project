# Other notable routers and gateways (grey literature: vendor documentation)

| Field | Value |
|---|---|
| Type | short notes on three products (not full reviews); grey literature |
| Pages read | landing or overview pages only (see references); deeper pages not read |
| Fetched | 2026-10-31 |
| Relevance to project | Low to Medium (context for the gap statement) |

## APA 7 references
Agentic AI Foundation. (n.d.). *Agent Router (formerly Envoy AI Gateway) documentation* (Version 1.2). Retrieved October 31, 2026, from https://aigateway.envoyproxy.io/docs/

Kong Inc. (n.d.). *AI Proxy Advanced*. Kong Docs. Retrieved October 31, 2026, from https://developer.konghq.com/plugins/ai-proxy-advanced/

Cloudflare. (2026, April 20). *Cloudflare AI Gateway* and *Fallbacks*. Cloudflare Docs. Retrieved October 31, 2026, from https://developers.cloudflare.com/ai-gateway/ and https://developers.cloudflare.com/ai-gateway/configuration/fallbacks/

## Not Diamond
Covered in its own file: [notdiamond.md](notdiamond.md).

## Agent Router (formerly Envoy AI Gateway)
Open-source project built on Envoy Proxy, Kubernetes-native, now under the Agentic AI Foundation. The overview lists shared access across teams, credentials kept out of applications, quotas, usage attribution, failover, and "hosted and self-managed models within a single platform boundary". Backend rate limiting and policy control are stated. Per-prompt model selection, load-aware selection and routing algorithms: **not documented** on the overview page read.

## Kong AI Proxy Advanced
Enterprise plugin (AI Gateway Enterprise licence). Load-balancing algorithms listed: round-robin (weighted), consistent-hashing (sticky sessions), **least-connections** ("route to backends with spare capacity"), **lowest-latency**, **lowest-usage** (token counts or cost), **semantic** ("route based on prompt-to-model similarity") and **priority** (tiered failover), with configurable retries, timeouts and failover. The semantic algorithm is per-prompt selection by embedding similarity; least-connections and lowest-latency are load-aware at the target level. Self-hosted model targets and queue-depth signals: not documented on the page read.

## Cloudflare AI Gateway
Analytics, logging, caching, rate limiting, and **request retry and fallback**: fallbacks are triggered on request errors or predetermined timeouts, with a `cf-aig-step` response header showing which step answered. No per-prompt model selection or load-aware routing found on the pages read. Pricing and self-hosting not documented there ("available on all plans" for the gateway).

## Why it matters for the project
Together with vLLM Semantic Router and LiteLLM, these show that per-prompt selection (Kong semantic, Not Diamond (see notdiamond.md), LiteLLM Auto Router), target-level load awareness (Kong, LiteLLM, TrueFoundry) and fallback (all) each exist in separate products. None of the pages read documents queue-depth or GPU signals, latency budgets, and learned per-prompt quality in one self-hostable router.
