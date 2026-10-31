# Judging LLM-as-a-judge with MT-Bench and Chatbot Arena (Zheng et al., 2023)

| Field | Value |
|---|---|
| Topic (home) | 07 Testing and benchmarking |
| Also relevant to | 01 Routing algorithms (MT-Bench is a RouterBench dataset) |
| Paper type | benchmark / empirical study |
| Venue and status | peer-reviewed (NeurIPS 2023, Datasets and Benchmarks Track) |
| Source read | full text (arXiv v4, https://arxiv.org/pdf/2306.05685v4) |
| Verified on | 2026-10-31, against the NeurIPS proceedings page and arXiv (comments field) |
| Relevance to project | High |

## APA 7 reference
Zheng, L., Chiang, W.-L., Sheng, Y., Zhuang, S., Wu, Z., Zhuang, Y., Lin, Z., Li, Z., Li, D., Xing, E. P., Zhang, H., Gonzalez, J. E., & Stoica, I. (2023). Judging LLM-as-a-judge with MT-Bench and Chatbot Arena. *Advances in Neural Information Processing Systems, 36*. https://proceedings.neurips.cc/paper_files/paper/2023/hash/91f18a1287b398d378ef22505bf41832-Abstract-Datasets_and_Benchmarks.html

(Page numbers were not confirmed, so none are given. arXiv DOI: https://doi.org/10.48550/arXiv.2306.05685.)

## In-text citation forms
(Zheng et al., 2023) · Zheng et al. (2023)

## 1. What it is about
The paper tests whether a strong LLM (such as GPT-4) can stand in for human judges when comparing chat assistants. It introduces MT-Bench, 80 hand-written multi-turn questions, and uses Chatbot Arena votes from the public to check how well LLM judgments match human preferences, and documents the judge's biases.

## 2. The problem
Standard benchmarks such as MMLU or HELM score closed-ended, short answers and do not separate aligned chat models from their base models, even though users prefer the aligned ones. Human preference evaluation is more faithful but slow and expensive. The authors ask whether LLM judges can approximate it, and where they fail.

## 3. Proposed solution
**MT-Bench.** 80 questions, ten in each of eight categories (writing, roleplay, extraction, reasoning, math, coding, STEM knowledge, humanities knowledge), each with a follow-up turn. Six models answered (GPT-4, GPT-3.5, Claude-v1, Vicuna-13B, Alpaca-13B, LLaMA-13B). 58 expert labelers (mostly graduate students) gave about 3K pairwise votes.

**Chatbot Arena.** Users chat with two anonymous models and vote for the better one; after a month it gathered about 30K votes. The paper samples 3K single-turn votes from 2,114 unique IPs.

**Judge modes.** Pairwise comparison, single-answer grading (a score per answer) and reference-guided grading. Mitigations: swap answer positions, few-shot examples, chain-of-thought prompting, and a reference answer for math.

**Agreement metric.** The probability that two randomly selected judges (one of each kind, not identical) agree on a random question, with or without ties.

## 4. Data, models and tools
- MT-Bench questions, 3K expert votes and 30K Arena conversations with human preferences are released through FastChat (github.com/lm-sys/FastChat, llm_judge).
- Judges: GPT-4, GPT-3.5 and Claude-v1.
- The paper also evaluates LLaMA and Vicuna variants to show that its benchmarks and traditional ones are complementary.

## 5. Key results
- GPT-4 agrees with human experts 85% of the time on MT-Bench under the non-tie setting, higher than the 81% agreement among humans (Table 5). Humans judged GPT-4's disagreeing judgments reasonable in 75% of cases and changed their own choice in 34%.
- Arena data shows a similar pattern (Table 6). The paper reports "over 80% agreement" overall.
- Agreement between GPT-4 and humans rises from about 70% to nearly 100% as the quality gap between the two models grows.
- Position bias (Table 2, 80 pairs of near-identical answers): Claude-v1 with the default prompt was consistent in 23.8% of cases and favoured the first answer 75.0% of the time; GPT-4 was consistent in 65.0% and favoured the first 30.0%.
- Verbosity bias ("repetitive list" attack on 23 answers, Table 3): failure rate 91.3% for Claude-v1 and GPT-3.5 versus 8.7% for GPT-4.
- Self-enhancement: GPT-4 favoured itself with a win rate about 10% higher and Claude-v1 25% higher than humans, but the authors say the data cannot establish this bias firmly.
- Weak maths and reasoning grading: with the default prompt GPT-4 wrongly accepted wrong answers in 14 of 20 math cases; with chain-of-thought 6 of 20; with a reference answer 3 of 20 (Table 4).

## 6. Limitations
Stated by the authors: helpfulness is emphasised and safety is largely neglected; helpfulness dimensions (accuracy, relevance, creativity) are collapsed into one score; the proposed bias mitigations are preliminary.

Identified by me: only 80 questions and six models in MT-Bench, answers from 2023-era models, judge agreement measured against a small group of experts and anonymous crowd users; self-preference could not be confirmed with this sample; results apply to one judge family and may not hold for newer judges or other languages.

## 7. Relevance to the AI Request Router
- Quality labels in the project's benchmarks (MT-Bench is one of RouterBench's datasets, scored by GPT-4) are produced this way, so the paper tells us how noisy they are: position, verbosity and self-enhancement biases, weak math grading, and about 80–85% agreement with humans (so 15–20% disagreement even between humans).
- Reuse: swap-order double judging to remove position bias, a reference answer for maths, reporting judge/human agreement, using a stronger judge than the models being judged, and treating small score differences as noise.
- Risk: if the router is trained or evaluated on judge scores, it may learn to prefer verbose or judge-family models; where possible, use ground-truth correctness for math and code and judge scores only for open-ended chat.
- Does not cover: cost, latency, routing.
- Related: [RouterBench](hu-2024-routerbench.md) uses GPT-4 as evaluator for MT-Bench and other sets; [FusionFactory](feng-2026-fusionfactory.md) adds an LLM-judge score to its logs; [Chatbot Arena (Chiang et al., 2024)](chiang-2024-chatbot-arena.md) scales up the human-vote side.

## 8. How to use it in the report
- Section 2.7 on quality-label construction and its noise, and the threats-to-validity discussion.
- Sentence: "Zheng et al. (2023) found that GPT-4 judgments agree with human experts about 85% of the time but are affected by position and verbosity bias, so judge-based quality labels in routing benchmarks carry non-trivial noise."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Zheng et al. (2023) | Can LLM judges approximate human preference for chat quality? | MT-Bench multi-turn questions; pairwise and single-answer LLM judging; Chatbot Arena votes | 80 MT-Bench questions, 3K expert votes, 30K Arena conversations; GPT-4, GPT-3.5, Claude-v1 | GPT-4–human agreement 85% vs human–human 81%; position, verbosity and self-enhancement biases | Small question set, helpfulness only, 2023 models, bias fixes preliminary |
