# Offline Classroom LAN

## Research context and kill criteria

**Working customer:** a lecturer or teacher who needs to share material, take attendance, and run a live quiz in a room with unreliable or expensive internet. This is the unnamed fifth idea. It is deliberately narrower than a school-in-a-box: it is a real-time, teacher-led local classroom tool.

**Stop or narrow the idea if:** a teacher cannot start a session and get students connected in under two minutes, the local network fails with a realistic class size, or students prefer existing messaging tools for the core material-sharing job.

## 1. What problem does it solve?

Internet-based classroom tools assume every student can connect to a remote server. In a poor-network classroom, this makes simple activities slow or impossible: distributing a PDF, checking attendance, running a quiz, collecting responses, or showing a shared resource.

The product makes the classroom itself the network. A teacher starts a local session from a phone, laptop, or school access point. Students nearby join with a short code and exchange only the material and responses needed for that class.

## 2. What existing solutions are there, and where do they fall short?

| Existing approach | What it does well | Gap worth testing |
| --- | --- | --- |
| WhatsApp, Bluetooth, AirDrop, and file-sharing apps | Familiar, quick for one file or one small group. | No shared class session, attendance, quiz control, roster, or teacher view of submissions. |
| Moodle mobile offline mode | Lets students download courses and work offline. [Moodle](https://download.moodle.org/mobile) | It is primarily a synchronized LMS. Offline quiz attempts have configuration limits and do not solve live local session setup. [Details](https://docs.moodle.org/501/en/Moodle_app_offline_features) |
| Kolibri | Supports local-network content, lessons, quizzes, and offline learner sync. [Kolibri](https://learningequality.org/kolibri/about-kolibri/) | More infrastructure and administration than a lecturer's immediate "start a quiz now" need. |
| RACHEL | Serves a large offline resource library over Wi-Fi. [RACHEL](https://rachel.worldpossible.org/about) | It is a library/server model, not focused on moment-by-moment teacher-led interaction. |

The opportunity is a simpler interaction model: **a local classroom session that starts in seconds, not an offline clone of Teams.** If that does not prove faster than a group chat plus file transfer, it should not be built.

## 3. What features should we offer, and how do they solve the problem?

| MVP feature | How it solves the problem |
| --- | --- |
| Teacher creates a local session and displays a six-character join code | Replaces account creation, web links, and mobile-data dependency at the classroom door. |
| Student join page that works in a browser on the same Wi-Fi | Avoids app-store installation and supports mixed device types. |
| Share one material pack per session | Lets students download the lecturer's files once over the local network. |
| Live attendance from join plus teacher confirmation | Makes attendance immediate, while allowing the teacher to correct proxy or late joins. |
| One live quiz format with a clear start/close control | Tests whether real-time local assessment is valuable before adding assignments, forums, or video calls. |
| Local submission receipt and teacher export | Gives students confidence that work arrived and lets the teacher retain results without cloud sync. |
| Session expiry and basic access controls | Prevents an old code or a nearby passer-by from keeping access indefinitely. |

**Positioning:** "Start a class network in minutes. Share, quiz, and collect work without the internet."

## Feasibility verdict

**Go, with a named caveat: validate the physical room first.** A thin prototype with a teacher laptop or access point, browser join page, file transfer, attendance, and one quiz is enough. Test 30 real student phones, representative file sizes, a power interruption, and the teacher's first-time setup. Do not add chat, video, AI, a course marketplace, or a full LMS until this workflow is repeatedly used.

## Sources and research trace

Searches used: official Moodle mobile/offline documentation, Kolibri, and RACHEL. These show that offline access and local-network learning are technically established; the distinct value here is the intentionally narrow, live classroom workflow.

- [Moodle app offline capability](https://download.moodle.org/mobile)
- [Moodle offline-feature limits](https://docs.moodle.org/501/en/Moodle_app_offline_features)
- [Kolibri offline-first platform](https://learningequality.org/kolibri/about-kolibri/)
- [RACHEL offline learning hotspot](https://rachel.worldpossible.org/about)
