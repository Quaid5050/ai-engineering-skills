# React Native mapping

| Concept | React Native (TypeScript) |
|---|---|
| View | Function components in `src/features/<f>/presentation/`; small components, no data fetching inside |
| View model | A custom hook per screen (`useListScreenModel()`) or a store slice (Zustand / Redux Toolkit) exposing immutable state + action functions; no JSX, no navigation object inside |
| Domain | `domain/`: plain types, discriminated unions for results (`{ kind: 'ok' } | { kind: 'notFound' }`), repository interfaces, pure functions |
| Repository | `data/apiListRepository.ts` implementing the domain interface; injected through a context or a module-level container, replaced in tests |
| Server cache | TanStack Query can be the repository's cache; keep query keys and fetchers inside `data/`, expose domain types only |
| Coordinator | A module started once per session (AppState listener, NetInfo listener) calling repositories |
| Service | generated OpenAPI client, Turbo/Native Modules or Expo modules wrappers in `data/` |
| Shared module | `src/shared/` with an eslint rule that it imports no `src/features/**` |
| Feature handle | `features/<f>/index.ts` re-exporting the public API only |
| Strings | i18next / FormatJS message files; ICU plurals |
| Theme | one `theme.ts`; eslint `no-restricted-syntax` against colour literals in components |
| Local DB | WatermelonDB, op-sqlite or expo-sqlite behind a database service with versioned migrations |

## Enforcement

- `eslint-plugin-boundaries` or `dependency-cruiser` rules: presentation → view model → data → domain; features only via `index.ts`; no cycles (`no-circular`).
- `@typescript-eslint/switch-exhaustiveness-check` on result unions.

## Performance

- `FlatList`/`FlashList` with `keyExtractor`; `React.memo` and narrow selectors (`useStore(s => s.field)`); `useMemo` for derived lists computed in the view model, not in render.
- Animations with Reanimated on the UI thread; respect `AccessibilityInfo.isReduceMotionEnabled()`.
- Images sized (`expo-image`/`FastImage` with explicit dimensions).
- Measure in a release build: the diagnostics supported by the installed React Native version (verify React Native DevTools/React profiling and any separately supported Flipper integration), `react-native-performance`, Hermes sampling profiler.

## RTL

Use `start`/`end` (`marginStart`, `paddingEnd`) and `I18nManager.isRTL`; never `left`/`right` for layout.
