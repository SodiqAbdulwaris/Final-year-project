# LLMLingua: prompt compression for cheaper inference (Jiang et al., 2023)

| Field | Value |
|---|---|
| Topic (home) | 04 Cost reduction |
| Also relevant to | none beyond this topic (affects the token-cost term used by 01 and 07) |
| Paper type | method (empirical) |
| Venue and status | peer-reviewed (EMNLP 2023, main conference) |
| Source read | full text, arXiv v2 (https://arxiv.org/pdf/2310.05736) |
| Verified on | 2026-10-31, against the ACL Anthology page and the arXiv abstract page |
| Relevance to project | Medium |

## APA 7 reference
Jiang, H., Wu, Q., Lin, C.-Y., Yang, Y., & Qiu, L. (2023). LLMLingua: Compressing prompts for accelerated inference of large language models. In *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing* (pp. 13358–13376). Association for Computational Linguistics. https://doi.org/10.18653/v1/2023.emnlp-main.825

## In-text citation forms
(Jiang et al., 2023) · Jiang et al. (2023). Where it must be told apart from LongLLMLingua, use (Jiang et al., 2023a) and (Jiang et al., 2024).

## 1. What it is about
A method that shortens a long prompt by deleting the tokens a small language model finds predictable, so a black-box LLM sees far fewer tokens. On GSM8K it compresses the prompt about 20 times with only a small drop in exact match. Fewer input tokens mean lower API cost and lower latency.

## 2. The problem
Chain-of-thought examples, retrieved documents and chat history push prompts to thousands of tokens. Quantisation or pruning need access to model weights and are useless when the LLM is reached through an API. Earlier prompt compression (Selective-Context) dropped tokens independently, ignoring their dependencies and the mismatch between the small compressor and the target model.

## 3. Proposed solution
A coarse-to-fine pipeline with a small LM (Alpaca-7B, or GPT-2 fine-tuned on Alpaca) that never touches the target LLM's gradients:
1. **Budget controller.** Splits the prompt into instruction, demonstrations and question. Instruction and question get light compression (rates 0.85 and 0.9 by default) while the demonstrations take most of the cut, via demonstration-level selection ranked by perplexity.
2. **Iterative token-level compression.** The prompt is divided into segments of 100 tokens; each is compressed conditioned on the already compressed earlier segments, and tokens with perplexity above a dynamic threshold are kept. This restores some token dependency.
3. **Distribution alignment.** The small LM is instruction-tuned on outputs from the target LLM so their token distributions are closer.

**How cost is modelled.** Mostly in **tokens**: compression ratio 1/τ, with the target's cost taken to scale with prompt length. The paper adds a computation estimate (Eq. 9): since a 7B compressor is about 1/25 of a 175B model per token, a 5x compression gives roughly one quarter of the compute, "nearly 4x savings". Latency is measured on a V100-32G. **No dollar prices are reported.**

## 4. Data, models and tools
- GSM8K and Big-Bench Hard (reasoning and in-context learning), ShareGPT (conversation), Arxiv-March23 (summarisation).
- Target LLMs: GPT-3.5-Turbo-0301 and Claude-v1.3, greedy decoding. Baselines: Selective-Context, sentence selection, random selection, GPT-4-generated compression.
- Code: https://aka.ms/LLMLingua.

## 5. Key results
- GSM8K (Table 2): full 8-shot prompt 78.85 exact match at 2,366 tokens; LLMLingua 79.08 at 446 tokens (about 5x); 77.41 at 171 tokens (14x); 77.33 at 117 tokens (20x).
- At 20x on GSM8K, Selective-Context gets 44.20 and GPT-4-generated compression 56.33 (Table 2). The text states a gap of 33.10 points over Selective-Context.
- With Claude-v1.3 (Table 4): 83.51 EM at 5x and 82.61 at 14x, versus 81.8 for the simple prompt at 3x.
- Ablation (Table 3): removing the budget controller or iterative compression costs about 5 to 6 EM points; distribution alignment adds 0.56.
- Latency (Table 6, V100-32G): 1.7x to 5.7x end-to-end speed-up for 2x to 10x compression; the compression step itself takes 0.2 to 0.8 s.
- Generated outputs also get shorter as compression rises (Figure 2), saving decoding compute.
- BBH loses more: at 5x EM falls about 8.5 points and at 7x about 13 points.

## 6. Limitations
*Stated by the authors:* notable degradation at very high ratios (25x to 30x on GSM8K); GPT-2-small as compressor is weaker than Alpaca-7B.

*My observations:* it needs a 7B compressor on a GPU in front of the LLM, adding its own latency and load (0.2 to 0.8 s here). Results are from 2023 models and mostly prompts with demonstrations; short chat prompts have little to remove. The compressed text is unreadable, which may break exact-match prompt caches, and no dollar savings or failure analysis on safety-relevant prompts are given.

## 7. Relevance to the AI Request Router
- A candidate **pre-routing optimisation** for long-context requests: shorten the prompt, then route. Savings flow straight into the token-price term of the cost function (cost ∝ input tokens × price).
- **Reuse:** compression ratio as a configurable knob; token-level cost accounting. **Avoid:** compressing short prompts. **Not covered:** the effect on routing quality predictions (does a difficulty classifier still work on compressed prompts?), live load, self-hosted GPU cost.

## 8. How to use it in the report
Section 2.4 (prompt compression) as a complementary, model-agnostic route to cost reduction alongside routing. Synthesis sentence: "Whereas routing chooses a cheaper model, Jiang et al. (2023) reduce cost by sending the same model fewer tokens, up to 20x on GSM8K with a 1.5-point exact-match loss."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Jiang et al. (2023) | Reduce LLM inference cost and latency via shorter prompts | Coarse-to-fine compression: budget controller, iterative token-level perplexity pruning, distribution alignment | GSM8K, BBH, ShareGPT, Arxiv-March23; GPT-3.5-Turbo, Claude-v1.3 | 20x compression, 77.33 vs 78.85 EM on GSM8K; 1.7x to 5.7x faster | Needs a 7B compressor; drops at 25x+; no dollar figures; 2023 models |
