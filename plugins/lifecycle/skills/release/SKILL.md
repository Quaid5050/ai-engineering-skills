---
name: release
description: "Ship merged work to users safely — decide the release path per component (backend deploy, web deploy, over-the-air patch where the stack supports it, or a store release for native code, permissions and new plugins — the default depends on the client), check preconditions, version and tag with the user's OK, roll out in stages with an OK and a watch window per step, watch health signals, and roll back per path when a safety or health signal regresses. Use when merged changes should reach users. Trigger on /release, 'ship it', 'release a new version', 'cut a release', 'hotfix', 'staged rollout', 'roll back the release', 'publish to the store'."
argument-hint: "[what to ship: PRs, a version, or hotfix <PR>]"
license: MIT
metadata:
  version: "2.0.0"
---

# Release

Release `$ARGUMENTS` (merged PRs, a version, or `hotfix <PR>`). Every step that reaches users needs the user's explicit go-ahead: this skill prepares and verifies; the user approves each irreversible step.

## 0. Read the project

Reuse the current task context and risk tier from `work-context` (foundation plugin); refresh only changed or missing facts. Load only relevant references. Task authorization and `safe-agent-execution` apply before tool actions.

From `AGENTS.md` and the repo: the release tooling (deploy pipeline, store build commands, over-the-air patch tool if any), where the version lives, the tag format, the environments, the health signals and their targets (`observe`). **No release tooling yet?** Say so; set it up as its own `chore(release)` issue the first time and record the real commands in `AGENTS.md`.

## 1. Decide the path

| Change since the last release | Path |
|---|---|
| Client code the over-the-air tool can patch (UI, logic, strings, already-bundled assets) | **Over-the-air patch**, where the stack supports one — minutes, no store review |
| Native code, bridge definitions, plugins/native dependencies, permissions, manifests, the runtime/engine version, new assets the tool cannot ship | **Store release** |
| Web front end (static bundle or server-rendered app) | **Web deploy**: content-hashed asset names, long cache only on hashed files, the entry HTML not cached; **old open tabs** keep running the previous bundle for hours, so the server stays compatible with it; a stale-bundle prompt or reload on a version mismatch |
| Server only, contract additive | **Backend deploy** (no client release) |
| Server + client, contract changed | Server first (additive, `deploy-check`), then the client |

```bash
git tag --list '<component>-v*' --sort=-v:refname | head -3
git log --oneline <last-tag>..origin/main
git diff --stat <last-tag>..origin/main -- '<native paths>' '<dependency manifests>'
```

**Default when unsure depends on the client:** a mobile app's first release, and any unsure mobile change, is a store release; a web front end ships by web deploy; a server by backend deploy. A repository with several deployable components decides the path **per component**.

**Gate:** the path is named with the diff that decides it.

## 2. Preconditions

- Main's CI green on the commit being released (`ci`).
- `deploy-check` passed for every included PR that touches API, data, native code or config.
- `device-test` (mobile plugin) done for anything touching background work, notifications, widgets or battery.
- Release notes drafted from the merged PR titles, in plain language.
- Crash and error reporting configured for the build.
- Mobile only: store privacy forms (data-safety form, privacy labels) and the privacy-policy URL match what the build collects; every new permission has its usage description.

## 3. Version and tag

Bump the version on a `chore/release-<component>-x.y.z` branch → PR → merge (semantic versioning; mobile build numbers always increase). Then, with the user's OK:

```bash
git tag <component>-vX.Y.Z <sha> && git push origin <component>-vX.Y.Z    # e.g. api-v1.4.0, app-v2.1.0, web-v1.4.0
```

A single-component repository may use plain `vX.Y.Z`. A monorepo tags **per component**, so each release path can be traced and rolled back on its own.

## 4. Roll out in stages

Each step with the user's OK and a watch window (`observe`) before the next:

- **Store release:** build the store artifacts **with the over-the-air tool's release command** when one is used, so later patches can target them; upload to internal testing / beta; install on real devices and run the `device-test` smoke rows; then use the store's supported phased-rollout schedule and measured stop conditions; stores differ in permitted percentages and timing.
- **Over-the-air patch:** confirm no native change since the release being patched; patch to a staging channel first, verify on a device, then promote.
- **Web deploy:** to a preview/staging URL first, smoke the main flows, then production; keep the previous build available for an instant rollback.
- **Backend deploy:** through the pipeline; scheduler coordination and recoverable dispatch during and after the deploy, workers drained gracefully (`references/backend-deploy.md`); migrations run before the new code only when they are additive (expand/contract); smoke the health endpoint and one authenticated call; canary or blue/green where available.

Store specifics are in [references/mobile-stores.md](references/mobile-stores.md); server strategies in [references/backend-deploy.md](references/backend-deploy.md).

**Gate (each step):** the watch window's health signals are at or above target; a regression in any safety signal → halt and roll back.

## 5. Roll back

- **Store build:** halt the staged rollout; ship a fixed build (users who already updated keep the bad one until then).
- **Over-the-air patch:** roll back the patch or publish the previous good code.
- **Web:** point production back to the previous build (or redeploy it); purge the entry-HTML cache.
- **Backend:** redeploy the previous image; roll migrations forward rather than down unless the down path was tested.

## Additional release targets

Desktop packages require signed artifacts, platform trust/notarization where applicable, updater signature verification, downgrade policy and interrupted-update recovery (`desktop-application`, desktop plugin). Model/data changes require evaluation gates, schema/index compatibility, artifact provenance and rollback of code plus model/data versions (`ml-lifecycle`, data plugin). A mobile store workflow does not substitute for these checks.

## Rules

- Never upload, tag, promote or deploy without the user's OK for that step.
- Never release from an unreviewed or red commit.
- Over-the-air patches never add permissions, native code or native dependencies.
- Keep "merged", "released to x%" and "released to everyone" distinct in every report.

## Composition

| From | This skill | To |
|---|---|---|
| `merge`, `deploy-check`, `device-test` (mobile) | A staged release | `observe` during each window; `incident` when it goes wrong |

## Report

Path and why, version/build, what shipped (PR list), rollout stage, health numbers, the next step and its date.
