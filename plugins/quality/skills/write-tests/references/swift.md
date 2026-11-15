# Swift tests (iOS / macOS)

| Need | Typical choice |
|---|---|
| Framework | XCTest; Swift Testing (`@Test`, `#expect`) on recent toolchains |
| One test | `xcodebuild test -scheme App -destination 'platform=iOS Simulator,name=iPhone 16' -only-testing:AppTests/OrderLimitTests/testAcceptsAtMost50Lines` · `swift test --filter OrderLimitTests` |
| Fake clock | Inject a `Clock`/`now: () -> Date`; never `Date()` in logic |
| Network fake | A `URLProtocol` subclass returning recorded responses, or a protocol-typed transport |
| Storage | Real SQLite/Core Data in a temporary directory per test |
| UI | XCUITest for flows; snapshot tests for key screens |
| Lint | SwiftLint in CI |

```swift
final class OrderLimitTests: XCTestCase {
    func testAcceptsAtMost50Lines() {
        XCTAssertTrue(Order.canHold(lines: 50))
        XCTAssertFalse(Order.canHold(lines: 51))
    }
}
```

- No `try!` or force unwraps outside tests; in tests prefer `XCTUnwrap`.
- Background behaviour (location, background tasks) is verified on a real device — the simulator only catches logic errors.
