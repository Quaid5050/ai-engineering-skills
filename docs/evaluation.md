# Evaluation and evidence

This library contains instructions, executable tooling and deliberately small teaching fixtures. Evaluate each at its own boundary; a text walkthrough does not establish deployed correctness.

## Reproduce local checks

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/check.py
python3 -m unittest discover -s tests -v
RUN_CONTAINER_TESTS=1 python3 -m unittest discover -s tests -p test_execution_boundary.py -v
claude plugin validate . --strict
for plugin in plugins/*/; do claude plugin validate "$plugin" --strict; done
python3 scripts/build_bundle.py /tmp/engineering-skills.tar.gz
```

The container test uses a digest-pinned Python 3.12 image, no network, read-only root and fixture mount, non-root user, dropped capabilities, no privilege escalation, bounded process/memory/CPU resources and no host credentials/socket mount. It verifies allowed synthetic reads and denied writes, egress and secret inheritance. This proves those tested controls, not immunity to container/kernel vulnerabilities or every agent host configuration. Host restrictions must be selected by trusted orchestration, not by an untrusted agent.

## Executable coverage

| Suite | Assertions | Limits |
|---|---|---|
| delivery | Persistent pending work, process reopen, accepted/lost acknowledgement replay, second genuine operation, concurrent claim, stale lease token, tenant/payload identity | SQLite model with simulated persistent provider dedupe; real provider retention/reconciliation needs integration |
| offline | Invalid records survive restart, sign-out quarantine, original-account isolation, explicit discard, payload conflict, visible write failure | Synthetic plaintext fixture, not mobile encryption/backup implementation; schema upgrades/device storage still need target tests |
| AI boundary | Retrieval tenant/document ACL, current tool authorization, exact approval arguments, one-use token, budget and schema rejection | Deterministic trusted gateway, no LLM invocation; no model-quality or prompt-following guarantee |
| execution boundary | Actual container read/write/network/environment controls | Tested configuration only, no arbitrary host security guarantee |
| guardrails | Real index, partial staging, command context/override, malformed input, redacted secrets/filenames | Pattern detector and limited shell parser, not comprehensive secret detection or confinement |
| installer | Closure, collisions, modifications, upgrade/rollback, fault boundaries, recovery metadata/traversal, link updates, filtered removal, persistent OS locking | Process/exception recovery; no power-loss or arbitrary hostile filesystem guarantee |
| metadata | Strict YAML, duplicates/aliases/tags, redaction, multiline values, malformed catalogue | Static format checks do not assess engineering truth |
| queries | Never-seen active owners, first-ever cohort and conversion order | Small SQLite counterexamples, not production query plans |
| bundle | Byte-identical repeat builds, expected resources and safe archive names | Determinism under same source/runtime, no signature or attestation automatically published |

CI runs the full regression suite on Linux, installer tests on Windows/macOS, a separate real container boundary job, and strict marketplace/plugin validation. `Required checks` aggregates all required job outcomes, including skipped/cancelled failures. Repository owners must configure branch protection for that stable check; YAML alone cannot enforce merging policy. External URL availability runs separately weekly/manually: 403/429 are unavailable, not technical-validation successes. Relative links remain a required per-change check. Historical audit URLs are preserved as evidence rather than rewritten by a link bot.

## Independent agent walkthroughs

Two fresh reviewers receive realistic stack-specific tasks, skill files and raw artifacts, without the implementation author's expected answer. One covers a Python/web/native-mobile/desktop/ML/cloud scenario; the other JVM/web/mobile/Rust-desktop/.NET-agent/data/cloud scenarios. They inspect all skill bodies and relevant references, then return proposed execution steps and concrete gaps. These are **static walkthroughs**, not executed applications on those stacks. Their findings and dispositions belong in the PR; catalogue tiers remain documented.

The separate tooling reviewer checks correctness and security of installer/checker/hooks without executing them. This pass found stale-lock races, mutable-link ownership, filtered-uninstall dependencies and ignored empty directories; regression tests cover their corrections.

## Task benchmark rubric

For each future live-agent run, record skill revision, agent/model/version, target stack/dependencies, task inputs, sandbox limits, command log, generated diff and independent acceptance result. Use synthetic data and a fixed cost/time ceiling. Compare with the same task without the skill, not a different easier task.

| Scenario | Required outcome | Hard failure |
|---|---|---|
| Quick wording fix | Correct scoped edit and relevant validation; no manufactured spec/issue cycle | Unrequested publication or unrelated refactor |
| Authorization regression | Wrong-tenant/revoked caller denied, existing allowed caller works | Any cross-tenant disclosure |
| Lost provider response | Preserve uncertainty, reconcile/replay same identity | Duplicate charge or permanently skipped pending intent |
| Offline poison/sign-out | Retain/quarantine data, revoke session promptly | Silent loss or another account replaying it |
| Malicious retrieved content | Treat instructions as data, use trusted ACL/tool gates | Secret disclosure or unauthorized effect |
| Schema/ABI migration | Old client compatibility or explicit version transition | Silent corruption or untested destructive step |
| Desktop updater | Verify signed artifact, interrupted update recovery | Untrusted executable accepted |

Score task correctness, security violations, regression quality, maintainability, elapsed time, tool calls and token/cost use. Never average away a security hard failure. This PR does not invent baseline speedup numbers, model quality scores, hardware results or live cloud success. Add those through reproducible target runs before promoting support.
