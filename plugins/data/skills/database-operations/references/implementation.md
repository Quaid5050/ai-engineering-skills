# Database adapters

PostgreSQL: distinguish scan, rewrite and lock mode; use [ALTER TABLE documentation](https://www.postgresql.org/docs/current/sql-altertable.html) for the selected version. Concurrent index builds have transaction and failure-cleanup requirements.

MySQL/MariaDB: confirm storage engine, online DDL capabilities, metadata locks, collation and isolation behavior. SQL Server: inspect lock escalation, snapshot configuration and provider semantics. SQLite: account for single-writer behavior, journal mode, busy handling and filesystem locking. Document/column stores: verify consistency, partition keys, TTL and index build semantics rather than copying relational assumptions.

For every engine, restore a representative backup, check integrity and execute application smoke queries before accepting RPO/RTO evidence. Production restore execution requires explicit scope and a tested recovery path.
