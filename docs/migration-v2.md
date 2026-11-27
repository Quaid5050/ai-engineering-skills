# Version 2 migration

The eight existing plugins move to 2.0.0 for breaking workflow/hook behavior; nine new plugins start at 1.0.0. Skill names/paths remain stable.

- Foundation dependencies provide context, risk and execution authority. Flat installation resolves them.
- Replace universal issue/spec/review rituals in consumer rules with the risk-based workflow; preserve genuine project controls.
- Replace sent-ledger/skip-on-duplicate guidance with durable intent, leases, payload identity and provider reconciliation. Local uniqueness does not imply exactly-once external effects.
- Keep invalid/offline work recoverable; revoke sign-out credentials promptly and quarantine original-account records with explicit discard/retention policy.
- Use architecture-specific boundaries and independent test oracles, including properties, sequences and meaningful boundary doubles.
- Legacy v1 copies have no ownership record. Back up and compare before choosing a clean installation destination; never forge ownership or force overwrite.
- Hooks and installer need Python 3.10+. Validation also needs `requirements-dev.txt`.

This migration does not publish a release, deploy production or authorize merging.
