# JVM: Spring Boot (Java or Kotlin)

How the generic rows map onto Spring. Package by feature, layers inside.

## Modules

```
com.example.<app>.<area>
├── domain        # entities as plain classes / Kotlin data classes, value objects, rules — no Spring, no JPA
├── application   # <Area>Service (@Service), ports as interfaces
├── persistence   # JPA entities or jOOQ/Spring Data JDBC mappings, repositories, query methods
├── web           # @RestController, request/response records, <Area>Validation, mappers
└── adapters      # vendor implementations of ports
```

Spring Modulith can verify module boundaries (Java `ApplicationModules.of(App.class).verify()`, Kotlin `ApplicationModules.of(App::class.java).verify()`). If the project maps the domain directly with JPA annotations, record that choice in a decision record; the domain allowlist then includes `jakarta.persistence` annotations only.

## Idioms

- Controllers: thin; validate shape (Bean Validation `@Valid` on request records, or a hand-written validator), pass the caller's id (Java `principal.getName()`, Kotlin `principal.name`, or your `@AuthenticationPrincipal` type's id) to one service method, map the result. Errors as RFC 9457 via `ProblemDetail` and one `@RestControllerAdvice`.
- Results: a sealed interface (`sealed interface Result<T>` / Kotlin `sealed interface`) with error `kind` + `code`. In Kotlin **do not name it `Result`** — it clashes with `kotlin.Result`; use `Outcome<T>` or `<Area>Result`.
- Reads: interface or record projections, `@EntityGraph` / `JOIN FETCH` to avoid N+1; `spring.jpa.open-in-view=false`; pagination with keyset (`Window`/`ScrollPosition` in Spring Data 3.1+).
- Bulk: `@Modifying @Query("update …")` (bypasses the persistence context — clear it), JDBC batch inserts (`hibernate.jdbc.batch_size`).
- Transactions: `@Transactional` on the **service** method only; locks via `@Lock(PESSIMISTIC_WRITE)` or `pg_advisory_xact_lock`; optimistic `@Version`; notify after commit with `@TransactionalEventListener(phase = AFTER_COMMIT)` — but such events are lost if the process dies after commit; anything that must not be lost goes through an outbox table. **Self-invocation bypasses the proxy:** calling a `@Transactional` method from the same class runs it without a transaction; call it through another bean.
- Time: inject `java.time.Clock`; tests use `Clock.fixed(...)`.
- Config: `@ConfigurationProperties` records with `@Validated` (fails at start); no `@Value` scattered in business classes; one properties class per secret purpose.
- Logging: SLF4J parameterised messages (`log.info("Order {} shipped", id)`); never `toString()` of entities carrying personal data.
- Resilience: `RestClient`/`WebClient` with timeouts; Resilience4j retry + circuit breaker for idempotent reads; sends get a breaker + timeout and are retried only by the job.
- Jobs: `@Scheduled` with ShedLock for single-instance runs, or a queue; a job calls one service method (`add-scheduled-job`).
- Uploads: `spring.servlet.multipart.max-file-size` / `max-request-size` set explicitly; stream to object storage (`MultipartFile.getInputStream()` or a presigned URL) instead of buffering whole files in memory (`add-file-upload`).
- Contract drift: springdoc-openapi generates `/v3/api-docs`; a test fetches it and diffs it against the contract file.

## Kotlin specifics

- Apply `kotlin("plugin.spring")` (all-open): Kotlin classes are final, and final classes/methods silently defeat `@Transactional`, `@Cacheable` and other proxies.
- Apply `kotlin("plugin.jpa")` (no-arg) for JPA entities; **don't use data classes as JPA entities** (`equals`/`hashCode`/`toString` over lazy relations break and leak); use regular classes with an id-based `equals`.
- Domain types can be data classes and value classes; keep JPA annotations off them.
- Static analysis: detekt + ktlint (warnings as errors); Konsist for architecture tests in Kotlin.
- Coroutines in controllers (`suspend fun`) need WebFlux or Spring MVC's coroutine support; don't mix blocking JDBC calls into coroutine code without `Dispatchers.IO`.

## Tests and tools

- JUnit 5, AssertJ (Kotlin: kotest assertions or AssertJ); `@SpringBootTest` + `MockMvc`/`WebTestClient` for HTTP; Testcontainers for the real database with `@ServiceConnection` (Spring Boot 3.1+) so no URL wiring is needed.
- Query count guard: `datasource-proxy` or Hibernate statistics asserted per request.
- Architecture tests: ArchUnit (`layeredArchitecture()`, `classes().that().resideInAPackage("..domain..").should().onlyDependOnClassesThat().resideInAnyPackage(...)`), Konsist for Kotlin, Spring Modulith verify.
- Migrations: Flyway (`V<n>__<name>.sql`) or Liquibase. Flyway migrations are **hand-written SQL** (no generator): write them, run them against a Testcontainers database in a test, read them for locks. Undo migrations need the paid edition, so the plan is **roll forward** (a new migration that fixes the previous one). `CREATE INDEX CONCURRENTLY` needs a non-transactional migration (Flyway script config `executeInTransaction=false`).
- Commands: `./gradlew check` or `./mvnw verify`.

## Quick greps

```bash
grep -rln 'Repository' src/main --include='*.java' --include='*.kt' | grep '/web/'
grep -rn 'LocalDateTime.now()\|Instant.now()' src/main | grep -v Clock
grep -rn '@Value(' src/main
grep -rnE 'catch \((e: )?Exception' src/main
```
