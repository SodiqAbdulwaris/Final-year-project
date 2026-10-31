Status: DRAFT
Depends on: D08; D12
Sources: Primary URLs in source table and proposal-audit section
Open items: Scoped numerical/final-version checks recorded below

# Q-DAPS: question difficulty from answer plausibility (Mozafari et al., 2026)

| Field | Value |
|---|---|
| Topic (home) | 02 Prompt difficulty prediction |
| Also relevant to | 07 Benchmarks and evaluation (difficulty labels from model agreement) |
| Paper type | method |
| Venue and status | peer-reviewed (ACL 2026 long paper, pp. 11124–11151) |
| Source read | full text (arXiv v1, https://arxiv.org/pdf/2605.12398); appendix tables not all read |
| Verified on | 2026-10-31, against ACL Anthology (2026.acl-long.510) and arXiv |
| Relevance to project | Low |

## APA 7 reference
Mozafari, J., Piryani, B., & Jatowt, A. (2026). Question difficulty estimation for large language models via answer plausibility scoring. In *Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)* (pp. 11124–11151). Association for Computational Linguistics. https://doi.org/10.18653/v1/2026.acl-long.510

## In-text citation forms
(Mozafari et al., 2026) · Mozafari et al. (2026)

## 1. What it is about
Q-DAPS scores how hard a factual question is for LLMs by asking a model to invent plausible wrong answers, rating how convincing each is, and taking the entropy of those ratings. If many wrong answers look about equally plausible, the question is hard. The score is checked against how many LLMs actually answer the question correctly.

## 2. The problem
Earlier difficulty estimates mostly came from the human reader's or the retrieval system's point of view: readability formulas, retrieval signals, popularity statistics. These do not reflect what makes a question hard for an LLM. The authors also point out that LLM-generated distractors are biased towards popular entities, which they say had not been studied for difficulty estimation.

## 3. Proposed solution
Three stages (Figure 2).

1. **Candidate generation.** An LLM (LLaMA 3.3 by default) produces up to N candidate wrong answers with a non-zero plausibility score up to 100 and a justification, in a single "listwise" prompt. A validation step checks for duplicates (semantic similarity), valid score range and exact count, raising temperature by 0.1 and retrying on failure.
2. **Popularity debiasing.** Each candidate's popularity is its monthly Wikipedia page-view count (2015–2024), normalised to [0, 1] after outlier removal. The plausibility score is reduced as Pl·(1 − α·Pop), with α searched on a grid. Candidates with no Wikipedia page get popularity zero.
3. **Scoring.** Scores are normalised into a distribution, the Shannon entropy is computed and divided by log2 N, giving a difficulty value in [0, 1].

The authors compare pointwise (one prompt per candidate), pairwise (Bradley–Terry over pairs) and listwise elicitation, and find listwise best and cheapest (one prompt, O(1) calls versus O(n) and O(n²)).

## 4. Data, models and tools
- Datasets: TriviaQA and Natural Questions (simple), MuSiQue and QASC (complex); 2,000 stratified questions from each.
- Ten LLMs in five size groups are used to define ground-truth difficulty: questions are grouped by how many of those LLMs answer correctly (checked with GPT-4 as judge), and the method is scored by correlation with that count (Spearman's ρ) and by Cohen's d.
- Baselines: readability (Flesch–Kincaid, Gunning–Fog), prompting an LLM to rate difficulty, popularity, retrieval-based signals and uncertainty-based methods.
- Code and data: https://github.com/DataScienceUIBK/Q-DAPS (stated in the paper; MIT license).

## 5. Key results
- Listwise setting (Table 1): Cohen's d from 0.91 (TriviaQA) to 1.43 (MuSiQue) and Spearman ρ from −0.61 (TriviaQA) to −0.96 (NQ) across the four datasets. A more negative ρ means more agreement with "more models succeed, so easier".
- Entropy of plausibility beats the average plausibility, and Q-DAPS beats all baselines; uncertainty-based methods come second, then retrieval-based, then prompt-based (Section 4.3).
- Ablations report that the method still works without the gold answer, without debiasing, and with smaller generators; two human-evaluation studies are reported as supporting it.
- Table 2 values differ from Table 1 and my text extraction of Table 2 was unreliable, so I quote only Table 1.

## 6. Limitations
Stated by the authors: best suited to question types with a compact candidate set (entity, date, number, boolean, label, multiple choice); English only; depends on LLM behaviour and biases.

Identified by me: it needs several LLM calls per question (candidate generation) plus a Wikipedia lookup, so it is a slow, post-hoc scorer rather than a pre-call classifier. The headline pipeline gives the generator the gold answer, so it cannot be applied to new user prompts without an answer. Only factoid and multiple-choice QA is covered; no coding, chat or reasoning prompts.

## 7. Relevance to the AI Request Router
- Mostly peripheral. It is not a per-request predictor and cannot run in the request path.
- Useful ideas to reuse offline: defining a prompt's difficulty label by the number of models that fail it (a label that needs no human annotation), and debiasing popularity when building difficulty labels.
- Could be used to label or audit a training set, then train the cheap embedding classifier on those labels.
- Not covered: cost, latency, load, open-ended prompts.

## 8. How to use it in the report
- Section 2.4, in the discussion of how difficulty labels are obtained (human, model-agreement, or generated-signal methods).
- Sentence: "Mozafari et al. (2026) define difficulty by the share of models that fail a question and score it from distractor plausibility, but their pipeline needs several LLM calls and the gold answer, so it cannot serve as an online router signal."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Mozafari et al. (2026) | LLM-oriented question difficulty for QA | Entropy of popularity-debiased plausibility scores of generated wrong answers | TriviaQA, NQ, MuSiQue, QASC; ten LLMs; LLaMA 3.3 generator | Listwise: ρ −0.61 to −0.96 with model-success count; beats readability, retrieval and prompt baselines | Multi-call, needs gold answer, factoid QA only, English |


## 2026-10-31 proposal audit

- Source attempted: https://arxiv.org/abs/2605.12398.
- Scope: Abstract/metadata check only in this session; detailed numerical results remain unchecked.
- Historical Source read above records the earlier session, not a claim of a fresh full reading.
- arXiv title matched: Question Difficulty Estimation for Large Language Models via Answer Plausibility Scoring. Latest listed version: v1; arXiv DOI identifies the preprint, not peer review. A missing journal reference does not prove that no published version exists.
