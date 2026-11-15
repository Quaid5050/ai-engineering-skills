# Web accessibility tools

- **axe-core** in end-to-end tests: `@axe-core/playwright` (`new AxeBuilder({ page }).analyze()`, assert `violations` is empty) or `jest-axe` / `vitest-axe` for component tests.
- **Testing Library** queries by role and accessible name (`getByRole('button', { name: 'Add to cart' })`) — a test that cannot find the element by role found an accessibility bug.
- **Lighthouse** accessibility score in CI (`lhci autorun`), plus manual checks: it covers only part of WCAG.
- Semantics: one `<h1>` per page, headings in order, landmarks (`header`, `nav` with `aria-label`, `main`, `footer`), real `<a>`/`<button>`, `<label for>` on every input, `alt` on images (`alt=""` when decorative).
- Focus: `:focus-visible` outline ≥ 3:1 against its background; no `outline: none` without a replacement; `inert` or focus trapping only inside open modals.
- Motion: `@media (prefers-reduced-motion: reduce)` for every CSS and JS animation.
- Text: `rem` units, no fixed heights on text containers, reflow at 320 px.
- RTL: `dir` and `lang` on `<html>`; logical properties (`margin-inline-start`, `inset-inline-end`).
- Screen readers to try: NVDA or JAWS (Windows), VoiceOver (macOS/iOS), TalkBack (Android Chrome).
