---
name: analytics-event
description: "Add or change a product analytics event, or answer a product question from events, without collecting personal data — first-party pipeline preferred, the product question first, object_action names, allow-listed properties only (never location, free text, contact details or raw user ids), pseudonymous ids hashed server-side with a secret, consent honoured, the event catalogue as the single source of truth, tests that the exact event is sent and nothing is recorded when analytics is off, cohort queries for questions. Use when someone wants to measure usage. Trigger on /analytics-event, 'track this', 'add an analytics event', 'measure adoption of', 'how many people use', 'funnel for', 'retention of'."
argument-hint: "[add <what to measure> | a product question]"
license: MIT
metadata:
  version: "1.1.0"
---

# Analytics event

`$ARGUMENTS` is either `add <what to measure>` or a **question** ("how many new shops added a product in week 1?"). If empty, ask which. Product analytics answer "do people use it?"; system health is `observe` (lifecycle plugin).

## 0. Read the project

1. Read `AGENTS.md` / `CLAUDE.md` and any analytics decision record: is the pipeline first-party or a vendor? Where is the **event catalogue** (for example `docs/analytics/events.md`)?
2. Find the client analytics API, the transport, the storage table and the consent setting.
3. No pipeline yet → building it is its own slice (`file-feature`, lifecycle plugin): catalogue, typed client API with batching and opt-out, an ingest endpoint, a storage table, a chart source. Prefer **first-party** (client → your API → your database → your charts); a third-party SDK needs a decision record (`decision`, meta plugin) and the user's decision.

## 1. The shape

| Part | Rule |
|---|---|
| Catalogue | Single source of truth: every event, its properties, the question it answers, its owner. An event not in the catalogue is not sent. |
| Client API | Typed events (`analytics.track(ProductAdded(category: "books"))`), no free-form maps from feature code. |
| Transport | Queued offline, sent in batches, dropped after N days; never blocks the UI or a safety-critical path. |
| Storage | `time`, `name`, pseudonymous user/tenant ids, platform, app version, properties. Retention stated (e.g. 13 months); account deletion deletes the person's rows. |
| Pseudonymous ids | The **server** computes `HMAC-SHA256(server secret, id)` — stable so events join each other, not joinable to user tables without the secret. The secret has its own configuration entry (one owner per purpose). |

## 2. Add an event

1. **Is it needed?** Write the product question it answers. No question → no event.
2. **Name:** `object_action`, snake_case, past tense: `product_added`, `order_placed`, `checkout_abandoned`, `onboarding_step_completed`. Reuse an existing event with a property before adding a near-duplicate.
3. **Properties — allow-list only:**
   - Allowed: enums (`category: books|games|other`, `platform`, `trigger: button|shortcut|widget`), counts, durations in seconds, booleans, app version, step names.
   - **Never:** location or distances, addresses or place names, contact details, names, message or note text, search text, photos, device or network identifiers, raw user or tenant ids (hash them in the transport), tokens, health or payment data.
4. **Consent:** honour the in-app analytics setting. Off → nothing is queued. Every feature works identically either way.
5. **Catalogue:** add the row in the same change.
6. **Test:** a test with a fake analytics sink asserting the exact event name and properties after the user action, and that **nothing is recorded when analytics is off**. A catalogue test keeps the typed events and the catalogue in sync.
7. **Review:** `security-privacy-review` §5 for any new property.

**Gate:** the question, the catalogue row and both tests exist before the event ships.

## 3. Answer a question

1. Turn it into a precise definition: population, time window, events, what counts as "active".
2. Check the events exist in the catalogue (a cohort question needs a start event). Missing → add them first; the answer only covers time after they shipped.
3. Query read-only (`data-check`, backend plugin). Example — share of new shops that added a product within 7 days:
   ```sql
   WITH cohort AS (
     SELECT shop_hash, min(time) AS created_at
     FROM analytics_events WHERE name = 'shop_created'
       AND time >= now() - interval '8 weeks' AND time < now() - interval '7 days'
     GROUP BY shop_hash
   )
   SELECT date_trunc('week', c.created_at) AS cohort_week,
          count(*) AS new_shops,
          count(*) FILTER (WHERE EXISTS (
            SELECT 1 FROM analytics_events e
            WHERE e.shop_hash = c.shop_hash AND e.name = 'product_added'
              AND e.time < c.created_at + interval '7 days')) AS added_in_week_1
   FROM cohort c GROUP BY 1 ORDER BY 1;
   ```
4. Report numbers with the definition, the window and caveats (opt-outs, versions without the event). Do not over-read small samples.
5. If the question will be asked again, save the query as a chart and link it from the catalogue row.

## Rules

- No personal data in events — when in doubt, leave it out.
- Analytics never delays or blocks a safety-critical path.
- A third-party analytics SDK needs a decision record and the user's decision.

## Composition

| From | This skill | To |
|---|---|---|
| `spec` (lifecycle plugin, analytics section), a product question | Event in the catalogue + tests, or a defined answer | `security-privacy-review` for new properties; `data-check` (backend) for queries; `observe` (lifecycle) for system health |
