Status: DRAFT
Depends on: D08; D12
Sources: Primary URLs in source table and proposal-audit section
Open items: Scoped numerical/final-version checks recorded below

# ServerlessLLM: low-latency serverless LLM inference with live migration (Fu et al., 2024)

| Field | Value |
|---|---|
| Topic (home) | 06 Error handling and fallback |
| Also relevant to | 03 Load balancing, 05 Serving systems |
| Paper type | system |
| Venue and status | peer-reviewed (OSDI 2024, pp. 135–153) |
| Source read | full text, arXiv v2 (https://arxiv.org/pdf/2401.14351) |
| Verified on | 2026-10-31, against the USENIX OSDI '24 presentation page |
| Relevance to project | Medium to Low |

## APA 7 reference
Fu, Y., Xue, L., Huang, Y., Brabete, A.-O., Ustiugov, D., Patel, Y., & Mai, L. (2024). ServerlessLLM: Low-latency serverless inference for large language models. In *Proceedings of the 18th USENIX Symposium on Operating Systems Design and Implementation* (pp. 135–153). USENIX Association. https://www.usenix.org/conference/osdi24/presentation/fu (preprint DOI: https://doi.org/10.48550/arXiv.2401.14351)

## In-text citation forms
(Fu et al., 2024) · Fu et al. (2024)

## 1. What it is about
A serverless inference system that cuts the "cold start" of loading large model checkpoints onto GPUs. It speeds up loading, schedules a model onto the server with the best checkpoint locality, and, where locality conflicts with a running request, **live-migrates** that inference to another server with little interruption.

## 2. The problem
Serverless platforms charge per use, but loading multi-gigabyte checkpoints makes first-token latency very high (the KServe baseline took 128 s for an OPT-6.7B first token, 114 s of it downloading). Moving a running LLM job is hard: it is stateful, its KV cache is large, and its duration is unpredictable.

## 3. Proposed solution
1. A loading-optimised checkpoint format and multi-tier storage pipeline (SSD, DRAM, GPU).
2. **Live migration of LLM inference.** The source server sends only the tokens generated so far (tens to hundreds), not the KV cache; the destination recomputes the cache from them, which is much faster than the source generating the same tokens; migration runs in rounds until the source can stop with little delay, then resumes at the destination.
3. A scheduler with cost models for loading time and migration time that picks the server minimising startup latency.
The design also states failure handling: if the source or destination server fails during loading or migration, the scheduler cancels the migration; if the destination fails while resuming, the source continues; a reliable key-value store lets the scheduler recover.

**How cost is modelled.** Time costs only: estimated checkpoint-load time from storage bandwidth, and migration time estimated from input tokens, generated tokens and model-specific parameters.

## 4. Data, models and tools
OPT, LLaMA-2 and Falcon models; GSM8K and ShareGPT workloads; request patterns from a public Azure serverless trace; four-server GPU cluster; baselines KServe, Ray Serve and Ray Serve with local checkpoint caching. Code: https://github.com/ServerlessLLM/ServerlessLLM.

## 5. Key results
- Checkpoint loading 3.6 to 8.2 times faster than Safetensors and PyTorch; 4.4 times faster for LoRA adapters.
- End-to-end latency 10 to 200 times lower than the serverless baselines across workloads (abstract).
- Under higher request rates the other systems' latency rises once load exceeds about 0.5 requests/s on GSM8K, while ServerlessLLM stays near 1 second because it can migrate; it was the only system to reach under one second against KServe.

## 6. Limitations
*Stated by the authors:* fairness of resources across the cluster and smart checkpoint placement are left for the future.

*My observations:* the paper is about latency and locality, not failure; its failure handling is described in prose with no fault-injection experiment. It assumes a stateless-looking token stream can be recomputed; results are for small clusters. The public repository's status for migration was inconsistent in one README table (reported by a search result, not verified).

## 7. Relevance to the AI Request Router
- A concrete precedent for **moving an unfinished request**: re-send the prompt plus the tokens already produced to another backend and let it continue by recomputing state. The same trick would let a router resume after a mid-generation failure on a self-hosted backend, at the cost of one prefill.
- Gives an example of **cost models based on time** that could feed the scoring function's latency term.
- **Reuse:** migrate-tokens-not-cache idea. **Avoid:** the serverless checkpoint machinery. **Not covered:** API providers, quality comparison between source and destination models, rate limits.

## 8. How to use it in the report
Section 2.5, request migration paragraph (alongside SpotServe and Llumnix in topic 03). "Fu et al. (2024) migrate running LLM inferences by forwarding only the generated tokens and recomputing the KV cache at the destination, an approach that keeps migration traffic small."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Fu et al. (2024) | Low-latency serverless LLM inference | Fast checkpoint loading; token-based live migration; locality-aware scheduling | OPT, LLaMA-2, Falcon; GSM8K, ShareGPT; Azure trace; KServe, Ray Serve | 10 to 200x lower latency; 3.6 to 8.2x faster loading | Small cluster; failure handling not evaluated |


## 2026-10-31 proposal audit

- Source attempted: https://arxiv.org/abs/2401.14351.
- Scope: Abstract/metadata check only in this session; detailed numerical results remain unchecked.
- Historical Source read above records the earlier session, not a claim of a fresh full reading.
- arXiv title matched: ServerlessLLM: Low-Latency Serverless Inference for Large Language Models. Latest listed version: v2; arXiv DOI identifies the preprint, not peer review. A missing journal reference does not prove that no published version exists.
