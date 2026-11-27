# Specialized profiles

| Profile | Concrete invariants and validation |
|---|---|
| Payments/ledgers | Integer minor units or justified decimal arithmetic, explicit currencies/rounding, balanced entries, immutable audit trail, idempotent operations, refunds/reconciliation and uncertain provider outcomes. Never infer success from a timeout. |
| Real-time collaboration | Ordering/versioning, conflict semantics, tombstones, offline replay, authorization changes and convergence. Choose CRDT/OT/locking only for the actual editing model and test partitions/rejoins. |
| SDK/library publishing | Public API/ABI compatibility, supported runtimes, packaging/licenses, reproducible artifacts, deprecation and consumer contract tests. |
| CLI tools | Argument parsing, exit codes, stdout/stderr contracts, pipe behavior, cancellation, shell escaping and noninteractive operation. |
| Browser extensions | Narrow permissions, content/background boundary, origin/message validation, store policy and update integrity. |
| Embedded/IoT | Hardware resource/time budgets, watchdog/recovery, power loss, secure boot/update, device identity and hardware-in-loop testing. |
| Scientific/HPC | Numerical conditioning/error bounds, units, reproducibility, precision/hardware effects, reference datasets and scaling measurements. |
| Graphics/games | Frame-time budgets, resource lifetime, input timing, asset pipeline integrity and platform-specific profiling. |
| Regulated/safety-critical | Applicable domain standards, traceability, hazard analysis and qualified independent review. Generic skills do not establish compliance. |

These are documented profiles, not certified or fully platform-tested implementations. Promote support only after the relevant fixture and expert/device evidence exists.
