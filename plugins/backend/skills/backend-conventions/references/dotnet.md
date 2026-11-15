# .NET (ASP.NET Core, EF Core)

How the generic rows map onto .NET. The project's own layout wins.

## Modules

| Generic | .NET |
|---|---|
| Domain | `<App>.Domain` class library, no package references beyond the BCL |
| Persistence | `<App>.Persistence`: `DbContext`, `IEntityTypeConfiguration<T>` in `Configurations/`, `Queries/` (`IQueryable` extensions), `Locks/` (Postgres advisory locks via raw SQL), `Migrations/` |
| Application | `<App>.Application/<Area>/<Area>Service.cs`; ports in `Application/Abstractions/` |
| Edge | `<App>.Api`: Minimal APIs, one `MapGroup` per area in `<Area>Endpoints.cs`, `<Area>Requests.cs` / `<Area>Responses.cs` records, `<Area>Validation.cs`, `<Area>Mappings.cs` (`ToResponse()`), `Program.cs` as composition root |
| Workers | `<App>.Workers` (Hangfire or Quartz), or `BackgroundService` in `Api/Background/` until a job host exists |

## Idioms

- Unit of work: the `DbContext` is scoped to one request/job and **not thread-safe** — never run two queries on it in parallel; reads use `AsNoTracking()`.
- Async: `async` all the way, `CancellationToken ct` last and passed to every EF/HTTP call; no `.Result`/`.Wait()`/`async void`.
- Realtime (SignalR): hub methods are thin edges; groups are joined server-side from membership, never from a client-supplied name.

- Handlers: `private static async Task<Results<Ok<X>, ValidationProblem, ProblemHttpResult>>`, return `TypedResults`; `RequireAuthorization()` on the group; `.WithName("<operationId>")` matching the contract.
- Errors: `Result<T>` + `Error(Kind, Code, Title)`; map to `TypedResults.Problem(...)` with `type` = problem URI; `UseExceptionHandler` + `AddProblemDetails()` for the 500 path.
- Validation: hand-written `<Area>Validation` returning `TypedResults.ValidationProblem(errors)`. DataAnnotations on request records do nothing unless validation is registered — decide once in a decision record.
- Reads: `AsNoTracking()` + `Select`; bulk: `ExecuteUpdateAsync` / `ExecuteDeleteAsync`; multiple `Include`s → `AsSplitQuery()`.
- Transactions: `await using var tx = await db.Database.BeginTransactionAsync(ct)`; locks: `pg_advisory_xact_lock`; optimistic concurrency: `xmin` mapped with `.IsRowVersion()` → `DbUpdateConcurrencyException` → conflict.
- Time: `TimeProvider` injected; tests use `FakeTimeProvider` (`Microsoft.Extensions.TimeProvider.Testing`).
- Options: `AddOptions<T>().BindConfiguration("Section").ValidateDataAnnotations().ValidateOnStart()`; no `IConfiguration` in constructors.
- Logging: `ILogger<T>`, message templates; `[LoggerMessage]` source generation on hot paths. Watch `{@Object}` destructuring: it serialises the whole object.
- Resilience: `IHttpClientFactory` + `Microsoft.Extensions.Http.Resilience` `AddStandardResilienceHandler`, `options.Retry.DisableForUnsafeHttpMethods()`; for sends, a breaker + timeout only.
- DI: `AddScoped` for services holding `DbContext`, `AddSingleton` for stateless adapters; `IServiceScopeFactory` in singletons that need a scope. Each project exposes `Add<Project>(this IServiceCollection)`.
- Analyzers: `<AnalysisLevel>latest-recommended</AnalysisLevel>`, `<TreatWarningsAsErrors>true</TreatWarningsAsErrors>` in `Directory.Build.props`; suppress at location with `[SuppressMessage(..., Justification = "...")]`.

## Tests and tools

- Tests: xUnit; integration through `WebApplicationFactory<Program>` against a real database (Testcontainers or the compose file); one fresh database per test class.
- Query count guard: an EF Core `DbCommandInterceptor` that counts commands, asserted per request.
- Architecture tests: ArchUnitNET or NetArchTest over the built assemblies.
- Migrations: `dotnet ef migrations add <Name> --project src/<App>.Persistence`; review `dotnet ef migrations script <Prev> <Name>`; `CREATE INDEX CONCURRENTLY` needs `suppressTransaction: true` and a non-idempotent script.
- Commands: `dotnet format --verify-no-changes && dotnet build -warnaserror && dotnet test`.

## Quick greps (should print nothing for new code)

```bash
grep -rln 'DbContext\|BeginTransaction' src/*.Api --include='*.cs' | grep -v Health/
grep -rn 'DateTime\(Offset\)\?\.\(UtcNow\|Now\)' src --include='*.cs' | grep -v Migrations
grep -rn 'IConfiguration ' src --include='*.cs' | grep -v 'Program.cs\|ServiceCollectionExtensions'
grep -rn 'catch *(Exception' src --include='*.cs'
```
