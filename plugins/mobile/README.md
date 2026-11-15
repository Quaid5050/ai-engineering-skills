# mobile 1.0.0

Mobile app architecture, a shared cross-platform core, background work and battery, an offline queue that never loses data, permissions, screens from designs, home-screen widgets and real-device testing. References for Flutter, React Native, Kotlin, Swift and Kotlin Multiplatform.

## Install

```text
/plugin marketplace add Quaid5050/ai-engineering-skills
/plugin install mobile@ai-engineering-skills
```

Installs with: `lifecycle`.

## Skills

| Skill | What it does |
|---|---|
| [`background-work`](skills/background-work/SKILL.md) | Anything that runs while the app is closed: OS mechanisms, battery, app killers, every stop reported |
| [`design-to-screen`](skills/design-to-screen/SKILL.md) | Build a screen from a design: inventory, tokens, every state, tests first, screenshot comparison |
| [`device-test`](skills/device-test/SKILL.md) | Real-device checklist (low-end Android, recent Android, iPhone) recorded in the PR |
| [`home-widget`](skills/home-widget/SKILL.md) | Home/lock-screen widgets, live activities, tiles: all states, precomputed snapshot, privacy |
| [`mobile-conventions`](skills/mobile-conventions/SKILL.md) | App architecture (view → view model → repository → service), shared code with rules, permissions UX, offline storage, performance (Flutter, React Native, Kotlin, Swift references) |
| [`offline-queue`](skills/offline-queue/SKILL.md) | A durable on-device outbox that never loses a record silently |
| [`shared-core`](skills/shared-core/SKILL.md) | One functional core shared by Android and iOS, thin platform shells, interop rules (Kotlin Multiplatform reference) |

See the [catalogue](../../README.md#catalogue) and the [workflow map](../../docs/engineering-workflow.md). License: MIT.
