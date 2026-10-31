Status: DRAFT
Depends on: Superseded earlier design
Sources: Original draft preserved by git mv
Open items: Archived historical text; excluded from assembly and active placeholder register

# Manuscript outline (optional, low priority)

Re-cuts the project as a journal article using `Scopus_Journal_Manuscript_Template.docx`. **Nothing here is written as a result.** Do not start this until Chapter 4 has real numbers. Journal choice is TODO and must follow the template's checklist (confirm Scopus indexing in the Scopus Sources list, not the journal's own claim; follow the journal's own template and reference style if it has one).

Template length guide: 6,000 to 9,000 words including references; 30 to 60 references; 6 to 10 figures and tables. Default layout A4, Times New Roman 12 pt, double spacing, line numbers.

| Manuscript section | Word guide (template) | Source in the project drafts | Status |
|---|---|---|---|
| Title and short running title | 10 to 20 words; up to 50 characters | `front-matter.md` options A to C; running title "Load-aware LLM request routing" (30 characters) | Pick with supervisor |
| Authors, affiliations, corresponding author, ORCID iDs | n/a | TODO (names, IDs, supervisor undecided). Authorship needs substantial contribution, drafting or revising, approval and accountability | TODO |
| Abstract (structured: Background, Objective, Methods, Results, Conclusion) | 200 to 250 | Write last; Results need actual numbers | Blocked on Chapter 4 |
| Highlights (3 to 5 bullets, each at most 85 characters) | n/a | From contributions in `ch1` 1.9 and the results | Blocked on Chapter 4 |
| 1. Introduction | 800 to 1,200 | `ch1` 1.1, 1.2, 1.3, 1.9, 1.10 as funnel: context, problem, gap, aim and RQ1 to RQ6 (or a reduced set), contributions, organisation | Reusable now |
| 2. Related Work (2.1 and 2.2 themes, 2.3 summary and gap with Table 1 comparing studies with the present work) | 1,000 to 1,500 | `ch2` 2.4 themes (merge the eight into two or three), 2.5 table, 2.7 gaps | Needs verified papers |
| 3. Materials and Methods: 3.1 Research design; 3.2 Data; 3.3 Proposed approach (equation 1 = scoring function, pseudocode, architecture figure); 3.4 Experimental setup and baselines; 3.5 Metrics and statistics; 3.6 Ethics | 1,500 to 2,500 | `ch3` 3.1, 3.7, 3.6.5, 3.6.1, 3.9, 3.10 | Reusable now; setup versions TODO |
| 4. Results (in the order of the research questions) | 1,000 to 2,000 | `ch4` 4.6.1 to 4.6.5 tables and figures | Blocked on Chapter 4 |
| 5. Discussion: interpretation, comparison with previous studies, implications, limitations and threats to validity | 1,000 to 1,500 | `ch4` 4.7, 4.8 | Blocked on Chapter 4 |
| 6. Conclusion | 300 to 500 | `ch5` 5.4 to 5.7, no new results or citations | Blocked on Chapter 4 |
| Declarations: CRediT author contributions; funding; competing interests; data availability; ethics; generative AI use | n/a | CRediT roles TODO. Data availability: replication package link TODO. Ethics: "not applicable, no human participants" if still true. Generative AI statement from `front-matter.md` section 6, reworded to the journal's form | TODO |
| Acknowledgements (remove for double-blind review) | n/a | `front-matter.md` section 7 | TODO |
| References in the journal's style (IEEE numbered in the template examples) | n/a | Re-format from `literature-review/references.md` | Blocked on references |
| Appendix A. Supplementary material; cover letter; pre-submission checklist | n/a | Replication package; template letter | Later |

## Equation to carry over

The template shows a scoring-style equation as an example. Equation (1) for this paper is the score in `ch3` Section 3.6.5:

S_i(x) = w_q · q̂_i(x) − w_c · ĉ_i(x) / c_ref − w_l · l̂_i(x) / L_ref

Define every symbol on first use (template rule). Weights and prices are TODO until the evaluation fixes them.

## Differences from the report to remember

- Journal papers are about the contribution and the finding, so merge the report's eight review themes into two or three, and drop the requirements tables, use cases and class diagrams.
- Double-blind review: remove names, affiliations, acknowledgements, self-identifying citations and repository links from the main file, and submit a separate title page.
- Similarity check: aim under 15 percent excluding references (template checklist). Rewrite report text rather than paste it.
