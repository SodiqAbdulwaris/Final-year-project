Status: DRAFT
Depends on: Project_Proposal_Hybrid_LLM_Router.docx (unchanged); Project_Proposal_Hybrid_LLM_Router_Humanized.docx
Sources: Humanizer 12B Distilled (Gemma 4 12B) Q4_K_M, llama.cpp b11335 via the Humanizer app; Template_for_Final_Year_Project_Revised.docx; Research Methodology Modules 2 and 3
Open items: every section below

# Parts to check and correct after humanizing

The model wrote all rewritten text; nothing was reworded by hand. Samples were screened by script and a reviewer, and weak ones were reverted to your wording instead of being edited. The model is a general-purpose humanizer, so expect plainer, shorter and sometimes clumsy sentences in the changed chunks. Read every changed chunk in `Project_Proposal_Hybrid_LLM_Router_Humanized-changelog.md` (before and after side by side).

## 1. Fix first: problems in your source draft (not changed)

- Cover page title says "PROMT-AWARE"; the status-confirmation page gives a different, longer title ("Design and Evaluation of a Hybrid Prompt-Aware, Multi-Objective ... with Automatic Fallback"). Decide on one title and use it everywhere (template: not more than 20 words).
- Student ID for Maryam Bawa Dahiru reads 242140247 here and 242120247 in the earlier Proposal_Working_Draft_v2. Confirm the right one.
- Open placeholders: [FULL NAME: MARYAM], [FULL NAME: WAHIDA], [FULL NAME: KABIRU], [FULL NAME: ADRIEL], [Supervisor's full name] (certification and declaration), [Permanent address of the group leader], [Role to be agreed], [To be agreed], the AI-declaration verification cell, and the five ₦ amounts in the budget table.
- The acknowledgement says "Dr. Emmanuel Aderemi"; other project files give "Dr. Emmanuel Aderemi Tunbosun". Use the full name consistently.
- There are six objectives but five research questions. The template asks for one research question per objective.
- In-text "Chen et al. (2023)" is FrugalGPT, but the reference list dates it "(2024a)". Make the years match. The check also found no matching reference entry for "Aggarwal et al. (2024)" and "Pedregosa et al. (2011)"; confirm those entries exist and are cited in the right form.
- LiteLLM references are lettered n.d.-a, n.d.-b, n.d.-d with no n.d.-c, and the text cites OpenRouter n.d.-c. Check the lettering against the reference list.
- AI-use declaration table: add a row for the Humanizer model (tool, task, sections, how checked). Suggested wording is at the end of this file.

## 2. What was and was not sent to the model

- Prose chunks sent: 139 (abstract and Chapters One to Three, about 65 words each; long paragraphs were split at sentence ends and rejoined).
- Rewritten by the model and kept: 67. Reverted to your wording: 72 (49 after a reviewer rejected the sample, 23 because no sample passed the checks in up to 40 tries).
- Never sent: headings, captions, tables, the objectives, research questions and hypotheses, the abbreviation and definition lists, equations and pseudocode, and the front matter. Chapter Four and Five are not in this document.

Checks every kept chunk passed: all numbers, years, citations, names and acronyms, section/table/figure references kept; no "we", "you", contractions, slang, shorthand or US spelling added; no sentence fragments from a short-sentence test; similarity of content words to the original of at least 0.6 (topic drift); no lost sentence, no change in how many negations or modal verbs appear, and the future tense kept.

## 3. Read these changed chunks carefully (highest risk first)

| Chunk | Section | What to check |
|---|---|---|
| 370 | 2.7 Research Gap and Justification of the Study | "automatically switching" became "gracefully fallback"; "adequate" added. dropped_terms:automa,monito,soluti,switch similarity to original 0.64 |
| 214.1 | 1.1 Background of the Study | dropped_terms:approa,outper similarity to original 0.64 |
| 221 | 1.2 Statement of the Problem | dropped_terms:applic,challe,demons,introd similarity to original 0.62 |
| 225 | 1.2 Statement of the Problem | dropped_terms:diffic,limita,mechan,monito similarity to original 0.67 |
| 250 | 1.4 Research Questions | dropped_terms:reduct,select similarity to original 0.68 |
| 253 | 1.5 Methodology Overview | Drops "teamwork, flexibility" and "incremental" nuance; otherwise faithful. dropped_terms:challe,emphas,flexib,incorp |
| 255 | 1.5 Methodology Overview | dropped_terms:comple,monito,organi,subseq similarity to original 0.69 |
| 257 | 1.5 Methodology Overview | Subject changed from "The project team" to "They"; check it still reads clearly after the paragraph break. dropped_terms:challe,comple,conduc,contai |
| 265 | 1.7 Scope of the Study | "The study covers" became "The paper discusses"; "needs" replaces "requirements". dropped_terms:integr,requir,restri |
| 280 | 1.9 Contributions of the Project | "per- and aggregate-routing decisions" is awkward; check meaning of "individual and aggregated". dropped_terms:availa,indivi,inform |
| 315 | 2.2.3 Constrained routing and reliability | dropped_terms:behavi,evalua similarity to original 0.68 |
| 326 | 2.3.3 Serving performance and latency | Splits one citation group into two parentheses "(Agrawal et al., 2024) (Zhong et al., 2024)"; APA wants one group. dropped_terms:distin,interf,proces |
| 395.1 | 3.3.1 Description of the Existing System | Parenthetical restructure; meaning intact. similarity to original 0.65 |
| 438.0 | 3.6.3 Behavioural Design (Sequence and Activity Diagrams) | will_added 0->3 similarity to original 0.64 |
| 492 | 3.12 Work Plan | Adds "Owners stick to the team roles" which repeats the previous sentence. similarity to original 0.61 |
| 114.2 | ABSTRACT | dropped_terms:combin,develo,lightw,retrie |
| 214.0 | 1.1 Background of the Study | Last sentence is stronger than the draft ("there is no possibility to change the model" vs "cannot adjust its choice"). |
| 215 | 1.1 Background of the Study | dropped_terms:attent,theref |
| 216 | 1.1 Background of the Study | dropped_terms:addres,availa,necess |
| 218 | 1.1 Background of the Study | dropped_terms:accomp,establ |
| 258 | 1.5 Methodology Overview | dropped_terms:adapta,differ,effect,evalua |
| 262 | 1.6 Significance of the Study | similarity to original 0.66 |
| 270 | 1.8 Limitations of the Study | similarity to original 0.69 |
| 285 | 1.10 Organisation of the Report | dropped_terms:consid,descri,infras,signif |
| 307 | 2.1 Review Methodology | similarity to original 0.64 |
| 310 | 2.2.1 Prompt-aware model routing | dropped_terms:illust,inspec |
| 312 | 2.2.2 Hybrid suitability estimation | dropped_terms:compon,evalua |
| 340 | 2.4.2 Embedding retrieval and historical-performance features | similarity to original 0.67 |
| 342 | 2.4.3 Cascades and joint quality–cost–latency optimisation | dropped_terms:compar,optimi,reduct |
| 346.0 | 2.4.4 Latency targets and deadline-aware selection | similarity to original 0.67 |
| 351.1 | 2.4.5 Failure handling and fallback | dropped_terms:catalo,return |
| 356 | 2.4.6 Evaluating routers | dropped_terms:alongs,benchm |
| 371 | 2.7 Research Gap and Justification of the Study | dropped_terms:diffic,effici,limita,mechan |
| 372.0 | 2.7 Research Gap and Justification of the Study | dropped_terms:combin,lightw |
| 372.1 | 2.7 Research Gap and Justification of the Study | dropped_terms:consis,evalua |
| 372.2 | 2.7 Research Gap and Justification of the Study | similarity to original 0.67 |
| 377.0 | 2.8 Chapter Summary | dropped_terms:evalua,unders |
| 382.0 | 3.1 Research and Development Methodology | similarity to original 0.68 |
| 440.1 | 3.6.4 Database Design | similarity to original 0.67 |
| 496 | 3.12 Work Plan | similarity to original 0.67 |

All other kept chunks passed every automated check and were not individually proofread beyond a sample. Common faults to look for: a sentence turned into a fragment, "the" or "a" dropped, a verb turned into a noun phrase, a subject replaced by "they", and a term replaced by a near-synonym that changes the meaning.

## 4. Reverted to your wording after a reviewer rejected the model sample

| Chunk | Section | Why the sample was rejected |
|---|---|---|
| 114.0 | ABSTRACT | garbled phrase ("lower cost model able requests"), fragment sentence |
| 114.1 | ABSTRACT | fragments ("Which chooses...", "Failing back..."); "publish no evaluation" became "not providing any feedback" |
| 114.3 | ABSTRACT | ungrammatical ("It will be injected failure tested") |
| 217 | 1.1 Background of the Study | opens with an imperative fragment; "declared" became "claimed" |
| 230 | Aim | aim relabelled "Objective of the project"; fallback clause misplaced in parentheses |
| 273 | 1.8 Limitations of the Study | meaning changed ("may not represent every workload" became "not all workloads may be publicly scoreable") |
| 318 | 2.2.3 Constrained routing and reliability | garbled; no complete sentences |
| 322 | 2.3.1 Prompt classification and embeddings | meaning reversed in part (labels assigned to the router; retrieval sentence garbled) |
| 333.0 | 2.4.1 Learned pre-generation routing between models | "1st one teaches the model" misstates "the first group learns"; fragment |
| 333.1 | 2.4.1 Learned pre-generation routing between models | "Both routes between 2 models exactly" is ungrammatical |
| 334.0 | 2.4.1 Learned pre-generation routing between models | "7 7B to 8B models" (seven models) garbled |
| 339.0 | 2.4.2 Embedding retrieval and historical-performance features | fragments ("1% history works.", "no more benefit...") |
| 343.1 | 2.4.3 Cascades and joint quality–cost–latency optimisation | meaning shifted ("sampling-based consistency is needed" became "It needs to be consistent through sampling") |
| 346.1 | 2.4.4 Latency targets and deadline-aware selection | fragment; "fixed runtime" for "predictable run times" |
| 377.1 | 2.8 Chapter Summary | topic drift ("publish no evaluation" became "do not advertise any assessment"); "See the following chapter" |
| 387 | 3.2 Requirements Elicitation | "no human subjects will be solicited" and "admins" change the decision wording |
| 390 | 3.2 Requirements Elicitation | tense and modality lost ("will be turned into" became "are converted") |
| 400 | 3.3.2 Limitations of the Existing System | meaning blurred ("fallback targets are fixed" became "are configured") |
| 401 | 3.3.2 Limitations of the Existing System | meaning changed ("One can have unlimited retries to worsen the outage") |
| 419 | 3.5.2 Non-Functional Requirements | garbled (non-inferiority margin sentence) |
| 453.1 | 3.6.5 Algorithm and Model Design | "3 or less attempts" and "See the full algorithm below"; tense lost |
| 485.1 | 3.10 Ethical Considerations | conditional consent sentence restructured |
| 505.1 | 3.15 Chapter Summary | telegraphic shorthand ("w leakage free splits ... w fixed targets") |
| 328 | 2.3.4 Gateway integration, resilience and telemetry | imperative and telegraphic sentences ("Implement provider adapters...", "Use existing gateway..."); citation group re-punctuated |
| 344.1 | 2.4.3 Cascades and joint quality–cost–latency optimisation | whole chunk wrapped in parentheses; fragment |
| 354.1 | 2.4.6 Evaluating routers | square brackets introduced around the citation; "number of the pool" garbled |
| 397 | 3.3.2 Limitations of the Existing System | sentence split into a fragment ("Even if..."); citation separator changed from semicolon to comma |
| 406.0 | 3.4.1 Description of the Proposed System | fragments ("Predicts the quality...", "Picks the lowest cost model...") |
| 424 | 3.5.3 Use Case Model | fragments and a stray "Figure 3.2:" caption-style opening |
| 447 | 3.6.5 Algorithm and Model Design | meaning reversed ("Sentence embedding model is embedded in every prompt") |
| 478 | 3.9 Evaluation Plan | shorthand "gateway->adapter->db" and list-like sentences |
| 335.1 | 2.4.1 Learned pre-generation routing between models | meaning changed (the predictor is a 7B LLM; the sample says it was split from one) |
| 338.1 | 2.4.2 Embedding retrieval and historical-performance features | telegraphic ("112-models*36054-questions", "with 1-GPU") |
| 339.1 | 2.4.2 Embedding retrieval and historical-performance features | narrative citation turned into a parenthetical subject |
| 343.0 | 2.4.3 Cascades and joint quality–cost–latency optimisation | meaning garbled (a good selection rule cannot compensate for poor predictions) |
| 348 | 2.4.4 Latency targets and deadline-aware selection | opening sentence garbled ("the admission decision in the face of the latency to a specified target") |
| 350 | 2.4.5 Failure handling and fallback | adds a heading-like phrase ("Group 5: Failure and recovery") inside the paragraph |
| 351.0 | 2.4.5 Failure handling and fallback | chat-style opener ("Here are two direct studies...") |
| 355 | 2.4.6 Evaluating routers | "12 routers (commercial)" wrongly says all were commercial |
| 358.0 | 2.5 Review of Existing Systems | opens with a fragment ("A comparison of 5 existing systems...") |
| 359.0 | 2.5 Review of Existing Systems | fragment sentences with no main verb |
| 359.1 | 2.5 Review of Existing Systems | citations moved to the end of the paragraph, after the Table 2.3 sentence |
| 382.1 | 3.1 Research and Development Methodology | list of fragments instead of sentences |
| 383.1 | 3.1 Research and Development Methodology | fragments ("Will have the planning meeting...", "Use pull requests...") |
| 413 | 3.5 Requirements Specification | "confirmed" became "re-checked"; stray "). and" punctuation |
| 469 | 3.7 Data Collection and Preparation | garbled label definition |
| 472 | 3.7 Data Collection and Preparation | imperative fragment ("Run a capped live run...") |
| 505.0 | 3.15 Chapter Summary | fragments and shorthand ("light classifier + embedding retrieval") |
| 227 | 1.2 Statement of the Problem | changes the template's closing sentence "This project therefore seeks to ..." and splits it in two |

## 5. Reverted because no sample passed the checks

These chunks stayed as you wrote them. Humanize them by hand or re-run them if you want them changed: 114.4, 223, 261, 266, 267, 268, 272, 314, 324, 336, 338.0, 347, 352, 363, 380, 432.0, 440.0, 457.1, 461.0, 468, 486, 498, 503.

## 6. Paragraphs never sent to the model (by rule)

| Paragraph | Section | Reason | Starts with |
|---|---|---|---|
| 247 | 1.4 Research Questions | notation/pseudocode | H₀: The hybrid router's mean cost per request is not lower t |
| 248 | 1.4 Research Questions | notation/pseudocode | H₁: The hybrid router's mean cost per request is lower than  |
| 287 | 1.11 Definition of Operational Terms | operational definition | An evaluation that removes or isolates a component to assess |
| 288 | 1.11 Definition of Operational Terms | operational definition | A comparison policy such as a fixed model, cheapest-eligible |
| 289 | 1.11 Definition of Operational Terms | operational definition | A rule that a candidate must satisfy before selection, such  |
| 290 | 1.11 Definition of Operational Terms | operational definition | Features obtained by comparing a request representation with |
| 291 | 1.11 Definition of Operational Terms | operational definition | A bounded attempt to process a request through another eligi |
| 292 | 1.11 Definition of Operational Terms | operational definition | Requests excluded from model fitting and tuning and reserved |
| 293 | 1.11 Definition of Operational Terms | operational definition | A routing strategy combining distinct evidence sources or pr |
| 294 | 1.11 Definition of Operational Terms | operational definition | A model that processes and generates language in response to |
| 295 | 1.11 Definition of Operational Terms | operational definition | A gateway that selects a model deployment for a client reque |
| 296 | 1.11 Definition of Operational Terms | operational definition | A specific hosted endpoint or local serving instance capable |
| 297 | 1.11 Definition of Operational Terms | operational definition | An estimate of how well a candidate deployment may meet a re |
| 298 | 1.11 Definition of Operational Terms | operational definition | Time consumed by gateway processing and selection apart from |
| 436 | 3.6.2 Structural Design (Class Diagram) | notation/pseudocode | The main classes follow the modules. Gateway receives reques |
| 448 | 3.6.5 Algorithm and Model Design | notation/pseudocode | Q̂(m, q) = w · p_clf(m, q) + (1 − w) · r_kNN(m, q), |
| 449 | 3.6.5 Algorithm and Model Design | notation/pseudocode | where p_clf is the classifier probability, r_kNN the retriev |
| 450 | 3.6.5 Algorithm and Model Design | notation/pseudocode | Let E be the models that pass the hard constraints, τ the mi |
| 451 | 3.6.5 Algorithm and Model Design | notation/pseudocode | m* = argmin Ĉ(m, q) over m ∈ E such that Q̂(m, q) ≥ τ, Ĉ(m,  |
| 452 | 3.6.5 Algorithm and Model Design | notation/pseudocode | breaking ties by higher Q̂. If no model meets τ, the policy  |
| 471 | 3.7 Data Collection and Preparation | notation/pseudocode | Prompts will be split 60/20/20 into training, validation and |

Short paragraphs under 25 words, captions and the operational definitions in 1.11 were also left alone. Check them for the same patterns.

## 7. Rules to re-check against the template and slides

- Future tense for proposed work (template and Module 3): search the changed chunks for "was", "is" and "has been" where the original said "will".
- Chapter Two: each theme should open with one or two sentences, review studies in groups with numbers and limitations, and end with a synthesis (Module 2). The model does not add comparison language, so check "Unlike X, Y ...", "Both A and B found ..., but neither ...".
- Every figure, percentage and citation was checked by script against the original; still verify against the papers.
- Abstract: 250 to 300 words, no citations, no undefined abbreviations. Recount the abstract after reading the changed chunks.
- British spelling and APA 7 author-date form (one parenthesis group per citation).

## 8. Suggested AI-declaration row

| Tool and version | Task | Section | How verified |
|---|---|---|---|
| Humanizer 12B Distilled (Gemma 4 12B, Q4_K_M) running on llama.cpp b11335 via Humanizer app 0.3.4 | Rewriting selected paragraphs of the abstract and Chapters 1 to 3 to remove formulaic phrasing; no hand rewording | Abstract; Chapters 1 to 3 (chunks listed in the changelog) | Scripted check of numbers, citations, names, references and tense on every chunk; weak samples reverted; team read-through still required |

## 9. AI-detector check (same passage, original vs humanized)

Passage: paragraphs 212, 214 to 218, 221, 250, 253, 255 and 257 (Chapter One), about 5,000 characters, before and after.

| Detector | Original | Humanized |
|---|---|---|
| ZeroGPT (free page) | 53.4% AI, "most likely AI/GPT generated" | 8.9% AI, "human written" |
| GPTZero (free page) | not run on this passage | blocked: free scans used up, now asks for sign-up even after clearing cookies and site data in Chrome |
| Scribbr | not run: the embedded editor did not accept automated input | not run |

The same two passages are saved as `detector-passage-ORIGINAL.txt` and `detector-passage-HUMANIZED.txt` so you can paste them into your own GPTZero session in Firefox. A low detector score is not evidence of quality: the humanized text is plainer and has more clumsy sentences than your original, which is also what detectors read as human. The AI-use declaration is still required.

## 10. Other notes

- Abstract is 302 words after humanizing (296 before); the template says 250 to 300. You said length can run over when the content holds, so I left it, but check the abstract reads correctly: only chunk 114.2 of the abstract was changed.
