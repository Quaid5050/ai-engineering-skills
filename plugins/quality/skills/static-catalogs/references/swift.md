# Static catalogs: Swift

## The table: one exhaustive switch that returns the whole row

Keep the enum (its `rawValue` is the persisted id) and replace the per-attribute switches with **one** switch that
returns a struct. The compiler still rejects a new case without a row, which a dictionary keyed by case does not.

```swift
public enum Plan: String, CaseIterable, Identifiable, Sendable {
    case free, pro, team            // raw values are saved: never rename them
    public var id: String { rawValue }

    public struct Info: Sendable, Equatable {
        public let title: String
        public let symbol: String
        public let monthlyPrice: Decimal
        public let seats: Int?
        public let group: Group
    }
    public enum Group: Int, CaseIterable, Sendable { case personal, business }

    /// Adding a plan: one row here and one id in `PlanCatalogTests.frozenIDs`.
    public var info: Info {
        switch self {
        case .free: Info(title: "Free", symbol: "leaf", monthlyPrice: 0, seats: 1, group: .personal)
        case .pro:  Info(title: "Pro", symbol: "star", monthlyPrice: 9, seats: 1, group: .personal)
        case .team: Info(title: "Team", symbol: "person.3", monthlyPrice: 29, seats: nil, group: .business)
        }
    }

    // Old accessors delegate, so callers do not change.
    public var title: String { info.title }
    public var symbol: String { info.symbol }

    /// Groups in display order, derived; no second list of cases.
    public static var grouped: [(Group, [Plan])] {
        Group.allCases.map { g in (g, allCases.filter { $0.info.group == g }) }
    }
}
```

- Put the type in the pure core module (no UI framework import) if the project has one.
- Behaviour stays a method: `func prompt(for text: String) -> String` builds from `info.promptTemplate`.
- A view never has its own `symbol(for:)`; it reads `plan.symbol`.

## Characterisation and guard tests (Swift Testing)

```swift
import Testing
@testable import Core

struct PlanCatalogTests {
    static let frozenIDs = ["free", "pro", "team"]          // persisted: append only

    @Test func idsAreFrozen() { #expect(Plan.allCases.map(\.rawValue) == Self.frozenIDs) }

    @Test(arguments: [
        (Plan.free, "Free", "leaf"), (.pro, "Pro", "star"), (.team, "Team", "person.3"),
    ])
    func rowIsPinned(plan: Plan, title: String, symbol: String) {
        #expect(plan.title == title)
        #expect(plan.symbol == symbol)
    }

    @Test func everyCaseIsGroupedOnce() {
        #expect(Plan.grouped.flatMap(\.1).sorted { $0.rawValue < $1.rawValue }
                == Plan.allCases.sorted { $0.rawValue < $1.rawValue })
    }
}
```

Write the pinned table from today's code **before** the move (copy the values out of the old switches), run it
green, then refactor with the test file unchanged.

## When generation is right, the standard tools

| Source of truth | Tool |
|---|---|
| UI text and translations | String Catalogs (`.xcstrings`); Xcode generates the symbols |
| Images, colours | Asset catalog symbol generation (Xcode); SwiftGen for older setups |
| HTTP API schema | `swift-openapi-generator` as a Swift package build plugin |
| A data file shared with another app | A small generator run by a Swift package build or command plugin, output committed, CI diff check |
| Repetitive conformances | Swift macros (compile time, type checked) before template tools such as Sourcery |

Avoid reading a bundled YAML or JSON file at launch for data fixed at build time: it needs a parser dependency,
fails at run time instead of compile time, and loses exhaustiveness.
