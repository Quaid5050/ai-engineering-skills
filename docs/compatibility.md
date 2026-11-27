# Coverage and evidence tiers

All catalogue entries conservatively remain **documented**. Targeted executable fixtures and independent walkthroughs are described in [evaluation](evaluation.md); neither certifies all platforms.

| Tier | Meaning |
|---|---|
| documented | Scoped instructions/references and sources, no implied execution |
| fixture-tested | Named fixture, versions, command and result retained |
| agent-evaluated | Independent task artifacts/rubric, with required execution evidence |

| Area | Documented coverage | Target-specific limits |
|---|---|---|
| Web | React/Next.js, Astro, Vue/Nuxt, Angular, Svelte/SvelteKit | Hydration, CSP, server/client and cache boundaries need framework/browser fixtures |
| Backend | Node, Python/Django, Java/Kotlin/Spring, Go, .NET, PHP/Laravel, Ruby/Rails | Runtime/ORM conventions differ; database SQL is engine-specific |
| Mobile | iOS/Swift/SwiftUI, Android/Kotlin/Compose, Flutter, React Native, shared cores | Real devices, battery, permissions and signing remain platform-specific |
| Desktop | macOS, Windows, Linux; Electron, Tauri, Qt, MAUI, native | IPC authority, signing, updates; MAUI has no official Linux desktop target |
| Systems | C/C++, Rust, Go, FFI, memory, concurrency, networking | ABI, sanitizers, races, backpressure and OS APIs require native tests |
| AI | LLM integration, RAG, bounded tool agents | Boundary fixtures are not model quality/cost or universal injection-resistance evaluations |
| Data/ML | Pipelines, relational/vector stores, database operations, training/serving | Leakage, lineage, deletion, drift, restore and serving parity |
| Operations | Cloud/IaC, CI/CD, SLOs, incidents, recovery | AWS/Azure/GCP and orchestration guidance; no live cloud certification |
| Specialized | Payments, collaboration, SDK/CLI/extensions, embedded, scientific, graphics | Demand-led profiles; qualification/hardware requirements remain explicit |

Scala, Elixir/Erlang, R, Julia, SQL, shell and WebAssembly can reuse shared workflows; add dedicated adapters only with demand, a maintainer and runnable evidence. Do not create one skill per language.

Maintainers own shared rules. Before promoting support, record reviewer, installed versions, primary source, verification date, fixture and limitations. Review volatile security/provider/platform guidance quarterly or after upstream changes. A live URL is not technical validation. Preserve historical audits and deprecate obsolete references with migration guidance.
