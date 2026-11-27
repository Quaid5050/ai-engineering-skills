# Review output template

```markdown
## Code review — <short head SHA>
**Tier:** Quick (self-review) | Standard | Structural / High-risk · **Reviewer:** reviewer agent (independent) | author (self-review)
**Verdict:** approve | approve with fixes | changes required
**Risk tier:** low | medium | high — why

### Critical / Major / Minor / Nits
- [severity] file:line — problem. Scenario: … Fix: … Rung: test → type.

### Design pass
- [major|minor] file:line — placement / duplication / reuse / boundary / validation-secret-storage / design review. Who would copy it: … Fix: …
(or "No design findings", followed by the checks run and what was searched for each; "not required for this tier" for Quick)

### Suspicions (non-blocking)
### Checked and fine
Every dimension checked with no findings, so "no issues" is a claim with coverage.
```

Re-review:

```markdown
## Code review — <new SHA> (re-review of <old SHA>)
Delta reviewed: `git diff <old>..<new>` (N files)
- Fixed: <finding> — how
- Still open: <finding> — why
- New from the fix: <finding> | none
```
