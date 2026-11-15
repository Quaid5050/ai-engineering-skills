# JVM tests (Java, Kotlin)

| Need | Typical choice |
|---|---|
| Framework | JUnit 5 (Kotlin: kotlin.test / Kotest on JUnit) |
| One test | `./gradlew test --tests "shop.OrderLimitTest.accepts at most 50 lines"` · `mvn -Dtest=OrderLimitTest#acceptsAtMost50 test` |
| Area / all | `./gradlew :api:test` · `./gradlew test` |
| Fake clock | Inject `java.time.Clock`; tests use `Clock.fixed(...)` or a mutable test clock |
| Integration host | Spring `@SpringBootTest(webEnvironment = RANDOM_PORT)` + `WebTestClient`/`MockMvc`; Ktor `testApplication` |
| Database fixture | Testcontainers with the production engine; Flyway/Liquibase migrations applied per test class |
| Parameterised | `@ParameterizedTest` + `@CsvSource` |
| Architecture tests | ArchUnit; Konsist (Kotlin) |
| Android unit tests | Robolectric only where needed; pure Kotlin tests for logic |

```kotlin
class OrderLimitTest {
    @ParameterizedTest
    @CsvSource("50,true", "51,false")
    fun `order accepts at most 50 lines`(lines: Int, expected: Boolean) {
        assertEquals(expected, Order.canHold(lines))
    }
}
```

- Mockito/MockK only for true boundaries (vendors, OS) — never for your own services.
- **Testcontainers with Spring Boot 3.1+:** declare the container as a bean with `@ServiceConnection` (or a static `@Container` + `@ServiceConnection` field) so the datasource is wired without manual properties:

```kotlin
@TestConfiguration(proxyBeanMethods = false)
class TestContainers {
    @Bean @ServiceConnection
    fun postgres() = PostgreSQLContainer("postgres:16-alpine")
}

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@Import(TestContainers::class)
class CreateOrderTest(@Autowired val client: WebTestClient) {
    @Test
    fun `a non-member gets 404`() {
        client.get().uri("/v1/teams/{id}/orders", UUID.randomUUID())
            .header("Authorization", "Bearer ${tokenFor("user-b")}")
            .exchange().expectStatus().isNotFound
    }
}
```

- Kotlin forms: `App::class.java`, `catch (e: IOException)`, `assertThrows<OrderFull> { … }`; grep Kotlin sources under `src/main/kotlin` (and `src/test/kotlin`).
- Kotlin/Native test names reject some characters (`, ( ) . : #`): keep backticked names plain if tests run on native targets.
