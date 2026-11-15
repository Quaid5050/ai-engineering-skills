---
name: web-conventions
description: "How a web front end is structured and written on any framework — for both content sites (marketing, docs: zero client script by default, sections, copy dictionaries) and web apps (dashboards, authenticated tools: screen → view model/hooks → repository → generated API client, server-state caching, forms mirroring server limits, cookie sessions with CSRF protection, errors keyed on problem codes) — plus design tokens from one source, no inline scripts (CSP), no third-party requests by default, accessibility, performance budgets and tests on the built output. Use when writing or reviewing web UI code. Trigger on 'web conventions', 'where does this go in the front end', 'component structure', 'dashboard structure', 'data fetching', 'design tokens', 'CSP', 'inline script', 'third-party script', 'SPA or static'."
argument-hint: "[web change, file to place, or diff]"
license: MIT
metadata:
  version: "1.0.0"
---

# Web conventions

How web front-end code is laid out and written. Apply it to `$ARGUMENTS` (a change, a file to place, or a diff). If empty, apply it to the change in hand. The why is `engineering-principles` (lifecycle plugin). Framework idioms: [references/react.md (SPA and Next.js)](references/react.md), [references/astro.md](references/astro.md).

## 0. Read the project

1. Read `AGENTS.md` / `CLAUDE.md` / the web folder's README: framework, rendering mode (static, server-rendered, single-page app, hybrid), commands (lint, type-check, unit, build, e2e), the design source, the token source (possibly shared with a mobile app), and content rules.
2. Decide which **kind** this is — a **content site**, a **web app**, or both in one repository (then each part follows its own section below).
3. Open the matching reference; if none matches, map the rules onto the framework's own conventions and say so.
4. Find the token source, the copy dictionaries, the CSP/headers config, the generated API client (apps), and the build-output checks.

**Gate:** you know the kind, the folder each part lands in, and the commands that prove it.

## 1. Shared rules (every kind)

| Kind of code | Home | Rule |
|---|---|---|
| Routes | The framework's route folder | Thin: pick locale and data, render one screen/composition component; no layout, copy or rules here |
| Layouts | One base layout | Document head, CSP, fonts, header/footer, `lang`/`dir` |
| Shared components | A components folder **with rules** | Small leaf components with typed props; never import a feature |
| Copy | Locale dictionaries (one source locale) | No literal user-facing text in components; plurals and placeholders through the formatter; other locales type-checked against the source |
| Tokens and base styles | One stylesheet of custom properties | Mirrored from the single token source; never a hex literal in a component |
| Static assets | The framework's static folder | Self-hosted fonts and media |
| Build guards | A scripts folder, not shipped | Checks over the built output |

- **Tokens and contrast:** a new colour is a token in the source first. A brand colour that fails contrast with white is decoration only; text and icons on it use the darker variant. Contrast is tested (`accessibility-audit`, quality plugin).
- **No inline scripts** (strict CSP `script-src 'self'`, nonces only where the framework injects its own), except structured data. Never weaken the CSP to make code work.
- **No third-party requests by default** (CDN fonts, analytics, embeds, pixels). One needs a decision record and a privacy note.
- **Images** through the framework's image pipeline with `width`/`height`, `alt` (`alt=""` when decorative), sized for their slot.
- **Security headers** (CSP, `Referrer-Policy`, `Permissions-Policy`, `X-Content-Type-Options`, HSTS) configured once, checked on the built output.
- **Accessibility:** one `<h1>`, headings in order, landmarks, real `<a>`/`<button>`, keyboard reachable with visible focus, targets ≥ 44 px, colour never the only signal, logical CSS properties for right-to-left, `prefers-reduced-motion` respected.
- **Performance budget** stated in the project (bytes of script and CSS, a lab score, Core Web Vitals); a change that grows them says by how much (`perf-check`, quality plugin).

## 2. Content sites

- One **composition component** per page holds section order and page-level data; one **section** per file. A new section = one file + one line in the composition.
- **Zero client script by default.** Prefer HTML that needs none: `<details>/<summary>`, `popover`, `:hover` with `:focus-visible`, CSS motion. When script is needed: one bundled entry calling `init*()` functions; elements found by `data-*` hooks; server values passed through `data-*` attributes, not globals.
- A client framework runtime on a content site needs a decision record with its size cost.
- Claims match what the product really does; anything not built is labelled planned.

## 3. Web apps

Same layering as a mobile app (`mobile-conventions`, mobile plugin) and the server's error contract (`add-endpoint`, backend plugin):

| Layer | Job | Must not |
|---|---|---|
| **Screen** (route component + its parts) | Layout, copy, states; forwards user actions | call the API client; hold business rules; build its own error messages from status codes |
| **View model / screen hooks** | Screen state, user actions as functions, combines repositories | touch the DOM; import the generated client |
| **Repository / data module** | One kind of data: fetch, cache, invalidate, map API models → app models, map problem codes → typed errors | return generated API types to screens |
| **Generated API client** | Generated from the contract, never hand-edited | be imported outside the data layer |

- **Server state** lives in one caching layer (a query cache) keyed per resource; writes invalidate or update the affected keys; no ad-hoc copies of server data in component state.
- **Forms:** validation mirrors server limits from the contract (lengths, formats) for instant feedback; the server's refusal (problem code + field names) is still handled and shown on the field.
- **Auth and session:** session in an **httpOnly, Secure, SameSite** cookie (no tokens in local storage); CSRF protection for cookie-authenticated writes; one place that handles **401** (sign in again), **403** (explain, hide the action) and **404** (gone or no longer yours — e.g. a member removed mid-session returns to a safe screen without leaking existence).
- **Errors keyed on stable problem codes**, never on titles or messages; unknown codes get a generic, honest message and are reported.
- **Optimistic updates** only for reversible, low-stakes actions; critical actions (payments, anything on the project's safety-critical list) show the real result.
- **Every state** per screen: loading, empty, error, offline/retrying, forbidden, success; long lists paginated with the API's cursor.
- Configuration through the build's environment variables, validated at start; no secrets in the client bundle.

## 4. Tests and checks

- Test first (`tdd`, quality plugin). Content sites: e2e on the built site (sections present per locale, controls work with keyboard, RTL) + build-output checks. Apps: component/screen tests per state with HTTP mocked **at the network boundary** (recorded responses), repository tests against the same, and e2e for the critical journeys against a production build with a seeded backend or recorded API.
- Order: lint/type-check → unit/component → build (with output guard) → e2e.

## Checklist for review

- [ ] The kind (content site / app) is clear and its section was followed.
- [ ] Routes thin; components typed; no literal user-facing text; tokens only; contrast rule respected.
- [ ] No inline script, no third-party request, CSP untouched; headers checked on the build.
- [ ] Apps: screens never import the generated client; server state in the cache layer; errors keyed on problem codes; 401/403/404 handled in one place; session in httpOnly cookies with CSRF protection; optimistic only for reversible actions; every state built.
- [ ] Content sites: zero-JS preferred; behaviour through `init*()` + `data-*` hooks; claims match scope.
- [ ] Accessibility basics; reduced motion; budget impact stated.
- [ ] Tests at the right level; all commands green.

## Rules

- The project's own conventions win on names and paths; no exceptions by precedent.
- Never add tracking or a third-party request without a decision record and the user's OK.
- Never store session tokens where scripts can read them.

## Composition

| From | This skill | To |
|---|---|---|
| `add-web-page`, `build-web-screen` (this plugin), `implement` (lifecycle), `code-review` (quality) | Web placement and rules | `accessibility-audit`, `perf-check`, `security-privacy-review` (quality); `decision` (meta) for a new framework or third party |
