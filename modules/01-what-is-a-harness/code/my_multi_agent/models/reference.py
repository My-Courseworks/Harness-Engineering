"""Shared lookup tables. Everything else points at these ids."""

from sqlalchemy import REAL, CheckConstraint, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class State(Base):
    __tablename__ = "states"

    state_id: Mapped[int] = mapped_column(Integer, primary_key=True, default=None)
    state_name: Mapped[str] = mapped_column(Text, unique=True)


class City(Base):
    __tablename__ = "cities"
    __table_args__ = (
        UniqueConstraint("city_name", "state_id"),
        CheckConstraint("cost_of_living_index > 0", name="cost_of_living_index_positive"),
    )

    city_id: Mapped[int] = mapped_column(Integer, primary_key=True, default=None)
    city_name: Mapped[str] = mapped_column(Text)
    state_id: Mapped[int] = mapped_column(ForeignKey("states.state_id"))
    cost_of_living_index: Mapped[float] = mapped_column(REAL)   # 100 = baseline


class Company(Base):
    __tablename__ = "companies"

    company_id: Mapped[int] = mapped_column(Integer, primary_key=True, default=None)
    company_name: Mapped[str] = mapped_column(Text, unique=True)
    industry: Mapped[str] = mapped_column(Text)
