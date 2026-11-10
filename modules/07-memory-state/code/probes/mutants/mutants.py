"""Mutants: each puts back one defect, so that the check named for a claim can be shown to fail.

A check that has never failed is a hypothesis. The round-5 review found three of mine that could not fail at all (a
scanner that could not see a month name with an apostrophe year, the same scanner reading msgpack as text, and a
stored-code search that only knew six contiguous digits). `python run_scenario.py --mutant <name> ...` applies one of
these patches to the product in the harness process and, through probes/mutants/sitecustomize.py, in every child process
(the shipped CLI, the shipped tick), then runs the probe; evidence/mutants/ holds one failing run per mutant. Nothing
here is on the product's path.
"""

import re


def door_lets_lists_through() -> None:
    """Round-5 behaviour in miniature: a message with more than one six-digit number, or typed in another conversation,
    is not touched at the door (the marker then appears only where the end-of-turn sweep finds a real code)."""
    from cardcare import world
    original = world.take_code_entry

    def mutant(db_path, user_id, session_id, text, now, max_failures, repeat_of_lost_call=False):
        taken = original(db_path, user_id, session_id, text, now, max_failures, repeat_of_lost_call)
        outcome = (taken["entry"] or {}).get("outcome")
        return {"text": text, "entry": taken["entry"]} if outcome in ("several_numbers", "other_conversation") else taken

    world.take_code_entry = mutant


def a_code_is_six_contiguous_digits() -> None:
    """The definition the round-5 redaction used: "481 975" is then not a typed code to the door."""
    from cardcare import world
    world._CODE_SPAN = re.compile(r"(?<!\d)\d{6}(?!\d)")
    world._SPOKEN_DIGITS = re.compile(r"(?!x)x")


def only_the_forms_the_bank_takes_are_looked_for() -> None:
    """A code written as "481,975" or "4819 75" is then no code to anything: not an entry, and not removed."""
    from cardcare import world
    world._SIX_DIGITS_ANYHOW = re.compile(r"(?!x)x")


def scheduler_finishes_every_erasure() -> None:
    """The round-5 scheduler: every pending erasure is finished before firing, whether or not anything is due."""
    from cardcare import scheduler, world
    scheduler.customers_with_due_records = lambda db_path, now: {customer[0] for customer in world.CUSTOMERS}


def no_cap_on_codes() -> None:
    from cardcare import world
    world.MAX_CODES_PER_DAY = 10 ** 6


def the_lock_is_not_said() -> None:
    """The third wrong entry reports a wrong code and nothing else."""
    from cardcare import world
    original = world.attempt_code

    def mutant(*args, **kwargs):
        return {key: value for key, value in original(*args, **kwargs).items() if key != "account_locked"}

    world.attempt_code = mutant


def a_role_keeps_its_group() -> None:
    """The round-5 masker: a date, an identifier or an amount keeps the group it took from a card number."""
    from cardcare import masking
    masking._release_card_groups = lambda tokens, text: None


def list_numerals_are_card_digits() -> None:
    """Neither rule for a list's own numerals: not the count (bare numerals), not the list-marker role ("3. …")."""
    from cardcare import masking
    masking._counts_up = lambda tokens: False
    masking._classify_list_markers = lambda tokens, text: None


MUTANTS = {fn.__name__.replace("_", "-"): fn for fn in (door_lets_lists_through, a_code_is_six_contiguous_digits,
                                                        only_the_forms_the_bank_takes_are_looked_for, scheduler_finishes_every_erasure,
                                                        no_cap_on_codes, the_lock_is_not_said, a_role_keeps_its_group, list_numerals_are_card_digits)}
