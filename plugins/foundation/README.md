# foundation 1.0.0

Shared task context, risk-based workflow and safe execution boundaries, without mandatory orchestration.

Install declared dependencies. Load only relevant skills/resources; required availability is not a recursive workflow.

| Skill | Purpose |
|---|---|
| [safe-agent-execution](skills/safe-agent-execution/SKILL.md) | Constrain agent access and handle untrusted content safely. Use when inspecting external repositories, running project commands, invoking tools or designing agent execution; not as a reason to block authorized read-only work. |
| [work-context](skills/work-context/SKILL.md) | Choose proportionate engineering steps and reuse current project context. Use when starting or resuming an engineering change; not for ordinary factual conversation. |
