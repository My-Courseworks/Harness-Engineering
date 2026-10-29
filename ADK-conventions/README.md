# Reference regarding when and how to use state variables
- borrowed from [ADK's docs](https://adk.dev/sessions/state/#a-warning-about-direct-state-modification)

- Avoid directly modifying the `session.state collection` (dictionary/Map) on a Session object that was obtained directly from the SessionService (e.g., via `session_service.get_session()` or `session_service.create_session()`) outside of the managed lifecycle of an agent invocation (i.e., not through a `CallbackContext` or `ToolContext`). 
    - For example, code like `retrieved_session = await session_service.get_session(...)`; `retrieved_session.state['key'] = value` **is problematic**.
- State modifications within callbacks or tools using `CallbackContext.state` or `ToolContext.state` are the correct way to ensure changes are tracked, as these context objects handle the necessary integration with the event system.
- Why direct modification (outside of contexts) is strongly discouraged:
    - **Bypasses Event History**: The change isn't recorded as an Event, losing auditability.
    - **Breaks Persistence**: Changes made this way will likely NOT be saved by DatabaseSessionService or VertexAiSessionService. They rely on append_event to trigger saving.
    - **Not Thread-Safe**: Can lead to race conditions and lost updates.
    - **Ignores Timestamps/Logic**: Doesn't update last_update_time or trigger related event logic.
- **Recommendation**: Stick to updating state via `output_key`(when initializing an agent), `EventActions.state_delta` (when manually creating events), or by modifying the state property of `CallbackContext` or `ToolContext` objects when within their respective scopes. 
    - These methods ensure reliable, trackable, and persistent state management. 
    - Use direct access to `session.state` (from a `SessionService`-retrieved session) only for reading state.