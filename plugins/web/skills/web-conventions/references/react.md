# React (single-page apps) and Next.js

How the generic web rows map onto React. Most web **apps** are a client-rendered SPA (Vite + a router); content sites and hybrid apps often use Next.js. Pick the section that matches the project.

## 1. React SPA (Vite + React Router + TanStack Query)

| Generic | React SPA |
|---|---|
| Routes (thin) | Route objects in `src/app/router.tsx` (`createBrowserRouter`), lazy-loaded per feature (`lazy: () => import(...)`) |
| Feature folders | `src/features/<feature>/{screens,components,hooks,data}` |
| Screen | `screens/<Screen>.tsx`: renders state, calls hook actions |
| View model | `hooks/use<Screen>.ts`: combines queries/mutations, exposes state + actions |
| Repository / data | `data/<thing>Repository.ts`: wraps the generated client, maps API models and problem codes; exports query keys and `queryOptions` |
| Generated client | `src/api/generated/` from the contract with **openapi-typescript + openapi-fetch**, or **orval** (can also emit TanStack Query hooks — if used, keep them inside `data/`); regenerate, never edit |
| Server-state cache | TanStack Query: one `QueryClient`; query keys per resource (`['orders', id]`); mutations `invalidateQueries` the affected keys; `retry` off for 4xx |
| Shared code | `src/shared/{components,lib}` with an import rule (eslint `no-restricted-imports` or dependency-cruiser): never imports `src/features/*` |
| Copy | `src/i18n/<locale>.ts` typed from the source locale, or react-i18next / FormatJS |
| Tokens | CSS custom properties in `src/styles/tokens.css` (Tailwind theme may read them) |
| Config | `import.meta.env.VITE_*`, parsed once with a schema (zod) at start; nothing secret — everything in the bundle is public |

### Idioms

- Forms: React Hook Form + a zod schema whose limits come from the contract (or generated from it); map the server's problem `errors` onto `setError(field)`.
- Auth: the server sets an httpOnly, Secure, SameSite cookie; the client sends `credentials: 'include'`; CSRF via a double-submit token header or SameSite=Strict plus an origin check on the server. One fetch middleware handles 401 (redirect to sign-in), 403 and 404 (a typed error the screen maps to a state).
- Errors: a typed `ApiProblem { code, fields? }` thrown by the repository; screens `switch` on `code`.
- Optimistic updates with `onMutate`/rollback only for reversible actions.
- Accessibility lint: `eslint-plugin-jsx-a11y`; focus management on route change.

### Tests

- Vitest + React Testing Library (query by role and name); **MSW** (Mock Service Worker) for HTTP at the network boundary with recorded responses — the same handlers in unit tests and in the browser during development.
- E2E: Playwright against `vite build && vite preview` (the built output) with `@axe-core/playwright`; seed a test backend or replay recorded API responses.
- Commands: `npm run lint && npm run typecheck && npx vitest run && npm run build && npx playwright test`.

## 2. Next.js (App Router)

| Generic | Next.js |
|---|---|
| Routes (thin) | `app/[locale]/<route>/page.tsx`: load data/dictionary, render one screen or composition component |
| Layouts | `app/[locale]/layout.tsx` (fonts via `next/font/local`, `<html lang dir>`); metadata via `generateMetadata` |
| Sections / screens | `components/sections/<Name>.tsx` (content), `features/<feature>/...` (app) — Server Components by default |
| Client behaviour | Only leaf components with `"use client"`; never on a section or layout |
| Data | Server Components call the repository; client-side server state via TanStack Query where interactive; Server Actions are edges: validate, call one use case on the API, map errors |
| Headers / CSP | `next.config.js` `headers()` or middleware with a nonce for the scripts Next.js injects |
| Images | `next/image` with `width`/`height`, `sizes`, `alt` |

- `next/font/google` downloads at build time and self-hosts for visitors. Use local font files when the build must also avoid external requests; distinguish build and browser network policies.
- Avoid raw HTML interpolation. JSON-LD also needs safe serialization, including escaping `<` so untrusted text cannot terminate the script element. Test hostile strings; apply a framework-compatible nonce/hash CSP.
- E2E: Playwright against `next build && next start`. Build-output checks: a Node script over `.next/` or `out/`.

## Quick greps

```bash
grep -rn "from '.*api/generated" src --include='*.ts*' | grep -v '/data/'      # generated client outside the data layer
grep -rn 'localStorage.*[Tt]oken' src                                          # tokens in script-readable storage
grep -rn '#[0-9a-fA-F]\{3,6\}\b' src --include='*.tsx' --include='*.css' | grep -v tokens.css
grep -rn 'dangerouslySetInnerHTML' src app components 2>/dev/null | grep -v ld+json
```
