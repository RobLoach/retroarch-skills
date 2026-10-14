#!/usr/bin/env python3
"""Validate every skills/<slug>/SKILL.md against the repository conventions.

See CONTRIBUTING.md. A skill without a `metadata:` map is a general skill and
skips the game checks. Uses only the standard library, so the frontmatter
parser handles single-line `key: value` pairs and one nested `metadata:` map.
"""

import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
CRC_RE = re.compile(r"^[0-9a-fA-F]{8}$")
CORE_RE = re.compile(r"^[a-z0-9_+-]+_libretro$")
# RetroArch MCP tools marked destructive, plus loading content over a
# running game. Skills must not pre-approve them.
DESTRUCTIVE = {
    "WRITE_CORE_MEMORY", "LOAD_STATE_SLOT", "SAVE_STATE_SLOT",
    "PLAY_REPLAY_SLOT", "SEEK_REPLAY", "RECORD_REPLAY", "SAVE_FILES",
    "LOAD_FILES", "LOAD_CORE", "START_CORE", "LOAD_CONTENT", "CLOSE_CONTENT",
    "UNLOAD_CORE", "QUIT", "RESET",
}


def slugify(game):
    text = unicodedata.normalize("NFKD", game)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower().replace("'", "")
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")


def unquote(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def frontmatter(text):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    try:
        end = lines.index("---", 1)
    except ValueError:
        return None
    data, section = {}, None
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, sep, value = line.strip().partition(":")
        if not sep:
            continue
        if line[0] in " \t":
            if section is not None:
                data[section][key.strip()] = unquote(value)
        elif value.strip():
            data[key.strip()] = unquote(value)
            section = None
        else:
            section = key.strip()
            data[section] = {}
    return data


def check(skill, seen):
    errors = []
    slug = skill.parent.name
    data = frontmatter(skill.read_text(encoding="utf-8"))
    if data is None:
        return ["missing --- frontmatter"]

    name = data.get("name", "")
    if name != slug:
        errors.append(f"name {name!r} does not match directory {slug!r}")
    if not NAME_RE.match(slug) or len(slug) > 64:
        errors.append("directory must be lowercase letters, numbers and hyphens, at most 64 characters")

    description = data.get("description", "")
    if not description:
        errors.append("description is missing")
    elif len(description) > 1024:
        errors.append(f"description is {len(description)} characters, the limit is 1024")

    if not data.get("license"):
        errors.append("license is missing")
    compatibility = data.get("compatibility", "")
    if len(compatibility) > 500:
        errors.append(f"compatibility is {len(compatibility)} characters, the limit is 500")
    for tool in data.get("allowed-tools", "").split():
        if tool.rpartition("__")[2] in DESTRUCTIVE:
            errors.append(f"allowed-tools: {tool} can lose the user's progress; leave it to a prompt")

    metadata = data.get("metadata")
    if metadata is None:
        return errors
    if not isinstance(metadata, dict):
        return errors + ["metadata must be a map"]
    game = metadata.get("game", "")
    system = metadata.get("system", "")
    cores = metadata.get("cores", "").split()
    crc32 = metadata.get("crc32")
    if not game:
        errors.append("metadata.game is missing")
    elif slug != slugify(game) and not slug.startswith(slugify(game) + "-"):
        errors.append(f"directory should be {slugify(game)!r}, the slug of metadata.game")
    if not system:
        errors.append("metadata.system is missing")
    for core in cores:
        if not CORE_RE.match(core):
            errors.append(f"metadata.cores: {core!r} is not a core name such as fceumm_libretro")
    if crc32 is not None and not CRC_RE.match(crc32):
        errors.append("metadata.crc32 must be 8 hex digits")

    key = (game, system)
    if game and system:
        if key in seen:
            errors.append(f"same game and system as {seen[key]}")
        seen[key] = slug
    return errors


def main():
    skills = sorted(SKILLS.glob("*/SKILL.md"))
    seen, failed = {}, 0
    for skill in skills:
        errors = check(skill, seen)
        for error in errors:
            print(f"{skill.relative_to(ROOT)}: {error}")
        failed += bool(errors)
    for directory in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        if not (directory / "SKILL.md").is_file():
            print(f"{directory.relative_to(ROOT)}: missing SKILL.md")
            failed += 1
    print(f"{len(skills)} skill(s) checked, {failed} with problems")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
