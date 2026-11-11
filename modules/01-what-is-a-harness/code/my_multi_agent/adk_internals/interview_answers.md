# Interview answers: ADK in this app

**What this file is for:** questions an interviewer could ask about how this multi-agent app uses ADK, each answered in bullets short enough to say aloud.

**What it is not for:** design history, alternatives we rejected, or setup steps. Those live elsewhere, for example in `paginated_read.md` and `chat/masking/PLAN.md`. An answer here says what the app does today and how that was checked. When the code changes, the answer changes with it.

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
