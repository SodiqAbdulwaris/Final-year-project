Status: DRAFT
Depends on: L04; L10
Sources: Official vendor documentation linked below
Open items: Pinned release/configuration and feature checks before submission

## 31 October 2026 current-source recheck

Current Auto Router documents task/market-based per-prompt model selection. The older provider-only description is obsolete. Do not preserve a claim that only providers, never models, are selected. [Vendor documentation](https://openrouter.ai/docs/guides/routing/routers/auto-router), accessed 31 October 2026. This note supersedes conflicting rows below; the earlier review is retained as history.

# OpenRouter (grey literature: vendor documentation)

| Field | Value |
|---|---|
| Type | commercial hosted API gateway; grey literature (vendor documentation, not peer reviewed) |
| Pages read | provider routing, model fallbacks, Auto Router, BYOK, FAQ (URLs below) |
| Fetched | 2026-10-31 (raw Markdown versions of the docs pages) |
| Relevance to project | High (named in the proposal; closest hosted "many models, one API" product) |

## APA 7 references
OpenRouter. (n.d.-a). *Provider routing*. Retrieved October 31, 2026, from https://openrouter.ai/docs/guides/routing/provider-selection

OpenRouter. (n.d.-b). *Model fallbacks*. Retrieved October 31, 2026, from https://openrouter.ai/docs/guides/routing/model-fallbacks

OpenRouter. (n.d.-c). *Auto Router*. Retrieved October 31, 2026, from https://openrouter.ai/docs/guides/routing/routers/auto-router

OpenRouter. (n.d.-d). *BYOK*. Retrieved October 31, 2026, from https://openrouter.ai/docs/guides/overview/auth/byok

OpenRouter. (n.d.-e). *FAQ*. Retrieved October 31, 2026, from https://openrouter.ai/docs/faq

In-text: (OpenRouter, n.d.-a)

## 1. What it is
One API in front of many hosted models and providers. The same model can be served by several providers, so OpenRouter has two decisions: which provider serves the requested model (provider routing), and, if the caller asks, which model should serve the prompt (Auto Router, model fallbacks).

## 2. How routing, fallback and load balancing work
**Default provider routing** scores each provider on effective price, throughput, time to first token, 429 rate, reliability and tool-call quality, each measured from recent production traffic. Requests pick a provider at random, weighted by those scores; a provider with much worse error or 429 rates gets no traffic until it recovers; the router learns how much load each provider can take before it returns 429s and sends the rest elsewhere. Retries pick from the remaining providers. Follow-up requests stay on one provider while its prompt cache is warm.

**Explicit controls** in the `provider` object: `sort` (`"price"`, `"throughput"`, `"latency"`, optional `partition`), `order`, `only`, `ignore`, `allow_fallbacks` (default `true`), `preferred_min_throughput` and `preferred_max_latency` (p50 to p99 cutoffs, which move a failing endpoint to the end of the list rather than excluding it), `max_price`, `data_collection`, `zdr`. Latency and throughput percentiles are computed over a "rolling 5-minute window", per model and provider. Setting `sort`, `order`, the `:nitro` or `:floor` shortcuts, or using your own provider key bypasses default routing.

**Model fallbacks:** a `models` array in priority order; the next model is tried if the first returns an error (providers down, rate-limited, moderation refusal).

**Auto Router** (`openrouter/auto`, early-access `openrouter/auto-beta`): a lightweight classifier assigns the prompt to one of about 30 task types (for example `code:debugging`, `math`); models are ranked by their share of OpenRouter community spend for that task type over a trailing 7-day window; a `cost_tier` (`low`, `medium`, `high`, `xhigh`, `max`) filters the band; the top models become the primary pick plus fallbacks. If classification or rankings are unavailable it degrades to a default model set.

## 3. Feature checklist
| Question | Finding |
|---|---|
| Per-prompt model choice | Yes, through Auto Router (task classifier plus market spend ranking). Provider routing itself is per model. |
| Predicts difficulty or quality per prompt | Not documented; ranking is by task type and spend share, not predicted quality |
| Live load signals | Provider-level only: recent throughput, latency, 429 rate and learned capacity, "reacts within minutes". No queue depth, GPU use or per-request latency budget. Auto Router ranking is a 7-day market signal, not live load |
| Latency budget per request | Soft preference only (`preferred_max_latency`); not a hard budget |
| Fallback | Yes (`allow_fallbacks`, `models` array, Auto Router fallbacks) |
| Self-hosted GPU backends | Not documented. BYOK means your own keys for supported providers; no self-hosted endpoint option found in the pages read |
| Openness | Hosted service; routing logic described at high level, not inspectable; source licence not stated on the pages read |
| Pricing model | Provider prices passed through without markup, a fee on credit purchases (FAQ); BYOK costs 5% of what the model would cost on OpenRouter, after a plan-dependent allowance (BYOK page) |

## 4. Limitations (for our purposes)
No self-hosted serving; provider routing treats traffic as aggregate statistics, not the state of your own queues; Auto Router bases its choice on community spend rather than the quality your task needs and cannot be tuned with your own data; routing rules are not inspectable.

## 5. Comparison with the AI Request Router
OpenRouter is a hosted marketplace layer. The project adds per-prompt difficulty and quality scoring trained on its own benchmark data, live signals from backends it controls (queue depth, GPU utilisation), latency budgets and routing to self-hosted vLLM or Ollama. OpenRouter's Auto Router now overlaps with "per-prompt model choice", so that alone is no longer a differentiator.

## 6. Proposal claims check (proposal section 2)
| Proposal claim | Status on 2026-10-31 |
|---|---|
| "Chooses between providers of the model you name, not between models" | **Outdated in part.** Provider routing is still per named model, but `openrouter/auto` selects a model per prompt, and the `models` array adds model-level fallback. |
| Latency and throughput come from "rolling 5-minute statistics" | **Holds for the percentile stats** behind `preferred_*` and the documented window. The default-routing page gives no window; it says routing "reacts within minutes" and shifts load before 429s. |
| "A sudden queue build-up shows up late" | **Inference, not stated in the docs.** Reword as "stats are averaged over recent minutes, so very short spikes may not register". |
| "Setting a sort order turns load balancing off" | **Holds** in the current wording: setting `sort` "bypasses default routing" and providers are tried in the sort order. |
| "Docs cover listed providers and your own provider keys, not self-hosted GPUs" | **Holds** for the pages read (BYOK only). |
