# S-LoRA: serving thousands of concurrent LoRA adapters (Sheng et al., 2024)

| Field | Value |
|---|---|
| Topic (home) | 08 System design and gateway |
| Also relevant to | 04 Cost reduction, 05 Latency and speed |
| Paper type | system |
| Venue and status | peer-reviewed (*Proceedings of Machine Learning and Systems*, vol. 6, MLSys 2024) |
| Source read | sections 1 to 9 of the full text (https://arxiv.org/pdf/2311.03285, v3 of 5 June 2024); **appendices were not read** (A.1 PEFT analysis and B user-satisfaction metric were only seen by heading); the MLSys proceedings PDF was opened to confirm its title and abstract only |
| Verified on | 2026-10-31, against the MLSys 2024 proceedings page and PDF, and arXiv |
| Relevance to project | Low to medium (relevant if routing among fine-tuned variants of one base model; its SLO scheduling idea is the useful part) |

## APA 7 reference
Sheng, Y., Cao, S., Li, D., Hooper, C., Lee, N., Yang, S., Chou, C., Zhu, B., Zheng, L., Keutzer, K., Gonzalez, J. E., & Stoica, I. (2024). S-LoRA: Serving thousands of concurrent LoRA adapters. *Proceedings of Machine Learning and Systems, 6*. https://proceedings.mlsys.org/paper_files/paper/2024/hash/906419cd502575b617cc489a1a696a67-Abstract-Conference.html (preprint DOI: https://doi.org/10.48550/arXiv.2311.03285)

Metadata note: the MLSys proceedings listing page shows the title as "SLoRA: Scalable Serving of Thousands of LoRA Adapters", but the proceedings PDF and arXiv v3 both print "S-LoRA: Serving Thousands of Concurrent LoRA Adapters". The printed title is used. Page numbers were not shown on the proceedings page and are not given.

## In-text citation forms
(Sheng et al., 2024) · Sheng et al. (2024)

## 1. What it is about
S-LoRA serves thousands of LoRA fine-tuned variants of one base LLM from a single machine. It stores all adapters in main memory, brings only the adapters needed by running requests to the GPU, and batches the shared base-model computation across all of them.

## 2. The problem
Fine-tuning with LoRA produces many small adapters on one base model, but serving each as a separate model wastes memory (merging an adapter into the weights means one copy of the model per variant) and loses batching. Swapping adapters in and out one at a time cuts throughput.

## 3. Proposed solution
- **Unified Paging:** one memory pool for adapter weights of different ranks and KV-cache tensors of different lengths, to reduce fragmentation.
- **Heterogeneous batching:** custom CUDA kernels that batch adapters of different ranks held in non-contiguous memory.
- **S-LoRA tensor parallelism:** a way to split LoRA computation across GPUs with little extra communication.
- **Admission control through early abort:** the system estimates which requests can still meet the latency target (SLO: first token within 6 seconds) and drops those that cannot, instead of serving requests that have already missed it.

## 4. Data, models and tools
Llama-7B, 13B, 30B and 70B base models; A10G 24 GB, A100 40 GB and 80 GB GPUs. Synthetic workloads use a Gamma arrival process with a power-law split of rates over adapters (200 to 400 adapters by default); a real-style trace is downsampled from LMSYS Chatbot Arena, where different base models stand in for different adapters. Baselines: HuggingFace PEFT, "vLLM-packed" (several vLLM workers on one GPU, one per merged adapter) and S-LoRA variants. Code: https://github.com/S-LoRA/S-LoRA.

## 5. Key results
- Throughput up to 4 times higher than vLLM-packed with few adapters and up to 30 times higher than PEFT, while serving several orders of magnitude more adapters (abstract; section 7.2).
- Table 3, single A100 80 GB, S1 setting: with 5 adapters S-LoRA 8.05 req/s, vLLM-packed 2.04, PEFT 0.88; with 100 adapters 7.99, out of memory, 0.25; with 2,000 adapters S-LoRA 7.61 req/s.
- Throughput stays nearly flat once the number of adapters passes about 100, because the number active in a batch is unchanged (section 7.2).
- The early-abort strategy beats first-come-first-served and last-come-first-served on user satisfaction and SLO attainment, with the largest gap at high burstiness (Figure 10).

## 6. Limitations
- **Authors:** their Llama-70B setting used different architecture parameters from the official model and no grouped-query attention (footnote); kernel analysis is out of scope.
- **Mine:** tied to LoRA and one base model; synthetic traffic; the PEFT baseline lacks continuous batching and paging (the authors say so in a footnote), so the 30 times figure partly reflects how basic that baseline is; no routing between different base models; no failure handling.

## 7. Relevance to the AI Request Router
- **Supports:** the self-hosted backend side (D-03), and admission control as a deadline-aware complement to the router's latency budget (FR-05). The early-abort idea is a model for how a router can refuse or redirect a request it predicts will miss its budget.
- **Reuse:** time to first token within a fixed limit as an SLO definition; Chatbot Arena traces as a source of multi-model request patterns.
- **Not covered:** per-prompt model choice, gateway, hosted APIs, circuit breaker. It is relevant only if the project's backends are adapters of one base model, which the proposal does not say.

## 8. How to use it in the report
- Chapter 2, section 2.4.8 (multi-model serving) and 2.3.
- Suggested synthesis sentence: "S-LoRA (Sheng et al., 2024) multiplexes many fine-tuned variants of one base model inside an engine and drops requests that cannot meet a first-token deadline; the proposed router applies a similar deadline test before the call, across different models."
- Link: [MuxServe](duan-2024-muxserve.md), [AlpaServe](li-2023-alpaserve.md).

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Sheng et al. (2024) | Serve thousands of LoRA adapters of one base model | Unified Paging; heterogeneous batching kernels; adapter tensor parallelism; early-abort admission control | Llama 7B to 70B; A10G and A100; synthetic and Chatbot Arena traces; PEFT, vLLM-packed | Up to 4x vs vLLM-packed, up to 30x vs PEFT; 2,000 adapters on one GPU at 7.61 req/s | LoRA and single base model; weak PEFT baseline; no model choice or failover |
