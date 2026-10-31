Status: DRAFT
Depends on: D01–D12; Chapter 3 protocol
Sources: _meta/hybrid-design.md; _meta/history/ch4-ch5-skeletons.md
Open items: See _meta/placeholders.md

# Appendix F: Experiment Protocol

## Freeze record

| Item | Pre-specified value/status |
|---|---|
| Protocol/version/date | [PLACEHOLDER: protocol revision and freeze date] |
| Candidate models | [PLACEHOLDER: model names] |
| Permitted dataset revisions | [PLACEHOLDER: dataset hashes and licence clearance] |
| Estimator/training labels | TODO: estimator and label definition. |
| Calibration method | TODO: validation-only calibration choice. |
| Split protocol | TODO: grouped/deduplicated split, proportions and seed policy. |
| Quality margin δ | [PROVISIONAL: revise after pilot]; justify before viewing test data. |
| Cost/latency reduction criteria | [PROVISIONAL: revise after pilot]; no invented threshold. |
| Interval/multiplicity plan | TODO: confidence level, resampling groups and confirmatory comparison family. |
| Live/API budget and sample cap | [PLACEHOLDER: authorised spending cap and pilot size] |
| Stopping rule | TODO: fixed sample/cost cap and safety/constraint stop conditions before testing. |
| Failure parameters | TODO: retry eligibility, attempt bound, cooldown and breaker thresholds. |

## Hypotheses and comparisons

The quality analysis will test non-inferiority against the best single model chosen on validation data, not retrospectively the best test-set performer. H0 will state ΔQ ≤ −δ and H1 ΔQ > −δ. Cost and latency reduction comparisons will test ΔC < 0 and ΔL < 0 with their nulls, using a predeclared primary latency endpoint. Effect sizes and uncertainty will be reported even when no decision is conclusive.

## Arms and ablations

The fixed-model, cheapest-eligible, rule-based and lightweight learned baselines will share the same eligible pool, request caps and adapters. The hybrid will add classification and embedding-derived features. Ablations will remove embeddings, remove classification/task features and optionally isolate retrieval-only prediction. A utility comparator will obey the same hard restrictions. A quality cascade will be optional and separately costed.

## Leakage, measurement and analysis

Evaluated outcomes will remain outside training and retrieval evidence for evaluated requests. Duplicate/related tasks will stay in one split. Tuning will use the pilot/validation partition only. The team will record seeds, dataset revisions, model/engine configurations, prices, concurrency, warm-up and network conditions.

Quality, cost, TTFT/completion p50/p95, calibration, constraint violations and fallback completion will follow Section 3.9. Offered-request denominators will include timeouts and rejections. Paired comparisons will use matched requests and independent resampling groups. Live timing will not be fabricated from stored quality outputs.

## Fault injection and deviations

Local tests will inject connection failures, throttling, slow responses, malformed responses and mid-stream disconnects. Fallback will recheck remaining policy/resources; optional quality escalation will use different triggers. The protocol will state which faults are retryable and which partial-delivery cases will terminate explicitly.

| Date/revision | Deviation | Reason | Test data already inspected? | Confirmatory/exploratory effect |
|---|---|---|---|---|

No experiment has been run by this drafting task.
