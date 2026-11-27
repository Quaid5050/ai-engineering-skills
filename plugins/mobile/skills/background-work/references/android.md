# Android background work

## Mechanisms

| Need | Use |
|---|---|
| Continuous user-visible work (an active session the user started) | **Foreground service** with the right `foregroundServiceType` (`location`, `dataSync`, `mediaPlayback`, `connectedDevice`, …), the matching `FOREGROUND_SERVICE_*` permission and an ongoing notification with actions. Android 14+ requires the type; Android 12+ restricts starting one from the background |
| Deferrable work with constraints | **WorkManager** (`OneTimeWorkRequest`/`PeriodicWorkRequest`, `Constraints(requiredNetworkType = CONNECTED)`); periodic minimum 15 min |
| Your own retry delay | Have the worker enqueue its next run with your delay (e.g. 30 s doubling to 5 min) — WorkManager's own backoff can grow to hours |
| Exact time | `AlarmManager.setExactAndAllowWhileIdle` needs `SCHEDULE_EXACT_ALARM`/`USE_EXACT_ALARM` — avoid unless a user-set alarm |
| After reboot / update | `BroadcastReceiver` for `BOOT_COMPLETED`, `LOCKED_BOOT_COMPLETED` (direct boot), `MY_PACKAGE_REPLACED`; restart only if the user had it on |
| Location in background | Fused Location Provider with adaptive priority/interval; `ACCESS_BACKGROUND_LOCATION` asked separately, after foreground, via settings on Android 11+ |
| Notifications | `POST_NOTIFICATIONS` runtime permission on Android 13+ |

## Doze, App Standby, OEM killers

- Doze defers jobs, alarms and network for idle devices; App Standby buckets limit how often work runs.
- Ask for `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` only with an explanation and only if the use case qualifies (Play policy).
- Xiaomi, Oppo/Realme, Vivo, Huawei, Samsung and others add their own killers ("auto-start", "battery saver"). See https://dontkillmyapp.com for per-vendor settings; deep-link users to them from the reliability check, and detect kills with a heartbeat.

## Emulator commands

```bash
adb -s <serial> shell dumpsys battery unplug
adb -s <serial> shell dumpsys deviceidle force-idle          # enter Doze
adb -s <serial> shell dumpsys deviceidle unforce && adb -s <serial> shell dumpsys battery reset
adb -s <serial> shell am set-standby-bucket <package> rare   # App Standby
adb -s <serial> shell am force-stop <package>                # process death; also blocks auto-restart until opened
adb -s <serial> root && adb -s <serial> shell kill -9 $(adb -s <serial> shell pidof <package>)   # userdebug: kill like the OS
adb -s <serial> emu geo fix <lng> <lat>                      # longitude first
adb -s <serial> shell cmd jobscheduler run -f <package> <job-id>   # run a job now
```

`adb shell am kill` does **not** stop a foreground service. Always pass `-s <serial>` so you never act on a real phone by accident.

## Battery

```bash
adb shell dumpsys batterystats --reset
# run the scenario for 1 h on a real device, unplugged
adb shell dumpsys batterystats > stats.txt        # keep out of git; check wakelocks, GPS time, jobs
```
Battery Historian visualises it.

## Sources

- Foreground services: https://developer.android.com/develop/background-work/services/fgs
- WorkManager: https://developer.android.com/develop/background-work/background-tasks/persistent
- Doze and App Standby: https://developer.android.com/training/monitoring-device-state/doze-standby
- Background location: https://developer.android.com/develop/sensors-and-location/location/background

## Long-running transfers (current Android versions)

- **User-initiated data transfer jobs** (Android 14+, `JobInfo.Builder.setUserInitiated(true)` with the `RUN_USER_INITIATED_JOBS` permission, started while the app is visible): the intended API for uploads or downloads the user started — they may run for a long time, show a notification, and survive the app going to the background. WorkManager does not expose them directly; use `JobScheduler` for this case or a `dataSync` foreground service on older versions.
- **`dataSync` foreground services are time-limited** on Android 15+ (about 6 hours in a 24-hour window; `onTimeout()` is called and the service must stop). Plan for the stop: persist progress, let the queue resume later, report the reason.
- Expedited WorkManager work (`setExpedited`) suits short, important uploads; it is quota-limited and may run as a normal job when the quota is used up.
- Uploads of large files: stream from the file on disk with a resumable protocol; never hold the whole file in memory.
- Unique work: `enqueueUniqueWork(name, ExistingWorkPolicy.KEEP, …)` so a second trigger does not start a parallel upload.

## Diagnosing stops

- **`ApplicationExitInfo`** (Android 11+): `ActivityManager.getHistoricalProcessExitReasons(packageName, 0, max)` on the next start lists why earlier processes died (`REASON_LOW_MEMORY`, `REASON_USER_REQUESTED` for force-stop, `REASON_EXCESSIVE_RESOURCE_USAGE`, `REASON_ANR`, `REASON_CRASH`, …) with timestamps. Match them to interrupted attempts by time and record the reason; read each entry once (keep the last seen timestamp).
- **WorkManager stop reasons** (`WorkInfo.stopReason`, API 31+, WorkManager 2.9+): quota, constraints, cancelled by app, system processing; log them per attempt.
- **Standby bucket:** `UsageStatsManager.getAppStandbyBucket()` explains long delays (`rare`, `restricted`).
- Force-stop cancels alarms and scheduled jobs until the user opens the app again; detect it by the exit reason and say so in the reliability screen.
