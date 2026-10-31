# AI-Powered Study System

## Research context and kill criteria

**Working customer:** secondary and tertiary students who already have course notes and need study material plus a trusted way to share it with classmates. Start with one course or department, not a public network for every subject.

**Stop or narrow the idea if:** students use it only once to generate content, shared packs are mostly low quality or copied material, or students will not invite classmates into a course space.

## 1. What problem does it solve?

Students often have notes but lack the time or prompting skill to turn them into active practice. They also share materials in fragmented channels such as messaging apps, files, and links, with little provenance, quality signal, or course context. The resulting advantage goes to students who know how to use AI well, rather than to students who have the best learning materials.

The core job is not "generate flashcards." Existing tools do that. The job is to turn a student's sources into traceable study material and let a course community reuse, improve, and practise it in one place.

## 2. What existing solutions are there, and where do they fall short?

| Existing approach | What it does well | Gap worth testing |
| --- | --- | --- |
| NotebookLM | Generates flashcards and quizzes from documents, offers explanations, and grounds answers in the supplied sources. [Google](https://blog.google/innovation-and-ai/models-and-research/google-labs/notebooklm-student-features/) | Strong source-grounded study aid, but it is not inherently a course community with reusable, quality-ranked student packs and shared practice history. |
| Quizlet | Turns notes, slides, and readings into practice tests, study guides, and flashcards that teachers can share. [Quizlet](https://quizlet.com/features/ai-study-tools) | Great study-set distribution, but the proposed wedge must prove better source provenance, course-space collaboration, or local curriculum fit. |
| Anki and manual flashcards | Excellent deliberate practice and spaced repetition. | Creation and sharing take effort, and source context is often lost. |
| Group chats and cloud drives | Familiar and easy to access. | No structured learning workflow, quality checks, or connection between a note and the questions generated from it. |

This is a crowded market. "NotebookLM for students" is not a sufficient difference because NotebookLM already targets student study workflows. The defensible hypothesis is a **course community where every generated item remains linked to the source and can be remixed, reviewed, and attributed**.

## 3. What features should we offer, and how do they solve the problem?

| MVP feature | How it solves the problem |
| --- | --- |
| Import notes, PDFs, slides, and pasted text into a private course space | Gives AI a clear source boundary and keeps material organized by subject. |
| One generator for concise notes, overview, flashcards, and quizzes | Covers the requested study outputs without making each one a separate product. |
| Source links on each generated answer or card | Lets a student check where an answer came from and correct weak source material. |
| Course code or username-based sharing with explicit permissions | Allows classmate-to-classmate sharing inside the app without making personal notes public by default. |
| Copy, remix, and attribution for shared packs | Lets better AI users help others while preserving the original contributor and source context. |
| Report, rate, and teacher or peer review for shared packs | Reduces the spread of incorrect questions, misleading summaries, and copyrighted uploads. |
| Basic practice history and weak-topic view | Turns generated material into a study loop rather than a download-and-forget library. |

**Positioning:** "Turn your course sources into study packs your class can verify, improve, and practise together."

## Feasibility verdict

**Not yet. Needs validation.** The technical path is straightforward, but the market is sophisticated and crowded. Run a no-code or thin prototype with one course: import notes, generate one study pack, share by code, and track whether classmates actually practise and remix it. Treat student privacy, age-appropriate design, and academic integrity as product requirements. UNESCO calls for privacy protection and age-appropriate, human-centred use of generative AI in education. [UNESCO](https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research?hub=387)

## Sources and research trace

Searches used: official NotebookLM and Quizlet study features; UNESCO guidance on generative AI in education. Official product pages establish current feature overlap. The differentiation in this brief is a testable product hypothesis, not a claim that competitors lack every sharing feature.

- [Google NotebookLM student features](https://blog.google/innovation-and-ai/models-and-research/google-labs/notebooklm-student-features/)
- [Quizlet AI study tools](https://quizlet.com/features/ai-study-tools)
- [UNESCO guidance for generative AI in education](https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research?hub=387)
