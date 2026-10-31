Status: DRAFT
Depends on: D01–D12; Chapter 3 protocol
Sources: _meta/hybrid-design.md; _meta/history/ch4-ch5-skeletons.md
Open items: See _meta/placeholders.md

# Appendix B: Dataset and Licence Register

Checked 31 October 2026. Public download access will not be treated as permission to redistribute every included component. No raw dataset will be distributed in this documentation change.

| Dataset | Primary source/version checked | Licence finding | Intended use | Redistribution status |
|---|---|---|---|---|
| RouterBench | [Repository](https://github.com/withmartian/routerbench/tree/cc67d1008bd8f3cf1e8040cc3ba4034d31b93c0c); [data card](https://huggingface.co/datasets/withmartian/routerbench) | Code LICENSE is MIT; card did not establish blanket data terms. | Candidate scored-output replay/training, after data/component terms checked. | Raw data not cleared; preserve code notices and resolve component terms. |
| LLMRouterBench | [Repository](https://github.com/ynulihao/LLMRouterBench/tree/0b81ba3053fbb74828382690a883849e2443e2d8); [data release](https://huggingface.co/datasets/NPULH/LLMRouterBench) | README MIT badge; LICENSE endpoint returned 404; no dataset card on inspected release. | Candidate scored-output reuse and model coverage. | Unresolved; badge alone insufficient. |
| LongMemEval | [Repository licence](https://github.com/xiaowu0162/LongMemEval/blob/9e0b455f4ef0e2ab8f2e582289761153549043fc/LICENSE) | MIT repository licence confirmed; retain copyright and permission notice. | Scope reference only while context studies unresolved. | Confirm packaged data/third-party terms before sharing; no core data use assumed. |

## Model and task alignment gate

| Slot | Required role | Frozen identity | Coverage evidence | Remaining gate |
|---|---|---|---|---|
| Small/cheap | Prefer local RTX 4070 execution. | [PLACEHOLDER: model names] | Qwen3-8B appears in official LLMRouterBench lightweight pool. | Shared scored request IDs, exact revision, fit and quantisation equivalence. |
| Mid-tier | Affordable hosted candidate. | [PLACEHOLDER: model names] | Gemini-2.5-flash appears in official performance–cost pool. | Shared tasks/labels with selected local/frontier model; API availability. |
| Frontier | Strong single-model reference candidate. | [PLACEHOLDER: model names] | GPT-5-medium appears in official performance–cost pool. | Version availability and aligned outcomes; reference chosen on validation only. |
| Optional fourth | Add only for justified diversity. | [PLACEHOLDER: optional fourth model] | TODO: coverage evidence. | Incremental value and budget. |

Recommendations do not freeze the model identities. Listing in separate pools will not establish aligned outcomes. The team will not replace missing per-request outcomes with unrelated published aggregate scores.

## Artifact manifest to complete

| Dataset/artifact | Revision/hash | Component/source terms | Permitted purpose | Notice obligations | Redistribution decision | Reviewer/date |
|---|---|---|---|---|---|---|

TODO: inspect the downloaded archives, verify exact licence texts and upstream components, record provider-output conditions and freeze the permitted subset. If terms remain unclear, obtain authoritative clarification before reuse/redistribution or use a permitted alternative.
