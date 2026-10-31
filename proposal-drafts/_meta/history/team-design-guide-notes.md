Status: DRAFT
Depends on: Superseded earlier design
Sources: Original draft preserved by git mv
Open items: Archived historical text; excluded from assembly and active placeholder register

# Notes on "LLM Router FYP: Architecture, Research Decisions and Experiment Guide" (Rev 2, 26 Oct 2026)

Source: `Research Review/Research Paper Review.docx` (team document, later than the 16 Oct proposal). This file records what it says and where it differs from `AI_Request_Router_Proposal.docx`. **Status of the conflict: DECISION-NEEDED (user/team/supervisor).** Until decided, the drafts treat the newer 26 Oct guide as the governing design and keep the proposal's elements that it does not contradict.

## 1. Key decisions in the guide
| Topic | Guide's decision |
|---|---|
| Framing | A budget-constrained, load/budget-aware gateway for hosted **and local** LLMs. Contribution = architectural integration + controlled evaluation, not a new routing invention. Negative results are valid. |
| Candidate models | 3–4 differentiated models/deployments |
| Selection | Hard eligibility filters (capabilities, context fit, health, privacy, affordability) → competence estimate → cheapest/lowest-latency option whose success **lower bound** meets a quality target. Never silently violate a guaranteed threshold. |
| Competence estimate | **k-NN over past per-model outcomes** (embeddings of scored tasks); validated and, only if needed, recalibrated (isotonic/Platt; reliability table, Brier score); minimum-evidence rule; unknown ≠ good |
| Learned difficulty classifier | Optional comparator, **not an MVP dependency** (difficulty ≠ model-specific success) |
| Budget | Three policy bands (Economy / Balanced / Quality) + request/session/project caps; atomic reservation; reconcile with provider usage |
| Switching | Session-aware **hysteresis**; hard-failure/capability exceptions |
| Context | Client owns context by default; optional router-managed sessions; no silent rewriting |
| Graph memory | Deferred from MVP; optional experiment (E3), manual vs automatic graph |
| Architecture | One modular FastAPI app + relational DB; no microservices, graph DB or Redis until measured need |
| Local models | First-class via OpenAI-compatible APIs (Ollama, LM Studio, llama.cpp, vLLM) |
| Evaluation | Five experiments E1–E5 (below), paired intervals, non-inferiority margin declared up front |
| SE evaluation | Requirements (≥5 developer interviews), MoSCoW + traceability matrix, ISO/IEC 25010 quality table, testing (≥80% line coverage, concurrency, fault injection), usability (SUS, ≥8 participants) |
| Out of scope | Training models, KV-cache transfer across models, distributed GPU scheduling, online RL/bandits, agent framework, LLM-built graphs on every live request |

## 2. Research questions in the guide
- **RQ1** Does k-NN competence estimation beat simple rules on cost–quality at the same budget? (E1; data: RouterBench, LLMRouterBench)
- **RQ2** Does controlled session switching cut cost/latency without material quality loss? (E2)
- **RQ3** How much conversation history is needed after switching; does optional graph retrieval beat bounded/text retrieval? (E3)
- Software-engineering verification: **E4** budget correctness under concurrency/failures; **E5** local backend and gateway overhead, fault injection (slow response, 429, connection failure, malformed output, mid-stream disconnect).
- Evaluation rules: declare primary metric and margin first; separate validation/test; pair comparisons; 95% intervals; separate meaningful / small / inconclusive findings; confirmatory tests limited to H1–H3.
- A synthetic simulation (`llm_router_synthetic_sim.py`) found k-NN 80.5% vs rules 81.7% (invented probabilities). Not evidence.

## 3. Differences from the 16 Oct proposal
| Item | 16 Oct proposal | 26 Oct guide |
|---|---|---|
| Quality prediction | sentence-transformers + logistic regression difficulty/task classifier | k-NN past-performance retrieval; classifier optional |
| Live load | Core feature: queue length, GPU use, tokens/s via vLLM + Prometheus | Health/latency/queue **estimates** in registry; vLLM `/metrics` only when exposed; no Prometheus/Redis in MVP |
| Failover | Retry on next-best + circuit breaker, Redis health state | Bounded retries and circuit breaker tested in E4/E5; no Redis until needed |
| Budget | Per-request latency budget | Cost budget bands/caps (cost-oriented), TTFT measured |
| Novel parts | Live-load-aware routing | Controlled switching (hysteresis), context policy, budget enforcement |
| Benchmarks | RouterBench, MT-Bench | RouterBench, LLMRouterBench (+ LongMemEval for E3) |
| Phases | 3 phases | 9-step build order |

## 4. Literature the guide cites (and review status)
- Varangot-Reille, Bouvard & Gourru (2026), *Generalising LLM Routing using Past Performance Retrieval*, EACL 2026 SRW, DOI 10.18653/v1/2026.eacl-srw.22. **Different paper from the JAIR survey** already in topic 01. New: topic 09.
- Zhang et al. (2026) MTRouter, ACL 2026 long; Tang et al. (2026) VDAR-Router (arXiv 2607.18098): new, topic 09.
- Wu et al. (2025) LongMemEval (ICLR 2025); Rasmussen et al. (2025) Zep (arXiv 2501.13956): new, topic 10.
- Already in the review: Hybrid LLM, RouteLLM, RouterBench (venue per guide: ICML 2024 Agentic Markets Workshop), LLMRouterBench (venue per guide: **Findings of ACL 2026**, DOI 10.18653/v1/2026.findings-acl.1881, unconfirmed).
- The guide itself says its relevance/limitation summaries were not re-read against full texts; the review files do that.
- It corrects an earlier Gemini review: the EACL paper and VDAR-Router are separate works.

## 5. Effect on the literature review
- Two new topics: **09** past-performance retrieval, k-NN routing, multi-turn and session routing; **10** conversation memory and context management (incl. graph memory).
- Gap statement now has two tracks (see `literature-review/gaps-and-synthesis.md` once updated): the live-load track (proposal) and the retrieval + switching + budget track (guide).
