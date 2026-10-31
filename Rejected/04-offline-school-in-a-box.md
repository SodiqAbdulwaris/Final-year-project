# Offline School-in-a-Box

## Research context and kill criteria

**Working customer:** a school or community learning centre with unreliable internet but phones, tablets, or computers that can join local Wi-Fi. The box is a local content and learning server. It is not an internet replacement.

**Stop or change direction if:** teachers do not use local content in lessons after training, students' devices cannot reliably join the local network, or the school cannot maintain power, device custody, and content updates.

## 1. What problem does it solve?

Students should not need mobile data or a working internet connection every time they need a video, textbook, past question, or learning activity. A portable local server can create a Wi-Fi network and serve a curated library to nearby devices. This lowers recurring data costs and makes the same resources available to an entire class at once.

The real problem includes content management: teachers need curriculum-relevant material and a simple way to add their own content, while students need a fast, familiar experience on low-cost devices.

## 2. What existing solutions are there, and where do they fall short?

| Existing approach | What it does well | Gap worth testing |
| --- | --- | --- |
| RACHEL | A portable, battery-powered Wi-Fi hotspot with offline educational content for phones, tablets, and laptops. [RACHEL](https://worldpossible.org/products/rachel-5-500) | Already validates the core idea. A new product needs better local curriculum, simpler school operations, or a stronger service model. |
| Kolibri | Open, offline-first learning platform that can serve old devices over a local network, with content, lessons, and quizzes. [Learning Equality](https://learningequality.org/kolibri/about-kolibri/) | Powerful but its setup, content curation, and administrator workflow can be too demanding for a teacher who just wants to teach tomorrow. |
| Preloaded media drives and shared files | Very cheap and simple. | No search, learner progress, teacher workflow, access control, or repeatable content catalogue. |
| Internet-based LMS | Mature learning tools. | Depends on internet for initial and ongoing access, which is the problem being solved. |

The biggest warning is that this product category already exists. Do not build a new content server or LMS first. Test whether packaging, local curriculum, teacher onboarding, and support create a service people will choose over RACHEL or Kolibri.

## 3. What features should we offer, and how do they solve the problem?

| MVP feature | How it solves the problem |
| --- | --- |
| A small local server that broadcasts a named Wi-Fi network and opens a local learning home page | Gives any browser-capable student device access without internet or app-store downloads. |
| Curated curriculum packs, searchable by class and subject | Makes the box useful on day one instead of becoming a pile of unrelated files. |
| Teacher upload from USB, phone, or local Wi-Fi | Lets teachers add local notes, videos, and past questions without first going online. |
| Local lessons, quizzes, and basic progress records | Supports actual teaching and practice, not only content browsing. |
| Admin backup/export and a deliberate update process | Protects school-created material and makes content maintenance manageable. |
| Power plan: battery/UPS option, safe shutdown, and low-power hardware | Treats unreliable electricity as a product constraint rather than an installation surprise. |
| Clear content licences and local-language content review | Avoids distributing material the school cannot legally or pedagogically use. |

**Positioning:** "A school's local learning library and classroom server, ready even when the internet is not."

## Feasibility verdict

**Go, with a named caveat: do not rebuild the platform.** Pilot with existing Kolibri or RACHEL, then add only the workflow that users demonstrably miss. Kolibri explicitly supports local-network access without internet, while RACHEL demonstrates a commercial portable-hardware package. The risk is operational adoption, content relevance, and support, not whether local Wi-Fi content delivery works.

## Sources and research trace

Searches used: official RACHEL and Kolibri product information plus local-network deployment documentation. These sources establish mature alternatives and technical feasibility. They do not prove demand in a particular school or country.

- [RACHEL offline hotspot overview](https://worldpossible.org/products/rachel-5-500)
- [Kolibri offline-first platform](https://learningequality.org/kolibri/about-kolibri/)
- [Kolibri local-network offline synchronization discussion](https://community.learningequality.org/t/offline-sync-between-coach-and-student-is-it-possible-in-kolibri/3367)
