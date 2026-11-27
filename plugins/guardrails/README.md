# guardrails 2.0.0

Opt-in advisory command preflight and actual-index Git checks. Host permissions and protected server-side checks remain the enforcement boundary.

The credential scanner reads staged blobs without textconv/filter helpers, redacts values and sensitive path names, and explicitly fails on unreadable/oversized blobs. It does not treat unstaged content as staged. Branch checking covers main/master, the discovered default branch and detached state; deliberate bootstrap overrides are explicit.

Preflight recognizes constrained direct commands, `git -C`, global config and simple directory changes. Unknown ambiguous commit forms fail rather than being guessed. Arbitrary shell semantics, aliases and other APIs are not enforceable by this hook.

Requires Python 3.10+; wrappers need Bash. See [host adapters](../../docs/other-agents.md) and [evaluation](../../docs/evaluation.md).
