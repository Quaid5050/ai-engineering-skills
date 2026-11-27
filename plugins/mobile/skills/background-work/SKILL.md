---
name: background-work
description: "Change mobile background work safely — periodic sync, uploading queued records, a long-running user-visible task — treating it as safety-critical when users rely on it: decide in the shared core first, change the app ↔ native contract first, follow the platform rules (user-visible foreground work where the OS requires it, adaptive scheduling, battery savers and vendor app killers detected and surfaced, restart after reboot or update, permission flow), record observed failures and distinguish unknown interruptions, write failure-path tests first, do an emulator/simulator pass, then device and battery tests before merge. Use when adding or changing anything that runs while the app is not on screen. Trigger on 'background task', 'background sync', 'runs in the background', 'stops after a while', 'killed in the background', 'foreground service', 'battery drain', 'restart after reboot', 'doze'."
argument-hint: "[the background behaviour to add or change]"
license: MIT
metadata:
  version: "2.0.0"
---

# Background work

Change the background behaviour in `$ARGUMENTS`. If empty, ask what should run while the app is closed and what the user relies on it for.

Background work fails quietly: the OS kills it, a battery saver delays it, a permission is downgraded — and nobody knows. Classify by consequence: a delayed feed refresh differs from a missed safety alert. Persist progress and freshness; device evidence is required for platform-dependent claims.

## 0. Read the project

Reuse the current task context and risk tier from `work-context` (foundation plugin); refresh only changed or missing facts. Load only relevant references. Task authorization and `safe-agent-execution` apply before tool actions.

1. Read `AGENTS.md`, `CLAUDE.md`, decision records, the native READMEs and the project's battery/performance budgets.
2. Find the bridge contract between app code and native code, the shared core if any (`shared-core`), the queue (`offline-queue`), and their test commands.
3. Platform specifics: [references/android.md](references/android.md), [references/ios.md](references/ios.md); cross-platform framework apps also [references/flutter.md](references/flutter.md) (the same questions apply to other frameworks' background plugins).
4. **Where the rules live.** In a native app they live in the shared core (`shared-core`). In a cross-platform framework app, the framework's own language code can be the core: the rules are written once there, pure and tested, and the native side holds only the OS glue the framework plugin needs. Which one this project uses is a **decision record** (`decision`, meta plugin); without one, raise it before writing the rule.

**Gate:** you know which OS mechanism runs this work on each platform today, and where its rules live.

## 1. The flow of a change

1. **Decide in the core.** Any new or changed rule — when to run, how often, when to retry, what blocks, what is reported — is a change in the core (the shared native core, or the cross-platform framework's code when that is the recorded core) with its test written first (`tdd`, quality plugin). No core at all? The rule goes in one tested, pure unit per platform, with shared test vectors so both behave the same — and a design question is raised to pick one core.
2. **Run the core tests on supported, affected targets.**
3. **Contract first:** a new field or call between app code and native code changes the bridge definition, then regenerates both sides. Never hand-edit generated files.
4. **Wire the shells only for OS work:** a new OS input passed in as a parameter, a new adapter method returning failures (never "empty"). If you are writing an `if` about policy in shell code, it belongs in step 1.
5. **Platform tests** where an adapter changed, then native lint.
6. **Emulator/simulator pass** on affected supported platforms (§4), then **device and battery** (§5).

## 2. Rules for supported platforms

- **Use the mechanism the OS intends.** Continuous user-visible work runs as user-visible foreground work with an ongoing notification that says what is running and offers actions (pause, open). A **transfer the user started** (uploading a submission, a large file) uses the OS's user-initiated transfer mechanism where it exists, and a background transfer session that keeps going after the app is suspended. Deferrable work goes to the OS job scheduler with constraints (network, charging). Know each mechanism's **time limits** on current OS versions — some foreground work types are now capped per day — and design for being stopped. Never a hand-rolled timer loop that keeps the process awake.
- **One runner at a time.** The foreground trigger, the background job and a retry timer must not run the same work concurrently: use the scheduler's unique-work policy plus a lease in storage (`offline-queue`).
- **Adaptive, not fixed.** Run often only when it matters (the user is active, data changes fast), back off when idle. Never "every few seconds, just in case".
- **Battery savers and vendor app killers.** Detect when the work was stopped or delayed (a heartbeat the server or the next run checks), surface it to the user with the fix (exempt from battery optimisation, vendor-specific setting) in an onboarding reliability check, and report it.
- **Restore eligible work after reboot/update** only through platform-supported mechanisms; force-stop, user termination and platform restrictions may require user relaunch.
- **Permissions:** explanation screen before every system prompt; background-level access only after foreground; "only while using" or "approximate" is handled by telling the user what will not work (`mobile-conventions` §4).
- **Record observed stop reasons** and last-success timestamps. The OS may kill a process without callback; report stale or unknown interruption rather than inventing a cause or promising immediate server notification.
- **Privacy:** no personal data in logs in release builds; debug logs only with synthetic data.

## 3. Tests (failure paths first)

Write these before the happy path (`testing-doctrine`, quality plugin):
- no network → work queued, retried, delivered later, or the failure is visible;
- process killed and restarted mid-run → state survives, work resumes;
- two runs started at once (foreground trigger + scheduled job) → only one does the work;
- permission revoked or downgraded → surfaced with a reason, not silent;
- server error / timeout → bounded retry with backoff, then a visible problem;
- duplicate or out-of-order runs → one effect, not two — **paired** with a test that dedupe does not swallow a genuine second event;
- device clock skew;
- boundary: eligibility is computed correctly just before/at/after the requested time; separately test delayed execution and missed windows. OS scheduling is not exact.

Each asserts the work still happens **or** the failure is visible to someone. "Nothing happened and nobody knows" is the bug these tests exist for.

## 4. Emulator and simulator (first pass, logic only)

Scripted location/network/time where relevant, forced idle/doze, and **real process death** — not just swiping the app away, which does not stop user-visible foreground work on every OS. Commands are in the platform references. Emulators catch logic errors only; they never replace §5.

## 5. Device and battery (required)

`device-test` rows for background work on representative supported devices, including a constrained device where relevant, in a **release** build: locked phone 30 min, app swiped away, reboot, airplane mode, battery saver on. Battery per the project's budget (for example ≤ X %/h active, ≤ Y %/h idle). Results recorded in the change. If the project batches device tests into one pass before release, list these rows as open in the PR — never skip them silently.

**Gate:** failure-path tests green, affected supported targets built, device and battery rows done or listed as open.

## Scheduling and observation limits

Execution timing and refresh are controlled by the platform. Do not promise exact execution or a known reason for every termination. Persist last successful state, attempt identity and timestamps; interrupted/unknown is distinct from success. A widget uses supported timeline/rendering mechanisms and visible last-update information; an inexact worker cannot guarantee an exact stale transition. Test the actual supported OS/target versions and distinguish force-stop/user termination from OS eviction. Recheck authorization on widget actions and clear shared private snapshots on account change.

## Rules

- No change to safety-critical background work without a failure-path test and a device test.
- Surface observed failures and stale/unknown progress; do not promise notification while the process cannot run.
- Rules change once (the core); a one-platform change says why the other is unaffected.
- Native changes ship by store release, never an over-the-air patch (`release`, lifecycle plugin).
- Record freshness impact; use a spec when risk or unresolved requirements justify one.

## Composition

| From | This skill | To |
|---|---|---|
| `implement`, `bugfix` (lifecycle) | Background change, core first | `shared-core`, `offline-queue`, `device-test`; `perf-check` (quality) for battery |
