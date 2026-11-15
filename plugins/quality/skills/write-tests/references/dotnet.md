# .NET tests

| Need | Typical choice |
|---|---|
| Framework | xUnit (or NUnit/MSTest — follow the project) |
| One test | `dotnet test --filter "FullyQualifiedName~OrderTests.Rejects_more_than_50_lines"` |
| Area / all | `dotnet test tests/Shop.Api.Tests` · `dotnet test` |
| Fake clock | Inject `TimeProvider`; tests use `FakeTimeProvider` (`Microsoft.Extensions.TimeProvider.Testing`) and `Advance(...)` |
| Integration host | `WebApplicationFactory<Program>`; replace only vendors in `ConfigureWebHost` |
| Database fixture | A class fixture that creates a fresh database per test class and applies every migration (Testcontainers or local services) |
| Parameterised | `[Theory]` + `[InlineData]` |
| Architecture tests | ArchUnitNET / NetArchTest |

```csharp
public class OrderLimitTests
{
    [Theory]
    [InlineData(50, true)]
    [InlineData(51, false)]
    public void Order_accepts_at_most_50_lines(int lines, bool expected)
    {
        var accepted = Order.CanHold(lines);

        Assert.Equal(expected, accepted);
    }
}
```

- Integration: `IClassFixture<WebApplicationFactory<Program>>` (or a subclass that swaps only true externals); sign in test users through helpers; assert status **and** exact body.
- Query counting: a command interceptor in tests; reset before the request, assert the exact count with one item and with several (catches N+1).
- Build with warnings as errors in CI: `dotnet build -warnaserror`.
