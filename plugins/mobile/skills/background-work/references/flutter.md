# Background work in Flutter apps

## Where the rules live

In a Flutter app the Dart code can be the core: the queue rules, retry policy and status decisions are written once in pure Dart (no Flutter imports, no plugins, time and OS facts as parameters) and unit-tested once. The native side only hosts the OS mechanisms. Record the choice in a decision record; when the background work must run with the Flutter engine not available (or must be identical with native-only code), a native shared core (`shared-core`) is the alternative.

## Mechanisms

| Need | Typical choice | Notes |
|---|---|---|
| Deferrable or periodic work | `workmanager` (WorkManager on Android, BGTaskScheduler on iOS) | Runs a top-level Dart callback in a **background isolate**: no access to the UI isolate's memory or providers — rebuild dependencies inside the callback, open the database there, keep it short |
| Uploads the user started / large files | Native background transfer (Android user-initiated jobs or a foreground service; iOS background `URLSession`) via a plugin such as `background_downloader`, or a small platform channel | Uploads from files on disk; map results back by client id |
| Continuous user-visible work | A foreground-service plugin (Android) + the matching iOS background mode | Needs store review justification |
| Calling native code | Platform channels, ideally generated (`pigeon`) | The bridge types stay in the data layer |

## Rules

- The background isolate and the UI isolate never share state in memory: they share the database (Drift with one connection per isolate, or `DriftIsolate`) and the queue's lease row.
- `@pragma('vm:entry-point')` on the background callback, or it is removed by tree shaking in release builds.
- Plugins used in the background isolate must support it; check each plugin's docs.
- Test the Dart task body as a plain function with fakes (`write-tests`, quality plugin); check scheduling and survival on real devices (`device-test`).
- iOS gives no guarantee when `BGTaskScheduler` work runs; anything the user waits for needs a foreground path too.
