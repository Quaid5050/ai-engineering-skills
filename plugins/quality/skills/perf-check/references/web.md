# Web performance tools

- **Core Web Vitals** budgets: LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1 at the 75th percentile, on throttled mobile.
- **Lighthouse CI** (`@lhci/cli`): `lhci autorun` with assertions (`categories:performance >= 0.9`, `largest-contentful-paint <= 2500`); run against the built site, 3+ runs (`numberOfRuns: 3`), median.
- **Bundle size:** `size-limit` or the bundler's analyzer (`vite-bundle-visualizer`, `webpack-bundle-analyzer`, `next build` output); a CI limit per entry point; a PR that adds JS or blocking CSS states the size change.
- **Profiling:** Chrome DevTools Performance panel with CPU 4× slowdown; the Coverage tab for unused JS/CSS.
- **Field data:** the `web-vitals` library reporting to first-party analytics (no personal data).
- Common fixes: images sized and lazy-loaded with width/height, fonts self-hosted with `font-display: swap` and preloaded, no render-blocking third-party scripts, ship less JavaScript (server-render, islands, `<details>` instead of JS toggles).
