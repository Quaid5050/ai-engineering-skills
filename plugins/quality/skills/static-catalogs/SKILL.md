---
name: static-catalogs
description: "Turn a closed set the app defines itself (languages, plans, providers, modes, built-in commands) into one table, one row per case holding every attribute, instead of the same switch repeated per attribute. Decide whether a data file plus code generation is justified (only when the source of truth lives outside the code or is shared across apps), pin today's values with characterisation tests, migrate without changing behaviour, and guard it. Use when adding one case means editing several places, or when someone proposes moving enums to a config file or codegen. Trigger on /static-catalogs, 'same switch everywhere', 'move this to YAML', 'should we codegen this', 'config file for enums', 'single source of truth', 'add a language', 'add a provider'."
argument-hint: "[type, file or feature to look at]"
license: MIT
metadata:
  version: "1.2.0"
---

# Static catalogs

Find and fix repeated per-case definitions in `$ARGUMENTS` (a type, a file or a feature). If empty, scan the
project's domain/core layer for the worst offenders and report them before changing anything.

A **catalog** is a closed set of cases the app itself defines, each with several attributes: a title, an icon, a
default, a flag, a prompt, a group. The smell is one `switch` (or `if` chain, or parallel array) **per attribute**
over the same cases. The fix is almost always one row per case, in the code, not a config file plus a generator.

## 0. Read the project

1. `AGENTS.md` / `CLAUDE.md`: layering (where pure rules live), the test command, safety-critical paths, and the
   persisted-settings rules (values saved to disk or sent over the network must never change).
2. Existing tables to copy: a type that already holds its attributes in one place is the house pattern. Follow it.
3. Existing generators: does the project already generate code (API clients, assets, translations)? Note the
   tool, where generated files live, and whether CI checks them.
4. The stack reference: [references/swift.md](references/swift.md) · [references/typescript.md](references/typescript.md).

## 1. Find the catalogs

For each candidate, write one line: the type, the number of cases, the attributes, and **how many places change
when one case is added**: count every switch arm, list entry and lookup that must be touched, across all files
(three switches and a group list = 4). Signs, worst first:

| Sign | Example |
|---|---|
| One switch per attribute over the same cases | `title`, `icon`, `hint`, `isPremium`, each its own switch |
| A value parsed back out of another value | the native name cut out of the menu title with a pattern |
| Two attributes that are always equal | `title` and `shortTitle` return the same strings |
| The same mapping repeated in a view | a screen has its own `icon(for:)` beside the type's `icon` |
| Parallel arrays or a separate order/group list | `groups` lists the cases again in display order |
| Defaults written beside the type, not in it | a default model per provider in another file |

Rank by edits per new case × how often cases are added. Report the ranking; fix the top ones. A type that already
keeps one row per case is the house pattern: report it as "already a table", add the §5 guards if missing, and
change nothing else.

Then check two facts per catalog, because both change the decision:
- **Who else lists the same ids?** Search sibling projects in the repo (a website, a backend, a worker) for the
  same ids or titles. A second copy elsewhere is §2 row 2.
- **What is persisted or sent?** Search the storage keys, settings, network payloads and analytics events for the
  raw values. Those values are frozen, however odd they look.

## 2. Choose the home

| The data is… | Home |
|---|---|
| A closed set the app owns, changed only with a release | **An in-code table** (default). One row per case, written so the language's exhaustiveness check rejects a case without a row (how: the stack reference). |
| Shared by two or more apps or languages in the repo (app and website list the same plans) | **One data file + a generator per language.** Generated files committed with a "generated, do not edit, source: …" header; CI regenerates and fails on a diff. |
| Defined by an outside spec (API schema, asset folder, translation catalog) | **The ecosystem's standard generator** for that spec. Never hand-write what a spec generates. |
| Meant to change without a release (remote config) | **Runtime data** with a typed decoder, a schema, a validation test and a safe built-in fallback. Ids stay in code. |
| Edited by the user (custom commands, saved filters) | **Not a catalog:** a repository with storage, versioned keys and a migration test. Built-in defaults may be a catalog. |

A data file plus a generator for an app-owned set adds a build step, a second language and generated diffs. It also
moves the error away from where the mistake was made. That trade only pays in rows 2–3.

**Gate:** the chosen row and the reason are written in the PR (or a decision record when it sets a project-wide
rule) before any code moves.

## 3. Shape the row

1. **Stable id.** A raw value that is saved or sent is frozen. Renaming a case never changes it.
2. **Every attribute is a field** of the row: titles, icons, flags, defaults, group, order.
3. **Derived values are computed from fields**, never parsed out of a display string. When a few cases break
   the rule, add an optional override field (empty means "derived"). Don't drop the derivation for every case.
4. **Duplicates collapse:** two always-equal attributes become one field. Keep the old accessor delegating to it
   if callers use both.
5. **Order and groups are data:** a `group` and `order` field, or the table's own order, instead of a second list.
6. **Behaviour stays code.** A prompt *template* may be data; building the prompt (interpolation, rules,
   branching) stays a function. A flag is data; what the flag does stays code.
7. **One lookup:** `row(for: id)` or the case's `info`. Callers keep their old accessors, which now read the row,
   so the change stays inside the type.

## 4. Migrate (tests first)

Follow `tdd` (this plugin). The migration is a refactor: behaviour must not change.

1. **Pin today's values:** a characterisation test over **every case × every attribute**, written against the
   current code and green before the move. Use a frozen expected table, not one computed by the code under test.
   Short fields go inline. Long text (prompts, templates, help) goes in fixture files, one per case, compared byte
   for byte. When the module has no test target yet, add one in the same layer as the catalog first.
2. **Pin the ids:** a test that the persisted raw values equal a frozen list, and that every case round-trips.
3. Move one catalog per commit, also inside a larger PR. The pinned tests stay unchanged and green after the move.
4. Remove the duplicates (view helpers, parallel lists) in the same commit, with their callers.

**Gate:** the characterisation test fails when any single value is changed by hand (break-it check), and passes
unchanged after the move.

## 5. Guard

Keep these tests next to the catalog:

- every case has exactly one row; ids unique; persisted ids equal the frozen list;
- required text fields non-empty; group and order cover every case;
- for generated code: the generator is deterministic, CI regenerates and fails on a diff, and generated files are
  never edited by hand (an architecture or lint rule if the project has one).

Adding a case is now: one row and one line in the frozen-ids list. Say so in the type's doc comment.

## Rules

- Never change a persisted or transmitted raw value, even to tidy a name.
- Never put secrets, keys or private URLs in a data file or a catalog.
- No runtime parsing of a bundled file for data that is fixed at build time; it trades compile errors for crashes.
- User-visible text follows the project's localisation system; a catalog holds the key or the default text, not a
  second translation mechanism.
- Generated files are never edited by hand; fix the source or the generator.
- Codegen only with a reason from row 2 or 3 of §2, written down.

## Composition

| From | This skill | To |
|---|---|---|
| `code-review` (this plugin) flags repeated switches; `engineering-principles` (lifecycle plugin) placement; `cleanup` (lifecycle) | Find → choose the home → shape the row → pin and migrate → guard | `tdd`, `write-tests` (this plugin); `decision` (meta plugin) when it sets a project-wide rule |
