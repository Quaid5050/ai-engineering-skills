# Installation and agent-host adapters

Skill text/resources are portable. Plugin loading, hooks, roles and permissions are host-specific; verify the client's current discovery path and enforcement capabilities.

```bash
python3 scripts/install_skills.py /path/to/skills --plugins lifecycle,backend --dry-run
python3 scripts/install_skills.py /path/to/skills --plugins lifecycle,backend
python3 scripts/install_skills.py /path/to/skills --rollback
python3 scripts/install_skills.py /path/to/skills --recover
python3 scripts/install_skills.py /path/to/skills --uninstall
```

The shell wrapper calls the same implementation; Windows can call Python directly. Copy mode needs no symlink privilege. Filtered installation includes required dependencies; filtered uninstall removes only requested plugin skills and rejects removal still needed by retained skills.

Ownership/content digests live in `.ai-engineering-skills.json`. Foreign destinations and changed owned copies are preserved by refusing the operation. Keep consumer customizations separately. Link mode owns the link's target identity, not source contents: source updates are immediately visible, so only use trusted clones. Retargeting an owned link is detected.

Updates stage on the target filesystem and retain one rollback transaction. Flat skill directories may be partly updated during a crash: this is **recoverable, not a whole-directory atomic switch**. Stop readers and use `--recover`; it validates destinations, backup digests and metadata before restoring. OS advisory locking serializes installers, including recovery, and releases on process exit. Do not delete the persistent lock file while another installer can run. Process interruption is tested; power-loss durability and network-filesystem lock semantics are not guaranteed. An attacker able to rewrite all installation metadata is outside the ownership model.

## Roles and scope

Load context once and only relevant references. Required dependencies mean availability, not recursive loading of every workflow companion. Architect/reviewer are static read-only profiles; their tools must be mapped and enforced by the host. Tests/builds run separately in a disposable restricted environment without secrets. Without an independent agent/session, label review non-independent.

## Hooks

Command preflights recognize limited shell forms and are advisory. Aliases, direct APIs, disabled hooks and other tools can bypass them. Protected server checks and host permissions enforce real boundaries.

Standalone Git hooks scan the actual index:

```sh
python3 /path/to/ai-engineering-skills/plugins/guardrails/scripts/guard.py secrets --git-hook
python3 /path/to/ai-engineering-skills/plugins/guardrails/scripts/guard.py branch --git-hook
```

Git hooks are also bypassable. Known credential patterns, including staged binary blobs, are checked with redacted values and sensitive paths. This is not a complete secret detector; unstaged/untracked content is not the commit index.
