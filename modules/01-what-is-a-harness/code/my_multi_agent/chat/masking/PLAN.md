# Masking package

Status: the split of the old `chat/masking.py` into this package is done (2026-11-10).
The "v2, not built" section at the end lists what was designed but deliberately left out.

## What masking does

Non-admin roles must not see internal agent or tool names. Admins see everything.
Three layers share one set of compiled name patterns:

1. **Prevention.** A runner-wide instruction tells the model not to narrate internals.
   In practice this does nearly all the work.
2. **Unit holdback on the live stream.** An answer is cut into units. A unit is printed
   only after it has been checked, and is never redrawn. A unit that names an internal
   is rewritten, trimmed or withheld.
3. **Persistence for replay.** A callback on the root agent stores the same cleaned text
   with the event, so a resumed session shows what the user originally saw.

A unit is one complete line, one whole table, or one fenced code block.

## Files and what each houses

### `utils.py`
Shared types and one helper. Imports nothing from the package.
- `Kind = Literal["agent", "tool"]`
- `CleanUnit = Callable[[str], Awaitable[str | None]]`: text to show, or `None` to withhold.
- `response_text(llm_response) -> str`: non-thought text parts, concatenated.

### `internal_names.py`
Finding the names and asking whether a text contains one.
- `ADK_INJECTED_TOOL_NAMES`: names ADK adds at call time, which the tree walk cannot find.
- `collect_internal_names(agent) -> dict[Kind, set[str]]`: walks the agent tree via
  `canonical_tools()`, classifies agent-wrapping tools as agents, keeps the two sets disjoint.
- `_compile_pattern(names) -> re.Pattern`: whole word, longest first, swallows the
  article, backticks, call syntax and a trailing "tool" or "agent".
- `compile_name_patterns(names) -> dict[Kind, re.Pattern]`
- `has_internal_name(text, patterns) -> bool`

### `units.py`
What a unit is, and the unit operations that need no model.
- `NOTHING_TO_SHOW`: shown when every unit of an answer was withheld.
- `split_units(text, final=False) -> list[str]`: closed units only; the open remainder
  is returned as a last unit when `final=True`.
- `clean_table(unit, patterns) -> str | None`: drops rows that name internals; a table
  left with no data rows is dropped.
- `clean_text(text, clean_unit) -> str`: whole-text form. Every unit cleaned or withheld,
  rejoined, with `NOTHING_TO_SHOW` as the fallback.

### `rewrite.py`
The unit cleaner, and the model call it makes for prose.
- `UNIT_REWRITE_INSTRUCTION`: rewrite one line without internals, keep every fact, or reply `DROP`.
- `build_unit_cleaner(patterns, rewriter) -> CleanUnit`: clean units pass through untouched.
  Otherwise a table goes to `clean_table`, a code block is withheld, and a prose line is
  rewritten by the model and rechecked, and withheld if that fails. Results are cached,
  so the live stream and the callback share one model call per offending unit.

### `masking_policy.py`
The entry point, the callback, and the two constants the rest of the harness reads.
- `DISPLAY_TEXT_KEY = "harness:display_text"`: key in `event.custom_metadata`.
- `MASKED_ROLE_INSTRUCTION`: the prevention text.
- `build_mask_callback(patterns, clean_unit) -> AfterModelCallback`: on a non-partial
  response that names an internal, stores the cleaned text under `DISPLAY_TEXT_KEY`.
  It never modifies `content`.
- `apply_masking(root_agent, user_role, is_masking_enabled) -> CleanUnit | None`: resolves
  the role once. For a masked role it collects names, compiles patterns, builds the
  cleaner, attaches the callback to `root_agent.after_model_callback`, and returns the
  cleaner. For an admin, or with the feature off, it attaches nothing and returns `None`.

There is no `__init__.py`. The folder is a namespace package, like `chat/` itself, and
callers import from the specific module.

## Import direction

`utils` ← `internal_names` ← `units` ← `rewrite` ← `masking_policy`

Each module imports only from those to its left. Nothing in the package imports from
`render_chat.py`, `turn.py` or `replay.py`.

## Who uses what, outside the package

| Caller | Imports | Use |
|---|---|---|
| `main.py` | `apply_masking`, `MASKED_ROLE_INSTRUCTION`, `CleanUnit` | Calls `apply_masking`, puts the result on `View.clean_unit`, and passes the instruction to `build_runtime` for a masked role. |
| `chat/render_chat.py` | `CleanUnit`, `split_units`, `NOTHING_TO_SHOW` | `View.clean_unit` decides live streaming (`None`) or unit holdback. `_release_units` splits, cleans and prints. |
| `chat/turn.py` | `DISPLAY_TEXT_KEY` | Prefers the stored cleaned text when closing the final answer. |
| `chat/replay.py` | `DISPLAY_TEXT_KEY` | Prefers the stored cleaned text when replaying an answer. |
| `chat/runtime.py` | nothing | Receives the instruction as a plain string. |

## Config it reads

```yaml
features:
  masking: true                   # kill switch, all roles
  masked_role_instruction: true   # the prevention layer; off = holdback on its own
```

The role rule is hard-coded for now: every role except `admin` is masked.

## Decisions recorded along the way

- **Withhold or rewrite, never substitute.** The stand-in phrases ("a colleague",
  "an internal tool") were removed. They read awkwardly and still hinted at the structure.
- **Nothing is taken back.** Printing only closed, checked units removed the need to
  redraw, which is what caused duplicated lines with a tall `Live` region.
- **`content` is never modified.** The raw text stays for admins and for audit. The
  cleaned text lives beside it in `custom_metadata`.
- **One cleaner, two callers.** The live stream and the callback use the same cleaner
  and cache, so what is persisted is what was shown.
- **Sub-agent answers are hidden, not cleaned.** The callback sits on the root agent
  only, so `display.<role>.show_subagent_answers` decides whether they are drawn at all.
- **Role resolved in one place.** `apply_masking` is the only function that looks at the
  role for the holdback. Everything downstream receives a function or `None`.

## Known limitations

- **Identifiers only.** The holdback detects names. With the instruction off, the model
  can describe the architecture in plain words and nothing stops it.
- **Thinking is not cleaned.** It is hidden for masked roles through `show_thinking`.
- **Tool-call and tool-response lines are not cleaned.** They are hidden through
  `show_tool_call` and `show_tool_response`.
- **Bullets print as separate blocks.** Each list line is its own unit, so the terminal
  shows a blank line between bullets.
- **The instruction decision sits in `main.py`.** It repeats the role and flag check
  that `apply_masking` already makes.

## v2, not built

Designed in discussion, deliberately deferred. Nothing below exists in code.

- **`MaskingPolicy` on `View`.** A frozen dataclass returned by the entry point, replacing
  the bare `clean_unit`, so consumers stop importing `DISPLAY_TEXT_KEY` and
  `NOTHING_TO_SHOW` directly. `apply_masking` becomes `apply_masking_policy`.
- **Entry point returns the instruction too.** Removes the duplicate check in `main.py`.
- **Per-role masking in config.** A `masking:` block under each `display.<role>`, with
  `kinds` (which name kinds to mask, empty meaning unmasked) and `rewrite_answers`.
  This replaces the hard-coded `admin` check, with roles as an enum.
- **Fallback beyond identifiers.** A vocabulary trigger plus a whole-answer rewrite, for
  when the instruction is beaten and the answer describes the design without naming anything.
- **Thinking for a role that may see it.** Thinking becomes a buffered segment and is
  rewritten, for a role with `show_thinking: true` that is still masked.
- **Progress lines** in place of raw tool-call lines for masked roles.
- **A list as one unit**, to fix the blank lines between bullets.
- **One output choke point in `render_chat.py`**, so that every printer passing through
  the policy is structural instead of remembered.
- **An `__init__.py`** re-exporting the public surface, once that surface is the policy
  alone.
