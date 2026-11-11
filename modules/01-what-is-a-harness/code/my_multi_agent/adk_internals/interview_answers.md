# Interview answers: ADK in this app

**What this file is for:** questions an interviewer could ask about how this multi-agent app uses ADK, each answered in bullets short enough to say aloud.

**What it is not for:** design history, alternatives we rejected, or setup steps. Those live elsewhere, for example in `chat/masking/PLAN.md` and in the docstrings of `tools/pagination.py`. An answer here says what the app does today and how that was checked. When the code changes, the answer changes with it.

One section per question. Newest at the bottom.

---

## How does the model use what a tool stored in session state?

Asked as: "Your tools write to state. How does the model then know when, what and how to fetch the next page?"

- **The model never reads state.** My code turns the stored record into a line of text inside the model's instruction.
- **Write side:** a decorator on every paged tool stores two things in session state after each call, per tool and per set of filters: the filters, and the next page number.
- **Read side:** every agent's instruction is a function, and ADK calls it again before each model call. For the people agent, that function also reads state and appends a note such as `_list_employee_names, filters {}: next_page is 5`. The other agents have no paged tools, so theirs appends nothing.
- **The model's part:** it reads the note and the tool's docstring, then calls that tool with page 5. It copies the number. It never calculates one.
- **Why state is needed at all:** sub-agents run in task mode. Once one finishes its task, its next run starts with no memory of its last tool result.
- **Proof:** I gave a session an empty conversation, with state saying page 4 had been read, and sent only "next page". With the note, the real model asked for page 5 in 5 of 5 runs. Without it, 0 of 5: three guessed page 2, two said they had no context.
- **The honest limit:** state is one of three memories. The orchestrator's own conversation history and an unfinished sub-agent task can also carry the page number, and usually do. State is the backstop for when both are missing.
- **The ADK detail behind it:** `{key}` placeholders are only filled in for plain-text instructions. Mine come from a function, so the function has to read state itself.

Where it lives: the decorator and the note are in `tools/pagination.py`, the instruction function is in `commons/build_agent_texts.py`, and the wiring is in `agents/people/agent.py`.

---

## How does a task-mode sub-agent hand control back to the orchestrator?

Asked as: "Your sub-agents run with `mode="task"`. What does that do, and what can go wrong?"

- **Delegation is a tool call.** ADK wraps each task-mode sub-agent as a tool on the orchestrator. Calling it opens a task, identified by that call's id.
- **There is one exit.** ADK adds a `finish_task` tool to the sub-agent, taking one `result` string. A successful call closes the task, and `result` returns to the orchestrator as the answer to its tool call.
- **An open task owns the conversation.** Before each user message, the runner looks for an open task and delivers the message to that sub-agent. The orchestrator's model is not called.
- **So handing back is the sub-agent model's decision alone.** No code, mine or ADK's, forces it.
- **ADK pushes the model to stay.** It appends this to every task agent's instruction: "Do NOT call `finish_task` prematurely. Use your available tools to fully complete every aspect of the delegated task first. If the task is unclear, ask the user for clarification before proceeding. Once the task is fully complete, call `finish_task` by itself with no accompanying text output."
- **Two consequences of that text:** an agent that writes its answer as text has not finished, and an agent asked for something outside its tools is told nothing about leaving.
- **Seen in a real chat:** I asked the people agent about an employee, then said "her leave has been approved, tell her". The notify tool belongs to the orchestrator. The people agent kept the conversation for two more turns, said it had no such tool, and drafted emails instead.
- **The trade-off:** task mode is what lets a sub-agent ask the user a question directly, such as "which Olivia?". The same ability is what lets it hold on.
- **What I added:** one shared text, appended to every task agent's instruction. Text is only for asking the user something. A request no tool can serve counts as complete and is passed back in `result`. `result` reports only what the agent's tools did.
- **Proof:** I replayed that three-message chat on `gpt-4.1-mini`, three runs each way. Before, no run reached the notify tool, and one run reported "has been informed" when nothing was sent. After, all three notified the right employee. DeepSeek, tested only after, also did in three of three.
- **A caveat on that proof:** those runs had one more rule, since removed: put the answer in `result`, not in text. Without it the chat still worked when tried by hand, but the three-run replay was not repeated.
- **One more ADK detail:** the orchestrator never sees a user message that was sent while a task was open. `result` is the only thing that crosses back.
- **The honest limit:** when the out-of-tools request arrives while the task is still open, `gpt-4.1-mini` now hands control back, but in three of three runs its `result` did not carry the request, so nothing was sent.
- **The cost:** every sub-agent answer is now restated by the orchestrator, which is one more model call per turn.

How it was checked: by reading the installed ADK 2.14.0 source, and by replaying scripted chats through the real agents and models against a copy of the database.

Where it lives: the shared text is `agents/task_agent_rules.md`, appended by `build_instructions(..., with_task_rules=True)` in `commons/build_agent_texts.py`. `mode="task"` is set in each `agents/*/agent.py` except the orchestrator's. In ADK, the tool and the appended instruction are in `agents/llm/task/_finish_task_tool.py`, the routing of user messages is `_find_active_task_scope` in `runners.py`, and the dispatch and the return of `result` are in `workflow/_llm_agent_wrapper.py`.
