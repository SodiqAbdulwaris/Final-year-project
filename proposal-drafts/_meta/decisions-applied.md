Status: DRAFT
Depends on: D01–D12
Sources: _meta/hybrid-design.md; owner instructions of 31 October 2026
Open items: See placeholders.md

# Decisions applied: 31 October 2026

The owner's current task will govern all active drafts. Earlier recommendations in decisions/D01–D12 and archived chapters are historical, not unanswered questions to re-ask. Supervisor acceptance of the final title and administrative submission remains unconfirmed.

| Decision | Applied outcome | Sections affected |
|---|---|---|
| D01 | Hybrid predictor, constrained selector and reliability controller; embeddings tested by ablation. | 1.3, 1.7, 3.4–3.9 |
| D02 | Personal/administrative fields remain exact bracketed placeholders; template HOD and Dean names retained as supplied. | Front matter |
| D03 | No invented numeric targets. Quality non-inferiority margin, cost and latency reductions remain provisional after pilot, frozen before testing. | 1.3, 3.5, 3.9, Appendix F |
| D04 | Owner's evaluation-focused gap wording used verbatim. No first/novel-algorithm claim. | 1.2, 2.7 |
| D05 | Three to four models: cheap/small, mid-tier and frontier, restricted to benchmark-covered candidates. | 1.7, 3.7, Appendix B |
| D06 | Two RTX 4070 laptops (Lenovo Legion 7i, ASUS ROG Zephyrus G16); scored-output reuse, capped hosted pilot, local failure tests. | 1.8, 3.8, Table 4.1 |
| D07 | No formal ethics approval; basic research ethics; human involvement minimal or none. This records the owner's stated approval position, not an independently obtained exemption. | 3.2, 3.10, Appendix C |
| D08 | Keep preprints/2026 works, label status, prefer established peer-reviewed version. | Chapter 2, references |
| D09 | Full AI declaration and log; team will read key sources directly. Exact past model versions remain unknown. | Front matter 06, Appendix E, style guide |
| D10 | No Scopus manuscript now; prior outline archived only. | _meta/history/manuscript-outline.md |
| D11 | Check code/data terms separately before reuse or redistribution; no datasets redistributed in this change. | 3.7, Appendix B |
| D12 | Bibliography and scoped source checks performed before Chapter 2 drafting; remaining gaps labelled. | Literature records, L03/L07, Chapter 2 |

## Model recommendation and coverage evidence

Recommendation: first test an LLMRouterBench candidate pool using **Qwen3-8B** as the small local candidate, **Gemini-2.5-flash** as a mid-tier candidate and **GPT-5-medium** as a frontier candidate; consider a fourth only if aligned records and the budget justify it. These are recommendations, not frozen experimental identities. Active model slots will remain [PLACEHOLDER: model names].

Evidence: the [official README](https://github.com/ynulihao/LLMRouterBench/blob/0b81ba3053fbb74828382690a883849e2443e2d8/README.md), checked 31 October 2026, lists Qwen3-8B in the lightweight performance pool and Gemini-2.5-flash / GPT-5-medium in the performance–cost pool. Its configuration separates these pools and task sets. That proves listed coverage, not shared prompts or complete scored-output availability across the proposed three models. The downloaded result archive has not been inspected. Before freezing names, check exact revisions, aligned request IDs, shared scoring and deployment availability. Do not join unrelated scores by benchmark name alone.

Local feasibility will require measured VRAM and a tested model/quantisation/context configuration. The shared RTX 4070 branding of the two laptops does not establish equal capacity. A quantised local deployment will not inherit full-precision benchmark quality labels without qualification. If no aligned mixed pool is usable, document the feasibility conflict rather than silently breaking D05 or commissioning an uncapped new evaluation.

## D11 findings and redistribution gate

| Dataset | Evidence checked on 31 October 2026 | Finding and permitted next step |
|---|---|---|
| RouterBench | [code MIT licence](https://github.com/withmartian/routerbench/blob/cc67d1008bd8f3cf1e8040cc3ba4034d31b93c0c/LICENSE); [data card](https://huggingface.co/datasets/withmartian/routerbench) | Code is MIT with notice obligations. Data card describes scored outputs but did not establish a blanket data redistribution licence. Check component datasets and generated-output terms; do not redistribute raw data yet. |
| LLMRouterBench | [README](https://github.com/ynulihao/LLMRouterBench/blob/0b81ba3053fbb74828382690a883849e2443e2d8/README.md); [data release](https://huggingface.co/datasets/NPULH/LLMRouterBench) | README has MIT badge, but repository LICENSE endpoint/API returned 404 and data release had no card. Badge alone will not clear code/data redistribution. Seek authoritative terms and component licences before use/distribution. |
| LongMemEval | [MIT licence](https://github.com/xiaowu0162/LongMemEval/blob/9e0b455f4ef0e2ab8f2e582289761153549043fc/LICENSE) | MIT repository licence confirmed; retain notices. Check downloaded data packaging and third-party material before sharing. Not core: context/memory scope remains unresolved. |

Appendix B will be the operational register. Licence checks do not imply that data have been downloaded or experiments run.

## Reconciliation and author choices

The old gateway/adapters, deterministic validation, budget accounting, logging and fault tests will be retained and revised. The learned classifier will become core; the previous k-NN-only predictor and mandatory hysteresis/context studies will not govern. Live GPU/queue telemetry, Redis/Prometheus, session hysteresis, router-managed context and graph memory will remain **unresolved earlier proposals**. Their acceptance or rejection will not be inferred.

The drafter selected five aligned objectives, iterative development with controlled experiments, a provisional modular application/relational schema and document-based requirements elicitation. These keep the design testable with limited funding and no mandatory human study; they do not select the unresolved estimator or split protocol. A relational schema is a design proposal, not an implemented database.

The requested Word template was unavailable in this checkout; the supplied structure was used. Original DOCX and excluded folders were not edited. The original dirty main checkout was preserved on codex/preserved-main-work; this worktree will hold main. No PR will be opened.

## Verification limits

Fresh metadata retrieval was attempted for all 90 paper files. Twenty full-text samples cover all nine topics; additional Chapter 2 sources will be used only for claims checked at abstract/metadata level. Full-document reading and every historical numerical claim have not been verified. L03/L07 record per-source scope and access failures. Mermaid source will be syntax-checked where tooling permits; Word layout and image rendering remain separate tasks.

## Final documentation checks

The package contains 86 Markdown files including eight archived drafts. The active Chapter 2 discusses 45 works and the bibliography contains those 45 cited entries. The abstract is 268 words with five alphabetically ordered keywords. Ten Mermaid sources parsed successfully with Mermaid 11.14.0; no images were rendered. The exact 86-file tree, required headers, active local links, citation closure, abstract length, marker catalogue and whitespace were checked. No router implementation or experiment was performed. Word page counts, formal approval wording, personal source reading and remaining metadata/licence gates are not verified.

## Synchronisation with the Word draft (4 November 2026)

The Word file `proposal frags/Proposal_Working_Draft_v2.docx` now leads. These repository files were regenerated from it:

- Front matter 01 to 07 and 09, and the abstract (296 words), with the title *Design and Implementation of a Prompt-Aware Large Language Model Request Routing System*, six members, session 2026/2027, free access.
- Chapter 1 (1.1 to 1.11): six objectives and six research questions (the earlier five are replaced); the Nigerian exchange-rate sentence rests on African Development Bank (2026); the two laptops are named in 1.8.
- Chapter 2: 33 studies in eight themes (the 45-study register is historical); Table 2.1 states that screening counts were not recorded; the comparison covers OpenRouter, LiteLLM and Portkey only (TrueFoundry and Not Diamond are dropped); the 2.4 theme files were renamed to match.
- Chapter 3: restructured to Sections 3.1 to 3.15 following the Module 3 slides (the former 3.11 summary is now 3.15; new 3.11 risks, 3.12 work plan, 3.13 budget, 3.14 expected outcomes, 3.6.8 traceability). Numeric targets are adopted (NFR-01 to NFR-10); Scrum with two-week sprints; sprint owners follow Tasks.md.
- References: the list in 06-references.md is the Word list (45 entries, Peffers et al. 2007 added).
- Figures: Codex-generated PNGs replace the Mermaid sources, which are archived.

**Decisions that differ from earlier records:** the numeric targets are fixed in Chapter 3 (previously provisional until a pilot); a revision is allowed only with a recorded reason before the test results are inspected. The lecturer’s slides ask for ethics approval and consent; the repository decision (no formal ethical approval, no human participants) is kept and still has to be confirmed with the supervisor.

**Not yet verified:** Peffers et al. (2007) DOI; descriptions in Table 2.3 that were not checked against the full text; the budget amounts and the assumed exchange rate (₦1,500 per US$); per-laptop specifications; model names.
