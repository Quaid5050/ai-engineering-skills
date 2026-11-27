# Idempotency: a worked example

Read this when an endpoint creates or changes something a client may retry. Two mechanisms, chosen by how long a retry can arrive after the first attempt.

## Online creates: an `Idempotency-Key` header

The client sends a fresh UUID per logical operation and reuses it on every retry of that operation:

```http
POST /workspaces/9b2.../orders
Idempotency-Key: 5f0c2a8e-3d4b-4f7a-9c1e-2b6d8e0a7f13
Content-Type: application/json

{ "lines": [{ "sku": "tea-01", "quantity": 2 }] }
```

The server stores one row per key:

| Column | Value |
|---|---|
| scope | `tenant_id` + `actor_id` + route/operation (`createOrder`) — the key is unique **within** that scope, so two callers or two tenants never collide or see each other's response |
| key | the header value |
| fingerprint | a hash of the canonical request (method, route, normalized body) |
| status / body | the original response, or `in_progress` while the first attempt runs |
| expires_at | created + the retention the project sets (for example 24 h), at least as long as the client's retry window |

On a request with a key:

1. Authenticate, then **re-check authorization now** (the access unit, current membership and role). A caller who lost access gets `404`/`403` even if a stored response exists.
2. Look up `(scope, key)`.
   - None → insert it as `in_progress` (unique constraint), run the use case, store the status and body, return it.
   - Found, same fingerprint, finished → return the **original status (`201` or `200`) and body**, unchanged; optionally mark it with an `Idempotent-Replayed: true` header.
   - Found, same fingerprint, `in_progress` → `409` with a retry-after, or wait briefly; never run the use case twice.
   - Found, **different fingerprint** → `422` (or `409`, per the project's error catalogue) with a stable code such as `idempotency_key_reused`; nothing is changed.
3. After `expires_at` the row may be deleted; a key reused after that is a new operation. Document it in the contract.

Tests: same key twice → one row, identical status and body; same key, changed body → `422`/`409`, no change; same key from another tenant or actor → independent, no leak of the first response; caller removed between attempts → `404`; concurrent identical requests → one effect.

## Offline creates: a permanent client id

Records a client may create offline (mobile queues, drafts) carry a **client-generated id** stored as a **unique key on the record itself**, with no expiry. A repeat, even weeks later, returns the original resource (same id, `200`/`201`) to an authorized caller with the same payload; a changed payload under that id is a conflict; another caller cannot read it. Never use the time-windowed key above for data that may sit in an offline queue longer than its retention. If the record was deleted, the contract says what a replay returns (for example `410` from a tombstone) — never a silent re-create.
