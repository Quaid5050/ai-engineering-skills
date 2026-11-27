# Tool-agent reference

Use [OWASP excessive agency](https://genai.owasp.org/llm2026/llm032026-excessive-agency/) to model authority and [tool misuse](https://genai.owasp.org/agentic-applications-2026/asi02-tool-misuse-and-exploitation/) for delegated/tool threats.

A tool contract records input schema, permissions, resource ownership, output schema, idempotency/reconciliation behavior, side effects, timeouts and safe audit fields. Application authorization executes outside the model. Store opaque approval tokens bound to a server-side action digest; a string saying approved is not sufficient.

Test a two-step booking workflow with a read-only availability tool and a scoped booking tool. Interrupt after provider acceptance, resume and prove reconciliation. Invalid approval, a different tenant or changed booking details must be denied.
