Status: DRAFT
Depends on: D08; D12
Sources: Primary URLs in source table and proposal-audit section
Open items: Scoped numerical/final-version checks recorded below

# Chatbot Arena: ranking LLMs from crowdsourced human preferences (Chiang et al., 2024)

| Field | Value |
|---|---|
| Topic (home) | 07 Testing and benchmarking |
| Also relevant to | 01 Routing algorithms (RouteLLM trains on Arena preference data) |
| Paper type | platform / benchmark / statistical methods |
| Venue and status | peer-reviewed (ICML 2024, PMLR 235:8359–8388) |
| Source read | full text (arXiv v1, https://arxiv.org/pdf/2403.04132v1); the ICML version may differ slightly |
| Verified on | 2026-10-31, against the PMLR page (proceedings.mlr.press/v235/chiang24b.html) and arXiv |
| Relevance to project | Medium |

## APA 7 reference
Chiang, W.-L., Zheng, L., Sheng, Y., Angelopoulos, A. N., Li, T., Li, D., Zhu, B., Zhang, H., Jordan, M., Gonzalez, J. E., & Stoica, I. (2024). Chatbot Arena: An open platform for evaluating LLMs by human preference. In *Proceedings of the 41st International Conference on Machine Learning* (Vol. 235, pp. 8359–8388). PMLR. https://proceedings.mlr.press/v235/chiang24b.html

## In-text citation forms
(Chiang et al., 2024) · Chiang et al. (2024)

## 1. What it is about
Chatbot Arena is a public website where visitors ask any question to two anonymous LLMs and vote for the better answer. The paper describes the platform, shows how the votes are turned into model rankings with statistical confidence intervals, and checks that crowd votes are diverse and agree with experts.

## 2. The problem
Static benchmarks with ground-truth answers (MMLU, GSM8K) are cheap and reproducible, but they are closed-ended, can be contaminated once questions leak, and cannot judge tasks with no single right answer. Human preference is a more direct measure of usefulness, but a live, open, diverse and efficient source of such judgements was lacking.

## 3. Proposed solution
**Data collection.** Users submit a prompt, see two anonymous responses, and vote (A, B, tie or both bad). Model identities are revealed after the vote. More than 240K votes were collected in several months, covering over 50 models, more than 100 languages (77% English, 5% Chinese), with an average of about 8K votes per model.

**Ranking.** The Bradley–Terry model estimates a latent strength per model from the pairwise outcomes (the Elo-style score is a transformation of the same quantity). Confidence intervals come from a pivot bootstrap or a sandwich-based interval, with multiplicity correction so that all rankings hold simultaneously.

**Efficient sampling.** An active sampling rule picks the model pair whose confidence interval would shrink most, concentrating votes on pairs with similar strength.

**Quality control.** Anomalous users (for example repeating "hi" or sending garbled text) are detected with a statistical test. Prompts are embedded and clustered into topics, and a harder benchmark is built from the most discriminating clusters.

## 4. Data, models and tools
- Public votes from the live platform; replay experiments use 213,576 historical votes.
- Agreement check: a sample of battles judged by experts and by GPT-4 as well as the crowd, for two model pairs (Llama-2-13b-chat and GPT-3.5-Turbo, each against GPT-4-Turbo).
- Related data: LMSYS-Chat-1M has conversations only, with no preference votes, so it cannot be used to rank models directly.
- Demo: chat.lmsys.org (as stated in the paper).

## 5. Key results
- Crowd–expert agreement is 72% to 83% (Table 3, for example 72.8%, 77.8% for Llama-2-13b versus the two experts) while expert–expert agreement is 79.4% to 89.8%. The authors attribute the 10–20% disagreement between experts largely to prompts with no ground-truth answer, and the 5–10% extra gap for the crowd to users overlooking factual errors.
- Prompts are diverse and discriminating: win rate of a stronger model can reach up to 97% in some topic clusters (Section 6), and can drop below 60% on others, so topic clusters help separate models.
- Active sampling needs fewer votes: the random baseline needs 54% and 5% more data (in the two settings tested) to reach the same precision (Section 7.1).
- The outlier detection method was evaluated on 25 manually labelled anomalous users against 25 normal users (Section 7.2); I did not extract its accuracy.

## 6. Limitations
Stated by the authors: the user base is mostly LLM hobbyists and researchers, so the sample is biased; prompts come from one chat interface and may not reflect production use or specialised domains; helpfulness is assessed, not safety.

Identified by me: preferences are single-turn pairwise votes, which blend correctness, style and length; there is no cost or latency; vote noise is quantified through agreement rates, but the crowd is anonymous (identified only by IP); tie handling and style effects are only partly examined in the main text I read; rankings change as models and the voting population change.

## 7. Relevance to the AI Request Router
- The project's chat-quality labels will likely come from preference data or an LLM judge, so this paper gives the reference method for how noisy human preference is: expect roughly 10–20% disagreement even between experts on open-ended prompts, and use confidence intervals, not a single point score.
- Reuse: Bradley–Terry strength with bootstrap intervals for comparing routing policies from pairwise outcomes; the idea of clustering prompts by topic to check where a router helps; outlier-user filtering for logged prompts.
- Related: [Zheng et al. (2023)](zheng-2023-mt-bench-llm-judge.md) checks judge agreement against these votes; RouteLLM (topic 01) trains its routers on Arena preference data, see [Ong et al. (2025)](../01-routing-algorithms/ong-2025-routellm.md).
- Does not cover: latency, load, cost, routing evaluation.

## 8. How to use it in the report
- Section 2.7 on preference-based evaluation and label noise, and the statistical-testing plan in Chapter 3.
- Sentence: "Chiang et al. (2024) report 72–83% agreement between crowd votes and experts versus 79–90% between experts, which sets a ceiling on how clean preference-derived quality labels can be."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Chiang et al. (2024) | Live, open evaluation of LLMs by human preference | Anonymous pairwise battles; Bradley–Terry ranking with bootstrap intervals; active sampling | 240K+ votes, 50+ models, 100+ languages | Crowd–expert agreement 72–83%; active sampling cuts votes needed | Hobbyist user bias, helpfulness only, no cost or latency |


## 2026-10-31 proposal audit

- Source attempted: https://arxiv.org/abs/2403.04132.
- Scope: Abstract/metadata check only in this session; detailed numerical results remain unchecked.
- Historical Source read above records the earlier session, not a claim of a fresh full reading.
- arXiv title matched: Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference. Latest listed version: v1; arXiv DOI identifies the preprint, not peer review. A missing journal reference does not prove that no published version exists.
