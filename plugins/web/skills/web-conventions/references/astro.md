# Astro

Astro is zero-JS by default, which fits the generic rules closely.

## Where things live

```
src/
├── pages/                 # routes only: 3-line wrappers (`<Landing locale="en" />`), one per locale
├── layouts/               # Base.astro (head, CSP meta, fonts, header/footer), Prose.astro
├── components/
│   ├── Landing.astro      # composition: Base layout, section ORDER, JSON-LD, the one <script> import
│   ├── sections/          # one section per file
│   └── <Shared>.astro     # Header, Footer, Logo
├── i18n/                  # en.ts (source), other locales typed against it, index.ts (t(), locales)
├── scripts/               # site.ts entry calling init*(); a big behaviour gets its own file
└── styles/global.css      # @font-face + tokens (:root custom properties) + base styles
public/                    # fonts/, media/, favicon, robots.txt
scripts/                   # build guards and tests (Node, not shipped)
```

## Idioms

- Components declare `interface Props` in the frontmatter; `const { locale } = Astro.props`.
- The only `<script>` is the processed one in the composition component importing `site.ts`, so Astro bundles one module. Use `is:inline` only with understood processing/output semantics; safely serialize JSON-LD (including `<`) rather than interpolating untrusted content.
- `astro.config.mjs`: `output: 'static'`, `build.inlineStylesheets` as the project chose; processed small scripts may be automatically inlined; configure a supported hash/nonce CSP or verified external output. Stylesheet settings do not control JavaScript inlining.
- Images: `<Image>`/`<Picture>` from `astro:assets` for images in `src/`; pre-rendered media in `public/` carry `width`/`height`.
- SVG colours in `style` (`style="fill: var(--brand)"`), not presentation attributes.
- No UI framework islands (`client:*`) unless a decision record adds one.

## Tests and checks

- `astro check` (types, including locale dictionaries) + eslint.
- Node unit tests (`node --test scripts/*.test.mjs`) over `dist/`: no unexpected network requests, scripts allowed by the selected CSP (the emitted-script check below), actual deployed security headers, no hex in components, tokens mirrored from the source.
- Playwright on the built `dist/` (served statically) with axe.
- Commands: `npm run lint && npm test && npm run build && npm run e2e`.

## Emitted-script check

Astro may inline small processed scripts, so checking `src/` for `is:inline` is not enough: check what the build **emitted**. This test fails on a third-party script, an inline executable script whose hash the CSP does not list, or JSON-LD that is not safely serialized. It reads the CSP from `dist/_headers` (adapt `cspFromBuild()` if the project sets headers elsewhere, e.g. in the host config or a server middleware with nonces — then assert the nonce is present and per-response in the e2e run instead).

```js
// scripts/emitted-scripts.test.mjs — run after `npm run build`: node --test scripts/*.test.mjs
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const DIST = 'dist';
const htmlFiles = (dir) => readdirSync(dir, { withFileTypes: true }).flatMap((e) =>
  e.isDirectory() ? htmlFiles(join(dir, e.name)) : e.name.endsWith('.html') ? [join(dir, e.name)] : []);

function cspFromBuild() {
  const f = join(DIST, '_headers');
  if (!existsSync(f)) return '';
  const line = readFileSync(f, 'utf8').split('\n').find((l) => /Content-Security-Policy:/i.test(l));
  return line ?? '';
}

const SCRIPT = /<script\b([^>]*)>([\s\S]*?)<\/script>/gi;

test('emitted scripts are first-party and CSP-authorized', () => {
  const csp = cspFromBuild();
  const problems = [];
  for (const file of htmlFiles(DIST)) {
    const html = readFileSync(file, 'utf8');
    for (const [, attrs, body] of html.matchAll(SCRIPT)) {
      const src = attrs.match(/\bsrc\s*=\s*["']?([^"'\s>]+)/i)?.[1];
      const type = attrs.match(/\btype\s*=\s*["']?([^"'\s>]+)/i)?.[1] ?? '';
      if (src) {
        if (/^(https?:)?\/\//i.test(src)) problems.push(`${file}: third-party script ${src}`);
        continue;
      }
      if (type === 'application/ld+json') {
        if (body.includes('<')) problems.push(`${file}: JSON-LD not serialized safely (raw "<")`);
        continue;
      }
      if (!body.trim()) continue;
      const hash = `'sha256-${createHash('sha256').update(body, 'utf8').digest('base64')}'`;
      if (!csp.includes(hash)) problems.push(`${file}: inline script not in CSP: ${hash}`);
    }
  }
  assert.deepEqual(problems, []);
});
```

A shell first pass for local use (it reports; the test above is the gate):

```bash
# third-party script sources in the build output → must print nothing
grep -rhoE '<script[^>]*src="(https?:)?//[^"]+"' dist --include='*.html'
# inline executable scripts that the CSP must authorize by hash (or nonce)
grep -rlE '<script(\s+type="module")?\s*>' dist --include='*.html'
```

Also exercise the deployed CSP in a real browser (the e2e run): no CSP violation reports in the console on every page.

## Quick greps

```bash
grep -rn 'client:' src
grep -rn '#[0-9a-fA-F]\{3,6\}\b' src/components src/layouts src/pages
```
