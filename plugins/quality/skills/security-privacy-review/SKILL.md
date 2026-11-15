---
name: security-privacy-review
description: "Review a change, spec or feature for how it could expose someone's personal data or be abused — map every piece of personal data (created, stored, sent, who reads it, kept how long), check authorisation and tenant isolation with forbidden-caller tests, consent and visibility, abuse cases by insiders and controlling people, leaks into logs/errors/telemetry/analytics (the canonical logging rule), uploads and metadata, secrets per purpose, an OWASP API Top 10 pass, retention and deletion. Use when a change touches personal data, auth, sharing, payments, uploads, exports or a new third-party SDK. Trigger on /security-privacy-review, 'security review', 'privacy review', 'threat model this', 'can this leak', 'is this safe', 'abuse case'."
argument-hint: "[PR, branch, spec or feature]"
license: MIT
metadata:
  version: "1.0.0"
---

# Security & privacy review

Review `$ARGUMENTS` (a PR, branch, spec or feature) for how it could expose someone's data or be abused. If empty, review the current branch's diff.

Run it when a change touches: personal data, sharing or visibility, roles and invitations, authentication and sessions, payments, notifications, analytics, uploads, exports or deletion, or any new third-party SDK.

## 0. Read the project

1. Read `AGENTS.md` / `CLAUDE.md` / `SECURITY.md` and any privacy policy or data inventory in the repo: what the project calls personal or sensitive data, its retention periods, its authorisation status codes.
2. Read the diff (or spec) and the code paths it reaches: entry points, use cases, storage, outbound calls, logs.
3. If the project has no written data rules, use §5 here as the default and offer to record it.

## 1. Map the data flow

For each piece of personal data the change reads or writes (names, contact details, location, payment data, health data, photos, messages, device identifiers):

| Data | Created where | Stored where (table, cache key, device storage) | Sent to (API, realtime channel, push, email/SMS, analytics, error reporting, third party) | Who can read it | Kept for |
|---|---|---|---|---|---|

Anything you cannot fill in is the first finding.

**Gate:** the table is complete, or each gap is listed as a finding.

## 2. Authorisation and isolation

- Every endpoint, realtime method and job checks the caller **owns or is a member of** the resource **and** has the role the action needs.
- Ids in URLs are never trusted: fetching another tenant's resource returns the project's not-found status (existence is not leaked), proven by an integration test with a non-member, a member without the role, and a removed member.
- Realtime groups/channels are joined server-side from membership, never from a client-supplied name.
- Losing access (removed, role changed, account closed) takes effect immediately, including caches — tested.
- Share links and invites: unguessable (≥ 128-bit random), expiring, revocable, scoped, rate-limited; revoking takes effect at once.

## 3. Consent and visibility

- Sharing personal data with other people is opt-in, and the person shared sees who can see what and can stop it.
- No silent collection: a new way of seeing someone's data appears on that person's own screen.
- People who cannot consent for themselves (children, dependants): who consented, and what the person sees.

## 4. Abuse cases

Ask "how would a controlling partner, an ex, an ex-employee, a malicious insider or a scraper misuse this?":
- Can someone add a person or device to a group without them knowing?
- Can a privacy choice (hiding, pausing, blocking) be detected and punished, or revealed by the app?
- Can history, exports, screenshots or notifications reveal more than the live view allows?
- Can a removed member keep a link, a token or cached data?
- Can support or admin tools see more than the task needs, without an audit trail?
- Can a manager or supervisor use data collected for the work (locations, timestamps, photos, activity) to track a person beyond the task — outside working hours, at home, over time? Collect only what the task needs, show the person what is recorded, and limit who can see history.
- A lost or stolen device: what can its finder read, and can the owner sign it out remotely?

## 5. Leaks — the logging rule

**The logging rule (canonical; other skills refer here):** personal data — names, contact details, precise location, addresses, payment data, health data, message text, tokens and secrets — never appears in anything that leaves the device or server process: release-build client logs, shipped server logs at any level, exception messages, URLs and query strings, error-reporting events and breadcrumbs, metrics, traces, analytics. Local debug builds with synthetic data may print them. Opaque ids (UUIDs) are allowed in logs, never as metric tags (cardinality and re-identification).

- A structured log, telemetry attribute or exception that **contains an object carrying personal data** breaks the rule as much as the raw field — object destructuring and default `toString` of such types included. Make those types' string forms leave the data out.
- Check the diff: search new log, print, telemetry and exception lines for personal fields; read every multi-line log call (line greps miss them).
- Notifications: no sensitive content on lock screens unless the person chose it; data payloads minimal.
- Analytics: no personal data or free text (`analytics-event`).
- Third parties: no personal data to ads/analytics SDKs; a new SDK needs a decision record (`decision`, meta plugin) and a privacy note.

## 6. Security basics

- **Authentication:** one-time codes rate-limited per identifier and per IP, attempt limits, expiry, no user enumeration in errors. Sessions: short-lived access tokens + refresh, revoked on sign-out and account deletion, with a server-side way to revoke all sessions of a device or account (remote sign-out of a lost device).
- **Tokens on mobile:** in the platform's secure storage (keychain / keystore), never in plain preferences or files.
- **Tokens on the web:** session in an `HttpOnly`, `Secure`, `SameSite` cookie — never in `localStorage` where any injected script can read it; cookie-based sessions need CSRF protection (a CSRF token or double-submit for state-changing requests from a single-page app, plus `SameSite`); XSS defences: output encoding by default, no raw HTML from data, and a Content Security Policy without `unsafe-inline` scripts.
- **Data at rest on the device:** queues, caches and files holding personal data live in app-private storage, excluded from cloud backup where the platform allows, and encrypted when the data is sensitive (the platform's file protection or an encrypted database with a key in secure storage); cleared on sign-out only when nothing unsent would be lost (`offline-queue`, mobile plugin).
- **Secrets:** one owner and one configuration entry per purpose, validated at start-up; never a fallback to another purpose's key; never in the repo or the client bundle.
- **Input:** validated at the boundary; size limits on uploads and batches; no query built by string concatenation.
- **Uploads:** size limit; type checked from the bytes, not the name or declared type; re-encoded server-side; **metadata (EXIF, GPS, device serials) stripped** — on the device before upload where the client can do it, and again on the server before storage; stored outside the web root under a random name; served through a signed or authorised URL; never executed or rendered as HTML (`add-file-upload`, backend plugin).
- **Metadata the product needs** (capture time, place of capture as evidence): never kept by leaving it inside the file. Extract only the needed fields into explicit, structured, consented data with its own retention and access rule, then strip the file.
- **Dependencies:** a new package needs a reason, a maintained source and a licence check; no package that phones home with user data.
- **Transport:** HTTPS only.
- **OWASP API Top 10 pass:** broken object-level authorisation, broken authentication, broken object-property-level authorisation (excessive data exposure, mass assignment), unrestricted resource consumption, broken function-level authorisation, unrestricted access to sensitive business flows, SSRF, misconfiguration, improper inventory, unsafe consumption of third-party APIs.

## 7. Retention and deletion

Data kept only as long as the project says; account deletion removes or anonymises every row that identifies the person (including analytics rows and media); backups follow the same rule within their window.

## 8. Output

```markdown
## Security & privacy review: <change>
Risk: low | medium | high

### Data flow (table)
### Findings
- [critical|major|minor] what — scenario (who is harmed and how) — fix — test that proves it
### Abuse cases considered
### Checked and fine
```

**Gate:** each finding names the test (usually an integration test with a forbidden or removed caller) that will prove the fix.

**Where it goes:** for a PR, post the review as **one** PR comment starting `## Security & privacy review — <short head SHA>` (checked against the project's attribution rules first); for a spec, under the spec's review notes. It is a required verdict for `merge` gate 8 (lifecycle plugin) whenever the change touches personal data, auth, sharing, uploads, payments or analytics.

## Rules

- `critical` findings block the merge (`merge` gate 8) unless the owner's acceptance is quoted in the PR.
- Never paste real personal data into the review, an issue or a PR; use synthetic examples.
- When in doubt whether data is personal, treat it as personal.

## Composition

| From | This skill | To |
|---|---|---|
| `code-review` (dimension 2), `spec` and `design-review` (lifecycle plugin), the `reviewer` agent (agents plugin) | Data flow, isolation, abuse cases, leaks | `file-bug` (lifecycle) for findings outside the change; `decision` (meta) for a new SDK |
