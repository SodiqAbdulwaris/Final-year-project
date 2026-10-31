# Offline Classroom LAN

**Scope:** A lecturer or teacher who needs to share material, take attendance, and run a live quiz in a room with unreliable or expensive internet. This is deliberately **narrower** than School-in-a-Box: a real-time, teacher-led local classroom tool, not a content library.

**Problem we're solving:** Internet-based classroom tools assume every student can reach a remote server — which makes even simple activities (share a PDF, take attendance, run a quiz, collect responses) slow or impossible in a poor-network room. The idea makes the classroom itself the network: a teacher starts a local session from a phone/laptop/access point, and nearby students join with a short code to exchange only what that class needs.

**Existing solutions and where they fall short:**
- **WhatsApp / Bluetooth / AirDrop / file-sharing apps** — familiar and quick for one file or a small group, but no shared class session, attendance, quiz control, or teacher view of submissions.
- **Moodle mobile offline mode** — lets students download and work offline, but it's a synced LMS with configuration limits on offline quizzes — it doesn't solve "start a live local session right now."
- **Kolibri** — supports local-network content/lessons/quizzes, but is more infrastructure and admin than a lecturer needs for "start a quiz now."
- **RACHEL** — a strong offline library/server, but built for content delivery, not moment-by-moment teacher-led interaction.

**The bet:** a local classroom session that starts in seconds — not an offline clone of Teams or Moodle. If it isn't faster than a group chat + file transfer, it isn't worth building.

**How we'd make this real:**
1. Teacher creates a local session and gets a six-character join code.
2. Students join via a browser page on the same Wi-Fi — no app install, works across device types.
3. One material pack shared per session — students download it once, locally.
4. Live attendance from join + teacher confirmation (to catch proxy/late joins).
5. One live quiz format with a clear start/close control.
6. Local submission receipt + teacher export — no cloud sync needed.
7. Session expiry + basic access control, so an old code can't be reused by a passer-by.

**First test, not a full build:** A thin prototype (teacher laptop or access point, browser join page, file transfer, attendance, one quiz), tested with ~30 real student phones, realistic file sizes, a power interruption, and a first-time setup by someone who hasn't seen it before. Don't add chat, video, AI, or a full LMS until this core workflow is proven and repeatedly used.

**Biggest open risk (not in the original research):** how the local network actually gets hosted (a laptop hotspot vs. an existing router behave very differently), and how phones handle "captive portal" detection when there's no real internet — worth a quick hands-on test before committing the architecture.
