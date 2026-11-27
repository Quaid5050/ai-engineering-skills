# Additional web adapters

Choose the installed framework version and rendering mode first; the shared conventions do not require a client query library or repository wrapper in every server-rendered app.

| Ecosystem | Implementation decisions | Verification |
|---|---|---|
| Vue / Nuxt | Keep reusable state in composables; do not share request-specific reactive state across SSR users. Use framework server routes/loaders for privileged access; client checks do not authorize writes. | Render two principals in isolation, hydration warnings, logout cache clearing, route errors and form accessibility. See [Vue SSR security](https://vuejs.org/guide/scaling-up/ssr.html) and [Nuxt data fetching](https://nuxt.com/docs/guide/concepts/data-fetching). |
| Angular | Choose signals for local derived state and streams for asynchronous event/cancellation semantics. Use the configured HTTP/interceptor layer, dispose subscriptions, and treat route guards as UX rather than server authorization. Avoid bypassing sanitization for untrusted HTML. | Component/service tests plus real browser navigation, unauthorized API calls, SSR request isolation and keyboard focus. See [Angular security](https://angular.dev/best-practices/security). |
| Svelte / SvelteKit | Keep secrets in server-only modules; use server load/actions for authorized mutations. Never put per-user mutable state in a shared server module. Model action failures without destroying valid form input. | Concurrent-user SSR isolation, invalid/forbidden action tests, no secret in client bundle, navigation cancellation and hydration. See [SvelteKit state management](https://svelte.dev/docs/kit/state-management). |
| React / Next.js | Server-rendered reads may call server-owned data modules directly; client bundles cannot import them. Client caches include user/tenant/query identity and clear on auth changes. | Keep the [React adapter](react.md) scoped to the project's router/render mode; test output CSP and serialized data. |

Cross-framework checks: semantic HTML, labels, keyboard/focus, reduced motion, locale/timezones, browser support, bounded bundle/request budgets, safe error states, authorization at the server, nonce/hash CSP and cache partitioning. Choose existing framework capabilities before adding a library; add one for a demonstrated gap, not stack uniformity.
