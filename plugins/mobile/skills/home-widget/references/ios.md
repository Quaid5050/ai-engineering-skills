# iOS widgets and live activities

- **WidgetKit** extension target (SwiftUI + `TimelineProvider`/`AppIntentTimelineProvider`), sharing an **App Group** container with the app (`UserDefaults(suiteName:)` or a file).
- Timeline: one entry now and one at `staleAfter` that renders the stale state; `.after(date)` reload policy; the app calls `WidgetCenter.shared.reloadTimelines(ofKind:)` after writing a new snapshot.
- **Interactive widgets** (iOS 17+): `Button(intent:)` / `Toggle(intent:)` with **App Intents**; the intent calls shared app code.
- **Lock screen / StandBy:** families `accessoryCircular`, `accessoryRectangular`, `accessoryInline`; respect `privacySensitive()` and `@Environment(\.redactionReasons)` for the hidden state.
- **Live Activities** (ActivityKit) and the Dynamic Island: `ActivityAttributes` + `ContentState`; start from the app, update locally or by push (ActivityKit push token sent to your server); end them when the task ends; stale date via `staleDate`.
- **Control Center controls** (iOS 18+): `ControlWidget` with App Intents.
- Previews: `#Preview(as: .systemSmall) { … } timeline: { … }` per state.
- Cross-platform bridges (e.g. `home_widget` for Flutter, `react-native-widget-extension`) only move the snapshot; the widget UI is still SwiftUI.
