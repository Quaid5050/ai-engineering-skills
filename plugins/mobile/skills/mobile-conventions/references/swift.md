# Native iOS (Swift) mapping

| Concept | iOS |
|---|---|
| View | SwiftUI `View` structs rendering a state value; or UIKit view controllers kept thin |
| View model | `@Observable` (or `ObservableObject`) `final class` marked `@MainActor`, immutable state struct + action methods; no `UIKit`/`SwiftUI` import in the view model where avoidable |
| Domain | a Swift package target with structs, `enum` results with associated values, repository `protocol`s |
| Repository | `final class` conforming to the domain protocol; `AsyncStream`/Combine publishers; maps `Codable` DTOs and persistence models to domain models |
| Coordinator | an `actor` or a `final class` owning a `Task`, cancelled on sign-out |
| Service | `URLSession` client (or generated OpenAPI client), persistence, platform wrappers |
| Modules | Swift Package Manager targets per feature and a `Shared` target that depends on no feature |
| Strings | String Catalogs (`.xcstrings`) with plural variants |
| Theme | one `Theme`/asset catalog colour set; SwiftLint custom rule against `Color(red:…)` literals |
| Local DB | SwiftData / Core Data / GRDB with versioned migrations and a test that opens a store written by the previous version |

## Rules

- Swift concurrency: `async`/`await`, `@MainActor` for UI state, `[weak self]` in long-lived closures; never mix queues and actors in one type.
- No `try!` or force unwraps outside tests; `do/catch` on specific errors.
- `final class` by default; API Design Guidelines naming.

## Enforcement

- Package target dependencies are the layer rules; a script over `import` lines for anything finer; SwiftLint in CI with no baseline.

## Performance

- Keep `body` cheap; `LazyVStack`/`List` with stable ids; Instruments (Time Profiler, SwiftUI, Hangs) on a device in Release.
