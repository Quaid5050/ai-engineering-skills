# Flutter accessibility checks

Add to the screen's widget test:

```dart
final handle = tester.ensureSemantics();
await expectLater(tester, meetsGuideline(androidTapTargetGuideline));  // ≥ 48x48 dp
await expectLater(tester, meetsGuideline(iOSTapTargetGuideline));      // ≥ 44x44 pt
await expectLater(tester, meetsGuideline(labeledTapTargetGuideline));  // every tappable has a label
await expectLater(tester, meetsGuideline(textContrastGuideline));      // 4.5:1 text contrast
handle.dispose();
```

Text scale: pump inside `MediaQuery(data: MediaQueryData(textScaler: TextScaler.linear(2.0)), child: …)` and assert `tester.takeException()` is null.

- Labels: `Semantics(label: …)` or `tooltip` from `AppLocalizations`; `ExcludeSemantics` for decoration; `MergeSemantics` for list rows.
- Reduced motion: `MediaQuery.disableAnimationsOf(context)` stops `AnimationController`s.
- RTL: `EdgeInsetsDirectional`, `AlignmentDirectional`, `Directionality`.
- Announcements: `SemanticsService.announce(message, textDirection)`.
