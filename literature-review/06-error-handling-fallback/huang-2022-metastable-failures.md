Status: DRAFT
Depends on: D08; D12
Sources: Primary URLs in source table and proposal-audit section
Open items: Scoped numerical/final-version checks recorded below

# Metastable failures in the wild (Huang et al., 2022)

| Field | Value |
|---|---|
| Topic (home) | 06 Error handling and fallback |
| Also relevant to | 03 Load balancing |
| Paper type | empirical study (with a model and reproductions) |
| Venue and status | peer-reviewed (OSDI 2022, pp. 73–90) |
| Source read | full text (https://www.usenix.org/system/files/osdi22-huang-lexiang.pdf) |
| Verified on | 2026-10-31, against the USENIX OSDI '22 presentation page |
| Relevance to project | High (for retry and failover design, not for LLM specifics) |

## APA 7 reference
Huang, L., Magnusson, M., Muralikrishna, A. B., Estyak, S., Isaacs, R., Aghayev, A., Zhu, T., & Charapko, A. (2022). Metastable failures in the wild. In *Proceedings of the 16th USENIX Symposium on Operating Systems Design and Implementation* (pp. 73–90). USENIX Association. https://www.usenix.org/conference/osdi22/presentation/huang-lexiang

*The USENIX page lists no DOI.*

## In-text citation forms
(Huang et al., 2022) · Huang et al. (2022)

## 1. What it is about
A study of "metastable failures": outages in which a temporary trigger pushes a system into overload and a *sustaining effect* (most often retries) then keeps it down even after the trigger is gone. The authors read hundreds of public incident reports, extend an earlier model, and reproduce several failures in test applications.

## 2. The problem
Reliability work had focused on fail-stop and Byzantine faults. Metastable failures look like many differently named incidents (retry storms, death spirals, cascading overload), so practitioners did not see them as one class, and the prior framework (Bronson et al.) rested on simplified Facebook examples with no data on how often they occur.

## 3. Proposed solution
- **Incident survey:** 21 publicly reported incidents (four each from AWS, Google Cloud and Azure, plus IBM, Spotify, Cassandra, Elasticsearch and others) coded by duration, impact, trigger, sustaining effect and mitigation; with one insider case study from Twitter (garbage collection as amplifier) this gives the 22 failures in the abstract.
- **Extended model:** capacity and load measured in abstract resource units. Two trigger types (a load spike, or a capacity decrease such as a bad deploy) and two amplification types (work amplification such as retries, and capacity degradation such as garbage collection). A system is *vulnerable* when it runs at high load that it handles only while nothing goes wrong; whether a trigger tips it over depends on trigger size, duration and how vulnerable it is.
- **Reproductions:** three open-source example applications that reproduce different metastable failures (https://github.com/lexiangh/Metastability).

**How cost is modelled.** Not as money. The paper makes a performance argument: operators run in the vulnerable state because it is cheaper (a database that takes 300 requests per second plus a 90%-hit cache serves 3,000), and a cache failure then overloads the database.

## 4. Data, models and tools
Public post-mortems from cloud providers and smaller services, found by sifting hundreds of reports; incidents are judged metastable on the presence of a sustaining effect; ambiguous cases are highlighted as only plausible.

## 5. Key results
- Metastable failures are widespread: at least 4 of 15 major AWS outages in the previous decade.
- Triggers: about 45% engineer errors (bad configuration or code, latent bugs); about 35% load spikes; 45% of incidents had more than one trigger.
- **Retry policy was the most common sustaining effect, in more than 50% of incidents** (the text names 11 of the 21 tabulated; the table marks one more).
- Mitigation usually meant cutting load: load shedding in over 55% of cases. Durations ranged from 1.5 to 73.53 hours, with 4 to 10 hours the most common band (35%).

## 6. Limitations
*Stated by the authors:* few public incidents with enough detail, so the number may understate prevalence, and they used judgement where reports were incomplete; failures are emergent and hard to predict.

*My observations:* it is a cloud-infrastructure study from 2013 to 2021 incidents with no LLM services and no quantitative threshold for when retries become harmful. It describes causes and mitigations qualitatively and offers no ready-made algorithm.

## 7. Relevance to the AI Request Router
- Strong, peer-reviewed justification for **bounded retries, retry budgets, backoff with jitter, load shedding and circuit breakers**: unbounded retries are the dominant way a transient fault becomes an outage. It matches the retry storm that ContinuityBench and FailureAtlas rediscovered when a fallback provider is rate-limited.
- A router that fails over *to* a nearly saturated backend can create the overload it is escaping; the vulnerable/stable framing supports checking the **target's headroom** (the live-load signal) before rerouting.
- **Reuse:** the trigger / sustaining-effect vocabulary for the failure analysis; load shedding as a last resort. **Not covered:** LLM-specific failure, quality-aware fallback.

## 8. How to use it in the report
Section 2.5 (resilience patterns) and the rationale for circuit breaker and retry limits in Chapter 3. "Huang et al. (2022) found retries sustaining over half of 21 reported cloud outages, so failover logic that retries without limits can prolong the failure it was meant to absorb."

## 9. Row for Table 2.3
| Author(s) and year | Aim / problem | Method / technique | Dataset / tools | Key findings | Limitations / gap |
|---|---|---|---|---|---|
| Huang et al. (2022) | How common and what sustains metastable failures | Incident survey; extended load-capacity model; reproductions | 21 public incident reports plus a Twitter case; 3 example apps | Retries sustain over half of incidents; at least 4 of 15 major AWS outages | Few incidents; no LLM context; qualitative |


## 2026-10-31 proposal audit

- Source attempted: https://www.usenix.org/system/files/osdi22-huang-lexiang.pdf.
- Scope: Source retrieval did not yield a usable abstract/metadata parse; no fresh detailed claim verification. Historical claims remain unverified.
- Historical Source read above records the earlier session, not a claim of a fresh full reading.

- Additional current check: USENIX publisher page https://www.usenix.org/conference/osdi22/presentation/huang-lexiang confirmed authors, venue, pages and abstract-level incident-analysis method; PDF fetch was blocked. No detailed numerical results reused.
