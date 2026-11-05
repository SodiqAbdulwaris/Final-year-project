Status: DRAFT
Depends on: Proposal_Working_Draft_v2.docx (unchanged); Proposal_Working_Draft_v2_Humanized.docx
Sources: Humanizer 12B Distilled (Gemma 4 12B) GGUF, Q4_K_M and Q8_0 via the Humanizer app 0.3.4; Template_for_Final_Year_Project_Revised.docx; Research Methodology Modules 2 and 3 slides
Open items: team read-through; add the Humanizer row to the AI declaration table in the Word file; decide whether to rewrite the 52 unchanged chunks more heavily

# Humanization report

## What was produced

`Proposal_Working_Draft_v2_Humanized.docx` is a copy of the working draft with 85 chunks rewritten across 74 paragraphs (abstract and Chapters One to Three). Every other element is byte-for-byte the same text: 598 of 667 body elements untouched, all 16 images identical, tables, captions, equations, objectives, research questions, definitions, references and the Chapter Four and Five template text left alone. The original file was not modified. `humanization-changelog.md` lists every before and after.

## Who wrote the new wording

The Humanizer model did not produce the final wording. It was run on 57 of the 137 chunks (284 samples with Q4_K_M) and screened by a checker that rejects any sample that changes a number, citation, name, section or table reference, or the future tense. 185 samples passed that facts gate, but only 47 also passed the register checks (no "you", "we", contractions, US spelling, slang or stock AI words). The samples that passed still read worse than the draft: ungrammatical fragments ("Ablations of each component."), "devs", "Nigerian guys", and meaning changes such as "recovers when a model fails" becoming "gracefully degrades when a model goes offline". The Q8_0 model (downloaded and checksum-verified, 12.7 GB) was no better on register and about ten times slower on this machine, so the app was switched back to Q4_K_M.

The final text was therefore written by Claude (Sonnet 5.5), edited from the draft with the humanizer skill's pattern list in mind, and checked with the same facts gate. This is model-assisted editing, not model-only output, and the AI declaration should say so.

## What changed

- Staccato disclaimer pairs ("X. It does not Y.") merged into one sentence.
- Run-on and stacked clauses split, and repeated sentence openings varied.
- "not X" phrasing changed to "rather than X" where it read as staging.
- Left as written: the mandated problem-statement lead-in, aim, objectives, research questions, scope exclusions and "no novelty claim" statements, the research-gap wording, and technical paragraphs that were already direct.

## What was verified

For every changed chunk a script confirmed that all numbers, years, author-year citations, proper names and acronyms, section/table/figure/chapter/objective references, and the count of "will" statements survive. Paragraph styles and the bold run-in labels (for example "What is.") are preserved. A read-through caught one real defect (the "Development model." label in 3.1 had been dropped) and it was fixed before the final build.

Not verified: that each sentence still means exactly what the draft meant. That was read by one reviewer (Claude), not independently. The team should diff the Word files or read the changelog.

## AI detector check

Same 515-word passage from section 1.1, scanned on the free GPTZero page:

| Version | GPTZero result |
|---|---|
| Original draft | 100% AI, "highly confident" |
| Edited copy | 100% AI, "highly confident" |
| Raw Humanizer-model output | not scanned: free scans ran out and GPTZero now asks for sign-up |

Scribbr's checker did not accept automated input. No result is claimed for it. The edits are meant to improve readability and remove formulaic patterns, and they did not move this detector. Detector scores on formal, citation-heavy academic prose are unreliable in both directions, and the result does not change the obligation to declare AI assistance.

## Needed in the Word file

Add a row to "Declaration on the Use of Generative AI Tools":

| Tool and version | Task | Chapter / section | How verified |
|---|---|---|---|
| Humanizer 12B (Gemma 4 12B, Q4_K_M and Q8_0) via Humanizer app 0.3.4; Claude Sonnet 5.5 | Sampling rewrites of selected paragraphs; final language editing by Claude | Abstract; Chapters 1 to 3 (85 chunks listed in humanization-changelog.md) | Scripted check of numbers, citations, names, identifiers and tense on every chunk; remaining meaning check by one reviewer; team read-through still required |
