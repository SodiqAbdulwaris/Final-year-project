Status: DRAFT
Depends on: D04; L04; L10
Sources: Current official sources in each competitor record
Open items: Release-specific and submission-date rechecks

# Current comparison note

The [active Table 2.2](../../proposal-drafts/02-literature-review/2.5-existing-systems.md) supersedes conflicting historical rows below. TrueFoundry now documents complexity routing and local backends; OpenRouter Auto Router selects models per prompt; Martian current offering details remain unverified. Vendor documentation is grey literature accessed 31 October 2026. No product was operationally benchmarked.

## Historical comparison

# Competitor review: overview (grey literature)

All facts come from vendor or project documentation fetched on **2026-10-31** and are grey literature, not peer-reviewed. "Not documented" means the page read does not say; it does not mean the feature is absent. Vendor docs change often; re-fetch before submission.

## 1. Systems reviewed
| System | File | Pages read |
|---|---|---|
| OpenRouter | [openrouter.md](openrouter.md) | provider routing, model fallbacks, Auto Router, BYOK, FAQ |
| LiteLLM (Router and Auto Router) | [litellm.md](litellm.md) | Router, Auto Routing (beta), v2 announcement |
| Portkey (now Prisma AIRS AI Gateway) | [portkey.md](portkey.md) | load balancing, fallbacks, conditional routing, circuit breaker, retries |
| TrueFoundry AI Gateway | [truefoundry.md](truefoundry.md) | virtual models and load balancing |
| Martian | [martian.md](martian.md) | docs home, Gateway page |
| vLLM Semantic Router | [vllm-semantic-router.md](vllm-semantic-router.md) | README, v0.3 blog, arXiv 2603.04444 |
| Not Diamond | [notdiamond.md](notdiamond.md) | docs index, routing concepts, custom-router training, `/modelSelect` reference, pricing |
| Agent Router (Envoy), Kong AI Proxy Advanced, Cloudflare AI Gateway | [other-gateways.md](other-gateways.md) | overview pages only |

## 2. Table 2.2: feature comparison
Legend: yes / no / partial as documented; "n.d." = not documented on the pages read. "Proposed" is a plan, not a result.

| Feature | OpenRouter | LiteLLM Router | LiteLLM Auto Router | Portkey | TrueFoundry | Martian | vLLM Semantic Router | Kong AI Proxy Adv. | Not Diamond | Proposed router |
|---|---|---|---|---|---|---|---|---|---|---|
| Chooses the model per prompt | partial (Auto Router: task type plus 7-day spend share) | no | yes (complexity tiers) | partial (hand-written rules on metadata and params) | no | n.d. (indicated by RouteLLM benchmark) | yes (signals, decisions, 13 selection algorithms) | partial (semantic algorithm) | yes (learned; pre-trained or custom router) | yes (planned) |
| Learned difficulty or quality predictor | no | no | no (heuristic, LLM classifier, adaptive bandit) | no | no | n.d. | partial (some learned selectors) | n.d. | yes (predicts best model per query; method not published) | yes (planned) |
| Live load signals | provider stats over minutes ("rolling 5-minute window" for percentile filters) | partial (least-busy, latency-based, usage-based) | partial (via the Router strategy on the chosen model) | no (static weights; circuit breaker on errors) | partial (TPOT, TTFT windows of 3 to 20 minutes) | n.d. | partial (runtime TPOT/TTFT percentiles; queue and GPU n.d.) | partial (least-connections, lowest-latency) | n.d. (latency is a catalog value) | yes (planned: queue depth, GPU, Prometheus) |
| Per-request latency budget | partial (`preferred_max_latency`, soft) | n.d. | n.d. | n.d. | partial (per-target `sla_cutoff`) | n.d. | n.d. (formulation mentions latency constraints; no budget, SLO or deadline mechanism found in the full preprint text) | n.d. | partial (`tradeoff: latency` mode, no budget) | yes (planned) |
| Fallback and failover | yes | yes | yes | yes (plus circuit breaker) | yes | n.d. | yes (weighted failover) | yes | n.d. | yes (planned) |
| Self-hosted GPU backends | n.d. (BYOK keys only) | yes (`hosted_vllm/` per the vLLM provider page) | yes (via Router) | n.d. for model servers | n.d. | n.d. | yes (local vLLM) | n.d. | partial (custom endpoints can be candidates; router hosted) | yes (planned) |
| Open source or inspectable rules | no source stated; high-level description | yes (self-hostable; licence not stated on page) | yes (same) | partial (open gateway repo exists) | n.d. | no rules published | yes (Apache-2.0) | no (Enterprise plugin) | no (closed service) | yes (own code, planned) |
| Pricing model documented | pass-through plus credit fee; BYOK 5% | n.d. | n.d. | n.d. | n.d. | n.d. | free software | enterprise licence | $0.05 per million tokens routed | n/a |

## 3. Proposal claims check (proposal section 2)
| Claim in `AI_Request_Router_Proposal.docx` | Status on 2026-10-31 | Suggested rewording |
|---|---|---|
| OpenRouter chooses between providers of a named model, "not between models" | **Outdated in part.** `openrouter/auto` selects a model per prompt (task classifier plus market spend ranking, `cost_tier`). | "Provider routing is per named model; its Auto Router picks a model per prompt from community spend, not from live backend load." |
| OpenRouter latency and throughput use rolling 5-minute statistics | **Holds** for the percentile filters (`preferred_*`); the default-routing page says only that it "reacts within minutes". | Say "statistics over recent minutes". |
| "A sudden queue build-up shows up late" | **Inference, not documented.** | Present as the project's argument, not as a documented fact. |
| Setting a sort order turns load balancing off | **Holds**: `sort` "bypasses default routing". | Use the doc's wording. |
| OpenRouter does not cover self-hosted GPUs | **Holds** for the pages read (BYOK keys only). | Keep, with "in the pages reviewed". |
| LiteLLM Router balances with latency-based, least-busy, cost-based strategies plus fallbacks | **Holds.** | Add that `simple-shuffle` is the default and recommended strategy. |
| LiteLLM usage-based strategy adds Redis latency and is not recommended for production | **Holds** (docs: "not recommended for production due to performance impacts"). | Keep. |
| LiteLLM Auto Router (beta, 2026) sorts into complexity tiers | **Holds**; v2 announced 2026-07-13, beta since v1.94.0, adds LLM classifiers, keyword rules and Thompson-sampled adaptive pools. | Describe v2 accurately. |
| Auto Router docs do not mention live load, queue depth, GPU use or latency budgets | **Holds for tier selection**; after the tier is chosen, the Router's `least-busy` or latency strategy can pick the deployment. | "Does not use load to choose the tier." |
| Martian is closed and cannot run on your infrastructure | **Not verifiable.** Public docs describe a hosted gateway and no routing method. | "The public documentation describes a hosted gateway only." |
| "In the documentation we reviewed, none picks the model per prompt, watches live load, and also runs on your own GPUs." | **No longer safe as written.** vLLM Semantic Router (open source) does per-prompt selection, self-hosted vLLM backends and runtime latency statistics; Kong, TrueFoundry and LiteLLM add target-level load or latency awareness. | Narrow it: none of the products reviewed documents queue-depth and GPU-utilisation signals together with a learned per-prompt quality score, explicit latency budgets and self-hosted serving in one router. Add vLLM Semantic Router to the review. |

## 4. RouteBalance and the "routing plus live load together" gap
RouteBalance (Da & Kalyvianaki, 2026; arXiv 2606.17949; file `../03-load-balancing/da-2026-routebalance.md`, written by another worker; I read that file, not the paper) is a **preprint** that chooses a model instance per request from a weighted score of predicted quality, latency and cost, with queue depth and KV-cache telemetry from vLLM workers, and uses vLLM Semantic Router as a baseline. It **weakens** the claim that nobody combines per-prompt choice with live load. What it does not cover (per that file): hosted API backends, per-request latency budgets, failover beyond losing a tier, one model family and one cluster, preprint status.

Combined with vLLM Semantic Router and the 2026 preprints listed in the topic 01 overview (batch routing under capacity limits, CEMA-Router, market-aware routing, RouterWorld), the gap should be stated as: **the peer-reviewed routing literature to 2025 and the commercial gateways documented here do not combine learned per-prompt quality prediction, live queue and GPU signals, per-request latency budgets, failover and hosted-plus-self-hosted backends in one router; recent preprints and the open-source vLLM Semantic Router cover parts of this combination.** The project's contribution then rests on the combination and on a measured comparison, not on being first.

## 5. Caveats
- vLLM Semantic Router's latency-budget cell is "not documented", not "absent": I searched the whole preprint text and README/blog for "budget", "SLO" and "deadline" and found no per-request mechanism, but I did not read the repository's configuration reference.
- Several pages were read as converted HTML or Markdown; config names were copied from those texts. Figures such as window lengths are as stated by each vendor.
- LiteLLM, OpenRouter and Portkey docs ship frequent changes; the Portkey docs now brand the product "Prisma AIRS AI Gateway".
- A README of one project contains public demo credentials; I did not use them.
- Martian, Agent Router and Cloudflare were read at overview depth only; Not Diamond was read in more depth (routing, training and API reference).
