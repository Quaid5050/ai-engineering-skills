# Lessons log

How the skills stay current: every real lesson becomes a **check, a gate or a rule**, and is logged here. A lesson nobody encodes is lost at the next session — agents start fresh and follow only what is written.

## From a real project to a skill change

```
something went wrong (bug, review miss, audit, incident, an agent copied a bad pattern)
        │
        ▼
1. Write it as a lesson (below): what happened, why it was not caught, which rung should have caught it
        │
        ▼
2. Generalise: strip the product, the stack and the people — does it hold on any stack?
   only on one stack → it goes in that stack's references/<stack>.md, not in a core skill
        │
        ▼
3. Pick the guard, cheapest and earliest first:
   machine check (test, lint, CI job, hook) → gate in the skill at the step where the mistake is made
   → checklist row → rule in a convention
        │
        ▼
4. Edit the skill with create-skill; dry-run with a fresh agent on a task that reproduces the
   original mistake — the updated skill must now stop it (two stacks for a core skill)
        │
        ▼
5. Bump the plugin version, add a CHANGELOG entry linking the lesson, open a PR, review, merge
        │
        ▼
6. Mark the lesson "applied in <plugin> <version>"
```

The `capture-lesson` skill (meta plugin) runs this process. "Be more careful" is never a change.

**Prevention/detection layers** are selected by effectiveness and cost, not a universal sequence; see `testing-doctrine`. Design/threat review can precede code. Historical entries below describe earlier policy; the amendment supersedes overgeneralized rules.

## Entry format

```markdown
### L<n> · <YYYY-MM-DD> — <one-line lesson>
- **What happened:** …
- **Why it was not caught:** …
- **Rung:** caught at … ; should have been caught at …
- **Generalised rule:** …
- **Change:** <skills, checks>
- **Status:** proposed | applied in <plugin> <version>
```

No personal data, product names, customer names or links to private projects.

---

## Log

### L1 · 2026-11-15 — The skills said what each layer *is*; the tests only checked names and imports
- **What happened:** Conventions described each layer precisely, and architecture tests were green, yet a hand-written binary file parser landed in the domain layer, and a feature added its own storage class and built validation inline in a request handler. Every test passed.
- **Why it was not caught:** The layer tests were denylists ("the domain does not reference the ORM"); a parser references nothing on the list. No rule said where a technical kind of code (parsing, storage, validation) lives.
- **Rung:** caught at an external audit; should have been caught at the architecture test, and before that at design review.
- **Generalised rule:** Layer rules are **allowlists** with **empty baselines**; there are no exceptions by precedent. The domain holds business concepts only — the **concept test** — and technical code goes in an adapter even when it is pure.
- **Change:** `engineering-principles` §1 (concept test, principle 10), [architecture-tests reference](../plugins/lifecycle/skills/engineering-principles/references/architecture-tests.md); `code-review` dimension "layer placement"; `bootstrap-project` installs allowlist tests from day one.
- **Status:** applied in lifecycle 1.0.0, quality 1.0.0

### L2 · 2026-11-15 — Every technical kind of code needs one stated home
- **What happened:** Without a stated home, each feature invented one: per-feature storage, a second upload reader, secrets reusing another purpose's key, a background loop holding business rules.
- **Why it was not caught:** "Where does this go?" had no written answer for technical code, so agents copied whatever was nearest.
- **Rung:** caught at review, late; should have been caught at design review and by a placement test.
- **Generalised rule:** One **placement row** per technical kind of code — secrets and crypto per purpose, one generic object-storage port, one upload reader, rate limiters, outbound-call resilience with one retry owner, coordinators/background loops that make one use-case call per pass, shared code — each with a home, a rule and a check. A `utils` folder is not bad; **a folder with no rules is**.
- **Change:** `engineering-principles` §3 and [placement-table reference](../plugins/lifecycle/skills/engineering-principles/references/placement-table.md); `backend-conventions`, `mobile-conventions` (shared module with rules).
- **Status:** applied in lifecycle 1.0.0, backend 1.0.0, mobile 1.0.0

### L3 · 2026-11-15 — Judgement steps must be explicit, posted and gated
- **What happened:** Agents follow written rules and copy nearby code. A wrong placement that nobody stopped became the template the next feature copied.
- **Why it was not caught:** Design judgement was "part of the review" — so it was sometimes shortened or skipped, and never visible.
- **Rung:** should have been caught at design review, which did not exist as a gate.
- **Generalised rule:** An **architect design review is posted on the issue before the first code commit** for every feature and non-trivial fix, answering placement, reuse and *"would the next feature have to write this again?"*; and **`code-review` has a separate design pass**, where a finding the next feature would copy is `major`.
- **Change:** `design-review` (new), `architect` agent, `start-issue`, `new-feature`, `spec`, `bugfix`, `implement`; `code-review` §2a.
- **Status:** applied in lifecycle 1.0.0, quality 1.0.0, agents 1.0.0

### L4 · 2026-11-15 — Green tests are not enough to merge
- **What happened:** Changes with green CI and a positive summary from the authoring session still carried problems a human reading the diff would have seen.
- **Why it was not caught:** The merging session trusted the summary and the checks.
- **Rung:** should have been caught at merge.
- **Generalised rule:** **The merging session reads the diff itself.** It is one of the eight merge gates.
- **Change:** `merge` gate 7; `create-pr`.
- **Status:** applied in lifecycle 1.0.0

### L5 · 2026-11-15 — The speed rule
- **What happened:** Briefs that asked to "go faster" led to skipped design reviews and shortened design passes.
- **Why it was not caught:** Nothing said which parts of the process may be cut for speed.
- **Rung:** process; should have been explicit in every brief.
- **Generalised rule:** Speed may reduce **test reruns and review rounds**, never **the tests written, the design review or the design pass**. Every brief that starts or reviews work names both as required.
- **Change:** `merge`, `new-feature`, `design-review`, `code-review`, the `architect` and `reviewer` agents.
- **Status:** applied in lifecycle 1.0.0, quality 1.0.0, agents 1.0.0

### L6 · 2026-11-15 — Never attach a self-hosted CI runner to a public repository
- **What happened:** A private project ran CI on a self-hosted machine. Making such a repository public would let anyone who opens a pull request run code on that machine.
- **Generalised rule:** Public repositories use hosted runners only; a repository with a self-hosted runner stays private while it is attached.
- **Change:** `ci`, `bootstrap-project`; this repository's CI uses hosted runners only.
- **Status:** applied in lifecycle 1.0.0

### L7 · 2026-11-27 — Correctness and proportionate verification supersede ceremony
- **What happened:** The audit found unsafe delivery/recovery rules, inconsistent review prerequisites and architecture/testing preferences expressed as universal requirements.
- **Why it was not caught:** Syntax checks did not exercise persistence failures, workflows or adversarial inputs.
- **Generalised rule:** Match process depth to impact while preserving authorization, integrity and meaningful verification. Persistent intent is not completion; a prompt/hook is not a security boundary; support claims need evidence.
- **Change:** Foundation, corrected procedures, redacted tooling, durable fixtures, dependency/installation checks and scoped capabilities. L1–L3/L5 architecture/review absolutes are superseded by the risk-based workflow; their original incidents remain recorded.
- **Status:** proposed in the remediation branch; release evidence is recorded separately.
