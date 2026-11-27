# Refactoring safely (maintenance mode)

1. **Pin the behaviour first.** Missing coverage → characterisation tests on the old code, passing, committed alone.
2. **Move, then change** — separate commits, tests green after each.
3. **Small steps, always green.** A red step is understood before the next step: revert it when the cause is the step itself, fix forward only when the failure exposed a real, understood gap.
4. **The contract does not move** unless the slice says so; a deliberate contract change follows `add-endpoint` compatibility rules.
5. **Baselines do not grow.** A new rule lands with the code fixed; if that is impossible, a shrinking-only baseline with a reason per entry and an issue to empty it.
6. **Tier:** a refactor inside one module is Standard; one that moves responsibilities across layers or features is Structural and gets a `design-review` first.
