# Notification port

Read this when a scheduled or queued job sends email, SMS, push or webhooks. It sits on top of the durable-outbox model in the skill: the outbox item is the record of **intent**, the port is how one attempt reaches a provider, and the outbox state records what the provider actually confirmed.

## Shape

- **One notification port** (`send(notification) -> outcome`) with one adapter per provider, chosen by configuration and passing the same contract tests. Features never call a provider SDK directly.
- **The job is thin.** It loads ids, claims outbox items and calls **one** use-case method per item (`backend-conventions` §2). The use case decides *whether* and *what* to send; the adapter only delivers. No rule, preference check or template choice in the job or the adapter.
- The adapter returns an outcome the outbox can store: `accepted(provider_reference)`, `retryable(category, retry_after?)`, `permanent(category)` or `unknown` (timeout, connection lost after the request left). Never map `unknown` to success or to failure.
- The outbox item's operation id is passed as the provider's idempotency key when the provider supports one, so a retry of the same item cannot create a second message within the provider's idempotency horizon.

## Templates

- Templates live in **one place**, keyed by notification kind + language (+ channel), versioned with the code or the template store.
- Jobs and use cases pass a kind and typed parameters; no message text is assembled in a job, an adapter or a query.
- A missing template or parameter is a permanent, visible failure at render time (and a test), not an empty message.
- Personal data in a template is the minimum the message needs; the lock screen or preview text of a push carries less than the body.

## Preferences, consent and unsubscribe

- Check preferences, consent and unsubscribe **at send time**, inside the use case, after the claim — not only when the item was scheduled. A withdrawn consent or an unsubscribed address records the item as `cancelled` with the reason, distinct from delivered.
- Keep **transactional** kinds (receipts, security codes, safety alerts the user set up, account notices) apart from **marketing** kinds (digests of offers, newsletters). Each kind is declared as one or the other in one catalogue.
- Every non-essential (marketing) message carries an unsubscribe path that works without signing in and takes effect before the next send. Transactional kinds may not be unsubscribed from only where the law and the product allow; say so in the catalogue.
- Respect quiet hours and per-user rate limits in the use case when the spec asks for them; a deferred send gets a new `next_attempt_at`, not a dropped item.

## Provider failures

- Every provider call has a timeout shorter than the lease, so a slow provider cannot let a second worker claim the same item while the first is still waiting.
- Put a **circuit breaker** around the provider client: after a run of failures it opens, the adapter returns `retryable(provider_unavailable)` without calling, and items keep their place in the outbox. It closes after a probe succeeds. The breaker never drops or completes an item.
- Retries are owned by **one layer** (the outbox dispatcher, with bounded attempts, backoff with jitter and the provider's `retry_after` honoured). Disable or account for the provider SDK's own retries so they do not multiply.
- After the attempt budget is spent, the item becomes `failed` with a safe error category, an alert fires for kinds that matter, and an operator can requeue it. A fallback channel for critical messages exists only if the spec requires one, and it is a new outbox item with its own identity.
- An `unknown` outcome is reconciled with the provider (look up by idempotency key or provider reference) before it is retried without a key; when neither is possible, the item stays `uncertain` and is escalated for high-impact kinds.

## Observability

Metrics per notification kind and channel (no personal data, no ids as tags):

| Metric | Meaning |
|---|---|
| `due` | Items whose `next_attempt_at` has passed (backlog size) |
| `claimed` | Items leased by a worker |
| `sent` | Items the provider accepted (record the confirmed level: accepted, delivered) |
| `failed` | Items that exhausted retries or were permanently rejected, by error category |
| `uncertain` | Items whose outcome is unknown and awaiting reconciliation |
| `lag` | Time from due to the provider's acknowledgement (p50/p95/max), and the age of the oldest due item |

Alerts with an owner for: oldest due item older than the delivery objective, `failed` or `uncertain` above zero for a safety-relevant kind, breaker open longer than N minutes (`observe`, lifecycle plugin). Logs carry the operation id, kind and error category, never message bodies, addresses or phone numbers (`security-privacy-review`, quality plugin).

## Tests

With a recording fake of the port that can be told to accept, reject, time out or accept-then-lose-the-acknowledgement:

- one due item → one call through the port with the expected template and parameters;
- unsubscribed or consent withdrawn before run time → no call, item `cancelled` with the reason;
- marketing kind without an unsubscribe link → render fails the test;
- breaker open → no provider call, items still pending, sent after it closes;
- provider timeout → item `uncertain` or retried with the same idempotency key, never `sent`;
- retry budget exhausted → `failed`, metric and alert emitted, item requeueable.
