"""Episodic memory's write path: a finished session becomes one short reflection, not a stored transcript.

Extraction is model-driven (the reflection prompt), so its output is treated as a
candidate: it is redacted again, and the structured outcome next to it comes from
the case system of record, not from the model's paraphrase. The full transcript
stays in the session store (working memory), where it belongs.
"""

import json
import re

from cardcare import world
from cardcare.memory_policy import episode_expires_at, redact_card_secrets

_CASE_ID = re.compile(r"\bC-\d{4}\b")

REFLECTION_PROMPT = """You write the long-term memory entry for one finished conversation between a card issuer's support assistant and a customer.
Return a JSON object with exactly two keys:
  "summary": at most 60 words. What the customer wanted, what was done (with case and transaction ids), anything promised and when, and any preference the customer stated.
  "lesson": one sentence on what the assistant should do differently next time, judged by how the conversation went and by any case outcome in it; or "none".
Use only facts present in the transcript. Never include card numbers or security codes.

Transcript:
{transcript}"""


def format_transcript(turns: list[dict]) -> str:
    """turns: [{"role": "customer" | "assistant" | "tool", "text": str}] in order."""
    return "\n".join(f"{turn['role']}: {turn['text']}" for turn in turns if turn["text"].strip())


def reflection_prompt(turns: list[dict]) -> str:
    return REFLECTION_PROMPT.format(transcript=format_transcript(turns))


def parse_reflection(raw: str) -> dict:
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    try:
        data = json.loads(match.group()) if match else {}
    except json.JSONDecodeError:
        data = {}
    return {
        "summary": redact_card_secrets(str(data.get("summary") or raw.strip())[:600]),
        "lesson": redact_card_secrets(str(data.get("lesson") or "none")[:300]),
    }


def case_outcomes(bank_db, user_id: str, turns: list[dict]) -> list[dict]:
    """Structured outcomes of every case this session touched, read from the case system of record."""
    case_ids = sorted({case_id for turn in turns for case_id in _CASE_ID.findall(turn["text"])})
    return [
        {key: case[key] for key in ("case_id", "txn_id", "reason", "status", "resolution_code", "resolution_note")}
        for case in world.cases_by_id(bank_db, case_ids)
        if case["user_id"] == user_id
    ]


def build_episode(user_id: str, session_id: str, now: str, reflection: dict, outcomes: list[dict], procedure_version: str) -> dict:
    outcome_text = "; ".join(
        f"{o['case_id']} {o['status']}" + (f" ({o['resolution_code']})" if o["resolution_code"] else "") for o in outcomes
    ) or "no case touched"
    return {
        "episode_id": f"E-{session_id}",
        "user_id": user_id,
        "session_id": session_id,
        "at": now,
        "summary": reflection["summary"],
        "lesson": reflection["lesson"],
        "outcomes": outcomes,
        "procedure_version": procedure_version,
        "expires_at": episode_expires_at(now),
        "text": f"Conversation on {now[:10]}: {reflection['summary']} Case outcomes: {outcome_text}. Lesson: {reflection['lesson']}",
    }
