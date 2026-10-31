# Offline School-in-a-Box

**Scope:** A school or community learning centre with unreliable internet but phones/tablets/computers that can join a local Wi-Fi network. This is a **local content and learning server** — not an internet replacement.

**Problem we're solving:** Students shouldn't need mobile data or working internet every time they need a video, textbook, past question, or activity. A portable local server can broadcast Wi-Fi and serve a curated library to every nearby device at once, cutting recurring data costs. The less obvious half of the problem is content management — teachers need curriculum-relevant material and a simple way to add their own, while students need a fast, familiar experience on low-cost devices.

**Existing solutions and where they fall short:**
- **RACHEL** — a proven, portable, battery-powered offline Wi-Fi hotspot with educational content. Already validates the core idea; a new product would need better local curriculum, simpler operations, or a stronger service model — not a reinvention.
- **Kolibri** — a powerful open, offline-first learning platform that serves old devices over local Wi-Fi with content, lessons, and quizzes. But setup, content curation, and admin workflow can be too demanding for a teacher who just wants to teach tomorrow.
- **Preloaded media drives / shared files** — cheap and simple, but no search, no progress tracking, no access control, no repeatable catalogue.
- **Internet-based LMS** — mature tools, but they depend on the internet connection this idea exists to avoid.

**Important flag:** This category already has mature, proven tools (RACHEL, Kolibri). The opportunity here is less "build a new server" and more "make deployment, local curriculum, and teacher onboarding better than what exists."

**How we'd make this real:**
1. A small local server that broadcasts a named Wi-Fi network + opens a local learning home page — no app-store downloads.
2. Curated curriculum packs, searchable by class/subject, so it's useful day one.
3. Teacher upload from USB/phone/local Wi-Fi — no need to go online first.
4. Local lessons, quizzes, and basic progress records.
5. Admin backup/export + a deliberate content-update process.
6. A real power plan (battery/UPS, safe shutdown, low-power hardware) — unreliable electricity is a design constraint, not a surprise.
7. Clear content licences + local-language content review.

**First test, not a full build:** Pilot with existing Kolibri or RACHEL in one school first, and only add the workflow that users demonstrably miss. The risk here is operational adoption and content relevance/support, not whether local Wi-Fi delivery technically works — that part is already proven.
