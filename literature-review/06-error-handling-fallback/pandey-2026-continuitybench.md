# ContinuityBench: stateful failover in multi-provider LLM routing (Pandey & Singh, 2026)

| Field | Value |
|---|---|
| Topic (home) | 06 Error handling and fallback |
| Also relevant to | 01 Routing algorithms, 07 Benchmarks |
| Paper type | benchmark and systems study |
| Venue and status | preprint only (arXiv, 17 July 2026, 16 pages); authors are from a commercial gateway vendor (Metriqual) |
| Source read | full text (https://arxiv.org/pdf/2607.15899) |
| Verified on | 2026-10-31, against the arXiv abstract page |
| Relevance to project | High |

## APA 7 reference
Pandey, V., & Singh, G. (2026a). *ContinuityBench: A benchmark and systems study of stateful failover in multi-provider LLM routing* [Preprint]. arXiv. https://doi.org/10.48550/arXiv.2607.15899

## In-text citation forms
(Pandey & Singh, 2026a) · Pandey and Singh (2026a); the same-year companion is 2026b

## 1. What it is about
The paper argues that a gateway can fail over successfully (HTTP 200, healthy dashboards) while the user's conversation silently resets, because the fallback model never sees the earlier turns. It defines two metrics, builds an open test harness, and compares a stateless failover proxy with one that forwards the full history.

## 2. The problem
Gateways such as LiteLLM, Portkey and OpenRouter retry a failed request on another provider, and their reliability claims concern uptime and returned responses. The authors say no benchmark checks whether the post-failover answer reflects the earlier dialogue ("availability is not continuity").

## 3. Proposed solution
- **Continuity Preservation Rate (CPR):** share of failover events where the fallback response shows access to a fact stated earlier. **Continuity Latency Overhead (CLO):** mean extra end-to-end latency of the stateful system over the stateless one, paired per conversation.
- **Architecture:** an OpenAI-compatible proxy with a request interceptor, a per-conversation state store, a deterministic fault injector (timeout, 502, 429) and a failover controller walking a fallback chain. The two compared systems differ in one line: the baseline forwards only the last user message; the treatment ("History-Forwarding") forwards the whole `messages[]` array.
- **Scoring:** a GPT-4o judge decides whether a planted fact (preference, invented term, name, number, date) is recalled; a substring fast-path skips the judge; calibration agreed with 19 of 20 hand labels; 10 treatment cases were audited by hand.

## 4. Data, models and tools
- 150 synthetic conversations of 7 to 11 turns, 30 per fact type, with the failure injected at the final probe turn; five runs gives N = 750 events per system; concurrency 100.
- Primary OpenAI gpt-4o-mini, fallback Anthropic Claude 3.5 Sonnet. Code and data: https://github.com/Vishal-sys-code/continuity-bench.

## 5. Key results
- Table 1: treatment CPR 744 / 750 = 99.20% (95% Wilson CI 98.27 to 99.63); baseline 0 / 750 (0.00%, CI 0.00 to 0.51). Per-run treatment CPR 98.7 to 99.3% (Table 2).
- Table 3 (run 5): mean CLO +59 ms, median −450 ms, P95 +13,614 ms; mean latency 6,283 ms vs 6,225 ms for the baseline. The tail cases are the longest conversations.
- Retry storm: with a fixed 2 s retry interval and a fallback limited to 15 requests per minute, 100 concurrent failovers hammered the endpoint, CPR fell to zero and the proxy crashed. This was observed during development with a Google Gemini free-tier fallback (15 requests per minute); Gemini was not part of the final OpenAI-to-Claude chain, so the headline CPR figures contain no retry-storm runs and the storm result is a negative finding, not a measured rate. The fix is capped exponential backoff with jitter, t = min(30, 2^a + U(0,1)) seconds.
- Race condition: a shared history cache let concurrent conversations mix, dropping CPR to 28% at concurrency 100 until histories were deep-copied per conversation.

## 6. Limitations
*Stated by the authors:* synthetic data; LLM-as-judge risk; one provider pair; text only, no streaming or mid-stream failover; a single failure per conversation, no cascading failovers.

*My observations:* the baseline is built to discard history, and the claim that deployed gateways behave this way rests on reading their documentation, not on testing them. A client of an OpenAI-compatible endpoint normally resends the full `messages[]` on every call, so the finding may mostly show that models answer from provided context. The paper's contribution is therefore the metrics and the failure modes, not the 99.2% figure. Single-vendor preprint; the "sub-5 ms" Rust data plane is not evaluated; no cost or load-aware routing; the paper's companion, FailureAtlas, describes this benchmark differently (as persona and multi-turn coherence), which suggests loose editing.

## 7. Relevance to the AI Request Router
- Closest published treatment of **gateway failover**. Supports a requirement that failover forwards complete conversation state (or a summary) and that continuity is tested, not assumed.
- **Reuse:** CPR and CLO as benchmark metrics for the failover tests (3.9); fault injection of timeout, 5xx and 429; backoff with jitter; per-session isolation of state under concurrency. **Avoid:** presenting 99.2% as general. **Not covered:** self-hosted backends, KV-cache loss, circuit breakers, live load, streaming.

## 8. How to use it in the report
Section 2.5 (fallback in LLM gateways) as the only direct study, labelled preprint; and the failover evaluation in 3.9. "Pandey and Singh (2026a) show in a preprint that failover without conversation history gives a 0% continuity rate in their harness, and that fixed-interval retries against a rate-limited fallback cause a retry storm."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Pandey & Singh (2026a) | Measure conversational continuity under provider failover | CPR and CLO metrics; stateless vs history-forwarding proxy; fault injection; LLM judge | 150 synthetic conversations × 5 runs; GPT-4o-mini to Claude 3.5 Sonnet | CPR 99.20% vs 0%; retry storm and race condition found | Preprint; synthetic; no streaming; strawman baseline |
