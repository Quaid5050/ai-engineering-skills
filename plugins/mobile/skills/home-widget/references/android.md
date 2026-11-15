# Android widgets and tiles

- **Jetpack Glance** (`GlanceAppWidget` + `GlanceAppWidgetReceiver`): compose-style widgets; sizes via `SizeMode.Responsive`; actions with `actionRunCallback<…>()` (`ActionCallback`) or `actionStartActivity`.
- Classic `AppWidgetProvider` + `RemoteViews` when Glance is not available.
- Updates: `GlanceAppWidget.update(context, id)` / `updateAll`; `updatePeriodMillis` minimum 30 min — schedule the live → stale switch at `staleAfter` with WorkManager (or an inexact alarm), don't poll.
- Shared data: the app writes the snapshot to `SharedPreferences`/DataStore (cross-platform bridges such as `home_widget` for Flutter or `react-native-android-widget` do this).
- **Quick Settings tile:** `TileService` with `onStartListening`/`onClick`; `requestListeningState` to refresh; toggles call into app code.
- **Ongoing status:** an ongoing notification; on Android 16+ consider progress-centric notifications ("live updates").
- Colours: map Material You dynamic colours to your tokens; check contrast on both light and dark wallpapers.
- Previews: `previewLayout` / Glance `@Preview` per state.
