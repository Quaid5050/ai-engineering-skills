# Kotlin Multiplatform core with an iOS (Swift) shell

## Layout

```
shared/                                  # its own Gradle build
├── build.gradle.kts                     # targets: android (KMP library plugin), iosArm64, iosSimulatorArm64
└── src/
    ├── commonMain/kotlin/<pkg>/core/    # every rule
    ├── commonTest/kotlin/<pkg>/core/    # every rule's tests (kotlin.test), fakes of core interfaces
    ├── androidMain/, iosMain/           # expect/actual primitives only (a re-entrant lock)
    └── androidHostTest/                 # JVM-only tests that need real threads
android/app/src/main/kotlin/<pkg>/…      # Android adapters + shell + bridge plugin
ios/Runner/<Feature>/…                   # Swift adapters + shell (import SharedCore)
```

Integration with Xcode: a Run Script build phase calling `./gradlew :shared:embedAndSignAppleFrameworkForXcode` (direct integration), or an XCFramework.

## What may go in `commonMain`

Allowed: pure functions and small classes; `kotlinx.serialization` **JSON tree** API (no compiler-plugin requirement if you want to keep the build simple); `kotlin.time.Instant` for ISO times; `kotlin.concurrent.Volatile`.
Forbidden (lint, no baseline): `java.*`, `android.*`, `platform.*`, `kotlinx.coroutines`, `Clock.System`, `println`/`print` (take a `log: (String) -> Unit`), files, SQLite, Keystore/Keychain, schedulers.

## Swift interop (Objective-C export)

- **Design the error bridge.** Unexpected Kotlin exceptions crossing an Objective-C/Swift boundary can terminate the process. Use explicit typed outcomes or documented `@Throws` declarations mapped to Swift errors; preserve cancellation and avoid catch-everything or null/false results that erase the cause. Test the generated interface for the installed compiler/export mode.
- **Enum entries `UPPER_SNAKE_CASE`**: `NOT_ALLOWED` → Swift `.notAllowed` (`NotAllowed` would become `.notallowed`). A Swift `switch` over a Kotlin enum needs `default`.
- **No `Pair`/`Triple`, no default arguments** relied on by Swift (it sees every parameter); use a small `data class`. Constants go in a `companion object` (`Uploader.companion.BATCH_SIZE`).
- **Numbers:** Kotlin `Int` → Swift `Int32`; nullable numbers and `Boolean`-returning lambdas are boxed (`KotlinLong?`, `KotlinBoolean`). Prefer `Long` epoch milliseconds and `Double`; put conversions in one `CoreBridge.swift` (`.kotlin`, `Clock.nowMs()`).
- **Lambdas returning `Unit`** are plain Swift closures; a `(() -> Unit) -> Unit` parameter hands Swift a task returning `KotlinUnit` (`{ task in queue.async { _ = task() } }`).
- **Conformances:** `final class FixQueue: NSObject, QueueStore` using the exported labels.
- **Objects** are `Object.shared` in Swift.
- **Test names** in common code: backticked sentences without `, ( ) . : #` (Kotlin/Native rejects them).

## Commands (adapt names)

```bash
./gradlew :shared:allTests                     # JVM + iOS simulator
./gradlew :shared:iosSimulatorArm64Test
./gradlew :app:testDebugUnitTest               # Android glue (depends on core JVM tests)
xcodebuild test -scheme Runner -destination 'platform=iOS Simulator,name=iPhone 16'
ktlint && swiftlint --strict
```

## Lint checks worth writing (a shell script is enough)

- *core*: every `commonMain` file's imports match `^import (kotlin|kotlinx)\.` and none of `kotlinx.coroutines`; no `Clock.System`, `println`.
- *shells*: grep Android and iOS glue for `== Problem.`/`!= .none`/`state ==` comparisons.
- *sizes*: `wc -l` ≤ 320 and ≤ 3 top-level `class|object|interface|enum|struct|protocol` per production file; skip `*.g.*`.

## Sources

- Kotlin, *Interoperability with Swift/Objective-C*: https://kotlinlang.org/docs/native-objc-interop.html
- Kotlin, *Direct integration with Xcode*: https://kotlinlang.org/docs/multiplatform/multiplatform-direct-integration.html
- Android, *Kotlin Multiplatform Android library plugin*: https://developer.android.com/kotlin/multiplatform/plugin
- Gary Bernhardt, *Functional core, imperative shell*: https://www.destroyallsoftware.com/screencasts/catalog/functional-core-imperative-shell

Deliberately declared `@Throws` exceptions can bridge to NSError/Swift throws; undeclared exceptions may terminate. Confirm the compiler/export mode and cancellation contract rather than imposing one universal no-exception rule. [Kotlin interop](https://kotlinlang.org/docs/native-objc-interop.html).
