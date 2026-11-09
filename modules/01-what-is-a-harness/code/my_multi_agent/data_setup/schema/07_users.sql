-- Chat users: the people who sit at the ops desk terminal. Deliberately separate from
-- employees, who are the subjects of the data, not its operators. ``role`` decides what
-- the terminal shows them; the allowed values must match the ``display`` keys in config.yml.

CREATE TABLE users (
    user_id    TEXT PRIMARY KEY,                           -- what ADK stores sessions under
    user_name  TEXT NOT NULL UNIQUE,                       -- shown in the picker and the greeting
    role       TEXT NOT NULL CHECK (role IN ('admin', 'user'))
);
