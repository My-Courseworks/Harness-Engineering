# Masking package: planned split of `chat/masking.py`

Status: plan, not yet implemented. `chat/masking.py` is still the live module.
Written 2026-11-10 from the design discussion; update or delete once the split lands.

## Why a package

One file currently holds three concerns: finding internal names and substituting
them, rewriting prose with a model, and the policy object plus the ADK callback
that the rest of the harness talks to. Splitting them makes the dependency
direction explicit and keeps the one public surface small.

## Files and what each houses

### `rewrite.py`
- `ANSWER_REWRITE_INSTRUCTION` (today's `REWRITE_INSTRUCTION`): first person,
  outcomes not process.
- `THINKING_REWRITE_INSTRUCTION` (new): describe what is being looked for and
  what was found, never which internal component does it.
- `response_text(llm_response) -> str`: non-thought text parts, concatenated.
- `thought_text(llm_response) -> str` (new): thought parts, concatenated.
- `rewrite_without_internals(rewriter, text, patterns, instruction) -> str`:
  one-shot model rewrite, recheck for names, fall back to substitution on error,
  empty output or leak. Never raises, never returns empty.

Imports from: `internal_names` (for `has_internal_name`, `substitute_internals`).

### `internal_names.py`
(Originally proposed as `collect_and_substitute_internals.py`; shorter name
describes the subject rather than two verbs.)
- `Kind = Literal["agent", "tool"]`
- `collect_internal_names(agent) -> dict[Kind, set[str]]`: walk the agent tree
  via `canonical_tools()`, classify agent-wrapping tools as agents, keep the two
  sets disjoint.
- `_compile_pattern(names) -> re.Pattern`: whole-word, longest-first, swallows
  article / backticks / call syntax / trailing "tool|agent".
- `compile_name_patterns(names) -> dict[Kind, re.Pattern]`
- `has_internal_name(text, patterns) -> bool`
- `substitute_internals(text, patterns, substitutes) -> str`: deterministic
  floor. `substitutes` comes from config (`labels`), no longer a module constant.

Imports from: nothing inside the package.

### `masking_policy.py`
- `DISPLAY_TEXT_KEY = "harness:display_text"` and
  `DISPLAY_THINKING_KEY = "harness:display_thinking"` (private to the feature;
  no other module imports them).
- `MaskingPolicy` (frozen dataclass), two callables:
  - `render: Callable[[str], str]` — applied by every printer to every string
    it draws (answer, thinking, tool-call author/name/args, tool response,
    answer header).
  - `stored_text: Callable[[Event, str], str | None]` — the persisted rewrite
    for `"answer"` or `"thinking"`, if any. Consumers: `turn.py`, `replay.py`.
- `no_masking() -> MaskingPolicy`: `render = passthrough`, `stored_text`
  always `None`. Returned when the kill switch is off or `kinds` is empty.
  `passthrough` lives here, not in `render_chat.py` or `main.py`.
- `build_mask_callback(patterns, substitutes, rewriter) -> AfterModelCallback`:
  on the final (non-partial) response of the root agent, rewrite answer text
  and thought text that contain names, write both keys into `custom_metadata`,
  leave `content` untouched.
- `apply_masking_policy(root_agent, masking_cfg, enabled) -> MaskingPolicy`:
  the feature's single entry point. Decides enablement (kill switch, then
  `kinds`), collects names, compiles patterns for the configured kinds only,
  builds the rewriter via `commons.create_model.create_model()` only if needed,
  **attaches the callback to `root_agent.after_model_callback`**, returns the
  policy. Logs a warning when the kill switch is off.

Imports from: `internal_names`, `rewrite`.

### `__init__.py`
Re-exports only `MaskingPolicy`, `apply_masking_policy`, `no_masking`.
Everything else is package-internal.

## Who calls what (outside the package)

| Caller | Uses |
|---|---|
| `main.py` | `apply_masking_policy(root_agent, config.displays[role].masking, config.features.masking)` → puts the policy on `View` |
| `render_chat.py` | `view.policy.render(text)` in every printer |
| `turn.py` | `view.policy.stored_text(event, "answer" / "thinking")` when closing a segment |
| `replay.py` | same as `turn.py`, on stored events |

No module outside the package imports a key, a pattern, a substitute phrase or
a model.

## Config it reads

```yaml
features:
  masking: true               # kill switch, all roles
display:
  <role>:
    ...show_* flags...
    masking:
      kinds: [agent, tool]    # [] = this role is unmasked
      rewrite_answers: true
labels:
  substitutes:
    agent: "a colleague"
    tool: "an internal tool"
```

## Decisions recorded along the way
- Substitution hides identifiers; only not drawing a surface hides structure.
  A role with `show_thinking: true` and non-empty `kinds` therefore gets
  thinking rewritten, not merely substituted.
- Rewrite applies to model-authored prose (answers, thinking). Tool-call args
  and tool responses get substitution only.
- `content` is never modified; raw text stays for admins and audit.
- Thinking must become a buffered segment (open/append/close) before `render`
  can apply to it; per-delta printing cannot mask split names.
- A single output choke point in `render_chat.py` (one `emit` for plain text,
  one for markdown) is how "every printer renders" becomes structural rather
  than remembered.
