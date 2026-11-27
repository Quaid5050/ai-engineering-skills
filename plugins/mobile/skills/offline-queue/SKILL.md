---
name: offline-queue
description: "Build or change a durable on-device outbox that never loses data silently — every record goes to a local queue that survives process death and carries a permanent client-generated id the server deduplicates on (a repeat returns the original), one uploader at a time, batches with capped backoff, attachments as files uploaded one by one with the parent completed only when all are confirmed, planned losses only when the spec accepts them, an unreadable queue ends the run with a retry (never 'done'), storage failure blocks with a visible problem, a refused batch is split to find the poison record, clock skew handled, old-build data stays readable. Use when an app must send data that may be created offline. Trigger on 'offline queue', 'offline first', 'sync queue', 'outbox on the phone', 'upload when back online', 'data lost offline', 'retry upload', 'batch upload', 'duplicate records after retry'."
argument-hint: "[what is queued, or the queue change]"
license: MIT
metadata:
  version: "2.0.0"
---

# Offline queue

Build or change the on-device queue for `$ARGUMENTS` (what kind of record is queued, or the change). If empty, ask what the app must send and what happens if one record is lost.

Phones go offline for days, get killed mid-upload and run out of storage. A queue that drops a record "because the network failed" loses user data with no trace, and a queue that re-sends without a stable identity creates duplicates. The rule: **durably accepted records remain recoverable until confirmed or explicitly discarded under the agreed policy. Stable identity prevents duplicate logical creates; it does not guarantee delivery. Unknown outcomes remain pending or visible for recovery.**

## 0. Read the project

Reuse the current task context and risk tier from `work-context` (foundation plugin); refresh only changed or missing facts. Load only relevant references. Task authorization and `safe-agent-execution` apply before tool actions.

1. Read `AGENTS.md`, `CLAUDE.md`, decision records, and the existing queue code if any (local database service, uploader, retry timer).
2. Find the server endpoint that receives batches and its dedupe rule (`add-endpoint`, backend plugin), the shared core if any (`shared-core`), and the background mechanism that runs uploads (`background-work`).
3. Find the stack's local database and its migration tests (`mobile-conventions` references).

**Gate:** you can name where records are written, who uploads them, and how the server recognises a repeat.

## 1. Design the queue

| Decision | Rule |
|---|---|
| Write path | The record is written to the local store **before** anything else happens; the write is on the queue's own thread, never the main thread |
| Identity | Each record gets a **client-generated id** (a random UUID) at creation, which is its **permanent** identity: the server stores it as a unique key on the record itself (not in a time-windowed idempotency store — a phone offline for a week must not create a duplicate) and an authorized replay of the same payload **returns the original resource**; a different payload under the same identity is a conflict, and another caller cannot read the original (`add-endpoint`, backend plugin) |
| Single flight | **One uploader at a time** per queue: the foreground trigger, the background worker and a retry timer all go through one lease or lock (a database row lease with an expiry, or the OS's unique-work mechanism) — two uploaders running at once is a classic cause of duplicates after the app is killed |
| Batching | Upload small records in batches (e.g. up to N records or K kB), never one request per record; delete rows only after the server confirmed them, and map each confirmation back by its client id |
| Attachments | Files (photos, documents) are **not** stored in the row: they are written to **app-private storage excluded from cloud backup** (encrypted when sensitive) and referenced by path + hash + size from a child row. Before queueing: compress to the agreed size and **strip metadata** (EXIF, location, device serials) — keep any needed field (capture time) as explicit structured data (`security-privacy-review`, quality plugin). Each file is uploaded on its own (resumable or chunked when large; `add-file-upload`, backend plugin); the **parent record completes only when every child is confirmed**; the file is deleted only after the parent is confirmed. Check free disk space before accepting a new attachment and tell the user when it is low |
| Retry | Backoff with a cap, e.g. 30 s doubling to 5 min, with jitter; the retry delay comes from one rule (the core), coordinated with the OS scheduler's constraints and retry policy; never bypass platform limits to promise exact timing |
| Server answers | A table in the core: success (including "already have it") → delete; retryable (timeout, 5xx, 429 with its delay) → keep and retry; auth expired → refresh then retry; "you may no longer send" → the planned-loss path, if the spec accepts it, else a visible blocked state; **a batch refused as invalid (400/413)** → split the batch to find the poison record. A **single** record or file refused on its own (invalid, too large) is **never dropped silently**: it moves to a visible "needs attention" state the user can see, fix or discard themselves, and it is counted and reported |
| Planned losses | **Only those the spec explicitly accepts**, listed with numbers — for example: sign-out, another account signs in on the device, the server says this device no longer sends, a retention limit (older than N days or beyond M records, oldest first). Each is counted and reported. Nothing else may drop a record. **When data must never be lost** (submissions, payments, evidence), there are no default losses: sign-out revokes the session immediately; pending records remain encrypted and bound to the original account in a quarantined outbox, with authenticated recovery/export or explicit discard according to the agreed policy, retention limits become a visible warning instead of a drop, and the owner decides any exception |
| Unreadable queue | A read error, a damaged row or an undeletable confirmed row **ends the run with a retry** — never "nothing to send" and never "done" |
| Storage failure | Every failed durable write is immediately reported as not saved; never acknowledge success for it. Block further acceptance while storage is unavailable, preserve existing data, and retry only with an explicit recovery path |
| Time | Each record carries wall time and provenance; monotonic measurements are useful only within their boot/session epoch, and server time is used where authoritative; the server tolerates and flags clock skew instead of rejecting |
| Schema | The stored format is versioned; a new build reads rows written by the old build |
| Privacy | Records and files with personal data stay in app-private storage, excluded from backup, encrypted when sensitive; cleared on sign-out only once nothing unsent remains (or the spec accepts the loss); no record content in logs |

Record the design (especially the planned-loss list) in the spec or a decision record.

**Gate:** the planned-loss list is written down **and accepted in the spec** (or is empty), every other path retries, and the dedupe key is the permanent client id.

## 2. Tests first

In the core's or the queue module's tests (`tdd`, quality plugin), failure paths first:
- offline for an hour → records kept, all uploaded on reconnect, in order, no gap;
- process killed after write, before upload → record uploaded after restart;
- process killed after the server confirmed, before delete → the repeat is deduplicated by the server (one row, the original returned, success answer);
- process killed **during** an upload (mid-batch, mid-file) → resumed after restart, one row, one file;
- **two uploaders started at once** (foreground trigger + background worker) → only one runs; duplicate transport attempts are tolerated and create only one logical record;
- a repeat after a long offline period (beyond any idempotency window, e.g. 8 days) → still one row;
- a parent with three attachments, the second upload fails → parent stays pending, retries only what is missing, completes after all three are confirmed;
- a single file the server refuses as too large → moved to "needs attention", visible, nothing else blocked, nothing dropped;
- low disk space → a new attachment is refused with a visible message, queued data untouched;
- server 5xx / timeout → retried with the backoff sequence (assert the exact delays), capped;
- batch refused as invalid → split, the invalid record persisted in needs-attention and counted, the others sent; restart preserves the invalid record and its recovery controls;
- unreadable queue / damaged row → the run ends with retry, not "done";
- the first failed write → not acknowledged as saved, a visible storage problem, existing records intact; recovery never fabricates the missing record;
- each planned loss → exactly the listed records removed, counted, reported — and nothing on any other path; sign-out revokes auth without exposing the original account's pending data to another account;
- retention limit → discard only under an explicit accepted loss policy; otherwise retain and show capacity/recovery controls;
- rows written by the previous build (real bytes from that build, not hand-written fixtures) still read;
- clock skew of ±1 day.

Plus server-side tests that the same client id twice creates one row and returns the original resource both times, also after any idempotency window has passed.

## 3. Build

Per `shared-core` (rules in the core, the database and HTTP as adapters returning failure values) or `mobile-conventions` (repository + database service) when the queue lives in app code. Uploads run through the background mechanism of `background-work`.

## 4. Verify

Run the tests on every target; then the emulator pass (airplane mode, process death) and the `device-test` rows for offline and reboot.

**Gate:** every test in §2 exists and passes; device rows done or listed as open.

## Rules

- A record is never dropped silently; a new loss path needs the spec updated, a counter and a test.
- Never report "done" or "empty" for a failure.
- One retry owner per path: the queue's rule, not a second retry layer in the HTTP client.
- Safety-critical actions do not wait silently in this queue: the UI says "not sent yet" and offers a fallback.
- One uploader at a time; a second trigger joins or waits, never runs in parallel.
- Files are never kept inside rows and never deleted before their parent is confirmed.

## Composition

| From | This skill | To |
|---|---|---|
| `spec`, `implement` (lifecycle), `background-work` | Queue design and tests | `add-endpoint` (backend) for the dedupe endpoint; `shared-core`; `device-test` |
