Status: DRAFT
Depends on: Project_Proposal_Hybrid_LLM_Router.docx; Project_Proposal_Hybrid_LLM_Router_Humanized.docx
Sources: Humanizer 12B Distilled (Gemma 4 12B) Q4_K_M via llama.cpp b11335; no hand rewording
Open items: team read-through of every entry

# Humanization change log (new proposal)

One entry per chunk the model rewrote and the checks accepted. Text under **After** is exactly what the model produced (line breaks joined). Chunks not listed here are unchanged.

## Chunk 114.2 (paragraph 114, ABSTRACT)

**Before**

The study follows Design Science Research, with development in six two-week Scrum sprints. The router will be built in Python with FastAPI behind one OpenAI-compatible endpoint. It will predict each model's quality on a prompt by combining a lightweight task classifier with embedding-based retrieval of scored past prompts, then select the cheapest model whose predicted quality meets a threshold within the request's cost cap and deadline.

**After**

The research follows a Design Science Research approach, implemented through 6 2-week Scrum sprints. The Python FastAPI router will have a single OpenAI-compatible endpoint. The router will predict the quality of each model for a specific prompt based on a simple task classifier and embedding-based look-up of the previously evaluated prompts (with scores), and select the lowest-cost model that has predicted quality exceeding a threshold within the request-specific cost limit and deadline.

## Chunk 212 (paragraph 212, LIST OF ABBREVIATIONS)

**Before**

This chapter explains the problem the proposed LLM request-routing gateway will address. It sets out the aim, objectives and research questions, followed by the proposed methods, scope, limitations and contributions.

**After**

This chapter will highlight the problem that the proposed LLM request-routing gateway is intended to solve. This chapter outlines the aim, objectives and research questions for the study before detailing the proposed methodology, scope, limitations and contributions.

## Chunk 214.0 (paragraph 214, 1.1 Background of the Study)

**Before**

A software application can access a large language model (LLM) through a hosted API or a locally operated deployment. The available deployments differ in their capabilities, charges, response times and availability; they can also perform differently on the same task. An application that sends every request to one model has a simple integration, but cannot adjust its choice for individual requests.

**After**

For a software application, a large language model (LLM) can be accessed via a hosted API or a locally run deployment. The characteristics of the deployments vary: their capabilities, fees, latency and availability. The performance of the deployments might differ when handling the same task. Integrating the application in the case where all requests are directed to a specific model is straightforward, but there is no possibility to change the model on a per request basis.

## Chunk 214.1 (paragraph 214, 1.1 Background of the Study)

**Before**

FrugalGPT, Hybrid LLM and RouteLLM show that selecting among models can change the balance between cost and response quality (Chen et al., 2023; Ding et al., 2024; Ong et al., 2025). Those results motivate this study, although they do not show that the proposed gateway will outperform simpler approaches.

**After**

FrugalGPT, Hybrid LLM, and RouteLLM have demonstrated that model selection can affect the trade-off between cost and response quality (Chen et al., 2023; Ding et al., 2024; Ong et al., 2025). While the results of these studies are the motivation for this study, they do not provide evidence that the proposed gateway will be more effective than simpler solutions.

## Chunk 215 (paragraph 215, 1.1 Background of the Study)

**Before**

The proposed router will sit between client applications and model deployments. Besides estimating which model may suit a request, it must validate that request, apply policies, select an eligible endpoint and report failures. Its operation must be observable. The project will therefore specify, build, deploy and test the gateway with attention to performance efficiency, reliability, security, compatibility and maintainability.

**After**

The proposed router will operate as the intermediary between the client applications and the model deployments. Aside from estimating which model might fit a request, it is responsible for validating it, policy enforcement, finding a suitable endpoint and signaling failures. The router's activities must be observable. For this reason, the project will define, develop, deploy and test the router considering the performance efficiency, reliability, security, compatibility and maintainability.

## Chunk 216 (paragraph 216, 1.1 Background of the Study)

**Before**

This work concerns the choice of a deployment for each request. It does not seek to replace the inference scheduler inside a model server. PagedAttention addresses a different part of the problem: memory management within model-serving infrastructure (Kwon et al., 2023). The gateway may use hosted and local endpoints where the necessary resources and permissions are available.

**After**

This work is about which deployment to use for a given request. It is not aiming to substitute the model server inference scheduler. PagedAttention looks at a different problem, which is the memory management problem inside model serving infrastructure (Kwon et al., 2023). The gateway can make use of hosted endpoints and local endpoints if the resources and permissions are there.

## Chunk 218 (paragraph 218, 1.1 Background of the Study)

**Before**

Existing benchmark data can support repeatable comparisons. RouterBench, for example, was designed to evaluate routing strategies (Hu et al., 2024). Replaying stored outputs cannot, however, establish actual network latency, provider availability or behaviour during injected failures. For that reason, offline experiments will be accompanied by integration tests and a limited live or controlled deployment evaluation. The project aims to produce a documented, deployable gateway and evidence of the benefits and overhead of the hybrid selection strategy.

**After**

With existing benchmarks there is potential to provide repeatable comparisons. For instance the RouterBench is intended to assess the routing strategies (Hu et al., 2024). However, it is not possible to retrieve real network latency, availability of provider or behaviour in the case of injecting failures by replaying stored outputs. Therefore, integration tests and a small-scale evaluation in live (or controlled) deployment will be performed alongside the offline experiments. The goal is to have a documentable gateway that can be deployed as well as to showcase gains and overhead of the hybrid selection strategy.

## Chunk 221 (paragraph 221, 1.2 Statement of the Problem)

**Before**

The growing use of Large Language Models (LLMs) has introduced challenges in managing response quality, cost, and latency. Many applications rely on a fixed model for all requests, regardless of their complexity. This can increase costs for simple tasks or reduce response quality for more complex ones. Research by Chen et al. (2023) and Ding et al. (2024) has demonstrated that selecting models based on request requirements can improve efficiency and reduce operational costs.

**After**

With the popularity of Large Language Models (LLMs), issues arise for controlling response quality, cost, and latency. Most of the time, a single model serves all requests without taking into account complexity. This means that it could be expensive when simple requests are made, or the response quality could decrease when complex requests are made. In recent works, Chen et al. (2023) and Ding et al. (2024) have shown how a model choice corresponding to request requirements can increase efficiency and lower operational cost.

## Chunk 225 (paragraph 225, 1.2 Statement of the Problem)

**Before**

Existing solutions do not always combine intelligent model selection, flexible model integration, performance monitoring, and reliable fallback mechanisms in one system. These limitations can make managing multiple LLMs difficult, potentially resulting in higher costs, slower responses, and inconsistent performance for developers and organizations.

**After**

Not all existing solutions offer intelligent model selection, flexible model integration, performance tracking, and fallback reliability all in one package. These shortcomings can lead to challenges in handling multiple LLMs effectively, which can increase costs, response times and inconsistency in performance for developers and organizations.

## Chunk 250 (paragraph 250, 1.4 Research Questions)

**Before**

The quality comparison will use an evaluation margin and scoring protocol fixed before the held-out results are examined. Any cost or latency reductions will be measured. Chapter Three will set out the hypotheses, metrics, sample selection and uncertainty analysis.

**After**

An evaluation margin and scoring method for quality will be pre-defined and used for the quality comparison. All cost and latency savings will be measured. The hypotheses, metrics, sample, uncertainty analysis will be defined in Chapter Three.

## Chunk 253 (paragraph 253, 1.5 Methodology Overview)

**Before**

The proposed LLM Router System will be developed using the Scrum framework, an Agile software development approach that emphasizes iterative development, teamwork, flexibility, and continuous improvement. Scrum was selected because it allows the project to be divided into smaller, manageable tasks and developed incrementally, making it easier to monitor progress, identify challenges, and incorporate improvements throughout the development process.

**After**

The Scrum framework will be used for the development of the proposed LLM Router System. Scrum is an Agile software development methodology focused on iterative development, collaboration, adaptability, and continuous enhancement. Scrum has been chosen because it enables breaking down the project into smaller, more manageable tasks and developing it iteratively. This facilitates tracking progress, identifying difficulties, and making improvements along the way.

## Chunk 255 (paragraph 255, 1.5 Methodology Overview)

**Before**

The development process will be organized into short iterations known as Sprints, with each Sprint focusing on specific features of the system. These features will include model integration, intelligent request routing, performance evaluation, cost and latency monitoring, and dashboard development. At the end of each Sprint, the team will review the completed work, test the implemented features, and gather feedback to guide subsequent development.

**After**

The development of the system will be divided into small iterations called Sprints, which will concentrate on certain parts of the system. These features may include model integration, intelligent request routing, system performance assessment, cost and latency tracking, and developing dashboards. The deliverables of each Sprint will be examined, tested with the features implemented, and evaluated with feedback. This feedback will inform further development.

## Chunk 257 (paragraph 257, 1.5 Methodology Overview)

**Before**

The project team will maintain a Product Backlog containing the system requirements, features, and tasks to be implemented. During Sprint Planning, tasks will be prioritized and assigned to team members based on the project's objectives. Regular team meetings will be conducted to discuss progress, address challenges, and ensure effective collaboration. Sprint Reviews and Retrospectives will also be used to evaluate completed work and improve the development process.

**After**

They will keep a Product Backlog which will have all the requirements, features and tasks that needs to be done for the system. During Sprint Planning, the tasks will be prioritized and assigned to members based on the goals of the project. Periodic team meetings will be held to discuss progress, problems and team collaboration. Sprint Reviews and Retrospectives will be held to review what has been done and improve the development process.

## Chunk 258 (paragraph 258, 1.5 Methodology Overview)

**Before**

By adopting Scrum, the team aims to ensure continuous testing, effective collaboration, adaptability to changing requirements, and gradual delivery of a functional LLM Router System. This approach will also support the integration and evaluation of different language models, including cloud-based and locally hosted models, while allowing the system to evolve based on testing results and project requirements.

**After**

The team is hoping to ensure continuous testing, collaborative work, flexibility to changing requirements, and incremental delivery of working LLM Router System with Scrum. The use of Scrum will also help in integrating and testing various language models (cloud and locally hosted models) and will enable the system to grow based on the testing results and project requirements.

## Chunk 262 (paragraph 262, 1.6 Significance of the Study)

**Before**

The study will add a controlled comparison of a hybrid predictor against simpler routing baselines on shared data, with ablations, at a time when benchmarks report that many routers do not beat the best single model (Li et al., 2026). It will also separate operational fallback from quality-based cascading in evaluation, which the literature often reports together. A negative or inconclusive result is still useful evidence for students and researchers choosing a routing method.

**After**

It will provide a controlled comparison of a hybrid predictor against naive routing baselines on common data (with ablations) in the context of benchmarks suggesting that many routers are not outperforming the single best model (Li et al., 2026). It will disentangle operational fallback from quality based cascading for evaluation that is often conflated in the literature. Even a negative or inconclusive finding is valuable data for students and researchers deciding on a routing strategy.

## Chunk 265 (paragraph 265, 1.7 Scope of the Study)

**Before**

The study covers the requirements, design, implementation, deployment, testing and empirical evaluation of a request-level LLM routing gateway. It is intended for developers and organisations that integrate multiple LLM deployments, without restriction to a country or user group.

**After**

The paper discusses the needs, design, implementation, deployment, testing and empirical evaluation of a request level LLM routing gateway. The target audience is developers and organisation that are using multiple LLM deployments, it is not limited to a country or user group.

## Chunk 270 (paragraph 270, 1.8 Limitations of the Study)

**Before**

API quotas, local computing resources and budgets may restrict the deployments tested. The team will record the model pool and limit its conclusions to those configurations.

**After**

Due to API quotas, local compute resources, and budgets, not all of the possible deployments will be tried. The team will log the model pool and only draw conclusions for these deployments.

## Chunk 275 (paragraph 275, 1.8 Limitations of the Study)

**Before**

Time and resources may limit concurrency testing and the size of any developer evaluation. Test conditions and sample sizes will be reported, and claims will remain within the observed evidence.

**After**

Concurrency testing may be limited by time and resources. The extent of evaluation by developers may also be limited. Sample sizes and test conditions will be made known. Claims will be confined to the evidence.

## Chunk 280 (paragraph 280, 1.9 Contributions of the Project)

**Before**

A telemetry and monitoring dashboard showing individual and aggregated routing decisions, estimated or recorded model costs, response latency, provider status and fallback events. What it can display will depend on the information made available by the integrated model providers.

**After**

Telemetry and monitoring dashboard showing per- and aggregate-routing decisions, estimated or actual costs of the models, latency of response, provider status and fallback events. The exact nature of what can be shown depends on what the integrated model providers will allow to be exposed.

## Chunk 285 (paragraph 285, 1.10 Organisation of the Report)

**Before**

Chapter One presents the problem, aim, objectives, research questions, significance, scope, limitations and expected contributions. Chapter Two reviews routing research, software infrastructure and existing systems to support the proposed design. Chapter Three describes the requirements and architecture, methods for development and deployment, data and evaluation plan, ethical considerations, risks, schedule and resources. Implementation results and conclusions will appear in the final project report.

**After**

Chapter One defines the problem, aim, objectives, research questions, importance of work, scope, limitations and anticipated contributions. Chapter Two provides literature review of routing research, software framework and current systems to motivate the proposed design. Chapter Three explains the requirements, architecture, development and deployment approach, data and evaluation strategy, ethical issues, risks, timeline and resources. Implementation results and conclusions will be reported in the final project report.

## Chunk 301 (paragraph 301, LITERATURE REVIEW)

**Before**

This chapter reviews the work that the project builds on. Section 2.1 explains how the literature was found and selected. Section 2.2 sets out the concepts and the theoretical lens, and Section 2.3 compares the techniques available for each part of the router. Section 2.4 reviews related work in six themes, Section 2.5 compares existing gateways, and Section 2.6 summarises the reviewed works in a table. Section 2.7 states the research gap and maps it to the objectives, and Section 2.8 closes the chapter.

**After**

This chapter covers the literature under study for this project. Section 2.1 discusses the method of literature search and selection. Section 2.2 describes the concepts and the theoretical perspective. Section 2.3 compares the techniques for different parts of router. Section 2.4 discusses the related works in six different themes. Section 2.5 focuses on the comparison of different gateways. Section 2.6 lists the summary of reviewed works in table. Section 2.7 discusses the research gap and its correspondence with objectives. Section 2.8 concludes this chapter.

## Chunk 303 (paragraph 303, 2.1 Review Methodology)

**Before**

The review followed the step-by-step approach taught in the module: the topic was divided into sub-topics, Boolean search strings were written for each, and the results were screened against stated criteria (Kitchenham & Charters, 2007). The project title was split into nine sub-topics: routing algorithms; prompt difficulty and suitability prediction; load balancing; cost reduction; latency; error handling and fallback; testing and benchmarking; gateway and serving system design; and retrieval-based and multi-turn routing.

**After**

The review process was carried out according to the process described in the module (break down into sub-topics, construct Boolean search phrases for each sub-topic, and sift through the results based on given criteria) (Kitchenham & Charters, 2007). Nine sub-topics were derived from the project title (routing algorithms, predicting prompt difficulty and suitability, load balancing, cost reduction, latency, error handling and fall-back strategy, testing and benchmarking, gateway design and serving system design, retrieval-based routing and multi-turn routing).

## Chunk 307 (paragraph 307, 2.1 Review Methodology)

**Before**

Preprints were kept where they are the only source on a sub-topic, mainly for 2026 work, and are labelled as preprints in the reference list. Where a preprint later appeared in a peer-reviewed venue, the venue version is cited. Vendor documentation for existing gateways was read on 31 October 2026 and is treated as grey literature.

**After**

Preprints were retained in the reference list if they were the only reference to a sub-topic (mostly 2026 work), and explicitly identified as such in the reference list. If there was a peer-reviewed version of the preprint then this is used. Documentation of existing gateways as provided by the vendor, which was reviewed on 31 October 2026 is considered as grey literature.

## Chunk 310 (paragraph 310, 2.2.1 Prompt-aware model routing)

**Before**

Prompt-aware routing chooses a model for a request using information available about the prompt. A rule, a learned score or a model-specific performance estimate can guide the choice. Routing before generation differs from a cascade, which may call another model after inspecting an earlier answer. That extra call can change both cost and latency. FrugalGPT illustrates cascading, while Hybrid LLM and RouteLLM study selection before generation (Chen et al., 2023; Ding et al., 2024; Ong et al., 2025).

**After**

Prompt-aware routing refers to selecting a model based on prompt-available information. This selection can be done using a rule, a learned score, or an estimate of model performance. The process is different from a cascade, in which a subsequent model might be invoked based on examining a previous output. The additional call to the model can alter both latency and cost. FrugalGPT shows an example of a cascade. Hybrid LLM and RouteLLM explore the selection prior to generation (Chen et al., 2023; Ding et al., 2024; Ong et al., 2025).

## Chunk 312 (paragraph 312, 2.2.2 Hybrid suitability estimation)

**Before**

The proposed suitability estimator will combine a task classification with embedding-derived evidence from previously evaluated requests. CSCR maps prompts and models into a shared representation, whereas EmbedLLM learns representations from model performance on questions (Shirkavand et al., 2025; Zhuang et al., 2025). Neither result proves that the proposed combination is better. An ablation of each component will test its contribution.

**After**

The proposed suitability estimator will use a task classification and embedding-based information from previously assessed requests. CSCR represents prompts and models in the same space. EmbedLLM finds representations from model performance on questions (Shirkavand et al., 2025; Zhuang et al., 2025). Both results do not show that combining them is better. Ablation of each part will assess their contribution.

## Chunk 315 (paragraph 315, 2.2.3 Constrained routing and reliability)

**Before**

Design science provides a useful research lens for this work: it links the creation of an artefact to its evaluation against a problem and stated requirements (Hevner et al., 2004). Here the artefact is the proposed gateway, and the evaluation will examine both its routing decisions and operational behaviour. Chapter Three will describe the method and acceptance criteria.

**After**

The methodology of design science is a useful perspective for research in this area. Design science relates the creation of an artefact to the assessment of the artefact against a problem and requirements (Hevner et al., 2004). The artefact in this case is the proposed gateway. Its assessment will include both routing decisions and operations of the gateway. Chapter Three will discuss the method and acceptance criteria.

## Chunk 326 (paragraph 326, 2.3.3 Serving performance and latency)

**Before**

Total latency includes gateway processing, any queueing and the time taken by the selected deployment. Etalon distinguishes delay before the first token from the timing of later tokens, while DistServe studies prefill and decoding in serving infrastructure (Agrawal et al., 2024; Zhong et al., 2024). The project will measure gateway overhead and completion time, and first-token delay where the interface permits. It will not modify the inference engine.

**After**

The latency comprises gateway time, queue time and the time spent by the deployment of choice. Etalon has a separation of pre first token delay from subsequent token timings. Pre fill & decoding times in serving infrastructure are investigated in DistServe (Agrawal et al., 2024) (Zhong et al., 2024). Gateway time and completion time will be measured as well as pre first token delay if it is exposed. The inference engine will not be altered.

## Chunk 334.1 (paragraph 334, 2.4.1 Learned pre-generation routing between models)

**Before**

Shirkavand et al. (2025) added cost bands to contrastive training and model "fingerprints" so that new models can be added without retraining, and reported the best area under the deferral curve on three benchmarks. These results come from accuracy-only or price-only settings with fixed model prices.

**After**

Shirkavand et al. (2025) applied cost bands to contrastive training and model "fingerprints" to add new models without re-training, and they achieved the highest area under deferral curve on three benchmarks. Results here are from accuracy-only or price-only (with fixed model prices).

## Chunk 335.0 (paragraph 335, 2.4.1 Learned pre-generation routing between models)

**Before**

The closest structural match to this project is Šakota et al. (2024). Their method trains a small DistilBERT meta-model to predict each model's success on a prompt and then assigns prompts to models under a budget by integer programming; they report about a 63% cost reduction at the accuracy of the largest model, with a calibrated meta-model.

**After**

This structure is most similar to Šakota et al. (2024). They train a small meta-model (DistilBERT) that predicts the likelihood of success for each model for a prompt, then dispatch prompts to models under a budget using integer programming, achieving roughly 63% cost reduction (for the largest model’s accuracy) (with a calibrated meta-model).

## Chunk 340 (paragraph 340, 2.4.2 Embedding retrieval and historical-performance features)

**Before**

These studies agree that embeddings of past prompts carry much of the routing signal, which supports including retrieval in the hybrid. They also share weaknesses: labels come from benchmark scoring, similar prompts are easy to find inside a benchmark but may be absent in real traffic, and none reports calibration or confidence intervals (Varangot-Reille et al., 2026a). Because plain k-NN is so competitive, this project treats it as a required baseline: the hybrid must beat k-NN alone to justify the classifier.

**After**

All the studies seem to agree that past prompt embeddings retain a strong routing signal, supporting the inclusion of retrieval in the hybrid, and all have some weaknesses such as using benchmark score as a label, similarity can be easily found within a benchmark but may not exist in actual traffic, and none of them include any calibration or confidence intervals (Varangot-Reille et al., 2026a). Since vanilla k-NN is quite competitive this project considers that it is a mandatory baseline, i.e. the hybrid needs to outperform k-NN alone to justify the classifier.

## Chunk 342 (paragraph 342, 2.4.3 Cascades and joint quality–cost–latency optimisation)

**Before**

The third group optimises cost and quality jointly, either by calling models in sequence or by solving a selection problem. Chen et al. (2024a) built FrugalGPT, a learned cascade over 12 APIs that reported up to 98% cost saving at GPT-4 accuracy on three datasets. Aggarwal et al. (2024) used few-shot self-verification to decide when to escalate and reported over 50% cost reduction at comparable performance with as few as 50 training examples. Both pay the latency of every model tried, and both depend on in-distribution labels.

**After**

The third approach balances cost and quality either by sequentially invoking models or by solving a selection problem. In the former, Chen et al. (2024a) introduced FrugalGPT, a learned cascade of 12 APIs that saved up to 98% cost (with GPT-4 accuracy) across 3 datasets. In the latter, Aggarwal et al. (2024) employed few-shot self-verification for escalating decision and achieved over 50% cost savings with similar performance (using as few as 50 training examples). Both approaches incur latency for all invoked models. They both require in-distribution labels.

## Chunk 344.0 (paragraph 344, 2.4.3 Cascades and joint quality–cost–latency optimisation)

**Before**

RouteBalance (Da & Kalyvianaki, 2026) is the closest prior work to joint quality–cost–latency selection. It scores model instances on predicted quality, latency and cost with a k-NN quality estimator and live queue estimates from vLLM workers, and reports 2.6 to 4.1 times lower latency than an enhanced BEST-Route baseline at high load.

**After**

The closest related prior art to join quality-cost-latency selection is RouteBalance (Da & Kalyvianaki, 2026), which predicts quality, latency and cost for model instances and scores them using a k-NN quality estimator and vLLM worker's live queue estimates, yielding 2.6-4.1X reduction of latency compared to enhanced BEST-Route baseline under high load.

## Chunk 346.0 (paragraph 346, 2.4.4 Latency targets and deadline-aware selection)

**Before**

The fourth group concerns meeting latency targets, mostly in serving systems below the gateway. INFaaS (Romero et al., 2021) lets callers state accuracy, latency and cost requirements and selects a model variant per query, achieving 1.6 times fewer service-level objective (SLO) violations and up to 21.6 times lower cost, with only 2.2 to 3.5 ms of median selection overhead.

**After**

The fourth set of problems is about achieving latency goals (mostly for sub-gateway serving systems). INFaaS (Romero et al., 2021) allows to specify accuracy, latency and cost goals by the users and chooses the model variant for each query. It can reduce the number of service-level objective (SLO) violations by 1.6x and reduces the cost up to 21.6x with only 2.2-3.5 ms median selection overhead.

## Chunk 351.1 (paragraph 351, 2.4.5 Failure handling and fallback)

**Before**

FailureAtlas (Pandey & Singh, 2026b) catalogued gateway failures from the issue trackers of LiteLLM, Portkey and OpenRouter and found that the worst were silent, returning a success status with an invalid body. Aderaldo and Mendonça (2026) provide a peer-reviewed method for choosing retry settings by fault injection.

**After**

FailureAtlas (Pandey & Singh, 2026b) identified gateway failures from the issue trackers of LiteLLM, Portkey and OpenRouter, observing that silent failures (i.e. success status but invalid body) were the worst. Aderaldo and Mendonça (2026) describe a peer-reviewed approach to configure retry parameters via fault injection.

## Chunk 354.0 (paragraph 354, 2.4.6 Evaluating routers)

**Before**

The last group concerns how routers are evaluated. RouterBench (Hu et al., 2024) stores responses from 11 models across about 405,000 samples and plots routers on a cost–quality plane; it found that learned routers barely beat a simple non-learned router. LLMRouterBench (Li et al., 2026) re-evaluated ten routers on 21 datasets and 33 models under shared conditions and found that routers converge, many do not beat the best single model, and a large gap to the oracle remains.

**After**

The last group addresses router evaluation. RouterBench (Hu et al., 2024) which aggregates the responses from 11 models on ~405k samples, creates a cost-quality plane for the routers and showed little gain for the learned routers compared to a naive non-learned router. LLMRouterBench (Li et al., 2026) re-evaluated the ten routers on 21 datasets and 33 models under the same settings, showing that routers tend to converge, most fail to outperform the strongest model alone, and that there is still large room for improvement compared to the oracle.

## Chunk 356 (paragraph 356, 2.4.6 Evaluating routers)

**Before**

These evaluations set the benchmark for this project. They show that a new router must be compared against the best single model, cheap baselines and the oracle under shared splits; that router overhead must be measured; and that judge-scored labels need caution. None measures live latency on real providers or injected failures, which this project adds alongside the standard offline comparison.

**After**

These evaluations are the bar for this project. They demonstrate the need to compare against the best single-model, cheap baselines and oracle for same splits. They show the need to measure router overhead. They demonstrate the danger in using judge-scored labels. They do not perform any evaluation of live latency on live providers, nor of injected failures which this project includes in addition to the usual offline comparison.

## Chunk 358.1 (paragraph 358, 2.5 Review of Existing Systems)

**Before**

LiteLLM is an open-source router and proxy that balances traffic across deployments of a named model with least-busy, latency-based and cost-based strategies, plus fallbacks; its Auto Router sorts requests into complexity tiers using heuristics, an LLM classifier or adaptive selection (Dholakia, 2026; LiteLLM, n.d.-a, n.d.-b). It also supports self-hosted vLLM deployments (LiteLLM, n.d.-d).

**After**

LiteLLM is an open-source router and proxy for load balancing (least busy, latency based, cost based load-balancing + fallbacks) across multiple deployments of the same named model. It has an Auto Router that heuristically classifies requests into different complexity tiers (or via LLM classifier or adaptive selection). (Dholakia, 2026; LiteLLM, n.d.-a,n.d.-b). It supports self-hosted vLLM deployments. (LiteLLM, n.d.-d)

## Chunk 370 (paragraph 370, 2.7 Research Gap and Justification of the Study)

**Before**

Despite improvements in LLM routing, existing solutions do not always provide a simple and flexible way to manage multiple language models while considering response quality, cost, latency, and user requirements. Some solutions also offer limited support for integrating locally hosted models, monitoring performance, and automatically switching to another suitable model when one becomes unavailable.

**After**

Although LLM routing has improved, current offerings do not always offer a straightforward and flexible approach to handle multiple language models, taking response quality, cost, latency and user requirements into consideration. There are also limited options to integrate local hosted models, tracking performance, or gracefully fallback to an alternate adequate model when one goes down.

## Chunk 371 (paragraph 371, 2.7 Research Gap and Justification of the Study)

**Before**

These limitations can make it difficult for developers and organizations to manage their LLM applications efficiently, potentially leading to higher costs, slower responses, and inconsistent performance. There is therefore a need for a system that combines intelligent model selection, flexible model integration, performance monitoring, and reliable fallback mechanisms in one platform.

**After**

These constraints may hinder effective control and management of LLM applications for developers and organizations, resulting in higher costs, slower response times, and inconsistent performance. Therefore, there is a need for a platform that can intelligently select models, integrate models flexibly, monitor performance, and provide dependable fallback solutions all in one.

## Chunk 372.0 (paragraph 372, 2.7 Research Gap and Justification of the Study)

**Before**

Reading the limitations column of Table 2.4 from top to bottom, four gaps emerge. First, learned and retrieval-based predictors are each shown to work, and plain k-NN is often as good as learned routers, but no study tests whether combining a lightweight classifier with embedding retrieval improves on either alone under the same data and splits (Shnitzer et al., 2023; Varangot-Reille et al., 2026a; Zhuang et al., 2025).

**After**

The top-to-bottom read of the limitations in Table 2.4 has four gaps: (1) the use of learned and retrieval based predictors is demonstrated to be effective, often naive k-NN can be as good as learned routers, but no work is done to determine if using light weight classifier with embedding based retrieval is better than learned or retrieval-based methods on the same data and splits (Shnitzer et al., 2023; Varangot-Reille et al., 2026a; Zhuang et al., 2025).

## Chunk 372.1 (paragraph 372, 2.7 Research Gap and Justification of the Study)

**Before**

Second, selection under hard per-request cost caps and deadlines across local and hosted models is rarely evaluated: most methods optimise average cost on static prices, and the one joint quality–cost–latency study is a single-family preprint (Da & Kalyvianaki, 2026; Dekoninck et al., 2025; Šakota et al., 2024). Third, fallback for LLM gateways has thin evidence, consisting of two small preprints and general microservice studies, and none chooses the fallback model by predicted quality and remaining budget (Aderaldo & Mendonça, 2026; Pandey & Singh, 2026a, 2026b).

**After**

Second, few methods consider selection for stringent per request cost limits and deadlines for local and hosted models. Most methods focus on average cost under static pricing; the single joint quality-cost-latency analysis is a single family preprint (Da & Kalyvianaki, 2026; Dekoninck et al., 2025; Šakota et al., 2024). Third, few studies consider LLM gateway fallback. There is limited evidence with two small preprints and microservice studies in general. None of them select a fallback model based on predicted quality and remaining budget (Aderaldo & Mendonça, 2026; Pandey & Singh, 2026a, 2026b).

## Chunk 372.2 (paragraph 372, 2.7 Research Gap and Justification of the Study)

**Before**

Fourth, shared-condition benchmarks report that many routers fail to beat the best single model, yet most papers do not compare against simple baselines or separate each component's contribution (Hu et al., 2024; Li et al., 2026; Lu et al., 2026).

**After**

(4) Shared-condition benchmarks also show that many routers do not outperform the best single model. However, few works conduct comparisons with simple baselines or separate out contributions from different parts (Hu et al., 2024; Li et al., 2026; Lu et al., 2026).

## Chunk 377.0 (paragraph 377, 2.8 Chapter Summary)

**Before**

The review found that the building blocks for prompt-aware routing are mature. Small predictors can estimate model-specific quality from the prompt, embedding retrieval of past outcomes is a strong and cheap signal, constrained formulations of the cost–quality trade-off exist, and resilience patterns for remote calls are well understood. It also found that these blocks are rarely combined and evaluated together under hard per-request limits, that evidence on LLM gateway fallback is thin, and that shared benchmarks often show complex routers failing to beat simple ones.

**After**

The review concluded that the building blocks for prompt-aware routing are mature (small predictors that can gauge model specific quality from the prompt, strong and cheap signal from embedding retrieval of past outcomes, known constrained cost-quality trade-off formulations, well known resilience patterns for remote calls). It also found that: these blocks are seldom used and assessed in combination with hard per-request limits; the evidence of LLM gateway fallback is scarce; complex routers often do not outperform simple routers for common benchmarks.

## Chunk 382.0 (paragraph 382, 3.1 Research and Development Methodology)

**Before**

The project will use Design Science Research (DSR), which builds an artefact to solve a relevant problem and evaluates it rigorously (Hevner et al., 2004). DSR suits this project because its main output is a working router and its research questions are about whether that artefact performs better than alternatives.

**After**

Design Science Research (DSR) method will be used in this project. DSR creates an artefact to solve a problem of interest and then rigorously evaluates it (Hevner et al., 2004). DSR is appropriate for this project as the primary deliverable is a functioning router and the research questions revolve around whether that artefact is superior to other options.

## Chunk 382.2 (paragraph 382, 3.1 Research and Development Methodology)

**Before**

The evaluation itself will be a controlled offline experiment with paired comparisons (Wohlin et al., 2012).

**After**

The evaluation will be a controlled offline experiment of paired comparisons (Wohlin et al., 2012).

## Chunk 383.0 (paragraph 383, 3.1 Research and Development Methodology)

**Before**

Development will use Scrum with six two-week sprints (Schwaber & Sutherland, 2020). Scrum fits because the predictor and selection thresholds can only be tuned after the gateway, adapters and data pipeline are working, and early results may change the design. Solomon will act as Scrum Master and coordinate with the supervisor, who will act as product owner for priorities.

**After**

Development will be Scrum, with six sprints of two weeks each (Schwaber & Sutherland, 2020). Scrum is suitable as the predictor and selection threshold tuning can only be done once the gateway, adapters and data pipeline are in place, and early results may require changes to design. Scrum Master will be Solomon. Coordination will be done with the supervisor (product owner for priorities).

## Chunk 389 (paragraph 389, 3.2 Requirements Elicitation)

**Before**

Provider API references will be analysed for request formats, error codes, rate-limit behaviour, token pricing and timeouts, and the OpenAI-compatible chat API will be used as the interface contract.

**After**

The OpenAI-compatible chat API will serve as the interface contract. Provider API references will be examined for request format, error codes, rate limiting behaviour, token cost and timeout.

## Chunk 391 (paragraph 391, 3.2 Requirements Elicitation)

**Before**

Gateway issue reports and incident studies (Pandey & Singh, 2026b; Yan et al., 2025) will be used to list failure scenarios the reliability controller must handle.

**After**

From gateway issue reports and incident study (Pandey & Singh, 2026b; Yan et al., 2025), failure scenarios to be considered by reliability controller will be listed.

## Chunk 392 (paragraph 392, 3.2 Requirements Elicitation)

**Before**

Wahida and Kabiru will extract candidate requirements into a shared sheet, recording the source of each. The whole team will then group them, write them as user stories with acceptance criteria, and prioritise them with MoSCoW in the Sprint 1 review. If the supervisor asks for user input, a short questionnaire for five to eight student and junior developers will be added, with an information sheet and consent form placed in Appendix C.

**After**

Wahida and Kabiru will capture the candidate requirements and put it in one sheet (with sources). The team will then cluster, write (including user stories with acceptance criteria) and prioritise (with MoSCoW) the requirements during the Sprint 1 review. If there is a request for user input from the supervisor, there will be a short questionnaire to five to eight students and junior developers which will be added together with information sheet and consent form in Appendix C.

## Chunk 395.0 (paragraph 395, 3.3.1 Description of the Existing System)

**Before**

In current practice a developer chooses one model, writes its name into the code or configuration, and sends every request to it through the provider's SDK or an OpenAI-compatible gateway. If a gateway is used, it may balance load across copies of that model and fall back to a named alternative after an error (LiteLLM, n.d.-a; Portkey, n.d.-b).

**After**

In the current setup, the developer picks a model, puts its name in code or config, and sends all requests to that model through the provider SDK or OpenAI-compatible gateway. If they use a gateway, it could distribute requests among instances of this model and, on error, switch to another named model (LiteLLM, n.d.-a; Portkey, n.d.-b).

## Chunk 395.1 (paragraph 395, 3.3.1 Description of the Existing System)

**Before**

Where per-prompt routing is offered, the developer enables a vendor feature and accepts its decisions without access to an evaluation of them (Dholakia, 2026; OpenRouter, n.d.-c). Cost is reviewed after the fact on the provider's billing page.

**After**

If the per-prompt routing exists, the developer activates the vendor feature (and goes along with the vendor decisions without being able to see an evaluation of those decisions) (Dholakia, 2026; OpenRouter, n.d.-c). They look at costs afterwards on the billing page from the provider.

## Chunk 406.1 (paragraph 406, 3.4.1 Description of the Proposed System)

**Before**

If the call fails in a retryable way, the reliability controller updates the provider's health, re-runs selection on the remaining eligible models and tries again within bounded attempts. Every decision is logged with its predictions and reason, and the response carries routing metadata.

**After**

If it fails in a way that can be retried, the provider's health is changed in reliability controller, and the remaining eligible models are selected again and retried (within bounded attempts). Each decision is logged with its predictions and reason. There are routing metadata in the response.

## Chunk 406.2 (paragraph 406, 3.4.1 Description of the Proposed System)

**Before**

An administrator registers models and prices, sets policy thresholds and reviews usage on a dashboard. An evaluator runs replay and fault-injection experiments through the same code.

**After**

The administrator registers models and prices, sets policy thresholds, and views a dashboard to see usage. The evaluator uses the same code to do replay and fault injection experiments.

## Chunk 407 (paragraph 407, 3.4.1 Description of the Proposed System)

**Before**

The system has five modules: the gateway API, the constraint filter, the prompt analyser and suitability predictor, the selection policy, and the reliability controller with provider adapters. A PostgreSQL database stores the model registry, requests, decisions, attempts, health events and quality scores.

**After**

The system consists of five different modules: The gateway API, Constraint filter, The prompt analyzer and suitability predictor, Selection policy, and Reliability controller with provider adapters.  The model registry, request, decision, attempt, health event, quality score are stored in the PostgreSQL database.

## Chunk 432.1 (paragraph 432, 3.6.1 System Architecture)

**Before**

Figure 3.3 shows the architecture and its deployment on the two laptops. Machine 1 runs the router, database and local model; Machine 2 runs the evaluation harness, load generator and mock provider so that test traffic does not compete with the router for resources.

**After**

Figure 3.3 depicts the architecture and how it is deployed on the two laptops: the router, database, and local model are running on Machine 1, while the evaluation harness, load generator, and mock provider are running on Machine 2 to avoid contention between the router and the test traffic.

## Chunk 438.0 (paragraph 438, 3.6.3 Behavioural Design (Sequence and Activity Diagrams))

**Before**

For a normal request, the gateway calls the constraint filter, then the prompt analyser, predictor and policy in sequence, then the reliability controller, which calls the chosen adapter and records the attempt. For a failed request, the controller records the failure on the breaker, asks the policy to select again from the models that remain eligible with the reduced budget and deadline, and calls the next adapter.

**After**

In the case of a normal request, the gateway will call constraint filter, then prompt analyser, predictor, policy in order, and finally the reliability controller (which in turn will call the chosen adapter and make a log of the attempt).  In the case of failure, the controller will log the failure in the breaker, ask policy to try again with the remaining available models (with reduced budget and deadline), and call the next adapter.

## Chunk 438.1 (paragraph 438, 3.6.3 Behavioural Design (Sequence and Activity Diagrams))

**Before**

Figure 3.5 in Section 3.6.5 shows this flow as an activity diagram. Sequence diagrams for the normal and fallback paths will be included in the final report.

**After**

The flow is depicted in an activity diagram in Figure 3.5 of Section 3.6.5. Sequence diagrams for normal path and fallback will also be included in the final report.

## Chunk 440.1 (paragraph 440, 3.6.4 Database Design)

**Before**

A full data dictionary will be given in the final report.

**After**

The final report will provide a complete data dictionary.

## Chunk 453.0 (paragraph 453, 3.6.5 Algorithm and Model Design)

**Before**

On a timeout, rate limit, server error or invalid response, the controller records a failure on that model's breaker. A breaker opens after a set number of consecutive failures, rejects calls during a cool-down, and lets one trial request through when half-open. The controller then removes the failed model, subtracts the cost already consumed from the cap and the elapsed time from the deadline, and re-runs selection.

**After**

On a timeout, rate limit, server error or invalid response, the controller marks a failure on that model's breaker. After N consecutive failures the breaker opens, then will reject requests during cool-down. When half-open, only one trial request is allowed. The controller removes the failed model, deducts consumed cost from the cap and elapsed time from the deadline, then re-selects.

## Chunk 457.0 (paragraph 457, 3.6.6 User Interface Design)

**Before**

The system's main interface is the API. The administrator dashboard is a secondary, read-mostly interface with four views: an overview with request count, spend, p95 latency and fallback rate; a request log showing the chosen model and the reason for each decision; a model page with prices, capabilities and breaker state; and an experiments page listing replay runs and their quality–cost curves.

**After**

The API is the primary interface of the system. The admin dashboard is a secondary interface used to read the system, with four views: overview (number of requests, spend, p95 latency and fallback rate), request log (model that was used, rationale behind every decision), model view (prices, capabilities and breaker state) and experiments view (list of replay runs and quality-cost curves).

## Chunk 461.1 (paragraph 461, 3.6.7 Security and Privacy Design)

**Before**

If any personal data is processed later, the design will follow the Nigeria Data Protection Act 2023, including purpose limitation and data minimisation (Federal Republic of Nigeria, 2023).

**After**

If any personal data is to be processed subsequently, the architecture will conform to the Nigeria Data Protection Act 2023 (such as purpose limitation, data minimisation). (Federal Republic of Nigeria, 2023)

## Chunk 470 (paragraph 470, 3.7 Data Collection and Preparation)

**Before**

The quantised local model may not match the full-precision model scored in the benchmark. A stratified sample of about 300 prompts will be run on the local model and scored with the benchmark's method; if agreement with the stored labels is poor, the local model will be labelled from its own outputs on that sample only and the limitation reported.

**After**

The quantised local model may differ from the full precision model evaluated in the benchmark, and a stratified sample of ~300 prompts will be evaluated on the local model using the benchmark evaluation procedure. If there is poor correlation with the stored labels then the labels for the local model will be set based only on the output of the local model for this sample of prompts, and this will be noted as a limitation.

## Chunk 482 (paragraph 482, 3.9 Evaluation Plan)

**Before**

Every comparison will include: always the frontier model; always the cheapest eligible model; rule-based routing by task category; k-NN retrieval only; classifier only; the weighted-utility policy; and the oracle (the cheapest model that answered acceptably, computed from stored labels) as an upper bound. A simpler baseline matching the hybrid is a valid result and will be reported as such.

**After**

All comparisons will contain: always the frontier model, always the least expensive eligible model, rule-based routing by task type, only k-NN retrieval, only classifier, weighted utility policy, and oracle (least expensive model giving an acceptable answer, calculated using stored labels), as an upper bound. Note: a simpler baseline equivalent to the hybrid is a valid outcome, and will be presented that way.

## Chunk 483 (paragraph 483, 3.9 Evaluation Plan)

**Before**

Because all policies are run on the same prompts, comparisons are paired. Binary outcomes (acceptable or not) will use McNemar's test, and per-request cost and latency will use the Wilcoxon signed-rank test (Wohlin et al., 2012). Non-inferiority will be judged by whether the lower bound of the 95% confidence interval for the quality difference lies above the negative margin. Live pilot results will be reported separately from offline replay because they use fewer prompts and real network conditions.

**After**

As the same prompts will be used for all policies, paired comparisons are made. For binary cases (acceptable or not), McNemar's test will be used. For per-request cost and latency, the Wilcoxon signed-rank test is used (Wohlin et al., 2012). Non-inferiority will be evaluated based on whether the lower bound of 95% confidence interval for the difference in quality is larger than the negative margin. Live pilot results are reported separately from offline replay. This is because they use fewer prompts and actual network conditions.

## Chunk 485.0 (paragraph 485, 3.10 Ethical Considerations)

**Before**

The project does not plan to recruit human participants, so no consent process is required for the core evaluation. The team has recorded the position that formal ethical approval is not needed; this will be confirmed in writing with the supervisor before Sprint 1, and if approval is required the team will apply to the university's research ethics committee before any data collection.

**After**

The project is not recruiting human participants, therefore there is no need for a consent procedure for the core evaluation. The stance that ethical approval is not required has been documented but the team will get this confirmed in writing from the supervisor before Sprint 1, and will apply for ethical approval from the university research ethics committee prior to collecting data if this is required.

## Chunk 492 (paragraph 492, 3.12 Work Plan)

**Before**

The work plan follows six two-week sprints across the two semesters, with report writing overlapping implementation. Owners follow the team roles in the statement of contributions.

**After**

Work is planned in 6x2-weeks sprints throughout both semesters (with report writing interleaved with implementation). The team roles are as specified in the statement of contributions. Owners stick to the team roles.

## Chunk 496 (paragraph 496, 3.12 Work Plan)

**Before**

The exact calendar weeks will be aligned with the university timetable once it is published. Chapters Four and Five will be drafted during Sprints 5 and 6.

**After**

The timing of the calendar weeks will be adjusted to match the university timetable once it is available. Chapters Four and Five will be written in Sprints 5 & 6.
