# Native Android (Kotlin) mapping

Follows Android's *Guide to app architecture* (UI layer, data layer, optional domain layer).

| Concept | Android |
|---|---|
| View | Jetpack Compose screens (`@Composable fun ListScreen(state, onAction)`), stateless where possible; or Fragments/Views |
| View model | `androidx.lifecycle.ViewModel` exposing `StateFlow<UiState>` (immutable `data class` / `sealed interface`) and action methods; no `Context`, no Compose imports |
| Domain | pure Kotlin module: `data class`, `sealed interface` results, repository interfaces |
| Repository | class implementing the domain interface; exposes `Flow`; maps Retrofit/Ktor DTOs and Room entities to domain models |
| Coordinator | a class with its own `CoroutineScope` (`SupervisorJob` + injected dispatcher), started from the `Application` or a `WorkManager` worker |
| Service | Retrofit/Ktor client, Room DAO, platform wrappers |
| DI | Hilt or Koin; tests replace bindings |
| Modules | Gradle modules `:feature:<f>`, `:core:<shared>`; `:core` never depends on `:feature` |
| Strings | `res/values/strings.xml`, `plurals` |
| Theme | Material 3 `ColorScheme` + custom tokens in one theme file |
| Local DB | Room with `@Database(version = N)` and `AutoMigration`/`MigrationTestHelper` tests |

## Rules

- Collect state with `collectAsStateWithLifecycle()`; one-off events as state, not `SharedFlow` hacks.
- Coroutines: no `GlobalScope`, no `runBlocking` on main; inject dispatchers for tests (`StandardTestDispatcher`).
- No `!!` in new code; catch specific exceptions (`IOException`, `SecurityException`).

## Enforcement

- Konsist or ArchUnit tests for layer imports; Gradle module boundaries; `ktlint`/`detekt` in CI with no baseline.

## Performance

- Compose: stable/immutable state classes, `remember`/`derivedStateOf`, `LazyColumn` with `key`, avoid reading state high in the tree; Baseline Profiles for startup; Macrobenchmark for frame timing.
