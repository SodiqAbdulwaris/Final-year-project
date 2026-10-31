Status: DRAFT
Depends on: D08; D12
Sources: Primary URLs in source table and proposal-audit section
Open items: Scoped numerical/final-version checks recorded below

# Faster cascades via speculative decoding (Narasimhan et al., 2025)

| Field | Value |
|---|---|
| Topic (home) | 04 Cost reduction |
| Also relevant to | 05 Serving and inference engines (speculative decoding) |
| Paper type | method (theory and empirical) |
| Venue and status | peer-reviewed (ICLR 2025, oral presentation per the ICLR proceedings listing); first posted on arXiv May 2024 |
| Source read | full text, arXiv v2 (https://arxiv.org/pdf/2405.19261) |
| Verified on | 2026-10-31, against the arXiv abstract page and the ICLR 2025 proceedings listing |
| Relevance to project | Low to Medium |

## APA 7 reference
Narasimhan, H., Jitkrittum, W., Rawat, A. S., Kim, S., Gupta, N., Menon, A. K., & Kumar, S. (2025). Faster cascades via speculative decoding. In *The Thirteenth International Conference on Learning Representations*. https://proceedings.iclr.cc/paper_files/paper/2025/hash/6f43166f50f26e8d8f3edc5545b0749f-Abstract-Conference.html (preprint DOI: https://doi.org/10.48550/arXiv.2405.19261)

## In-text citation forms
(Narasimhan et al., 2025) · Narasimhan et al. (2025)

## 1. What it is about
Cascades and speculative decoding both pair a small and a large model to save inference cost, but by different means. This paper merges them: the small model drafts tokens, the large model checks them in parallel, and a *deferral rule* (instead of strict distribution matching) decides which draft tokens to keep. The result trades quality against latency better than either approach alone.

## 2. The problem
A cascade defers hard inputs to the large model and often gives a better cost-quality trade-off than the large model alone, but it runs sequentially, calling the large model once per deferred token. Speculative decoding verifies a block of draft tokens in parallel and is quality-neutral by construction, but it rejects draft tokens whenever the two models disagree, even when the small model is right.

## 3. Proposed solution
**Speculative cascades** run speculative decoding against a *target distribution* π built from the drafter q and the verifier p, rather than p itself. The target mixes them as (1−α)·q + α·p, where α encodes the deferral decision. Accepted tokens skip a large-model call; rejected ones are resampled from a residual.

Deferral rules plugged into this recipe: Chow's confidence threshold, a confidence-difference rule (Diff), a plug-in estimate of the theoretically optimal rule (OPT), and a token-specific rule. The paper characterises the optimal token-level rule: defer when the small model's expected loss exceeds the large model's expected loss plus a cost penalty c. Compared against sequence-level and token-level cascades, lossy speculative decoding, and BiLD.

**How cost is modelled.** Cost has two proxies: the *fraction of tokens that require a large-model call* (deferral or rejection rate) and measured *wall-clock latency at batch size 1* relative to calling the large model alone. In the optimal-rule derivation cost is a penalty c added when deferring. No dollar prices or GPU-hour figures appear.

## 4. Data, models and tools
- Fine-tuned T5 v1.1: T5-small (77M) drafting for T5-large (800M) or T5-XL (3B), on WMT En→De, XSum and CNN/DM, temperatures 0 to 1, block sizes 3, 5, 7.
- Few-shot Gemma v2: 2B drafting for 27B (and 9B), on WMT, CNN/DM, GSM8K, MBPP, SQuAD 2.0, WebQuestions, NaturalQA, TriviaQA.

## 5. Key results
- Table 2 (T = 1, block size 5), latency reduction when matching the large model's quality: SpecCascade [OPT] 2.61x on WMT small→XL and 1.95x on WMT small→large; SpecCascade [Token] 2.50x (WMT small→XL); the sequence-level cascade [Chow] gives 1.55x and 2.46x on WMT but under 1x on XSum and CNN/DM (0.84x to 0.98x); lossy speculative decoding gives 1.61x and 2.17x on WMT.
- Best quality without exceeding the large model's latency (same table, WMT small→large, BLEU): SpecCascade [Token] 22.50, versus 17.26 for lossy speculative decoding and 16.52 for the token-level cascade.
- With Gemma 2B→27B (Figure 3), the token-specific variant usually matches 27B quality at a lower rejection rate and often exceeds 27B's quality. TriviaQA is the exception.
- Sequential cascades keep an advantage in the very-low-latency regime.

## 6. Limitations
*Stated by the authors:* higher throughput but also higher total compute than sequential cascades; the plug-in rule is not learned from ground truth; extension beyond two models is future work. They also say they do not claim a new state of the art for fast LM inference.

*My observations:* it needs logits from both models at every token, so both must be served together with the same tokenizer; it cannot cross hosted-API providers. Latency is measured at batch size 1, which says little about busy GPU serving, and only T5 and Gemma models were tested.

## 7. Relevance to the AI Request Router
- Mostly **background**: it shows that cost-quality trade-offs exist *inside* a single serving engine, below the router's model-selection layer. vLLM supports speculative decoding (my note; see topic 05), so the router can treat it as an engine-level optimisation, not a routing decision.
- **Reuse:** the "defer when expected small-model loss exceeds large-model loss plus cost" form, which mirrors the router's per-request scoring; the deferral rate as a cost proxy. **Avoid:** building token-level cascades across separate endpoints. **Not covered:** more than two models, load, hosted APIs.

## 8. How to use it in the report
Section 2.4 (distinguishing routing from in-engine efficiency) with a pointer to topic 05. Synthesis sentence: "Narasimhan et al. (2025) show that cascade deferral can be implemented speculatively, achieving up to 2.6x lower latency at large-model quality, but only where both models share a serving stack, unlike gateway-level routing."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Narasimhan et al. (2025) | Combine cascade quality gains with speculative-decoding speed | Speculative execution of cascade deferral rules (Chow, Diff, OPT, token-specific) | T5-small to large/XL on WMT, XSum, CNN/DM; Gemma 2B to 27B on 8 few-shot tasks | Up to 2.61x latency reduction at large-model quality; better trade-off than cascades or speculative decoding alone | Two co-served models; logits needed; batch size 1; higher total compute |


## 2026-10-31 proposal audit

- Source attempted: https://arxiv.org/abs/2405.19261.
- Scope: Abstract/metadata check only in this session; detailed numerical results remain unchecked.
- Historical Source read above records the earlier session, not a claim of a fresh full reading.
- arXiv title matched: Faster Cascades via Speculative Decoding. Latest listed version: v2; arXiv DOI identifies the preprint, not peer review. A missing journal reference does not prove that no published version exists.
