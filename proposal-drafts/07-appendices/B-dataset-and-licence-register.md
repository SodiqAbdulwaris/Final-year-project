Status: DRAFT
Depends on: D01–D12; Chapter 3 protocol
Sources: _meta/hybrid-design.md; _meta/history/ch4-ch5-skeletons.md
Open items: See _meta/placeholders.md

# Appendix B: Dataset and Licence Register

Checked 31 October 2026. Public download access will not be treated as permission to redistribute every included component. No raw dataset will be distributed in this documentation change.

| Dataset | Primary source/version checked | Licence finding | Intended use | Redistribution status |
|---|---|---|---|---|
| RouterBench | [Repository](https://github.com/withmartian/routerbench/tree/cc67d1008bd8f3cf1e8040cc3ba4034d31b93c0c); [data card](https://huggingface.co/datasets/withmartian/routerbench) | Code LICENSE is MIT; card did not establish blanket data terms. | Candidate scored-output replay/training, after data/component terms checked. | Raw data not cleared; preserve code notices and resolve component terms. |
| LLMRouterBench | [Repository](https://github.com/ynulihao/LLMRouterBench/tree/0b81ba3053fbb74828382690a883849e2443e2d8); [data release](https://huggingface.co/datasets/NPULH/LLMRouterBench) | README MIT badge. Checked 3 November 2026 in Chrome: the Hugging Face dataset repo contains a `LICENSE` file, MIT, "Copyright (c) 2025-2026 LLMRouterBench contributors", covering the repository files. No dataset card. The MIT text does not state terms for the underlying benchmark datasets or third-party model outputs. | Candidate scored-output reuse and model coverage. | Repository-level MIT confirmed; component dataset and model-output terms (e.g. benchmark sources, proprietary model outputs) still unchecked; keep raw data unredistributed until they are. |
| LongMemEval | [Repository licence](https://github.com/xiaowu0162/LongMemEval/blob/9e0b455f4ef0e2ab8f2e582289761153549043fc/LICENSE) | MIT repository licence confirmed; retain copyright and permission notice. | Scope reference only while context studies unresolved. | Confirm packaged data/third-party terms before sharing; no core data use assumed. |

## Model and task alignment gate

| Slot | Required role | Frozen identity | Coverage evidence | Remaining gate |
|---|---|---|---|---|
| Small/cheap | Prefer local RTX 4070 execution. | Qwen3-8B (recommended, not yet owner-confirmed) | Qwen3-8B appears in the lightweight pool; prompts align with Gemini-2.5-flash and `gpt-5` on GPQA, LiveCodeBench, MMLU-Pro (archive checked 3 November 2026). | Exact revision, local fit and quantisation equivalence, cost basis. |
| Mid-tier | Affordable hosted candidate. | Gemini-2.5-flash (recommended, not yet owner-confirmed) | Appears in the performance–cost pool; aligned with Qwen3-8B and `gpt-5` on the three datasets above. | Current API availability and price; revision behind the folder. |
| Frontier | Strong single-model reference candidate. | `gpt-5` (owner-approved 3 November 2026, replacing GPT-5-medium) | `gpt-5` records in the LLMRouterBench archive align with Qwen3-8B and Gemini-2.5-flash on GPQA, LiveCodeBench and MMLU-Pro; GPT-5-medium has only SWE-Bench results. | Confirm the reasoning setting and revision behind the `gpt-5` folder, current API availability and price; reference chosen on validation only. |
| Optional fourth | Add only for justified diversity. | [PLACEHOLDER: optional fourth model] | TODO: coverage evidence. | Incremental value and budget. |

### Archive inspection, 3 November 2026

Source: `bench-release.tar.gz` (1,283,503,080 bytes) from the Hugging Face dataset `NPULH/LLMRouterBench`, downloaded to a scratch folder outside the repo; 700 JSON result files, 40 model folders. Checked by script (not by hand):

| Finding | Evidence |
|---|---|
| Qwen3-8B and Gemini-2.5-flash are aligned on three datasets | GPQA: 198 prompts, identical indices and text. LiveCodeBench: 1,055, identical. MMLU-Pro `test_1000`: 1,001 records each, 998 identical prompt texts (3 differ), same indices. AIME (`hybrid`) and LiveMathBench also have files for both (not compared). |
| Mean scores on aligned prompts (single run, one score per prompt) | GPQA: Qwen3-8B 0.576, Gemini-2.5-flash 0.662. LiveCodeBench: Qwen3-8B 0.677, Gemini-2.5-flash 0.600. MMLU-Pro (998 shared): 0.693 vs 0.796. The small model beats the mid-tier model on LiveCodeBench, so a router has something to gain there. |
| Per-record cost is stored | Example records: GPQA cost 0.00049 (Qwen3-8B) vs 0.00227 (Gemini-2.5-flash). How Qwen3-8B cost was derived (API price vs local) is not yet checked. |
| **GPT-5-medium is not aligned** | The only GPT-5-medium file in the archive is SWE-Bench verified, which Qwen3-8B has no results for. It has no GPQA, LiveCodeBench, AIME or MMLU-Pro results here, despite the README listing it in the performance-cost pool. |
| Closest frontier substitutes on the same datasets | `gpt-5-chat` (AIME, GPQA, HumanEval, LiveCodeBench, LiveMathBench, MMLU-Pro) and `gpt-5` (five of those); also Gemini-2.5-pro, Claude-sonnet-4, Qwen3-235B and others with five-dataset overlap. Alignment of these with Qwen3-8B was not compared in detail. |

Consequence: a Qwen3-8B / Gemini-2.5-flash / frontier pool is feasible on GPQA, LiveCodeBench and MMLU-Pro only if the frontier model is changed (for example `gpt-5-chat` or `gpt-5`) or scored by the team; GPT-5-medium cannot be used from this release. The owner must choose (decision D05 reopened for the frontier slot). Not checked: exact model revisions behind each folder name, whether `gpt-5` means a particular reasoning setting, quantised-local equivalence, and whether Qwen3-8B cost reflects local or API pricing.

### Frontier substitute comparison, 3 November 2026

Same archive, same method (prompt text matched against Qwen3-8B and Gemini-2.5-flash records; one score per prompt; cost is the per-record cost field, averaged). All four candidates have complete aligned coverage (GPQA 198, LiveCodeBench 1,055, MMLU-Pro 1,001 records).

| Candidate | GPQA score / cost | LiveCodeBench score / cost | MMLU-Pro score / cost |
|---|---|---|---|
| Qwen3-8B (small) | 0.576 / 0.0011 | 0.677 / 0.0018 | 0.692 / 0.0005 |
| Gemini-2.5-flash (mid) | 0.662 / 0.0134 | 0.600 / 0.0058 | 0.796 / 0.0041 |
| `gpt-5-chat` | 0.737 / 0.0094 | 0.622 / 0.0038 | 0.788 / 0.0045 |
| **`gpt-5`** | **0.848 / 0.0401** | **0.864 / 0.0521** | **0.857 / 0.0133** |
| `claude-sonnet-4` | 0.687 / 0.0134 | 0.581 / 0.0135 | 0.815 / 0.0077 |
| `gemini-2.5-pro` | 0.848 / 0.0838 | 0.791 / 0.1352 | 0.839 / 0.0392 |

Reading: `gpt-5-chat` is not a real frontier reference here (it scores below Gemini-2.5-flash on LiveCodeBench and MMLU-Pro) and `claude-sonnet-4` is not clearly better than the mid-tier model. `gpt-5` is best or tied-best on all three datasets with a large cost gap over the mid-tier model, which gives a router real cost-quality range. `gemini-2.5-pro` ties on GPQA but costs about two to three times as much and shares a provider with the mid-tier model.

Supervisor recommendation (not frozen): small = Qwen3-8B, mid = Gemini-2.5-flash, frontier = **`gpt-5`**, restricted to GPQA, LiveCodeBench and MMLU-Pro (plus AIME and LiveMathBench after alignment is checked). Caveats: what reasoning setting the `gpt-5` folder used and whether it is the same as the README's "GPT-5-medium" is not stated in the files read; costs are the benchmark's recorded costs at collection time, not today's prices; Qwen3-8B's cost basis is unchecked; scores are one run per prompt.

Recommendations do not freeze the model identities. Listing in separate pools will not establish aligned outcomes. The team will not replace missing per-request outcomes with unrelated published aggregate scores.

## Artifact manifest to complete

| Dataset/artifact | Revision/hash | Component/source terms | Permitted purpose | Notice obligations | Redistribution decision | Reviewer/date |
|---|---|---|---|---|---|---|

TODO: inspect the downloaded archives, verify exact licence texts and upstream components, record provider-output conditions and freeze the permitted subset. If terms remain unclear, obtain authoritative clarification before reuse/redistribution or use a permitted alternative.
