# Mobile store releases and over-the-air patches

## Google Play

- **Tracks:** internal testing (up to 100 testers, available in minutes) → closed/open testing → production.
- **Staged rollout:** production releases can go to a percentage of users (e.g. 10% → 50% → 100%). You can **halt** a staged rollout; users who already updated keep the build.
- Version: `versionCode` must always increase; `versionName` is the user-facing semantic version.
- Pre-launch report and Android vitals (crash rate, ANR rate) are the first health signals.
- New permissions and background location need the Data safety form and, for some permissions, a declaration.
- **New personal developer accounts** must run a **closed test with at least 12 testers for 14 days** before they can apply for production access — plan it into the first release.
- **Signing:** an upload key you keep safe (in CI secrets, never in the repository) and Play App Signing holding the app signing key.
- A **privacy-policy URL** is required for apps that handle personal or sensitive data (and for most permissions).

## Apple App Store

- **TestFlight:** internal testers immediately; external testers after a short beta review.
- **Phased release** for automatic updates over 7 days (1%, 2%, 5%, 10%, 20%, 50%, 100%); it can be **paused** (up to 30 days) or released to everyone. Users can still update manually during a phased release.
- Build number must increase per version; the marketing version is semantic.
- New usage descriptions (location, camera, contacts) and background modes need review notes explaining the use.
- App Store privacy labels must match what the build collects (including crash logs and diagnostics).
- **Usage strings:** every permission (camera, photo library, location, microphone, contacts, …) needs its purpose string in the app's Info.plist, in words a reviewer accepts; a missing one crashes the app when it asks.
- **Signing:** a distribution certificate and provisioning profiles (or automatic signing); for CI, an App Store Connect API key as a secret. iOS builds need macOS (a hosted macOS runner works).
- A **privacy-policy URL** is required in App Store Connect.

## Over-the-air (OTA) patch tools

| Stack | Tool | What it can ship | What it cannot |
|---|---|---|---|
| Flutter | Shorebird (`shorebird release`, `shorebird patch`) | Dart code changes to a release built with Shorebird | Native code, plugins, permissions, engine/Flutter upgrades, assets not in the release; patches only apply to releases built with `shorebird release` |
| React Native / Expo | Expo Updates (EAS Update) | JS bundle and assets for a matching runtime version | Native modules, permissions, SDK upgrades (bump `runtimeVersion` → store release) |
| React Native | CodePush (and successors) | JS bundle and assets | Native code |

Rules for all of them:

- Build store artifacts **with the OTA tool's release command** so patches can target them.
- Patch a staging/preview channel first, verify on a device, then promote.
- Store guidelines allow interpreted-code updates that do not change the app's primary purpose; never use a patch to ship a new feature that needs review.
- The patch must tolerate the installed native side; when in doubt, store release.

## Rollback

- Play: halt the staged rollout; upload a fixed build with a higher `versionCode`.
- App Store: pause the phased release; submit a fixed build (expedited review exists for critical fixes).
- OTA: roll back to the previous patch in the tool's console/CLI, or publish the previous good code as a new patch.
