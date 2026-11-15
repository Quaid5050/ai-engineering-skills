# GitHub Actions: a minimal, safe CI template

Hosted runners only (safe for public repositories), path filters so each area builds only when it changed, `concurrency` to cancel superseded PR runs (never runs on main), a PR-links-an-issue check, least-privilege permissions. Adapt job names to the project and keep them stable: the merge gates refer to them.

```yaml
name: CI

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

concurrency:
  # cancel superseded runs on pull requests only; every commit on main gets a complete run
  group: ci-${{ github.event_name == 'pull_request' && github.ref || github.run_id }}
  cancel-in-progress: ${{ github.event_name == 'pull_request' }}

jobs:
  changes:
    name: Changed areas
    runs-on: ubuntu-latest
    outputs:
      backend: ${{ steps.filter.outputs.backend }}
      web: ${{ steps.filter.outputs.web }}
      mobile: ${{ steps.filter.outputs.mobile }}
    steps:
      - uses: actions/checkout@v4
      - uses: dorny/paths-filter@v3
        id: filter
        with:
          filters: |
            backend:
              - 'backend/**'
              - 'contracts/**'
              - '.github/workflows/**'
            web:
              - 'web/**'
              - '.github/workflows/**'
            mobile:
              - 'mobile/**'
              - 'contracts/**'
              - '.github/workflows/**'

  issue-link:
    name: PR links an issue
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - name: Body says Closes #<n>
        env:
          BODY: ${{ github.event.pull_request.body }}
          AUTHOR: ${{ github.event.pull_request.user.login }}
        run: |
          case "$AUTHOR" in dependabot*|renovate*) exit 0 ;; esac
          printf '%s' "$BODY" | grep -qiE '(close[sd]?|fix(e[sd])?|resolve[sd]?) +#[0-9]+' \
            || { echo "The PR body must say 'Closes #<issue>'."; exit 1; }

  backend:
    name: Backend
    needs: changes
    if: needs.changes.outputs.backend == 'true'
    runs-on: ubuntu-latest
    services:                       # hosted Linux runners support service containers
      db:
        image: postgres:17
        env: { POSTGRES_PASSWORD: test }
        ports: ['5432:5432']
        options: >-
          --health-cmd "pg_isready" --health-interval 5s --health-timeout 5s --health-retries 10
    steps:
      - uses: actions/checkout@v4
      # set up the toolchain with its official setup action, with caching keyed on the lock file
      - run: make backend-check     # the same command AGENTS.md tells people to run locally

  web:
    name: Web
    needs: changes
    if: needs.changes.outputs.web == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: make web-check

  mobile:
    name: Mobile (analyse + unit tests)
    needs: changes
    if: needs.changes.outputs.mobile == 'true'
    runs-on: ubuntu-latest           # Android builds and most cross-platform test steps run on Linux
    steps:
      - uses: actions/checkout@v4
      - run: make mobile-check

  ios:
    name: iOS build
    needs: changes
    if: needs.changes.outputs.mobile == 'true'
    runs-on: macos-latest            # iOS builds need macOS; hosted macOS minutes cost more — keep this job lean
    steps:
      - uses: actions/checkout@v4
      - run: make ios-build          # no code signing on PRs
```

## Toolchain setup steps (examples — pin the versions your project uses)

| Stack | Setup step | Cache key |
|---|---|---|
| Python | `actions/setup-python` with `python-version` and `cache: pip` (or set up uv/poetry) | the lock file |
| Node | `actions/setup-node` with `node-version` and `cache: npm` / `pnpm` | the lock file |
| JVM (Java/Kotlin) | `actions/setup-java` (`distribution: temurin`) + `gradle/actions/setup-gradle` | Gradle files |
| .NET | `actions/setup-dotnet` with `dotnet-version`, `cache: true` with a lock file | `packages.lock.json` |
| Flutter | `subosito/flutter-action` with a pinned version and `cache: true` | `pubspec.lock` |
| iOS | Xcode preinstalled on `macos-*` runners; select a version with `sudo xcode-select -s` | `Podfile.lock` / package resolution |

Use the action's current major version (check its README); let Dependabot or Renovate keep the pins current.

## Notes

- **Same command locally and in CI.** Put the steps in a `Makefile`/script and call it from both, so `debug` can reproduce a failure exactly.
- **Skipped means passed** only for a job whose area did not change; a workflow change runs every job.
- **Pin actions.** Major tags are the minimum; pin to a commit SHA for actions that receive secrets or write permissions. Let Dependabot or Renovate keep them current.
- **Forks:** `pull_request` from a fork has no secrets and a read-only token — good. Never combine `pull_request_target` with checking out the PR head.
- **Self-hosted runners** are for private repositories only. A public repository with a self-hosted runner lets any fork PR run code on that machine.
- **Required checks:** set them in branch protection / rulesets by job name; when PR CI is temporarily off, the merge gate is the same commands run locally on the head commit with their summary pasted in the PR.
- **Link checking, lint, docs:** cheap jobs that run on every PR catch most "review comment" problems before a human looks.
