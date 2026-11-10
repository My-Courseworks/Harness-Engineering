"""IT cluster: equipment and employee-facing requests."""

from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import UTC_NOW_SQL, Base, utc_now


class AssetCategory(Base):
    """The catalogue of kinds of equipment. IT owns it; other domains reference
    category_id, never free text, so "is this the same kind of thing?" is an exact comparison."""

    __tablename__ = "asset_categories"
    __table_args__ = (CheckConstraint("max_per_employee > 0", name="max_per_employee_positive"),)

    category_id: Mapped[int] = mapped_column(Integer, primary_key=True, default=None)
    category_name: Mapped[str] = mapped_column(Text, unique=True)
    max_per_employee: Mapped[int] = mapped_column(Integer)   # policy as data


class Asset(Base):
    __tablename__ = "assets"
    __table_args__ = (
        CheckConstraint("status IN ('in_stock', 'assigned', 'repair', 'retired')", name="status_allowed"),
        CheckConstraint("(status = 'assigned') = (assigned_emp_id IS NOT NULL)", name="assignee_iff_assigned"),
        Index("idx_assets_assignee", "assigned_emp_id"),
        Index("idx_assets_category", "category_id"),
    )

    asset_id: Mapped[int] = mapped_column(Integer, primary_key=True, default=None)
    category_id: Mapped[int] = mapped_column(ForeignKey("asset_categories.category_id"))
    model: Mapped[str] = mapped_column(Text)   # display only; never used for matching
    serial_no: Mapped[str] = mapped_column(Text, unique=True)
    assigned_emp_id: Mapped[int | None] = mapped_column(ForeignKey("employees.emp_id"), default=None)
    status: Mapped[str] = mapped_column(Text, default="in_stock", server_default="in_stock")


class ITTicket(Base):
    __tablename__ = "it_tickets"
    __table_args__ = (
        CheckConstraint("category IN ('account', 'hardware', 'access')", name="category_allowed"),
        CheckConstraint("status IN ('open', 'in_progress', 'closed')", name="status_allowed"),
        # A hardware ticket is about a specific unit; account and access tickets have none.
        CheckConstraint("(category = 'hardware') = (asset_id IS NOT NULL)", name="asset_iff_hardware"),
        Index("idx_it_tickets_emp", "emp_id"),
    )

    ticket_id: Mapped[int] = mapped_column(Integer, primary_key=True, default=None)
    emp_id: Mapped[int] = mapped_column(ForeignKey("employees.emp_id"))
    category: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Text, default="open", server_default="open")
    created_at: Mapped[str] = mapped_column(Text, default_factory=utc_now, server_default=UTC_NOW_SQL)
    asset_id: Mapped[int | None] = mapped_column(ForeignKey("assets.asset_id"), default=None)
