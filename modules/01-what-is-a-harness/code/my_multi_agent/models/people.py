"""People cluster: employee master data and the pay policy."""

from sqlalchemy import REAL, CheckConstraint, ForeignKey, Index, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Employee(Base):
    __tablename__ = "employees"
    __table_args__ = (
        CheckConstraint("salary > 0", name="salary_positive"),
        CheckConstraint("status IN ('active', 'terminated')", name="status_allowed"),
        CheckConstraint(
            "end_reason IN ('resignation', 'layoff', 'performance', 'retirement', 'other')",
            name="end_reason_allowed",
        ),
        # end_date and end_reason are set if and only if the employee is terminated.
        CheckConstraint("(status = 'terminated') = (end_date IS NOT NULL)", name="end_date_iff_terminated"),
        CheckConstraint("(status = 'terminated') = (end_reason IS NOT NULL)", name="end_reason_iff_terminated"),
        Index("idx_employees_city", "city_id"),
        Index("idx_employees_company", "company_id"),
        Index("idx_employees_profession", "profession"),
    )

    emp_id: Mapped[int] = mapped_column(Integer, primary_key=True, default=None)
    emp_name: Mapped[str] = mapped_column(Text)
    salary: Mapped[float] = mapped_column(REAL)
    state_id: Mapped[int] = mapped_column(ForeignKey("states.state_id"))
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.city_id"))
    profession: Mapped[str] = mapped_column(Text)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.company_id"))
    status: Mapped[str] = mapped_column(Text, default="active", server_default="active")
    start_date: Mapped[str] = mapped_column(Text)                        # ISO date
    end_date: Mapped[str | None] = mapped_column(Text, default=None)     # ISO date
    end_reason: Mapped[str | None] = mapped_column(Text, default=None)
    end_note: Mapped[str | None] = mapped_column(Text, default=None)     # free text from whoever terminated


class SalaryBand(Base):
    __tablename__ = "salary_bands"
    __table_args__ = (
        CheckConstraint("min_salary > 0 AND min_salary <= max_salary", name="band_ordered"),
    )

    profession: Mapped[str] = mapped_column(Text, primary_key=True)
    min_salary: Mapped[float] = mapped_column(REAL)
    max_salary: Mapped[float] = mapped_column(REAL)
