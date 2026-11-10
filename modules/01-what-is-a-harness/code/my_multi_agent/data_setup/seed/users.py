"""Users cluster: the fixed set of people allowed to sit at the terminal.

Deterministic by construction (no randomness), so it needs nothing from earlier seeders.
Names are chosen outside the employee name pools so a user is never mistaken for an employee.
"""

from __future__ import annotations

from typing import ClassVar

from models import User

from .base import Seeder, SeedContext


class UsersSeeder(Seeder):
    name = "users"
    tables = (User,)

    # (user_id, user_name, role). ``akshay`` keeps the id the app used before users existed,
    # so sessions recorded under it stay reachable.
    _USERS: ClassVar[tuple[tuple[str, str, str], ...]] = (
        ("akshay", "Akshay Prabhakant", "admin"),
        ("nadia.ferreira", "Nadia Ferreira", "admin"),
        ("owen.blackwood", "Owen Blackwood", "admin"),
        ("lena.hartmann", "Lena Hartmann", "user"),
        ("samir.qureshi", "Samir Qureshi", "user"),
        ("joy.mbeki", "Joy Mbeki", "user"),
    )

    def seed(self, ctx: SeedContext) -> None:
        ctx.add_rows(User, ("user_id", "user_name", "role"), self._USERS)
        ctx.publish("user_ids", [user_id for user_id, _, _ in self._USERS])
