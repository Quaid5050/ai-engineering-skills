---
name: home-widget
description: "Add or change a home-screen or lock-screen widget, live activity / ongoing status surface, or quick-settings tile — every state built (live, stale with age and reason, paused, off, urgent takeover, hidden on the lock screen), the app writes a small snapshot with precomputed state and a staleAfter instant so the freshness rule is never copied into widget code, no network call on every refresh, actions routed through the app's own code paths, lock-screen privacy, tests per state, device test. Use when building any glanceable surface outside the app. Trigger on 'add a widget', 'home screen widget', 'lock screen widget', 'live activity', 'dynamic island', 'quick settings tile', 'glance widget'."
argument-hint: "[widget, tile or live activity name]"
license: MIT
metadata:
  version: "1.0.0"
---

# Home-screen widget

Build `$ARGUMENTS` (a widget, live activity or tile). If empty, list the designs for glanceable surfaces and ask which one.

## 0. Read the project

1. Read `AGENTS.md`, `CLAUDE.md`, the design for the widget, and the native conventions (`shared-core`, `mobile-conventions`).
2. Find how app code shares data with native extensions today (shared app group / shared preferences / a bridge package), and the existing freshness rule in the app's domain.
3. Platform specifics: [references/android.md](references/android.md), [references/ios.md](references/ios.md).

## 1. States

Every widget implements every state that applies:

| State | Shows |
|---|---|
| Live | The current data and how old it is |
| Stale | Age **and reason** ("Offline since 18:58"), never a fake live state |
| Paused | A clear paused state with a resume action |
| Off / not set up | What is off and how to fix it (opens the app) |
| Urgent takeover | Replaces normal content when something needs attention now |
| Hidden on lock screen | No names, places or content when the user chose privacy on the lock screen |
| Signed out | A sign-in prompt, no stale personal data |

**Gate:** every state has a design or an agreed fallback.

## 2. Data flow

- The app writes a small **snapshot** (versioned JSON: display labels, state per item, ages, no precise personal data unless the widget needs it, then reduced) into storage shared with the extension, and asks the system to reload the widget.
- **The freshness rule is never copied into widget code.** App code computes each item's state with its own domain rule and writes it into the snapshot, together with `staleAfter` (the instant a live entry turns stale). Widget code only renders the state it is given and switches from live to stale at `staleAfter` (a timeline entry or a scheduled update). No time limit is spelled in widget code: a second copy of the rule drifts. A decision the app cannot precompute goes into the shared core with tests, never into widget code.
- Widgets **never call the network on every refresh**. Updates come from the app (new data, a push, background work) within the platform's refresh budget.
- Interactive actions (toggle, start, open) run the app's own code paths (an intent/broadcast into app code), not duplicated logic.
- The snapshot is cleared on sign-out.

## 3. Tests

- App code: snapshot builder unit tests per state, asserting the exact JSON, including urgent takeover, hidden-on-lock-screen and `staleAfter`.
- Native: previews per state; a unit test that the widget parses every snapshot version it may meet (an old app version may have written it).
- Accessibility basics: labels, contrast, large text (`accessibility-audit`, quality plugin).

## 4. Build

Per platform reference. Same names and states on both platforms; tokens mapped from the app's theme.

## 5. Device test

On a real Android and iPhone (`device-test`): add the widget; toggle from it; lock the phone (privacy state); trigger the urgent state and back; kill the app and confirm the widget turns **stale with a reason** rather than staying live. Record results in the PR. Widgets ship with a store release.

**Gate:** all states tested in code and seen on a device (or listed as open per the project's device-test batching rule).

## Rules

- No business rule in widget code; no network per refresh; no personal data on the lock screen unless the user chose it.
- Never show "live" for data the app has not confirmed fresh.

## Composition

| From | This skill | To |
|---|---|---|
| `implement` (lifecycle), `design-to-screen` | Widget states and snapshot | `shared-core` for any decision; `device-test`; `release` (lifecycle) — store release |
