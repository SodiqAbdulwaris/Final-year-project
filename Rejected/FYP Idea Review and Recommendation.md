# FYP Candidate Ideas: Critique and Recommendation

Reviewed: `README.md` + the five briefs (`01-medical-transcriber`, `02-medical-triage-system`, `03-ai-powered-study-system`, `04-offline-school-in-a-box`, `05-offline-classroom-lan`).

## Bottom line

The five briefs are unusually rigorous for a pre-proposal stage — real citations, explicit kill criteria, honest "here's who already does this" competitive scans. That's the right instinct and worth keeping. But they're written as **startup validation briefs**, not **final-year-project proposals**, and that mismatch is the main thing to fix before you take any of these to a supervisor. A validation brief asks "will a customer pay for this / adopt this." A FYP committee asks "is there a defined technical contribution, can one student build and evaluate it in the time available, and can you actually get the data/users you need." Those are different questions, and two of the five ideas fail the second test badly regardless of how sound the first-test reasoning is.

**Recommendation: build on #05 (Offline Classroom LAN), narrow #03 (AI-Powered Study System) as a fallback, and drop the two medical ideas as FYP candidates.** Details and a possible way to combine 05 and 03 are below.

## Per-idea assessment

### 05 — Offline Classroom LAN (ranked #1 in your README)

**This is the strongest FYP candidate, and for a different reason than the brief gives.** The brief ranks it #1 because it's cheap to pilot. For a FYP, its real advantage is that it's the only idea where you control every dependency: your test users are fellow students (easy to recruit 30 phones on your own campus), there's no clinical or institutional gatekeeper, and the technical surface is exactly the kind of thing a software engineering examiner wants to see — network programming, real-time sync, a captive-portal-style local web server, offline-first data handling, and a live demo that works in the room.

Gaps to close before you commit:
- **The brief doesn't say who hosts the network.** "A teacher starts a local session from a phone, laptop, or school access point" glosses over a genuinely hard engineering decision. A laptop-hosted Wi-Fi hotspot (Windows Mobile Hotspot / Linux hostapd) behaves very differently from "use the existing classroom router" — different setup complexity, different reliability, different demo risk. Pick one and design around it; don't leave it open, because it changes your architecture.
- **Captive-portal / DNS behavior on real student phones is the actual technical risk**, not the quiz logic. iOS and Android both do aggressive captive-portal detection and will sometimes silently refuse to load a local page without internet. This is worth a spike (a few hours testing on real phones) before you commit the whole FYP to this approach — it's exactly the kind of "unsafe under-triage" style kill criterion the brief uses for the medical ideas, but it's missing here.
- **Your own stack maps onto this cleanly**: Express/Socket.io (or Fastify) for the local server and live quiz state, SQLite or local Postgres for session data, Docker only for your own dev/build convenience (the deployed artifact has to run on a bare laptop with no internet, so containerizing the *runtime* target may be the wrong call — worth deciding early rather than defaulting to Docker because it's familiar).
- **Novelty for a committee**: "local classroom session tool" alone may read as thin next to Moodle/Kolibri/RACHEL, which the brief itself lists. The defensible technical contribution is the "starts in under two minutes, no accounts, works on any browser on someone else's Wi-Fi" constraint — make that constraint the spine of your write-up (a measurable requirement: session bootstrap time, join success rate on N heterogeneous devices), not a side note.

### 03 — AI-Powered Study System (ranked #2)

Good fallback, and it's honest about the hard part: NotebookLM and Quizlet already do the obvious version. The brief's proposed wedge — a course-space with provenance/remix/attribution — is a real product idea but it's a *community/marketplace* problem, which is a much bigger build than a solo FYP timeline usually allows (auth, sharing permissions, moderation/reporting, practice-history analytics, on top of the AI generation itself).

If you pursue this, narrow hard: drop the community/sharing/remix layer entirely for the FYP submission and make the technical contribution the **grounding and citation mechanism** — i.e., can you build a RAG pipeline that reliably generates flashcards/quizzes from a student's own uploaded notes *with correct source attribution per generated item*, and can you evaluate that (precision of the source link, hallucination rate) rather than just demo it. That's a concrete, measurable, examiner-friendly contribution. The sharing/course-community angle can live in your "future work" section, which is normal and expected in a FYP write-up.

Practical upside: FastAPI + your Node stack for the app shell, any embedding model + vector store for retrieval — all within tooling you already use.

### 04 — Offline School-in-a-Box (ranked #3)

Read your own brief's verdict carefully: **"Go, with a named caveat: do not rebuild the platform... Pilot with existing Kolibri or RACHEL."** That is a good, honest product verdict — and it's also close to a disqualifying verdict for a FYP. If the correct move is "don't build a new one, deploy the existing open-source one and see if operations/adoption is the real gap," there may be no first-party system left for you to design, build, and defend as *your* technical work. A committee will ask what you actually engineered versus configured.

If you want to keep this idea alive, the FYP-shaped version is narrower than "school in a box": pick one specific unsolved technical piece — e.g., a low-bandwidth content-sync protocol for updating a Kolibri-like box from an intermittent connection, or a curriculum-tagging/search improvement for low-resource local content — and build *that*, using Kolibri as the environment you plug into rather than the thing you replace. As written, this idea is weaker for a FYP than for a real product.

### 01 — Medical Transcriber (ranked #4) and 02 — Medical Triage System (ranked #5)

Both briefs are well-researched, and both correctly conclude these need real clinical validation before they're viable products ("ten clinicians review drafts," "retrospective clinician-reviewed validation," FDA clinical-decision-support guidance). That's exactly right for a startup — and it's exactly why these are poor **FYP** choices for a solo undergraduate on a fixed academic timeline, independent of how interesting the technical problem is:

- **Access**: you need consenting patients or clinicians, or de-identified clinical records, or a hospital's real capacity data. Getting any of that as a student without an existing institutional partnership is a multi-month problem on its own, before you write a line of code. Neither brief has a realistic plan for how *you specifically* get that access.
- **Regulatory exposure is worse than the brief accounts for, because you're in Nigeria, not the US.** Both briefs cite HIPAA and FDA guidance, which don't govern you. The relevant law is the **Nigeria Data Protection Act 2023 (NDPA)** — under it, an entity processing health data at any real scale is likely a "Data Controller of Major Importance," which brings mandatory NDPC registration, a data protection officer, breach reporting within 72 hours, and penalties from ₦2–10M+ or 2% of revenue for violations. ([Mondaq: NDPA and health care delivery](https://www.mondaq.com/nigeria/data-protection/1434994/nigeria-data-protection-act-2023-relevant-provisions-for-health-care-delivery-in-nigeria)) That's not a reason the *idea* is bad — it's a reason it's a bad fit for something you have to fully build, test with real data, and defend in a few months without institutional legal backing.
- **Safety-critical framing raises the stakes of a demo going wrong** in front of an examiner in a way the offline/study ideas don't.

My honest read: these two are good material for a **literature review / problem-analysis chapter**, or for a future project once you have a clinical partner (your SIWES network at Freeman, or a hospital contact, could eventually be that), but not for this FYP. I'd shelve rather than force them.

## What's missing across all five documents

1. **No academic framing.** Every brief is customer/MVP/feasibility-verdict shaped. Your department will want something closer to: problem statement, related work (peer-reviewed, not product pages — several citations here are marketing pages, which is fine for product validation but won't satisfy a literature review), objectives, methodology/SDLC approach, system design, evaluation plan, and expected contribution. Whichever idea you pick, budget time to re-derive this structure — it's a different document, not a reformat.
2. **No stated timeline or solo-vs-team assumption.** Every "pilot with 20 students" / "ten clinicians" plan implicitly assumes time and access you haven't confirmed you have. Pin down your actual FYP calendar (proposal deadline, how many semesters, solo build) before finalizing scope — it changes which of these is realistic.
3. **No explicit novelty statement.** Nigerian university FYP guidance consistently flags two things reviewers check early: a genuinely new angle (not a repackaged known tool) and confirmed access to the data/respondents you're planning to use. ([MonoEd: choosing a FYP topic in Nigeria](https://monoed.africa/blog/how-to-choose-final-year-project-topic-nigeria)) Idea #04 currently fails the first check as written; the two medical ideas are weak on the second.
4. **Regulatory framing is US-centric** (HIPAA, FDA) in a project set that should probably reason from NDPA if health data is ever revisited.

## A possible way to combine your top two

If you want one idea with both a clean core (for a working, demoable FYP) and a novelty story (for the write-up), consider: **Offline Classroom LAN as the backbone, with an optional "smart" mode** — when the host device *does* have internet, the teacher can generate a quiz from uploaded material via the RAG approach from #03; when offline, the system falls back to teacher-authored quizzes only. This gives you a single deployable system, a genuine technical contribution (graceful hybrid online/offline operation for AI-assisted teaching in low-connectivity settings — a real, citable gap given everything in your own #04/#05 research about connectivity), and it doesn't require the community/sharing complexity that makes #03 too big alone.

## Suggested next step

Before writing a formal proposal: take your actual department's FYP guidelines/rubric (ask your supervisor or the SE handbook) and check it against whichever idea you shortlist — the criteria above are general patterns from public guidance, not Nile University's specific rubric, and that rubric should be the tie-breaker.

## Sources

- [Nigeria Data Protection Act 2023: Relevant Provisions for Health Care Delivery in Nigeria (Mondaq)](https://www.mondaq.com/nigeria/data-protection/1434994/nigeria-data-protection-act-2023-relevant-provisions-for-health-care-delivery-in-nigeria)
- [How to Choose a Final Year Project Topic in Nigeria (MonoEd Africa)](https://monoed.africa/blog/how-to-choose-final-year-project-topic-nigeria)
