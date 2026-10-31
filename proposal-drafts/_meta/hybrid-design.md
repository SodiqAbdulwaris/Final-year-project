Status: DRAFT
Depends on: D01–D12; decisions-applied.md
Sources: owner design response and proposal-building task
Open items: Final title; model identities; estimator; pilot targets

# Hybrid routing direction: owner response to D01

Recorded: 31 October 2026. Source: the owner's D01 response in this chat.

**Status:** owner-selected design direction. Supervisor approval is not established. This direction supersedes the earlier assumption that the 26 October guide governs every conflict. Neither the original proposal nor the guide alone defines the new core. This is a design record, not a verified literature claim or an experimental result.

## Working title and research question

Owner-proposed working title: **Design and Evaluation of a Hybrid Prompt-Aware, Multi-Objective LLM Routing Algorithm with Automatic Fallback**. Final title approval remains TODO.

Owner-proposed central question: Can combining lightweight prompt classification, embedding-based suitability features, and constrained multi-objective optimisation reduce inference cost and latency while preserving response quality and improving resilience compared with conventional routing methods?

Evaluate quality, cost and latency together; test resilience separately. Improvement is a hypothesis. A simpler router performing as well as the hybrid is a valid outcome.

## Three responsibilities

1. **Prompt-aware predictor:** estimate model-specific suitability from classification, prompt features and historical performance evidence.
2. **Constrained selection policy:** filter eligible models and select using predicted quality, cost and latency.
3. **Reliability controller:** execute through adapters, track provider health and handle bounded operational fallback.

Provider health affects eligibility and execution. It does not substitute for quality prediction.

## Request flow

### 1. Deterministic constraint filtering

Exclude candidates that violate mandatory capability, context-window, structured-output, budget or availability requirements. A classifier cannot override these restrictions. Identify which requirements are hard and which preferences may be relaxed.

### 2. Hybrid prompt analysis

Use lightweight classification for task category and required capabilities; difficulty may also be a feature. Retrieve similar historical requests using embeddings and their scored per-model outcomes. Classification, difficulty and similarity are correlated predictive features, not independent evidence of quality. Their contribution must be tested.

### 3. Model-specific suitability prediction

Estimate expected quality as Q_hat(m, q) = f(task, difficulty, similarity, model). Use one estimator with query/model features or a small set of per-model predictors; the exact estimator remains TODO. Prefer a practical sentence embedding model plus lightweight classifier over reproducing RouterDC's full dual-contrastive training architecture initially.

Training data, labels, calibration method and split protocol remain TODO. Keep evaluation outcomes out of training and retrieval evidence for the evaluated requests.

### 4. Constrained multi-objective selection

The preferred formulation applies justified minimum predicted quality, estimated cost caps and deadline constraints, then selects the most economical feasible candidate. Predicted quality and latency do not guarantee actual outcomes; measure calibration and violations.

A weighted utility U(m, q) = alpha * Q_hat - beta * C_hat - gamma * L_hat is a possible comparator or policy variant. Put terms on comparable scales and evaluate sensitivity to weights and constraints. The utility must not override hard restrictions. Exact policy, normalisation, weights, quality threshold and deadline semantics remain TODO.

If no candidate is feasible, follow an explicit policy: reject, relax an explicitly soft preference, or obtain permission to exceed an applicable constraint. Never silently exceed a hard budget or capability restriction. Which infeasibility response the MVP supports remains TODO.

### 5. Execution and operational fallback

Use deterministic logic for eligible retryable failures. Re-evaluate candidates against remaining budget, deadline, provider health and potentially consumed tokens. Track circuit-breaker state and bound retries. Retry eligibility, timeouts, thresholds, cooldowns and handling of uncertain usage remain TODO.

Operational fallback responds to execution failures. Quality cascading responds to an inadequate completed answer and is a separate, optional experiment. Do not conflate their costs, triggers or success rates.

### 6. Monitoring and calibration

Record predictions and observed quality, usage/cost and latency when measurable. Logging alone is not adaptive learning. Specify whether updates are offline or online, how often they occur and which evidence they use before claiming adaptation. No live learning mechanism has been approved.

## Scope by technique

| Technique | Owner's direction |
|---|---|
| Rule-based constraint filtering | Essential |
| Lightweight task/capability classification | Essential |
| Model suitability prediction | Essential |
| Cost and latency optimisation | Essential |
| Embedding similarity | Recommended hybrid component; evaluate with ablation |
| Health-aware eligibility and operational fallback | Essential |
| Quality-based cascading | Optional experimental extension |
| Reward-guided learning | Future enhancement |
| Reinforcement learning or POMDP | Exclude initially |
| Generative ensembling / response fusion | Exclude initially |

Live GPU/queue telemetry, Redis/Prometheus, session hysteresis, router-managed context and graph memory are not established as core requirements by this response. Preserve them as unresolved earlier proposals until explicitly reconciled; do not silently retain them as mandatory deliverables. The source of latency/load estimates remains TODO.

## Build and evaluation sequence

1. Establish fixed-model, cheapest-eligible, rule-based task-routing and lightweight learned-predictor baselines. Collect comparable scored outcomes for each candidate model.
2. Build the hybrid using classification and embedding-derived features. Compare with simpler baselines and ablations that isolate each component. Evaluate the quality–cost–latency trade-off and constraint satisfaction; do not assume the scoring formula is optimal.
3. Add provider-health tracking, circuit breakers, bounded retries and operational fallback. Test injected failures separately. Add a quality cascade only if time and evaluation budget allow.

The owner has specified two RTX 4070 machines and a minimal API budget. Use benchmark-covered model slots pending aligned coverage checks; numeric targets remain provisional under D03. The examples of 90% predicted success and $0.01 cost in the owner's explanation are illustrative, **not project targets**. No numeric targets or results are adopted here.

## D04: approved by owner on 31 October 2026

Recommended wording:

> This project investigates whether combining lightweight classification and embedding-derived suitability features with constrained cost–quality–latency selection improves on simpler routing baselines. Operational fallback is evaluated separately for resilience.

The contribution is the formal decision policy, integration and empirical evaluation. Do not claim first-of-its-kind status, a fundamentally new ML algorithm or demonstrated improvement without evidence. The owner explicitly approved this exact wording in the proposal-building task.

Hybrid LLM, RouteLLM, RouterDC and FrugalGPT were named as inspirations in the response. This record does not verify their claims, citations, versions or DOIs. Verify them under D12 and the source spot-check before using paper-specific assertions in the report.

## Remaining decisions and reconciliation

The proposal-building task supplies D01–D12 outcomes. Use decisions-applied.md; do not re-ask them. D10 is no manuscript now.

The active split Chapters 1–3 will follow this design. Earlier drafts and conflict tables are retained under history/ and are not governing text.

The owner now authorises Markdown proposal drafting, commit/push to main and no PR. Original DOCX files and Rejected/, Research Review/ and Team Briefs/ remain outside the editing scope.
