# Chapter One: bibliographic audit

Audited on 1 November 2026. This audit covers the five references and their uses in sections 1.1 and 1.2 of `LLM_Router_Chapter_One_Rewritten.docx`. The original Word document was left unchanged.

## Findings and corrections

All five works were located. Relevant full-text passages support the claims for which the chapter cites them. None of those claims required withdrawal. The reference list was incomplete, and RouteLLM combined a conference year with a preprint title and identifier.

| Reference | Identity, version and correction | Claim support checked |
|---|---|---|
| Chen, Zaharia and Zou | The 2023 date correctly identifies the FrugalGPT preprint. Retained that version and added its title, preprint designation, repository and link. | Sections 3 (LLM cascade) and 4 (evaluation) support learned cascading and a cost–quality trade-off. They do not establish the performance of this proposed gateway. |
| Ding and seven coauthors | Verified the 2024 ICLR paper. Expanded the author list and added the venue, proceedings pages 41348–41366 and official source link. | Sections 3 and 4 describe learned query routing and compare cost and quality. The chapter makes no numerical savings claim. |
| Hu and seven coauthors | Verified the 2024 RouterBench preprint and identifier 2403.12031. Expanded the author list and identified the repository. No conference venue was inferred from its ICML keyword. | Sections 3–5 support repeatable routing comparisons. Section 6 explicitly limits the evaluation to performance and economic cost, leaving latency and throughput for further work. |
| Kwon and eight coauthors | Verified the 2023 SOSP paper, author order, venue, pages 611–626 and DOI 10.1145/3600006.3613165. | Sections 3 and 4, especially 4.1–4.2, support the statement that PagedAttention concerns memory management within a model-serving engine. |
| Ong and seven coauthors | The 2025 date is valid for ICLR. Used the proceedings title, “RouteLLM: Learning to Route LLMs from Preference Data,” full authors, venue, pages 34433–34448 and official link. The PDF and arXiv title use “with”; this is a recorded title difference, not a different work. | Sections 3–5 support learned routing between model classes and evaluation of cost and response quality. |

The reference heading now reads “References.” All five entries have full author lists and clickable source links. The two Chen citations now use “Chen et al., 2023,” consistent with the other citations for works with three or more authors. Each cited work has one reference entry, and each entry is cited.

## Sources and locators

- **FrugalGPT:** [2023 full text](https://arxiv.org/html/2305.05176v1), sections 3–4; [repository record](https://arxiv.org/abs/2305.05176). A later TMLR publication exists, but this audit retains the verified 2023 version already cited in the chapter.
- **Hybrid LLM:** [official ICLR record](https://proceedings.iclr.cc/paper_files/paper/2024/hash/b47d93c99fa22ac0b377578af0a1f63a-Abstract-Conference.html), linked PDF sections 3–4, and the proceedings’ BibTeX export. The [arXiv full text](https://arxiv.org/html/2404.14618v1) was also inspected.
- **RouterBench:** [full text](https://arxiv.org/html/2403.12031v2), sections 3–6, and [repository metadata](https://arxiv.org/abs/2403.12031).
- **PagedAttention:** [author-deposited full text](https://arxiv.org/html/2309.06180v1), sections 3–4; [Crossref DOI metadata](https://api.crossref.org/works/10.1145/3600006.3613165) for authors, publisher, date, venue and pages.
- **RouteLLM:** [official proceedings record](https://proceedings.iclr.cc/paper_files/paper/2025/hash/5503a7c69d48a2f86fc00b3dc09de686-Abstract-Conference.html), linked PDF sections 3–5, and the proceedings’ BibTeX export.

## Boundaries of the result

The gateway design, constraints, fallback policy and dashboard are proposed project decisions, not findings demonstrated by these papers. The need for live tests of availability and injected failures is a methodological inference; it is not presented as a result obtained by RouterBench. The chapter retains its limits on generalisation and its statement that hybrid routing itself is not claimed as novel.

ACM’s DOI destination returned an access restriction. Its identity was checked against Crossref’s registered metadata and the DOI printed in the author-deposited paper; the restriction was not treated as a broken or fabricated reference. OpenReview imposed a browser check, so accessible arXiv texts and official ICLR records/PDFs supplied the evidence used here.

This was a bibliographic and citation-support audit, not an independent reproduction of the papers’ experiments or an exhaustive search establishing the project’s novelty. No quotations, numerical performance results or additional project commitments were added to the chapter.
