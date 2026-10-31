Status: DRAFT
Depends on: Superseded earlier design
Sources: Original draft preserved by git mv
Open items: Archived historical text; excluded from assembly and active placeholder register

# Front matter (draft)

Paste each block into the matching page of `Template_for_Final_Year_Project_Revised.docx`. Nothing here invents a name, ID or date: gaps are `TODO`. Facts come from `00-source-facts.md`.

---

## 1. Title options

**Updated after the 26 Oct team guide** (see `design-reconciliation.md`, item 17). The template allows at most 20 words, capitals, concise and specific. Word counts are shown. `DECISION-NEEDED`: pick one with the supervisor.

| Option | Title | Words |
|---|---|---|
| A | A BUDGET-AWARE REQUEST ROUTER FOR HOSTED AND LOCAL LARGE LANGUAGE MODELS USING PAST-PERFORMANCE RETRIEVAL AND CONTROLLED SWITCHING | 17 |
| B | DESIGN AND EVALUATION OF A BUDGET-AWARE OPENAI-COMPATIBLE GATEWAY THAT ROUTES REQUESTS BETWEEN HOSTED AND LOCALLY SERVED LANGUAGE MODELS | 18 |
| C | AI REQUEST ROUTER: K-NN MODEL SELECTION, BUDGET BANDS AND SESSION-AWARE SWITCHING FOR HOSTED AND LOCAL LLMS | 16 |

ASSUMPTION: Option B is closest to the template's aim wording ("design, implement and evaluate"). Option A names the research idea (past-performance retrieval and switching). Option C keeps the project name.

*Superseded 16 Oct options (live-load framing), kept for the record:* "AI REQUEST ROUTER: A LOAD-AWARE GATEWAY FOR SELECTING LARGE LANGUAGE MODELS BY COST, QUALITY AND LATENCY"; "DESIGN AND EVALUATION OF AN AI REQUEST ROUTER USING PROMPT DIFFICULTY, COST AND LIVE BACKEND LOAD"; "AN OPENAI-COMPATIBLE AI REQUEST ROUTER FOR HOSTED AND SELF-HOSTED LANGUAGE MODELS WITH LIVE LOAD AWARENESS AND FAILOVER".

**Short running title (for a later journal manuscript, up to 50 characters):** `Budget-aware LLM request routing` (32 characters).

**Cover page block** (template wording, filled where known):

```
[TITLE: option chosen above, in capitals]

BY

TODO: FULL NAME OF MEMBER 1 (STUDENT ID)
TODO: FULL NAME OF MEMBER 2 (STUDENT ID)
TODO: FULL NAME OF MEMBER 3 (STUDENT ID)
TODO: FULL NAME OF MEMBER 4 (STUDENT ID)
TODO: FULL NAME OF MEMBER 5 (STUDENT ID)      (delete unused lines; template allows up to five)

A PROJECT SUBMITTED TO THE DEPARTMENT OF SOFTWARE ENGINEERING, FACULTY OF COMPUTING,
NILE UNIVERSITY OF NIGERIA, IN PARTIAL FULFILMENT OF THE REQUIREMENTS FOR THE AWARD OF
THE DEGREE OF BACHELOR OF SCIENCE (B.Sc. HONS) IN SOFTWARE ENGINEERING,
NILE UNIVERSITY OF NIGERIA

TODO: MONTH AND YEAR OF SUBMISSION (the template example is JUNE 2027)
```

---

## 2. Status confirmation for bachelor's project

| Field | Value |
|---|---|
| Project title | TODO: same as the cover page |
| Academic session | TODO: 20XX/20XX. ASSUMPTION: 2026/2027, because the proposal is dated 16 October 2026 and the course module is for first semester 2026/2027. Confirm. |
| Group members named in the agreement | TODO: full names of all group members |
| Access choice (tick one): Confidential / Restricted / Free access | TODO: group decision. Nothing in the proposal suggests confidential or restricted material. |
| Permanent address of the group leader | TODO |
| Supervisor's name | TODO: the template prints "Dr. Supervisor" as a placeholder. Replace with the real name and title. |
| Signatures and dates | Left blank for signing. |

---

## 3. Certification

Template text, filled where possible:

> This is to certify that the project titled "**TODO: title**" by **TODO: FULL NAME (STUDENT ID)**, **TODO: FULL NAME (STUDENT ID)**, **TODO: FULL NAME (STUDENT ID)** and **TODO: FULL NAME (STUDENT ID)** has been read and approved as meeting the requirements for the award of the degree of Bachelor of Science (B.Sc. Hons) in Software Engineering, Department of Software Engineering, Faculty of Computing, Nile University of Nigeria, Abuja.

Signature panel:

| Signature line | Name and role |
|---|---|
| ………………… | TODO: Project Supervisor full name, PROJECT SUPERVISOR |
| ………………… | Assoc. Prof. Ibrahim Salihu Anka, HOD SOFTWARE ENGINEERING (as printed in the template; confirm it is current) |
| ………………… | Prof. Joshua Abah, DEAN FACULTY OF COMPUTING (as printed in the template; confirm it is current) |
| ………………… | EXTERNAL EXAMINER (name TODO, assigned by the department) |

---

## 4. Declaration

Use the template wording unchanged. It already mentions generative AI, so the AI table below is required.

> We hereby declare that this project report is our own work and has not been submitted, in whole or in part, for any other degree or qualification. All sources consulted have been duly cited and acknowledged in the references, and any use of generative AI tools has been declared in this report.

Signature lines (one per member, as in the template):

```
Name (Student ID): TODO ………………………   Signature: ………………………
Name (Student ID): TODO ………………………   Signature: ………………………
Name (Student ID): TODO ………………………   Signature: ………………………
Name (Student ID): TODO ………………………   Signature: ………………………
Supervisor: ………………………   SUPERVISOR FULLNAME: TODO
```

---

## 5. Statement of individual contributions

Each member must state honestly what they contributed. The proposal does not say who does what, so every cell is TODO. The template's examples are shown only to guide the wording.

| S/N | Full name | Student ID | Role | Main contributions (modules, chapters, tasks) | Signature |
|---|---|---|---|---|---|
| 1 | TODO | TODO | TODO | TODO | |
| 2 | TODO | TODO | TODO | TODO | |
| 3 | TODO | TODO | TODO | TODO | |
| 4 | TODO | TODO | TODO | TODO | |
| 5 | TODO | TODO | TODO | TODO | |

A neutral way to split the work, if the team wants a starting point (ASSUMPTION: not in either source document; follows the guide's nine-step order and the template's example roles):

| Candidate role | Maps to |
|---|---|
| Requirements and usability | Steps 1 and 9: interviews, MoSCoW and traceability, SUS study (Chapter 3.2, 3.5, 3.9.7; Chapter 4.5) |
| Gateway, adapters and failover | Steps 2 and 8: FastAPI endpoint, hosted and local adapters, retries and circuit breaker (3.6.1; E5) |
| Registry, filters and budget ledger | Steps 3 and 4: eligibility filter, bands, atomic reservation (3.6.5; E4) |
| Routing and evaluation | Steps 5 to 7: rule and k-NN routers, calibration, hysteresis, context policies (E1 to E3) |
| Documentation, QA and literature | Test cases, coverage, Chapter 2, report assembly |

---

## 6. Declaration on the use of generative AI tools

The template requires an honest, specific table. **The team must confirm every row before submission.** Only tools actually used belong here. What is known from the project files:

- The planning notes (`PLAN.md`) record that an AI coding assistant (Claude Code, Anthropic) is being used to read sources, draft these chapter scaffolds and organise the literature-review notes.
- The proposal does not say whether any AI tool was used to write it. TODO: the team states this.

| Tool and version | Task it was used for | Chapter / section | How the output was verified or edited |
|---|---|---|---|
| Claude Code (Anthropic). TODO: confirm the exact model name and version used by the team | Extracting facts from the proposal, the 26 Oct team guide, the template and the course module; drafting section skeletons and first-draft wording for Chapters 1 to 5 and the front matter; reconciling the two plans; generating the Chapter 2 tables from the literature-review notes | Front matter; Chapters 1 to 5 (drafts and skeletons); reconciliation and README notes; literature-review notes feeding Chapter 2 | TODO: the team must state how each claim was checked against the proposal and against the original papers, and what was rewritten. Every citation to be checked against the original source before use. |
| TODO: other tools used (for example a code assistant while building the router, a grammar checker) | TODO | TODO | TODO |

If, in the end, no generative AI tool was used for the final text or code, replace the table with the template sentence: "No generative AI tools were used in the preparation of this project or report." Do not use that sentence while the drafting assistance above stands.

TODO: add the University's current AI-use policy reference if the department requires it.

---

## 7. Dedication and acknowledgement

Left for the team to write. Neither can be drafted from the project documents.

> TODO: "I dedicate this project to …"
> TODO: "I would like to express gratitude to …" (supervisor, department, anyone who supplied GPU access or API credits, if applicable)

## 8. Abstract and keywords

**Write last.** The template requires one paragraph of 250 to 300 words with real result figures. No results exist yet, so no abstract is drafted.

Keywords (template: four to six, alphabetical). Candidate list from the project documents, for the team to trim:

`budget-aware routing; k-nearest neighbours; large language models; model switching; request gateway; software engineering`

---

## 9. List of tables and list of figures

Generate these automatically in Word (References, Insert Table of Figures). Planned captions so far (numbers will shift when assembled):

| Item | Caption |
|---|---|
| Table 2.1 | Literature search strategy (with Table 2.1b counts by theme) |
| Table 2.2 | Feature comparison of existing systems and the proposed system |
| Table 2.3 | Summary of related works |
| Table 2.4 | Mapping of research gaps to project objectives |
| Table 3.1 | Functional requirements |
| Table 3.2 | Non-functional requirements |
| Table 3.3 | Tools and technologies |
| Table 3.4 | Build order and done conditions |
| Table 3.5 | Limitations of the existing way of working |
| Table 3.6 | How the proposed system addresses each limitation |
| Table 4.1 | Hardware and software requirements |
| Table 4.2 | Functional test cases |
| Tables 4.3 to 4.15 | Unit and integration results; quality table; usability results; E1 to E5 setup and results (see `ch4-ch5-skeletons.md`) |
| Table 5.1 | Achievement of objectives |
| Figure 2.1 | PRISMA-style flow of the literature search |
| Figure 2.2 | Conceptual framework of the study |
| Figure 3.1 | Methodology diagram |
| Figure 3.2 | Logical pipeline and request flow |

### Objectives and research questions (for the front pages and abstract planning)

| Objective | Short form | Research question | Experiment | Hypothesis |
|---|---|---|---|---|
| O1 | k-NN competence estimation against rules | RQ1 | E1 | H1 |
| O2 | Session-aware hysteresis | RQ2 | E2 | H2 |
| O3 | Context after switching | RQ3 | E3 | H3 |
| O4 | Budget bands and atomic reservation | RQ4 | E4 | none (verification) |
| O5 | Adapters, failover and overhead | RQ5 | E5 | none (verification) |
| O6 | Requirements, quality and usability | RQ6 | none | none |

---

## 10. List of abbreviations

Alphabetical, as the template requires. Spell each out in full at its first use in the text. Add rows as the report grows.

| Abbreviation | Meaning |
|---|---|
| API | Application Programming Interface |
| CI | Confidence Interval; Continuous Integration (state which in context) |
| DSR | Design Science Research |
| ERD | Entity Relationship Diagram |
| FR | Functional Requirement |
| GPU | Graphics Processing Unit |
| H0 | Null hypothesis |
| H1 | Alternative hypothesis (also used for the guide's hypothesis 1; written H1 to H3 in the text) |
| HTTP | Hypertext Transfer Protocol |
| ISO/IEC | International Organization for Standardization / International Electrotechnical Commission |
| k-NN | k-Nearest Neighbours |
| LLM | Large Language Model |
| MoSCoW | Must, Should, Could, Won't (requirement priorities) |
| MVP | Minimum Viable Product |
| NDPA | Nigeria Data Protection Act |
| NFR | Non-Functional Requirement |
| p95 | 95th percentile (the value that 95 percent of measurements do not exceed) |
| PRISMA | Preferred Reporting Items for Systematic Reviews and Meta-Analyses |
| RQ | Research Question |
| SMART | Specific, Measurable, Achievable, Relevant, Time-bound |
| SSRF | Server-Side Request Forgery |
| SUS | System Usability Scale |
| TTFT | Time To First Token |
| UML | Unified Modeling Language |

Product and benchmark names are not abbreviations and are not listed: FastAPI, LM Studio, LLMRouterBench, llama.cpp, LongMemEval, Ollama, RouterBench, scikit-learn, sentence-transformers, vLLM. TODO: confirm the long forms of any other short name the team adds before listing it.
