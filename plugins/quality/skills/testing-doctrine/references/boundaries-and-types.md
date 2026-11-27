# Default fake boundaries and test types

## Fake only at real boundaries (default table)

Use the real implementation of code you own, injected through the constructor or container. A UI or view-model test may replace a repository with an **in-memory implementation of the repository interface**; the repository's own logic is tested against a fake transport.

| Boundary | Fake |
|---|---|
| Time | Injected clock with a fake that tests set and advance |
| OS / device (location, camera, sensors, permissions) | A fake of the bridge interface with scripted answers |
| Outbound vendors (email, SMS, push, payments, maps) | A recording sender: tests assert the message and the recipient |
| HTTP from a client app | A transport fake returning recorded real responses |
| Identity providers (OTP sender, token signing keys) | A development provider / fake key source |
| Object storage | Not faked: a real compatible engine in a container or the provider's local emulator (document the semantics it lacks), a fresh bucket per test class |

**Databases and caches are not faked in integration tests.** Run the real engine, give each test class its own fresh, migrated database or schema, seed and clean its own data. CI runs the same engine version.

## Test types: what each proves and when it runs

| Type | Proves | Size and speed | Runs |
|---|---|---|---|
| **Unit / property** | One rule, function or view model; invariants over generated inputs | Most tests; milliseconds | Every save and every PR |
| **Integration** | Real parts together through a real entry point and real engine | Some; seconds | Every PR |
| **End-to-end** | One whole user flow through the real interface | Few, main flows only; minutes | Before merging into the integration branch |
| **Smoke** | The build is alive: starts, main screen shows, no crash in the first seconds | 5–10 checks; about a minute | After every build, deploy or release, before anything else |
| **Regression** | A fixed bug stays fixed | The failing test a fix adds, at the smallest type that catches it | With the rest, forever |
| **Device / manual** | What automation cannot see on the real target | A checklist; tens of minutes | Before a release (`device-test`) |

- Smallest type that can catch it; a larger test only for what smaller ones cannot see.
- Keep the pyramid: when end-to-end tests outgrow unit tests, move checks down a type.
- Coverage is a signal for finding untested safety-critical code, never a target.
- **Speed:** while iterating run the single test and the area; run the full required suites once on the final candidate, and again only when their inputs change.
