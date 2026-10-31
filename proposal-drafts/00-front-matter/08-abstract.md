Status: DRAFT
Depends on: D02; D09; Chapters 1–3
Sources: _meta/decisions-applied.md; _meta/history/front-matter.md; owner-supplied template structure
Open items: Final title, dataset/model identities and frozen evaluation protocol

# Abstract

Large language model applications will need routing decisions that account for request requirements, model suitability, cost, latency and provider availability. This project will design and evaluate a hybrid prompt-aware routing algorithm with automatic operational fallback. Its contribution will be an explicit decision policy, an integrated gateway and controlled empirical evaluation rather than a claim of a fundamentally new machine-learning algorithm.

The proposed gateway will apply deterministic capability, context-window, budget and availability filters before selecting a deployment. Lightweight classification and embedding-derived evidence from historical scored requests will inform model-specific suitability estimates. A constrained policy will identify candidates meeting minimum predicted quality, estimated cost and deadline requirements, then prefer the cheapest feasible candidate. Health tracking, circuit breakers and bounded retries will handle eligible execution failures. Operational fallback will be evaluated separately from optional quality-based cascading after completed answers.

The study will reuse scored benchmark outputs where licences and aligned model coverage permit. Three to four candidate models will span small or cheap, mid-tier and frontier roles. Two RTX 4070 machines will support local feature processing and small-model reliability tests, while new hosted calls will be restricted to a capped subset. Fixed-model, cheapest-eligible, rule-based and lightweight learned baselines will be compared with the hybrid and component ablations.

Evaluation will measure quality, cost, latency, calibration, constraint violations and fallback success under injected failures. The team will justify a quality non-inferiority margin and freeze the protocol before examining test outcomes. Expected outputs will include the routing specification, software artefact and reproducible evaluation evidence. A simpler router matching the hybrid will remain a valid finding; no performance improvement or experimental result will be assumed.

**Keywords:** Calibration; Constraint-aware routing; Large language models; Operational fallback; Suitability prediction.
