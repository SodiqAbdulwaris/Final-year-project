Status: DRAFT
Depends on: D01–D12; _meta/decisions-applied.md
Sources: _meta/hybrid-design.md; _meta/source-facts.md
Open items: See _meta/placeholders.md

# AI Request Router proposal drafts

This folder will assemble the B.Sc. Software Engineering proposal for Nile University of Nigeria. The governing design is [_meta/hybrid-design.md](_meta/hybrid-design.md); applied decisions and verification limits are in [_meta/decisions-applied.md](_meta/decisions-applied.md). The router itself is not implemented by this documentation task.

## Paste order

1. [Front matter](00-front-matter/00-overview.md), in its listed order.
2. [Chapter 1](01-introduction/00-overview.md), sections 1.1–1.11.
3. [Chapter 2](02-literature-review/00-overview.md), including the seven related-work themes.
4. [Chapter 3](03-methodology-design/00-overview.md), including all seven design subsections.
5. [Chapter 4 skeleton](04-implementation-results/00-overview.md).
6. [Chapter 5](05-conclusion/5.1-summary.md), then 5.2.
7. [References](06-references.md), then [Appendices](07-appendices/00-overview.md).

Read the [style guide](_meta/style-guide.md) before Word assembly. Remove header blocks and Notes for the team from submission text. Apply Word heading/caption styles and regenerate contents, lists and page numbers. Figures are the PNG files listed in the Appendix G register; regenerate or replace them there, not from Mermaid.

| Status | Meaning |
|---|---|
| DRAFT | Drafted, awaiting team reading and approval |
| TODO | Missing information or work |
| NEEDS-DECISION | A specific unresolved choice affects the text |
| VERIFIED | Only the stated item and scope were checked |

The old drafts were moved with git mv to [_meta/history/](_meta/history/); they are historical sources, not paste-ready alternatives. Their older objectives, synthetic figures and targets will not govern the new proposal. The source-facts record will preserve what the original proposal said, rather than being rewritten to pretend that its design was always the hybrid.

## Verification route

Use limitations/L07-fact-check-sample.md for sampled source checks and limitations/L03-unconfirmed-citations.md for metadata coverage. Abstract-level verification will support only the claims checked at that level. Unsampled detailed numerical claims will not be copied into Chapter 2. See [_meta/placeholders.md](_meta/placeholders.md) for remaining work. Dataset redistribution is not cleared by public availability or a code licence alone.

## Documentation check scope

On 4 November 2026 the Markdown drafts were brought into line with the Word working draft (`proposal frags/Proposal_Working_Draft_v2.docx`), which is now the leading text. The package has the abstract (296 words, five alphabetical keywords), Chapters 1 to 3 in the Module 3 proposal structure (Chapter 3 has Sections 3.1 to 3.15), 33 reviewed studies in Table 2.3, a 45-entry reference list, and Figure 2.1 and Figures 3.1 to 3.11 as Codex-generated PNGs. Chapters 4 and 5 are still skeletons. The earlier Mermaid sources are archived in `03-methodology-design/outputs/chapter-3/mermaid-sources.md`. Final Word layout, page counts and departmental wording have not been verified.
