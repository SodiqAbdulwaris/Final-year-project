# Medical Transcriber

**Scope:** Outpatient clinics and hospitals whose clinicians document patient encounters. The tool drafts clinical notes from a consensually recorded clinician–patient conversation. It does **not** diagnose, prescribe, or file notes into the record on its own — the clinician always reviews and signs off.

**Problem we're solving:** Clinical documentation eats into patient-facing time and spills into after-hours "pajama time" (one study found ~2.5 hrs/week saved by ambient documentation tools). The hard part isn't speech-to-text — it's turning a conversation into a structured, specialty-appropriate note that a clinician can trust and check quickly before it becomes part of the official record.

**Existing solutions and where they fall short:**
- **Human scribes/transcribers** — understand local workflow, but expensive, limited availability, not immediate.
- **Ambient AI (Abridge, Nuance DAX)** — enterprise-grade, already crowded. A new entrant only wins by fitting a specific specialty, language, EHR, or low-connectivity workflow better — not by just saying "AI notes."
- **Generic dictation/transcription** — fast capture, but leaves the clinician to turn raw text into a defensible note.
- **EHR templates** — familiar, but still require active typing during/after the visit.

**How we'd make this real:**
1. Explicit patient consent + a visible "recording" state.
2. Capture audio (or dictation) → generate a **specialty-specific** draft note, starting with one specialty and one note format.
3. Speaker labels + time-linked evidence per section, so the clinician can verify claims fast instead of trusting a black box.
4. Mandatory clinician review/edit/sign-off — the draft is never the final chart by itself.
5. Structured export into the clinic's existing workflow (copy/export first, EHR integration later).
6. Encryption, role-based access, retention controls, audit history.

**First test, not a full build:** Have ~10 clinicians in one specialty review drafts from already-consented recordings. Measure editing time, error types, and whether it beats their current workflow. Don't build EHR integration, billing automation, or multi-specialty support until that passes.

**Biggest open risk:** Access and compliance. We'd need a clinic partner willing to share real (consented) recordings, and — since we're building in Nigeria, not the US — this is governed by the Nigeria Data Protection Act 2023, not HIPAA. Health-data processing at scale likely makes us a "Data Controller of Major Importance," with registration, a data protection officer, and breach-reporting obligations. Worth confirming we have a real clinic partner before investing heavily here.
