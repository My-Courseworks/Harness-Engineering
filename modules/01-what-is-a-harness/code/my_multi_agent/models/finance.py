"""Finance cluster: what employees spend, the per-claim caps, and the audit trail.

Policy is code, not data: the rules that gate a claim live in the Finance tools.
Only reference values (the caps here, AssetCategory.max_per_employee) are stored.
"""

from sqlalchemy import REAL, CheckConstraint, ForeignKey, Index, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import UTC_NOW_SQL, Base, utc_now


class ExpenseLimit(Base):
    __tablename__ = "expense_limits"
    __table_args__ = (CheckConstraint("max_amount > 0", name="max_amount_positive"),)

    category: Mapped[str] = mapped_column(Text, primary_key=True)   # travel | meals | equipment | training
    max_amount: Mapped[float] = mapped_column(REAL)                 # per-claim cap


class ExpenseClaim(Base):
    __tablename__ = "expense_claims"
    __table_args__ = (
        CheckConstraint("amount > 0", name="amount_positive"),
        CheckConstraint(
            "status IN ('submitted', 'needs_review', 'approved', 'rejected', 'paid')", name="status_allowed"
        ),
        # Equipment claims name the KIND of asset by catalogue id; every other category leaves it NULL.
        CheckConstraint(
            "(category = 'equipment') = (asset_category_id IS NOT NULL)", name="asset_category_iff_equipment"
        ),
        CheckConstraint("category = 'equipment' OR asset_id IS NULL", name="asset_only_for_equipment"),
        Index("idx_expense_claims_emp", "emp_id"),
    )

    claim_id: Mapped[int] = mapped_column(Integer, primary_key=True, default=None)
    emp_id: Mapped[int] = mapped_column(ForeignKey("employees.emp_id"))
    amount: Mapped[float] = mapped_column(REAL)
    category: Mapped[str] = mapped_column(ForeignKey("expense_limits.category"))
    asset_category_id: Mapped[int | None] = mapped_column(
        ForeignKey("asset_categories.category_id"), default=None
    )
    # The specific unit, for claims about an existing asset (a repair, an accessory). Purchases of
    # new equipment have no unit yet. The tool checks the unit's category matches asset_category_id.
    asset_id: Mapped[int | None] = mapped_column(ForeignKey("assets.asset_id"), default=None)
    description: Mapped[str | None] = mapped_column(Text, default=None)
    status: Mapped[str] = mapped_column(Text, default="submitted", server_default="submitted")
    submitted_at: Mapped[str] = mapped_column(Text, default_factory=utc_now, server_default=UTC_NOW_SQL)


class ClaimCheck(Base):
    """Audit trail: which code-defined rule ran against which claim, and what it found. Starts empty."""

    __tablename__ = "claim_checks"
    __table_args__ = (
        CheckConstraint("result IN ('pass', 'fail', 'pending')", name="result_allowed"),
        Index("idx_claim_checks_claim", "claim_id"),
    )

    check_id: Mapped[int] = mapped_column(Integer, primary_key=True, default=None)
    claim_id: Mapped[int] = mapped_column(ForeignKey("expense_claims.claim_id"))
    rule_name: Mapped[str] = mapped_column(Text)
    result: Mapped[str] = mapped_column(Text)
    details: Mapped[str | None] = mapped_column(Text, default=None)
    checked_at: Mapped[str] = mapped_column(Text, default_factory=utc_now, server_default=UTC_NOW_SQL)
