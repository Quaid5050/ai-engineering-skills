# Contributing

Thanks for helping. The bar for a change here is: *would this rule have stopped a real mistake, on any stack?*

## What makes a good contribution

- **A lesson from real work** — a bug that passed every test, a review that missed something, a pattern an agent copied wrongly — turned into a check, gate or rule. Follow [docs/lessons.md](docs/lessons.md) and use the `capture-lesson` skill.
- **A stack reference** (`references/<stack>.md`) that maps the generic rules of a skill onto a stack's idioms, tools and commands.
- **A fix** to a step that is ambiguous, wrong or out of date.

Not wanted: rules nobody needed yet, framework names in core skill text, product-specific examples, long essays.

## How

1. Open an issue describing the problem (what went wrong, which skill, which rung should have caught it).
2. Branch: `docs/<short-slug>` or `feat/<short-slug>`.
3. Edit following [docs/skill-format.md](docs/skill-format.md). For a new or changed skill, run the fresh-agent dry run (`create-skill` §3) — on **two different stacks** for any core skill — and paste the gaps found and fixed in the PR.
4. Version and log it (below).
5. Run the checks:
   ```bash
   python3 -m pip install -r requirements-dev.txt
   python3 scripts/update_catalog.py
   python3 scripts/check.py
   python3 -m unittest discover -s tests -v
   claude plugin validate . --strict
   claude plugin validate plugins/<plugin> --strict
   ```
6. Open a PR with conventional commits (`docs(lifecycle): …`, `feat(mobile): …`). It is reviewed with the `code-review` skill, design pass included.

## Versioning (semantic, per plugin)

| Change | Bump |
|---|---|
| Wording, typo, clearer example, new stack reference | PATCH |
| New skill, new gate or check, new required step, new hook | MINOR |
| Removed or renamed skill or agent, a changed gate other skills rely on, a hook that now blocks more | MAJOR |

A bump changes three places, which CI checks agree: the plugin's `plugin.json` `version`, its entry in `.claude-plugin/marketplace.json`, and `metadata.version` in every `SKILL.md` of that plugin. Then add to [CHANGELOG.md](CHANGELOG.md):

```markdown
## <plugin> <version> — <YYYY-MM-DD>
- <what changed and why> (lesson: <link to docs/lessons.md entry>, if any)
```

## Privacy

This repository is public. Never commit names, emails, phone numbers, customer or product names, issue numbers or links from private projects, internal paths, tokens or keys. `scripts/check.py privacy` catches the common shapes; it is not a substitute for reading your diff.

## Code of conduct

Be kind, assume good intent, critique the text not the person.

## Evidence and support

Use the [evaluation rubric](docs/evaluation.md). Preserve historical audits. Fresh-agent dry runs on two stacks distinguish actual execution from simulated reasoning. Device/provider support requires appropriate execution evidence; host security boundaries require negative tests. Record owner, version, source and limits before promoting a support tier.
