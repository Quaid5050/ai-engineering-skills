# Mobile accessibility (Android and iOS)

| Need | Android | iOS |
|---|---|---|
| Screen reader | TalkBack | VoiceOver |
| Labels | `contentDescription`; Compose `Modifier.semantics { contentDescription = … }` | `accessibilityLabel`, `accessibilityValue`, `accessibilityHint` |
| Grouping | `mergeDescendants`, `importantForAccessibility` | `accessibilityElements`, `.accessibilityElement(children: .combine)` |
| Hide decoration | `importantForAccessibility="no"` / `invisibleToUser()` | `isAccessibilityElement = false`, `.accessibilityHidden(true)` |
| Announce | `announceForAccessibility`, live regions | `UIAccessibility.post(notification: .announcement, …)` |
| Text size | `sp` units; test at font scale 2.0 | Dynamic Type; test at the largest accessibility size |
| Reduced motion | `Settings.Global.ANIMATOR_DURATION_SCALE`, "Remove animations" | `UIAccessibility.isReduceMotionEnabled` |
| Targets | ≥ 48×48 dp | ≥ 44×44 pt |
| Automated | Accessibility Scanner, Espresso `AccessibilityChecks.enable()` | Xcode Accessibility Inspector audit, `XCUIApplication().performAccessibilityAudit()` |

React Native: `accessibilityLabel`, `accessibilityRole`, `accessibilityState`, `AccessibilityInfo.announceForAccessibility`, `AccessibilityInfo.isReduceMotionEnabled()`; test with `@testing-library/react-native` `getByRole`/`getByLabelText`.
