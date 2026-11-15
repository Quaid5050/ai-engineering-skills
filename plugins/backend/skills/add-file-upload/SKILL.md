---
name: add-file-upload
description: "Add or change file uploads and attachments on the server end to end — one upload reader at the edge and the one storage port (never a per-feature storage class), presigned vs multipart vs resumable chosen deliberately, type detected from the bytes, size caps that fail visibly, images re-encoded and metadata stripped (needed fields kept only as explicit, consented structured data), random names outside the web root, member-checked or signed short-lived reads, a parent record that commits only when all its attachments are confirmed, orphan cleanup, optional malware scanning, and tests including forbidden callers and oversize files. Trigger on /add-file-upload, 'upload a file', 'attach photos', 'image upload', 'presigned URL', 'multipart upload', 'store files', 'avatar upload', 'download a file'."
argument-hint: "[what is uploaded, by whom, and what it is attached to]"
license: MIT
metadata:
  version: "1.0.0"
---

# Add a file upload

Add or change the upload for `$ARGUMENTS` (what is uploaded, by whom, what it is attached to). If empty, ask: which files (kind, typical and maximum size), who uploads and who may read them, whether they may be created offline, and how long they are kept.

Uploads are where storage code multiplies (each feature writes its own), where privacy leaks hide (photo metadata carries location and device), and where data is lost quietly (a record saved without its files). This skill keeps one home for each part.

## 0. Read the project

1. `AGENTS.md`, the placement table (`engineering-principles` §3, lifecycle plugin): is there already **one upload reader** and **one storage port** with adapters? Reuse them; if a feature has its own storage class, that is a design finding to fix, not a pattern to copy.
2. The storage providers per environment (local disk or a container for development, an object store in production) and the configuration for each.
3. The client: web, mobile (offline? background upload? — `offline-queue`, `background-work`, mobile plugin).

**Gate:** you can name the upload reader, the storage port and its adapters, and the access unit that decides who may read a file.

## 1. Choose the transfer

| Option | Use when | Notes |
|---|---|---|
| **Multipart through the API** | Small files (≤ a few MB), simple clients | The upload reader streams to the storage port; never buffer whole files in memory |
| **Presigned direct upload** | Larger files, many uploads, mobile | The API issues a short-lived, single-object, size- and type-limited URL; the client uploads; the client (or a storage event) **confirms**; the server then validates the stored object |
| **Resumable / chunked** | Very large files or bad networks | Chunks with an upload id; the server assembles or the store supports it natively; expiry for abandoned uploads |

Record the choice (and the limits) in the spec; a change of transfer method is a `decision` (meta plugin).

## 2. Design

| Part | Rule |
|---|---|
| Reader | **One** upload reader at the edge: media type sniffed **from the bytes** (not the name or the declared type), size cap enforced with or without a declared length, an allowlist of types; handlers never read the raw body themselves |
| Storage | **One** storage port (`put`, `get`, `delete`, `presign`) with one adapter per provider, chosen by configuration and passing the same contract tests; the feature decides the object key layout in its use case, never its own storage class |
| Names | Random object keys (no user-supplied names in paths), outside the web root; the original filename, if needed, is metadata |
| Processing | Images re-encoded server-side (this also drops embedded scripts and malformed data); **metadata stripped** (EXIF location, device ids). Fields the product needs (capture time, a location as evidence) are kept only as **explicit, consented structured data** on the record — never left inside the file. Mobile clients strip on the device too, before upload |
| Reads | Through a member-checked endpoint or a short-lived signed URL issued after the access check; never a public bucket for personal files |
| Parent records | A record with attachments (a submission with photos) is **complete only when every attachment is confirmed**: a draft/pending state until then; the client-generated id of each attachment is its permanent idempotency key (`add-endpoint`, this plugin) |
| Failures | Oversize, wrong type or a failed scan is a **visible problem with a stable error code** — never a silent drop. A client queue never "drops the poison file" without telling the user |
| Cleanup | Orphans (uploaded, never confirmed; parent deleted) removed by a scheduled job (`add-scheduled-job`, this plugin) after a stated delay; account deletion deletes the files too |
| Scanning (optional) | For files other people download: a malware scan before the file becomes readable; "pending scan" is a state |
| Limits | Per-user rate and quota limits through the project's limiter row |

**Gate:** the design names the reader, the port, the transfer, the metadata rule, the completion rule and the cleanup — reviewed in `design-review` (lifecycle plugin), and `security-privacy-review` (quality plugin) for personal files.

## 3. Tests first

Through the real entry point and a real or containerised storage engine (an S3-compatible container counts as real; `testing-doctrine`, quality plugin):

- happy path: upload → confirm → the record is complete and the file is readable by an allowed caller;
- **forbidden callers**: a non-member gets not found on upload, confirm and read; a removed member loses read access immediately, including through previously issued signed URLs once they expire (keep them short);
- a file whose bytes do not match an allowed type → rejected with the code, even with a correct extension;
- oversize → a visible problem with the code, nothing stored;
- metadata: a test image with location metadata comes out without it;
- the same attachment sent twice (same client id) → one object, one row, the original answer;
- a parent with one attachment missing stays pending; it completes when the last one is confirmed;
- orphan cleanup removes only unconfirmed objects older than the delay.

## 4. Build and verify

Build per `backend-conventions` (this plugin): the reader and the storage adapters in their placement rows, the use case owning the object keys and the completion rule. Run the contract tests for every storage adapter. In the PR: the limits, the metadata rule, the access rule and the cleanup delay.

## Rules

- Never a per-feature storage class or a second upload reader.
- Never trust the filename or the declared type; never serve uploads from the web root.
- Never keep location or device metadata inside stored files; never drop a file silently.

## Composition

| From | This skill | To |
|---|---|---|
| `implement`, `spec`, `design-review` (lifecycle), `add-endpoint` | Upload reader, storage port use, completion and cleanup | `add-migration`, `add-scheduled-job` (this plugin); `security-privacy-review` (quality); `offline-queue` (mobile) |
