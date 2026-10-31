# AI-Powered Study System

**Scope:** Secondary and tertiary students who already have course notes and want study material plus a trustworthy way to share it with classmates. Start with **one course or department** — not a public network for every subject.

**Problem we're solving:** Students have notes but not always the time or prompting skill to turn them into active practice material. What they share, they share in fragmented channels (chats, random files, links) with no quality signal or course context — so the advantage goes to students who already know how to use AI well, not to students with the best material. The real job isn't "generate flashcards" (everyone does that) — it's turning a student's own sources into *traceable* study material that a course community can reuse and improve together.

**Existing solutions and where they fall short:**
- **NotebookLM** — strong source-grounded flashcards/quizzes/explanations, but not built as a course community with reusable, quality-ranked shared packs.
- **Quizlet** — great at distributing study sets, but we'd need to prove better source provenance or course-space collaboration to matter.
- **Anki** — excellent spaced repetition, but creating and sharing cards takes real effort, and source context gets lost.
- **Group chats / cloud drives** — easy, but zero structure, no link between a note and the questions generated from it.

This is a crowded space — "NotebookLM for students" isn't a real differentiator. The actual bet is: **a course community where every generated item stays linked to its source and can be remixed, reviewed, and attributed.**

**How we'd make this real:**
1. Import notes/PDFs/slides/pasted text into a private course space.
2. One generator covering notes, overview, flashcards, and quizzes (not five separate tools).
3. Source link on every generated card/answer, so students can check and correct it.
4. Course-code or username-based sharing with explicit permissions — not public by default.
5. Copy/remix with attribution, so strong AI users can help others without erasing the original source/contributor.
6. Report/rate/review on shared packs, to catch bad or copied material.
7. Basic practice history + weak-topic view, so it's a study loop, not a download-and-forget library.

**First test, not a full build:** A thin prototype in one course — import notes, generate one study pack, share by code — and see whether classmates actually practice and remix it, not just download it once.

**Biggest open risk:** Market is sophisticated and crowded, and this is realistically the widest-scope idea of the five if we try to build the full sharing/community layer. Worth deciding up front whether we're building the whole thing or just the generation-with-citations core first.
