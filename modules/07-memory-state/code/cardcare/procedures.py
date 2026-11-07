"""Procedural memory: the versioned instruction, and the reviewed path by which episodes become rules.

The rules the agent follows live in an instruction file with a version, never in a searchable store
where they could drift. v1 is committed next to this file. Promotion is a policy decision:
  - evidence: the same case outcome in conversations with at least two different customers (scheduler-only
    sessions do not count), decided in at least two separate back-office decisions (cases decided in one
    batch share a decision_id, so a batch is one decision however many cases it closes);
  - routing by source, not by wording: every rule promoted from dispute outcomes changes how disputes are
    taken, so it needs both an ops lead and the disputes policy owner. No phrasing of the rule can route
    around that, because the rule's text is not what decides it;
  - review: the model drafts, a person edits, the person's text ships. A promotion without the draft it was
    reviewed from is refused, and the diff between draft and approved text is recorded;
  - approvers are named people whose roles come from a registry (procedure_versions/reviewers.json), never
    a role the approver asserts on the command line;
  - scope: procedural text reaches every customer's prompt, so it may name no customer, case or
    transaction. Provenance (which episodes, which customers) lives in the registry, an audit log the
    model never sees;
  - retraction: only the active version can be retracted, back to the version it was promoted from (or that
    version's own base), and only by a reviewer who holds a registry role. A retracted version is marked and can
    never be made active again by retraction: bringing its rule back is a new promotion, with the same evidence,
    draft and approvals. The retraction reports every conversation held under the retracted version, for review;
  - the registry is read, changed and written under a file lock and replaced atomically, so two reviewers acting
    at once cannot lose each other's change.
Promoted versions are written under var/ so a fresh run always starts from v1; in production that write
would be a reviewed pull request against procedure_versions/.
"""

import difflib
import fcntl
import json
import os
import re
import textwrap
from contextlib import contextmanager
from pathlib import Path

from cardcare import world

BASELINE_DIR = Path(__file__).resolve().parent / "procedure_versions"
BASELINE_VERSION = "v1"
PROMOTION_MIN_DISTINCT_USERS = 2
PROMOTION_MIN_DISTINCT_DECISIONS = 2
POLICY_OWNER_ROLE = "disputes_policy_owner"
OPS_ROLE = "ops_lead"
REQUIRED_ROLES_FOR_DISPUTE_RULES = (OPS_ROLE, POLICY_OWNER_ROLE)
_REVIEWERS = json.loads((Path(__file__).resolve().parent / "procedure_versions" / "reviewers.json").read_text())
_NO_RULES_LINE = "(none yet: rules learned from past conversations are added here only after human review)"
_REFUSAL = re.compile(
    r"\b(do not|don't|never)\s+(\w+\s+){0,2}(file|submit|re-?file|call file_dispute)\b"
    r"|\bonly\s+(\w+\s+){0,2}(file|submit|call file_dispute)\b"
    r"|\b(cannot|can't|must not|may not)\s+(\w+\s+){0,2}(file|submit|re-?file|be filed|be accepted)\b"
    r"|\b(isn't|is not|are not|aren't|not)\s+(\w+\s+){0,1}accepted\b",
    re.IGNORECASE,
)
_RECORD_ID = re.compile(r"\b[CTF]-[0-9a-f]{4,8}\b")


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
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(registry, indent=2))
    os.replace(tmp, path)


@contextmanager
def _registry_lock(var_dir: Path):
    lock = var_dir / "procedures" / ".registry.lock"
    lock.parent.mkdir(parents=True, exist_ok=True)
    with open(lock, "w") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


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
        f"- What you remember about this customer (their facts only; current, and authoritative over anything recalled from past conversations):\n"
        f"{textwrap.indent(profile, '  ')}\n"
        f"- What Kestrel keeps from this conversation: its transcript, which is everything the customer types (including any last four "
        f"and ZIP they gave; card numbers the masking recognises are replaced by [REDACTED ...]), for up to 30 days from its first "
        f"message; then only a short summary, kept 180 days; the facts above until they change or expire. Dispute cases and messages "
        f"already sent are bank records with their own retention.\n"
    )


def identifiers_in(text: str) -> list[str]:
    """Customer names, user ids, and case / transaction / follow-up ids found in a piece of rule text."""
    found = [m.group() for m in _RECORD_ID.finditer(text)]
    for user_id, display_name, _, _ in world.CUSTOMERS:
        found += [m.group() for m in re.finditer(rf"\b({re.escape(user_id)}|{re.escape(display_name)})\b", text, re.IGNORECASE)]
    return found


def refusal_language(text: str) -> list[str]:
    return [m.group() for m in _REFUSAL.finditer(text)]


def promotion_candidates(episodes: list[dict], registry: dict) -> list[dict]:
    """Case outcomes that recur in conversations with distinct customers, from distinct decisions, not yet covered."""
    covered = {rule["resolution_code"] for rule in registry["versions"][registry["active"]]["rules"]}
    by_code: dict[str, dict] = {}
    for episode in episodes:
        if not episode.get("customer_present"):
            continue
        for outcome in episode["outcomes"]:
            code = outcome.get("resolution_code")
            if not code or code in covered:
                continue
            group = by_code.setdefault(code, {"resolution_code": code, "users": set(), "decisions": set(), "episodes": [],
                                              "lessons": [], "notes": set()})
            group["users"].add(episode["user_id"])
            group["decisions"].add(outcome.get("decision_id") or f"(undated decision on {outcome['case_id']})")
            group["episodes"].append(episode["episode_id"])
            group["lessons"].append(episode["lesson"])
            group["notes"].add(outcome.get("resolution_note") or "")
    return [
        {**group, "users": sorted(group["users"]), "decisions": sorted(group["decisions"]), "notes": sorted(group["notes"])}
        for group in by_code.values()
        if len(group["users"]) >= PROMOTION_MIN_DISTINCT_USERS and len(group["decisions"]) >= PROMOTION_MIN_DISTINCT_DECISIONS
    ]


def rule_drafting_prompt(candidate: dict) -> str:
    lessons = "\n".join(f"- {lesson}" for lesson in candidate["lessons"])
    notes = "\n".join(f"- {note}" for note in candidate["notes"] if note)
    return (
        "You maintain the operating procedure of a card-issuer support assistant. Disputes from "
        f"{len(candidate['users'])} different customers were decided with outcome {candidate['resolution_code']}.\n"
        f"Back-office notes:\n{notes}\nLessons written after those conversations:\n{lessons}\n\n"
        "Draft ONE imperative rule (at most two sentences) for the assistant that would make this outcome less likely. "
        "Name the tool behaviour precisely (for example what to ask for before calling file_dispute and what to pass as "
        "evidence_note). Do not name any customer, case or transaction. Output only the rule text; a human reviewer will edit it."
    )


def approver_roles(approvers: list[str]) -> list[dict]:
    """Named approvers and the roles the registry gives them; unknown names get none."""
    return [{"name": name, "roles": list(_REVIEWERS.get(name, []))} for name in approvers]


def rule_review_problems(rule_text: str, draft_text: str, approvers: list[str]) -> list[str]:
    """Why this rule cannot ship with these approvers (empty if it can). The text's wording never lowers the bar."""
    problems = []
    if not draft_text.strip():
        problems.append("a promotion needs the model draft it was reviewed from")
    if identifiers_in(rule_text):
        problems.append(f"rule text may not identify customers or records: {identifiers_in(rule_text)}")
    roles = {role for approver in approver_roles(approvers) for role in approver["roles"]}
    missing = [role for role in REQUIRED_ROLES_FOR_DISPUTE_RULES if role not in roles]
    if missing:
        problems.append(f"a rule learned from dispute outcomes needs approval from {', '.join(REQUIRED_ROLES_FOR_DISPUTE_RULES)}; "
                        f"missing: {', '.join(missing)}")
    return problems


def promote(var_dir: Path, candidate: dict, draft_text: str, approved_text: str, approvers: list[str], now: str) -> str:
    """Write a new version = active text + the reviewer's approved rule, and make it active. Raises ValueError on any review problem."""
    approved_text = approved_text.strip()
    problems = rule_review_problems(approved_text, draft_text, approvers)
    if problems:
        raise ValueError("; ".join(problems))
    with _registry_lock(var_dir):
        return _promote_locked(var_dir, candidate, draft_text, approved_text, approvers, now)


def _promote_locked(var_dir: Path, candidate: dict, draft_text: str, approved_text: str, approvers: list[str], now: str) -> str:
    registry = load_registry(var_dir)
    base_version = registry["active"]
    new_version = f"v{len(registry['versions']) + 1}"
    rule_id = f"R{sum(len(v['rules']) for v in registry['versions'].values()) + 1}"
    rule = {
        "rule_id": rule_id,
        "resolution_code": candidate["resolution_code"],
        "approved_text": approved_text,
        "draft_text": draft_text.strip(),
        "edited": approved_text != draft_text.strip(),
        "diff": list(difflib.unified_diff(draft_text.strip().split(". "), approved_text.split(". "), "draft", "approved", lineterm="")),
        "refusal_language_in_draft": refusal_language(draft_text),
        "approvals": approver_roles(approvers),
        "approved_at": now,
        "evidence_episodes": candidate["episodes"],
        "evidence_users": candidate["users"],
        "evidence_decisions": candidate["decisions"],
    }
    rule_line = f"- {approved_text} (Rule {rule_id}, added in {new_version} on {now[:10]} after review.)"
    base_text = procedure_text(var_dir, base_version)
    new_text = base_text.replace(_NO_RULES_LINE, rule_line) if _NO_RULES_LINE in base_text else base_text.rstrip() + "\n" + rule_line + "\n"
    (var_dir / "procedures").mkdir(parents=True, exist_ok=True)
    (var_dir / "procedures" / f"{new_version}.md").write_text(new_text)
    registry["versions"][new_version] = {"rules": registry["versions"][base_version]["rules"] + [rule], "based_on": base_version}
    registry["active"] = new_version
    registry["history"].append({"event": "promoted", "version": new_version, "based_on": base_version, "by": approvers, "at": now})
    _save_registry(var_dir, registry)
    return new_version


def _ancestors(registry: dict, version: str) -> list[str]:
    chain = []
    while (version := registry["versions"].get(version, {}).get("based_on")):
        chain.append(version)
    return chain


def retract(var_dir: Path, to_version: str, reviewer: str, reason: str, now: str) -> dict:
    """Retract the active version: point the instruction back at a version it was built on. Nothing is deleted, so it
    stays auditable. Raises ValueError for anything else (an unknown or retracted target, a reviewer with no role)."""
    roles = approver_roles([reviewer])[0]["roles"]
    if not roles:
        raise ValueError(f"{reviewer!r} holds no reviewer role in the registry; a retraction needs an {OPS_ROLE} or a {POLICY_OWNER_ROLE}")
    with _registry_lock(var_dir):
        registry = load_registry(var_dir)
        active = registry["active"]
        if to_version not in registry["versions"]:
            raise ValueError(f"unknown procedure version {to_version}")
        if registry["versions"][to_version].get("retracted"):
            raise ValueError(f"{to_version} was retracted; bringing its rule back is a new promotion, with evidence and approvals")
        if to_version not in _ancestors(registry, active):
            raise ValueError(f"{to_version} is not a version {active} was built on; only the active version can be rolled back, to its base")
        registry["versions"][active]["retracted"] = {"by": reviewer, "roles": roles, "reason": reason, "at": now}
        registry["active"] = to_version
        registry["history"].append({"event": "retracted", "version": active, "active_now": to_version, "by": reviewer, "roles": roles,
                                    "reason": reason, "at": now})
        _save_registry(var_dir, registry)
    return registry


def conversations_under_version(episodes: list[dict], version: str) -> list[dict]:
    """Every remembered conversation held while `version` was in force: the review list after a retraction."""
    return [{"user_id": e["user_id"], "episode_id": e["episode_id"], "at": e["at"], "outcomes": e["outcomes"]}
            for e in episodes if e.get("procedure_version") == version]
