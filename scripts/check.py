#!/usr/bin/env python3
"""Repository checks for the skills marketplace. Standard library only.

Checks:
  manifests   marketplace.json and every plugin.json parse, point at real folders, and agree on name and version
  skills      every SKILL.md has valid frontmatter (Agent Skills rules), its name equals its folder,
              its metadata.version equals its plugin's version, and it has the house sections
  agents      every agent file has name + description frontmatter
  links       every relative Markdown link resolves to a file in the repository
  frameworks  no framework, language or vendor name in a SKILL.md (stack detail lives in references/)
  privacy     no product names, personal data, issue numbers, internal URLs or secrets anywhere

Usage: python3 scripts/check.py [check ...]     (no argument = all checks)
Exit code 1 when any check fails.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))


# ---------------------------------------------------------------- frontmatter

def parse_frontmatter(text: str, where: str) -> tuple[dict, str] | None:
    """Parse the small YAML subset our frontmatter uses: `key: value`, quoted values, one nested map level."""
    if not text.startswith("---\n"):
        fail(f"{where}: frontmatter must start on the first line with ---")
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        fail(f"{where}: frontmatter is not closed with ---")
        return None
    block, body = text[4:end], text[end + 5:]
    data: dict = {}
    parent: str | None = None
    for n, line in enumerate(block.splitlines(), start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^( *)([A-Za-z][\w-]*):(?: (.*))?$", line)
        if not m:
            fail(f"{where}:{n}: cannot parse frontmatter line: {line!r}")
            continue
        indent, key, value = len(m.group(1)), m.group(2), (m.group(3) or "").strip()
        value = re.sub(r"\s+#.*$", "", value) if not value.startswith(("'", '"')) else value
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
            value = value[1:-1]
            if m.group(3).strip()[0] == '"':
                value = value.replace('\\"', '"')
        if indent == 0:
            if value == "":
                data[key] = {}
                parent = key
            else:
                data[key] = value
                parent = None
        else:
            if parent is None:
                fail(f"{where}:{n}: indented key without a parent map")
                continue
            data[parent][key] = value
    return data, body


NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(-[0-9A-Za-z.-]+)?$")


# ---------------------------------------------------------------- manifests

def load_json(p: Path) -> dict | None:
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        fail(f"{rel(p)}: invalid JSON: {e}")
        return None


def plugins() -> dict[str, dict]:
    """name -> {'dir': Path, 'manifest': dict}"""
    out: dict[str, dict] = {}
    market = load_json(ROOT / ".claude-plugin" / "marketplace.json")
    if not market:
        return out
    for entry in market.get("plugins", []):
        src = entry.get("source", "")
        if not isinstance(src, str) or not src.startswith("./"):
            fail(f"marketplace.json: plugin {entry.get('name')!r} source must be a ./relative path")
            continue
        d = (ROOT / src).resolve()
        mf = load_json(d / ".claude-plugin" / "plugin.json") if d.is_dir() else None
        if mf is None:
            fail(f"marketplace.json: plugin {entry.get('name')!r} has no readable {src}/.claude-plugin/plugin.json")
            continue
        out[entry["name"]] = {"dir": d, "manifest": mf, "entry": entry}
    return out


def check_manifests() -> None:
    market = load_json(ROOT / ".claude-plugin" / "marketplace.json")
    if not market:
        return
    for key in ("name", "owner", "plugins", "description"):
        if key not in market:
            fail(f"marketplace.json: missing {key!r}")
    if not NAME_RE.match(market.get("name", "")):
        fail("marketplace.json: name must be kebab-case")
    names = [p.get("name") for p in market.get("plugins", [])]
    if len(names) != len(set(names)):
        fail("marketplace.json: duplicate plugin names")
    on_disk = {p.name for p in (ROOT / "plugins").iterdir() if p.is_dir()}
    for missing in sorted(on_disk - set(names)):
        fail(f"plugins/{missing}: folder exists but is not listed in marketplace.json")
    for name, info in plugins().items():
        mf, entry = info["manifest"], info["entry"]
        where = rel(info["dir"] / ".claude-plugin" / "plugin.json")
        if mf.get("name") != name:
            fail(f"{where}: name {mf.get('name')!r} differs from the marketplace entry {name!r}")
        if not NAME_RE.match(name) or name.startswith(("claude", "anthropic")):
            fail(f"{where}: plugin name {name!r} is not an allowed kebab-case name")
        version = mf.get("version", "")
        if not SEMVER_RE.match(version):
            fail(f"{where}: version {version!r} is not semantic (MAJOR.MINOR.PATCH)")
        if entry.get("version") and entry["version"] != version:
            fail(f"marketplace.json: {name} version {entry['version']} differs from plugin.json {version}")
        for key in ("description", "author", "license", "repository"):
            if key not in mf:
                fail(f"{where}: missing {key!r}")
        for dep in mf.get("dependencies", []):
            dep_name = dep if isinstance(dep, str) else dep.get("name")
            if dep_name not in names:
                fail(f"{where}: dependency {dep_name!r} is not a plugin of this marketplace")
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8") if (ROOT / "CHANGELOG.md").exists() else ""
        if f"{name} {version}" not in changelog:
            fail(f"CHANGELOG.md: no entry for '{name} {version}'")


# ---------------------------------------------------------------- skills and agents

REQUIRED_SECTIONS = ("## 0. Read the project", "## Rules", "## Composition")


def check_skills() -> None:
    for name, info in plugins().items():
        version = info["manifest"].get("version")
        for skill_md in sorted((info["dir"] / "skills").glob("*/SKILL.md")):
            where = rel(skill_md)
            parsed = parse_frontmatter(skill_md.read_text(encoding="utf-8"), where)
            if not parsed:
                continue
            fm, body = parsed
            folder = skill_md.parent.name
            sname, desc = fm.get("name", ""), fm.get("description", "")
            if sname != folder:
                fail(f"{where}: name {sname!r} must equal the folder name {folder!r}")
            if not NAME_RE.match(sname) or len(sname) > 64:
                fail(f"{where}: name {sname!r} breaks the Agent Skills name rules")
            if not desc:
                fail(f"{where}: description is empty")
            elif len(desc) > 1024:
                fail(f"{where}: description is {len(desc)} characters (max 1024)")
            elif "Trigger on" not in desc and "Use when" not in desc:
                fail(f"{where}: description has no trigger phrases ('Use when' / 'Trigger on')")
            meta = fm.get("metadata", {})
            if not isinstance(meta, dict) or meta.get("version") != version:
                fail(f"{where}: metadata.version must be the plugin version {version}")
            if fm.get("license") != "MIT":
                fail(f"{where}: license must be MIT")
            for section in REQUIRED_SECTIONS:
                if section not in body:
                    fail(f"{where}: missing section '{section}'")
            lines = body.count("\n")
            if lines > 450:
                fail(f"{where}: {lines} lines; move reference material to references/ (limit 450)")


def check_agents() -> None:
    for agent in sorted(ROOT.glob("plugins/*/agents/*.md")):
        parsed = parse_frontmatter(agent.read_text(encoding="utf-8"), rel(agent))
        if not parsed:
            continue
        fm, _ = parsed
        if fm.get("name") != agent.stem:
            fail(f"{rel(agent)}: name must equal the file name {agent.stem!r}")
        if not fm.get("description"):
            fail(f"{rel(agent)}: description is empty")


# ---------------------------------------------------------------- links

LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


def markdown_files() -> list[Path]:
    return [p for p in ROOT.rglob("*.md") if ".git" not in p.parts and "node_modules" not in p.parts]


def check_links() -> None:
    for md in markdown_files():
        text = md.read_text(encoding="utf-8")
        text = re.sub(r"```.*?```", "", text, flags=re.S)          # links inside code blocks are examples
        text = re.sub(r"`[^`\n]*`", "", text)
        for target in LINK_RE.findall(text):
            if re.match(r"^[a-z]+:", target) or target.startswith("#"):
                continue
            path = target.split("#", 1)[0]
            if "${" in path:
                continue
            if not (md.parent / path).resolve().exists():
                fail(f"{rel(md)}: broken link -> {target}")


# ---------------------------------------------------------------- framework names in skill bodies

def check_frameworks() -> None:
    terms = [t.strip() for t in (ROOT / "scripts" / "framework-terms.txt").read_text(encoding="utf-8").splitlines()
             if t.strip() and not t.startswith("#")]
    patterns = [(t, re.compile(r"(?<![\w.#-])" + re.escape(t) + r"(?![\w#+-])")) for t in terms]
    for skill_md in sorted(ROOT.glob("plugins/*/skills/*/SKILL.md")):
        text = skill_md.read_text(encoding="utf-8")
        for n, line in enumerate(text.splitlines(), start=1):
            if "references/" in line and "](" in line:
                line = re.sub(r"\[[^\]]*\]\(references/[^)]*\)", "", line)   # link text names the stack: allowed
            for term, pat in patterns:
                if pat.search(line):
                    fail(f"{rel(skill_md)}:{n}: framework/vendor name {term!r} in a core skill body "
                         f"(move it to references/<stack>.md)")


# ---------------------------------------------------------------- privacy

def private_term_patterns() -> list[tuple[re.Pattern[str], str]]:
    """Names that must stay out of this repo, without publishing them here.

    Read from the git-ignored `.private-terms`, one term per line. Spaces in a
    term match any spacing. Without the file (as in CI) this one rule is skipped.
    """
    path = ROOT / ".private-terms"
    if not path.is_file():
        return []
    terms = [t.strip() for t in path.read_text(encoding="utf-8").splitlines()
             if t.strip() and not t.startswith("#")]
    return [(re.compile(r"\s*".join(map(re.escape, t.split())), re.I), "private term") for t in terms]


PRIVACY = [
    *private_term_patterns(),
    (re.compile(r"[A-Za-z0-9._%+-]+@(?!users\.noreply\.github\.com)[A-Za-z0-9.-]+\.[a-z]{2,}"), "email address"),
    (re.compile(r"(?<![\w/&(\[-])#\d{2,5}\b"), "issue or PR number"),
    (re.compile(r"\+?\d{2,3}[ -]?\(?\d{3}\)?[ -]?\d{3}[ -]?\d{4}\b"), "phone number"),
    (re.compile(r"claude\.ai/(artifact|code)|docs\.google\.com|/Users/[a-z]+/"), "internal URL or path"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}|gh[pousr]_[0-9A-Za-z]{36}|sk_live_[0-9A-Za-z]{20,}|xox[baprs]-[0-9A-Za-z-]{10,}"), "secret"),
    (re.compile(r"\bgeofenc|\bSOS\b|\bghost mode\b|\bcheck-in timer", re.I), "product-specific feature term"),
]
PRIVACY_SKIP = {"scripts/check.py", ".private-terms"}  # hold the patterns themselves


def check_privacy() -> None:
    for p in ROOT.rglob("*"):
        if not p.is_file() or ".git" in p.parts or rel(p) in PRIVACY_SKIP:
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for n, line in enumerate(text.splitlines(), start=1):
            for pat, what in PRIVACY:
                m = pat.search(line)
                if m:
                    fail(f"{rel(p)}:{n}: possible {what}: {m.group(0)!r}")


CHECKS = {
    "manifests": check_manifests,
    "skills": check_skills,
    "agents": check_agents,
    "links": check_links,
    "frameworks": check_frameworks,
    "privacy": check_privacy,
}


def main(argv: list[str]) -> int:
    selected = argv or list(CHECKS)
    for name in selected:
        if name not in CHECKS:
            print(f"unknown check {name!r}; choose from {', '.join(CHECKS)}", file=sys.stderr)
            return 2
        before = len(errors)
        CHECKS[name]()
        print(f"{name:<11} {'ok' if len(errors) == before else f'{len(errors) - before} problem(s)'}")
    for e in errors:
        print(f"  {e}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
