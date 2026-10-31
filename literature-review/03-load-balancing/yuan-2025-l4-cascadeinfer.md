Status: DRAFT
Depends on: D08; D12
Sources: Primary URLs in source table and proposal-audit section
Open items: Scoped numerical/final-version checks recorded below

# L4 / CascadeInfer: length-aware multi-instance scheduling (Yuan et al., 2025)

| Field | Value |
|---|---|
| Topic (home) | 03 LLM load balancing |
| Also relevant to | 05 Serving engines (attention backend behaviour) |
| Paper type | system |
| Venue and status | preprint only (arXiv v1 22 Dec 2025 titled "L4: Low-latency and load-balanced LLM serving via length-aware scheduling"; v3 15 May 2026 retitled CascadeInfer) |
| Source read | full text of v3 (https://arxiv.org/pdf/2512.19179) |
| Verified on | 2026-10-30, against arXiv abs 2512.19179 (v1 title checked on the v1 page) |
| Relevance to project | Medium |

## APA 7 reference
Yuan, Y., Zhao, C., Zhao, B., Cao, Z., He, Y., & Wu, W. (2025). *CascadeInfer: Length-aware scheduling of LLM serving with low latency and load balancing* [Preprint, formerly titled "L4: Low-latency and load-balanced LLM serving via length-aware scheduling"]. arXiv. https://doi.org/10.48550/arXiv.2512.19179

## In-text citation forms
(Yuan et al., 2025) · Yuan et al. (2025)

## 1. What it is about
In a cluster of identical LLM replicas serving long-context traffic, mixing short and very long sequences in one batch wastes GPU time. This paper (L4 in its first version, CascadeInfer in the latest) groups replicas into "stages" serving ranges of sequence length and migrates a request to the next stage as it grows.

## 2. The problem
Attention kernels are sensitive to length differences inside a batch: the GPU idles waiting for the long sequences, and one replica cannot gather enough similar-length requests to avoid it. Inter-instance schedulers such as Llumnix balance memory or load but ignore length, so every replica still gets mixed batches.

## 3. Proposed solution
- **Length-specialised pipeline.** A new request enters the earliest stage whose range covers its prompt and moves downstream when decoding outgrows the range.
- **Stage planning.** Dynamic programming over the historical length distribution picks stage boundaries that maximise a quality-of-experience (QoE) model of predicted latency.
- **Runtime adaptation.** Each replica's LoadTracker records token-level load and exchanges summaries with peers and neighbouring stages, which recompute boundaries as the length mix drifts.
- **Decentralised balancing.** An overloaded instance (example: memory demand 25% above the stage average) starts a "bid-ask" exchange: receivers reply with load and earliest transfer start time and the sender picks among the lighter, earlier bidders. Migration reuses Llumnix's live KV transfer. With no central scheduler, the authors say decisions rest on less stale state.

## 4. Data, models and tools
- Implemented on vLLM; baselines vLLM 0.9.1 and SGLang 0.4.9 behind round-robin, and Llumnix.
- Two 16-GPU testbeds (H20, L40); eight models from 3B to 32B plus Llama-3.1-70B; ShareGPT with Poisson arrivals.
- Metrics: TTFT, time per output token (TPOT), throughput, SLO attainment. No code link found.

## 5. Key results
- Abstract: end-to-end latency down by up to 67%, tail latency by up to 69%, throughput up to 2.89× versus state-of-the-art multi-instance schedulers.
- Under heavy load mean TTFT is lower by 67–78% than vLLM, 70–84% than SGLang and 36–66% than Llumnix (Section 6.2, Fig. 6); tail TTFT lower on average by 56%, 62% and 19%.
- Throughput under heavy load averaged 1.99× vLLM, 2.18× SGLang and 1.71× Llumnix on H20; on L40, 1.37×, 1.21× and 1.34× (Section 6.3).
- SLO attainment on Llama-3.2-3B: 3.8–7.6× at a 5× SLO and 2.0–2.8× at 20× (Section 6.4, Fig. 12).
- Under light load the system behaves like standard multi-instance scheduling, close to Llumnix.

## 6. Limitations
- *Stated by authors:* gains shrink when weights leave little memory for large batches or lengths are uniform; only homogeneous instances evaluated.
- *My observations:* helps mainly long-context, large-batch workloads; needs engine access for KV migration; ShareGPT with synthetic arrivals only; preprint whose title changed between versions.

## 7. Relevance to the AI Request Router
- **Live-load signals:** token counts (sequence length) beat request counts as a load signal, and small per-instance summaries avoid a stale central view. Motivates prompt length in the load score.
- **Reuse:** with several replicas of one model, a gateway could route by prompt-length bucket.
- **Not covered:** stage pipeline and KV migration are engine-level; no model choice, cost or quality.

## 8. How to use it in the report
- Section on length-aware load balancing, as a more recent step beyond Llumnix (Sun et al., 2024); cite with a note that it is a preprint.
- Synthesis sentence: "Yuan et al. (2025) extend memory-aware balancing with sequence length, reporting up to 1.71× higher throughput than Llumnix under heavy long-context load, though only on homogeneous replicas."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Yuan et al. (2025) | Remove length heterogeneity within batches across replicas | Length-specialised stage pipeline, DP stage planning, decentralised bid-ask migration | vLLM, ShareGPT, H20/L40, 8 models | Up to 67% lower latency, 2.89× throughput vs SOTA; 1.71× Llumnix at heavy load | Homogeneous replicas; engine access; preprint |


## 2026-10-31 proposal audit

- Source attempted: https://arxiv.org/abs/2512.19179.
- Scope: Abstract/metadata check only in this session; detailed numerical results remain unchecked.
- Historical Source read above records the earlier session, not a claim of a fresh full reading.
- arXiv title matched: CascadeInfer: Length-Aware Scheduling of LLM Serving with Low Latency and Load Balancing. Latest listed version: v3; arXiv DOI identifies the preprint, not peer review. A missing journal reference does not prove that no published version exists.
