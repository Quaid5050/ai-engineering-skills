# Standard labels (GitHub example)

Run with the owner's OK — labels are visible to everyone on the repository. `--force` updates colour and description of an existing label.

```bash
#!/usr/bin/env bash
set -euo pipefail
REPO="${1:?usage: setup_labels.sh owner/repo}"
label() { gh label create "$1" -R "$REPO" --color "$2" --description "$3" --force; }

label "type:feature" 1D76DB "A user-visible capability (one vertical slice)"
label "type:bug"     D73A4A "Something does not work as specified"
label "type:chore"   C5DEF5 "Maintenance, tooling, docs, refactor, spike"
label "type:epic"    5319E7 "A feature made of several slices (sub-issues)"
label "P0" B60205 "Urgent: safety, data loss or exposure; drop everything"
label "P1" D93F0B "Must for the milestone"
label "P2" FBCA04 "Should; has a workaround"
label "P3" 0E8A16 "Could; cosmetic"
label "safety-critical"   B60205 "A silent failure here can harm a person, lose money or data"
label "privacy"           5319E7 "Touches personal data, sharing or consent"
label "needs-device-test" 006B75 "Must be checked on real devices before release"
label "spike"             BFDADC "Time-boxed research; output is a decision, not merged code"
label "needs-design"      F9D0C4 "No design yet: a state table and low-fidelity flow must be approved first"
label "in-progress"       0052CC "Someone is working on it"
label "blocked"           000000 "Cannot move; see the Blocked by comment"
for r in decision design depends-on account device; do
  label "blocked:$r" 444444 "Blocked by: $r"
done
# Areas: one per module, e.g.
for a in server client web mobile data infra ci docs; do
  label "area:$a" EDEDED "Touches $a"
done
```

Feature labels are created per feature by `feature-to-issues`: `gh label create "feature:<slug>" -R "$REPO" --color 1D76DB --description "<Feature>"` (no `--force`, so an existing label is kept).

Blocked issues say why: `blocked` + every matching `blocked:<reason>`, and a comment `**Blocked by:** …` naming what unblocks it (`Blocked by #N` for `depends-on`). When the blocker clears, remove the labels and say so in a comment.
