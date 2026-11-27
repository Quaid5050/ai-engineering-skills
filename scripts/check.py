#!/usr/bin/env python3
"""Repository checks for the skills marketplace. Requires PyYAML from requirements-dev.txt.

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
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors: list[str] = []


def fail(msg: str) -> None:
    for pattern, category in globals().get("PRIVACY", []):
        msg = pattern.sub("<redacted " + category + ">", msg)
    errors.append(msg)


def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))


# ---------------------------------------------------------------- frontmatter

class UniqueSafeLoader(yaml.SafeLoader):
    """Reject duplicates instead of silently replacing a policy value."""


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str) or key in result:
            raise ValueError("duplicate or non-string mapping key")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueSafeLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def parse_frontmatter(text: str, where: str) -> tuple[dict, str] | None:
    if not text.startswith("---\n"):
        fail(f"{where}: frontmatter must start on the first line")
        return None
    end = text.find("\n---\n", 4)
    if end < 0 or end > 65536:
        fail(f"{where}: missing or oversized frontmatter")
        return None
    block = text[4:end]
    try:
        if any(isinstance(t, (yaml.tokens.AliasToken, yaml.tokens.AnchorToken)) for t in yaml.scan(block)):
            raise ValueError("aliases and anchors are not supported")
        data = yaml.load(block, Loader=UniqueSafeLoader)
        if not isinstance(data, dict):
            raise ValueError("frontmatter must be a mapping")
        for key in ("name", "description", "license", "argument-hint", "compatibility"):
            if key in data and not isinstance(data[key], str):
                raise ValueError("metadata field must be a string")
        if "metadata" in data and (not isinstance(data["metadata"], dict) or
                any(not isinstance(k, str) or not isinstance(v, str) for k, v in data["metadata"].items())):
            raise ValueError("metadata must map strings to strings")
    except (yaml.YAMLError, ValueError, TypeError, RecursionError):
        # Parser exceptions can contain source text, including secrets. Do not echo them.
        fail(f"{where}: invalid frontmatter syntax, duplicate key, type or unsupported alias")
        return None
    return data, text[end + 5:]


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
        if not isinstance(src, str) or not src.startswith("./") or ".." in Path(src).parts:
            fail(f"marketplace.json: plugin {entry.get('name')!r} source must be a ./relative path")
            continue
        d = (ROOT / src).resolve()
        if not d.is_relative_to(ROOT.resolve()):
            fail("marketplace.json: plugin source escapes repository")
            continue
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
            elif not any(phrase in desc for phrase in ("Trigger on", "Use when", "Use for")):
                fail(f"{where}: description has no applicability phrase")
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
                    fail(f"{rel(p)}:{n}: possible {what} (value redacted)")


def check_catalog() -> None:
    path = ROOT / "catalog" / "skills.json"
    data = load_json(path)
    if not isinstance(data, dict) or set(data) != {"schema_version", "skills"} or type(data.get("schema_version")) is not int or data.get("schema_version") != 1 or not isinstance(data.get("skills"), list):
        fail("catalog: invalid schema version or skills array")
        return
    entries = data["skills"]
    required = {"name", "plugin", "path", "version", "description", "requires", "optional_companions", "support", "owner", "resources"}
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != required:
            fail("catalog: unexpected or missing entry fields"); return
        for key in required - {"requires", "optional_companions", "resources"}:
            if not isinstance(entry[key], str) or not entry[key]:
                fail("catalog: non-string or empty metadata"); return
        for key in ("requires", "optional_companions", "resources"):
            values = entry[key]
            if not isinstance(values, list) or any(not isinstance(v, str) or not v for v in values) or len(set(values)) != len(values):
                fail("catalog: malformed or duplicate list values"); return
    names = [e.get("name") for e in entries if isinstance(e, dict)]
    if len(names) != len(entries) or len(set(names)) != len(names):
        fail("catalog: invalid or duplicate skill entries")
        return
    lookup = {e["name"]: e for e in entries}
    for entry in entries:
        if any(n not in lookup for n in entry["optional_companions"]):
            fail("catalog: unknown optional companion")
    disk = {p.parent.name for p in ROOT.glob("plugins/*/skills/*/SKILL.md")}
    if set(names) != disk:
        fail("catalog: registered skills differ from filesystem")
    visiting, done = set(), set()
    def visit(name):
        if name in visiting:
            fail("catalog: required dependency cycle")
            return
        if name not in lookup:
            fail("catalog: missing required dependency")
            return
        if name in done: return
        visiting.add(name)
        for dependency in lookup[name].get("requires", []): visit(dependency)
        visiting.remove(name); done.add(name)
    for entry in entries:
        name = entry["name"]
        if not isinstance(name, str) or not NAME_RE.fullmatch(name):
            fail("catalog: invalid skill identifier"); continue
        if entry.get("path") != f"plugins/{entry.get('plugin')}/skills/{name}":
            fail("catalog: skill path does not match its owner/name"); continue
        directory = ROOT / entry["path"]
        if directory.is_symlink() or not directory.resolve().is_relative_to(ROOT.resolve()):
            fail("catalog: skill path escapes repository"); continue
        for key in ("requires", "optional_companions", "resources"):
            if not isinstance(entry.get(key), list) or any(not isinstance(x,str) for x in entry.get(key, [])):
                fail("catalog: invalid list metadata"); return
        if entry.get("support") not in ("documented", "fixture-tested", "agent-evaluated"):
            fail("catalog: unknown support tier")
        resources = {str(p.relative_to(directory)) for p in directory.rglob("*") if p.is_file()}
        if set(entry["resources"]) != resources:
            fail(f"catalog: resource inventory stale for {name}")
        for resource in entry["resources"]:
            target = directory / resource
            if Path(resource).is_absolute() or ".." in Path(resource).parts or target.is_symlink() or not target.resolve().is_relative_to(directory.resolve()):
                fail(f"catalog: unsafe resource for {name}")
        parsed = parse_frontmatter((directory / "SKILL.md").read_text(), entry["path"])
        if parsed and entry.get("version") != parsed[0].get("metadata", {}).get("version"):
            fail(f"catalog: version differs for {name}")
        visit(name)
    manifests = plugins()
    active, visited = set(), set()
    def visit_plugin(name):
        if name in active:
            fail("manifests: plugin dependency cycle"); return
        if name in visited or name not in manifests: return
        active.add(name)
        for dep in manifests[name]["manifest"].get("dependencies", []):
            visit_plugin(dep if isinstance(dep,str) else dep.get("name"))
        active.remove(name); visited.add(name)
    for name in manifests: visit_plugin(name)


CHECKS = {
    "manifests": check_manifests,
    "catalog": check_catalog,
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
