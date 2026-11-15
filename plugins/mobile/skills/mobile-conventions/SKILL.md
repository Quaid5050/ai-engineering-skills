---
name: mobile-conventions
description: "How a mobile app is structured and written on any stack — view → view model → repository → service layers with may/must-not rules, coordinators for long-lived loops, feature modules and a shared module with rules, immutable state and closed result types, explicit errors, permission UX, offline storage behind the repository, performance on a low-end device, localisation and RTL, and the architecture tests that enforce it. Use when placing app code, starting a screen or feature, or reviewing a mobile diff. Trigger on 'mobile conventions', 'where does this go in the app', 'view model', 'repository in the app', 'new screen structure', 'is this widget too big', 'permission flow', 'offline storage', 'app architecture'."
argument-hint: "[a change, a file to place, or a diff]"
license: MIT
metadata:
  version: "1.0.0"
---

# Mobile conventions

How app code is laid out and written. Apply it to `$ARGUMENTS` (a change, a file to place, or a diff). If empty, apply it to the change in hand. The principles behind it are `engineering-principles` (lifecycle plugin); background work is `background-work`, a shared cross-platform core is `shared-core`, screens from designs are `design-to-screen`.

## 0. Read the project

1. Read `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, the app's README and any decision records.
2. Identify the stack from the manifest and build files, then open the matching reference: [references/flutter.md](references/flutter.md), [references/react-native.md](references/react-native.md), [references/kotlin.md](references/kotlin.md) (native Android), [references/swift.md](references/swift.md) (native iOS).
3. Find the project's own layer names, folder layout, state-management choice, theme source, string resources and its architecture test. Those are the concrete answer; this skill explains them.

The project wins on facts. If it has no layer rules or no architecture test, say so and offer to add them (`bootstrap-project`, lifecycle plugin).

## 1. Layers

```
 View (screen, components) ──user events──► View model (screen state + actions)
      ▲                                            │ calls
      └──────── observes state ◄───────────────────┤
                                                   ▼
                              Repository (interface in domain, implementation in data)
                                                   │ calls
                                                   ▼
             Service (generated API client, native bridge, OS/plugin wrapper, local database)
```

| Layer | Job | May call | Must not |
|---|---|---|---|
| **View** | Layout, theme, strings, animation, navigation; forwards user events to its view model | its view model; read-only observable data | call a repository or service; hold business rules; catch business errors; format data beyond display |
| **View model** | Screen state (immutable), user actions as methods, combines repositories | repositories, domain functions | import UI toolkit types or a UI context; call services directly; navigate by itself |
| **Domain** | Immutable models, repository **interfaces**, pure rules, input validators — business concepts only (the concept test) | an allowlist: core language libraries and other domain code | I/O, codecs, the UI toolkit, the state library, generated or bridge types |
| **Repository** | Source of truth for one kind of data: fetch, cache, observe, map service models → domain models, map errors → domain errors | services | know other repositories or coordinators; return generated/bridge types or transport exceptions |
| **Coordinator** | A long-lived loop that drives repositories over time: reconnect, reconcile, retry until confirmed, finish pending work | repositories, services, domain rules | be imported by a repository; hold rules (the rule is a domain function, the loop applies it) |
| **Service** | Stateless wrapper around one external source | the outside world | hold state; contain rules |

Rules that follow:
- **A view never calls a repository.** A screen with actions or more than one data source has a view model; a read-only list may observe a repository-backed stream, but every user action goes through a view-model method.
- **Repositories don't know each other.** Combine data in a view model or a domain function.
- **View ↔ view model is 1:1.** A sheet or dialog that performs an action is a view with its own view model; one that only collects input and returns it does not. State shared between screens lives in a repository, never in another screen's view model.
- **One repository method per user action**, named for the action (`renameList(id, name)`), not a general `update(...)` with optional fields.
- **After a write, the screen refreshes from the single source of truth**: the repository's observable re-emits after its own successful writes; otherwise the view model invalidates the affected data.
- **Generated and bridge types never leave the data layer.** API client models and native-bridge models are mapped to domain models by the repository (tested).
- A domain "use case" class is added only when the same multi-repository logic is needed by two view models.

**Gate:** every new file has a layer and a folder from this table (or the project's equivalent); anything that fits nowhere is a design question for `design-review`.

## 2. Features and shared code

- **Feature-first folders:** `features/<feature>/{data,domain,presentation}` (or the project's names). A feature imports another **only through its domain or one public handle** — a file that only re-exports what others may use (no declarations, no logic). Never another feature's presentation or private data files.
- **No cycles between features** (tested). When two features need the same type, it belongs to the lower one or to the shared module.
- **A screen of one feature shown in another feature's flow is composed by the app shell** (the router passes it in as a builder), not imported across features.
- **The shared module has rules:** a stated purpose, an allowlist of what may live there (session, clock, failures, retry backoff, value types), and a test that it **never imports a feature**. Something with its own screens or its own port is a feature, not shared code.
- **The app shell** (app root, router, theme, config, error reporting, design-system components) is an allowlist too.

## 3. State, models and errors

- State and models are **immutable**; screen state is one value (or a loading/data/error wrapper) the view renders.
- Expected outcomes are **closed result types** (sealed/union cases) from repositories → view-model state; the compiler finds every unhandled case.
- Every catch names the type it handles and either surfaces the failure (state, message, report) or rethrows; never an empty catch. Safety-critical actions show the **real** result — no optimistic success.
- Enum labels come from string resources in the presentation layer, never from the enum's name.
- Time comes from an injected clock; never read the system clock in a view or view model.

## 4. Permissions

- **Explain before every system prompt**: an in-app screen says what the permission is for and what stops working without it. Never trigger the OS prompt on first launch with no context.
- Handle every answer visibly: granted, denied, limited/approximate/"while using", revoked later in settings. The app shows what does not work and how to fix it (a deep link to settings), and anything that depends on it reports the reason instead of silently doing nothing.
- Ask for the **background-level** (always) variant only after the foreground one, and only with its own explanation.
- Re-check permissions on every return to the foreground; the OS may have downgraded them.
- New permissions ship with a store release, store review notes and an updated privacy declaration (`deploy-check`, lifecycle plugin).

## 5. Offline storage

- A local database is a **service**: tables, data-access objects and migrations only, no rules.
- The **repository** stays the single source of truth: reads from the local store first, refreshes from the network, and writes per an offline-first recipe (local write + a durable sync queue, `offline-queue`), or online-only for actions that must reach the server now.
- **Safety-critical actions never wait silently in a sync queue**: they show "not sent yet", retry, and offer a fallback.
- Schema changes are versioned migrations with a migration test (data written by the previous build is still readable).

## 6. Performance on a low-end device

Budgets live in the project (cold start, frame time, memory); measuring is `perf-check` (quality plugin), always in a profile/release build on a real low-end device.
- **Rebuild only what changes:** observe the smallest slice of state in the smallest component that needs it; split screens into components so unchanged parts are skipped; a ticking clock or age label lives in its own small component.
- **No work in the render/build function:** sort, filter, format and parse in the view model, once per state change.
- **Lazy lists** with stable keys for anything that can grow.
- **Heavy work off the main thread** (large JSON, images, big sorts).
- **Cheap paint:** animate opacity/transform, avoid offscreen layers and blur/shadow in scrolled or animated parts; isolate independently animating parts.
- **Images decoded at their on-screen size.**
- **Clean up:** every controller, subscription, timer and animation is disposed; animations stop off screen and with reduced motion.
- **Startup:** nothing heavy before the first frame; initialise plugins lazily.

## 7. Strings, localisation, RTL, accessibility

- Every user-facing string is a key in the string resources (with a description; plurals and placeholders via the message format). No literal text in views.
- Layout uses start/end (directional) insets and alignment, never left/right, so RTL locales mirror correctly.
- Colours, radii, spacing and type come from the one theme source; a missing token is added there, never a literal colour in a view (tested). See `design-to-screen` for the contrast rule.
- Interactive elements have labels and ≥ 48 dp / 44 pt targets (`accessibility-audit`, quality plugin).

## 8. Enforcement

An architecture test reads the source tree and fails (empty baseline) when: generated/bridge code is imported outside the data layer; a feature imports another other than through its domain or public handle, a handle declares anything, or features form a cycle; a domain file imports outside its allowlist; the shared module imports a feature; the app shell holds a file outside its allowlist; a colour literal appears outside the theme; a view model imports the UI toolkit; a view imports a repository or calls one; a repository imports a coordinator; a fake used by tests declares app-level bindings; a presentation file passes a size limit (e.g. 320 lines). Lint and formatting run in CI.

## Rules

- No exceptions by precedent: code that breaks a rule is fixed or gets an issue, never copied.
- The stack reference adds detail; it never overrides the layer rules.
- Safety and privacy rules of the project always win (no personal data in logs or crash reports).

## Composition

| From | This skill | To |
|---|---|---|
| `implement`, `design-review` (lifecycle), `design-to-screen`, `code-review` (quality) | Layers, placement, checklist | `background-work`, `offline-queue`, `shared-core` for native work; `perf-check` (quality) to measure |

## Checklist for review

- [ ] Files in the right layer/folder with the project's suffixes; generated code untouched.
- [ ] No view calls a repository or service; actions go through a view-model method.
- [ ] View models import no UI toolkit; domain imports only its allowlist.
- [ ] Repositories implement a domain interface, return domain models/closed results, never generated types or transport errors; they don't call each other.
- [ ] Features meet only through domain or a re-export handle; no cycles; shared module has rules and imports no feature.
- [ ] Rules are domain functions; long loops are coordinators.
- [ ] Permissions explained before prompts; every denial visible.
- [ ] Performance rules of §6; numbers in the change for list/animation-heavy screens.
- [ ] Strings, tokens, directional layout, semantics.
- [ ] Every catch typed and visible; safety actions show the real result.
