# Clockwork: a central controller that serves DNNs within latency SLOs (Gujarati et al., 2020)

| Field | Value |
|---|---|
| Topic (home) | 08 System design and gateway |
| Also relevant to | 03 Load balancing, 05 Latency and speed, 06 Fallback |
| Paper type | system |
| Venue and status | peer-reviewed (14th USENIX OSDI, November 2020, pp. 443–462) |
| Source read | full text of sections 1 to 9 (https://arxiv.org/pdf/2006.02464, v2 of 26 October 2020); reference list and any appendix not read |
| Verified on | 2026-10-31, against the USENIX OSDI '20 presentation page and the arXiv abstract page |
| Relevance to project | High as a design idea (reject a request that cannot meet its deadline, decided centrally from predicted time); not directly applicable to LLMs |

## APA 7 reference
Gujarati, A., Karimi, R., Alzayat, S., Hao, W., Kaufmann, A., Vigfusson, Y., & Mace, J. (2020). Serving DNNs like Clockwork: Performance predictability from the bottom up. In *Proceedings of the 14th USENIX Symposium on Operating Systems Design and Implementation (OSDI 20)* (pp. 443–462). USENIX Association. https://www.usenix.org/conference/osdi20/presentation/gujarati (USENIX issues no DOI; preprint DOI: https://doi.org/10.48550/arXiv.2006.02464)

## In-text citation forms
(Gujarati et al., 2020) · Gujarati et al. (2020)

## 1. What it is about
Clockwork is a distributed system for serving deep neural network (DNN) models with predictable latency. Its central claim is that DNN inference on a GPU takes almost the same time every run, so a controller that makes all scheduling choices can predict completion times and only run a request if it can meet its deadline.

## 2. The problem
Model serving systems must meet latency service level objectives (SLOs), but existing ones use reactive techniques (fair queuing, auto-scaling, throttling) that tolerate unpredictable execution times and let tail latency grow. Over-provisioning hides the problem at the price of low utilisation. The authors note that many applications cannot justify a dedicated GPU, so many models must share accelerators.

## 3. Proposed solution
- **Observation:** executing ResNet50v2 11 million times in isolation on a V100 GPU showed the 99.99th percentile latency within 0.03% of the median. Running inferences concurrently raised throughput by up to 25% but increased tail latency by 100 times, because GPU and operating-system scheduling add variability.
- **Consolidating choice:** workers have no choices; one centralised controller decides when to load models and when to run each inference, and workers follow the schedule exactly. If a worker cannot run an action in its time window it rejects it.
- **Controller:** keeps per-worker, per-model performance profiles (recent action durations, stratified by batch size), tracks memory state and pending actions, predicts when each action would complete, and only submits work that can meet the request's deadline. Requests wait in per-model, per-batch-size queues and are dropped once they can no longer be satisfied.
- **Workers:** a custom runtime built from the TVM compiler with pre-allocated GPU memory in 16 MB pages, one execution at a time, and executors pinned to cores. About 26,000 lines of C++.

## 4. Data, models and tools
A private cluster of 12 Dell servers, each with 32 cores, 768 GB RAM and two NVIDIA V100 32 GB GPUs on 10 Gbps Ethernet; controller, clients and workers on separate machines. Models: ResNet50 (up to 3,601 copies on one worker) and a mix of other image models (DenseNet, DLA, GoogLeNet, Inception and others). Production workloads from Microsoft Azure Functions traces. Baselines: Clipper and INFaaS (INFaaS was run on AWS EC2 because it could not be deployed on the authors' cluster, so that comparison is described as qualitative).

## 5. Key results
- The system supports thousands of models while meeting a 100 ms latency target for 99.9999% of requests (abstract; section 6.2 with 3,600 model instances on one worker).
- Against Clipper and INFaaS (15 ResNet50 copies on one GPU, Figure 5): at a 500 ms SLO Clockwork and INFaaS reach comparable goodput of about 800 requests per second, but goodput collapses for both rivals below a 100 ms SLO, while only Clockwork continues to serve SLOs below 100 ms.
- On the Azure trace, about 987 unique models per minute (about 25% of models) have a cold start, but cold-start requests are only 1.3% of requests (126 per second on average).
- Scalability: with emulated workers, peak goodput grew linearly to 103,387 requests per second at 110 workers, after which the controller became the bottleneck (section 6.6).
- Prediction error: the paper reports 99th-percentile prediction errors of 144 and 55 for over- and under-prediction of inference time; the unit symbol was lost in my text extraction (presumably microseconds), so check the PDF before quoting.

## 6. Limitations
- **Authors:** no fault tolerance (a fault-tolerant centralised scheduler is needed, though predictability should make "grey failure" easier to detect); the prototype routes all inputs and outputs through the controller, which will bottleneck at scale (a tier of load balancers is planned); it assumes exclusive control of workers and a predictable network; it excludes pre- and post-processing and security.
- **Mine:** it relies on DNN inference being deterministic, which does not hold for LLM text generation where output length varies (ServerlessLLM, in [topic 06](../06-error-handling-fallback/fu-2024-serverlessllm.md), notes LLM latency depends on output length); image models only; no hosted APIs; the INFaaS comparison is across different hardware environments.

## 7. Relevance to the AI Request Router
- **Supports:** the per-request latency budget and the scoring engine (D-04, FR-05). Clockwork's rule is to execute a request only if the controller can predict it will finish in time, and to drop it otherwise. That is the same logic as the router excluding a backend whose predicted latency exceeds the budget.
- **Reuse:** (a) predict from recent measured durations per backend and model (the router's live-load term could keep the same kind of rolling profile); (b) report prediction error, as in Figure 10, for the router's own latency predictor; (c) treat unpredictability as a design caveat: because LLM output length varies, the router's predicted latency will be less exact than Clockwork's, so the evaluation should report prediction error; (d) the authors' own fault-tolerance and single-controller bottleneck remarks are direct support for the router's retry, circuit breaker and shared Redis state.
- **Not covered:** LLMs, per-prompt model choice, hosted APIs, circuit breaker.

## 8. How to use it in the report
- Chapter 2, section 2.4.5 (latency and deadlines), 2.4.8 and 2.4.6; Chapter 3, section 3.6.5 (latency prediction and hard budget constraint).
- Suggested synthesis sentence: "Clockwork (Gujarati et al., 2020) runs a request only when a central controller predicts it will meet its deadline; the proposed router applies the same admission idea to LLM backends, where output length makes prediction less exact, and adds a retry and circuit breaker that Clockwork leaves as future work."
- Link: [INFaaS](romero-2021-infaas.md) (compared in the paper), [AlpaServe](li-2023-alpaserve.md).

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Gujarati et al. (2020) | Predictable tail latency for DNN serving | Central controller schedules all loads and inferences from predicted durations; workers reject actions that miss their window | ResNet50 and other image models; 12 servers, 24 V100 GPUs; Azure traces; Clipper and INFaaS | 100 ms target met for 99.9999% of requests with thousands of models; goodput kept below 100 ms SLO where rivals collapse | Deterministic DNNs only; no fault tolerance; controller becomes bottleneck at scale |
