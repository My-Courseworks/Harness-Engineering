"""baseline schema

Revision ID: 710539c55c19
Revises: 
Create Date: 2026-11-10 19:44:08.080026

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '710539c55c19'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create every table. Generated from the models and reviewed; this is the first
    link of the chain, so a database built from empty always starts here."""
    op.create_table('asset_categories',
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('category_name', sa.Text(), nullable=False),
    sa.Column('max_per_employee', sa.Integer(), nullable=False),
    sa.CheckConstraint('max_per_employee > 0', name=op.f('ck_asset_categories_max_per_employee_positive')),
    sa.PrimaryKeyConstraint('category_id', name=op.f('pk_asset_categories')),
    sa.UniqueConstraint('category_name', name=op.f('uq_asset_categories_category_name'))
    )
    op.create_table('companies',
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('company_name', sa.Text(), nullable=False),
    sa.Column('industry', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('company_id', name=op.f('pk_companies')),
    sa.UniqueConstraint('company_name', name=op.f('uq_companies_company_name'))
    )
    op.create_table('expense_limits',
    sa.Column('category', sa.Text(), nullable=False),
    sa.Column('max_amount', sa.REAL(), nullable=False),
    sa.CheckConstraint('max_amount > 0', name=op.f('ck_expense_limits_max_amount_positive')),
    sa.PrimaryKeyConstraint('category', name=op.f('pk_expense_limits'))
    )
    op.create_table('rooms',
    sa.Column('room_id', sa.Integer(), nullable=False),
    sa.Column('room_name', sa.Text(), nullable=False),
    sa.Column('capacity', sa.Integer(), nullable=False),
    sa.Column('floor', sa.Integer(), nullable=False),
    sa.CheckConstraint('capacity > 0', name=op.f('ck_rooms_capacity_positive')),
    sa.PrimaryKeyConstraint('room_id', name=op.f('pk_rooms')),
    sa.UniqueConstraint('room_name', name=op.f('uq_rooms_room_name'))
    )
    op.create_table('salary_bands',
    sa.Column('profession', sa.Text(), nullable=False),
    sa.Column('min_salary', sa.REAL(), nullable=False),
    sa.Column('max_salary', sa.REAL(), nullable=False),
    sa.CheckConstraint('min_salary > 0 AND min_salary <= max_salary', name=op.f('ck_salary_bands_band_ordered')),
    sa.PrimaryKeyConstraint('profession', name=op.f('pk_salary_bands'))
    )
    op.create_table('states',
    sa.Column('state_id', sa.Integer(), nullable=False),
    sa.Column('state_name', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('state_id', name=op.f('pk_states')),
    sa.UniqueConstraint('state_name', name=op.f('uq_states_state_name'))
    )
    op.create_table('users',
    sa.Column('user_id', sa.Text(), nullable=False),
    sa.Column('user_name', sa.Text(), nullable=False),
    sa.Column('role', sa.Text(), nullable=False),
    sa.CheckConstraint("role IN ('admin', 'user')", name=op.f('ck_users_role_allowed')),
    sa.PrimaryKeyConstraint('user_id', name=op.f('pk_users')),
    sa.UniqueConstraint('user_name', name=op.f('uq_users_user_name'))
    )
    op.create_table('cities',
    sa.Column('city_id', sa.Integer(), nullable=False),
    sa.Column('city_name', sa.Text(), nullable=False),
    sa.Column('state_id', sa.Integer(), nullable=False),
    sa.Column('cost_of_living_index', sa.REAL(), nullable=False),
    sa.CheckConstraint('cost_of_living_index > 0', name=op.f('ck_cities_cost_of_living_index_positive')),
    sa.ForeignKeyConstraint(['state_id'], ['states.state_id'], name=op.f('fk_cities_state_id_states')),
    sa.PrimaryKeyConstraint('city_id', name=op.f('pk_cities')),
    sa.UniqueConstraint('city_name', 'state_id', name=op.f('uq_cities_city_name'))
    )
    op.create_table('employees',
    sa.Column('emp_id', sa.Integer(), nullable=False),
    sa.Column('emp_name', sa.Text(), nullable=False),
    sa.Column('salary', sa.REAL(), nullable=False),
    sa.Column('state_id', sa.Integer(), nullable=False),
    sa.Column('city_id', sa.Integer(), nullable=False),
    sa.Column('profession', sa.Text(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Text(), server_default='active', nullable=False),
    sa.Column('start_date', sa.Text(), nullable=False),
    sa.Column('end_date', sa.Text(), nullable=True),
    sa.Column('end_reason', sa.Text(), nullable=True),
    sa.Column('end_note', sa.Text(), nullable=True),
    sa.CheckConstraint("(status = 'terminated') = (end_date IS NOT NULL)", name=op.f('ck_employees_end_date_iff_terminated')),
    sa.CheckConstraint("(status = 'terminated') = (end_reason IS NOT NULL)", name=op.f('ck_employees_end_reason_iff_terminated')),
    sa.CheckConstraint("end_reason IN ('resignation', 'layoff', 'performance', 'retirement', 'other')", name=op.f('ck_employees_end_reason_allowed')),
    sa.CheckConstraint("status IN ('active', 'terminated')", name=op.f('ck_employees_status_allowed')),
    sa.CheckConstraint('salary > 0', name=op.f('ck_employees_salary_positive')),
    sa.ForeignKeyConstraint(['city_id'], ['cities.city_id'], name=op.f('fk_employees_city_id_cities')),
    sa.ForeignKeyConstraint(['company_id'], ['companies.company_id'], name=op.f('fk_employees_company_id_companies')),
    sa.ForeignKeyConstraint(['state_id'], ['states.state_id'], name=op.f('fk_employees_state_id_states')),
    sa.PrimaryKeyConstraint('emp_id', name=op.f('pk_employees'))
    )
    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.create_index('idx_employees_city', ['city_id'], unique=False)
        batch_op.create_index('idx_employees_company', ['company_id'], unique=False)
        batch_op.create_index('idx_employees_profession', ['profession'], unique=False)

    op.create_table('assets',
    sa.Column('asset_id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('model', sa.Text(), nullable=False),
    sa.Column('serial_no', sa.Text(), nullable=False),
    sa.Column('assigned_emp_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.Text(), server_default='in_stock', nullable=False),
    sa.CheckConstraint("(status = 'assigned') = (assigned_emp_id IS NOT NULL)", name=op.f('ck_assets_assignee_iff_assigned')),
    sa.CheckConstraint("status IN ('in_stock', 'assigned', 'repair', 'retired')", name=op.f('ck_assets_status_allowed')),
    sa.ForeignKeyConstraint(['assigned_emp_id'], ['employees.emp_id'], name=op.f('fk_assets_assigned_emp_id_employees')),
    sa.ForeignKeyConstraint(['category_id'], ['asset_categories.category_id'], name=op.f('fk_assets_category_id_asset_categories')),
    sa.PrimaryKeyConstraint('asset_id', name=op.f('pk_assets')),
    sa.UniqueConstraint('serial_no', name=op.f('uq_assets_serial_no'))
    )
    with op.batch_alter_table('assets', schema=None) as batch_op:
        batch_op.create_index('idx_assets_assignee', ['assigned_emp_id'], unique=False)
        batch_op.create_index('idx_assets_category', ['category_id'], unique=False)

    op.create_table('leave_balances',
    sa.Column('emp_id', sa.Integer(), nullable=False),
    sa.Column('leave_type', sa.Text(), nullable=False),
    sa.Column('days_left', sa.REAL(), nullable=False),
    sa.CheckConstraint("leave_type IN ('annual', 'sick', 'personal')", name=op.f('ck_leave_balances_leave_type_allowed')),
    sa.CheckConstraint('days_left >= 0', name=op.f('ck_leave_balances_days_left_non_negative')),
    sa.ForeignKeyConstraint(['emp_id'], ['employees.emp_id'], name=op.f('fk_leave_balances_emp_id_employees')),
    sa.PrimaryKeyConstraint('emp_id', 'leave_type', name=op.f('pk_leave_balances'))
    )
    op.create_table('leave_requests',
    sa.Column('request_id', sa.Integer(), nullable=False),
    sa.Column('emp_id', sa.Integer(), nullable=False),
    sa.Column('leave_type', sa.Text(), nullable=False),
    sa.Column('start_date', sa.Text(), nullable=False),
    sa.Column('end_date', sa.Text(), nullable=False),
    sa.Column('days', sa.REAL(), nullable=False),
    sa.Column('status', sa.Text(), server_default='pending', nullable=False),
    sa.CheckConstraint("leave_type IN ('annual', 'sick', 'personal')", name=op.f('ck_leave_requests_leave_type_allowed')),
    sa.CheckConstraint("status IN ('pending', 'approved', 'rejected', 'cancelled')", name=op.f('ck_leave_requests_status_allowed')),
    sa.CheckConstraint('days > 0', name=op.f('ck_leave_requests_days_positive')),
    sa.CheckConstraint('end_date >= start_date', name=op.f('ck_leave_requests_dates_ordered')),
    sa.ForeignKeyConstraint(['emp_id'], ['employees.emp_id'], name=op.f('fk_leave_requests_emp_id_employees')),
    sa.PrimaryKeyConstraint('request_id', name=op.f('pk_leave_requests'))
    )
    with op.batch_alter_table('leave_requests', schema=None) as batch_op:
        batch_op.create_index('idx_leave_requests_emp', ['emp_id'], unique=False)

    op.create_table('notifications',
    sa.Column('notification_id', sa.Integer(), nullable=False),
    sa.Column('emp_id', sa.Integer(), nullable=False),
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('created_at', sa.Text(), server_default=sa.text("(strftime('%Y-%m-%dT%H:%M','now') || 'Z')"), nullable=False),
    sa.ForeignKeyConstraint(['emp_id'], ['employees.emp_id'], name=op.f('fk_notifications_emp_id_employees')),
    sa.PrimaryKeyConstraint('notification_id', name=op.f('pk_notifications'))
    )
    op.create_table('room_bookings',
    sa.Column('booking_id', sa.Integer(), nullable=False),
    sa.Column('room_id', sa.Integer(), nullable=False),
    sa.Column('booked_by', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.Text(), nullable=False),
    sa.Column('end_time', sa.Text(), nullable=False),
    sa.Column('status', sa.Text(), server_default='active', nullable=False),
    sa.CheckConstraint("status IN ('active', 'cancelled')", name=op.f('ck_room_bookings_status_allowed')),
    sa.CheckConstraint('end_time > start_time', name=op.f('ck_room_bookings_times_ordered')),
    sa.ForeignKeyConstraint(['booked_by'], ['employees.emp_id'], name=op.f('fk_room_bookings_booked_by_employees')),
    sa.ForeignKeyConstraint(['room_id'], ['rooms.room_id'], name=op.f('fk_room_bookings_room_id_rooms')),
    sa.PrimaryKeyConstraint('booking_id', name=op.f('pk_room_bookings'))
    )
    with op.batch_alter_table('room_bookings', schema=None) as batch_op:
        batch_op.create_index('idx_room_bookings_room_time', ['room_id', 'start_time'], unique=False)

    op.create_table('expense_claims',
    sa.Column('claim_id', sa.Integer(), nullable=False),
    sa.Column('emp_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.REAL(), nullable=False),
    sa.Column('category', sa.Text(), nullable=False),
    sa.Column('asset_category_id', sa.Integer(), nullable=True),
    sa.Column('asset_id', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('status', sa.Text(), server_default='submitted', nullable=False),
    sa.Column('submitted_at', sa.Text(), server_default=sa.text("(strftime('%Y-%m-%dT%H:%M','now') || 'Z')"), nullable=False),
    sa.CheckConstraint("(category = 'equipment') = (asset_category_id IS NOT NULL)", name=op.f('ck_expense_claims_asset_category_iff_equipment')),
    sa.CheckConstraint("category = 'equipment' OR asset_id IS NULL", name=op.f('ck_expense_claims_asset_only_for_equipment')),
    sa.CheckConstraint("status IN ('submitted', 'needs_review', 'approved', 'rejected', 'paid')", name=op.f('ck_expense_claims_status_allowed')),
    sa.CheckConstraint('amount > 0', name=op.f('ck_expense_claims_amount_positive')),
    sa.ForeignKeyConstraint(['asset_category_id'], ['asset_categories.category_id'], name=op.f('fk_expense_claims_asset_category_id_asset_categories')),
    sa.ForeignKeyConstraint(['asset_id'], ['assets.asset_id'], name=op.f('fk_expense_claims_asset_id_assets')),
    sa.ForeignKeyConstraint(['category'], ['expense_limits.category'], name=op.f('fk_expense_claims_category_expense_limits')),
    sa.ForeignKeyConstraint(['emp_id'], ['employees.emp_id'], name=op.f('fk_expense_claims_emp_id_employees')),
    sa.PrimaryKeyConstraint('claim_id', name=op.f('pk_expense_claims'))
    )
    with op.batch_alter_table('expense_claims', schema=None) as batch_op:
        batch_op.create_index('idx_expense_claims_emp', ['emp_id'], unique=False)

    op.create_table('it_tickets',
    sa.Column('ticket_id', sa.Integer(), nullable=False),
    sa.Column('emp_id', sa.Integer(), nullable=False),
    sa.Column('category', sa.Text(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('status', sa.Text(), server_default='open', nullable=False),
    sa.Column('created_at', sa.Text(), server_default=sa.text("(strftime('%Y-%m-%dT%H:%M','now') || 'Z')"), nullable=False),
    sa.Column('asset_id', sa.Integer(), nullable=True),
    sa.CheckConstraint("(category = 'hardware') = (asset_id IS NOT NULL)", name=op.f('ck_it_tickets_asset_iff_hardware')),
    sa.CheckConstraint("category IN ('account', 'hardware', 'access')", name=op.f('ck_it_tickets_category_allowed')),
    sa.CheckConstraint("status IN ('open', 'in_progress', 'closed')", name=op.f('ck_it_tickets_status_allowed')),
    sa.ForeignKeyConstraint(['asset_id'], ['assets.asset_id'], name=op.f('fk_it_tickets_asset_id_assets')),
    sa.ForeignKeyConstraint(['emp_id'], ['employees.emp_id'], name=op.f('fk_it_tickets_emp_id_employees')),
    sa.PrimaryKeyConstraint('ticket_id', name=op.f('pk_it_tickets'))
    )
    with op.batch_alter_table('it_tickets', schema=None) as batch_op:
        batch_op.create_index('idx_it_tickets_emp', ['emp_id'], unique=False)

    op.create_table('claim_checks',
    sa.Column('check_id', sa.Integer(), nullable=False),
    sa.Column('claim_id', sa.Integer(), nullable=False),
    sa.Column('rule_name', sa.Text(), nullable=False),
    sa.Column('result', sa.Text(), nullable=False),
    sa.Column('details', sa.Text(), nullable=True),
    sa.Column('checked_at', sa.Text(), server_default=sa.text("(strftime('%Y-%m-%dT%H:%M','now') || 'Z')"), nullable=False),
    sa.CheckConstraint("result IN ('pass', 'fail', 'pending')", name=op.f('ck_claim_checks_result_allowed')),
    sa.ForeignKeyConstraint(['claim_id'], ['expense_claims.claim_id'], name=op.f('fk_claim_checks_claim_id_expense_claims')),
    sa.PrimaryKeyConstraint('check_id', name=op.f('pk_claim_checks'))
    )
    with op.batch_alter_table('claim_checks', schema=None) as batch_op:
        batch_op.create_index('idx_claim_checks_claim', ['claim_id'], unique=False)



def downgrade() -> None:
    """Drop every table."""
    with op.batch_alter_table('claim_checks', schema=None) as batch_op:
        batch_op.drop_index('idx_claim_checks_claim')

    op.drop_table('claim_checks')
    with op.batch_alter_table('it_tickets', schema=None) as batch_op:
        batch_op.drop_index('idx_it_tickets_emp')

    op.drop_table('it_tickets')
    with op.batch_alter_table('expense_claims', schema=None) as batch_op:
        batch_op.drop_index('idx_expense_claims_emp')

    op.drop_table('expense_claims')
    with op.batch_alter_table('room_bookings', schema=None) as batch_op:
        batch_op.drop_index('idx_room_bookings_room_time')

    op.drop_table('room_bookings')
    op.drop_table('notifications')
    with op.batch_alter_table('leave_requests', schema=None) as batch_op:
        batch_op.drop_index('idx_leave_requests_emp')

    op.drop_table('leave_requests')
    op.drop_table('leave_balances')
    with op.batch_alter_table('assets', schema=None) as batch_op:
        batch_op.drop_index('idx_assets_category')
        batch_op.drop_index('idx_assets_assignee')

    op.drop_table('assets')
    with op.batch_alter_table('employees', schema=None) as batch_op:
        batch_op.drop_index('idx_employees_profession')
        batch_op.drop_index('idx_employees_company')
        batch_op.drop_index('idx_employees_city')

    op.drop_table('employees')
    op.drop_table('cities')
    op.drop_table('users')
    op.drop_table('states')
    op.drop_table('salary_bands')
    op.drop_table('rooms')
    op.drop_table('expense_limits')
    op.drop_table('companies')
    op.drop_table('asset_categories')
