# Architecture profiles

Layered/ports-and-adapters design fits many business applications but is not mandatory. A compiler may organize around parsing/analysis/code generation; a data pipeline around transformation and lineage; a library around a stable API; a CLI around commands and I/O boundaries; a game around update/render/data ownership.

SOLID, DRY and patterns are decision aids. Avoid duplicated business knowledge; tolerate similar code when independent concepts evolve separately. Interfaces can serve in-process contracts and testability, but each abstraction needs a current purpose. Favor clear ownership over one universal generic service.

Artifacts: context/dataflow view, workload assumptions, alternatives table, key invariants, failure/recovery model and decision record. Extend existing project documentation rather than adding a second architecture system.
