# Area skill routing

Open the row for each part the change touches. Load only those skills.

| Part | Skill |
|---|---|
| Endpoint / contract | `add-endpoint` (backend plugin) |
| Schema | `add-migration` (backend plugin) |
| Scheduled or background server job, outbound notifications | `add-scheduled-job` (backend plugin) |
| File uploads and attachments (server side) | `add-file-upload` (backend plugin) + `security-privacy-review` (quality plugin) |
| Mobile screen from a design | `design-to-screen` (mobile plugin) |
| Web app screen (forms, data, auth) | `build-web-screen` (web plugin) |
| Web content page or section | `add-web-page` (web plugin) |
| Rules shared by Android and iOS | `shared-core` (mobile plugin) |
| Mobile background work, offline queue | `background-work`, `offline-queue` (mobile plugin) |
| Widget / live activity / tile | `home-widget` (mobile plugin) |
| Personal data, auth, sharing, uploads | `security-privacy-review` (quality plugin) |
| Product event | `analytics-event` (quality plugin) |
| Repeated switches over a closed set | `static-catalogs` (quality plugin) |
| Model-backed feature, retrieval, tool agent | `llm-integration`, `rag-pipeline`, `agent-workflow` (ai plugin) |
| Service SLOs, infrastructure, restore drills | `service-reliability`, `infrastructure-change`, `recovery-drill` (operations plugin) |
