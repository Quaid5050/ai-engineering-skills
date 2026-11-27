---
name: device-test
description: "Real-device test checklist for mobile changes that touch background work, offline behaviour, notifications, widgets, permissions or battery — device slots (low-end Android, recent Android, iPhone), release builds, test accounts only, an emulator/simulator first pass, checklist rows, battery against the budget, a results table in the PR, and a bug for every failure; device tests may be batched into one pass before release when the project allows, but are never silently skipped. Use before merging or releasing anything a simulator cannot prove. Trigger on 'device test', 'test on a real phone', 'test on device', 'battery test', 'does it work when the app is killed', 'test on low-end android'."
argument-hint: "[PR, branch or feature]"
license: MIT
metadata:
  version: "2.0.0"
---

# Device test

Run the rows that apply to `$ARGUMENTS` (a PR, branch or feature) and record the results. If empty, use the current branch's PR.

Emulators and simulators catch logic errors. Background limits, vendor battery killers, notification delivery on a locked phone and real battery drain only show on real hardware, in a release build.

## 0. Read the project

Reuse the current task context and risk tier from `work-context` (foundation plugin); refresh only changed or missing facts. Load only relevant references. Task authorization and `safe-agent-execution` apply before tool actions.

1. Read `AGENTS.md`, `CLAUDE.md`, the project's device list, performance and battery budgets, and its rule for **when** device tests run (per PR, or batched into one pass before release).
2. Find the build commands for a release-mode build on each platform and the test accounts/environment to use.

## 1. Devices

| Slot | Example | Why |
|---|---|---|
| Low-end Android (2–4 GB RAM, aggressive vendor battery management) | a budget model from a vendor known for app killers | Slow CPU, background killing |
| Recent Android | a current flagship | Reference behaviour |
| iPhone | a model a few years old, current iOS | Background limits, notifications |

Install a **release** (or profile) build. Debug builds behave differently in the background. Use test accounts and synthetic data — never a real user's data.

## 2. First pass on emulator/simulator (optional)

Scripted network loss, forced idle/doze, real process death and scripted location or time where relevant (commands in `background-work` references). Logic only; it does not count as a device test.

## 3. Checklist (mark ✅ / ❌ / n/a per device)

**Onboarding and permissions**
- [ ] Fresh install → each permission is explained before its system prompt.
- [ ] Deny / "only while using" / "approximate" / revoke later in settings → the app shows what does not work and how to fix it.
- [ ] Camera and photo library (if used): first-time prompt after an explanation; denied → a way to fix it; iOS limited photo access → the app works with the selected photos and offers to change the selection.

**Background work**
- [ ] Runs while the app is in the background; slows down when idle, as designed.
- [ ] App swiped away / phone locked 30 min → still runs, or the UI shows age + reason.
- [ ] Reboot and app update with the feature on → resumes.
- [ ] Battery saver / vendor optimisation on → detected and surfaced with the fix.

**Offline and uploads**
- [ ] Airplane mode 10 min while creating data → queued, uploaded on reconnect, nothing missing, no duplicates.
- [ ] Offline for **days** (set the device clock or leave it overnight in airplane mode) with several records and attachments → all durable records recovered on reconnect; retries create one logical record per identity.
- [ ] Killed while offline → data still uploads after the next start.
- [ ] Killed **during** an upload (force-stop mid-transfer of a large attachment) → resumes after restart; the server has one record and one copy of each file.
- [ ] Flaky network (throttled, dropping) and a captive portal (Wi-Fi that answers with a login page) → no false "sent", retries, no duplicates.
- [ ] Low storage (fill the device to near full) → a new attachment is refused with a clear message; queued data is untouched.

**Notifications**
- [ ] Arrive on a locked phone within the budget; tapping opens the right screen.
- [ ] Lock-screen text respects the privacy setting.
- [ ] Duplicate events produce one notification; a genuine repeat still notifies.

**Widgets and tiles** (if changed)
- [ ] Added, every state seen, actions work, lock-screen privacy, app killed → stale with reason.

**Battery** (project budget)
- [ ] 1 h active use: % used vs budget.
- [ ] 1 h idle with the feature on: % used vs budget.

**Accessibility smoke**
- [ ] Largest font size: main flows usable, nothing clipped.
- [ ] Screen reader (TalkBack / VoiceOver): the main action, and any urgent action, can be completed and cancelled.

Add rows the change needs; remove none that apply.

## 4. Record in the PR

```markdown
### Device test
| Row | Low-end Android (model, OS) | Recent Android (model, OS) | iPhone (model, iOS) |
|---|---|---|---|
| Background: locked 30 min | ✅ | ✅ | ❌ stopped after 18 min — <bug link> |
| Battery, active | 3.6 %/h | 2.9 %/h | 3.1 %/h |
```

Every ❌ gets a bug (`file-bug`, lifecycle plugin) or a fix in the same PR before release.

**Gate:** every applicable row has a result per device, or — if the project batches device tests — is listed as **open** in the PR and in the pre-release device pass.

## Rules

- Never mark a device row passed from an emulator run.
- Never skip a row silently: not done = listed as open, with the reason.
- Never use real people's accounts or data; never act on a device you were not asked to use (address devices by serial).
- A release that touches background work, notifications, widgets or battery does not ship with open device rows.

## Composition

| From | This skill | To |
|---|---|---|
| `background-work`, `offline-queue`, `home-widget`, `implement` (lifecycle) | Device checklist and results | `file-bug` (lifecycle) for each ❌; `release` (lifecycle) requires it; `perf-check` (quality) for battery detail |
