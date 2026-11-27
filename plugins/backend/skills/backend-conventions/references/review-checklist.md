# Backend review checklist

Use when reviewing a backend diff against `backend-conventions`. Each line restates a rule in the skill; the skill is the source.

- [ ] Files in the right module and folder with the right suffix; one public type per file (DTO groups excepted).
- [ ] Each technical kind of code in its placement row (secrets, storage, parsing, limiters, loops).
- [ ] Edges thin: no data access, transaction, lock or rule; one use-case call (default profile: ~15 lines, ≤ ~5 parameters).
- [ ] Services take plain ids/values, return results/read models, own the transaction, notify after commit, re-read rights under the lock.
- [ ] Non-member → not found, missing role → forbidden (or the project's rule), through the access unit.
- [ ] Domain: only its allowlist (the project's profile, or the default profile); new types pass the concept test.
- [ ] Shape validation in the validation unit using domain constants; invariants still guarded in the domain.
- [ ] No database or cache call in a loop; projections and paging in the database; workload evidence (plan or query count) for query and index changes.
- [ ] Expected errors have stable codes; catches typed and visible; safety paths never swallow.
- [ ] Injected clock; timeouts on I/O; no blocking on async results where the stack is async.
- [ ] Logs pass the personal-data rule; no ids or unbounded values as metric tags.
- [ ] New tables: constraints, FKs with explicit delete, enums as text, UTC, a concurrency strategy per invariant, retention/deletion.
- [ ] Options validated at start; one secret per purpose; lifetimes right (nothing per-request held by a shared object); one retry owner per send.
- [ ] The use case authorises; permission caches (if any) scoped, invalidated and bounded; jobs re-check access at run time.
- [ ] Architecture tests and analyzers green; allowlists with empty baselines, or the project's owned, expiring exceptions.
