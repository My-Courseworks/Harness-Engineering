"""Procedural memory: the versioned instruction, and the reviewed path by which episodes become rules.

The rules the agent follows live in an instruction file with a version, never in a
searchable store where they could drift. v1 is committed next to this file.
Promotion is a policy decision with a threshold (the same failure in episodes from
at least two *different* customers), a reviewer who signs off, and a retraction
path back to any earlier version. Promoted versions are written under var/ so a
fresh run always starts from v1; in production that write would be a reviewed pull
request against this directory.
"""

import json
import textwrap
from pathlib import Path

BASELINE_DIR = Path(__file__).resolve().parent / "procedure_versions"
BASELINE_VERSION = "v1"
PROMOTION_MIN_DISTINCT_USERS = 2
_NO_RULES_LINE = "(none yet: rules learned from past conversations are added here only after human review)"


def _registry_path(var_dir: Path) -> Path:
    return var_dir / "procedures" / "registry.json"


def load_registry(var_dir: Path) -> dict:
    path = _registry_path(var_dir)
    if path.exists():
        return json.loads(path.read_text())
    return {"active": BASELINE_VERSION, "versions": {BASELINE_VERSION: {"rules": []}}, "history": [
        {"event": "baseline", "version": BASELINE_VERSION}
    ]}


def _save_registry(var_dir: Path, registry: dict) -> None:
    path = _registry_path(var_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(registry, indent=2))


def procedure_text(var_dir: Path, version: str) -> str:
    if version == BASELINE_VERSION:
        return (BASELINE_DIR / f"{version}.md").read_text()
    return (var_dir / "procedures" / f"{version}.md").read_text()


def active_procedure(var_dir: Path) -> tuple[str, str]:
    """(version, text) of the instruction in force right now; read fresh every turn."""
    version = load_registry(var_dir)["active"]
    return version, procedure_text(var_dir, version)


def render_system_prompt(procedure: str, version: str, profile: str, review_days: int, now: str) -> str:
    """The instruction in force, plus the per-turn context the harness assembles around it."""
    return (
        f"{procedure}\n"
        f"## Context for this turn (assembled by the harness; procedure {version})\n"
        f"- Current time: {now}\n"
        f"- Disputes are currently reviewed in about {review_days} days (app-wide operating setting).\n"
        f"- What you remember about this customer (their facts only):\n{textwrap.indent(profile, '  ')}\n"
    )


def promotion_candidates(episodes: list[dict], registry: dict) -> list[dict]:
    """Case outcomes that recur across distinct customers' episodes and no active rule covers yet."""
    covered = {rule["resolution_code"] for rule in registry["versions"][registry["active"]]["rules"]}
    by_code: dict[str, dict] = {}
    for episode in episodes:
        for outcome in episode["outcomes"]:
            code = outcome.get("resolution_code")
            if not code or code in covered:
                continue
            group = by_code.setdefault(code, {"resolution_code": code, "users": set(), "episodes": [], "lessons": [], "notes": set()})
            group["users"].add(episode["user_id"])
            group["episodes"].append(episode["episode_id"])
            group["lessons"].append(episode["lesson"])
            group["notes"].add(outcome.get("resolution_note") or "")
    return [
        {**group, "users": sorted(group["users"]), "notes": sorted(group["notes"])}
        for group in by_code.values()
        if len(group["users"]) >= PROMOTION_MIN_DISTINCT_USERS
    ]


def rule_drafting_prompt(candidate: dict) -> str:
    lessons = "\n".join(f"- {lesson}" for lesson in candidate["lessons"])
    notes = "\n".join(f"- {note}" for note in candidate["notes"] if note)
    return (
        "You maintain the operating procedure of a card-issuer support assistant. Disputes from "
        f"{len(candidate['users'])} different customers were decided with outcome {candidate['resolution_code']}.\n"
        f"Back-office notes:\n{notes}\nLessons written after those conversations:\n{lessons}\n\n"
        "Write ONE imperative rule (at most two sentences) for the assistant that would have prevented this outcome. "
        "Name the tool behaviour precisely (for example what to ask for before calling file_dispute and what to pass "
        "as evidence_note). Output only the rule text."
    )


def promote(var_dir: Path, candidate: dict, rule_text: str, reviewer: str, now: str) -> str:
    """Write a new version = active text + the reviewed rule, and make it active. Returns the new version id."""
    registry = load_registry(var_dir)
    base_version = registry["active"]
    new_version = f"v{len(registry['versions']) + 1}"
    rule = {
        "resolution_code": candidate["resolution_code"],
        "text": rule_text.strip(),
        "evidence_episodes": candidate["episodes"],
        "evidence_users": candidate["users"],
        "approved_by": reviewer,
        "approved_at": now,
    }
    rule_line = (
        f"- {rule['text']} (Promoted {now[:10]} from {len(rule['evidence_episodes'])} episodes across customers "
        f"{', '.join(rule['evidence_users'])}; outcome {rule['resolution_code']}; approved by {reviewer}.)"
    )
    base_text = procedure_text(var_dir, base_version)
    new_text = base_text.replace(_NO_RULES_LINE, rule_line) if _NO_RULES_LINE in base_text else base_text.rstrip() + "\n" + rule_line + "\n"
    (var_dir / "procedures").mkdir(parents=True, exist_ok=True)
    (var_dir / "procedures" / f"{new_version}.md").write_text(new_text)
    registry["versions"][new_version] = {"rules": registry["versions"][base_version]["rules"] + [rule], "based_on": base_version}
    registry["active"] = new_version
    registry["history"].append({"event": "promoted", "version": new_version, "based_on": base_version, "by": reviewer, "at": now})
    _save_registry(var_dir, registry)
    return new_version


def retract(var_dir: Path, to_version: str, reviewer: str, reason: str, now: str) -> dict:
    """Point the active instruction back at an earlier version; nothing is deleted, so it stays auditable."""
    registry = load_registry(var_dir)
    if to_version not in registry["versions"]:
        raise ValueError(f"unknown procedure version {to_version}")
    retracted = registry["active"]
    registry["active"] = to_version
    registry["history"].append({"event": "retracted", "version": retracted, "active_now": to_version, "by": reviewer, "reason": reason, "at": now})
    _save_registry(var_dir, registry)
    return registry
