# Medical Triage System

## Research context and kill criteria

**Working customer:** a hospital emergency unit or urgent-care network. The system helps trained staff prioritize and route patients. It does not replace emergency clinicians, make a diagnosis, or deny care.

**Stop or narrow the idea if:** retrospective testing finds unsafe under-triage against the facility's accepted standard, clinicians cannot explain or override recommendations, or the hospital cannot supply reliable current capacity and staff-availability data.

## 1. What problem does it solve?

Triage decides who must be seen now, who can safely wait, and what care setting is appropriate. Traditional triage can be subjective, and mis-triage can delay care for people with time-critical conditions or worsen crowding. [AHRQ](https://digital.ahrq.gov/program-overview/research-stories/machine-learning-improve-patient-triage-emergency-department)

The user's routing idea adds an operational problem: after acuity is identified, a facility must allocate scarce rooms, equipment, and suitably qualified staff without sending low-acuity cases to the most specialized clinician. That is a staffing and capacity decision constrained by clinical safety, not an AI diagnosis problem.

## 2. What existing solutions are there, and where do they fall short?

| Existing approach | What it does well | Gap worth testing |
| --- | --- | --- |
| ESI and similar emergency-department protocols | Give a structured acuity and expected-resource framework. | They do not continuously optimize local staff, rooms, equipment, or referral capacity. |
| WHO Interagency Integrated Triage Tool | Provides a three-colour, acuity-based protocol for emergency units, including resource-limited settings. [WHO](https://www.who.int/tools/triage) | It is a clinical protocol, not a live operational routing engine. Any product must preserve its safety logic rather than overwrite it. |
| Symptom checkers and digital triage | Gather symptoms and suggest next steps. | They usually lack verified local capacity, staffing privileges, and responsibility for a patient's arrival-to-care workflow. |
| Queue, bed-management, and staff-scheduling tools | Help operations teams use capacity. | They often do not combine clinical red flags, a transparent acuity reason, and clinician-approved assignment rules. |

AI decision support shows promise, but the evidence base still has large implementation gaps. A recent systematic review found external validation in only 32% and prospective validation in only 8% of included AI-CDS studies. [Systematic review](https://pmc.ncbi.nlm.nih.gov/articles/PMC13012507/)

## 3. What features should we offer, and how do they solve the problem?

| MVP feature | How it solves the problem |
| --- | --- |
| Approved red-flag and acuity rules based on the hospital's chosen protocol | Flags immediate dangers deterministically before any optimization runs. |
| Clinician-facing recommendation with reasons, not a patient-facing diagnosis | Shows the acuity rule, relevant input, and suggested destination so staff can independently assess it. |
| Live capacity board for available rooms, equipment, and on-duty roles | Makes routing reflect real operating conditions rather than a generic directory. |
| Credential and scope rules for assignments | Prevents a specialist from being used for routine work when an appropriate clinician is available, while allowing explicit override for emergencies. |
| Mandatory human accept, change, or override with a reason | Preserves accountability and produces data for safety review. |
| Audit log, missed-escalation review, and fairness monitoring | Supports incident review and checks whether recommendations perform unevenly across patient groups. |
| Referral/transfer checklist output | Keeps routing connected to safe handoff. WHO's toolkit includes triage and transfer tools for this reason. [WHO toolkit](https://www.who.int/teams/integrated-health-services/clinical-services-and-systems/emergency-and-critical-care/emergency-care-toolkit) |

**Positioning:** "A transparent triage-and-capacity copilot for the charge nurse and emergency team." Never claim it replaces triage.

## Feasibility verdict

**Go only with a named caveat: supervised clinical decision support.** Start with one facility, one protocol, and retrospective de-identified cases. Compare recommendations with clinicians' decisions before any live use. FDA guidance distinguishes decision support from functions that give specific directives for time-critical decisions, so obtain jurisdiction-specific regulatory advice before deployment. [FDA guidance](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/clinical-decision-support-software)

## Sources and research trace

Searches used: WHO triage standards; AHRQ emergency-department triage research; systematic reviews of AI clinical decision support; FDA clinical-decision-support guidance. WHO and FDA are primary policy sources. The systematic review describes research quality, not proof that this product is safe.

- [WHO Interagency Integrated Triage Tool](https://www.who.int/tools/triage)
- [AHRQ triage decision-support research](https://digital.ahrq.gov/program-overview/research-stories/machine-learning-improve-patient-triage-emergency-department)
- [AI-CDS systematic review](https://pmc.ncbi.nlm.nih.gov/articles/PMC13012507/)
- [FDA Clinical Decision Support Software guidance](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/clinical-decision-support-software)
