---
name: add-endpoint
description: "Add or change a backend API endpoint contract-first on any stack — the contract file first (paths, methods, schemas, problem-detail errors, auth, pagination, idempotency, compatibility), failing integration tests first including forbidden callers (non-member, wrong role, removed member), a thin handler over one use case per backend-conventions, regenerated clients, and a contract drift test. Use when adding or changing a route, request, response or error. Trigger on 'add an API for', 'new endpoint', 'change the API', 'add a route', 'REST endpoint', 'expose this over HTTP', 'API design'."
argument-hint: "[what the endpoint does and who calls it]"
license: MIT
metadata:
  version: "1.0.0"
---

# Add endpoint

Add or change the endpoint for `$ARGUMENTS`. If empty, ask what it should do and who may call it.

## 0. Read the project

1. Read `AGENTS.md` / `CLAUDE.md` / the conventions: where the **contract file** lives (OpenAPI, GraphQL schema, protobuf), how clients are generated, the error-code catalogue, the access rule for tenant/workspace resources, and the test host.
2. Read `backend-conventions` (this plugin) and its stack reference for the handler, service and test idioms.
3. Find a similar existing endpoint and its tests; copy their structure, not their mistakes.
4. Are there released clients (mobile apps, partners) still calling this API? Then every change must be compatible (`deploy-check`, lifecycle plugin).

**Gate:** you know the contract file, the client generator command, the access rule and an example endpoint to follow.

## 1. Contract first

Change the contract before any code: path, method, `operationId` (camelCase verb: `getOrder`, `createBooking`), tags by area, request and response schemas, every error status, and in the description **who may call it** ("any member of the workspace", "workspace admin").

### API design rules

| Topic | Rule |
|---|---|
| Paths | `/v1/<plural-noun>/{id}/<sub-resource>`; kebab-case segments; ids are opaque strings (UUIDs); a non-CRUD action is a `POST` to a verb sub-path (`/v1/orders/{id}/cancel`) |
| Methods | `GET` safe; `PUT` replaces and is idempotent; `PATCH` changes only the fields sent; `DELETE` idempotent → `204`; create → `201` with `Location` when a `GET` for it exists |
| Body | camelCase JSON; enums as strings; times ISO-8601 UTC; no `null` where omission or an empty list says it; secrets and codes only in bodies, never in paths or queries (those land in logs) |
| Errors | RFC 9457 problem details (`application/problem+json`); a new expected failure gets a stable **code** in the project's error catalogue; clients key on the code, never the title; `400` validation with field names, `401`, `403`, `404`, `409`, `429` |
| Auth | Every endpoint requires authentication unless the contract marks it public (sign-in, health); rate limits on anything guessable or costly (codes, sign-in, search) |
| Files | Uploads and downloads follow `add-file-upload` (this plugin): one upload reader, the storage port, presigned or multipart, size caps |
| Isolation | A caller who is not a member of the owning tenant gets `404` (existence is not leaked); a member without the role gets `403` — or the project's stated rule. The **use case** checks it through the access unit on every request: no cached permission decisions, so a removed member loses access on their next request; removal also revokes that member's sessions or tokens scoped to the tenant |
| Filtering and sorting | Explicit query parameters (`?status=open&sort=-createdAt`), each backed by an index; only the filters a screen needs; unknown values → `400` |
| Pagination | Cursor-based for any list that can grow: `?limit=` (default 50, max 200) and `?after=<cursor>`, response `{ "items": [...], "next": "<cursor>" | null }`. An existing list's shape never changes for released clients — paging it is a new operation |
| Idempotency | **Records a client may create offline** (mobile queues, drafts) carry a **client-generated id** that is a **permanent unique key**: a repeat — even weeks later — returns the original resource (same id, `200`/`201`), never an error and never a second row. **Online-only creates** a client may retry carry an `Idempotency-Key` header (UUID); the server stores key + caller + response for a window (e.g. 24 h) and replays the response for a repeat. Never use a time-windowed key for data that may sit in an offline queue longer than the window |
| Compatibility | Released clients keep working: additive changes only (new optional fields, new endpoints). A breaking change is a new version of that resource (`/v2/...`); the old operation is marked `deprecated` and kept until the oldest supported client no longer calls it |

**Gate:** the contract diff is reviewed and every response (including each error) is in it.

## 2. Failing tests first

Integration tests through the real entry point, real database, the project's test host:

- happy path: status + exact body;
- validation: each invalid input → `400` naming the field;
- **authorisation: unauthenticated → `401`; non-member → `404`; member without the role → `403`; removed member → `404`** (or the project's rule);
- idempotency: the same create sent twice (same client id, or same key inside the window) → one row, the same response; for offline-created records, also after the key window has passed;
- revocation: a member removed between two requests gets `404` on the second, including through any cached session;
- pagination: limit, cursor, last page `next: null` — for list endpoints;
- conflict/limit errors from the domain → the right problem code.

Run them and see each fail for the right reason (`tdd`, quality plugin).

**Gate:** every test is red with an assertion failure, not a setup error.

## 3. Implement

Follow `backend-conventions` (this plugin):

- **Handler** (edge): bind, validate shape in the area's validation unit, pass the caller's id to **one** service method, map the result to the response record or the problem. No data access, transaction or rule in it.
- **Service** (application): **authorisation** through the access unit (the edge only authenticates), domain calls, one transaction, notify after commit, result with errors from the area's error list.
- **Rules** in the domain, unit-tested there; reusable queries in persistence; locks in the lock unit.
- Injected clock; timeouts on I/O; logs without personal data; a metric for any new failure mode on a safety-critical path (`observe`, lifecycle plugin).
- Schema change → `add-migration` (this plugin).

## 4. Regenerate clients

Run the project's generator for every client of the contract (never hand-edit generated code), then the clients' analyze/test commands. Use the generated client only from the client's data/repository layer.

## 5. Verify

- The area's full test suite and the build with warnings as errors.
- **Contract drift test:** the server's generated contract compared with the contract file (operations, ids, status codes) — add one if the project has none; it fails on drift.
- For endpoints touching personal data, sharing, auth or payments: `security-privacy-review` (quality plugin).
- In the PR: the contract diff, the authorisation tests, and the compatibility statement.

## Rules

- Never ship a handler before its contract entry and its forbidden-caller tests.
- Never change a released response shape in place; version it.
- Never put secrets, codes or personal data in a path or query string.

## Composition

| From | This skill | To |
|---|---|---|
| `implement`, `new-feature` (lifecycle) | Contract → tests → handler → client | `add-migration`, `add-file-upload`, `add-scheduled-job` (this plugin), `security-privacy-review` (quality), `deploy-check` (lifecycle) |
