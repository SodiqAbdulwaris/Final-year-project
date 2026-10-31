# Not Diamond (grey literature: vendor documentation)

| Field | Value |
|---|---|
| Type | commercial hosted model-routing service (API plus SDKs); grey literature (vendor documentation, not peer reviewed) |
| Pages read | docs index, "What is Model Routing?", key concepts, custom-router training, routing between custom models, `/modelSelect` API reference, pre-trained router for code, rate limits, security, pricing page |
| Fetched | 2026-10-31 |
| Relevance to project | **High**: it is the product most similar to the project's *per-prompt scoring* component, but not to its load-aware gateway part |

## APA 7 references
Not Diamond. (n.d.-a). *What is model routing?* Retrieved October 31, 2026, from https://docs.notdiamond.ai/docs/what-is-model-routing

Not Diamond. (n.d.-b). *Key concepts*. Retrieved October 31, 2026, from https://docs.notdiamond.ai/docs/key-concepts

Not Diamond. (n.d.-c). *Training a custom router*. Retrieved October 31, 2026, from https://docs.notdiamond.ai/docs/router-training-quickstart

Not Diamond. (n.d.-d). */modelSelect* [API reference]. Retrieved October 31, 2026, from https://docs.notdiamond.ai/reference/token_model_select_v2_modelrouter_modelselect_post

Not Diamond. (n.d.-e). *Pricing*. Retrieved October 31, 2026, from https://www.notdiamond.ai/pricing

In-text: (Not Diamond, n.d.-a)

## 1. What it is
A service that "predicts which model will provide the highest quality response at the lowest cost" for each query (paraphrasing the docs). The caller sends the messages plus a list of candidate models (`llm_providers`) to the `/modelSelect` endpoint (SDK: `client.model_router.select_model(...)`) and receives the chosen model and a session ID; the application then calls that model itself. The pricing FAQ says Not Diamond "is not a gateway" and integrates with existing gateway infrastructure.

## 2. How routing works
- **Routers:** a *pre-trained router: Chat* trained on cross-domain data; a *pre-trained router: Code* (early access, aimed at long-horizon coding agents; the page claims it "reduces your long-horizon coding agent cost by 30%+", a vendor claim not independently checked); and **custom routers**.
- **Custom router training:** you supply (1) inputs representative of your prompts, (2) the responses of each candidate LLM, and (3) evaluation scores for those responses, from any metric; the service learns a "meta-model" that predicts which LLM to use per query. Candidate models may include your own fine-tuned models or any inference endpoint, declared with `"is_custom": true` plus `context_length`, `input_price`, `output_price` and `latency` (seconds). The result is identified by a `preference_id`.
- **Three documented trade-off modes:** quality (default), cost and latency; the latency mode favours the fastest response above a quality threshold per the routing overview, which is a preference rather than a per-request budget. **Trade-off parameters:** `tradeoff` (`"cost"`, `"latency"`, or none for quality-first; the docs say it uses Pareto optimisation); `cost_quality_tradeoff`, an integer 0 to 10 (0 is quality-first, 10 always the cheapest), supported only on the pre-trained router and mutually exclusive with `tradeoff`. Other request fields include `metric` (default `"accuracy"`), `max_model_depth`, `hash_content`, `previous_session` and `tools`.
- **Fallback and failure handling:** not documented in the pages read. The API returns a selection; calling the model and retrying are left to the application. Rate limit: 50 requests per second, with a 429 on excess and advice to use exponential backoff.

## 3. Feature checklist
| Question | Finding |
|---|---|
| Per-prompt model choice | **Yes**, learned (pre-trained or customer-trained) |
| Predicts difficulty or quality | Yes: predicts which candidate gives the best response on the chosen `metric`; the model internals are not described |
| Live load signals | **Not documented.** Latency is a catalog value per model (and a number you declare for custom models), not a live measurement; no queue depth or GPU state |
| Latency budget per request | **Partial: a latency preference, not a budget.** The docs list three trade-off modes (quality by default, cost, latency); the latency mode "minimizes response time while maintaining quality thresholds" (routing overview). No per-request time limit or SLO is documented |
| Fallback and failover | Not documented |
| Self-hosted GPU backends | Custom endpoints can be named as candidates, so you can route *to* your own model server; whether the router itself can run on your infrastructure is not documented (the pricing page lists "privacy-preserving deployment" for Enterprise; the docs page titled for local deployments contains only a security note) |
| Openness | Closed hosted service; SDKs are published (`notdiamond`); no router source or training method documented |
| Pricing | Pay-as-you-go "$0.05 per million tokens routed" (pricing page, as read); Enterprise on contact |

## 4. Limitations (for our purposes)
Selection is a one-shot API call before generation, so each request carries an extra network round trip; routing quality depends on evaluation data you must supply for custom routers; no load or availability awareness is documented, so a chosen model can still be saturated; the method is not published, so it cannot be inspected or reproduced.

## 5. Comparison with the AI Request Router
Not Diamond covers the *what is the best model for this prompt* half with a trade-off dial, much like the project's classifier and cost-quality scoring function, and it can name custom endpoints. It does not document the other half the project targets: signals from live backends (queue depth, GPU use), explicit latency budgets, failover and a gateway that runs on the user's own infrastructure. It is a reasonable external baseline or an optional scoring plug-in, and a good reason to avoid claiming that per-prompt model choice is novel.
