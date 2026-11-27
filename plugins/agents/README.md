# agents 2.0.0

Independent roles with host-enforced scope. Install the declared foundation dependency and the relevant skills for the task.

| Role | Purpose |
|---|---|
| [Architect](agents/architect.md) | Independent, static design review when risk warrants it |
| [Reviewer](agents/reviewer.md) | Independent static review of the exact candidate and its design |
| [Tester](agents/tester.md) | Scoped test authoring; execution through a separately constrained runner |

Review roles have no general shell. Role text is not an execution sandbox; the host must enforce tools, paths, credentials and network limits. Return the report to the caller; posting it externally requires task authorization. See [host adapters](../../docs/other-agents.md).
