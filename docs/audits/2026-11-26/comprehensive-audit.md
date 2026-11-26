# Comprehensive AI Engineering Skills Audit and Improvement Plan

Repository: [Quaid5050/ai-engineering-skills](https://github.com/Quaid5050/ai-engineering-skills/). Audit date: 26 November 2026. Audited commit: [`4dab7293821283e30bee7d7f3814c10e8ee72f2a`](https://github.com/Quaid5050/ai-engineering-skills/tree/4dab7293821283e30bee7d7f3814c10e8ee72f2a).

## A. Executive Summary

**Overall assessment: a useful, unusually coherent engineering workflow collection, but not yet a production-grade, general-purpose engineering skills library.** Its strengths are practical lifecycle orchestration, explicit evidence requirements, failure-path thinking, mobile operating constraints, and attention to data isolation. Its weaknesses are incorrect reliability guarantees, incomplete enforcement, overly prescriptive architecture and testing rules, untested cross-skill composition, and major capability gaps outside conventional web/mobile application work.

The highest-value next step is to correct and prove the existing core before expanding the catalogue. Adding hundreds of framework-specific skills would multiply the current maintenance and consistency problems.

### Scope and evidence

The audit covered **all 127 tracked files, 7,925 lines, 51 skills, 38 supporting references, three agent roles, eight plugin packages, and all repository documentation, manifests, hooks, installation scripts and CI files**. It examined the pinned tree rather than treating the README as a proxy. A companion file inventory records every path, line count and SHA-256. Every tracked file's contents were compared with its Git object after the audit; all matched. No repository files were modified.

The review combined file-by-file analysis, cross-reference and workflow analysis, local validation, isolated behavioral probes, and checks against primary technical documentation. Findings below use these distinctions:

- **Verified defect:** directly present in the text/code, or reproduced by a local probe. An incorrect instruction is a defect even if no downstream application has yet implemented it.
- **Coverage gap:** the tree lacks an adequate procedure or reference. This does not establish that its maintainers lack the expertise.
- **Recommendation:** an engineering judgment about the desired library, not a claim of an observed exploit or production incident.
- **Unverified:** execution or external state that the available evidence cannot establish.

Validation results:

| Check | Result and meaning |
|---|---|
| `python3 scripts/check.py` | All six groups passed: manifests, skills, agents, links, framework vocabulary, privacy. These are structural/content checks, not proof of technical correctness. |
| Strict Claude plugin validation | Marketplace plus all eight plugins passed using installed Claude Code 2.1.285. |
| Shell parsing | Installer and all three guardrail scripts passed `bash -n`. |
| Isolated behavioral probes | Fourteen probes covered normal hook behavior, hook bypasses, malformed input, installation collisions/updates/dependencies, frontmatter parsing, and a model of the documented notification algorithm. Details are in B and D and the evidence JSON. |
| Repository integrity | All 127 tracked files still matched the audited commit. |

**Limits:** this was not a penetration test of a deployed product. No production database, real device fleet, cloud account, complete historical secret scan, or full external-link sweep was exercised. Framework snippets were reviewed against their context and documentation, not compiled as applications: the repository supplies no executable application fixture projects for them. No controlled agent-versus-baseline evaluation was performed. The changelog describes prior fresh-agent dry runs, but the audited tree does not contain reproducible traces, fixture snapshots and scored results sufficient to independently verify those claims. Remote branch protections and actual hosted CI results were not established by local checks.

### Existing strengths

1. **A connected lifecycle:** investigation, specifications, issues, implementation, reviews, CI, deployment, release, observation and incidents are connected rather than isolated prompts.
2. **Concrete production concerns:** idempotency, revoked access, old clients, migration locks, background execution, offline persistence, queue failures, staged release and rollback receive real attention.
3. **Useful test discipline:** observable behavior, synthetic data, real database integration, failure paths, controlled clocks and proof that important tests detect defects are sound foundations.
4. **Good writing structure:** consistent project discovery, phased procedures, gates and composition tables make skills easier to follow. References separate much stack-specific detail.
5. **Healthy operating instincts:** explicit authorization for shared databases, limited output of sensitive data, hosted CI for public PRs, least-privilege default CI permissions, and honest reporting of tests not run.

### Major weaknesses and opportunities

- **Dangerous reliability guidance:** inserting a sent-ledger row before sending and treating any duplicate as delivered can permanently lose notifications. Offline-queue instructions disagree about retaining versus dropping invalid records.
- **Incomplete security boundaries:** commit hooks can miss ordinary Git command forms or inspect the wrong repository; other secret checks print matched sensitive text. Reviewer roles can run arbitrary repository code through Bash despite being described as read-only.
- **Unproven effectiveness:** the library validates prose shape but has no committed behavioral regression suite for its own scripts, examples or agent workflows.
- **Universal rules that are not universal:** mandatory clean/onion layers, hypothetical future reuse, only literal test values, one action per test and an index for every query clause can produce worse engineering decisions.
- **Workflow and dependency contradictions:** required deployment verdicts are demanded before the prescribed deployment step; plugin dependencies do not fully represent actual skill composition; copy installation does not provide an upgrade path.
- **Uneven breadth:** web, backend and mobile application workflows dominate. LLM product engineering, RAG, agent security, ML/data pipelines, desktop engineering, systems programming, cloud/IaC, database operations and comprehensive test strategy need substantial work.

A credible differentiator would be **small, composable procedures backed by executable examples, versioned platform adapters, adversarial evaluations and traceable acceptance evidence**. Breadth should be an outcome of this architecture, not the number of folders.

## B. Existing Skills Audit

Priority describes the most important change to that skill, not its overall quality. **P0** means immediate correction of credible security/data-loss guidance or a foundational safety boundary; **P1** means essential reliability, correctness or maintainability; **P2** means breadth and refinement; **P3** means later optimization. R identifiers point to the actionable roadmap in G. Paths below are relative to the pinned repository; skill names link to their source files.

### Lifecycle plugin — all 24 skills

| Skill | What is useful and correct | Problems and specific improvement | Priority / roadmap |
|---|---|---|---|
| [shape-idea](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/lifecycle/skills/shape-idea/SKILL.md) | Separates the problem, users, assumptions, MVP and outcomes. | Extend discovery to evidence quality, operational cost and non-app products such as libraries, CLI tools and data services. State how to reject an unsupported premise instead of always progressing toward implementation. | P2 · R06, R17 |
| [bootstrap-project](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/lifecycle/skills/bootstrap-project/SKILL.md) | Establishes real commands, conventions, architecture checks and initial CI. | App/backend-oriented scaffolding needs explicit product profiles. Add threat boundaries, reproducible toolchain setup and a minimum viable bootstrap; avoid installing every process gate before a small project can begin. | P1 · R05, R06, R10 |
| [investigate-feature](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/lifecycle/skills/investigate-feature/SKILL.md) | Reads actual code/designs, identifies missing facts and produces a build pack. | Clarify provenance and treatment of hostile external instructions; separate discovered facts from suggested designs. Permit investigation without first generating unnecessary tracker/document artifacts. | P1 · R04, R06 |
| [spec](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/lifecycle/skills/spec/SKILL.md) | Includes failure modes, state, budgets, compatibility and rollout. | Add explicit trust boundaries, quantitative capacity/SLO assumptions and alternative designs. Clarify provisional epic creation before the approved breakdown; the exception is present but distributed across procedures. Use one review state machine. | P1 · R06, R07, R12 |
| [feature-to-issues](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/lifecycle/skills/feature-to-issues/SKILL.md) | Promotes vertical slices, risk-first sequencing and acceptance evidence. | Support dependency graphs, discovery spikes, migration prerequisites and infrastructure/library enablers; not every valuable change is a user-facing vertical slice. Check cycles and ownership. | P2 · R06, R17 |
| [file-feature](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/lifecycle/skills/file-feature/SKILL.md) | Produces a useful implementation contract with acceptance criteria and test expectations. | Add duplicate search, explicit N/A for irrelevant UI sections, and a shorter template for bounded changes. Avoid treating every issue as a product-screen design task. | P2 · R06 |
| [file-bug](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/lifecycle/skills/file-bug/SKILL.md) | Captures symptoms, reproduction, impact and sanitized evidence. | Reuse authorization already granted when asked to file a bug; reserve preview approval for uncertain scope or recipients. Add duplicate search and distinguish severity from scheduling priority. | P2 · R06 |
| [start-issue](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/lifecycle/skills/start-issue/SKILL.md) | Keeps unrelated changes separate and makes the implementation plan explicit. | Shell fallback can conceal failed parent lookup as absent parent. Distinguish not-found from authentication/network failure. Bind the plan/review to a revision and support repository default branches and merge-queue workflows. | P1 · R06, R07 |
| [design-review](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/lifecycle/skills/design-review/SKILL.md) | Checks placement, reuse, risks, contract and testability before expensive work. | Requiring a reusable generic component because a hypothetical next feature might need one encourages premature abstraction. Judge alternatives, concrete reuse and reversibility. Define acceptable reviewer independence and fallback evidence consistently. | P1 · R06, R07 |
| [engineering-principles](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/lifecycle/skills/engineering-principles/SKILL.md) | Cohesion, explicit boundaries, validated configuration, concurrency invariants and ADRs are valuable. | Rewrite universal clean/onion placement rules as defaults with applicability tests. Parsing/crypto can be a product's domain. In-process interfaces can be useful. Fix sent-ledger propagation, arbitrary size thresholds and the demand that every code kind fit the table. | P0 for delivery rule; otherwise P1 · R01, R06 |
| [new-feature](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/lifecycle/skills/new-feature/SKILL.md) | Gives agents a single entry point and preserves lifecycle evidence. | A docs issue/PR, mandatory slice design review and separate gates for every small change impose substantial overhead. Its review-before-deploy sequence conflicts with required review verdicts. Route by risk, artifact and scope; share one gate definition. | P1 · R06, R07 |
| [implement](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/lifecycle/skills/implement/SKILL.md) | Connects the plan, test-first work, companion skills and verification. | Maintenance restrictions on changing tests are too broad for legitimate refactors and dependency migrations. Reverting every red increment is not a universal debugging strategy. Add scoped recovery, checkpoint and exception rules. | P1 · R06, R08 |
| [bugfix](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/lifecycle/skills/bugfix/SKILL.md) | Reproduction, regression, blast radius and existing-data repair receive attention. | Add a controlled route for intermittent or non-reproducible incidents: instrumentation, characterization, mitigation, hypothesis confidence and follow-up. Determine required design review by risk, not just change count. | P1 · R06, R08, R12 |
| [investigate-bug](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/lifecycle/skills/investigate-bug/SKILL.md) | Emphasizes evidence before changes and preventing the broader defect class. | A minimum of five hypotheses and fixed five-whys reasoning can manufacture work or causal certainty. Use the smallest discriminating experiment, causal graphs, bisection, traces and explicit unresolved causes. | P1 · R08, R12 |
| [pre-commit](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/lifecycle/skills/pre-commit/SKILL.md) | Named-path staging and generated-code synchronization reduce accidental commits. | Grep commands print complete matching diff lines, including secrets and personal data. Checks may validate the working tree rather than the staged snapshot. Use redacted scanners and validate the actual commit candidate. | P0 · R03; P1 · R07 |
| [create-pr](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/lifecycle/skills/create-pr/SKILL.md) | Requires meaningful evidence, preserves existing PR context and uses body files. | Make optional versus blocking findings consistent across review and merge. Capture head SHA and required evidence without circular dependencies on a later deploy step. | P1 · R07 |
| [ci](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/lifecycle/skills/ci/SKILL.md) | Reads actual failures, requires applicable checks and discourages rerunning until lucky. | The example lacks required PR-file permissions, misses some cross-area changes and lacks an explicit aggregate gate. Support merge groups and distinguish flaky infrastructure from product failures. | P1 · R07, R10 |
| [deploy-check](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/lifecycle/skills/deploy-check/SKILL.md) | Correctly considers old clients, data transitions, configuration and scheduling. | Additive schema/API changes can still break exhaustive clients or change semantics. Replace sent-ledger and singleton assumptions with explicit delivery/coordination models. Bind verdict to the candidate and environment. | P0 for delivery rule; P1 otherwise · R01, R07 |
| [merge](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/lifecycle/skills/merge/SKILL.md) | Requires more than green unit tests: reviews, evidence and applicable release readiness. | Comment headings and timestamps are weak proof of review provenance; Git author dates are mutable. Revalidate the exact head atomically and support merge queues. Resolve exception-policy differences between skills. | P1 · R07 |
| [release](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/lifecycle/skills/release/SKILL.md) | Staging, rollout monitoring, old-client compatibility and rollback are strong. | Pin provider/runtime/store rules. CodePush guidance does not distinguish retired App Center hosting from maintained alternatives. OTA policy is oversimplified; the Play privacy-policy requirement is understated. | P1 · R11 |
| [observe](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/lifecycle/skills/observe/SKILL.md) | Low-cardinality signals, failure alarms and delivery visibility are good. | Replace absolute delivery promises with measurable SLOs and uncertainty states. Add traces, burn-rate alerts, dependency health, diagnostic retention and runbook ownership. | P1 · R01, R12 |
| [incident](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/lifecycle/skills/incident/SKILL.md) | Correctly prioritizes containment, evidence and follow-up. | Make urgent authorized mitigation possible before ordinary issue/review ceremony. Add incident roles, communication cadence, evidence preservation, credential compromise and restoration verification. | P1 · R04, R12 |
| [postmortem](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/lifecycle/skills/postmortem/SKILL.md) | Blameless analysis and owned preventive work are useful. | Use causal contributors rather than a compulsory linear chain. Verify that action items reduce recurrence; do not equate earlier detection with universally cheaper prevention. | P2 · R12, R17 |
| [cleanup](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/lifecycle/skills/cleanup/SKILL.md) | Protects dirty worktrees and persistent volumes; scopes cleanup. | Verify ownership and merged content before branch/worktree removal, handle multiple worktrees and symlinks, and separate safe cleanup from destructive reset. A blanket stash prohibition can be a project preference, not a universal rule. | P2 · R06, R09 |

### Backend plugin — all six skills

| Skill | What is useful and correct | Problems and specific improvement | Priority / roadmap |
|---|---|---|---|
| [add-endpoint](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/backend/skills/add-endpoint/SKILL.md) | Contract-first design, caller isolation, revoked-access tests, stable errors and generated-client checks. | Its entry scope includes protocols that its REST-specific rules do not cover. Add protocol adapters. Idempotency needs payload-fingerprint mismatch behavior, tenant/caller scoping, in-flight handling, authorization on replay and concurrency tests. | P1 · R01, R13 |
| [add-file-upload](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/backend/skills/add-file-upload/SKILL.md) | Byte-based type checks, bounded streaming, private storage, random names, attachment completion and orphan cleanup. | Re-encoding is not a complete malware/parser defense. Immediate access revocation conflicts with valid bearer URLs. Add quarantine, parser resource limits, safe serving headers/origins and immutable object/version/checksum confirmation to avoid post-scan overwrites. | P0 for security guarantees · R03, R13 |
| [add-migration](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/backend/skills/add-migration/SKILL.md) | Expand/migrate/contract, reading SQL, bounded backfills, duplicate repair and lock awareness. | Blanket indexing and table-rewrite claims are inaccurate. PostgreSQL does not permit a UNIQUE constraint to be added NOT VALID in the suggested sense. Separate engine/version-specific DDL capabilities and scans from rewrites. Test representative data and concurrent writers. | P1 · R13 |
| [add-scheduled-job](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/backend/skills/add-scheduled-job/SKILL.md) | Rechecks access, owns retries, considers DST, claims work and measures lag. | The insert-before-send/duplicate-means-sent algorithm loses work on a pre-send crash. Rewrite around durable pending state, leases, recovery, provider idempotency and uncertain outcomes. One physical scheduler is not universally required. | P0 · R01 |
| [backend-conventions](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/backend/skills/backend-conventions/SKILL.md) | Cohesive boundaries, transaction ownership, tenancy, typed configuration and outbox awareness. | Layering and type/file rules overgeneralize across languages. Centralized technical services may become excessive coupling. Domain invariants remain necessary after edge validation. Reconcile safer outbox advice with the scheduler guidance. | P1 · R01, R06, R13 |
| [data-check](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/backend/skills/data-check/SKILL.md) | Read-only roles, per-session timeouts, aggregates, expected cohorts and controls are valuable. | Freshness SQL excludes owners with no recent events, hiding the worst outages. Index use is not itself correctness. IDs and coarse buckets can remain sensitive. Make EXPLAIN ANALYZE execution and read-only side-effect limitations explicit. | P1 · R03, R13 |

### Mobile plugin — all seven skills

| Skill | What is useful and correct | Problems and specific improvement | Priority / roadmap |
|---|---|---|---|
| [background-work](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/mobile/skills/background-work/SKILL.md) | Recognizes OS constraints, durable state, user-visible failure and real-device testing. | Do not promise exact scheduling or an observable reason for every OS termination. Define unknown/interrupted states and freshness bounds; distinguish force-stop, user termination, crashes and OS eviction. Validate by OS and target SDK. | P1 · R11 |
| [offline-queue](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/mobile/skills/offline-queue/SKILL.md) | Permanent record identities, backoff, restart durability, attachment coordination and explicit loss policy. | Design retains invalid records for user recovery, while tests require dropping them. Reconcile retention with no-loss requirements. Add account separation, durable-write failure semantics, conflict/tombstone behavior and safe sign-out with quarantined encrypted pending data. | P0 · R02; P1 · R13 |
| [shared-core](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/mobile/skills/shared-core/SKILL.md) | Isolates portable logic and uses cross-language test vectors. | Its allowance for encoding conflicts with domain placement rules elsewhere. Foreign-boundary exception and panic behavior needs ABI/compiler-specific detail. Do not flatten all errors to null/false; preserve typed diagnostics and cancellation. | P1 · R06, R11, R16 |
| [mobile-conventions](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/mobile/skills/mobile-conventions/SKILL.md) | Lifecycle-aware state, cancellation, localization and migration concerns are practical. | One view/one view-model and no repository dependencies are architectural preferences, not universal platform rules. Add Swift concurrency isolation, Kotlin structured concurrency and modern React Native diagnostics with tested versions. | P2 · R06, R11, R16 |
| [design-to-screen](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/mobile/skills/design-to-screen/SKILL.md) | Tokens, states, design evidence, screenshots and accessibility are integrated. | Adapt to a one-platform scope and existing design systems. Do not force every dimension into a token or every small visual change through an additional design approval. Provide meaningful reduced-motion alternatives. | P2 · R06, R16 |
| [home-widget](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/mobile/skills/home-widget/SKILL.md) | Versioned snapshots, stale-data handling and privacy clearing are strong concerns. | A timer-driven worker cannot guarantee exact stale UI updates under OS throttling. Specify platform-supported timeline/rendering behavior and visible last-update information; recheck auth on actions and clear shared stores on sign-out. | P1 · R11 |
| [device-test](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/mobile/skills/device-test/SKILL.md) | Real release builds and explicit unrun tests are better evidence than simulator-only claims. | Build a risk-based supported-device/OS matrix, including upgrades and old supported OS versions. Disk-full/clock-change tests need recovery steps; battery measurements need a baseline, controlled conditions and repeated samples. | P2 · R08, R11 |

### Quality plugin — all eight skills

| Skill | What is useful and correct | Problems and specific improvement | Priority / roadmap |
|---|---|---|---|
| [testing-doctrine](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/quality/skills/testing-doctrine/SKILL.md) | Observable behavior, boundary fakes, real DB integration, deterministic clocks and mutation-style proof of important assertions. | Literal-only inputs, no loops/randomness and exactly one action reject valid property, state-machine, concurrency and idempotency tests; supplied references themselves sometimes use multiple calls. Replace delete-or-fix flakiness with bounded quarantine and restored coverage. | P1 · R08 |
| [tdd](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/quality/skills/tdd/SKILL.md) | A clear red/green/refactor procedure with some non-code exceptions. | Distinguish new behavior from characterization, experiments, generated changes and integration-only behavior. Require meaningful failure evidence without forcing an artificial red test for every edit. | P2 · R08 |
| [write-tests](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/quality/skills/write-tests/SKILL.md) | Concrete commands and framework references, failure paths and actual DB boundaries. | Add test-strategy selection, contract/compatibility tests, browser E2E, property/fuzz/concurrency tests and fixture projects. Test success must be tied to the relevant source revision and environment. | P1 · R05, R08 |
| [security-privacy-review](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/quality/skills/security-privacy-review/SKILL.md) | Strong attention to coercion, sharing, isolation, sensitive logs, consent and API abuse. | Needs verifiable control mappings and dedicated auth, threat-model, dependency, cryptography, SSRF and AI-tool procedures. Pseudonymous identifiers are not automatically non-personal. Include privileged execution and egress boundaries. | P0 for agent boundary · R04; P1 · R03, R10, R14 |
| [analytics-event](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/quality/skills/analytics-event/SKILL.md) | Purpose, consent, typed allowlists, retention and event-schema discipline. | Stable hashes are linkable pseudonyms. Purge or block queued events after consent withdrawal. Conversion SQL must ensure events follow the cohort event and distinguish true first-ever events from first observed in-window events. | P1 · R03, R13, R15 |
| [accessibility-audit](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/quality/skills/accessibility-audit/SKILL.md) | Keyboard, screen readers, focus, contrast, scaling, RTL and platform tools. | It is not a complete WCAG conformance assessment. Map applicable criteria and evidence, including focus obscuration, dragging alternatives, redundant entry and accessible authentication. Separate native guidance and manual checks from automated scan coverage. | P1 · R08, R16 |
| [perf-check](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/quality/skills/perf-check/SKILL.md) | Budgets, before/after measurements and profiler-led changes discourage guesswork. | Three medians do not establish tail latency or reliability. Local lab measurements are useful despite a blanket prohibition. Add workload models, percentiles, variance, saturation and arrival-rate tests; reconcile examples with the stated pacing rule. | P1 · R08, R12 |
| [code-review](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/quality/skills/code-review/SKILL.md) | Detailed dimensions, separate design consideration, ranked findings and evidence checking. | Deployment-verdict timing conflicts with orchestration. Review headings are not authentication. A new-commits-only re-review can miss interactions with the whole change. Preserve read-only scope and use isolated execution for untrusted tests. | P1 · R04, R06, R07 |

### Web plugin — all three skills

| Skill | What is useful and correct | Problems and specific improvement | Priority / roadmap |
|---|---|---|---|
| [web-conventions](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/web/skills/web-conventions/SKILL.md) | Typed APIs, explicit UI states, semantic HTML, CSRF awareness, localization and performance budgets. | Blanket inline-script rules conflict with framework output and safe nonce/hash CSP. JSON-LD needs safe serialization. Next font and Astro bundling claims need correction; server-component architecture needs a coherent adapter. | P1 · R11, R16 |
| [add-web-page](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/web/skills/add-web-page/SKILL.md) | Progressive content, keyboard behavior, accessibility checks and screenshots. | Output checks can reject valid framework-generated inline scripts or ordinary external hyperlinks. Verify actual network requests and deployed HTTP headers, not just a headers file. Adapt tokens/content checks to the project. | P1 · R11, R16 |
| [build-web-screen](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/web/skills/build-web-screen/SKILL.md) | Covers loading/error/empty states, forms, auth, duplicate submissions and server-state caching. | Define tenant/user-sensitive cache keys, session-switch invalidation and private-data cache policy. Add framework-specific server/client boundaries and independent authorization for server-side actions. | P1 · R13, R16 |

### Meta plugin — all three skills

| Skill | What is useful and correct | Problems and specific improvement | Priority / roadmap |
|---|---|---|---|
| [capture-lesson](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/meta/skills/capture-lesson/SKILL.md) | Converts observed failures into durable checks, preserves installed caches and distinguishes upstream proposals. | Some example generalizations are not universal: all parsing outside domain, empty baselines everywhere, speculative generic storage. Add applicability, counterexamples and effectiveness review. Prevention is not a single ordered ladder. | P1 · R05, R06, R17 |
| [create-skill](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/meta/skills/create-skill/SKILL.md) | Researches real commands, checks overlap, composes existing skills and asks for fresh-context dry runs. | Convert dry-run advice into reproducible eval fixtures with routing negatives, artifacts and scores. Clarify changed-contract versioning, portability fields and existing authorization. Vocabulary bans are weaker than semantic scope checks. | P1 · R05, R09, R17 |
| [decision](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/meta/skills/decision/SKILL.md) | Records real alternatives, costs, consequences and revisit triggers; preserves superseded records. | Keep short ADRs, but permit evidence appendices for complex decisions. Number allocation needs concurrent-author handling. Acceptance should reflect the project's decision authority rather than merge alone in every organization. | P2 · R06, R17 |

### All 38 supporting reference files

References are not executable demonstrations merely because they contain commands. Each needs a named owner, supported version range, official sources, a last-verified date and at least a minimal fixture where practical. Entries below identify what to retain and what specifically to improve; no reference was excluded from the read.

| Reference path within `plugins/` | Assessment and required change | Priority |
|---|---|---|
| [backend/skills/add-scheduled-job/references/stacks.md](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/backend/skills/add-scheduled-job/references/stacks.md) | Useful runner comparison; SQL repeats the unsafe sent-ledger algorithm. Distinguish scheduler leadership from worker concurrency. `on_commit` alone does not provide crash-durable publication. | P0 |
| [backend/skills/backend-conventions/references/django.md](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/backend/skills/backend-conventions/references/django.md) | Useful ORM, transaction and query guidance. Add executable concurrency/outbox examples; make architecture a supported profile rather than a compulsory Django rewrite. | P1 |
| [backend/skills/backend-conventions/references/dotnet.md](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/backend/skills/backend-conventions/references/dotnet.md) | Useful DI, EF and project-boundary examples. Add cancellation propagation, realistic transaction isolation and provider-specific migration fixtures; avoid one-type/one-layer as a universal requirement. | P1 |
| [backend/skills/backend-conventions/references/node.md](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/backend/skills/backend-conventions/references/node.md) | Useful validation, async and data access conventions. Add runnable package/toolchain versions, cancellation/timeouts and graceful shutdown; distinguish process termination from a missing logged diagnosis. | P1 |
| [backend/skills/backend-conventions/references/spring.md](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/backend/skills/backend-conventions/references/spring.md) | Useful transaction/proxy and persistence concerns. Test proxy boundaries, lock behavior and rollback; compare idiomatic Spring approaches rather than prescribing an identical structure to other stacks. | P1 |
| [lifecycle/skills/bootstrap-project/references/agents-md-template.md](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/lifecycle/skills/bootstrap-project/references/agents-md-template.md) | Good operational context template. Add trust boundaries, command risk, supported platforms and risk-scaled gates; keep facts separate from policy and never grant new authority through repository text. | P1 |
| [lifecycle/skills/bootstrap-project/references/labels.md](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/lifecycle/skills/bootstrap-project/references/labels.md) | Useful starter taxonomy. Make it optional and map to existing trackers rather than creating a second competing label system. | P2 |
| [lifecycle/skills/ci/references/github-actions.md](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/lifecycle/skills/ci/references/github-actions.md) | Good hosted-runner and permission instincts. Fix PR-file read permission, dependency-aware paths, stable aggregate gate, immutable pins and merge-group support. | P1 |
| [lifecycle/skills/engineering-principles/references/architecture-tests.md](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/lifecycle/skills/engineering-principles/references/architecture-tests.md) | Import-boundary checks are useful mechanical enforcement. They do not prove semantic placement or all runtime dependency paths. Add runnable fixtures and documented legacy-baseline ratcheting. | P1 |
| [lifecycle/skills/engineering-principles/references/design-patterns.md](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/lifecycle/skills/engineering-principles/references/design-patterns.md) | Useful pattern selection intent. Remove clean/onion as an always-applicable choice; add tradeoffs, concrete forces and examples where a simpler architecture wins. | P1 |
| [lifecycle/skills/engineering-principles/references/placement-table.md](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/lifecycle/skills/engineering-principles/references/placement-table.md) | Useful stack mapping, but mirrors policy elsewhere and cannot cover every product domain. Generate shared rule content or reference its canonical owner. | P1 |
| [lifecycle/skills/release/references/backend-deploy.md](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/lifecycle/skills/release/references/backend-deploy.md) | Strong expand/contract and drain guidance. Correct deduplication semantics, test interrupted deploys and distinguish application rollback from data restoration. | P0 delivery correction; P1 remainder |
| [lifecycle/skills/release/references/mobile-stores.md](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/lifecycle/skills/release/references/mobile-stores.md) | Useful actual store release/rollback differences. Correct Play privacy scope, clarify CodePush hosting and provider-specific OTA rules; reverify eligibility/signing requirements on each release. | P1 |
| [mobile/skills/background-work/references/android.md](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/mobile/skills/background-work/references/android.md) | Meaningful OS/target-SDK guidance, not merely old generic advice. Add explicit unsupported execution guarantees and a versioned device matrix; distinguish force-stop from other termination. | P1 |
| [mobile/skills/background-work/references/flutter.md](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/mobile/skills/background-work/references/flutter.md) | Useful native-versus-cross-platform boundary. Test plugin registration, isolates, cancellation and platform return semantics in a runnable fixture. | P2 |
| [mobile/skills/background-work/references/ios.md](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/mobile/skills/background-work/references/ios.md) | Correctly treats background modes as constrained. Specify which APIs can relaunch under which conditions; avoid one blanket rule for user termination. Validate entitlements and real devices. | P1 |
| [mobile/skills/home-widget/references/android.md](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/mobile/skills/home-widget/references/android.md) | Shared snapshot and update guidance is useful. WorkManager is inexact; test stale presentation and reboot/account-change behavior without assuming an exact refresh. | P1 |
| [mobile/skills/home-widget/references/ios.md](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/mobile/skills/home-widget/references/ios.md) | WidgetKit/App Group separation is appropriate. Add timeline budget limitations, protected-data access and privacy-clearing tests across app/widget versions. | P1 |
| [mobile/skills/mobile-conventions/references/flutter.md](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/mobile/skills/mobile-conventions/references/flutter.md) | Useful state, repository and testing conventions. Provide options compatible with established state-management choices; add migration and platform-channel fixtures. | P2 |
| [mobile/skills/mobile-conventions/references/kotlin.md](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/mobile/skills/mobile-conventions/references/kotlin.md) | Useful coroutine/state and modular boundaries. Support justified repository composition and test cancellation, lifecycle collection and dispatcher ownership. | P2 |
| [mobile/skills/mobile-conventions/references/react-native.md](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/mobile/skills/mobile-conventions/references/react-native.md) | Useful native/JS boundaries and performance concerns. Version the diagnostics guidance; verify Flipper applicability rather than recommending it generically for current projects. | P2 |
| [mobile/skills/mobile-conventions/references/swift.md](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/mobile/skills/mobile-conventions/references/swift.md) | Useful SwiftUI state and platform boundaries. Add compiler-checked actor isolation/Sendable examples and avoid assuming a view-model layer is always required. | P2 |
| [mobile/skills/shared-core/references/kmp.md](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/mobile/skills/shared-core/references/kmp.md) | Valuable native interop and portable test-vector concerns. Distinguish deliberate `@Throws` bridging from unhandled exceptions; specify export mode, coroutine cancellation and supported compiler versions. | P1 |
| [mobile/skills/shared-core/references/other-cores.md](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/mobile/skills/shared-core/references/other-cores.md) | Useful Rust/C++/other interop starting point. `catch_unwind` cannot catch aborting panics; document ABI, ownership, allocator, error and cancellation contracts. | P1 |
| [quality/skills/accessibility-audit/references/flutter.md](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/quality/skills/accessibility-audit/references/flutter.md) | Semantics and Flutter accessibility tools are useful. Add manual TalkBack/VoiceOver coverage and supported text-scale/device checks; automated scans are partial evidence. | P2 |
| [quality/skills/accessibility-audit/references/mobile.md](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/quality/skills/accessibility-audit/references/mobile.md) | Useful native assistive technology checks. Separate platform target guidance from WCAG criteria and use WCAG2ICT where relevant. | P2 |
| [quality/skills/accessibility-audit/references/web.md](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/quality/skills/accessibility-audit/references/web.md) | Useful axe/keyboard/screen-reader examples. Add criterion-level coverage, dynamic announcements, accessible authentication and CI/manual evidence separation. | P1 |
| [quality/skills/perf-check/references/backend.md](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/quality/skills/perf-check/references/backend.md) | Useful query and load examples. Model arrivals, pacing, representative data, percentiles and saturation; the sample does not establish production tail behavior. | P1 |
| [quality/skills/perf-check/references/mobile.md](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/quality/skills/perf-check/references/mobile.md) | Good native profiler starting points. Add repeatable device conditions, thermal/battery baselines and regression thresholds with variance. | P2 |
| [quality/skills/perf-check/references/web.md](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/quality/skills/perf-check/references/web.md) | Useful Lighthouse/browser measurements. Reconcile valid local built-site lab testing with the core prohibition; avoid lazy-loading critical above-fold/LCP imagery. | P1 |
| [quality/skills/write-tests/references/dotnet.md](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/quality/skills/write-tests/references/dotnet.md) | Useful framework and real-database patterns. Add buildable fixtures with pinned packages, isolation/cleanup and cancellation/error tests. | P1 |
| [quality/skills/write-tests/references/flutter.md](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/quality/skills/write-tests/references/flutter.md) | Useful unit/widget/integration split. Add runnable semantics/navigation and platform-channel cases; distinguish widget tests from real OS behavior. | P1 |
| [quality/skills/write-tests/references/jvm.md](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/quality/skills/write-tests/references/jvm.md) | Useful JUnit/container patterns. Reconcile generated identifiers and sequential behavior with literal-only/one-action doctrine; compile and run the fixture against declared versions. | P1 |
| [quality/skills/write-tests/references/node.md](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/quality/skills/write-tests/references/node.md) | Useful framework/request-boundary examples. Add real dependency isolation, async lifecycle cleanup and a browser/contract complement. | P1 |
| [quality/skills/write-tests/references/python.md](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/quality/skills/write-tests/references/python.md) | Useful pytest/database patterns. Sequential deduplication examples demonstrate why multi-action tests must be allowed. Add property-based and concurrency fixtures. | P1 |
| [quality/skills/write-tests/references/swift.md](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/quality/skills/write-tests/references/swift.md) | Useful Swift tests and boundary examples. Reconcile sequential assertions with doctrine; compile under declared Swift concurrency settings and separate host tests from device tests. | P1 |
| [web/skills/web-conventions/references/astro.md](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/web/skills/web-conventions/references/astro.md) | Good static-site composition intent. Processed scripts may be automatically inlined; `is:inline` is a processing directive, not simply a guarantee of embedded code. Test CSP against built output and the deployed headers. | P1 |
| [web/skills/web-conventions/references/react.md](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/web/skills/web-conventions/references/react.md) | Useful SPA/Next distinctions. Correct font-network guidance, secure JSON-LD and explicitly model RSC/server actions, caching and authenticated boundaries. | P1 |

### Agent roles, guardrails, repository infrastructure and documentation

| Files / component | Verified assessment | Required change / priority |
|---|---|---|
| `plugins/agents/agents/architect.md` | Fresh-context review is useful; requires speculative generic reuse and invokes lifecycle skills not represented by the agent package dependency alone. Bash is available despite no-edit instructions. | Scope authority at runtime, remove speculative reuse gate, test dependency closure. P0 boundary / P1 procedure. |
| `plugins/agents/agents/reviewer.md` | Evidence-based review is strong. Test execution can execute hostile PR code; timestamp/comment provenance and delta-only re-review are weak. | Isolated execution without secrets, trusted review identity/head binding and full-change interaction review. P0/P1. |
| `plugins/agents/agents/tester.md` | Good focus on failure paths and proving assertions. Permits production fixes despite being framed as a test-gap role. | Enforce task-specific write scope; separate a newly discovered production fix when outside authorization. P1. |
| `plugins/guardrails/scripts/read-command.sh` | Malformed JSON becomes an empty command; absent parser results in skipped enforcement. | Explicit supported-input/error behavior, bounded parsing and tested failure handling. P0 with downstream scripts. |
| `plugins/guardrails/scripts/no-commit-on-main.sh` | Substring detection misses Git global options; project directory can differ from target; an override-looking string in `echo` bypasses it. Only main/master recognized. | Treat as advisory; use Git/server enforcement and real target resolution. Test branches/worktrees/global options. P0. |
| `plugins/guardrails/scripts/check-staged-secrets.sh` | Positive controls block common synthetic key shapes and print filenames only. `git -C` and `cd … && git commit` bypass the intended scan. Includes unrelated unstaged/untracked content. | Scan the actual candidate in the actual repo, cover all channels with CI/server controls, redact output and document scope. P0. |
| `plugins/guardrails/hooks/hooks.json` | Valid JSON; current hook documentation supports command/args execution. No basis to call that schema invalid. | Add tested runtime capability/version requirements and explicit error behavior; a hook is not an authorization boundary. P1. |
| `scripts/install-skills.sh` | Basic copy/link installation works. Filtered installs omit referenced skills; old copied directories are skipped; unrelated symlinks are replaced; unknown plugin filters succeed with zero work. | Ownership manifest, dependency closure, atomic update/rollback, collision refusal, useful exit codes and platform support. P1. |
| `scripts/check.py` | Useful fast structural and hygiene checks; all pass. Handwritten frontmatter parser accepts duplicate keys and unclosed quotes. Privacy errors include matching sensitive values. Links do not prove semantic dependency resolution or anchors. | Redact first (P0); adopt real parsing/schema validation, path containment, dependency checks and adversarial unit fixtures (P1). |
| `scripts/framework-terms.txt` | Enforces a house convention, not technical neutrality. Case-sensitive vocabulary misses variants and can block legitimate routing terms. | Validate responsibility/scope, allow names in applicability metadata, keep stack details in adapters. P2. |
| `.github/workflows/ci.yml` | Read-only token, hosted runners, timeouts and PR-only cancellation are good. CLI install floats; actions use mutable tags; checks do not exercise behavior. Link acceptance includes 403/429 and excludes the repository's own GitHub links. | Pin dependencies, test scripts/examples, distinguish unreachable from verified links, add eval tiers and release provenance. P1. |
| `.claude-plugin/marketplace.json` and eight `plugin.json` files | All parse and pass strict validation. Plugin dependency fields are supported. Actual composition edges are incomplete: quality uses lifecycle/agents; agents uses lifecycle; meta uses lifecycle/quality. | Build an acyclic canonical dependency model; do not simply add mutually recursive plugin dependencies. Generate distribution metadata. P1. |
| Root `README.md` and all eight plugin READMEs | Helpful catalogue/install overview; they are consistent enough for discovery but broad applicability is not demonstrated. | Generate catalogue and compatibility tables from a registry; distinguish documented, fixture-tested and agent-evaluated support. P1/P2. |
| `AGENTS.md` | Useful contributor rules, ownership and framework separation. | Add evidence freshness and exception policy; reduce duplicated mandates and global vocabulary bans. P1. |
| `CONTRIBUTING.md` | Requires real investigation, validation and dry runs. | Specify reproducible eval artifacts, review owners, security reporting and consistent versioning for behavior changes. P1. |
| `docs/engineering-workflow.md` | Useful map and shared lifecycle policy. | Make it the generated view of one risk-based gate graph; resolve approval and review-order contradictions. P1. |
| `docs/skill-format.md` | Useful consistent structure. | Add input/output contracts, applicability, failure paths and examples; distinguish portable metadata from agent-specific extensions. P1. |
| `docs/other-agents.md` | Recognizes that installation and agent mapping differ. | A copied SKILL.md is not proof of identical tool, hook, argument or subagent behavior. Test each supported host and make Git-hook wrappers independent of Claude JSON input. P1. |
| `docs/lessons.md` | Valuable record of learned rules. | Revisit overgeneralized lessons with counterexamples and keep links to regression fixtures and effectiveness results. P1. |
| `CHANGELOG.md` | Useful change history and stated dry-run claims. | Link releases to auditable test/eval results and migration notes; distinguish claim from retained evidence. P1. |
| `.gitignore` and `LICENSE` | Standard repository hygiene and MIT license are present; no specific defect found in their current content. | Preserve them; add third-party snippet/fixture license attribution if introduced. P2 maintenance recommendation. |

### Reproduced behavior

Tests invoked the scripts directly with synthetic hook payloads in temporary repositories; they did not make real commits or exercise a live Claude hook session. The first two rows are positive controls. These results establish the scripts' behavior, not that a particular deployed host configuration is exploitable.

| Probe | Observed result | Interpretation |
|---|---|---|
| Ordinary commit with staged synthetic secret | Exit 2, filename-only message | Basic secret detection works. |
| Ordinary commit on main | Exit 2 | Basic branch guard works. |
| Secret scan for `git -C <other-repo> commit` | Exit 0 | Command matching/target repository not correctly handled. |
| Secret scan for `cd <other-repo> && git commit` | Exit 0 | Hook scans original working directory. |
| Main-branch guard for `git -c user.name=Test commit` | Exit 0 | Literal command substring misses a valid Git form. |
| `echo GUARDRAILS_ALLOW_MAIN_COMMIT=1 && git commit` | Exit 0 | Override detection accepts unrelated text. |
| Malformed hook JSON | Exit 0 | Input failure silently disables this check. |
| Install only quality | Eight skills installed, referenced engineering-principles absent | Successful installation does not mean composition is usable. |
| Repeat copy install after installed content differs | Existing copies skipped, success | No owned-copy upgrade workflow. |
| Preexisting unrelated `tdd` symlink | Link replaced | Collision can overwrite another installation's link; underlying target was not deleted. |
| Unknown plugin name | Zero installed, exit 0 | Typo is not reported as failure. |
| Duplicate frontmatter name | Last value accepted, no parser errors | Parser is not a strict YAML/schema validator. |
| Unclosed quoted description | Accepted, no parser errors | Malformed input escapes this parsing check. |
| Model of ledger insert → crash → retry | Retry skips; zero deliveries | Documented algorithm confuses intent with completed effect. This is an algorithmic reproduction, not an application integration test. |

## C. Missing Skills

These are capability families, not instructions to create one skill for every row or framework. Extend an existing owner where the workflow already exists. Create a separate skill only when it has distinct inputs, decisions, outputs and validation. Existing architecture, testing, security and documentation material should be improved, not falsely described as wholly absent.

| Engineering category | Missing or insufficient capability | Why it is needed and what to add | Priority / affected owners |
|---|---|---|---|
| Safe agent execution | Trusted instructions, untrusted repository/tool data, tool authorization, isolated execution | A reviewed PR can change package scripts or instructions. Define read/write/network boundaries, scoped credentials, command previews for consequential actions and resistance to exfiltration. | P0 · agents, all execution skills; R04 |
| Architecture and system design | Workload-driven architecture, quality attributes, capacity, modular monolith versus services | Current placement rules are not a system-design method. Add context/container views, trust/data boundaries, throughput and latency estimates, alternatives and reversible decisions. | P1 · spec, design-review, decision; R06, R12 |
| Clean code and modernization | Safe refactoring, characterization, legacy seams, dependency upgrades | SOLID/DRY/patterns need tradeoffs, not mandates. Add behavior-preserving changes, strangler migration, deprecation and performance constraints. | P1 · implement, bugfix, principles; R06, R08 |
| Distributed systems | Delivery semantics, consistency, ordering, leases/fencing, backpressure, sagas | Required to repair the current job guidance and handle duplicate, delayed and out-of-order work. Add state-machine and fault-injection examples. | P0 delivery repair; P1 broader capability · R01, R13 |
| API engineering | GraphQL, gRPC/protobuf, asynchronous events, webhooks, compatibility | Shared contract principles need protocol-specific auth, errors, pagination, evolution and streaming rules. Webhooks need signature verification, replay windows and idempotent processing. | P1 · add-endpoint, deploy-check; R13 |
| Database engineering | Query design, transaction isolation, engine-specific DDL, restore/DR, CDC | Migration checklists do not cover deadlocks, isolation anomalies, replicas, PITR, index economics or restoration. Add representative workloads and restore drills. | P1 · add-migration, data-check; R13 |
| Identity and secure coding | OAuth/OIDC, session lifecycle, MFA/passkeys, service identities, key management | Auth checks do not replace a protocol-aware implementation guide. Add authorization matrices, token audience/issuer checks, refresh reuse handling, session invalidation and cryptographic library selection. | P1 · security-privacy-review, add-endpoint; R14 |
| Threat modeling and privacy | Assets, adversaries, trust boundaries, abuse cases, retention/deletion, data flows | Build on the existing coercion/privacy strengths. Add accountable threat decisions, storage/key lifecycle and tests of deletion and consent withdrawal. | P1 · security-privacy-review, analytics-event; R03, R14 |
| Supply chain and CI security | Dependency provenance, secret scanning, SBOM, signed artifacts, CI trust boundaries | Pins and dependency alerts alone do not protect build credentials or artifact integrity. Add lockfile review, provenance verification, isolated fork PRs and release credential policy. | P1 · ci, release, guardrails; R10 |
| QA strategy | Test-layer selection, contract/E2E, exploratory, mutation, property/fuzz, concurrency | The doctrine is strong on example tests but lacks a balanced risk-based portfolio. Add evidence matrices, deterministic fixtures and failure triage. | P1 · testing-doctrine, write-tests; R08 |
| Performance and reliability | Workload modeling, tail latency, capacity, SLO/error budgets, overload and recovery | Average/median timings cannot establish resilience. Add arrival-rate tests, saturation curves, resource limits, backpressure and recovery criteria. | P1 · perf-check, observe, incident; R12 |
| DevOps and cloud | IaC, containers, orchestration, cloud IAM/networking, deployment environments | Current CI/deploy advice assumes infrastructure exists. Add plan/apply separation, drift, state protection, image hardening, resource requests/limits and rollback validation. | P1 shared workflows; P2 provider adapters · R10, R16 |
| LLM applications | Provider integration, structured outputs, streaming, retries, budgets, fallbacks | The repository guides coding agents but does not adequately teach building LLM products. Add schema validation, cancellation, rate limits, model/version migration and quality-cost-latency evaluation. | P1 · new AI family, quality, observe; R15 |
| RAG and search | Ingestion, chunking, embeddings, retrieval evaluation, ACLs, citations, deletion | Vector retrieval can expose another tenant's documents or retain deleted data. Add tenant-aware retrieval, lexical/hybrid baselines, recall/answer-grounding evaluation and index migration. | P1 · AI, data, security; R15 |
| Agent applications | Tool contracts, durable state, bounded loops, approval, replay, delegation | Prompt instructions alone cannot secure tools. Add per-tool authorization, idempotency, checkpoint/resume, budget limits and adversarial tool-output tests. | P1 application engineering, P0 library execution baseline · R04, R15 |
| ML and data engineering | Dataset/version lineage, leakage prevention, reproducible training, validation, deployment/drift | General application tests do not assess statistical quality or data drift. Add train/validation/test separation, batch/stream schema evolution, reproducible artifacts and monitoring. | P2, after AI/data foundations · R15, R16 |
| Desktop | IPC, filesystem authority, native accessibility, packaging/signing, secure updates | Web/mobile patterns do not cover desktop privilege, shell integration or update channels. Add shared desktop workflows with native and hybrid adapters. | P2 · new desktop family, release/security; R16 |
| Systems and networking | Memory ownership, unsafe code, ABI, races, sockets, protocol parsing | Shared-core bridges are not systems-engineering coverage. Add sanitizers, fuzzing, cancellation, resource bounds, allocator/ownership contracts and platform builds. | P2 · systems family, shared-core; R16 |
| Accessibility and internationalization | Conformance evidence, native semantics, locale/date/currency/input methods | RTL and translated strings are only part of the problem. Add locale-sensitive formatting, pluralization, Unicode/bidi security, keyboard layouts, time zones and assistive-technology matrices. | P1 accessibility completeness; P2 expanded locale coverage · R08, R16 |
| Documentation and developer experience | API/SDK docs, runnable tutorials, runbooks, architectural views, onboarding | Good prose is not enough when examples cannot execute. Add documentation tests, versioned examples, troubleshooting and support/deprecation policy. | P2 · meta, bootstrap, all references; R17 |
| Specialized professional domains | Payments/ledgers, real-time collaboration, SDK/library publishing, CLI tooling, browser extensions | These have distinct invariants: monetary precision/reconciliation, conflict resolution, public compatibility, shell safety and extension permissions. Add only when maintained fixtures and demand exist. | P2 selected domains; P3 broad expansion · R16, R18 |
| Advanced specialist domains | Embedded/IoT, scientific computing/HPC, graphics/games, regulated or safety-critical systems | Require domain-specific evidence, numerical or timing correctness, hardware constraints and qualified review. A generic checklist must not imply certification. | P3 · R18 |

### Dedicated security assessment

The existing security skill includes useful API-focused material. That does not establish complete web, mobile, infrastructure or AI security coverage. Use a versioned control matrix with applicability and evidence, rather than a claim that a checklist is OWASP-compliant. The current [OWASP Web Top 10:2025](https://top10.owasp.org/2025/0x00_2025-Introduction/) provides a risk map; [ASVS 5.0.0](https://asvs.owasp.org/) provides testable application requirements. Mobile coverage should separately use [MASVS and MASTG](https://mas.owasp.org/MASVS/).

| Security area | Current coverage | Concrete missing controls and validation |
|---|---|---|
| Broken access control | Good caller/tenant/revocation intent | Authorization matrices across object, action, property and tenant; account switching; bulk endpoints; replayed idempotency keys; signed-URL residual access. Test both permitted and forbidden cases. |
| Misconfiguration | Some headers, config and CI permissions | Production debug exposure, cloud IAM/storage/network defaults, proxy trust, CORS, safe error pages and runtime configuration verification. |
| Supply chain failures | Dependency awareness and plugin validation | Trusted sources, immutable pins, lockfiles, malicious install scripts, package namespace confusion, SBOM and artifact provenance verification. |
| Cryptographic failures | Secret hygiene and transport concerns | Key generation/storage/rotation, authenticated encryption, nonce discipline, platform keystores and backup-key lifecycle. Prefer established libraries; require misuse tests. |
| Injection | Validation and some web/API defenses | Parameterized queries, shell argument arrays, template/HTML contexts, path traversal, SSRF redirects/DNS/egress and unsafe deserialization. Validation does not replace context-specific encoding or authorization. |
| Insecure design | Design review and abuse cases | Explicit threat models, business abuse/rate limits, resource exhaustion, recovery flows and security design decisions linked to tests. |
| Authentication failures | Cookies/session/API considerations | Protocol-specific sign-in, account recovery, credential stuffing, session fixation, logout/revocation and service-token validation. |
| Software/data integrity | Generated contracts and review gates | Signed update verification, trusted release provenance, model/data artifact integrity and verified review/check identities. |
| Logging/alerting failures | Redaction and metrics intent | Fix actual sensitive output; test audit event completeness, access controls, retention and alerts without recording tokens or unnecessary personal data. |
| Exceptional conditions | Strong failure-path emphasis | Unknown outcomes, partial commits, exhausted resources, cancellation and fail-safe defaults. Correct the delivery algorithm and test interrupted transitions. |
| Privacy | Consent, minimization, sharing and coercion awareness | Treat stable identifiers as potentially personal; enforce deletion across queues, backups and indexes; model consent withdrawal and aggregation re-identification risk. |
| CI/CD | Hosted runners/read-only defaults are good | No secrets during untrusted execution, minimal tokens by job, protected release environments, immutable artifacts and auditable promotion. |
| AI-specific security | Sparse and inconsistent | Direct/indirect prompt injection, poisoned retrieval/tool results, excessive agency, unsafe generated output, data/model supply chain, cross-agent trust and resource/cost abuse. |

AI safety here must be enforced outside the prompt: narrowly scoped tools, authorization on each action, isolated execution, constrained egress and reliable audit records. Instruction/data separation is helpful but not a guarantee. This follows the threat distinction in [OWASP prompt injection](https://genai.owasp.org/llm2026/llm012026-prompt-injection/) and [excessive agency](https://genai.owasp.org/llm2026/llm032026-excessive-agency/). No malicious repository payload was executed in this audit.

### Dedicated QA and testing assessment

| Test capability | Assessment | Required strategy |
|---|---|---|
| Unit | Strong but too restrictive | Keep clear examples and independent expectations; allow parameterization, properties, sequences and justified tolerances. |
| Integration | Good database emphasis | Add engine/version fixtures, isolation/cleanup, actual auth middleware, transaction anomalies and failure injection. |
| End-to-end | Fragmented web/device advice | Maintain a small set of critical user journeys across browser/device environments; test auth and deployment configuration, not just mocked UI. |
| Regression | Strong principle, weak library implementation | Commit a reproducer for each corrected finding; make it fail before the correction and pass after. |
| Contract and compatibility | Generated-contract focus | Add old-client/new-server combinations, schema evolution, consumer expectations and event replay. |
| Performance/load | Useful measurement workflow | Define workload and arrival model, p95/p99, throughput, saturation, error rate, warmup and recovery. Use representative synthetic data. |
| Security | Checklists without comprehensive executable suite | Add auth negatives, secret fixtures, dependency/build checks, static analysis, authorized dynamic tests and malicious agent-input scenarios. |
| Accessibility | Good starter coverage | Map applicable WCAG criteria; combine automation with keyboard and assistive-technology testing. Automated scans alone cannot establish conformance. |
| Coverage and quality | Tests must detect bugs, but narrow doctrine | Use risk/requirement coverage, branch coverage for important paths and targeted mutation testing. Do not set a universal 100% line target. |
| Flakiness | Delete-or-fix rule is unsafe | Track owner/root cause; time-bound quarantine with replacement coverage; record retries as flaky rather than silently green. |
| Cross-platform | Partial mobile guidance | Test declared OS/compiler/runtime/architecture combinations, filesystem behavior and real mobile devices where necessary. |
| Library quality gates | Syntax, structure and prose checks | Add parser/hook/installer tests, snippet compilation, dependency closure, routing evaluations and task-completion evaluations. |

Tool selection should follow the defect class. A browser automation framework is valuable for real navigation/auth flows; it does not replace a unit test for pure logic. Property-testing tools fit parsers, serializers and invariants; fuzzing and sanitizers fit untrusted byte processing and native code. Load tools need a deliberately chosen workload model. Static analyzers and secret scanners need reviewed findings, redaction and scoped exceptions. Do not add several overlapping tools without measurable incremental coverage.

## D. Incorrect or Outdated Practices

The following are the most important concrete corrections. Source links pin repository evidence to the audited commit; external documentation supplies the technical comparison. Several findings are contradictions or overclaims, not evidence that a real system has already failed.

### D1. A pre-send ledger entry is not evidence of delivery — P0

Evidence: [add-scheduled-job, line 36](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/backend/skills/add-scheduled-job/SKILL.md#L36) and its stacks reference. The instruction inserts a unique row before sending and skips on conflict. Crash after insertion but before sending: retry sees the row and skips forever. The local model reproduced zero deliveries.

Correct design: commit business state and a pending outbox record atomically; claim with a lease; send using a stable downstream idempotency key where supported; mark confirmed completion; recover expired claims; distinguish unknown acknowledgement from known failure. A crash after sending can still cause a duplicate unless the downstream effect is idempotent or reconciled. Never promise end-to-end exactly-once delivery for arbitrary email/SMS/webhook providers. The [transactional outbox pattern](https://microservices.io/patterns/data/transactional-outbox.html) addresses durable publication intent but still requires duplicate handling.

Required tests: crash before claim, after claim, before send, after send before acknowledgement, after acknowledgement before marking complete; concurrent workers; expired lease; repeated provider response; permanent rejection; revoked access. Apply the correction everywhere this rule is repeated, not only in one skill.

### D2. Offline recovery and test instructions disagree — P0

Evidence: [offline-queue, line 34 versus line 59](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/mobile/skills/offline-queue/SKILL.md#L34). The design preserves an individually invalid item in a visible recovery state; the test list drops it. Make persisted states explicit: pending, uploading, retryable, needs-attention, confirmed, and user-authorized discard. Delete only after confirmed completion or an explicitly permitted loss action. Test both data retention and user visibility. Deduplication alone does not guarantee delivery or resolve edits/deletes/conflicts.

### D3. Security checks can expose what they detect — P0

Evidence: [pre-commit lines 38–42](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/lifecycle/skills/pre-commit/SKILL.md#L38) prints matching diff lines; [check.py line 282](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/scripts/check.py#L282) includes matched text in errors. A secret can enter chat or CI logs through the check itself, including a deleted secret in a diff.

Emit location, category and a nonreversible identifier only. Never emit the value. Detect failures with synthetic credentials and assert their literal bytes are absent from stdout/stderr/artifacts. If an actual exposure occurs, scope containment and rotation to the credential and exposed locations. [GitHub's security guidance](https://docs.github.com/en/actions/reference/security/secure-use) explicitly cautions that automatic masking is not guaranteed.

### D4. Bash substring hooks are not reliable enforcement — P0

Evidence: the three guardrail scripts and B's reproduced bypasses. Git global options, command chains and alternate repositories defeat the intended checks. A string resembling the override need not be an actual environment assignment. Direct Git hooks also do not naturally provide the Claude JSON payload expected by these wrappers.

Separate a repository scanner from host adapters. Use a Git hook for developer feedback, CI/server checks for merge enforcement, and host permissions for tool authority. Test target directories, staged snapshots, worktrees, unusual filenames, malformed input and missing dependencies. Document bypassability. Current [Claude hook documentation](https://code.claude.com/docs/en/hooks) supports the command/args schema used here; the defect is behavior and enforcement assumptions, not an invented schema incompatibility.

### D5. Migration and indexing rules overgeneralize database behavior — P1

Evidence: [add-migration lines 28, 53–55 and 73](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/backend/skills/add-migration/SKILL.md#L28). An index for every WHERE/JOIN/ORDER BY is not a sound general rule. Selectivity, composite key order, write amplification, storage and query frequency matter; a sequential scan can be optimal.

For PostgreSQL, validating NOT NULL can scan a table without rewriting it; default handling depends on the expression and version. UNIQUE cannot be added NOT VALID in the implied PostgreSQL workflow. The duplicate-repair/online-unique-index sequence is useful, but its introductory warning is misleading for PostgreSQL. Describe exact engine/version capabilities, locks and scan/rewrite distinctions using [ALTER TABLE documentation](https://www.postgresql.org/docs/current/sql-altertable.html). Do not export PostgreSQL syntax as a universal SQL recipe.

### D6. Freshness and funnel queries can report misleading health — P1

Evidence: `data-check` limits events to the last day before selecting stale owners, so owners with no events or only older events disappear. Start with the expected active-owner cohort, left-join latest events and count both NULL and overdue timestamps. Test fresh, stale, never-seen, inactive and clock-skewed cases.

`analytics-event` also needs a temporal predicate ensuring conversion follows the cohort event. A first event within a window is not necessarily the user's first-ever event. Define the cohort and attribution window first; test pre-cohort conversions, repeated events and late arrivals.

### D7. Signed URLs cannot promise application-level immediate revocation — P0 correction

Evidence: [add-file-upload line 56](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/backend/skills/add-file-upload/SKILL.md#L56) combines immediate revoked-member denial with URLs that remain valid until expiry. With S3, presigned URLs can be reused and uploads can overwrite the same object key. [AWS documents these semantics](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html).

State the residual access window. If immediate per-user revocation is required, use an authorization-enforcing serving path or a provider-specific revocation mechanism. Confirm and scan an immutable version/checksum, not a mutable key that a still-valid upload URL can replace. Re-encoding accepted image formats reduces some risks but does not eliminate parser vulnerabilities or decompression bombs; bound resources and isolate processing.

### D8. Test doctrine excludes valid testing techniques — P1

Evidence: [testing-doctrine lines 24–35](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/quality/skills/testing-doctrine/SKILL.md#L24). Idempotency inherently requires repeated calls. State-machine/concurrency tests require sequences. Property tests need generated inputs and shrinking; numerical code may require justified tolerances. The useful rule is independent oracles and reproducible failure evidence, not literal-only inputs. Keep simple example tests simple, but allow techniques matched to the invariant. Do not delete a flaky regression solely to restore a green build.

### D9. Architecture preferences are treated as correctness laws — P1

Evidence: engineering-principles, design-patterns, design-review and the architect role. A parser can be core business logic in a compiler; cryptographic processing can be a product's domain; small scripts need not adopt onion architecture. A second implementation is not required before an interface can serve a meaningful in-process boundary. Similarly, [Android's official data-layer guidance](https://developer.android.com/topic/architecture/data-layer) explicitly permits repositories depending on other repositories.

Replace mandatory structure with applicability, tradeoffs and acceptance invariants. Preserve cohesive responsibility and dependency direction where useful. Require concrete benefit before introducing generic abstractions. No-call-in-a-loop should target unwanted repeated I/O/N+1 behavior, not ban ordinary algorithms.

### D10. Review and deployment ordering conflicts — P1

Evidence: new-feature places code review before CI/deploy-check, while [code-review dimension 15](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/quality/skills/code-review/SKILL.md#L52) marks missing deploy verdicts major. Resolve this with an explicit graph: implementation evidence → applicable security/deploy assessments and CI → final review disposition → merge gate. Earlier reviews may be provisional. Require trusted actor, candidate SHA, environment and result for gate evidence. Use atomic head matching or the platform's merge queue to avoid merging a head different from the reviewed one.

### D11. CI template lacks a required permission and complete invalidation — P1

Evidence: `lifecycle/skills/ci/references/github-actions.md` gives contents:read but uses dorny/paths-filter on PRs. Its [v3 documentation](https://github.com/dorny/paths-filter/tree/v3) requires pull-requests:read for that API path. Add permission only to the changes job. Include contracts and shared build/lock/config inputs for every dependent area, and add a stable always-evaluated aggregate job that fails on failed/cancelled required checks. Configure merge_group when using merge queues. Mutable action tags and an unpinned CLI reduce reproducibility; they are risks, not proof of a compromised dependency.

### D12. Web framework claims need correction — P1

Evidence: [React reference lines 47–48](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/web/skills/web-conventions/references/react.md#L47) and [Astro reference lines 25–26](https://github.com/Quaid5050/ai-engineering-skills/blob/4dab7293821283e30bee7d7f3814c10e8ee72f2a/plugins/web/skills/web-conventions/references/astro.md#L25).

- `next/font/google` self-hosts fonts; it does not require the visitor's browser to contact Google. A build-time network restriction can still justify local files. Distinguish those policies. [Next.js font documentation](https://nextjs.org/docs/pages/getting-started/fonts).
- Astro may automatically inline small processed scripts. `build.inlineStylesheets` does not control JavaScript inlining. Test emitted output and adopt supported nonce/hash or external-script strategies for the selected version. Do not weaken CSP merely to silence a failure. [Astro script documentation](https://docs.astro.build/en/guides/client-side-scripts/).
- JSON-LD is not safe merely because of its script type: unsafe serialization can terminate the HTML script element. Escape appropriately, including `<`, and test hostile strings. [Next.js JSON-LD guidance](https://nextjs.org/docs/app/guides/json-ld).

### D13. Mobile/release guidance needs versioned guarantees — P1

Android periodic WorkManager execution is inexact and subject to constraints/optimizations; a widget cannot promise a precisely scheduled stale-state transition through it. [Android work-request documentation](https://developer.android.com/develop/background-work/background-tasks/persistent/getting-started/define-work).

The store reference understates Google Play's privacy-policy scope: the developer policy requires it for all apps. [Google Play User Data policy](https://support.google.com/googleplay/android-developer/answer/10144311?hl=en). The CodePush row must distinguish the retired App Center service from independently hosted or maintained alternatives; Microsoft documents that distinction in its [retirement guidance](https://learn.microsoft.com/en-us/appcenter/retirement). Do not label all CodePush implementations unusable. Likewise, the current Shorebird asset/native-change limitations were checked and are not presented here as a verified defect.

Platform termination behavior is API-specific. The audit did not treat every iOS user-termination statement as necessarily wrong: location services and background URLSession have different rules. Require versioned source links and device evidence instead of one blanket relaunch claim.

### D14. Native interop error handling needs precise boundaries — P1

Kotlin/Native can deliberately bridge declared exceptions via `@Throws`; uncontrolled exceptions are a separate concern. [Kotlin interop documentation](https://kotlinlang.org/docs/native-objc-interop.html). Rust `catch_unwind` only catches unwinding panics, not aborting ones. [Rust documentation](https://doc.rust-lang.org/std/panic/fn.catch_unwind.html). Define supported ABIs, panic strategy, ownership and error mapping; do not imply a universal catch-all wrapper makes foreign calls safe.

### D15. Portability and validation are weaker than the format claims — P1

The portable [Agent Skills specification](https://agentskills.io/specification) describes metadata and progressive resources, but agent-specific argument substitution, tool controls, roles and hooks need host adapters. `argument-hint` and `$ARGUMENTS` should not be assumed to behave identically everywhere. Current Claude plugin dependency fields are supported; the actual problem is missing semantic edges and no verified closure in the generic installer. Format validation alone cannot establish successful routing or task execution.

## E. Cross-Platform Coverage

**Documented does not mean tested.** The tree has no executable multi-platform fixture/eval matrix demonstrating these workflows. The following assesses available guidance, not certified compatibility.

| Ecosystem | Existing coverage | Required extension |
|---|---|---|
| React / Next.js | Direct reference and web workflows | Correct RSC/client boundaries, auth/cache isolation, font/CSP claims, routing/rendering modes and tested examples. |
| Vue / Angular / Svelte | Generic web principles only | Thin adapters for Vue/Nuxt, Angular and Svelte/SvelteKit: lifecycle/state, SSR/hydration, forms, routing, testing and deployment. |
| Astro | Direct static-site reference | Correct script/CSP handling; versioned static/server examples and deployed-header checks. |
| Node.js / TypeScript / JavaScript | Backend/web/test references | Runtime/package-manager support, event-loop/cancellation/streams, ESM boundaries, dependency security and executable fixtures. |
| Python | Django backend and Python testing | FastAPI/Flask where demand exists, packaging/type checks/async behavior, scientific/ML and data pipelines. |
| Java / JVM | Spring plus JVM testing | Java-specific concurrency/runtime profiles, build/package support; Kotlin server extensions without duplication. |
| Go | Incidental mentions rather than full guidance | Context cancellation, goroutine ownership, races, modules, HTTP lifecycle, profiling and deployment. |
| .NET | Backend and test references | ASP.NET profiles, async/cancellation, EF provider details, SDK packaging and Windows/native distinctions. |
| PHP / Ruby | No substantive dedicated implementation adapters | Laravel/Symfony and Rails adapters tied to actual versions and maintained fixture applications. |
| iOS / Swift / SwiftUI | Substantial mobile references | Swift concurrency, signing/privacy/entitlements, lifecycle and OS-version matrix; UIKit interoperability where needed. |
| Android / Kotlin / Compose | Substantial mobile references | Target-SDK behavior, structured concurrency, lifecycle/state restoration, permissions and device coverage. |
| Flutter | Conventions, testing, accessibility/background references | Buildable plugin/isolate/platform-channel fixtures, platform-specific release and accessibility tests. |
| React Native | Conventions and release mentions | Current architecture/debugging, native modules, Hermes, upgrade/runtime compatibility and E2E devices. |
| macOS native | Swift context is reusable but not a desktop workflow | AppKit/SwiftUI, sandbox/TCC, notarization, menu/keyboard behavior, updates and filesystem permissions. |
| Windows native | .NET backend support is not desktop support | WinUI/WPF/Win32 or selected native stack, MSIX/signing, elevation, registry/COM boundaries and accessibility. |
| Linux native | No full desktop workflow | Packaging/distribution targets, Wayland/X11 differences, permissions, desktop integration and accessibility. |
| Electron / Tauri / Qt / .NET MAUI | No substantive dedicated coverage | Shared desktop lifecycle plus bridge/IPC security, platform packaging and native capability adapters. |
| C / C++ / Rust | Limited shared-core/interop discussion | Ownership, memory safety, unsafe review, ABI, sanitizers/fuzzing, build systems, OS APIs and architecture matrix. |
| Operating systems / networking | No systematic coverage | Processes/threads, sockets/TLS/DNS, resource lifetimes, cancellation, clocks, locking and failure models. |
| AI / LLM / RAG / agents | Coding-agent process rather than AI application engineering | Integration, retrieval/ACLs, evals, tool execution, durable orchestration, monitoring and deployment. |
| ML / data | Application SQL/analytics only | Data contracts/lineage, ingestion/streaming, training/evaluation, serving, drift and reproducibility. |
| Cloud / infrastructure | CI and deployment checklists | Shared IaC/container workflows; AWS/Azure/GCP and Kubernetes/serverless adapters based on maintained demand. |

Additional essential implementation languages/formats are SQL, shell and PowerShell, HCL, Dockerfiles, YAML and JSON/schema tooling. Optional later ecosystems include Scala for JVM/data, R/Julia for scientific work, Elixir/Erlang for concurrent services, WebAssembly/edge runtimes and embedded targets. Add a maintained adapter because its behavior differs materially, not merely because its name is missing.

A capability matrix should distinguish **generic guidance**, **documented adapter**, **fixture-tested adapter**, and **agent-evaluated workflow**. Each supported platform declares OS/runtime/compiler versions, prerequisites, limitations and last successful evidence. Universal coverage is achieved through shared engineering contracts plus selective adapters; no single architecture or test runner works equally well everywhere.

## F. Recommended Repository Architecture

Keep the recognizable skill entry points initially. Separate canonical content from distribution wrappers, and introduce a small shared foundation to break dependency cycles. The following is a proposed target, not a modification made by this audit:

```text
ai-engineering-skills/
  README.md
  CONTRIBUTING.md
  SECURITY.md
  CHANGELOG.md
  LICENSE
  catalog/
    skills.yaml                 # stable IDs, ownership, dependencies, maturity
    compatibility.yaml          # host/runtime/OS support and evidence
    sources.yaml                # primary sources and verification dates
  schemas/
    skill-metadata.schema.json
    evaluation.schema.json
  skills/
    foundation/                 # context, authority, evidence, risk, shared policy
    lifecycle/                  # existing routing and delivery procedures
    architecture/
    backend/
    data/
    web/
    mobile/
    desktop/
    systems/
    ai/
    security/
    quality/
    operations/
    meta/
  adapters/
    agents/                     # Claude/Codex/other tested host wrappers
    languages/                  # language/runtime-specific differences
    frameworks/                 # React, Django, Spring, etc.
    platforms/                  # OS/cloud/browser/device differences
  examples/                     # runnable minimal application fixtures
  tests/
    tooling/                    # parser, installer, hook behavior
    snippets/                   # compilation and command verification
    composition/                # dependency and lifecycle contract tests
  evals/
    routing/                    # positive, implicit, ambiguous, negative triggers
    tasks/                      # real artifact-producing engineering tasks
    adversarial/                # injection, unsafe execution, conflicting inputs
    rubrics/
    baselines/
  tooling/                      # lint, registry generation, install, package
  dist/                         # generated host packages/manifests
  docs/
    workflow.md
    compatibility.md
    maintenance.md
    decisions/
    lessons/
  .github/workflows/
```

Empty domains need not be created before content is ready. A skill remains a discoverable directory containing SKILL.md and its required resources. Distribution must package referenced resources so copied installations do not contain dangling paths. Do not blindly assume a host recursively discovers the proposed authoring hierarchy: generate the host's expected installed layout.

### Canonical skill contract

Each skill should state: purpose and non-goals; triggers and negative triggers; required inputs; prerequisites; read/write/network effects; applicable platforms; risk tier; procedure with decisions; failure/recovery paths; outputs; acceptance evidence; dependencies; examples/counterexamples; sources; maintainer; version and verification date. Keep the initial body concise; load detailed references only when relevant.

Use portable fields in SKILL.md and put repository-specific structured metadata in the catalogue or supported metadata fields. Do not invent mandatory manifest keys that hosts reject. The [Agent Skills format](https://agentskills.io/specification) is a packaging baseline, not an execution guarantee.

### Dependencies and shared policy

Foundation contains small reusable rules without depending on orchestration. Specialist workflows depend on foundation. Lifecycle routes to specialists; agent role adapters invoke procedures without creating a hard install cycle. Distinguish required dependencies from optional companion suggestions. Validate graph closure, missing IDs, cycles and resources for every supported installation profile.

Define shared policies once: authorization, sensitive output, evidence provenance, test selection, risk tiers and exceptions. Generate summary tables if needed. Architecture rules should state when they apply and how a justified alternative is recorded. A project can choose a different architecture; it cannot turn untrusted content into new user authorization.

### Maintenance and discoverability

Generate catalogues and workflow maps from stable IDs. Give each capability an owner and declared support range. Review high-risk guidance and volatile platform APIs more frequently than stable principles. Source links need dates and version context, not just a link-check pass. Maintain deprecation aliases and migration notes when renaming skills.

Version skill contracts according to behavior: breaking input/output or safety-gate changes need explicit compatibility handling; compatible additions and corrections need documented release notes. Plugin package versions may bundle skill versions, but should not imply every unchanged skill was independently revalidated. Track install ownership and checksums; support atomic update, rollback, collision refusal and an uninstall that removes only owned files.

### Standards and mature practices to adopt selectively

| Reference | Actual value for this library |
|---|---|
| [NIST SSDF](https://csrc.nist.gov/projects/ssdf) | Organize secure-development responsibilities and evidence across preparation, protection, production and vulnerability response. Use as a process map, not a certification claim. |
| [OWASP ASVS](https://asvs.owasp.org/) | Turn security review topics into selected, versioned, testable application controls. |
| [OWASP MASVS/MASTG](https://mas.owasp.org/MASVS/) | Supply mobile-specific storage, platform, network and privacy verification missing from generic web checklists. |
| [SLSA 1.2](https://slsa.dev/spec/v1.2/) | Specify build/source integrity and provenance expectations for released skill bundles and tooling. Adopt levels only with corresponding evidence. |
| [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | Map web accessibility requirements to criterion-level evidence. Keep native platform testing explicit. |
| [Systematic skill evaluations](https://developers.openai.com/blog/eval-skills) | Evaluate routing and resulting artifacts, including negative cases, instead of treating readable instructions as proof of usefulness. |

These comparisons show where the repository falls short: it contains many good practices, but lacks the maintained control mapping, executable fixtures, release evidence and measured outcomes found in mature engineering systems. Copying the complete standards into prompts would create bulk and staleness; reference selected requirements and test them.

## G. Prioritized Improvement Roadmap

Each recommendation states the change, reason, concrete work, affected skills and expected benefit. Recommendations in earlier tables map here; platform-specific refinements are grouped to avoid an unmaintainable task list.

### P0 — Critical

| ID | What and why | Add or modify / affected skills | Expected benefit and acceptance evidence |
|---|---|---|---|
| R01 | Repair effect-delivery semantics: current guidance can lose work. | Rewrite add-scheduled-job and stacks reference; reconcile principles, backend-conventions, deploy-check, backend-deploy, observe and endpoint idempotency. Add durable state/lease/provider-ack examples. | No loss of pending work in the documented crash windows; duplicates/unknown outcomes honestly modeled. All crash/concurrency scenarios in D1 pass. |
| R02 | Resolve offline loss-policy contradictions. | Modify offline-queue design/tests and related upload/endpoints. Define persistent states, user discard, retention, durable-write failure and account separation. | Invalid records remain recoverable unless explicitly discarded; restart/upgrade/account-switch tests prove the policy. |
| R03 | Prevent sensitive-output leaks and false upload/privacy guarantees. | Redact check.py and pre-commit; correct add-file-upload URL/processing semantics; update security-privacy-review, data-check and analytics-event privacy language. | Synthetic secrets never appear in output; revoked-access residual windows are documented/tested; confirmed uploads cannot be silently replaced. |
| R04 | Establish a real agent execution boundary. | Rework guardrails and host wrappers; constrain architect/reviewer/tester execution; add foundational untrusted-input/tool-authority policy used by every execution skill. | Negative scenarios cannot obtain secrets, broaden permissions or write outside task scope. Hooks are honestly advisory; CI/host controls enforce the actual boundary. |

### P1 — High Priority

| ID | What and why | Add or modify / affected skills | Expected benefit and acceptance evidence |
|---|---|---|---|
| R05 | Test the library as a software product. Prose checks miss consequential errors. | Add tooling unit tests, buildable examples, composition tests and agent evals. Modify create-skill, capture-lesson, CONTRIBUTING and CI. | Every corrected defect has a regression; routing and task outcomes have retained artifacts. Critical scenarios pass without prohibited actions. |
| R06 | Replace universal doctrine and excessive ceremony with risk-based decisions. | Revise principles, patterns, design-review, architect, bootstrap, new-feature, implement and issue/spec procedures. | Simple safe tasks complete with proportionate overhead; high-risk changes retain necessary checks. Counterexample fixtures support multiple legitimate architectures. |
| R07 | Unify review/CI/deploy/merge gates. Current ordering and provenance are inconsistent. | Define one gate graph and evidence contract; update start-issue, create-pr, code-review, ci, deploy-check, merge and reviewer. Bind evidence to candidate and trusted actor. | No circular prerequisite; changed-head and forged-comment cases fail; merge queue/direct merge paths enforce current evidence. |
| R08 | Broaden test strategy while preserving strong assertions. | Rewrite doctrine; extend tdd, write-tests, tester, bugfix, perf-check, accessibility-audit and device-test. Add property/state/concurrency/contract/E2E examples. | Tests catch seeded defects across layers; valid sequence/property tests are accepted; flaky tests are tracked rather than silently removed. |
| R09 | Make installation and composition dependable. | Implement strict parsing, schemas, dependency closure, resource packaging, ownership/checksum lock, atomic upgrade/rollback and collision handling. Update installer, manifests, other-agents and skill-format. | Clean/filtered/repeated/upgraded installs are usable; unknown filters fail; foreign files survive; all packaged references resolve. |
| R10 | Secure and reproduce CI/releases. | Pin tools/actions, add dependency/security checks and artifact provenance, fix path-filter permissions/coverage and aggregate gates. Extend ci, release, bootstrap and actual repository CI. | Same inputs produce traceable packages; untrusted PRs have no privileged credentials; changed shared contracts trigger all affected checks. |
| R11 | Correct current platform claims before adding breadth. | Fix React/Astro references, mobile-stores, background-work, widgets and native interop. Give volatile guidance sources, versions and verification dates. | Framework examples build and behave as stated; background and rollout limits are explicit; no unsupported guarantee remains in the maintained examples. |
| R12 | Add production reliability and diagnosis depth. | Extend spec, perf-check, observe, incident and postmortem with SLOs, workload models, capacity, recovery and incident roles. | A representative service has measured latency/error budgets, actionable alerts and a verified recovery runbook. |
| R13 | Complete API/data/distributed correctness. | Extend add-endpoint, add-migration, backend-conventions, data-check, analytics-event, offline-queue and web caching. Add protocol/DB adapters, replay/conflict/isolation semantics and restore tests. | Multi-tenant replay, concurrent update, old-client compatibility and migration/recovery fixtures pass. |
| R14 | Build verifiable security engineering workflows. | Extend security-privacy-review with threat modeling, auth/session, crypto/secrets, privacy and control-test mappings; link all applicable backend/web/mobile/release skills. | Selected ASVS/MASVS controls have applicability, owner and actual evidence; exceptions have scope/expiry rather than a generic accepted-risk phrase. |
| R15 | Add the essential AI engineering capability family. | New LLM integration, RAG and agent workflow procedures, sharing security/testing/data/operations foundations. Add structured-output validation, ACL retrieval, tool contracts and eval datasets. | Small representative AI apps meet defined quality, leakage, tool-authority, latency and cost budgets. ML training/data-platform depth follows at P2. |

### P2 — Medium Priority

| ID | What and why | Add or modify / affected skills | Expected benefit and acceptance evidence |
|---|---|---|---|
| R16 | Expand platforms through maintained adapters. | Add E's missing web/backend/mobile/desktop/systems/cloud/language adapters and ML/data extensions. Reuse conventions, shared-core, write-tests, accessibility and release owners. | Every claimed supported ecosystem has a runnable fixture, supported-version statement and applicable CI/device evidence; no duplicate core doctrine. |
| R17 | Improve discoverability, documentation and governance. | Generated catalogue, compatibility tiers, owners, sources, ADR/lesson follow-ups, runnable onboarding and migration notes. Update README/docs/meta and all references. | A user can identify the right skill and support level; stale guidance has an owner; docs examples and cross-references are tested. |

### P3 — Future Improvements

| ID | What and why | Add or modify / affected skills | Expected benefit and acceptance evidence |
|---|---|---|---|
| R18 | Optimize and specialize after the core is reliable. | Demand-led payments, collaboration, SDK/CLI/extensions, embedded/scientific/graphics profiles; benchmark automation, selective eval scheduling, drift detection and cost/context optimization. | Each addition proves incremental task success over the existing library and fits a sustainable owner/test budget. Retire low-value duplicate guidance. |

Do not interpret these priorities as permission to postpone a discovered high-impact vulnerability in a P2 adapter. Priority is based on the current repository evidence; newly identified exposure can move work forward.

## H. Final Implementation Plan

This is the proposed execution plan. **No implementation changes were made during the audit.** Sequence by dependencies and acceptance evidence rather than an unsupported calendar estimate.

| Milestone / order | Dependencies | Required work | Exit criteria / outcome |
|---|---|---|---|
| M0 — Freeze the baseline | None | Record commit, inventory, current checks and known failures. Assign owners to R01–R04. Preserve the current release for comparison. | Reproducible baseline and prioritized issues; all critical findings accepted, disputed with evidence, or explicitly scoped. |
| M1 — Safety correction release | M0 | Implement R01–R04 in small reviewed changes. Add reproductions before fixes, including log-redaction and crash windows. Correct every duplicated rule. | No known P0 guidance left unaddressed; direct probes and integration examples pass; release notes explain changed guarantees. |
| M2 — Reliable validation and installation | M1, with tooling work possible alongside it | Implement R05 and R09. Strict parsing/schema, graph checks, hook/installer tests, packaged references, owned updates and rollback. | Clean and upgrade installation matrix passes; malformed inputs and collisions handled; examples are executable and versioned. |
| M3 — Coherent shared workflow | M2 | Implement R06–R08. One risk taxonomy, gate graph and evidence format; remove duplicated policy; support legitimate architecture/testing alternatives. | A small docs fix, ordinary feature, migration and security-sensitive change each complete without contradictions or unnecessary approvals. |
| M4 — Production/security foundations | M2–M3 | R10–R14: CI integrity, current-platform corrections, API/data correctness, threat controls, SLOs and recovery. | Tested end-to-end reference projects; fault injection, old-client/migration and auth-negative tests; signed/traceable release artifacts and working runbooks. |
| M5 — AI engineering baseline | Safe execution, testing and data foundations | R15: minimal LLM integration, ACL-aware RAG and bounded tool-agent examples; adversarial and quality datasets. | Quality/cost/latency budgets met; no cross-tenant retrieval in test corpus; unauthorized tools blocked; cancellation/replay/recovery demonstrated. |
| M6 — Coverage waves | M3–M5; owners and fixture capacity | R16–R17. First deepen existing stacks; then missing web/backend adapters; then desktop/systems; then wider ML/data/cloud and specialized domains. | Each advertised support tier has real evidence. Documentation and metadata are generated and consistent. |
| M7 — Continuous improvement | Stable maintained baseline | R18; scheduled upstream review, regression triage, task benchmarks, deprecations and selective expansion. | Measurable improvements in task success/security/maintainability without unsustainable prompt size or maintenance cost. |

### Evaluation design and release gates

Use two layers of evaluation. **Deterministic tests** verify scripts, schemas, dependency graphs, examples and resulting artifacts. **Agent evaluations** verify that instructions lead to the right behavior when asked explicitly, implicitly, ambiguously, or in an out-of-scope context. A fresh agent's favorable opinion is not sufficient.

Begin with a small, representative suite:

1. A small documentation change that must not trigger a full application workflow.
2. An authenticated endpoint with cross-tenant access attempts and replayed create requests.
3. A scheduled notification interrupted at every persistence/send boundary.
4. An offline record rejected by the server, followed by process death and recovery.
5. A large-table migration with duplicate data, concurrent writes and an older client.
6. A web page with hostile JSON-LD content, CSP and keyboard/assistive-technology checks.
7. A PR containing malicious instructions or a test script that attempts network exfiltration.
8. A partial install, conflicting symlink, existing owned copy and rollback.
9. A mobile background task delayed or killed by the OS.
10. An AI retrieval/tool task with poisoned content, revoked access and a strict execution budget.

Retain prompt, skill version, host/model version, fixture commit, tool policy, resulting diff/artifacts, commands/results, rubric and cost/time. Compare with no skill and the previous version under the same conditions. Repeat nondeterministic scenarios enough to estimate variation; use independent reviewers for subjective quality, with deterministic checks wherever possible. OpenAI's [skill-evaluation guidance](https://developers.openai.com/blog/eval-skills) supports this artifact-and-routing approach; the specific suite above is tailored to this audit's findings.

Suggested initial gates are: all deterministic critical regressions pass; no unauthorized action or secret disclosure in the defined adversarial suite; no unresolved critical correctness finding; required examples compile/run; dependency and install tests pass; task success does not regress against the approved baseline. Report sample size and uncertainty rather than claiming universal safety from a finite suite. Agree numeric task-quality thresholds after measuring the initial baseline.

### Implementation mechanics

Keep the first correction releases compatible where possible. Introduce stable IDs and generated packaging before moving source folders. Migrate one plugin at a time with aliases and install-upgrade tests. Do not combine a directory rewrite, broad doctrine changes and many new frameworks in one PR. Preserve a short decision record for consequential choices and link every audited defect to its regression test and release.

## I. Final Assessment

**1. What are the biggest weaknesses?**

Incorrect delivery guarantees, inconsistent policy across skills, incomplete execution/security enforcement, over-prescriptive architecture/testing doctrine, and lack of executable evidence for claimed broad usefulness. These matter more than missing framework names.

**2. What critical skills are missing?**

Safe agent/tool execution; complete threat/auth/supply-chain workflows; distributed delivery and data correctness; risk-based test strategy; cloud/IaC and production reliability; and actual LLM/RAG/agent application engineering. Desktop, systems, ML/data and additional frameworks need maintained adapters after the foundations.

**3. Which existing skills are technically incorrect or need rewriting?**

Rewrite add-scheduled-job's delivery algorithm and reconcile offline-queue. Substantially revise engineering-principles, testing-doctrine, design-review and the lifecycle gate contract. Correct add-migration, data-check, analytics-event, upload revocation/processing, pre-commit, CI templates, React/Astro references and mobile release guidance. Harden guardrails, check.py and the installer. Preserve the many useful portions identified in B.

**4. What should be removed, merged or simplified?**

Remove universal exactly-once promises, automatic poison-record deletion, secret-printing commands, invalid framework claims and unsupported architecture absolutes. Merge duplicated authorization, evidence, delivery, placement and test policy into canonical owners. Keep useful public entry points such as implement and bugfix, but let them share a common procedure. Simplify mandatory issue/docs/review ceremony for bounded low-risk work. Do not delete all existing skills or split every framework into a new doctrine.

**5. How can this serve virtually every major stack?**

Use shared contracts for discovery, design, security, verification and delivery, with versioned language/framework/platform adapters for what actually differs. Package resources correctly, test host behavior, declare support tiers and maintain representative fixtures. A stack-neutral vocabulary alone does not create stack-neutral engineering.

**6. What would make it significantly better than typical collections?**

Evidence that using it improves outcomes: executable examples, reproducible task evaluations, adversarial safety tests, honest compatibility claims, explicit failure/recovery procedures, traceable standards mappings and regression-backed maintenance. A smaller proven library is more valuable than a large collection of plausible instructions.

**7. What should be implemented first?**

Implement R01–R04: durable delivery semantics, consistent offline retention, redacted checks/correct security guarantees, and a genuine execution boundary. Ship those with regression tests. Then repair the installer/dependency model and shared gate logic before expanding platform coverage.
