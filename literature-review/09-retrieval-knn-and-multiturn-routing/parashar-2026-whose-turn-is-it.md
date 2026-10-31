# Whose turn is it? Session-aware routing and the cost of switching (Parashar et al., 2026)

| Field | Value |
|---|---|
| Topic (home) | 09 Retrieval, k-NN and multi-turn routing (session routing and switching cost) |
| Also relevant to | 04 Cost reduction, 03 Load balancing (prefix-cache effects) |
| Paper type | empirical study with a cost model |
| Venue and status | preprint only (arXiv v1, 13 Oct 2026, marked "Preprint", Microsoft authors); no peer-reviewed venue found |
| Source read | full text (https://arxiv.org/pdf/2610.19292v1) |
| Verified on | 2026-10-31, against the arXiv abstract page and PDF |
| Relevance to project | High |

## APA 7 reference
Parashar, A., Dutta, A., Chauhan, V., Gulwani, S., Gupta, P., Hasanbeig, H., Le, V., Tiwari, A., & Williams, J. (2026). *Whose turn is it? Context-guided model routing for stateful agents* (arXiv:2610.19292). arXiv. https://doi.org/10.48550/arXiv.2610.19292

## In-text citation forms
(Parashar et al., 2026) · Parashar et al. (2026)

## 1. What it is about
The paper studies routing between a cheap and an expensive model across the turns of a multi-turn agent session. It compares decision rules and adds a closed-form analysis of how switching models forfeits the provider's prompt cache.

## 2. The problem
Routers usually treat requests as independent. In a stateful session a turn's difficulty depends on earlier turns, earlier model choices shape later ones, and each switch makes the new model re-read the conversation as uncached input. The authors want zero-shot, cost-aware policies that need no routing labels, and a clear view of switching costs.

## 3. Proposed solution
- **Setting.** Two candidates per session, a cheap and an expensive model (pairs differ in size, reasoning effort or provider; names are pseudonyms). A router sees the current request, optionally with the serialised history (requests, responses, tool calls, errors, prior routing decisions).
- **Policies (Table 1).** (1) LLM router: a prompted small LLM acts as a zero-shot binary classifier once per user turn. (2) The same router without history. (3) Escalation: start on the cheap model and let it hand over. (4) De-escalation: the reverse. (5) Random routing. Models share state only through serialised text, never KV tensors.
- **Cost accounting.** Total cost includes router overhead and cache effects; the fixed-model baseline gets the most cache-favourable treatment, so the comparison is conservative for routed policies.
- **Break-even analysis.** After a downward switch the first call on the cheap model pays for L context tokens at the uncached price, and later calls read from its own cache. The switch repays itself after k = (cheap model's uncached input price − expensive model's cached price) / (expensive model's cached price − cheap model's cached price) (Eq. 3), independent of the context length L. An upward switch costs L × (expensive uncached price − cheap cached price).

## 4. Data, models and tools
- Multi-turn spreadsheet tasks: SheetCopilot (112 multi-subtask tasks, 2.88 turns on average, maximum 7) and SpreadsheetBench 2 (221 workflows, 4.76 turns on average, maximum 6), built by splitting single-turn tasks into sequential turns.
- Metric: end-to-end pass rate of the final workbook and cost per task including router overhead and cache effects; compared on the quality–cost plane.
- Three candidate pairs; only the Opus high/low pair has exact routed costs.

## 5. Key results
- History matters: at nearly the same share of turns sent to the cheap model (23.3% without history, 22.7% with), the history-aware router passes 28.3% of tasks versus 25.0% without history, a 3.3-point gain that holds for every pair (5.4 points for one pair, 2.7 for another).
- On SheetCopilot the history-aware router stays within 0.9 points of expensive-only, routing 21.1–24.2% of turns to the cheap model; on SpreadsheetBench 2 it uses the cheap model on only 0.4–1.7% of turns and matches expensive-only at 29.3%.
- No clear saving for the one pair with exact costs: $0.369 versus $0.365 per task (SheetCopilot) and $2.080 versus $2.009 (SpreadsheetBench 2). Escalation, de-escalation and random switching do not preserve quality. The cheap model's per-task cost advantage narrows from 6.8× to 3.2× in longer sessions.
- Cache analysis (Section 4.4): a downward switch breaks even after about 1.25 calls on the cheap model; an upward switch does not break even on input cost and costs about $4.9 per million tokens of context versus about $0.5 downward. At 75K tokens one upward switch costs about as much as a whole SheetCopilot task on the expensive model.
- Stated design principle: switch sticky and context-length aware, down early and stay, up only when the quality gain outweighs a cost that grows with the session.

## 6. Limitations
Stated by the authors: only zero-shot, cost-aware policies are studied (learned routers and quality-oriented methods are complementary); sessions average nearly three turns with at most seven, so longer trajectories, independent tasks and cross-sheet interactions are future work; decomposing annotated subtasks into turns only approximates natural interaction.

Identified by me: one domain (spreadsheet agents), two-model pools, cost accounting that depends on cache pricing and an assumed cache-hit pattern, no intervals in the passages I read; preprint.

## 7. Relevance to the AI Request Router
- Strongest direct support for the guide's session-aware hysteresis (RQ2): a first-order switch-cost formula, the asymmetry (down early is cheap, up late is expensive), and evidence that history improves decisions at equal offload.
- Reuse: the break-even formula with the project's own prices; total cost including router overhead and cache loss; the policies to compare (per-turn router with and without history, escalation, de-escalation, random); pass rate versus cost at the same offload share.
- What the project must decide: the hysteresis threshold (how much better the new model must be, for how many turns), which switch direction is free, and hard-failure exceptions. Local servers (Ollama, vLLM) have their own prefix-cache behaviour that the project must measure.
- Not covered: k-NN competence estimates, calibration, budgets, pools beyond two models.
- Related: [MTRouter](zhang-2026-mtrouter.md) notes the same cache loss without measuring it; [Preble](../03-load-balancing/srivatsa-2025-preble.md) concerns prefix sharing on the serving side.

## 8. How to use it in the report
- Chapter 2 on multi-turn routing and Chapter 3 on the hysteresis rule and the switching-cost model.
- Sentence: "Parashar et al. (2026) show that session history improves pass rate at equal offload and that a downward switch repays its cache cost within about one turn whereas a late upward switch does not, which motivates sticky switching."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Parashar et al. (2026) | Cost-aware routing across turns of a stateful agent session | Zero-shot per-turn LLM router with or without history; escalation, de-escalation, random; closed-form cache break-even | SheetCopilot (112 tasks) and SpreadsheetBench 2 (221 workflows); three cheap/expensive pairs | History adds 3.3 points at equal offload; downward switch repays in about 1.25 calls; upward switch does not | One domain, two models, short sessions, cache pricing assumptions, preprint |
