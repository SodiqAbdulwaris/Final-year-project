Status: DRAFT
Depends on: L04; L10
Sources: Official vendor documentation linked below
Open items: Pinned release/configuration and feature checks before submission

## 31 October 2026 current-source recheck

Current homepage focuses on model-science work and links Thesean AI; the historical router offering details were not established by this page. Treat old routing/deployment claims as unverified. [Vendor documentation](https://withmartian.com/), accessed 31 October 2026. This note supersedes conflicting rows below; the earlier review is retained as history.

# Martian (grey literature: vendor documentation)

| Field | Value |
|---|---|
| Type | commercial model gateway and router; grey literature (vendor documentation) |
| Pages read | documentation home, Gateway page, company home page; a pricing page URL returned 404 |
| Fetched | 2026-10-31 |
| Relevance to project | Medium (named in the proposal; routing behaviour is largely undocumented publicly) |

## APA 7 references
Martian. (n.d.-a). *Martian documentation*. Retrieved October 31, 2026, from https://docs.withmartian.com/

Martian. (n.d.-b). *Gateway*. Retrieved October 31, 2026, from https://docs.withmartian.com/gateway

Martian. (n.d.-c). *Martian: Understanding intelligence*. Retrieved October 31, 2026, from https://www.withmartian.com/

In-text: (Martian, n.d.-a)

## 1. What it is
The public documentation describes the **Martian Gateway**: "unified access to 200+ AI models through a single API", compatible with the OpenAI and Anthropic APIs, with a dashboard showing real-time usage, model performance and request history. The company describes itself as a research lab; the documentation also covers a separate agent-training framework (ARES). Some further documentation is for partners behind a login.

## 2. How routing, fallback and load balancing work
**Not documented** in the public pages read: no algorithm, config names, fallback behaviour or load-balancing strategy. An earlier third-party description exists in peer-reviewed work: RouteLLM (Ong et al., 2025, Appendix E) benchmarked a Martian router by choosing performance optimisation with a maximum cost of USD 10.45 per million tokens, which implies a cost-cap parameter and per-prompt selection. I did not verify this against Martian's own documentation, and it describes the router as it was in 2024.

## 3. Feature checklist
| Question | Finding |
|---|---|
| Per-prompt model choice | Not documented in the public pages; indicated by RouteLLM's 2024 benchmark of a Martian router |
| Predicts difficulty or quality | Not documented |
| Live load signals | Not documented |
| Latency budget per request | Not documented |
| Fallback and failover | Not documented |
| Self-hosted GPU backends | Not documented (the Gateway is a hosted API) |
| Openness | Closed source is not stated, but no source code or rules are published for the router; the company has a GitHub organisation (RouterBench data was released there, per a search result not checked against the repository) |
| Pricing | Not documented (the pricing page URL tried returned 404) |

## 4. Limitations (for our purposes)
Nothing can be concluded beyond the API surface. For the report, Martian is best treated as a closed commercial router that was a baseline in RouteLLM and the source of the RouterBench dataset, with claims limited to what is documented.

## 5. Comparison with the AI Request Router
The proposal's statement that Martian's rules cannot be inspected and it cannot run on your own infrastructure is **consistent with the public documentation but not confirmed by it**: the docs describe only a hosted API. Word it as "the public documentation describes a hosted gateway and does not describe the routing method".
