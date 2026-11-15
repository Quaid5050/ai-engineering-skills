# Python: Django (and Django REST Framework)

How the generic rows map onto Django. Django's "fat models" habit conflicts with the concept test only when models grow technical code; keep business rules on models or in plain domain modules, and use cases in services.

## Modules (per app = per feature area)

| Generic | Django |
|---|---|
| Domain | `<area>/domain.py` (plain classes, dataclasses, pure functions, constants) — no `django.*` imports. Simple invariants may sit on the model's methods if the project chose that; say so in the conventions |
| Persistence | `<area>/models.py` (ORM models = mapping), `<area>/queries.py` (reusable `QuerySet` methods / custom managers), `migrations/` |
| Application | `<area>/services.py`: one function or class method per use case; ports in `<project>/ports.py` (Protocols) |
| Edge | `<area>/views.py` (or DRF `viewsets.py`), `<area>/serializers.py` = request/response shapes + shape validation, `urls.py` |
| Access unit | `<area>/access.py`: one function per resource kind (`require_member(user_id, household_id)` → not found / forbidden); DRF `permission_classes` / `has_object_permission` only *call* it, so the rule has one home |
| Adapters | `<project>/adapters/<vendor>.py` implementing the Protocols |
| Workers | Celery tasks / django-q / RQ in `<area>/tasks.py`, thin: call a service |

## Idioms

- Views stay thin: deserialize + `is_valid()`, call one service with `request.user.id`, map the result. No `Model.objects` calls in views (an import-linter contract can enforce it).
- **Serializers: plain `Serializer` classes** for request/response shapes, not `ModelSerializer` with `.save()` (that puts writes at the edge). DRF generic views with `queryset=` do data access at the edge: use `APIView`/`ViewSet` methods that call services instead. If the project deliberately allows `ModelSerializer` for read-only responses, record it in a decision record and name that exception in the architecture test's allowlist.
- Authorisation: the service calls the access unit; `has_object_permission` may delegate to it but never holds its own copy of the rule. Never cache a permission result across requests.
- Errors: a small `Result`/`Error` type in services; one exception handler (DRF `EXCEPTION_HANDLER`) renders RFC 9457 problems (`application/problem+json`). `get_object_or_404` only inside the access unit, so non-members get 404.
- Reads: `.only()` / `.values()` / annotations; `select_related` (FK) and `prefetch_related` (collections) to avoid N+1; `.exists()` not `.count() > 0`; `.iterator()` for big scans.
- Bulk: `bulk_create`, `bulk_update`, `QuerySet.update()` (bypasses `save()` and signals — say so).
- Transactions: `with transaction.atomic():` in the service; `select_for_update()` for row locks; `pg_advisory_xact_lock` via `connection.cursor()` for invariants; `transaction.on_commit(lambda: notify(...))` for after-commit notices. Avoid `ATOMIC_REQUESTS` hiding where the transaction is.
- Time: inject a clock (a callable passed in) instead of `timezone.now()` inside rules; tests use `freezegun` or `time-machine` only at the boundary. `USE_TZ = True`.
- Settings: typed settings via `pydantic-settings` or `django-environ`, validated at import; one setting per secret purpose; no `os.environ` reads outside settings.
- Signals: avoid for business flow (hidden control flow); explicit calls instead.
- Logging: `logger.info("Order %s shipped", order_id)` (lazy args), never f-strings with personal data.
- Resilience: `httpx` with explicit timeouts; `tenacity` for idempotent reads only; sends retried only by the task (`autoretry_for` + idempotency key), never the client.
- Django is synchronous by default: keep request work short, put long or outbound work in a task; if the project uses async views, use the async ORM methods consistently and never call sync I/O from them.

## Tasks and scheduling (Celery; RQ/django-q are similar)

- Queue tasks **after commit**: `transaction.on_commit(lambda: send_reminder.delay(chore_id))` — a task enqueued inside the transaction can run before the row is visible, or for a rolled-back row.
- **Exactly one beat (scheduler) process** in every environment, including during deploys (a rolling deploy can briefly run two: use a lock such as `django-celery-beat` + a single replica, or a scheduler lock). Duplicate sends usually start here.
- `acks_late=True` + the broker's visibility timeout means a task can run **twice** (worker killed, timeout shorter than the task): every task is idempotent.
- Claim due rows in the task: `Chore.objects.select_for_update(skip_locked=True).filter(due_at__lte=now, reminded_at__isnull=True)[:100]` inside `transaction.atomic()`.
- A **sent-ledger** row with a unique constraint (`UniqueConstraint(fields=["chore", "due_at"], name="uq_reminder_sent")`) is the dedupe: insert it before sending; `IntegrityError` → already sent, skip.
- Re-check membership in the task at run time, not only when the job was scheduled.
- Details and tests: `add-scheduled-job`.

## Contract-first with a code-first framework

Generate the schema (`python manage.py spectacular --file /tmp/schema.yaml --validate` with drf-spectacular) and **diff it against the contract file** in a test or CI step; drift fails the build. Annotate views (`@extend_schema`) so operation ids and error responses match the contract.

## Tests and tools

- pytest + pytest-django; `@pytest.mark.django_db`; real database (the compose file or testcontainers), not SQLite, when the production database differs.
- Query count guard: `django_assert_num_queries(n)` (pytest-django) or `assertNumQueries`.
- Architecture tests: import-linter contracts (`layers`, `forbidden`, `independence`), plus a pytest over `ast` imports for the domain allowlist.
- Models: a Django model is both mapping and (often) the entity. Decide once (decision record): either rules live on the model's methods (domain allowlist then includes the model module's pure methods), or plain domain classes are mapped from models in the persistence layer.
- Migrations: `python manage.py makemigrations`; review `python manage.py sqlmigrate <app> <n>`; `AddIndexConcurrently` (`django.contrib.postgres.operations`) with `atomic = False`; data backfills in a task, not a migration.
- Commands: `ruff check . && ruff format --check . && mypy . && pytest` (mypy needs `django-stubs` and `djangorestframework-stubs` with the mypy plugin configured).
- After-commit hooks in tests: `TestCase` never commits, so `on_commit` callbacks do not run — use `captureOnCommitCallbacks(execute=True)` / the `django_capture_on_commit_callbacks` fixture, or the test silently skips the notification.
- Recording sender for email: the locmem backend and `django.core.mail.outbox`.

## Quick greps

```bash
grep -rn 'objects\.' */views.py */viewsets.py
grep -rn 'timezone.now()\|datetime.now()' */domain.py */services.py
grep -rn 'except Exception' --include='*.py' .
grep -rn 'os.environ' --include='*.py' . | grep -v settings
```
