# Project context

**AI Request Router.** Nile University of Nigeria, Department of Software Engineering (draft of 16 October 2026; team and supervisor to be confirmed).

A gateway that scores each request for difficulty, weighs predicted quality, cost and the live load on every backend, and routes it to the best model (hosted or self-hosted) with failover. One OpenAI-compatible endpoint.

| Proposal feature | Planned build | Topics that inform it |
|---|---|---|
| Difficulty and task scoring | sentence-transformers + scikit-learn logistic regression | 02, 01 |
| Live-load awareness | vLLM metrics via Prometheus | 03, 05 |
| One endpoint, hosted + self-hosted | FastAPI, vLLM, Ollama | 08, competitors |
| Quality–cost–latency score + latency budget | custom Python scoring | 01, 04, 05 |
| Failover | Redis health state + circuit breaker | 06 |
| Benchmarking | RouterBench, MT-Bench, Grafana | 07 |

Out of scope: training language models.

## Questions each topic must help answer

| # | Topic | Question for the project |
|---|---|---|
| 01 | Routing algorithms | What routing methods exist, what do they need as input, and how do they generalise? |
| 02 | Prompt difficulty | Can difficulty be predicted cheaply and reliably before the call? |
| 03 | Load balancing | Which live signals matter and how stale/accurate can they be? |
| 04 | Cost reduction | How is cost modelled and what savings are credible? |
| 05 | Latency and speed | How is latency defined and measured (TTFT, TPOT, p95), and how can a budget be predicted? |
| 06 | Fallback | How should failover, retries and circuit breakers work for LLM calls? |
| 07 | Benchmarking | How do we evaluate a router fairly, and what do public benchmarks miss? |
| 08 | Gateway design | What reference architectures exist for a gateway in front of mixed backends? |

Gap claims from the proposal and how the literature changes them are in [gaps-and-synthesis.md](gaps-and-synthesis.md).
