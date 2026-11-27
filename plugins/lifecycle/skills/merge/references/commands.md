# Merge commands and multi-PR cases

```bash
gh pr view <PR> --json headRefOid,mergeStateStatus,statusCheckRollup,body,closingIssuesReferences
gh pr view <PR> --comments          # the newest "## Code review — <SHA>" must cover the head
gh issue view <issue> --comments    # Structural: the "## Design review" and its revision vs the first production-code commit
gh pr diff <PR>                     # gate 7: read it yourself
gh pr merge <PR> --merge --match-head-commit <head-sha>
```

**Stacked PRs:** merge bottom-up. After the bottom one merges, retarget the next to main (`gh pr edit <next> --base main`), merge main in, get a fresh green run and a review covering the new head (a delta re-review when only the merge changed), then merge.

**Open device tests** do not hold a merge only when the project's policy batches them into one real-device pass before release; list them in the PR as open and run `device-test` (mobile plugin) before `release`. Otherwise they are part of gate 4.

**Report:** each gate → evidence; the merge commit; main's CI after the merge; anything left open (device tests, follow-up issues).
