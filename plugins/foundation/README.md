# foundation 1.0.0

Shared task context: picks the Quick, Standard or Structural/High-risk tier once per task, keeps a task card so nothing is re-read, briefs subagents with a digest, and sets safe execution boundaries.

Install declared dependencies. Load only relevant skills/resources; required availability is not a recursive workflow.

| Skill | Purpose |
|---|---|
| [safe-agent-execution](skills/safe-agent-execution/SKILL.md) | Constrain agent access and handle untrusted content safely. Use when inspecting external repositories, running project commands, invoking tools or designing agent execution; not as a reason to block authorized read-only work. |
| [work-context](skills/work-context/SKILL.md) | Pick the right amount of process for an engineering change and reuse what is already known. Classifies the task Quick, Standard or Structural/High-risk with concrete triggers, says which steps, reviews, subagents and test runs each tier gets, keeps a short task card so nothing is re-read, and briefs subagents with a digest instead of whole skills. Use at the start or resumption of any code change. Trigger on 'how much process', 'is a design review needed', 'quick fix', 'small change', 'why is this so slow', 'risk tier'. |
