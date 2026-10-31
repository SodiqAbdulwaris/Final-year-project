# FailureAtlas: failure modes of multi-provider LLM gateways (Pandey & Singh, 2026)

| Field | Value |
|---|---|
| Topic (home) | 06 Error handling and fallback |
| Also relevant to | 01 Routing algorithms, 04 Cost reduction |
| Paper type | taxonomy (empirical catalog) |
| Venue and status | preprint only (arXiv, 20 July 2026); same vendor authors as ContinuityBench |
| Source read | full text (https://arxiv.org/pdf/2607.17525) |
| Verified on | 2026-10-31, against the PDF header and a search listing; the arXiv abstract page itself was not fetched |
| Relevance to project | High |

## APA 7 reference
Pandey, V., & Singh, G. (2026b). *FailureAtlas: A taxonomy of failure modes in multi-provider LLM serving infrastructure* [Preprint]. arXiv. https://doi.org/10.48550/arXiv.2607.17525

## In-text citation forms
(Pandey & Singh, 2026b) when cited together with ContinuityBench · Pandey and Singh (2026b)

## 1. What it is about
A small catalog of real failure modes in LLM gateways (reverse proxies that route, load-balance and rate-limit calls to model APIs), organised on two axes: the layer where the fault originates and whether it is *loud* (visible to ordinary monitoring) or *silent* (HTTP 200 but wrong).

## 2. The problem
Gateway bugs are scattered across issue trackers and post-mortems and are rediscovered by each team. Classical failure taxonomies do not include LLM-specific concerns such as streaming token protocols and conversation state, and model benchmarks treat infrastructure as transparent.

## 3. Proposed solution
A 5 × 2 matrix. Layers: network/transport, streaming/protocol, state/session, model behaviour, governance/cost. Detectability: loud or silent. Entries had to be concrete, backed by a persistent URL and mechanistically explained. The catalog has five entries (three from the LiteLLM issue tracker, two from the authors' own stress tests):
- **Streaming index collision** (silent): a proxy stamps every streamed tool call `index=0`, merging parallel tool-call arguments into invalid JSON that is saved to history and fails one turn later.
- **Redis semaphore leak** (loud): a missing cleanup on an error path leaves a rate-limit counter that never decrements, locking out the key.
- **Event-loop block** (loud): a synchronous call blocks the async loop, so health probes time out.
- **History race condition** (silent): concurrent read-modify-write on session history silently drops turns.
- **Retry storm** (loud): synchronised fixed-interval retries against a rate-limited provider; the authors report 25% of requests failing permanently in their test, with 100 parallel agents.
The model-behaviour layer is left empty for lack of reproducible evidence.

**How cost enters.** Not modelled numerically. The governance layer notes that retries, partial completions and duplicate calls corrupt cost accounting, and silent substitution of cheaper model variants is cited as an example of a silent failure.

## 4. Data, models and tools
Public GitHub issue trackers of LiteLLM, Portkey and OpenRouter, scoped search strings, manual verification of each thread and fix; standalone reproduction scripts for three entries (race, retry storm, index collision). Catalog repository: https://github.com/Vishal-sys-code/failure-atlas.

## 5. Key results
- Principal claim: the most severe failures are silent; the three loud entries were reported as incidents and fixed, while the two silent ones were found only through semantic checks or manual inspection of raw chunks.
- Reproductions show fixed-interval retries failing against a mock rate-limited provider while exponential backoff with jitter succeeds.
- The paper offers no prevalence or frequency figures.

## 6. Limitations
*Stated by the authors:* only five entries; three from one gateway; one layer empty; two entries reproduced only by the authors themselves; the findings are architectural patterns, not a claim about other gateways.

*My observations:* a selection-driven catalog (survivors of strict inclusion criteria) cannot support claims about how common failures are or that silent failures dominate. Non-peer-reviewed, written by a vendor of a competing gateway, and self-citing: it describes ContinuityBench as measuring persona and factual coherence, while that paper's actual metric is post-failover continuity.

## 7. Relevance to the AI Request Router
- A **checklist for the failover design and its tests**: jittered backoff, per-session locking, bounded semaphores released in `finally`, no blocking calls in the async path, stateful stream chunk handling.
- Motivates **semantic health checks** in addition to HTTP status and latency, relevant to the circuit-breaker signals (error rate and latency alone would miss silent faults).
- **Reuse:** the layer × detectability vocabulary for the Chapter 3 risk table. **Avoid:** quoting it as evidence of prevalence. **Not covered:** self-hosted engines, GPU faults, recovery times.

## 8. How to use it in the report
Section 2.5 and the risk analysis. "Pandey and Singh (2026b) catalog five reproducible gateway failure modes and argue that status-code monitoring cannot see the silent ones, which motivates semantic checks alongside circuit breakers."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Pandey & Singh (2026b) | Classify failures of multi-provider LLM gateways | Layer × detectability taxonomy; five verified entries with reproductions | LiteLLM, Portkey, OpenRouter issue trackers; mock provider | Worst failures are silent (HTTP 200) | Five entries; preprint; vendor authors; no prevalence data |
