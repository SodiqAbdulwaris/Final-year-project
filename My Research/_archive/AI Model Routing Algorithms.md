# AI Model Routing Algorithms: Comprehensive Literature Review and Research Notes

**Research Area:** Software Engineering for AI-Powered Systems (SE4AI)

**Specialisation:** Large Language Model Operations (LLMOps), LLM Serving, and Inference Optimisation

**Focus:** Cost-Aware, Prompt-Aware LLM Request Routing with Automatic Fallback

**Literature Covered:** Ten research papers published or initially released between 2023 and 2026.

---

# 1. Introduction to AI Model Routing

## 1.1 What Is AI Model Routing?

AI model routing is the process of automatically selecting an appropriate artificial intelligence model from a collection of available models to handle an incoming request.

Given a user request and several available AI models, the central problem is:

**How can a system automatically select the most suitable model while balancing response quality, monetary cost, latency, computational resources, and operational reliability?**

Different AI models have different capabilities, strengths, limitations, prices, and resource requirements.

For example:

- A smaller language model may be sufficient for text classification, summarisation, or simple factual questions.
- A reasoning-oriented model may perform better on complex mathematics, planning, and multi-step problem-solving.
- A specialised programming model may be more suitable for code generation, debugging, and software development.
- A model with a large context window may be necessary for processing extensive documents.
- A multimodal model may be required when a request contains images, audio, or other non-textual information.

However, using the most expensive or powerful model for every request does not necessarily produce the most efficient system.

Model routing attempts to exploit differences between models so that each request is processed by a model that satisfies its requirements without unnecessary expenditure.

## 1.2 The Traditional Approach to Model Selection

Traditional LLM-based applications frequently use a fixed-model architecture.

In such systems, developers configure one model to handle all incoming requests.

For example, an application might send every user message to a single general-purpose LLM, regardless of the task's complexity.

This creates several potential problems.

### 1.2.1 Unnecessary Computational and Monetary Cost

Simple requests may be processed by expensive models even when cheaper models would produce responses of comparable quality.

For example, converting a short list into JSON may not require the same reasoning capabilities as solving an advanced mathematical problem.

Using the same expensive model for both can waste computational resources and increase operating costs.

### 1.2.2 Inefficient Resource Allocation

Different models have different levels of expertise.

A general-purpose model may perform adequately across many tasks while a specialised model performs better on a particular category.

A static model-selection strategy does not take full advantage of this specialisation.

### 1.2.3 Lack of Adaptability

The capabilities, prices, and availability of AI models change over time.

A fixed-model application may require manual configuration changes whenever a better or more economical model becomes available.

### 1.2.4 Limited Failure Recovery

Applications dependent on one model or provider may experience service disruptions when that provider encounters:

- Network failures.
- API timeouts.
- Rate-limit errors.
- Service outages.
- Capacity restrictions.
- Model deprecation or unavailability.

Without an appropriate fallback strategy, these failures can interrupt service delivery.

### 1.2.5 Conversation Continuity During Model Switching

When a user manually switches models during a conversation, response consistency may be affected if the application does not preserve the necessary context.

Possible causes include:

- Missing or truncated conversation history.
- Inconsistent system instructions.
- Different context-window limits.
- Different support for tools or structured output.
- Different model capabilities and response styles.
- Loss of application-maintained state.

However, switching models does not automatically reduce output quality.

A properly designed system can preserve conversation history and relevant state across models, although models may interpret the same context differently.

This makes context management an important engineering consideration for model-routing systems.

## 1.3 Intelligent AI Model Routing

An intelligent model router analyses an incoming request and selects an appropriate model based on predefined rules, learned predictions, or optimisation algorithms.

A typical routing system performs the following operations:

1. Receives an incoming user request.
2. Extracts relevant request features.
3. Identifies available models.
4. Eliminates models that cannot satisfy mandatory requirements.
5. Estimates suitability, quality, cost, and other relevant characteristics.
6. Selects an appropriate model.
7. Executes the request through the selected model or provider.
8. Handles failures or escalations when necessary.
9. Records performance data for monitoring and evaluation.

The routing algorithm may be rule-based, machine-learning-based, decision-theoretic, or a combination of multiple approaches.

The goal is not always to select the cheapest model or the model with the highest benchmark score.

Instead, the goal is to select the model that best satisfies the request under the system's constraints.

---

# 2. Fundamental Concepts in AI Model Routing

## 2.1 Query or Prompt Awareness

Prompt awareness refers to a router's ability to inspect the content and requirements of an incoming request before deciding which model should process it.

A prompt-aware router may consider:

- Task category.
- Estimated task difficulty.
- Required reasoning capabilities.
- Input token count.
- Expected output length.
- Required context-window size.
- Programming language or subject domain.
- Presence of images, audio, or documents.
- Tool-calling requirements.
- Structured-output requirements.
- User-specified quality preferences.

For example, a prompt requesting a short summary and another requesting a complex software architecture review should not automatically receive identical routing treatment.

However, prompt complexity is not a perfect predictor of model performance.

A short query can be extremely difficult, while a long query may involve a simple transformation.

Therefore, a router should ideally estimate model-specific suitability rather than relying exclusively on prompt length or apparent complexity.

## 2.2 Cost Awareness

Cost-aware routing considers the financial or computational expense of processing a request.

For commercial language model APIs, cost may depend on:

- Input tokens.
- Output tokens.
- Cached input tokens.
- Reasoning tokens, where separately accounted for.
- Tool usage.
- Additional provider-specific charges.

For locally hosted models, costs may instead include GPU time, energy consumption, infrastructure utilisation, and hardware amortisation.

A basic API cost estimate can be expressed as:

**Estimated Cost = Estimated Input Cost + Estimated Output Cost + Additional Charges**

One challenge is that the actual output length is unknown before generation.

Therefore, a router may need to predict output length or estimate a cost distribution.

An accurate cost-aware system should distinguish between predicted costs and actual billed costs.

## 2.3 Quality Awareness

Quality-aware routing attempts to estimate whether a candidate model can produce an acceptable response.

Quality may be measured using:

- Exact-match accuracy.
- Task-specific correctness.
- Human preference.
- Expert evaluation.
- LLM-as-a-judge scores.
- Code execution and test results.
- Structured-output validity.
- Task-completion success.

No single quality metric is appropriate for all tasks.

For instance, mathematical answers may be evaluated against known solutions, while creative writing may require subjective preference judgments.

## 2.4 Latency Awareness

Latency-aware routing considers how long a model is expected to take to complete a request.

Important metrics include:

- Time to first token.
- Total response latency.
- Output generation speed.
- Queueing delay.
- Network delay.
- Provider response variability.
- P50, P95, and P99 latency.

A cheaper model may not always be faster.

Consequently, an optimal routing policy may need to consider both financial cost and response time.

## 2.5 Resource Awareness

Resource-aware routing considers the computational requirements of executing a model.

Relevant resources include:

- CPU.
- GPU.
- GPU memory.
- System memory.
- Storage.
- Network bandwidth.
- Energy consumption.
- Available inference capacity.

Resource-aware routing is especially important when models are self-hosted.

A model may offer excellent accuracy but be unsuitable if its memory or computational requirements exceed the available infrastructure.

## 2.6 Reliability Awareness

Reliability-aware routing incorporates the current operational condition of models and providers.

The router may consider:

- Error rates.
- Provider availability.
- Recent timeouts.
- Rate-limit status.
- Service degradation.
- Historical execution success rates.

Reliability awareness is related to, but distinct from, model quality.

A model might be highly capable but temporarily unavailable.

## 2.7 Routing Versus Cascading Versus Ensembling

These concepts are closely related but should not be treated as interchangeable.

### Routing

Routing selects a model before generating the response.

Typically, one model processes the request.

Example: A classifier predicts that Model B is best suited to a programming task, so the request is sent to Model B.

### Cascading

Cascading processes a request through one model and conditionally invokes another model if the initial response is insufficient.

Example: A small model attempts the task. A verification mechanism assigns a low confidence score, causing escalation to a larger model.

### Ensembling

Ensembling obtains multiple model responses and selects or combines them.

Example: Three models produce answers. A ranking model evaluates the responses, and a fusion model combines useful information.

### Operational Fallback

Operational fallback invokes an alternative model or provider after an execution failure.

Example: The selected provider times out, so the application attempts another compatible provider.

Operational fallback differs from quality-based cascading because the triggering event is a service or execution failure rather than an inadequate but successfully generated response.

### Internal Mixture-of-Experts Routing

Mixture-of-Experts (MoE) routing selects internal neural-network experts within a model.

This differs from an external LLM request router, which selects among independently deployed models or providers.

The present literature review focuses primarily on external model routing.

---

# 3. Existing AI Model Routing Algorithm Families

The literature describes several major categories of routing algorithms.

These categories overlap, and individual systems may combine techniques from multiple families.

## 3.1 Classification-Based Routing

Classification-based routing trains a predictive model to determine which language model is most appropriate for a particular request.

The classifier receives features extracted from the prompt and predicts either:

- The most suitable model.
- The probability that each model will succeed.
- The relative quality difference between candidate models.
- Whether a stronger model is necessary.

### Representative Papers

1. Ding et al. (2024), *Hybrid LLM: Cost-Efficient and Quality-Aware Query Routing*.
2. Shnitzer et al. (2023), *Large Language Model Routing with Benchmark Datasets*.
3. Ong et al. (2024), *RouteLLM: Learning to Route LLMs with Preference Data*, which also evaluates classifier-based approaches.

### Advantages

- Can make routing decisions before expensive generation.
- Usually has lower inference overhead than multi-model evaluation.
- Can learn task-specific patterns.
- Can support cost-quality optimisation.
- Often easier to benchmark than complex reinforcement-learning approaches.

### Limitations

- Requires suitable training data.
- Predictions may be poorly calibrated.
- Performance can deteriorate on unfamiliar query distributions.
- New models may require additional training or calibration.

### Relevance to the Proposed Project

Classification-based routing is a strong candidate for the primary prompt-aware decision mechanism.

It provides a relatively practical foundation for estimating model suitability without generating responses from every available model.

## 3.2 Embedding-Based and Contrastive-Learning Routing

Embedding-based routing represents prompts and candidate models using numerical vectors.

The router estimates the suitability of a model by comparing vector representations.

Models and prompts with stronger learned compatibility should receive higher selection scores.

### Representative Paper

Chen et al. (2024), *RouterDC: Query-Based Router by Dual Contrastive Learning for Assembling Large Language Models*.

### Advantages

- Can represent semantic relationships between tasks.
- Can capture specialisation across several models.
- Can support retrieval or similarity-based routing.
- May generalise better than simple manually defined task categories.

### Limitations

- Requires meaningful embeddings.
- Semantic similarity does not guarantee comparable model performance.
- Trainable approaches require representative performance data.
- Model additions and changing capabilities can require recalibration.

### Relevance to the Proposed Project

Embedding-based routing is particularly relevant when selecting between several models with different expertise.

A simpler embedding-similarity baseline could also be compared with a trained classifier.

## 3.3 Preference-Based Routing

Preference-based routing learns from comparisons of responses produced by different models.

Instead of requiring a single objectively correct response, the method uses judgments indicating which response is preferred.

### Representative Paper

Ong et al. (2024), *RouteLLM: Learning to Route LLMs with Preference Data*.

### Advantages

- Suitable for open-ended tasks.
- Can incorporate human preferences.
- Supports learning from comparative quality judgments.
- Can reduce reliance on exact-answer evaluation.

### Limitations

- Preference labels may be sparse.
- Human judgments can be subjective.
- LLM-generated preference labels may contain bias.
- User preferences may differ from benchmark preferences.

### Relevance to the Proposed Project

Preference-based approaches are useful when evaluating tasks without objectively correct answers.

They can also inform how response-quality labels should be collected for training and evaluation.

## 3.4 Reward-Guided Routing

Reward-guided routing uses a reward model to evaluate generated responses and learn which language models are suitable for different categories of queries.

The reward information is typically collected during training.

A lightweight router can subsequently make decisions without invoking the reward model for every request.

### Representative Paper

Lu et al. (2023), *Routing to the Expert: Efficient Reward-guided Ensemble of Large Language Models*.

The proposed method is called **Zooter**.

### Advantages

- Reduces dependence on manually labeled model-selection data.
- Captures model specialisation.
- Can train a relatively efficient inference-time router.
- Uses existing reward models as supervisory signals.

### Limitations

- Reward models may be biased.
- Training data generation can be expensive.
- Reward scores may not align with actual user satisfaction.
- Training labels may become stale as model capabilities change.

### Relevance to the Proposed Project

Reward-guided routing provides a way to develop empirical model capability profiles.

However, implementing a complete reward-model training pipeline may be unnecessary for the initial project scope.

## 3.5 Cascading Algorithms

Cascading algorithms process requests through a sequence of models.

A decision mechanism determines whether an initial response is acceptable or whether the request should be escalated.

### Representative Papers

1. Chen et al. (2023), *FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance*.
2. Aggarwal et al. (2023/2024), *AutoMix: Automatically Mixing Language Models*.

### Advantages

- Can avoid expensive models for requests adequately handled by cheaper models.
- Uses response-level evidence.
- Can improve the cost-quality trade-off.
- Supports progressive escalation.

### Limitations

- Multiple model calls can increase latency.
- Verification may itself incur cost.
- Incorrect verification can reject good answers or accept poor ones.
- Escalation does not guarantee improved quality.

### Relevance to the Proposed Project

Cascading is important for evaluating whether post-generation quality checks provide meaningful benefits over direct pre-generation routing.

## 3.6 Decision-Theoretic Routing

Decision-theoretic routing frames model selection as a sequential decision problem under uncertainty.

The router considers possible actions, their expected rewards, their costs, and uncertainty about the current state.

### Representative Paper

Aggarwal et al. (2023/2024), *AutoMix: Automatically Mixing Language Models*.

AutoMix uses a Partially Observable Markov Decision Process (POMDP).

### Advantages

- Explicit treatment of uncertainty.
- Can incorporate multiple decision stages.
- Provides a mathematical foundation for cost-quality optimisation.
- Can support sequential decisions.

### Limitations

- More complex implementation.
- Requires assumptions about transition and reward behaviour.
- Sensitive to inaccurate estimates.
- Potentially excessive for simple routing systems.

### Relevance to the Proposed Project

Decision-theoretic routing can inform the mathematical formulation of the proposed system.

However, a simpler constrained optimisation policy may be a better starting point.

## 3.7 Ensemble-Based Routing and Response Selection

Ensemble approaches use multiple language models to improve response quality.

They typically evaluate or combine generated responses.

### Representative Paper

Jiang et al. (2023), *LLM-Blender: Ensembling Large Language Models with Pairwise Ranking and Generative Fusion*.

### Advantages

- Combines complementary model strengths.
- Can improve response quality.
- Evaluates actual generated outputs.
- May outperform individual models on selected tasks.

### Limitations

- Multiple generation calls increase cost.
- Response comparison adds processing overhead.
- Fusion introduces additional latency.
- May conflict with objectives focused on inexpensive inference.

### Relevance to the Proposed Project

Ensembling should be included as a related technique but does not need to be part of the initial implementation.

## 3.8 Difficulty-Aware Routing

Difficulty-aware approaches estimate how challenging a request is and use that estimate to determine the necessary model capability.

Typical features include:

- Reasoning complexity.
- Number of subproblems.
- Required domain knowledge.
- Prompt structure.
- Task uncertainty.

Difficulty-aware routing may use classifiers, language models, or heuristic rules.

### Limitation

Difficulty is not an absolute property independent of the candidate models.

A task that is difficult for one model may be easy for another.

Therefore, model-specific suitability estimates may be more useful than a single generic difficulty score.

## 3.9 Similarity-Based and Clustering-Based Routing

These approaches group similar requests together or identify historical examples resembling an incoming request.

Routing decisions are informed by how candidate models performed on similar examples.

### Advantages

- Can use historical execution data.
- May be relatively interpretable.
- Can work without training a large neural router.
- Supports incremental addition of examples.

### Limitations

- Similar prompts may require different reasoning abilities.
- Quality depends on the relevance of historical examples.
- Retrieval introduces computational overhead.
- Performance may degrade when new query categories appear.

RouteLLM's similarity-weighted ranking method provides a useful example.

## 3.10 Reinforcement-Learning and Contextual-Bandit Routing

Reinforcement-learning approaches learn routing policies using reward signals.

A contextual bandit chooses a model based on the current request and receives feedback about the selected action.

More general reinforcement-learning approaches can support sequential routing and cascading decisions.

### Advantages

- Can adapt to observed performance.
- Supports cost-quality reward formulations.
- Can potentially adjust to changing model capabilities.
- May learn policies from ongoing interaction data.

### Limitations

- Requires careful exploration.
- Low-quality exploration decisions can affect users.
- Feedback may be delayed or missing.
- Reward design is difficult.
- Online experimentation requires safety and cost controls.

These approaches are relevant as potential future extensions rather than mandatory components of the initial implementation.

## 3.11 Survey and Taxonomy Literature

Survey papers synthesise existing methods and organise the field.

### Representative Papers

1. Moslem and Kelleher (2026), *Dynamic Model Routing and Cascading for Efficient LLM Inference: A Survey*.
2. Varangot-Reille et al. (2025), *Doing More with Less: A Survey on Routing Strategies for Resource Optimisation in Large Language Model-Based Systems*.

These papers are primarily useful for understanding the classification, evolution, limitations, and research directions of routing algorithms.

They should not be treated as newly proposed routing algorithms when selecting experimental baselines.

---

# 4. Detailed Analysis of the Ten Research Papers

## 4.1 AutoMix: Automatically Mixing Language Models

**Authors:** Pranjal Aggarwal et al.

**Year:** Initially released in 2023; NeurIPS 2024.

**Reference:** arXiv:2310.12963.

**Link:** https://arxiv.org/abs/2310.12963

**Algorithm Families:** Cascading, self-verification, decision-theoretic routing, uncertainty-aware routing.

**Relevance:** Very High.

### 4.1.1 Research Problem

AutoMix addresses the difficulty of deciding whether a cheaper language model's response is sufficiently reliable or whether a more capable model should be invoked.

A simple strategy might automatically escalate every difficult-looking request.

However, such a strategy can waste resources because a smaller model may already have produced an acceptable answer.

Alternatively, accepting every response from the smaller model may reduce overall quality.

AutoMix attempts to balance these outcomes.

### 4.1.2 Proposed Solution

The authors propose a mechanism combining few-shot self-verification with a POMDP-based routing policy.

The system first generates a response using a smaller model.

It then estimates the reliability of that response.

The resulting verification information informs a decision to accept the response or invoke another model.

### 4.1.3 Algorithmic Procedure

1. Receive an incoming query.
2. Invoke a relatively inexpensive model.
3. Generate a candidate response.
4. Apply few-shot self-verification.
5. Estimate whether the response is reliable.
6. Use the verification information within the routing policy.
7. Decide whether to return the answer or escalate.
8. Return the final selected response.

### 4.1.4 Partially Observable Markov Decision Process

A POMDP is appropriate when the system cannot directly observe the true state.

In AutoMix, the true correctness or relative suitability of candidate models is not fully known.

The system instead observes an imperfect verification signal.

Its routing policy attempts to maximise expected utility while accounting for uncertainty and the cost of invoking more models.

A simplified utility formulation is:

U = Expected Performance − λ × Expected Cost

Here, λ determines how strongly cost affects the decision.

This represents the general cost-performance trade-off; the complete POMDP contains additional decision structure.

### 4.1.5 Methodology and Findings

The authors evaluate the approach using five language models and five challenging datasets.

They report that AutoMix reduces computational cost by more than 50% while achieving performance comparable to strong alternatives in the evaluated settings.

The study also investigates the behaviour of routing under noisy verification signals and different model configurations.

### 4.1.6 Strengths

- Does not require extensive supervised router training.
- Can work with black-box language model APIs.
- Introduces uncertainty into the routing decision.
- Uses actual generated responses rather than only prompt characteristics.
- Provides a theoretical framework for escalation decisions.

### 4.1.7 Limitations

- Self-verification may be unreliable.
- Verification introduces extra model inference.
- Multiple model calls can increase latency.
- Reliable verification is difficult for subjective or open-ended tasks.
- The algorithm adds implementation complexity.
- The paper does not primarily evaluate infrastructure-level provider recovery.

### 4.1.8 Relevance to the Proposed FYP

AutoMix provides a foundation for implementing and evaluating quality-driven escalation.

It also supports the argument that routing decisions should account for uncertainty.

A practical implementation could compare a simple confidence threshold with a more sophisticated escalation policy.

However, implementing an entire POMDP is not essential for the initial FYP.

### 4.1.9 Key Research Lesson

**A router should consider whether additional model inference is likely to provide enough improvement to justify its cost.**

---

## 4.2 RouterDC: Query-Based Router by Dual Contrastive Learning for Assembling Large Language Models

**Authors:** Shuhao Chen, Weisen Jiang, Baijiong Lin, James T. Kwok, and Yu Zhang.

**Year:** 2024.

**Publication:** NeurIPS 2024.

**Reference:** arXiv:2409.19886.

**Link:** https://arxiv.org/abs/2409.19886

**Algorithm Families:** Embedding-based routing, contrastive learning, prompt-aware routing.

**Relevance:** High.

### 4.2.1 Research Problem

Different language models possess complementary capabilities.

However, multiple models may perform well on the same query.

A traditional routing classifier that assumes one uniquely correct model per query may fail to capture this relationship.

RouterDC investigates how to learn richer associations between queries and candidate models.

### 4.2.2 Proposed Solution

RouterDC introduces a query encoder and learnable embeddings representing candidate language models.

It trains the routing mechanism using two contrastive-learning objectives.

### 4.2.3 Sample–LLM Contrastive Learning

This objective teaches the router which models perform well on particular examples.

A query representation should align more strongly with models that can handle the query successfully.

It avoids treating model selection as an oversimplified single-label classification problem.

### 4.2.4 Sample–Sample Contrastive Learning

This objective improves the representation of queries.

It encourages the embedding space to capture relationships between training examples and supports more stable routing behaviour.

### 4.2.5 Algorithmic Procedure

1. Collect queries and observed model-performance information.
2. Generate query representations with an encoder.
3. Maintain learnable embeddings for candidate models.
4. Optimise the two contrastive objectives.
5. Receive a new query.
6. Encode the query.
7. Calculate compatibility scores between the query and candidate models.
8. Select a model according to the learned scores.

### 4.2.6 Methodology and Findings

The researchers evaluate RouterDC on both in-distribution and out-of-distribution tasks.

The study reports improvements of 2.76% and 1.90%, respectively, over the relevant comparison methods in its experimental settings.

These results suggest that representation learning can improve model selection when multiple models have overlapping expertise.

### 4.2.7 Strengths

- Captures semantic and task-related relationships.
- Represents several model capabilities within one learned system.
- Handles cases where multiple models perform well.
- Investigates performance on unfamiliar tasks.
- Performs routing before response generation.

### 4.2.8 Limitations

- Requires training data containing model-performance information.
- Training is more complex than simple heuristic routing.
- Learned representations may become outdated.
- Changing candidate models may require adaptation.
- Cost, latency, and provider health are not the central routing objectives.

### 4.2.9 Relevance to the Proposed FYP

RouterDC is especially relevant to prompt-aware suitability estimation.

Its ideas could support a model capability matching system.

A simpler implementation might compare prompt embeddings with historical examples or predefined task profiles.

A full contrastive router could be considered for an advanced experimental baseline.

### 4.2.10 Key Research Lesson

**Effective routing should model the relationship between the request and each candidate model's capabilities, rather than assuming a universal model ranking.**

---

## 4.3 Large Language Model Routing with Benchmark Datasets

**Authors:** Tal Shnitzer et al.

**Year:** 2023.

**Reference:** arXiv:2309.15789.

**Link:** https://arxiv.org/abs/2309.15789

**Algorithm Families:** Classification-based routing, benchmark-supervised learning.

**Relevance:** Very High.

### 4.3.1 Research Problem

No single language model consistently achieves the highest performance on every benchmark or task.

This creates an opportunity to improve overall performance by selecting different models for different queries.

However, training a router requires information about model capabilities.

The authors investigate whether existing benchmark datasets can provide that information.

### 4.3.2 Proposed Solution

The paper reformulates model routing as a collection of binary classification problems.

For each candidate model, a classifier predicts whether the model is likely to answer a given query correctly.

### 4.3.3 Mathematical Formulation

For a query q and candidate model Mᵢ:

P(correct | q, Mᵢ)

represents the estimated probability that the model will answer the query correctly.

A simple quality-maximising router selects the model with the highest predicted probability.

This formulation can later be extended to account for cost.

### 4.3.4 Algorithmic Procedure

1. Collect benchmark questions.
2. Obtain candidate model responses.
3. Determine whether responses are correct.
4. Construct training data for each model.
5. Train correctness-prediction classifiers.
6. Receive a new query.
7. Estimate the probability of correctness for candidate models.
8. Select a model based on the predictions.

### 4.3.5 Methodology and Findings

The study reuses existing benchmark datasets, including benchmark results associated with HELM.

The authors demonstrate that learned routing can outperform consistently selecting one fixed model.

They also investigate the limitations of transferring learned routing knowledge to unfamiliar tasks.

### 4.3.6 Strengths

- Straightforward problem formulation.
- Reuses available benchmark datasets.
- Provides measurable correctness targets.
- Supports lightweight routing models.
- Demonstrates the value of model-specific predictions.

### 4.3.7 Limitations

- Correctness labels are difficult for open-ended tasks.
- Benchmark data may not represent real production workloads.
- Models may perform differently on unfamiliar domains.
- Predictions can be poorly calibrated.
- Training data may become stale as models improve or change.

### 4.3.8 Relevance to the Proposed FYP

This paper is directly relevant to designing the project's core routing algorithm.

The proposed system could estimate model success using features such as task category, context length, required capabilities, and historical performance.

It is also a strong foundation for defining classification-based routing baselines.

### 4.3.9 Key Research Lesson

**Model routing can be formulated as a supervised prediction problem using historical evidence about model performance.**

---

## 4.4 Routing to the Expert: Efficient Reward-guided Ensemble of Large Language Models

**Authors:** Keming Lu et al.

**Year:** 2023.

**Reference:** arXiv:2311.08692.

**Link:** https://arxiv.org/abs/2311.08692

**Proposed System:** Zooter.

**Algorithm Families:** Reward-guided routing, model expertise learning, reward distillation.

**Relevance:** High.

### 4.4.1 Research Problem

Different language models have different areas of expertise.

Identifying these strengths manually is difficult.

Generating answers from every model and ranking them during inference can also be expensive.

The researchers investigate whether the expertise of candidate models can be learned in advance.

### 4.4.2 Proposed Solution

Zooter uses reward models to evaluate model outputs during training.

The resulting scores provide supervisory information for learning a routing function.

This process is called reward distillation.

### 4.4.3 Algorithmic Procedure

1. Collect a diverse set of queries.
2. Generate responses using candidate LLMs.
3. Evaluate the responses using reward models.
4. Convert reward information into routing supervision.
5. Use task tags to improve the supervision.
6. Train a query-based router.
7. Select an appropriate model during inference.

### 4.4.4 Tag-Based Label Enhancement

Reward scores can be noisy.

Zooter introduces tag-based label enhancement to reduce the uncertainty associated with individual training examples.

Queries associated with related task categories can provide additional information about which models are likely to perform well.

### 4.4.5 Methodology and Findings

The authors evaluate Zooter using 26 benchmark subsets across different tasks and domains.

The paper reports that Zooter outperforms the best individual model on average and achieves the highest performance on 44% of the evaluated tasks.

It also reduces inference-time overhead compared with methods that generate and rank responses from multiple models.

### 4.4.6 Strengths

- Learns model expertise.
- Reduces the need for manually labeled training examples.
- Avoids repeated multi-model inference after training.
- Supports task-specific routing.
- Uses existing reward models as supervision.

### 4.4.7 Limitations

- Reward labels are imperfect.
- Reward models may contain biases.
- Generating training responses is expensive.
- The router can become outdated when the model pool changes.
- Monetary cost and operational reliability are not the primary optimisation targets.

### 4.4.8 Relevance to the Proposed FYP

Zooter provides useful ideas for developing model capability profiles and collecting training signals.

The project could use benchmark results, evaluations, and feedback to estimate which models perform well on specific categories of tasks.

### 4.4.9 Key Research Lesson

**A router can learn model expertise from evaluated historical responses, allowing inexpensive model selection during subsequent inference.**

---

## 4.5 LLM-Blender: Ensembling Large Language Models with Pairwise Ranking and Generative Fusion

**Authors:** Dongfu Jiang, Xiang Ren, and Bill Yuchen Lin.

**Year:** 2023.

**Publication:** ACL 2023.

**Reference:** arXiv:2306.02561.

**Link:** https://arxiv.org/abs/2306.02561

**Algorithm Families:** Ensemble learning, response ranking, generative fusion.

**Relevance:** Moderate.

### 4.5.1 Research Problem

Individual language models may produce responses of different quality for the same query.

Even a generally strong model may generate a weaker response than another model on a particular example.

The researchers investigate how to exploit complementary model strengths by comparing and combining their outputs.

### 4.5.2 Proposed Solution

LLM-Blender contains two principal components:

1. PairRanker.
2. GenFuser.

### 4.5.3 PairRanker

PairRanker compares pairs of candidate responses.

It jointly processes the input query and response pairs to determine which response is preferable.

This allows the system to rank outputs according to their quality for a particular request.

### 4.5.4 GenFuser

GenFuser uses highly ranked responses as inputs to generate a consolidated output.

The goal is to combine useful information from multiple responses while reducing their individual weaknesses.

### 4.5.5 Algorithmic Procedure

1. Receive a query.
2. Generate responses from multiple language models.
3. Compare the responses using PairRanker.
4. Rank the candidate responses.
5. Select the strongest candidates.
6. Apply GenFuser.
7. Return the generated combined response.

### 4.5.6 Methodology and Findings

The paper introduces MixInstruct, a benchmark resource constructed from instruction-following datasets.

The authors evaluate ranking and fusion against individual models and comparison methods.

They report improved performance across their evaluated metrics, demonstrating the potential benefit of combining complementary model outputs.

### 4.5.7 Strengths

- Evaluates actual responses.
- Exploits complementary information.
- Supports fine-grained response comparison.
- Can improve quality on tasks where different models contribute useful information.

### 4.5.8 Limitations

- Requires several model calls.
- Introduces response-ranking overhead.
- Fusion adds another generation step.
- Can increase cost and latency.
- May not suit applications prioritising inexpensive inference.

### 4.5.9 Relevance to the Proposed FYP

LLM-Blender provides an important alternative to routing.

Rather than selecting one model before generation, it uses several models and combines their outputs.

It is useful for justifying why the proposed project prioritises efficient selection instead of unrestricted multi-model generation.

The response-ranking ideas may also inform an optional verification module.

### 4.5.10 Key Research Lesson

**Ensembling may improve response quality, but its additional inference requirements must be considered when evaluating efficiency.**

---

## 4.6 FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance

**Authors:** Lingjiao Chen, Matei Zaharia, and James Zou.

**Year:** 2023.

**Reference:** arXiv:2305.05176.

**Link:** https://arxiv.org/abs/2305.05176

**Algorithm Families:** Cost-aware routing, cascading, quality-based escalation.

**Relevance:** Very High.

### 4.6.1 Research Problem

Different LLM APIs have substantially different prices.

Using expensive models for every request may lead to unnecessary financial expenditure.

However, cheaper models may perform inadequately on difficult tasks.

FrugalGPT investigates how to combine models to reduce inference cost while maintaining acceptable performance.

### 4.6.2 Cost Optimisation Strategies

The paper discusses three broad strategies.

**Prompt adaptation:** Reducing unnecessary prompt-processing costs.

**LLM approximation:** Using cheaper models or mechanisms to approximate the capabilities of more expensive models.

**LLM cascading:** Sequentially invoking models and deciding whether additional inference is required.

### 4.6.3 Proposed Cascading Algorithm

FrugalGPT learns model sequences and response-acceptance conditions.

A request is processed by a model in the selected sequence.

A scoring function evaluates its output.

If the answer satisfies an acceptance threshold, the system returns it.

Otherwise, another model is invoked.

### 4.6.4 Basic Mathematical Formulation

Let:

g(q, a)

represent the quality score assigned to answer a for query q.

Let:

τᵢ

represent the acceptance threshold associated with a model or cascade stage.

The system accepts the response when:

g(q, a) ≥ τᵢ

Otherwise, it proceeds to the next stage if one is available.

The complete approach considers how model sequences and thresholds influence expected cost and performance.

### 4.6.5 Methodology and Findings

The authors study 12 LLM APIs from five providers.

They evaluate cost and performance across several tasks.

The paper reports up to 98% cost reduction while matching the performance of a strong individual model in certain experimental settings.

It also reports a scenario in which accuracy improves by approximately four percentage points at equivalent cost.

These are experiment-specific results and should not be interpreted as guaranteed savings for modern APIs.

### 4.6.6 Strengths

- Directly addresses API cost.
- Provides a practical multi-model inference strategy.
- Supports configurable cost-performance trade-offs.
- Introduces learned acceptance thresholds.
- Demonstrates that smaller models can handle many requests effectively.

### 4.6.7 Limitations

- Multiple requests may increase latency.
- Reliability scoring is difficult.
- Escalation incurs additional cost.
- The original experimental models and prices are dated.
- Operational provider-failure recovery is not the central contribution.

### 4.6.8 Relevance to the Proposed FYP

FrugalGPT is one of the most important references for cost-efficient model inference.

It provides a basis for implementing quality-based escalation and evaluating cost savings.

However, the FYP should distinguish between quality escalation and operational fallback.

For example, a model returning an inadequate response and a provider returning HTTP 429 require different recovery policies.

### 4.6.9 Key Research Lesson

**Learning when a cheaper model's response is sufficient can substantially reduce the cost of LLM-powered systems.**

---

## 4.7 Hybrid LLM: Cost-Efficient and Quality-Aware Query Routing

**Authors:** Dujian Ding et al.

**Year:** 2024.

**Publication:** ICLR 2024.

**Reference:** arXiv:2404.14618.

**Link:** https://arxiv.org/abs/2404.14618

**Algorithm Families:** Classification-based routing, quality-aware routing, cost-aware routing.

**Relevance:** Very High.

### 4.7.1 Research Problem

Large language models generally provide strong performance but can be expensive to deploy and operate.

Smaller language models are less resource-intensive but may struggle on more demanding tasks.

The researchers investigate how to select between smaller and larger models while controlling the trade-off between cost and response quality.

### 4.7.2 Proposed Solution

Hybrid LLM introduces a routing mechanism that predicts whether a smaller model can produce a response comparable to that of a larger model.

The router uses this prediction and a desired quality level to determine which model should process a request.

### 4.7.3 Quality-Gap Prediction

The central idea is to compare the expected response quality of two candidate models.

A conceptual quality-gap function can be expressed as:

H(q) = Q(S, q) − Q(L, q)

Where:

- S is the smaller model.
- L is the larger model.
- Q is a response-quality function.

If the quality gap is sufficiently favourable to the smaller model, the system may select it.

The actual paper investigates specific ways of learning the routing decision rather than requiring this illustrative formula to be evaluated directly at inference time.

### 4.7.4 Dynamic Quality Thresholds

The desired quality level can be adjusted at inference time.

A system can therefore operate under different cost-quality requirements without necessarily retraining the router for every threshold.

A stricter quality policy generally sends more uncertain requests to the larger model.

### 4.7.5 Algorithmic Procedure

1. Collect paired model-performance information.
2. Train a router using the quality relationships between model outputs.
3. Receive a new query.
4. Estimate whether the smaller model is sufficiently capable.
5. Compare the estimate with the desired quality criterion.
6. Select the smaller or larger model.
7. Return the selected model's response.

### 4.7.6 Methodology and Findings

The researchers evaluate different model pairings and quality requirements.

They report up to 40% fewer calls to the larger model without a measured reduction in response quality in their experimental settings.

This demonstrates that routing can reduce reliance on expensive models while preserving a defined performance standard.

### 4.7.7 Strengths

- Performs routing before generation.
- Directly considers response quality.
- Supports adjustable cost-quality preferences.
- Uses a relatively interpretable decision framework.
- Provides a useful basis for lightweight routing.

### 4.7.8 Limitations

- Focuses primarily on small-large model pairs.
- Requires training or calibration data.
- Generalisation to larger model pools requires additional design.
- Model updates may change the learned quality relationships.
- Operational availability is not a central optimisation dimension.

### 4.7.9 Relevance to the Proposed FYP

Hybrid LLM is one of the strongest references for the core routing decision.

Its quality-aware approach could be extended to several candidate models with different prices, latencies, and capabilities.

It also provides a foundation for configurable routing priorities.

### 4.7.10 Key Research Lesson

**The routing decision should estimate whether a cheaper model can satisfy the required quality level, not merely whether the query looks simple.**

---

## 4.8 Dynamic Model Routing and Cascading for Efficient LLM Inference: A Survey

**Authors:** Yasmin Moslem and John D. Kelleher.

**Year:** 2026.

**Reference:** arXiv:2603.04445.

**Version Reviewed:** v3.

**Link:** https://arxiv.org/abs/2603.04445

**Category:** Survey and taxonomy.

**Relevance:** Essential.

### 4.8.1 Research Objective

The survey reviews existing methods for dynamically selecting between independently trained language models.

It seeks to explain how routing algorithms differ, what information they require, and the circumstances under which they are appropriate.

### 4.8.2 Major Algorithmic Paradigms

The survey covers:

1. Difficulty-aware routing.
2. Human-preference-based routing.
3. Clustering-based routing.
4. Reinforcement-learning-based routing.
5. Uncertainty-aware routing.
6. Cascading.
7. Multimodal routing.

### 4.8.3 Conceptual Framework

The authors propose analysing routing systems along three dimensions.

**When is the routing decision made?**

Examples include before generation, after partial generation, and during multi-stage inference.

**What information informs the routing decision?**

Examples include query features, estimated difficulty, preferences, confidence, and model performance.

**How is the routing decision computed?**

Examples include learned classifiers, similarity functions, thresholds, reinforcement-learning policies, and uncertainty-based decision rules.

### 4.8.4 Main Findings

The survey emphasises that different routing methods introduce different trade-offs.

Some methods are computationally inexpensive but require extensive training data.

Other methods use response-level evidence but introduce additional inference calls.

The survey also highlights that practical routing systems can combine several paradigms.

### 4.8.5 Strengths

- Recent overview of the research field.
- Clear distinction between routing paradigms.
- Discusses multiple optimisation objectives.
- Connects routing and cascading literature.
- Helps structure theoretical and conceptual frameworks.

### 4.8.6 Limitations

- It is a survey rather than an independently evaluated routing algorithm.
- Its conclusions depend on the included literature.
- The research field continues to evolve.
- Individual methods still require direct examination and evaluation.

### 4.8.7 Relevance to the Proposed FYP

This paper is highly useful for structuring Chapter Two.

It supports the classification of routing algorithms and the development of a hybrid architecture.

It also helps justify combining prompt-aware selection, cost estimation, and operational decision rules.

### 4.8.8 Key Research Lesson

**Practical routing systems are often compositional, combining multiple decision mechanisms to satisfy deployment requirements.**

---

## 4.9 Doing More with Less: A Survey on Routing Strategies for Resource Optimisation in Large Language Model-Based Systems

**Authors:** Clovis Varangot-Reille et al.

**Year:** 2025.

**Reference:** arXiv:2502.00409.

**Version Reviewed:** v3.

**Link:** https://arxiv.org/abs/2502.00409

**Category:** Survey, optimisation framework, resource-aware routing.

**Relevance:** Essential.

### 4.9.1 Research Objective

This survey investigates routing strategies intended to improve the resource efficiency of LLM-based systems.

The authors examine why routing is necessary, where it can be introduced, and how routing decisions can be optimised.

Its scope includes monetary expenditure, computational resources, system performance, and other aspects of resource consumption.

### 4.9.2 Central Research Argument

Static LLM-based architectures frequently allocate the same general-purpose model to requests with different levels of complexity.

This can create inefficient resource usage.

Routing mechanisms can improve efficiency by selecting more suitable system components.

### 4.9.3 Mathematical Formulation

A generic constrained routing problem can be represented as:

R(q) = argmax over eligible M of S(q, M)

Subject to:

C(q, M) ≤ B

Where:

- R is the routing policy.
- q is the request.
- M is a candidate model.
- S represents model suitability or performance.
- C represents resource cost.
- B represents an available resource budget.

This is a general optimisation formulation consistent with the survey's themes, not a claim that every method reviewed uses the same equation.

### 4.9.4 Main Areas Covered

The survey discusses:

- Routing objectives.
- Cost minimisation.
- Performance maximisation.
- Routing timing.
- Model and component selection.
- Computational efficiency.
- Resource constraints.
- Generalisation.
- Adaptive model selection.
- Evaluation challenges.

### 4.9.5 Strengths

- Broad perspective on resource optimisation.
- Useful mathematical and architectural concepts.
- Distinguishes routing from related inference techniques.
- Supports consideration of computational rather than purely monetary cost.
- Helps define meaningful evaluation objectives.

### 4.9.6 Limitations

- Does not introduce one new routing algorithm.
- Covers a broad category of LLM-based systems.
- Specific methods still need individual verification.
- The results of the surveyed studies may not be directly comparable.

### 4.9.7 Relevance to the Proposed FYP

This survey provides a foundation for the problem statement and optimisation objectives.

It supports the argument that the proposed system should consider cost, quality, latency, and resource constraints together.

### 4.9.8 Key Research Lesson

**Model selection is fundamentally a constrained resource-allocation problem rather than simply a task-classification problem.**

---

## 4.10 RouteLLM: Learning to Route LLMs with Preference Data

**Authors:** Isaac Ong et al.

**Year:** Initially released in 2024; version 4 released in 2025.

**Reference:** arXiv:2406.18665.

**Version Reviewed:** v4.

**Link:** https://arxiv.org/html/2406.18665v4

**Algorithm Families:** Preference-based routing, classification, similarity-based routing, learned model selection.

**Relevance:** Very High.

### 4.10.1 Research Problem

Selecting a powerful LLM for every request can be expensive.

However, routing all requests to a cheaper model may reduce response quality.

RouteLLM investigates how human preference data can be used to predict when a stronger model is worth invoking.

### 4.10.2 Proposed Solution

The researchers develop a framework for training routing models using preference comparisons.

The system predicts whether a stronger model is likely to produce a preferable response compared with a weaker model.

A configurable threshold determines the final model selection.

### 4.10.3 Routing Algorithms Evaluated

RouteLLM investigates four approaches.

**Similarity-Weighted Ranking**

Uses similarity between an incoming query and previously observed preference examples to estimate the appropriate model.

**Matrix Factorisation**

Learns latent relationships from preference data.

**BERT Classifier**

Uses a transformer-based classifier to estimate whether the stronger model is likely to be preferred.

**Causal LLM Classifier**

Uses a causal language model for preference prediction.

### 4.10.4 Mathematical Formulation

Let:

P(strong wins | q)

represent the predicted probability that the stronger model's response will be preferred for query q.

Let α be the routing threshold.

The RouteLLM decision rule selects the stronger model when:

P(strong wins | q) ≥ α

Otherwise, it selects the weaker model.

In this formulation, increasing α generally causes more requests to be routed to the weaker model, because greater confidence is required before choosing the stronger model.

### 4.10.5 Training Data

The authors use human preference data from Chatbot Arena.

The study also investigates data augmentation using labeled benchmark examples and LLM-based preference judgments.

### 4.10.6 Evaluation Metrics

RouteLLM introduces important metrics for measuring routing effectiveness.

**Strong-model call rate**

The proportion of requests directed to the stronger model.

**Performance Gap Recovered (PGR)**

Measures how much of the quality difference between the weaker and stronger model is recovered by the router.

Conceptually:

PGR = (Router Quality − Weak Model Quality) / (Strong Model Quality − Weak Model Quality)

This assumes the stronger model has a higher aggregate evaluation score.

**Average Performance Gap Recovered (APGR)**

Summarises routing performance across different strong-model call rates.

**Call-Performance Threshold (CPT)**

Measures the minimum proportion of strong-model calls required to achieve a specified performance-gap recovery target.

These metrics are valuable because choosing the stronger model for every query may produce high quality but no cost savings.

A routing evaluation must consider quality and resource usage together.

### 4.10.7 Methodology and Findings

The researchers evaluate multiple routing algorithms using public benchmarks.

They report more than twofold cost reductions in certain model-pair and benchmark configurations without substantially compromising measured quality.

They also investigate transfer to different model pairs and out-of-distribution evaluation settings.

### 4.10.8 Strengths

- Uses human preference data.
- Supports open-ended tasks.
- Compares several router architectures.
- Provides useful routing evaluation metrics.
- Investigates transfer and generalisation.
- Supports adjustable cost-quality policies.

### 4.10.9 Limitations

- Primarily studies strong-versus-weak model selection.
- Preference data can be sparse.
- Human preferences may vary.
- LLM-judge augmentation can introduce bias.
- Generalisation is not guaranteed for every model combination.
- Provider failure recovery is not the primary focus.

### 4.10.10 Relevance to the Proposed FYP

RouteLLM is one of the most directly relevant references for algorithm selection and evaluation.

Its similarity-based and classification-based approaches could be reproduced or adapted as experimental baselines.

Its APGR and CPT metrics also provide a foundation for measuring the effectiveness of routing decisions.

### 4.10.11 Key Research Lesson

**Human preference data can train efficient routing policies, and routing performance should be evaluated across quality-cost trade-offs rather than at one fixed operating point.**

---

# 5. Cross-Paper Analysis

## 5.1 Common Findings

Several important conclusions emerge from the reviewed literature.

### 5.1.1 No Single Model Is Universally Optimal

Different models perform better on different tasks.

This finding is central to Shnitzer et al., RouterDC, Zooter, and RouteLLM.

An effective router should therefore consider model-specific strengths instead of assuming that a globally stronger model is always the best choice.

### 5.1.2 Expensive Models Are Frequently Unnecessary

FrugalGPT, Hybrid LLM, AutoMix, and RouteLLM demonstrate that inexpensive models can handle a meaningful proportion of requests while maintaining competitive aggregate quality.

However, their reported savings depend on the workloads, model pairs, prices, and evaluation conditions.

### 5.1.3 Routing Decisions Can Be Learned

Classification, preference learning, contrastive learning, and reward distillation all provide ways to learn model suitability.

This means a router does not necessarily need a large reasoning model to decide where requests should go.

### 5.1.4 Training Data Strongly Influences Router Quality

A routing algorithm trained on a narrow set of examples may struggle on unfamiliar tasks.

Benchmark diversity, label quality, model coverage, and evaluation design are therefore important.

### 5.1.5 Quality Prediction Is Inherently Uncertain

A router cannot generally know the exact quality of an ungenerated response.

It must use estimated correctness, preference, reward, confidence, or historical performance.

These signals can be wrong and should be evaluated for calibration.

### 5.1.6 Routing Overhead Matters

A router that spends substantial resources deciding which model to use may eliminate the savings it was designed to achieve.

Therefore, routing latency and computational cost should be measured separately from model execution.

### 5.1.7 Direct Routing and Cascading Have Different Trade-Offs

Direct routing typically invokes one model per request.

Cascading may obtain additional quality information by invoking multiple models sequentially.

Direct routing can be faster, while cascading may improve decision reliability on some tasks at the expense of additional calls.

### 5.1.8 Research Evaluation Is Not the Same as Production Reliability

A routing algorithm may achieve strong benchmark performance without establishing that the full system can recover reliably from provider outages, rate limits, and timeouts.

These are separate engineering objectives that require dedicated testing.

---

# 6. Potential Research Gaps

The following are potential research gaps motivated by the reviewed papers.

They should be treated as hypotheses for further literature investigation rather than definitive claims that no previous research addresses them.

## 6.1 Multi-Objective Optimisation

Many routing studies emphasise cost and quality.

Production systems may additionally require:

- Low latency.
- Operational reliability.
- Availability.
- Capability compatibility.
- Resource constraints.
- User-specific requirements.

**Potential research question:**

Can combining model-specific quality prediction with cost, latency, and availability constraints improve practical model selection?

## 6.2 Multi-Model and Multi-Provider Generalisation

Several studies focus primarily on selecting between stronger and weaker models.

A practical gateway may manage a larger model pool with different capabilities and pricing structures.

**Potential research question:**

How effectively can a lightweight routing policy rank several heterogeneous models without retraining for every model-pool change?

## 6.3 Operational Failure Recovery

Quality-based escalation does not automatically address network failures, timeouts, or rate limits.

**Potential research question:**

How much can operational-health-aware fallback improve task completion and service reliability under controlled provider-failure conditions?

## 6.4 Prompt-Aware Versus Cost-Only Routing

Selecting the cheapest model is easy to implement but may reduce quality.

Selecting the strongest model may increase cost unnecessarily.

**Potential research question:**

Does prompt-aware suitability prediction significantly outperform static and cheapest-eligible routing strategies?

## 6.5 Routing Overhead

Complex routing models can add computational overhead.

**Potential research question:**

Do the improvements from a learned routing policy outweigh the cost and latency of executing the router itself?

## 6.6 Robustness to Unseen Tasks

Routing policies may be trained on benchmark distributions that differ from real application workloads.

**Potential research question:**

How much does routing performance deteriorate when the system encounters unfamiliar tasks or domains?

## 6.7 Conversation-Aware Model Switching

A multi-model conversational application must preserve relevant conversational state.

**Potential research question:**

How does maintaining consistent conversation context affect response quality when requests within the same session are routed across different models?

This is a relevant secondary engineering investigation, although it should not automatically become a primary research objective without sufficient evaluation scope.

## 6.8 Adaptive Model Capability Profiles

Model performance can change with model updates and changing workloads.

**Potential research question:**

Can periodically updated performance profiles improve routing quality compared with static model rankings?

---

# 7. Proposed Direction for the FYP

## 7.1 Project Focus

The proposed FYP focuses on building and evaluating a lightweight LLM request-routing system that combines:

- Prompt-aware model selection.
- Predicted response suitability.
- Monetary cost estimation.
- Latency awareness.
- Capability constraints.
- Provider availability information.
- Automatic operational fallback.
- Performance monitoring.

The objective is not necessarily to introduce a new foundation model.

Instead, the project investigates how existing models can be selected and orchestrated more efficiently through software engineering and optimisation.

## 7.2 Proposed Routing Approach

A suitable starting approach is a **constraint-aware, multi-objective model-ranking algorithm**.

The system would filter incompatible models, estimate the utility of eligible models, and select the candidate offering the strongest predicted trade-off.

## 7.3 Mathematical Formulation

Let:

- q represent a request.
- M represent the set of available models.
- Q(Mᵢ, q) represent predicted response quality.
- C(Mᵢ, q) represent predicted monetary cost.
- L(Mᵢ, q) represent predicted latency.
- F(q) represent the set of models satisfying mandatory constraints.

A candidate utility function is:

U(Mᵢ, q) = αQ(Mᵢ, q) − βC(Mᵢ, q) − γL(Mᵢ, q)

Where α, β, and γ determine the relative importance of the objectives.

Because quality, cost, and latency have different units, their values must be normalised or converted to comparable utility units.

The routing decision is:

M* = argmax U(Mᵢ, q), for Mᵢ in F(q)

This is a proposed synthesis informed by the literature, not an algorithm attributed to one of the reviewed authors.

Reliability can be incorporated through hard eligibility constraints, a separate prediction term, or a risk-adjusted objective.

## 7.4 Proposed System Components

### 7.4.1 Request Processor

Receives user requests and extracts routing-relevant metadata.

### 7.4.2 Prompt Analysis Module

Identifies task characteristics and estimates complexity or capability requirements.

### 7.4.3 Model Registry

Maintains information about candidate models, including:

- Provider.
- Model identifier.
- Supported capabilities.
- Context-window constraints.
- Price.
- Rate-limit information.
- Availability status.

### 7.4.4 Suitability Estimator

Predicts how well candidate models are likely to handle the request.

This component could use:

- Classification.
- Embedding similarity.
- Historical task performance.
- Model capability profiles.

### 7.4.5 Cost and Latency Estimator

Predicts expected execution cost and response time.

### 7.4.6 Routing Policy Engine

Combines suitability estimates with configuration and constraints.

It ranks eligible models and chooses one for execution.

### 7.4.7 Provider Adapter Layer

Provides a consistent interface for invoking different model APIs.

The adapters handle provider-specific request formats, authentication, responses, token usage, and error structures.

### 7.4.8 Fallback and Recovery Module

Responds to retryable execution failures.

Fallback decisions should account for:

- Remaining request budget.
- Remaining time.
- Provider health.
- Model compatibility.
- Retry limits.
- Potential duplicate execution.
- Partial or uncertain request completion.

### 7.4.9 Observability and Evaluation Module

Records:

- Selected model.
- Routing decision.
- Routing duration.
- Input and output tokens.
- Estimated cost.
- Actual cost.
- End-to-end latency.
- Execution outcome.
- Failure category.
- Fallback attempts.
- Evaluation scores.

These observations support both operational monitoring and research evaluation.

---

# 8. Experimental Evaluation Plan

## 8.1 Research Objective

Evaluate whether prompt-aware, multi-objective model routing can improve cost efficiency and operational reliability while maintaining acceptable response quality and latency.

## 8.2 Research Questions

**RQ1:** Does prompt-aware routing reduce average cost per request compared with static model selection while maintaining a predefined quality level?

**RQ2:** Does incorporating cost and latency estimates improve routing performance compared with quality-only selection?

**RQ3:** How does the proposed routing policy perform on tasks that differ from its training or calibration distribution?

**RQ4:** Does operational-health-aware fallback improve successful request completion under controlled provider failures?

**RQ5:** What computational and latency overhead is introduced by the routing algorithm?

## 8.3 Hypotheses

**H1:** Prompt-aware routing achieves lower average request cost than a fixed strong-model baseline while satisfying a predefined quality constraint.

**H2:** A multi-objective routing policy achieves a more favourable cost-latency-quality trade-off than a quality-only routing policy.

**H3:** Operational-health-aware fallback improves request completion rates under injected provider failures.

**H4:** Routing overhead remains sufficiently small that it does not eliminate the benefits of model selection.

These hypotheses should be converted into measurable acceptance criteria before experimentation.

## 8.4 Recommended Baselines

### Baseline 1: Fixed Strong-Model Routing

All requests are processed by the same high-capability model.

Purpose: Establish a quality-oriented reference.

### Baseline 2: Fixed Low-Cost Model

All requests are processed by a cheaper model.

Purpose: Establish a cost-oriented reference.

### Baseline 3: Cheapest-Eligible Routing

The system selects the cheapest model satisfying the request's mandatory capability requirements.

Purpose: Determine whether intelligent suitability prediction improves over simple cost minimisation.

### Baseline 4: Prompt-Aware Routing

The router selects models using prompt-derived suitability predictions.

Purpose: Isolate the benefit of prompt awareness.

### Baseline 5: Cost-Quality Routing

The router combines predicted suitability with monetary cost.

Purpose: Evaluate multi-objective selection without additional latency or health features.

### Proposed System

The complete router combines prompt suitability, quality requirements, cost, latency, capability constraints, and operational recovery.

Purpose: Evaluate the incremental value of the proposed architecture.

An additional FrugalGPT-style cascade could be included if the experimental budget allows.

## 8.5 Evaluation Metrics

### Response Quality

Measures the quality of generated answers using task-appropriate evaluation methods.

### Average Cost per Request

Measures actual monetary expenditure averaged across evaluated requests.

Cost accounting should include router-related inference, verification, and fallback calls.

### Task Success Rate

Measures the proportion of requests that satisfy defined acceptance criteria.

### P50 and P95 End-to-End Latency

Measure typical and high-percentile request completion time.

### Routing Overhead

Measures the time and computational resources consumed by the routing process itself.

### Strong-Model Call Rate

Measures how frequently relatively expensive models are invoked.

### Fallback Success Rate

Measures successful recovery following eligible failures.

### Budget Violation Rate

Measures the proportion of requests exceeding their permitted budgets.

### Out-of-Distribution Performance

Measures routing effectiveness on unfamiliar task categories or datasets.

### Cost-Quality Pareto Performance

Evaluates whether one routing policy provides better quality at a given cost or lower cost at a given quality level.

### APGR and CPT

For experiments involving strong-versus-weak model pairs, RouteLLM's APGR and CPT metrics can provide additional insight.

## 8.6 Evaluation Datasets

The benchmark suite should represent different task categories, such as:

- Mathematical reasoning.
- Programming.
- General knowledge.
- Question answering.
- Text summarisation.
- Structured data extraction.
- Instruction following.
- Open-ended writing.

The selected datasets should reflect the capabilities being tested and the practical request distribution expected by the system.

A combination of objective and preference-based evaluation may be necessary.

## 8.7 Experimental Controls

To ensure fair comparison:

1. Use the same candidate model pool.
2. Apply consistent task instructions.
3. Record model versions.
4. Use the same evaluation requests.
5. Standardise relevant decoding parameters where supported.
6. Record actual token usage and pricing assumptions.
7. Separate router computation from model execution.
8. Keep training, calibration, and test datasets separate.
9. Evaluate statistical uncertainty.
10. Report unsuccessful and timed-out requests rather than excluding them silently.

## 8.8 Ablation Studies

Ablation experiments determine whether each component contributes meaningfully.

Recommended comparisons include:

- Full system.
- System without prompt-aware selection.
- System without cost prediction.
- System without latency awareness.
- System without health-aware routing.
- System without operational fallback.

If removing a component does not materially affect the measured outcomes, the necessity of that component should be reconsidered.

## 8.9 Failure Injection

Provider recovery should be evaluated using controlled failures such as:

- Simulated timeouts.
- Rate limiting.
- Provider unavailability.
- Temporary server errors.
- Connection interruptions.

Not every failure is appropriate for automatic retry.

Authentication failures, invalid request formats, and unsupported capabilities generally require different treatment from temporary service failures.

---

# 9. Research Novelty and Contribution

A project is not academically novel merely because it combines several existing methods.

Its contribution must be defined precisely and supported by evidence.

Possible contributions include:

## 9.1 Architectural Contribution

Designing a modular gateway that integrates learned model suitability with cost, latency, capability, and operational constraints.

## 9.2 Algorithmic Contribution

Defining and evaluating a lightweight routing policy that combines multiple prediction signals under explicit constraints.

## 9.3 Empirical Contribution

Providing a controlled comparison between static routing, cheapest-eligible routing, prompt-aware routing, and multi-objective routing.

## 9.4 Reliability Contribution

Measuring the effect of operational fallback under controlled provider-failure scenarios.

## 9.5 Generalisation Contribution

Investigating how routing policies respond to unfamiliar tasks and changes to the available model pool.

The strongest achievable contribution may be a combination of architectural design and rigorous empirical evaluation rather than introducing a completely new machine-learning algorithm.

---

# 10. Recommended Literature Review Structure for Chapter Two

## 2.1 Introduction

Introduce intelligent model routing and explain its relevance to modern LLM applications.

## 2.2 Large Language Models and Model Heterogeneity

Discuss differences in capabilities, costs, inference requirements, and task specialisation.

## 2.3 LLM Serving and Inference Optimisation

Explain cost, latency, resource constraints, and deployment efficiency.

## 2.4 AI Model Routing Fundamentals

Define routing, cascading, ensembling, operational fallback, and internal MoE routing.

## 2.5 Classification-Based Routing

Review Hybrid LLM and Shnitzer et al.

## 2.6 Preference-Based Routing

Review RouteLLM.

## 2.7 Embedding-Based and Contrastive Routing

Review RouterDC.

## 2.8 Reward-Guided Routing

Review Zooter.

## 2.9 Cascading and Decision-Theoretic Routing

Review FrugalGPT and AutoMix.

## 2.10 Ensemble-Based Alternatives

Review LLM-Blender.

## 2.11 Resource-Aware and Multi-Objective Routing

Use both survey papers and relevant primary studies.

## 2.12 Comparative Analysis of Existing Approaches

Compare algorithm objectives, training requirements, inference overhead, generalisation, and operational implications.

## 2.13 Identified Research Gaps

Explain the unresolved or insufficiently evaluated issues most relevant to the proposed project.

## 2.14 Proposed Conceptual Framework

Describe the intended architecture and routing policy.

## 2.15 Chapter Summary

Summarise the literature and connect its findings to the proposed methodology.

---

# 11. Recommended Reading Order

The papers should be read in the following order to develop the necessary concepts progressively.

### Stage 1: Understand the Research Field

1. *Dynamic Model Routing and Cascading for Efficient LLM Inference: A Survey* — Moslem and Kelleher (2026).

2. *Doing More with Less: A Survey on Routing Strategies for Resource Optimisation in Large Language Model-Based Systems* — Varangot-Reille et al. (2025).

### Stage 2: Understand Core Routing Algorithms

3. *Hybrid LLM: Cost-Efficient and Quality-Aware Query Routing* — Ding et al. (2024).

4. *RouteLLM: Learning to Route LLMs with Preference Data* — Ong et al. (2024).

5. *Large Language Model Routing with Benchmark Datasets* — Shnitzer et al. (2023).

### Stage 3: Understand Cost-Aware Cascading

6. *FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance* — Chen et al. (2023).

7. *AutoMix: Automatically Mixing Language Models* — Aggarwal et al. (2023/2024).

### Stage 4: Study Advanced Model Suitability Learning

8. *RouterDC: Query-Based Router by Dual Contrastive Learning for Assembling Large Language Models* — Chen et al. (2024).

9. *Routing to the Expert: Efficient Reward-guided Ensemble of Large Language Models* — Lu et al. (2023).

### Stage 5: Understand Alternatives to Single-Model Routing

10. *LLM-Blender: Ensembling Large Language Models with Pairwise Ranking and Generative Fusion* — Jiang et al. (2023).

---

# 12. Literature Search Strategy

## 12.1 Original Search String

"AI Model Routing Algorithms"

This describes the subject appropriately but may be too restrictive for a comprehensive literature search.

Relevant papers often use alternative terminology.

## 12.2 Recommended Search String

("large language model" OR LLM OR "foundation model")

AND

("model routing" OR "query routing" OR "model selection" OR "model cascading" OR "adaptive routing")

AND

(algorithm OR optimization OR "cost efficiency" OR "inference efficiency" OR "quality-aware")

## 12.3 Additional Search Terms

Useful alternatives include:

- Cost-aware LLM routing.
- Prompt-aware model selection.
- Dynamic LLM routing.
- Multi-model LLM serving.
- Learning to route LLMs.
- Preference-based model routing.
- Adaptive LLM cascading.
- Model capability prediction.
- Latency-aware LLM routing.
- LLM gateway optimisation.
- Reliability-aware model selection.
- LLM inference resource allocation.

## 12.4 Research Databases

Relevant sources include:

- Google Scholar.
- arXiv.
- ACL Anthology.
- IEEE Xplore.
- ACM Digital Library.
- Semantic Scholar.
- OpenReview.

## 12.5 Systematic Review Considerations

If the literature review is presented as systematic, the research process should document:

- Databases searched.
- Exact search strings.
- Search dates.
- Inclusion criteria.
- Exclusion criteria.
- Duplicate removal.
- Title and abstract screening.
- Full-text screening.
- Final included studies.

A systematic review should not be claimed without carrying out and documenting these procedures.

---

# 13. Overall Findings and Conclusion

The reviewed literature demonstrates that intelligent model selection is a significant research area within LLM serving and inference optimisation.

The major findings are:

1. Different language models have complementary strengths, making static model selection potentially inefficient.

2. Classification-based routing can predict model suitability using benchmark and query-level information.

3. Embedding-based approaches can represent relationships between prompts and model expertise.

4. Preference-based routing can learn when a stronger model is worth invoking without relying exclusively on objectively correct answers.

5. Reward-guided approaches can distil performance information into efficient routing policies.

6. Cascading systems can reduce cost by accepting adequate responses from cheaper models and escalating when required.

7. Decision-theoretic approaches provide a framework for considering uncertainty and sequential decisions.

8. Ensemble systems may improve response quality but introduce additional cost and latency.

9. Routing effectiveness depends on the workload, model pool, evaluation criteria, and quality of training data.

10. Practical routing architectures must also consider engineering constraints such as latency, capabilities, provider availability, and operational failure recovery.

For the proposed FYP, the most promising direction is a **lightweight, prompt-aware, cost-aware, and latency-aware model-routing system with automatic operational fallback**.

Rather than assuming that the most expensive model is always preferable, the system would estimate model suitability and make selection decisions under defined constraints.

The project's contribution should be established through rigorous comparison with simpler routing strategies.

The literature provides strong foundations for the model-selection problem, but the final research gap and novelty claim must be checked against additional relevant studies before submission.

---

# 14. References

The following references use an author–year format with complete paper titles and persistent arXiv links. For final academic submission, format them consistently according to the department's required citation style and verify venue-specific bibliographic metadata.

**[1] Aggarwal, P., et al. (2024).** *AutoMix: Automatically Mixing Language Models.* Advances in Neural Information Processing Systems (NeurIPS 2024). First released as arXiv:2310.12963 in 2023.

Aggarwal, P., Anand, A., Faruqui, M., Gupta, A., Kappaganthu, K., Madaan, A., Mausam, M., Mishra, S., Potharaju, S.P., Rajagopal, D., Upadhyay, S., Yang, Y., & Zhou, P. (2023). AutoMix: Automatically Mixing Language Models. ArXiv, abs/2310.12963.

https://arxiv.org/abs/2310.12963

**[2] Chen, S., Jiang, W., Lin, B., Kwok, J. T., & Zhang, Y. (2024).** *RouterDC: Query-Based Router by Dual Contrastive Learning for Assembling Large Language Models.* Advances in Neural Information Processing Systems (NeurIPS 2024).

Chen, S., Jiang, W., Lin, B., Kwok, J.T., & Zhang, Y. (2024). RouterDC: Query-Based Router by Dual Contrastive Learning for Assembling Large Language Models. ArXiv, abs/2409.19886.

https://arxiv.org/abs/2409.19886

**[3] Shnitzer, T., et al. (2023).** *Large Language Model Routing with Benchmark Datasets.* arXiv preprint arXiv:2309.15789.

Shnitzer, T., Ou, A., Silva, M., Soule, K., Sun, Y., Solomon, J., Thompson, N., & Yurochkin, M. (2023). Large Language Model Routing with Benchmark Datasets. ArXiv, abs/2309.15789.

https://arxiv.org/abs/2309.15789

**[4] Lu, K., et al. (2023).** *Routing to the Expert: Efficient Reward-guided Ensemble of Large Language Models.* arXiv preprint arXiv:2311.08692.

Lu, K., Yuan, H., Lin, R., Lin, J., Yuan, Z., Zhou, C., & Zhou, J. (2023). Routing to the Expert: Efficient Reward-guided Ensemble of Large Language Models. North American Chapter of the Association for Computational Linguistics.

https://arxiv.org/abs/2311.08692

**[5] Jiang, D., Ren, X., & Lin, B. Y. (2023).** *LLM-Blender: Ensembling Large Language Models with Pairwise Ranking and Generative Fusion.* Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (ACL 2023).

Jiang, D., Ren, X., & Lin, B. (2023). LLM-Blender: Ensembling Large Language Models with Pairwise Ranking and Generative Fusion. Annual Meeting of the Association for Computational Linguistics.

https://arxiv.org/abs/2306.02561

**[6] Chen, L., Zaharia, M., & Zou, J. (2023).** *FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance.* arXiv preprint arXiv:2305.05176.

Chen, L., Zaharia, M.A., & Zou, J.Y. (2023). FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance. ArXiv, abs/2305.05176.

https://arxiv.org/abs/2305.05176

**[7] Ding, D., et al. (2024).** *Hybrid LLM: Cost-Efficient and Quality-Aware Query Routing.* International Conference on Learning Representations (ICLR 2024).

Ding, D., Mallick, A., Wang, C., Sim, R., Mukherjee, S., Rühle, V., Lakshmanan, L.V., & Awadallah, A.H. (2024). Hybrid LLM: Cost-Efficient and Quality-Aware Query Routing. ArXiv, abs/2404.14618.

https://arxiv.org/abs/2404.14618

**[8] Moslem, Y., & Kelleher, J. D. (2026).** *Dynamic Model Routing and Cascading for Efficient LLM Inference: A Survey.* arXiv preprint arXiv:2603.04445, version 3.

Moslem, Y., & Kelleher, J.D. (2026). Dynamic Model Routing and Cascading for Efficient LLM Inference: A Survey. ArXiv, abs/2603.04445.

https://arxiv.org/abs/2603.04445

**[9] Varangot-Reille, C., et al. (2025).** *Doing More with Less: A Survey on Routing Strategies for Resource Optimisation in Large Language Model-Based Systems.* arXiv preprint arXiv:2502.00409, version 3.

Varangot-Reille, C., Bouvard, C., Ciancone, M., Gourru, A., Schaeffer, M., & Jacquenet, F. (2025). Doing More with Less: A Survey on Routing Strategies for Resource Optimisation in Large Language Model-Based Systems. J. Artif. Intell. Res., 86.

https://arxiv.org/abs/2502.00409

**[10] Ong, I., et al. (2024).** *RouteLLM: Learning to Route LLMs with Preference Data.* arXiv preprint arXiv:2406.18665, version 4 (2025).

Ong, I., Almahairi, A., Wu, V., Chiang, W., Wu, T., Gonzalez, J.E., Kadous, M.W., & Stoica, I. (2024). RouteLLM: Learning to Route LLMs with Preference Data. ArXiv, abs/2406.18665.

https://arxiv.org/html/2406.18665v4

---

# 15. Final Recommendations for the FYP

Based on the ten reviewed papers, the following research direction is recommended.

**Primary research foundation:**

- Hybrid LLM for quality-aware selection.
- RouteLLM for learned routing and evaluation.
- FrugalGPT for cost-aware cascading.
- RouterDC for model-specific prompt suitability.
- AutoMix for uncertainty and escalation decisions.

**Supporting research:**

- Shnitzer et al. for benchmark-based correctness prediction.
- Zooter for reward-guided expertise learning.
- LLM-Blender for understanding response-level ensemble alternatives.
- Both surveys for theoretical framing and research classification.

**Recommended implementation priority:**

First, establish a reliable multi-provider model-execution and measurement layer.

Second, implement static, cheapest-eligible, and prompt-aware routing baselines.

Third, develop a cost-quality-latency ranking policy and evaluate its incremental benefit.

Fourth, introduce operational fallback and validate it with controlled fault injection.

Finally, compare the resulting system against the established baselines using response quality, cost, latency, reliability, and routing overhead.

**Central research question:**

*To what extent can a lightweight, prompt-aware, multi-objective LLM routing policy reduce inference cost and maintain response quality while satisfying latency constraints and improving reliability through automatic fallback?*

This question provides a coherent foundation for the proposed algorithm, system architecture, experimental methodology, and final-year research contribution.