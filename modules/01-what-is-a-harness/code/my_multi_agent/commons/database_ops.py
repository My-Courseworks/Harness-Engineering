"""
All database related ops handled by a singular file.
Acts as intermediary between tools that need to perform some DB op and the database
SQLite connection in data_setup/database.py
"""

from pathlib import Path

from datetime import datetime

from data_setup.database import Database
from utils.time_fmt import format_local

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DB_FILE = PROJECT_ROOT / "data_setup" / "generated" / "ops.db"

LOCAL_TZ = datetime.now().astimezone().tzinfo

def _connect():
    # TODO: try-except
    return Database(BACKEND_DB_FILE)

def to_local(value: str) -> str:
    """
    Convert all times to local timezone
    """
    return format_local(value, LOCAL_TZ)

def now_local(date: bool = False) -> str:
    """Current wall-clock time in the local zone."""
    if date:
        return datetime.now().astimezone(LOCAL_TZ).strftime("%Y-%m-%d")
    return datetime.now().astimezone(LOCAL_TZ).strftime("%Y-%m-%d %H:%M %Z")
    

# ----------  NOTIFICATIONS -----------------

def notify_db(emp_id: str, message: str) -> bool:
    """
    """
    with _connect() as db:
        LIST_EMPLOYEES_WITH_GIVEN_EMP_ID_QUERY = """
select emp_name, status
from employees
where emp_id = ? 
"""
        emp_record = db.fetch_all(LIST_EMPLOYEES_WITH_GIVEN_EMP_ID_QUERY, (emp_id,))
        if not emp_record:
            return False
        db.insert_many(
            table = 'notifications',
            columns=['emp_id', 'message'],
            rows = [
                (emp_id, message)
            ]
        )
        return True

def list_notifications_db(emp_id: str):
    """
    List notifications of an employee.
    TODO: This will be deprecated once employee sign in is figured out
    """
    LIST_NOTIFICATIONS_QUERY = f"""
SELECT *
FROM notifications
WHERE emp_id = {emp_id}
ORDER BY created_at
"""
    with _connect() as db:
        rows = db.fetch_all(LIST_NOTIFICATIONS_QUERY)
        return [dict(r) for r in rows]

# -----------   EMPLOYEES   ------------------

def list_employees_from_db():
    """
    """
    with _connect() as db:
        rows = db.fetch_all(
            """
            SELECT e.emp_id, e.emp_name
            FROM employees AS e
            ORDER BY e.emp_id
            """,
        )
    return [dict(r) for r in rows]

# ----------  LIST CHAT USERS. -------------------
def list_chat_users():
    """
    """
    with _connect() as db:
        rows = db.fetch_all(
            """
            SELECT * FROM users
            """
        )
        return [dict(r) for r in rows]