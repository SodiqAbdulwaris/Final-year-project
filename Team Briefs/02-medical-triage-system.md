# Medical Triage System

**Scope:** A hospital emergency unit or urgent-care network. The system helps *trained staff* prioritize and route patients faster. It does **not** replace emergency clinicians, diagnose, or deny care — every recommendation is reviewed by a human.

**Problem we're solving:** Triage decides who needs care now vs. who can safely wait, and mis-triage can delay time-critical care or worsen crowding. There's a second, less obvious problem underneath it: once acuity is known, a facility still has to allocate scarce rooms, equipment, and appropriately-qualified staff — without sending simple cases to the most specialized (and busiest) clinician. That's an operations/capacity problem constrained by clinical safety, not just an AI-diagnosis problem.

**Existing solutions and where they fall short:**
- **ESI and similar ED protocols** — give a structured acuity framework, but don't continuously optimize local staff, rooms, or equipment.
- **WHO Interagency Integrated Triage Tool** — a solid clinical protocol (including for resource-limited settings), but it's a protocol, not a live routing engine. Any product we build must preserve its safety logic, not override it.
- **Symptom checkers / digital triage** — gather symptoms and suggest next steps, but usually don't know a facility's real capacity or staffing.
- **Queue/bed-management/scheduling tools** — help operations teams, but rarely combine clinical red flags with a transparent, clinician-approved assignment.

**How we'd make this real:**
1. Encode the hospital's *chosen* protocol's red-flag/acuity rules — deterministic safety checks before anything else runs.
2. Show staff a recommendation **with reasons** (the rule, the input, the suggested destination) — never a silent black-box decision.
3. A live capacity board (rooms, equipment, on-duty roles) so routing reflects real conditions.
4. Credential/scope rules for assignments, with explicit override for emergencies.
5. Mandatory human accept/change/override, with a reason logged.
6. Audit log + missed-escalation review + fairness monitoring across patient groups.

**First test, not a full build:** A retrospective run on one facility's de-identified cases, comparing our recommendations against what clinicians actually decided — before any live use.

**Biggest open risk:** This is the highest-risk idea of the five, for reasons outside pure engineering: it needs a hospital partner, de-identified real data, and (per FDA-style guidance) likely regulatory sign-off wherever we deploy since a bad call can harm a patient. Realistically needs an institutional partner before it's buildable as a team project — flagging this so we decide early whether we actually have that access.
