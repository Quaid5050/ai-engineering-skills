# Mobile performance tools

| Need | Android | iOS |
|---|---|---|
| Startup | Macrobenchmark `StartupTimingMetric`; `adb shell am start -W` | Instruments App Launch; `XCTApplicationLaunchMetric` |
| Frames / jank | Macrobenchmark `FrameTimingMetric`; Perfetto / System Trace | Instruments Animation Hitches |
| Memory | Android Studio Memory Profiler, heap dumps | Instruments Allocations / Leaks |
| Size | Android Studio APK Analyzer, `bundletool get-size total` | App Thinning Size Report (`xcodebuild -exportArchive` with thinning) |
| Battery | `adb shell dumpsys batterystats --reset`, run the scenario 1 h, `adb shell dumpsys batterystats > stats.txt` (keep out of git); Battery Historian; check wakelocks and GPS time | Xcode Organizer Energy reports; Instruments Energy Log on a device |
| Background limits to test | Doze: `adb shell dumpsys deviceidle force-idle`; App Standby buckets | Background App Refresh off; Low Power Mode |

Framework notes:
- **Flutter:** `flutter run --profile --trace-startup` (writes `build/start_up_info.json`); DevTools Performance with "Track widget builds"; `integration_test` + `traceAction` and `flutter drive --profile` for frame percentiles; `flutter build apk --analyze-size --target-platform android-arm64`.
- **React Native:** Hermes profiler, React DevTools Profiler, Flashlight for Android FPS/CPU; `react-native-bundle-visualizer`.
- Always measure on a release/profile build on a real device, including a low-end Android (2–3 GB RAM).
