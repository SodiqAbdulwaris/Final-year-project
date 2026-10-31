# Learning how hard to think: predicting per-query compute needs (Damani et al., 2025)

| Field | Value |
|---|---|
| Topic (home) | 02 Prompt difficulty prediction (added replacement paper) |
| Also relevant to | 01 Routing algorithms, 04 Cost reduction |
| Paper type | method |
| Venue and status | peer-reviewed (ICLR 2025) |
| Source read | full text of arXiv v1 (https://arxiv.org/pdf/2410.04707v1, Oct 2024); the ICLR camera-ready may differ in numbers |
| Verified on | 2026-10-31, against the ICLR 2025 proceedings page and arXiv |
| Relevance to project | High |

## APA 7 reference
Damani, M., Shenfeld, I., Peng, A., Bobu, A., & Andreas, J. (2025). Learning how hard to think: Input-adaptive allocation of LM computation. In *The Thirteenth International Conference on Learning Representations*. https://proceedings.iclr.cc/paper_files/paper/2025/hash/ff414825df833edb8b1839e3d5d495e9-Abstract-Conference.html

(ICLR proceedings carry no DOI; the arXiv DOI is https://doi.org/10.48550/arXiv.2410.04707.)

## In-text citation forms
(Damani et al., 2025) · Damani et al. (2025)

## 1. What it is about
The paper trains a lightweight predictor that reads a query and estimates how much extra computation would improve the answer, then spends a compute budget where it helps most. It uses this in adaptive best-of-k sampling and in routing between a cheap and an expensive decoding procedure.

## 2. The problem
Language models are normally run with the same decoding procedure for every input, so easy queries waste compute and hard ones may be under-served. Some queries are hopeless (no amount of sampling helps) and others are trivial. The authors ask whether the benefit of extra computation can be predicted from the query alone, before generating.

## 3. Proposed solution
For each training query the authors sample many responses and compute empirical *marginal rewards*: how much the expected reward improves when the budget grows from j−1 to j samples. A predictor is trained to output this whole vector with mean squared error. When rewards are binary (code, math), it instead predicts the single-sample success probability with cross-entropy, from which the best-of-k success curve follows: 1 − (1 − p)^k.

Two predictor designs: a two-layer MLP on the last hidden state of the base LM, or LoRA fine-tuning of the base LM. At inference the MLP adds almost no cost because the hidden states are already computed.

Allocation is a small optimisation problem solved greedily (a matroid structure makes the greedy answer optimal): "turn on" the budget increments with the highest predicted gain. The online variant needs a batch of queries; the offline variant bins held-out queries by predicted reward and fixes a budget per bin, so each query can be handled independently. For routing, the predictor outputs the probability that the strong procedure's answer is preferred over the weak one, and the top queries are routed to the strong one.

## 4. Data, models and tools
- Math: subset of NuminaMath-CoT with Mathstral-7B and an oracle verifier. Code: subset of TACO with a StarCoder-15B model, success means all tests pass. Chat: LMSYS-Chat with Gemma-7b-it and the Llama-3-OffsetBias-RM-8B reward model.
- Routing pairs: Gemma-2b-it versus Gemma-7b-it on LMSYS; plain sampling versus value-augmented sampling with Llama-2 7B (about 10× the decoding cost) on the harmless subset of Anthropic HH.
- Baselines: uniform best-of-k, random routing, and an oracle using true marginal rewards. No code link noted in the text I read.

## 5. Key results
- Summary (Section 1): on math and code, the same performance as non-adaptive best-of-k with up to 50% less compute; on chat, up to 10% less; in routing, matching the expensive decoder while calling it only 50–75% of the time.
- Routing (Section 4.2, Figure 5): up to 25–40% fewer calls to the expensive decoding scheme at similar reward in the value-augmented setting. In some cases routing even beat always using the strong decoder, because the weak one sometimes does better.
- Predictor quality (Table 1): median-threshold accuracy for easy-versus-hard is 74% (code), 84% (math), 72% (chat, model routing) and 72% (chat, value-augmented routing). Test loss is below the "predict the average" baseline in every setting, but a gap to the oracle remains.
- Gains are smaller on the full chat and math test sets (0–10% budget reduction) than on "tranches" of the highest- and lowest-variance queries (25–40%), per Section 4.1.

## 6. Limitations
Stated by the authors: the math experiments assume access to a verifier (usually unavailable, so a reward model would be used); there is a gap between the predictor and the oracle, so better predictors are future work.

Identified by me: only one model family per setting, and the predictor is tied to the specific base LM whose hidden states it reads. The routing pairs are two sizes of Gemma or two decoding procedures, not a pool of heterogeneous hosted models. Cost is counted as the number of samples or expensive calls, not latency, money or load. The offline allocation can violate the budget if the query distribution shifts, as the authors note. The 50% figure applies to the best cases (math and code), not chat.

## 7. Relevance to the AI Request Router
- Closest match to the project's classifier idea among the papers in this folder: a cheap predictor reads the query once and outputs an expected-benefit score used by a budget-aware allocator.
- Reuse: label construction by repeated sampling (no human annotation); soft labels (success probability) instead of hard easy/hard classes; the offline binning policy, which lets each request be routed independently without batching; evaluation against uniform and oracle baselines using compute-versus-reward curves; the finding that difficulty is predictable (above 70% accuracy) but far from perfect.
- Avoid: relying on the target LM's hidden states at routing time; a sentence-embedding encoder would replace them and must be tested.
- Not covered: heterogeneous hosted backends, latency, live load, failover.

## 8. How to use it in the report
- Section 2.4 (predicting benefit of compute from the prompt) and the evaluation-design chapter for the oracle-versus-learned comparison.
- Sentence: "Damani et al. (2025) show that a lightweight probe on a query's hidden state can predict how much extra computation will help and cut compute by up to 50% on math and code, but their routing experiments use only two decoders at a time and no load signal."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Damani et al. (2025) | Allocate decoding compute per query by predicted benefit | Probe/LoRA predicts marginal reward; greedy budget allocation; routing variant | NuminaMath, TACO, LMSYS-Chat, Anthropic HH; Mathstral, StarCoder, Gemma | Up to 50% less compute on math/code; 25–40% fewer expensive calls in routing; predictor accuracy 72–84% | Two-option routing, hidden-state input, sample-count cost, no latency or load |
