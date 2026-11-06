"""Episodic memory's write path: turns become short reflections, never stored transcripts.

Extraction is model-driven (the reflection prompt), so its output is a candidate and goes through a
validation stage before it is stored:
  - card data is masked again;
  - anything that identifies another customer (their name, user id, or a case that is not on this
    customer's account) is replaced, so one customer's episode can never carry another's data;
  - the structured outcome next to it comes from the case system of record, not from the model.

Reflection is incremental. A session records how many of its customer turns are already reflected,
and each reflection covers only the turns after that mark. Re-reflecting a whole transcript, which is
how a resumed old session could re-create an episode retention had deleted, cannot happen.
"""

import json
import re

from cardcare import world
from cardcare.memory_policy import episode_expires_at, redact_card_secrets

_CASE_ID = re.compile(r"\bC-\d{4}\b")

REFLECTION_PROMPT = """You write the long-term memory entry for part of a conversation between a card issuer's support assistant and one customer.
Return a JSON object with exactly two keys:
  "summary": at most 60 words. What the customer wanted, what was done (with case and transaction ids), anything promised and when, and any preference the customer stated. Report what the customer claimed but no tool confirmed as "the customer said ... (not verified)".
  "lesson": one sentence on what the assistant should do differently next time, judged by how the conversation went and by any case outcome in it; or "none". Do not blame the assistant for a tool refusing a call it then retried successfully.
Use only facts present in the transcript. Never include card numbers or security codes. Refer to people other than this customer only as "another customer".

Transcript:
{transcript}"""


def format_transcript(turns: list[dict]) -> str:
    """turns: [{"role": "customer" | "assistant" | "tool", "text": str}] in order."""
    return "\n".join(f"{turn['role']}: {turn['text']}" for turn in turns if turn["text"].strip())


def group_by_customer_turn(turns: list[dict]) -> list[list[dict]]:
    """Split a flat transcript into one group per customer turn (the customer message and everything after it)."""
    groups: list[list[dict]] = []
    for turn in turns:
        if turn["role"] == "customer" or not groups:
            groups.append([])
        groups[-1].append(turn)
    return groups


def reflection_prompt(turns: list[dict]) -> str:
    return REFLECTION_PROMPT.format(transcript=format_transcript(turns))


def scrub_other_customers(text: str, user_id: str, own_case_ids: set[str]) -> str:
    """Authorization before storage: nothing that identifies another customer enters this customer's memory."""
    for other_id, display_name, _, _ in world.CUSTOMERS:
        if other_id == user_id:
            continue
        text = re.sub(rf"\b({re.escape(other_id)}|{re.escape(display_name)})('s)?\b", "another customer", text, flags=re.IGNORECASE)
    return _CASE_ID.sub(lambda m: m.group() if m.group() in own_case_ids else "[a case not on this account]", text)


def parse_reflection(raw: str, user_id: str, own_case_ids: set[str]) -> dict:
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    try:
        data = json.loads(match.group()) if match else {}
    except json.JSONDecodeError:
        data = {}

    def validate(value: str, limit: int) -> str:
        return scrub_other_customers(redact_card_secrets(value[:limit]), user_id, own_case_ids)

    return {"summary": validate(str(data.get("summary") or raw.strip()), 600), "lesson": validate(str(data.get("lesson") or "none"), 300)}


def case_outcomes(bank_db, user_id: str, turns: list[dict]) -> list[dict]:
    """Structured outcomes of every case of this customer's that the turns touched, read from the case system."""
    case_ids = sorted({case_id for turn in turns for case_id in _CASE_ID.findall(turn["text"])})
    return [
        {key: case[key] for key in ("case_id", "txn_id", "reason", "status", "resolution_code", "resolution_note", "resolved_at")}
        for case in world.cases_by_id(bank_db, case_ids)
        if case["user_id"] == user_id
    ]


def own_case_ids(bank_db, user_id: str) -> set[str]:
    return {case["case_id"] for case in world.list_cases(bank_db, user_id, None)}


def build_episode(user_id: str, session_id: str, sequence: int, now: str, reflection: dict, outcomes: list[dict],
                  procedure_version: str, customer_present: bool) -> dict:
    outcome_text = "; ".join(
        f"{o['case_id']} {o['status']}" + (f" ({o['resolution_code']})" if o["resolution_code"] else "") for o in outcomes
    ) or "no case touched"
    opening = f"Conversation on {now[:10]}" if customer_present else f"Scheduled follow-up on {now[:10]} (customer not present)"
    return {
        "episode_id": f"E-{session_id}-{sequence}",
        "user_id": user_id,
        "session_id": session_id,
        "at": now,
        "summary": reflection["summary"],
        "lesson": reflection["lesson"],
        "outcomes": outcomes,
        "procedure_version": procedure_version,
        "customer_present": customer_present,
        "expires_at": episode_expires_at(now),
        "text": f"{opening}: {reflection['summary']} Case outcomes: {outcome_text}. Lesson: {reflection['lesson']}",
    }
