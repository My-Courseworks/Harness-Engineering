"""What kind of session a turn runs in: decided by whoever starts the session and passed in, never read back from state.

Round 3 read "unattended" from session state (`followup_id`). An erasure that ran inside a follow-up's own turn
deleted that state, and the scheduler's message then ran as a live chat, with the full tool set, and wrote a new
transcript and episode. The kind now travels with the job: the scheduler builds it from the follow-up record and
hands it to the agent, and nothing a session stores can change it.
"""

from typing import NamedTuple


class SessionKind(NamedTuple):
    unattended: bool = False      # started by the scheduler; the customer is not in it and cannot reply
    followup: dict | None = None  # the scheduler record it serves (unattended sessions only)
    persist: bool = True          # False: nothing about this session is stored (its record predates an erasure)

    @property
    def label(self) -> str:
        return "unattended" if self.unattended else "live"


LIVE = SessionKind()


def followup_kind(record: dict, persist: bool = True) -> SessionKind:
    return SessionKind(unattended=True, followup=record, persist=persist)
