"""Scheduling cluster: reservations of a person's time (leave) and a room's time (bookings)."""

from sqlalchemy import REAL, CheckConstraint, ForeignKey, Index, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

_LEAVE_TYPES = "leave_type IN ('annual', 'sick', 'personal')"


class LeaveBalance(Base):
    __tablename__ = "leave_balances"
    __table_args__ = (
        CheckConstraint(_LEAVE_TYPES, name="leave_type_allowed"),
        CheckConstraint("days_left >= 0", name="days_left_non_negative"),
    )

    emp_id: Mapped[int] = mapped_column(ForeignKey("employees.emp_id"), primary_key=True)
    leave_type: Mapped[str] = mapped_column(Text, primary_key=True)
    days_left: Mapped[float] = mapped_column(REAL)


class LeaveRequest(Base):
    __tablename__ = "leave_requests"
    __table_args__ = (
        CheckConstraint(_LEAVE_TYPES, name="leave_type_allowed"),
        CheckConstraint("days > 0", name="days_positive"),
        CheckConstraint("status IN ('pending', 'approved', 'rejected', 'cancelled')", name="status_allowed"),
        CheckConstraint("end_date >= start_date", name="dates_ordered"),
        Index("idx_leave_requests_emp", "emp_id"),
    )

    request_id: Mapped[int] = mapped_column(Integer, primary_key=True, default=None)
    emp_id: Mapped[int] = mapped_column(ForeignKey("employees.emp_id"))
    leave_type: Mapped[str] = mapped_column(Text)
    start_date: Mapped[str] = mapped_column(Text)   # ISO date
    end_date: Mapped[str] = mapped_column(Text)     # ISO date, inclusive
    days: Mapped[float] = mapped_column(REAL)
    status: Mapped[str] = mapped_column(Text, default="pending", server_default="pending")


class Room(Base):
    __tablename__ = "rooms"
    __table_args__ = (CheckConstraint("capacity > 0", name="capacity_positive"),)

    room_id: Mapped[int] = mapped_column(Integer, primary_key=True, default=None)
    room_name: Mapped[str] = mapped_column(Text, unique=True)
    capacity: Mapped[int] = mapped_column(Integer)
    floor: Mapped[int] = mapped_column(Integer)


class RoomBooking(Base):
    __tablename__ = "room_bookings"
    __table_args__ = (
        CheckConstraint("status IN ('active', 'cancelled')", name="status_allowed"),
        CheckConstraint("end_time > start_time", name="times_ordered"),
        Index("idx_room_bookings_room_time", "room_id", "start_time"),
    )

    booking_id: Mapped[int] = mapped_column(Integer, primary_key=True, default=None)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.room_id"))
    booked_by: Mapped[int] = mapped_column(ForeignKey("employees.emp_id"))
    start_time: Mapped[str] = mapped_column(Text)   # ISO datetime (UTC), minute precision
    end_time: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Text, default="active", server_default="active")
