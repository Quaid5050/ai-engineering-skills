# Backend performance tools

## Query plans
- PostgreSQL: `EXPLAIN (ANALYZE, BUFFERS) <query>;` — look for `Seq Scan` on large tables, row-estimate errors, sorts spilling to disk. MySQL: `EXPLAIN ANALYZE`. SQL Server: actual execution plan.
- Seed 10× realistic synthetic data before judging; run `ANALYZE` after seeding.
- Time-partitioned tables (TimescaleDB hypertables, native partitions): every query carries a time predicate so partitions are pruned.
- Geometry: a GiST index on any geometry used in `WHERE` / `ST_DWithin`.

## Statement statistics
- PostgreSQL `pg_stat_statements`: `CREATE EXTENSION IF NOT EXISTS pg_stat_statements;` then
  `SELECT calls, round(mean_exec_time) AS ms, query FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 20;`
  (needs `shared_preload_libraries = 'pg_stat_statements'`).
- App-side slow-query logging: an ORM interceptor that logs commands over 100 ms with SQL text and **no parameter values**.

## Query counting in tests
| Stack | Hook |
|---|---|
| .NET / EF Core | a `DbCommandInterceptor` counting `ReaderExecuting`; `Reset()` then assert `Assert.Equal(n, sql.Count)` |
| Django | `django_assert_num_queries(n)` / `assertNumQueries(n)` |
| SQLAlchemy | `event.listen(engine, "before_cursor_execute", counter)` |
| Node (Prisma / Knex / TypeORM) | query event listeners (`$on('query')`, `knex.on('query')`, a logger) |
| Spring / Hibernate | `hibernate.generate_statistics` + `Statistics.getPrepareStatementCount()`, or datasource-proxy |

Assert once with one item and once with several items: an N+1 changes the count.

## Load tests
k6 example:
```js
import http from "k6/http";
export const options = {
  stages: [{ duration: "1m", target: 50 }, { duration: "3m", target: 50 }],
  thresholds: { http_req_duration: ["p(95)<200"], http_req_failed: ["rate<0.001"] },
};
export default function () { http.get(`${__ENV.BASE_URL}/v1/products?limit=50`); }
```
Run `k6 run -e BASE_URL=http://localhost:8080 perf/products.js`. Alternatives: Gatling, Locust, Artillery.

## Micro-benchmarks
BenchmarkDotNet (.NET), JMH (JVM), `pytest-benchmark` (Python), `tinybench`/`mitata` (Node), Go `testing.B`.
