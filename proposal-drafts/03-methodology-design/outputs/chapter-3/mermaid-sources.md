Status: SUPERSEDED (kept as editable sources)
Depends on: none
Sources: Mermaid blocks removed from the Chapter 3 section files on 2026-11-04
Open items: none; the Word draft uses the Codex-generated PNGs in this folder, with new figure numbers

# Mermaid sources of the earlier Chapter 3 diagrams

The Word draft now uses the PNG figures in this folder (Figures 3.1 to 3.11). The earlier numbering is kept below only so that the sources can be traced; do not paste these blocks into the report.

## From 3.5-requirements.md

**Figure 3.1: Use cases and external actors.** The arrows will show participation, not inheritance or execution order.

```mermaid
flowchart LR
  C[Client application] --> R([Route request])
  C --> X([Apply constraints])
  C --> F([Operational fallback])
  A[Administrator] --> M([Monitor and calibrate])
  A --> X
  P[Provider / model backend] --> R
  P --> F
  R --> X
```

## From 3.6.1-architecture.md

**Figure 3.2: Logical architecture of the hybrid router.** Solid arrows will describe the request path; dotted arrows will show evidence and state dependencies.

```mermaid
flowchart LR
 C[Client] --> G[Gateway and validation]
 G --> F[Hard filters]
 F --> P[Preprocessing and classification]
 P --> E[Embedding and k-NN retrieval]
 P --> Q[Suitability predictor]
 E --> Q
 Q --> S[Constrained selector]
 S --> A[Execution adapters]
 A --> H[Hosted model]
 A --> L[Local model]
 R[Registry and budget reservations] -.-> F
 R -.-> S
 T[Health tracker and circuit breaker] -.-> F
 T -.-> A
 A --> O[Monitoring and logs]
 O -.-> T
 O -.-> V[Offline calibration on validation data]
 V -.-> Q
```

## From 3.6.1-architecture.md

**Figure 3.3: Proposed development and evaluation deployment.** The diagram will assign roles without assuming simultaneous model residency or equal VRAM.

```mermaid
flowchart TB
 C[Client and experiment driver] --> G[Router application and relational store]
 subgraph D[Laptop A: RTX 4070]
 G
 E[Embeddings / classifier / k-NN index]
 L[Small model via vLLM or Ollama]
 end
 subgraph P[Laptop B: RTX 4070]
 T[Local test backend / failure injection]
 end
 G --> E
 G --> L
 G --> T
 G --> A[Hosted API: capped pilot only]
```

## From 3.6.2-class-diagram.md

**Figure 3.4: Proposed domain responsibilities.** Classes will describe interfaces and ownership, not implemented code.

```mermaid
classDiagram
 class Gateway {
  +route(request, policy)
 }
 class EligibilityFilter {
  +eligible(request, deployments)
 }
 class PromptAnalyser {
  +classify(request)
 }
 class HistoricalRetriever {
  +neighbours(features, permittedIndex)
 }
 class SuitabilityPredictor {
  +predict(features, model)
 }
 class ConstrainedSelector {
  +select(estimates, constraints)
 }
 class ExecutionController {
  +execute(candidate, remainingPolicy)
  +fallback(failure)
 }
 class ProviderAdapter {
  +invoke(request, deployment)
 }
 class HealthTracker {
  +state(deployment)
  +record(outcome)
 }
 class BudgetAccountant {
  +reserve(attempt)
  +reconcile(usage)
 }
 class DecisionLog {
  +record(metadata)
 }
 Gateway --> EligibilityFilter
 Gateway --> PromptAnalyser
 PromptAnalyser --> HistoricalRetriever
 Gateway --> SuitabilityPredictor
 SuitabilityPredictor --> HistoricalRetriever
 Gateway --> ConstrainedSelector
 Gateway --> ExecutionController
 ExecutionController --> ProviderAdapter
 ExecutionController --> HealthTracker
 ExecutionController --> BudgetAccountant
 Gateway --> DecisionLog
```

## From 3.6.3-sequence-activity.md

**Figure 3.5: Normal routing request.** Validation and reservation will precede execution.

```mermaid
sequenceDiagram
 participant C as Client
 participant G as Gateway
 participant P as Feature pipeline / predictor
 participant S as Filter / selector
 participant B as Budget accountant
 participant A as Adapter / backend
 participant M as Monitoring
 C->>G: Request and declared policy
 G->>S: Validate and filter mandatory constraints
 G->>P: Analyse prompt and permitted history
 P-->>G: Per-model quality estimates
 G->>S: Quality, cost, latency and deadline estimates
 S-->>G: Cheapest feasible candidate or infeasible
 G->>B: Revalidate and reserve attempt spend
 B-->>G: Reservation or rejection
 G->>A: Dispatch only if reserved
 A-->>G: Response, usage and timing
 G->>B: Reconcile known usage
 G->>M: Redacted decision and attempt outcome
 G-->>C: Response or explicit error
```

## From 3.6.3-sequence-activity.md

**Figure 3.6: Execution failure and operational fallback.** Recovery will be a new constrained attempt, not continuation of an already delivered stream.

```mermaid
sequenceDiagram
 participant C as Client
 participant R as Reliability controller
 participant A as Primary backend
 participant H as Health tracker
 participant S as Selector / budget accountant
 participant F as Fallback backend
 R->>A: Reserved attempt
 A-->>R: Eligible retryable failure
 R->>H: Record failure and update breaker
 R->>S: Reconcile uncertain spend and check remaining deadline
 alt Attempts remain and no unsafe partial delivery
 S-->>R: Revalidated, affordable fallback reservation
 R->>F: New permitted attempt
 F-->>R: Response or failure
 R->>S: Reconcile fallback usage
 R-->>C: Response or explicit exhausted error
 else Retry unsafe, budget exhausted or no feasible candidate
 R-->>C: Explicit failure and no silent constraint relaxation
 end
```

## From 3.6.3-sequence-activity.md

**Figure 3.7: Request activity flow.** Infeasibility will be distinguished from provider failure.

```mermaid
flowchart TD
 A[Validate request] --> B[Filter capability, context, budget and availability]
 B --> C{Eligible candidates?}
 C -- No --> X[Explicit infeasibility]
 C -- Yes --> D[Classify and retrieve permitted neighbours]
 D --> E[Predict per-model suitability, cost and latency]
 E --> F[Apply quality, cost and deadline constraints]
 F --> G{Feasible candidate?}
 G -- No --> X
 G -- Yes --> H[Choose cheapest and revalidate and reserve]
 H --> I[Execute]
 I --> J{Completed?}
 J -- Yes --> K[Reconcile and return]
 J -- No --> L[Record health and uncertain usage]
 L --> M{Retryable, safe, attempts and resources remain?}
 M -- Yes --> B
 M -- No --> N[Explicit execution failure]
 X --> O[Redacted monitoring]
 K --> O
 N --> O
```

## From 3.6.4-database.md

**Figure 3.8: Proposed entity relationships.** Cardinalities will describe stored evidence; raw prompt text will not be required in the operational request table.

```mermaid
erDiagram
 MODEL ||--o{ DEPLOYMENT : exposes
 MODEL ||--o{ MODEL_CAPABILITY : supports
 CAPABILITY ||--o{ MODEL_CAPABILITY : defines
 DEPLOYMENT ||--o{ PRICE_VERSION : priced_by
 POLICY_VERSION ||--o{ REQUEST : governs
 REQUEST ||--o{ ESTIMATE : receives
 MODEL ||--o{ ESTIMATE : predicted_for
 REQUEST ||--o{ ATTEMPT : executes
 DEPLOYMENT ||--o{ ATTEMPT : handles
 PRICE_VERSION ||--o{ ATTEMPT : accounts_for
 ATTEMPT ||--|| RESERVATION : reserves
 DEPLOYMENT ||--o{ HEALTH_EVENT : produces
 EXPERIMENT_RUN ||--o{ EVALUATION_RECORD : contains
 MODEL ||--o{ EVALUATION_RECORD : scored_for
```

## From 3.6.6-user-interface.md

**Figure 3.9: Proposed operator dashboard wireframe.** This will be a layout source, not a rendered product screenshot.

```mermaid
flowchart TB
 H[AI Request Router: run ID / configuration version]
 H --> A[Summary: offered / completed / cost / p95 / violations]
 A --> B[Deployment health: model / endpoint / breaker / last observation]
 B --> C[Quality and calibration: policy / predicted vs observed]
 C --> D[Attempt log: request ID / reason / cost / latency / outcome]
 D --> E[Filters: run / model / fault type / date]
 E --> F[Export aggregate report / inspect safe details]
```

## From 3.9-evaluation-plan.md

**Figure 3.10: Experiment and evaluation pipeline.**

```mermaid
flowchart LR
 A[Licensed scored outputs] --> B[Deduplicate and group]
 B --> C[Training]
 B --> D[Validation and pilot]
 B --> E[Untouched test]
 C --> F[Predictors and permitted index]
 D --> G[Freeze policy, margin and configuration]
 F --> G
 G --> H[Baselines / hybrid / component ablations]
 E --> H
 H --> I[Paired quality, cost and calibration analysis]
 G --> J[Capped live pilot and local fault injection]
 J --> K[Latency, fallback and constraint analysis]
 I --> L[Report intervals and limitations]
 K --> L
```
