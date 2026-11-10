"""The data model: one module per domain, every class re-exported here.

Importing this package registers every table on ``Base.metadata``, which is
what Alembic and the seeders rely on.
"""

from .base import Base
from .finance import ClaimCheck, ExpenseClaim, ExpenseLimit
from .it import Asset, AssetCategory, ITTicket
from .orchestrator import Notification
from .people import Employee, SalaryBand
from .reference import City, Company, State
from .scheduling import LeaveBalance, LeaveRequest, Room, RoomBooking
from .users import User

__all__ = [
    "Base",
    "State", "City", "Company",
    "Employee", "SalaryBand",
    "LeaveBalance", "LeaveRequest", "Room", "RoomBooking",
    "AssetCategory", "Asset", "ITTicket",
    "ExpenseLimit", "ExpenseClaim", "ClaimCheck",
    "Notification",
    "User",
]
