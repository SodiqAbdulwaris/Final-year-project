# Front matter (draft)

Paste each block into the matching page of `Template_for_Final_Year_Project_Revised.docx`. Nothing here invents a name, ID or date: gaps are `TODO`. Facts come from `00-source-facts.md`.

---

## 1. Title options

The template allows at most 20 words, capitals, concise and specific. Word counts are shown. Pick one with the supervisor.

| Option | Title | Words |
|---|---|---|
| A | AI REQUEST ROUTER: A LOAD-AWARE GATEWAY FOR SELECTING LARGE LANGUAGE MODELS BY COST, QUALITY AND LATENCY | 16 |
| B | DESIGN AND EVALUATION OF AN AI REQUEST ROUTER USING PROMPT DIFFICULTY, COST AND LIVE BACKEND LOAD | 16 |
| C | AN OPENAI-COMPATIBLE AI REQUEST ROUTER FOR HOSTED AND SELF-HOSTED LANGUAGE MODELS WITH LIVE LOAD AWARENESS AND FAILOVER | 17 |

ASSUMPTION: Option B is the closest to the template's aim wording ("design, implement and evaluate"). Option A names the main difference from existing routers (live load). Option C names the self-hosted angle.

**Short running title (for a later journal manuscript, up to 50 characters):** `Load-aware LLM request routing` (30 characters).

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

A neutral way to split the work, if the team wants a starting point (ASSUMPTION: not in the proposal; follows the three phases and the template's example roles):

| Candidate role | Maps to |
|---|---|
| Gateway and backend integration | Phase 1: FastAPI endpoint, hosted APIs, vLLM and Ollama adapters (Chapter 3.6.1, Chapter 4.2) |
| Classifier and scoring | Phase 1: sentence-transformers features, logistic regression, scoring function (3.6.5, 3.7, 4.6.1) |
| Resilience and load awareness | Phase 2: Redis state, Prometheus signals, circuit breaker (3.6.1, 4.6.3, 4.6.4) |
| Benchmarking and evaluation | Phase 3: RouterBench and MT-Bench harness, Grafana dashboards (3.9, 4.6) |
| Documentation and QA | Test cases (4.5), literature review (Chapter 2), report assembly |

---

## 6. Declaration on the use of generative AI tools

The template requires an honest, specific table. **The team must confirm every row before submission.** Only tools actually used belong here. What is known from the project files:

- The planning notes (`PLAN.md`) record that an AI coding assistant (Claude Code, Anthropic) is being used to read sources, draft these chapter scaffolds and organise the literature-review notes.
- The proposal does not say whether any AI tool was used to write it. TODO: the team states this.

| Tool and version | Task it was used for | Chapter / section | How the output was verified or edited |
|---|---|---|---|
| Claude Code (Anthropic). TODO: confirm the exact model name and version used by the team | Extracting facts from the proposal, template and course module; drafting section skeletons and first-draft wording for Chapters 1 to 3 and the front matter; organising literature-review notes | Front matter; Chapters 1 to 3 (drafts); literature-review notes feeding Chapter 2 | TODO: the team must state how each claim was checked against the proposal and against the original papers, and what was rewritten. Every citation to be checked against the original source before use. |
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

`cost optimisation; large language models; latency; load balancing; model routing; request gateway`

---

## 9. List of tables and list of figures

Generate these automatically in Word (References, Insert Table of Figures). Planned captions so far:

| Item | Caption |
|---|---|
| Table 2.1 | Literature search strategy |
| Table 2.2 | Feature comparison of existing systems and the proposed system |
| Table 2.3 | Summary of related works |
| Table 2.4 | Mapping of research gaps to project objectives |
| Table 3.1 | Functional requirements |
| Table 3.2 | Non-functional requirements |
| Table 3.3 | Tools and technologies |
| Table 3.4 onward | Extra Chapter 3 tables (see `ch3-methodology-design.md`; renumber with Word's caption tool) |
| Table 4.1 to 4.x | See `ch4-ch5-skeletons.md` |
| Table 5.1 | Achievement of objectives |
| Figure 2.1 | PRISMA-style flow of the literature search |
| Figure 2.2 | Conceptual framework of the study (the template's example list calls it Figure 2.1; see `00-source-facts.md`, section 11) |
| Figure 3.1 | Methodology diagram |
| Figure 3.2 | Request flow and system architecture (redraw proposal Figure 1) |

---

## 10. List of abbreviations

Alphabetical, as the template requires. Spell each out in full at its first use in the text. Add rows as the report grows.

| Abbreviation | Meaning |
|---|---|
| API | Application Programming Interface |
| CI | Confidence Interval |
| DSR | Design Science Research |
| ERD | Entity Relationship Diagram |
| FR | Functional Requirement |
| GPU | Graphics Processing Unit |
| H0 | Null hypothesis |
| H1 | Alternative hypothesis |
| HTTP | Hypertext Transfer Protocol |
| LLM | Large Language Model |
| MoSCoW | Must, Should, Could, Won't (requirement priorities) |
| NDPA | Nigeria Data Protection Act |
| NFR | Non-Functional Requirement |
| p95 | 95th percentile (the value that 95 percent of measurements do not exceed) |
| PRISMA | Preferred Reporting Items for Systematic Reviews and Meta-Analyses |
| RQ | Research Question |
| SMART | Specific, Measurable, Achievable, Relevant, Time-bound |
| SUS | System Usability Scale (keep only if a usability study is run) |
| TPS | Tokens Per Second |
| UML | Unified Modeling Language |

Product and benchmark names are not abbreviations and are not listed: FastAPI, Grafana, MT-Bench, Ollama, Prometheus, Redis, RouterBench, scikit-learn, sentence-transformers, vLLM. TODO: confirm the long forms of any other short name the team adds before listing it.
