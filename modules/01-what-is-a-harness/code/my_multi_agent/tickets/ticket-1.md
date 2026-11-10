# TICKET-1 · Per-user display preferences via slash commands (`/thinking off`)

| Field | Value |
|---|---|
| Type | Feature |
| Component | chat harness (`main.py`, `chat/render_chat.py`, `commons/config.py`, `commons/database_ops.py`) |
| Priority | Low (not scheduled) |
| Status | Backlog |
| Reporter | Akshay |
| Created | 2026-11-10 |
| Depends on | role-centric config layout (`roles.<role>.display` / `roles.<role>.masking`), not yet implemented |

## Summary

Let a logged-in user change their own presentation preferences at runtime with
slash commands (`/thinking off`, `/tools on`, ...), persist the choice per user,
and apply it in every later session. Preferences may only touch `Display`
fields. Nothing under `masking` is ever overridable this way.

## Background

Today every visibility flag (`show_thinking`, `show_tool_call`,
`show_tool_response`, `show_agent_name`, `show_subagent_answers`,
`show_error_details`) is a per-role default in `config.yml`, resolved once in
`main()` into a frozen `View`. An admin who wants a quieter session has no way
to get one short of editing the operator's config file.

Terminology, so the ticket is precise:

- `styles` / `labels` are **cosmetic** (theming).
- `display` flags are **presentation preferences**, the thinking and tool flags
  specifically being **verbosity**. A preference is something the person is
  allowed to be wrong about.
- `masking` is **policy** (access control over information). A policy is not.

This feature touches preferences only.

## User story

As an admin, I want to type `/thinking off` and stop seeing the thinking stream
for the rest of this session and all future sessions, without asking an
operator to change `config.yml`, so that I can read answers without the noise
when I am not debugging.

## Design (agreed in discussion, 2026-11-10)

Three layers, each answering one question. The effective `Display` is computed
once at `View` construction by merging them, and no printer changes.

| Layer | Question it answers | Owner | Example |
|---|---|---|---|
| Config | What is the default for this role? | operator, git | `roles.admin.display.show_thinking: true` |
| Data | What has this person chosen? | the app, persisted | `nadia.ferreira` turned thinking off |
| Code | Which fields may a person choose at all? | allowlist in the merge function | display flags yes, masking never |

### Merge

```python
def effective_display(default: Display, overrides: dict[str, bool]) -> Display:
    allowed = {k: v for k, v in overrides.items() if k in OVERRIDABLE_DISPLAY_FIELDS}
    return dataclasses.replace(default, **allowed)
```

`OVERRIDABLE_DISPLAY_FIELDS` is the explicit allowlist. Unknown keys are dropped
and logged, never applied.

### Persistence (decision pending, see Open questions)

Option A — ADK `user:`-prefixed session state (`user:display.show_thinking`).
Already persisted in `session.db`, scoped per user across all their sessions,
no new table. Cost: state is model-adjacent (a tool or instruction template
could read/write it). Harmless for a display preference.

Option B — `user_preferences(user_id, key, value)` table in `ops.db` via
`database_ops.py`. Explicit, queryable, not visible to the model. Costs a
schema file, a seeder no-op, and two functions.

Recommendation: start with A, move to B only if a reason appears.

### Command handling

- The input loop in `main()` checks for a leading `/` **before** anything is
  sent to the runner. A slash command is a harness command; it never becomes
  a model turn and is never persisted as a user message.
- Handler writes the override to the data layer, then rebuilds the view with
  `dataclasses.replace(view, display=effective_display(...))`. `View` stays
  frozen; nothing is mutated in place; the next printer call sees the new flags.
- Startup reads the user's overrides after `choose_user()` and before `View`
  is built, so the next session inherits them.

### Commands (initial set)

| Command | Field |
|---|---|
| `/thinking on\|off` | `show_thinking` |
| `/tools on\|off` | `show_tool_call` and `show_tool_response` together |
| `/subagents on\|off` | `show_subagent_answers` |
| `/errors on\|off` | `show_error_details` |
| `/prefs` | print current effective display and which values are overrides |
| `/prefs reset` | delete all overrides for this user |

`/help` lists them. Unknown slash commands print one line and do nothing.

## Scope

In:
- allowlist + merge function
- persistence of per-user overrides (one of the two options)
- slash-command parsing and the six commands above
- startup load of overrides into the initial `View`

Out:
- anything under `masking` (kill switch, kinds, rewrite). Not overridable, by
  construction, not by convention.
- overriding `styles` / `labels` (theming) — separate ticket if ever wanted
- the app writing back into `config.yml`. That file is the operator's and is
  under version control; the program must never edit it.
- a settings UI of any kind

## Acceptance criteria

1. As admin, `/thinking off` hides the thinking header and deltas for the rest
   of the session; `exit`, restart, resume any session as the same user, and
   thinking is still hidden.
2. The same command typed by a different user has no effect on the first user.
3. `/prefs` shows the effective flags and marks which ones are overrides.
4. `/prefs reset` restores the role defaults from `config.yml` immediately and
   persistently.
5. A slash command never appears in the session's event history and never
   reaches the model (verify with `show_tool_call` on: no tool call, no model
   turn, no new event).
6. No command, including a deliberately crafted one such as
   `/masking off` or `/thinking off masking.kinds=[]`, changes any masking
   behaviour. The allowlist test must include a negative case per masking field.
7. A role with `show_thinking: false` in config can turn thinking **on** only
   if that is intended; decide and encode. (See Open questions.)
8. Unknown keys in persisted overrides (for example after a field is renamed)
   are dropped with a logged warning, never crash startup.

## Open questions

- **Persistence option**: A (`user:` state) or B (`ops.db` table)? Default A.
- **Can a preference widen visibility beyond the role default?** `/thinking on`
  for a role whose default is off would reveal thinking to a role the operator
  chose to keep it from. Two defensible answers: (a) overrides may only narrow
  (turn off), never widen; (b) the role's `display` block is the ceiling and a
  separate `overridable: [...]` list per role says what the user may touch.
  (a) is simpler and safe; (b) is more flexible. Decide before implementing.
- Should `/prefs` persist nothing and only display? Yes, as specified.

## Risks

- Overrides persisted under a key that later gets renamed in `Display` →
  silently ignored. Mitigated by AC 8 and by logging.
- If option A is chosen, a tool writing `user:display.*` could flip a
  preference. Acceptable for preferences; this is exactly why masking is not
  in this layer.

## References

- `commons/config.py` — `Display` dataclass
- `chat/render_chat.py` — `View`, printers that read `view.display`
- `main.py` — input loop, `View` construction
- Course notes: M7 (`user:` state scope), M15 (preference vs policy framing)
