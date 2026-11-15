# Flutter / Dart tests

| Need | Typical choice |
|---|---|
| Framework | `flutter_test` (widget + unit), `integration_test` for device flows |
| One test | `flutter test test/orders/order_limit_test.dart --plain-name "accepts at most 50 lines"` |
| Area / all | `flutter test test/orders` · `flutter analyze && flutter test` |
| Fake clock | An injectable clock provider overridden with a fixed clock; widget tests: `tester.pump(duration)` (the binding fakes time); `fake_async` for pure timer logic |
| Dependency overrides | Riverpod `ProviderScope(overrides: [...])` / `ProviderContainer`; other DI: constructor injection |
| Repository fakes | In-memory implementations of the repository interface in `test/support/` |
| Transport fakes | A fake HTTP adapter returning recorded responses |
| Goldens | `matchesGoldenFile(...)`; update with `--update-goldens` only for intended changes |
| Accessibility | `meetsGuideline(androidTapTargetGuideline)`, `labeledTapTargetGuideline`, `textContrastGuideline` |
| Architecture tests | A test that reads `lib/` import lines against an allowlist |
| Local database | Drift: `NativeDatabase.memory()` per test (the real SQL engine, no file); migration tests with `drift_dev`'s schema verifier and dumped old schemas |
| Native dialogs (permissions, notifications) | `patrol` (or `integration_test` + platform tools) on an emulator/simulator — `flutter_test` cannot tap OS dialogs |
| Background work | Test the Dart task body as a plain function with fakes; the `workmanager` callback only wires it — check scheduling on a device (`device-test`, mobile plugin) |

```dart
testWidgets('shows the out-of-stock label when quantity is zero', (tester) async {
  await tester.pumpWidget(ProviderScope(
    overrides: [stockRepositoryProvider.overrideWithValue(InMemoryStock({'sku-1': 0}))],
    child: const MaterialApp(
      localizationsDelegates: AppLocalizations.localizationsDelegates,
      supportedLocales: AppLocalizations.supportedLocales,
      home: ProductCard(sku: 'sku-1'),
    ),
  ));

  final l10n = await AppLocalizations.delegate.load(const Locale('en'));
  expect(find.text(l10n.outOfStock), findsOneWidget);   // the string comes from the .arb file, never a literal in the widget
});
```

The expected text may also be the hard-coded English literal (`'Out of stock'`) when the test pins the English copy on purpose; what must never happen is a literal inside the widget.

- `pumpAndSettle` never settles with an endless animation: disable animations (`MediaQueryData(disableAnimations: true)`) or `pump(duration)`.
- Wrap screens with the real localizations delegates so strings come from the translation files.
