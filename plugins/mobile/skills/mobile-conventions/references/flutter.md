# Flutter mapping

| Concept | Flutter |
|---|---|
| View | `StatelessWidget`/`ConsumerWidget` screen in `features/<f>/presentation/<screen>_screen.dart`; parts as widget **classes** in `presentation/widgets/` (no `Widget _buildX()` helper methods) |
| View model | Riverpod `Notifier`/`AsyncNotifier` in `presentation/<screen>_view_model.dart`; no `material.dart`/`BuildContext` import |
| Domain | `domain/`: immutable models (`final` fields, `==`/`copyWith` or freezed), `sealed class` results, repository `abstract interface class` |
| Repository | `data/api_<thing>_repository.dart`, exposed by a top-level provider typed as the domain interface |
| Coordinator | `data/<thing>_coordinator.dart`, started by a provider that lives as long as the session |
| Service | generated OpenAPI client (`lib/api/`), Pigeon bindings (`lib/native/`), plugin wrappers in `data/` |
| Shared module | `lib/shared/{domain,data,presentation}/` |
| Feature handle | `data/<feature>_providers.dart` containing only `export '…' show …;` |
| Strings | ARB files + `flutter gen-l10n`; `AppLocalizations.of(context)` |
| Theme | one `theme.dart` (`AppColors`, text styles); a test fails on `Color(0x…)` elsewhere |
| Local DB | Drift (tables/DAOs in a database service; versioned migrations with `SchemaVerifier` tests) |

## Riverpod rules

- Providers are top-level `final`, one per name, typed as interfaces; never in `fake_*` files.
- `ref.watch` in `build`, `ref.read` in callbacks; `ref.watch(p.select((s) => s.field))` to narrow rebuilds.
- No legacy `StateNotifier`/`StateProvider`/`ChangeNotifierProvider` in new code.
- Tests override providers with in-memory fakes (`ProviderContainer(overrides: […])`, disposed with `addTearDown`).

## Performance

- `const` constructors; `ListView.builder` with keys; `Isolate.run`/`compute` for heavy work; `RepaintBoundary` around animated parts; `FadeTransition` instead of `Opacity`; `cacheWidth`/`cacheHeight` on images.
- Animations check `MediaQuery.disableAnimationsOf(context)`.
- Measure with `flutter run --profile` + DevTools, `--trace-startup`, `integration_test` `traceAction`.

## Directional layout

`EdgeInsetsDirectional`, `AlignmentDirectional`, `PositionedDirectional`; a test can fail on non-directional insets that differ left/right.

## Architecture test

A plain `test/architecture/layering_test.dart` that walks `lib/`, parses `import` lines and checks them against allowlists per folder (domain, view model, shared, shell), plus a file-size check for `presentation/`.

## Analyzer

Enable Effective Dart lints such as `avoid_catches_without_on_clauses`, `prefer_final_fields`, `directives_ordering`; `flutter analyze` must print `No issues found!`.

## Files, media and offline data

- **Where queued files live:** `path_provider` → `getApplicationSupportDirectory()` (app-private, not visible to the user); on iOS exclude the folder from iCloud backup (`NSURLIsExcludedFromBackupKey` via a small platform call or a plugin) and use file protection (`NSFileProtectionComplete` or `…UntilFirstUserAuthentication` when background uploads must read the file while locked); on Android, app-specific internal storage is already excluded from backup if `android:allowBackup`/`dataExtractionRules` exclude it — set them explicitly. Never `getTemporaryDirectory()` for data that must survive: the OS may clear it.
- **Encryption at rest** for sensitive queued data: an encrypted database (SQLCipher-backed) or encrypted files with the key in `flutter_secure_storage` (keychain / keystore).
- **Local database:** Drift (SQLite) — tables, DAOs and versioned migrations in a database service; the repository stays the single source of truth; migration tests with the schema verifier. One connection per isolate (background isolates open their own, or use `DriftIsolate`).
- **Camera and photos:** `image_picker` or `camera`; permissions via `permission_handler`. iOS: `NSCameraUsageDescription`, `NSPhotoLibraryUsageDescription` and **limited photo access** (the user picks some photos — handle it and offer `presentLimitedLibraryPicker`); Android 13+: the system photo picker needs no storage permission.
- **Compression and metadata:** `flutter_image_compress` (re-encode to the agreed size; by default it drops EXIF — verify with a test on a photo that carries GPS tags), or the `image` package in an isolate. Read any field the product needs (capture time) **before** stripping and store it as structured data.
- Large uploads: from the file on disk, never `readAsBytes()` of a whole video into memory.
