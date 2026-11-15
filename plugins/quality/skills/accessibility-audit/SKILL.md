---
name: accessibility-audit
description: "Audit a screen, page, feature or PR for accessibility against WCAG 2.2 AA, on web and mobile — automated checks added to the tests (labels, tap targets, contrast), a text-scaling test to 200%, manual checks (screen-reader labels and order, state not by colour alone, contrast per token pair, targets, reduced motion, time limits, sound/haptics, right-to-left, error announcements) and a screen-reader pass on a real device. Use for UI-heavy changes and before release. Trigger on /accessibility-audit, 'accessibility check', 'a11y review', 'is this accessible', 'screen reader', 'contrast check', 'WCAG'."
argument-hint: "[screen, page, feature folder, PR or design]"
license: MIT
metadata:
  version: "1.0.0"
---

# Accessibility audit

Audit `$ARGUMENTS` (a screen, page, feature folder, PR or design). If empty, audit the UI files in the current branch's diff. Critical flows must be usable by everyone: someone with large text, someone using a screen reader, someone in a hurry or under stress.

## 0. Read the project

1. Read `AGENTS.md` / `CLAUDE.md` and the design system: the colour tokens, the type scale, the components, any measured contrast table.
2. Find the existing accessibility helpers in the tests (guideline matchers, an "expect accessible" helper, axe runs).
3. Detect the platform and open the reference: [references/web.md](references/web.md) · [references/mobile.md](references/mobile.md) · [references/flutter.md](references/flutter.md).

## 1. Automated checks (added to the tests)

Add to the screen's or page's UI test, so a regression fails the build:
- every interactive element has an accessible name;
- tap/click targets ≥ 48×48 dp on Android, ≥ 44×44 pt on iOS, ≥ 24×24 CSS px (WCAG 2.2 minimum; 44 px recommended) on web;
- text contrast ≥ 4.5:1 (large text ≥ 3:1), UI parts and focus indicators ≥ 3:1;
- a text-scale test at **200%**: no overflow or clipped controls, key text still visible.

**Gate:** the automated checks run in the test suite and pass.

## 2. Manual checks

| Area | Check |
|---|---|
| Labels | Icon-only buttons have labels from the localisation files; list items and map markers announce what they are and their state. |
| Order | Reading order follows visual order; decorative images and backgrounds are excluded from the accessibility tree. |
| State not only by colour | Success, warning, error, offline, selected each also have text or an icon shape. |
| Contrast | Each new text/background token pair measured; a pair that fails is not used for text. Brand colours that fail with white text are decoration only. A new pair gets a row in the project's contrast test if it has one. |
| Targets | Large and forgiving for critical actions; spacing between adjacent targets. |
| Motion | Pulses, spinners, parallax and auto-playing animation stop when the OS asks for reduced motion. |
| Text scaling | Layout works at 200% (WCAG 1.4.4) and reflows at 320 CSS px on web (1.4.10). |
| Time limits | Timed flows announce remaining time and can be extended or cancelled without precise gestures. |
| Sound & haptics | No critical event conveyed by sound or vibration alone. |
| Right-to-left | Layouts mirror with logical/directional properties; icons that imply direction flip. |
| Errors | Error text says what happened and what to do, and is announced (live region / accessibility announcement). |
| Focus | Keyboard (and switch access) reaches everything, focus is visible and never trapped; dialogs move and return focus. |
| Authentication | No cognitive test without an alternative (WCAG 3.3.8); paste allowed in code and password fields. |

## 3. On a device

For UI-heavy changes: navigate the flow end to end with the platform screen reader (TalkBack, VoiceOver; a desktop screen reader for web), perform the main action and its cancel, at the largest system font. Record what was tested in the PR.

**Gate:** the main action of the flow can be completed with a screen reader and with the largest font.

## 4. Output

Findings with severity (`critical` = a critical action cannot be completed with a screen reader, keyboard or large text), `file:line`, the WCAG criterion, and the fix; plus the list of checks passed. The automated checks become part of the fix.

## Rules

- Never fix contrast by lightening a warning or error state until it no longer stands out; pick a darker token.
- Accessibility labels come from the localisation files like any other string.
- An accessibility regression on a critical flow blocks the merge.

## Composition

| From | This skill | To |
|---|---|---|
| `code-review` (dimension 8), `design-to-screen` (mobile plugin), `add-web-page` (web plugin), `release` (lifecycle) | Automated + manual + device checks | `file-bug` (lifecycle) for findings outside the change; `device-test` (mobile) for the device pass |
