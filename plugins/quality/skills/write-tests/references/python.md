# Python tests

| Need | Typical choice |
|---|---|
| Framework | pytest (Django projects: pytest-django or the built-in runner — follow the project) |
| One test | `pytest tests/test_orders.py::test_rejects_more_than_50_lines` · `pytest -k "50_lines"` |
| Area / all | `pytest tests/orders` · `pytest` |
| Fake clock | Pass `now` / a clock object in; `time-machine` or `freezegun` only at the edge |
| Integration host | Django test client / `APIClient`; FastAPI `TestClient`; Flask `app.test_client()` |
| Database fixture | Real engine (Testcontainers or local services); a transaction or fresh schema per test (`pytest-django` `db` fixture, `--reuse-db` locally) |
| Parameterised | `@pytest.mark.parametrize` |
| Vendors | Recording fakes injected via settings/DI; `responses`/`respx` for recorded HTTP |
| Architecture tests | import-linter contracts; an `ast` import walker |

```python
import pytest
from shop.domain.orders import can_hold

@pytest.mark.parametrize("lines, expected", [(50, True), (51, False)])
def test_order_accepts_at_most_50_lines(lines, expected):
    assert can_hold(lines) is expected
```

- Query counting: `django_assert_num_queries(n)`; SQLAlchemy event listener counting `before_cursor_execute`.
- **After-commit work in Django tests:** `TestCase` wraps each test in a transaction that never commits, so `transaction.on_commit` callbacks (sending mail, queuing tasks) **never run** and a test can pass falsely. Use `with self.captureOnCommitCallbacks(execute=True):` (pytest-django: `django_capture_on_commit_callbacks`), or `TransactionTestCase` when you need real commits.
- **Email:** the locmem backend (the default in Django tests) records messages in `django.core.mail.outbox` — the recording sender; assert recipient, subject and count (including that a second run sent nothing).
- **Celery tasks:** call the task function directly (`send_reminder.run(chore_id)` or the plain function it wraps) with fakes for vendors; test idempotency by calling it twice. `task_always_eager` hides real behaviour (serialisation, retries, `acks_late` redelivery, transaction timing) — use it only for wiring tests, and cover redelivery explicitly.
- Run once with `TZ=Pacific/Auckland pytest` when time logic changes.
