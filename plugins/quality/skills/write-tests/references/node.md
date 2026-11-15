# Node / TypeScript tests

| Need | Typical choice |
|---|---|
| Framework | Vitest or Jest (follow the project); Node's built-in `node:test` for small packages |
| One test | `npx vitest run src/orders.test.ts -t "accepts at most 50 lines"` · `npx jest src/orders.test.ts -t "..."` |
| Area / all | `npx vitest run src/orders` · `npm test` |
| Fake clock | Inject a `clock` / `now()`; `vi.useFakeTimers()` / `jest.useFakeTimers()` only for timer scheduling |
| Integration host | `supertest` against the app instance (Express/Fastify/Nest `createTestingModule`) |
| Database fixture | Real engine via Testcontainers or local services; migrate a fresh schema per file; truncate per test |
| Parameterised | `it.each` / `test.each` |
| Vendors | Recording fakes behind ports; `msw` or `nock` for recorded HTTP |
| UI | Testing Library (`render`, `screen.getByRole`), Playwright for end to end |
| Architecture tests | dependency-cruiser, eslint `no-restricted-imports` |

```ts
import { describe, it, expect } from "vitest";
import { canHold } from "./orders";

describe("order limits", () => {
  it.each([[50, true], [51, false]])("holding %i lines → %s", (lines, expected) => {
    expect(canHold(lines)).toBe(expected);
  });
});
```

- Prefer `getByRole` with the accessible name over test ids: it tests accessibility too.
- **UI against the API:** Mock Service Worker (`msw`) intercepts requests at the network layer, so the real data-fetching code (client, cache, retries) runs; define handlers from recorded or contract-shaped responses, including the error responses (401, 403, 404 with problem codes) and slow responses for loading states.

```ts
import { http, HttpResponse } from "msw";
import { setupServer } from "msw/node";
const server = setupServer(
  http.get("/api/orders/:id", () => HttpResponse.json({ type: "about:blank", code: "order_not_found" }, { status: 404 })),
);
beforeAll(() => server.listen({ onUnhandledRequest: "error" }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```
