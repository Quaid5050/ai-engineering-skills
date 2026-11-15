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
- The only `<script>` is the processed one in the composition component importing `site.ts`, so Astro bundles one module. **No `is:inline`** except JSON-LD (`<script type="application/ld+json" set:html={...} />`).
- `astro.config.mjs`: `output: 'static'`, `build.inlineStylesheets` as the project chose; scripts never inlined (CSP `script-src 'self'`).
- Images: `<Image>`/`<Picture>` from `astro:assets` for images in `src/`; pre-rendered media in `public/` carry `width`/`height`.
- SVG colours in `style` (`style="fill: var(--brand)"`), not presentation attributes.
- No UI framework islands (`client:*`) unless a decision record adds one.

## Tests and checks

- `astro check` (types, including locale dictionaries) + eslint.
- Node unit tests (`node --test scripts/*.test.mjs`) over `dist/`: no third-party URLs, no inline scripts, headers file, no hex in components, tokens mirrored from the source.
- Playwright on the built `dist/` (served statically) with axe.
- Commands: `npm run lint && npm test && npm run build && npm run e2e`.

## Quick greps

```bash
grep -rn 'is:inline' src | grep -v 'ld+json'
grep -rn 'client:' src
grep -rn '#[0-9a-fA-F]\{3,6\}\b' src/components src/layouts src/pages
```
