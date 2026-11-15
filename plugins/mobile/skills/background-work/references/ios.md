# iOS background work

## Mechanisms

| Need | Use |
|---|---|
| Deferrable refresh | `BGTaskScheduler` with `BGAppRefreshTaskRequest` (short) or `BGProcessingTaskRequest` (long, can require power/network); identifiers in `Info.plist` `BGTaskSchedulerPermittedIdentifiers`; the system decides when |
| Finish a task after backgrounding | `beginBackgroundTask(expirationHandler:)` — seconds, not minutes; always end it |
| Uploads/downloads that outlive the app | Background `URLSession` (`URLSessionConfiguration.background`) — the system transfers and relaunches you on completion |
| Continuous location | `allowsBackgroundLocationUpdates = true`, background mode `location`, `pausesLocationUpdatesAutomatically` tuned, `activityType` set; or `CLLocationUpdate.liveUpdates()` + `CLBackgroundActivitySession` on newer iOS |
| Wake on movement after termination | Significant-change location service and region monitoring (relaunch the app after termination; restore state in launch) |
| Push-triggered work | Silent push (`content-available`), budgeted and not guaranteed |
| User-started long task (iOS 26+) | `BGContinuedProcessingTask` with visible progress |

Background modes need App Review justification. Never request "Always" location before your explanation; handle provisional "Always" (granted as "While Using" until the system asks later).

## Facts to design for

- A user force-quit from the app switcher stops most background execution until the user opens the app again (location relaunch is an exception for significant changes/regions).
- Low Power Mode and Background App Refresh off reduce or stop refresh tasks — read `ProcessInfo.processInfo.isLowPowerModeEnabled` and `UIApplication.shared.backgroundRefreshStatus` and report them as reasons.
- When Location Services are off globally, the authorisation status reads as denied: check `CLLocationManager.locationServicesEnabled()` first to report the right reason.

## Simulator and debugging

- Features › Location › City Run / Freeway Drive; or a GPX file in the scheme.
- Trigger a scheduled task from the debugger, paused in the app:
  `e -l objc -- (void)[[BGTaskScheduler sharedScheduler] _simulateLaunchForTaskWithIdentifier:@"<id>"]`
- Simulate expiration: `_simulateExpirationForTaskWithIdentifier:`.
- Kill like the system: stop from Xcode (not swipe), then trigger the relaunch event.

## Battery

Xcode Organizer energy reports, Instruments Energy Log / Power Profiler on a real device, in Release.

## Sources

- Handling location updates in the background: https://developer.apple.com/documentation/corelocation/handling-location-updates-in-the-background
- BGTaskScheduler: https://developer.apple.com/documentation/backgroundtasks/bgtaskscheduler
- Background URLSession: https://developer.apple.com/documentation/foundation/downloading-files-in-the-background

## Background uploads

- A **background `URLSession`** (`URLSessionConfiguration.background(withIdentifier:)`) keeps transfers going while the app is suspended or terminated by the system, and relaunches the app to deliver results (`application(_:handleEventsForBackgroundURLSession:completionHandler:)`).
- Background sessions upload **only from a file** (`uploadTask(with:fromFile:)`): write a multipart body or the raw file to a file in app-private storage first; data or stream uploads are not supported in the background.
- Each task carries the record's client id (in `taskDescription` or a header) so results map back to the queue row after a relaunch.
- A user force-quit cancels background session transfers; the queue must pick them up again on next launch.
- `BGProcessingTask` suits deferrable work that needs minutes (with `requiresNetworkConnectivity`); it may be delayed for hours.
