# Design review template

| Review | Covers | Posted on |
|---|---|---|
| Spec-level | The whole technical design of a specified feature (from `spec`) | The epic (multi-slice) or the feature issue |
| Slice-level | Only what a slice adds beyond the spec-level review; one line when it adds no structure | The slice issue, before its first production-code commit |
| Fix | A fix that moves responsibilities or needs a shared fix for the bug class | The bug issue; the reproduction test may already be committed |

```markdown
## Design review — <YYYY-MM-DD>
Plan reviewed: <link or summary> · Revision: <commit or plan version> · Reviewer: architect agent (independent) | author (not independent)

### Decisions
- <what the plan commits to> — because <reason>
### Reuse
- Use <existing piece> for <part>. / New shared piece: <name>, instead of a feature-specific one.
- Searched: <terms, folders>
### Risks (ranked)
- <risk> — scenario: <concrete failure> — fix: <change to the plan>
### Questions for the owner
### Costly-to-reverse choices
- <choice> → needs a decision record (`decision`, meta plugin)
### Open design findings
- [blocking] <finding> | None
```

Post with the tracker's CLI, for example `gh issue comment <n> --body-file <file>`, after checking the text against the project's attribution and privacy rules.
